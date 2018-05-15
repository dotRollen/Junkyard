import argparse
from collections import OrderedDict
import json
import os
import subprocess

import KitsuUtils.bmc as BMC
import KitsuUtils.xcat as xCAT
import KitsuUtils.solarflare as SolarFlare
import KitsuUtils.core as Core
import KitsuUtils.megacli as MegaCLI

VERSION = '0.0.1 (Alpha)'

def config_all(noderange, keyfile):

    """ Configures all SolarFlare cards in the target node

        Args:
            noderange (list): list of xCAT node names to target for configuration
            keyfile (string, Optional): full path to key file on targeted system (Default: None)
    """

    print '[KitsuSF][Global] Starting firmware updates for {}'.format(noderange)
    SolarFlare.sf_update(noderange, write=True, image=None, yes=True)

    print '[KitsuSF][Global] Setting boot options for {}'.format(noderange)
    SolarFlare.sf_boot(noderange, clear=False, bootimage="optionrom", boottype="pxe")

    if keyfile is not 'nokey':
        print '[KitsuSF][Global] Setting keys for {}'.format(noderange)

        print '[KitsuSF][Global] Copying keyfile "{}" to nodes'.format(keyfile)
        xCAT.xdcp(noderange, source=keyfile, destination="/tmp/")

        local_keyfile = '/tmp/{}'.format(os.path.basename(keyfile))
        print '[KitsuSF][Global] Setting keys for {} using {}'.format(noderange, local_keyfile)
        SolarFlare.sf_key(noderange, all=True, install=local_keyfile)

    print '[KitsuSF][Global] Sending BIOS settings for {}'.format(noderange)
    xCAT.pasu(batch_file='/Tools/Kitsu/Stanley/files/x3650m5-20171027.pasu.bat', group=noderange)

def set_dhcp(noderange):

    print '[Kitsu] Starting MAC Binding'

    work_list = []
    for node in xCAT.nodels(noderange):
        if node and Core.ping(node):
            func = BMC.bind_mac
            fargs = (node, )
            work_list.append((func, fargs))
        else:
            print '[Kitsu][{}] ERROR - Node is unreachable!'.format(node)   

    Core.p_execute(work_list)
    

def _generate_update_json(node, system_serial, update_output, node_dict):

    """ Parses sfupdate output and populates node json dictionary

        Args:
            node (string): xCAT node name the output is tied to
            system_serial (string): the serial number of the chassis
            update_output (list): output from sfupdate to parse
            node_dict (OrderedDict): dictionary representing json string for node
    """

    slot_key = ''
    port_key = ''

    for line in update_output:

        _line = line.replace('{}: '.format(node), '')
        _line_list = _line.split()

        if 'ens' in _line:
            slot_key = 'Slot{}'.format(_line_list[0][3])
            port_key = 'Port{}'.format(_line_list[0][5])
            port_mac = _line_list[3]

            if not slot_key in node_dict[system_serial]:
                node_dict[system_serial][slot_key] = OrderedDict()
            if not port_key in node_dict[system_serial][slot_key]:
                node_dict[system_serial][slot_key][port_key] = OrderedDict()

            node_dict[system_serial][slot_key][port_key]['MacAddress'] = port_mac
        
        elif 'Firmware version' in _line:
            node_dict[system_serial][slot_key]['FirmwareVersion'] = _line_list[2]

        elif 'Controller type:' in _line:
            node_dict[system_serial][slot_key]['ControllerType'] = ' '.join(_line_list[2:])

        elif 'Controller version:' in _line:
            node_dict[system_serial][slot_key]['ControllerVersion'] = _line_list[2]

        elif 'Boot ROM version' in _line:
            node_dict[system_serial][slot_key]['BootROMVersion'] = _line_list[3]
        

def _generate_boot_json(node, system_serial, boot_output, node_dict):
    
    """ Parses sfboot output and populates node json dictionary

        Args:
            node (string): xCAT node name the output is tied to
            system_serial (string): the serial number of the chassis
            boot_output (list): output from sfboot to parse
            node_dict (OrderedDict): dictionary representing json string for node
    """
    
    curr_slot = ''
    curr_port = ''

    for line in boot_output:

        _line = line.replace('{}: '.format(node), '')

        if 'ens' in _line:
            curr_slot = _line[3]
            curr_port = _line[5]
        else:
            _line_split = [s.strip() for s in _line.split('  ') if s]

            if len(_line_split) == 2:
                line_key = _line_split[0].title().replace(' ', '')
                node_dict[system_serial]['Slot{}'.format(curr_slot)]['Port{}'.format(curr_port)][line_key] = _line_split[1]


def _generate_key_json(node, system_serial, key_output, node_dict):

    """ Parses sfkey output and populates node json dictionary

        Args:
            node (string): xCAT node name the output is tied to
            system_serial (string): the serial number of the chassis
            key_output (list): output from sfkey to parse
            node_dict (OrderedDict): dictionary representing json string for node
    """

    curr_slot = ''

    for line in key_output:

        _line = line.replace('{}: '.format(node), '')

        if 'ens' in _line:
            curr_slot = _line[3]

            _line_split = [s.strip() for s in _line.split() if s]
            node_dict[system_serial]['Slot{}'.format(curr_slot)]['SerialNumber'] = _line_split[1].strip()
            
        else:
            _line_split = [s.strip() for s in _line.split('\t') if s]
            if len(_line_split) == 2:                
                if 'Product name' in _line:
                    node_dict[system_serial]['Slot{}'.format(curr_slot)]['ProductName'] = _line_split[1].strip('\t')

                elif 'Installed keys' in _line:
                    node_dict[system_serial]['Slot{}'.format(curr_slot)]['InstalledKeys'] = _line_split[1].strip().replace(' ', '')

                    if not 'PTP' in node_dict[system_serial]['Slot{}'.format(curr_slot)]['InstalledKeys']:
                        print '[KitsuSF][{}] WARNING! PTP License not installed on: {}'.format(node, node_dict[system_serial]['Slot{}'.format(curr_slot)]['SerialNumber'])
                        with open('/po/sf/missing_licenses.txt', 'a+') as license_file:
                            if not node_dict[system_serial]['Slot{}'.format(curr_slot)]['SerialNumber'] in license_file.read():
                                license_file.write(node_dict[system_serial]['Slot{}'.format(curr_slot)]['SerialNumber'] + '\n')

                    else:
                        lines_to_keep = []
                        serial = node_dict[system_serial]['Slot{}'.format(curr_slot)]['SerialNumber']

                        with open('/po/sf/missing_licenses.txt', 'r') as license_file:
                            for l in license_file:
                                if not serial in l:
                                    lines_to_keep.append(l)
                                else:
                                    print '[KitsuSF][{}] Removing {} from Missing Keys file since PTP is installed'.format(node, node_dict[system_serial]['Slot{}'.format(curr_slot)]['SerialNumber'])
                        
                        with open('/po/sf/missing_licenses.txt', 'w') as license_file:
                            license_file.writelines(lines_to_keep)                


def generate_qc(noderange):
    
    """ Generates QC .json files for all nodes in the specified range

        Args:
            noderange (string): xCAT node or nodegroup name to target
    """

    node_list = xCAT.nodels(noderange)

    print '[KitsuSF][Global] Generating QC Output for {}'.format(noderange)

    for node in node_list:

        if Core.ping(node):

            node_dict = OrderedDict()

            print '[KitsuSF][{}] Generating QC File for {}'.format(node, node)

            system_serial = SolarFlare.get_system_serial(node)

            try:
                update_output = SolarFlare.sf_update(node, silent=False).splitlines()
                boot_output = SolarFlare.sf_boot(node).splitlines()
                key_output = SolarFlare.sf_key(node, all=True).splitlines()

            except:
                print '[KitsuSF][{}] FAIL - No SolarFlare output returned for {}'.format(node, node)
                continue

            jsonpath = '/po/sf/{}_solarflare.json'.format(system_serial)
            with open(jsonpath, 'w') as nodefile:
                
                node_dict[system_serial] = OrderedDict()
                node_dict[system_serial]['ChassisHostname'] = node
                
                _generate_update_json(node, system_serial, update_output, node_dict)
                _generate_boot_json(node, system_serial, boot_output, node_dict)
                _generate_key_json(node, system_serial, key_output, node_dict)

                nodefile.write(json.dumps(node_dict, indent=4, sort_keys=True))
                print '[KitsuSF][{}] Wrote QC data for {} to \'{}\''.format(node, node, jsonpath)

        else:
            print '[KitsuSF][{}] FAIL - Node is unreachable!'.format(node)

    
    print '[KitsuSF][Global] Finished generating QC files for {}'.format(noderange)


def set_raid(noderange):

    for node in xCAT.nodels(noderange):
        if node and Core.ping(node):
            xCAT.set_comment(node, 'set_raid')

            # Delete existing logical drives
            if not MegaCLI.delete_logical_drive(node):
                print '[KitsuSF][{}] FAIL - Failed to delete existing logical drives!'.format(node)

            # Create GLobal Hot Spare first
            if not MegaCLI.create_global_spare(node, 10):
                 print '[KitsuSF][{}] FAIL - Failed to create Global Hot Spare!'.format(node)

            # Create RAID 1 on drives 0 and 1
            if not MegaCLI.create_raid_1(node, [0,1]):
                 print '[KitsuSF][{}] FAIL - Failed to create RAID 1!'.format(node)

            # Create RAID 10 using drives 2-5 as Span0 and 6-9 as Span1
            span0 = [2,3,4,5]
            span1 = [6,7,8,9]
            if not MegaCLI.create_raid_10(node, [span0, span1]):
                print '[KitsuSF][{}] FAIL - Failed to create RAID 10!'.format(node)

            print '[KitsuSF][{}] Finished configuring storage for {}'.format(node, node)

        else:
            print '[KitsuSF][{}] FAIL - Node is unreachable!'.format(node)      

def bind_sf_macs(noderange):

    print '[Kitsu] Starting SolarFlare binding'

    work_list = []
    for node in xCAT.nodels(noderange):
        if node and Core.ping(node):
            func = SolarFlare.bind_sf_mac
            fargs = (node, 'ens1f0')
            work_list.append((func, fargs))
        else:
            print '[Kitsu][{}] ERROR - Node is unreachable!'.format(node)   

    Core.p_execute(work_list)


def main():

    parser = argparse.ArgumentParser(description='')

    parser.add_argument("noderange", metavar="<noderange>", help='xCAT noderange to target')
    parser.add_argument("-c", "--config", nargs='?', const='nokey', default=None, help='Configure SolarFlare adapters')
    parser.add_argument("-s", "--showconfig", action='store_true', help='Export node QC data')
    parser.add_argument("-b", "--bind", action="store_true", help="Bind IMM macs to DHCP IP")
    parser.add_argument("-r", "--raid", action="store_true", help="Configure RAID settings")
    parser.add_argument("-m", "--sfmac", action="store_true", help="Binds SolarFlare macs for PXE")

    args = parser.parse_args()

    print '[KitsuSF][Global] KitsuUtils for SolarFlare - v{}'.format(VERSION)

    if args.config:
        config_all(args.noderange, args.config)

    if args.bind:
        set_dhcp(args.noderange)

    if args.showconfig:
        generate_qc(args.noderange)

    if args.raid:
        set_raid(args.noderange)

    if args.sfmac:
        bind_sf_macs(args.noderange)

if __name__ == "__main__":
    main()
