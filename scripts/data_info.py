import pandas as pd

class DataFrameInfo():
    def __init__(self, df):
        self.df = df.copy()


    def get_columns_list(self):
        '''
        Return Column list of the Dataframe
        '''
        return self.df.columns.to_list()


    def detail_info(self):
        '''
        Display the detail of the DataFrame information
        '''

        print(self.df.info())


    def null_column_percentage(self):
        '''
        Display Total Null percentage of the Data Frame Columns
        '''

        num_rows, num_columns = self.df.shape
        df_size = num_rows * num_columns
        
        null_size = (self.df.isnull().sum()).sum()
        percentage = round((null_size / df_size) * 100, 2)
        print(f"The Telecom data contains { percentage }% missing values.")


    def get_null_counts(self):
        '''
        Display Null Counts of each column
        '''

        print(self.df.isnull().sum())

#df.skew().sort_values(ascending=False)
    def skewness(self):
        '''
        Display The skew value of each columns 
        '''
        print(self.df.skew())