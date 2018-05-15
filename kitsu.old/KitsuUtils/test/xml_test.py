from collections import OrderedDict
import xml.etree.ElementTree as ET
import openpyxl
import os
import re
   
def rack_u_sort(data_list):
    racks = OrderedDict()
    sorted_list = []
    for entry in data_list:
        rack_num = entry[0][1:3]
        if not rack_num in racks:
            racks[rack_num] = []
        racks[rack_num].append(entry)
    
    for rack in sorted(racks.keys()):
        for node in sorted(racks[rack], key=lambda x: x[0][-2:], reverse=True):
            sorted_list.append(node)

    return sorted_list
        




def create_qc_entry(node, file_path):

    qc_list = [node]
    mac_list = [node]

    hwinv_items = [ ('System.Embedded.1', 'BIOSVersionString'),
                    ('System.Embedded.1','LifecycleControllerVersion'),
                    ('RAID.Integrated.1-1', 'ControllerFirmwareVersion') ]

    bios_items =  OrderedDict([('NIC.Slot.2-1-1' , ['LegacyBootProto']),
                               ('NIC.Slot.3-1-1' , ['LegacyBootProto']),
                               ('BIOS.Setup.1-1' , ['BiosBootSeq']),
                               ('iDRAC.Embedded.1', ['NIC.1#Selection', 'IPv4Static.1#DNSFromDHCP', 'IPMISOL.1#Enable', 'IPv4.1#DHCPEnable']),
                               ('System.Embedded.1' , ['ServerPwr.1#PSRedPolicy', 'ServerPwr.1#PSRapidOn']) 
                               ])

    mac_items = [
        ('System.Embedded.1', 'ServiceTag'),
        ('iDRAC.Embedded.1-1#IDRACinfo', 'PermanentMACAddress'),
        ('NIC.Integrated.1-1-1', 'PermanentMACAddress'),
        ('NIC.Integrated.1-2-1', 'PermanentMACAddress'),
        ('NIC.Integrated.1-3-1', 'PermanentMACAddress'),
        ('NIC.Integrated.1-4-1', 'PermanentMACAddress'),
        ('NIC.Slot.2-1-1', 'PermanentMACAddress'),
        ('NIC.Slot.2-2-1', 'PermanentMACAddress'),
        ('NIC.Slot.3-1-1', 'PermanentMACAddress'),
        ('NIC.Slot.3-2-1', 'PermanentMACAddress')
    ]


    raid_set = False
    smart_alerts = []

    try: 
        config = ET.parse('{}/{}-hwinv.xml'.format(file_path, node))
        hwroot = config.getroot()
 
        """for component in hwroot.findall('Component'):
                if component.get('Key') == 'Disk.Virtual.0:RAID.Integrated.1-1':
                    for prop in component.findall('PROPERTY.ARRAY'):
                        if prop.get('NAME') == 'PhysicalDiskIDs':
                            disks = prop.find('VALUE.ARRAY').findall('VALUE')
                            if len(disks) == 2 and 'Disk.Bay.0' in disks[0].text and 'Disk.Bay.1' in disks[1].text:
                                raid_set = True
        """
        for component in hwroot.findall('Component'):
            if component.get('Classname') == 'DCIM_PhysicalDiskView':
                for prop in component.findall('PROPERTY'):
                    if prop.get('NAME') == 'PredictiveFailureState':
                        if not 'Absent' in prop.find('DisplayValue').text:
                            smart_alerts.append(component.get('Key')[:10])    

        for item in mac_items:    
            for component in hwroot.findall('Component'):
                if component.get('Key') == item[0]:
                    for prop in component.findall('PROPERTY'):
                        if prop.get('NAME') == item[1]:
                            mac_list.append(prop.find('VALUE').text)


        for item in hwinv_items:    
            for component in hwroot.findall('Component'):
                if component.get('Key') == item[0]:
                    for prop in component.findall('PROPERTY'):
                        if prop.get('NAME') == item[1]:
                            qc_list.append(prop.find('VALUE').text)
    except:
        print 'Failed to parse hwinv file!'   

    try: 
        config = ET.parse('{}/{}-bios.xml'.format(file_path, node))
        biosroot = config.getroot()

        for key in bios_items:
            for item in bios_items.get(key):
                for component in biosroot.findall('Component'):
                    if key in component.get('FQDD'):
                        for attribute in component.findall('Attribute'):                        
                            if attribute.get('Name') == item:
                                qc_list.append(attribute.text)

    except:
        print 'Failed to parse bios file!'    

    #if raid_set:
    #    qc_list.append('Yes')
    #else:
    #    qc_list.append('NOT SET')

    if len(smart_alerts) > 0:
        qc_list.append(','.join(smart_alerts))
    else:
        qc_list.append('None')

    return qc_list, mac_list


def generate_csv(directory, data_list, mac_list):

    wb = openpyxl.Workbook()
    
    biosSheet = wb.active
    biosSheet.title = 'GAIA Node QC'

    macSheet = wb.create_sheet('MAC and Serial')

    biosColumnTitles = ['Node', 'Bios FW', 'Lifecycle FW', 'PERC FW', '10G NIC BootProto', 'Boot Sequence', 'iDRAC NIC', 'DNS from DHCP', 'IPMI Over LAN', 'iDRAC DHCP', 'PSU Redundancy',
                    'Hot Spare', 'Drives w/ Smart Alerts']

    macColumnTitles = [
        'Node',
        'ServiceTag',
        'iDRAC.Embedded.1-1',
        'NIC.Integrated.1-1-1',
        'NIC.Integrated.1-2-1',
        'NIC.Integrated.1-3-1',
        'NIC.Integrated.1-4-1',
        'NIC.Slot.2-1-1',
        'NIC.Slot.2-2-1'
    ]

    biosSheet.append(biosColumnTitles)
    macSheet.append(macColumnTitles)
    
    for node in rack_u_sort(data_list):
        biosSheet.append(node)

    for node in rack_u_sort(mac_list):
        macSheet.append(node)

    for col in biosSheet.columns:
        max_length = 0
        column = col[0].column # Get the column name
        for cell in col:
            try: # Necessary to avoid error on empty cells
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = (max_length + 2)
        biosSheet.column_dimensions[column].width = adjusted_width

    for col in macSheet.columns:
        max_length = 0
        column = col[0].column # Get the column name
        for cell in col:
            try: # Necessary to avoid error on empty cells
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = (max_length + 2)
        macSheet.column_dimensions[column].width = adjusted_width

    wb.save(filename = '{}/summary.xlsx'.format(directory))


if __name__ == "__main__":
    
    config = ET.parse('hwinv.xml')
    hwroot = config.getroot()

    for item in hwroot.findall("./Component[@Classname='DCIM_VirtualDiskView']"):
        print item.find("./PROPERTY[@NAME='FQDD']/VALUE").text
        for prop in item.findall("./PROPERTY"):
            print "\t", prop.get('NAME'), "=", prop.find("./DisplayValue").text
        print ""
    #ET.dump(item)
