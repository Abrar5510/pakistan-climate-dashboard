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
#  DESIGN SYSTEM
#  Background:  #080d18 (slate-950)
#  Cards:       rgba(30,41,59,0.55)  glass on slate-800
#  Text hi:     #f1f5f9   (slate-100) — 11:1 contrast
#  Text mid:    #94a3b8   (slate-400)
#  Text lo:     #475569   (slate-600)
#  Cyan:        #06b6d4 / #22d3ee
#  Violet:      #8b5cf6 / #a78bfa
#  Emerald:     #10b981
#  Amber:       #f59e0b
#  Rose:        #f43f5e
# ══════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

*, *::before, *::after { box-sizing: border-box; }
html, body, [data-testid="stAppViewContainer"], .main {
    font-family: 'Inter', sans-serif !important;
    -webkit-font-smoothing: antialiased;
}
.block-container { padding-top: 2rem !important; }

/* ── BACKGROUND ─────────────────────────────────────────────── */
.stApp {
    background:
        radial-gradient(ellipse at 12% 18%, rgba(6,182,212,0.07)   0%, transparent 50%),
        radial-gradient(ellipse at 88% 82%, rgba(139,92,246,0.07)  0%, transparent 50%),
        radial-gradient(ellipse at 55% 50%, rgba(16,185,129,0.03)  0%, transparent 40%),
        #080d18 !important;
    min-height: 100vh !important;
}

/* ── SIDEBAR ────────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: #040810 !important;
    border-right: 1px solid rgba(6,182,212,0.14) !important;
    box-shadow: 6px 0 40px rgba(0,0,0,0.6) !important;
}

/* Every piece of text inside the sidebar — white, no exceptions */
section[data-testid="stSidebar"],
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] div,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] small,
section[data-testid="stSidebar"] li {
    color: #f1f5f9 !important;
    font-family: 'Inter', sans-serif !important;
}

/* Widget labels */
section[data-testid="stSidebar"] [data-testid="stWidgetLabel"],
section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
    font-size: 0.7rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.13em !important;
    color: #94a3b8 !important;
    margin-bottom: 0.4rem !important;
}

/* Select box */
section[data-testid="stSidebar"] [data-baseweb="select"] > div:first-child {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(6,182,212,0.25) !important;
    border-radius: 10px !important;
    min-height: 44px !important;
    transition: border-color 0.2s !important;
}
section[data-testid="stSidebar"] [data-baseweb="select"] > div:first-child:hover {
    border-color: rgba(6,182,212,0.55) !important;
}
section[data-testid="stSidebar"] [data-baseweb="select"] input,
section[data-testid="stSidebar"] [data-baseweb="select"] [class*="placeholder"] {
    color: #94a3b8 !important;
    caret-color: #22d3ee !important;
}
section[data-testid="stSidebar"] [data-baseweb="select"] svg {
    fill: #64748b !important;
}

/* Chips / tags */
section[data-testid="stSidebar"] [data-baseweb="tag"] {
    background: rgba(6,182,212,0.15) !important;
    border: 1px solid rgba(6,182,212,0.35) !important;
    border-radius: 8px !important;
}
section[data-testid="stSidebar"] [data-baseweb="tag"] span {
    color: #22d3ee !important;
}
section[data-testid="stSidebar"] [data-baseweb="tag"] [data-baseweb="icon"] svg {
    fill: #22d3ee !important;
}

/* ── HERO ───────────────────────────────────────────────────── */
.hero {
    position: relative;
    overflow: hidden;
    border-radius: 24px;
    padding: 4rem 3rem 3.5rem;
    margin-bottom: 2rem;
    text-align: center;
    /* Gradient border trick */
    background:
        linear-gradient(#0d1424, #0d1424) padding-box,
        linear-gradient(135deg, rgba(6,182,212,0.5), rgba(139,92,246,0.4), rgba(6,182,212,0.2)) border-box;
    border: 1px solid transparent;
    backdrop-filter: blur(24px);
    box-shadow:
        0 0 0 1px rgba(255,255,255,0.03),
        0 32px 80px rgba(0,0,0,0.55),
        inset 0 1px 0 rgba(255,255,255,0.06);
}
/* Subtle inner glow */
.hero::before {
    content: '';
    position: absolute; inset: 0; border-radius: 24px;
    background:
        radial-gradient(ellipse at 50% 0%,   rgba(6,182,212,0.1) 0%, transparent 55%),
        radial-gradient(ellipse at 0%  100%, rgba(139,92,246,0.08) 0%, transparent 55%),
        radial-gradient(ellipse at 100% 100%, rgba(6,182,212,0.06) 0%, transparent 55%);
    pointer-events: none;
}
/* Top specular edge */
.hero::after {
    content: '';
    position: absolute; top: 0; left: 8%; right: 8%; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(6,182,212,0.5), rgba(139,92,246,0.4), transparent);
}

.hero-eyebrow {
    position: relative; z-index: 1;
    display: inline-block;
    background: rgba(6,182,212,0.1);
    border: 1px solid rgba(6,182,212,0.28);
    color: #22d3ee;
    padding: 0.28rem 0.9rem;
    border-radius: 100px;
    font-size: 0.68rem; font-weight: 700;
    letter-spacing: 0.14em; text-transform: uppercase;
    margin-bottom: 1.5rem;
    box-shadow: 0 0 20px rgba(6,182,212,0.15);
}
.hero-title {
    position: relative; z-index: 1;
    font-size: 4rem; font-weight: 900;
    line-height: 1.06; letter-spacing: -0.04em;
    margin-bottom: 1rem;
    background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 40%, #22d3ee 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.hero-sub {
    position: relative; z-index: 1;
    font-size: 0.85rem; font-weight: 400;
    color: #475569 !important;
    letter-spacing: 0.12em; text-transform: uppercase;
}

/* ── METRIC CARDS ───────────────────────────────────────────── */
.g-card {
    position: relative; overflow: hidden;
    border-radius: 16px;
    padding: 1.75rem 1.5rem;
    margin: 0.35rem 0;
    text-align: center;
    background: rgba(15, 23, 42, 0.65);
    backdrop-filter: blur(20px) saturate(160%);
    -webkit-backdrop-filter: blur(20px) saturate(160%);
    border: 1px solid rgba(255,255,255,0.07);
    box-shadow:
        0 4px 24px rgba(0,0,0,0.35),
        inset 0 1px 0 rgba(255,255,255,0.06);
    transition:
        transform  0.28s cubic-bezier(0.34,1.56,0.64,1),
        box-shadow 0.28s ease,
        border-color 0.28s ease;
}
.g-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 2px;
    border-radius: 16px 16px 0 0;
}
.g-card:hover {
    transform: translateY(-5px);
    border-color: rgba(255,255,255,0.13);
    box-shadow: 0 20px 50px rgba(0,0,0,0.45), inset 0 1px 0 rgba(255,255,255,0.08);
}
.g-card.cyan::before  { background: linear-gradient(90deg, #06b6d4, #22d3ee); }
.g-card.cyan:hover    { box-shadow: 0 20px 50px rgba(0,0,0,0.45), 0 0 30px rgba(6,182,212,0.1); }
.g-card.violet::before { background: linear-gradient(90deg, #8b5cf6, #a78bfa); }
.g-card.violet:hover   { box-shadow: 0 20px 50px rgba(0,0,0,0.45), 0 0 30px rgba(139,92,246,0.1); }
.g-card.rose::before  { background: linear-gradient(90deg, #f43f5e, #fb7185); }
.g-card.rose:hover    { box-shadow: 0 20px 50px rgba(0,0,0,0.45), 0 0 30px rgba(244,63,94,0.1); }
.g-card.amber::before { background: linear-gradient(90deg, #f59e0b, #fbbf24); }
.g-card.amber:hover   { box-shadow: 0 20px 50px rgba(0,0,0,0.45), 0 0 30px rgba(245,158,11,0.1); }

.g-icon  { font-size: 1.4rem; display: block; line-height: 1; margin-bottom: 0.5rem; }
.g-value {
    font-size: 2.8rem; font-weight: 900;
    letter-spacing: -0.05em; line-height: 1;
    color: #f1f5f9;
}
.g-label {
    font-size: 0.68rem; font-weight: 600;
    text-transform: uppercase; letter-spacing: 0.13em;
    color: #475569;
    margin-top: 0.5rem;
}

/* ── CHART CONTAINERS ───────────────────────────────────────── */
.c-glass {
    position: relative; overflow: hidden;
    border-radius: 16px;
    padding: 1.5rem 1.5rem 0.5rem;
    margin: 0.75rem 0;
    background: rgba(15,23,42,0.55);
    backdrop-filter: blur(16px);
    -webkit-backdrop-filter: blur(16px);
    border: 1px solid rgba(255,255,255,0.065);
    box-shadow: 0 4px 24px rgba(0,0,0,0.3);
}
.c-title {
    font-size: 0.95rem; font-weight: 700;
    color: #e2e8f0 !important;
    letter-spacing: -0.01em;
}
.c-meta {
    font-size: 0.7rem;
    color: #475569 !important;
    text-transform: uppercase; letter-spacing: 0.09em;
    margin: 0.15rem 0 0.3rem;
}

/* ── SECTION LABELS ─────────────────────────────────────────── */
.s-label {
    font-size: 0.64rem; font-weight: 700;
    color: #475569;
    text-transform: uppercase; letter-spacing: 0.18em;
    margin: 1.75rem 0 1rem;
    display: flex; align-items: center; gap: 0.75rem;
}
.s-label::after {
    content: ''; flex: 1; height: 1px;
    background: linear-gradient(90deg, rgba(6,182,212,0.15) 0%, transparent 100%);
}

/* ── PILLS ──────────────────────────────────────────────────── */
.pill-teal {
    background: rgba(6,182,212,0.07);
    border: 1px solid rgba(6,182,212,0.2);
    border-radius: 12px; padding: 0.85rem 1.25rem; margin: 0.4rem 0;
    color: #cbd5e1 !important; font-size: 0.875rem; line-height: 1.55;
}
.pill-amber {
    background: rgba(245,158,11,0.07);
    border: 1px solid rgba(245,158,11,0.2);
    border-radius: 12px; padding: 0.85rem 1.25rem; margin: 0.4rem 0;
    color: #cbd5e1 !important; font-size: 0.875rem; line-height: 1.55;
}

/* ── TABS ───────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(15,23,42,0.7) !important;
    border-radius: 14px !important;
    padding: 4px !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    gap: 2px !important;
    margin-bottom: 1.25rem !important;
}
.stTabs [data-baseweb="tab"] {
    color: #475569 !important;
    background: transparent !important;
    border-radius: 10px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
    padding: 0.5rem 1.35rem !important;
    transition: all 0.2s ease !important;
    border: none !important;
}
.stTabs [data-baseweb="tab"]:hover {
    color: #94a3b8 !important;
    background: rgba(255,255,255,0.04) !important;
}
.stTabs [aria-selected="true"] {
    background: rgba(6,182,212,0.12) !important;
    color: #22d3ee !important;
    border: 1px solid rgba(6,182,212,0.22) !important;
    box-shadow: 0 0 16px rgba(6,182,212,0.15), inset 0 1px 0 rgba(6,182,212,0.2) !important;
}
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] { display: none !important; }

/* ── ST.METRIC ──────────────────────────────────────────────── */
[data-testid="stMetric"] {
    background: rgba(15,23,42,0.6) !important;
    border-radius: 16px !important;
    padding: 1.5rem !important;
    border: 1px solid rgba(255,255,255,0.065) !important;
    box-shadow: 0 4px 20px rgba(0,0,0,0.25) !important;
    backdrop-filter: blur(12px) !important;
}
[data-testid="stMetricValue"] {
    color: #f1f5f9 !important;
    font-weight: 800 !important;
    font-family: 'Inter', sans-serif !important;
    letter-spacing: -0.02em !important;
}
[data-testid="stMetricLabel"] {
    color: #475569 !important;
    font-size: 0.7rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
    font-weight: 600 !important;
}

/* ── EXPANDER ───────────────────────────────────────────────── */
.streamlit-expanderHeader {
    background: rgba(15,23,42,0.55) !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    color: #94a3b8 !important;
    font-weight: 500 !important;
    font-family: 'Inter', sans-serif !important;
}
.streamlit-expanderContent {
    border: 1px solid rgba(255,255,255,0.05) !important;
    border-top: none !important;
    border-radius: 0 0 12px 12px !important;
    background: rgba(8,13,24,0.4) !important;
}

/* ── DOWNLOAD BUTTON ────────────────────────────────────────── */
.stDownloadButton > button {
    background: rgba(6,182,212,0.1) !important;
    border: 1px solid rgba(6,182,212,0.3) !important;
    color: #22d3ee !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    transition: all 0.22s ease !important;
}
.stDownloadButton > button:hover {
    background: rgba(6,182,212,0.18) !important;
    border-color: rgba(6,182,212,0.55) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 24px rgba(6,182,212,0.2) !important;
}

/* ── TYPOGRAPHY ─────────────────────────────────────────────── */
.stMarkdown p, .stMarkdown li { color: #94a3b8 !important; }
.stCaption, [data-testid="stCaptionContainer"] { color: #475569 !important; }
h1, h2, h3, h4 {
    color: #e2e8f0 !important;
    font-family: 'Inter', sans-serif !important;
    letter-spacing: -0.02em;
}

/* ── DATAFRAME ──────────────────────────────────────────────── */
[data-testid="stDataFrame"] {
    border-radius: 12px !important;
    overflow: hidden !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
}

/* ── FOOTER ─────────────────────────────────────────────────── */
.dash-footer {
    text-align: center; padding: 2rem 1rem 1.5rem;
    color: #334155 !important; font-size: 0.76rem; letter-spacing: 0.07em;
    border-top: 1px solid rgba(255,255,255,0.05); margin-top: 3rem;
}

/* ── SCROLLBAR ──────────────────────────────────────────────── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(6,182,212,0.2); border-radius: 100px; }
::-webkit-scrollbar-thumb:hover { background: rgba(6,182,212,0.4); }

/* ── HIDE CHROME ────────────────────────────────────────────── */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
#   DATA
# ══════════════════════════════════════════════════════════════════
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("pakistan_heatwave_data.csv")
        df["Year"]                 = df["Year"].astype(str)
        df["Deaths"]               = df["Deaths"].fillna(0)
        df["Heatstroke_Cases"]     = df["Heatstroke_Cases"].fillna(0)
        df["Agriculture_Loss_pct"] = df["Agriculture_Loss_pct"].fillna(0)
        df["Livestock_Loss"]       = df["Livestock_Loss"].fillna("No data available")
        df["Water_Shortage_Impact"]= df["Water_Shortage_Impact"].fillna("No significant impact")
        return df
    except FileNotFoundError:
        st.error("CSV not found — ensure 'pakistan_heatwave_data.csv' is present.")
        return pd.DataFrame()

df = load_data()
if df.empty:
    st.stop()


# ══════════════════════════════════════════════════════════════════
#   CHART THEME
# ══════════════════════════════════════════════════════════════════
def theme(fig, height=440):
    ax = dict(
        gridcolor="rgba(255,255,255,0.04)",
        zeroline=False,
        tickfont=dict(color="#475569", size=11, family="Inter"),
        title_font=dict(color="#64748b", size=12, family="Inter"),
        linecolor="rgba(255,255,255,0.05)",
        tickcolor="rgba(255,255,255,0.05)",
    )
    fig.update_layout(
        height=height,
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter, sans-serif", color="#64748b", size=12),
        xaxis={**ax}, yaxis={**ax},
        legend=dict(
            bgcolor="rgba(15,23,42,0.6)",
            bordercolor="rgba(255,255,255,0.07)",
            borderwidth=1,
            font=dict(color="#94a3b8", size=11, family="Inter"),
        ),
        hoverlabel=dict(
            bgcolor="#0d1424",
            bordercolor="rgba(6,182,212,0.35)",
            font=dict(family="Inter", color="#f1f5f9", size=13),
        ),
        bargap=0.28, bargroupgap=0.1,
        margin=dict(l=10, r=10, t=10, b=10),
    )
    fig.update_traces(marker_line_width=0)
    return fig


# ══════════════════════════════════════════════════════════════════
#   HERO
# ══════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">🌡️&nbsp; Pakistan &nbsp;·&nbsp; 2022 – 2025</div>
    <h1 class="hero-title">Climate Impact<br>Dashboard</h1>
    <p class="hero-sub">Heatwave Intelligence &nbsp;·&nbsp; Meteorological &amp; Health Data</p>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
#   SIDEBAR
# ══════════════════════════════════════════════════════════════════
st.sidebar.markdown("""
<div style="margin-bottom:1.5rem;padding-bottom:1.2rem;border-bottom:1px solid rgba(6,182,212,0.14);">
  <div style="font-size:0.68rem;font-weight:700;color:#475569;
              text-transform:uppercase;letter-spacing:0.16em;margin-bottom:0.2rem;">
    Filters
  </div>
  <div style="font-size:0.78rem;color:#334155;">Select cities &amp; years</div>
</div>
""", unsafe_allow_html=True)

cities = sorted(df["City"].dropna().unique().tolist())
selected_cities = st.sidebar.multiselect(
    "Cities", cities, default=[cities[0]] if cities else []
)

years = sorted(df["Year"].dropna().unique().tolist())
selected_years = st.sidebar.multiselect(
    "Years", years, default=years[-2:] if len(years) >= 2 else years
)

st.sidebar.markdown("""
<div style="margin-top:2rem;padding-top:1rem;border-top:1px solid rgba(255,255,255,0.04);
            font-size:0.68rem;color:#1e293b;text-align:center;line-height:1.8;letter-spacing:0.05em;">
  Pakistan Meteorological Dept<br>Health Ministry · 2022–2025
</div>
""", unsafe_allow_html=True)


# ── Filter ────────────────────────────────────────────────────────
if selected_cities and selected_years:
    fdf = df[df["City"].isin(selected_cities) & df["Year"].isin(selected_years)]
else:
    fdf = pd.DataFrame()

if fdf.empty:
    st.warning("⚠️ No data — pick at least one city and one year.")
    st.stop()


# ══════════════════════════════════════════════════════════════════
#   METRIC CARDS
# ══════════════════════════════════════════════════════════════════
st.markdown('<div class="s-label">Overview</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
hottest_row = fdf.loc[fdf["Peak_Temp_C"].idxmax()]
longest_row = fdf.loc[fdf["Duration_Days"].idxmax()]

metrics = [
    (c1, "cyan",   "🏙️", str(len(selected_cities)),                   "Cities Analysed"),
    (c2, "violet", "🌡️", f"{fdf['Peak_Temp_C'].mean():.1f}°C",        "Avg Peak Temp"),
    (c3, "rose",   "💀", f"{int(fdf['Deaths'].sum()):,}",              "Total Deaths"),
    (c4, "amber",  "⏱️", f"{int(fdf['Duration_Days'].max())}d",        "Longest Heatwave"),
]
for col, cls, icon, val, label in metrics:
    with col:
        st.markdown(f"""
        <div class="g-card {cls}">
            <span class="g-icon">{icon}</span>
            <div class="g-value">{val}</div>
            <div class="g-label">{label}</div>
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

# ── Temperature ────────────────────────────────────────────────────
with tab1:
    # Scientific sequential: cyan → blue → violet (professional data viz)
    temp_pal  = ["#22d3ee","#06b6d4","#0ea5e9","#3b82f6","#6366f1","#8b5cf6"]
    dur_pal   = ["#a78bfa","#8b5cf6","#7c3aed","#6d28d9","#5b21b6","#4c1d95"]

    st.markdown("""<div class="c-glass">
        <div class="c-title">Peak Temperature Comparison</div>
        <div class="c-meta">Maximum recorded °C · by city and year</div>""",
        unsafe_allow_html=True)
    fig1 = px.bar(fdf, x="City", y="Peak_Temp_C", color="Year",
                  barmode="group", color_discrete_sequence=temp_pal,
                  labels={"Peak_Temp_C": "Peak Temp (°C)", "City": ""})
    fig1.update_traces(
        marker_opacity=0.9,
        hovertemplate="<b>%{x}</b><br>Peak Temp: <b>%{y:.1f}°C</b><extra></extra>")
    theme(fig1, 420)
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""<div class="c-glass">
        <div class="c-title">Heatwave Duration</div>
        <div class="c-meta">Consecutive days above danger threshold · by city and year</div>""",
        unsafe_allow_html=True)
    fig2 = px.bar(fdf, x="City", y="Duration_Days", color="Year",
                  barmode="group", color_discrete_sequence=dur_pal,
                  labels={"Duration_Days": "Days", "City": ""})
    fig2.update_traces(
        marker_opacity=0.9,
        hovertemplate="<b>%{x}</b><br>Duration: <b>%{y} days</b><extra></extra>")
    theme(fig2, 420)
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ── Health Impact ──────────────────────────────────────────────────
with tab2:
    col_a, col_b = st.columns(2)

    with col_a:
        rose_pal = ["#fda4af","#fb7185","#f43f5e","#e11d48","#be123c","#9f1239"]
        st.markdown("""<div class="c-glass">
            <div class="c-title">Heat-related Deaths</div>
            <div class="c-meta">Fatalities per city and year</div>""",
            unsafe_allow_html=True)
        fig3 = px.bar(fdf, x="City", y="Deaths", color="Year",
                      barmode="group", color_discrete_sequence=rose_pal,
                      labels={"Deaths": "Deaths", "City": ""})
        fig3.update_traces(marker_opacity=0.9,
            hovertemplate="<b>%{x}</b><br>Deaths: <b>%{y:,}</b><extra></extra>")
        theme(fig3, 370)
        st.plotly_chart(fig3, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_b:
        amber_pal = ["#fef08a","#fde047","#facc15","#f59e0b","#d97706","#b45309"]
        st.markdown("""<div class="c-glass">
            <div class="c-title">Heatstroke Cases</div>
            <div class="c-meta">Reported hospitalisations per city and year</div>""",
            unsafe_allow_html=True)
        fig4 = px.bar(fdf, x="City", y="Heatstroke_Cases", color="Year",
                      barmode="group", color_discrete_sequence=amber_pal,
                      labels={"Heatstroke_Cases": "Cases", "City": ""})
        fig4.update_traces(marker_opacity=0.9,
            hovertemplate="<b>%{x}</b><br>Cases: <b>%{y:,}</b><extra></extra>")
        theme(fig4, 370)
        st.plotly_chart(fig4, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""<div class="c-glass">
        <div class="c-title">Health Impact Summary</div>
        <div class="c-meta">Aggregated across selected filters</div>""",
        unsafe_allow_html=True)
    summary = (fdf.groupby(["City","Year"])
               .agg(Deaths=("Deaths","sum"),
                    Heatstroke_Cases=("Heatstroke_Cases","sum"),
                    Peak_Temp_C=("Peak_Temp_C","max"))
               .reset_index())
    st.dataframe(summary, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ── Agriculture ────────────────────────────────────────────────────
with tab3:
    green_pal = ["#6ee7b7","#34d399","#10b981","#059669","#047857","#065f46"]
    st.markdown("""<div class="c-glass">
        <div class="c-title">Agricultural Loss</div>
        <div class="c-meta">Estimated crop yield loss (%) · by city and year</div>""",
        unsafe_allow_html=True)
    fig5 = px.bar(fdf, x="City", y="Agriculture_Loss_pct", color="Year",
                  barmode="group", color_discrete_sequence=green_pal,
                  labels={"Agriculture_Loss_pct": "Loss (%)", "City": ""})
    fig5.update_traces(marker_opacity=0.9,
        hovertemplate="<b>%{x}</b><br>Loss: <b>%{y:.1f}%</b><extra></extra>")
    theme(fig5, 430)
    st.plotly_chart(fig5, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="s-label">Livestock Impact</div>', unsafe_allow_html=True)
    shown = False
    for _, row in fdf.iterrows():
        if row["Livestock_Loss"] != "No data available":
            st.markdown(
                f'<div class="pill-teal"><strong>{row["City"]} ({row["Year"]})</strong>'
                f' — {row["Livestock_Loss"]}</div>', unsafe_allow_html=True)
            shown = True
    if not shown:
        st.markdown('<div class="pill-teal">No livestock data for selected filters.</div>',
                    unsafe_allow_html=True)

# ── Water Crisis ────────────────────────────────────────────────────
with tab4:
    st.markdown('<div class="s-label">Water Shortage Reports</div>', unsafe_allow_html=True)
    shown = False
    for _, row in fdf.iterrows():
        if row["Water_Shortage_Impact"] != "No significant impact":
            st.markdown(
                f'<div class="pill-amber"><strong>{row["City"]} ({row["Year"]})</strong>'
                f' — {row["Water_Shortage_Impact"]}</div>', unsafe_allow_html=True)
            shown = True
    if not shown:
        st.markdown('<div class="pill-amber">No water shortage data for selected filters.</div>',
                    unsafe_allow_html=True)

    # Bubble chart — vivid categorical palette
    bubble_pal = ["#22d3ee","#a78bfa","#34d399","#fbbf24","#fb7185","#60a5fa"]
    st.markdown("""<div class="c-glass">
        <div class="c-title">Temperature vs Duration</div>
        <div class="c-meta">Bubble size represents deaths · colour by city</div>""",
        unsafe_allow_html=True)
    fig6 = px.scatter(
        fdf, x="Peak_Temp_C", y="Duration_Days",
        size="Deaths", color="City", hover_name="City",
        hover_data={"Year": True, "Heatstroke_Cases": True,
                    "Deaths": True, "Peak_Temp_C": ":.1f"},
        color_discrete_sequence=bubble_pal,
        labels={"Peak_Temp_C": "Peak Temperature (°C)", "Duration_Days": "Duration (Days)"},
        size_max=55,
    )
    fig6.update_traces(
        marker=dict(opacity=0.85, line=dict(width=1, color="rgba(255,255,255,0.1)")),
        hovertemplate=(
            "<b>%{hovertext}</b><br>"
            "Temp: <b>%{x:.1f}°C</b>  ·  Duration: <b>%{y}d</b><br>"
            "Deaths: <b>%{customdata[2]:,}</b><extra></extra>"
        ),
    )
    theme(fig6, 460)
    st.plotly_chart(fig6, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════
#   DATA EXPORT
# ══════════════════════════════════════════════════════════════════
st.markdown('<div class="s-label">Raw Data</div>', unsafe_allow_html=True)
with st.expander("📋  View & Export Filtered Data"):
    st.dataframe(fdf, use_container_width=True, hide_index=True)
    fname = f"pakistan_heatwave_{'_'.join(selected_cities)}_{'_'.join(selected_years)}.csv"
    st.download_button("📥  Download CSV", fdf.to_csv(index=False), fname, "text/csv")


# ══════════════════════════════════════════════════════════════════
#   SUMMARY STATISTICS
# ══════════════════════════════════════════════════════════════════
st.markdown('<div class="s-label">Summary Statistics</div>', unsafe_allow_html=True)
s1, s2, s3, s4 = st.columns(4)

with s1:
    st.metric("🌡️  Peak Temp", f"{fdf['Peak_Temp_C'].max():.1f}°C")
    st.caption(f"{hottest_row['City']} · {hottest_row['Year']}")
with s2:
    st.metric("💀  Total Deaths", f"{int(fdf['Deaths'].sum()):,}")
    st.caption("across selected filters")
with s3:
    st.metric("🏥  Heatstroke Cases", f"{int(fdf['Heatstroke_Cases'].sum()):,}")
    st.caption("across selected filters")
with s4:
    st.metric("⏱️  Longest Heatwave", f"{int(fdf['Duration_Days'].max())} days")
    st.caption(f"{longest_row['City']} · {longest_row['Year']}")


# ══════════════════════════════════════════════════════════════════
#   FOOTER
# ══════════════════════════════════════════════════════════════════
st.markdown("""
<div class="dash-footer">
    Pakistan Meteorological Department &nbsp;·&nbsp; Health Ministry Reports &nbsp;·&nbsp; 2022 – 2025
</div>
""", unsafe_allow_html=True)
