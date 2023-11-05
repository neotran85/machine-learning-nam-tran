import streamlit as st
import requests
import base64
from PIL import Image
import io
import json

st.title("NSFW Image Check")

# Assuming the API key and URL are already set correctly.
api_key = "m3jRLKB54RHAcA4JsEKjaGGi4VGDdKQC8Si3cRFyzpzV4Cv4DAvxl8RJF58l"  # Replace with your actual API key
api_url = "https://stablediffusionapi.com/api/v3/nsfw_image_check"

# This function encodes the uploaded file into a base64 string.
def img_to_base64(uploaded_file):
    img = Image.open(uploaded_file)
    buffered = io.BytesIO()
    img_format = 'PNG' if uploaded_file.type == 'image/png' else 'JPEG'
    img.save(buffered, format=img_format)
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

# This function sends the request to the API.
def check_image(base64_str):
    payload = json.dumps({
        "key": api_key,
        "init_image": base64_str  # Send the base64 string instead of the path
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(api_url, headers=headers, data=payload)
    return response.json()

# Streamlit file uploader.
uploaded_file = st.file_uploader("Upload an image for NSFW check", type=["jpg", "jpeg", "png"])

# When a file is uploaded, convert it and send the check request.
if uploaded_file is not None:
    base64_str = img_to_base64(uploaded_file)
    result = check_image(base64_str)
    st.write(result)
    # Handle the response.
    if result.get("has_nsfw_concept", [False])[0]:
        st.error("The image is NSFW.")
    else:
        st.success("The image is safe.")
