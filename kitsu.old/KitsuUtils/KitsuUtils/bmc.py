import subprocess
import sys

import KitsuUtils.core as Core
import KitsuUtils.xcat as xCAT

def get_mfg(node):
    """
        Get manufacturer ID using IPMI tool.
        
        Returns lenovo, dell , hpe
    """

    cmd = "ipmitool mc info | grep 'Manufacturer ID' | awk -F: '{print $NF}'"
    mfgid = xCAT.psh(node, cmd).strip()

    # 19046 = Lenovo
    # 11    = HPE
    # 674   = DELL

    if mfgid == '19046':
        return 'lenovo'
    elif mfgid == '11':
        return 'hpe'
    elif mfgid == '674':
        return 'dell'
    else:
        return None
        
def get_mac(node, mfg):
    
    """ Returns BMC MAC address using IPMI tool """

    lan_channel = ''
    if mfg == 'lenovo' or mfg == 'dell':
        lan_channel = '1'
    elif mfg == 'hpe':
        lan_channel = '2'

    cmd = "ipmitool lan print %s | grep 'MAC Address' | grep -io '[0-9A-F]\{2\}\(:[0-9A-F]\{2\}\)\{5\}' |egrep -m 1 '\w+'" % lan_channel
    return xCAT.psh(node, cmd)

def set_user(node, user='admin', password='Passw0rd!'):

    """ Creates second user on BMC """

    xCAT.psh(node, " ipmitool user set name 2 {}".format(user))
    xCAT.psh(node, " ipmitool user set password 2 {}".format(password))
    xCAT.psh(node, " ipmitool channel setaccess 2 2 link=on ipmi=on callin=on privilege=4".format())
    xCAT.psh(node, " ipmitool user enable 2".format())

def get_lan_channel(mfg):
    
    """ Returns manufacturer lan channel. Dell and Lenovo = channel 1 HPE = channel 2 """

    lan_channel = ''
    if mfg == 'lenovo' or mfg == 'dell':
        return '1'
    elif mfg == 'hpe':
        return '2'
    else:
        return '1'


def bind_mac(node):

    """ Binds BMC MAC address to the <node>-bmc definiton, change BMC to DHCP and create a DHCP static lease.

        Args:
            node (string): the xCAT name of the node to target

        Returns:
            (string) 
    """

    mfg = get_mfg(node)        
    if mfg:
        try:
            mac = get_mac(node, mfg)
            xCAT.chdef('node', '{}-bmc'.format(node), 'mac={}'.format(mac))
            bmcmac = subprocess.check_output("lsdef " + node + "-bmc | grep 'mac=' | awk -F= '{print $NF}'", shell=True, stderr=subprocess.STDOUT)

            if mac == bmcmac:
                xCAT.makedhcp(node + '-bmc')
                xCAT.psh(node, 'ipmitool lan set {} ipsrc dhcp'.format(get_lan_channel(mfg)))
                xCAT.psh(node, 'ipmitool mc reset cold')
                return "[Kitsu][{}] Successfully enabled DHCP on BMC.".format(node)

            else:
                return "[Kitsu][{}] Mac definition doesn't match ipmitool output.".format(node)

        except:
            return "[Kitsu][{}] Failed to set BMC to DHCP.".format(node)                
            
    else:
        return "[Kitsu][{}] Failed to get Manufacturer ID.".format(node)
