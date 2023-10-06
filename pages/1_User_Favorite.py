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


# Upload dataset
st.title("Predict the Top N Probable Items to be Purchased")

def processData(filename):
    # Label encoding
    df = pd.read_csv(filename)  

    df['Gender'] = le_gender.fit_transform(df['Gender'])
    df['Item Purchased'] = le_item.fit_transform(df['Item Purchased'])
    # Splitting the data
    X = df[['Age', 'Gender']]
    y = df['Item Purchased']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Training the classifier
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    # Streamlit interface

    # User inputs
    age = st.slider("Select Age", 20, 70)
    gender = st.radio("Select Gender", ["Male", "Female"])

    predicted_items, probabilities = get_top_n_probable_items(clf, age, gender)

    # Visualization
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.pie(probabilities, labels=predicted_items, startangle=90, autopct='%1.1f%%')
    ax.axis('equal')
    plt.title('Top N Probable Items')
    st.pyplot(fig)


def get_top_n_probable_items(clf, age, gender, n=10):
    # Encoding the inputs
    gender_encoded = le_gender.transform([gender])[0]
    
    # Predicting probabilities
    probs = clf.predict_proba([[age, gender_encoded]])[0]
    
    # Sorting items based on probabilities
    sorted_indices = probs.argsort()[::-1][:n]
    sorted_probs = probs[sorted_indices]
    sorted_items = le_item.inverse_transform(sorted_indices)
    
    return sorted_items, sorted_probs

# Choice for the user
choice = st.radio('Choose a data source', ['Upload my own dataset', 'Use default dataset'])

if choice == 'Upload my own dataset':
    uploaded_file = st.file_uploader("Upload your dataset (csv file)", type="csv")
    if uploaded_file is not None:
        try:
            processData(uploaded_file)
        except:
            processData('trend.csv')
else:
    processData('trend.csv')

    