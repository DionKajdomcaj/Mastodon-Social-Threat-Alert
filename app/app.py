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
        self.database.createTable()
        self.trustFollowings()

    def modelDecision(self, account_data):
        return True

    def isItThreat(self, account_id):
        account_data = self.api.getAccountData(account_id)
        threat = self.modelDecision(account_data)
        return (account_data, threat)
    
    def actionsForTheAccount(self, account_data, action, threat, admin = False):
        if(action.lower() == 'block'):
            self.api.blockAccount(account_data['id'])
            print("blocked")
            if admin:
                self.api.restrictAccount(account_data['id'])
        self.api._userApiInstance.account_unblock(account_data['id'])
    
    def isAccountInDatabase(self, account_id):
        try:
            return self.database.checkIfRecordExists(account_id)
        except Exception:
            return -1

    def insertAccountInDatabase(self, account_data, threat):
        try:
            self.database.insertData(int(account_data['id']), account_data['username'],threat)
        except Exception:
            print("DIDNT INSERT DATA. ERROR")

    def startSession(self):
        try:
            notifications = self.api.getNotifications()
            accounts_reaching_user = []
            [accounts_reaching_user.append(notification['account']['id']) 
            for notification in notifications 
            if notification['account']['id'] not in accounts_reaching_user
            and not self.isAccountInDatabase(int(notification['account']['id']))]

            return accounts_reaching_user
        except Exception:
            return -1

    def trustFollowings(self):
        following_accounts = self.api.getFollowingAccounts()   
        for account_data in following_accounts:
            try:
                self.database.insertData(int(account_data['id']), account_data['username'], False) 
            except Exception:
                print("nothing")

    def stopApp(self):
        exit()


    
        