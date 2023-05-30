import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import calendar
from datetime import datetime

df =  pd.read_csv('data/final_noise_data.csv')
events = pd.read_csv('data/export41.csv')

st.set_page_config(page_title="Insights in the Noise dataset", page_icon="🔊", layout='wide', initial_sidebar_state='auto')
st.title('Insights in the Noise Dataset')

# with st.sidebar:
#     st.title('Noise insights')



# GETTING FAMILIAR WITH THE DATA

st.header('Getting familiar with the data')

# Add explanation
st.markdown("""The noise data consisted of 3 distinctive sets: 
noise levels measured every second, noise events with a probability per type and ... .
To make the analysis a bit more coherent and logical, a aggregation range of 10 minutes was decided on.
This is the time that we expect when residents get aggitated, call the police and the latter arrive on scene.
Let us now look at some initial data concerning the noise levels, based on the important parameters from the model.""")

# Bar plot of average noise levels by month
# Group the data by month and calculate the average noise levels
avg_noise_by_month = df.groupby('month')['lcpeak_avg'].mean()
# Create the bar chart using Plotly
fig = go.Figure(data=go.Bar(x=avg_noise_by_month.index, y=avg_noise_by_month.values))
# Set the y-axis range
fig.update_yaxes(range=[68, 75])
# Set labels and title
fig.update_layout(xaxis_title='Month', yaxis_title='Average Noise Level Peaks',
                  title='Bar plot of Average Noise Level Peaks by Month')
# Show the plot using Streamlit
st.plotly_chart(fig)

# Add explanation
st.markdown("""Between months, there is not much difference to detect. 
        However, the months February and March appear to be the loudest ones, 
        in contrast to January and July being the quitest months.""")

# # Scatter plot of noise levels by time interval
# # Create a scatter plot using Plotly
# fig = go.Figure(data=go.Scatter(x=df['10_min_interval_start_time'],
#                                y=df['lcpeak_avg'],
#                                mode='markers'))
# # Set labels and title
# fig.update_layout(xaxis_title='10 Min Interval Start Time',
#                   yaxis_title='Average Noise Level',
#                   title='Scatter Plot of Noise Levels by Time Interval')
# # Show the plot using Streamlit
# st.plotly_chart(fig)

# Define the order of weekdays
weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
# Calculate the mean of lcpeak_avg for each day of the week
mean_lcpeak_avg = df.groupby('day_week')['lcpeak_avg'].mean().reindex(weekday_order).reset_index()

# Create a box plot using Plotly
fig = go.Figure()
fig.add_trace(go.Box(y=df['lcpeak_avg'], x=df['day_week'], name='Distribution per Week Day'))

# Add a red trend line for the mean values
fig.add_trace(go.Scatter(x=mean_lcpeak_avg['day_week'], y=mean_lcpeak_avg['lcpeak_avg'],
                         mode='lines', name='Mean per Week Day', line=dict(color='red')))

# Set labels and title
fig.update_layout(xaxis_title='Weekday',
                  yaxis_title='Average Noise Level Peaks',
                  title='Box Plot of Noise Level Peaks by Day of the Week')
fig.update_layout(width=850, height=450)

# Show the plot using Streamlit
st.plotly_chart(fig)


# Add explanation
st.markdown("""An obvious remark here is that Sunday has the lowest median and quartiles, but the highest outliers. 
                This is something to consider when using the predictive option on the model page.""")



# SOME MORE CREATIVE FIGURES

st.header('More creative insights')

st.markdown("""The first thing that we will look into are the seperate noise events that were detected.
        To do this, please select the month that you want to look into or the day of the week.
        Afterwards, the distribution of cases will be shown, 
        while taking into account the uncertainties during the registration.
        What we recommend is clicking on all the transport types in the legend to get them off the graph,
        as these are things that will be difficult to mitigate (sirens) 
        and often happen during the day (passenger car).""")

# NOISE EVENTS

# Convert 'result_timestamp' column to datetime
events['result_timestamp'] = pd.to_datetime(events['result_timestamp'])

# PER MONTH
# Create a dictionary to map month names to month numbers
month_names = list(calendar.month_name)[1:]
# Create a selectbox to select the month
selected_month_name = st.selectbox("Select Month", month_names, index=0)
# Get the corresponding month number
selected_month_number = month_names.index(selected_month_name) + 1
# Filter the data based on the selected month
filtered_events = events[events['result_timestamp'].dt.month == selected_month_number]
# Calculate the distribution of detected noise events classes
class_counts = filtered_events['noise_event_laeq_primary_detected_class'].value_counts()
# Calculate the weighted class counts by multiplying with certainty
weighted_class_counts = class_counts * filtered_events.groupby('noise_event_laeq_primary_detected_class')[
    'noise_event_laeq_primary_detected_certainty'].mean()
# Create a pie chart using Plotly
fig_month = px.pie(weighted_class_counts, values=weighted_class_counts.values, names=weighted_class_counts.index)
# Set the chart title
fig_month.update_layout(title=f"Detected Noise Events Classes Distribution - Month {selected_month_name}")
# Resize the figure
fig_month.update_layout(width=520, height=400)


# PER WEEKDAY
# Create a list of weekday names
weekday_names = list(calendar.day_name)
# Create a selectbox to select the weekday
selected_weekday_name = st.selectbox("Select Weekday", weekday_names)
# Filter the data based on the selected weekday
filtered_events = events[events['result_timestamp'].dt.strftime("%A") == selected_weekday_name]
# Calculate the distribution of detected noise events classes
class_counts = filtered_events['noise_event_laeq_primary_detected_class'].value_counts()
weighted_class_counts = class_counts * filtered_events.groupby('noise_event_laeq_primary_detected_class')[
    'noise_event_laeq_primary_detected_certainty'].mean()
# Create a pie chart using Plotly
fig_weekday = px.pie(weighted_class_counts, values=weighted_class_counts.values, names=weighted_class_counts.index)
# Set the chart title
fig_weekday.update_layout(title=f"Detected Noise Events Classes Distribution - {selected_weekday_name}")
# Resize the figure
fig_weekday.update_layout(width=520, height=400)

# Display the graphs side by side
col1, col2 = st.columns(2)
# Show the pie chart for month in the first column
with col1:
    st.plotly_chart(fig_month)
# Show the pie chart for weekday in the second column
with col2:
    st.plotly_chart(fig_weekday)

    

# REMARK: EDIT THE VALUES ETC BASED ON WHAT SIMULATION YOU WANT TO SHOW

# # Create Streamlit app
# st.markdown("**Sound Level Simulation**")
# # Filter the data
# time_range = st.sidebar.slider("Select Time Range", min_value=0, max_value=24, value=(8, 18))
# filtered_df = df[(df["time"] >= time_range[0]) & (df["time"] <= time_range[1])]
# # Create interactive map using Plotly
# fig = px.scatter_mapbox(filtered_df, lat="latitude", lon="longitude", size="sound_level",
#                         hover_data=["location"], color="sound_level", color_continuous_scale="Viridis",
#                         size_max=15, zoom=13, mapbox_style="carto-positron")

# fig.update_layout(mapbox_center={"lat": filtered_df["latitude"].mean(), "lon": filtered_df["longitude"].mean()})
# # Run the Streamlit app
# st.plotly_chart(fig)


# # Convert result_timestamp column to datetime
# events['result_timestamp'] = pd.to_datetime(events['result_timestamp'])
# # Extract month and day of the week from the result_timestamp
# events['month'] = events['result_timestamp'].dt.month
# events['day_of_week'] = events['result_timestamp'].dt.dayofweek
# # Group the data by month and calculate the count of noise events
# events_per_month = events.groupby('month').size().reset_index(name='count')
# # Create a pie chart for noise events per month
# fig1 = px.pie(events_per_month, names='month', values='count', title='Noise Events per Month')
# # Group the data by day of the week and calculate the count of noise events
# events_per_day_of_week = events.groupby('day_of_week').size().reset_index(name='count')
# # Create a pie chart for noise events per day of the week
# fig2 = px.pie(events_per_day_of_week, names='day_of_week', values='count', title='Noise Events per Day of the Week')
# # Group the data by detected class and calculate the count of noise events
# events_per_detected_class = events.groupby('noise_event_laeq_primary_detected_class').size().reset_index(name='count')
# # Create a pie chart for the distribution of detected class
# fig3 = px.pie(events_per_detected_class, names='noise_event_laeq_primary_detected_class', values='count',
#               title='Distribution of Detected Class')
# # Group the data by detected unit and calculate the count of noise events
# events_per_detected_unit = events.groupby('noise_event_laeq_primary_detected_class_unit').size().reset_index(name='count')
# # Create a pie chart for the distribution of detected unit
# fig4 = px.pie(events_per_detected_unit, names='noise_event_laeq_primary_detected_class_unit', values='count',
#               title='Distribution of Detected Unit')
# # Display the pie charts using Streamlit
# st.plotly_chart(fig1)
# st.plotly_chart(fig2)
# st.plotly_chart(fig3)
# st.plotly_chart(fig4)




st.markdown("""To get some more insight in how the data evolves at the exact same time period,
        but over multiple weeks, another graph is provided.
        Please select the location you want to look into, the day of the week you are interested in
        and the time period, given in a normal time format.
        Mind the fact that you can always alter the weeks displayed on the graph 
        by simply clicking on their respective icon in the legend.""")

# Filter the data based on selected location, day of the week, and time range
selected_location = st.selectbox("Select Location", df['location'].unique())
selected_day = st.selectbox("Select Day of the Week", df['day_week'].unique())
start_time = st.selectbox("Select Start Time",
                          options=df[df['day_week'] == selected_day]['10_min_interval_start_time'].unique())
end_time = st.selectbox("Select End Time",
                        options=df[df['day_week'] == selected_day]['10_min_interval_start_time'].unique())

# Combine relevant columns to create a datetime column
df['datetime'] = pd.to_datetime(df['year'].astype(str) + '-' +
                               df['month'].astype(str) + '-' +
                               df['day_month'].astype(str) + ' ' +
                               df['10_min_interval_start_time'])

# Get the filtered data from the input parameters
filtered_df = df[(df['location'] == selected_location) &
                 (df['day_week'] == selected_day) &
                 (df['10_min_interval_start_time'].between(start_time, end_time))]

# Calculate the week number based on the selected time range
filtered_df['week_number'] = filtered_df['datetime'].dt.isocalendar().week

# Group the data by week and calculate the average noise levels for each week
grouped_df = filtered_df.groupby(['week_number', '10_min_interval_start_time'])['lcpeak_avg'].mean().reset_index()

# Create a separate line for each week
fig = go.Figure()

for week_number, week_data in grouped_df.groupby('week_number'):
    fig.add_trace(go.Scatter(x=week_data['10_min_interval_start_time'], y=week_data['lcpeak_avg'],
                             name=f"Week {week_number}", mode='lines'))

# Set labels and title
fig.update_layout(xaxis_title='Time period', yaxis_title='Average Noise Level',
                  title=f'Noise Levels on {selected_day} at Location: {selected_location} ({start_time} - {end_time})')

# Show the plot using Streamlit
st.plotly_chart(fig)