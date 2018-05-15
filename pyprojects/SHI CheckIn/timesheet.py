import sqlite3
from datetime import datetime
from checkin_inventory import var

def device_checkout(cursor, employee_dict):
 
    try:

        for index, device in enumerate(employee_dict['devices']):

            if is_checked_in(cursor, employee_dict):

                cursor.execute(''' UPDATE timesheet
                    SET check_out = :check_in,
                    WHERE id = :last_entry ''',
                    {'check_out': str(datetime.datetime.now()),
                    'last_entry': device['last_entry']
                    }
                )

            else:
            
                cursor.execute(''' INSERT INTO timesheet
                        (employee_id, 
                        device_id, 
                        check_out)
                    VALUES
                        (:employee_id,
                        :device_id, 
                        :check_out)
                    ''',
                    {
                        'employee_id':employee_dict.get('employee').get('id'), 
                        'device_id': device['id'],
                        'check_out': str(datetime.now())
                    }
                )

    except:
        raise

def device_checkin(cursor, employee_dict):
    
    try:

        for index, device in enumerate(employee_dict['devices']):

            if is_checked_out(cursor, employee_dict):

                cursor.execute(''' UPDATE timesheet
                    SET check_in = :check_in,
                    WHERE id = :last_entry ''',
                    {'check_in': str(datetime.datetime.now()),
                    'last_entry': device['last_entry']}
                )

            else:
            
                cursor.execute('''
                    INSERT INTO timesheet
                        (employee_id, 
                        device_id, 
                        check_in)
                    VALUES
                        (:employee_id,
                        :device_id, 
                        :check_in)
                    ''',
                    {
                        'employee_id':employee_dict.get('employee').get('id'), 
                        'device_id': device['id'],
                        'check_in':  str(datetime.now())
                    }
                )

    except:
        raise

def is_checked_in(cursor, employee_dict):
    
    try:        

        for index, device in enumerate(employee_dict['devices']):
            
            cursor.execute('''
                SELECT * FROM timesheet 
                WHERE employee_id = :employee_id AND device_id = :device_id
                ''',

                {
                    'employee_id':employee_dict.get('employee').get('id'),
                    'device_id':device['id']
                }
            )

            try:

                device['last_entry'] = cursor.fetchall()[-1][0]
                last_entry = cursor.fetchall()[-1]

            except IndexError:
                continue

        if last_entry[-1] and not last_entry[-2]:

            return employee_dict
                
    except:
        raise

def is_checked_out(cursor, employee_dict):

    try:
        for index, device in enumerate(employee_dict['devices']):
            
            cursor.execute('''
                SELECT * FROM timesheet 
                WHERE employee_id = :employee_id AND device_id = :device_id
                ''',

                {'employee_id':employee_dict.get('employee').get('id'),
                 'device_id':device['id']
                }
            )

            try:                
                device['last_entry'] = cursor.fetchall()[-1][0]
                last_entry = cursor.fetchall()[-1]

            except IndexError:
                continue

            try:            
                if last_entry[-2] and not last_entry[-1]:
                    return last_entry[0]

            except IndexError:
                continue

    except:
        raise

def device_lookup(cursor, employee_dict):

    try:

        for index, device in enumerate(employee_dict['devices']):

            cursor.execute('''
                    SELECT id FROM device WHERE serial = :serial OR asset_tag = :asset_tag
                ''', 
                device
            )
            
            employee_dict['devices'][index]['id'] = cursor.fetchone()[0]

        return employee_dict

    except:
        raise

def device_entry(cursor, employee_dict):

    try:

        for index, device in enumerate(employee_dict['devices']):

            cursor.execute('''
                    INSERT INTO device(model, serial, asset_tag, employee_id)
                    SELECT :model, :serial, :asset_tag, :employee_id
                    WHERE NOT EXISTS(
                        SELECT 1 FROM device WHERE model = :model AND serial = :serial AND asset_tag = :asset_tag 
                )''',
                {
                    'model':device.get('model'), 
                    'serial':device.get('serial'), 
                    'asset_tag':device.get('asset_tag'), 
                    'employee_id':employee_dict.get('employee').get('id')
                }
            )

        return employee_dict

    except:
        raise

def list_employees(cursor):

    try:
        
        for row in cursor.execute('''SELECT * FROM employee ORDER BY last_name'''):
            print(row)

    except: 
        raise

def employee_lookup(cursor, employee_dict):

    try:
        
        cursor.execute('''
            SELECT id FROM employee WHERE name = :first_name AND last_name = :last_name
            ''', 
            employee_dict['employee']
        )

        employee_dict['employee']['id'] = cursor.fetchone()[0]

        return employee_dict

    except: 
        raise

def employee_entry(cursor, employee_dict):

    try:
        cursor.execute('''
        INSERT INTO employee(name, last_name, email, phone)
        SELECT :first_name, :last_name, :email, :phone 
        WHERE NOT EXISTS(
            SELECT 1 FROM employee WHERE name = :first_name AND last_name = :last_name AND email = :email
        )''',
        employee_dict['employee']
        )

    except:
        raise

def db_setup(cursor):

    try:
        cursor.executescript('''
        CREATE TABLE 
        IF NOT EXISTS employee (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name TEXT,
            last_name TEXT,
            email TEXT,
            phone TEXT
        );

        CREATE TABLE 
        IF NOT EXISTS device (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            model TEXT, 
            serial TEXT, 
            asset_tag TEXT,
            employee_id INTEGER,
            FOREIGN KEY (employee_id) REFERENCES employee(id)
        );

        CREATE TABLE 
        IF NOT EXISTS timesheet (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER,
            device_id INTEGER,
            check_in TEXT,
            check_out TEXT,
            FOREIGN KEY (employee_id) REFERENCES employee(id),
            FOREIGN KEY (device_id) REFERENCES device(id)
        )
        ''')

    except:
        raise

def db_connect(sqlite_file):

    try:
    
        db = sqlite3.connect(sqlite_file)
        cursor = db.cursor()

        return db, cursor

    except:
        raise

def main():

    db, cursor = db_connect('db\database.sqlite')

    # employee_dict = {
    #     'employee':{
    #         'first_name':'Edward', 'last_name':'Nunez', 'email':'edward_nunez@shi.com', 'phone':'6096088525'
    #     }, 
    #     'devices': [
    #         {'model':'HP Laptop', 'serial':'123', 'asset_tag':'456'}, 
    #         {'model':'Surface Tablet', 'serial':'789', 'asset_tag':'000'}
    #     ]
    # }

    with db:
        db_setup(cursor)

        list_employees(cursor)
        
        # for index, employee in enumerate(var):

            # employee_dict = {
            #     'employee':{
            #         'first_name':'', 'last_name':'', 'email':'', 'phone':''
            #     }, 
            #     'devices': []
            # }

            # employee_dict['employee']['first_name'] = employee[0]
            # employee_dict['employee']['last_name'] = employee[1]
            # employee_dict['devices'].append({'model': employee[2], 'serial': employee[3], 'asset_tag': employee[4]})

            # employee_entry(cursor, employee_dict)
            # employee_lookup(cursor, employee_dict)
            # device_entry(cursor, employee_dict)
            # device_lookup(cursor, employee_dict)
            # device_checkin(cursor, employee_dict)
            
if __name__ == '__main__':
    main()