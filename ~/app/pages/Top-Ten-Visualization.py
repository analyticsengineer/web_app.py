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

# Load Image
try:
    image = Image.open('image1.png')
except:
    image = None

# Header layout
col1, col2 = st.columns(2)
col1.header("Simple Data Analysis Web App")
col1.markdown(
    '<p style="font-family:sans-serif; color:Grey;">Visualize the TOP TEN Insights from your dataset</p>',
    unsafe_allow_html=True,
)
if image:
    col2.image(image)
else:
    col2.warning("Image not found.")

# Hide menu and footer
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# File upload
uploaded_file = st.file_uploader("Upload your file:", type=["csv", "xlsx", "pickle"])
df_file = None

if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            df_file = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(".xlsx"):
            df_file = pd.read_excel(uploaded_file, engine="openpyxl")
        elif uploaded_file.name.endswith(".pickle"):
            df_file = pd.read_pickle(uploaded_file)

        st.markdown("### Your Data Record:")
        AgGrid(df_file, editable=True)

    except Exception as e:
        st.error(f"Error loading file: {e}")

# Visuals
if df_file is not None:
    try:
        # Select value and label columns
        cols = st.selectbox(
            'SELECT VALUE:',
            options=df_file.select_dtypes(include=['int', 'float', 'datetime']).columns
        )
        cols2 = st.selectbox(
            'SELECT LABEL:',
            options=df_file.select_dtypes(include='object').columns
        )

        # Top 10 summary
        grouped_df = df_file.groupby(cols2)[cols].sum().nlargest(n=10).reset_index()

        st.markdown(
            '<p style="font-family: Quicksand_medium; color:#ffffff; font-size: 20px;">Choose Your Graph</p>',
            unsafe_allow_html=True,
        )

        chart_mode = st.radio("Pick one", ["Color", "No Color"])
        plot_type = st.selectbox("Plot Type:", ["Choose", "Line", "Bar", "Pie"])

        if plot_type != "Choose":
            try:
                if plot_type == "Line":
                    fig = px.line(grouped_df, x=cols2, y=cols)
                elif plot_type == "Pie":
                    fig = px.pie(grouped_df, names=cols2, values=cols)
                elif plot_type == "Bar":
                    if chart_mode == "Color":
                        fig = px.bar(grouped_df, x=cols2, y=cols, color=cols2)
                    else:
                        fig = px.bar(grouped_df, x=cols2, y=cols)

                st.plotly_chart(fig, theme="streamlit", use_container_width=True)

            except Exception as e:
                st.error(f"Chart rendering error: {e}")

    except Exception as e:
        st.warning(f"Analysis issue: {e}")
else:
    st.info("Please upload a dataset to begin.")
