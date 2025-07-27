import streamlit as st
import pandas as pd
import plotly.express as px

# Page setup
st.set_page_config(
    page_title="🔥 Pakistan Heatwave Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🌡️"
)

# Custom CSS
st.markdown("""
<style>
    html, body, .stApp {
        background-color: #0d1117;
        color: white;
    }
    h1, h2, h3, h4 {
        color: white;
    }
    .stTabs [role="tab"] {
        background-color: #161b22;
        color: #fff;
        padding: 10px;
        border-radius: 5px;
        margin-right: 10px;
    }
    .stTabs [role="tab"][aria-selected="true"] {
        background-color: #238636;
    }
    footer {
        text-align: center;
        color: gray;
        margin-top: 4rem;
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("heatwave_pakistan.csv")

try:
    df = load_data()
except:
    st.error("❌ Please upload `heatwave_pakistan.csv` with the required columns.")
    st.stop()

# Sidebar filters
st.sidebar.title("🌍 Filters")
cities = st.sidebar.multiselect("Select Cities", options=sorted(df["City"].unique()), default=sorted(df["City"].unique()))
years = st.sidebar.multiselect("Select Years", options=sorted(df["Year"].unique()), default=sorted(df["Year"].unique()))
filtered_df = df[(df["City"].isin(cities)) & (df["Year"].isin(years))]

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🌡️ Temperature", "🩺 Health", "🌾 Agriculture", "💧 Water"])

# 🌡️ Temperature Tab
with tab1:
    st.header("🌡️ Peak Temperatures")
    fig_temp = px.bar(
        filtered_df,
        x="Year",
        y="Peak_Temp_C",
        color="City",
        barmode="group",
        title="Peak Temperatures (°C) Over Years"
    )
    st.plotly_chart(fig_temp, use_container_width=True)

    st.subheader("📌 Summary")
    col1, col2 = st.columns(2)
    col1.metric("Max Temperature", f"{filtered_df['Peak_Temp_C'].max():.1f} °C")
    col2.metric("Average Temperature", f"{filtered_df['Peak_Temp_C'].mean():.1f} °C")

# 🩺 Health Tab
with tab2:
    st.header("🩺 Health Impacts")
    fig_health = px.bar(
        filtered_df,
        x="City",
        y=["Deaths", "Heatstroke_Cases"],
        barmode="group",
        title="Heatwave Deaths and Heatstroke Cases"
    )
    st.plotly_chart(fig_health, use_container_width=True)

    st.subheader("📌 Summary")
    col1, col2 = st.columns(2)
    col1.metric("Total Deaths", int(filtered_df["Deaths"].sum()))
    col2.metric("Heatstroke Cases", int(filtered_df["Heatstroke_Cases"].sum()))

# 🌾 Agriculture Tab
with tab3:
    st.header("🌾 Agricultural Loss")
    fig_agri = px.bar(
        filtered_df,
        x="City",
        y="Agriculture_Loss_pct",
        color="Year",
        barmode="group",
        title="Agricultural Loss by City & Year (%)"
    )
    st.plotly_chart(fig_agri, use_container_width=True)

    st.subheader("📌 Summary")
    col1, col2 = st.columns(2)
    col1.metric("Max Loss", f"{filtered_df['Agriculture_Loss_pct'].max():.1f}%")
    col2.metric("Avg Loss", f"{filtered_df['Agriculture_Loss_pct'].mean():.1f}%")

# 💧 Water Tab
with tab4:
    st.header("💧 Water Shortage & Duration")
    fig_duration = px.bar(
        filtered_df,
        x="Year",
        y="Duration_Days",
        color="City",
        barmode="group",
        title="Heatwave Duration (Days) Over Years"
    )
    st.plotly_chart(fig_duration, use_container_width=True)

    st.subheader("📌 Summary")
    col1, col2 = st.columns(2)
    col1.metric("Longest Duration", f"{filtered_df['Duration_Days'].max()} Days")
    col2.metric("Avg Duration", f"{filtered_df['Duration_Days'].mean():.1f} Days")

# Footer
st.markdown("<footer>Made with ❤️ by Abrar — 2025</footer>", unsafe_allow_html=True)
