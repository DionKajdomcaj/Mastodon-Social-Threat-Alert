from database.database import Database


class TestDatabase:

    def testCreatingDatabase(self):
        database = Database()
        database.dropAccountTable()
        
        assert True == database.createTableAccounts()

        for _ in range(3):
            assert False == database.createTableAccounts()
            
    def testDropTable(self):
        database = Database()
        database.dropAccountTable()
        database.createTableAccounts()

        assert True == database.dropAccountTable()

    def testInsertData(self):
        database = Database()
        database.dropAccountTable()
        database.createTableAccounts()

        id = 1234123
        user = 'Dion'
        domain = 'gibberish'
        threat = False
        assert database.insertAccount(id, user, domain, threat) == True

    def testCheckRecordExistence(self):
        database = Database()
        database.dropAccountTable()
        database.createTableAccounts()

        assert False == database.checkIfRecordExists(51123)

        id = 1234123
        user = 'Dion'
        domain = 'gibberish'
        threat = False

        assert True == database.checkInstance(threat, bool)
        database.insertAccount(id, user, domain, threat)

        assert database.checkIfRecordExists(id) == True

    def testCloseConnection(self):
        database = Database()
        database.dropAccountTable()
        database.createTableAccounts()

        id = 1234123
        user = 'Dion'
        domain = 'gibberish'
        threat = False

        database.insertAccount(id, user, domain, threat)

        assert True == database.closeConnection()

        for _ in range(3):
            assert False == database.closeConnection()
    
    def testCreateDomainTable(self):
        database = Database()
        database.dropDomainTable()

        assert True == database.createTableDomain()

        for _ in range(3):
            assert False == database.createTableDomain()
    
    def testInsertDomain(self):
        database = Database()
        database.dropDomainTable()

        database.createTableDomain()

        domain = 'nevermind'
        blocked = False

        assert True == database.insertDomain(domain, blocked)

        for _ in range(2):
            assert False == database.insertDomain(domain, blocked)
    
    def testDropDomain(self):
        database = Database()
        database.dropDomainTable()

        database.createTableDomain()

        assert True == database.dropDomainTable()