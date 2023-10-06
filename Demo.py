import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
import streamlit as st

# Upload dataset
st.title("Predict Churn of Telecom Services")

def handleMissingData(df):
    # Identify and handle missing values
    for col in df.columns:
        if df[col].dtype == 'object':
            # For string columns, fill NaN with the most frequent value in that column
            df[col].fillna(df[col].mode()[0], inplace=True)
        else:
            # For numeric columns, fill NaN with the median value of that column
            df[col].fillna(df[col].median(), inplace=True)
    return df
def processData(df):
    le = LabelEncoder()

    # Drop Customer_ID as it's an identifier and not a predictor
    df.drop('Customer_ID', axis=1, inplace=True)
    df = handleMissingData(df)
    # Identify all non-numeric columns
    string_cols = df.select_dtypes(include='object').columns
    for col in string_cols:
        df[col] = le.fit_transform(df[col])
        
    # Assume 'churn' is the target column
    X = df.drop('churn', axis=1)
    y = df['churn']

    # Split data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Scale the data
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    clf = LogisticRegression(max_iter=1000)  # Increased max_iter for convergence
    clf.fit(X_train_scaled, y_train)
    y_pred = clf.predict(X_test_scaled)
    results = pd.DataFrame({'Actual': y_test, 'Predicted': y_pred})

    # Counting the actual churns and no-churns
    actual_counts = results['Actual'].value_counts()
    predicted_counts = results['Predicted'].value_counts()

    # Setting the bar positions
    bar_positions = range(2)  # Assuming binary classification: churned or not-churned
    bar_width = 0.35

    # Create a new figure and axis
    fig, ax = plt.subplots(figsize=(10,6))

    # Creating bars on the ax
    ax.bar(bar_positions, actual_counts, width=bar_width, label='Actual', color='blue')
    ax.bar([pos+bar_width for pos in bar_positions], predicted_counts, width=bar_width, label='Predicted', color='red')

    # Adding labels, title, and legend
    ax.set_xlabel('Churn')
    ax.set_ylabel('Count')
    ax.set_title('Actual vs Predicted Churn')
    ax.set_xticks([pos+bar_width/2 for pos in bar_positions])
    ax.set_xticklabels(['No Churn', 'Churn'])
    ax.legend()

    # Display the plot
    plt.tight_layout()
    st.pyplot(fig)

def plotChurnOverTime(df):
    # Group by eqpdays and compute churn rate
    churn_rate = df.groupby('eqpdays')['churn'].mean()

    fig, ax = plt.subplots(figsize=(10,6))
    churn_rate.plot(ax=ax)
    ax.set_title('Churn Rate over Time (eqpdays)')
    ax.set_ylabel('Churn Rate')
    ax.set_xlabel('Equipment Days')
    plt.tight_layout()
    st.pyplot(fig)

def plotPieLoyalty(df):
    # Count of loyal vs not loyal
    churn_counts = df['churn'].value_counts()

    # Plot
    labels = ['Loyal', 'Not Loyal']
    colors = ['green', 'red']
    explode = (0.1, 0)  # explode 1st slice for emphasis

    fig, ax = plt.subplots(figsize=(10,6))
    ax.pie(churn_counts, explode=explode, labels=labels, colors=colors,
    autopct='%1.1f%%', shadow=True, startangle=140)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax.set_title("Percentage of Customers Loyal vs. Not Loyal")
    st.pyplot(fig)
    plt.show()

data = pd.read_csv('Telecom_customer.csv')
processData(data)
plotChurnOverTime(data)
plotPieLoyalty(data)

