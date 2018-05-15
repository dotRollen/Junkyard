""" Implements functions for Dell-specific interaction

    Requirements:
        * You must have RACADM installed on the Management Node this is being used on

    Todo:
        * Add local RACADM support using ssh/psh(xCAT) if iDRAC is not reachable
        * Add journal checks for job status
        * Add more specific error/return checks
"""

import os
import subprocess

FNULL = open(os.devnull, 'w')

def set_bios(node, file_path):
    """ Sets BIOS settings for Big Data nodes using racadm for xml import """
    
    racadm_power(node, 'off')

    cmd = "set -f {} -t xml -b Forced ".format(file_path)
    result = racadm_call(node, cmd)
    
    if result and "Import configuration XML file operation initiated" in result:
        return "[{}] Start BIOS Import: Success".format(node)
    else:
        return "[{}] Start BIOS Import: Failed".format(node)

def racadm_update(node, project):
    """ Updates the specified Big Data node """
    
    racadm_power(node, 'off')

    cmd = "update -f Catalog.xml -e '10.2.255.252/{}' -t TFTP -a TRUE".format(project)
    result = racadm_call(node, cmd)
     
    if result and "Update from repository operation has been initiated" in result:
        return "[{}] Start Update: Success".format(node)
    else:
        return "[{}] Start Update: Failed".format(node)

def racadm_sendtobios(node):
    """ Sets node to boot to the BIOS on next reboot, then hard reboots the node

        Args:
            node (string): hostname or IPv4 address of target node
    """

    boot_once_cmd = 'set iDRAC.serverboot.BootOnce 1'
    boot_dev_cmd = 'set iDRAC.serverboot.FirstBootDevice BIOS'

    once_result = racadm_call(node, boot_once_cmd)
    dev_result = racadm_call(node, boot_dev_cmd)

    if 'value modified successfully' in once_result:
        if 'value modified successfully' in dev_result:
            print '[{n}] Booting to BIOS on next restart'.format(n=node)
            racadm_power(node, 'hard')
            return '[{n}] Successfuly sent to BIOS'.format(n=node)

    return '[{n}] Failed to send to BIOS'.format(n=node)

def racadm_sendtopxe(node):
    """ Sets node to boot to PXE on next reboot, then powers off the server

        Args:
            node (string): hostname or IPv4 address of target node
    """

    boot_once_cmd = 'set iDRAC.serverboot.BootOnce 1'
    boot_dev_cmd = 'set iDRAC.serverboot.FirstBootDevice PXE'

    once_result = racadm_call(node, boot_once_cmd)
    dev_result = racadm_call(node, boot_dev_cmd)

    if 'value modified successfully' in once_result:
        if 'value modified successfully' in dev_result:
            racadm_power(node, 'off')
            return '[{n}] Successfuly sent to PXE'.format(n=node)

    return '[{n}] Failed to send to PXE'.format(n=node)

def racadm_power(node, setting):
    """ Wrapper fuction to send server power commands to the specified node

        Args:
            node (string): hostname or IPv4 address of target node
            setting (string): setting to be applied to node.
                Options are:
                    'soft': soft resets the node
                    'hard: hard resets the node
                    'off': powers off the node
                    'on': power on the node
    """

    options = {'soft': 'powercycle',
               'hard': 'hardreset',
               'off': 'powerdown',
               'on': 'poweron'}

    if setting == 'off':
        if 'ON' in racadm_call(node=node, args='serveraction powerstatus | grep status:'):
            try:
                power_cmd = "serveraction {option}".format(option=options[setting])
                racadm_call(node=node, args=power_cmd, check_output=False)
            except KeyError:
                print "[{n}] Failed to send action to node: Invalid setting specified".format(n=node)
    else:
        try:
            power_cmd = "serveraction {option}".format(option=options[setting])
            racadm_call(node=node, args=power_cmd, check_output=False)
        except KeyError:
            print "[{n}] Failed to send power action to node: Invalid setting specified".format(n=node)

def racadm_call(node, args, check_output=True, user='root', password='calvin'):
    """ Executes a remote RACADM call

        Args:
            node (string): hostname or IPv4 address of target node
            args (string): the body of the RACADM call to be sent
            check_output (bool): Return the full output of the call (default: True)
            user (string, optional): iDRAC username (default: root)
            password (string, optional): iDRAC password (default: calvin)
     """

    cmd = "racadm -r {n} -u {u} -p {p} {a}".format(n=node, u=user, p=password, a=args)
    try:
        if check_output:
            return subprocess.check_output(cmd, shell=True)
        else:
            return subprocess.call(cmd, shell=True, stdout=FNULL, stderr=subprocess.STDOUT) == 0
    except:
        print '[{n}] Failed to execute RACADM call! ({c})'.format(n=node, c=cmd)
        return None

def racadm_get_versions(node):
    """ Gets firmware inventory for target node

    Args:
        host (string): hostname or IPv4 address of target node

    Returns:
        a dictionary in the form of Item:Version pairs
        
    """

    cmd = "getversion"
    result = racadm_call(node, cmd).splitlines()

    version_dict = {}

    for line in result:
        if 'Version' in line:
            line_list = line.replace(' ', '').split('=')
            version_dict[line_list[0]] = line_list[1]

    cmd = 'storage get controllers:RAID.Integrated.1-1 -p FirmwareVersion'
    result = racadm_call(node, cmd).splitlines()

    for line in result:
        if 'Version' in line:
            line_list = line.replace(' ', '').split('=')
            version_dict['RaidVersion'] = line_list[1]

    cmd = 'get NIC.FrmwImgMenu.1.FamilyVersion'
    result = racadm_call(node, cmd).splitlines()

    for line in result:
        if 'Version' in line:
            line_list = line.replace(' ', '').split('=')
            version_dict['NetworkVersion'] = line_list[1]

    return version_dict

def racadm_led(node, state):
    """ Sets Identify Light on or off """

    OPTIONS = {
        'on': '1',
        'off': '0'
    }
    
    cmd = 'setled -l {}'.format(OPTIONS[state])
    racadm_call(node, cmd)

def racadm_clearsel(node):
    """ Clears System Event log for specified node """
    
    cmd = 'clrsel'
    racadm_call(node, cmd)