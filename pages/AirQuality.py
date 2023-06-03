import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
import pickle
st.set_page_config(page_title="Air Quality", page_icon="༄", layout='wide', initial_sidebar_state='auto')

@st.cache_data
def load_data():
    df = pd.read_csv("data/model_input.csv", delimiter=";")
    df.drop(['location'],axis=1,inplace=True)
    df = df[df['lceq_avg'] != 0]
    airquality = pd.read_csv("data/Air_Quality.csv", delimiter=",")
    with open('data/xgb_airquality.pkl', 'rb') as f:
        model = pickle.load(f)
    return df, airquality, model
df, airquality, model = load_data()

airquality['time_stamp'] = pd.to_datetime(airquality['time_stamp'])
airquality['month'] = airquality['time_stamp'].dt.month
airquality['day_month'] = airquality['time_stamp'].dt.day
airquality['day_week'] = airquality['time_stamp'].dt.dayofweek.apply(lambda x: 7 if x == 6 else x + 1)  
airquality['hour'] = airquality['time_stamp'].dt.hour
airquality['minute'] = airquality['time_stamp'].dt.minute

merged_df = pd.merge(df, airquality, how='left', on=['month', 'day_month', 'day_week', 'hour', 'minute'])

new_df = merged_df.drop(['lcpeak_avg', 'lceq_avg', 'v85', 'Telraam data', 'avg_pedestrians', 'avg_bikes', 'avg_cars', 'avg_trucks' ], axis=1)

st.title("Air Quality analysis ༄")
st.markdown("In this section, we will analyse the air quality data found in the PurpleAir API. We will start by looking at the data and then we will try to find some correlations between the different variables.")


# Group the data by month and calculate the mean of '2.5_um_count'
grouped_df = new_df.groupby('month')['2.5_um_count'].mean().reset_index()


st.header("Correlation heatmap")
st.markdown("We will start by looking at the correlation heatmap of the different variables. This will give us a first idea of the variables that are somewhat correlated with the count of 2.5um particles.")
columns_of_interest = ['LC_TEMP', 'LC_DAILYRAIN', 'LC_RAD', 'LC_WINDDIR', 'month', '2.5_um_count']
corr_matrix = new_df[columns_of_interest].corr()

# Create the correlation heatmap using Plotly
fig = go.Figure(data=go.Heatmap(
    z=corr_matrix.values,
    x=corr_matrix.columns,
    y=corr_matrix.columns,
    colorscale='RdBu',
    zmin=-1,
    zmax=1,
    colorbar=dict(title="Correlation")
))

# Add custom annotations for the correlation values inside each square
annotations = []
for i, row in enumerate(corr_matrix.values):
    for j, value in enumerate(row):
        annotations.append(
            dict(
                x=corr_matrix.columns[j],
                y=corr_matrix.columns[i],
                text=str(round(value, 2)),
                font=dict(color='white' if abs(value) > 0.5 else 'black'),
                showarrow=False
            )
        )

fig.update_layout(
    title='Correlation Heatmap',
    xaxis_title='Variables',
    yaxis_title='Variables',
    width=800,
    height=600,
    annotations=annotations
)

# Display the plot using Streamlit
st.plotly_chart(fig)


# # # Scatter plot of 2.5_um_count by day 
# st.header("2.5_um_count by day")
# st.markdown("We will now look at the 2.5_um_count by day. We can see that there is a negative correlation between the 2.5_um_count and the day. This means that when the day is higher, the air quality is better.")
# fig = px.scatter(new_df, x="day_month", y="2.5_um_count", trendline="ols",
#                     animation_frame="month", animation_group="day_month", color="day_month",
#                     hover_name="day_month", range_x=[0, 31], range_y=[0, 50])
# fig.update_layout(title='2.5_um_count by day', xaxis_title='Day', yaxis_title='2.5_um_count')
# st.plotly_chart(fig)

# Group the data by month and calculate the average 2.5_um_count per month
monthly_avg = new_df.groupby('month')['2.5_um_count'].mean().reset_index()

# Create the line plot
fig = px.line(monthly_avg, x='month', y='2.5_um_count', color_discrete_sequence=['#3366cc'])

# Update the plot layout and axis labels
fig.update_layout(title='Average 2.5_um_count per Month',
                  xaxis_title='Month', yaxis_title='Average 2.5_um_count')

# Display the plot
st.plotly_chart(fig)

# Scatter plot of 2.5_um_count by LC_TEMP
st.header("2.5_um_count by LC_TEMP")
st.markdown("We will now look at the 2.5_um_count by LC_TEMP. We can see that there is a negative correlation between the 2.5_um_count and the LC_TEMP. This means that when the temperature is higher, the air quality is better.")
fig = px.scatter(new_df, x="LC_TEMP", y="2.5_um_count", trendline="ols", 
                 animation_frame="month", animation_group="day_month", color="day_month",
                 hover_name="day_month", range_x=[-5, 25], range_y=[0, 40])
fig.update_layout(title='2.5_um_count by LC_TEMP', xaxis_title='LC_TEMP', yaxis_title='2.5_um_count')
st.plotly_chart(fig)



merged_df['2.5_um_count'] = merged_df['2.5_um_count'].fillna(method='ffill').rolling(window=10, min_periods=1).mean()
merged_df = merged_df.drop(['time_stamp'], axis=1)
x = merged_df.drop(['2.5_um_count'], axis=1) 
y = merged_df['2.5_um_count']  
xgb = model


st.header("Feature importance")
st.markdown("""We will now look at the feature importance of the different variables. 
The used model is a XGBoost model, with the target variable being the 2.5_um_count. By looking at the feature importance, we can see which variables are the most important in predicting the 2.5_um_count.
            We can see that the most important variables are the temporal data and weather conditions.""")
importance_sorted = sorted(zip(xgb.feature_importances_, x.columns), reverse=True)
importance_values_sorted = [imp for imp, _ in importance_sorted]
variable_names_sorted = [var for _, var in importance_sorted]

fig = px.bar(x=importance_values_sorted, y=variable_names_sorted, orientation='h')

fig.update_layout(
    title='Feature importance',
    xaxis_title='Importance',
    yaxis_title='Variables',
    yaxis=dict(
        tickmode='array',
        ticktext=variable_names_sorted,
        tickvals=variable_names_sorted,
        showticklabels=True,
        automargin=True
    )
)

st.plotly_chart(fig)
