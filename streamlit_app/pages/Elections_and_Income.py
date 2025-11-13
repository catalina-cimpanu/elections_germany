import streamlit as st
import pandas as pd
import plotly.express as px
import json

st.set_page_config(page_title="Election Results in Germany and Income", layout="wide")

@st.cache_data
def load_data(path, dtype):
    df = pd.read_csv(path, dtype=dtype)
    return df

sorted_elects = load_data(path="../../data/sorted_elects.csv", dtype={"state_code": str, "county": str})
sorted_incomes = load_data(path="../../data/sorted_incomes.csv", dtype={"state_code": str, "code": str})
geojson = json.load(open("../data/georef-germany-kreis.geojson"))

st.title("Election results and income in Germany")

election_years = sorted_elects["election_year"].unique()
income_years = sorted_incomes["year"].unique()

@st.cache_resource
def generate_maps(year):
    elections_winner_fig = px.choropleth_map(
        sorted_elects[sorted_elects["election_year"] == year],
        geojson=geojson,
        locations="county",
        featureidkey="properties.krs_code",
        color="winner",
        hover_name="winner",
        zoom=4.5,
        title="Elected party per district",    
        labels={'winner': 'Winner party'},
        color_discrete_map={
            'cdu':'#003B6F',
            'spd':'#A6006B',
            'gruene':'#1AA037',
            'fdp':'#FFEF00',
            'linke_pds':'#E3000F',
            'afd':'#0489DB'
        },
        # width=900, height=650,
    )
    elections_winner_fig.update_layout(
        title_text="Elected party per district",
        map_center={"lat": 51, "lon": 10},
        autosize=False,
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )

    left_fig = px.choropleth_map(
        sorted_elects[sorted_elects["election_year"] == year],
        geojson=geojson,
        locations="county",
        featureidkey="properties.krs_code",
        color="perc_far_left_w_linke",
        hover_name="county",
        zoom=4.5,
        title="Percentage of people voting far left",
        labels={'perc_far_left_w_linke': 'Votes (%)'},
        color_continuous_scale="Reds", 
        # width=900, height=650,
        range_color=(0, 50)
    )
    left_fig.update_layout(
        map_center={"lat": 51, "lon": 10},
        autosize=False,
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )

    right_fig = px.choropleth_map(
        sorted_elects[sorted_elects["election_year"] == year],
        geojson=geojson,
        locations="county",
        featureidkey="properties.krs_code",
        color="perc_far_right",
        hover_name="county",
        zoom=4.5,
        title="Percentage of people voting far left",
        labels={'perc_far_right': 'Votes (%)'},
        color_continuous_scale="Blues", 
        # width=900, height=650,
        range_color=(0, 50)
    )
    right_fig.update_layout(
        map_center={"lat": 51, "lon": 10},
        autosize=False,
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )

    if year in income_years:
        temp_year = year
    elif year-1 in income_years:
        temp_year = year-1
    elif year-2 in income_years:
        temp_year = year-2
    elif year-3 in income_years:
        temp_year = year-3
    elif year+1 in income_years:
        temp_year = year+1
    elif year+2 in income_years:
        temp_year = year+2
    elif year+3 in income_years:
        temp_year = year+3
    else:
        temp_year = 0

    if temp_year == 0:
        st.write(f"We don't have income data for {year} +/- 3 years.")
        income_fig = None
    else:
        income_fig = px.choropleth_map(
            sorted_incomes[sorted_incomes["year"]==temp_year],
            geojson=geojson,
            locations="code",
            featureidkey="properties.krs_code",
            color="income_per_capita",
            hover_name="region",
            zoom=4.5,
            title="Income",
            labels={'income_per_capita': 'Income \n(TSD Euro)'},
            color_continuous_scale="Purples", 
            # width=900, height=650,
            range_color=(sorted_incomes[sorted_incomes["year"]==temp_year]["income_per_capita"].min(), sorted_incomes[sorted_incomes["year"]==temp_year]["income_per_capita"].max())
        )
        income_fig.update_layout(
            map_center={"lat": 51, "lon": 10},
            autosize=False,
            margin={"r": 0, "t": 0, "l": 0, "b": 0}
        )
    return [elections_winner_fig, income_fig,left_fig, right_fig]

year = st.selectbox("Select the election year: ", election_years[::-1])
if year in income_years:
    temp_year = year
elif year-1 in income_years:
    temp_year = year-1
elif year-2 in income_years:
    temp_year = year-2
elif year-3 in income_years:
    temp_year = year-3
elif year+1 in income_years:
    temp_year = year+1
elif year+2 in income_years:
    temp_year = year+2
elif year+3 in income_years:
    temp_year = year+3
else:
    temp_year = 0


figs = generate_maps(year)

col1, col2 = st.columns(2)

with col1:
    st.subheader(f"Election Results for {year} (per district)")
    st.plotly_chart(figs[0])

with col2:
    st.subheader(f"Income in Thousands of Euros in {year} {"(estimated from marks)" if temp_year<2000 else ""}")
    if figs[1] == None:
        st.write(f"We don't have income data for the year {year}")        
    else:
        st.plotly_chart(figs[1])


st.subheader("Click these if you want to see more")
col3, col4 = st.columns(2)

with col3:
    if st.checkbox(f"Show Extreme Left-Leaning Votes for {year}"):
        # st.subheader("Extreme Left-Leaning Votes")
        st.plotly_chart(figs[2])

with col4:
    if st.checkbox(f"Show Extreme Right-Leaning Votes for {year}"):
        # st.subheader("Extreme Right-Leaning Votes")
        st.plotly_chart(figs[3])