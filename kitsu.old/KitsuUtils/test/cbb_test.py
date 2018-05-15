import argparse
from collections import OrderedDict
import json
import os

import KitsuUtils.bmc as BMC
import KitsuUtils.xcat as xCAT
import KitsuUtils.core as Core

def configall(noderange):
    
    print '[Kitsu] Sending BIOS setting'

    xCAT.pasu(batch_file='/Tools/Kitsu/CBB/files', group=noderange)
    
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

def _generate_dmidecode_json(node, system_serial, boot_output, node_dict):
    
    curr_slot = ''
    curr_port = ''

    for line in boot_output:

        # if 'ens' in line:
        #     curr_slot = line[3]
        #     curr_port = line[5]
        # else:
        #     _line_split = [s.strip() for s in _line.split('  ') if s]

        #     if len(_line_split) == 2:
        #         line_key = _line_split[0].title().replace(' ', '')
        #         node_dict[system_serial]['Slot{}'.format(curr_slot)]['Port{}'.format(curr_port)][line_key] = _line_split[1]
        pass

def generate_qc(noderange):
    
    print '[Kistu] Starting QC output'

    for node in noderange:
        
        if Core.ping(node):
            
            node_dict = OrderedDict()

            print '[KitsuSF][{}] Generating QC File for {}'.format(node, node)

            system_serial = xCAT.lsdef(obj_type='node', group=node, grep="| grep 'serial=' | awk -F= '{print $2}'")
            
            try:
                pasu_output = xCAT.pasu(node, cmd="show all", grep="| awk '{$1="";print $0}'")
                lspci_output = xCAT.psh(node, cmd="lspci | awk '{$1="";print $0}'")
                dmidecode_output = xCAT.psh(node, cmd="dmidecode | awk '{$1="";print $0}'")
            
            except:
                print '[KitsuSF][{}] FAIL - No QC output returned for {}'.format(node, node)
                continue

            jsonpath = '/po/sf/{}_solarflare.json'.format(system_serial)
            with open(jsonpath, 'w') as nodefile:
                
                node_dict[system_serial] = OrderedDict()
                node_dict[system_serial]['ChassisHostname'] = node
                
                #_generate_pasu_json(node, system_serial, pasu_output, node_dict)
                #_generate_lspci_json(node, system_serial, lspci_output, node_dict)
                _generate_dmidecode_json(node, system_serial, dmidecode_output, node_dict)

                nodefile.write(json.dumps(node_dict, indent=4, sort_keys=True))
                print '[KitsuSF][{}] Wrote QC data for {} to \'{}\''.format(node, node, jsonpath)

        else:
            print '[KitsuSF][{}] FAIL - Node is unreachable!'.format(node)


def main():
    
    parser = argparse.ArgumentParser(description='')

    parser.add_argument("noderange", metavar="<noderange>", help='xCAT noderange to target')
    parser.add_argument("-c", "--config", nargs='?', const='nokey', default=None, help='Configure SolarFlare adapters')
    parser.add_argument("-s", "--showconfig", action='store_true', help='Export node QC data')
    parser.add_argument("-b", "--bind", action="store_true", help="Bind IMM macs to DHCP IP")

    args = parser.parse_args()

    if args.config:
        configall(args.noderange)
    if args.bind:
        set_dhcp(args.noderange)
    if args.showconfig:
        generate_qc(args.noderange)

if __name__ == "__main__":
    main()