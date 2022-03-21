from mastodon import Mastodon
import os

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
            api_base_url = self._mastodonServer,
            to_file = 'app/secretFolder/mastodonApiAppUser.secret'
        )  

        Mastodon.create_app(
            "mastodonApiAppAdmin",
            api_base_url = self._mastodonServer,
            to_file = "app/secretFolder/mastodonApiAppAdmin.secret"
        )  

    def setUpAccounts(self):
        self._user = Mastodon(
            client_id = 'app/secretFolder/mastodonApiAppUser.secret',
            api_base_url = self._mastodonServer
        )

        self._admin = Mastodon(
            client_id = 'app/secretFolder/mastodonApiAppAdmin.secret',
            api_base_url = self._mastodonServer
        )
        


    def loginAccount(self, username, password, user=True):
        if user:
            self._user.log_in(
                username,
                password,
                to_file = 'app/secretFolder/usercredentials.secret' 
            )
        else:
            self._admin.log_in(
                username,
                password,
                to_file = 'app/secretFolder/admincredentials.secret'
            )
    
    def createApiInstance(self):
        self._userApiInstance = Mastodon(
            access_token = 'app/secretFolder/usercredentials.secret',
            api_base_url = self._mastodonServer
        )

    def getNotifications(self, user=True):
        return self._userApiInstance.notifications() if user else self._adminApiInstance.notifications()

    def getNumberOfNotifications(self, user=True):
         return len(self._userApiInstance.notifications()) if user else len(self._adminApiInstance.notifications())

    def clearNotifications(self, user=True):
        self._userApiInstance.notifications_clear() if user else self._adminApiInstance.notifications_clear()

    def getAccountData(self, account_id, admin=True):
        return self._userApiInstance.account(account_id) if not admin else self._adminApiInstance.admin_account(account_id)
    
        


        


    




        
