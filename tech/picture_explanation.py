import streamlit as st 
import base64
import requests
import json
import os
from google.cloud import vision
from google.oauth2 import service_account
import consts

st.title("AI Image Explanation")
def get_image_base64_encoding(image_path: str) -> str:
    with open(image_path, 'rb') as file:
        image_data = file.read()
        image_extension = os.path.splitext(image_path)[1]
        base64_encoded = base64.b64encode(image_data).decode('utf-8')
    return f"data:image/{image_extension[1:]};base64,{base64_encoded}"
# Create a client
def asticaAPI(endpoint, payload, timeout):
    response = requests.post(endpoint, data=json.dumps(payload), timeout=timeout, headers={ 'Content-Type': 'application/json', })
    if response.status_code == 200:
        return response.json()
    else:
        return {'status': 'error', 'error': 'Failed to connect to the API.'}
# Set up the Streamlit app
uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
if uploaded_image:
    # Read the uploaded image as bytes
    image_bytes = uploaded_image.read()
    asticaAPI_input = base64.b64encode(image_bytes).decode('utf-8')
    # Display the loader
    with st.spinner('Analyzing the image...'):
        # API configurations
        asticaAPI_key = consts.API_KEY_ASTICA
        asticaAPI_timeout = 100
        asticaAPI_endpoint = 'https://vision.astica.ai/describe'
        asticaAPI_modelVersion = '2.1_full'  # '1.0_full', '2.0_full', or '2.1_full'

        asticaAPI_visionParams = 'gpt_detailed,describe_all,text_read,faces,objects,color,tags'  # comma separated, defaults to "all".
        asticaAPI_gpt_prompt = 'Describe about its deep meaning, messages, context, lessons, objects, predictions and main characters in detail.'
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
    # print API output
    if 'caption_GPTS' in asticaAPI_result:
        st.markdown('Explanation: ' + asticaAPI_result['caption_GPTS'])
    else:
        st.markdown('The picture cannot be explained.')
    
    st.image(uploaded_image)