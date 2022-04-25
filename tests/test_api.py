from app.app import Application


class TestAPI:
    def testAccountCreation(self):
        app = Application('kajdo', 'dinoni12', 'mastodon.elte.hu')
        assert True == app.initApi()
    
    def testGetNotification(self):
        app = Application('kajdo', 'dinoni12', 'mastodon.elte.hu')
        app.initApi()
        assert type(app.api.getNotifications()) is list

    def testGetFollowingAccounts(self):
        app = Application('kajdo', 'dinoni12', 'mastodon.elte.hu')
        app.initApi()
        assert 2 == len(app.api.getFollowingAccounts())
    
    def testGetAccountData(self):
        app = Application('kajdo', 'dinoni12', 'mastodon.elte.hu')
        app.initApi()
        assert 'gerazo' == app.api.getAccountData(1)['username']
    
    def testClearNotification(self):
        app = Application('kajdo', 'dinoni12', 'mastodon.elte.hu')
        app.initApi()
        assert True == app.api.clearNotifications()
    
    def testBlockAccount(self):
        app = Application('kajdo', 'dinoni12', 'mastodon.elte.hu')
        app.initApi()
        assert True == app.api.blockAccount(108055689433205398)
        assert True == app.api.unblockAccount(108055689433205398)
    
    def testBlockDomain(self):
        app = Application('kajdo', 'dinoni12', 'mastodon.elte.hu')
        app.initApi()
        assert True == app.api.blockDomain('fosstodon.org')
        assert True == app.api.unblockDomain('fosstodon.org')
    
    def testMuteAccount(self):
        app = Application('kajdo', 'dinoni12', 'mastodon.elte.hu')
        app.initApi()
        assert True == app.api.muteAccount(108055689433205398)
