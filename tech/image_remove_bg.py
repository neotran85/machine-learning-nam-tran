import streamlit as st
from rembg import remove
from PIL import Image
from io import BytesIO
import base64


st.write("## Remove background from your picture")

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