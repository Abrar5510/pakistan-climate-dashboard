import streamlit as st
import pandas as pd
import plotly.express as px

# 🎨 Page Configuration with Custom Theme
st.set_page_config(
    page_title="🔥 Pakistan Heatwave Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🌡️"
)

# 🎨 Custom CSS for Beautiful Styling
st.markdown('''
<style>
    .main-header {
        background: linear-gradient(135deg, #1e3c72, #2a5298);
        padding: 3rem 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .main-title {
        font-size: 3rem;
        margin: 0;
    }
    .main-subtitle {
        font-size: 1.25rem;
        opacity: 0.9;
    }
    .metric-card {
        background: linear-gradient(to right, #6a11cb, #2575fc);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
    }
    .metric-label {
        font-size: 1rem;
        opacity: 0.9;
    }
    .sidebar-header {
        color: white;
        padding: 1rem 0;
        font-size: 1.2rem;
        border-bottom: 2px solid #444;
        margin-bottom: 1rem;
    }
</style>
''', unsafe_allow_html=True)

# 🧠 Load and preprocess data
@st.cache_data
def load_data():
    df = pd.read_csv("pakistan_heatwave_data.csv")
    df['Year'] = df['Year'].astype(str)
    df['Deaths'] = df['Deaths'].fillna(0)
    df['Heatstroke_Cases'] = df['Heatstroke_Cases'].fillna(0)
    df['Agriculture_Loss_pct'] = df['Agriculture_Loss_pct'].fillna(0)
    df['Livestock_Loss'] = df['Livestock_Loss'].fillna("No data available")
    df['Water_Shortage_Impact'] = df['Water_Shortage_Impact'].fillna("No significant impact")
    return df

df = load_data()

# 🌐 Header Section
st.markdown('''
<div class="main-header">
    <h1 class="main-title">🔥 Pakistan Heatwave Analytics</h1>
    <p class="main-subtitle">Advanced Climate Impact Dashboard • Real-time Data Insights</p>
</div>
''', unsafe_allow_html=True)

# 📊 Sidebar Filters
st.sidebar.markdown('''
<div class="sidebar-header">🔍 Smart Filters</div>
''', unsafe_allow_html=True)

cities = sorted(df['City'].dropna().unique().tolist())
selected_cities = st.sidebar.multiselect("🏙️ Select Cities to Compare", cities, default=[cities[0]])

years = sorted(df['Year'].dropna().unique().tolist())
selected_years = st.sidebar.multiselect("📅 Select Years to Compare", years, default=[years[-1]])

# ✅ Filter data
filtered_df = df[df['City'].isin(selected_cities) & df['Year'].isin(selected_years)]

if filtered_df.empty:
    st.warning("⚠️ No data found for the selected filters. Try different cities or years.")
    st.stop()

# 📊 Metric Cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f'''
    <div class="metric-card">
        <div class="metric-value">{len(selected_cities)}</div>
        <div class="metric-label">🏙️ Cities Selected</div>
    </div>
    ''', unsafe_allow_html=True)

with col2:
    st.markdown(f'''
    <div class="metric-card">
        <div class="metric-value">{len(selected_years)}</div>
        <div class="metric-label">📅 Years Analyzed</div>
    </div>
    ''', unsafe_allow_html=True)

with col3:
    st.markdown(f'''
    <div class="metric-card">
        <div class="metric-value">{len(filtered_df)}</div>
        <div class="metric-label">📋 Total Records</div>
    </div>
    ''', unsafe_allow_html=True)

with col4:
    avg_temp = filtered_df['Peak_Temp_C'].mean()
    st.markdown(f'''
    <div class="metric-card">
        <div class="metric-value">{avg_temp:.1f}°C</div>
        <div class="metric-label">🌡️ Avg Peak Temp</div>
    </div>
    ''', unsafe_allow_html=True)

# 📈 Example Chart – Deaths by Year per City
st.subheader("🧍‍♂️ Heatwave Deaths by Year and City")
fig = px.bar(
    filtered_df,
    x="Year",
    y="Deaths",
    color="City",
    barmode="group",
    text_auto=True,
    labels={"Deaths": "Number of Deaths"},
    height=500
)
st.plotly_chart(fig, use_container_width=True)
