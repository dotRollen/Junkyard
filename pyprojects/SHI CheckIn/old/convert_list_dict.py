from checkin_inventory import var


def main():

    for index, employee in enumerate(var):
        
        employee_dict = {
            'employee':{
                'first_name':'', 'last_name':'', 'email':'', 'phone':''
            }, 
            'devices': []
        }

        employee_dict['employee']['first_name'] = employee[0]
        employee_dict['employee']['last_name'] = employee[1]
        employee_dict['devices'].append({'model': employee[2], 'serial': employee[3], 'asset_tag': employee[4]})

        print(employee_dict)

if __name__ == '__main__':
    main()