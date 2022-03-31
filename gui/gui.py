
from cgi import test
from cgitb import text
from email.mime import image
from threading import Event
from threading import Thread
import time
import tkinter as tk
from PIL import ImageTk, Image
from tkinter.ttk import Combobox

from numpy import rot90
from app.app import Application

class LogIn(tk.Tk):

    def __init__(self):
        super().__init__()

        self.username = ''
        self.password = ''
        self.server = ''
        self.action = ''
        self.widgets = {'main' : [], 'running' : [], 'action' : set([])}
        self.thevent = Event()

        self.title('Mastodon Threat Alert')

        window_height = 500
        window_width = 400
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        self['bg'] = 'light blue'

        self.welcome_label = tk.Label(self, text = 'Mastodon Threat Alert', font = ('Ariel', 18), bg = 'light blue')
        self.empty_label = tk.Label(self, bg = 'light blue')
        
        self.main_label1 = tk.Label(self, text = 'Mastodon Username', font = ('Ariel', 14), bg = 'light blue')
        self.widgets['main'].append(self.main_label1)

        self.canvas = tk.Canvas(self, width = 200, height = 250, bg = 'light blue', highlightthickness = 0)
        #self.canvas.pack_propagate(False)
        

        self.main_entry1 = tk.Entry(self)
        self.widgets['main'].append(self.main_entry1)

        self.main_label2 = tk.Label(self, text = 'Mastodon Password', font = ('Ariel', 14), bg = 'light blue')
        self.widgets['main'].append(self.main_label2)

        self.main_entry2 = tk.Entry(self, show = "*")
        self.widgets['main'].append(self.main_entry2)

        self.main_label3 = tk.Label(self, text = 'Mastodon Server', font = ('Ariel', 14), bg = 'light blue')
        self.widgets['main'].append(self.main_label3)

        self.main_entry3 = tk.Entry(self)
        self.widgets['main'].append(self.main_entry3)

        self.main_button1 = tk.Button(self, text = 'Start App', state = 'disabled', command = self.startApp)
        self.widgets['main'].append(self.main_button1)

        self.welcome_label.pack()
        self.empty_label.pack()

        self.main_label1.pack()
        self.main_entry1.pack()
        self.main_entry1.bind('<KeyRelease>', self.getInput)


        self.main_label2.pack()
        self.main_entry2.pack()
        self.main_entry2.bind('<KeyRelease>', self.getInput)

        self.main_label3.pack()
        self.main_entry3.pack()
        self.main_entry3.bind('<KeyRelease>', self.getInput)

        self.main_button1.pack()

        self.img = Image.open('gui/images/bg2.png')
        self.resizable_img = self.img.resize((200,250), Image.ANTIALIAS)
        self.new_image = ImageTk.PhotoImage(self.resizable_img)
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor = tk.NW, image = self.new_image)
        self.canvas.image_types = 'png' 

        self.running_label1 = tk.Label(self, text = "The program state is:\n Currently running...", font = ("Ariel",20), bg = 'light blue')
        self.widgets['running'].append(self.running_label1)

        self.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
        self.resizable(0,0)

    def startApp(self):
        self.app = Application(self.username, self.password, self.server)

        self.running_end = tk.Button(self, text = "Stop the app", command = self.app.stopApp)
        self.widgets['running'].append(self.running_end)

        self.app.initApi()
        self.runningScreen()
        self.callSession()
        
    def getInput(self, event):
        print(event)
        self.username = self.main_entry1.get()
        self.password = self.main_entry2.get()
        self.server = self.main_entry3.get()
        if self.username == '' or self.password == '' or self.server == '':
            self.main_button1['state'] = tk.DISABLED
        else:
            print(self.username)
            print(self.password)
            print(self.server)
            self.main_button1['state'] = tk.NORMAL
    
    def getActionInput(self):
        self.action = self.action_combobox.get()
    
    def callSession(self):
        while True:
            self.update()
            time.sleep(2.4)
            print("running")
            accounts_reaching_user = self.app.startSession()
            
            if len(accounts_reaching_user) > 0:
                for account in accounts_reaching_user:
                    threat_checked_account = self.app.isItThreat(account)
                    account_data = threat_checked_account[0]
                    threat_data = threat_checked_account[1]
                    if threat_data:
                        self.done = False

                        self.string_var = tk.StringVar()
                        self.action_combobox = Combobox(self, textvariable = self.string_var)
                        self.action_combobox['values'] = ("Nothing", "Block", "Report")
                        self.widgets['action'].add(self.action_combobox)
                        self.action_button = tk.Button(self, text = 'Take action', command = lambda : self.takeAction(account_data,threat_data))
                        self.widgets['action'].add(self.action_button)
                        self.cleanRunning()
                        while not self.done:
                            self.update()
                            print('not done')
                        self.cleanAction()
                        
                    self.app.insertAccountInDatabase(account_data, threat_data)
    
    def runningScreen(self):
        for widget in self.widgets['main']:
            widget.pack_forget()
        for widget in self.widgets['running']:
            widget.pack()
    def takeAction(self, account_data, threat_data):
        action = self.action_combobox.get()
        self.app.actionsForTheAccount(account_data, action, threat_data)
        self.done = True
        

    def cleanRunning(self):
        for widget in self.widgets['running']:
            widget.pack_forget()
        for widget in self.widgets['action']:
            widget.pack()
    
    def cleanAction(self):
        for widget in self.widgets['action']:
            widget.pack_forget()
        for widget in self.widgets['running']:
            widget.pack()




