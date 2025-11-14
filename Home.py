import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Home", layout="wide")
st.title("🥨 Elections in Germany")
st.write("Welcome to our app! Here we explore the election results in Germany and different socio-economic parameters over time! \n\nUse the sidebar to navigate to other pages.")

st.markdown("""
            ### Our Results    
            """) 

st.markdown("""
            ##### Income and Election Results
            *⚠️ **Cave** The dataset doesn't mention which parties are considered extreme right and extreme left, these results might vary according to this definition.*
            - The regions with lower income have a tendency to vote more extreme, with left leaning votes up to 2013, and with clear shift towards the right starting 2017
            - AfD gained popularity starting 2017, with massive territory gain in 2025
            - CSU has been very stable over the years in south-east Germany
            - The Greens have been punctually chosen in 2021, mainly in areas with high income, lost popularity again in 2025       

            If you want to see the maps     
            """)
st.page_link("pages/04_Elections_and_Income.py", label="Click here")

st.markdown("""


            """)

st.page_link("pages/06_Information_about_the_parties.py", label="Click here to see information about the German political parties")