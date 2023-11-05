import streamlit as st
import os
import importlib.util
import sys

# Set page config
st.set_page_config(page_title="My Portfolio", layout="wide")

# Define your project structure
folders = {
    "Data Science": ["0_Ads_Comparation"]
    # Add more folders and script names (without the .py extension)
}

# Function to import and run a script
def run_script(script_name):
    # Load the script as a module
    spec = importlib.util.spec_from_file_location(script_name, f"./pages/{script_name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

# Use Streamlit's session state to track the current script
if 'current_script' not in st.session_state:
    st.session_state['current_script'] = None

# Sidebar with the folder structure
for folder_name, scripts in folders.items():
    with st.sidebar.expander(folder_name):
        for script in scripts:
            # When a link is clicked, update the session state to the clicked script
            if st.button(script):
                st.session_state['current_script'] = script

# Main page logic
if st.session_state['current_script']:
    run_script(st.session_state['current_script'])
else:
    st.title("Welcome to My Portfolio")
    st.write("Please select a project from the sidebar to learn more.")

