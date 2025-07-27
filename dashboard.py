import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page Configuration
st.set_page_config(
    page_title="Pakistan Heatwave Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🌡️"
)

# Custom CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    .main { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); font-family: 'Poppins', sans-serif; }
</style>
""", unsafe_allow_html=True)

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
        st.error("CSV file not found. Please make sure 'pakistan_heatwave_data.csv' is in the same directory.")
        return pd.DataFrame()

df = load_data()
if df.empty:
    st.stop()

# Header
st.markdown("""
<div style='background: linear-gradient(90deg, #ff6b6b, #feca57, #48dbfb, #ff9ff3, #54a0ff); padding: 2rem; border-radius: 20px; text-align: center;'>
    <h1 style='color: white; font-size: 3rem;'>🔥 Pakistan Heatwave Analytics</h1>
    <p style='color: white; font-size: 1.2rem;'>Advanced Climate Impact Dashboard • Real-time Data Insights</p>
</div>
""", unsafe_allow_html=True)

# Sidebar Filters
st.sidebar.header("🔍 Smart Filters")
cities = sorted(df['City'].dropna().unique().tolist())
selected_cities = st.sidebar.multiselect("🏙️ Select Cities to Compare", cities, default=cities[:1])
years = sorted(df['Year'].dropna().unique().tolist())
selected_years = st.sidebar.multiselect("📅 Select Years to Compare", years, default=years[-2:])

# Filtered Data
if selected_cities and selected_years:
    filtered_df = df[(df["City"].isin(selected_cities)) & (df["Year"].isin(selected_years))]
else:
    filtered_df = pd.DataFrame()

if filtered_df.empty:
    st.warning("⚠️ No Data Available. Please adjust your filters.")
    st.stop()

# Metrics Summary
col1, col2, col3, col4 = st.columns(4)
col1.metric("🏙️ Cities Selected", len(selected_cities))
col2.metric("📅 Years Analyzed", len(selected_years))
col3.metric("📋 Total Records", len(filtered_df))
col4.metric("🌡️ Avg Peak Temp", f"{filtered_df['Peak_Temp_C'].mean():.1f}°C")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "🌡️ Temperature Analysis",
    "⚕️ Health Impact",
    "🌾 Agricultural Impact",
    "💧 Water & Climate Crisis"
])

with tab1:
    st.subheader("🔥 Peak Temperature Comparison")
    fig1 = px.bar(
        filtered_df, x="City", y="Peak_Temp_C", color="Year",
        barmode="group", title="Peak Temperature by City and Year"
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("⏱️ Heatwave Duration")
    fig2 = px.bar(
        filtered_df, x="City", y="Duration_Days", color="Year",
        barmode="group", title="Heatwave Duration by City and Year"
    )
    st.plotly_chart(fig2, use_container_width=True)

with tab2:
    st.subheader("☠️ Heat-Related Deaths")
    fig3 = px.bar(
        filtered_df, x="City", y="Deaths", color="Year",
        barmode="group", title="Deaths from Heatwaves"
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("🏥 Heatstroke Cases")
    fig4 = px.bar(
        filtered_df, x="City", y="Heatstroke_Cases", color="Year",
        barmode="group", title="Heatstroke Cases Reported"
    )
    st.plotly_chart(fig4, use_container_width=True)

with tab3:
    st.subheader("🌾 Agricultural Loss (%)")
    fig5 = px.bar(
        filtered_df, x="City", y="Agriculture_Loss_pct", color="Year",
        barmode="group", title="Agriculture Loss by City"
    )
    st.plotly_chart(fig5, use_container_width=True)

    st.subheader("🐄 Livestock Loss Reports")
    for _, row in filtered_df[filtered_df['Livestock_Loss'] != "No data available"].iterrows():
        st.info(f"{row['City']} ({row['Year']}): {row['Livestock_Loss']}")

with tab4:
    st.subheader("💧 Water Shortage Impact")
    for _, row in filtered_df[filtered_df['Water_Shortage_Impact'] != "No significant impact"].iterrows():
        st.warning(f"{row['City']} ({row['Year']}): {row['Water_Shortage_Impact']}")

# Downloadable Data
with st.expander("📋 View & Download Filtered Data"):
    st.dataframe(filtered_df)
    csv = filtered_df.to_csv(index=False).encode()
    st.download_button("📥 Download CSV", data=csv, file_name="filtered_heatwave_data.csv", mime="text/csv")

# Footer
st.markdown("""
<hr>
<p style='text-align: center; color: gray;'>📊 Pakistan Heatwave Dashboard • Built with Streamlit • 2025</p>
""", unsafe_allow_html=True)
