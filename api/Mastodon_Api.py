from mastodon import Mastodon


class Mastodon_Api:

    def __init__(self):
        self._user = Mastodon()
        self._admin = Mastodon()
        self._userApiInstance = Mastodon()
        self._adminApiInstance = Mastodon()
        self._mastodonServer = ""

    def createApp(self, mastodon_server):
        if(mastodon_server.split("://")[0] != "https"):
            self._mastodonServer = "https://" + mastodon_server
        else:
            self._mastodonServer = mastodon_server

        Mastodon.create_app(
            "mastodonApiAppUser",
            api_base_url=self._mastodonServer,
            to_file='app/secretFolder/mastodonApiAppUser.secret'
        )  

        Mastodon.create_app(
            "mastodonApiAppAdmin",
            api_base_url=self._mastodonServer,
            to_file="app/secretFolder/mastodonApiAppAdmin.secret"
        )  

    def setUpAccounts(self):
        self._user = Mastodon(
            client_id='app/secretFolder/mastodonApiAppUser.secret',
            api_base_url=self._mastodonServer
        )

        self._admin = Mastodon(
            client_id='app/secretFolder/mastodonApiAppAdmin.secret',
            api_base_url=self._mastodonServer
        )
        
    def loginAccount(self, username, password, user=True):
        if user:
            self._user.log_in(
                username,
                password,
                to_file='app/secretFolder/usercredentials.secret' 
            )
        else:
            self._admin.log_in(
                username,
                password,
                to_file='app/secretFolder/admincredentials.secret'
            )
    
    def createApiInstance(self):
        self._userApiInstance = Mastodon(
            access_token='app/secretFolder/usercredentials.secret',
            api_base_url=self._mastodonServer
        )

    def getNotifications(self):
        return self._userApiInstance.notifications()

    def getNumberOfNotifications(self):
        return len(self._userApiInstance.notifications())

    def clearNotifications(self):
        self._userApiInstance.notifications_clear()

    def getAccountData(self, account_id, admin=False):
        if not admin:
            return self._userApiInstance.account(account_id)
        else:
            return self._adminApiInstance.admin_account(account_id)

    def blockAccount(self, account_id):
        self._userApiInstance.account_block(account_id)
        return True
    
    def getFollowingAccounts(self):
        my_id = self._userApiInstance.me()['id']
        return self._userApiInstance.account_following(my_id)
    
    def unblockAccount(self, account_id):
        self._userApiInstance.account_unblock(account_id)