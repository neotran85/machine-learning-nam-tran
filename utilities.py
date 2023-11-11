import inspect
import textwrap
import base64
import streamlit as st
import os
import importlib.util
import sys
import consts

# delete out files
def delete_out_file(path):
    if os.path.exists(path):
        os.remove(path)

def show_code(demo):
    """Showing the code of the demo."""
    show_code = st.sidebar.checkbox("Show code", True)
    if show_code:
        # Showing the code of the demo.
        st.markdown("## Code")
        sourcelines, _ = inspect.getsourcelines(demo)
        st.code(textwrap.dedent("".join(sourcelines[1:])))

def show_about_me():
    # CSS to style the sidebar
    style = """
        <style>
            .sidebar .sidebar-content {
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            #avatar {
                border-radius: 50%;
                margin-top: 10px;
                margin-bottom: 10px;
                width: 100px;
            }
            #name {
                font-weight: bold;
                font-size: 20px;
                color: #4A90E2;
            }
        </style>
    """
    # Function to convert image to base64
    def get_image_base64(path):
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')

    # Get the path to the avatar.png image
    avatar_base64 = get_image_base64("avatar.png")

    # Applying the CSS style
    st.markdown(style, unsafe_allow_html=True)

    # Displaying avatar and name on the sidebar with styling
    st.sidebar.markdown(f'<img id="avatar" src="data:image/png;base64,{avatar_base64}" />', unsafe_allow_html=True)
    st.sidebar.markdown('<p id="name">Nam Tran</p>', unsafe_allow_html=True)
    st.sidebar.markdown("""I am a passionate individual with a keen interest in the realm of machine learning. Driven by curiosity and a deep-seated desire to unravel the complexities of data, I continually seek to harness the power of algorithms to extract meaningful insights and solve real-world problems. Whether it's building predictive models or delving into the intricacies of neural networks, my enthusiasm for the field is palpable. Always eager to learn and evolve, I believe that machine learning holds the key to the future, and is fervently working towards making a significant impact in this dynamic domain.""", unsafe_allow_html=True)

    # Your social media links
    linkedin_link = "https://www.linkedin.com/in/nam-tran-bb765220b"
    telegram_link = "https://t.me/namtrantelegram"

    telegram_base64 = get_image_base64("telegram.png")
    linkedId_base64 = get_image_base64("linkedin.png")

    st.sidebar.markdown(
        f'''
        <a href="{telegram_link}" target="_blank">
            <img id="telegram_avatar" src="data:image/png;base64,{telegram_base64}" style="width:50px; height:50px; display:inline; margin-right:10px;"/>
        </a>
        <a href="{linkedin_link}" target="_blank">
            <img id="linkedin_avatar" src="data:image/png;base64,{linkedId_base64}" style="width:50px; height:50px; display:inline;"/>
        </a>
        ''', 
        unsafe_allow_html=True
    )
def run_script(script_name):
        script_path = os.path.join('tech', f"{script_name}.py")
        spec = importlib.util.spec_from_file_location(script_name, script_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules[script_name] = module
        spec.loader.exec_module(module)

def show_left_menu():
    # Define your project structure with titles
    folders = {
        "AI-powered Image Processing": [("image_generate_from_text", "Text To Image Generator"),
                                ("image_inpainting", "Image Inpainting"),
                                ("image_enhance", "Image Enhancement"),
                                ("image_upscale", "Image Upscaler"),
                                ("image_extender", "Image Extender"),
                                ("image_face_fix", "Fix Faces"),
                                ("image_explanation", "Picture Explanation"),
                                ("image_annotation", "Video/Images Annotation"),
                                ("image_pose_detector", "Pose Detector"),
                                ("image_emotion_detector", "Emotion Detector"),
                                ("image_remove_bg", "Background Eraser")],
        "Natural Language Processing": [("language_chatbot", "AI Assistant"),
                                        ("ads_comparation", "Item 222")],                 
        "Data Science": [("ads_comparation1", "Item 112"),
                         ("ads_comparation1", "Item 212")]
        # Add more folders and script-title tuples (without the .py extension)
    }

    # Use Streamlit's session state to track the current script
    if 'current_script' not in st.session_state:
        st.session_state['current_script'] = None

    # Custom CSS to inject contained in a string
    custom_css = """
        <style>
            .stButton > button {
                width: 100%;
                justify-content: flex-end;
                text-align: right;
                padding-right: 1rem; /* Adjust the padding to control the text position */
            }
            .stButton > button > span {
                font-size: 0.6em; /* Adjust font size as needed */
            }
        </style>
    """

    # Inject custom CSS
    st.markdown(custom_css, unsafe_allow_html=True)

    # Sidebar with the folder structure
    for folder_name, scripts in folders.items():
        with st.sidebar.expander(folder_name):
            for script, title in scripts:
                # When a link is clicked, update the session state to the clicked script
                if st.button(title):
                    st.session_state['current_script'] = script

    # Main page logic
    if st.session_state['current_script']:
        run_script(st.session_state['current_script'])
    else:
        st.title("Welcome to My Portfolio")
        st.write("Please select a project from the sidebar to learn more.")


