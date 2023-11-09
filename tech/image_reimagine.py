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


# Initialize the Stability API client
stability_api = client.StabilityInference(
    key=consts.API_KEY_STABILITY_AI,
    verbose=True, # Print debug messages.
    engine="stable-diffusion-xl-1024-v1-0", # Set the engine to use for generation.
)
def resize_to_multiple_of_64(image):
    # Calculate the new dimensions, rounding down to the nearest multiple of 64
    new_width = (image.width // 64) * 64
    new_height = (image.height // 64) * 64
    # Resize the image to the new dimensions
    resized_image = image.resize((new_width, new_height), Image.ADAPTIVE)
    return resized_image

# Define the inpainting function using Stability SDK
def inpaint_with_stability(prompt, init_image_path, mask_image_path):
    init_image = Image.open(init_image_path)
    mask_image = Image.open(mask_image_path)
    # Feathering the edges of our mask generally helps provide a better result. Alternately, you can feather the mask in a suite like Photoshop or GIMP.
    blur = GaussianBlur(11,20)
    masked = blur(mask_image)

    # Generate the image
    answers = stability_api.generate(
        prompt=prompt,
        init_image=init_image,
        mask_image=masked,
        start_schedule=1,
        seed=1, # If attempting to transform an image that was previously generated with our API,
                    # initial images benefit from having their own distinct seed rather than using the seed of the original image generation.
        steps=60, # Amount of inference steps performed on image generation. Defaults to 30.
        cfg_scale=8.0, # Influences how strongly your generation is guided to match your prompt.
                    # Setting this value higher increases the strength in which it tries to match your prompt.
                    # Defaults to 7.0 if not specified.
        width=1024, # Generation width, if not included defaults to 512 or 1024 depending on the engine.
        height=1024, # Generation height, if not included defaults to 512 or 1024 depending on the engine.
        sampler=generation.SAMPLER_K_DPMPP_SDE # Choose which sampler we want to denoise our generation with.
                                                    # Defaults to k_lms if not specified. Clip Guidance only supports ancestral samplers.
                                                    # (Available Samplers: ddim, plms, k_euler, k_euler_ancestral, k_heun, k_dpm_2, k_dpm_2_ancestral, k_dpmpp_2s_ancestral, k_lms, k_dpmpp_2m, k_dpmpp_sde)
    )
    # Iterate over the generated answers and return the image
    for resp in answers:
        for artifact in resp.artifacts:
            if artifact.type == generation.ARTIFACT_IMAGE:
                global img2
                img2 = Image.open(io.BytesIO(artifact.binary))
                img2.save("result.png") 
                return img2
    return None
def save_canvas_as_png(image_data, filename):
    # Convert the image data to a PIL Image object
    image = Image.fromarray(image_data.astype('uint8'), 'RGBA')

    # Create a white background image with the same size as the canvas image
    white_bg = Image.new('RGB', image.size, 'white')
    
    # Paste the image onto the white background
    # Since the mode is 'RGBA', the alpha channel is used to blend the images
    white_bg.paste(image, (0, 0), image)

    # Save the image with white background as a PNG file
    white_bg.save(filename, 'PNG')

# Set up the streamlit app
st.title("Image Masking App")

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])
if uploaded_file is not None:
    original_image = Image.open(uploaded_file).convert("RGB")
    original_image = resize_to_multiple_of_64(original_image)
    img_array = np.array(original_image)
    # Save original image 
    original_image.save("original.png")
    # Set up canvas properties
    stroke_width = st.slider("Stroke width: ", 1, 50, 3)
    stroke_color = st.color_picker("Stroke color: ")
    bg_color = st.color_picker("Background color: ", "#ffffff")
    drawing_mode = st.selectbox(
        "Drawing tool:", ("freedraw", "line", "rect", "circle", "transform")
    )
    realtime_update = st.checkbox("Update in realtime", True)

    # Create a canvas component
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",  # Fixed fill color with some opacity
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
    
    # When the user is done with the drawing and a save button is clicked
    if st.button('Save Canvas'):
        # Check if there is image data from the canvas
        if canvas_result.image_data is not None:
            save_canvas_as_png(canvas_result.image_data, "canvas.png")
            result = inpaint_with_stability("make it nicer and beautiful", "original.png", "canvas.png")
            st.image(result, caption='Result', use_column_width=True)

        
