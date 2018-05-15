""" Implements wrapper functions for interacting with MegaCLI

    Requirements:
        * You must have MegaCLI installed on the target node (in the stateless image usually)
    Todo:
        * A lot.
"""

import KitsuUtils.xcat as xCAT

STATUS_SUCCESS = '0x00'

def _get_enclosure_id(node):

    # Get number of drives to check which apdater is the correct one
    num_drives = int(xCAT.psh(node, '/opt/MegaRAID/MegaCli/MegaCli64 -EncInfo -a0 | grep -A 12 \'Enclosure 0:\' | grep Physical | sed -n -e \'s/^.*: //p\'').splitlines()[0])

    # If there are physical drives on the enclosure, get its Device ID and return it
    if num_drives != 0:
        device_id = xCAT.psh(node, '/opt/MegaRAID/MegaCli/MegaCli64 -EncInfo -a0 | grep -A 12 \'Enclosure 0:\' | grep Device | sed -n -e \'s/^.*: //p\'').splitlines()[0]
        return device_id

def delete_logical_drive(node, drive='all'):

    cmd = '/opt/MegaRAID/MegaCli/MegaCli64 -CfgLdDel -L{drive} -a0'.format(drive=drive)

    if STATUS_SUCCESS in xCAT.psh(node, cmd):
        return True
    else:
        return False

def create_global_spare(node, drive_num):

    device_id = _get_enclosure_id(node)

    rcmd = '/opt/MegaRAID/MegaCli/MegaCli64 -PDHSP -Rmv -PhysDrv [{}:{}] -a0'.format(device_id, drive_num)
    xCAT.psh(node, rcmd)
    
    cmd = '/opt/MegaRAID/MegaCli/MegaCli64 -PDHSP -Set -PhysDrv [{id}:{drive}] -a0'.format(id=device_id, drive=drive_num)

    if STATUS_SUCCESS in xCAT.psh(node, cmd):
        return True
    else:
        return False

def create_raid_1(node, drive_list):

    device_id = _get_enclosure_id(node)
    
    drive_string = ",".join('{}:{}'.format(device_id, drive) for drive in drive_list)
    
    cmd = '/opt/MegaRAID/MegaCli/MegaCli64 -CfgLdAdd -r1[{}] -a0'.format(drive_string)
    
    if STATUS_SUCCESS in xCAT.psh(node, cmd):
        return True
    else:
        return False

def create_raid_6(node, drive_list):

    device_id = _get_enclosure_id(node)
    
    drive_string = ",".join('{}:{}'.format(device_id, drive) for drive in drive_list)
    
    cmd = '/opt/MegaRAID/MegaCli/MegaCli64 -CfgLdAdd -r6[{}] -a0'.format(drive_string)
    
    if STATUS_SUCCESS in xCAT.psh(node, cmd):
        return True
    else:
        return False

def create_raid_10(node, span_list):

    device_id = _get_enclosure_id(node)

    drives_span0 = ",".join('{}:{}'.format(device_id, drive) for drive in span_list[0])
    drives_span1 = ",".join('{}:{}'.format(device_id, drive) for drive in span_list[1])
    
    cmd = '/opt/MegaRAID/MegaCli/MegaCli64 -CfgSpanAdd -r10 -Array0[{}] -Array1[{}] -a0'.format(drives_span0, drives_span1)

    if STATUS_SUCCESS in xCAT.psh(node, cmd):
        return True
    else:
        return False


# def get_drives_by_ld(node):


    