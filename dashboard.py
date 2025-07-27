import streamlit as st
import pandas as pd
import plotly.express as px

# 🌡️ Page Configuration
st.set_page_config(page_title="🔥 Pakistan Heatwave Dashboard", layout="wide", page_icon="🌡️")

# 🎨 Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .main-header {
        background-color: #1e293b;
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }

    .main-header h1 {
        font-size: 2.8rem;
        margin: 0;
    }

    .main-header p {
        font-size: 1.1rem;
        color: #cbd5e1;
        margin-top: 0.5rem;
    }

    .chart-container {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 3px 12px rgba(0,0,0,0.05);
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# 📊 Main Header
st.markdown("""
<div class="main-header">
    <h1>🔥 Pakistan Heatwave Dashboard</h1>
    <p>Analyzing temperature, health, agriculture & water crisis (2022–2025)</p>
</div>
""", unsafe_allow_html=True)

# 📂 Load Dataset
df = pd.read_csv("pakistan_heatwave_data.csv")

# 📅 Sidebar Filters
st.sidebar.header("📍 Filter Data")
years = sorted(df['Year'].unique())
cities = sorted(df['City'].unique())

selected_years = st.sidebar.multiselect("Select Years", years, default=years)
selected_cities = st.sidebar.multiselect("Select Cities", cities, default=cities)

filtered_df = df[(df['Year'].isin(selected_years)) & (df['City'].isin(selected_cities))]

# 🧭 Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🌡️ Temperature", "⚕️ Health Impact", "🌾 Agriculture", "💧 Water Crisis"])

# 🌡️ Tab 1: Temperature
with tab1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)

    fig_temp = px.line(filtered_df, x='Year', y='Peak_Temp_C', color='City', markers=True,
                       title="Peak Temperature (°C) Over Years")
    st.plotly_chart(fig_temp, use_container_width=True)

    st.subheader("📈 Temperature Summary")
    col1, col2 = st.columns(2)
    with col1:
        max_temp = filtered_df['Peak_Temp_C'].max()
        hottest = filtered_df.loc[filtered_df['Peak_Temp_C'].idxmax()]
        st.metric("Highest Temperature", f"{max_temp:.1f}°C")
        st.caption(f"in {hottest['City']} ({hottest['Year']})")
    with col2:
        st.metric("Average Peak Temperature", f"{filtered_df['Peak_Temp_C'].mean():.1f}°C")

    st.markdown('</div>', unsafe_allow_html=True)

# ⚕️ Tab 2: Health
with tab2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)

    fig_deaths = px.bar(filtered_df, x='City', y='Deaths', color='Year', barmode='group',
                        title="Heatwave-Related Deaths by City")
    st.plotly_chart(fig_deaths, use_container_width=True)

    st.subheader("🩺 Health Impact Summary")
    col1, col2 = st.columns(2)
    with col1:
        total_deaths = int(filtered_df['Deaths'].sum())
        deadliest = filtered_df.loc[filtered_df['Deaths'].idxmax()]
        st.metric("Total Deaths", total_deaths)
        st.caption(f"Most in {deadliest['City']} ({deadliest['Year']})")
    with col2:
        total_cases = int(filtered_df['Heatstroke_Cases'].sum())
        worst_case = filtered_df.loc[filtered_df['Heatstroke_Cases'].idxmax()]
        st.metric("Heatstroke Cases", total_cases)
        st.caption(f"Most in {worst_case['City']} ({worst_case['Year']})")

    st.markdown('</div>', unsafe_allow_html=True)

# 🌾 Tab 3: Agriculture
with tab3:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)

    fig_agri = px.bar(filtered_df, x='City', y='Agriculture_Loss_pct', color='Year',
                      title="Agriculture Loss (%) by City")
    st.plotly_chart(fig_agri, use_container_width=True)

    st.subheader("🌾 Agriculture Summary")
    col1, col2 = st.columns(2)
    with col1:
        ag_max = filtered_df['Agriculture_Loss_pct'].max()
        ag_city = filtered_df.loc[filtered_df['Agriculture_Loss_pct'].idxmax()]
        st.metric("Max Agriculture Loss", f"{ag_max:.1f}%")
        st.caption(f"in {ag_city['City']} ({ag_city['Year']})")
    with col2:
        st.metric("Average Loss", f"{filtered_df['Agriculture_Loss_pct'].mean():.1f}%")

    st.markdown('</div>', unsafe_allow_html=True)

# 💧 Tab 4: Water Crisis
with tab4:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)

    fig_duration = px.line(filtered_df, x='Year', y='Duration_Days', color='City', markers=True,
                           title="Heatwave Duration (Days) Over Years")
    st.plotly_chart(fig_duration, use_container_width=True)

    fig_water = px.bar(filtered_df, x='City', y='Water_Shortage_Impact', color='Year',
                       title="Water Shortage Impact by City")
    st.plotly_chart(fig_water, use_container_width=True)

    st.subheader("💧 Water & Duration Summary")
    col1, col2 = st.columns(2)
    with col1:
        longest = filtered_df['Duration_Days'].max()
        long_city = filtered_df.loc[filtered_df['Duration_Days'].idxmax()]
        st.metric("Longest Heatwave", f"{longest} days")
        st.caption(f"in {long_city['City']} ({long_city['Year']})")
    with col2:
        st.metric("Average Duration", f"{filtered_df['Duration_Days'].mean():.1f} days")

    st.markdown('</div>', unsafe_allow_html=True)
