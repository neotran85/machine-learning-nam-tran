from pathlib import Path
from openai import OpenAI
import os
import consts
import streamlit as st
import tempfile

os.environ['OPENAI_API_KEY'] = consts.API_KEY_OPEN_AI
client = OpenAI()

speech_file_path = tempfile.NamedTemporaryFile(delete=True).name
response = client.audio.speech.create(
  model="tts-1",
  voice="alloy",
  input="Currently, the name is not shown in the UI but is only set as an accessibility label. For accessibility reasons, you should not use an empty string."
)
response.stream_to_file(speech_file_path)
st.audio(speech_file_path)

