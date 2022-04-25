import os
import time
import tkinter as tk
from PIL import ImageTk, Image
from tkinter.ttk import Combobox
from tkinter.messagebox import showerror
from tkinter.messagebox import showinfo
from app.app import Application


class LogIn(tk.Tk):

    def __init__(self):
        super().__init__()

        self.username = ''
        self.password = ''
        self.server = ''
        self.action = ''
        self.widgets = {'main': [], 'running': set([]), 'action': set([])}
        
        self.title('Mastodon Threat Alert')

        window_height = 600
        window_width = 400
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width / 2) - (window_width / 2))
        y = int((screen_height / 2) - (window_height / 2))
        self['bg'] = 'light blue'

        self.welcome_label = tk.Label(self, text='Mastodon Threat Alert', 
                                    font=('Ariel', 18), bg='light blue')

        self.empty_label = tk.Label(self, bg='light blue')
        
        self.main_label1 = tk.Label(self, text='Mastodon Username', 
                                    font=('Ariel', 14), bg='light blue')
        self.widgets['main'].append(self.main_label1)

        self.canvas = tk.Canvas(self, width=200, height=250, 
                                bg='light blue', highlightthickness=0)

        self.main_entry1 = tk.Entry(self)
        self.widgets['main'].append(self.main_entry1)

        self.main_label2 = tk.Label(self, text='Mastodon Password', 
                                    font=('Ariel', 14), bg='light blue')

        self.widgets['main'].append(self.main_label2)

        self.main_entry2 = tk.Entry(self, show="*")
        self.widgets['main'].append(self.main_entry2)

        self.main_label3 = tk.Label(self, text='Mastodon Server', 
                                    font=('Ariel', 14), bg='light blue')

        self.widgets['main'].append(self.main_label3)

        self.main_entry3 = tk.Entry(self)
        self.widgets['main'].append(self.main_entry3)

        self.empty_label2 = tk.Label(self, bg='light blue')
        self.widgets['main'].append(self.empty_label2)

        self.main_button1 = tk.Button(self, text='Start the application', 
                                    state='disabled', command=self.startApp)
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
        
        self.empty_label2.pack()
        
        self.main_button1.pack()

        self.img = Image.open('gui/images/bg2.png')
        self.resizable_img = self.img.resize((200, 250), Image.ANTIALIAS)
        self.new_image = ImageTk.PhotoImage(self.resizable_img)
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.new_image)
        self.canvas.image_types = 'png' 

        text_running = "The program state is\n Currently running..."
        self.running_label1 = tk.Label(self, 
                                        text=text_running, 
                                        font=("Ariel", 20), bg='light blue')
        self.widgets['running'].add(self.running_label1)

        self.empty_label4 = tk.Label(self, bg='light blue')
        self.widgets['running'].add(self.empty_label4)

        self.running_end = tk.Button(self, text="Exit the application", 
                                    command=self.stopApp)
        self.widgets['running'].add(self.running_end)

        self.geometry("{}x{}+{}+{}"
                    .format(window_width, window_height, x, y))
        self.resizable(0, 0)

    def startApp(self):
        try:
            self.app = Application(self.username, self.password, self.server)
            self.app.initApi()
            self.app.initDatabase()
            self.runningScreen()
            self.protocol('WM_DELETE_WINDOW', self.stopApp)
            self.callSession()
        except Exception:
            showerror(message="Invalid credentials for mastodon account")
    
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
        self.update()
    
    def callSession(self):
        while True:
            self.update()
            print("running")
            try:
                self.accounts_reaching_user = []
                self.after(2400, self.sendRequest)
                t_end = time.time() + 2.4

                while time.time() <= t_end:
                    self.update()

                if len(self.accounts_reaching_user) > 0:
                    for account in self.accounts_reaching_user:
                        threat_checked_account = self.app.isItThreat(account)
                        account_data = threat_checked_account[0]
                        account_name = account_data['username']
                        threat_data = threat_checked_account[1]
                        domain = account_data['url'].split('/')[2]
                        if threat_data:
                            message = ("Account: " + account_name
                                        + "\nFrom domain: " + domain 
                                        + "\nMay be a threat!\nTake action!")
                            showinfo(message=message)

                            self.done = False

                            self.cleanRunning() 
                            self.createAction(account_data, threat_data)
                            
                            while not self.done:
                                self.update()
                                #print("not done")
                                if self.done:
                                    break
                            self.cleanAction()
                        self.app.insertAccountInDatabase(account_data, 
                                                        threat_data)
            except Exception:
                print("Error")
    
    def runningScreen(self):
        for widget in self.widgets['main']:
            widget.pack_forget()
        for widget in self.widgets['running']:
            widget.pack()

    def takeAction(self, account_data, threat_data):
        action = self.action_combobox.get()
        domain_action = self.domain_combobox.get()
        self.app.actionsForTheAccount(account_data, action, threat_data)
        self.app.actionsForTheDomain(account_data, domain_action)
        self.done = True
        
    def cleanRunning(self):
        for widget in self.widgets['running']:
            widget.pack_forget()
        
    def cleanAction(self):
        for widget in self.widgets['action']:
            widget.destroy()
        self.widgets['action'].clear()
        for widget in self.widgets['running']:
            widget.pack()

    def sendRequest(self):
        self.accounts_reaching_user = self.app.startSession()
        print(self.accounts_reaching_user)

    def createAction(self, account_data, threat_data):
        self.canvas.pack_forget()
        self.action_label1 = tk.Label(self, text="Account Action", 
                                    font=('Ariel', 14), bg='light blue')
        self.widgets['action'].add(self.action_label1)
        self.action_label1.pack()

        self.string_var = tk.StringVar()
        self.action_combobox = Combobox(self, 
                            textvariable=self.string_var)

        self.action_combobox['values'] = ("Trust", 
                                        "Block",
                                        "Mute")
        self.action_combobox.current(0)
        self.widgets['action'].add(self.action_combobox)
        self.action_combobox.pack()

        self.action_label2 = tk.Label(self, text="Domain Action", 
                                font=('Ariel', 14), bg='light blue')

        self.widgets['action'].add(self.action_label2)
        self.action_label2.pack()

        self.string_var2 = tk.StringVar()
        self.domain_combobox = Combobox(self, 
                            textvariable=self.string_var2)
        self.domain_combobox['values'] = ("Trust", 
                                        "Block")
        self.domain_combobox.current(0)
        self.widgets['action'].add(self.domain_combobox)
        self.domain_combobox.pack()

        self.empty_label3 = tk.Label(self, bg='light blue')
        self.widgets['action'].add(self.empty_label3)
        self.empty_label3.pack()

        self.action_button = tk.Button(self, 
                            text='Take action', 
                            command=lambda:
                            self.takeAction(account_data, threat_data))

        self.widgets['action'].add(self.action_button)
        self.action_button.pack()
        self.canvas.pack()

    def stopApp(self):
        self.app.closeApp()
        self.destroy()
        os._exit(0)