
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

model['day_week'] = model['day_week'].map({1:'Monday', 2:'Tuesday', 3:'Wednesday', 4:'Thursday', 5:'Friday', 6:'Saturday', 7:'Sunday'})
model['day_week'] = pd.Categorical(model['day_week'], categories=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], ordered=True)
import plotly.express as px


st.header('Model - Weather dataset 🌞')

expander = st.expander('Sun radiation and noise level per day in one year', expanded=False)

expander.markdown(
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

if False: """"
fig = px.scatter(model, x="day_month", y="LC_RAD60", animation_frame="month", animation_group="lcpeak_avg",
           color="lcpeak_avg", hover_name="lcpeak_avg",
           size_max=55, range_x=[-2,33], range_y=[-45,871],
          title=" Sun radiation and noise level per day in one year")
st.plotly_chart(fig)

fig = px.scatter(model, x="day_month", y="lcpeak_avg", animation_frame="month", animation_group="LC_RAD60",
           color="LC_RAD60", hover_name="lcpeak_avg",
           size_max=100, range_x=[-2,33], range_y=[50,90],
          title=" Sun radiation and noise level per day in one year")
st.plotly_chart(fig)

from sklearn.preprocessing import MinMaxScaler

# normalize the 'lcpeak_avg' column
scaler = MinMaxScaler()
model['lcpeak_avg_norm'] = scaler.fit_transform(model[['lcpeak_avg']])
model['lcpeak_avg_norm'] = model['lcpeak_avg_norm'].clip(0, 1)

fig = px.scatter(model, 
                 x="day_month", 
                 y="LC_RAD60", 
                 animation_frame="month", 
                 animation_group="lcpeak_avg",
                 color="lcpeak_avg", 
                 hover_name="lcpeak_avg",
                 color_continuous_scale=["white", "white"], # Set color scale as white
                 size_max=55, 
                 range_x=[-2,33], 
                 range_y=[-45,871],
                 title=" Sun radiation and noise level per day in one year")

# Add opacity based on normalized 'lcpeak_avg'
fig.update_traces(marker=dict(opacity=model['lcpeak_avg_norm'].tolist()))

st.plotly_chart(fig)

import plotly.graph_objects as go

# Create animation frames
frames = []
for month in model['month'].sort_values().unique():
    filtered_df = model[model['month'] == month]
    frames.append(go.Frame(data=[go.Bar(x=filtered_df['day_month'], y=filtered_df['LC_RAD60'],
                                        marker=dict(color=filtered_df['lcpeak_avg'],
                                                    colorscale='RdYlGn', # 'RdYlGn' stands for Red, Yellow, Green
                                                    cmin=filtered_df['lcpeak_avg'].min(),
                                                    cmax=filtered_df['lcpeak_avg'].max(),
                                                    colorbar=dict(title='Noise Level')))],
                           name=str(month)))  # name the frame with the corresponding month

# Create initial frame
init_data = model[model['month'] == model['month'].sort_values().unique()[0]]
fig = go.Figure(
    data=[go.Bar(x=init_data['day_month'], y=init_data['LC_RAD60'],
                 marker=dict(color=init_data['lcpeak_avg'],
                             colorscale='RdYlGn',
                             cmin=init_data['lcpeak_avg'].min(),
                             cmax=init_data['lcpeak_avg'].max(),
                             colorbar=dict(title='Noise Level')))],
    layout=go.Layout(
        title_text="Sun radiation and noise level per day in one year",
        sliders=[dict(steps=[dict(method='animate',
                                  args=[[frame['name']]],
                                  label=frame['name']) for frame in frames],
                      transition=dict(duration=300, easing='cubic-in-out'))],
        updatemenus=[dict(type="buttons",
                          buttons=[dict(label="Play",
                                        method="animate",
                                        args=[None])])]),
    frames=frames
)

st.plotly_chart(fig)

fig = px.scatter(model, x="day_month", y="LC_RAD60", animation_frame="month", animation_group="lcpeak_avg",
           color="lcpeak_avg", hover_name="lcpeak_avg",
           size_max=55, range_x=[-2,33], range_y=[-45,871],
           color_continuous_scale=["red", "green"],
           title=" Sun radiation and noise level per day in one year")

st.plotly_chart(fig)"""
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

expander.markdown(
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
# create model1 = model where lcpeak_avg !=0
model1 = model[model['LC_TEMP'] != 0]

fig = px.scatter(model1, x="day_month", y="LC_TEMP", animation_frame="month", animation_group="lcpeak_avg",
         color="lcpeak_avg", hover_name="lcpeak_avg",range_y=[-15,45],
         color_continuous_scale="RdYlGn_r",
         range_x=[-1,31.5],title=" Temperature vs Noise level per day in one year" )
fig.update_xaxes(title_text='Day of the Month')
fig.update_yaxes(title_text='Temperature (°C)')
fig.update_coloraxes(colorbar_title='Sound Level')
fig.update_traces(marker=dict(opacity=0.5))
st.plotly_chart(fig)


# In[ ]:

st.markdown(
    """
    Beneath you can see a plot describing the sun radiation versus the noise level per day, every 10 minutes. 
    This shows us the behaviour of the noise level every day of the week at the same time in intervals of 10 minutes.
    The colours represent the noise levels with their corresponding value. 
    Unquestionably, from Monday to Friday when the sun radiation increases with time, the noise levels do too.
    However, in the weekend (Friday, Saturday and Sunday) we can find higher levels of sun radiation, but the noise levels are
    remain lower than the rest of the weekdays.
    
    From midnight to 6:10 AM, sun radiation is logically low and the noise most of the time as well.
    
"""
)


# In[ ]:

# add column hour:minute to noise data
model['10_min_interval_start_time'] = model['hour'].astype(str) + ':' + model['minute'].astype(str)

fig = px.scatter(model.sort_values(["hour","minute",'day_week']), x="day_week", y="LC_RAD60", animation_frame="10_min_interval_start_time", animation_group="lcpeak_avg",
           color="lcpeak_avg", hover_name="lcpeak_avg",
           size_max=55,  range_y=[0,871],
           color_continuous_scale="RdYlGn_r",
          title=" Sun radiation vs Noise level per day every 10 minutes")
fig.update_xaxes(title_text='Day of the Week')
fig.update_yaxes(title_text='Weighted Solar Radiation (W/m2)')
fig.update_coloraxes(colorbar_title='Sound Level')
fig.update_traces(marker=dict(opacity=0.5))
st.plotly_chart(fig)

# In[ ]:

st.markdown(
    """
    The scatter plot of temperature vs sun radiation every 10 minutes is given below.
    The colours represent the noise levels with its correspondent value. 
    
    Between midnight and 12:10 PM, we can see that these three variables increase.
    However, this tendency changes between 12:10 and 12:40 PM, 
    the noise levels increase regardless of temperature and sun radiation.
    After 16:40, the sun radiation and the noise level decreases (regardless of temperature).
    """)


# In[ ]:

fig = px.scatter(model, x="LC_TEMP", y="LC_RAD60", animation_frame="10_min_interval_start_time", animation_group="lcpeak_avg",
           color="lcpeak_avg", hover_name="lcpeak_avg",
           size_max=55, range_x=[-1.5,42], range_y=[-45,871],
           color_continuous_scale="RdYlGn_r",
          title=" Temperature vs sun radiation every 10 minutes")
fig.update_xaxes(title_text='Temperature (°C)')
fig.update_yaxes(title_text='Weighted Solar Radiation (W/m2)')
fig.update_coloraxes(colorbar_title='Sound Level')

fig.update_traces(marker=dict(opacity=0.7))
st.plotly_chart(fig)

# In[ ]:

st.header('Model - Telraam dataset 🚗')

st.markdown(
    """
    The scatter plot 'Noise level of average cars per day in one month' shows us the noise level produced by
    the average cars per day. 
    The colors represent the noise levels with its correspondent value. 
    
    We obtained that higher average of cars does not imply higher noise level. One example of this situation occurs 
    on the 14th day, we can see a noise level of 73.56 dB with an average of 80 cars 
    and a noise level of 80,20 dB is obtained when the average cars are 42.
    Besides, we got that different average car can cause identical noise levels (in different periods).
    On the 27th day of the month, a noise level of 81 dB is found when the average cars have the value of 30 and 54,47.
    
"""
)

# In[ ]:

fig = px.scatter(model, x="day_month", y="avg_cars", animation_frame="day_month", animation_group="lcpeak_avg",
           color="lcpeak_avg", hover_name="lcpeak_avg",
           size_max=55, range_x=[-2,33], range_y=[-2,100],
           color_continuous_scale="RdYlGn_r",
          title=" Noise level of average cars per day in one month")
fig.update_xaxes(title_text='Day of the Month')
fig.update_yaxes(title_text='Average Number of Cars')
fig.update_coloraxes(colorbar_title='Sound Level')

fig.update_traces(marker=dict(opacity=0.7))

st.plotly_chart(fig)

st.markdown(
    """
    Next up is the scatter plot with the noise level of average cars per day every 10 minutes.
    This plot shows us a comparison between the behaviour of the noise level and the behaviour of the average cars,
    every day of the week at the same time in intervals of 10 minutes.
    The colours represent the noise levels with its corresponding values. 
    Again, we get that a higher average of cars does not directly imply higher levels of noise. 
    However, time does influence the noise level.
    
    At 3:00 AM the average amount of cars increases,
    however the noise levels start to change. 
    At this time window, we see on Saturday that the average amount of cars is 0, but the noise level is 67.5. 
    Wednesday, Thursday and Friday have a similar trend and their
    noise levels stay between 64 and 66 dB when the average of cars is 0. 
    Saturday at 4:00 AM, we get a high noise level of 70.1 dB when the average autos is 0.
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

st.plotly_chart(fig)
