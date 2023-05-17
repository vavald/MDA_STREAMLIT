import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import time
import pickle
import sklearn
from sklearn.ensemble import RandomForestRegressor

st.title('Gradient Boosting Model - Feel free to play around with the parameters 🤪🤪')


# Load the model
with open('xgboost_model.pkl', 'rb') as f:
    model = pickle.load(f)

# Define a function to take user inputs
def user_input():
    st.sidebar.header('User Input Parameters')

    # Define your inputs here. For instance, assuming you have two features 'feature1' and 'feature2'
    feature1 = st.sidebar.slider('Feature 1', min_value=0.0, max_value=10.0, value=5.0, step=0.1)
    feature2 = st.sidebar.slider('Feature 2', min_value=0.0, max_value=10.0, value=5.0, step=0.1)

    # Pack user inputs into a dictionary
    data = {'Feature 1': feature1,
            'Feature 2': feature2}

    # Transform the data into a data frame
    features = pd.DataFrame(data, index=[0])
    return features

# Call the function
input_df = user_input()

# Display user input
st.subheader('User Input Parameters')
st.write(input_df)

# Predict and display the output
prediction = model.predict(input_df)
st.subheader('Prediction')
st.write(prediction)