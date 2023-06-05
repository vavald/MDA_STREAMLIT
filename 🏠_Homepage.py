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
    model_input = pd.read_csv("data/model_input.csv")
    df_meta = pd.read_csv('data/01_Metadata_v2.csv')
    df_noise = pd.read_csv('data/final_noise_data.csv')
    df_noise['hour'] = df_noise['10_min_interval_start_time'].str[:2]
    df_noise['minute'] = df_noise['10_min_interval_start_time'].str[3:5]
    df_noise['date'] = pd.to_datetime(df_noise['year'].astype(str) + '-' + df_noise['month'].astype(str) + '-' + df_noise['day_month'].astype(str) + ' ' + df_noise['hour'].astype(str) + ':' + df_noise['minute'].astype(str), format='%Y-%m-%d %H:%M')

    # remove rows where lcpeak_avg or lceq_avg is 0
    model_input = model_input[model_input['lcpeak_avg'] != 0]
    model_input = model_input[model_input['lceq_avg'] != 0]
    df_noise['date'] = pd.to_datetime('2022' + '-' + df_noise['month'].astype(str) + '-' + df_noise['day_month'].astype(str) + ' ' + df_noise['10_min_interval_start_time'].astype(str))

    return model_input, df_meta, df_noise

# Use the function to load data
model_input, df_meta, df_noise = load_data()

# Custom CSS styling for dark mode
css = """
<style>
    .blue-box {
        background-color: #002f5d;
        padding: 20px;
        border-radius: 10px;
        color: #ffffff;
    }

    .blue-box a {
        color: #ffffff;
    }
</style>
"""

# Display the blue box with the content
st.sidebar.markdown(f'<div class="blue-box">{css}<h1>About</h1><p>Web App Url: <a href="https://vavald-mda-streamlit--homepage-7lms53.streamlit.app/">Streamlit</a></p><p>GitHub repository: <a href="https://github.com/vavald/MDA_streamlit">Github</a></p></div>', unsafe_allow_html=True)

####################
# Homepage Map
####################

# Display the app title and user input
st.title('MDA Switzerland - Data Science Project 🇨🇭')

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

# list of sensors without option
sensors2 = ['Please select a sensor','Naamsestraat 35','Naamsestraat 57','Naamsestraat 62','His & Hears','Calvariekapel','Parkstraat 2','Naamsestraat 81','Vrijthof']
# remove the selected sensor from the list
sensors2.remove(option)

# drop down menu with sensors2
option2 = st.selectbox('Which sensor would you like to compare with ?',sensors2)
df_noise_location2 = df_noise[df_noise['location'] == option2]
date_range2 = pd.date_range(start='2022-01-01', end='2022-12-31', freq='D')
df_date_range2 = pd.DataFrame(date_range2, columns=['date'])
df_noise_location2 = pd.merge(df_date_range2, df_noise_location2, on='date', how='left')

# create button to show bar chart
if st.button('Show Bar Chart'):
    # create a bar chart showing lcpeak_avg where the sensor is selected using plotly.graph_objects
    if option == 'Please select a sensor':
        st.error('Please select a sensor in the first drop-down menu')
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
        st.markdown("""As you can see, a lot of data is missing for some of the Noise sensors. 
        The noise sensor at the Calvariekapel has no missing data and sits pretty close to a Telraam Sensor that has data for the year of 2022. 
        This makes the Calvariekapel sensor very interesting for us and thus a good reason to use it as the main sound sensor in our analysis""")


# create button to show both bar charts
if st.button('Show Both Bar Charts'):
    if option == 'Please select a sensor' or option2 == 'Please select a sensor':
        st.error('Please select two sensors')
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
        st.markdown("""As you can see, a lot of data is missing for some of the Noise sensors. 
        The noise sensor at the Calvariekapel has no missing data and sits pretty close to a Telraam Sensor that has data for the year of 2022. 
        This makes the Calvariekapel sensor very interesting for us and thus a good reason to use it as the main sound sensor in our analysis""")

        ########################
        # Resample your dataframe to get the average lcpeak_avg per day
        df_daily_avg2 = df_noise_location2.resample('D', on='date')['lcpeak_avg'].mean()

        # Calculate 7-day moving average with a minimum of 1 observation
        df_noise_location2['lcpeak_avg_smooth'] = df_noise_location2['lcpeak_avg'].rolling(window=7, min_periods=1,center=True).mean()

        # Reset index so 'date' becomes a column
        df_noise_location2.reset_index(inplace=True)

        # Create a figure with secondary y-axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])

        fig.add_trace(
            go.Scatter(x=df_noise_location2['date'], y=df_noise_location2['lcpeak_avg_smooth'], mode='lines', name='lcpeak_avg_smooth', line_shape='spline'),
            secondary_y=False
        )

        # Get the dates where data is missing
        missing_data_dates = df_daily_avg2[df_daily_avg2.isna()].index

        # Add vertical red lines for missing dates
        for date in missing_data_dates:
            fig.add_shape(
                type="line",
                xref="x", yref="paper",
                x0=date, y0=0, x1=date, y1=1,
                line=dict(color="tomato", width=4),
                secondary_y=True,
            )

        fig.update_layout(title_text='7-day Rolling Average sound level for ' + option2,
        )
        fig.update_yaxes(title_text="Sound Level (dB)", automargin=True)

        st.plotly_chart(fig, use_container_width=True)
        


