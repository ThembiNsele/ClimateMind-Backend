import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

class DataProcessor():

    """
    TODO:
    - implement verbocity flag [print data distributions, ]
    """


    def __init__(self, dataset, target_class, lr_threshold, balance_method = None,  rank = False, verbose = False):
        super().__init__()

        self.data = pd.read_csv(dataset, sep=',')
        self.target_class = target_class
        self.lr_threshold = lr_threshold
        self.verbose = verbose

        if balance_method == 'oversample':

            self.oversample() #Call oversampling method

        elif balance_method == 'undersample':

            self.undersample() #Call undersampling method

        else:
            pass #TODO

        rad_binned_data = self.bin_data() #get the binned radical data

        # NOTE:The assumption here is that the first column is the lr score column and the rest
        #      are feature vectors.
        self.X = rad_binned_data.iloc[:, 1:11] #get the attributes
        self.y = rad_binned_data.iloc[:,0] #target value

        print("data x")
        print(type(self.X))

        self.y = self.encode(self.y)

        if rank:
            print("Ranking data...\n")

            self.rank_data() #Call ranking method

    def bin_data(self):
        """@returns radical liberal dataframe & radical conservative dataframe"""

        rad_to_bin_df = self.data.copy() #work on a copy of the dataset

        def bin_libs(lr_score):

            if lr_score <= self.lr_threshold:
                return 1 #radical liberal
            else:
                return 0 #not liberal

        def bin_cons(lr_score):

            if lr_score >= self.lr_threshold:
                return 1 # radical conservative
            else:
                return 0 #not conservative

        if self.target_class == 'liberal':
            print(f"\nBinning radical liberal instances with lr score <= {self.lr_threshold}\n")

            rad_to_bin_df['lrscale'] = rad_to_bin_df['lrscale'].apply(bin_libs)

        elif self.target_class == 'conservative':
            print(f"\nBinning radical conservative instances with lr score <= {self.lr_threshold}\n")

            rad_to_bin_df['lrscale'] = rad_to_bin_df['lrscale'].apply(bin_cons)

        return rad_to_bin_df

    def oversample(self):
        print("Oversampling data...\n")
        #TODO
        pass

    def undersample(self):
        print("Undersampling data...\n")
        pass #TODO

    def rank_data(self):
        print("Ranking data...\n")
        pass #TODO

    def encode(self, target_data, type = 'label'):
        """@returns encoded target data"""
        #label and one hot encode, for MVP just label encoding
        if type == 'label':

            label_encoder = LabelEncoder()
            y_labeled = label_encoder.fit_transform(target_data)
        else:
            #ToDo: implement alternative to label encoding
            label_encoder = LabelEncoder()
            y_labeled = label_encoder.fit_transform(target_data)

        return y_labeled

    def decode(self, type = 'label'):
        #label and one-hot decode, for MVP just label decoding
        pass #TODO

    def split_data(self, split = 0.2):
        """returns data split in training and test """
        return train_test_split(self.X, self.y)


