""" Implements functions for SolarFlare-specific interaction

    Requirements:
        * You must have sfutils installed on the HOST you are configuring. (usually in)

    Todo:
        * A lot.
"""
import subprocess

import KitsuUtils.xcat as xCAT

def get_system_serial(node):

    """ Gets the system serial of the node

        Args:
            node (string): the xCAT node name to target
        
        Returns:
            string: The node serial number or 'None'
    """

    cmd = "dmidecode --string system-serial-number"
    try:
        return xCAT.psh(node, cmd).lstrip('{}: '.format(node)).strip()
    except:
        return None


def get_interface_mac(node, interface_name):

    cmd = 'sfupdate | grep {} | sed -n -e \'s/^.*: //p\''.format(interface_name)
    return xCAT.psh(node, cmd).strip().replace('-', ':')


def bind_sf_mac(node, interface_name):

    mac = get_interface_mac(node, interface_name)
    xCAT.chdef('node', '{}'.format(node), 'mac={}'.format(mac))

    def_mac = subprocess.check_output("lsdef " + node + " | grep 'mac=' | awk -F= '{print $NF}'", shell=True, stderr=subprocess.STDOUT).strip()
    if mac == def_mac:
        xCAT.makedhcp(node)
        return '[Kitsu][{}] Successfully bound mac to SolarFlare interface!'.format(node)
    else:
        return '[Kitsu][{}] Failed to set mac to SolarFlare interface!'.format(node)


def sf_update(group, write=False, image=None, force=False, yes=False, silent=True):
    
    """ Wrapper for SolarFlare CLI tool "sfupate"

        Args:
            group (string): xCAT group name to target with firmware update
            image (string, Optional): SolarFlare firmware image to be update to. Default: "None" - use built-in image
            force (bool, Optional): Forces firmware update even if current version is newer than target version. Default: False
            yes (bool, Optional): Skips answers "yes" to final confirmation before updating.
            silent (bool, Optional): Suppress all output except errors, useful for scripting. Default: True

        Returns:
            string: The raw output from the sfupdate command.
    """

    # Create default command
    cmd = "sfupdate"

    # Append options to command
    if write:
        cmd += " --write"
    if image:
        cmd += " --image={img}".format(img=image)
    if force:
        cmd += " --force"
    if yes:
        cmd += " -y"
    if silent:
        cmd += " --silent"

    # Send command using xCAT's "psh" to all nodes in the specified group
    return xCAT.psh(group, cmd)


def sf_key(group, all=False, inventory=False, keys=False, install=None):

    """ Wrapper for SolarFlare CLI tool "sfkey"

        Args:
            group (string): xCAT group name to target with firmware update
            all (bool, Optional): Applys to all adaptors.
            inventory (bool, Optional): List the adaptors that support licensing.
            keys (bool, Optional): Display keys for all adaptors
            install  (string, Optional): Install key file to SolarFlare cards.
                                        Use: --install <keyfile>

        Returns:
            string: The raw output from the sfkey command.
    """

    # Default 
    cmd = "sfkey"

    if all:
        cmd += " --all"
    if inventory:
        cmd += " --inventory"
    if keys:
        cmd += " --keys"
    if install:
        cmd += " --install {0}".format(install)

    # Send command using xCAT's "psh" to all nodes in the specified group
    return xCAT.psh(group, cmd)


def sf_boot(group, clear=False, bootimage=None, boottype=None):

    """ Wrapper for SolarFlare CLI tool "sfboot"

        Args:
            group (string): xCAT group name to target with firmware update
            clear (bool, Optional): Reset SolarFlare adapter settings to default.
            bootimage (string, Optional): Specifies which boot firmware images are served up to the BIOS during start up.
                                          Options: 'all','optionrom','uefi','disabled'
            boottype (string, Optional): Sets the adapter boot type - effective on next boot. Options: 'pxe','disabled'

        Returns:
            string: The raw output from the sfboot command.
    """

    # Default
    cmd = "sfboot"

    if clear:
        cmd += " --clear"
    if bootimage:
        cmd += " boot-image={0}".format(bootimage)
    if boottype:
        cmd += " boot-type={0}".format(boottype)

    # Send command using xCAT's "psh" to all nodes in the specified group
    return xCAT.psh(group, cmd)