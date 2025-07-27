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
