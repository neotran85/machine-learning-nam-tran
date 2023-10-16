import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
import streamlit as st
import base64
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import streamlit as st
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
import dateutil.parser
import re
import sweetviz as sv
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from PIL import Image, ImageDraw, ImageFont


le_gender = LabelEncoder()
le_item = LabelEncoder()

# CSS to style the sidebar
style = """
    <style>
        .sidebar .sidebar-content {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        #avatar {
            border-radius: 50%;
            margin-top: 10px;
            margin-bottom: 10px;
            width: 100px;
        }
        #name {
            font-weight: bold;
            font-size: 20px;
            color: #4A90E2;
        }
    </style>
"""
# Function to convert image to base64
def get_image_base64(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

avatar_base64 = get_image_base64("avatar.png")

# Applying the CSS style
st.markdown(style, unsafe_allow_html=True)

# Displaying avatar and name on the sidebar with styling
st.sidebar.markdown(f'<img id="avatar" src="data:image/png;base64,{avatar_base64}" />', unsafe_allow_html=True)
st.sidebar.markdown('<p id="name">Nam Tran</p>', unsafe_allow_html=True)
st.sidebar.markdown("""I am a passionate individual with a keen interest in the realm of machine learning. Driven by curiosity and a deep-seated desire to unravel the complexities of data, I continually seek to harness the power of algorithms to extract meaningful insights and solve real-world problems. Whether it's building predictive models or delving into the intricacies of neural networks, my enthusiasm for the field is palpable. Always eager to learn and evolve, I believe that machine learning holds the key to the future, and is fervently working towards making a significant impact in this dynamic domain.""", unsafe_allow_html=True)

# Your social media links
linkedin_link = "https://www.linkedin.com/in/nam-tran-bb765220b"
telegram_link = "https://t.me/namtrantelegram"

telegram_base64 = get_image_base64("telegram.png")
linkedId_base64 = get_image_base64("linkedin.png")

st.sidebar.markdown(
    f'''
    <a href="{telegram_link}" target="_blank">
        <img id="telegram_avatar" src="data:image/png;base64,{telegram_base64}" style="width:50px; height:50px; display:inline; margin-right:10px;"/>
    </a>
    <a href="{linkedin_link}" target="_blank">
        <img id="linkedin_avatar" src="data:image/png;base64,{linkedId_base64}" style="width:50px; height:50px; display:inline;"/>
    </a>
    ''', 
    unsafe_allow_html=True
)
def showHeatMap(data):
    missing_data = data.isnull()
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(missing_data, cbar=False, cmap="viridis_r", ax=ax)
    ax.set_title("Missing Data Heatmap (Yellow for missing values)")
    st.pyplot(fig)

# Show boxplot of all columns of data frame function
def showBoxPlots(data):
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.boxplot(data=data, ax=ax)
    ax.set_title("Boxplot of all columns")
    st.pyplot(fig)
  
# DEMO
st.title("AI Image Labeling")

import io
from google.cloud import vision
from google.oauth2 import service_account

# Define the path to your service account JSON key file
# Upload image file
# Replace with your Azure Computer Vision API credentials
subscription_key = '778c7e6500f547cc9e57c09018ad06eb'
endpoint = 'https://testdemo2.cognitiveservices.azure.com/'
# Create a client
client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

# Set up the Streamlit app
uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_image:
    if st.button("Label Image"):
        # Convert the bytes object to a file-like object
        image_stream = io.BytesIO(uploaded_image.read())

        # Analyze the image and get object tags
        results = client.analyze_image_in_stream(image_stream, visual_features=[VisualFeatureTypes.objects])

        # Get the object tags
        object_tags = results.objects

        # Create a PIL Image object from the uploaded image
        image = Image.open(image_stream)

        # Load the "arial.ttf" font for text drawing
        font_size = 50  # Adjust the font size as needed
        font = ImageFont.truetype("arial.ttf", font_size)

        # Draw the bounding box for each object and label with the specified font
        draw = ImageDraw.Draw(image)
        for obj in object_tags:
            bounding_box = obj.rectangle
            draw.rectangle([bounding_box.x, bounding_box.y, bounding_box.x + bounding_box.w, bounding_box.y + bounding_box.h], outline='red')
            draw.text((bounding_box.x, bounding_box.y), obj.object_property, fill='black', font=font)

        # Display the image with the bounding boxes and labels overlaid
        st.image(image, use_column_width=True)