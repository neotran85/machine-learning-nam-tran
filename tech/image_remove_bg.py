import streamlit as st
from rembg import remove
from PIL import Image
from io import BytesIO
import base64


st.write("## Remove background from your picture")
st.write("Quickly and effortlessly separate the subject from the background with AI-powered tool.")

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB

# Download the fixed image
def convert_image(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    byte_im = buf.getvalue()
    return byte_im

def fix_image(upload):
    image = Image.open(upload)
    col1.write("Before:")
    col1.image(image)

    fixed = remove(image)
    col2.write("After:")
    col2.image(fixed)

col1, col2 = st.columns(2)
my_upload = st.file_uploader("Upload a picture here:", type=["png", "jpg", "jpeg"])

if my_upload is not None:
    if my_upload.size > MAX_FILE_SIZE:
        st.error("The uploaded file is too big. Please upload a picture smaller than 5MB. Thank you.")
    else:
        fix_image(upload=my_upload)


st.write("""
#### Background Removal with rembg

Rembg is an AI-powered tool that removes the background from images. It is based on a machine learning model that has been trained on a large dataset of images with and without backgrounds. 
         
1. **Input**: Upload your image to the tool. rembg supports various image formats such as JPG, PNG, and BMP.

2. **Detection**: The AI model within rembg analyzes the image, identifying and segmenting the main subject from the background. It's trained on a vast dataset of images, which allows it to handle complex scenarios like fine hair details, transparent objects, and various backgrounds.

3. **Processing**: Once the subject is identified, rembg processes the image to separate the subject from its background. This step involves creating a mask that outlines the subject perfectly.

4. **Output**: The final result is a clear image of the subject with a transparent background (usually in PNG format) that you can download and use in various applications such as graphic design, product presentations, or web design.

The process is quick, efficient, and requires no manual editing, making rembg a powerful tool for photographers, designers, and content creators who need to isolate subjects from their backgrounds frequently.
""")

st.write("""
#### Image Requirements for Optimal Background Removal

To achieve the best results with rembg, your images should meet the following criteria:

- **High Resolution**: The finer the details, the better rembg can detect edges and separate the subject from the background.

- **Good Lighting**: Well-lit subjects with minimal shadows allow the AI to more accurately identify the edges and contours.

- **Contrast**: Images where the subject has distinct colors compared to the background help in creating a more precise cut-out.

- **Minimal Noise**: Clean images with low levels of grain or digital noise prevent the AI from mistaking noise for part of the subject.

- **Subject Placement**: Central placement of the subject with some space around it can improve the detection process.

- **Sharp Focus**: The subject should be in sharp focus, with the background preferably out of focus to enhance separation.

Remember, the quality of the input image greatly influences the final result. Images that do not meet these criteria may still be processed but could lead to less accurate background removal.
""")

