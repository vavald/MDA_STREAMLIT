import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import calendar
from datetime import datetime
st.set_page_config(page_title="Noise", page_icon="🔊", layout='wide', initial_sidebar_state='auto')

@st.cache_data
def load_data():
    df = pd.read_csv('data/final_noise_data.csv')
    events = pd.read_csv('data/export41.csv')
    return df, events

df, events = load_data()

st.title('Insights in the Noise Dataset 🔊')

# with st.sidebar:
#     st.title('Noise insights')

# GETTING FAMILIAR WITH THE DATA

st.header('Getting familiar with the data')

# Add explanation
st.markdown("""The noise data consisted of 3 distinctive sets: 
        noise levels measured every second raw, processed and noise events with a probability per type.
        To make the analysis a bit more coherent and logical, a aggregation range of 10 minutes was decided on.
        This is the time that we expect when residents get aggitated, call the police and the latter arrive on scene.
        Let us now look at some initial data concerning the noise levels, based on the important parameters from the model.""")

# Add explanation
st.markdown("""Between months, there is not much difference to detect. 
        However, the months February and March appear to be the loudest ones, 
        in contrast to January and July being the quitest months.
        We like to point out that the average noise level peak values have been used in this graph.""")

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
st.markdown("""An obvious remark here is that Sunday has the lowest median and quartiles, but the highest outliers. 
        This is something to consider when using the predictive option on the model page.
        We recommend you to click on the legend items to disable them, eg. when the distribution of the box plots
        is clicked upon, the overall trend becomes more clear when only the mean (red line) is shown.""")

# Define the order of weekdays
weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
# Calculate the mean of lcpeak_avg for each day of the week
mean_lcpeak_avg = df.groupby('day_week')['lcpeak_avg'].mean().reindex(weekday_order).reset_index()
# Create a box plot using Plotly
fig = go.Figure()
fig.add_trace(go.Box(y=df['lcpeak_avg'], x=df['day_week'], name='Distribution per Week Day'))
# Add a red trend line for the mean values
fig.add_trace(go.Scatter(x=mean_lcpeak_avg['day_week'], y=mean_lcpeak_avg['lcpeak_avg'],
                         mode='lines', name='Mean per Week Day', line_shape='spline',line=dict(color='red')))
# Add a white line to indicate the threshold value for the model
# fig.add_shape(type='line', x0='Monday', x1='Sunday', y0=75, y1=75, name="Threshold value", line=dict(color="white"))
# Set labels and title
fig.update_layout(xaxis_title='Weekday',
                  yaxis_title='Average Noise Level Peaks',
                  title='Box Plot of Noise Level Peaks by Day of the Week')
fig.update_layout(width=850, height=450)

# Show the plot using Streamlit
st.plotly_chart(fig)




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
events['result_timestamp'] = pd.to_datetime(events['result_timestamp'],format="%d/%m/%Y %H:%M:%S.%f")
# Select one location with the highest amount of data
location = "MP 01: Naamsestraat 35  Maxim"


# PER MONTH
# Create a dictionary to map month names to month numbers
month_names = list(calendar.month_name)[1:]
# Create a selectbox to select the month
selected_month_name = st.selectbox("Select Month", month_names, index=0, key="month_selectbox")
# Get the corresponding month number
selected_month_number = month_names.index(selected_month_name) + 1
# Filter the data based on the selected month + the correct location
filtered_events = events[events['result_timestamp'].dt.month == selected_month_number]
filtered_events = filtered_events[filtered_events['description'] == location]
# Calculate the distribution of detected noise events classes
class_counts = filtered_events['noise_event_laeq_primary_detected_class'].value_counts()
# Calculate the weighted class counts by multiplying with certainty
weighted_class_counts = class_counts * filtered_events.groupby('noise_event_laeq_primary_detected_class')[
    'noise_event_laeq_primary_detected_certainty'].mean()
# Create a pie chart using Plotly
fig_month = px.pie(weighted_class_counts, values=weighted_class_counts.values, names=weighted_class_counts.index)
# Set the chart title
fig_month.update_layout(title=f"Detected Noise Events Classes Distribution - {selected_month_name}")
# Resize the figure
fig_month.update_layout(width=520, height=400)


# PER WEEKDAY
# Create a list of weekday names
weekday_names = list(calendar.day_name)
# Create a selectbox to select the weekday
selected_weekday_name = st.selectbox("Select Weekday", weekday_names)
# Filter the data based on the selected month + weekday + correct location
filtered_events2 = filtered_events[filtered_events['result_timestamp'].dt.strftime("%A") == selected_weekday_name]
# Calculate the distribution of detected noise events classes
class_counts = filtered_events2['noise_event_laeq_primary_detected_class'].value_counts()
# Calculate the weighted class counts by multiplying with certainty
weighted_class_counts = class_counts * filtered_events2.groupby('noise_event_laeq_primary_detected_class')[
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

 

st.markdown("""To get some more insight in how the data evolves at the exact same time period,
        but over multiple weeks, another graph is provided.
        Please select the location you want to look into, the day of the week you are interested in
        and the time period, given in a normal time format.
        Mind the fact that you can always alter the weeks displayed on the graph 
        by simply clicking on their respective icon in the legend.""")

# Filter the data based on selected location, day of the week, and time range
selected_location = st.selectbox("Select Location", df['location'].unique())
selected_month_names = st.selectbox("Select Month", month_names, index=0, key="month_selectbox2")
selected_month_numb = month_names.index(selected_month_names) + 1
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
                 (df['month'] == selected_month_numb) &
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