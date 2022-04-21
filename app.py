from os import sep
from time import sleep
import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image

st.set_page_config(
     page_title='H1B Data Visualization Application',
     layout="wide",
     initial_sidebar_state="expanded",
     page_icon="🌐"
)

st.title("H1B data visualization")
@st.cache  # add caching so we load the data only once

# ===================================== PART 0 =====================================
# Read data

def load_data(url, encode = 'utf-8'):
    return pd.read_csv(url, encoding = encode, index_col=0)

url_application = 'https://raw.githubusercontent.com/CMU-IDS-2022/final-project-ketchup-wants-h1b/main/Data/h1b_application.csv'
url_employer = 'https://raw.githubusercontent.com/CMU-IDS-2022/final-project-ketchup-wants-h1b/main/Data/h1b_employers.csv'

application = load_data(url_application)
employer = load_data(url_employer)


##Side Bar
st.sidebar.header('Feature Selection:')

major_list = application.FOREIGN_WORKER_INFO_MAJOR.value_counts()[application.FOREIGN_WORKER_INFO_MAJOR.value_counts()>100].index
major_selection = st.sidebar.selectbox(
    'Select or Type in Your Interested Major:',
    major_list,
)

job_list = application.JOB_TITLE.value_counts()[application.JOB_TITLE.value_counts()>100].index
job_selection = st.sidebar.selectbox(
    'Select or Type in Your Interested Job Title:',
    job_list
)

state_list = application.WORKSITE_STATE.unique()
state_selection = st.sidebar.selectbox(
    'Select or Type in Your Interested Worksite State:',
    state_list
)
