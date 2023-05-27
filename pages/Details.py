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
        especially the peaks where some conflict between parties can arise.
        To do this, the given datasets are aggregated to 10 minute intervals, 
        as this is the time we estimate between the noise and the police intervening.""")

st.header('Datasets')

st.markdown("""The two datasets given are the noise dataset on the Naamsestraat and the weather dataset around Leuven.
        There are some factors that are important when dealing with noise, 
        as is also visible when looking at the seperate noise events with given distributions as to what might have caused it.
        Traffic is one of them, where we tried to include traffic counts via Telraam data. 
        """)

st.header('Overview of the process')

st.markdown("""The process started with preprocessing every dataset. This is needed to eliminate some missing values,
        get a clearer view on what the variables are that you will be working with and so on.
        The process afterwards is indicated in both our notebooks (with full code for eg. preprocessing measures)
        and our streamlit applications, in which you are reading right now. 
        The step-by-step guide would be to look at the notebooks 
        and afterwards follow the pages from the streamlit app 
        going from the homepage to more details including the model to more specific insights eg. in noise.""")