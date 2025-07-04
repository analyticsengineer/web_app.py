import streamlit as st
from PIL import Image

# Safely load image
try:
    image = Image.open("image.png")
except FileNotFoundError:
    image = None

# App layout
col1, col2 = st.columns(2)

with col1:
    st.header("📊 Simple Data Visualization Web App")
    st.write("Data visualization is the process of transforming data into visual representations that make it easier to understand. "
             "By using charts, graphs, and other visuals, you can communicate your data in a way that is clear, concise, and engaging.")

    st.write("Our simple data visualization app makes it easy to create beautiful and informative data visualizations.")

    st.markdown(
        """
        <p style="font-family:sans-serif; color:Grey; font-size:16px;">
            This Web App helps you visualize your data,<br>
            in a simple and elegant way.
        </p>
        """, unsafe_allow_html=True
    )

with col2:
    if image:
        st.image(image, use_column_width=True)
    else:
        st.warning("Image not found. Please ensure 'image.png' is in the same directory.")

# Hide Streamlit menu and footer
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True
)
