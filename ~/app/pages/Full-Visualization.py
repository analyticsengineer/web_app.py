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

# Load image
try:
    image = Image.open('image3.png')
except:
    image = None

# Header section
col1, col2 = st.columns(2)

col1.header("Simple Data Analysis Web App")
col1.markdown(
    '<p style="font-family:sans-serif; color:Grey;">View FULL VISUALIZATION of your dataset</p>',
    unsafe_allow_html=True,
)

if image:
    col2.image(image)
else:
    col2.warning("Image not found.")

# Hide Streamlit menu and footer
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

# File uploader
uploaded_file = st.file_uploader("Upload your file:", type=["csv", "xlsx", "pickle"])

df_file = None

# Handle file reading
if uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            df_file = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(".xlsx"):
            df_file = pd.read_excel(uploaded_file, engine="openpyxl")
        elif uploaded_file.name.endswith(".pickle"):
            df_file = pd.read_pickle(uploaded_file)
    except Exception as e:
        st.error(f"Error reading file: {e}")

# Display DataFrame
if df_file is not None:
    st.markdown("### Your Data Record:")
    AgGrid(df_file, editable=True)

    try:
        # User selections
        cols5 = st.selectbox(
            "SELECT VALUE:",
            options=df_file.select_dtypes(include=["int", "float", "datetime"]).columns,
        )
        cols6 = st.selectbox(
            "SELECT LABEL:",
            options=df_file.select_dtypes(include="object").columns,
        )

        # Group and summarize
        grouped_df = df_file.groupby(cols6)[cols5].sum().nlargest(10).reset_index()
    except Exception as e:
        st.warning(f"Selection failed: {e}")
        grouped_df = None

    # Graph rendering
    if grouped_df is not None:
        st.markdown(
            '<p style="font-family: Quicksand_medium; color:#ffffff; font-size: 20px;">Choose Your Graph</p>',
            unsafe_allow_html=True,
        )

        graph_style = st.radio("Pick one", ["Color", "No Color"])
        plot_type = st.selectbox("Plot Type:", ["Choose", "Line", "Bar", "Pie"])

        if plot_type != "Choose":
            try:
                if plot_type == "Line":
                    fig = px.line(
                        grouped_df, x=cols6, y=cols5,
                        color=cols6 if graph_style == "Color" else None
                    )
                elif plot_type == "Bar":
                    fig = px.bar(
                        grouped_df, x=cols6, y=cols5,
                        color=cols6 if graph_style == "Color" else None
                    )
                elif plot_type == "Pie":
                    fig = px.pie(
                        grouped_df, names=cols6, values=cols5
                    )

                st.plotly_chart(fig, theme="streamlit", use_container_width=True)

            except Exception as e:
                st.error(f"Error creating chart: {e}")
else:
    st.info("Please upload a dataset to begin.")
