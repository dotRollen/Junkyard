import os
import subprocess
import argparse
import KitsuUtils.ssacli as SSACLI
import KitsuUtils.xcat as xCAT
import KitsuUtils.bmc as BMC
import KitsuUtils.hp as HPE
import KitsuUtils.core as Core

VERSION = '0.0.1 (Alpha)'

def _ilo_fn(node):
    BMC.bind_mac(node)
    BMC.set_user(node)

def set_ilo(noderange):

    work_list = []

    for node in xCAT.nodels(noderange):
        target_node = node
        if '-bmc' in node:
            target_node = node.rstrip('-bmc')
        if target_node and Core.ping(target_node):
            func = _ilo_fn
            fargs = (target_node, )
            work_list.append((func, fargs))
        else:
            print '[Kitsu][{}] ERROR - Node is unreachable!'.format(target_node)   
            
    Core.p_execute(work_list)

def set_bios(noderange):
    for node in xCAT.nodels(noderange):
        restobj = HPE.create_session(node)
        HPE.change_bios_setting(restobj,)


def set_raid(noderange):

    SSACLI.create_raid0(noderange)
    SSACLI.get_diagnostics(noderange, output_directory='/ProjectOutput/Cassandra/')

def main():

    parser = argparse.ArgumentParser(description='')
    parser.add_argument("noderange", metavar="<noderange>", help="xCAT noderange to target")
    parser.add_argument("-i", "--ilo", action="store_true", help="Set BMC username and bind DHCP host.")
    parser.add_argument("-r", "--raid", action="store_true", help="Set RAID array configuration")
    parser.add_argument("-b", "--bios", action="store_true", help="Set RAID array configuration")
    args = parser.parse_args()

    print '[KitsuSF][Global] KitsuUtils for Cassandra - v{}'.format(VERSION)

    if args.ilo:
        set_ilo(args.noderange)

    if args.raid:
        set_raid(args.noderange)
    
    if args.bios:
        set_bios(args.noderange)

if __name__ == "__main__":
    main()