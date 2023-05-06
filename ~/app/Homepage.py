from PIL import Image
import streamlit as st

# setting image
image = Image.open('image.png')


col1, col2 = st.columns(2)

col1.header("Simple Data Visualization Web App")
col1.write("Data visualization is the process of transforming data into visual representations that make it easier to understand. By using charts, graphs, and other visuals, you can communicate your data in a way that is clear, concise, and engaging.")
col1.write("Our simple data visualization app makes it easy to create beautiful and informative data visualizations.")

title_1 =  '<p style="font-family:sans-serif; color:Grey;">This Web App helps you visualize your data,</p>'
col1.markdown(title_1, unsafe_allow_html=True)
title_2 =  '<p style="font-family:sans-serif; color:Grey;">in a simple and elegant way.</p>'
col1.markdown(title_2, unsafe_allow_html=True)
col2.image(image)

# Setting menu visibility
st.markdown(""" <style>
#Mainmenu {visibility: hidden;}
footer {visibility: hidden;}
</style>""", unsafe_allow_html=True)
