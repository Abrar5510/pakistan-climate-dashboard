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
        st.error("CSV file not found. Please make sure 'pakistan_heatwave_data.csv' is in the same directory.")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.stop()

st.title("🔥 Pakistan Heatwave Analysis Dashboard")

# Sidebar filters
st.sidebar.title("🔍 Filter Options")

cities = sorted(df['City'].dropna().unique().tolist())
selected_cities = st.sidebar.multiselect(
    "Select Cities to Compare",
    cities,
    default=[cities[0]] if cities else []
)

years = sorted(df['Year'].dropna().unique().tolist())
selected_years = st.sidebar.multiselect(
    "Select Years to Compare",
    years,
    default=years[-2:] if len(years) >= 2 else years
)

# Filter data
if selected_cities and selected_years:
    filtered_df = df[
        (df["City"].isin(selected_cities)) &
        (df["Year"].isin(selected_years))
    ]
else:
    filtered_df = pd.DataFrame()

if filtered_df.empty:
    st.warning("⚠️ No data available for selected cities and years. Please adjust your filters.")
    st.stop()

# Layout metrics
col1, col2 = st.columns(2)

with col1:
    st.metric("Cities Selected", len(selected_cities))
    st.metric("Years Selected", len(selected_years))

with col2:
    st.metric("Total Records", len(filtered_df))
    avg_temp = filtered_df['Peak_Temp_C'].mean()
    st.metric("Average Peak Temperature", f"{avg_temp:.1f}°C")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Temperature Analysis",
    "⚕️ Health Impact",
    "🌾 Agricultural Impact",
    "💧 Water Crisis"
])

with tab1:
    st.subheader("Peak Temperature Comparison")
    fig1 = px.bar(
        filtered_df,
        x='City',
        y='Peak_Temp_C',
        color='Year',
        barmode='group',
        title="Peak Temperature by City and Year",
        labels={'Peak_Temp_C': 'Peak Temperature (°C)'}
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Heatwave Duration")
    fig2 = px.bar(
        filtered_df,
        x='City',
        y='Duration_Days',
        color='Year',
        barmode='group',
        title="Heatwave Duration by City and Year",
        labels={'Duration_Days': 'Duration (Days)'}
    )
    st.plotly_chart(fig2, use_container_width=True)

with tab2:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Deaths from Heatwaves")
        fig3 = px.bar(
            filtered_df,
            x='City',
            y='Deaths',
            color='Year',
            barmode='group',
            title="Heat-related Deaths"
        )
        st.plotly_chart(fig3, use_container_width=True)

    with col2:
        st.subheader("Heatstroke Cases")
        fig4 = px.bar(
            filtered_df,
            x='City',
            y='Heatstroke_Cases',
            color='Year',
            barmode='group',
            title="Heatstroke Cases Reported"
        )
        st.plotly_chart(fig4, use_container_width=True)

    st.subheader("Health Impact Summary")
    health_summary = filtered_df.groupby(['City', 'Year']).agg({
        'Deaths': 'sum',
        'Heatstroke_Cases': 'sum',
        'Peak_Temp_C': 'max'
    }).reset_index()
    st.dataframe(health_summary, use_container_width=True)

with tab3:
    st.subheader("Agricultural Losses")
    fig5 = px.bar(
        filtered_df,
        x='City',
        y='Agriculture_Loss_pct',
        color='Year',
        barmode='group',
        title="Agricultural Losses by City and Year"
    )
    st.plotly_chart(fig5, use_container_width=True)

    st.subheader("Livestock Impact Details")
    for _, row in filtered_df.iterrows():
        if row['Livestock_Loss'] != "No data available":
            st.info(f"**{row['City']} ({row['Year']})** — {row['Livestock_Loss']}")

with tab4:
    st.subheader("Water Shortage Impact")
    for _, row in filtered_df.iterrows():
        if row['Water_Shortage_Impact'] != "No significant impact":
            st.warning(f"**{row['City']} ({row['Year']})** — {row['Water_Shortage_Impact']}")

    st.subheader("Temperature vs Duration Analysis")
    fig6 = px.scatter(
        filtered_df,
        x='Peak_Temp_C',
        y='Duration_Days',
        size='Deaths',
        color='City',
        hover_data=['Year', 'Heatstroke_Cases'],
        title="Peak Temperature vs Duration"
    )
    st.plotly_chart(fig6, use_container_width=True)

# Raw data
with st.expander("📋 View Raw Data"):
    if not filtered_df.empty:
        st.dataframe(filtered_df, use_container_width=True)

        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Filtered Data as CSV",
            data=csv,
            file_name=f"pakistan_heatwave_filtered_{'-'.join(selected_cities)}_{'-'.join(selected_years)}.csv",
            mime="text/csv"
        )
    else:
        st.info("No data to display. Please select cities and years from the sidebar.")

# Summary Stats
if not filtered_df.empty:
    st.subheader("📈 Summary Statistics")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Highest Temperature", f"{filtered_df['Peak_Temp_C'].max():.1f}°C")
        hottest = filtered_df.loc[filtered_df['Peak_Temp_C'].idxmax()]
        st.caption(f"in {hottest['City']} ({hottest['Year']})")

    with col2:
        st.metric("Total Deaths", int(filtered_df['Deaths'].sum()))
        st.caption("across selected data")

    with col3:
        st.metric("Total Heatstroke Cases", int(filtered_df['Heatstroke_Cases'].sum()))
        st.caption("across selected data")

    with col4:
        st.metric("Longest Heatwave", f"{filtered_df['Duration_Days'].max()} days")
        longest = filtered_df.loc[filtered_df['Duration_Days'].idxmax()]
        st.caption(f"in {longest['City']} ({longest['Year']})")

# Footer
st.markdown("---")
st.caption("📊 Data Source: Pakistan Meteorological Department & Health Ministry Reports (2022–2025)")
st.caption("🔧 Dashboard built with Streamlit & Plotly")
