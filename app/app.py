from api.Mastodon_Api import Mastodon_Api
from time import sleep
from database.database import Database
class Application:

    def __init__(self, username, password, server, user = True):
        self.api = Mastodon_Api()
        self.database = Database()
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
    
    def actionsForTheAccount(self, account, admin = False):
        action = input('Decide the action for the account')
        if(action.lower() == 'block'):
            self.api.blockAccount(account)
            print("blocked")
            if admin:
                self.api.restrictAccount(account)
        self.api._userApiInstance.account_unblock(account)

    def start(self):
        try:
            self.database.createTable()
            while True:
                sleep(2.6)
                notifications = self.api.getNotifications()
                accounts_reaching_user = []
                [accounts_reaching_user.append(notification['account']['id']) for notification in notifications if notification['account']['id'] not in accounts_reaching_user]
                if len(accounts_reaching_user) > 0:
                    for account in accounts_reaching_user:
                        if(not self.database.checkIfRecordExists(int(account))):
                            print("wsp")
                            account_data = self.api.getAccountData(account,False)
                            print(str(account_data['created_at']))
                            threat = self.isItThreat(account_data)
                            if(threat):
                                self.actionsForTheAccount(account)
                                print("Done")
                            else:
                                print("Not a threat")

                            self.database.insertData(int(account_data['id']), str(account_data['username']), threat)
                        else:
                            print("Record exists")
                else:
                    print("No account")
        except Exception:
            print("Something went wrong with the app")      
                
    

            



    
        