import user_overview_page
import user_engagement_page
import user_experience_page
import user_satisifaction_page 
import streamlit as st

PAGES = {
    "Data Overview": user_overview_page,
    "User Engagement Analysis":  user_engagement_page,
    "User Experience Analytics": user_experience_page,
    "User Satisfaction Analysis": user_satisifaction_page
}

selection = st.sidebar.radio("Go to page", list(PAGES.keys()))
page = PAGES[selection]
page.app()