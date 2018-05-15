import errno
import time
import os
import subprocess

import KitsuUtils.xcat as xCAT

def create_raid0(noderange, drives="allunassigned"):

    raid_cmd = ('modprobe sg && '
        'ssacli rescan && ' 
        'ssacli controller slot=0 create type=arrayr0 drives={}'.format(drives))

    # Load drivers and set raid
    xCAT.psh(noderange, raid_cmd)

def get_diagnostics(noderange, output_directory):

    # Create new directory to hold noderange
    directory = output_directory + ('%s-Storage-' % noderange) + time.strftime('%Y%m%d-%H%M%S')

    try:
        os.makedirs(directory)
    except OSError as e:    
        if e.errno != errno.EEXIST:
            raise
    
    diag_cmd = ('mkdir -p /tmp/storagediag && '
                'rm -f /tmp/storagediag/storagediag.zip && '
                'rm -f /tmp/storagediag/ssddiag.zip && '
                'ssacli controller all diag file=/tmp/storagediag/storagediag.zip && '
                'ssacli controller all diag file=/tmp/storagediag/ssddiag.zip ssdrpt=on')
    
    # Create storage diagnostics
    xCAT.psh(noderange, diag_cmd)    

    # Copy all storage diagnostics to xCAT MN
    xCAT.xdcp(noderange, '/tmp/storagediag', directory, True)        
