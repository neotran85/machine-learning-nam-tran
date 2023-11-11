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

# Function to convert image to base64
def image_to_base64(image, width, height):
    new_width, new_height = calculate_new_dimensions(width, height)
    # Resize the image
    resized_image = image.resize((new_width, new_height))
    # Convert the resized image to a byte array
    img_byte_arr = io.BytesIO()
    resized_image.save(img_byte_arr, format='PNG')  # or 'JPEG' depending on your image
    img_byte_arr = img_byte_arr.getvalue()
    return base64.b64encode(img_byte_arr).decode('utf-8'), new_width, new_height

# Define the inpainting function using Stability SDK
def face_fix(base64_image):
    # Generate a random seed
    random_seed = random.randint(0, 2**10 - 1) 
    url = "https://api.getimg.ai/v1/enhancements/face-fix"
    payload = {
        "image": base64_image,
        "model": "gfpgan-v1-3",
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
# Function to convert image bytes to base64
def get_image_base64(image_bytes):
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')  # You can change to 'JPEG' if needed
    img_byte_arr = img_byte_arr.getvalue()
    return base64.b64encode(img_byte_arr).decode('utf-8')


st.title("Ai-powered Face Fixer")

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the original image
    image = Image.open(uploaded_file).convert("RGB")
    # Get original dimensions
    original_width, original_height = image.size

    # Calculate new dimensions
    new_width, new_height = calculate_new_dimensions(original_width, original_height)
    st.write(f"New dimensions: {new_width} x {new_height}")
    # Resize the image
    resized_image = image.resize((new_width, new_height))
    # Write size of resized image
    st.write(f"Resized image: {resized_image.size}")
    
    base64_string = get_image_base64(resized_image)

    with st.spinner("Enhancing faces..."):
        result = face_fix(base64_string)
        if result:
            st.image(result, caption="Result", use_column_width=True)
        else:
            st.error("Failed to get a result.")