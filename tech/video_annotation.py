import streamlit as st
import cv2
import tempfile
import torch
import os
# Check if CUDA is available and set the device to GPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# Load YOLOv5 model onto the device
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True).to(device)

st.title("AI-powered Object Detector")

if torch.cuda.is_available():
    st.write("CUDA is available here")
else:
    st.write("CUDA is NOT available here")

uploaded_file = st.file_uploader("Please upload a MP4 video (shorter than 30 seconds):", type=["mp4"])

if uploaded_file is not None:
    with st.spinner('Analyzing the video...'):
        tfile = tempfile.NamedTemporaryFile(delete=False) 
        tfile.write(uploaded_file.read())
        tfile.flush()
        # Open the video file
        cap = cv2.VideoCapture(tfile.name)

        # Delete the original temp file to free up space
        os.unlink(tfile.name)

        # Create a named temporary file for the output
        temp_out_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
        frame_width = int(cap.get(3))
        frame_height = int(cap.get(4))

        # Define the codec and create VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(temp_out_file.name, fourcc, 20.0, (frame_width, frame_height))

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

            # Get the path of the temporary output file
            temp_out_file_path = temp_out_file.name
            # Read the video file in binary mode
            with open(temp_out_file_path, 'rb') as f:
                video_bytes = f.read()

            # Display the video with Streamlit video component
            st.write("Please click the play button to watch the resullt video below:")
            st.video(video_bytes)

        except Exception as e:
            st.error('Error: %s' % e)
        finally:
            # Close the temporary files
            temp_out_file.close()
            # Delete the temporary file
            os.unlink(temp_out_file.name)
