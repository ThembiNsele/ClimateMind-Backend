from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import Lasso, LassoCV, LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score
from sklearn.model_selection import KFold, cross_validate
from sklearn import metrics
import pickle
import numpy as np

# RRR: Why two binary models instead of:
# 1. Regression model?
""" Data contains mostly center/neutral political orientation instances. During our first attempts (admittedly)
without balancing the data the model was learning to predict mostly values 4 - 5.5. We are mostly concerned about radical people so the 
'radical binning' approach seemed to guarantee predicting those instances.
 """
# 2. 3 class classification - L, R, N
"""Good point and definitely something to look into. At this point the double binary classification implementation just simplified the task
and made it easier to train baseline models with decent scores while focusing on the radical instances
Do you think there is something wrong with this approach? """


class Model:
    def __init__(
        self,
        model,
        target_class,
        training_data=None,
        test_data=None,
        loaded_model_path=None,
        verbose=False,
    ):
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

        if model == "LASSO":

            # self.model = Lasso(alpha = 1.0) #'alpha' --> lambda value
            self.model = LassoCV(
                alphas=np.arange(0.0, 1, 0.01), n_jobs=-1, verbose=False
            )  # Automatic hyperparameter optimization

        elif model == "NaiveBayes":
            print("Initialising Naive Bayes classifier...\n")

            self.model = GaussianNB()

        elif model == "RandomForest":
            print("Initialising Random Forest Classifier...\n")

            self.model = RandomForestClassifier(max_depth=None, random_state=0)

        elif model == "Pretrained":
            print(
                f"Loading pretrained model from {loaded_model_path}...\n"
            )

            self.model = pickle.load(open(loaded_model_path, "rb"))

        else:
            raise ValueError("Invalid model type argument or missing path")

        if model != "Pretrained":

            self.train()

    def train(self): #,X=self.X_train, y=self.y_train):
        print(f"Training {self.model} ...\n")
        return self.model.fit(self.X_train, self.y_train)
        
            
    def validate(self,k=10):
        cv_results = cross_validate(self.model, self.X_train, self.y_train, scoring=['accuracy', 'f1', 'precision', 'recall'])
        return cv_results
        #ToDo: return results, add possibility for hyperparameter tweaking

    def predict(self, X_test=None):
        """Returns predicted data"""
        #print("THE ATTRIBUTES:")
        #print(self.X_test)
        return self.model.predict(self.X_test)

    def test(self, X_test=None, y_test=None):
        """Scores model's predictions. Prints Accuracy, sensitivity, & specificity"""

        if self.model_type == "LASSO":

            alpha_value = self.model.alpha_
            print("\nAlpha: ", alpha_value)
            coeficients = self.model.coef_
            print("Coefficients ", coeficients, "\n")
            determination_coefficient = self.model.score(self.X_test, self.y_test)
            print("Determination coefficient r^2: ", determination_coefficient, "\n")


            preds = self.predict()          
            preds = [round(pred) for pred in preds]#Using LASSO as a classifier
            self.model_accuracy = np.mean(preds == self.y_test)
            print("\nScores for ", self.model_type, " predicting ", self.target_class, "\n")
            print(self.model_accuracy)

            
        else:

            preds = self.predict()
            ######
            print("Predicted:")
            print(preds)
            print("Actual:")
            print(self.y_test)
            self.model_accuracy = np.mean(preds == self.y_test)

        def sensitivity(TP, FN):
            return TP / (TP + FN)

        def specificity(TN, FP):
            return TN / (TN + FP)

        tn, fp, fn, tp = metrics.confusion_matrix(self.y_test, preds).ravel()

        print("\nScores for ", self.model_type, " predicting ", self.target_class, "\n")
        print("Accuracy: ", accuracy_score(self.y_test, preds, "\n"))
        print("Sensitivity: ", sensitivity(tp, fn), "\n")
        print("Specificity: ", specificity(tn, fp), "\n")

    def store_model(self, directory):

        file_name = (
            directory
            + self.model_type
            + "_"
            + self.target_class
            + "_"
            + str(round(self.model_accuracy, 3))
            + ".pickle"
        )
        pickle.dump(self.model, open(file_name, "wb"))  # write in binary mode
        print("Model stored succesfully!\n")
