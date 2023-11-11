# app.py
import streamlit as st
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
import io
import consts

import streamlit as st
from PIL import Image, ImageDraw
import base64   
import random
import consts
import requests
import io

# Resize the image to the nearest multiple of 64
def resize_to_multiple_of_64(width, height):
    # Calculate the new dimensions, rounding down to the nearest multiple of 64
    new_width = int((width // 64) * 64)
    new_height = int((height // 64) * 64)
    return new_width, new_height

# Calculate new dimensions while maintaining aspect ratio
def calculate_new_dimensions(width, height, max_dimension=1024):
    ratio = width / height
    if width > height:
        temp_width = max_dimension
        temp_height = temp_width / ratio
    else:
        temp_height = max_dimension
        temp_width = temp_height * ratio
    return resize_to_multiple_of_64(temp_width, temp_height)

# Function to convert image bytes to base64
def get_image_base64(image_bytes):
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')  # You can change to 'JPEG' if needed
    img_byte_arr = img_byte_arr.getvalue()
    return base64.b64encode(img_byte_arr).decode('utf-8')

# Define the inpainting function using Stability SDK
def upscale(base64_image, scale_factor):
    # Generate a random seed
    random_seed = random.randint(0, 2**10 - 1) 
    url = "https://api.getimg.ai/v1/enhancements/upscale"
    payload = {
        "image": base64_image,
        "model": "real-esrgan-4x",
        "scale": scale_factor
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {consts.API_KEY_GETIMG_AI}"
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        response_json = response.json()
        image_base64 = response_json.get('image')  # Assuming the key is 'image'
        if image_base64:
            # Create the full data URI scheme string
            data_url = f"data:image/png;base64,{image_base64}"
            return data_url
        else:
            st.error("No image in response.")
    else:
        st.error("Failed to get a successful response.")
        st.write(response.text)
    return None

st.title('AI-powered Image Upscaler')

# File uploader
uploaded_file = st.file_uploader("Please choose an image to 4x upscale :", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Display the original image
    image = Image.open(uploaded_file).convert("RGB")
    # Get original dimensions
    original_width, original_height = image.size

    # Calculate new dimensions
    new_width, new_height = calculate_new_dimensions(original_width, original_height)
    # Resize the image
    resized_image = image.resize((new_width, new_height))
    # Write size of resized image

    base64_string = get_image_base64(resized_image)
    upscale_multiplier = 4
    with st.spinner("Upscaling image..."):
        result = upscale(base64_string, upscale_multiplier)
        if result:
            st.image(result, caption="Result", use_column_width=True)
        else:
            st.error("Failed to get a result.")

