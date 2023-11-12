import streamlit as st
from openai import OpenAI
import consts
import os
import tempfile

def clear_history():
  st.session_state.audio_history = []
  show_audio_history()  # Show the empty chat history
  chat_container.empty()  # Clear the chat input box

def show_audio(message): 
    # if message is empty, do not show audio
    if message:
      speech_file_path = tempfile.NamedTemporaryFile(delete=True).name
      response = client.audio.speech.create(
          model="tts-1",
          voice=selected_voice,
          input=message
      )
      response.stream_to_file(speech_file_path)
      st.audio(speech_file_path)


# Placeholder for chat messages
chat_container = st.empty()
os.environ['OPENAI_API_KEY'] = consts.API_KEY_OPEN_AI
client = OpenAI()

def show_audio_history():
    for author, message in st.session_state.audio_history:
        with st.chat_message(author):
            if author == 'AI Assistant':
                show_audio(message)
            else:
              st.write(message)

# Streamlit UI
st.title("AI-powered Text To Speech")
voices = ['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer'] 
selected_voice = st.selectbox("Choose a voice", voices)


# Initialize chat history in session state
if 'audio_history' not in st.session_state:
    st.session_state.audio_history = []
    
# Chat input for user message
user_message = st.chat_input("Type something to for AI to read...")

if user_message:
    clear_history()  # Clear the chat history
    # Add user message to chat history
    st.session_state.audio_history.append(('user', user_message))

    # Temporary loading message
    loading_message = "AI is preparing..."
    st.session_state.audio_history.append(('AI Assistant', loading_message))
    show_audio_history()  # Show chat history with loading message

    # Replace the loading message with the actual response
    st.session_state.audio_history[-1] = ('AI Assistant', user_message)
    # Redisplay the chat history with the actual response
    st.experimental_rerun()

show_audio_history()  # Show the chat history



