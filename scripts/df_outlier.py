import os
import sys
import pandas as pd
import numpy as np
    
def fix_outlier(df, column):
    df[column] = np.where(df[column] > df[column].quantile(0.95), df[column].mode(),df[column])

    return df[column]


def replace_outliers_with_iqr(df, columns):
    for col in columns:
        Q1, Q3 = df[col].quantile(0.25), df[col].quantile(0.75)
        IQR = Q3 - Q1
        cut_off = IQR * 1.5
        lower, upper = Q1 - cut_off, Q3 + cut_off

        df[col] = np.where(df[col] > upper, upper, df[col])
        df[col] = np.where(df[col] < lower, lower, df[col])