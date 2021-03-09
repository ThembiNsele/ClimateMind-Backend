from data_processor import *
from model import *
import imblearn
print("imblearn version", imblearn.__version__)

    # """ Call data processor 
    #     call DataProcessor.split() to get train and test data
    #     Call model and pass train, test data
    #     Call model.test"""

def main():

    conservative = DataProcessor("../datasets/pvq21_REVERSED_CENTRED.csv", 7)
    X_train, X_test, y_train, y_test = conservative.split_data()

    RF_model = Model("RandomForest", (X_train, y_train), (X_test, y_test))

    
if __name__ == "__main__":
    main()
    
