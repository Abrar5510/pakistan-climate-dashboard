import streamlit as st
import pandas as pd
import plotly.express as px

from plotly.subplots import make_subplots
import plotly.graph_objects as go

st.set_page_config(page_title="🔥 Pakistan Heatwave Dashboard", layout="wide")

# Custom CSS for professional styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    .main { background-color: #f5f7fa; font-family: 'Inter', sans-serif; }
    .main-header { background-color: #1e293b; padding: 2.5rem 2rem; border-radius: 12px; margin-bottom: 2rem; text-align: center; color: white; box-shadow: 0 6px 20px rgba(0,0,0,0.1); }
    .main-title { font-size: 2.8rem; font-weight: 700; margin: 0; }
    .main-subtitle { font-size: 1.1rem; font-weight: 400; margin-top: 0.5rem; color: #cbd5e1; }
    .metric-card { background: white; padding: 1.5rem; border-radius: 10px; text-align: center; margin: 0.5rem 0; box-shadow: 0 2px 10px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; transition: 0.2s ease; }
    .metric-card:hover { transform: translateY(-2px); box-shadow: 0 6px 15px rgba(0,0,0,0.1); }
    .metric-value { font-size: 2rem; font-weight: 700; margin: 0; color: #1e293b; }
    .metric-label { font-size: 0.95rem; color: #475569; margin-top: 0.25rem; font-weight: 500; }
    .chart-container { background: white; padding: 1.5rem; border-radius: 12px; margin: 1rem 0; box-shadow: 0 2px 10px rgba(0,0,0,0.05); border: 1px solid #e2e8f0; }
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
<div class="main-header">
    <h1 class="main-title">🔥 Pakistan Heatwave Dashboard</h1>
    <p class="main-subtitle">Advanced Climate Impact Analysis • 2022–2025 Data</p>
</div>
""", unsafe_allow_html=True)

# Sidebar filters
st.sidebar.title("🔍 Filter Options")
cities = sorted(df['City'].dropna().unique().tolist())
selected_cities = st.sidebar.multiselect("Select Cities to Compare", cities, default=[cities[0]] if cities else [])

years = sorted(df['Year'].dropna().unique().tolist())
selected_years = st.sidebar.multiselect("Select Years to Compare", years, default=years[-2:] if len(years) >= 2 else years)

if selected_cities and selected_years:
    filtered_df = df[(df["City"].isin(selected_cities)) & (df["Year"].isin(selected_years))]
else:
    filtered_df = pd.DataFrame()

if filtered_df.empty:
    st.warning("⚠️ No data available for selected cities and years. Please adjust your filters.")
    st.stop()

# Metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{len(selected_cities)}</div>
        <div class="metric-label">Cities Selected</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{len(selected_years)}</div>
        <div class="metric-label">Years Selected</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{len(filtered_df)}</div>
        <div class="metric-label">Total Records</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    avg_temp = filtered_df['Peak_Temp_C'].mean()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{avg_temp:.1f}°C</div>
        <div class="metric-label">Average Peak Temperature</div>
    </div>
    """, unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Temperature Analysis",
    "⚕️ Health Impact",
    "🌾 Agricultural Impact",
    "💧 Water Crisis"
])

with tab1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("Peak Temperature Comparison")
    fig1 = px.bar(
        filtered_df, x='City', y='Peak_Temp_C', color='Year',
        barmode='group',
        color_discrete_sequence=px.colors.sequential.Turbo,
        labels={'Peak_Temp_C': 'Peak Temperature (°C)'},
        title="🌡️ Peak Temperature by City and Year"
    )
    fig1.update_traces(hovertemplate="<b>%{x}</b><br>Temp: %{y}°C<br>Year: %{customdata[0]}", customdata=filtered_df[['Year']])
    fig1.update_layout(height=500, plot_bgcolor='rgba(0,0,0,0)', font_family="Inter")
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Heatwave Duration")
    fig2 = px.bar(
        filtered_df, x='City', y='Duration_Days', color='Year',
        barmode='group',
        color_discrete_sequence=px.colors.sequential.Plasma,
        labels={'Duration_Days': 'Duration (Days)'},
        title="🕒 Heatwave Duration by City and Year"
    )
    fig2.update_traces(hovertemplate="<b>%{x}</b><br>Duration: %{y} Days<br>Year: %{customdata[0]}", customdata=filtered_df[['Year']])
    fig2.update_layout(height=500, plot_bgcolor='rgba(0,0,0,0)', font_family="Inter")
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Deaths from Heatwaves")
        fig3 = px.bar(
            filtered_df, x='City', y='Deaths', color='Year',
            barmode='group',
            color_discrete_sequence=px.colors.sequential.Reds,
            title="☠️ Heat-related Deaths"
        )
        fig3.update_traces(hovertemplate="<b>%{x}</b><br>Deaths: %{y}<br>Year: %{customdata[0]}", customdata=filtered_df[['Year']])
        fig3.update_layout(height=400, plot_bgcolor='rgba(0,0,0,0)', font_family="Inter")
        st.plotly_chart(fig3, use_container_width=True)

    with col2:
        st.subheader("Heatstroke Cases")
        fig4 = px.bar(
            filtered_df, x='City', y='Heatstroke_Cases', color='Year',
            barmode='group',
            color_discrete_sequence=px.colors.sequential.Oranges,
            title="💥 Heatstroke Cases Reported"
        )
        fig4.update_traces(hovertemplate="<b>%{x}</b><br>Cases: %{y}<br>Year: %{customdata[0]}", customdata=filtered_df[['Year']])
        fig4.update_layout(height=400, plot_bgcolor='rgba(0,0,0,0)', font_family="Inter")
        st.plotly_chart(fig4, use_container_width=True)

    st.subheader("🧾 Health Impact Summary")
    health_summary = filtered_df.groupby(['City', 'Year']).agg({
        'Deaths': 'sum',
        'Heatstroke_Cases': 'sum',
        'Peak_Temp_C': 'max'
    }).reset_index()
    st.dataframe(health_summary, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("Agricultural Losses")
    fig5 = px.bar(
        filtered_df, x='City', y='Agriculture_Loss_pct', color='Year',
        barmode='group',
        color_discrete_sequence=px.colors.sequential.Aggrnyl,
        labels={'Agriculture_Loss_pct': 'Agriculture Loss (%)'},
        title="🌽 Agricultural Losses by City and Year"
    )
    fig5.update_layout(height=500, plot_bgcolor='rgba(0,0,0,0)', font_family="Inter")
    st.plotly_chart(fig5, use_container_width=True)

    st.subheader("🐄 Livestock Impact")
    for _, row in filtered_df.iterrows():
        if row['Livestock_Loss'] != "No data available":
            st.info(f"**{row['City']} ({row['Year']})** — {row['Livestock_Loss']}")
    st.markdown('</div>', unsafe_allow_html=True)

with tab4:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.subheader("Water Shortage Impact")
    for _, row in filtered_df.iterrows():
        if row['Water_Shortage_Impact'] != "No significant impact":
            st.warning(f"**{row['City']} ({row['Year']})** — {row['Water_Shortage_Impact']}")

    st.subheader("💧 Temperature vs Duration Analysis")
    fig6 = px.scatter(
        filtered_df,
        x='Peak_Temp_C',
        y='Duration_Days',
        size='Deaths',
        color='City',
        hover_name='City',
        hover_data=['Year', 'Heatstroke_Cases'],
        title="🔥 Peak Temperature vs Duration (Bubble = Deaths)",
        color_discrete_sequence=px.colors.qualitative.Dark2
    )
    fig6.update_layout(height=500, plot_bgcolor='rgba(0,0,0,0)', font_family="Inter")
    fig6.update_traces(marker=dict(opacity=0.7, line=dict(width=1, color='DarkSlateGrey')))
    st.plotly_chart(fig6, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Raw Data + Download
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
