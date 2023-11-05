import streamlit as st
import os
import importlib.util
import sys
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

avatar_file_path = os.path.abspath("assets/avatar.png")
avatar_base64 = get_image_base64(avatar_file_path)

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
# Set page config
st.set_page_config(page_title="My Portfolio", layout="wide")

# Define your project structure with titles
folders = {
    "Data Science": [("ads_comparation", "Ads Comparation")]
    # Add more folders and script-title tuples (without the .py extension)
}

# Function to import and run a script
def run_script(script_name):
    script_path = os.path.join('tech', f"{script_name}.py")
    spec = importlib.util.spec_from_file_location(script_name, script_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[script_name] = module
    spec.loader.exec_module(module)

# Use Streamlit's session state to track the current script
if 'current_script' not in st.session_state:
    st.session_state['current_script'] = None

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
