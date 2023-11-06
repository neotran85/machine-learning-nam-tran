import streamlit as st
import cv2
import tempfile
import torch
import os
import time
import  numpy as np
# Load YOLOv5 model

# delete out files
def delete_out_files(path):
    if os.path.exists(path):
        os.remove(path)

model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

st.title("AI-powered Object Detector")
out_path = ''
uploaded_file = st.file_uploader("Upload a MP4 video (shorter than 30 seconds)...", type=["mp4"])

if uploaded_file is not None:
    timestamp = int(round(time.time() * 1000))
    out_path = f"out_{timestamp}.mp4"
    with st.spinner('Analyzing the video...'):
        tfile = tempfile.NamedTemporaryFile(delete=False) 
        tfile.write(uploaded_file.read())
        # Open the video file
        cap = cv2.VideoCapture(tfile.name)
        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))

        # Use 'mp4v' codec for MP4 format
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(out_path, fourcc, 20, (frame_width, frame_height))
        try:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                # Convert frame to format required by model
                results = model(frame)
                # Draw the results on the frame
                annotated_frame = results.render()[0]
                # Write frame to output video
                out.write(annotated_frame)
            cap.release()
            out.release()
            # Display the video with Streamlit video component
            st.write('Click to play the result video below:')
            st.video(out_path, format='video/mp4', start_time=0)
        except Exception as e:
            st.write(e)
        finally:
            tfile.close()

