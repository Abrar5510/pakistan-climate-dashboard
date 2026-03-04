import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Pakistan Climate Dashboard",
    layout="wide",
    page_icon="🌡️",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════
#   VOLCANIC INFERNO — LIQUID GLASS DESIGN SYSTEM
# ══════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* ─── GLOBAL ─────────────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [data-testid="stAppViewContainer"],
[data-testid="stApp"], .main { font-family: 'Inter', sans-serif !important; }
.block-container { padding-top: 1.5rem !important; max-width: 1400px; }

/* ─── VOLCANIC AURORA BACKGROUND ─────────────────────────────── */
.stApp {
    background:
        radial-gradient(ellipse at 18% 22%, rgba(255, 80,  0, 0.20) 0%, transparent 48%),
        radial-gradient(ellipse at 82% 78%, rgba(255, 160, 0, 0.16) 0%, transparent 48%),
        radial-gradient(ellipse at 65%  8%, rgba(220, 30, 30, 0.14) 0%, transparent 44%),
        radial-gradient(ellipse at 10% 82%, rgba(251,180, 36, 0.10) 0%, transparent 42%),
        radial-gradient(ellipse at 90% 42%, rgba(180, 20, 20, 0.10) 0%, transparent 40%),
        linear-gradient(155deg, #0b0604 0%, #100906 45%, #0c0705 100%) !important;
    min-height: 100vh !important;
}

/* ─── SIDEBAR ─────────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: linear-gradient(175deg, #130a05 0%, #0e0705 100%) !important;
    border-right: 1px solid rgba(255, 110, 0, 0.22) !important;
    box-shadow: 6px 0 50px rgba(0,0,0,0.7) !important;
}

/* Force ALL sidebar text white */
section[data-testid="stSidebar"],
section[data-testid="stSidebar"] *,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] div,
section[data-testid="stSidebar"] label {
    color: rgba(255,255,255,0.88) !important;
    font-family: 'Inter', sans-serif !important;
}

/* Widget labels */
section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p,
section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] {
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.12em !important;
    color: rgba(255,200,100,0.7) !important;
    margin-bottom: 0.4rem !important;
}

/* Multiselect box */
section[data-testid="stSidebar"] [data-baseweb="select"] > div:first-child {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,110,0,0.35) !important;
    border-radius: 12px !important;
    min-height: 44px !important;
    transition: border-color 0.2s ease !important;
}
section[data-testid="stSidebar"] [data-baseweb="select"] > div:first-child:hover {
    border-color: rgba(255,130,0,0.6) !important;
}
section[data-testid="stSidebar"] [data-baseweb="select"] input,
section[data-testid="stSidebar"] [data-baseweb="select"] [class*="placeholder"],
section[data-testid="stSidebar"] [data-baseweb="select"] [class*="singleValue"] {
    color: rgba(255,255,255,0.7) !important;
    caret-color: white !important;
}
section[data-testid="stSidebar"] [data-baseweb="select"] svg { fill: rgba(255,255,255,0.5) !important; }

/* Tags/chips */
section[data-testid="stSidebar"] [data-baseweb="tag"] {
    background: rgba(255,90,0,0.28) !important;
    border: 1px solid rgba(255,120,0,0.45) !important;
    border-radius: 8px !important;
    color: rgba(255,220,160,0.95) !important;
}
section[data-testid="stSidebar"] [data-baseweb="tag"] span { color: rgba(255,220,160,0.9) !important; }
section[data-testid="stSidebar"] [data-baseweb="tag"] [data-baseweb="icon"] svg { fill: rgba(255,200,150,0.7) !important; }

/* ─── HERO ────────────────────────────────────────────────────── */
.hero {
    position: relative;
    overflow: hidden;
    border-radius: 28px;
    padding: 4rem 3rem 3.5rem;
    margin-bottom: 2.25rem;
    text-align: center;
    background: linear-gradient(145deg,
        rgba(255,255,255,0.075) 0%,
        rgba(255,255,255,0.03)  100%);
    backdrop-filter: blur(44px) saturate(180%);
    -webkit-backdrop-filter: blur(44px) saturate(180%);
    border: 1px solid rgba(255,120,0,0.22);
    box-shadow:
        0 40px 110px rgba(0,0,0,0.65),
        0 0 90px rgba(255,70,0,0.07),
        inset 0 1.5px 0 rgba(255,200,100,0.22),
        inset 0 -1px 0 rgba(0,0,0,0.45);
}
/* Inner volcanic glow */
.hero::before {
    content: '';
    position: absolute; inset: 0; border-radius: 28px;
    background:
        radial-gradient(ellipse at 50% -15%, rgba(255,110,0,0.26) 0%, transparent 52%),
        radial-gradient(ellipse at 20% 110%, rgba(220,40,0,0.18) 0%, transparent 52%),
        radial-gradient(ellipse at 80% 110%, rgba(255,160,0,0.14) 0%, transparent 52%);
    pointer-events: none;
}
/* Specular top edge */
.hero::after {
    content: '';
    position: absolute; top: 0; left: 5%; right: 5%; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,200,80,0.55), transparent);
}
.hero-eyebrow {
    position: relative; z-index: 1;
    display: inline-flex; align-items: center; gap: 0.5rem;
    background: rgba(255,80,0,0.14);
    border: 1px solid rgba(255,80,0,0.35);
    color: #ff9040;
    padding: 0.3rem 1rem; border-radius: 100px;
    font-size: 0.68rem; font-weight: 700;
    letter-spacing: 0.14em; text-transform: uppercase;
    margin-bottom: 1.5rem;
    box-shadow: 0 0 32px rgba(255,80,0,0.22), inset 0 1px 0 rgba(255,180,60,0.18);
}
.hero-title {
    position: relative; z-index: 1;
    font-size: 4.2rem; font-weight: 900;
    line-height: 1.04; letter-spacing: -0.045em;
    margin-bottom: 1rem;
    background: linear-gradient(140deg, #ffffff 0%, #ffe0b0 45%, rgba(255,160,60,0.75) 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    filter: drop-shadow(0 0 40px rgba(255,110,0,0.35));
}
.hero-sub {
    position: relative; z-index: 1;
    font-size: 0.85rem; font-weight: 400;
    color: rgba(255,255,255,0.35) !important;
    letter-spacing: 0.14em; text-transform: uppercase;
}

/* ─── LIQUID GLASS METRIC CARDS ──────────────────────────────── */
.g-card {
    position: relative; overflow: hidden;
    border-radius: 22px;
    padding: 1.8rem 1.25rem;
    margin: 0.4rem 0;
    text-align: center;
    background: linear-gradient(150deg,
        rgba(255,255,255,0.085) 0%,
        rgba(255,255,255,0.03)  100%);
    backdrop-filter: blur(28px) saturate(200%);
    -webkit-backdrop-filter: blur(28px) saturate(200%);
    border: 1px solid rgba(255,255,255,0.095);
    box-shadow:
        0 18px 52px rgba(0,0,0,0.44),
        inset 0 1.5px 0 rgba(255,200,100,0.18),
        inset 0 -1px 0 rgba(0,0,0,0.35);
    transition:
        transform  0.32s cubic-bezier(0.34, 1.56, 0.64, 1),
        box-shadow 0.32s ease,
        border-color 0.32s ease;
}
/* Specular top edge */
.g-card::before {
    content: '';
    position: absolute; top: 0; left: 10%; right: 10%; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,200,100,0.32), transparent);
}
.g-card:hover {
    transform: translateY(-7px) scale(1.03);
    border-color: rgba(255,130,0,0.38);
    box-shadow:
        0 32px 80px rgba(0,0,0,0.54),
        0 0 64px rgba(255,90,0,0.14),
        inset 0 1.5px 0 rgba(255,210,100,0.25),
        inset 0 -1px 0 rgba(0,0,0,0.35);
}
.g-icon  { font-size: 1.6rem; line-height: 1; display: block; }
.g-value {
    font-size: 2.9rem; font-weight: 900;
    letter-spacing: -0.05em; line-height: 1;
    margin: 0.4rem 0 0;
    color: #ffffff;
}
.g-label {
    font-size: 0.67rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.14em;
    color: rgba(255,255,255,0.32);
    margin-top: 0.55rem;
}
.g-bar { height: 2px; border-radius: 100px; margin: 0.8rem auto 0; width: 40px; }

/* ─── CHART GLASS CONTAINERS ─────────────────────────────────── */
.c-glass {
    position: relative; overflow: hidden;
    border-radius: 20px;
    padding: 1.5rem 1.5rem 0.5rem;
    margin: 0.75rem 0;
    background: linear-gradient(150deg,
        rgba(255,255,255,0.055) 0%,
        rgba(255,255,255,0.018) 100%);
    backdrop-filter: blur(20px) saturate(160%);
    -webkit-backdrop-filter: blur(20px) saturate(160%);
    border: 1px solid rgba(255,255,255,0.07);
    box-shadow: 0 8px 36px rgba(0,0,0,0.38), inset 0 1px 0 rgba(255,200,80,0.07);
}
.c-glass::before {
    content: '';
    position: absolute; top: 0; left: 15%; right: 15%; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,180,60,0.22), transparent);
}
.c-title { font-size: 1rem; font-weight: 700; color: rgba(255,255,255,0.92) !important; letter-spacing: -0.015em; }
.c-meta  { font-size: 0.7rem; color: rgba(255,255,255,0.28) !important; text-transform: uppercase; letter-spacing: 0.1em; margin: 0.2rem 0 0.4rem; }

/* ─── INFO / WARNING PILLS ───────────────────────────────────── */
.pill-green {
    background: rgba(16,185,129,0.09); border: 1px solid rgba(16,185,129,0.25);
    border-radius: 14px; padding: 0.9rem 1.25rem; margin: 0.4rem 0;
    color: rgba(255,255,255,0.82) !important; font-size: 0.875rem; line-height: 1.55;
    box-shadow: inset 0 1px 0 rgba(16,185,129,0.08);
}
.pill-orange {
    background: rgba(255,100,0,0.09); border: 1px solid rgba(255,100,0,0.25);
    border-radius: 14px; padding: 0.9rem 1.25rem; margin: 0.4rem 0;
    color: rgba(255,255,255,0.82) !important; font-size: 0.875rem; line-height: 1.55;
    box-shadow: inset 0 1px 0 rgba(255,130,0,0.08);
}

/* ─── TABS ────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.04) !important;
    border-radius: 16px !important; padding: 5px !important;
    border: 1px solid rgba(255,100,0,0.14) !important;
    gap: 3px !important; margin-bottom: 1.25rem !important;
    backdrop-filter: blur(12px) !important;
}
.stTabs [data-baseweb="tab"] {
    color: rgba(255,255,255,0.40) !important;
    background: transparent !important; border-radius: 12px !important;
    font-family: 'Inter', sans-serif !important; font-weight: 500 !important;
    font-size: 0.85rem !important; padding: 0.55rem 1.4rem !important;
    transition: all 0.22s ease !important; border: none !important;
}
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(255,100,0,0.22) 0%, rgba(255,60,0,0.12) 100%) !important;
    color: rgba(255,255,255,0.96) !important;
    box-shadow: 0 2px 14px rgba(255,70,0,0.24), inset 0 1px 0 rgba(255,210,100,0.22) !important;
    border: 1px solid rgba(255,110,0,0.24) !important;
}
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] { display: none !important; }

/* ─── ST.METRIC ───────────────────────────────────────────────── */
[data-testid="stMetric"] {
    background: linear-gradient(150deg, rgba(255,255,255,0.07) 0%, rgba(255,255,255,0.025) 100%) !important;
    border-radius: 18px !important; padding: 1.5rem !important;
    border: 1px solid rgba(255,100,0,0.14) !important;
    box-shadow: 0 4px 22px rgba(0,0,0,0.28), inset 0 1px 0 rgba(255,180,60,0.08) !important;
    backdrop-filter: blur(16px) !important;
}
[data-testid="stMetricValue"] {
    color: #ffffff !important; font-weight: 800 !important;
    font-family: 'Inter', sans-serif !important; letter-spacing: -0.025em !important;
}
[data-testid="stMetricLabel"] {
    color: rgba(255,255,255,0.38) !important; font-size: 0.72rem !important;
    text-transform: uppercase !important; letter-spacing: 0.1em !important; font-weight: 600 !important;
}

/* ─── SECTION LABEL ──────────────────────────────────────────── */
.s-label {
    font-size: 0.64rem; font-weight: 700; color: rgba(255,160,50,0.55);
    text-transform: uppercase; letter-spacing: 0.18em;
    margin: 1.75rem 0 1rem;
    display: flex; align-items: center; gap: 0.75rem;
}
.s-label::after {
    content: ''; flex: 1; height: 1px;
    background: linear-gradient(90deg, rgba(255,100,0,0.18) 0%, transparent 100%);
}

/* ─── EXPANDER ───────────────────────────────────────────────── */
.streamlit-expanderHeader {
    background: rgba(255,255,255,0.04) !important; border-radius: 14px !important;
    border: 1px solid rgba(255,100,0,0.14) !important;
    color: rgba(255,255,255,0.65) !important; font-weight: 500 !important;
    font-family: 'Inter', sans-serif !important;
}
.streamlit-expanderContent {
    border: 1px solid rgba(255,100,0,0.08) !important; border-top: none !important;
    border-radius: 0 0 14px 14px !important; background: rgba(255,255,255,0.02) !important;
}

/* ─── DOWNLOAD BUTTON ────────────────────────────────────────── */
.stDownloadButton > button {
    background: linear-gradient(135deg, rgba(255,100,0,0.20) 0%, rgba(255,60,0,0.12) 100%) !important;
    border: 1px solid rgba(255,110,0,0.35) !important;
    color: rgba(255,255,255,0.92) !important; border-radius: 12px !important;
    font-weight: 600 !important; font-family: 'Inter', sans-serif !important;
    transition: all 0.25s ease !important;
    box-shadow: inset 0 1px 0 rgba(255,200,100,0.14) !important;
}
.stDownloadButton > button:hover {
    background: linear-gradient(135deg, rgba(255,110,0,0.32) 0%, rgba(255,70,0,0.20) 100%) !important;
    border-color: rgba(255,130,0,0.55) !important; transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(255,70,0,0.28), inset 0 1px 0 rgba(255,210,100,0.2) !important;
}

/* ─── SCROLLBAR ──────────────────────────────────────────────── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(255,100,0,0.25); border-radius: 100px; }
::-webkit-scrollbar-thumb:hover { background: rgba(255,120,0,0.45); }

/* ─── HIDE STREAMLIT CHROME ──────────────────────────────────── */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }
[data-testid="stDecoration"] { display: none; }

/* ─── TEXT / TYPOGRAPHY ──────────────────────────────────────── */
.stMarkdown p, .stMarkdown li { color: rgba(255,255,255,0.78) !important; }
.stCaption, [data-testid="stCaptionContainer"] { color: rgba(255,255,255,0.32) !important; }
h1, h2, h3, h4 {
    color: rgba(255,255,255,0.92) !important; font-family: 'Inter', sans-serif !important;
}
[data-testid="stDataFrame"] {
    border-radius: 12px !important; overflow: hidden !important;
    border: 1px solid rgba(255,100,0,0.12) !important;
}

/* ─── FOOTER ─────────────────────────────────────────────────── */
.dash-footer {
    text-align: center; padding: 2rem 1rem 1.5rem;
    color: rgba(255,255,255,0.2) !important; font-size: 0.76rem; letter-spacing: 0.07em;
    border-top: 1px solid rgba(255,100,0,0.1); margin-top: 3rem;
}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
#   DATA
# ══════════════════════════════════════════════════════════════════
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("pakistan_heatwave_data.csv")
        df["Year"] = df["Year"].astype(str)
        df["Deaths"]               = df["Deaths"].fillna(0)
        df["Heatstroke_Cases"]     = df["Heatstroke_Cases"].fillna(0)
        df["Agriculture_Loss_pct"] = df["Agriculture_Loss_pct"].fillna(0)
        df["Livestock_Loss"]       = df["Livestock_Loss"].fillna("No data available")
        df["Water_Shortage_Impact"]= df["Water_Shortage_Impact"].fillna("No significant impact")
        return df
    except FileNotFoundError:
        st.error("CSV file not found — ensure 'pakistan_heatwave_data.csv' is present.")
        return pd.DataFrame()

df = load_data()
if df.empty:
    st.stop()


# ══════════════════════════════════════════════════════════════════
#   CHART THEME
# ══════════════════════════════════════════════════════════════════
def apply_theme(fig, height=440):
    """Unified volcanic dark theme for all Plotly figures."""
    ax = dict(
        gridcolor="rgba(255,255,255,0.045)",
        zeroline=False,
        tickfont=dict(color="rgba(255,255,255,0.45)", size=11, family="Inter"),
        title_font=dict(color="rgba(255,255,255,0.50)", size=12, family="Inter"),
        linecolor="rgba(255,255,255,0.06)",
        tickcolor="rgba(255,255,255,0.06)",
    )
    fig.update_layout(
        height=height,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color="rgba(255,255,255,0.55)", size=12),
        xaxis=ax, yaxis=ax,
        legend=dict(
            bgcolor="rgba(255,255,255,0.045)",
            bordercolor="rgba(255,255,255,0.08)",
            borderwidth=1,
            font=dict(color="rgba(255,255,255,0.65)", size=11, family="Inter"),
        ),
        hoverlabel=dict(
            bgcolor="rgba(10,5,2,0.96)",
            bordercolor="rgba(255,120,0,0.4)",
            font=dict(family="Inter", color="white", size=13),
        ),
        bargap=0.26,
        bargroupgap=0.10,
        margin=dict(l=10, r=10, t=10, b=10),
    )
    fig.update_traces(marker_line_width=0)
    return fig


# ══════════════════════════════════════════════════════════════════
#   HERO
# ══════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">🔥&nbsp; Heatwave Intelligence &nbsp;·&nbsp; 2022 – 2025</div>
    <h1 class="hero-title">Pakistan Climate<br>Impact Dashboard</h1>
    <p class="hero-sub">Meteorological &amp; Health Data &nbsp;·&nbsp; Five Cities &nbsp;·&nbsp; Four Years</p>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
#   SIDEBAR
# ══════════════════════════════════════════════════════════════════
st.sidebar.markdown("""
<div style="padding-bottom:1.2rem; border-bottom:1px solid rgba(255,110,0,0.18); margin-bottom:1.5rem;">
  <div style="font-size:0.68rem;font-weight:700;color:rgba(255,190,80,0.6);
              text-transform:uppercase;letter-spacing:0.16em;margin-bottom:0.15rem;">
    Dashboard Controls
  </div>
  <div style="font-size:0.75rem;color:rgba(255,255,255,0.35);letter-spacing:0.04em;">
    Filter by city &amp; year
  </div>
</div>
""", unsafe_allow_html=True)

cities = sorted(df["City"].dropna().unique().tolist())
selected_cities = st.sidebar.multiselect(
    "Cities", cities,
    default=[cities[0]] if cities else [],
)

years = sorted(df["Year"].dropna().unique().tolist())
selected_years = st.sidebar.multiselect(
    "Years", years,
    default=years[-2:] if len(years) >= 2 else years,
)

st.sidebar.markdown("""
<div style="margin-top:2rem;padding-top:1.2rem;border-top:1px solid rgba(255,110,0,0.1);
            font-size:0.68rem;color:rgba(255,255,255,0.22);text-align:center;letter-spacing:0.06em;line-height:1.8;">
  Pakistan Meteorological Dept<br>Health Ministry Reports
</div>
""", unsafe_allow_html=True)


# ─── Filter ──────────────────────────────────────────────────────
if selected_cities and selected_years:
    filtered_df = df[df["City"].isin(selected_cities) & df["Year"].isin(selected_years)]
else:
    filtered_df = pd.DataFrame()

if filtered_df.empty:
    st.warning("⚠️ No data for selected filters — pick at least one city and one year.")
    st.stop()


# ══════════════════════════════════════════════════════════════════
#   METRIC CARDS
# ══════════════════════════════════════════════════════════════════
st.markdown('<div class="s-label">Overview</div>', unsafe_allow_html=True)

avg_temp     = filtered_df["Peak_Temp_C"].mean()
total_deaths = int(filtered_df["Deaths"].sum())
total_cases  = int(filtered_df["Heatstroke_Cases"].sum())
max_dur      = int(filtered_df["Duration_Days"].max())

c1, c2, c3, c4 = st.columns(4)
cards = [
    (c1, "🏙️", str(len(selected_cities)), "Cities Analysed",
     "linear-gradient(90deg,#a855f7,#7c3aed)"),
    (c2, "🌡️", f"{avg_temp:.1f}°", "Avg Peak Temp (°C)",
     "linear-gradient(90deg,#ff4500,#dc2626)"),
    (c3, "💀", f"{total_deaths:,}", "Total Deaths",
     "linear-gradient(90deg,#ff8c00,#f97316)"),
    (c4, "⏱️", f"{max_dur}d", "Longest Heatwave",
     "linear-gradient(90deg,#fbbf24,#f59e0b)"),
]
for col, icon, val, label, bar_grad in cards:
    with col:
        st.markdown(f"""
        <div class="g-card">
            <span class="g-icon">{icon}</span>
            <div class="g-value">{val}</div>
            <div class="g-label">{label}</div>
            <div class="g-bar" style="background:{bar_grad};"></div>
        </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
#   TABS
# ══════════════════════════════════════════════════════════════════
st.markdown('<div class="s-label">Analysis</div>', unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs([
    "📊  Temperature",
    "⚕️  Health Impact",
    "🌾  Agriculture",
    "💧  Water Crisis",
])

# ── Temperature ───────────────────────────────────────────────────
with tab1:
    # Inferno-style palette — cold→hot
    inferno = ["#fcffa4","#f7d13d","#fb9b06","#ed6925","#cf4446","#a52c60","#781c6d","#4b0c6b"]

    st.markdown("""<div class="c-glass">
        <div class="c-title">Peak Temperature Comparison</div>
        <div class="c-meta">Max recorded °C · by city &amp; year</div>""",
        unsafe_allow_html=True)
    fig1 = px.bar(filtered_df, x="City", y="Peak_Temp_C", color="Year",
                  barmode="group", color_discrete_sequence=inferno,
                  labels={"Peak_Temp_C": "Peak Temp (°C)", "City": ""})
    fig1.update_traces(
        hovertemplate="<b>%{x}</b><br>Peak Temp: <b>%{y:.1f}°C</b><extra></extra>",
        marker_opacity=0.92)
    apply_theme(fig1, 420)
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    plasma = ["#f0f921","#fca636","#e16462","#b12a90","#6a00a8","#0d0887"]
    st.markdown("""<div class="c-glass">
        <div class="c-title">Heatwave Duration</div>
        <div class="c-meta">Consecutive days above danger threshold · by city &amp; year</div>""",
        unsafe_allow_html=True)
    fig2 = px.bar(filtered_df, x="City", y="Duration_Days", color="Year",
                  barmode="group", color_discrete_sequence=plasma,
                  labels={"Duration_Days": "Duration (days)", "City": ""})
    fig2.update_traces(
        hovertemplate="<b>%{x}</b><br>Duration: <b>%{y} days</b><extra></extra>",
        marker_opacity=0.92)
    apply_theme(fig2, 420)
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ── Health Impact ─────────────────────────────────────────────────
with tab2:
    col_a, col_b = st.columns(2)

    with col_a:
        reds = ["#fecaca","#f87171","#ef4444","#dc2626","#b91c1c","#7f1d1d"]
        st.markdown("""<div class="c-glass">
            <div class="c-title">Heat-related Deaths</div>
            <div class="c-meta">Fatalities per city &amp; year</div>""",
            unsafe_allow_html=True)
        fig3 = px.bar(filtered_df, x="City", y="Deaths", color="Year",
                      barmode="group", color_discrete_sequence=reds,
                      labels={"Deaths": "Deaths", "City": ""})
        fig3.update_traces(
            hovertemplate="<b>%{x}</b><br>Deaths: <b>%{y:,}</b><extra></extra>",
            marker_opacity=0.92)
        apply_theme(fig3, 380)
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_b:
        ambers = ["#fef08a","#fde047","#facc15","#f59e0b","#d97706","#92400e"]
        st.markdown("""<div class="c-glass">
            <div class="c-title">Heatstroke Cases</div>
            <div class="c-meta">Reported hospitalisations per city &amp; year</div>""",
            unsafe_allow_html=True)
        fig4 = px.bar(filtered_df, x="City", y="Heatstroke_Cases", color="Year",
                      barmode="group", color_discrete_sequence=ambers,
                      labels={"Heatstroke_Cases": "Cases", "City": ""})
        fig4.update_traces(
            hovertemplate="<b>%{x}</b><br>Cases: <b>%{y:,}</b><extra></extra>",
            marker_opacity=0.92)
        apply_theme(fig4, 380)
        st.plotly_chart(fig4, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""<div class="c-glass">
        <div class="c-title">Health Impact Summary</div>
        <div class="c-meta">Aggregated across selected filters</div>""",
        unsafe_allow_html=True)
    health_summary = (
        filtered_df
        .groupby(["City","Year"])
        .agg(Deaths=("Deaths","sum"),
             Heatstroke_Cases=("Heatstroke_Cases","sum"),
             Peak_Temp_C=("Peak_Temp_C","max"))
        .reset_index()
    )
    st.dataframe(health_summary, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ── Agriculture ───────────────────────────────────────────────────
with tab3:
    greens = ["#d1fae5","#6ee7b7","#34d399","#10b981","#059669","#064e3b"]
    st.markdown("""<div class="c-glass">
        <div class="c-title">Agricultural Loss</div>
        <div class="c-meta">Estimated crop yield loss (%) · by city &amp; year</div>""",
        unsafe_allow_html=True)
    fig5 = px.bar(filtered_df, x="City", y="Agriculture_Loss_pct", color="Year",
                  barmode="group", color_discrete_sequence=greens,
                  labels={"Agriculture_Loss_pct": "Loss (%)", "City": ""})
    fig5.update_traces(
        hovertemplate="<b>%{x}</b><br>Loss: <b>%{y:.1f}%</b><extra></extra>",
        marker_opacity=0.92)
    apply_theme(fig5, 430)
    st.plotly_chart(fig5, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="s-label">Livestock Impact</div>', unsafe_allow_html=True)
    any_data = False
    for _, row in filtered_df.iterrows():
        if row["Livestock_Loss"] != "No data available":
            st.markdown(
                f'<div class="pill-green"><strong>{row["City"]} ({row["Year"]})</strong>'
                f' — {row["Livestock_Loss"]}</div>', unsafe_allow_html=True)
            any_data = True
    if not any_data:
        st.markdown('<div class="pill-green">No livestock impact data for selected filters.</div>',
                    unsafe_allow_html=True)

# ── Water Crisis ──────────────────────────────────────────────────
with tab4:
    st.markdown('<div class="s-label">Water Shortage Reports</div>', unsafe_allow_html=True)
    any_w = False
    for _, row in filtered_df.iterrows():
        if row["Water_Shortage_Impact"] != "No significant impact":
            st.markdown(
                f'<div class="pill-orange"><strong>{row["City"]} ({row["Year"]})</strong>'
                f' — {row["Water_Shortage_Impact"]}</div>', unsafe_allow_html=True)
            any_w = True
    if not any_w:
        st.markdown('<div class="pill-orange">No significant water shortage data for selected filters.</div>',
                    unsafe_allow_html=True)

    city_colors = ["#f472b6","#fb923c","#34d399","#60a5fa","#a78bfa","#facc15"]
    st.markdown("""<div class="c-glass">
        <div class="c-title">Temperature vs Duration</div>
        <div class="c-meta">Bubble size = deaths · colour by city</div>""",
        unsafe_allow_html=True)
    fig6 = px.scatter(
        filtered_df, x="Peak_Temp_C", y="Duration_Days",
        size="Deaths", color="City", hover_name="City",
        hover_data={"Year": True, "Heatstroke_Cases": True,
                    "Deaths": True, "Peak_Temp_C": ":.1f"},
        color_discrete_sequence=city_colors,
        labels={"Peak_Temp_C": "Peak Temperature (°C)", "Duration_Days": "Duration (Days)"},
        size_max=58,
    )
    fig6.update_traces(
        marker=dict(opacity=0.82, line=dict(width=1.2, color="rgba(255,255,255,0.12)")),
        hovertemplate=(
            "<b>%{hovertext}</b><br>"
            "Temp: <b>%{x:.1f}°C</b> · Duration: <b>%{y}d</b><br>"
            "Deaths: <b>%{customdata[2]:,}</b><extra></extra>"
        ),
    )
    apply_theme(fig6, 460)
    st.plotly_chart(fig6, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
#   RAW DATA
# ══════════════════════════════════════════════════════════════════
st.markdown('<div class="s-label">Data Export</div>', unsafe_allow_html=True)
with st.expander("📋  View & Download Raw Data"):
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)
    fname = f"pakistan_heatwave_{'_'.join(selected_cities)}_{'_'.join(selected_years)}.csv"
    st.download_button(
        "📥  Download as CSV", filtered_df.to_csv(index=False), fname, "text/csv"
    )


# ══════════════════════════════════════════════════════════════════
#   SUMMARY STATISTICS
# ══════════════════════════════════════════════════════════════════
st.markdown('<div class="s-label">Summary Statistics</div>', unsafe_allow_html=True)

hottest = filtered_df.loc[filtered_df["Peak_Temp_C"].idxmax()]
longest = filtered_df.loc[filtered_df["Duration_Days"].idxmax()]

s1, s2, s3, s4 = st.columns(4)
with s1:
    st.metric("🌡️ Highest Temperature", f"{filtered_df['Peak_Temp_C'].max():.1f}°C")
    st.caption(f"in {hottest['City']} ({hottest['Year']})")
with s2:
    st.metric("💀 Total Deaths", f"{int(filtered_df['Deaths'].sum()):,}")
    st.caption("across selected filters")
with s3:
    st.metric("🏥 Heatstroke Cases", f"{int(filtered_df['Heatstroke_Cases'].sum()):,}")
    st.caption("across selected filters")
with s4:
    st.metric("⏱️ Longest Heatwave", f"{int(filtered_df['Duration_Days'].max())} days")
    st.caption(f"in {longest['City']} ({longest['Year']})")


# ══════════════════════════════════════════════════════════════════
#   FOOTER
# ══════════════════════════════════════════════════════════════════
st.markdown("""
<div class="dash-footer">
    Pakistan Meteorological Department &nbsp;·&nbsp; Health Ministry Reports &nbsp;·&nbsp; 2022–2025
</div>
""", unsafe_allow_html=True)
