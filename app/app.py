from api.Mastodon_Api import Mastodon_Api
from database.database import Database


class Application:

    def __init__(self, username, password, server, user=True):
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
    
    def actionsForTheAccount(self, account_data, action, admin=False):
        if(action.lower() == 'block'):
            self.api.blockAccount(account_data['id'])
            print("blocked")
            self.api._userApiInstance.account_unblock(account_data['id'])
        elif(action.lower() == 'report'):
            self.api.reportAccount(account_data['id'])
        
    def isAccountInDatabase(self, account_id):
        try:
            return self.database.checkIfRecordExists(account_id)
        except Exception:
            return -1

    def insertAccountInDatabase(self, account_data, threat):
        try:
            id = int(account_data['id'])
            username = account_data['username']
            self.database.insertData(id, username, threat)
        except Exception:
            print("DIDNT INSERT DATA. ERROR")

    def startSession(self):
        try:
            notifications = self.api.getNotifications()
            accounts_reaching_user = []
            for notification in notifications:
                account_id = notification['account']['id']
                inDatabase = self.isAccountInDatabase(int(account_id))
                if account_id not in accounts_reaching_user and not inDatabase:
                    accounts_reaching_user.append(account_id)
            return accounts_reaching_user
        except Exception:
            return []

    def trustFollowings(self):
        following_accounts = self.api.getFollowingAccounts()   
        for account_data in following_accounts:
            try:
                account_id = int(account_data['id'])
                username = str(account_data['username'])
                self.database.insertData(account_id, username, False) 
            except Exception:
                print("nothing")
    
    def closeApp(self):
        self.database.closeConnection()
