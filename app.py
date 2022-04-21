from os import sep
from time import sleep
import streamlit as st
import seaborn as sns
import pandas as pd
import altair as alt
from PIL import Image

st.set_page_config(
     page_title='H1B Data Visualization Application',
     layout="wide",
     initial_sidebar_state="expanded",
     page_icon="🌐"
)

st.title("Can I get my H1B visa?🥺🥺🥺")
@st.cache  # add caching so we load the data only once
#st.text("This application is aiming to ")

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
feature_selection = st.sidebar.radio(
    'Select the funtion you want to use:',
    ('Data Visualization Dashboard', 'Approval Probability Prediction Model')
)

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

categorized_by = st.sidebar.radio(
    'What feature do you want your chart to be categorized by?',
    ['CASE_STATUS', 'RECEIVED_YEAR', 'DECISION_YEAR']
)

# Visualization Dashboard

if feature_selection == 'Data Visualization Dashboard':
    st.header('Many charts here')
    st.subheader('Choropleth map that shows the aggregate summary of total approved and denied H-1B applications from the spatial view')
    
    st.subheader('The top 10 job title for a major that user interested in')
    job_data = application[application['FOREIGN_WORKER_INFO_MAJOR']==major_selection].groupby([categorized_by,'JOB_TITLE']).count().sort_values('CASE_NUMBER', ascending=False).reset_index()
    st.text('There are ' + str(job_data['CASE_NUMBER'].sum()) +' applicants majored in ' + major_selection)
    job_chart = alt.Chart(job_data, 
    title="Top 10 Job in " + major_selection.lower()).mark_bar(tooltip = True
    ).encode(
        x = alt.X('CASE_NUMBER', title='Count'),
        y = alt.Y('JOB_TITLE', sort='-x'),
        color = categorized_by
    ).transform_window(
        rank = 'rank(CASE_NUMBER)',
        sort = [alt.SortField('CASE_NUMBER', order='descending')]
    ).transform_filter(
        (alt.datum.rank<10)
    ).properties(
        width=800
    )
    st.write(job_chart)

    st.subheader('The distribution (Boxplot) of wage of user-selected states')
    st.subheader('Choropleth world map to show that what country did the H1B applicants come from for a user-selected company and job title')


# Prediction Model
elif feature_selection == 'Approval Probability Prediction Model':
    st.header('Model here')
    st.subheader("Predictive model to calculate the probability of getting H1B visa approval based on user's input")
