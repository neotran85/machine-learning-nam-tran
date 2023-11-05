import streamlit as st
import tensorflow as tf
from PIL import Image
import numpy as np
import io

# Load your pre-trained model (this is just a placeholder path)
MODEL_PATH = 'nsfw_mobilenet2.224x224.h5'
model = tf.keras.models.load_model(MODEL_PATH)

# Define the image size that your model expects
IMG_SIZE = (224, 224) # for example

# NSFW check function
def check_image_for_nsfw(image_data):
    # Prepare the image for the model
    image = Image.open(io.BytesIO(image_data))
    image = image.resize(IMG_SIZE)
    image_array = np.array(image) / 255.0  # Normalize to [0, 1] if that's what your model expects

    # Your model makes a prediction here
    prediction = model.predict(np.array([image_array]))[0]

    # Assuming your model outputs a single probability for NSFW content
    is_nsfw = prediction[0] > 0.5  # This threshold might be different for your model
    return is_nsfw

# Streamlit app interface
st.title("NSFW Content Checker")

uploaded_file = st.file_uploader("Upload an image file", type=['jpg', 'png', 'jpeg'])

if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.read()
    
    # Display the uploaded image
    st.image(bytes_data, caption='Uploaded Image', use_column_width=True)
    
    # Check the image for NSFW content immediately after uploading
    if check_image_for_nsfw(bytes_data):
        st.error("NSFW content detected!")
    else:
        st.success("No NSFW content detected.")
else:
    st.write("No image uploaded yet. Please upload an image to check.")
