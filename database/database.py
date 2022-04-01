import sqlite3 as sql
from traceback import print_tb

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
                THREAT BOOL
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
    
    def closeConnection(self):
        try:
            self.connection.commit()
            self.connection.close()
            print("Database Closed")
        except Exception:
            print("Database couldn't close")

    def checkInstance(self, variable, v_type):
        return type(variable) == v_type

    def insertData(self, account_id, username, threat ):
        try:
            if(not self.checkInstance(account_id, int)):
                raise Exception("Invalid type for account Id")

            if(not self.checkInstance(username, str)):
                raise Exception("Invalid type for Username")

            if(not self.checkInstance(threat, bool)):
                raise Exception("Invalid type for threat")

            values = (account_id, username, threat)
            execute_str = 'INSERT INTO HandledAccounts (id, username, threat) VALUES {}'.format(values)
            self.cursor.execute(execute_str)
            print("Data successfully inserted")

        except Exception:
            print(Exception)

    def checkIfRecordExists(self, account_id):
        try:
            if(not self.checkInstance(account_id, int)):
                raise Exception("Invalid type for account id")
            execute_str = 'SELECT * FROM HandledAccounts WHERE id = {}'.format(account_id)
            self.cursor.execute(execute_str)
            result = self.cursor.fetchall()
            return len(result) > 0
        except Exception:
            print('problem query')




    



        