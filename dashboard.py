import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Pakistan Heatwave Dashboard", layout="wide")

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
        st.error("CSV file not found. Please ensure ‘pakistan_heatwave_data.csv’ is in the same directory.")
        return pd.DataFrame()

df = load_data()
if df.empty:
    st.stop()

st.title("🔥 Pakistan Heatwave Analysis Dashboard")
st.sidebar.title("🔍 Filter Options")

cities = sorted(df['City'].dropna().unique())
selected_cities = st.sidebar.multiselect("Select Cities to Compare", cities, default=cities[:2])
years = sorted(df['Year'].dropna().unique())
selected_years = st.sidebar.multiselect("Select Years to Compare", years, default=years[-2:])

if selected_cities and selected_years:
    filtered_df = df[(df['City'].isin(selected_cities)) & (df['Year'].isin(selected_years))]
else:
    filtered_df = pd.DataFrame()

if filtered_df.empty:
    st.warning("⚠️ No data available for selected cities and years. Please adjust your filters.")
    st.stop()

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Temperature", "⚕️ Health", "🌾 Agriculture", "💧 Water Crisis"])

# ——— TEMPERATURE TAB ———
with tab1:
    st.subheader("Peak Temperature by City and Year")
    fig1 = px.bar(
        filtered_df,
        x="City",
        y="Peak_Temp_C",
        color="Year",
        barmode="group",
        color_discrete_sequence=px.colors.qualitative.Set3,
        labels={"Peak_Temp_C": "Peak Temperature (°C)"}
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Heatwave Duration")
    fig2 = px.bar(
        filtered_df,
        x="City",
        y="Duration_Days",
        color="Year",
        barmode="group",
        color_discrete_sequence=px.colors.qualitative.set3,
        labels={"Duration_Days": "Duration (Days)"}
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("📈 Summary Statistics")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Cities Selected", len(selected_cities))
        st.metric("Years Selected", len(selected_years))
    with col2:
        avg_temp = filtered_df["Peak_Temp_C"].mean()
        st.metric("Average Peak Temperature", f"{avg_temp:.1f}°C")
        max_temp = filtered_df["Peak_Temp_C"].max()
        hottest = filtered_df.loc[filtered_df["Peak_Temp_C"].idxmax()]
        st.caption(f"Hottest in {hottest['City']} ({hottest['Year']}): {max_temp}°C")

# ——— HEALTH TAB ———
with tab2:
    st.subheader("Heatwave Deaths")
    fig3 = px.bar(
        filtered_df,
        x="City",
        y="Deaths",
        color="Year",
        barmode="group",
        color_discrete_sequence=px.colors.sequential.thermal,
        labels={"Deaths": "Number of Deaths"}
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Heatstroke Cases")
    fig4 = px.bar(
        filtered_df,
        x="City",
        y="Heatstroke_Cases",
        color="Year",
        barmode="group",
        color_discrete_sequence=px.colors.sequential.sunsetdark,
        labels={"Heatstroke_Cases": "Cases"}
    )
    st.plotly_chart(fig4, use_container_width=True)

    st.subheader("📊 Health Summary")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Deaths", int(filtered_df["Deaths"].sum()))
    with col2:
        st.metric("Heatstroke Cases", int(filtered_df["Heatstroke_Cases"].sum()))
    
    health_summary = filtered_df.groupby(['City', 'Year']).agg({
        'Deaths': 'sum',
        'Heatstroke_Cases': 'sum',
        'Peak_Temp_C': 'max'
    }).reset_index()
    st.dataframe(health_summary, use_container_width=True)

# ——— AGRICULTURE TAB ———
with tab3:
    st.subheader("Agriculture Loss (%)")
    fig5 = px.bar(
        filtered_df,
        x="City",
        y="Agriculture_Loss_pct",
        color="Year",
        barmode="group",
        color_discrete_sequence=px.colors.sequential.amp,
        labels={"Agriculture_Loss_pct": "Loss %"}
    )
    st.plotly_chart(fig5, use_container_width=True)

    st.subheader("📊 Livestock Impact")
    for _, row in filtered_df.iterrows():
        if row['Livestock_Loss'] != "No data available":
            st.info(f"**{row['City']} ({row['Year']})** — {row['Livestock_Loss']}")

# ——— WATER TAB ———
with tab4:
    st.subheader("Water Shortage Impact Reports")
    for _, row in filtered_df.iterrows():
        if row["Water_Shortage_Impact"] != "No significant impact":
            st.warning(f"**{row['City']} ({row['Year']})** — {row['Water_Shortage_Impact']}")

    st.subheader("Temperature vs Duration")
    fig6 = px.scatter(
        filtered_df,
        x="Peak_Temp_C",
        y="Duration_Days",
        size="Deaths",
        color="City",
        hover_data=["Year", "Heatstroke_Cases"],
        color_discrete_sequence=px.colors.sequential.Viridis,
        title="Peak Temperature vs Heatwave Duration"
    )
    st.plotly_chart(fig6, use_container_width=True)

# ——— RAW DATA ———
with st.expander("📋 View Raw Data"):
    st.dataframe(filtered_df, use_container_width=True)
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv,
        file_name=f"pakistan_heatwave_filtered_{'-'.join(selected_cities)}_{'-'.join(selected_years)}.csv",
        mime="text/csv"
    )

# ——— FOOTER ———
st.markdown("—")
st.caption("📊 Data Source: Pakistan Meteorological Department & Ministry of Climate Change (2022–2025)")
st.caption("🔧 Dashboard built with Streamlit & Plotly | Theme: Bright Colors + Modular Layouts")
