import pandas as pd 
import numpy as np
from sklearn.model_selection import train_test_split, cross_validate
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import Lasso, LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
from sklearn import metrics
import matplotlib.pyplot as plt

from data_processor import *



class Model():
    
    def __init__ (self, classifier_type):

        if classifier_type == 'LASSO':
            self.model = Lasso(alpha = 1.0) #'alpha' --> lambda value
            print("Initating LASSO")
        elif classifier_type == 'LinearRegression':
            self.model = LinearRegression()
            print("Initating Linear Regression")

                                                                #QUESTION for Kameron: What path do I pass?
        self.X_train, self.X_test, self.y_train, self.y_test = load_data("/Users/alexiscarras/Desktop/cm backend/climatemind-backend/ml_models/politcial_preference/datasets/pvq21CENTRED.csv")
        
    def train(self):

        print("training model...")
        return self.model.fit(self.X_train, self.y_train)

    def predict(self, X_test = None):
        """Returns predicted data"""
        return self.model.predict(self.X_test)

    def test(self, X_test = None, y_test = None): 
        """Scores model's predictions"""
        pred = self.predict()    
        #print(predictions)
        # print("Accuracy of: ", np.mean(predictions.astype(int) == self.y_test.astype()))

        #Bining the data 

        pass

