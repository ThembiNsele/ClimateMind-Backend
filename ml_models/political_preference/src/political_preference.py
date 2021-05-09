from data_processor import *
from model import *


# print("imblearn version", imblearn.__version__)
RUN = 'TEST'
RANK = True
BALANCE = 'oversample'
MODEL = "Pretrained"
STORE = False

def main():

    if RUN == 'TRAIN':
        # Radical-conservative run
        conservatives = DataProcessor(
            "../datasets/ESS/ess_8-9_merged.csv",
            "conservative",
            8, 
            rank=RANK
        )
        X_train, X_test, y_train, y_test = conservatives.split_data()

        if BALANCE == "oversampling":
            X_train, y_train = conservatives.oversample(X_train, y_train)
        elif BALANCE == "undersampling":
            X_train, y_train = conservatives.undersample(X_train, y_train)

        RF_con_model = Model(MODEL, "conservative", (X_train, y_train), (X_test, y_test), loaded_model_path="../models/NaiveBayes_conservative_0.586.pickle") #returns a trained model
        RF_con_model.train()
        #print(RF_con_model.validate())
        RF_con_model.test()
        

        #Radical-liberal run
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

        RF_lib_model = Model(MODEL, "liberal", (X_train, y_train), (X_test, y_test), loaded_model_path="../models/NaiveBayes_liberal_0.641.pickle")

        #RF_lib_model.validate()
        RF_lib_model.test()

        if STORE == True:
            RF_con_model.store_model(directory="../models/")
            RF_lib_model.store_model(directory="../models/")


    elif RUN == 'TEST':

        ######## CONSERVATIVE PREDICTION RUN ########

        conservatives = DataProcessor(
            "../datasets/database_test_data.csv",
            "conservative",
            7, 
            rank=RANK
        )
        
        X_test, y_test = conservatives.get_data()

        con_model = Model(MODEL,
                         "conservative", 
                        (X_test, y_test), 
                        (X_test, y_test), 
                        loaded_model_path="../models/NaiveBayes_conservative_ranked_0.708.pickle") #returns a trained model

        con_model.test()
        ######## LIBERAL PREDICTION RUN ########

        liberals = DataProcessor(
            "../datasets/database_test_data.csv",
            "liberal",
            3, 
            rank=RANK
        )

        X_test, y_test = liberals.get_data()

        lib_model = Model(MODEL, 
                        "liberal", 
                        (X_test, y_test), 
                        (X_test, y_test), 
                        loaded_model_path="../models/NaiveBayes_liberal_ranked_0.569.pickle")

        lib_model.test()

if __name__ == "__main__":
    main()
