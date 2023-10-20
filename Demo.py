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
import requests
from io import BytesIO
import requests
import json
import base64
import os

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
def get_image_base64_encoding(image_path: str) -> str:
    with open(image_path, 'rb') as file:
        image_data = file.read()
        image_extension = os.path.splitext(image_path)[1]
        base64_encoded = base64.b64encode(image_data).decode('utf-8')
    return f"data:image/{image_extension[1:]};base64,{base64_encoded}"
# Create a client
client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
def asticaAPI(endpoint, payload, timeout):
    response = requests.post(endpoint, data=json.dumps(payload), timeout=timeout, headers={ 'Content-Type': 'application/json', })
    if response.status_code == 200:
        return response.json()
    else:
        return {'status': 'error', 'error': 'Failed to connect to the API.'}
# Set up the Streamlit app
uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
if uploaded_image:
    if st.button("Describe the uploaded image"):
        # Read the uploaded image as bytes
        image_bytes = uploaded_image.read()

        # Encode the image as base64
        asticaAPI_input = base64.b64encode(image_bytes).decode('utf-8')

        # Display the loader
        with st.spinner('Analyzing...'):
            # API configurations
            asticaAPI_key = '66B65C6D-CC58-4E17-89B6-36808A6082EAF4CAA167-1D86-4FEF-8B3C-C946E3B7D61E'  # visit https://astica.ai
            asticaAPI_timeout = 100  # in seconds. "gpt" or "gpt_detailed" require increased timeouts
            asticaAPI_endpoint = 'https://vision.astica.ai/describe'
            asticaAPI_modelVersion = '2.0_full'  # '1.0_full', '2.0_full', or '2.1_full'

            # vision parameters:  https://astica.ai/vision/documentation/#parameters
            asticaAPI_visionParams = 'gpt_detailed,describe_all'  # comma separated, defaults to "all".
            asticaAPI_gpt_prompt = 'In Vietnamese, describe the images about layout, positions, colors, impression, as a professional designer.'
            asticaAPI_prompt_length = '1000'  # number of words in GPT response
            # Define payload dictionary
            asticaAPI_payload = {
                'tkn': asticaAPI_key,
                'modelVersion': asticaAPI_modelVersion,
                'visionParams': asticaAPI_visionParams,
                'gpt_prompt': asticaAPI_gpt_prompt,
                'input': asticaAPI_input,
            }

            # call API function and store result
            asticaAPI_result = asticaAPI(asticaAPI_endpoint, asticaAPI_payload, asticaAPI_timeout)

        # Remove the loader
        st.spinner(None)

        # print API output
        if 'caption_GPTS' in asticaAPI_result:
            st.markdown('Description: ' + asticaAPI_result['caption_GPTS'])
        else:
            st.markdown('No description available.')
        st.image(uploaded_image, use_column_width=True)
