from os import sep
from time import sleep
import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image

st.title("H1B data visualization")
@st.cache  # add caching so we load the data only once

# ===================================== PART 0 =====================================
# Read data

def load_data(url, encode = 'utf-8'):
    return pd.read_csv(url, encoding = encode, index_col=0)

url_application = 'https://raw.githubusercontent.com/CMU-IDS-2022/final-project-ketchup-wants-h1b/main/Data/h1b_application_for_ml.csv'
url_employer = 'https://raw.githubusercontent.com/CMU-IDS-2022/final-project-ketchup-wants-h1b/main/Data/h1b_employers.csv'

application_df = load_data(url_application)
employer_df = load_data(url_employer)
