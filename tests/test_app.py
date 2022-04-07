from app.app import Application


class TestApplication:

    def testCreateApplication(self):
        app = Application('kajdo', 'dinoni12', 'mastodon.elte.hu')

        assert True == app.initApi()
        app.__database.dropTable()
    
    def testModelDecision(self):
        app = Application('kajdo', 'dinoni12', 'mastodon.elte.hu')
        app.initApi()

        assert False == app.isItThreat(1)[1]
        assert True == app.isItThreat(108055689433205398)[1]
        app.__database.dropTable()
    
    def testActionsTaken(self):
        app = Application('kajdo', 'dinoni12', 'mastodon.elte.hu')
        app.initApi()
        account_data = app.isItThreat(108055689433205398)[0]

        assert True == app.actionsForTheAccount(account_data, 'Trust')
        assert True == app.actionsForTheAccount(account_data, 'bLocK')
        app.api.unblockAccount(108055689433205398)      
        app.__database.dropTable()  