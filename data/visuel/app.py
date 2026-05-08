import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
df = pd.read_csv("C:/Users/requirements/india.csv")

#df = pd.read_csv("C:\Users\requirements\india.csv")

list_of_states = list(df["State"].unique())
list_of_states.insert(0, 'Overall India')

st.sidebar.title('India Data Visualization')

selected_state = st.sidebar.selectbox('Select the state', list_of_states)
primary = st.sidebar.selectbox('Select a primary parameter', sorted(df.columns[5:]))
secondary = st.sidebar.selectbox('Select a secondary parameter', sorted(df.columns[5:]))

if selected_state == 'Overall India':
    filtered_df = df
else:
    filtered_df = df[df["State"] == selected_state]

plot = px.scatter(
    filtered_df,
    x=primary,
    y=secondary,
    color="State",
    title=f"{primary} vs {secondary} in {selected_state}"
)

st.plotly_chart(plot, use_container_width=True)

st.text('Size represents primary parameter')
st.text('Color represents secondary parameter')

if selected_state == 'Overall India':
    fig = px.scatter_mapbox(
        df,
        lat="Latitude",
        lon="Longitude",
        size=primary,
        color=secondary,
        zoom=4,
        size_max=35,
        mapbox_style="carto-positron",
        hover_name="State"
    )
    st.plotly_chart(fig, use_container_width=True)
