import subprocess
xcatgroup = raw_input("Please enter xCAT group name: ")
try:
    node_list = subprocess.check_output("nodels " + xcatgroup, stderr=subprocess.STDOUT, shell=True).split()
    print(node_list)
except (subprocess.CalledProcessError) as e:
    print e.output
