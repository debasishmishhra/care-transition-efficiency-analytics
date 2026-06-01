import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Care Transition Analytics", layout="wide")

df = pd.read_excel("HHS_Unaccompanied_Alien_Children_Program.xlsx")

df["Date"] = pd.to_datetime(df["Date"])

st.title("HHS Unaccompanied Alien Children Program Dashboard")

start_date = st.sidebar.date_input(
    "Start Date",
    df["Date"].min()
)

end_date = st.sidebar.date_input(
    "End Date",
    df["Date"].max()
)

filtered = df[
    (df["Date"] >= pd.to_datetime(start_date))
    & (df["Date"] <= pd.to_datetime(end_date))
]

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric(
    "Transfer Efficiency",
    f"{filtered['Transfer Efficiency Ratio'].mean():.2%}"
)

c2.metric(
    "Discharge Effectiveness",
    f"{filtered['Discharge Effectiveness'].mean():.2%}"
)

c3.metric(
    "Avg Backlog",
    round(filtered['Backlog Accumulation'].mean(),2)
)

c4.metric(
    "Max CBP Custody",
    int(filtered['Children in CBP custody'].max())
)

c5.metric(
    "Max HHS Care",
    int(filtered['Children in HHS Care'].max())
)

st.subheader("Care Pipeline Population Trends")

fig1 = px.line(
    filtered,
    x="Date",
    y=["Children in CBP custody","Children in HHS Care"]
)

st.plotly_chart(fig1, use_container_width=True)

st.subheader("Transfer vs Discharge Trends")

fig2 = px.line(
    filtered,
    x="Date",
    y=[
        "Children transferred out of CBP custody",
        "Children discharged from HHS Care"
    ]
)

st.plotly_chart(fig2, use_container_width=True)

st.subheader("Bottleneck Detection")

threshold = st.slider(
    "Backlog Alert Threshold",
    0,
    50,
    10
)

fig3 = px.bar(
    filtered,
    x="Date",
    y="Backlog Accumulation"
)

st.plotly_chart(fig3, use_container_width=True)
