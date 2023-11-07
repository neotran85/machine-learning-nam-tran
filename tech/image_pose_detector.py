import streamlit as st
from ultralytics import YOLO
import tempfile
from PIL import Image, ImageDraw
import io

st.title("Pose Detection with YOLOv8")

model = YOLO("yolov8x-pose-p6.pt")

# Upload form
uploaded_file = st.file_uploader("Please upload an image or MP4 video (shorter than 30 seconds):", type=["mp4", "jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Process image
    if uploaded_file.type in ["image/jpeg", "image/png"]:
        with st.spinner('Analyzing the image...'):
            bytes_data = uploaded_file.getvalue()
            image = Image.open(io.BytesIO(bytes_data))
            # Perform inference
            results = model(image)
            # Show the results
            for r in results:
                im_array = r.plot()  # plot a BGR numpy array of predictions
                im = Image.fromarray(im_array[..., ::-1])  # RGB PIL image
            st.image(im)
    