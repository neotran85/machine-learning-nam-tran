import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np
import cv2
import consts
import tempfile
import os
import io
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
from torchvision.transforms import GaussianBlur
import base64
import requests
import random

def image_to_base64(image, width, height):
    new_width, new_height = calculate_new_dimensions(width, height)
    # Resize the image
    resized_image = image.resize((new_width, new_height))
    # Convert the resized image to a byte array
    img_byte_arr = io.BytesIO()
    resized_image.save(img_byte_arr, format='PNG')  # or 'JPEG' depending on your image
    img_byte_arr = img_byte_arr.getvalue()
    return base64.b64encode(img_byte_arr).decode('utf-8'), new_width, new_height

def save_canvas_as_base64(image_data, width, height):
    # Convert the image data to a PIL Image object
    image = Image.fromarray(image_data.astype('uint8'), 'RGBA')

    # Create a black background image with the same size as the canvas image
    black_bg = Image.new('RGB', image.size, 'black')
    
    # Paste the image onto the black background
    black_bg.paste(image, (0, 0), image)
    return image_to_base64(black_bg, width, height)

# Function to convert image bytes to base64
def get_image_base64(image_bytes):
    base64_bytes = base64.b64encode(image_bytes)
    base64_string = base64_bytes.decode('utf-8')
    return base64_string

# Initialize the Stability API client
stability_api = client.StabilityInference(
    key=consts.API_KEY_STABILITY_AI,
    verbose=True, # Print debug messages.
    engine="stable-diffusion-xl-1024-v1-0", # Set the engine to use for generation.
)
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

# Define the inpainting function using Stability SDK
def inpaint_with_getimg_ai(prompt, upload_file, mask_file, new_width, new_height, target_dimension=2048):
    # Generate a random seed
    random_seed = random.randint(0, 2**10 - 1)  # for a 32-bit signed integer
     # Calculate new dimensions while maintaining aspect ratio
    url = "https://api.getimg.ai/v1/stable-diffusion/inpaint"
    payload = {
        "image": upload_file,
        "mask_image": mask_file,
        "model": "realistic-vision-v5-1-inpainting",
        "prompt": prompt,
        "negative_prompt": "bad, Disfigured, cartoon, blurry, nude",
        "strength": 0.001,
        "width": new_width,
        "height": new_height,
        "steps": 80,
        "seed": random_seed,
        "output_format": "png"
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

# Set up the streamlit app
st.title("Image Inpainting")

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])
if uploaded_file is not None:
    # To read as bytes
    bytes_data = uploaded_file.getvalue()
    # Get base64 string
    upload_file_base64_string = get_image_base64(bytes_data)
    original_image = Image.open(uploaded_file).convert("RGB")
    img_array = np.array(original_image)

    st.write("Draw on the image to create a mask: Click and drag your mouse across the image to create an area for inpainting. If you make a mistake, simply use the undo/redo button below the image.")

    # Set up canvas properties
    stroke_width = st.slider("Stroke width: ", 1, 100, 20)
    # stroke_color is white at beginning
    stroke_color = "#ffffff"
    #bg_color is black at beginning
    bg_color = "#000000"
    drawing_mode = "freedraw"
    realtime_update = True
    # Create a canvas component
    canvas_result = st_canvas(
        fill_color="rgba(255, 255, 255, 1)",  # Fixed fill color with some opacity
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=bg_color,
        background_image=Image.open(uploaded_file).convert("RGBA"),
        update_streamlit=realtime_update,
        height=img_array.shape[0],
        width=img_array.shape[1],
        drawing_mode=drawing_mode,
        key="canvas",
    )
    prompt = st.text_input('Please enter a prompt about what you would like to inpaint:', 'Make it look like a Christmas style.')

    # When the user is done with the drawing and a save button is clicked
    if st.button('Inpaint the picture'):
        # Check if there is image data from the canvas
        if canvas_result.image_data is not None:
            with st.spinner("Inpainting... Please wait."):
                # Get the width and height of the image
                image = Image.open(uploaded_file)
                width, height = image.size
                canvas_base64_string, new_width, new_height = save_canvas_as_base64(canvas_result.image_data, width, height)
                result = inpaint_with_getimg_ai(prompt, upload_file_base64_string, canvas_base64_string, new_width, new_height)
                if result:
                    st.image(result, caption="Result", use_column_width=True)
                else:
                    st.error("Failed to get a result.")

        
