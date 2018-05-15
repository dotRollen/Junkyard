import argparse
import errno
import os
import re
import time

import KitsuUtils.bmc as BMC
import KitsuUtils.core as Core
import KitsuUtils.dell as Dell
import KitsuUtils.xcat as xCAT

VERSION = '0.0.1 (Alpha)'
MODELS = ['R730xd', 'R630', 'C4130']
ROLES = ['storage', 'compute', 'mgmt', 'gpu']

def is_gcp(noderange):

    regstr = re.compile('gaia-r\d+u\d+')

    if noderange.count('-') > 1:
        node_list = xCAT.nodels(noderange[:noderange.rindex('-')])
    elif regstr.match(noderange) is not None:
        print '[Kistu][is_gcp] Found single node, using group "{}" to check for GCP'.format(noderange[:noderange.rindex('u')])
        node_list = xCAT.nodels(noderange[:noderange.rindex('u')])
    else:
        node_list = xCAT.nodels(noderange)

    if node_list:
        for node in node_list:
            if 'gpu' in xCAT.get_comment(node):
                return True
    return False

def set_dhcp(noderange):

    print '[Kitsu] Starting MAC Binding'

    work_list = []
    for node in xCAT.nodels(noderange):
        target_node = node
        if '-bmc' in node:
            target_node = node.rstrip('-bmc')
        if target_node and Core.ping(target_node):
            func = BMC.bind_mac
            fargs = (target_node, )
            work_list.append((func, fargs))
        else:
            print '[Kitsu][{}] ERROR - Node is unreachable!'.format(node)   

    Core.p_execute(work_list)
    

def import_settings(noderange, xmlfile=None):

    print '[Kitsu] Starting BIOS Import'
    
    work_list = []
    for node in xCAT.nodels(noderange):    
        
        biosfile = xmlfile
        if not biosfile:            
            node_model = xCAT.get_node_property(node.rstrip('-bmc'), 'mtm')
            for model in MODELS:
                if model in node_model:
                    biosfile = '/data/Gaia/bios_dell_{}.xml'.format(model.lower())

        if biosfile:
            target_node = node
            if not '-bmc' in node:
                target_node = node + '-bmc'
            if target_node and Core.ping(target_node):
                func = Dell.set_bios
                fargs = (target_node, biosfile)
                work_list.append((func, fargs))
            else:
                print '[Kitsu][{}] ERROR - Node is unreachable!'.format(node)
        else:
            print '[Kitsu][{}] ERROR - Unable to determine node type, make sure node is discovered!'.format(node)

    Core.p_execute(work_list)


def update_nodes(noderange):

    print '[Kitsu] Starting Firmware Update'

    work_list = []
    for node in xCAT.nodels(noderange):
        target_node = node
        if not '-bmc' in node:
            target_node = node + '-bmc'
        if target_node and Core.ping(target_node): 
            func = Dell.racadm_update
            fargs = (target_node, 'Gaia')
            work_list.append((func, fargs))
        else:
            print '[Kitsu][{}] ERROR - Node iDRAC is unreachable, please ensure iDRAC for {} is configured and pinging!'.format(node, node)

    Core.p_execute(work_list)


def compare_firmware_versions(node):

    versions = Dell.racadm_get_versions(node)
    
    mismatch = False
    bad_versions = ['[{}] Firmware Version Check'.format(node)]
    nodetype = xCAT.get_comment(node.rstrip('-bmc'))

    if not 'gpu' in nodetype:
        if versions['BiosVersion'] != '2.2.5':
            bad_versions.append('Bios - Required: 2.2.5 - Actual: {}'.format(versions['BiosVersion']))
            mismatch = True
        if versions['iDRACVersion'] != '2.41.40.40':
            bad_versions.append('iDRAC - Required: 2.41.40.40 - Actual: {}'.format(versions['iDRACVersion']))
            mismatch = True
        if versions['LifecycleControllerVersion'] != '2.41.40.40':
            bad_versions.append('Lifecycle - Required: 2.41.40.40 - Actual: {}'.format(versions['LifecycleControllerVersion']))
            mismatch = True
        if versions['RaidVersion'] != '25.5.0.0018':
            bad_versions.append('Raid - Required: 25.5.0.0018 - Actual: {}'.format(versions['RaidVersion']))
            mismatch = True
        if versions['NetworkVersion'] != '16.5.20':
            bad_versions.append('Network - Required: 16.5.20 - Actual: {}'.format(versions['NetworkVersion']))
            mismatch = True
    else:
        if versions['BiosVersion'] != '2.4.2':
            bad_versions.append('Bios - Required: 2.4.2 - Actual: {}'.format(versions['BiosVersion']))
            mismatch = True
        if versions['iDRACVersion'] != '2.41.40.40':
            bad_versions.append('iDRAC - Required: 2.41.40.40 - Actual: {}'.format(versions['iDRACVersion']))
            mismatch = True
        if versions['LifecycleControllerVersion'] != '2.41.40.40':
            bad_versions.append('Lifecycle - Required: 2.41.40.40 - Actual: {}'.format(versions['LifecycleControllerVersion']))
            mismatch = True

    if mismatch:
        return ' | '.join(bad_versions)

    else:
        return '[{}] Firmware Version Check - ALL PASSED'.format(node.rstrip('-bmc'))


def check_update_success(noderange):

    print '[Kitsu] Starting Firmware Version Check for {}'.format(noderange)

    work_list = []
    for node in xCAT.nodels(noderange):
        target_node = node
        if not '-bmc' in node:
            target_node = node + '-bmc'
        if target_node and Core.ping(target_node): 
            func = compare_firmware_versions
            fargs = (target_node, )
            work_list.append((func, fargs))
        else:
            print '[Kitsu][{}] ERROR - Node iDRAC is unreachable, please ensure iDRAC for {} is configured and pinging!'.format(node, node)

    for item in Core.p_execute(work_list):
        #if not 'ALL PASSED' in item:
            #print item
        print item

def configure_raid(noderange):

    print '[Kitsu] Starting RAID Configuration'
    
    work_list = []

    gcp = is_gcp(noderange)
    if gcp:
        print '[Kitsu] This is a GCP Rack - Using GCP configuration for any storage nodes'
    else:
        print '[Kitsu] This is not a GCP Rack - Using High-Density configuration for any storage nodes'

    for node in xCAT.nodels(noderange):        
        raid_file = None
        node_role = xCAT.get_comment(node.rstrip('-bmc'))

        if 'gpu' in node_role:
            print '[Kitsu][{}] Skipping {} - Reason: GPU Node'.format(node, node)
            continue

        for role in ROLES:
            if role in node_role:
                if 'storage' in role:                
                    raid_file = '/data/Gaia/raid_dell_r730xd_shi.sh'
                else:
                    raid_file = '/data/Gaia/raid_dell_r630_shi.sh'

        if raid_file:
            target_node = node
            if '-bmc' in node:
                target_node = node.rstrip('-bmc')
            if target_node and Core.ping(target_node):
                func = xCAT.xdsh_script
                fargs = (target_node, raid_file)
                work_list.append((func, fargs))
            else:
                print '[Kitsu][{}] ERROR - Node is unreachable!'.format(node)
        else:
            print '[Kitsu][{}] ERROR - Unable to determine node type, make sure node is discovered!'.format(node)

    print '[Kitsu] Executing MegaCLI configuration, this may take a few minutes...'
    output_list = Core.p_execute(work_list, print_output=False)
    for entry in output_list:        
        if entry and 'Created VD 0' in ''.join(entry):
            print '[Kitsu][{}] SUCCESS - Successfully configured RAID.'.format(entry[0].replace(': ', '').strip())
        else:
            print '[Kitsu] ERROR - Failed to configure RAID!'

def wipe_raid(noderange):
    raid_file = '/data/Gaia/raid_dell_wipe.sh'

    print '[Kitsu] Wiping RAID Configuration for {}'.format(noderange)

    work_list = []
    for node in xCAT.nodels(noderange):
        target_node = node
        if '-bmc' in node:
            target_node = node.rstrip('-bmc')
        if target_node and Core.ping(target_node):
            if not xCAT.in_genesis(node):
                func = xCAT.xdsh_script
                fargs = (target_node, raid_file)
                work_list.append((func, fargs))
            else:
                print '[Kitsu][{}] ERROR - Node is in genesis kernel, boot to kitsu-netboot and retry!'.format(node)
        else:
            print '[Kitsu][{}] ERROR - Node is unreachable!'.format(node)
    
    for result in Core.p_execute(work_list):
        if result:
            print result[-1]
        else:
            print ""


def get_inventory(node, xml_directory):
    """ Gets BIOS settings and HWInventory in xml form for BigData nodes using racadm """
    
    node_directory = '{xml_dir}/{name}'.format(xml_dir=xml_directory, name=node.rstrip('-bmc').lstrip('gaia-')) 

    try:
        os.makedirs(node_directory)
    except OSError as e:    
        if e.errno != errno.EEXIST:
            raise

    bios_cmd = "get -f {}/{}-bios.xml -t xml --replace".format(node_directory, node.rstrip('-bmc').lstrip('gaia-'))
    bios_result = Dell.racadm_call(node, bios_cmd)

    inv_cmd = "hwinventory export -f {}/{}-hwinv.xml".format(node_directory, node.rstrip('-bmc').lstrip('gaia-'))
    inv_result = Dell.racadm_call(node, inv_cmd)

    full_result_string = '[{}] Export Inventory - '.format(node)
    full_result_bool = True

    if bios_result and "exported successfully" in bios_result:
        full_result_string += "Bios: Success | "
    else:
        full_result_string += "Bios: Failed | "
        full_result_bool = False

    if inv_result and "exported successfully" in inv_result:
        full_result_string += "Inv: Success"
    else:
        full_result_string += "Inv: Failed"
        full_result_bool = False

    return (full_result_string, full_result_bool)


def get_qc_data(noderange):
    """ Generates all QC files for the specified BigData rack """

    rack_directory = '/po/GAIA/'+ ('%s-' % noderange.replace('-bmc', '').replace('gaia-', '').replace('-node', '')) + time.strftime('%m%d')

    try:
        os.makedirs(rack_directory)
    except OSError as e:    
        if e.errno != errno.EEXIST:
            raise

    print '[Kitsu] Starting QC Data Export for {}'.format(noderange)

    work_list = []
    for node in xCAT.nodels(noderange):
        target_node = node
        if not '-bmc' in node:
            target_node = node + '-bmc'
        if target_node and Core.ping(target_node): 
            func = get_inventory
            fargs = (target_node, rack_directory)
            work_list.append((func, fargs))
        else:
            print '[Kitsu][{}] ERROR - Node iDRAC is unreachable, please ensure iDRAC for {} is configured and pinging!'.format(node, node)

    Core.p_execute(work_list)

def flash_node(node):
    Dell.racadm_led(node, 'on')
    Dell.racadm_led(node, 'off')

def identify_nodes(noderange):
    print '[Kitsu] Starting Elevation Check for {}'.format(noderange)
    time.sleep(5)
    for node in xCAT.nodels(noderange):
        target_node = node
        if not '-bmc' in node:
            target_node = node + '-bmc'
            print '[Kitsu] Flashing ID Light on {}'.format(node)
            Dell.racadm_led(target_node, 'on')
        else:
            print '[Kitsu][{}] ERROR - Node iDRAC is unreachable, please ensure iDRAC for {} is configured and pinging!'.format(node, node)
    for node in xCAT.nodels(noderange):
        target_node = node
        if not '-bmc' in node:
            target_node = node + '-bmc'
            print '[Kitsu] Stopping ID Light on {}'.format(node)
            Dell.racadm_led(target_node, 'off')
        else:
            print '[Kitsu][{}] ERROR - Node iDRAC is unreachable, please ensure iDRAC for {} is configured and pinging!'.format(node, node)

def pxe_node(noderange):
    print '[Kitsu] PXE booting {}'.format(noderange)

    work_list = []
    for node in xCAT.nodels(noderange):
        target_node = node
        if not '-bmc' in node:
            target_node = node + '-bmc'
        if target_node and Core.ping(target_node): 
            func = Dell.racadm_sendtopxe
            fargs = (target_node, )
            work_list.append((func, fargs))
        else:
            print '[Kitsu][{}] ERROR - Node iDRAC is unreachable, please ensure iDRAC for {} is configured and pinging!'.format(node, node)
    
    for result in Core.p_execute(work_list):
        if result:
            print result
        else:
            print ""


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='KistuUtils for Gaia')

    parser.add_argument("noderange", metavar="<noderange>", help='noderange')
    parser.add_argument("-d", "--dhcp", action='store_true', help='Bind MAC and change iDRAC to DHCP')
    parser.add_argument("-u", "--update", action='store_true', help='Do firmware updates')
    parser.add_argument("-c", "--checkupdate", action='store_true', help='Check firmware versions')    
    parser.add_argument("-b", "--bios", action='store_true', help='Set BIOS settings')
    parser.add_argument("-x", "--xmlfile", default=None, help='Bios xml file to use for update')
    parser.add_argument("-r", "--raid", action='store_true', help='Set RAID configuration')
    parser.add_argument("-i", "--identify", action='store_true', help='Light identify lights')    
    parser.add_argument("-q", "--qc", action='store_true', help='Export QC data')
    parser.add_argument("-w", "--wiperaid", action='store_true', help='Clear raid configuration')
    parser.add_argument("-p", "--pxe", action='store_true', help='Set next boot to PXE and shut down node')

    args = parser.parse_args()

    print '[Kitsu][Global] KitsuUtils for GAIA - v{}'.format(VERSION)

    if args.update:
        update_nodes(args.noderange)

    if args.dhcp:
        set_dhcp(args.noderange)

    if args.bios:
        import_settings(args.noderange, args.xmlfile)

    if args.checkupdate:
        check_update_success(args.noderange)

    if args.qc:
        get_qc_data(args.noderange)

    if args.raid:
        configure_raid(args.noderange)
    
    if args.identify:
        identify_nodes(args.noderange)

    if args.wiperaid:
        wipe_raid(args.noderange)

    if args.pxe:
        pxe_node(args.noderange)

