import requests
import streamlit as st

# Assuming consts.py is in the same directory and contains the API_KEY_HUGGING_FACE
from consts import API_KEY_HUGGING_FACE

# Set the API URL for a specific model
API_URL = "https://api-inference.huggingface.co/models/meta-llama/Llama-2-7b-chat-hf"

# Headers with the Hugging Face API Key
headers = {"Authorization": f"Bearer {API_KEY_HUGGING_FACE}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Function to update conversation history and return AI response
def send_message(message):
    payload = {
        "inputs": message,
        "parameters": {
            "max_new_tokens": 1000  # Sets the maximum length of the generation
        }
    }
    output = query(payload)
    ai_message = output[0]["generated_text"] if output else "No response from AI."
    st.session_state.history.append(("User", message))
    st.session_state.history.append(("AI", ai_message))
    st.session_state.user_input = ''  # Clear the user input after sending the message

st.title('AI Conversation Chat')

# Initialize session state variables if they don't exist
if 'history' not in st.session_state:
    st.session_state['history'] = []
if 'user_input' not in st.session_state:
    st.session_state['user_input'] = ''

# Text input for user message with an on_change callback to clear input after message is sent
user_message = st.text_input("You:", value=st.session_state.user_input, key="user_input")

# When the user presses enter or the send button, update the conversation history
if st.button("Send"):
    if user_message:
        send_message(user_message)

# Display the conversation history
for role, message in st.session_state['history']:
    if role == "User":
        st.text_area("", value=message, height=40, key=f"user_{len(st.session_state['history'])}")
    else:
        st.text_area("", value=message, height=100, key=f"ai_{len(st.session_state['history'])}")
