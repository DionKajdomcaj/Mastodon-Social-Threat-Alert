from faulthandler import disable
import tkinter as tk
from turtle import onclick
from app.app import Application
class AppGUI(tk.Tk):

    def __init__(self):
        super().__init__()

        self.username = ''
        self.password = ''
        self.server = ''

        self.title('Mastodon Threat Alert')
        self.label1 = tk.Label(self, text='Mastodon Username')
        self.entry1 = tk.Entry(self)
        self.label2 = tk.Label(self, text='Mastodon Password')
        self.entry2 = tk.Entry(self)
        self.label3 = tk.Label(self, text='Mastodon Server')
        self.entry3 = tk.Entry(self)
        self.button1 = tk.Button(self, text='Start App', state='disabled')

        self.label1.pack()
        self.entry1.pack()
        self.entry1.bind('<KeyRelease>', self.getInput)


        self.label2.pack()
        self.entry2.pack()
        self.entry2.bind('<KeyRelease>', self.getInput)

        self.label3.pack()
        self.entry3.pack()
        self.entry3.bind('<KeyRelease>', self.getInput)

        self.button1.pack()
        self.button1.bind("<Button-1>", self.startApp)

        self.geometry("400x300+10+10")
        self.resizable(0,0)
    
    def startApp(self, event):
        self.app = Application(self.username, self.password, self.server)
        self.app.initApi()
        self.withdraw()
        self.app.start()


    def getInput(self, event):
        print(event)
        self.username = self.entry1.get()
        self.password = self.entry2.get()
        self.server = self.entry3.get()
        if self.username == '' or self.password == '' or self.server == '':
            self.button1['state'] = tk.DISABLED
        else:
            print(self.username)
            print(self.password)
            print(self.server)
            self.button1['state'] = tk.NORMAL


        


