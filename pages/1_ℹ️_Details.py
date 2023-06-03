import streamlit as st

st.set_page_config(page_title="Information", page_icon="ℹ️", layout='wide', initial_sidebar_state='auto')

st.title("Some explanation on the project    ℹ️")

st.markdown("""In context of the course 'Modern Data Analytics' at the KU Leuven,
        a group project is used as the evaluation criteria.
        The provided data consisted of two large datasets concerning the weather in Leuven
        and noise more narrowly measured along the Naamsestraat.
        What the researchers try to do using this app is making you comfortable with the data,
        providing a simple model to estimate dependencies between variables 
        and giving you some deeper insights using visualisations.
        """)

st.header('Goal')

st.markdown("""The project focuses on the analytics of the noise problem on the Naamsestraat.
        Leuven is a student city, so balancing the vibrant nightlife with the residents' sleep pattern is no sinecure.
        To find peace between both groups, some behavioural ‘nudges’ to reduce noise will be implemented.
        However, to do so it is important to analyse which elements have the most effect on noise.
        The goal of this whole project is to carefully analyse and predict noise, 
        especially the peaks where some conflict between parties can arise.
        To do this, the given datasets are aggregated to 10 minute intervals, 
        as this is the time we estimate between the noise and the police intervening.""")

st.header('Datasets')

st.markdown("""The two datasets given are the noise dataset on the Naamsestraat and the weather dataset around Leuven.
        There are some factors that are important when dealing with noise, 
        as is also visible when looking at the seperate noise events with given distributions as to what might have caused it.
        Traffic is one of them, where we tried to include traffic counts via Telraam data. 
        """)

st.markdown("""The first dataset to discuss is the data used for the implemented model. 
        This is a combination of multiple parameters from other datasets, discussed below.
        The used :blue[**model input**] data is preprocessed to get a CSV file with the following parameters:
        location of the sensor, the date (consisting of month and day of the month), the day of the week,
        the time (consisting of the hour and minute), the humidity, the dewpoint temperature, the amount of measures n, 
        the radiation, the rain intensity and the daily rain, the wind direction and speed, the rad60, 
        the average amount of trucs, cars and pedestrians, v85, lceq_avg and lcpeak_avg.
        There are also two columns added to indicate weather and telraam data. 
        """)
st.markdown("""The used :blue[**noise**] data is preprocessed to get a CSV file with the following parameters:
        location of the sensor, date (consisting of year, month and day of the month), the day of the week,
        the starting time of each 10 minute interval, lceq_avg and lcpeak_avg. 
        """)
st.markdown("""The used :blue[**noise events**] data is preprocessed to get a CSV file with the following parameters:
        the object ID, the description of the sensor (location), the timestamp,
        the noise event laeq model ID and unit, the detected certainty and unit and to finish
        the detected class and unit. 
        """)
st.markdown("""The used :blue[**weather**] data is preprocessed to get a CSV file with the following parameters:
        the ID of the sensor, the date (consisting of year, month and day of the month), the day of the week, 
        the starting time of each 10 minute interval, the humidity, the dewpoint temperature, n, the radiation,
        the rain intensity and the daily rain, the wind direction and speed, the rad60 and the temperature.
        """)
st.markdown("""The used :blue[**air quality**] data is preprocessed to get a CSV file with the following parameters:
        a timestamp and the PM2.5 particles count. Monitoring this air quality is important because it is associated with
        respiratory and cardiovascular diseases. The dataset is combined with the noise and weather data to see if there
        is a correlation between the features and the PM2.5 particles count. The sensor gathering the data is located in Sluispark
        in Leuven, which isn't in close proximity to Naamsestraat, which means that the correlation is not susbtantial between
        the noise data and the air quality data. However, through model training with the XGBoost regressor, we identify important features that contribute to predicting the level of PM2.5 such as the date, daily rainfall, wind speed, temperature and other weather parameters.
        These findings suggest that the weather conditions and seasonal patterns play a role in predicting the level of air quality. Other factors such as traffic-related variables show a smaller importance, albeit still influential. 
""")

st.header('Overview of the process')

st.markdown("""The process started with preprocessing every dataset. This is needed to eliminate some missing values,
        get a clearer view on what the variables are that you will be working with and so on.
        The process afterwards is indicated in both our notebooks (with full code for eg. preprocessing measures)
        and our streamlit applications, in which you are reading right now. 
        The step-by-step guide would be to look at the notebooks 
        and afterwards follow the pages from the streamlit app 
        going from the homepage to more details including the model to more specific insights eg. in noise.""")