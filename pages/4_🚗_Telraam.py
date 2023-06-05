
import pandas as pd
import numpy as np
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import time
st.set_page_config(page_title="Telraam", page_icon="🚗", layout='wide', initial_sidebar_state='auto')

@st.cache_data
def load_data():
    noise = pd.read_csv('data/final_noise_data.csv')
    model =  pd.read_csv('data/model_input.csv', index_col=0)
    model = model[model['lcpeak_avg'] != 0]
    return noise, model
noise, model = load_data()

st.title('Insights in the Model Dataset')

import calendar

model['month'] = model['month'].apply(lambda x: calendar.month_name[x])

model['day_week'] = model['day_week'].map({1:'Monday', 2:'Tuesday', 3:'Wednesday', 4:'Thursday', 5:'Friday', 6:'Saturday', 7:'Sunday'})
model['day_week'] = pd.Categorical(model['day_week'], categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], ordered=True)
import plotly.express as px


st.header('Model - Telraam dataset 🚗')



# In[ ]:
expander4 = st.expander('NOISE LEVEL VS AVERAGE CAR PER DAY PER MONTH', expanded=False)
expander4.markdown(
    """
    The scatter plot 'Noise level of average cars per day in one year' shows us the noise level produced by
    the average cars everyday in one year.
    We obtained that higher average of cars does not imply higher noise level. One example of this situation occurs 
    19th october, where we can see a noise level of 81 dB with an average of 10 cars 
    and where a noise level of 80dB is obtained when the average cars are 14.
"""
)
fig = px.scatter(model, x="day_month", y="avg_cars", animation_frame="month", animation_group="lcpeak_avg",
           color="lcpeak_avg", hover_name="lcpeak_avg",
           size_max=55, range_x=[-2,33], range_y=[-2,100],
           color_continuous_scale="RdYlGn_r",
          title=" Noise level of average cars per day per month")
fig.update_xaxes(title_text='Day of the Month')
fig.update_yaxes(title_text='Average Number of Cars')
fig.update_coloraxes(colorbar_title='Sound Level')

fig.update_traces(marker=dict(opacity=0.7))

expander4.plotly_chart(fig)


expander5 = st.expander('NOISE LEVEL VS AVERAGE CARS PER DAY', expanded=False)

expander5.markdown(
    """
    Next up is the scatter plot with the noise level of average cars per day every 10 minutes.
    This plot shows us a comparison between the behaviour of the noise level and the behaviour of the average cars,
    every day of the week at the same time in intervals of 10 minutes.
    Again, we get that a higher average of cars does not directly imply higher levels of noise. 
    However, time does influence the noise level.
    
    At 3:00 AM the average amount of cars increases,
    however the noise levels start to change. 
    At this time window, we see on Saturday that the average amount of cars is 0 but the noise level is 67.5. 
    Wednesday, Thursday and Friday have a similar trend and their
    noise levels stay between 64 and 66 dB when the average of cars is 0. 
    Saturday at 4:00 AM, we get a high noise level of 70.1 dB when the average cars is 0.
    Wednesday and Thursday have the same situation with 68 dB and 70 dB respectively, when the average of cars is 0.
             
    Monday to Friday:
    Between 7:00 AM and 7:50 AM, the average of cars increases and in a regular week, the noise levels
    increase too. But this increase is not proportional, again a higher average of cars does not imply higher noise levels.
    After 4:00 PM, the noise level decreases.
    Saturday and Sunday:
    Most of the time, until 7:10 PM, the noise levels were 'significantly' lower than the other days.
   
    However, Friday, Saturday and Sunday at 7:10 PM, we can see that the noise level starts to increase and the 
    average amount of cars driving around is smaller than the afternoon period during the whole week.
    All this can be linked to more weekend-related activities.
"""
)

fig = px.scatter(model.sort_values(["hour","minute",'day_week']), x="day_week", y="avg_cars", animation_frame="hour", animation_group="lcpeak_avg",
           color="lcpeak_avg", hover_name="lcpeak_avg",
           size_max=55,  range_y=[-2,90],
           color_continuous_scale="RdYlGn_r",
           title=" Noise level of average cars per day every 10 minutes")
fig.update_xaxes(title_text='Day of the Week')
fig.update_yaxes(title_text='Average Number of Cars')
fig.update_coloraxes(colorbar_title='Sound Level')

fig.update_traces(marker=dict(opacity=0.7))

expander5.plotly_chart(fig)
