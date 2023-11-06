import streamlit as st
from streamlit_image_comparison import image_comparison
from stability_sdk import client
from PIL import Image
import io
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
import consts
import time
import os

# Initialize the Stability AI client
stability_api = client.StabilityInference(
    key=consts.API_KEY_STABILITY_AI,  
    upscale_engine="esrgan-v1-x2plus",  
    verbose=True,
)

# Title for the Streamlit app
st.title('Image Enhancement')

# File uploader allows user to add their own image
uploaded_file = st.file_uploader("Upload an image to enhance", type=["png", "jpg", "jpeg"])
original_image_path, upscaled_image_path = '',''
max_size = 2048
# Check if a file has been uploaded
if uploaded_file is not None:
    # Convert the file to an image
    original_image = Image.open(uploaded_file).convert("RGB")
    
    # Calculate new dimensions while maintaining aspect ratio
    original_width, original_height = original_image.size
    
    # Get the current time in milliseconds
    timestamp = int(round(time.time() * 1000))

    # Save the original image to a temporary path with the timestamp
    original_image_path = f"original_image_{timestamp}.png"

    # Upscale the image using Stability SDK
    with st.spinner('Enhancing image...'):
        if original_width > original_height:
                responses = stability_api.upscale(
                init_image=original_image,
                steps=100,
                width=max_size,
            )
        else:
            responses = stability_api.upscale(
                init_image=original_image,
                steps=100,
                height=max_size, 
            )

        # Retrieve the upscaled image
        upscaled_image = None
        for resp in responses:
            for artifact in resp.artifacts:
                if artifact.type == generation.ARTIFACT_IMAGE:
                    upscaled_image = Image.open(io.BytesIO(artifact.binary))

        if upscaled_image:
            # Save the upscaled image temporarily to disk
            upscaled_image_path = f"upscaled_image_{timestamp}.png"
            upscaled_image.save(upscaled_image_path)
            original_image.save(original_image_path)

            image_comparison(
                img1=original_image_path,
                img2=upscaled_image_path,
                label1='Before',
                label2='After',
            )
        else:
            st.error('Unable to upscale the image.')
    # After displaying the images, delete the temporary files
    if os.path.exists(original_image_path):
        os.remove(original_image_path)
    if os.path.exists(upscaled_image_path):
        os.remove(upscaled_image_path)

