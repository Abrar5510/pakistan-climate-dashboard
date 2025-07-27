import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(
    page_title="🔥 Pakistan Heatwave Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🌡️"
)

# Custom CSS
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500&display=swap');
        html, body, [class*="css"] {
            font-family: 'Orbitron', sans-serif;
            background-color: #0d1117;
            color: white;
        }
        .chart-container {
            background-color: #161b22;
            padding: 1.5em;
            margin: 1em 0;
            border-radius: 10px;
            box-shadow: 0 0 15px rgba(0,0,0,0.3);
        }
        .metric-container {
            background-color: #1f2937;
            padding: 1em;
            border-radius: 8px;
            text-align: center;
        }
        .stTabs [data-baseweb="tab-list"] {
            background-color: #1f2937;
            border-radius: 8px;
        }
        .stTabs [data-baseweb="tab"] {
            color: white;
        }
        footer {
            text-align: center;
            margin-top: 3em;
            color: #888;
            font-size: 0.9em;
        }
    </style>
""", unsafe_allow_html=True)

# Load Data
@st.cache_data
def load_data():
    return pd.read_csv("/mnt/data/heatwave_pakistan.csv")

df = load_data()

# Sidebar Filters
st.sidebar.header("🔍 Filter Data")
selected_city = st.sidebar.multiselect("Select Cities", options=df["City"].unique(), default=list(df["City"].unique()))
selected_year = st.sidebar.multiselect("Select Years", options=df["Year"].unique(), default=list(df["Year"].unique()))
filtered_df = df[(df["City"].isin(selected_city)) & (df["Year"].isin(selected_year))]

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🌡️ Temperature", "🩺 Health", "🌾 Agriculture", "💧 Water Crisis"])

with tab1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("🌡️ Temperature Trends")
    fig_temp = px.bar(
        filtered_df,
        x='Year',
        y='Peak_Temp_C',
        color='City',
        barmode='group',
        title="Peak Temperature (°C) Over Years"
    )
    st.plotly_chart(fig_temp, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.subheader("📈 Temperature Summary")
    col1, col2 = st.columns(2)
    with col1:
        max_temp = filtered_df['Peak_Temp_C'].max()
        hottest = filtered_df.loc[filtered_df['Peak_Temp_C'].idxmax()]
        st.metric("Highest Temperature", f"{max_temp:.1f}°C")
        st.caption(f"in {hottest['City']} ({hottest['Year']})")
    with col2:
        st.metric("Average Peak Temperature", f"{filtered_df['Peak_Temp_C'].mean():.1f}°C")

with tab2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("🩺 Health Impact")
    fig_health = px.bar(
        filtered_df,
        x='City',
        y=['Deaths', 'Heatstroke_Cases'],
        barmode='group',
        title="Health Impact by City"
    )
    st.plotly_chart(fig_health, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.subheader("🩺 Health Impact Summary")
    col1, col2 = st.columns(2)
    with col1:
        total_deaths = int(filtered_df['Deaths'].sum())
        st.metric("Total Deaths", total_deaths)
        deadliest = filtered_df.loc[filtered_df['Deaths'].idxmax()]
        st.caption(f"Most in {deadliest['City']} ({deadliest['Year']})")
    with col2:
        total_cases = int(filtered_df['Heatstroke_Cases'].sum())
        st.metric("Heatstroke Cases", total_cases)
        worst_case = filtered_df.loc[filtered_df['Heatstroke_Cases'].idxmax()]
        st.caption(f"Most in {worst_case['City']} ({worst_case['Year']})")

with tab3:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("🌾 Agricultural Loss")
    fig_agri = px.bar(
        filtered_df,
        x='City',
        y='Agriculture_Loss_pct',
        color='Year',
        barmode='group',
        title="Agricultural Loss (%) by City and Year"
    )
    st.plotly_chart(fig_agri, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.subheader("🌾 Agriculture Summary")
    col1, col2 = st.columns(2)
    with col1:
        ag_max = filtered_df['Agriculture_Loss_pct'].max()
        ag_city = filtered_df.loc[filtered_df['Agriculture_Loss_pct'].idxmax()]
        st.metric("Max Agriculture Loss", f"{ag_max:.1f}%")
        st.caption(f"in {ag_city['City']} ({ag_city['Year']})")
    with col2:
        st.metric("Average Loss", f"{filtered_df['Agriculture_Loss_pct'].mean():.1f}%")

with tab4:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("💧 Heatwave Duration & Water Shortage")
    fig_duration = px.bar(
        filtered_df,
        x='Year',
        y='Duration_Days',
        color='City',
        barmode='group',
        title="Heatwave Duration (Days) Over Years"
    )
    st.plotly_chart(fig_duration, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.subheader("💧 Water & Duration Summary")
    col1, col2 = st.columns(2)
    with col1:
        longest = filtered_df['Duration_Days'].max()
        long_city = filtered_df.loc[filtered_df['Duration_Days'].idxmax()]
        st.metric("Longest Heatwave", f"{longest} days")
        st.caption(f"in {long_city['City']} ({long_city['Year']})")
    with col2:
        st.metric("Average Duration", f"{filtered_df['Duration_Days'].mean():.1f} days")

# Footer
st.markdown("<footer>Made with ❤️ by Abrar • 2025</footer>", unsafe_allow_html=True)
