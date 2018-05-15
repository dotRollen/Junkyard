import sys
import json
import os
import platform
import subprocess

def kitsu_log(string, prefix):
    print '[Kitsu][%s] %s' % (prefix, string)

def change_bios_setting(restobj, bios_property, property_value, bios_password=None):
    instances = restobj.search_for_type("Bios.")

    for instance in instances:
        body = {bios_property: property_value}

        response = restobj.rest_patch(instance["href"], body)
        if response.status != 200:
            kitsu_log('Failed to patch setting {%s : %s}' % (bios_property, property_value), current_node)
            return False
        else:
            kitsu_log('Successfully patched setting {%s : %s}' % (bios_property, property_value), current_node)

    return True    

def reset_server(restobj, bios_password=None):
    
    instances = restobj.search_for_type("ComputerSystem.")

    for instance in instances:
        body = dict()
        body["Action"] = "Reset"
        body["ResetType"] = "ForceRestart"

        response = restobj.rest_post(instance["href"], body)
        if response.status != 200:
            kitsu_log('Failed to restart node', current_node)
            return False
        else:
             kitsu_log('Successfully restarted node', current_node)
    
    return True
        
def set_bootmode(restobj, mode, reboot=True):

    valid_options = ("Uefi", "LegacyBios")

    if mode in valid_options:
        success = change_bios_setting(restobj, "BootMode", mode)

        if success and reboot:
            reset_server(restobj)

    else:
        kitsu_log('Invalid boot option specified. Options are: "Uefi/LegacyBios"', current_node)

def remove_ilo_account(restobj, ilo_account_name='admin'):

    instances = restobj.search_for_type("AccountService.")

    for instance in instances:
        response = restobj.rest_get(instance["href"])
        accounts = restobj.rest_get(response.dict["links"]["Accounts"]["href"])

        for account in accounts.dict["Items"]:
            if account["UserName"] == ilo_account_name:
                resp = restobj.rest_delete(account["links"]["self"]["href"])
                if response.status != 200:
                    kitsu_log('Failed to remove iLO Account: "%s"' % ilo_account_name, current_node)
                    return False
                else:
                    kitsu_log('Successfully removed iLO Account: "%s"' % ilo_account_name, current_node)
                    return True
            
    sys.stderr.write("Account not found\n")

def create_session(node, iLO_account='admin', iLO_password='Passw0rd!'):
    try:
        restobj = RestObject(node, iLO_account, iLO_password)
        return restobj
    except:
         kitsu_log('Failed to create session', node)
         return None
