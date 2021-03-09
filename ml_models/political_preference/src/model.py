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


class Model():

    def __init__ (self, model, training_data, test_data, verbose = False):
        """@args model: type as a string, 
                training_data tuple containing X,y training data
                test_data tuple containing X,y test data"""

        self.X_train = training_data[0]
        self.y_train = training_data[1]
        self.X_test = test_data[0]
        self.y_test = test_data[1]

        self.verbose = verbose

        if model == 'LASSO':
            self.model = Lasso(alpha = 1.0) #'alpha' --> lambda value

        elif model == 'NB':
            self.model = GaussianNB()

        elif model == 'RandomForest':
            
            print("Initialising Random Forest Classifier...\n")
            self.model = RandomForestClassifier(max_depth=None, random_state=0)
        else:
            raise ValueError("Invalid model type argument")
                                           
        self.train()
        self.test()

    
        
    def train(self):
        print(f"Training {self.model} ...\n")
        return self.model.fit(self.X_train, self.y_train)

    def validate(self):
        pass

    def predict(self, X_test = None):
        """Returns predicted data"""
        return self.model.predict(self.X_test)

    def test(self, X_test = None, y_test = None): 
        """Scores model's predictions"""
        pred = self.predict()    
        print("Accuracy of: ", np.mean(pred == self.y_test))

    def store_model(self):
        #Store the model
        pass

