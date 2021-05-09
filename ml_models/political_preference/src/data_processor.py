import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from imblearn.under_sampling import RandomUnderSampler, TomekLinks
from imblearn.over_sampling import RandomOverSampler

from collections import Counter


class DataProcessor:

    """
    TODO:
    - implement verbocity flag [print data distributions, ]
    """

    def __init__(
        self,
        dataset,
        target_class,
        lr_threshold,
        balance_method=None,
        rank=False,
        verbose=False,
    ):
        #super().__init__()

        self.data = pd.read_csv(dataset, sep=",")
        self.target_class = target_class
        self.lr_threshold = lr_threshold
        self.verbose = verbose

        if balance_method == "oversample":

            self.oversample()  # Call oversampling method

        elif balance_method == "undersample":

            self.undersample()  # Call undersampling method

        else:
            pass  # TODO

        rad_binned_data = self.bin_data()  # get the binned radical data

        # NOTE:The assumption here is that the first column is the lr score column and the rest
        #      are feature vectors. Last column (12) is average score and is also ignored
        self.X = rad_binned_data.iloc[:, 1:11]  # get the attributes
        self.y = rad_binned_data.iloc[:, 0]  # target value

        # alphabetise attributes
        self.X = self.X.reindex(sorted(self.X.columns), axis=1)

        # self.y = self.encode(self.y)

        if rank:

            self.data = self.rank_data()  # Call ranking method

        
    def get_data(self):
        return self.X, self.y


    def bin_data(self):
        """@returns radical liberal dataframe & radical conservative dataframe"""

        rad_to_bin_df = self.data.copy()  # work on a copy of the dataset

        def bin_libs(lr_score):

            if lr_score <= self.lr_threshold:
                return 1  # radical liberal
            else:
                return 0  # not liberal

        def bin_cons(lr_score):

            if lr_score >= self.lr_threshold:
                return 1  # radical conservative
            else:
                return 0  # not conservative

        if self.target_class == "liberal":
            print(
                f"\nBinning radical liberal instances with lr score <= {self.lr_threshold}\n"
            )

            rad_to_bin_df["lrscale"] = rad_to_bin_df["lrscale"].apply(bin_libs)

        elif self.target_class == "conservative":
            print(
                f"\nBinning radical conservative instances with lr score >= {self.lr_threshold}\n"
            )

            rad_to_bin_df["lrscale"] = rad_to_bin_df["lrscale"].apply(bin_cons)

        return rad_to_bin_df

    def oversample(self, X, y):

        print(f"Unbalanced counts: {Counter(y)}")

        print("Oversampling data...\n")
        random_over_sampler = RandomOverSampler(random_state=42, sampling_strategy=0.8)
        X_over_sampled, y_over_sampled  = random_over_sampler.fit_resample(X, y)
      
        print(f"Balanced counts: {Counter(y_over_sampled)}")

        return X_over_sampled, y_over_sampled 

    def undersample(self, X, y):
        
        print(f"Unbalanced counts: {Counter(y)}")

        print("Undersampling data...\n")
        random_under_sampler = TomekLinks(sampling_strategy='majority')#RandomUnderSampler(random_state=42, sampling_strategy=0.8)#
        X_under_sampled, y_under_sampled  = random_under_sampler.fit_resample(X, y)
      
        print(f"Balanced counts: {Counter(y_under_sampled)}")

        return X_under_sampled, y_under_sampled 


    def rank_data(self):
        print("Ranking data...\n")

        df_copy = self.data.copy()
        ranked_df = pd.DataFrame()
        col_name = ''
        for column_name, data in df_copy.iteritems():
            for other_column_name, other_data in df_copy.iteritems():
                if column_name != other_column_name:
                    comp_col_name = column_name + ' < ' + other_column_name
                    ranked_df[comp_col_name] = df_copy[column_name] < df_copy[other_column_name]

        return ranked_df


    def split_data(self, split=0.2):
        """returns data split in training and test """
        return train_test_split(self.X, self.y)
