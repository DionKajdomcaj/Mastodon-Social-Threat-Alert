from time import sleep
from api.Mastodon_Api import Mastodon_Api

server= 'mastodon.elte.hu'

api = Mastodon_Api()

api.createApp(server)
api.setUpAccounts()
api.loginAccount("kajdo","dinoni12")
api.createApiInstance()
def check(acc):
    print("done")
while True:
    sleep(3)
    notifications = api.getNotifications()
    if(len(notifications) > 0):
        for i in notifications:
            check(i)
            
