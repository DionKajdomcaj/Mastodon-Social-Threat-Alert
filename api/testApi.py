import imp
from traceback import print_tb
from mastodon import Mastodon
from Mastodon_Api import Mastodon_Api
'''

Mastodon.create_app(
     'pytooterapp',
     api_base_url = 'https://mastodon.elte.hu',
     to_file = 'pytooter_clientcred.secret'
)

mastodon = Mastodon(
    client_id = 'pytooter_clientcred.secret',
    api_base_url = 'https://mastodon.elte.hu'
)
mastodon.log_in(
    'kajdo',
    'dinoni12',
    to_file = 'pytooter_usercred.secret'
)
mastodon = Mastodon(
    access_token = 'pytooter_usercred.secret',
    api_base_url = 'https://mastodon.elte.hu'
)
print(len(mastodon.notifications()))


'''

api = Mastodon_Api()
email = "kajdo"
password =  "dinoni12"
mastodon_server = "mastodon.elte.hu"
'''
api.setUpAccounts()
api.loginAccount(email,password)
api.createApiInstance()
print(len(api.getNotifications()))

'''
api.createApp(mastodon_server)






#mastodon.toot('Tooting from python using #mastodonpy2 !')