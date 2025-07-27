import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page Configuration
st.set_page_config(
    page_title="🔥 Pakistan Heatwave Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🌡️"
)

# Custom CSS Styling
st.markdown('''
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    .main {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        font-family: 'Inter', sans-serif;
    }

    .main-header {
        background: linear-gradient(135deg, #1e293b 0%, #334155 50%, #475569 100%);
        padding: 3rem 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.1);
    }

    .main-title {
        font-size: 3.2rem;
        font-weight: 700;
        color: white;
        margin: 0;
        letter-spacing: -0.02em;
    }

    .main-subtitle {
        font-size: 1.1rem;
        color: #cbd5e1;
        margin-top: 0.75rem;
        font-weight: 400;
    }

    .sidebar-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        text-align: center;
        border: 1px solid #334155;
    }

    .metric-card {
        background: white;
        padding: 2rem 1.5rem;
        border-radius: 12px;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
    }

    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
    }

    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        margin: 0;
        color: #1e293b;
    }

    .metric-label {
        font-size: 0.9rem;
        color: #64748b;
        margin-top: 0.5rem;
        font-weight: 500;
    }
</style>
''', unsafe_allow_html=True)

# Load Data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("pakistan_heatwave_data.csv")
        df['Year'] = df['Year'].astype(str)
        df['Deaths'] = df['Deaths'].fillna(0)
        df['Heatstroke_Cases'] = df['Heatstroke_Cases'].fillna(0)
        df['Agriculture_Loss_pct'] = df['Agriculture_Loss_pct'].fillna(0)
        df['Livestock_Loss'] = df['Livestock_Loss'].fillna("No data available")
        df['Water_Shortage_Impact'] = df['Water_Shortage_Impact'].fillna("No significant impact")
        return df
    except FileNotFoundError:
        st.error("🚨 CSV file not found. Please make sure 'pakistan_heatwave_data.csv' is in the same directory.")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.stop()

# Header Section
st.markdown('''
<div class="main-header">
    <h1 class="main-title">🔥 Pakistan Heatwave Analytics</h1>
    <p class="main-subtitle">Advanced Climate Impact Dashboard & Data Insights</p>
</div>
''', unsafe_allow_html=True)

# Sidebar Filters
st.sidebar.markdown('''
<div class="sidebar-header">
    <h2 style="color: white; margin: 0; font-size: 1.4rem; font-weight: 600;">🔍 Filter Controls</h2>
</div>
''', unsafe_allow_html=True)

cities = sorted(df['City'].dropna().unique().tolist())
selected_cities = st.sidebar.multiselect(
    "🏙️ Select Cities to Compare",
    cities,
    default=[cities[0]] if cities else [],
    help="Choose one or more cities for comparison"
)

years = sorted(df['Year'].dropna().unique().tolist())
selected_years = st.sidebar.multiselect(
    "📅 Select Years to Compare",
    years,
    default=years[-2:] if len(years) >= 2 else years,
    help="Select years for temporal analysis"
)

# Filter Data
if selected_cities and selected_years:
    filtered_df = df[(df["City"].isin(selected_cities)) & (df["Year"].isin(selected_years))]
else:
    filtered_df = pd.DataFrame()

if filtered_df.empty:
    st.markdown('''
    <div style="background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%);
                padding: 2rem; border-radius: 12px; text-align: center; color: white; margin: 2rem 0;">
        <h2 style="margin: 0;">⚠️ No Data Available</h2>
        <p style="margin: 0.5rem 0 0 0;">Please adjust your filters to view the dashboard</p>
    </div>
    ''', unsafe_allow_html=True)
    st.stop()
