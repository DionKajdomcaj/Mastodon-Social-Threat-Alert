from sys import path
from typing import Tuple
path.append("/MASTODON-SOCIAL-THREAT-ALERT/database/")
from database.database import Database
class DatabaseTests:
    def testCreatingDatabase(self):
        database = Database()
        database.dropTable()
        
        assert True == database.createTable()

        for iter in range(3):
            assert False == database.createTable()
    
    def testDropTable(self):
        database = Database()
        database.dropTable()
        database.createTable()

        assert True == database.dropTable()

        for iter in range(3):
            assert False == database.dropTable()

    def testInsertData(self):
        database = Database()
        database.dropTable()
        database.createTable()

        account_data = {'id' : 123412, 'username' : 'Dion', 'threat' : True}
        assert database.insertData(account_data['id'], account_data['username'], account_data['threat']) == True

    def testCheckRecordExistence(self):
        database = Database()
        database.dropTable()
        database.createTable()

        assert False == database.checkIfRecordExists(51123)

        account_data = {'id' : 123412, 'username' : 'Dion', 'threat' : True}
        database.insertData(account_data['id'], account_data['username'], account_data['threat'])

        assert database.checkIfRecordExists(account_data['id']) == True

    def testCloseConnection(self):
        database = Database()
        database.dropTable()
        database.createTable()

        account_data = {'id' : 123412, 'username' : 'Dion', 'threat' : True}
        database.insertData(account_data['id'], account_data['username'], account_data['threat'])

        assert True == database.closeConnection()

        for iter in range(3):
            assert False == database.closeConnection()
    






