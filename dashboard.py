import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import io

# --- Page Configuration & UI ---
st.set_page_config(
    page_title="🔥 Pakistan Heatwave Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🌡️"
)

# Custom CSS Styling
st.markdown('''
<style>
    /* CSS code from your prompt */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    .main { background-color: #f5f7fa; font-family: 'Inter', sans-serif; }
    .main-header { background-color: #1e293b; padding: 2.5rem 2rem; border-radius: 12px; margin-bottom: 2rem; text-align: center; color: white; box-shadow: 0 6px 20px rgba(0,0,0,0.1); }
    .main-title { font-size: 2.8rem; font-weight: 700; margin: 0; }
    .main-subtitle { font-size: 1.1rem; font-weight: 400; margin-top: 0.5rem; color: #cbd5e1; }
    .sidebar-header { background-color: #334155; padding: 1.2rem; border-radius: 10px; margin-bottom: 1.5rem; text-align: center; color: white; }
    .metric-card { background: white; padding: 1.5rem; border-radius: 10px; text-align: center; margin: 0.5rem 0; box-shadow: 0 2px 10px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; transition: 0.2s ease; }
    .metric-card:hover { transform: translateY(-2px); box-shadow: 0 6px 15px rgba(0,0,0,0.1); }
    .metric-value { font-size: 2rem; font-weight: 700; margin: 0; color: #1e293b; }
    .metric-label { font-size: 0.95rem; color: #475569; margin-top: 0.25rem; font-weight: 500; }
    .stButton>button { background-color: #0f172a; color: white; border: none; padding: 0.5rem 1rem; border-radius: 8px; font-weight: 600; cursor: pointer; transition: background-color 0.2s ease; }
    .stButton>button:hover { background-color: #1e293b; }
</style>
''', unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.markdown('''
<div class="sidebar-header">
    <h2 style="color: white; margin: 0; font-size: 1.4rem; font-weight: 600;">📊 Data & Filters</h2>
</div>
''', unsafe_allow_html=True)

# --- Data Loading ---
uploaded_file = st.sidebar.file_uploader("📂 Upload your Heatwave CSV File", type="csv")

# Main Dashboard Header
st.markdown('''
<div class="main-header">
    <h1 class="main-title">🔥 Pakistan Heatwave Analysis</h1>
    <p class="main-subtitle">An interactive dashboard to explore heatwave data from 2022-2025</p>
</div>
''', unsafe_allow_html=True)

# Conditional logic: The app will only proceed if a file has been uploaded
if uploaded_file is None:
    st.info("ℹ️ Please upload a CSV file using the sidebar to begin analysis.")
    st.stop()

# Load the data from the uploaded file
df = pd.read_csv(uploaded_file)


# --- Sidebar Filters ---
st.sidebar.markdown("---") # Visual separator
st.sidebar.markdown('<h3 style="font-family: Inter; font-weight: 600;">🔍 Filter Controls</h3>', unsafe_allow_html=True)

cities = sorted(df['City'].dropna().unique().tolist())
selected_cities = st.sidebar.multiselect(
    "🏙️ Select Cities to Compare",
    cities,
    default=["Karachi", "Lahore", "Islamabad"] if "Karachi" in cities else [cities[0]],
    help="Choose one or more cities for comparison"
)

years = sorted(df['Year'].dropna().unique().tolist(), reverse=True)
selected_years = st.sidebar.multiselect(
    "📅 Select Years to Compare",
    years,
    default=years[:2] if len(years) >= 2 else years,
    help="Select years for temporal analysis"
)

# --- Data Filtering ---
if selected_cities and selected_years:
    filtered_df = df[(df["City"].isin(selected_cities)) & (df["Year"].isin(selected_years))].copy()
else:
    # Create an empty dataframe with same columns if selection is empty
    filtered_df = pd.DataFrame(columns=df.columns)

# --- Dashboard Display ---
if filtered_df.empty:
    st.markdown('''
    <div style="background: linear-gradient(135deg, #f97316 0%, #fb923c 100%);
                padding: 2rem; border-radius: 12px; text-align: center; color: white; margin: 2rem 0;">
        <h2 style="margin: 0;">🤔 No Data Found</h2>
        <p style="margin: 0.5rem 0 0 0;">Please select at least one city and year to view the data.</p>
    </div>
    ''', unsafe_allow_html=True)
    st.stop()

# --- Example: Displaying a Chart ---
st.markdown("### 🌡️ Peak Temperatures (°C) Comparison")
fig_temp = px.bar(
    filtered_df,
    x='City',
    y='Peak_Temp_C',
    color='Year',
    barmode='group',
    title="Peak Temperatures by City and Year",
    labels={'Peak_Temp_C': 'Peak Temperature (°C)', 'City': 'City', 'Year': 'Year'},
    color_discrete_sequence=px.colors.sequential.Reds_r
)
fig_temp.update_layout(
    plot_bgcolor='white',
    font_family='Inter',
    legend_title_text='Year'
)
st.plotly_chart(fig_temp, use_container_width=True)

# --- Example: Displaying a Table ---
st.markdown("### 📊 Raw Filtered Data")
st.dataframe(filtered_df, use_container_width=True)
