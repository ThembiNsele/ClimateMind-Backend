#from lzma import *
from data_processor import *

def main():
    """ Call data processor 
        call DataProcessor.split() to get train and test data
        Call model and pass train, test data
        Call model.test"""
    print("Running?")
    DataProcessor("./datasets/pvq21_REVERSED_CENTRED.csv")

    

if __name__ == "main":
    main()