from data_processor import *
from model import *


# print("imblearn version", imblearn.__version__)

RANK = True
BALANCE = "oversampling"
MODEL = "NaiveBayes"

def main():

    # Radical-conservative run
    conservatives = DataProcessor(
        "../datasets/ESS/ess_8-9_merged.csv",
        "conservative",
        6, 
        rank=RANK
    )
    X_train, X_test, y_train, y_test = conservatives.split_data()

    if BALANCE == "oversampling":
        X_train, y_train = conservatives.oversample(X_train, y_train)
    elif BALANCE == "undersampling":
        X_train, y_train = conservatives.undersample(X_train, y_train)

    RF_con_model = Model(MODEL, "conservative", (X_train, y_train), (X_test, y_test), loaded_model_path="../models/RandomForest_conservative_0.738.pickle") #returns a trained model

    #print(RF_con_model.validate())
    RF_con_model.test()
    RF_con_model.store_model(directory="../models/")

    # Radical-liberal run
    liberals = DataProcessor(
        "../datasets/ESS/ess_8-9_merged.csv",
        "liberal",
        4, 
        rank=RANK
    )
    X_train, X_test, y_train, y_test = liberals.split_data()

    if BALANCE == "oversampling":
            X_train, y_train = conservatives.oversample(X_train, y_train)
    elif BALANCE == "undersampling":
        X_train, y_train = conservatives.undersample(X_train, y_train)

    RF_lib_model = Model(MODEL, "Pretrained", (X_train, y_train), (X_test, y_test), loaded_model_path="../models/RandomForest_liberal_0.785.pickle")

    #RF_lib_model.validate()
    RF_lib_model.test()
    RF_lib_model.store_model(directory="../models/")


if __name__ == "__main__":
    main()
