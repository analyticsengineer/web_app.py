# Necessary Libraries
import time
from PIL import Image
import streamlit as st
import pandas as pd
from datetime import date
from openpyxl import load_workbook
import requests
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
import plotly.express as px
import numpy as np

# Set image
try:
    image = Image.open('image4.png')
except:
    image = None

# Set header
col1, col2 = st.columns(2)

col1.header("Simple Data Analysis Web App")
col1.markdown('<p style="font-family:sans-serif; color:Grey;">View Your Data Summary</p>', unsafe_allow_html=True)

if image:
    col2.image(image)
else:
    col2.warning("Image not found.")

# Hide Streamlit menu
st.markdown(""" 
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# File upload
uploaded_file = st.file_uploader("Upload your file:", type=['csv', 'xlsx', 'pickle'])

df_file = None

if uploaded_file:
    try:
        if uploaded_file.name.endswith('.csv'):
            df_file = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('.xlsx'):
            df_file = pd.read_excel(uploaded_file, engine='openpyxl')
        elif uploaded_file.name.endswith('.pickle'):
            df_file = pd.read_pickle(uploaded_file)

        if df_file is not None:
            st.markdown("### Your Data Record:")
            AgGrid(df_file, editable=True)
        else:
            st.error("Unsupported file format or empty file.")

    except Exception as e:
        st.error(f"Error loading file: {e}")
else:
    st.info("Please upload a CSV, Excel, or Pickle file to continue.")

# Generate and show profile report
if st.button("Data Summary"):
    if df_file is not None:
        try:
            profile = ProfileReport(df_file, title="Data Summary Report", explorative=True)
            st_profile_report(profile)
        except Exception as e:
            st.error(f"Could not generate profile report: {e}")
    else:
        st.warning("Please upload a valid dataset first.")
