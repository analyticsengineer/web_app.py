from PIL import Image
import streamlit as st
import pandas as pd
from pandas_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
from openpyxl import load_workbook

# setting image
image = Image.open('image4.png')

# setting header 
col1, col2 = st.columns(2)

col1.header("Simple Data Analysis Web App")
title_1 =  '<p style="font-family:sans-serif; color:Grey;">View Your Data Summary</p>'
col1.markdown(title_1, unsafe_allow_html=True)
col2.image(image)

# Setting menu visibility
st.markdown(""" <style>
#Mainmenu {visibility: hidden;}
footer {visibility: hidden;}
</style>""", unsafe_allow_html=True)

# uploading file 
df_file = st.file_uploader("Upload your file: ", type=['csv', 'xlsx', 'pickle'])

# Open Csv File
try:
  df_file = pd.read_csv(df_file)
  st.markdown("Your Data Record: ")
  st.dataframe(df_file)
        
except:
  csv = '<p style="font-family: Quicksand_medium; color:#c28080; font-size: 20px;">Please Load A CSV, EXCEL Or ' \
           'PICKLE File To Begin</p>'
  st.markdown(csv, unsafe_allow_html=True)

# Open Excel File
try:
  df_file = pd.read_excel(df_file, engine='openpyxl')
  st.markdown("Your Data Record: ")
  st.dataframe(df_file)     
except:
  pass

# Read Pickle File
try:
  df_file = pd.read_pickle(df_file)
  st.markdown("Your Data Record: ")
  AgGrid(df_file, editable=True)
except:
  pass

data_summary = st.button("Data Summary")
if data_summary:
  st_profile_report(df_file)
