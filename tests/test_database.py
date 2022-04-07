from database.database import Database


class TestDatabase:

    def testCreatingDatabase(self):
        database = Database()
        database.dropTable("TestTable")
        
        assert True == database.createTable("TestTable")

        for _ in range(3):
            assert False == database.createTable("TestTable")
            
    def testDropTable(self):
        database = Database()
        database.dropTable()
        database.createTable("TestTable")

        assert True == database.dropTable("TestTable")

    def testInsertData(self):
        database = Database()
        database.dropTable()
        database.createTable("TestTable")

        id = 1234123
        user = 'Dion'
        threat = False
        assert database.insertData(id, user, threat) == True

    def testCheckRecordExistence(self):
        database = Database()
        database.dropTable("TestTable")
        database.createTable("TestTable")

        assert False == database.checkIfRecordExists(51123)

        id = 1234123
        user = 'Dion'
        threat = False

        assert True == database.checkInstance(threat, bool)
        database.insertData(id, user, threat)

        assert database.checkIfRecordExists(id) == True

    def testCloseConnection(self):
        database = Database()
        database.dropTable("TestTable")
        database.createTable("TestTable")

        id = 1234123
        user = 'Dion'
        threat = False
        database.insertData(id, user, threat)

        assert True == database.closeConnection()

        for _ in range(3):
            assert False == database.closeConnection()