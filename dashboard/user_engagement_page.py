import pickle
from pydoc import Helper
import sys
import os
import sys
import pandas as pd
import streamlit as st
from sklearn.cluster import KMeans
from user_experience_page import hist

sys.path.append(os.path.abspath(os.path.join('../scripts'))) 
import plots

@st.cache
def loadCleanData():
    df = pd.read_csv("../data/user_engagement.csv")
    return df

@st.cache
def getEngagemetData():
    df = loadCleanData().copy()
    user_engagement_df = df[['Customer_Id', 'Session_Frequency', 'Duration', 'Total_Data_Volume']].copy()
    user_engagement = df.groupby(
        'Customer_Id').agg({'Session_Frequency': 'count', 'Duration': 'sum', 'Total_Data_Volume': 'sum'}) 
    return user_engagement


def plotTop10(df): 
    col = st.sidebar.selectbox(
        "Select top 10 from", (["Session_Frequency", "Duration", "Total_Data_Volume"]))
    if col == "Sessions_Frequency":
        sessions = df.nlargest(10, "Session_Frequency")['Sessions_Frequency']
        return hist(sessions)
    elif col == "Duration":
        duration = df.nlargest(10, "Duration")['Duration']

        return plots.mult_hist([duration], 1, 1, "User Engagement Duration", ['Duration (sec)'])

    else:
        total_data_volume = df.nlargest(
            10, "Total_Data_Volume")['Total_Data_Volume']
        
        return plots.mult_hist([total_data_volume], 1, 1, "User Engagement Total Data Volume", ['Total Data Volume (kbps)'])


def app():
    st.title('User Engagement Analysis')
    st.header("Top 10 customers per Engagement Metric")
    user_engagement = getEngagemetData().copy()  
    plotTop10(user_engagement)

    st.header("Clustering customers based on their Engagement metric")
    st.markdown(
    '''
        Here we will try to cluster customers based on their Engagement.
        To start, choose the number of times to runs k-means.
    ''')
    num = st.selectbox('Select', range(0, 20))
    select_num = 1
    if(num != 0): 

        st.markdown(
        '''
            Select the optimized values for k
        ''')
        select_num = st.selectbox('Select', range(1, num+1))

    if(select_num != 1):

        kmeans = KMeans(n_clusters=select_num, random_state=0).fit(user_engagement)
        user_engagement.insert(0, 'Cluster', kmeans.labels_)

        st.markdown(
        '''
            Number of elements in each cluster
        ''')
        st.write(user_engagement['Cluster'].value_counts())

        show2D = False
        if st.button('Show 2D visualization'):
            if(show2D):
                show2D = False
            else:
                show2D = True


        if(show2D):
            st.markdown(
            '''
                2D Visualization of Vluster
            ''')

            plots.scatter2d(user_engagement, x='Total_Data_Volume', y="Duration", c='Cluster', s='Session_Frequency') 
        
        show3D = False
        if st.button('Show 3D Visualization'):
            if(show3D == True):
                show3D = False
            else:
                show3D = True
        if(show3D):
            st.markdown(
            '''
                3D Visualization of Cluster
            ''')
                       
            plots.scatter3D(user_engagement, 'Total_Data_Volume', "Duration", 'Session_Frequency', 'Cluster', interactive=True) 
        
        st.warning(
            'Remember cluster with the least engagement. we need that for satisfaction analysis')
        st.markdown(
        '''
            Save the model for user satisfaction analysis
        ''')
        if st.button('Save Model'):
            Helper.save_csv(user_engagement,
                            '../data/user_engagement.csv', index=True)

            with open("../models/user_engagement.pkl", "wb") as f:
                pickle.dump(kmeans, f)