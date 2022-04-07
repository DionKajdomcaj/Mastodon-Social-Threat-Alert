import sqlite3 as sql


class Database:
    def __init__(self):
        try:
            self.connection = sql.connect("MSTAdatabase.db")
            self.__cursor = self.connection.cursor()
            print("Successful Connection")
        except Exception:
            print("Database connection was unsuccessful")
    
    def createTable(self):
        try:
            self.__cursor.execute('''
            CREATE TABLE HandledAccounts (
                ID INTEGER PRIMARY KEY,
                USERNAME TEXT,
                THREAT BOOL
            );
            ''')
            print("SUCCESSFULLY CREATED THE TABLE")
            return True
        except Exception:
            print("FAILED TO CREATE THE TABLE")
            return False

    def dropTable(self):
        try:
            self.__cursor.execute('''
                DROP TABLE IF EXISTS HandledAccounts;
            ''')
            print("Table dropped")
            return True
        except Exception:
            print("Error")
                
    def closeConnection(self):
        try:
            self.connection.commit()
            self.connection.close()
            print("Database Closed")
            return True
        except Exception:
            print("Database couldn't close")
            return False

    def checkInstance(self, variable, v_type):
        return type(variable) == v_type

    def insertData(self, account_id, username, threat):
        try:
            if(not self.checkInstance(account_id, int)):
                raise Exception("Invalid type for account Id")

            if(not self.checkInstance(username, str)):
                raise Exception("Invalid type for Username")

            if(not self.checkInstance(threat, bool)):
                raise Exception("Invalid type for threat")

            values = (account_id, username, threat)
            execute_str = 'INSERT INTO HandledAccounts (id, username, threat)\
                VALUES {}'.format(values)
            self.__cursor.execute(execute_str)
            print("Data successfully inserted")
            return True

        except Exception:
            print("SDi")
            return False

    def checkIfRecordExists(self, account_id):
        try:
            if(not self.checkInstance(account_id, int)):
                raise Exception("Invalid type for account id")
            execute_str = 'SELECT * FROM HandledAccounts\
                WHERE id = {}'.format(account_id)
            self.__cursor.execute(execute_str)
            result = self.__cursor.fetchall()
            return len(result) > 0
        except Exception:
            print('problem query')