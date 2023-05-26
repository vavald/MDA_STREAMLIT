import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import time
import pickle
import sklearn
from sklearn.ensemble import RandomForestRegressor
import plotly.graph_objects as go

# Set up the main layout
st.set_page_config(page_title="Gradient Boosting Model Explanation", page_icon="🌳", layout='wide', initial_sidebar_state='auto')

data = pd.read_csv('data/model_input.csv',delimiter=';')

# Load the model
with open('data/xgboost_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Define a function to take user inputs
def user_input(data):
    st.sidebar.header('User Input Parameters')

    # define the month of the year using integers in selectbox
    month = st.sidebar.selectbox('Month', ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August',
                                           'September', 'October', 'November', 'December'])
    # map the month to an integer
    month = data['month'].map({'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 
                                'June': 6, 'July': 7, 'August': 8, 'September': 9, 'October': 10,
                                'November': 11, 'December': 12})
    # define the day of the week 
    day_week = st.sidebar.selectbox('Day of the week', ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])
    # map the day of the week to an integer
    day_week = data['day_week'].map({'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4,
                                    'Saturday': 5, 'Sunday': 6})
    # define the hour of the day
    hour = st.sidebar.selectbox('Hour of the day', data['hour'].unique())
    # define the day of the month
    day_month = st.sidebar.selectbox('Day of the month', data['day_month'].unique())
    # define the 10 minutes interval
    minute = st.sidebar.selectbox('Minute of the hour', data['minute'].unique())
    # define the DWP_TEMP
    LC_DWPTEMP = 7.9
    LC_n=36.7
    # define the LC_RAD (sunshine) using a slider
    LC_RAD = st.sidebar.slider('Solar radiation (W/m2)', min_value=0.0, max_value=871.0, value=0.0, step=0.1)
    # define the temperature using a slider
    LC_TEMP = st.sidebar.slider('Temperature (°C)', min_value=-10.0, max_value=40.0, value=0.0, step=0.1)
    # define the humidity using a slider
    LC_HUMIDITY = st.sidebar.slider('Humidity (%)', min_value=0.0, max_value=99.0, value=0.0, step=0.1)
    # define the windspeed using a slider
    LC_WINDSPEED = st.sidebar.slider('Wind Speed (m/s)', min_value=0.0, max_value=6.31, value=0.5, step=0.1)
    # define the rain using a slider
    LC_RAININ = st.sidebar.slider('Rain Intensity (mm/h)', min_value=0.0, max_value=78.0, value=0.0, step=0.1)
    avg_trucks = st.sidebar.slider('Average Trucks', min_value=data['avg_trucks'].min(), max_value=data['avg_trucks'].max(), value=0.0, step=0.5)
    avg_cars = st.sidebar.slider('Average Cars', min_value=data['avg_cars'].min(), max_value=data['avg_cars'].max(), value=0.0, step=0.5)
    avg_bikes = st.sidebar.slider('Average Bikes', min_value=data['avg_bikes'].min(), max_value=data['avg_bikes'].max(), value=0.0, step=0.5)
    avg_pedestrians = st.sidebar.slider('Average Pedestrians', min_value=data['avg_pedestrians'].min(), max_value=data['avg_pedestrians'].max(), value=0.0, step=0.5)
    v85 = data['v85'].mean()
    Telraam_data = 1
    Weather_data = 1
    # define LC_RAD60
    LC_RAD60 = LC_RAD
    LC_DAILYRAIN = LC_RAININ
    LC_WINDDIR = 0

    # Pack user inputs into a dictionary
    data = {'month': month,
            'day_month': day_month,
            'day_week': day_week,
            'hour': hour,
            'minute': minute,
            'LC_HUMIDITY': LC_HUMIDITY,
            'LC_DWPTEMP': LC_DWPTEMP,
            'LC_n': LC_n,
            'LC_RAD': LC_RAD,
            'LC_RAININ': LC_RAININ,
            'LC_DAILYRAIN': LC_DAILYRAIN,
            'LC_WINDDIR': LC_WINDDIR,
            'LC_WINDSPEED': LC_WINDSPEED,
            'LC_RAD60': LC_RAD60,
            'LC_TEMP': LC_TEMP,
            'avg_trucks': avg_trucks,
            'avg_cars': avg_cars,
            'avg_bikes': avg_bikes,
            'avg_pedestrians': avg_pedestrians,
            'v85': v85,
            'Telraam data': Telraam_data,
            'Weather data': Weather_data
            }

    # Transform the data into a data frame
    features = pd.DataFrame(data, index=[0])
    return features


# Call the function to get user input
input_df = user_input(data)

# Display the app title and user input
st.title('Gradient Boosting Model Explanation App 🌳')
st.write('\n')
#st.subheader('User Input Parameters:')
#st.write(input_df)
st.subheader("Please enter the parameters on the left sidebar and click the button below to see the prediction for the given parameters !")


# Predict and display the output
if st.button("Click here to get the prediction"):
    prediction = model.predict_proba(input_df)
    st.subheader('Prediction:')
    if prediction[0][1] > 0.4:
        st.error('With the given parameters, the probability is high that the sound barrier of 75 dB(A) will be exceeded.')
    else:
        st.success('With the given parameters, the sound barrier of 75 dB(A) will not be exceeded.')

# Add an explanation section (you can expand this with SHAP or LIME-based explanations)
st.subheader('Model Explanation:')
st.markdown("""
    In this section, we can provide a detailed explanation of the Gradient Boosting model. 
""")

# Calculate and display feature importances
plt.figure(figsize=(5, 3))
features = ['Month', 'Day of the month', 'Day of the week', 'Hour of the day', 'Minute of the hour', 'Humidity (%)', 'Dew Point Temperature (°C)', 'Number of measures', 'Solar radiation (W/m2)', 'Rain Intensity (mm/h)', 'Daily Rain Sum (mm)', 'Wind Direction', 'Wind Speed (m/s)', 'Weighted Solar Radiation (W/m2)', 'Temperature (°C)', 'Average Trucks','Average Cars','Average Pedestrians','Average Bikes','v85','Telraam data Present ?','Weather data Present ?']
importances = model.feature_importances_
indices = np.argsort(importances)

sorted_indices = np.argsort(importances)
sorted_importances = importances[sorted_indices]
sorted_features = [features[i] for i in sorted_indices]

fig = go.Figure()
colors = ['lightgreen' if i > 10 else 'lightblue' for i in range(len(sorted_features))]

fig.add_trace(go.Bar(
    x=importances[indices],
    y=[features[i] for i in indices],
    orientation='h',
    marker=dict(
        color=colors,
        line=dict(color='rgba(58, 71, 80, 1.0)', width=3)
    )
))

fig.update_layout(title_text='Feature Importances', title_x=0.5, autosize=False, 
                      width=900, height=700,
                      xaxis_title="Relative Importance", yaxis_title="Features", 
                      template='plotly_white')

st.plotly_chart(fig)
st.write('As you can see the Features that are the most important in determining wether or not a certain sound level is going to be exceeded largely depends on the Solar Radiation, the Hour of the day and Day of the week, but also the average number of cars and pedestrians passing by during that time interval.')