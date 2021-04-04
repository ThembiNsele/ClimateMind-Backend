from data_processor import *
from model import *


#print("imblearn version", imblearn.__version__)

def main():

    #Radical-conservative run
    conservatives = DataProcessor("ml_models/political_preference/datasets/pvq21_REVERSED_CENTRED.csv", 'conservative', 7)
    X_train, X_test, y_train, y_test = conservatives.split_data()

    RF_con_model = Model("LASSO", "conservative", (X_train, y_train), (X_test, y_test))
    RF_con_model.test()
    #RF_con_model.store_model()

    #Radical-liberal run
    liberals = DataProcessor("ml_models/political_preference/datasets/pvq21_REVERSED_CENTRED.csv", 'liberal', 3)
    X_train, X_test, y_train, y_test = liberals.split_data()

    RF_lib_model = Model("LASSO", "liberal", (X_train, y_train), (X_test, y_test))
    RF_lib_model.test()
    #RF_lib_model.store_model()


if __name__ == "__main__":
    main()

