import streamlit as st

st.set_page_config(page_title="Election Results in Germany and Income in Images", layout="wide")

st.title("Election Results in Germany and Income")
st.markdown("""
            *⚠️ **Cave** The dataset doesn't mention which parties are considered extreme right and extreme left, these results might vary according to this definition.*
            """)

with st.expander("2013"):
    st.image("figures/2013.png", caption="2013")

with st.expander("2017"):
    st.image("figures/2017.png", caption="2017")

with st.expander("2021"):
    st.image("figures/2021.png", caption="2021")

with st.expander("2025"):
    st.image("figures/2025.png", caption="2025")