from time import sleep
from app.app import Application

application = Application("kajdo", "dinoni12", "mastodon.elte.hu")
application.initApi()
application.start()