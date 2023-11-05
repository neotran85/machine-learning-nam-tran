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

# Check if a file has been uploaded
if uploaded_file is not None:
    # Convert the file to an image
    original_image = Image.open(uploaded_file).convert("RGB")
    # Get the current time in milliseconds
    timestamp = int(round(time.time() * 1000))

    # Save the original image to a temporary path with the timestamp
    original_image_path = f"original_image_{timestamp}.png"
    original_image.save(original_image_path)

    # Display the original image
    # st.image(original_image, caption='Original Image', use_column_width=True)

    # Upscale the image using Stability SDK
    with st.spinner('Enhancing image...'):
        responses = stability_api.upscale(
            init_image=original_image,
            steps=100,
            width=2048
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
            # Show comparison slider
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
