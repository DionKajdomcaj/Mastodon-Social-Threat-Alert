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

        id = 1234123
        user = 'Dion'
        threat = False
        assert database.insertData(id, user, threat) == True

    def testCheckRecordExistence(self):
        database = Database()
        database.dropTable()
        database.createTable()

        assert False == database.checkIfRecordExists(51123)

        id = 1234123
        user = 'Dion'
        threat = False
        database.insertData(id, user, threat)

        assert database.checkIfRecordExists(id) == True

    def testCloseConnection(self):
        database = Database()
        database.dropTable()
        database.createTable()

        id = 1234123
        user = 'Dion'
        threat = False
        database.insertData(id, user, threat)

        assert True == database.closeConnection()

        for iter in range(3):
            assert False == database.closeConnection()