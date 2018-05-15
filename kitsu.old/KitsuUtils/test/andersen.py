import os
import subprocess
import argparse
import KitsuUtils.xcat as xCAT
import KitsuUtils.bmc as BMC
import KitsuUtils.core as Core
import KitsuUtils.megacli as MegaCLI

VERSION = '0.0.1 (Alpha)'

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

def set_raid(noderange, raid_type, slots):

    work_list = []
    if '-' in slots:
        drive_list = range(int(slots.split('-')[0]), int(slots.split('-')[1])+1)
    elif ',' in slots:
        drive_list = slots.split(',')
    else:
        print('Error: Enter slot range as either a comma separated list or in the format "LOW-HIGH" IE: 0-5')

    if raid_type == '1':            
        for node in xCAT.nodels(noderange):
            if MegaCLI.create_raid_1(node, drive_list):
                print 'Succesfully created RAID 1 on physical drives {}'.format(",".join(str(x) for x in drive_list))

    elif raid_type == '6':            
        for node in xCAT.nodels(noderange):
            if MegaCLI.create_raid_6(node, drive_list):
                print 'Succesfully created RAID 1 on physical drives {}'.format(",".join(str(x) for x in drive_list))

    else:
        print 'Error: Invalid raid type specified!'

def main():

    parser = argparse.ArgumentParser(description='')

    parser.add_argument("noderange", metavar="<noderange>", help='xCAT noderange to target')
    parser.add_argument("-b", "--bind", action="store_true", help="Bind IMM macs to DHCP IP")
    parser.add_argument("-r1", "--raid1", nargs='?', const='nokey', default=None, help='Configure RAID 1')
    parser.add_argument("-r6", "--raid6", nargs='?', const='nokey', default=None, help='Configure RAID 6')

    args = parser.parse_args()

    print '[KitsuSF][Global] KitsuUtils for Andersen - v{}'.format(VERSION)

    if args.bind:
        set_dhcp(args.noderange)

    if args.raid1:
        set_raid(args.noderange, '1', args.raid1)

    if args.raid6:
        set_raid(args.noderange, '6', args.raid6)

if __name__ == "__main__":
    main()