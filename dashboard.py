import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Pakistan Climate Dashboard",
    layout="wide",
    page_icon="🌡️",
    initial_sidebar_state="expanded"
)

# ╔══════════════════════════════════════════════════════════════════╗
# ║                    LIQUID GLASS CSS DESIGN                      ║
# ╚══════════════════════════════════════════════════════════════════╝
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
        font-family: 'Inter', sans-serif !important;
    }

    /* ── Aurora Background ── */
    .stApp {
        background:
            radial-gradient(ellipse at 12% 38%, rgba(168, 85, 247, 0.14) 0%, transparent 52%),
            radial-gradient(ellipse at 88% 12%, rgba(239, 68, 68, 0.13) 0%, transparent 52%),
            radial-gradient(ellipse at 52% 92%, rgba(59, 130, 246, 0.12) 0%, transparent 52%),
            radial-gradient(ellipse at 72% 58%, rgba(16, 185, 129, 0.08) 0%, transparent 44%),
            radial-gradient(ellipse at 35% 75%, rgba(251, 191, 36, 0.06) 0%, transparent 40%),
            linear-gradient(160deg, #06091a 0%, #0b0f22 50%, #07091a 100%) !important;
        min-height: 100vh !important;
    }

    /* ── Sidebar: Liquid Glass ── */
    [data-testid="stSidebar"] {
        background: rgba(6, 9, 26, 0.65) !important;
        backdrop-filter: blur(32px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(32px) saturate(180%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.07) !important;
        box-shadow: 4px 0 40px rgba(0, 0, 0, 0.4) !important;
    }
    [data-testid="stSidebar"] * { color: rgba(255,255,255,0.75) !important; }
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3 { color: rgba(255,255,255,0.9) !important; }

    /* ── Hero Header ── */
    .hero-header {
        position: relative;
        background: linear-gradient(145deg,
            rgba(255, 255, 255, 0.09) 0%,
            rgba(255, 255, 255, 0.04) 60%,
            rgba(255, 255, 255, 0.02) 100%);
        backdrop-filter: blur(40px) saturate(200%);
        -webkit-backdrop-filter: blur(40px) saturate(200%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 28px;
        padding: 3.25rem 2.5rem 2.75rem;
        margin-bottom: 2rem;
        text-align: center;
        overflow: hidden;
        box-shadow:
            0 30px 80px rgba(0, 0, 0, 0.55),
            inset 0 1.5px 0 rgba(255, 255, 255, 0.14),
            inset 0 -1px 0 rgba(0, 0, 0, 0.3);
    }

    /* Inner aurora glow */
    .hero-header::before {
        content: '';
        position: absolute;
        inset: 0;
        background:
            radial-gradient(ellipse at 25% -10%, rgba(239, 68, 68, 0.18) 0%, transparent 55%),
            radial-gradient(ellipse at 85% 110%, rgba(168, 85, 247, 0.15) 0%, transparent 55%);
        pointer-events: none;
        border-radius: 28px;
    }

    /* Specular top highlight */
    .hero-header::after {
        content: '';
        position: absolute;
        top: 0; left: 8%; right: 8%;
        height: 1px;
        background: linear-gradient(90deg,
            transparent 0%,
            rgba(255, 255, 255, 0.4) 50%,
            transparent 100%);
    }

    .hero-badge {
        display: inline-block;
        background: rgba(239, 68, 68, 0.14);
        border: 1px solid rgba(239, 68, 68, 0.32);
        color: #f87171;
        padding: 0.28rem 0.9rem;
        border-radius: 100px;
        font-size: 0.68rem;
        font-weight: 700;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        margin-bottom: 1.2rem;
        position: relative;
        z-index: 1;
        box-shadow: 0 0 24px rgba(239, 68, 68, 0.18);
    }

    .hero-title {
        font-size: 3.5rem;
        font-weight: 900;
        margin: 0;
        background: linear-gradient(145deg, #ffffff 0%, rgba(255,255,255,0.55) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        letter-spacing: -0.04em;
        line-height: 1.1;
        position: relative;
        z-index: 1;
    }

    .hero-subtitle {
        font-size: 0.85rem;
        font-weight: 400;
        margin-top: 0.8rem;
        color: rgba(255, 255, 255, 0.32) !important;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        position: relative;
        z-index: 1;
    }

    /* ── Liquid Glass Metric Cards ── */
    .glass-card {
        background: linear-gradient(150deg,
            rgba(255, 255, 255, 0.09) 0%,
            rgba(255, 255, 255, 0.04) 100%);
        backdrop-filter: blur(24px) saturate(200%);
        -webkit-backdrop-filter: blur(24px) saturate(200%);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 22px;
        padding: 1.75rem 1.5rem;
        margin: 0.35rem 0;
        transition: transform 0.35s cubic-bezier(0.4, 0, 0.2, 1),
                    box-shadow 0.35s cubic-bezier(0.4, 0, 0.2, 1),
                    border-color 0.35s ease;
        box-shadow:
            0 12px 40px rgba(0, 0, 0, 0.35),
            inset 0 1.5px 0 rgba(255, 255, 255, 0.14),
            inset 0 -1px 0 rgba(0, 0, 0, 0.22);
        position: relative;
        overflow: hidden;
        text-align: center;
    }

    /* Top specular edge light */
    .glass-card::before {
        content: '';
        position: absolute;
        top: 0; left: 12%; right: 12%;
        height: 1px;
        background: linear-gradient(90deg,
            transparent,
            rgba(255, 255, 255, 0.35),
            transparent);
    }

    /* Subtle inner glow blob */
    .glass-card::after {
        content: '';
        position: absolute;
        top: -30%;
        left: 50%;
        transform: translateX(-50%);
        width: 60%;
        height: 60%;
        background: radial-gradient(ellipse, rgba(255,255,255,0.04) 0%, transparent 70%);
        pointer-events: none;
    }

    .glass-card:hover {
        transform: translateY(-6px) scale(1.02);
        border-color: rgba(255, 255, 255, 0.2);
        box-shadow:
            0 28px 64px rgba(0, 0, 0, 0.48),
            0 0 48px rgba(168, 85, 247, 0.1),
            inset 0 1.5px 0 rgba(255, 255, 255, 0.2),
            inset 0 -1px 0 rgba(0, 0, 0, 0.2);
    }

    .metric-icon { font-size: 1.5rem; display: block; line-height: 1; }
    .metric-value {
        font-size: 2.6rem;
        font-weight: 800;
        margin: 0.45rem 0 0;
        color: rgba(255, 255, 255, 0.95);
        letter-spacing: -0.045em;
        line-height: 1;
        position: relative;
        z-index: 1;
    }
    .metric-label {
        font-size: 0.7rem;
        color: rgba(255, 255, 255, 0.35);
        margin-top: 0.55rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.12em;
    }
    .metric-accent {
        height: 2px;
        border-radius: 100px;
        margin: 0.8rem auto 0;
        width: 36px;
    }

    /* ── Chart Glass Container ── */
    .chart-glass {
        background: linear-gradient(150deg,
            rgba(255, 255, 255, 0.06) 0%,
            rgba(255, 255, 255, 0.02) 100%);
        backdrop-filter: blur(20px) saturate(160%);
        -webkit-backdrop-filter: blur(20px) saturate(160%);
        border: 1px solid rgba(255, 255, 255, 0.07);
        border-radius: 20px;
        padding: 1.5rem 1.5rem 0.75rem;
        margin: 0.75rem 0;
        box-shadow:
            0 8px 32px rgba(0, 0, 0, 0.3),
            inset 0 1px 0 rgba(255, 255, 255, 0.09);
        position: relative;
        overflow: hidden;
    }
    .chart-glass::before {
        content: '';
        position: absolute;
        top: 0; left: 18%; right: 18%;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.18), transparent);
    }
    .chart-title {
        font-size: 0.95rem !important;
        font-weight: 700 !important;
        color: rgba(255, 255, 255, 0.9) !important;
        margin: 0 0 0.1rem !important;
        letter-spacing: -0.01em;
    }
    .chart-meta {
        font-size: 0.7rem !important;
        color: rgba(255, 255, 255, 0.28) !important;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        margin-bottom: 0.5rem !important;
    }

    /* ── Info / Warning Pills ── */
    .info-pill {
        background: rgba(59, 130, 246, 0.08);
        border: 1px solid rgba(59, 130, 246, 0.2);
        border-radius: 14px;
        padding: 0.85rem 1.25rem;
        margin: 0.4rem 0;
        color: rgba(255, 255, 255, 0.72) !important;
        font-size: 0.875rem;
        line-height: 1.5;
        box-shadow: inset 0 1px 0 rgba(59,130,246,0.1);
    }
    .warning-pill {
        background: rgba(245, 158, 11, 0.08);
        border: 1px solid rgba(245, 158, 11, 0.2);
        border-radius: 14px;
        padding: 0.85rem 1.25rem;
        margin: 0.4rem 0;
        color: rgba(255, 255, 255, 0.72) !important;
        font-size: 0.875rem;
        line-height: 1.5;
        box-shadow: inset 0 1px 0 rgba(245,158,11,0.1);
    }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255, 255, 255, 0.04) !important;
        border-radius: 16px !important;
        padding: 5px !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        gap: 3px !important;
        backdrop-filter: blur(12px) !important;
        margin-bottom: 1.25rem !important;
    }
    .stTabs [data-baseweb="tab"] {
        color: rgba(255, 255, 255, 0.42) !important;
        background: transparent !important;
        border-radius: 12px !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
        padding: 0.55rem 1.35rem !important;
        transition: all 0.25s ease !important;
        border: none !important;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg,
            rgba(255,255,255,0.13) 0%,
            rgba(255,255,255,0.06) 100%) !important;
        color: rgba(255, 255, 255, 0.95) !important;
        box-shadow:
            0 2px 14px rgba(0,0,0,0.25),
            inset 0 1px 0 rgba(255,255,255,0.16) !important;
    }
    .stTabs [data-baseweb="tab-highlight"],
    .stTabs [data-baseweb="tab-border"] { display: none !important; }

    /* ── st.metric ── */
    [data-testid="stMetric"] {
        background: linear-gradient(150deg,
            rgba(255,255,255,0.07) 0%,
            rgba(255,255,255,0.02) 100%) !important;
        border-radius: 18px !important;
        padding: 1.5rem !important;
        border: 1px solid rgba(255,255,255,0.07) !important;
        box-shadow:
            0 4px 20px rgba(0,0,0,0.22),
            inset 0 1px 0 rgba(255,255,255,0.08) !important;
        backdrop-filter: blur(16px) !important;
    }
    [data-testid="stMetricValue"] {
        color: rgba(255,255,255,0.95) !important;
        font-weight: 800 !important;
        font-family: 'Inter', sans-serif !important;
        letter-spacing: -0.02em !important;
    }
    [data-testid="stMetricLabel"] {
        color: rgba(255,255,255,0.38) !important;
        font-size: 0.74rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
        font-weight: 600 !important;
    }
    [data-testid="stMetricDelta"] {
        font-size: 0.8rem !important;
        font-weight: 500 !important;
    }

    /* ── Expander ── */
    .streamlit-expanderHeader {
        background: rgba(255,255,255,0.04) !important;
        border-radius: 14px !important;
        border: 1px solid rgba(255,255,255,0.07) !important;
        color: rgba(255,255,255,0.65) !important;
        font-weight: 500 !important;
        font-family: 'Inter', sans-serif !important;
        backdrop-filter: blur(10px) !important;
    }
    .streamlit-expanderContent {
        border: 1px solid rgba(255,255,255,0.05) !important;
        border-top: none !important;
        border-radius: 0 0 14px 14px !important;
        background: rgba(255,255,255,0.02) !important;
    }

    /* ── Download Button ── */
    .stDownloadButton > button {
        background: linear-gradient(135deg,
            rgba(255,255,255,0.1) 0%,
            rgba(255,255,255,0.05) 100%) !important;
        border: 1px solid rgba(255,255,255,0.15) !important;
        color: rgba(255,255,255,0.85) !important;
        border-radius: 12px !important;
        font-weight: 500 !important;
        font-family: 'Inter', sans-serif !important;
        backdrop-filter: blur(10px) !important;
        transition: all 0.25s ease !important;
        box-shadow: inset 0 1px 0 rgba(255,255,255,0.1) !important;
    }
    .stDownloadButton > button:hover {
        background: linear-gradient(135deg,
            rgba(255,255,255,0.16) 0%,
            rgba(255,255,255,0.08) 100%) !important;
        border-color: rgba(255,255,255,0.25) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(0,0,0,0.25),
                    inset 0 1px 0 rgba(255,255,255,0.15) !important;
    }

    /* ── Section Label ── */
    .section-label {
        font-size: 0.66rem;
        font-weight: 700;
        color: rgba(255,255,255,0.26);
        text-transform: uppercase;
        letter-spacing: 0.17em;
        margin: 1.5rem 0 1rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    .section-label::after {
        content: '';
        flex: 1;
        height: 1px;
        background: linear-gradient(90deg, rgba(255,255,255,0.07) 0%, transparent 100%);
    }

    /* ── Sidebar control label ── */
    .sidebar-title {
        font-size: 0.68rem;
        font-weight: 700;
        color: rgba(255,255,255,0.28);
        text-transform: uppercase;
        letter-spacing: 0.15em;
        padding-bottom: 0.75rem;
        border-bottom: 1px solid rgba(255,255,255,0.06);
        margin-bottom: 1.5rem;
    }

    /* ── Footer ── */
    .dashboard-footer {
        text-align: center;
        padding: 2rem 1rem 1.5rem;
        color: rgba(255,255,255,0.18) !important;
        font-size: 0.76rem;
        letter-spacing: 0.07em;
        border-top: 1px solid rgba(255,255,255,0.05);
        margin-top: 3rem;
    }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 5px; height: 5px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.08); border-radius: 100px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.16); }

    /* ── Hide default Streamlit chrome ── */
    #MainMenu, footer, header { visibility: hidden; }
    [data-testid="stToolbar"] { display: none; }

    /* ── Typography overrides ── */
    .stMarkdown p { color: rgba(255,255,255,0.7) !important; }
    .stCaption, [data-testid="stCaptionContainer"] { color: rgba(255,255,255,0.3) !important; }
    h1, h2, h3, h4 {
        color: rgba(255,255,255,0.9) !important;
        font-family: 'Inter', sans-serif !important;
        letter-spacing: -0.02em;
    }
    .stDataFrame thead th {
        background: rgba(255,255,255,0.06) !important;
        color: rgba(255,255,255,0.65) !important;
    }
    .stDataFrame { border-radius: 12px !important; overflow: hidden !important; }

    /* ── Multiselect tags ── */
    [data-baseweb="tag"] {
        background: rgba(168,85,247,0.2) !important;
        border: 1px solid rgba(168,85,247,0.35) !important;
        border-radius: 8px !important;
        color: rgba(255,255,255,0.85) !important;
    }

    /* Remove top padding from main block */
    .block-container { padding-top: 1.5rem !important; }
</style>
""", unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════════════╗
# ║                         DATA LOADING                            ║
# ╚══════════════════════════════════════════════════════════════════╝
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
        st.error("CSV file not found. Please ensure 'pakistan_heatwave_data.csv' is in the same directory.")
        return pd.DataFrame()

df = load_data()
if df.empty:
    st.stop()


# ╔══════════════════════════════════════════════════════════════════╗
# ║                      CHART THEME HELPER                         ║
# ╚══════════════════════════════════════════════════════════════════╝
def dark_chart(fig, height=460):
    """Apply consistent dark liquid-glass chart theme."""
    fig.update_layout(
        height=height,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Inter, sans-serif", color='rgba(255,255,255,0.55)', size=12),
        xaxis=dict(
            gridcolor='rgba(255,255,255,0.04)',
            zeroline=False,
            tickfont=dict(color='rgba(255,255,255,0.42)', size=11),
            title_font=dict(color='rgba(255,255,255,0.45)', size=12),
            linecolor='rgba(255,255,255,0.06)',
            tickcolor='rgba(255,255,255,0.06)',
        ),
        yaxis=dict(
            gridcolor='rgba(255,255,255,0.04)',
            zeroline=False,
            tickfont=dict(color='rgba(255,255,255,0.42)', size=11),
            title_font=dict(color='rgba(255,255,255,0.45)', size=12),
            linecolor='rgba(255,255,255,0.06)',
            tickcolor='rgba(255,255,255,0.06)',
        ),
        legend=dict(
            bgcolor='rgba(255,255,255,0.04)',
            bordercolor='rgba(255,255,255,0.08)',
            borderwidth=1,
            font=dict(color='rgba(255,255,255,0.6)', size=11),
        ),
        hoverlabel=dict(
            bgcolor='rgba(8, 12, 32, 0.96)',
            bordercolor='rgba(255,255,255,0.14)',
            font=dict(family="Inter", color='white', size=13),
        ),
        margin=dict(l=10, r=10, t=10, b=10),
        bargap=0.28,
        bargroupgap=0.12,
    )
    return fig


# ╔══════════════════════════════════════════════════════════════════╗
# ║                         HERO HEADER                             ║
# ╚══════════════════════════════════════════════════════════════════╝
st.markdown("""
<div class="hero-header">
    <div class="hero-badge">Live Analysis &nbsp;·&nbsp; 2022–2025 Data</div>
    <h1 class="hero-title">🌡️ Pakistan Climate<br>Impact Dashboard</h1>
    <p class="hero-subtitle">Advanced Heatwave Analysis &nbsp;·&nbsp; Meteorological &amp; Health Intelligence</p>
</div>
""", unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════════════╗
# ║                           SIDEBAR                               ║
# ╚══════════════════════════════════════════════════════════════════╝
st.sidebar.markdown('<div class="sidebar-title">Dashboard Controls</div>', unsafe_allow_html=True)

cities = sorted(df['City'].dropna().unique().tolist())
selected_cities = st.sidebar.multiselect(
    "Cities", cities,
    default=[cities[0]] if cities else [],
    help="Select one or more Pakistani cities to analyze"
)

years = sorted(df['Year'].dropna().unique().tolist())
selected_years = st.sidebar.multiselect(
    "Years", years,
    default=years[-2:] if len(years) >= 2 else years,
    help="Select one or more years to compare"
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    '<p style="font-size:0.72rem; color:rgba(255,255,255,0.25); text-align:center; '
    'letter-spacing:0.06em; margin-top:0.5rem;">Pakistan Meteorological Dept<br>'
    'Health Ministry Reports</p>',
    unsafe_allow_html=True
)


# ── Filter data ──────────────────────────────────────────────────
if selected_cities and selected_years:
    filtered_df = df[df["City"].isin(selected_cities) & df["Year"].isin(selected_years)]
else:
    filtered_df = pd.DataFrame()

if filtered_df.empty:
    st.warning("⚠️ No data for selected filters. Please choose at least one city and year.")
    st.stop()


# ╔══════════════════════════════════════════════════════════════════╗
# ║                        METRIC CARDS                             ║
# ╚══════════════════════════════════════════════════════════════════╝
st.markdown('<div class="section-label">Overview</div>', unsafe_allow_html=True)

avg_temp = filtered_df['Peak_Temp_C'].mean()
total_deaths = int(filtered_df['Deaths'].sum())
total_cases = int(filtered_df['Heatstroke_Cases'].sum())
max_temp = filtered_df['Peak_Temp_C'].max()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="glass-card">
        <span class="metric-icon">🏙️</span>
        <div class="metric-value">{len(selected_cities)}</div>
        <div class="metric-label">Cities Analysed</div>
        <div class="metric-accent" style="background: linear-gradient(90deg, #a855f7, #7c3aed);"></div>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="glass-card">
        <span class="metric-icon">📅</span>
        <div class="metric-value">{len(selected_years)}</div>
        <div class="metric-label">Years Selected</div>
        <div class="metric-accent" style="background: linear-gradient(90deg, #3b82f6, #1d4ed8);"></div>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="glass-card">
        <span class="metric-icon">🌡️</span>
        <div class="metric-value">{avg_temp:.1f}°</div>
        <div class="metric-label">Avg Peak Temp (°C)</div>
        <div class="metric-accent" style="background: linear-gradient(90deg, #ef4444, #dc2626);"></div>
    </div>""", unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="glass-card">
        <span class="metric-icon">💀</span>
        <div class="metric-value">{total_deaths:,}</div>
        <div class="metric-label">Total Deaths</div>
        <div class="metric-accent" style="background: linear-gradient(90deg, #f97316, #ea580c);"></div>
    </div>""", unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════════════╗
# ║                            TABS                                 ║
# ╚══════════════════════════════════════════════════════════════════╝
st.markdown('<div class="section-label">Analysis Modules</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "📊  Temperature",
    "⚕️  Health Impact",
    "🌾  Agriculture",
    "💧  Water Crisis",
])


# ── TAB 1: Temperature Analysis ─────────────────────────────────
with tab1:
    # Color palette: fire
    fire_colors = ['#ff9a3c', '#ff6b35', '#f43f5e', '#be123c', '#9d174d',
                   '#7c3aed', '#4f46e5', '#0891b2']

    # Chart 1 — Peak Temperature
    st.markdown("""
    <div class="chart-glass">
        <div class="chart-title">Peak Temperature Comparison</div>
        <div class="chart-meta">Maximum recorded temperature &nbsp;·&nbsp; °Celsius by city &amp; year</div>
    """, unsafe_allow_html=True)

    fig1 = px.bar(
        filtered_df, x='City', y='Peak_Temp_C', color='Year',
        barmode='group',
        color_discrete_sequence=fire_colors,
        labels={'Peak_Temp_C': 'Peak Temp (°C)', 'City': ''},
    )
    fig1.update_traces(
        hovertemplate="<b>%{x}</b><br>Peak Temp: <b>%{y:.1f}°C</b><extra></extra>",
        marker_line_width=0,
        marker_opacity=0.9,
    )
    dark_chart(fig1, height=400)
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Chart 2 — Heatwave Duration
    st.markdown("""
    <div class="chart-glass">
        <div class="chart-title">Heatwave Duration</div>
        <div class="chart-meta">Consecutive days above danger threshold &nbsp;·&nbsp; by city &amp; year</div>
    """, unsafe_allow_html=True)

    plasma_colors = ['#f0f921', '#fca636', '#e16462', '#b12a90', '#6a00a8', '#0d0887']
    fig2 = px.bar(
        filtered_df, x='City', y='Duration_Days', color='Year',
        barmode='group',
        color_discrete_sequence=plasma_colors,
        labels={'Duration_Days': 'Duration (Days)', 'City': ''},
    )
    fig2.update_traces(
        hovertemplate="<b>%{x}</b><br>Duration: <b>%{y} days</b><extra></extra>",
        marker_line_width=0,
        marker_opacity=0.9,
    )
    dark_chart(fig2, height=400)
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ── TAB 2: Health Impact ────────────────────────────────────────
with tab2:
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("""
        <div class="chart-glass">
            <div class="chart-title">Heat-related Deaths</div>
            <div class="chart-meta">Fatalities attributed to heatwave events</div>
        """, unsafe_allow_html=True)

        red_palette = ['#fecaca', '#f87171', '#ef4444', '#dc2626', '#b91c1c', '#7f1d1d']
        fig3 = px.bar(
            filtered_df, x='City', y='Deaths', color='Year',
            barmode='group',
            color_discrete_sequence=red_palette,
            labels={'Deaths': 'Deaths', 'City': ''},
        )
        fig3.update_traces(
            hovertemplate="<b>%{x}</b><br>Deaths: <b>%{y:,}</b><extra></extra>",
            marker_line_width=0, marker_opacity=0.9,
        )
        dark_chart(fig3, height=360)
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_b:
        st.markdown("""
        <div class="chart-glass">
            <div class="chart-title">Heatstroke Cases</div>
            <div class="chart-meta">Reported heatstroke hospitalisations</div>
        """, unsafe_allow_html=True)

        orange_palette = ['#fed7aa', '#fb923c', '#f97316', '#ea580c', '#c2410c', '#7c2d12']
        fig4 = px.bar(
            filtered_df, x='City', y='Heatstroke_Cases', color='Year',
            barmode='group',
            color_discrete_sequence=orange_palette,
            labels={'Heatstroke_Cases': 'Cases', 'City': ''},
        )
        fig4.update_traces(
            hovertemplate="<b>%{x}</b><br>Cases: <b>%{y:,}</b><extra></extra>",
            marker_line_width=0, marker_opacity=0.9,
        )
        dark_chart(fig4, height=360)
        st.plotly_chart(fig4, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # Health summary table
    st.markdown("""
    <div class="chart-glass">
        <div class="chart-title">Health Impact Summary</div>
        <div class="chart-meta">Aggregated health metrics across selected filters</div>
    """, unsafe_allow_html=True)
    health_summary = filtered_df.groupby(['City', 'Year']).agg(
        Deaths=('Deaths', 'sum'),
        Heatstroke_Cases=('Heatstroke_Cases', 'sum'),
        Peak_Temp_C=('Peak_Temp_C', 'max')
    ).reset_index()
    st.dataframe(health_summary, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ── TAB 3: Agricultural Impact ──────────────────────────────────
with tab3:
    st.markdown("""
    <div class="chart-glass">
        <div class="chart-title">Agricultural Loss (%)</div>
        <div class="chart-meta">Estimated crop yield loss attributed to heatwave stress</div>
    """, unsafe_allow_html=True)

    green_palette = ['#d1fae5', '#6ee7b7', '#34d399', '#10b981', '#059669', '#064e3b']
    fig5 = px.bar(
        filtered_df, x='City', y='Agriculture_Loss_pct', color='Year',
        barmode='group',
        color_discrete_sequence=green_palette,
        labels={'Agriculture_Loss_pct': 'Loss (%)', 'City': ''},
    )
    fig5.update_traces(
        hovertemplate="<b>%{x}</b><br>Loss: <b>%{y:.1f}%</b><extra></extra>",
        marker_line_width=0, marker_opacity=0.9,
    )
    dark_chart(fig5, height=420)
    st.plotly_chart(fig5, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="section-label">Livestock Impact Reports</div>', unsafe_allow_html=True)
    has_livestock = False
    for _, row in filtered_df.iterrows():
        if row['Livestock_Loss'] != "No data available":
            st.markdown(
                f'<div class="info-pill"><strong>{row["City"]} ({row["Year"]})</strong>'
                f' — {row["Livestock_Loss"]}</div>',
                unsafe_allow_html=True
            )
            has_livestock = True
    if not has_livestock:
        st.markdown('<div class="info-pill">No livestock impact data for selected filters.</div>',
                    unsafe_allow_html=True)


# ── TAB 4: Water Crisis ─────────────────────────────────────────
with tab4:
    st.markdown('<div class="section-label">Water Shortage Reports</div>', unsafe_allow_html=True)
    has_water = False
    for _, row in filtered_df.iterrows():
        if row['Water_Shortage_Impact'] != "No significant impact":
            st.markdown(
                f'<div class="warning-pill"><strong>{row["City"]} ({row["Year"]})</strong>'
                f' — {row["Water_Shortage_Impact"]}</div>',
                unsafe_allow_html=True
            )
            has_water = True
    if not has_water:
        st.markdown('<div class="warning-pill">No significant water shortage data for selected filters.</div>',
                    unsafe_allow_html=True)

    # Bubble chart
    st.markdown("""
    <div class="chart-glass">
        <div class="chart-title">Temperature vs Duration</div>
        <div class="chart-meta">Bubble size represents deaths &nbsp;·&nbsp; colour by city</div>
    """, unsafe_allow_html=True)

    bubble_colors = ['#818cf8', '#f472b6', '#34d399', '#fbbf24', '#60a5fa', '#f87171']
    fig6 = px.scatter(
        filtered_df,
        x='Peak_Temp_C',
        y='Duration_Days',
        size='Deaths',
        color='City',
        hover_name='City',
        hover_data={'Year': True, 'Heatstroke_Cases': True, 'Deaths': True,
                    'Peak_Temp_C': ':.1f', 'Duration_Days': True},
        color_discrete_sequence=bubble_colors,
        labels={'Peak_Temp_C': 'Peak Temperature (°C)', 'Duration_Days': 'Duration (Days)'},
        size_max=60,
    )
    fig6.update_traces(
        marker=dict(opacity=0.8, line=dict(width=1, color='rgba(255,255,255,0.15)')),
        hovertemplate=(
            "<b>%{hovertext}</b> (%{customdata[0]})<br>"
            "Temp: <b>%{x:.1f}°C</b>  ·  Duration: <b>%{y} days</b><br>"
            "Deaths: <b>%{customdata[2]:,}</b>  ·  Heatstroke: <b>%{customdata[1]:,}</b>"
            "<extra></extra>"
        ),
    )
    dark_chart(fig6, height=460)
    st.plotly_chart(fig6, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ╔══════════════════════════════════════════════════════════════════╗
# ║                       RAW DATA EXPORT                           ║
# ╚══════════════════════════════════════════════════════════════════╝
st.markdown('<div class="section-label">Data</div>', unsafe_allow_html=True)
with st.expander("📋  View & Export Raw Data"):
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)
    csv = filtered_df.to_csv(index=False)
    fname = f"pakistan_heatwave_{'_'.join(selected_cities)}_{'_'.join(selected_years)}.csv"
    st.download_button(
        label="📥  Download Filtered Data as CSV",
        data=csv,
        file_name=fname,
        mime="text/csv"
    )


# ╔══════════════════════════════════════════════════════════════════╗
# ║                      SUMMARY STATISTICS                         ║
# ╚══════════════════════════════════════════════════════════════════╝
st.markdown('<div class="section-label">Summary Statistics</div>', unsafe_allow_html=True)

s1, s2, s3, s4 = st.columns(4)

hottest = filtered_df.loc[filtered_df['Peak_Temp_C'].idxmax()]
longest = filtered_df.loc[filtered_df['Duration_Days'].idxmax()]

with s1:
    st.metric(
        "🌡️  Highest Temperature",
        f"{filtered_df['Peak_Temp_C'].max():.1f}°C",
        help=f"Recorded in {hottest['City']} ({hottest['Year']})"
    )
    st.caption(f"in {hottest['City']} ({hottest['Year']})")

with s2:
    st.metric(
        "💀  Total Deaths",
        f"{int(filtered_df['Deaths'].sum()):,}",
        help="Across all selected cities and years"
    )
    st.caption("across selected filters")

with s3:
    st.metric(
        "🏥  Heatstroke Cases",
        f"{int(filtered_df['Heatstroke_Cases'].sum()):,}",
        help="Total reported heatstroke hospitalisations"
    )
    st.caption("across selected filters")

with s4:
    st.metric(
        "⏱️  Longest Heatwave",
        f"{int(filtered_df['Duration_Days'].max())} days",
        help=f"Occurred in {longest['City']} ({longest['Year']})"
    )
    st.caption(f"in {longest['City']} ({longest['Year']})")


# ╔══════════════════════════════════════════════════════════════════╗
# ║                           FOOTER                                ║
# ╚══════════════════════════════════════════════════════════════════╝
st.markdown("""
<div class="dashboard-footer">
    Pakistan Meteorological Department &nbsp;·&nbsp; Health Ministry Reports &nbsp;·&nbsp; 2022–2025
</div>
""", unsafe_allow_html=True)
