import streamlit as st
from streamlit_image_comparison import image_comparison
from stability_sdk import client
from PIL import Image
import io
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation

# Initialize the Stability AI client
stability_api = client.StabilityInference(
    key='sk-XRJbmWtHE22TCSDCRiT8ZF5Pqt7qrhyxq6vyKkVlQhvq8kdC',  # Replace with your Stability API key
    upscale_engine="esrgan-v1-x2plus",  # Replace with your desired upscale engine
    verbose=True,
)

# Title for the Streamlit app
st.title('Image Enhancement')

# File uploader allows user to add their own image
uploaded_file = st.file_uploader("Upload an image to upscale", type=["png", "jpg", "jpeg"])

# Check if a file has been uploaded
if uploaded_file is not None:
    # Convert the file to an image
    original_image = Image.open(uploaded_file).convert("RGB")
    # Save the original image to a temporary path
    original_image_path = "original_image.png"
    original_image.save(original_image_path)

    # Display the original image
    # st.image(original_image, caption='Original Image', use_column_width=True)

    # Upscale the image using Stability SDK
    with st.spinner('Enhancing image...'):
        responses = stability_api.upscale(
            init_image=original_image,
            steps=200,
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
            upscaled_image_path = 'upscaled_image.png'
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
