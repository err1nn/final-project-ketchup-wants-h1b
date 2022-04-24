from os import sep
from time import sleep
import streamlit as st
import seaborn as sns
import pandas as pd
import altair as alt
import joblib
import numpy as np
from vega_datasets import data


st.set_page_config(
     page_title='H-1B Data Visualization Application',
     layout="wide",
     initial_sidebar_state="expanded",
     page_icon="🌐"
)

st.title("Things You May Want to Know about H-1B Data")
#@st.cache  #add caching so we load the data only once

# ===================================== PART 0 =====================================

# Read data

def load_data(url, encode = 'utf-8'):
    return pd.read_csv(url, encoding = encode, index_col=0)

url_application = 'https://raw.githubusercontent.com/CMU-IDS-2022/final-project-ketchup-wants-h1b/main/Data/h1b_application.csv'
url_employer = 'https://raw.githubusercontent.com/CMU-IDS-2022/final-project-ketchup-wants-h1b/main/Data/h1b_employers.csv'
url_column_name = 'https://raw.githubusercontent.com/CMU-IDS-2022/final-project-ketchup-wants-h1b/main/Data/data_columns.csv'
url_ml = 'https://raw.githubusercontent.com/CMU-IDS-2022/final-project-ketchup-wants-h1b/main/Data/data_ml.csv'
url_state = 'https://raw.githubusercontent.com/CMU-IDS-2022/final-project-ketchup-wants-h1b/main/Data/state_abbr_fips.csv'
url_country = 'https://raw.githubusercontent.com/CMU-IDS-2022/final-project-ketchup-wants-h1b/main/Data/country_code.csv'

application = load_data(url_application)
employer = load_data(url_employer)
test = load_data(url_column_name)
ml_data = load_data(url_ml)
state_code = load_data(url_state).reset_index()
country_code = load_data(url_country).reset_index()
rf = joblib.load("rf.pkl")


# ===================================== PART 1: Visualization =====================================

# Side Bar
st.sidebar.header('Feature Selection')
feature_selection = st.sidebar.radio(
    'H-1B Data Application',
    ('Data Visualization Dashboard', 'Approval Probability Prediction Model')
)

major_list = application.FOREIGN_WORKER_INFO_MAJOR.value_counts() \
    [application.FOREIGN_WORKER_INFO_MAJOR.value_counts()>50].index
major_selection = st.sidebar.selectbox(
    'Select or Type in Your Interested Major:',
    major_list,
)

job_list = application.JOB_TITLE.value_counts() \
    [application.JOB_TITLE.value_counts()>50].index
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
    'What feature do you want the chart to be categorized by?',
    ['CASE_STATUS', 'RECEIVED_YEAR', 'DECISION_YEAR']
)

# Visualization Dashboard

if feature_selection == 'Data Visualization Dashboard':
    
    # Chart 1
    st.subheader("Let's find out where the employers offering visa sponsorships are 🔍")
    
    ## Data processing
    states = alt.topo_feature(data.us_10m.url, 'states')

    employer_data = employer[['State', 'Approval', 'Denial', 'Employer']] \
        .groupby('State').agg({'Approval':'sum','Denial':'sum','Employer':lambda x: x.nunique()}) \
        .reset_index()
    employer_data = pd.merge(employer_data, state_code, how='right', \
                             left_on=['State'], right_on=['Abbr'])
    employer_data = employer_data.drop(['State_x', 'Abbr'], axis=1)
    
    ## Chart
    employer_chart = alt.Chart(states).mark_geoshape(
        stroke = 'lightgray'
    ).encode(
        alt.Color("Employer:Q"),
        tooltip = [alt.Tooltip("State_y:N", title="State"),
                   alt.Tooltip("Employer:Q", title='Employers')]
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(employer_data, 'Id', ["Employer"])
    ).properties(
        width=800,
        height=500
    ).project(
        type='albersUsa'
    )
        
    st.write(employer_chart)

    # Chart 2: Top 10 job titles for each major
    st.subheader('Select your major to see the top 10 job titles 👀')
    
    ## Data Processing
    job_data = application[application['FOREIGN_WORKER_INFO_MAJOR']==major_selection] \
        .groupby([categorized_by,'JOB_TITLE']) \
        .count() \
        .sort_values('CASE_NUMBER', ascending=False) \
        .reset_index()
    
    ## Chart
    st.text('There are ' + str(job_data['CASE_NUMBER'].sum()) +' applicants majored in ' + major_selection)

    job_chart = alt.Chart(job_data, 
        title="Top 10 Job in " + major_selection.lower()
    ).mark_bar(
        tooltip = True
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

    # Chart 3
    st.subheader('Select the state you reside in to see the wage distribution 💰')
    
    # Chart 4
    st.subheader("Select your job title to see where other applicants in the same position come from 🌍")
    
    ## Data Processing
    world = alt.topo_feature(data.world_110m.url, "countries")

    country_code['name'] = country_code['name'].str.upper()
    
    application = pd.merge(application, country_code, how='left',
                           left_on='COUNTRY_OF_CITIZENSHIP', right_on='name')
    application = application.drop(['name'],axis=1)
    application['country-code'] = application['country-code'].astype('Int64')
    
    ### Data Cleaning
    applicant_data = application[['CASE_NUMBER', 'COUNTRY_OF_CITIZENSHIP', 'country-code', 'JOB_TITLE']]
    
    applicant_data = applicant_data[applicant_data['JOB_TITLE']=='Software Engineer'] \
        .groupby(['COUNTRY_OF_CITIZENSHIP']) \
        .agg({'CASE_NUMBER' : 'count', 'country-code' : 'first'}) \
        .reset_index()
    
    ## Chart
    background = alt.Chart(world).mark_geoshape(
        fill='lightgray',
        stroke='white'
    ).properties(
        width=800,
        height=500
    ).project('naturalEarth1')

    applicant_layer = alt.Chart(applicant_data).mark_geoshape().encode(
        alt.Color("CASE_NUMBER:Q"),
        tooltip = [alt.Tooltip("COUNTRY_OF_CITIZENSHIP:N", title="Country"),
                   alt.Tooltip("CASE_NUMBER:Q", title='H-1B Applicants')]
    ).transform_lookup(
        lookup='country-code',
        from_=alt.LookupData(world, 'country-code', fields=["type", "properties", "geometry"])
    ).properties(
        width=800,
        height=500
    ).project(
        type='naturalEarth1'
    )
        
    applicant_chart = background + applicant_layer
    
    st.write(applicant_chart)

# ===================================== PART 2: Prediction Model =====================================

# Prediction Model
elif feature_selection == 'Approval Probability Prediction Model':

    st.subheader("Enter your information:")
    ml_employer_list = sorted(ml_data.EMPLOYER_NAME.unique())
    ml_state_list = sorted(ml_data.WORKSITE_STATE.unique())
    ml_job_list = ml_data.JOB_TITLE.unique()
    ml_country_list = ml_data.COUNTRY_OF_CITIZENSHIP.unique()
    ml_education_list = ml_data.FOREIGN_WORKER_EDUCATION.unique()
    ml_major_list = ml_data.FOREIGN_WORKER_INFO_MAJOR.unique()

    employer_selection = st.selectbox(
        'Employer Name', ml_employer_list
    )
    state_selection = st.selectbox(
        'Worksite Location', ml_state_list
    )
    job_selection = st.selectbox(
        'Job Title', ml_job_list
    )
    country_selection = st.selectbox(
        'Country of Citizenship', ml_country_list
    )
    education_selection = st.selectbox(
        'Education Level', ml_education_list
    )
    major_selection = st.selectbox(
        'Major', ml_major_list
    )
    wage = st.number_input("Enter Expected Wage")


    if st.button("Submit"):
    
    # Unpickle classifier
        st.text("Calculating probability.")
    # Store inputs into dataframe
        if 'EMPLOYER_NAME_'+employer_selection in test.columns:
            test['EMPLOYER_NAME_'+employer_selection] = 1
        if 'WORKSITE_STATE_'+state_selection in test.columns:
            test['WORKSITE_STATE_'+state_selection] = 1
        if 'JOB_TITLE_'+job_selection in test.columns:
            test['JOB_TITLE_'+job_selection] = 1
        if 'COUNTRY_OF_CITIZENSHIP_'+country_selection in test.columns:
            test['COUNTRY_OF_CITIZENSHIP_'+country_selection] = 1
        if 'FOREIGN_WORKER_EDUCATION_'+education_selection in test.columns:
            test['FOREIGN_WORKER_EDUCATION_'+education_selection] = 1
        if 'FOREIGN_WORKER_INFO_MAJOR_'+major_selection in test.columns:
            test['FOREIGN_WORKER_INFO_MAJOR_'+major_selection] = 1
        test['WAGE_OFFER_FROM'] = wage
     
    # Get prediction
        test = np.array(test.iloc[0])
        test = test.reshape(1, -1)   
        prediction = rf.predict(test)
        probability = rf.predict_proba(test)[0][1]
    
    # Output prediction
        st.subheader('The probability of certified is ' + str(round(probability,3)*100)+'%.')
    