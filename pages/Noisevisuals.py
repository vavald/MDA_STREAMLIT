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

# Bar plot of average noise levels by month
st.bar_chart(df.groupby('month')['lceq_avg'].mean())
# Add explanation
st.markdown("Between months, there is not much difference to detect.")

# Scatter plot of noise levels by time interval
# Create a scatter plot using Plotly
fig = go.Figure(data=go.Scatter(x=df['10_min_interval_start_time'],
                               y=df['lceq_avg'],
                               mode='markers'))
# Set labels and title
fig.update_layout(xaxis_title='10 Min Interval Start Time',
                  yaxis_title='Average Noise Level',
                  title='Scatter Plot of Noise Levels by Time Interval')
# Show the plot using Streamlit
st.plotly_chart(fig)

# Create a box plot using Plotly
fig = go.Figure()
fig.add_trace(go.Box(y=df['lceq_avg'], x=df['day_week']))
# Set labels and title
fig.update_layout(xaxis_title='Weekday',
                  yaxis_title='Average Noise Level',
                  title='Box Plot of Noise Levels by Weekday')
# Show the plot using Streamlit
st.plotly_chart(fig)
