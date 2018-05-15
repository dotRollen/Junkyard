import sys, paramiko, time, argparse

# CHANGE WHEN IOS IMAGE CHANGES
IOS_IMAGE_NAME = 'isr4300-universalk9.16.03.04.SPA.bin'

class ExpectTimeout(Exception):
    def __init__(self, cmd, expect_string, timeout):
        self.cmd = cmd
        self.expect_string = expect_string
        self.timeout = timeout

def expect(remote_conn, expect_string, timeout=10):
    #print '[debug] expect: entering'

    # Set timeout time to now plus <timeout> seconds
    timeout = time.time() + timeout

    # Get initial output from command
    output = remote_conn.recv(1000)
    #print '[debug] expect: initial output: {}'.format(output)
    # Loop until we find the specified string or hit the timeout
    while True:
        if expect_string in output:
            #print '[debug] expect: found string'
            return True

        elif time.time() > timeout:
            #print '[debug] expect: timed out'
            raise ExpectTimeout('none', expect_string, timeout)

        else:
            #print '[debug] expect: waiting for {}'.format(expect_string)
            time.sleep(1)
            output += remote_conn.recv(1000) 

def send_expect(remote_conn, cmd_list, expect_string, timeout=10):
    #print '[debug] send expect: entering'
    #print '[debug] send expect: starting cmds - cmdlist={}'.format(cmd_list)
    # Send command to client shell
    for cmd in cmd_list:
        #print '[debug] send expect: send cmd: {}'.format(cmd)
        remote_conn.send(cmd)
        time.sleep(1)

    time.sleep(2)
    # Set timeout time to now plus <timeout> seconds
    timeout = time.time() + timeout

    # Get initial output from command
    output =  remote_conn.recv(1000)
    #print '[debug] send expect: initial output: {}'.format(output)
    # Loop until we find the specified string or hit the timeout
    while True:
        #print '[debug] send expect: waiting for {}'.format(expect_string)
        if expect_string in output:
            #print '[debug] send expect: found string'
            return True

        elif time.time() > timeout:
            #print '[debug] send expect: timed out'
            raise ExpectTimeout(cmd_list, expect_string, timeout)

        else:
            #print '[debug] send expect: waiting for {}'.format(expect_string)
            time.sleep(1)
            output += remote_conn.recv(1000) 


def disable_paging(remote_conn):
    '''Disable paging on a Cisco device'''

    remote_conn.send("terminal length 0\n")
    time.sleep(1)

    # Clear the buffer on the screen
    output = remote_conn.recv(1000)

    return output

def default_paging(remote_conn):
    '''Disable paging on a Cisco device'''

    remote_conn.send("terminal no length\n")
    time.sleep(1)

    # Clear the buffer on the screen
    output = remote_conn.recv(1000)

    return output

def connect_to_port(remote_conn, port):
    if int(port) > 0 and int(port) <= 48:
        remote_conn.send("\n")
        remote_conn.send('pmshell -l port{}\n'.format(port))
        time.sleep(3)
        #remote_conn.send(' \n')
        #time.sleep(1)

def copy_tftp(client_shell, filename, destination_path):
    copy_cmd = "copy tftp://192.168.2.244/cisco/{} {}\n".format(filename, destination_path)
    client_shell.send(copy_cmd)
    time.sleep(2)

    output = client_shell.recv(1000)
    if "Destination filename" in output:
        client_shell.send('\n')
        time.sleep(1)

    output = client_shell.recv(1000)
    if '%Warning:There is a file already existing with this name' in output:
        print 'File "{}" already exists in "{}". Skipping.'.format(filename, destination_path)
        client_shell.send('n')
        time.sleep(1)
        return True
    
    time.sleep(2)
    output = client_shell.recv(1000)
    if 'bytes copied in' in output:
        print 'Downloading file "{}" to "{}"'.format(filename, destination_path)
        print 'Download of "{}" complete.'.format(filename) 
        return True

    elif 'Loading' in output:
        print 'Downloading file "{}" to "{}"'.format(filename, destination_path)
        time.sleep(5)
        output = client_shell.recv(1000)
        while not '/sec' in output:
            time.sleep(5)
            output += client_shell.recv(1000)
        print 'Download of "{}" complete.'.format(filename) 
        return True
    else:
        return False

def create_session(opengear_num, opengear_port, username, password):
    
    port = 22

    OPENGEAR_MAPPING = {
        '1': '192.168.2.247',
        '2': '192.168.2.248',
        '3': '192.168.2.249'
    }

    if not opengear_num or not opengear_port:
        return False
    
    opengear_ip = OPENGEAR_MAPPING[str(opengear_num)]

    try:
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.WarningPolicy)

        # Create ssh session to opengear
        client.connect(opengear_ip, port=port, username=username, password=password)
        print "SSH connection established to {}.".format(opengear_ip)

    except:
        return False
    
    try:
        # Create interactive shell so we can send multiple commands
        client_shell = client.invoke_shell()
        print "Interactive shell opened to {}.".format(opengear_ip)    

        # Strip the initial router prompt
        output = client_shell.recv(1000)

        # Start session to appliance on specified opengear port
        connect_to_port(client_shell, opengear_port)
        
        # Make sure we get a prompt
        client_shell.send('\r')
        time.sleep(1)

        return client, client_shell

    except:
        client.close()
        return False


def configure_device(opengear_num, opengear_port, config_file_path, username='root', password='default'):

    try:
        session = create_session(opengear_num, opengear_port, username=username, password=password)
        client, client_shell = session

        if not session:
            print 'Failed to create session. Terminating.'
            exit(-1)

        initial_output = client_shell.recv(1000)

        if 'Would you like to enter the initial configuration dialog?' in initial_output:
            print 'Skipping initial configuration dialog.'
            client_shell.send('no\n')
            time.sleep(2)
            client_shell.send('\r\n')
            time.sleep(40)
            client_shell.send('\r\n')
            time.sleep(3)

        elif 'assword' in initial_output:
            print 'Logging in.'
            client_shell.send('mcl1_mc\r')
            time.sleep(2)

            if 'failed' in client_shell.recv(1000):
                print 'Login failed. Ending.'
                return 'Login failed. Ending.'

        
        client_shell.send('\r\n')
        time.sleep(3)
        # Enter priv exec
        if '>' in client_shell.recv(1000):
            print 'Elevating to priv exec.'
            client_shell.send('en\n')
            time.sleep(1)



        # Disable interactive paging so we get all lines at once
        print 'Disabling paging.'
        disable_paging(client_shell)

        
        # Most customer configs do this for us.
        client_shell.send('configure terminal\n')
        
        # Open specified file and send it line by line to the appliance.
        
        print 'Sending configuration.'
        with open(config_file_path, 'r') as config_file:
            for command in config_file:
                if 'hostname' in command:
                    HOSTNAME = command.split(' ')[1]
                    print 'Found hostname: {}'.format(HOSTNAME)
                    client_shell.send(command.strip() + '\n')
                    time.sleep(.25)
                elif 'license accept end user agreement' in command or 'license boot suite FoundationSuiteK9' in command:
                    print 'Accepting EULA'
                    client_shell.send(command.strip() + '\n')
                    time.sleep(5)
                    client_shell.send('yes\n')
                    time.sleep(1)
                else:
                    client_shell.send(command.strip() + '\n')
                    time.sleep(.25)

        # Exit config t
        print 'Exiting config t.'
        client_shell.send('end\n')
        time.sleep(.25)

        # Copy config to nvram
        print 'Copying running config to nvram.'
        client_shell.send('copy run start\n')
        time.sleep(1)
        client_shell.send('\n')
        time.sleep(1)
        client_shell.send('\n')
        time.sleep(5)
        

        # Clean buffer so we only get the output we want
        output = client_shell.recv(5000)
        client_shell.send('\n')
        time.sleep(1)
        
        qc_output = ''
        # Get QC data from appliance
        print 'Getting QC data.'
        client_shell.send('show start\n')
        time.sleep(30)
        qc_output += client_shell.recv(100000)
        client_shell.send('show ver\n')
        time.sleep(3)
        qc_output += client_shell.recv(5000)
        client_shell.send('show inv\n')
        time.sleep(3)
        qc_output += client_shell.recv(5000)
        client_shell.send('show plat\n')
        time.sleep(3)
        qc_output += client_shell.recv(5000)
        client_shell.send('show license feature\n')
        time.sleep(3)
        qc_output += client_shell.recv(5000)
        client_shell.send('show ip int br\n')
        time.sleep(3)
        qc_output += client_shell.recv(5000)

        qc_filename = '{}.txt'.format(HOSTNAME.strip())
        with open(qc_filename, 'w') as qc_file:
            for line in qc_output.splitlines():
                if not line.isspace():
                    qc_file.write(line + '\n')
    
    except ExpectTimeout as e:
        print 'Expect failed to find "{}" in output of command "{}" within {} seconds.'.format(e.expect_string, e.cmd, e.timeout)
        return

    finally:
        print 'Cleaning up.'       
        default_paging(client_shell)
        # Exit console session
        client_shell.send('exit\n')
        time.sleep(.5)
        client_shell.send('end\n')
        client.close()
        print 'Complete.'


def update_device(opengear_num, opengear_port, ios_image, username='root', password='default'):

    try:
        session = create_session(opengear_num, opengear_port, username=username, password=password)
        client, client_shell = session

        if not session:
            print '[O{}P{}] Failed to create session. Terminating.'.format(opengear_num, opengear_port) 
            exit(-1)

        inital_output = client_shell.recv(1000)

        if 'Would you like to enter the initial configuration dialog?' in inital_output:
            print '[O{}P{}] Skipping initial configuration dialog.'.format(opengear_num, opengear_port) 
            client_shell.send('no\n')
            time.sleep(2)
            client_shell.send('\r\n')
            print '[O{}P{}] Waiting for device to initializate.'.format(opengear_num, opengear_port) 
            time.sleep(40)
            client_shell.send('\r\n')
            print '[O{}P{}] Device standing by.'.format(opengear_num, opengear_port) 
            time.sleep(3)

        elif 'assword' in inital_output:
            print '[O{}P{}] Logging in.'.format(opengear_num, opengear_port) 
            client_shell.send('mcl1_mx\n')
            time.sleep(2)
            if 'failed' in client_shell.recv(1000):
                print '[O{}P{}] Login failed. Ending.'.format(opengear_num, opengear_port) 
                return '[O{}P{}] Login failed. Ending.'.format(opengear_num, opengear_port) 
        
        client_shell.send('\r\n')
        time.sleep(3)
        # Enter priv exec
        if '>' in client_shell.recv(1000):
            print '[O{}P{}] Elevating to priv exec.'.format(opengear_num, opengear_port) 
            client_shell.send('en\n')
            time.sleep(1)

        # Disable interactive paging so we get all lines at once
        print '[O{}P{}] Disabling paging.'.format(opengear_num, opengear_port) 
        disable_paging(client_shell)

        # Most customer configs do this for us.
        #client_shell.send('configure terminal\n')
        
        # Open specified file and send it line by line to the appliance.
        print '[O{}P{}] Setting mgmt0 to DHCP.'.format(opengear_num, opengear_port) 
        dhcp_cmds = ['conf t\n', 'ip tftp blocksize 8192\n', 'int g0\n','ip address dhcp\n', 'no shut\n']
        for command in dhcp_cmds:
            client_shell.send(command + '\n')
            time.sleep(1)

        # Exit config t
        print '[O{}P{}] Exiting config t.'.format(opengear_num, opengear_port) 
        client_shell.send('end\n')
        time.sleep(.25)

        # Clean buffer so we only get the output we want
        output = client_shell.recv(5000)
        client_shell.send('\n')
        time.sleep(.25)        

        # Wait until mgmt0 gets DHCP IP
        print '[O{}P{}] Waiting for GigabitEthernet0 to get DHCP IP.'.format(opengear_num, opengear_port) 
        timeout = time.time() + 100
        while True:
            if 'Interface GigabitEthernet0 assigned DHCP address' in client_shell.recv(5000):
                print '[O{}P{}] Got DHCP IP on GigabitEthernet0.'.format(opengear_num, opengear_port) 
                
                if copy_tftp(client_shell, 'ISR-WAAS-6.2.3c.63.ova', 'harddisk:') and \
                    copy_tftp(client_shell, ios_image, 'bootflash:') and \
                    copy_tftp(client_shell, 'isr4200_4300_rommon_164_3r_SPA.pkg', 'bootflash:') and \
                    copy_tftp(client_shell, 'pp-adv-isr4000-163.2-27-34.0.0.pack', 'bootflash:') and \
                    copy_tftp(client_shell, 'pp-adv-isr4000-163.2-27-27.0.0.pack', 'bootflash:'):

                    print '[O{}P{}] Downloads complete.'.format(opengear_num, opengear_port)                      
                    client_shell.send('config t\n')
                    time.sleep(1)
                    client_shell.send('ip tftp blocksize 512\n')
                    time.sleep(1)
                    client_shell.send('boot system flash bootflash:{}\n'.format(ios_image))
                    time.sleep(2)

                    # Exit config t
                    print '[O{}P{}] Exiting config t.'.format(opengear_num, opengear_port) 
                    client_shell.send('end\n')
                    time.sleep(.25)

                    # Clear buffer
                    client_shell.recv(1000)

                    # Update rommon
                    client_shell.send('upgrade rom-monitor filename bootflash:isr4200_4300_rommon_164_3r_SPA.pkg all\n')
                    time.sleep(5)
                    if 'Upgrade rom-monitor' in client_shell.recv(1000):
                        print '[O{}P{}] Upgrading rommon.'.format(opengear_num, opengear_port) 
                        output = client_shell.recv(1000)
                        while not 'upgrade complete' in output:
                            time.sleep(5)
                            output += client_shell.recv(1000)
                        print '[O{}P{}] Rommon upgrade complete.'.format(opengear_num, opengear_port) 
                    else:
                        print '[O{}P{}] Failed to start rommon upgrade.'.format(opengear_num, opengear_port) 
                        return '[O{}P{}] Failed to start rommon upgrade.'.format(opengear_num, opengear_port) 
                    
                    # Copy config to nvram
                    print '[O{}P{}] Copying running config to nvram.'.format(opengear_num, opengear_port) 
                    client_shell.send('copy run start\n')
                    time.sleep(1)
                    client_shell.send('\n')
                    time.sleep(1)
                    client_shell.send('\n')
                    time.sleep(10)

                    # Clean up
                    print '[O{}P{}] Cleaning up.'.format(opengear_num, opengear_port) 
                    default_paging(client_shell)

                    # Reboot device and wait for it to come back up
                    print '[O{}P{}] Reloading device.'.format(opengear_num, opengear_port) 
                    try:
                        send_expect(client_shell, ('reload\n',), '[confirm]', 5)
                        send_expect(client_shell, ('\n',), 'Reload requested by console.', 10)
                        expect(client_shell, 'Press RETURN to get started!', 600)
                        print '[O{}P{}] Waiting for device initialization.'.format(opengear_num, opengear_port) 
                        time.sleep(60)
                        # Clear buffer
                        client_shell.recv(1000)
                        print '[O{}P{}] Device standing by.'.format(opengear_num, opengear_port) 

                    except ExpectTimeout:
                        print '[O{}P{}] Failed to reload device before ROMMON update.'.format(opengear_num, opengear_port) 
                        return '[O{}P{}] Failed to reload device before ROMMON update.'.format(opengear_num, opengear_port) 
                    
                    # Re-set boot system and reload to complete IOS update
                    client_shell.send('\r\n')
                    time.sleep(3)
                    client_shell.send('\n')
                    time.sleep(3)

                    output = client_shell.recv(1000)
                    # Enter priv exec
                    if '>' in output or not '#' in output:
                        print '[O{}P{}] Elevating to priv exec.'.format(opengear_num, opengear_port) 
                        client_shell.send('en\n')
                        time.sleep(1)

                    # Enter config t    
                    print '[O{}P{}] Entering config t.'.format(opengear_num, opengear_port)                         
                    client_shell.send('config t\n')
                    time.sleep(1)

                    # Set boot system to use new IOS image
                    print "[O{}P{}] Setting boot file.".format(opengear_num, opengear_port) 
                    client_shell.send('boot system flash bootflash:{}\n'.format(ios_image))
                    time.sleep(2)

                    # Exit config t
                    print '[O{}P{}] Exiting config t.'.format(opengear_num, opengear_port) 
                    client_shell.send('end\n')
                    time.sleep(.25)

                    # Copy config to nvram
                    print '[O{}P{}] Copying running config to nvram.'.format(opengear_num, opengear_port) 
                    client_shell.send('copy run start\n')
                    time.sleep(1)
                    client_shell.send('\n')
                    time.sleep(1)
                    client_shell.send('\n')
                    time.sleep(10)

                    # Reboot device and wait for it to come back up
                    print '[O{}P{}] Reloading device.'.format(opengear_num, opengear_port) 
                    try:
                        send_expect(client_shell, ['reload\n'], '[confirm]', 5)
                        send_expect(client_shell, ['\n'], 'Reload requested by console.', 5)
                        expect(client_shell, 'Press RETURN to get started!', 600)
                        print '[O{}P{}] Waiting for device initialization.'.format(opengear_num, opengear_port) 
                        time.sleep(60)
                        # Clear buffer
                        client_shell.recv(1000)

                    except ExpectTimeout:
                        print '[O{}P{}] Failed to reload device before IOS update.'.format(opengear_num, opengear_port) 
                        return '[O{}P{}] Failed to reload device before IOS update.'.format(opengear_num, opengear_port) 
                    
                    print "[O{}P{}] Update Complete.".format(opengear_num, opengear_port) 
                    return "[O{}P{}] Update Complete.".format(opengear_num, opengear_port) 

                else:
                    print '[O{}P{}] Failed to download files.'.format(opengear_num, opengear_port) 
                    return '[O{}P{}] Failed to download files.'.format(opengear_num, opengear_port) 

            elif time.time() > timeout:
                print '[O{}P{}] Failed to get DHCP in time, check switchport VLAN and spanning-tree mode.'.format(opengear_num, opengear_port) 
                return '[O{}P{}] Failed to get DHCP in time, check switchport VLAN and spanning-tree mode.'.format(opengear_num, opengear_port) 

            else:
                time.sleep(5)                 

    finally:        
        # Exit console session
        client.close()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='KistuNet - A Network Appliance Automation Toolkit')

    parser.add_argument("-o", "--opengear", help='Number of OpenGear switch to target.')
    parser.add_argument("-p", "--port", help='Serial port number to connect to.')
    parser.add_argument("--username", help='OpenGear username to use.')
    parser.add_argument("--password", help='OpenGear password to use.')
    parser.add_argument("-c", "--config", help='Configure the target device.')
    parser.add_argument("-u", "--update", action='store_true', help='Update the target device.')

    args = parser.parse_args()

    if not args.opengear:
        print 'You must specify the number of the OpenGear switch to connect to.'

    elif not args.port:
        print 'You must specify the port number on the OpenGear switch to connect to.'

    else:
        if not args.username:
            username = 'root'

        if not args.password:
            password = 'default'

        if args.update:
            update_device(args.opengear, args.port, IOS_IMAGE_NAME, username, password)

        if args.config:        
            configure_device(opengear_num=args.opengear, opengear_port=args.port, config_file_path=args.config, username=username, password=password)  


