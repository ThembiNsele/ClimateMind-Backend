# RRR: pandas is not used in this file
import pandas as pd
import numpy as np
# RRR: Not used
from sklearn.model_selection import train_test_split, cross_validate
from sklearn.preprocessing import OneHotEncoder, LabelEncoder

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import Lasso, LassoCV, LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score # RRR: not used classification_report
from sklearn import metrics
# RRR Not used
import matplotlib.pyplot as plt

import pickle

# RRR: Why two binary models instead of:
# 1. Regression model?
# 2. 3 class classification - L, R, N

class Model():


    def __init__ (self, model, target_class, training_data, test_data, loaded_model_path = None, verbose = False):
        """@args model: string,
                target_class: string (i.e. 'liberal' or 'conservative')
                training_data tuple containing X,y training data
                test_data tuple containing X,y test data"""
        self.model_type = model
        self.target_class = target_class
        self.X_train = training_data[0]
        self.y_train = training_data[1]
        self.X_test = test_data[0]
        self.y_test = test_data[1]
        self.target_class = target_class
        self.verbose = verbose
        self.model_accuracy = None

        if model == 'LASSO':

            #self.model = Lasso(alpha = 1.0) #'alpha' --> lambda value
            self.model = LassoCV(alphas = np.arange(0, 1, 0.01), n_jobs = -1, verbose = False) #Automatic hyperparamete optimization

        elif model == 'NB':
            print("Initialising Naive Bayes classifier...\n")

            self.model = GaussianNB()

        elif model == 'RandomForest':
            print("Initialising Random Forest Classifier...\n")

            self.model = RandomForestClassifier(max_depth=None, random_state=0)

        elif model == 'Preloaded':
            print(f"Loading preloaded {target_class} model from {loaded_model_path}...\n")

            self.model = pickle.load(open(loaded_model_path, 'rb'))

        else:
            raise ValueError("Invalid model type argument or missing path")

        if model != 'Preloaded':

            self.train()


    def train(self):
        print(f"Training {self.model} ...\n")

        return self.model.fit(self.X_train, self.y_train)

    def validate(self):
        pass #ToDo

    def predict(self, X_test = None):
        """Returns predicted data"""
        return self.model.predict(self.X_test)

    def test(self, X_test = None, y_test = None):
        """Scores model's predictions. Prints Accuracy, sensitivity, & specificity"""

        if self.model_type == "LASSO":
            print("\nScores for ", self.model_type, " predicting ", self.target_class, "\n")
            alpha_value = self.model.alpha_
            print("\nAlpha: ", alpha_value)
            coeficients = self.model.coef_
            print("Coefficients ", coeficients, "\n")
            determination_coefficient = self.model.score(self.X_test, self.y_test)
            print("Determination coefficient r^2: ", determination_coefficient, "\n")
            return 1

        pred = self.predict()
        self.model_accuracy = np.mean(pred == self.y_test)
        # print("Custom measure of (?) Accuracy: ", self.model_accuracy, "\n")

        def sensitivity(TP, FN):
            return (TP/(TP+FN))

        def specificity(TN, FP):
            return (TN/(TN+FP))

        tn, fp, fn, tp = metrics.confusion_matrix(self.y_test, pred).ravel()

        print("\nScores for ", self.model_type, " predicting ", self.target_class, "\n")
        print("Accuracy: ", accuracy_score(self.y_test, pred, "\n"))
        print("Sensitivity: ", sensitivity(tp, fn), "\n")
        print("Specificity: ", specificity(tn, fp), "\n")


    def store_model(self):

        # RRR: it is preferred to add a .pickle extension to the pickle file so someone knows what type it is
        file_name = "../models/" + self.model_type + "_" + self.target_class + "_" + str(round(self.model_accuracy, 3)) #ATTENTION directory path differs between Mac/Win OS
        pickle.dump(self.model, open(file_name, 'wb')) #write in binary mode
        print("Model stored succesfully...\n")

