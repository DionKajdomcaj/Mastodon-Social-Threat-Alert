from database.database import Database


class TestDatabase:

    def testCreatingDatabase(self):
        database = Database()
        database.dropTable()
        
        assert True == database.createTable()

        for _ in range(3):
            assert False == database.createTable()