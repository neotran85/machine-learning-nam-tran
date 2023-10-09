import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
import streamlit as st
import base64
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import streamlit as st
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
le_gender = LabelEncoder()
le_item = LabelEncoder()

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

# DEMO
st.title("Demo")
import streamlit as st
import openai
import requests

# Configure OpenAI API

def generate_and_structure_quiz(topic):
    # Set up OpenAI API key
    openai.api_key = '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'    
    # Define the prompt
    prompt_text = f"Please generate 10 multiple-choice questions on the topic of {topic}. Format each question as follows:\n\nQuestion: [Question Text]\nA) [Choice A]\nB) [Choice B]\nC) [Choice C]\nD) [Choice D]\nAnswer: [Letter of Correct Answer]\n\nUse a newline to separate each question."
    
    # Get the model's response
    response = openai.Completion.create(engine="davinci", prompt=prompt_text, max_tokens=1000)
    raw_quiz = response.choices[0].text.strip()

    # Process raw quiz to structured data
    raw_questions = raw_quiz.split("\n\n")
    structured_questions = []

    for rq in raw_questions:
        lines = rq.split("\n")
        question_text = lines[0].split(": ")[1]
        options = {
            "A": lines[1].split(") ")[1],
            "B": lines[2].split(") ")[1],
            "C": lines[3].split(") ")[1],
            "D": lines[4].split(") ")[1]
        }
        answer = lines[5].split(": ")[1]
        
        structured_questions.append({
            "question": question_text,
            "options": options,
            "answer": answer
        })
    print(structured_questions)
    return structured_questions
# Streamlit App
st.title("Quiz Generator using OpenAI")
quiz = generate_and_structure_quiz("Machine Learning")
    