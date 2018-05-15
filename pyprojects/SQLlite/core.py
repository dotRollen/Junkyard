import sqlite3



def database():



if __name__ == '__main__':
    try:
        db = sqlite3.connect('data/db.sqlite3')
        cursor = db.cursor()
        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS
                        users(id INTEGER PRIMARY KEY, name TEXT, email TEXT)
                        ''')
        cursor.execute('''
                        CREATE TABLE IF NOT EXISTS
                        device(id INTEGER PRIMARY KEY, device TEXT, model TEXT, serial TEXT, asset tag TEXT )
                        ''')
        db.commit()

    except Exception as e:
        db.rollback()
        raise e
        
    finally:
        db.close()

    main()
