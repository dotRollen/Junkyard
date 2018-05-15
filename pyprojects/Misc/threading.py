#! python2 

import subprocess, os, platform, re, time, sys, argparse, openpyxl

def ping(host):
	ping_str = "-n 1" if platform.system().lower() == "windows" else "-c 1"
	args = "ping " + " " + ping_str + " " + host

	return subprocess.call(args, shell=need_sh(), stdout=FNULL, stderr=subprocess.STDOUT) == 0

def need_sh():
	return False if platform.system().lower() == "windows" else True

def FNULL():
	return open(os.devnull, 'w')

class getinventory(hosts):
	def getmac(hosts):
		for host in hosts:
			if ping(host):
				try:
					print "Processing " + host + " hardware inventory..."
					rawmodel = subprocess.check_output(args, stderr=subprocess.STDOUT, shell=need_sh()).strip('\r\n')
					SerialN = subprocess.check_output(argsSN, stderr=subprocess.STDOUT, shell=need_sh()).strip('\r\n')
					MAC1 = subprocess.check_output(argsM1, stderr=subprocess.STDOUT, shell=need_sh()).strip('\r\n')
					MAC2 = subprocess.check_output(argsM2, stderr=subprocess.STDOUT, shell=need_sh()).strip('\r\n')
					MAC3 = subprocess.check_output(argsM3, stderr=subprocess.STDOUT, shell=need_sh()).strip('\r\n')
					MAC4 = subprocess.check_output(argsM4, stderr=subprocess.STDOUT, shell=need_sh()).strip('\r\n')
					MAC10G1 = subprocess.check_output(args10M1, stderr=subprocess.STDOUT, shell=need_sh()).strip('\r\n')
					MAC10G2 = subprocess.check_output(args10M2, stderr=subprocess.STDOUT, shell=need_sh()).strip('\r\n')
					iDRACMAC4 = subprocess.check_output(argsiDRAC, stderr=subprocess.STDOUT, shell=need_sh()).strip('\r\n')
					inv = (host, rawmodel, SerialN, MAC1, MAC2, MAC3, MAC4, MAC10G1, MAC10G2, iDRACMAC4)
					
					writecvs(inv)

				except subprocess.CalledProcessError as error:
					try:
						print error.output.split("\n")[7] + ": " + host
					except:
						nond = error.output.split("\n")
						for error in nond:
							fe = re.search(r'ERROR.*', error)
							if fe:
								print fe.group() + " " + host
			else:
				print "ERROR: Can not ping system " + host + "!!!"

	def  writecvs(inv):

		ws1.append(inv)
		wb.save(filename=dest_filename)

		print(host + " hardware inventory complete")

def bindbmc(hosts):
	for host in hosts:
		if ping(host):
			mac = subprocess.check_output("psh " + host + " ipmitool lan print 1|grep -io '[0-9A-F]\{2\}\(:[0-9A-F]\{2\}\)\{5\}' |egrep -m 1 '\w+'",
			stderr=subprocess.STDOUT, shell=need_sh(), stdout=FNULL())
			subprocess.call("chdef " + host + "-bmc mac=" + mac, shell=need_sh(), stdout=FNULL())
			bmcmac = subprocess.check_output("lsdef " + host + "-bmc | grep 'mac=' | awk -F= '{print $NF}'",
			stderr=subprocess.STDOUT, shell=need_sh(), stdout=FNULL())
			if mac == bmcmac:
				subprocess.call('makedhcp -a ' + host + "-bmc", shell=need_sh(), stdout=FNULL())
				print("Complete: " + host + "-bmc MAC address has been bound.")
			else: 
				print("ERROR: MAC address for " + host + "-bmc mac:" + mac)
		else:
			print("ERROR: Can not ping system " + host + "!!!")

	sys.exit()

def main():
	parser = argparse.ArgumentParser(description='Automate BMC mac binding, get hardware and software inventory')
	parser.add_argument("noderange", metavar="<noderange>", 
						help='groups or node range IE: node1,node2,node3 | rack1')
	parser.add_argument("-g", "--getinv", action='store_true',
						help='get hardware and software inventory for Dell R630 and R730xd')
	parser.add_argument( "-b", "--bmcbind", action='store_true',
						help='get hardware and software inventory for Dell R630 and R730xd')
	args = parser.parse_args()
	try:
		hosts = subprocess.check_output("nodels " + args.noderange, stderr=subprocess.STDOUT, shell=True).split()

		if args.getinv == True or args.bmcbind == True:
			
			if args.getinv:
				print("getinv")

			if args.bmcbind:
				bindbmc(hosts)
		else:
			print("Error: Must include at least one argument. Type \"inv.py -h\" or --help for more information.")

	except (subprocess.CalledProcessError) as error:
		print(error.output)
		sys.exit()
    while not workQueue.empty():
   pass
    exitFlag = 1

    for t in threads:
        t.join()
        print "Exiting Main Thread"

if __name__ == "__main__":
	main()