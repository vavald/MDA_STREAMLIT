import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import time
import plotly.graph_objects as go

st.set_page_config(page_title="MDA Switzerland - Data Science Project", page_icon="🇨🇭", layout='wide', initial_sidebar_state='auto')
# Load Data
model_input = pd.read_csv("data/model_input.csv",delimiter=";")
df_weather=pd.read_csv('data/Weather_cleaned.csv')
df_meta = pd.read_csv('data/01_Metadata_v2.csv')
df_noise = pd.read_csv('data/final_noise_data.csv')
# remove rows where lcpeak_avg or lceq_avg is 0
model_input = model_input[model_input['lcpeak_avg'] != 0]
model_input = model_input[model_input['lceq_avg'] != 0]
df_noise['date'] = pd.to_datetime('2022' + '-' + df_noise['month'].astype(str) + '-' + df_noise['day_month'].astype(str) + ' ' + df_noise['10_min_interval_start_time'].astype(str))


####################
# Homepage Map
####################

# Display the app title and user input
st.title('MDA_Switzerland - Data Science Project 🇨🇭')

# Show data loading progress bar to the user
#progress_text = "Map is being built... Please wait"
#my_bar = st.progress(0, text=progress_text)

#for percent_complete in range(100):
    #time.sleep(0.03)
    #my_bar.progress(percent_complete + 1, text=progress_text)

# Add explanation
st.markdown("""In context of a group project related to the Modern Data Analytics course at KU Leuven, 
        a thorough research was conducted on a noise dataset.
        The data was gathered by 8 different sensors located on the main road of Leuven: the Naamsestraat.
        Additionally, some wheather data was introduced, as well as Telraam traffic counts and general air quality of the environments.
        Beneath you will find the geographical locations of the sensors used in the project.
        Because the main ones will be the noise data collectors, 
        an interactive tool was provided to check them out below.""")

st.markdown("""More information concerning the background of the project and the overview of steps
    can be found on the details page. Please refer to this page if you have additional questions.""")

# showing the html map to he user
st.components.v1.html(open("sensors_map.html", 'r').read(), height=600)

# drop down menu to select a sensor
option = st.selectbox('Which sensor would you like to know more about ?',('Please select a sensor','Naamsestraat 35','Naamsestraat 57','Naamsestraat 62','His & Hears','Calvariekapel','Parkstraat 2','Naamsestraat 81','Vrijthof'))

# create button to show bar chart
if st.button('Show Bar Chart'):
    # create a bar chart showing lcpeak_avg where the sensor is selected using plotly.graph_objects
    if option == 'Please select a sensor':
        st.error('Please select a sensor')
    else:
        fig = go.Figure(data=[go.Bar(x=df_noise[df_noise['location'] == option]['date'], y=df_noise[df_noise['location'] == option]['lcpeak_avg'])])
        fig.update_layout(title_text='LCPEAK_AVG for ' + option)
        st.plotly_chart(fig, use_container_width=True)