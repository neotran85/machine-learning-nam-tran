import streamlit as st
from deepface import DeepFace
from PIL import Image
import numpy as np
import cv2

st.title("Emotion Detector")

img_file_buffer = st.camera_input("Take a snapshot and analyze your emotions")

if img_file_buffer is not None:
    # Convert the buffer to a PIL Image
    image = Image.open(img_file_buffer)
    # Convert to NumPy array
    img_array = np.array(image)

    try:
        # Analyze the image for emotions
        analysis = DeepFace.analyze(img_array, actions=['emotion'])
        
        # Get the dominant emotion and the region of the detected face
        dominant_emotion = analysis[0]["dominant_emotion"]
        face_region = analysis[0]["region"]
        x, y, w, h = face_region["x"], face_region["y"], face_region["w"], face_region["h"]
        
        # Draw a rectangle around the face
        cv2.rectangle(img_array, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
        # Put the dominant emotion text above the rectangle
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img_array, dominant_emotion, (x, y-10), font, 0.9, (0, 255, 0), 2, cv2.LINE_AA)

        # Convert back to Image for display in Streamlit
        image_with_detections = Image.fromarray(img_array)

        # Display the image with detections
        st.image(image_with_detections, caption='Processed Image', use_column_width=True)

    except Exception as e:
        st.error(f"Error in processing the image: {e}")
