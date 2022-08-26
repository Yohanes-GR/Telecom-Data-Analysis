# importing library
import pandas as pd
import numpy as np
# creating class
class DataFrameCleaning():
    def __init__(self, df):
        self.df = df.copy()
        print('Automation in Action...Great!!!')
    

    def get_column_with_many_null(self):
        '''
        Return List of Columns which contain more than 30% of null values
        '''
        df_size = self.df.shape[0]
        
        columns_list = self.df.columns
        many_null_columns = []
        
        for column in columns_list:
            null_per_column = self.df[column].isnull().sum()
            percentage = round((null_per_column / df_size) * 100 , 2)
            
            if(percentage > 30):
                many_null_columns.append(column)
        
        return many_null_columns
    

    def drop_columns(self, columns):
        '''
        Return Dataframe with Most null columns removed.
        '''

        self.df.drop(columns, axis=1, inplace=True)


    def convert_to_datetime(self, df):
        """
        convert start and end column to datetime
        """

        df['Start'] = pd.to_datetime(df['Start'])
        df['End'] = pd.to_datetime(df['End'])

        return df


    def drop_duplicate(self, df):
        """
        drop duplicate rows
        """
        df.drop_duplicates(inplace=True)

        return df


    def drop_rows(self, columns):
        '''
        Drop Rows of specified columns, which contain null values
        '''
        self.df.dropna(subset=columns, inplace=True)

    
    def fill_numerical_column(self, column):
        '''
        Fill Numerical null values with mean or median based on the skewness of the column
        '''
 
        for col in column:
            skewness = self.df[col].skew() 
            if((-1 < skewness) and (skewness < -0.5)):
                self.df[col] = self.df[col].fillna(self.df[col].mean()) 

            else:
                self.df[col] = self.df[col].fillna(self.df[col].median())

    
    def fill_categorical_columns(self, column):
        '''
        Fill Categorical null values with column Mode
        '''
 
        for col in column:
            mode = self.df[col].mode()[0]
            self.df[col] = self.df[col].fillna(mode)