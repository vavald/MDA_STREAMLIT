import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import time
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="MDA Switzerland - Data Science Project", page_icon="🇨🇭", layout='wide', initial_sidebar_state='auto')

@st.cache_data
def load_data():
    # Load Data
    model_input = pd.read_csv("data/model_input.csv",delimiter=";")
    df_weather=pd.read_csv('data/Weather_cleaned.csv')
    df_meta = pd.read_csv('data/01_Metadata_v2.csv')
    df_noise = pd.read_csv('data/final_noise_data.csv')
    df_noise['hour'] = df_noise['10_min_interval_start_time'].str[:2]
    df_noise['minute'] = df_noise['10_min_interval_start_time'].str[3:5]
    df_noise['date'] = pd.to_datetime(df_noise['year'].astype(str) + '-' + df_noise['month'].astype(str) + '-' + df_noise['day_month'].astype(str) + ' ' + df_noise['hour'].astype(str) + ':' + df_noise['minute'].astype(str), format='%Y-%m-%d %H:%M')

    # remove rows where lcpeak_avg or lceq_avg is 0
    model_input = model_input[model_input['lcpeak_avg'] != 0]
    model_input = model_input[model_input['lceq_avg'] != 0]
    df_noise['date'] = pd.to_datetime('2022' + '-' + df_noise['month'].astype(str) + '-' + df_noise['day_month'].astype(str) + ' ' + df_noise['10_min_interval_start_time'].astype(str))

    return model_input, df_weather, df_meta, df_noise

# Use the function to load data
model_input, df_weather, df_meta, df_noise = load_data()

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

# showing the html map to the user
st.components.v1.html(open("sensors_map.html", 'r').read(), height=600)

# drop down menu to select a sensor
option = st.selectbox('Which sensor would you like to know more about ?',('Please select a sensor','Naamsestraat 35','Naamsestraat 57','Naamsestraat 62','His & Hears','Calvariekapel','Parkstraat 2','Naamsestraat 81','Vrijthof'))
###
df_noise_location = df_noise[df_noise['location'] == option]
date_range = pd.date_range(start='2022-01-01', end='2022-12-31', freq='D')
df_date_range = pd.DataFrame(date_range, columns=['date'])
df_noise_location = pd.merge(df_date_range, df_noise_location, on='date', how='left')


# create button to show bar chart
if st.button('Show Bar Chart'):
    # create a bar chart showing lcpeak_avg where the sensor is selected using plotly.graph_objects
    if option == 'Please select a sensor':
        st.error('Please select a sensor')
    else:

        # Resample your dataframe to get the average lcpeak_avg per day
        df_daily_avg = df_noise_location.resample('D', on='date')['lcpeak_avg'].mean()

        # Calculate 7-day moving average with a minimum of 1 observation
        df_noise_location['lcpeak_avg_smooth'] = df_noise_location['lcpeak_avg'].rolling(window=7, min_periods=1,center=True).mean()

        # Reset index so 'date' becomes a column
        df_noise_location.reset_index(inplace=True)

        # Create a figure with secondary y-axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_trace(
            go.Scatter(x=df_noise_location['date'], y=df_noise_location['lcpeak_avg_smooth'], mode='lines', name='lcpeak_avg_smooth', line_shape='spline'),
            secondary_y=False
        )

        # Get the dates where data is missing
        missing_data_dates = df_daily_avg[df_daily_avg.isna()].index

        # Add vertical red lines for missing dates
        for date in missing_data_dates:
            fig.add_shape(
                type="line",
                xref="x", yref="paper",
                x0=date, y0=0, x1=date, y1=1,
                line=dict(color="tomato", width=4),
                secondary_y=True,
            )

        fig.update_layout(title_text='7-day Rolling Average sound level for ' + option,
        )
        fig.update_yaxes(title_text="Sound Level (dB)", automargin=True)

        st.plotly_chart(fig, use_container_width=True)

# create button to compare two sensors next to the other button
if st.button('Compare with another sensor'):
    # create dropdown menu to select a second sensor
    option2 = st.selectbox('Which sensor would you like to compare with ?',('Please select a sensor','Naamsestraat 35','Naamsestraat 57','Naamsestraat 62','His & Hears','Calvariekapel','Parkstraat 2','Naamsestraat 81','Vrijthof'))

