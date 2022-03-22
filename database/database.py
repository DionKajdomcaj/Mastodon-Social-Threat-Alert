import sqlite3 as sql

class Database:
    def __init__(self):
        try:
            self.connection = sql.connect("MSTAdatabase.db")
            self.cursor = self.connection.cursor()
            print("Successful Connection")
        except Exception:
            print("Database connection was unsuccessful")
    
    def createTable(self):
        try:
            self.cursor.execute('''
            CREATE TABLE HandledAccounts (
                ID INTEGER PRIMARY KEY,
                USERNAME TEXT,
                THREAT BOOL,
                VIOLATIONS INT DEFAULT 0
            );
            ''')
            print("SUCCESSFULLY CREATED THE TABLE")
        except Exception:
            print("FAILED TO CREATE THE TABLE")

    def dropTable(self):
        try:
            self.cursor.execute('''
                DROP TABLE IF EXISTS HandledAccounts;
            ''')
            print("Table dropped")
        except Exception:
            print("Table not dropped ERROR")

    



        