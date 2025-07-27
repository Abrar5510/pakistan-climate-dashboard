import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page Configuration with Custom Theme

st.set_page_config(
page_title="Pakistan Heatwave Dashboard",
layout="wide",
initial_sidebar_state="expanded",
page_icon="🌡️"
)

# Custom CSS for Beautiful Styling

st.markdown(

<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    .main {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        font-family: 'Poppins', sans-serif;
    }
    
    .main-header {
        background: linear-gradient(90deg, #ff6b6b, #feca57, #48dbfb, #ff9ff3, #54a0ff);
        background-size: 300% 300%;
        animation: gradient 8s ease infinite;
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .main-title {
        font-size: 3.5rem;
        font-weight: 700;
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        margin: 0;
        letter-spacing: -1px;
    }
    
    .main-subtitle {
        font-size: 1.2rem;
        color: rgba(255,255,255,0.9);
        margin-top: 0.5rem;
        font-weight: 300;
    }
    
    .sidebar-header {
        background: linear-gradient(45deg, #ff6b6b, #feca57);
        padding: 1rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
        margin-top: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: 5px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        border-radius: 10px;
        color: white;
        font-weight: 600;
        background: transparent;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(45deg, #ff6b6b, #feca57) !important;
        color: white !important;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    .chart-container {
        background: rgba(255,255,255,0.95);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 15px 35px rgba(0,0,0,0.1);
        backdrop-filter: blur(10px);
    }
    
    .stAlert {
        border-radius: 15px;
        border: none;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .footer {
        background: linear-gradient(90deg, #2c3e50, #34495e);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin-top: 3rem;
        text-align: center;
    }
</style>

‘’’, unsafe_allow_html=True)

@st.cache_data
def load_data():
try:
df = pd.read_csv("pakistan_heatwave_data.csv")
df[‘Year’] = df[‘Year’].astype(str)
df[‘Deaths’] = df[‘Deaths’].fillna(0)
df[‘Heatstroke_Cases’] = df[‘Heatstroke_Cases’].fillna(0)
df[‘Agriculture_Loss_pct’] = df[‘Agriculture_Loss_pct’].fillna(0)
df[‘Livestock_Loss’] = df[‘Livestock_Loss’].fillna("No data available")
df[‘Water_Shortage_Impact’] = df[‘Water_Shortage_Impact’].fillna("No significant impact")
return df
except FileNotFoundError:
st.error("CSV file not found. Please make sure ‘pakistan_heatwave_data.csv’ is in the same directory.")
return pd.DataFrame()

df = load_data()

if df.empty:
st.stop()

# Beautiful Header

st.markdown(’’’

<div class="main-header">
    <h1 class="main-title">🔥 Pakistan Heatwave Analytics</h1>
    <p class="main-subtitle">Advanced Climate Impact Dashboard • Real-time Data Insights</p>
</div>
''', unsafe_allow_html=True)

# Enhanced Sidebar

st.sidebar.markdown(’’’

<div class="sidebar-header">
    <h2 style="color: white; margin: 0; font-size: 1.5rem;">🔍 Smart Filters</h2>
</div>
''', unsafe_allow_html=True)

cities = sorted(df[‘City’].dropna().unique().tolist())
selected_cities = st.sidebar.multiselect(
"🏙️ Select Cities to Compare",
cities,
default=[cities[0]] if cities else [],
help="Choose one or more cities for comparison"
)

years = sorted(df[‘Year’].dropna().unique().tolist())
selected_years = st.sidebar.multiselect(
"📅 Select Years to Compare",
years,
default=years[-2:] if len(years) >= 2 else years,
help="Select years for temporal analysis"
)

# Filter data

if selected_cities and selected_years:
filtered_df = df[(df["City"].isin(selected_cities)) & (df["Year"].isin(selected_years))]
else:
filtered_df = pd.DataFrame()

if filtered_df.empty:
st.markdown(’’’
<div style="background: linear-gradient(45deg, #ff6b6b, #feca57); padding: 2rem; border-radius: 15px; text-align: center; color: white;">
<h2>⚠️ No Data Available</h2>
<p>Please adjust your filters to view the dashboard</p>
</div>
‘’’, unsafe_allow_html=True)
st.stop()

# Enhanced Metrics with Beautiful Cards

st.markdown("### 📊 Dashboard Overview")
col1, col2, col3, col4 = st.columns(4)

with col1:
st.markdown(f’’’
<div class="metric-card">
<div class="metric-value">{len(selected_cities)}</div>
<div class="metric-label">🏙️ Cities Selected</div>
</div>
‘’’, unsafe_allow_html=True)

with col2:
st.markdown(f’’’
<div class="metric-card">
<div class="metric-value">{len(selected_years)}</div>
<div class="metric-label">📅 Years Analyzed</div>
</div>
‘’’, unsafe_allow_html=True)

with col3:
st.markdown(f’’’
<div class="metric-card">
<div class="metric-value">{len(filtered_df)}</div>
<div class="metric-label">📋 Total Records</div>
</div>
‘’’, unsafe_allow_html=True)

with col4:
avg_temp = filtered_df[‘Peak_Temp_C’].mean()
st.markdown(f’’’
<div class="metric-card">
<div class="metric-value">{avg_temp:.1f}°C</div>
<div class="metric-label">🌡️ Avg Peak Temp</div>
</div>
‘’’, unsafe_allow_html=True)

# Enhanced Tabs with Beautiful Content

tab1, tab2, tab3, tab4 = st.tabs([
"🌡️ Temperature Analysis",
"⚕️ Health Impact",
"🌾 Agricultural Impact",
"💧 Water & Climate Crisis"
])

with tab1:
st.markdown(’<div class="chart-container">’, unsafe_allow_html=True)

```
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🔥 Peak Temperature Comparison")
    fig1 = px.bar(
        filtered_df, x='City', y='Peak_Temp_C', color='Year',
        barmode='group', 
        color_discrete_sequence=['#ff6b6b', '#feca57', '#48dbfb', '#ff9ff3', '#54a0ff'],
        labels={'Peak_Temp_C': 'Peak Temperature (°C)'},
        title="Peak Temperature by City and Year"
    )
    fig1.update_traces(
        hovertemplate="<b>%{x}</b><br>🌡️ Temp: %{y}°C<br>📅 Year: %{customdata[0]}<extra></extra>", 
        customdata=filtered_df[['Year']]
    )
    fig1.update_layout(
        height=400, 
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Poppins", size=12),
        title_font_size=16,
        showlegend=True
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown("#### ⏱️ Heatwave Duration")
    fig2 = px.bar(
        filtered_df, x='City', y='Duration_Days', color='Year',
        barmode='group', 
        color_discrete_sequence=['#a55eea', '#26de81', '#fd79a8', '#fdcb6e', '#6c5ce7'],
        labels={'Duration_Days': 'Duration (Days)'},
        title="Heatwave Duration by City and Year"
    )
    fig2.update_traces(
        hovertemplate="<b>%{x}</b><br>⏱️ Duration: %{y} Days<br>📅 Year: %{customdata[0]}<extra></extra>", 
        customdata=filtered_df[['Year']]
    )
    fig2.update_layout(
        height=400, 
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Poppins", size=12),
        title_font_size=16
    )
    st.plotly_chart(fig2, use_container_width=True)

# 3D Surface Plot for Temperature Trends
st.markdown("#### 🌍 Advanced Temperature Analysis")
if len(filtered_df) > 3:
    fig_3d = go.Figure(data=[go.Scatter3d(
        x=filtered_df['City'],
        y=filtered_df['Year'],
        z=filtered_df['Peak_Temp_C'],
        mode='markers+lines',
        marker=dict(
            size=filtered_df['Duration_Days']/2,
            color=filtered_df['Peak_Temp_C'],
            colorscale='Plasma',
            showscale=True,
            colorbar=dict(title="Temperature (°C)")
        ),
        line=dict(color='darkblue', width=2),
        hovertemplate="<b>%{x}</b><br>Year: %{y}<br>Peak Temp: %{z}°C<extra></extra>"
    )])
    
    fig_3d.update_layout(
        title="3D Temperature Analysis (Bubble Size = Duration)",
        scene=dict(
            xaxis_title="City",
            yaxis_title="Year", 
            zaxis_title="Peak Temperature (°C)",
            bgcolor="rgba(0,0,0,0)"
        ),
        height=500,
        font=dict(family="Poppins")
    )
    st.plotly_chart(fig_3d, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)
```

with tab2:
st.markdown(’<div class="chart-container">’, unsafe_allow_html=True)

```
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### ☠️ Heat-Related Deaths")
    fig3 = px.bar(
        filtered_df, x='City', y='Deaths', color='Year',
        barmode='group', 
        color_discrete_sequence=['#ff6b6b', '#ff7675', '#fd79a8', '#fdcb6e'],
        title="Deaths from Heatwaves"
    )
    fig3.update_traces(
        hovertemplate="<b>%{x}</b><br>☠️ Deaths: %{y}<br>📅 Year: %{customdata[0]}<extra></extra>", 
        customdata=filtered_df[['Year']]
    )
    fig3.update_layout(
        height=400, 
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Poppins")
    )
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.markdown("#### 🏥 Heatstroke Cases")
    fig4 = px.bar(
        filtered_df, x='City', y='Heatstroke_Cases', color='Year',
        barmode='group', 
        color_discrete_sequence=['#fd79a8', '#fdcb6e', '#e17055', '#a29bfe'],
        title="Heatstroke Cases Reported"
    )
    fig4.update_traces(
        hovertemplate="<b>%{x}</b><br>🏥 Cases: %{y}<br>📅 Year: %{customdata[0]}<extra></extra>", 
        customdata=filtered_df[['Year']]
    )
    fig4.update_layout(
        height=400, 
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Poppins")
    )
    st.plotly_chart(fig4, use_container_width=True)

# Combined Health Impact Chart
st.markdown("#### 📊 Combined Health Impact Analysis")
fig_combined = make_subplots(
    rows=1, cols=2,
    subplot_titles=('Deaths vs Temperature', 'Heatstroke Cases vs Duration'),
    specs=[[{"secondary_y": False}, {"secondary_y": False}]]
)

fig_combined.add_trace(
    go.Scatter(x=filtered_df['Peak_Temp_C'], y=filtered_df['Deaths'],
              mode='markers', name='Deaths vs Temp',
              marker=dict(size=10, color='red', opacity=0.7)),
    row=1, col=1
)

fig_combined.add_trace(
    go.Scatter(x=filtered_df['Duration_Days'], y=filtered_df['Heatstroke_Cases'],
              mode='markers', name='Cases vs Duration',
              marker=dict(size=10, color='orange', opacity=0.7)),
    row=1, col=2
)

fig_combined.update_layout(
    height=400,
    font=dict(family="Poppins"),
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)'
)
st.plotly_chart(fig_combined, use_container_width=True)

# Health Summary Table
st.markdown("#### 📋 Health Impact Summary")
health_summary = filtered_df.groupby(['City', 'Year']).agg({
    'Deaths': 'sum',
    'Heatstroke_Cases': 'sum',
    'Peak_Temp_C': 'max'
}).reset_index()

# Style the dataframe
st.dataframe(
    health_summary.style.background_gradient(cmap='Reds', subset=['Deaths'])
                       .background_gradient(cmap='Oranges', subset=['Heatstroke_Cases'])
                       .background_gradient(cmap='YlOrRd', subset=['Peak_Temp_C'])
                       .format({'Peak_Temp_C': '{:.1f}°C'}),
    use_container_width=True
)

st.markdown('</div>', unsafe_allow_html=True)
```

with tab3:
st.markdown(’<div class="chart-container">’, unsafe_allow_html=True)

```
st.markdown("#### 🌾 Agricultural Impact Analysis")

col1, col2 = st.columns(2)

with col1:
    fig5 = px.bar(
        filtered_df, x='City', y='Agriculture_Loss_pct', color='Year',
        barmode='group', 
        color_discrete_sequence=['#00b894', '#00cec9', '#6c5ce7', '#a29bfe'],
        labels={'Agriculture_Loss_pct': 'Agriculture Loss (%)'},
        title="Agricultural Losses by City and Year"
    )
    fig5.update_layout(
        height=400, 
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Poppins")
    )
    st.plotly_chart(fig5, use_container_width=True)

with col2:
    # Pie chart for total losses by city
    city_losses = filtered_df.groupby('City')['Agriculture_Loss_pct'].sum().reset_index()
    fig_pie = px.pie(
        city_losses, values='Agriculture_Loss_pct', names='City',
        title="Total Agricultural Losses by City",
        color_discrete_sequence=['#ff6b6b', '#feca57', '#48dbfb', '#ff9ff3', '#54a0ff']
    )
    fig_pie.update_layout(
        height=400,
        font=dict(family="Poppins"),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("#### 🐄 Livestock Impact Reports")
livestock_data = filtered_df[filtered_df['Livestock_Loss'] != "No data available"]
if not livestock_data.empty:
    for _, row in livestock_data.iterrows():
        st.markdown(f'''
        <div style="background: linear-gradient(45deg, #fd79a8, #fdcb6e); padding: 1rem; border-radius: 10px; margin: 0.5rem 0; color: white;">
            <strong>🏙️ {row["City"]} ({row["Year"]})</strong><br>
            🐄 {row["Livestock_Loss"]}
        </div>
        ''', unsafe_allow_html=True)
else:
    st.info("📊 No significant livestock impact data available for selected filters.")

st.markdown('</div>', unsafe_allow_html=True)
```

with tab4:
st.markdown(’<div class="chart-container">’, unsafe_allow_html=True)

```
st.markdown("#### 💧 Water Crisis Impact")
water_data = filtered_df[filtered_df['Water_Shortage_Impact'] != "No significant impact"]
if not water_data.empty:
    for _, row in water_data.iterrows():
        st.markdown(f'''
        <div style="background: linear-gradient(45deg, #48dbfb, #0984e3); padding: 1rem; border-radius: 10px; margin: 0.5rem 0; color: white;">
            <strong>🏙️ {row["City"]} ({row["Year"]})</strong><br>
            💧 {row["Water_Shortage_Impact"]}
        </div>
        ''', unsafe_allow_html=True)
else:
    st.info("📊 No significant water shortage impacts reported for selected filters.")

st.markdown("#### 🔥 Temperature vs Duration Analysis")
fig6 = px.scatter(
    filtered_df,
    x='Peak_Temp_C',
    y='Duration_Days',
    size='Deaths',
    color='City',
    hover_name='City',
    hover_data=['Year', 'Heatstroke_Cases'],
    title="Peak Temperature vs Duration (Bubble Size = Deaths)",
    color_discrete_sequence=['#ff6b6b', '#feca57', '#48dbfb', '#ff9ff3', '#54a0ff']
)
fig6.update_layout(
    height=500, 
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(family="Poppins")
)
fig6.update_traces(
    marker=dict(opacity=0.8, line=dict(width=2, color='white')),
    hovertemplate="<b>%{hovertext}</b><br>🌡️ Peak Temp: %{x}°C<br>⏱️ Duration: %{y} days<br>📅 Year: %{customdata[0]}<br>🏥 Heatstroke Cases: %{customdata[1]}<extra></extra>"
)
st.plotly_chart(fig6, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)
```

# Enhanced Raw Data Section

with st.expander("📋 View & Download Raw Data", expanded=False):
if not filtered_df.empty:
st.markdown("#### 📊 Filtered Dataset")

```
    # Enhanced dataframe with styling
    styled_df = filtered_df.style.background_gradient(cmap='coolwarm', subset=['Peak_Temp_C', 'Duration_Days'])\
                                .background_gradient(cmap='Reds', subset=['Deaths', 'Heatstroke_Cases'])\
                                .background_gradient(cmap='Greens', subset=['Agriculture_Loss_pct'])\
                                .format({'Peak_Temp_C': '{:.1f}°C', 'Agriculture_Loss_pct': '{:.1f}%'})
    
    st.dataframe(styled_df, use_container_width=True)
    
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv,
        file_name=f"pakistan_heatwave_filtered_{'-'.join(selected_cities)}_{'-'.join(selected_years)}.csv",
        mime="text/csv",
        help="Download the current filtered dataset"
    )
else:
    st.info("🔍 No data to display. Please select cities and years from the sidebar.")
```

# Enhanced Summary Statistics

if not filtered_df.empty:
st.markdown("### 📈 Key Insights & Statistics")

```
col1, col2, col3, col4 = st.columns(4)

with col1:
    hottest_temp = filtered_df['Peak_Temp_C'].max()
    hottest = filtered_df.loc[filtered_df['Peak_Temp_C'].idxmax()]
    st.markdown(f'''
    <div class="metric-card"style="background: linear-gradient(45deg, #ff6b6b, #ff7675);">
        <div class="metric-value">{hottest_temp:.1f}°C</div>
        <div class="metric-label">🔥 Highest Temperature</div>
        <div style="font-size: 0.8rem; margin-top: 0.5rem; opacity: 0.8;">
            📍 {hottest["City"]} ({hottest["Year"]})
        </div>
    </div>
    ''', unsafe_allow_html=True)

with col2:
    total_deaths = int(filtered_df['Deaths'].sum())
    st.markdown(f'''
    <div class="metric-card"style="background: linear-gradient(45deg, #fd79a8, #fdcb6e);">
        <div class="metric-value">{total_deaths}</div>
        <div class="metric-label">☠️ Total Deaths</div>
        <div style="font-size: 0.8rem; margin-top: 0.5rem; opacity: 0.8;">
            Across selected data
        </div>
    </div>
    ''', unsafe_allow_html=True)

with col3:
    total_cases = int(filtered_df['Heatstroke_Cases'].sum())
    st.markdown(f'''
    <div class="metric-card"style="background: linear-gradient(45deg, #a55eea, #3742fa);">
        <div class="metric-value">{total_cases}</div>
        <div class="metric-label">🏥 Heatstroke Cases</div>
        <div style="font-size: 0.8rem; margin-top: 0.5rem; opacity: 0.8;">
            Total reported cases
        </div>
    </div>
    ''', unsafe_allow_html=True)

with col4:
    longest_duration = filtered_df['Duration_Days'].max()
    longest = filtered_df.loc[filtered_df['Duration_Days'].idxmax()]
    st.markdown(f'''
    <div class="metric-card"style="background: linear-gradient(45deg, #26de81, #20bf6b);">
        <div class="metric-value">{longest_duration}</div>
        <div class="metric-label">⏱️ Longest Heatwave</div>
        <div style="font-size: 0.8rem; margin-top: 0.5rem; opacity: 0.8;">
            📍 {longest["City"]} ({longest["Year"]})
        </div>
    </div>
    ''', unsafe_allow_html=True)
```

# Beautiful Footer

st.markdown(’’’

<div class="footer">
    <h3 style="margin: 0; color: #ecf0f1;">📊 Pakistan Heatwave Analytics Dashboard</h3>
    <p style="margin: 0.5rem 0; color: #bdc3c7;">Advanced Climate Data Visualization & Analysis Platform</p>
    <hr style="border: 1px solid #34495e; margin: 1rem 0;">
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap;">
        <div>
            <strong>📈 Data Sources:</strong><br>
            Pakistan Meteorological Department • Health Ministry Reports • Agricultural Survey Data
        </div>
        <div style="text-align: right;">
            <strong>🛠️ Built with:</strong><br>
            Streamlit • Plotly • Pandas • Advanced Analytics
        </div>
    </div>
    <p style="margin-top: 1rem; font-size: 0.9rem; color: #95a5a6;">
        Last Updated: 2025 • Real-time Climate Monitoring System
    </p>
</div>
''', unsafe_allow_html=True)
