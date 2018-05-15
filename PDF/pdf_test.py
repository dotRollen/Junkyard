import argparse
import datetime
import os
import sys
import json
import openpyxl
import dateutil.parser
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdftypes import resolve1

def parse_order_pdf(pdf_path):

    fp = open(pdf_path, 'rb')

    order_dict = {
        'sales_order': '',
        'pk_ticket': '',
        'customer_name': '',
        'comments': '',
        'today': '',
        'tech': '',
        'device_1': {
            'device_model': None,
            'type': None,
            'quantity': 0
        },
        'device_2': {
            'device_model': None,
            'type': None,
            'quantity': 0
        },
        'device_3': {
            'device_model': None,
            'type': None,
            'quantity': 0
        },
        'device_4': {
            'device_model': None,
            'type': None,
            'quantity': 0
        },
        'services': {
            'image': False,
            'material_removed': False,
            'password_set': False,
            'domain_join': False,
            'bundle_kitting': False,
            'logged_in': False,
            'hardware_added': False,
            'asset_tag': False,        
            'bios_change': False,
            'ac_adapter': False,
            'units_cleaned': False,
            'restarted': False,
            'documentation': False,
            'name_change': False,
            'etching': False,
            'misc_accessories': False,
            'apps_winconfig': False,
            'checked_out': False
        }    
    }

    parser = PDFParser(fp)
    doc = PDFDocument(parser)
    fields = resolve1(doc.catalog['AcroForm'])['Fields']
    for i in fields:
        field = resolve1(i)
        name, value = field.get('T'), field.get('V')
        if name in order_dict:
            if name == 'today':
                order_dict[name] = dateutil.parser.parse(value).strftime('%Y-%m-%d')
            else:
                order_dict[name] = value.strip()
        elif value and ('device_model' in name or 'type' in name or 'quantity' in name):
            device_split = name.rsplit('_', 1)
            order_dict['device_' + device_split[1]][device_split[0]] = value
        elif value and value == 'X':
            order_dict['services'][name] = True

    return order_dict


def generate_order_entry(order_dict):
    order_entry = []

    order_entry.append(order_dict['tech'])
    order_entry.append(order_dict['customer_name'])
    order_entry.append(order_dict['sales_order'])

    device_quantity = int(order_dict['device_1']['quantity']) \
                    + int(order_dict['device_2']['quantity']) \
                    + int(order_dict['device_3']['quantity']) \
                    + int(order_dict['device_4']['quantity'])

    order_entry.append(device_quantity)

    image, config, asset_tag = (False, False, False)
    for service, required in order_dict['services'].iteritems():
        if required and service == 'image':
            image = True
        elif required and service == 'asset_tag':
            asset_tag = True
        elif required and (service == 'bios_change' or service == 'domain_join' or service == 'name_changed'):
            config = True

    if image and not config:
        order_entry.append('YES')
    else:
        order_entry.append('NO')

    if not image and not config:
        order_entry.append('YES')
    else:
        order_entry.append('NO')

    if image and config:
        order_entry.append('YES')
    else:
        order_entry.append('NO')

    order_entry.append(order_dict['today'])

    return order_entry


def create_order_workbook(order_data, output_filename):
    wb = openpyxl.Workbook()
    
    orders_sheet = wb.active
    orders_sheet.title = 'ORDERS_TEST'
    orders_sheet_headers = ['Technician', 'Customer Name', 'Sales Order', 'QTY', 'Imaging Only?', 'Asset Tag Only?', 'Imaging + Config', 'Date']
    orders_sheet.append(orders_sheet_headers)

    for order in order_data:
        orders_sheet.append(generate_order_entry(order))

    for col in orders_sheet.columns:
        max_length = 0
        column = col[0].column
        for cell in col:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(cell.value)
            except:
                pass
        adjusted_width = (max_length + 2)
        orders_sheet.column_dimensions[column].width = adjusted_width

    if not output_filename:
        output_filename = 'PDF_OUTPUT_{}.xlsx'.format(datetime.date.today().strftime('%Y-%m-%d'))

    wb.save(filename = output_filename)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='KistuUtils for Gaia')
    parser.add_argument("target_directory", metavar="<target_directory>", help='Directory containing order PDFs to parse.')
    parser.add_argument("-o", "--outputfile", help='Output file name. (Default: PDF_OUTPUT_<YEAR-MONTH-DAY>.xlsx)')
    args = parser.parse_args()

    if not os.path.isdir(args.target_directory):
        print 'DirectoryError: {} either does not exist or is not a directory.'

    parsed_order_details = []
    for order_file in os.listdir(args.target_directory):
        print 'Attempting to parse file: {}'.format(order_file)
        order_file_path = os.path.join(sys.argv[1], order_file)
        parsed_order_details.append(parse_order_pdf(order_file_path))
        print 'Finished with file: {}'.format(order_file)

    print '{} files parsed.'.format(len(parsed_order_details))
    print 'Generating spreadsheet data.'
    create_order_workbook(parsed_order_details, args.outputfile)
    print 'Finished.'
    os.system('pause')
