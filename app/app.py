from api.Mastodon_Api import Mastodon_Api
from database.database import Database
import pickle


class Application:

    def __init__(self, username, password, server, user=True):
        self.api = Mastodon_Api()
        self.__database = Database()
        self.__username = username
        self.__password = password
        self.__server = server
        self.user = user
        with open('model/model.pickle', 'rb') as model_file:
            self.model = pickle.load(model_file)

        self.features = ['followers', 'followings', 'statuses',
        'profile', 'fosstodon.org', 'hofelho.hu', 'mastodon.elte.hu', 
        'mastodon.social', 'mastodon.technology', 'mastodon.xyz', 
        'scholar.social', 2015, 2016, 2017, 2018, 2019, 2020, 2021,
        2022]

    def initApi(self):
        try:
            self.api.createApp(self.__server)
            self.api.setUpAccounts()
            self.api.loginAccount(self.__username, self.__password, self.user)
            self.api.createApiInstance()
            self.__database.createTable()
            self.trustFollowings()
            return True
        except Exception:
            return False

    def modelDecision(self, account_data):
        dataForModel = {}
        dataForModel['followers'] = int(account_data['followers_count'])
        dataForModel['followings'] = int(account_data['following_count'])
        dataForModel['statuses'] = account_data['statuses_count']
        dataForModel['profile'] = 1 if 'missing' in account_data['avatar'].split('/') else 0
        dataForModel['server'] = account_data['url'].split('/')[2]
        dataForModel['dateOfCreation'] = int(str(account_data['created_at']).split('-')[0])
        data = []
        for index, feature in enumerate(self.features):
            if index < 4:
                data.append(dataForModel[feature])
            elif index > 3 and index < 11:
                if feature == dataForModel['server']:
                    data.append(1)
                else:
                    data.append(0)
            else:
                if feature == dataForModel['dateOfCreation']:
                    data.append(1)
                else:
                    data.append(0)

        model_result = bool(self.model.predict([data])[0])
        return model_result

    def isItThreat(self, account_id):
        account_data = self.api.getAccountData(account_id)
        threat = self.modelDecision(account_data)
        return (account_data, threat)
    
    def actionsForTheAccount(self, account_data, action, admin=False):
        if(action.lower() == 'block'):
            self.api.blockAccount(account_data['id'])
            print("blocked")
        return True
        
    def isAccountInDatabase(self, account_id):
        try:
            return self.__database.checkIfRecordExists(account_id)
        except Exception:
            return -1

    def insertAccountInDatabase(self, account_data, threat):
        try:
            id = int(account_data['id'])
            username = account_data['username']
            self.__database.insertData(id, username, threat)
        except Exception:
            print("DIDNT INSERT DATA. ERROR")

    def startSession(self):
        try:
            notifications = self.api.getNotifications()
            accounts_reaching_user = []
            for notification in notifications:
                account_id = notification['account']['id']
                valid_notification = (notification['type'] == 'mention' 
                                    or notification['type'] == 'reblog')

                inDatabase = self.isAccountInDatabase(int(account_id))

                if (account_id not in accounts_reaching_user and not inDatabase 
                                                        and valid_notification):
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
                self.__database.insertData(account_id, username, False) 
            except Exception:
                print("nothing")
    
    def closeApp(self):
        self.__database.closeConnection()