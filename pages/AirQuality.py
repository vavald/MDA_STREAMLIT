import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px

df = pd.read_csv("data/model_input.csv", delimiter=";")
df.drop(['location'],axis=1,inplace=True)
df = df[df['lceq_avg'] != 0]

airquality = pd.read_csv("data/Air_Quality.csv", delimiter=",")
airquality['time_stamp'] = pd.to_datetime(airquality['time_stamp'])
airquality['month'] = airquality['time_stamp'].dt.month
airquality['day_month'] = airquality['time_stamp'].dt.day
airquality['day_week'] = airquality['time_stamp'].dt.dayofweek.apply(lambda x: 7 if x == 6 else x + 1)  
airquality['hour'] = airquality['time_stamp'].dt.hour
airquality['minute'] = airquality['time_stamp'].dt.minute

merged_df = pd.merge(df, airquality, how='left', on=['month', 'day_month', 'day_week', 'hour', 'minute'])
merged_df.to_csv("merged_df.csv", index=False)

new_df = merged_df.drop(['lcpeak_avg', 'lceq_avg', 'v85', 'Telraam data', 'avg_pedestrians', 'avg_bikes', 'avg_cars', 'avg_trucks' ], axis=1)

st.title("Air Quality analysis")
st.markdown("In this section, we will analyse the air quality data found in the PurpleAir API. We will start by looking at the data and then we will try to find some correlations between the different variables.")

# # Correlation matrix
# st.header("Correlation matrix")
# st.markdown("We will start by looking at the correlation matrix of the different variables. This will give us a first idea of the variables that are correlated.")
# corr = merged_df.corr()
# mask = np.triu(np.ones_like(corr, dtype=bool))
# f, ax = plt.subplots(figsize=(11, 9))
# cmap = sns.diverging_palette(230, 20, as_cmap=True)
# sns.heatmap(corr, mask=mask, cmap=cmap, vmax=1, vmin=-1, center=0, square=True, linewidths=.5, cbar_kws={"shrink": .5})
# st.pyplot(f)

# Group the data by month and calculate the mean of '2.5_um_count'
grouped_df = new_df.groupby('month')['2.5_um_count'].mean().reset_index()

# Correlation heatmap
st.header("Correlation heatmap")
st.markdown("We will start by looking at the correlation heatmap of the different variables. This will give us a first idea of the variables that are somewhat correlated with the count of 2.5um particles.")
columns_of_interest = ['LC_TEMP', 'LC_RAD', 'LC_WINDDIR', '2.5_um_count']
corr_matrix = new_df[columns_of_interest].corr()
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
plt.title('Correlation Heatmap')
plt.xticks(rotation=45)
plt.tight_layout()
st.pyplot(plt.gcf())


# Line plot of 2.5_um_count by month
st.header("2.5_um_count by month")
st.markdown("We will start by looking at the 2.5_um_count by month. We can see that the 2.5_um_count is higher in the winter months than in the summer months. This is probably due to the fact that people are more inside during the winter months and therefore the air quality is worse.")
fig, ax = plt.subplots()
fig.set_size_inches(5, 3)
ax.plot(grouped_df['month'], grouped_df['2.5_um_count'])
ax.set_title('2.5_um_count by month')
ax.set_xlabel('Month')
ax.set_ylabel('2.5_um_count')
st.pyplot(fig)

# Scatter plot of 2.5_um_count by day 
st.header("2.5_um_count by day")
st.markdown("We will now look at the 2.5_um_count by day. We can see that there is a negative correlation between the 2.5_um_count and the day. This means that when the day is higher, the air quality is better.")
fig = px.scatter(new_df, x="day_month", y="2.5_um_count", trendline="ols",
                    animation_frame="month", animation_group="day_month", color="day_month",
                    hover_name="day_month", range_x=[0, 31], range_y=[0, 50])
fig.update_layout(title='2.5_um_count by day', xaxis_title='Day', yaxis_title='2.5_um_count')
st.plotly_chart(fig)


# Scatter plot of 2.5_um_count by LC_TEMP
st.header("2.5_um_count by LC_TEMP")
st.markdown("We will now look at the 2.5_um_count by LC_TEMP. We can see that there is a negative correlation between the 2.5_um_count and the LC_TEMP. This means that when the temperature is higher, the air quality is better.")
fig = px.scatter(new_df, x="LC_TEMP", y="2.5_um_count", trendline="ols", 
                 animation_frame="month", animation_group="day_month", color="day_month",
                 hover_name="day_month", range_x=[-10, 30], range_y=[0, 60])
fig.update_layout(title='2.5_um_count by LC_TEMP', xaxis_title='LC_TEMP', yaxis_title='2.5_um_count')
st.plotly_chart(fig)