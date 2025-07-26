import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Pakistan Heatwave Dashboard", layout="wide")

@st.cache_data
def load_data():
    df = pd.read_csv("pakistan_heatwave_data.csv")
    df.fillna("N/A", inplace=True)
    return df

df = load_data()

# Sidebar filters
st.sidebar.title("🔍 Compare Heatwave Data")
cities = sorted(df['City'].dropna().unique().tolist())
years = sorted(df['Year'].dropna().unique().tolist())

selected_city = st.sidebar.selectbox("Select City", cities)
year1 = st.sidebar.selectbox("Select First Year", years, index=0)
year2 = st.sidebar.selectbox("Select Second Year", years, index=1)

# Filter data
filtered = df[(df["City"] == selected_city) & (df["Year"].isin([year1, year2]))]

# Check for data
if filtered.empty:
    st.warning("No data available for selected city and years.")
else:
    st.title(f"🔥 Heatwave Comparison for {selected_city} ({year1} vs {year2})")

    st.markdown("### Peak Temperature")
    fig1 = px.bar(filtered, x='Year', y='Peak_Temp_C', color='Period', text='Period')
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("### Duration (Days)")
    fig2 = px.bar(filtered, x='Year', y='Duration_Days', color='Period')
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("### Deaths")
    fig3 = px.bar(filtered, x='Year', y='Deaths', color='Period')
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown("### Heatstroke Cases")
    fig4 = px.bar(filtered, x='Year', y='Heatstroke_Cases', color='Period')
    st.plotly_chart(fig4, use_container_width=True)

    st.markdown("### Agriculture Loss (%)")
    fig5 = px.bar(filtered, x='Year', y='Agriculture_Loss_pct', color='Period')
    st.plotly_chart(fig5, use_container_width=True)

    st.markdown("### Livestock Loss")
    for index, row in filtered.iterrows():
        st.info(f"**{row['Year']}** — {row['Livestock_Loss']}")

    st.markdown("### Water Shortage Impact")
    for index, row in filtered.iterrows():
        st.warning(f"**{row['Year']}** — {row['Water_Shortage_Impact']}")

# Optional table view
with st.expander("📋 See Raw Table Data"):
    st.dataframe(filtered, use_container_width=True)

# Footer
st.caption("Data Source: Pakistan heatwave dataset (2022–2025)")
