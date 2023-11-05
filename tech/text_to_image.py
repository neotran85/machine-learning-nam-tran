import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# Function to send request to Stable Diffusion API
def get_generated_image(api_key, prompt):
    url = "https://stablediffusionapi.com/api/v3/text2img"

    payload = {
        "key": api_key,
        "prompt": prompt,
        "negative_prompt": "",
        "width": "512",
        "height": "512",
        "samples": "1",
        "num_inference_steps": "22",
        "safety_checker": "yes",
        "enhance_prompt": "yes",
        "seed": None,
        "guidance_scale": 7.5,
        "multi_lingual": "no",
        "panorama": "no",
        "self_attention": "no",
        "upscale": "yes",
        "embeddings_model": None,
        "webhook": None,
        "track_id": None
    }

    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()

# Streamlit UI
st.title("AI Image Generator")

# User inputs
api_key = "abj99slmdtaeLhnFwHJzSJDbia5RiB4TFpMSECy9xSU8x4kzNPEGJlS3ayQp"
prompt = st.text_input("Enter a prompt for the image:", value="A cute, happy dog with 2 wings, flying in a blue sky")
# Button to generate image
if st.button("Generate Image"):
    if api_key and prompt:
        with st.spinner("Generating image..."):
            result = get_generated_image(api_key, prompt)
            st.write(result)
            # Check if the request was successful
            if result["status"] == "success":
                # Get the image URL
                image_url = result["output"][0]

                # Display the image
                response = requests.get(image_url)
                img = Image.open(BytesIO(response.content))
                st.image(img, caption="Generated Image", use_column_width=True)
            else:
                st.error("So sorry. Failed to generate image. Please try again.")
    else:
        st.warning("Please enter an API key and a prompt.")
