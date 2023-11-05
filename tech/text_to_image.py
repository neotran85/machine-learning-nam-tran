import streamlit as st
import requests
import os
import base64
import consts

# Set up your API key and endpoint
engine_id = "stable-diffusion-xl-1024-v1-0"
api_host = os.getenv('API_HOST', 'https://api.stability.ai')
api_key = consts.API_KEY_STABILITY_AI

if api_key is None:
    raise Exception("Missing Stability API key.")

# Streamlit web app interface
st.title('AI Image Generator')

prompt = st.text_input('Enter a prompt for the AI to generate an image:', 'A far future world where humans have colonized the colorful galaxy.')
generate_button = st.button('Generate Image')

if generate_button:
    with st.spinner('Please wait... Generating image.'):
        response = requests.post(
            f"{api_host}/v1/generation/{engine_id}/text-to-image",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": f"Bearer {api_key}"
            },
            json={
                "text_prompts": [
                    {
                        "text": prompt
                    }
                ],
                "cfg_scale": 7,
                "height": 1024,
                "width": 1024,
                "samples": 1,
                "steps": 30,
            },
        )

        if response.status_code == 200:
            data = response.json()
            for i, image in enumerate(data["artifacts"]):
                # Decode the base64 string into binary data
                image_data = base64.b64decode(image["base64"])
                
                # Display the image in the Streamlit app
                st.image(image_data, caption=f'Generated Image {i+1}', use_column_width=True)
        else:
            st.error("Error with image generation request: " + str(response.text))
