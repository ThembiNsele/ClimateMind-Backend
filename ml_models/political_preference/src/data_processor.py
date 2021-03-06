import pandas as pd 

class DataProcessor():


    def __init__(self, dataset, balance_method = None,  rank = False, verbose = False):
        super().__init__()

        self.data = pd.read_csv(dataset, sep=',')
        self.verbose = verbose
        
        if balance_method == 'oversample':
            #Call oversampling method
            self.oversample()
        elif balance_method == 'undersample':
            #Call undersampling method
            self.undersample()
        else:
            pass

        if rank:
            print("Ranking data...\n")
            #Call ranking method
            self.rank_data()


    def oversample(self):
        print("Oversampling data...\n")
        pass

    def undersample(self):
        print("Undersampling data...\n")
        pass
    
    def rank_data(self):
        print("Ranking data...\n")

    def encode(self, type = 'label'):
        #label and one hot encode, for MVP just label encoding
        pass

    def decode(self, type = 'label'):
        #label and one-hot decode, for MVP just label decoding
        pass

    def split_data(self, split = 0.2):
        """returns data split in training and test """
        pass

