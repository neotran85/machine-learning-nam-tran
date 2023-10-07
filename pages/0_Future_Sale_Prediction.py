
import streamlit as st
from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer
import seaborn as sns
from sklearn.linear_model import LinearRegression
import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from statsmodels.tsa.arima.model import ARIMA
from prophet import Prophet

import streamlit as st

st.title("Forecasted Number of Customers Using Prophet with Japanese Holidays")
st.sidebar.markdown("""
**Description:**

This code is designed for visualizing and forecasting customer data, specifically with a focus on monthly customer counts. The forecasting model used is the Prophet model, which is especially tailored for time series forecasting involving multiple seasonalities and special events. A unique feature is the inclusion of Japanese holidays, which are used to inform the model about potential seasonality shifts or specific days where customer counts might deviate from the norm.

**Potential Business Benefits:**

1. **Informed Decision Making:** By visualizing customer trends over time, businesses can make informed decisions regarding marketing campaigns, inventory management, and resource allocation.
2. **Proactive Approach:** The forecasting feature allows businesses to prepare for expected customer counts in advance, optimizing resource utilization.
3. **Targeted Marketing:** Understanding the distribution of customers based on education and marital status can allow for more targeted marketing campaigns.
4. **Cultural Sensitivity:** By acknowledging and incorporating Japanese holidays, businesses can better tailor their strategies to the Japanese market, whether it's for marketing campaigns, promotions, or inventory management.
5. **Customizability:** The code provides options for users to upload their datasets or use a default one, making it versatile for various business needs.

""")

def processData(filename):
    data = pd.read_csv(filename, delimiter=';')
    # Hypothetical prior scales based on expected impact
    strong_effect = 10
    weak_effect = 0.5
    # Specifying the holidays with their expected effects
    holidays_data = {
        'New Year\'s Day (Shōgatsu)': '2024-01-01', 
        'Coming of Age Day (Seijin no Hi)': '2024-01-08',  # Might have moderate impact
        'National Foundation Day (Kenkoku Kinen no Hi)': '2024-02-11', 
        'The Emperor\'s Birthday': '2024-02-23', 
        'Vernal Equinox Day (Shunbun no Hi)': '2024-03-20',
        'Shōwa Day (Shōwa no Hi)': '2024-04-29',
        'Constitution Memorial Day (Kenpō Kinenbi)': '2024-05-03',
        'Greenery Day (Midori no Hi)': '2024-05-04',
        'Children\'s Day (Kodomo no Hi)': '2024-05-05',
        'Marine Day (Umi no Hi)': '2024-07-15',
        'Mountain Day (Yama no Hi)': '2024-08-11', 
        'Respect for the Aged Day (Keirō no Hi)': '2024-09-16',
        'Autumnal Equinox Day (Shūbun no Hi)': '2024-09-22',
        'Sports Day (Taiiku no Hi)': '2024-10-14',
        'Culture Day (Bunka no Hi)': '2024-11-03', 
        'Labor Thanksgiving Day (Kinrō Kansha no Hi)': '2024-11-23'
    }

    # Let's assume holidays like New Year's Day and Golden Week have a strong impact, while others have a weaker impact.
    strong_holidays = ['New Year\'s Day (Shōgatsu)', 'Shōwa Day (Shōwa no Hi)', 'Constitution Memorial Day (Kenpō Kinenbi)', 'Greenery Day (Midori no Hi)', 'Children\'s Day (Kodomo no Hi)']

    prior_scales = [strong_effect if holiday in strong_holidays else weak_effect for holiday in holidays_data.keys()]

    japanese_holidays = pd.DataFrame({
        'holiday': list(holidays_data.keys()),
        'ds': pd.to_datetime(list(holidays_data.values())),
        'lower_window': 0,
        'upper_window': 1,
        'prior_scale': prior_scales
    })


    # Load dataset
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


    # Convert 'Dt_Customer' column to datetime
    data['Dt_Customer'] = pd.to_datetime(data['Dt_Customer'])

    # Resample the data by month and count the number of customers for each month
    customer_counts_monthly = data.resample('M', on='Dt_Customer').size()

    # Create a figure and ax object
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot using ax
    customer_counts_monthly.plot(ax=ax)
    # Setting monthly labels
    ax.set_xticks(customer_counts_monthly.index)
    ax.set_xticklabels([months[i.month-1] for i in customer_counts_monthly.index], rotation=45)

    ax.set_ylabel('Number of Customers')
    ax.set_xlabel('Month')
    ax.set_title('Number of Customers Over Time (by Month)')
    ax.grid(True)
    st.pyplot(fig)



    # Resample data by month and count the number of customers for each month
    monthly_counts = data.resample('M', on='Dt_Customer').size().reset_index()
    monthly_counts.columns = ['ds', 'y']  # 'ds' for date and 'y' for value are required column names for Prophet

    # Initialize and fit the model
    model = Prophet(yearly_seasonality=True, holidays=japanese_holidays)
    model.fit(monthly_counts)

    # Create future dataframe for 2024 predictions
    future = model.make_future_dataframe(periods=12, freq='M')

    # Forecast
    forecast = model.predict(future)

    # Extract months and predicted y values for plotting
    forecasted_dates = forecast['ds'][-12:]  # Extracting only the last 12 months (i.e., the forecasted period for 2024)
    forecasted_values = forecast['yhat'][-12:]
    # Example: Replacing the outliers with the average of surrounding months
    forecasted_values.iloc[0] = forecasted_values.mean()
    forecasted_values.iloc[-1] = forecasted_values.mean()


    # Create a figure and ax object
    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot historical data
    ax.plot(monthly_counts['ds'], monthly_counts['y'], label='Historical', color='gray', linestyle='--')

    # Plot forecasted data
    ax.plot(forecasted_dates, forecasted_values, label='Forecasted', color='blue')

    # Setting monthly labels
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    ax.set_xticks(forecasted_dates)
    ax.set_xticklabels(months, rotation=45)

    ax.set_ylabel('Number of Customers')
    ax.set_xlabel('Month of 2024')
    ax.set_title('Forecasted Number of Customers Using Prophet')
    ax.grid(True)
    ax.legend()

    st.pyplot(fig)

    # Create a figure and axes object
    fig, ax = plt.subplots(figsize=(10, 10))

    # Calculate the percentage of customers in each education level
    education_counts = data['Education'].value_counts()
    education_percentages = education_counts / education_counts.sum() * 100

    # Create a pie chart of the number of customers by education level
    ax.pie(education_percentages, labels=education_counts.index, autopct='%1.1f%%')
    ax.set_title('Number of Customers by Education Level')

    # Display the figure
    st.pyplot(fig)


    # Calculate the average monthly revenue per customer by marital status
    average_monthly_revenue_by_marital_status = data.groupby('Marital_Status')['MntWines'].mean()

    # Create a figure and axes object
    fig, ax = plt.subplots(figsize=(10, 10))

    # Create a pie chart of the average monthly revenue per customer by marital status
    ax.pie(average_monthly_revenue_by_marital_status, labels=average_monthly_revenue_by_marital_status.index, autopct='%1.1f%%')
    ax.set_title('Average Monthly Revenue per Customer by Marital Status')

    # Display the figure
    st.pyplot(fig)


    # Display Japanese holidays
    st.subheader("Japanese Holidays for 2024:")
    st.table(japanese_holidays.drop(columns=['lower_window', 'upper_window']))

    st.write("Displaying the entire dataset:")
    st.write(data)

# Choice for the user
choice = st.radio('Choose a data source', ['Upload my own dataset', 'Use default dataset'])

if choice == 'Upload my own dataset':
    uploaded_file = st.file_uploader("Upload your dataset (csv file)", type="csv")
    if uploaded_file is not None:
        try:
            processData(uploaded_file)
        except:
            processData('campaign.csv')
else:
    processData('campaign.csv')
    

