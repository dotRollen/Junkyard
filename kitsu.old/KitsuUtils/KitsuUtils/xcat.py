""" Implements wrappers for xCAT functions and interaction

    Todo:
        * Add additional function wrappers as needed
"""

import os
import subprocess

def nodels(groupname):
    """ Returns the members of the specified xCAT group

        Args:
            groupname (string): xCAT node or group to search

        Returns:
            list: List of hostnames in the specified xCAT group or None if
    """

    cmd = 'nodels {group}'.format(group=groupname)

    with open(os.devnull, 'w') as devnull:
        try:
            return subprocess.check_output(cmd.split(), stderr=devnull).splitlines()
        except:
            return None

def psh(group, cmd):
    """ Sends parallel command to specified xCAT group or node """

    pcmd = 'psh {g} {c}'.format(g=group, c=cmd)
    try:
        return subprocess.check_output(pcmd, shell=True, stderr=subprocess.STDOUT)
    except:
        return None

def in_genesis(node):
    cmd = "echo '$PS1'"
    if 'genesis' in str(psh(node, cmd)).lower():
        return True
    else:
        return False

def xdcp(group, source, destination, pull=False):
    """ Executes an xCAT parallel copy """

    if pull:
        pcmd = 'xdcp {g} -P -R {s} {d}'.format(g=group, s=source, d=destination)
    else:
        pcmd = 'xdcp {g} {s} {d}'.format(g=group, s=source, d=destination)

    try:
        return subprocess.check_output(pcmd, shell=True).splitlines()
    except:
        return None

def chdef(obj_type='node', group=None, options=None):
    
    """ List node definitons for <noderange>

        Args:
            obj_type = Define object type, available types are:
                        auditlog, boottarget, eventlog, firmware, group, kit, kitcomponent, 
                        kitrepo, monitoring, network, node, notification, osdistro, osdistroupdate, 
                        osimage, pdu, policy, rack, route, site, taskstate, zone
            group    = <noderange>

            options  = add table option for xCAT definition.
    """
    
    cmd = 'chdef -t {t} '.format(t=obj_type)

    if group:
        cmd += '-o {g} '.format(g=group)
    else:
       return None

    cmd += options

    try:
        return subprocess.check_output(cmd, shell=True).splitlines()
    except:
        return None


def set_comment(noderange, comment):

    cmd = 'chdef {} usercomment="{}"'.format(noderange, comment)

    try:
        return subprocess.check_output(cmd, shell=True).splitlines()
    except:
        return None

def get_node_property(node, property_name):

    cmd = 'lsdef {} -i {} | grep {} | awk -F"=" \'{{print $2}}\''.format(node, property_name, property_name)

    try:
        return subprocess.check_output(cmd, shell=True)
    except:
        return None


def get_comment(node):

    return get_node_property(node, 'usercomment')

def lsdef(obj_type='node', group=None, grep=None):
    
    """ List node definitons for <noderange>

        Args:
            obj_type = Define object type options are as follow
                        auditlog, boottarget, eventlog, firmware, group, kit, kitcomponent, 
                        kitrepo, monitoring, network, node, notification, osdistro, osdistroupdate, 
                        osimage, pdu, policy, rack, route, site, taskstate, zone
            group    = noderange
    """
    cmd = 'lsdef -t {} '.format(obj_type)

    if group:
        cmd += '-o {g} '.format(g=group)

    if grep:
        cmd += '| {}'.format(grep)

    else:
       return None
    
    try:
        return subprocess.check_output(cmd, shell=True).splitlines()
    except:
        return None

def get_node(node):
    node_output = lsdef(group=node)
    if node_output:
        node_dict = dict(line.strip().split('=') for line in node_output[1:])
        return node_dict
    else:
        return 'Node "{}" does not exist.'.format(node)

def print_node(node):

    node_dict = get_node(node)
    if type(node_dict) is dict:
        print 'Node: {}'.format(node)
        print('\n'.join("  {}: {}".format(k, v) for k, v in node_dict.items()))
    else: 
        print node_dict


def makedhcp(group, delete=False):
    """ Make or delete a DHCP static lease, by default creates DHCP lease.

        Args:
            delete = If true deletes DHCP lease, default is false.
    """
    if delete:
        cmd = 'makedhcp -d {}'.format(group)
    else:
        cmd = 'makedhcp {}'.format(group)
    subprocess.check_output(cmd, shell=True)

def pasu(group, params=None, batch_file=None, grep=None):

    """
        Parallel ASU sets the BIOS configuration or sends settings batch file.

        Args:
            batch_file = File name for batch file.abs
            group      = <noderange>
            command    = "set <command>" for bios setting
    """
    
    cmd = "pasu "

    if batch_file:
        cmd += "-b {b} {g} ".format(b=batch_file, g=group)
        if grep:
            cmd += "| grep {}".format(grep)

        print 'Calling xCAT Command: "{}"'.format(cmd)
        return subprocess.check_output(cmd, shell=True).splitlines()

    elif params:
        cmd += "{g} {p} ".format(g=group, p=params)
        if grep:
            cmd += "| grep {}".format(grep)

        print 'Calling xCAT Command: "{}"'.format(cmd)
        return subprocess.check_output(cmd, shell=True).splitlines()
    

def makeknownhosts(group, delete=False):

    if delete:
        cmd = "makeknownhosts -d {g}".format(group)
    else:
        cmd = "makeknownhosts {g}".format(group)
    
    print 'Calling xCAT Command: "{}"'.format(cmd)
    return subprocess.check_output(cmd, shell=True).splitlines()


def xdsh_script(noderange, script_path, script_args=None):
    
    cmd = 'xdsh {} -e "{}"'.format(noderange, script_path)
    if script_args:
        cmd += ' {}'.format(script_args)

    try:
        return subprocess.check_output(cmd, shell=True).splitlines()
    except:
        return None
