import sqlite3

#check if the required database exists or not.
def check_if_db_exists():
    return

#create a database in sqlite.
def createDatabase(db_name):
    db = sqlite3.connect(db_name, check_same_thread=False)
    c = db.cursor()
    return True

#creating a table in the DB
def create_table(table_name, db_cursor):

    #the argument table_name is of type list.
    for i in table_name:
        print(i)
        db_cursor.execute("CREATE TABLE IF NOT EXISTS {} (ts datetime primary key, price real(15,5), volume integer)".format(i))
    try:
        db.commit()
    except:
        db.rollback()