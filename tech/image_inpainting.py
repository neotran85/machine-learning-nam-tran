import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np
import consts
import tempfile
import io
from PIL import Image
import base64
import requests
import random

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

def image_to_base64(image):
    # Resize the image
    # Convert the resized image to a byte array
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')  # or 'JPEG' depending on your image
    img_byte_arr = img_byte_arr.getvalue()
    return base64.b64encode(img_byte_arr).decode('utf-8')

def save_canvas_as_base64(image_data):
    # Convert the image data to a PIL Image object
    image = Image.fromarray(image_data.astype('uint8'), 'RGBA')

    # Create a black background image with the same size as the canvas image
    black_bg = Image.new('RGB', image.size, 'black')
    
    # Paste the image onto the black background
    black_bg.paste(image, (0, 0), image)
    return image_to_base64(black_bg)

# Function to convert image bytes to base64
def get_image_base64(image_bytes):
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')  # You can change to 'JPEG' if needed
    img_byte_arr = img_byte_arr.getvalue()
    return base64.b64encode(img_byte_arr).decode('utf-8')

# Define the inpainting function using Stability SDK
def inpaint_with_getimg_ai(prompt, upload_file, mask_file, new_width, new_height):
    random_seed = random.randint(0, 2**10 - 1)  # for a 32-bit signed integer
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
        return image_base64
    else:
        st.error("Failed to get a successful response.")
        st.write(response.text)
    return None

def correct_base64_padding(base64_string):
    # Correct the padding of the Base64 string if necessary
    padding = len(base64_string) % 4
    return base64_string + "=" * (4 - padding) if padding else base64_string

# Save the Base64 string as an image file to tempfile
def save_base64_image(base64_string):
    # Ensure the Base64 string is correctly padded
    base64_string = correct_base64_padding(base64_string)
    # Decode the Base64 string to get the binary data
    try:
        image_data = base64.b64decode(base64_string)
    except Exception as e:
        raise ValueError(f"Error decoding Base64 string: {e}")

    # Open a file in binary write mode and write the image data
    filename = tempfile.NamedTemporaryFile(delete=True, suffix=".png").name
    with open(filename, 'wb') as file:
        file.write(image_data)
    return filename

def display_image_from_base64(base64_string):
    # Convert the Base64 string to bytes
    image_data = base64.b64decode(base64_string)

    # Create a BytesIO stream from the image data
    image_stream = io.BytesIO(image_data)

    # Open the image
    image = Image.open(image_stream)

    # Display the image using Streamlit
    st.image(image, use_column_width=True)

# Set up the streamlit app
st.title("Image Inpainting")

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])
if uploaded_file is not None:
    # Open the image using PIL
    image = Image.open(uploaded_file)

    # Get original dimensions
    original_width, original_height = image.size

    # Calculate new dimensions
    new_width, new_height = calculate_new_dimensions(original_width, original_height)
    
    # Resize the image
    resized_image = image.resize((new_width, new_height))
    img_array = np.array(resized_image)
    
    # get Base64 string of Resized image
    upload_file_base64_string = get_image_base64(resized_image)

    st.write("Draw on the image to create a mask: Click and drag your mouse across the image to create an area for inpainting. If you make a mistake, simply use the undo/redo button below the image.")
    # Set up canvas properties
    stroke_width = st.slider("Stroke width: ", 1, 100, 20)
    # stroke_color is white at beginning
    stroke_color = "#ffffff"
    #bg_color is black at beginning
    bg_color = "#000000"
    # Create a canvas component
    canvas_result = st_canvas(
        fill_color="rgba(255, 255, 255, 1)",  # Fixed fill color with some opacity
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=bg_color,
        background_image=resized_image,
        update_streamlit=True,
        height=img_array.shape[0],
        width=img_array.shape[1],
        drawing_mode="freedraw",
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
                canvas_base64_string = save_canvas_as_base64(canvas_result.image_data)
                result = inpaint_with_getimg_ai(prompt, upload_file_base64_string, canvas_base64_string, new_width, new_height)

                if result:
                    display_image_from_base64(result)
                else:
                    st.error("Failed to get a result.")

        
