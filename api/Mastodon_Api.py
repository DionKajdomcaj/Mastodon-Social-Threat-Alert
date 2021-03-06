from mastodon import Mastodon


class Mastodon_Api:

    def __init__(self):
        self._user = Mastodon()
        self._userApiInstance = Mastodon()
        self._mastodonServer = ""

    def createApp(self, mastodon_server):
        if(mastodon_server.split("://")[0] != "https"):
            self._mastodonServer = "https://" + mastodon_server
        else:
            self._mastodonServer = mastodon_server

        print(self._mastodonServer)

        Mastodon.create_app(
            "mastodonApiAppUser",
            api_base_url=self._mastodonServer,
            to_file='app/secretFolder/mastodonApiAppUser.secret'
        )

    def setUpAccounts(self):
        self._user = Mastodon(
            client_id='app/secretFolder/mastodonApiAppUser.secret',
            api_base_url=self._mastodonServer
        )
        
    def loginAccount(self, username, password, user=True):
        if user:
            self._user.log_in(
                username,
                password,
                to_file='app/secretFolder/usercredentials.secret' 
            )
    
    def createApiInstance(self):
        self._userApiInstance = Mastodon(
            access_token='app/secretFolder/usercredentials.secret',
            api_base_url=self._mastodonServer
        )

    def getNotifications(self):
        return self._userApiInstance.notifications(mentions_only=True)

    def getNumberOfNotifications(self):
        return len(self._userApiInstance.notifications())

    def clearNotifications(self):
        self._userApiInstance.notifications_clear()
        return True

    def getAccountData(self, account_id, admin=False):
        if not admin:
            return self._userApiInstance.account(account_id)

    def blockAccount(self, account_id):
        self._userApiInstance.account_block(account_id)
        print("done")
        return True
    
    def getFollowingAccounts(self):
        my_id = self._userApiInstance.me()['id']
        return self._userApiInstance.account_following(my_id)
    
    def unblockAccount(self, account_id):
        self._userApiInstance.account_unblock(account_id)
        return True

    def blockDomain(self, domain):
        self._userApiInstance.domain_block(domain)
        return True
    
    def unblockDomain(self, domain):
        self._userApiInstance.domain_unblock(domain)
        return True
    
    def muteAccount(self, account_id):
        self._userApiInstance.account_mute(account_id)
        return True
    
    def unmuteAccount(self, account_id):
        self._userApiInstance.account_unmute(account_id)
        return True