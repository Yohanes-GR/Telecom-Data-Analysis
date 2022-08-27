import sys
import os
import sys 
import pickle
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px

sys.path.append(os.path.abspath(os.path.join('../scripts')))
import plots

@st.cache
def getEngagemetData():
    df = pd.read_csv("../data/user_engagement.csv")
    return df


@st.cache
def getExperienceData():
    df = pd.read_csv("../data/user_experiance.csv")
    df.rename(columns = {'MSISDN_Number':'Customer_Id'}, inplace=True)
    return df


def getEngagemetModel():
    with open("../models/user_engagement.pkl", "rb") as f:
        kmeans = pickle.load(f)
    return kmeans

def getExperienceModel():
    with open("../models/user_experiance.pkl", "rb") as f:
        kmeans = pickle.load(f)
    return kmeans

def getUserEngagement(less_engagement):
    eng_df = getEngagemetData().copy()
    eng_model = getEngagemetModel() 
    eng_df = eng_df.set_index('Customer_Id')[
        ['Session_Frequency', 'Duration', 'Total_Data_Volume']]
        
    distance = eng_model.fit_transform(eng_df)
    distance_from_less_engagement = list(
        map(lambda x: x[less_engagement], distance))
    eng_df['Engagement_Score'] = distance_from_less_engagement
    return eng_df

def getUserExperience(worst_experience):
    exp_df = getExperienceData().copy()
    exp_model = getExperienceModel()
    exp_df = exp_df.set_index('Customer_Id')[
        ["Total_Avg_RTT", "Total_Avg_Bearer_TP", "Total_Avg_TCP"]] 
        
    distance = exp_model.fit_transform(exp_df)
    distance_from_worst_experience = list(
        map(lambda x: x[worst_experience], distance))
    exp_df['Experience_Score'] = distance_from_worst_experience
    return exp_df

def getSatisfactionData(less_engagement, worst_experience):
    user_engagement = getUserEngagement(less_engagement)
    user_experience = getUserExperience(worst_experience)

    user_engagement.reset_index(inplace=True)
    user_experience.reset_index(inplace=True)

    user_id_engagement = user_engagement['Customer_Id'].values
    user_id_experience = user_experience['Customer_Id'].values

    user_intersection = list(
        set(user_id_engagement).intersection(user_id_experience))

    user_engagement_df = user_engagement[user_engagement['Customer_Id'].isin(
        user_intersection)]
    
    user_experience_df = user_experience[user_experience['Customer_Id'].isin(
        user_intersection)]
    
    user_df = pd.merge(user_engagement_df, user_experience_df, on='Customer_Id')
    user_df['Satisfaction_Score'] = (
        user_df['Engagement_Score'] + user_df['Experience_Score'])/2
    sat_score_df = user_df[['Customer_Id', 'Engagement_Score',
                            'Experience_Score', 'Satisfaction_Score']]
    sat_score_df = sat_score_df.set_index('Customer_Id')
    return sat_score_df

def app():
    st.title('User Satisfaction Analysis')
    num1 = st.sidebar.selectbox('Select the cluster with less Engagement', range(0, 20))
    num2 = st.sidebar.selectbox('Select the cluster with worst Experience', range(0, 20))
    if st.sidebar.button('Ok'):
        df = getSatisfactionData(num1, num2)

        st.header("Top 10 customers per users Satisifaction")
        sorted_by_satisfaction = df.sort_values(
            'Satisfaction_Score', ascending=False)
        sat_top_10 = sorted_by_satisfaction['Satisfaction_Score'].head(10)
        
        st.markdown(
        '''
            Plot showing relationship between Engagement score and Satisfaction score.        
        ''')
        plots.scatter2d(df, 'Engagement_Score', 
                'Experience_Score', 'Satisfaction_Score')

