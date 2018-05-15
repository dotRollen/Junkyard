#!/usr/bin/python
#
#
#

# DO NOT CHANGE THIS LINE!
import subprocess, os, platform, re, time

# BEGIN User Defined Variables
# Make sure to change these variables to match your environment!

# Windows path to racadm.exe.  Please note that you must use forward slashes(/) here!
#CMD = os.path.normpath("C:/Program Files/Dell/SysMgt/idrac/racadm.exe")
# Linux path to racadm binary. 
CMD = "/opt/dell/srvadmin/sbin/racadm"
USERID = "root"
PASSWD = "calvin"
XML_LIST1 = "R730xd_config_V6.xml"
XML_LIST2 = "R630_config_V3.xml"
MODEL1 = "R730xd"
MODEL2 = "R630"
DM = "PowerEdge"
NFS = "192.168.70.254:/dell"
# Change to the 3 digit code for the location
LOC = "ash"
# Change to the Rack location
RACK = "r01"
# The node file list should be in the same directory as this script; one node number per line ONLY, no comments, no header. ie: N01 would be listed as 01.
IPLIST = "node_list.txt"
# END User Defined Variables


# DO NOT CHANGE ANYTHING BELOW THIS LINE!!!!!
input_file = open(IPLIST)

FNULL = open(os.devnull, 'w')

def ping(host):

    ping_str = "-n 1" if  platform.system().lower()=="windows" else "-c 1"
    args = "ping " + " " + ping_str + " " + "n" + host + "-bmc"
    need_sh = False if  platform.system().lower()=="windows" else True

    # Ping
    return subprocess.call(args, shell=need_sh, stdout=FNULL, stderr=subprocess.STDOUT) == 0

for line in input_file:
	line = line.rstrip('\r\n')
	if ping(line):
		#get model
        args = CMD + " -r n" + line + "-bmc -u " + USERID + " -p " + PASSWD + " get BIOS.SysInformation.systemmodelName"
        need_sh = False if  platform.system().lower()=="windows" else True

		try:
			rawmodel = subprocess.check_output(args, stderr=subprocess.STDOUT, shell=need_sh)
			if re.findall(MODEL1,rawmodel):
				XML_FILE = XML_LIST1
			elif re.findall(MODEL2,rawmodel):
				XML_FILE = XML_LIST2
			else:
				wmodel = re.match(DM,rawmodel)
				wmodel = rawmodel.split('=')[2]
				print "ERROR: System is not a known model type. Model detected as " + wmodel.rstrip('\r\n') + ".  " + line + "-bmc"
				continue
            args = CMD + " -r n" + line + "-bmc -u " + USERID + " -p " + PASSWD + "jobqueue delete --all" 
            args1 = CMD + " -r n" + line + "-bmc -u " + USERID + " -p " + PASSWD + " set -t xml -f " + XML_FILE + " -l " + NFS + ' -b "graceful"'
	        args2 = CMD + " -r n" + line + "-bmc -u " + USERID + " -p " + PASSWD + " set System.Location.DataCenter "  + LOC          
			args3 = CMD + " -r n" + line + "-bmc -u " + USERID + " -p " + PASSWD + " set System.Location.Rack.Name " + RACK 
        	args4 = CMD + " -r n" + line + "-bmc -u " + USERID + " -p " + PASSWD + " set System.Location.Rack.Slot " + line 

			subprocess.call(args, shell=need_sh)	
			subprocess.call(args2, shell=need_sh)	
			subprocess.call(args3, shell=need_sh)	
			subprocess.call(args4, shell=need_sh)	
			time.sleep(15)
			subprocess.call(args1, shell=need_sh)
		except subprocess.CalledProcessError as e:
			try:
				print e.output.split("\n")[7] + ": " + line + "-bmc"
			except:
				nond =  e.output.split("\n")
				for error in nond:
					fe = re.search(r'ERROR.*',error)
					if fe:
						print fe.group() + " " + line + "-bmc"
	else:
		print "ERROR: Can not ping system. " + line + "-bmc"
