import pandas as pd
import numpy as np
import matplotlib as plt
import seaborn as sns
import plotly.graph_objects as go
import streamlit as st
import plotly.express as px
from urllib.request import urlopen
import json
from copy import deepcopy

# ─────────────────────────────────────────────
#  STREAMLIT PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(page_title="Germany Elections & Economy", layout="wide")
st.title("Germany: GDP, Unemployment and Federal Election Results")

# ─────────────────────────────────────────────
#  LOAD DATA
# ─────────────────────────────────────────────
election = pd.read_csv('data/federal_muni_harm_25.csv')

gdp_df = pd.read_csv('data/gdp.csv', skiprows=3)
gdp_df = gdp_df.iloc[:, :-1]

# Getting the data for the GDP growth only for Germany 
deu_gdp = gdp_df[gdp_df['Country Code'] == 'DEU']

# Select only the columns containing the years, and create a new dataframe for easy plotting.
year_cols = [col for col in deu_gdp.columns if col.isdigit()]
df_deu = deu_gdp[year_cols].T
df_deu = df_deu.iloc[1:, :]
df_deu.columns = ['gdp_growth']

# Create a new dataframe from df_deu (keep original unchanged)
df_deu_new = df_deu.copy()

# Move index to column
df_deu_new = df_deu_new.reset_index().rename(columns={'index': 'year'})

# Convert year to int
df_deu_new['year'] = df_deu_new['year'].astype(int)

# Filter for years between 1990 and 2025
df_deu_new = df_deu_new[(df_deu_new['year'] >= 1990) & (df_deu_new['year'] <= 2025)]

# ─────────────────────────────────────────────
#  UNEMPLOYMENT DATA
# ─────────────────────────────────────────────
df_unemp_raw = pd.read_csv(
    "data/unemployment.csv",
    sep=";",
    encoding="cp1252",
    skiprows=1,
)
df_unemp = deepcopy(df_unemp_raw)
df_unemp = df_unemp.iloc[2:]
df_unemp.drop(df_unemp.columns[1:5], axis=1, inplace=True)
df_unemp.drop(df_unemp.columns[2:], axis=1, inplace=True)
df_unemp.drop(df_unemp.index[-132:], axis=0, inplace=True)  # rows
df_unemp.columns = ["year", "unemployment_percentage"]

df_unemp["unemployment_percentage"] = (
    df_unemp["unemployment_percentage"]
    .str.replace(",", ".", regex=False)
    .astype(float)
)
df_unemp["year"] = df_unemp["year"].astype(int)

# ─────────────────────────────────────────────
#  PARTY VOTE SHARES
# ─────────────────────────────────────────────
party_cols = ['cdu', 'csu', 'spd', 'gruene', 'fdp', 'linke_pds', 'afd']
for i in party_cols:
    election[f'{i}_total'] = election[i] * election['total_votes']

# Aggregate votes per party and per election year
total_cols = [
    'cdu_total',
    'csu_total',
    'spd_total',
    'gruene_total',
    'fdp_total',
    'linke_pds_total',
    'afd_total',
]

party_sum = election.groupby('election_year')[total_cols].sum()
valid_sum = election.groupby('election_year')['valid_votes'].sum()

df_parties = party_sum.div(valid_sum, axis=0) * 100
df_parties = df_parties.reset_index()

# Since cdu_csu union can also be computed I will add it to the dataframe
df_parties['cdu_csu'] = df_parties['cdu_total'] + df_parties['csu_total']

# ─────────────────────────────────────────────
#  GDP MERGE (for lag etc.)
# ─────────────────────────────────────────────
gdp = df_deu.reset_index()
gdp = gdp.rename(columns={'index': 'election_year'})
gdp['election_year'] = gdp['election_year'].astype(int)

df_merged = df_parties.merge(gdp, on='election_year', how='left')
df_merged = df_merged.sort_values('election_year')
df_merged['gdp_growth_lag1'] = df_merged['gdp_growth'].shift(1)

# ─────────────────────────────────────────────
#  COMMON SETTINGS
# ─────────────────────────────────────────────
party_cols_for_plot = [
    "cdu_csu",
    "spd_total",
    "gruene_total",
    "fdp_total",
    "afd_total",
    "linke_pds_total",
]

legend_names = {
    "cdu_csu": "CDU/CSU",
    "spd_total": "SPD",
    "gruene_total": "Greens",
    "fdp_total": "FDP",
    "afd_total": "AfD",
    "linke_pds_total": "Linke/PDS",
}

party_colors = {
    "cdu_csu": "black",
    "spd_total": "red",
    "gruene_total": "green",
    "fdp_total": "yellow",
    "afd_total": "blue",
    "linke_pds_total": "purple",
}

governments = [
    {"start": 1990, "end": 1994, "coalition": ["cdu_csu", "fdp_total"]},
    {"start": 1994, "end": 1998, "coalition": ["cdu_csu", "fdp_total"]},
    {"start": 1998, "end": 2002, "coalition": ["spd_total", "gruene_total"]},
    {"start": 2002, "end": 2005, "coalition": ["spd_total", "gruene_total"]},
    {"start": 2005, "end": 2009, "coalition": ["cdu_csu", "spd_total"]},
    {"start": 2009, "end": 2013, "coalition": ["cdu_csu", "fdp_total"]},
    {"start": 2013, "end": 2018, "coalition": ["cdu_csu", "spd_total"]},
    {"start": 2018, "end": 2021, "coalition": ["cdu_csu", "spd_total"]},
    {"start": 2021, "end": 2025, "coalition": ["spd_total", "gruene_total", "fdp_total"]},
    {"start": 2025, "end": 2026, "coalition": ["cdu_csu", "spd_total"]},
]

gov_label_map = {
    "cdu_csu": "CDU/CSU",
    "spd_total": "SPD",
    "gruene_total": "Greens",
    "fdp_total": "FDP",
}

events = {
    1990: "1990, Reunification of Germany",
    1997: "1997, Asian financial crisis",
    2001: "2001, 9/11",
    2002: "2002, Introduction of Euro in Germany",
    2004: "2004, Expansion of EU, 10 new countries",
    2008: "2008, Global financial crisis",
    2011: "2011, Eurozone economic crisis",
    2015: "2015, Migration crisis",
    2016: "2016, Brexit",
    2020: "2020, COVID-19",
    2022: "2022, Russian-Ukrainian war",
}

# ─────────────────────────────────────────────
#  FIGURE 1: GDP + PARTY VOTE SHARES
# ─────────────────────────────────────────────
fig = go.Figure()

# GDP Growth Bars (left axis)
fig.add_trace(
    go.Bar(
        x=df_deu_new["year"],
        y=df_deu_new["gdp_growth"],
        name="GDP Growth (%)",
        marker_color="orange",
        opacity=0.65,
        yaxis="y1",
        hovertemplate="<b>GDP Growth</b><br>%{y:.2f}%<extra></extra>",
    )
)

# Party Lines (right axis)
for party in party_cols_for_plot:
    fig.add_trace(
        go.Scatter(
            x=df_merged["election_year"],
            y=df_merged[party],
            mode="lines+markers",
            name=legend_names.get(party, party),
            line=dict(color=party_colors.get(party, "gray")),
            marker=dict(size=16),
            yaxis="y2",
            hovertemplate="<b>%{fullData.name}</b><br>Year: %{x}<br>Vote Share: %{y:.2f}%<extra></extra>",
        )
    )

# Government Period Backgrounds
ymin = df_merged[party_cols_for_plot].min().min()
ymax = df_merged[party_cols_for_plot].max().max()

for g in governments:
    start, end = g["start"], g["end"]
    coalition = g["coalition"]
    n = len(coalition)
    width = (end - start) / n

    # color slices
    for i, party in enumerate(coalition):
        x0 = start + i * width
        x1 = start + (i + 1) * width
        fig.add_vrect(
            x0=x0,
            x1=x1,
            fillcolor=party_colors.get(party),
            opacity=0.62,
            layer="below",
            line_width=0,
        )

    # outer box
    fig.add_vrect(
        x0=start,
        x1=end,
        fillcolor="rgba(0,0,0,0)",
        line_width=4.5,
        line_dash="dash",
        line_color="rgba(120,120,120,0.95)",
        layer="below",
    )

    # coalition label
    label = "<br>".join(gov_label_map[p] for p in coalition)
    fig.add_annotation(
        x=(start + end) / 2,
        xref="x",
        y=1.0,
        yref="paper",
        text=label,
        showarrow=False,
        font=dict(size=11),
        align="center",
        yanchor="bottom",
    )

# Events
for year, text in events.items():
    # fig.add_trace(
    #     go.Scatter(
    #         x=[year, year],
    #         y=[ymin, ymax * 1.1],
    #         mode="lines",
    #         line=dict(color="white", width=1),
    #         showlegend=False,
    #     )
    # )

    fig.add_annotation(
        x=year,
        y=ymin,
        text=f"<b>{text}</b>",
        textangle=-90,
        font=dict(size=12, color="white"),
        showarrow=False,
        xanchor="center",
        yanchor="bottom",
    )

# Layout
fig.update_layout(
    title="GDP Growth (%) and Party Vote Shares with Governments",
    xaxis=dict(title="Election Year"),
    yaxis=dict(  # LEFT AXIS (GDP)
        title="GDP Growth (%)",
        showgrid=False,
        range=[-10, 10],
    ),
    yaxis2=dict(  # RIGHT AXIS
        title="Vote Share (%)",
        overlaying="y",
        side="right",
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.12,
        xanchor="center",
        x=0.5,
        font=dict(size=11),
    ),
    template="plotly_white",
    width=1200,
    height=720,
)

# STREAMLIT OUTPUT FOR FIGURE 1
st.subheader("GDP Growth (%) and Party Vote Shares with Governments")
st.plotly_chart(fig, use_container_width=True)

# ─────────────────────────────────────────────
#  FIGURE 2: UNEMPLOYMENT + PARTY VOTE SHARES
# ─────────────────────────────────────────────
fig = go.Figure()

# Unemployment Bars (left axis)
fig.add_trace(
    go.Bar(
        x=df_unemp["year"],
        y=df_unemp["unemployment_percentage"],
        name="Unemployment (%)",
        marker_color="cyan",
        opacity=0.65,
        yaxis="y1",
        hovertemplate="<b>Unemployment Rate</b><br>%{y:.2f}%<extra></extra>",
    )
)

# Party Lines (right axis)
for party in party_cols_for_plot:
    fig.add_trace(
        go.Scatter(
            x=df_merged["election_year"],
            y=df_merged[party],
            mode="lines+markers",
            name=legend_names.get(party, party),
            line=dict(color=party_colors.get(party, "gray")),
            marker=dict(size=16),
            yaxis="y2",
            hovertemplate="<b>%{fullData.name}</b><br>Year: %{x}<br>Vote Share: %{y:.2f}%<extra></extra>",
        )
    )

# Government Period Backgrounds
ymin = df_merged[party_cols_for_plot].min().min()
ymax = df_merged[party_cols_for_plot].max().max()

for g in governments:
    start, end = g["start"], g["end"]
    coalition = g["coalition"]
    n = len(coalition)
    width = (end - start) / n

    # color slices
    for i, party in enumerate(coalition):
        x0 = start + i * width
        x1 = start + (i + 1) * width
        fig.add_vrect(
            x0=x0,
            x1=x1,
            fillcolor=party_colors.get(party),
            opacity=0.62,
            layer="below",
            line_width=0,
        )

    # outer box
    fig.add_vrect(
        x0=start,
        x1=end,
        fillcolor="rgba(0,0,0,0)",
        line_width=4.5,
        line_dash="dash",
        line_color="rgba(120,120,120,0.95)",
        layer="below",
    )

    # coalition label
    label = "<br>".join(gov_label_map[p] for p in coalition)
    fig.add_annotation(
        x=(start + end) / 2,
        xref="x",
        y=1.0,
        yref="paper",
        text=label,
        showarrow=False,
        font=dict(size=11),
        align="center",
        yanchor="bottom",
    )

# Events
for year, text in events.items():
    # fig.add_trace(
    #     go.Scatter(
    #         x=[year, year],
    #         y=[ymin, ymax * 1.1],
    #         mode="lines",
    #         line=dict(color="white", width=1),
    #         showlegend=False,
    #     )
    # )

    fig.add_annotation(
        x=year,
        y=ymin,
        text=f"<b>{text}</b>",
        textangle=-90,
        font=dict(size=12, color="white"),
        showarrow=False,
        xanchor="center",
        yanchor="bottom",
    )

# Layout
fig.update_layout(
    title="Unemployment (%) and Party Vote Shares with Governments",
    xaxis=dict(title="Election Year"),
    yaxis=dict(  # LEFT AXIS (Unemployment)
        title="Unemployment (%)",
        showgrid=False,
        range=[0, 15],
    ),
    yaxis2=dict(  # RIGHT AXIS
        title="Vote Share (%)",
        overlaying="y",
        side="right",
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.12,
        xanchor="center",
        x=0.5,
        font=dict(size=11),
    ),
    template="plotly_white",
    width=1200,
    height=720,
)

# STREAMLIT OUTPUT FOR FIGURE 2
st.subheader("Unemployment (%) and Party Vote Shares with Governments")
st.plotly_chart(fig, use_container_width=True)