import sqlite3

db = sqlite3.connect('sqlite.file')

cursor = db.cursor()

big_dictionary = {
    'employee':{
        'name':'Edward', 'last_name':'Nunez', 'email':'edward_nunez@shi.com', 'phone':'6096088525'}, 
    'device1':{
        'model':'HP Laptop', 'serial1':'123', 'asset_tag1':'456'}, 
    'device2':{
        'model':'Surface Tablet', 'serial2':'789', 'asset_tag2':'000'},
}

big_dictionary['employee']['id'] = big_dictionary['device1']['employee_id'] = big_dictionary['device2']['employee_id'] = "2"

db.executescript('''
    CREATE TABLE 
    IF NOT EXISTS employee (
        name TEXT,
        last_name TEXT,
        email TEXT,
        phone TEXT
        )
''')

str = 'employee'

cursor.execute('''INSERT INTO employee VALUES(:name, :last_name, :email, :phone)''', big_dictionary[str])
db.commit()
db.close()


print(big_dictionary['employee'],big_dictionary['device1'],big_dictionary['device2'])


for index, device in enumerate(employee_dict['devices']):
    print 'Index:', index
    print 'Model: {} | Serial: {} | Asset Tag: {}'.format(device['model'], device['serial'], device['asset_tag'])
    employee_dict['devices'][index]['id'] = 100 + index

for device in employee_dict['devices']:
    print 'ID:', device['id'] 