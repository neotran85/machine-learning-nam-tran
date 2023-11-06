# app.py
import streamlit as st
from PIL import Image
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
import io
import consts

# Initialize the Stability API client
stability_api = client.StabilityInference(
    key=consts.API_KEY_STABILITY_AI,
    upscale_engine="esrgan-v1-x2plus",
    verbose=True,
)

# Streamlit interface
st.title('AI-powered Image Upscaler')

# Upscaling factor selection
upscale_factor = st.radio(
    'Select the upscaling factor:',
    ('2x', '4x'),  # Removed 8x for simplicity as it may not be directly supported
    index=0  # Default to '2x'
)

# File uploader allows user to add their own image
uploaded_file = st.file_uploader("Please choose an image (width and height < 1000px):", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Open the image with PIL and convert to RGB
    img = Image.open(uploaded_file).convert('RGB')

    # Depending on the factor, set the upscaling parameters
    width, height = img.size
    upscale_multiplier = int(upscale_factor.strip('x'))  # Convert '2x' or '4x' to int 2 or 4
    upscaled_width = width * upscale_multiplier
    upscaled_height = height * upscale_multiplier

    # Display the original image smaller by the upscale factor
    display_size = (width // upscale_multiplier, height // upscale_multiplier)
    display_img = img.resize(display_size)
    st.image(display_img, caption='Original Image')

    with st.spinner('Upscaling image...'):
        # Call the upscale method from the Stability SDK
        answers = stability_api.upscale(
            init_image=img,
            width=upscaled_width, 
            # Other parameters can be added if necessary
        )

        # Process the response and display the upscaled image
        for resp in answers:
            for artifact in resp.artifacts:
                if artifact.finish_reason == generation.FILTER:
                    st.error("Your request activated the API's safety filters and could not be processed.")
                elif artifact.type == generation.ARTIFACT_IMAGE:
                    # Convert binary data to PIL Image
                    upscaled_img = Image.open(io.BytesIO(artifact.binary))

                    # Use Streamlit to display the upscaled image
                    st.image(upscaled_img, caption=f'Upscaled Image ({upscale_factor})')

                    # If you also want to allow users to download the upscaled image:
                    buf = io.BytesIO()
                    upscaled_img.save(buf, format='PNG')
                    byte_im = buf.getvalue()
                    st.download_button(
                        label="Download Upscaled Image",
                        data=byte_im,
                        file_name=f"upscaled_image_{upscale_factor}.png",
                        mime="image/png"
                    )
