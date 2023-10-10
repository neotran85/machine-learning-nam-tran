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
import dateutil.parser
import re

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
def showHeatMap(data):
    missing_data = data.isnull()
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(missing_data, cbar=False, cmap="viridis_r", ax=ax)
    ax.set_title("Missing Data Heatmap (Yellow for missing values)")
    st.pyplot(fig)

def is_date_string(cols):
    # Regex pattern for date strings in the format DD-MM-YY for example: 01-Jan-23.
    pattern = re.compile(r'\d{2}-[a-zA-Z]{3}-\d{2}')
    # Return True if any of the values in cols match the pattern, else False.
    return any(pattern.match(str(val)) for val in cols) 
  
  
# DEMO
# I - Data Preprocessing
df = pd.read_csv('breast_cancer.csv')
print(df)
# Drop all rows having 100% missing values
df.dropna(axis=0, how='all', inplace=True)
showHeatMap(df)
# Drop the column named Patient_ID
df.drop('Patient_ID', axis=1, inplace=True)

# Missing Values
st.markdown("## Missing Values:")

for column in df.columns:
    if df[column].dtype == 'object':
        df[column].fillna(df[column].mode()[0], inplace=True)
print(df)
# Find columns with date strings
date_cols = [col for col in df.columns if is_date_string(df[col])]

for column in date_cols:
        temp = pd.to_datetime(df[column])
        df[column] = temp.astype('int64') // 10**6
print(df)
# For date_cols, find missing data and replace with K Nearest Neighbor imputation
from sklearn.impute import KNNImputer
imputer = KNNImputer(n_neighbors=3)
df[date_cols] = imputer.fit_transform(df[date_cols])
showHeatMap(df)

# Check if there are any missing values left
print(df.isnull().sum())
# Encoding
st.markdown("## Encoding:")
# For categorical columns, if it is binary with only two unique values, use cat codes to encode
for column in df.columns:
    if df[column].dtype == 'object':
        len_unique = len(df[column].unique())
        if len_unique == 1:
            df[column] = 1
        elif len_unique == 2:
            df[column] = df[column].astype('category').cat.codes
print(df)

# check if there are any binary categorical columns left
print(df.nunique())
# For categorical columns, use one hot encoding
df = pd.get_dummies(df, drop_first=True)
print(df)
# Check if the data frame is ready for modeling
print(df.head())

# Visualize the data distribution
st.markdown("## Data Distribution:")
st.markdown("### Histogram:")
for column in df.columns:
    fig, ax = plt.subplots()
    sns.histplot(df[column], ax=ax)
    st.pyplot(fig)
st.markdown("### Boxplot:")
for column in df.columns:
    fig, ax = plt.subplots()
    sns.boxplot(df[column], ax=ax)
    st.pyplot(fig)
st.markdown("### Violinplot:")
for column in df.columns:
    fig, ax = plt.subplots()
    sns.violinplot(df[column], ax=ax)
    st.pyplot(fig)
st.markdown("### Scatterplot:")
for column in df.columns:
    fig, ax = plt.subplots()
    sns.scatterplot(x=df[column], y=df['Breast Cancer'], ax=ax)
    st.pyplot(fig)


