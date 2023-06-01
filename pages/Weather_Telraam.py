
import pandas as pd
import numpy as np
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
st.set_page_config(page_title="Weather - Telraam", page_icon="🌞", layout='wide', initial_sidebar_state='auto')

@st.cache_data
def load_data():
    noise = pd.read_csv('data/final_noise_data.csv')
    model =  pd.read_csv('data/model_input.csv', sep=';', index_col=0)
    model = model[model['lcpeak_avg'] != 0]
    return noise, model
noise, model = load_data()

st.title('Insights in the Model Dataset')

import calendar

model['month'] = model['month'].apply(lambda x: calendar.month_name[x])

model['day_week'] = model['day_week'].apply(lambda x: calendar.day_name[x-1])

import plotly.express as px


st.header('Model - Weather dataset 🌞')

st.markdown(
    """
   Below you can see a plot with the sun radiation and noise level per day in one year. 
   The colours represent the noise levels with its corresponding value. 
   The solar radiation increases and the noise levels increase too, especially in May and June.
   Despite the sun radiation in July being higher, the noise levels appear to be lower 
   (eg. people on vacation/no students in Leuven).
   
   In the second semester, although the sun radiation decreases, the noise levels do not follow the same pattern.   
   December has a lower sun radiation than January, 
   however the noise levels are higher (eg. because of Christmas Eve and other holidays).  """
)


# In[ ]:

fig = px.scatter(model, x="day_month", y="LC_RAD60", animation_frame="month", animation_group="lcpeak_avg",
           color="lcpeak_avg", hover_name="lcpeak_avg",
           size_max=55, range_x=[-2,33], range_y=[-45,871],
          title=" Sun radiation and noise level per day in one year")
st.plotly_chart(fig)

# In[ ]:

st.markdown(
    """
   The scatter plot shows us the relationship between Temperature and Noise level per day in one year,
   where the colours respresent the noise levels with their corresponding value. 
   In January and February, both the temperature and the noise levels are high. 
   In March there is a difference in comparison to the first two months of the year:
   the temperature increases as well as the noise levels. 
   This tendecy prevails until June. 
   Despite July having higher temperatures, the noise levels decrease (eg. people are on vacations)/
   Although the temperature decreases after July, we cannot assume that the noise level decreases directly.
   We can distinguish the tendency that the noise level does not change significantly. 
   Noise levels do not excede 80dB (only in a counted number of days). 
"""
)


# In[ ]:

fig = px.scatter(model, x="day_month", y="LC_TEMP", animation_frame="month", animation_group="lcpeak_avg",
         color="lcpeak_avg", hover_name="lcpeak_avg",range_y=[-15,45],
            range_x=[-1,31.5],title=" Temperature vs Noise level per day in one year" )
st.plotly_chart(fig)


# In[ ]:

st.markdown(
    """
    Beneath you can see a plot describing the sun radiation versus the noise level per day, every 10 minutes. 
    This shows us the behaviour of the noise level every day of the week at the same time in intervals of 10 minutes.
    The colours represent the noise levels with their corresponding value. 
 
    Unquestionably, from Monday to Friday as the sun radiation increases with time and the noise levels too.
    However in the weekend (Friday, Saturday and Sunday) we can find higher levels of sun radiation but the noise levels are
    lower than the rest days of the week.
    
    From midnight to 6:10 am, sun radiation is low and the noise too.
    
    Monday to Friday: between 6:40 am and 12:10 pm, the sun radiation increases and the noise too.
                     from 12:12 pm to 4:00 pm , sun radiation increases but noise level not.
                     After 4:pm sun radiation decreases and noise level too.
"""
)


# In[ ]:

# add column hour:minute to noise data
model['10_min_interval_start_time'] = model['hour'].astype(str) + ':' + model['minute'].astype(str)


# In[ ]:

fig = px.scatter(model, x="day_week", y="LC_RAD60", animation_frame="10_min_interval_start_time", animation_group="lcpeak_avg",
           color="lcpeak_avg", hover_name="lcpeak_avg",
           size_max=55, range_x=[-0.5,7.5], range_y=[-45,871],
          title=" Sun radiation vs Noise level per day every 10 minutes")
st.plotly_chart(fig)

# In[ ]:

st.markdown(
    """
     Scatter plot Temperature vs sun radiation every 10 minutes' 
    The colors represent the noise levels with its correspondent value. 
    
   between midnight until 12:10 pm,  we can see that noise level increases as the temperature and 
   the sun radiation increase too.
   However this tendency changes between 12:10 and 12:40 pm, the noise level increases regarless temperature and sun radiation.
   
   After 16:40 hr, as the sun radiation decreases, the noise level also decrease (regardless temperature) 
"""
)


# In[ ]:

fig = px.scatter(model, x="LC_TEMP", y="LC_RAD60", animation_frame="10_min_interval_start_time", animation_group="lcpeak_avg",
           color="lcpeak_avg", hover_name="lcpeak_avg",
           size_max=55, range_x=[-1.5,42], range_y=[-45,871],
          title=" Temperature vs sun radiation every 10 minutes")

st.plotly_chart(fig)

# In[ ]:

st.header('Model - Telraam dataset 🚗')

st.markdown(
    """
    The scatter plot 'Noise level of average cars per day in one month' shows us the noise level produced by
    the average cars per day. 
    The colors represent the noise levels with its correspondent value. 
    
    For example, in the 14th day we can see a noise level of 73.56 dB with a averge of autos of 80. 
    However it is important to note that higher average of autos does not imply higher noise level 
    We can see for example in the 14th day that a noise level of  80,20dB is obtained when the average autos is 41,69.
    Also in the day 27 we can find two picks at the same day with a different number of average autos:
    Noise level of 81 dB when the average autos is 30 and again, noise level of 81,2db when the average autos is 54,47
     
     Therefore, different average autos can offer the same noise level ( in different periods)
"""
)

# In[ ]:

fig = px.scatter(model, x="day_month", y="avg_cars", animation_frame="day_month", animation_group="lcpeak_avg",
           color="lcpeak_avg", hover_name="lcpeak_avg",
           size_max=55, range_x=[-2,33], range_y=[-2,100],
          title=" Noise level of average cars per day in one month")
st.plotly_chart(fig)

st.markdown(
    """
     Scatter plot Noise level of average cars per day every 10 minutes.
     This plot shows us a comparison between the behavior of the noise level and the behavio of the average autos
     every day of the week at the same time in intervals of 10 minutes.
    The colors represent the noise levels with its correspondent value. 
 
    Again, we get that higher average autos does not imply higher levels of noise. 
    However, the time influences the noise level.
    
    at 3:00 am the average autos increases,however the noise levels start to change. In this time we see on Saturday that 
    the average autos is 0 but the noise level is 67.5. Wednesday, Thursday and Friday have a similar condition,
    the average autos for these 3 days stay between 64-66 dB and the average autos is 0. 
    
    at 4:00 am, on Saturday we get a high noise level of 70.1 dB when the average autos is 0..
             Wednesday and Thursday have the same situatio with 68dB and 70dB respectively, when the average autos is 0.
             
    Monday to Friday:
    Between 7:00 am and 7:50 am, the average autos increases and the regular week the noise level 
    increases too. But this increasing is not proportional, again higher average autos does not imply higher noise level.
    
    Between 10:00 am and 12:10 am he average autos increases and the regular week the noise level 
    increases too. These levels are higher than the previous hours.
    
    After 4:00 pm, the noise level decreases.
    
   Saturday and Sunday:
   
   Most of the time, until 7:10 pm, the noise level was "significant" lower than the other days.
   
   However, Friday, Saturday and Sunday at 7:10 pm, we can see that the noise level starts to increase and the 
   average autos is smaller than the afternoon time in the whole week.
"""
)


# In[ ]:

fig = px.scatter(model, x="day_week", y="avg_cars", animation_frame="10_min_interval_start_time", animation_group="lcpeak_avg",
           color="lcpeak_avg", hover_name="lcpeak_avg",
           size_max=55, range_x=[-0.5,8], range_y=[-2,100],
          title=" Noise level of average cars per day every 10 minutes")
st.plotly_chart(fig)
