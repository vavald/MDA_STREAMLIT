import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

df =  pd.read_csv('data/final_noise_data.csv')

st.set_page_config(page_title="Insights in the Noise dataset", page_icon="🔊", layout='wide', initial_sidebar_state='auto')
st.title('MDA Switzerland - Insights in the Noise dataset')

# with st.sidebar:
#     st.title('Noise insights')

# GETTING FAMILIAR WITH THE DATA

st.header('Getting familiar with the data')

# Add explanation
st.markdown("""The noise data consisted of 3 distinctive sets: 
noise levels measured every second, noise events with a probability per type and ... .
To make the analysis a bit more coherent and logical, a aggregation range of 10 minutes was decided on.
This is the time that we expect when residents get aggitated, call the police and the latter arrive on scene.
Let us now look at some initial data concerning the noise levels.""")

# Bar plot of average noise levels by month
# Group the data by month and calculate the average noise levels
avg_noise_by_month = df.groupby('month')['lceq_avg'].mean()
# Create the bar chart using Plotly
fig = go.Figure(data=go.Bar(x=avg_noise_by_month.index, y=avg_noise_by_month.values))
# Set the y-axis range
fig.update_yaxes(range=[56, 62])
# Set labels and title
fig.update_layout(xaxis_title='Month', yaxis_title='Average Noise Level',
                  title='Bar plot of Average Noise Levels by Month')
# Show the plot using Streamlit
st.plotly_chart(fig)

# Add explanation
st.markdown("""Between months, there is not much difference to detect. 
        However, the months February and March appear to be the loudest ones, 
        in contrast to January and July being the quitest months.""")

# # Scatter plot of noise levels by time interval
# # Create a scatter plot using Plotly
# fig = go.Figure(data=go.Scatter(x=df['10_min_interval_start_time'],
#                                y=df['lceq_avg'],
#                                mode='markers'))
# # Set labels and title
# fig.update_layout(xaxis_title='10 Min Interval Start Time',
#                   yaxis_title='Average Noise Level',
#                   title='Scatter Plot of Noise Levels by Time Interval')
# # Show the plot using Streamlit
# st.plotly_chart(fig)



# Create a box plot using Plotly
fig = go.Figure()
fig.add_trace(go.Box(y=df['lceq_avg'], x=df['day_week']))
# Set labels and title
fig.update_layout(xaxis_title='Weekday',
                  yaxis_title='Average Noise Level',
                  title='Box Plot of Noise Levels by Day of the week')
# Show the plot using Streamlit
st.plotly_chart(fig)

# Add explanation
st.markdown("""An obvious remark here is that Sunday has the lowest median and quartiles, but the highest outliers. 
                This is something to consider when working with the data.""")


# SOME MORE CREATIVE FIGURES

st.header('More creative insights')

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


# Noise level with interactive period and location

# Filter the data based on selected location, day of the week, and time range
selected_location = st.selectbox("Select Location", df['location'].unique())
selected_day = st.selectbox("Select Day of the Week", df['day_week'].unique())
start_time = st.selectbox("Select Start Time",
                          options=df[df['day_week'] == selected_day]['10_min_interval_start_time'].unique())
end_time = st.selectbox("Select End Time",
                        options=df[df['day_week'] == selected_day]['10_min_interval_start_time'].unique())

filtered_df = df[(df['location'] == selected_location) &
                 (df['day_week'] == selected_day) &
                 (df['10_min_interval_start_time'].between(start_time, end_time))]

# Calculate the week number based on the selected time range
filtered_df['week_number'] = filtered_df['10_min_interval_start_time'].dt.isocalendar().week

# Group the data by week and calculate the average noise levels for each week
grouped_df = filtered_df.groupby('week_number')['lceq_avg'].mean().reset_index()

# Create a separate line for each week
fig = go.Figure()
for week_number, week_data in grouped_df.groupby('week_number'):
    fig.add_trace(go.Scatter(x=week_data['10_min_interval_start_time'], y=week_data['lceq_avg'],
                             name=f"Week {week_number}", mode='lines'))

# Set labels and title
fig.update_layout(xaxis_title='10 Min Interval Start Time', yaxis_title='Average Noise Level',
                  title=f'Noise Levels on {selected_day} at Location: {selected_location} ({start_time} - {end_time})')

# Show the plot using Streamlit
st.plotly_chart(fig)