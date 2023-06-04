
import pandas as pd
import numpy as np
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
st.set_page_config(page_title="Weather", page_icon="🌞", layout='wide', initial_sidebar_state='auto')

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

model['day_week'] = model['day_week'].map({1:'Monday', 2:'Tuesday', 3:'Wednesday', 4:'Thursday', 5:'Friday', 6:'Saturday', 7:'Sunday'})
model['day_week'] = pd.Categorical(model['day_week'], categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], ordered=True)
import plotly.express as px


st.header('Model - Weather dataset 🌞')

expander = st.expander('SUN RADIATION AND NOISE LEVEL PER DAY IN ONE YEAR', expanded=False)

expander.markdown(
    """
   Below you can see a plot with the sun radiation and noise level per day in one year. 
   The colours represent the noise levels with its corresponding values. 
   The solar radiation increases and the noise levels increase too, especially in May and June.
   Despite the sun radiation in July being higher, the noise levels appear to be lower 
   (eg. people on vacation/no students in Leuven).
  In the second semester, although the sun radiation decreases, the noise levels do not follow the same pattern.
     December has a lower sun radiation than January but the noise levels are higher (eg. because of Christmas Eve and other holidays)
     """
)
#################
fig = px.scatter(model, x="day_month", y="LC_RAD60", animation_frame="month", animation_group="lcpeak_avg",
           color="lcpeak_avg", hover_name="lcpeak_avg",
           size_max=55, range_x=[-2,33], range_y=[-45,871],
           color_continuous_scale="RdYlGn_r",
           title=" Sun radiation and noise level per day in one year")
fig.update_xaxes(title_text='Day of the Month')
fig.update_yaxes(title_text='Weighted Solar Radiation (W/m2)')
fig.update_coloraxes(colorbar_title='Sound Level')
fig.update_traces(marker=dict(opacity=0.5))

expander.plotly_chart(fig)
#####################




# In[ ]:
# create model1 = model where lcpeak_avg !=0
expander2 = st.expander('TEMPERATURE VS NOISE LEVEL PER DAY IN ONE YEAR', expanded=False)
model1 = model[model['LC_TEMP'] != 0]

fig = px.scatter(model1, x="day_month", y="LC_TEMP", animation_frame="month", animation_group="lcpeak_avg",
         color="lcpeak_avg", hover_name="lcpeak_avg",range_y=[-15,45],
         color_continuous_scale="RdYlGn_r",
         range_x=[-1,31.5],title=" Temperature vs Noise level per day in one year" )
fig.update_xaxes(title_text='Day of the Month')
fig.update_yaxes(title_text='Temperature (°C)')
fig.update_coloraxes(colorbar_title='Sound Level')
fig.update_traces(marker=dict(opacity=0.5))

expander2.markdown(
    """
   The scatter plot shows us the relationship between Temperature and Noise level per day in one year,
   where the colours respresent the noise levels with their corresponding values. 
   In January and February, both the temperature and the noise levels are high. 
   In March there is a difference in comparison to the first two months of the year:
   the temperature increases as well as the noise levels. 
   This tendency prevails until June. 
   Despite July having higher temperatures, the noise levels decrease (eg. people are on vacations).
   Although the temperature decreases after July, we do not assume that the noise level decreases directly.
   We can distinguish the tendency that the noise level does not change significantly. 
"""
)
expander2.plotly_chart(fig)


# In[ ]:


# add column hour:minute to noise data
model['10_min_interval_start_time'] = model['hour'].astype(str) + ':' + model['minute'].astype(str)
expander3 = st.expander('SUN RADIATION VS NOISE LEVEL PER DAY EVERY 10 MINUTES', expanded=False)

expander3.markdown(
    """
    Beneath you can see a plot describing the sun radiation versus the noise level per day, every 10 minutes. 
    This shows us the behaviour of the noise level every day of the week at the same time in intervals of 10 minutes. 
    From Monday to Friday, when the sun radiation increases over time, the noise levels do too.
    However, in the weekend (Friday, Saturday and Sunday) we can find higher levels of sun radiation, but the noise levels do
    remain lower than the rest of the weekdays.
    
    From midnight to 6:10 AM, sun radiation is logically low and the noise most of the time as well.
    
"""
)

fig = px.scatter(model.sort_values(["hour","minute",'day_week']), x="day_week", y="LC_RAD60", animation_frame="10_min_interval_start_time", animation_group="lcpeak_avg",
           color="lcpeak_avg", hover_name="lcpeak_avg",
           size_max=55,  range_y=[0,871],
           color_continuous_scale="RdYlGn_r",
          title=" Sun radiation vs Noise level per day every 10 minutes")
fig.update_xaxes(title_text='Day of the Week')
fig.update_yaxes(title_text='Weighted Solar Radiation (W/m2)')
fig.update_coloraxes(colorbar_title='Sound Level')
fig.update_traces(marker=dict(opacity=0.5))
expander3.plotly_chart(fig)




expander4 = st.expander('TEMPERATURE VS SUN RADIATION VS SOUND LEVEL OVER THE YEAR', expanded=False)
expander4.markdown(
    """
    The scatter plot of temperature vs sun radiation every 10 minutes is given below.
    Between midnight and 12:10 PM, we can see that these three variables increase.
    However, this tendency changes between 12:10 and 12:40 PM.
    After 16:40, the sun radiation and the noise level decrease (regardless of temperature).
    """)
fig = px.scatter(model, x="LC_TEMP", y="LC_RAD60", animation_frame="10_min_interval_start_time", animation_group="lcpeak_avg",
           color="lcpeak_avg", hover_name="lcpeak_avg",
           size_max=55, range_x=[-1.5,42], range_y=[-45,871],
           color_continuous_scale="RdYlGn_r",
          title=" Temperature vs sun radiation every 10 minutes")
fig.update_xaxes(title_text='Temperature (°C)')
fig.update_yaxes(title_text='Weighted Solar Radiation (W/m2)')
fig.update_coloraxes(colorbar_title='Sound Level')

fig.update_traces(marker=dict(opacity=0.7))
expander4.plotly_chart(fig)
