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

# REMARK: ADD TITLE TO BAR PLOT 
st.markdown("**Bar Plot of average Noise Levels by month**")

# Bar plot of average noise levels by month
st.bar_chart(df.groupby('month')['lceq_avg'].mean())

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
                  title='Box Plot of Noise Levels by weekday')
# Show the plot using Streamlit
st.plotly_chart(fig)



# SOME MORE CREATIVE FIGURES

st.header('More creative insights')