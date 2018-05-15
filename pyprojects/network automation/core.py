
from netmiko import ConnectHandler
from datetime import datetime

cisco_asa = {
        'device_type': 'cisco_asa',
        'ip': '192.168.1.1',
        'username': 'Philips',
        'password': 'Philips',
        'secret': '',
        'verbose': False,
    }

net_connect = ConnectHandler(**cisco_asa)
output = net_connect.send_command("show int ip brief")

print output