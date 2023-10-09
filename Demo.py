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
#I - Data Preprocessing
df = pd.read_csv('breast_cancer.csv')
print(df)
import pandas as pd
st.title("Missing Data Visualization with Missingno")
st.write("Missing data matrix:")

st.title("Missing Data Visualization")

# Create a heatmap of missing data
st.write("### Missing Data Heatmap:")

# Convert data presence (True/False) into integers (1/0)
df = df.drop('Patient_ID', axis=1)
print(df)
def showHeatMap(data):
    missing_data = data.isnull()
    fig, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(missing_data, cbar=False, cmap="viridis_r", ax=ax)
    ax.set_title("Missing Data Heatmap (Yellow for missing values)")
    st.pyplot(fig)
showHeatMap(df)

# Drop rows where more than 50% of data is missing
threshold = 0.5 * len(df.columns) # 50% of the number of columns
df = df.dropna(thresh=threshold)
showHeatMap(df)

numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

from sklearn.impute import SimpleImputer
mean_imputer = SimpleImputer(strategy='mean')
df_mean_imputed = df.copy()

def convertDateToMilliseconds(date_string):
    try:
        date_obj = pd.to_datetime(date_string, format="%d-%b-%y")
        timestamp_millis = int(date_obj.timestamp() * 1000)
        return timestamp_millis
    except: return None
def roman_to_int(s: str) -> int:
    roman_dict = {
        'I': 1,
        'V': 5,
        'X': 10,
        'L': 50,
        'C': 100,
        'D': 500,
        'M': 1000
    }

    total = 0
    prev_value = 0

    for char in s[::-1]:  # Reverse the string for easy processing
        value = roman_dict[char]
        if value < prev_value:
            total -= value
        else:
            total += value
        prev_value = value

    return total

df_mean_imputed['Date_of_Surgery'] = df_mean_imputed['Date_of_Surgery'].apply(convertDateToMilliseconds)
df_mean_imputed['Date_of_Last_Visit'] = df_mean_imputed['Date_of_Last_Visit'].apply(convertDateToMilliseconds)
df_mean_imputed['Tumour_Stage'] = df_mean_imputed['Tumour_Stage'].apply(roman_to_int)
categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
for col in categorical_cols:
    df_mean_imputed[col] = df_mean_imputed[col].astype('category').cat.codes
print(df_mean_imputed)

numeric_cols = df_mean_imputed.select_dtypes(include=['float64', 'int64']).columns.tolist()
mean_imputer = SimpleImputer(strategy='mean')
df_mean_imputed[numeric_cols] = mean_imputer.fit_transform(df_mean_imputed[numeric_cols])
showHeatMap(df_mean_imputed)

def is_all_numeric(df):
    return df.select_dtypes(include=['number']).shape[1] == df.shape[1]
print(is_all_numeric(df_mean_imputed))