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
st.set_page_config(page_title="Random Forest Model Explanation", page_icon="🌳", layout='wide', initial_sidebar_state='auto')

data = pd.read_csv('data/model_input.csv',delimiter=';')

# Load the model
with open('xgboost_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Define a function to take user inputs
def user_input(data):
    st.sidebar.header('User Input Parameters')

    # define the month of the year using integers in selectbox
    month = st.sidebar.selectbox('Month', data['month'].unique())  
    # define the day of the week
    day_week = st.sidebar.selectbox('Day', data['day_week'].sort_values().unique())
    # define the hour of the day
    hour = st.sidebar.selectbox('Hour', data['hour'].unique())
    # define the day of the month
    day_month = st.sidebar.selectbox('Day of Month', data['day_month'].unique())
    # define the 10 minutes interval
    minute = st.sidebar.selectbox('Minutes', data['minute'].unique())
    # define the DWP_TEMP
    LC_DWPTEMP = 7.9
    LC_n=36.7
    # define the LC_RAD (sunshine) using a slider
    LC_RAD = st.sidebar.slider('LC_RAD', min_value=0.0, max_value=871.0, value=0.0, step=0.1)
    # define the temperature using a slider
    LC_TEMP = st.sidebar.slider('Temperature', min_value=-10.0, max_value=40.0, value=0.0, step=0.1)
    # define the humidity using a slider
    LC_HUMIDITY = st.sidebar.slider('Humidity', min_value=0.0, max_value=99.0, value=0.0, step=0.1)
    # define the windspeed using a slider
    LC_WINDSPEED = st.sidebar.slider('Windspeed', min_value=0.0, max_value=6.31, value=0.5, step=0.1)
    # define the rain using a slider
    LC_RAININ = st.sidebar.slider('Rain', min_value=0.0, max_value=78.0, value=0.0, step=0.1)
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
            'LC_TEMP': LC_TEMP
            }

    # Transform the data into a data frame
    features = pd.DataFrame(data, index=[0])
    return features


# Call the function to get user input
input_df = user_input(data)

# Display the app title and user input
st.title('Random Forest Model Explanation App 🌳')
st.write('\n')
st.subheader('User Input Parameters:')
st.write(input_df)
st.subheader("Please enter the parameters on the left sidebar and click the button below")


# Predict and display the output
if st.button("Show me the prediction !"):
    prediction = model.predict(input_df)
    st.subheader('Prediction:')
    if prediction == 1:
        st.error('With the given parameters, the probability is high that the sound barrier of 75 dB(A) will be exceeded.')
    else:
        st.success('With the given parameters, the sound barrier of 75 dB(A) will not be exceeded.')

# Add an explanation section (you can expand this with SHAP or LIME-based explanations)
st.subheader('Model Explanation:')
st.markdown("""
    In this section, we can provide a detailed explanation of the Random Forest model. 
""")

# Calculate and display feature importances
plt.figure(figsize=(5, 3))
features = ['month', 'day_month', 'day_week', 'hour', 'minute', 'LC_HUMIDITY', 'LC_DWPTEMP', 'LC_n', 'LC_RAD', 'LC_RAININ', 'LC_DAILYRAIN', 'LC_WINDDIR', 'LC_WINDSPEED', 'LC_RAD60', 'LC_TEMP']
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