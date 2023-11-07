import streamlit as st
from ultralytics import YOLO
import tempfile
from PIL import Image, ImageDraw
import io

st.title("AI-powered Pose Detector")
with st.spinner("Loading the AI model..."):
    model = YOLO("yolov8x-pose-p6.pt")

# Upload form
uploaded_file = st.file_uploader("Please upload an image with people in it...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    image = Image.open(io.BytesIO(bytes_data))

    with st.spinner("Analyzing the image..."):
        # Perform inference
        results = model(image)
        # Show the results
        for r in results:
            im_array = r.plot()  # plot a BGR numpy array of predictions
            im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
        st.image(im)
