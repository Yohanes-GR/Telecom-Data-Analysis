import sys
import os
import sys
import pandas as pd
import streamlit as st
import plotly.io as pio
import plotly.express as px
from sklearn.cluster import KMeans

sys.path.append(os.path.abspath(os.path.join('../scripts'))) 
import plots

@st.cache
def loadCleanData():
    df = pd.read_csv("../data/user_experiance.csv")
    return df

@st.cache
def getExperienceDataFrame():
    df = loadCleanData().copy()
    user_experience_df = df[[\
        "MSISDN_Number", "Total_Avg_RTT", "Total_Avg_Bearer_TP", "Total_Avg_TCP"]].copy() 

    return user_experience_df

@st.cache
def getExperienceData():
    df = getExperienceDataFrame().copy()
    user_experience = df.groupby('MSISDN_Number').agg({
        'Total_Avg_RTT': 'sum',
        'Total_Avg_Bearer_TP': 'sum',
        'Total_Avg_TCP': 'sum'})
    return user_experience


def hist(sr, interactive=False):
    x = ["Id: " + str(i) for i in sr.index]
    fig = px.histogram(x=x, y=sr.values)
    if(interactive):
        st.plotly_chart(fig)
    else:
        st.image(pio.to_image(fig, format='png', width=1200))

def plot10(df):
    col = st.selectbox("Compute & list 10 of the top, bottom and most frequent: from", (
        [
            "TCP values",
            "Duration", 
            "Throughput values"
        ]))
    if col == "TCP values":
        sorted_by_tcp = df.sort_values('Total_Avg_TCP', ascending=False)
        return plot10Sorted(sorted_by_tcp, 'Total_Avg_TCP')

    elif col == "RTT values":
        sorted_by_rtt = df.sort_values('Total_Avg_RTT', ascending=False)
        return plot10Sorted(sorted_by_rtt, 'Total_Avg_RTT')  

    else:
        sorted_by_tp = df.sort_values('Total_Avg_Bearer_TP', ascending=False)
        return plot10Sorted(sorted_by_tp, 'Total_Avg_Bearer_TP')


def plot10Sorted(df, col_name):
    col = st.selectbox("Select from: from", (
        [
            "Top 10",
            "Last 10",
        ]))
    
    if col == "Top 10":
        sat_top_10 = df.head(10)[col_name]
        return hist(sat_top_10)
    else:
        sat_last_10 = df.tail(10)[col_name]
        return hist(sat_last_10)

def app():
    st.title('User Experience Analytics')
    st.header("Top 10 customers per Experience Metric")
    user_experience = getExperienceData().copy() 
    plot10(user_experience)

    st.header("Clustering customers based on their Experience")
    st.markdown(
    '''
        Here we will try to cluster customers based on their experience.
        To find the optimized value of k, first, let's plot an elbow curve graph.
        To start, choose the number of times to runs k-means.
    ''')
    num = st.selectbox('Select', range(0, 20))
    select_num = 1

    if(num != 0): 
        select_num = st.selectbox('Select', range(1, num+1))

    if(select_num != 1):
        st.markdown(
        '''
            Based on the image above choose the number of clusters
        ''')
        kmeans = KMeans(n_clusters=select_num, random_state=0).fit(user_experience)
        user_experience["Cluster"] = kmeans.labels_

        st.markdown(
        '''
            Number of elements in each cluster
        ''')
        st.write(user_experience['Cluster'].value_counts())

        show2D = False
        if st.button('Show 2D visualization'):
            if(show2D):
                show2D = False
            else:
                show2D = True

        if(show2D):
            st.markdown(
                '''
                2D visualization of cluster
            ''')
                    
            plots.scatter2d(user_experience, x='Total_Avg_TCP', y="Total_Avg_RTT", c='Cluster', s='Total_Avg_Bearer_TP') 

        show3D = False
        if st.button('Show 3D visualization'):
            if(show3D):
                show3D = False
            else:
                show3D = True
        if(show3D):
            st.markdown(
                '''
                3D visualization of cluster
            ''')

            plots.scatter3D(user_engagement, 'Total_Avg_TCP', "Total_Avg_RTT", 'Total_Avg_Bearer_TP', 'Cluster', interactive=True)

        st.warning(
            'Remember the cluster with the worst experience. we need that for satisfaction analysis')
        st.markdown(
        '''
            Save the model for satisfaction analysis
        ''')
        if st.button('Save CSV'):
            helper.save_csv(user_experience,
                            '../data/user_experiance.csv', index=True)

            with open("../models/user_experiance.pkl", "wb") as f:
                pickle.dump(kmeans, f)