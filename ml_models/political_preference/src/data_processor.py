import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

class DataProcessor():

    """
    TODO:

    - verbocity flag - implement
    - handle liberal datasets implement
        - Use one object for both conservatives and liberals and return both at once OR use separately? Perhaps the second is better from an OOP perspective
    """

    def __init__(self, dataset, con_threshold, balance_method = None,  rank = False, verbose = False):
        super().__init__()

        self.data = pd.read_csv(dataset, sep=',')
        self.verbose = verbose
        self.con_threshold = con_threshold

        if balance_method == 'oversample':
            #Call oversampling method
            self.oversample()
        elif balance_method == 'undersample':
            #Call undersampling method
            self.undersample()
        else:
            pass

        radical_conservative_df = self.bin_data()
        self.X = radical_conservative_df.iloc[:, 1:11] #get the attributes
        self.y = radical_conservative_df.iloc[:,0] #target value

        self.y = self.encode(self.y)

        if rank:
            print("Ranking data...\n")
            #Call ranking method
            self.rank_data()

    def bin_data(self):
        """@returns radical liberal dataframe & radical conservative dataframe"""

        rad_libs_df = self.data.copy() #work on a copy of the dataset
        rad_cons_df = self.data.copy() #same for dataset with radical conservative scores

        def bin_libs(lr_score):

            if lr_score < self.lib_threshold:
                return 1 #radical liberal
            else:
                return 0 #not liberal

        def bin_cons(lr_score):

            if lr_score >= self.con_threshold:
                return 1 # radical conservative
            else:
                return 0 #not conservative

        #rad_libs_df['lrscale'] = rad_libs_df['lrscale'].apply(bin_libs) TODO
        rad_cons_df['lrscale'] = rad_cons_df['lrscale'].apply(bin_cons)

        return rad_cons_df
        


    def oversample(self):
        print("Oversampling data...\n")
        pass

    def undersample(self):
        print("Undersampling data...\n")
        pass

    def rank_data(self):
        print("Ranking data...\n")

    def encode(self, target_data, type = 'label'):
        """@returns encoded target data"""

        #label and one hot encode, for MVP just label encoding
        if type == 'label':

            label_encoder = LabelEncoder()
            y_labeled = label_encoder.fit_transform(target_data)
        
        return y_labeled

    def decode(self, type = 'label'):
        #label and one-hot decode, for MVP just label decoding
        pass

    def split_data(self, split = 0.2):
        """returns data split in training and test """
        return train_test_split(self.X, self.y)


