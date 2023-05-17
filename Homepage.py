import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import time

# Load Data
model_input = pd.read_csv("data/model_input.csv",delimiter=";")
df_weather=pd.read_csv('data/Weather_cleaned.csv')
df_meta = pd.read_csv('data/01_Metadata_v2.csv')
# remove rows where lcpeak_avg or lceq_avg is 0
model_input = model_input[model_input['lcpeak_avg'] != 0]
model_input = model_input[model_input['lceq_avg'] != 0]


####################
# Homepage Map
####################
st.title('MDA_Switzerland - Data Science Project 🇨🇭🇨🇭')

# Show data loading progress bar to the user
#progress_text = "Map is being built... Please wait"
#my_bar = st.progress(0, text=progress_text)

#for percent_complete in range(100):
    #time.sleep(0.03)
    #my_bar.progress(percent_complete + 1, text=progress_text)

# showing the html map to he user
st.components.v1.html(open("sensors_map.html", 'r').read(), height=600)

# drop down menu to select a sensor
option = st.selectbox(
    'Which sensor would you like to know more about?',
    ('Please select a sensor','Naamsestraat 35','Naamsestraat 57','Naamsestraat 62','His & Hears','Calvariekapel','Parkstraat 2','Naamsestraat 81','Vrijthof'))

# create a bar chart showing lcpeak_avg by day of week
#st.dataframe(model_input)
