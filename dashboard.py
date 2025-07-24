# dashboard.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Pakistan Climate Crisis Dashboard", layout="wide")
st.title("🌍 Pakistan Climate Crisis Dashboard (2020–2025)")

st.markdown("""
This dashboard presents a **multi-dimensional view of Pakistan's climate crisis** from 2020 to 2025.  
It includes temperature trends, rainfall patterns, economic losses, droughts, floods, food insecurity, and water scarcity.
""")

# --- DATA ---
climate_overview = pd.DataFrame({
    'Year': [2020, 2021, 2022, 2023, 2024, 2025],
    'Peak_Temp_C': [47.0, 45.8, 49.5, 46.5, 47.2, 50.0],
    'Heat_Deaths': [75, 50, 90, 100, 568, 200],
    'Rainfall_Deficit_Percent': [30, 15, 62, 25, 45, 67],
    'Crop_Losses_MT': [2.5, 1.8, 4.5, 2.1, 3.8, 5.2],
    'Food_Insecure_Million': [6.0, 6.5, 7.2, 7.8, 8.6, 8.6],
    'Water_Availability_m3_capita': [1050, 1000, 950, 900, 800, 720],
    'Economic_Loss_Billion_USD': [5.5, 4.2, 30.0, 6.8, 12.2, 8.5]
})

rainfall_data = pd.DataFrame({
    'Year': [2020, 2021, 2022, 2023, 2024, 2025],
    'Annual_Rainfall_mm': [185, 215, 425, 195, 165, 82],
    'Monsoon_Rainfall_mm': [125, 145, 285, 135, 95, 45],
    'Deficit_from_Normal_Percent': [-30, -15, 180, -25, -45, -67],
    'Drought_Affected_Areas_Percent': [30, 20, 15, 25, 35, 45],
    'Flood_Events': [1, 2, 12, 3, 4, 2],
    'Climate_Pattern': ['Moderate Drought', 'Normal/Slight Deficit', 'Extreme Floods',
                        'Moderate Drought', 'Mixed (Drought + Floods)', 'Severe Drought']
})

# --- DASHBOARD ---
fig = make_subplots(
    rows=3, cols=2,
    subplot_titles=(
        'Temperature Trends (2020–2025)',
        'Heat-Related Deaths',
        'Water Availability Crisis',
        'Food Insecurity Growth',
        'Rainfall Patterns',
        'Economic Impact'
    ),
    specs=[[{}, {}], [{}, {}], [{}, {}]]
)

fig.add_trace(go.Scatter(
    x=climate_overview['Year'],
    y=climate_overview['Peak_Temp_C'],
    mode='lines+markers',
    name='Peak Temperature',
    line=dict(color='red', width=3)
), row=1, col=1)

fig.add_trace(go.Bar(
    x=climate_overview['Year'],
    y=climate_overview['Heat_Deaths'],
    name='Heat Deaths',
    marker_color='darkred'
), row=1, col=2)

fig.add_trace(go.Scatter(
    x=climate_overview['Year'],
    y=climate_overview['Water_Availability_m3_capita'],
    mode='lines+markers',
    name='Water Availability',
    line=dict(color='blue', width=3)
), row=2, col=1)

fig.add_trace(go.Scatter(
    x=climate_overview['Year'],
    y=climate_overview['Food_Insecure_Million'],
    mode='lines+markers',
    name='Food Insecurity',
    line=dict(color='orange', width=3)
), row=2, col=2)

fig.add_trace(go.Bar(
    x=rainfall_data['Year'],
    y=rainfall_data['Annual_Rainfall_mm'],
    name='Annual Rainfall',
    marker_color='lightblue'
), row=3, col=1)

fig.add_trace(go.Bar(
    x=rainfall_data['Year'],
    y=rainfall_data['Monsoon_Rainfall_mm'],
    name='Monsoon Rainfall',
    marker_color='darkblue'
), row=3, col=1)

fig.add_trace(go.Bar(
    x=climate_overview['Year'],
    y=climate_overview['Economic_Loss_Billion_USD'],
    name='Economic Loss ($B)',
    marker_color='purple'
), row=3, col=2)

fig.update_layout(
    height=1000,
    title_text="🇵🇰 Pakistan Climate Crisis Interactive Dashboard (2020–2025)",
    title_x=0.5,
    showlegend=True,
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.info("Made by Abrar Ahmad as part of the WWF Eco-Internship Project")
