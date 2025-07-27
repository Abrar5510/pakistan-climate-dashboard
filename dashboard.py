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
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    .main {
        background-color: #f5f7fa;
        font-family: 'Inter', sans-serif;
    }

    .main-header {
        background-color: #1e293b;
        padding: 2.5rem 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 6px 20px rgba(0,0,0,0.1);
    }

    .main-title {
        font-size: 2.8rem;
        font-weight: 700;
        margin: 0;
    }

    .main-subtitle {
        font-size: 1.1rem;
        font-weight: 400;
        margin-top: 0.5rem;
        color: #cbd5e1;
    }

    .sidebar-header {
        background-color: #334155;
        padding: 1.2rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        text-align: center;
        color: white;
    }

    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        border: 1px solid #e2e8f0;
        transition: 0.2s ease;
    }

    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(0,0,0,0.1);
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
        color: #1e293b;
    }

    .metric-label {
        font-size: 0.95rem;
        color: #475569;
        margin-top: 0.25rem;
        font-weight: 500;
    }

    .stButton>button {
        background-color: #0f172a;
        color: white;
        border: none;
        padding: 0.5rem 1rem;
        border-radius: 8px;
        font-weight: 600;
        cursor: pointer;
        transition: background-color 0.2s ease;
    }

    .stButton>button:hover {
        background-color: #1e293b;
    }

</style>
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
