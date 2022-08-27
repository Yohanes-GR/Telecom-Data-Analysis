import sys
import os
import sys
import numpy as np
import pandas as pd
import streamlit as st


def loadDescription():
    df = pd.read_csv("../data/Field_Descriptions.csv")
    return df


def loadOriginalData():
    df = pd.read_csv("../data/Week1_challenge_data_source(CSV).csv")
    return df


def loadPreprocessedData():
    df = pd.read_csv("../data/cleaned_Telecom_data.csv")
    return df


def app():
    st.title('TellCo Telecom Analytics Overview')

    st.header('Table Description')
    st.markdown(
    '''
        The Telecom Dataset has 150001 observations with 55 columns. 
        Here is the description of each columns.
    ''')
    df = loadDescription()
    st.write(df, width=1200)

    st.header('Here is a sample Data from the Table')
    df = loadOriginalData()
    st.write(df.head(10))
