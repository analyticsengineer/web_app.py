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


# setting image
image = Image.open('image1.png')

# setting header 
col1, col2 = st.columns(2)

col1.header("Simple Data Analysis Web App")
title_1 =  '<p style="font-family:sans-serif; color:Grey;">Visualize the TOP TEN Insights fom your dataset</p>'
col1.markdown(title_1, unsafe_allow_html=True)
col2.image(image)

# Setting menu visibility
st.markdown(""" <style>
#Mainmenu {visibility: hidden;}footer {visibility: hidden;}
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

try:
  cols = st.selectbox('SELECT VALUE:',
                       options=df_file.select_dtypes(include=['int', 'float', 'datetime'], exclude='object').columns)
  cols2 = st.multiselect('SELECT LABEL:',
                        options=df_file.select_dtypes(include='object', exclude=['int', 'float']).columns)
  df_file = df_file.groupby(df_file[cols2])[cols].sum().nlargest(n=10).reset_index()
except:
  pass

option3_header = '<p style="font-family: Quicksand_medium; color:#ffffff; font-size: 20px;">Choose Your Graph</p>'
st.markdown(option3_header, unsafe_allow_html=True)

tab1, tab2 = st.tabs(["Color", "No Color"])
with tab1:
        plotType_color = st.selectbox("Plot Type:", ['Choose', 'Line', 'Bar', 'Pie'])
        if plotType_color == 'Line':
            fig = px.line(df_file, x=df_file[cols2], y=df_file[cols])
            st.plotly_chart(fig, use_container_width=True)
        if plotType_color == 'Pie':
            fig = px.pie(names=df_file[cols2], values=df_file[cols])
            st.plotly_chart(fig, use_container_width=True)
        if plotType_color == 'Bar':
            fig = px.bar(df_file, x=df_file[cols2], y=df_file[cols], color=df_file[cols2])
            st.plotly_chart(fig, use_container_width=True)
            
with tab2:
        plotType_color = st.selectbox("Plot Type:", ['Choose', 'Line', 'Bar', 'Pie'])
        if plotType_color == 'Line':
            fig = px.line(df_file, x=df_file[cols2], y=df_file[cols])
            st.plotly_chart(fig, use_container_width=True)
        if plotType_color == 'Pie':
            fig = px.pie(names=df_file[cols2], values=df_file[cols])
            st.plotly_chart(fig, use_container_width=True)
        if plotType_color == 'Bar':
            fig = px.bar(df_file, x=df_file[cols2], y=df_file[cols])
            st.plotly_chart(fig, use_container_width=True)
