#! python2

import subprocess, platform, re, sys, argparse, os


def ping(host):

    ping_str = "-n 1" if platform.system().lower() == "windows" else "-c 1"
    args = "ping " + " " + ping_str + " " + host

    return subprocess.call(args, shell=need_sh(), stdout=FNULL(), stderr=subprocess.STDOUT) == 0


def need_sh():

    return False if platform.system().lower() == "windows" else True

def FNULL():

    return open(os.devnull, 'w')

def bindbmc(hosts):

	for host in hosts:

		if ping(host):

			mfgid = subprocess.check_output("psh " + host + " ipmitool mc info | grep 'Manufacturer ID' | awk -F: '{print $NF}'", shell=need_sh(), stderr=subprocess.STDOUT).strip()

			# MFG ID 19046 = Lenovo
			# MFG ID 11 = HP

			if mfgid == '19046':
				print("Complete: Found vendor Lenovo for " + host)
				try:
					mac = subprocess.check_output("psh " + host + " ipmitool lan print 1|grep -io '[0-9A-F]\{2\}\(:[0-9A-F]\{2\}\)\{5\}' |egrep -m 1 '\w+'", shell=need_sh(), stderr=subprocess.STDOUT)
					subprocess.call("chdef " + host + "-bmc mac=" + mac, shell=need_sh(), stdout=FNULL(), stderr=subprocess.STDOUT)
					bmcmac = subprocess.check_output("lsdef " + host + "-bmc | grep 'mac=' | awk -F= '{print $NF}'", shell=need_sh(), stderr=subprocess.STDOUT)

					if mac == bmcmac:

						subprocess.call("makedhcp -a " + host + "-bmc", shell=need_sh(), stdout=FNULL(), stderr=subprocess.STDOUT)	
						print("Complete: " + host + "-bmc MAC address has been bound.")

					subprocess.call("psh " + host + " ipmitool lan set 1 ipsrc dhcp", shell=need_sh(), stdout=FNULL(), stderr=subprocess.STDOUT)
					subprocess.call("psh " + host + " ipmitool mc reset cold", shell=need_sh(), stdout=FNULL(), stderr=subprocess.STDOUT)
					print("Complete: " + host + " IPMI DHCP enabled.")
				except(subprocess.CalledProcessError) as error:

					print(error.output)
					sys.exit()

			elif mfgid == '11':
				print("Complete: Found vendor HP for " + host)
				try:
					mac = subprocess.check_output("psh " + host + " ipmitool lan print 2|grep -io '[0-9A-F]\{2\}\(:[0-9A-F]\{2\}\)\{5\}' |egrep -m 1 '\w+'", shell=need_sh(), stderr=subprocess.STDOUT)
					subprocess.call("chdef " + host + "-bmc mac=" + mac, shell=need_sh(), stdout=FNULL(), stderr=subprocess.STDOUT)
					bmcmac = subprocess.check_output("lsdef " + host + "-bmc | grep 'mac=' | awk -F= '{print $NF}'", shell=need_sh(), stderr=subprocess.STDOUT)

					if mac == bmcmac:
					
							subprocess.call("makedhcp -a " + host + "-bmc", shell=need_sh(), stdout=FNULL(), stderr=subprocess.STDOUT)	
							print("Complete: " + host + "-bmc MAC address has been bound.")

							subprocess.call("psh" + host + " ipmitool user set name 2 admin", shell=need_sh(), stdout=FNULL(), stderr=subprocess.STDOUT)
							subprocess.call("psh" + host + " ipmitool user set password 2 Passw0rd!", shell=need_sh(), stdout=FNULL(), stderr=subprocess.STDOUT)
							subprocess.call("psh" + host + " ipmitool channel setaccess 2 2 link=on ipmi=on callin=on privilege=4", shell=need_sh(), stdout=FNULL(), stderr=subprocess.STDOUT)
							subprocess.call("psh" + host + " ipmitool user enable 2", shell=need_sh(), stdout=FNULL(), stderr=subprocess.STDOUT)
							print("Complete: " + host + " Username and password configured.")

					subprocess.call("psh " + host + " ipmitool lan set 2 ipsrc dhcp", shell=need_sh(), stdout=FNULL(), stderr=subprocess.STDOUT)
					subprocess.call("psh " + host + " ipmitool mc reset cold", shell=need_sh(), stdout=FNULL(), stderr=subprocess.STDOUT)
					print("Complete: " + host + " IPMI DHCP enabled.")
				except(subprocess.CalledProcessError) as error:

					print(error.output)
					sys.exit()
				
			else:

				print("Ed hasn't added manufacturer for node " + host + ". SHAME SHAME SHAME! ")

		else:	

			print("ERROR: Can not ping system " + host + "!!!")

	sys.exit()

def main():

    parser = argparse.ArgumentParser(description='Automate BMC mac binding and enable DHCP.')
    parser.add_argument("noderange", metavar="<noderange>", help='groups or node range IE: node1,node2,node3 | rack1')
    parser.add_argument("-b", "--bmcbind", action='store_true', help='bind host\'s BMC mac to BMC host definition.')
    args = parser.parse_args()

    try:

        hosts = subprocess.check_output("nodels " + args.noderange, shell=True, stderr=subprocess.STDOUT).split()

        if args.bmcbind == True:

            if args.bmcbind:

                bindbmc(hosts)

        else:

            print( "Error: Must include at least one argument. Type \"inv.py -h\" or --help for more information.")

    except (subprocess.CalledProcessError) as error:

        print(error.output)
        sys.exit()

if __name__ == "__main__":

    main()