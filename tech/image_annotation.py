import streamlit as st
import cv2
import tempfile
import torch
import os
from PIL import Image
import numpy as np

# Check if CUDA is available and set the device to GPU
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
# Load YOLOv5 model onto the device
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True).to(device)

st.title("AI-powered Image and Video Annotator")

if torch.cuda.is_available():
    st.write("CUDA is available. Using GPU for inference.")
else:
    st.write("CUDA is not available. Using CPU for inference.")

uploaded_file = st.file_uploader("Please upload an image or MP4 video (shorter than 30 seconds):", type=["mp4", "jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Process image
    if uploaded_file.type in ["image/jpeg", "image/png"]:
        with st.spinner('Analyzing the image...'):
            # Read the image into memory
            bytes_data = uploaded_file.getvalue()
            image = Image.open(uploaded_file)
            image = np.array(image)  # Convert to numpy array

            # Ensure that image is RGB (3 channels)
            if image.ndim == 2 or (image.ndim == 3 and image.shape[2] == 1):
                image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
            elif image.ndim == 3 and image.shape[2] > 3:
                image = image[:, :, :3]

            # Inference
            results = model(image)

            # Render the results
            rendered_data = results.render()
            annotated_image = rendered_data[0]  # Take the first annotated image

            # Convert the annotated image to PIL format to display in Streamlit
            annotated_image_pil = Image.fromarray(annotated_image)
            st.image(annotated_image_pil, caption='Annotated Image', use_column_width=True)

    # Process video
    elif uploaded_file.type == "video/mp4":
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
                st.write("Please click the play button to watch the result video below:")
                st.video(video_bytes)

            except Exception as e:
                st.error('Error: %s' % e)
            finally:
                # Close the temporary files
                temp_out_file.close()
                # Delete the temporary file
                os.unlink(temp_out_file.name)
