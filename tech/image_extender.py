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
def inpaint_with_getimg_ai(prompt, upload_file, mask_file, new_width, new_height, target_dimension=1024):
    # Generate a random seed
    random_seed = random.randint(0, 2**10 - 1)  # for a 32-bit signed integer
     # Calculate new dimensions while maintaining aspect ratio
    url = "https://api.getimg.ai/v1/stable-diffusion/inpaint"
    payload = {
        "image": upload_file,
        "mask_image": mask_file,
        # "model": "realistic-vision-v5-1-inpainting",
        "model": "stable-diffusion-v1-5-inpainting",
        "prompt": prompt,
        "negative_prompt": "bad, Disfigured, cartoon, blurry, nude, frame, picture, painting, drawing, text, boring, same pattern, separated, irrelevant, gallery, album, banners",
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

st.title("Image Extender")

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the original image
    image = Image.open(uploaded_file).convert("RGB")

    # Use slider to adjust the extension size in percentage
    left = st.slider("Left", 0, 100, 0) * image.width // 100
    right = st.slider("Right", 0, 100, 0) * image.width // 100
    top = st.slider("Top", 0, 100, 0) * image.height // 100
    bottom = st.slider("Bottom", 0, 100, 0) * image.height // 100

    # Create a new image with the desired dimensions
    new_width = image.width + left + right
    new_height = image.height + top + bottom

    # Fill with gray color
    new_image = Image.new("RGB", (new_width, new_height), "gray")

    # Paste the original image onto the new background
    new_image.paste(image, (left, top))
    # Resize new_image
    new_image = new_image.resize((new_width, new_height))

    # Display the extended image
    st.image(new_image, caption='Sample Extended Image.', use_column_width=True)
    new_image_base64_string, temp_width, temp_heigh = image_to_base64(new_image, new_width, new_height)

    # Create another new image for the rectangle
    rectangle_image = Image.new("RGB", (new_width, new_height), "white")
    draw = ImageDraw.Draw(rectangle_image)
    draw.rectangle([(left + 20, top + 20), (left + image.width - 20, top + image.height - 20)], fill="black")
    mask_image_base64_string, temp_width, temp_heigh = image_to_base64(rectangle_image, new_width, new_height)

    # Display the rectangle image
    # st.image(rectangle_image, caption='Image with Rectangle.', use_column_width=True)
    # additional_prompt = " In extending the image, please avoid creating any separate, distinct sections that do not seamlessly blend with the existing content. Do not generate isolated elements or images within images, such as gallery pictures, that would disrupt the continuity of the scene. The extension should appear as a natural, uninterrupted continuation of the original image, without any abrupt changes in theme, style, or content."
    additional_prompt = ""
    prompt = st.text_input('Tell us about what you would like the extended area to be:', '')
    if st.button("Extend the image"):
        with st.spinner("Extending the image..."):
            # prompt = prompt + additional_prompt
            result_image_base64_string = inpaint_with_getimg_ai(prompt + additional_prompt, new_image_base64_string, mask_image_base64_string, temp_width, temp_heigh)
            if result_image_base64_string:
                st.image(result_image_base64_string, caption="Result", use_column_width=True)
            else:
                st.error("Failed to get a result.")