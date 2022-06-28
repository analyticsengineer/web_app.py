from PIL import Image
import streamlit as st

# setting image
image = Image.open('image.png')


col1, col2 = st.columns(2)

col1.header("Simple Data Visualization Web App")
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
