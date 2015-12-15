#!/usr/bin/python2
import sqlite3

# Got some great tips from:
# http://www.pythoncentral.io/introduction-to-sqlite-in-python/

# Class to manage all database operations
class DatabaseBuilder:

    # Create a new database connection _
    def __init__(self, dbfile, dbstruct):
        self.msg = '\n=======__init--() ==='    
        try:
            self.dbfile = dbfile
            self.dbstruct = dbstruct
            self.db = sqlite3.connect(self.dbfile) 
            self.msg += '\nStarted DB'    
            self.build()
        except Exception as e:
            self.msg += '\nERROR: '+str(e)   

    # Build the db and create the structure if it doesn't exist
    def build(self):
        self.msg = '\n====--database build()====='  
        try:
            cursor = self.db.cursor()
            # lets loop through our structure 
            for tablename in self.dbstruct:
                # Check if our table exists
                qry = "SELECT * FROM sqlite_master WHERE type='table' AND name='{}';".format(tablename)
                cursor.execute(qry)
                table = str(cursor.fetchone())
                # It doesn't seem to exist so lets create it
                if table == 'None':
                    fieldlist = s = ''
                    for fieldname in self.dbstruct[tablename]:
                        fieldtype = self.dbstruct[tablename][fieldname]
                        if fieldlist != '': s = ','
                        fieldlist += '{}{} {}'.format(s, fieldname,fieldtype)
                    qry = 'CREATE TABLE {0} ({1})'.format(tablename, fieldlist)
                    cursor.execute(qry)
                    self.msg += '\nBuilt a new database'
                else:
                    self.msg += '\nFound "{}" so didn\'t recreate it'.format(tablename) 
            self.db.commit()
            return True
        except Exception as e:
            self.msg += '\n'+str(e) 
    
    # Close the dbconnection
    def close(self):
        self.db.close()

# Is this script being run directly i.e pyhton ./databasebuilder.py
if __name__ == "__main__":     
# Example showing how to to use this class. Run: python2 ./database.py
# Place this scripot in the same directory as your script and use the following code:
    from databasebuilder import DatabaseBuilder

    # Our database structure
    dbstruct = {
        'table1':{
            'id':'INTEGER PRIMARY KEY',
            'uniquekey':'TEXT unique',                
            'timestamp':'INTEGER',
            'autotimestamp':'DATETIME DEFAULT CURRENT_TIMESTAMP',
            'title':'TEXT',
            'lat':'REAL',
            'lon':'REAL'
        },
        'table2':{
            'id':'INTEGER PRIMARY KEY',
            'uniquekey':'TEXT unique',                
            'timestamp':'INTEGER',
            'autotimestamp':'DATETIME DEFAULT CURRENT_TIMESTAMP',
            'title':'TEXT',
            'lat':'REAL',
            'lon':'REAL'
        }
    }
    
    # Initialise the database and build it if it doesn't exist
    databasefile = "db.sqlite3"
    builder = DatabaseBuilder(databasefile, dbstruct)
    print(builder.msg)  

    # Connect to the database
    db = sqlite3.connect(databasefile)
    cursor = db.cursor()

    # INSERT a value
    values = (1234, 'Test Title', 0.222, 56.999)
    cursor.execute('INSERT INTO table1(timestamp, title, lat, lon) VALUES(?,?,?,?)', values)
    db.commit()

    # SELECT
    cursor.execute("SELECT timestamp, title, lat, lon FROM table1")
    rows = cursor.fetchall()
    for row in rows:
        print('timestamp:{} title:{} lat:{} lon:{}'.format(row[0], row[1], row[2], row[3]))
    
    # UPDATE a value(s)
    cursor.execute("UPDATE table1 SET timestamp=1 WHERE timestamp=1234")
    db.commit()

    # SELECT
    print('-----')
    cursor.execute("SELECT timestamp, title, lat, lon FROM table1")
    rows = cursor.fetchall()
    for row in rows:
        print('timestamp:{} title:{} lat:{} lon:{}'.format(row[0], row[1], row[2], row[3]))






