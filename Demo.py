import streamlit as st
import base64
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# Import AutoML stuff
import h2o
from h2o.automl import H2OAutoML
from sklearn.model_selection import train_test_split

h2o.init()
st.title('AutoML Demo for every dataset')
st.write('This is a demo for AutoML on every dataset. You can upload your own dataset and see the results of AutoML on it. The results are shown in the sidebar on the left. You can also download the results as a csv file.')

# Step 1: Upload your dataset
st.header('Step 1: Upload your dataset')
st.write('Upload your dataset as a csv file (only). The first row should contain the column names. The last column should be the target column.')
uploaded_file = st.file_uploader("Choose a file", type="csv")


# Step 2: Choose the target column. 
# Define a function for step 2 named step2() and call it in step 1
target_column = None
def step2():
    st.header('Step 2: Choose the target column')   
    st.write('Choose the target column of your dataset. The target column should be the last column of your dataset.')
    default_target_column = data.columns[-1]
    target_column = st.selectbox('Which column is the target column?', data.columns, index=data.columns.get_loc(default_target_column))
    return target_column

# Show Heatmap of all columns to see missing values
def showHeatmapOfMissingData():
    # Create a figure and axes for the heatmap
    fig, ax = plt.subplots(figsize=(8, 6))
    # Create the heatmap to visualize missing values
    sns.heatmap(data.isnull(), cbar=False, cmap='viridis', ax=ax)
    ax.set_title('Missing Values Heatmap')
    st.pyplot(fig)
    # % missing values in each column. Only get 2 decimals. Column 1: column name, column 2: % missing values
    # Calculate missing value percentages
    st.write('Percentage of Missing Values Table')
    missing_percentages = round(data.isnull().sum() / len(data) * 100, 2)
    # Create a Pandas DataFrame for the missing value percentages
    missing_data_table = pd.DataFrame({'Features': missing_percentages.index, 'Missing Percentage (%)': missing_percentages.values})
    # Display the table using Streamlit
    st.write(missing_data_table)

# Show skewed data
def showSkewedData():
    skewness_threshold = 1.0  # Adjust this value as needed
    # Visualize the skewness for each numeric column
    st.write('Skewness Histograms')
    for column in data.select_dtypes(include='number').columns:
        fig, ax = plt.subplots(figsize=(6, 4))
        sns.histplot(data[column], kde=True, color='blue', ax=ax)
        ax.set_title(f'Distribution of {column}')
        ax.set_xlabel(column)
        ax.set_ylabel('Frequency')
        skewness = data[column].skew()
        if abs(skewness) > skewness_threshold:
            # Annotate skewed features
            ax.annotate(f"Skewness: {skewness:.2f} (Skewed)", xy=(0.7, 0.9), xycoords='axes fraction', color='red')
        st.pyplot(fig)


# Step 3: Exploratory data analysis
# Define a function for step 3 named step3() and call it in step 2    
# After uploading completed, show 5 head rows of the dataset and all column names
def step3():
    st.header('Step 3: Exploratory data analysis')
    # Show Heatmap to see missing values
    st.write('The heatmap below shows the missing values in the dataset.')
    showHeatmapOfMissingData()
    showSkewedData()

# Step 4: AutoML building models
def step4():
    st.header('Step 4: AutoML building models')
    # Split the data into train and test sets
    h2o_data = h2o.H2OFrame(data)
    train, test = h2o_data.split_frame(ratios=[0.7], seed=42)
    aml = H2OAutoML(max_runtime_secs=180)  # Maximum runtime in seconds
    aml.train(x=h2o_data.columns, y=target_column, training_frame=train)
    lb = aml.leaderboard
    # Get the top 10 models
    st.write('Top 10 Models')
    st.write(lb.head(rows=10))

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write(data.head())
    st.write('The column names are: ' + ', '.join(data.columns))
    target_column = step2()
    if(target_column is not None):
        ## step3()
        step4()
    