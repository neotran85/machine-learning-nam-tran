
import streamlit as st
from deepface import DeepFace
from PIL import Image   
import numpy as np

img_file_buffer = st.camera_input("Take a snapshot")

if img_file_buffer is not None:
    # Convert the buffer to a PIL Image
    image = Image.open(img_file_buffer)
    # Convert to NumPy array
    img_array = np.array(image)

    try:
        # Analyze the image for emotions
        # The analyze function will automatically find the face, no need for face detection
        analysis = DeepFace.analyze(img_array, actions=['emotion'])
        st.write(analysis)
    except Exception as e:
        st.error(f"Error in processing the image: {e}")