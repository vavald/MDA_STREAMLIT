import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

noise =  pd.read_csv('data/final_noise_data.csv')

st.set_page_config(page_title="Insights in the Noise dataset", page_icon="🔊", layout='wide', initial_sidebar_state='auto')
st.title('MDA Switzerland - Insights in the Noise dataset')

with st.sidebar:
    st.title('Noise insights')

# GETTING FAMILIAR WITH THE DATA

st.header('Getting familiar with the data')
