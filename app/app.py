from api.Mastodon_Api import Mastodon_Api
from time import sleep
class Application:

    def __init__(self, username, password, server, user = True):
        self.api = Mastodon_Api()
        self.username = username
        self.password = password
        self.server = server
        self.user = user
    
    def initApi(self):
        self.api.createApp(self.server)
        self.api.setUpAccounts()
        self.api.loginAccount(self.username, self.password, self.user)
        self.api.createApiInstance()

    def isItThreat(self, account):
        return True
    
    def actionsForTheAccount(self, account):
        pass

    def start(self):
        while True:
            sleep(2.6)
            notifications = self.api.getNotifications()
            accounts_reaching_user = []
            [accounts_reaching_user.append(notification['account']['id']) for notification in notifications if notification['account']['id'] not in accounts_reaching_user]
            if len(accounts_reaching_user) > 0:
                for account in accounts_reaching_user:
                    if(self.isItThreat(account)):
                        self.actionsForTheAccount(account)
                        print("Done")
            else:
                print("No account")
                
    

            



    
        