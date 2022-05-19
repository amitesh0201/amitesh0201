import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

#streamlit run app.py

st.set_page_config(page_title="Dashboard",
                    page_icon=":gorilla:",
                    layout="wide"
)

st.title("Civic Champs Dashboard")

df = pd.read_excel(
    io="Data.xlsx",
    sheet_name="Data",
    engine="openpyxl",
    usecols="A:Q",
    nrows=68609,
)

st.sidebar.header("Options")
organization = st.sidebar.multiselect("Select the Organization",
    options=df.sort_values(by="Organization")["Organization"].unique(),
    default=df.sort_values(by="Organization")["Organization"].unique()
)
year = st.sidebar.multiselect("Select the Year",
    options=df.sort_values(by="Year")["Year"].unique(),
    default=df.sort_values(by="Year")["Year"].unique()
)
month = st.sidebar.multiselect("Select the Month",
    options=df.sort_values(by="Month")["Month"].unique(),
    default=df.sort_values(by="Month")["Month"].unique()
)
day = st.sidebar.multiselect("Select the Day",
    options=df.sort_values(by="Day")["Day"].unique(),
    default=df.sort_values(by="Day")["Day"].unique()
)
df_selection = df.query(
    "Organization == @organization & Year == @year & Month == @month & Day == @day"
)

st.markdown("##")

total_hours = int(df_selection["Hours Volunteered"].sum())
total_users = int(df_selection["User ID"].nunique())
total_activity = int(df_selection["Activity Source"].count())

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Hours Volunteered:")
    st.subheader(f"{total_hours:,}")
with middle_column:
    st.subheader("Users:")
    st.subheader(f"{total_users:,}")
with right_column:
    st.subheader("Activity Count:")
    st.subheader(f"{total_activity:,}")

st.markdown("---")

hours_volunteered_year = (
    df_selection.groupby(by=["Month"]).sum()["Hours Volunteered"]
)
fig1 = px.bar(
    hours_volunteered_year,
    y="Hours Volunteered",
    x=hours_volunteered_year.index,
    title="<b>Hours Volunteered by Year<b>",
    color_discrete_sequence=["#0083B8"] * len(hours_volunteered_year),
)
fig1.update_traces(
    textfont_size=12,
    textangle=0,
    textposition="outside",
    cliponaxis=False
)
fig1.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)

st.plotly_chart(fig1)
