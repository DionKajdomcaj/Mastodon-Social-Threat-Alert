from tkinter.messagebox import NO
import pandas as pd
import numpy as np
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

class Model:

    def __init__(self):
        self.model = LogisticRegression()
        self.df = pd.read_csv("data/HR_comma_sep.csv")
        self.training = None
        self.x_train = None
        self.x_test = None
        self.y_train = None
        self.y_test = None
        
    def train_model(self):
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split()
        pass

    def test_model(self,test_data):
        pass

    def save_training(self):
        with open("training.pickle","wb") as f:
            pickle.dump(self.training)
    
    def load_model(self):
        with open("training.pickle", "wb") as f:
            self.training = pickle.load(f)

        



