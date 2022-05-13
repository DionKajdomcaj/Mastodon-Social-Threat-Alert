import sqlite3 as sql


class Database:
    def __init__(self):
        try:
            self.connection = sql.connect("MSTAdatabase.db")
            self.cursor = self.connection.cursor()
            print("Successful Connection")
        except Exception:
            print("Database connection was unsuccessful")
    
    def createTableAccounts(self):
        try:
            self.cursor.execute('''
            CREATE TABLE HandledAccounts (
                ID INTEGER PRIMARY KEY,
                USERNAME TEXT,
                DOMAIN TEXT,
                THREAT BOOL
            );
            ''')
            print("SUCCESSFULLY CREATED THE TABLE")
            return True
        except Exception:
            print("FAILED TO CREATE THE TABLE")
            return False

    def createTableDomain(self):
        try:
            self.cursor.execute('''
            CREATE TABLE HandledDomains (
                DOMAIN TEXT PRIMARY KEY,
                BLOCKED BOOL
            );
            ''')
            print("SUCCESSFULLY CREATED THE TABLE")
            return True
        except Exception:
            print("FAILED TO CREATE THE TABLE")
            return False
        
    def dropAccountTable(self):
        try:
            self.cursor.execute('''
                DROP TABLE IF EXISTS HandledAccounts;
            ''')
            print("Table dropped")
            return True
        except Exception:
            print("Table not dropped ERROR")
    
    def dropDomainTable(self):
        try:
            self.cursor.execute('''
                DROP TABLE IF EXISTS HandledDomains;
            ''')
            print("Table dropped")
            return True
        except Exception:
            print("Table not dropped ERROR")

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

    def insertAccount(self, account_id, username, domain, threat):
        try:
            if(not self.checkInstance(account_id, int)):
                raise Exception("Invalid type for account Id")

            if(not self.checkInstance(username, str)):
                raise Exception("Invalid type for Username")

            if(not self.checkInstance(threat, bool)):
                raise Exception("Invalid type for threat")

            if(not self.checkInstance(domain, str)):
                raise Exception("Invalid type for Username")

            values = (account_id, username, domain, threat)
            execute_str = 'INSERT INTO HandledAccounts (id, username, domain, threat)\
                VALUES {}'.format(values)
            self.cursor.execute(execute_str)
            print("Data successfully inserted")
            return True

        except Exception:
            print("Already exists")
            return False

    def insertDomain(self, domain, blocked):
        try:
            if(not self.checkInstance(domain, str)):
                raise Exception("Invalid type for Domain")
            if(not self.checkInstance(blocked, bool)):
                raise Exception("Invalid type for Blocked")

            values = (domain, blocked)
            execute_str = 'INSERT INTO HandledDomains (domain, blocked)\
                VALUES {}'.format(values)
            self.cursor.execute(execute_str)
            print("Data successfully inserted")
            return True
        except Exception:
            print("Already exists")
            return False

    def checkIfRecordExists(self, account_id):
        try:
            if(not self.checkInstance(account_id, int)):
                raise Exception("Invalid type for account id")
            execute_str = 'SELECT * FROM HandledAccounts\
                WHERE id = {}'.format(account_id)
            self.cursor.execute(execute_str)
            result = self.cursor.fetchall()
            return len(result) > 0
        except Exception:
            print('problem query')