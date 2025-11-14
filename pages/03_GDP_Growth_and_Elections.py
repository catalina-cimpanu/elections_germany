import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from urllib.request import urlopen
import json
from copy import deepcopy


# '''
# This is my long comment
# over multiple lines
# '''
@st.cache_data
def load_data(path):
    df = pd.read_csv(path, index_col=0)
    return df

gdp_votes_raw = load_data(path = "data/gdp_votes.csv")
gdp_votes = deepcopy(gdp_votes_raw)

gdp_growth = load_data(path = "data/deu_gdp.csv")
deu_gdp = deepcopy(gdp_growth)

st.title("Analysis of GDP Growth (%) and Vote Share in Germany")
st.header("Dataframes")

if st.checkbox("Show Elections Dataframe"):
    st.subheader("Combined dataset with election data and GDP growth:")
    st.dataframe(data=gdp_votes.set_index("election_year", inplace=False))

if st.checkbox("Show GDP growth Dataframe"):
    st.subheader("GDP growth dataset in Germany over the years:")
    st.dataframe(data=deu_gdp)

raw_gdp_fig = go.Figure()

raw_gdp_fig.add_trace(go.Scatter(
    x=deu_gdp.index,
    y=deu_gdp['gdp_growth'],
    mode='lines+markers',
    name='Germany',
    line=dict(color='royalblue', width=2),
    marker=dict(size=6),
    hovertemplate='Year: %{x}<br>GDP growth: %{y:.2f}%<extra></extra>'
))

# Layout settings
raw_gdp_fig.update_layout(
    title='GDP Growth in Germany Over Time',
    xaxis_title='Year',
    yaxis_title='GDP Growth (%)',
    template='plotly_white',
    hovermode='x unified'
)

with st.expander("Show GDP growth plot"):
    st.plotly_chart(raw_gdp_fig, use_container_width=True)

st.header("Vote Share Trends Across the Years (Nation-Wide)")

left_col, right_col = st.columns([1,1])

party_cols = ['cdu_csu', 'spd_total', 'gruene_total', 'fdp_total', 'afd_total', 'linke_pds_total']

parties = ["All"] + sorted(party_cols)
party = left_col.selectbox("Choose political party", parties)

show_events = right_col.checkbox("Show global crises / major events?", value=False)

events = {
    2008: "Global financial crisis",
    2015: "Migration crisis",
    2020: "COVID-19",
    2022: "Energy & inflation shock"
}

if party == "All":
    reduced_df = gdp_votes
    parties_to_plot = party_cols
else:
    reduced_df = gdp_votes[['election_year', party, 'gdp_growth', 'gdp_growth_lag1']]
    parties_to_plot = [party]


trends_fig = go.Figure()

trends_fig.add_trace(
    go.Bar(
        x=reduced_df['election_year'],
        y=reduced_df['gdp_growth'],
        name="GDP Growth (%)",
        marker_color='lightblue',
        opacity=0.6,
        yaxis="y1"
    )
)

party_colors={
        'cdu_csu':'#003B6F',
        'spd_total':'#A6006B',
        'gruene_total':'#1AA037',
        'fdp_total':'#FFEF00',
        'linke_pds_total':'#E3000F',
        'afd_total':'#0489DB'
    }

for p in parties_to_plot:
    trends_fig.add_trace(
        go.Scatter(
            x=reduced_df['election_year'],
            y=reduced_df[p],
            mode='lines+markers',
            name=p,
            line=dict(color=party_colors.get(p, 'gray')),
            yaxis="y2",
            hovertemplate=(
                f"<b>{p}</b><br>"
                "Year: %{x}<br>"
                "Vote Share: %{y:.2f}%<extra></extra>"
            )
        )
    )


trends_fig.update_layout(
    title="GDP Growth (%) and Party Vote Shares Over Time",
    xaxis=dict(title="Election Year"),
    
    yaxis=dict(
        title="GDP Growth (%)",
        side="left",
        showgrid=False
    ),
    
    yaxis2=dict(
        title="Vote Share (%)",
        overlaying="y",
        side="right"
    ),
    
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="right",
        x=1
    ),
    
    template="plotly_white",
    width=900,
    height=600
)

if show_events:
    for year, label in events.items():
        
        trends_fig.add_vline(
            x=year,
            line_width=1,
            line_dash="dash",
            line_color="gray",
            opacity=0.7
        )
    
    for i, (year, label) in enumerate(events.items()):
        y_pos = 1.00 if i % 2 == 0 else 1.05
        
        trends_fig.add_annotation(
            x=year,
            xref="x",
            y=y_pos,
            yref="paper",
            text=label,
            showarrow=True,
            font=dict(size=10),
            align="center"
        )

trends_fig.update_layout(
    margin=dict(t=110)  
)

st.plotly_chart(trends_fig, use_container_width=True)

st.header("Correlations Vote Share and GDP Growth")

corr_lag2 = {'cdu_csu': 0.7385220348384772,
 'spd_total': 0.07134373387810822,
 'gruene_total': -0.7224423723462742,
 'fdp_total': -0.06053097583137555,
 'linke_pds_total': -0.05243341525474488,
 'afd_total': -0.33560639299721756}

parties = list(corr_lag2.keys())
values = list(corr_lag2.values())
colors = [party_colors[p] for p in parties]

corr_fig = go.Figure(go.Bar(
    x=values,
    y=parties,
    orientation='h',
    marker_color=colors,
    opacity=0.85,
))

corr_fig.update_layout(
    title="Correlation between Vote Share and 2-Year Average GDP Growth",
    xaxis_title="Correlation with gdp_lag2_avg",
    yaxis_title="Political Party",
    width=900,
    height=450,
    template="plotly_white"
)

st.plotly_chart(corr_fig)

with st.expander("Show interpretation of the plot"):
    st.markdown("""
    ### Interpretation of GDP and Party Vote-Share Trends

    **Macroeconomic context (GDP growth)** 
    The blue bars show GDP growth in election years. 
                Strong positive growth in the early 1990s is followed by weaker performance around the early 2000s, 
                a sharp contraction around the 2009 financial crisis, and another large drop in 2020 during the COVID-19 pandemic.
                The subsequent recovery and energy/inflation shock period (around 2022) mark another volatile phase. The last events can be seen more in detail in the GDP growth over the years figure.


    **CDU/CSU and SPD** dominate the vote shares in the 1990s but both exhibit a long-run decline. 
                CDU/CSU experiences temporary recoveries around some crises. SPD declines until the late 2000s, stabilises somewhat, and then shows a partial recovery in the most recent elections.

    **The Greens** show a gradual upward trend over the entire period. 
                Their growth appears to be driven more by other factors (i.e., climate, urban and younger voters) than by the business cycle. **FDP** fluctuates more strongly, with pronounced peaks and pits (e.g. a strong result around 2009 followed by a collapse).
 
   **AfD** enters the party system in the 2010s and gains support in the periods following major crises (migration crisis, COVID-19, energy/inflation shock).
                 Its rise is most pronounced when economic or socio-political uncertainty is high. **Die Linke**, by contrast, peaks around the late 2000s and then steadily declines.

""")