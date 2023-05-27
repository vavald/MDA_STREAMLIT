import streamlit as st

st.set_page_config(page_title="Information", page_icon="ℹ️", layout='wide', initial_sidebar_state='auto')

st.title("Some explanation on the project.")

st.markdown("""In context of the course 'Modern Data Analytics' at the KU Leuven,
        a group project is used as the evaluation criteria.
        The provided data consisted of two large datasets concerning the weather in Leuven
        and noise more narrowly measured along the Naamsestraat.
        What the researchers try to do using this app is making you comfortable with the data,
        providing a simple model to estimate dependencies between variables 
        and giving you some deeper insights using visualisations.
        """)

st.header('Goal')

st.markdown("""The project focuses on the analytics of the noise problem on the Naamsestraat.
        Leuven is a student city, so balancing the vibrant nightlife with the residents' sleep pattern is no sinecure.
        To find peace between both groups, some behavioural ‘nudges’ to reduce noise will be implemented.
        However, to do so it is important to analyse which elements have the most effect on noise.
        The goal of this whole project is to carefully analyse and predict noise, 
        especially the peaks where some conflict between parties can arise.""")

st.header('Datasets')

st.markdown("""
        """)

st.header('Overview of the process')

