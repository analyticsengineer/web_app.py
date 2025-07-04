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


# App Header
col1, col2 = st.columns(2)
try:
    image = Image.open("image2.png")
    col2.image(image)
except:
    col2.warning("Image not found.")

col1.header("📊 Simple Data Analysis Web App")
col1.markdown(
    '<p style="font-family:sans-serif; color:Grey;">Visualize the BOTTOM TEN insights from your dataset</p>',
    unsafe_allow_html=True
)

# Hide Streamlit footer and menu
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# Upload file
uploaded_file = st.file_uploader("Upload your file", type=['csv', 'xlsx', 'pickle'])

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
            st.dataframe(df_file)
        else:
            st.error("Unsupported file format.")
    except Exception as e:
        st.error(f"Error reading file: {e}")
else:
    st.info("Please upload a CSV, Excel, or Pickle file to continue.")

# Visualization logic
if df_file is not None:
    try:
        numeric_cols = df_file.select_dtypes(include=['int', 'float']).columns.tolist()
        category_cols = df_file.select_dtypes(include='object').columns.tolist()

        if numeric_cols and category_cols:
            cols3 = st.selectbox('Select Value Column (Numeric):', options=numeric_cols)
            cols4 = st.selectbox('Select Label Column (Category):', options=category_cols)

            df_vis = df_file.groupby(cols4)[cols3].sum().nsmallest(10).reset_index()

            st.markdown('<p style="font-family: Quicksand_medium; color:#ffffff; font-size: 20px;">Choose Your Graph</p>',
                        unsafe_allow_html=True)

            color_choice = st.radio("Pick one", ['Color', 'No Color'])

            if color_choice == 'Color':
                plot_type = st.selectbox("Plot Type:", ['Choose', 'Line', 'Bar', 'Pie'])
                if plot_type == 'Line':
                    st.plotly_chart(px.line(df_vis, x=cols4, y=cols3), use_container_width=True)
                elif plot_type == 'Bar':
                    st.plotly_chart(px.bar(df_vis, x=cols4, y=cols3, color=cols4), use_container_width=True)
                elif plot_type == 'Pie':
                    st.plotly_chart(px.pie(df_vis, names=cols4, values=cols3), use_container_width=True)

            elif color_choice == 'No Color':
                plot_type = st.selectbox("Plot Type:", ['Choose', 'Line', 'Bar', 'Pie'])
                if plot_type == 'Line':
                    st.plotly_chart(px.line(df_vis, x=cols4, y=cols3), use_container_width=True)
                elif plot_type == 'Bar':
                    st.plotly_chart(px.bar(df_vis, x=cols4, y=cols3), use_container_width=True)
                elif plot_type == 'Pie':
                    st.plotly_chart(px.pie(df_vis, names=cols4, values=cols3), use_container_width=True)
        else:
            st.warning("Your dataset must contain both numeric and categorical columns.")
    except Exception as e:
        st.error(f"Error generating plot: {e}")
