import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Pakistan Heatwave Dashboard", layout="wide")

# Load CSV
@st.cache_data
def load_data():
    df = pd.read_csv("pakistan_heatwave_data.csv")
    df.fillna("N/A", inplace=True)
    return df

df = load_data()

# Sidebar filters
st.sidebar.title("🔍 Filters")
cities = df['City'].unique().tolist()
years = sorted(df['Year'].dropna().unique().tolist())

selected_cities = st.sidebar.multiselect("Select City", cities, default=cities)
selected_years = st.sidebar.multiselect("Select Year", years, default=years)
view_mode = st.sidebar.radio("View Mode", ["📈 Graph View", "📋 Table View"])

# Filter data
filtered_df = df[df["City"].isin(selected_cities) & df["Year"].isin(selected_years)]

# Dashboard Title
st.title("🔥 Pakistan Heatwave Dashboard (2022–2025)")
st.markdown("Explore heatwave impacts on cities across Pakistan, including deaths, heatstroke cases, agriculture, and water shortages.")

# Display View
if view_mode == "📋 Table View":
    st.markdown("### Full Heatwave Impact Table")
    st.dataframe(filtered_df, use_container_width=True, height=700)
else:
    st.markdown("### Peak Temperatures by City")
    fig = px.bar(filtered_df, x='City', y='Peak_Temp_C', color='Period',
                 hover_data=['Year', 'Deaths', 'Heatstroke_Cases', 'Agriculture_Loss_pct'],
                 title="Peak Temperatures (as reported)", height=500)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### Heatstroke Cases by City")
    fig2 = px.bar(filtered_df, x='City', y='Heatstroke_Cases', color='Year',
                  hover_data=['Period', 'Deaths'], height=500)
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("### Deaths Reported by City")
    fig3 = px.bar(filtered_df, x='City', y='Deaths', color='Year',
                  hover_data=['Water_Shortage_Impact'], height=500)
    st.plotly_chart(fig3, use_container_width=True)

# Sector-wide note
if "Sector‑wide Pakistan" in filtered_df['City'].values:
    st.markdown("### 📌 National-Level Sector Impact")
    sector_row = df[df['City'] == "Sector‑wide Pakistan"].iloc[0]
    st.info(f"""
    **Agriculture Impact**: {sector_row['Agriculture_Loss_pct']}  
    **Livestock Impact**: {sector_row['Livestock_Loss']}  
    **Water Shortage Summary**: {sector_row['Water_Shortage_Impact']}
    """)

# Footer
st.caption("Data Source: Compiled from heatwave analysis (2022–2025) — custom dataset")
