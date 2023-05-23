import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

model =  pd.read_csv('data/model_input.csv', sep=';', index_col=0)

model.head()

print(model.info())

model.day_week.unique()

model.month .unique()

### Scatter plot of average cars by day and lcpeak_avg
# Make figure
fig = px.scatter(model, x="day_month", y="avg_cars", animation_frame="day_month", animation_group="lcpeak_avg",
                 color="lcpeak_avg", hover_name="lcpeak_avg",
                 size_max=55, range_x=[-5, 40], range_y=[-5, 100])
# Set title and axis labels
fig.update_layout(title='Average Cars by Day and lcpeak_avg',
                  xaxis_title='Day',
                  yaxis_title='Average Cars')
# Show the plot using Streamlit
st.plotly_chart(fig)

### Scatter plot of lcpeak_avg by month
# Make figure
fig = px.scatter(model, x="month", y="lcpeak_avg", animation_frame="month", animation_group="lcpeak_avg",
                 color="lcpeak_avg", hover_name="lcpeak_avg", range_x=[0, 13])
# Set title and axis labels
fig.update_layout(title='lcpeak_avg by Month',
                  xaxis_title='Month',
                  yaxis_title='lcpeak_avg')
# Show the plot using Streamlit
st.plotly_chart(fig)


# Scatter plot of LC_WINDSPEED by day and month
fig = px.scatter(model, x="day_month", y="LC_WINDSPEED", animation_frame="month", animation_group="LC_WINDSPEED",
                 color="LC_WINDSPEED", hover_name="LC_WINDSPEED", size_max=55, range_x=[0, 13])
# Set title and axis labels
fig.update_layout(title='LC_WINDSPEED by Day and Month',
                  xaxis_title='Day',
                  yaxis_title='LC_WINDSPEED')
# Show the plot using Streamlit
st.plotly_chart(fig)


# Bar chart of avg_trucks by month
fig = px.bar(model, x="month", y="avg_trucks", color="lcpeak_avg",
             animation_frame="month", animation_group="lcpeak_avg", range_x=[-10, 15])
# Set title and axis labels
fig.update_layout(title='Average Trucks by Month',
                  xaxis_title='Month',
                  yaxis_title='Average Trucks')
# Show the plot using Streamlit
st.plotly_chart(fig)


# Scatter plot of lcpeak_avg by LC_DWPTEMP
fig = px.scatter(model, x="LC_DWPTEMP", y="lcpeak_avg", animation_frame="month", animation_group="lcpeak_avg",
                 color="lcpeak_avg", hover_name="lcpeak_avg", size_max=55, range_x=[-20, 30], range_y=[25, 90])
# Set title and axis labels
fig.update_layout(title='lcpeak_avg by LC_DWPTEMP',
                  xaxis_title='LC_DWPTEMP',
                  yaxis_title='lcpeak_avg')
# Show the plot using Streamlit
st.plotly_chart(fig)


# Bar chart of lcpeak_avg by LC_DWPTEMP
fig = px.bar(model, x="LC_DWPTEMP", y="lcpeak_avg", color="lcpeak_avg",
             animation_frame="month", animation_group="LC_DWPTEMP", range_y=[0, 137])
# Set title and axis labels
fig.update_layout(title='lcpeak_avg by LC_DWPTEMP',
                  xaxis_title='LC_DWPTEMP',
                  yaxis_title='lcpeak_avg')
# Show the plot using Streamlit
st.plotly_chart(fig)


# px.scatter(model, x="day_month", y="avg_cars", animation_frame="day_month", animation_group="lcpeak_avg",
#            color="lcpeak_avg", hover_name="lcpeak_avg",
#            size_max=55, range_x=[-5,40], range_y=[-5,100])

# px.scatter(model, x="month", y="lcpeak_avg", animation_frame="month", animation_group="lcpeak_avg",
#          color="lcpeak_avg", hover_name="lcpeak_avg",
#             range_x=[0,13])

# px.scatter(model, x="day_month", y="LC_WINDSPEED", animation_frame="month", animation_group="LC_WINDSPEED",
#          color="LC_WINDSPEED", hover_name="LC_WINDSPEED",
#             size_max=55, range_x=[0,13])

# fig = px.bar(model, x="month", y="avg_trucks", color="lcpeak_avg",
#   animation_frame="month", animation_group="lcpeak_avg",range_x=[-10,15])
# fig.show()

# px.scatter(model, x="LC_DWPTEMP", y="lcpeak_avg", animation_frame="month", animation_group="lcpeak_avg",
#            color="lcpeak_avg", hover_name="lcpeak_avg",
#            size_max=55, range_x=[-20,30], range_y=[25,90])

# fig = px.bar(model, x="LC_DWPTEMP", y="lcpeak_avg", color="lcpeak_avg",
#   animation_frame="month", animation_group="LC_DWPTEMP", range_y=[0,137])
# fig.show()
