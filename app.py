import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="MuleGuard AI",
    layout="wide",
    page_icon="⚡",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# GLOBAL CSS — Cyberpunk / Intelligence-Ops aesthetic
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;600;700;800&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #020408 !important;
    color: #E2E8F0;
    font-family: 'Syne', sans-serif;
}

[data-testid="stSidebar"] {
    background: #060C14 !important;
    border-right: 1px solid #0FF4C615;
}

[data-testid="stSidebar"] * { color: #CBD5E1 !important; }

/* ── Animated grid background ── */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(0,255,163,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,255,163,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
    z-index: 0;
}

/* ── Top accent line ── */
[data-testid="stAppViewContainer"]::after {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #00FFA3, #00C8FF, #FF2D78, transparent);
    z-index: 9999;
    animation: scanline 4s ease-in-out infinite alternate;
}

@keyframes scanline {
    from { opacity: 0.6; }
    to   { opacity: 1; }
}

/* ── Hero header ── */
.hero-header {
    position: relative;
    padding: 36px 0 28px;
    margin-bottom: 8px;
}
.hero-tag {
    display: inline-block;
    font-family: 'Space Mono', monospace;
    font-size: 11px;
    letter-spacing: 3px;
    color: #00FFA3;
    background: rgba(0,255,163,0.08);
    border: 1px solid rgba(0,255,163,0.25);
    padding: 4px 14px;
    border-radius: 2px;
    margin-bottom: 16px;
    text-transform: uppercase;
}
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(28px, 4vw, 52px);
    font-weight: 800;
    letter-spacing: -1.5px;
    line-height: 1.1;
    background: linear-gradient(135deg, #FFFFFF 0%, #94A3B8 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-title span {
    background: linear-gradient(135deg, #00FFA3, #00C8FF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-family: 'Space Mono', monospace;
    font-size: 12px;
    color: #475569;
    margin-top: 10px;
    letter-spacing: 0.5px;
}

/* ── KPI cards ── */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 12px;
    margin: 24px 0;
}
.kpi-card {
    position: relative;
    background: linear-gradient(135deg, #0D1520 0%, #0A1018 100%);
    border: 1px solid #1E293B;
    border-radius: 12px;
    padding: 22px 20px 18px;
    overflow: hidden;
    transition: border-color 0.3s, transform 0.2s;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    border-radius: 12px 12px 0 0;
}
.kpi-card.green::before  { background: linear-gradient(90deg, #00FFA3, transparent); }
.kpi-card.blue::before   { background: linear-gradient(90deg, #00C8FF, transparent); }
.kpi-card.red::before    { background: linear-gradient(90deg, #FF2D78, transparent); }
.kpi-card.orange::before { background: linear-gradient(90deg, #FF8C00, transparent); }
.kpi-card.purple::before { background: linear-gradient(90deg, #A855F7, transparent); }

.kpi-card::after {
    content: '';
    position: absolute;
    bottom: -30px; right: -30px;
    width: 80px; height: 80px;
    border-radius: 50%;
    opacity: 0.06;
}
.kpi-card.green::after  { background: #00FFA3; }
.kpi-card.blue::after   { background: #00C8FF; }
.kpi-card.red::after    { background: #FF2D78; }
.kpi-card.orange::after { background: #FF8C00; }
.kpi-card.purple::after { background: #A855F7; }

.kpi-label {
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #475569;
    margin-bottom: 10px;
}
.kpi-value {
    font-family: 'Syne', sans-serif;
    font-size: 34px;
    font-weight: 800;
    letter-spacing: -1px;
    line-height: 1;
}
.kpi-card.green  .kpi-value { color: #00FFA3; }
.kpi-card.blue   .kpi-value { color: #00C8FF; }
.kpi-card.red    .kpi-value { color: #FF2D78; }
.kpi-card.orange .kpi-value { color: #FF8C00; }
.kpi-card.purple .kpi-value { color: #A855F7; }

.kpi-sub {
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    color: #334155;
    margin-top: 6px;
}

/* ── Section heading ── */
.sec-heading {
    font-family: 'Space Mono', monospace;
    font-size: 11px;
    letter-spacing: 3px;
    color: #00FFA3;
    text-transform: uppercase;
    margin: 32px 0 14px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.sec-heading::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, #0F2A20, transparent);
}

/* ── Alert boxes ── */
.alert-critical {
    background: linear-gradient(135deg, #1A0714 0%, #120510 100%);
    border: 1px solid #FF2D7840;
    border-left: 3px solid #FF2D78;
    border-radius: 10px;
    padding: 20px 24px;
    position: relative;
    overflow: hidden;
}
.alert-critical::before {
    content: '⚠ CRITICAL';
    font-family: 'Space Mono', monospace;
    font-size: 9px;
    letter-spacing: 3px;
    color: #FF2D78;
    position: absolute;
    top: 10px; right: 14px;
    opacity: 0.7;
}
.alert-high {
    background: linear-gradient(135deg, #1A100A 0%, #120B06 100%);
    border: 1px solid #FF8C0040;
    border-left: 3px solid #FF8C00;
    border-radius: 10px;
    padding: 20px 24px;
}
.alert-medium {
    background: linear-gradient(135deg, #191400 0%, #120E00 100%);
    border: 1px solid #EAB30840;
    border-left: 3px solid #EAB308;
    border-radius: 10px;
    padding: 20px 24px;
}
.alert-low {
    background: linear-gradient(135deg, #041A10 0%, #021208 100%);
    border: 1px solid #00FFA340;
    border-left: 3px solid #00FFA3;
    border-radius: 10px;
    padding: 20px 24px;
}

/* ── Risk badge ── */
.risk-badge {
    display: inline-block;
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 3px;
    font-weight: 700;
    margin-bottom: 8px;
}
.badge-critical { background: rgba(255,45,120,0.15); color: #FF2D78; border: 1px solid #FF2D7840; }
.badge-high     { background: rgba(255,140,0,0.15);  color: #FF8C00; border: 1px solid #FF8C0040; }
.badge-medium   { background: rgba(234,179,8,0.15);  color: #EAB308; border: 1px solid #EAB30840; }
.badge-low      { background: rgba(0,255,163,0.12);  color: #00FFA3; border: 1px solid #00FFA340; }

/* ── Score ring ── */
.score-ring-wrap {
    text-align: center;
    padding: 20px 0 10px;
}
.score-number {
    font-family: 'Syne', sans-serif;
    font-size: 56px;
    font-weight: 800;
    letter-spacing: -2px;
}
.score-label {
    font-family: 'Space Mono', monospace;
    font-size: 10px;
    letter-spacing: 3px;
    color: #475569;
    text-transform: uppercase;
    margin-top: 4px;
}

/* ── Sidebar custom ── */
.sidebar-logo {
    font-family: 'Syne', sans-serif;
    font-size: 22px;
    font-weight: 800;
    color: #FFFFFF !important;
    letter-spacing: -0.5px;
    padding: 8px 0 4px;
}
.sidebar-logo span { color: #00FFA3 !important; }
.sidebar-tagline {
    font-family: 'Space Mono', monospace;
    font-size: 9px;
    color: #334155 !important;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 24px;
}

/* ── Streamlit tab override ── */
[data-baseweb="tab-list"] {
    background: transparent !important;
    gap: 4px;
    border-bottom: 1px solid #1E293B !important;
}
[data-baseweb="tab"] {
    font-family: 'Space Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 1px !important;
    color: #475569 !important;
    background: transparent !important;
    border-radius: 6px 6px 0 0 !important;
    padding: 10px 18px !important;
    border: none !important;
}
[aria-selected="true"][data-baseweb="tab"] {
    color: #00FFA3 !important;
    background: rgba(0,255,163,0.05) !important;
    border-bottom: 2px solid #00FFA3 !important;
}
[data-testid="stDataFrame"] {
    border: 1px solid #1E293B !important;
    border-radius: 10px !important;
    overflow: hidden;
}

/* ── Upload area ── */
[data-testid="stFileUploader"] {
    border: 1px dashed #1E3A2F !important;
    border-radius: 10px !important;
    background: rgba(0,255,163,0.02) !important;
}

/* ── Slider ── */
[data-testid="stSlider"] > div > div > div {
    background: #00FFA3 !important;
}

/* ── Download button ── */
[data-testid="stDownloadButton"] button {
    font-family: 'Space Mono', monospace !important;
    font-size: 11px !important;
    letter-spacing: 1px !important;
    background: transparent !important;
    border: 1px solid #00FFA360 !important;
    color: #00FFA3 !important;
    border-radius: 6px !important;
    padding: 10px 20px !important;
    transition: all 0.2s !important;
}
[data-testid="stDownloadButton"] button:hover {
    background: rgba(0,255,163,0.1) !important;
    border-color: #00FFA3 !important;
}

/* ── Selectbox ── */
[data-testid="stSelectbox"] > div > div {
    background: #0D1520 !important;
    border: 1px solid #1E293B !important;
    border-radius: 8px !important;
    color: #E2E8F0 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 12px !important;
}

/* ── Info / warning boxes ── */
[data-testid="stAlert"] {
    background: rgba(0,200,255,0.05) !important;
    border: 1px solid rgba(0,200,255,0.2) !important;
    border-radius: 8px !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 12px !important;
}

/* ── Hide streamlit default branding ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #0A0F18; }
::-webkit-scrollbar-thumb { background: #1E293B; border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: #00FFA320; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# PLOTLY THEME
# ─────────────────────────────────────────────
PLOT_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Space Mono, monospace", color="#64748B", size=11),
    title_font=dict(family="Syne, sans-serif", color="#E2E8F0", size=15),
    legend=dict(
        bgcolor="rgba(6,12,20,0.8)",
        bordercolor="#1E293B",
        borderwidth=1,
        font=dict(family="Space Mono, monospace", size=10),
    ),
    margin=dict(l=16, r=16, t=44, b=16),
    xaxis=dict(
        gridcolor="#0F1F2E",
        linecolor="#1E293B",
        tickfont=dict(family="Space Mono, monospace", size=10, color="#475569"),
        title_font=dict(color="#64748B"),
    ),
    yaxis=dict(
        gridcolor="#0F1F2E",
        linecolor="#1E293B",
        tickfont=dict(family="Space Mono, monospace", size=10, color="#475569"),
        title_font=dict(color="#64748B"),
    ),
)

RISK_COLORS = {
    "Critical": "#FF2D78",
    "High":     "#FF8C00",
    "Medium":   "#EAB308",
    "Low":      "#00FFA3",
}


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def risk_level(score):
    if score >= 80: return "Critical"
    if score >= 50: return "High"
    if score >= 20: return "Medium"
    return "Low"

def badge_class(level):
    return {
        "Critical": "badge-critical",
        "High":     "badge-high",
        "Medium":   "badge-medium",
        "Low":      "badge-low",
    }.get(level, "badge-low")

def alert_class(level):
    return {
        "Critical": "alert-critical",
        "High":     "alert-high",
        "Medium":   "alert-medium",
        "Low":      "alert-low",
    }.get(level, "alert-low")

def score_color(level):
    return RISK_COLORS.get(level, "#00FFA3")

def generate_alert(score):
    if score >= 80: return "Critical mule account suspected — immediate escalation to fraud investigation team required."
    if score >= 50: return "High-risk account detected — manual review and enhanced monitoring recommended."
    if score >= 20: return "Medium-risk account — schedule routine behavioral analysis."
    return "Low-risk account — no immediate action required. Continue passive monitoring."

def recommended_action(level):
    return {
        "Critical": "🔴 Freeze account immediately and escalate to Tier-2 Fraud Investigation.",
        "High":     "🟠 Place under enhanced monitoring; initiate KYC review within 24 hrs.",
        "Medium":   "🟡 Flag for next scheduled review cycle; watch for velocity changes.",
        "Low":      "🟢 No action required. Routine surveillance applies.",
    }.get(level, "")


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">Mule<span>Guard</span> AI</div>
    <div class="sidebar-tagline">Financial Crime Intelligence</div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload Account / Transaction CSV", type=["csv"])

    st.markdown("---")
    threshold = st.slider("Flag Threshold (%)", 0, 100, 80, 5,
                          help="Accounts scoring above this are flagged as suspicious.")

    st.markdown("---")
    st.markdown("""
    <div style="font-family:'Space Mono',monospace;font-size:10px;color:#334155;line-height:1.8;">
    ENGINE &nbsp;&nbsp;&nbsp; XGBoost v2<br>
    IMPUTER &nbsp; Iterative<br>
    EXPLAINER &nbsp;SHAP<br>
    VERSION &nbsp;&nbsp; 3.1.0
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# HERO HEADER
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-header">
    <div class="hero-tag">⚡ Explainable AI · Real-Time Scoring</div>
    <div class="hero-title">Suspicious <span>Mule Account</span><br>Detection Platform</div>
    <div class="hero-sub">// XGBoost · Feature Selection · SHAP Explainability · Risk Intelligence</div>
</div>
""", unsafe_allow_html=True)

if uploaded_file is None:
    st.markdown("""
    <div style="
        border: 1px dashed #1E3A2F;
        border-radius: 14px;
        background: rgba(0,255,163,0.02);
        padding: 60px 40px;
        text-align: center;
        margin: 40px 0;
    ">
        <div style="font-size:48px;margin-bottom:16px;">📡</div>
        <div style="font-family:'Syne',sans-serif;font-size:22px;font-weight:700;color:#E2E8F0;margin-bottom:8px;">
            Awaiting Data Feed
        </div>
        <div style="font-family:'Space Mono',monospace;font-size:12px;color:#334155;">
            Upload a CSV via the sidebar to initialise the detection engine
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()


# ─────────────────────────────────────────────
# LOAD MODEL
# ─────────────────────────────────────────────
try:
    model        = joblib.load("mule_detector.pkl")
    imputer      = joblib.load("imputer.pkl")
    top_features = joblib.load("top_features.pkl")
except Exception as e:
    st.error(f"Model files not found: {e}")
    st.stop()

try:
    feature_importance = pd.read_csv("feature_importance.csv")
except:
    feature_importance = None


# ─────────────────────────────────────────────
# PREPROCESSING
# ─────────────────────────────────────────────
raw_df = pd.read_csv(uploaded_file)
MAX_ROWS = 1000

if len(raw_df) > MAX_ROWS:
    st.warning(f"Large file detected. Using first {MAX_ROWS} rows for live demo.")
    raw_df = raw_df.head(MAX_ROWS)
df = raw_df.copy()

account_ids = df["Unnamed: 0"] if "Unnamed: 0" in df.columns else pd.Series(range(len(df)))
if "Unnamed: 0" in df.columns:
    df = df.drop(columns=["Unnamed: 0"])

actual = None
if "F3924" in df.columns:
    actual = df["F3924"]
    df = df.drop(columns=["F3924"])

categorical_cols = ['F2230','F3886','F3888','F3889','F3890','F3891','F3892','F3893']
for col in categorical_cols:
    if col in df.columns:
        df[col] = pd.factorize(df[col].astype(str))[0]

expected = list(imputer.feature_names_in_)
for col in expected:
    if col not in df.columns:
        df[col] = np.nan
df = df[expected]

df_imp   = pd.DataFrame(imputer.transform(df), columns=expected)
df_model = df_imp[top_features]

probs      = model.predict_proba(df_model)[:, 1]
risk_scores = probs * 100

results = pd.DataFrame({
    "Account_ID": account_ids.values,
    "Risk_Score":  risk_scores,
})
results["Risk_Level"] = results["Risk_Score"].apply(risk_level)
results["Alert"]      = results["Risk_Score"].apply(generate_alert)
results["Flagged"]    = results["Risk_Score"] >= threshold
if actual is not None:
    results["Actual_Label"] = actual.values


# ─────────────────────────────────────────────
# KPI METRICS
# ─────────────────────────────────────────────
total_acc   = len(results)
flagged_acc = int(results["Flagged"].sum())
critical_n  = int((results["Risk_Level"] == "Critical").sum())
high_n      = int((results["Risk_Level"] == "High").sum())
avg_risk    = results["Risk_Score"].mean()
flag_rate   = flagged_acc / total_acc * 100

st.markdown(f"""
<div class="kpi-grid">

  <div class="kpi-card blue">
    <div class="kpi-label">Total Accounts</div>
    <div class="kpi-value">{total_acc:,}</div>
    <div class="kpi-sub">records ingested</div>
  </div>

  <div class="kpi-card orange">
    <div class="kpi-label">Flagged Accounts</div>
    <div class="kpi-value">{flagged_acc:,}</div>
    <div class="kpi-sub">above threshold ({threshold}%)</div>
  </div>

  <div class="kpi-card red">
    <div class="kpi-label">Critical Risk</div>
    <div class="kpi-value">{critical_n:,}</div>
    <div class="kpi-sub">score ≥ 80 · immediate action</div>
  </div>

  <div class="kpi-card purple">
    <div class="kpi-label">Flag Rate</div>
    <div class="kpi-value">{flag_rate:.2f}%</div>
    <div class="kpi-sub">of total portfolio</div>
  </div>

  <div class="kpi-card green">
    <div class="kpi-label">Avg Risk Score</div>
    <div class="kpi-value">{avg_risk:.1f}</div>
    <div class="kpi-sub">portfolio mean</div>
  </div>

</div>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "RISK ANALYTICS",
    "FLAGGED ACCOUNTS",
    "DATA PREVIEW",
    "EXPLAINABILITY",
    "INVESTIGATION",
])


# ── Tab 1 · Risk Analytics ──────────────────
with tab1:
    st.markdown('<div class="sec-heading">Risk Score Distribution</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns([3, 2])

    with col_a:
        fig_hist = go.Figure()
        fig_hist.add_trace(go.Histogram(
            x=results["Risk_Score"],
            nbinsx=50,
            marker=dict(
                color=results["Risk_Score"],
                colorscale=[
                    [0.0,  "#00FFA3"],
                    [0.25, "#00C8FF"],
                    [0.6,  "#FF8C00"],
                    [1.0,  "#FF2D78"],
                ],
                line=dict(width=0),
            ),
            hovertemplate="Score range: %{x}<br>Count: %{y}<extra></extra>",
            name="",
        ))
        fig_hist.update_layout(
            **PLOT_LAYOUT,
            title="Account Risk Score Distribution",
            bargap=0.05,
            xaxis_title="Risk Score (%)",
            yaxis_title="Account Count",
        )
        # add threshold vline
        fig_hist.add_vline(
            x=threshold,
            line_color="#FF2D78",
            line_dash="dot",
            line_width=1.5,
            annotation_text=f" Threshold {threshold}%",
            annotation_font=dict(family="Space Mono", size=10, color="#FF2D78"),
        )
        st.plotly_chart(fig_hist, use_container_width=True)

    with col_b:
        level_counts = results["Risk_Level"].value_counts().reset_index()
        level_counts.columns = ["Risk_Level", "Count"]
        order = ["Critical", "High", "Medium", "Low"]
        level_counts["Risk_Level"] = pd.Categorical(level_counts["Risk_Level"], categories=order, ordered=True)
        level_counts = level_counts.sort_values("Risk_Level")

        fig_pie = go.Figure(go.Pie(
            labels=level_counts["Risk_Level"],
            values=level_counts["Count"],
            hole=0.68,
            marker=dict(
                colors=[RISK_COLORS.get(l, "#333") for l in level_counts["Risk_Level"]],
                line=dict(color="#020408", width=3),
            ),
            textfont=dict(family="Space Mono, monospace", size=10),
            hovertemplate="%{label}: %{value} accounts<br>%{percent}<extra></extra>",
        ))
        total_flagged_display = flagged_acc
        fig_pie.update_layout(
            **PLOT_LAYOUT,
            title="Risk Level Breakdown",
            annotations=[dict(
                text=f"<b style='font-size:18px'>{flagged_acc}</b><br><span style='font-size:10px;color:#475569'>FLAGGED</span>",
                x=0.5, y=0.5, showarrow=False,
                font=dict(family="Syne, sans-serif", color="#E2E8F0", size=14),
            )],
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # ── Cumulative risk curve ──
    st.markdown('<div class="sec-heading">Cumulative Risk Profile</div>', unsafe_allow_html=True)

    sorted_scores = np.sort(results["Risk_Score"].values)[::-1]
    x_pct = np.linspace(0, 100, len(sorted_scores))

    fig_cum = go.Figure()
    fig_cum.add_trace(go.Scatter(
        x=x_pct, y=sorted_scores,
        mode="lines",
        line=dict(color="#00C8FF", width=2),
        fill="tozeroy",
        fillcolor="rgba(0,200,255,0.05)",
        hovertemplate="Top %{x:.1f}% of accounts<br>Risk Score: %{y:.1f}%<extra></extra>",
        name="Risk Curve",
    ))
    fig_cum.add_hline(y=threshold, line_color="#FF2D78", line_dash="dot", line_width=1,
                      annotation_text=f" Flag Threshold", annotation_font=dict(family="Space Mono", size=9, color="#FF2D78"))
    fig_cum.update_layout(
        **PLOT_LAYOUT,
        title="Cumulative Risk Curve — Sorted by Score (Highest → Lowest)",
        xaxis_title="Accounts (Percentile %)",
        yaxis_title="Risk Score",
    )
    st.plotly_chart(fig_cum, use_container_width=True)


# ── Tab 2 · Flagged Accounts ────────────────
with tab2:
    st.markdown('<div class="sec-heading">High-Risk Account Registry</div>', unsafe_allow_html=True)

    flagged_df = results[results["Flagged"]].sort_values("Risk_Score", ascending=False).reset_index(drop=True)

    if flagged_df.empty:
        st.info("No accounts exceed the current threshold. Lower the slider to see flagged accounts.")
    else:
        # Mini bar chart of top 20
        top20 = flagged_df.head(20)
        colors_bar = [RISK_COLORS.get(l, "#00FFA3") for l in top20["Risk_Level"]]

        fig_bar = go.Figure(go.Bar(
            x=top20["Risk_Score"],
            y=top20["Account_ID"].astype(str),
            orientation="h",
            marker=dict(color=colors_bar, line=dict(width=0)),
            text=[f"{s:.1f}%" for s in top20["Risk_Score"]],
            textposition="inside",
            textfont=dict(family="Space Mono, monospace", size=9, color="#000"),
            hovertemplate="Account %{y}<br>Risk: %{x:.2f}%<extra></extra>",
            name="",
        ))
        _layout = {**PLOT_LAYOUT, "yaxis": {**PLOT_LAYOUT["yaxis"], "autorange": "reversed"}}
        fig_bar.update_layout(**_layout, title="Top 20 Highest-Risk Accounts",
                      xaxis_title="Risk Score (%)", height=420)
        st.plotly_chart(fig_bar, use_container_width=True)

        # Full table
        st.markdown('<div class="sec-heading">Full Flagged Account Table</div>', unsafe_allow_html=True)
        display_cols = ["Account_ID", "Risk_Score", "Risk_Level", "Alert"]
        if "Actual_Label" in flagged_df.columns:
            display_cols.append("Actual_Label")
        st.dataframe(
            flagged_df[display_cols].style.format({"Risk_Score": "{:.2f}%"}),
            use_container_width=True,
            height=340,
        )

        csv = results.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇  EXPORT FULL PREDICTION REPORT",
            data=csv,
            file_name="muleguard_predictions.csv",
            mime="text/csv",
        )


# ── Tab 3 · Data Preview ────────────────────
with tab3:
    st.markdown('<div class="sec-heading">Uploaded Dataset Preview</div>', unsafe_allow_html=True)
    st.dataframe(raw_df.head(50), use_container_width=True, height=380)

    col1, col2, col3 = st.columns(3)
    col1.metric("Rows", f"{len(raw_df):,}")
    col2.metric("Columns", f"{len(raw_df.columns):,}")
    col3.metric("Missing Values", f"{raw_df.isnull().sum().sum():,}")

    st.markdown('<div class="sec-heading">Column Summary</div>', unsafe_allow_html=True)
    # summary = raw_df.describe(include="all").T.reset_index()
    # summary.columns = ["Feature"] + list(summary.columns[1:])
    # st.dataframe(summary, use_container_width=True, height=300)


# ── Tab 4 · Explainability ──────────────────
with tab4:
    st.markdown('<div class="sec-heading">Model Explainability · Feature Intelligence</div>', unsafe_allow_html=True)

    st.markdown("""
    <div style="
        font-family:'Space Mono',monospace;font-size:12px;color:#475569;
        background:#060C14;border:1px solid #1E293B;border-radius:10px;
        padding:16px 20px;line-height:1.8;margin-bottom:16px;
    ">
    Model uses <strong style="color:#00FFA3">XGBoost</strong> with iterative imputation and top-k feature selection.
    SHAP values quantify each feature's contribution to the final risk score,
    providing investigators with auditable, evidence-based flagging.
    </div>
    """, unsafe_allow_html=True)

    if feature_importance is not None:
        top_imp = feature_importance.head(20).copy()

        fig_imp = go.Figure(go.Bar(
            x=top_imp["importance"],
            y=top_imp["feature"],
            orientation="h",
            marker=dict(
                color=top_imp["importance"],
                colorscale=[
                    [0.0, "#1E293B"],
                    [0.5, "#00C8FF"],
                    [1.0, "#00FFA3"],
                ],
                line=dict(width=0),
            ),
            text=[f"{v:.4f}" for v in top_imp["importance"]],
            textposition="inside",
            textfont=dict(family="Space Mono, monospace", size=9),
            hovertemplate="%{y}<br>Importance: %{x:.4f}<extra></extra>",
            name="",
        ))
        _layout = {**PLOT_LAYOUT, "yaxis": {**PLOT_LAYOUT["yaxis"], "autorange": "reversed"}}
        fig_imp.update_layout(**_layout, title="Top 20 Predictive Features — Importance Score",
                      xaxis_title="Feature Importance", height=520)
        st.plotly_chart(fig_imp, use_container_width=True)
    else:
        st.info("feature_importance.csv not found. Place it in the working directory.")

    st.markdown('<div class="sec-heading">SHAP Summary Plot</div>', unsafe_allow_html=True)
    try:
        st.image("shap_summary.png", use_container_width=True)
    except:
        st.markdown("""
        <div style="
            border:1px dashed #1E293B;border-radius:10px;padding:40px;text-align:center;
            font-family:'Space Mono',monospace;font-size:12px;color:#334155;
        ">
            shap_summary.png not found — add it to the working directory
        </div>
        """, unsafe_allow_html=True)


# ── Tab 5 · Investigation Panel ─────────────
with tab5:
    st.markdown('<div class="sec-heading">AI Investigation Console</div>', unsafe_allow_html=True)

    sorted_results = results.sort_values("Risk_Score", ascending=False)
    selected_id = st.selectbox(
        "Select Account for Deep Investigation",
        sorted_results["Account_ID"].head(200).values,
    )

    row = results[results["Account_ID"] == selected_id].iloc[0]
    level = row["Risk_Level"]
    score = row["Risk_Score"]
    clr   = score_color(level)

    # Score + badge + alert
    col_left, col_right = st.columns([1, 2])

    with col_left:
        st.markdown(f"""
        <div style="
            background:linear-gradient(135deg,#0D1520,#0A1018);
            border:1px solid #1E293B;
            border-top: 2px solid {clr};
            border-radius:12px;
            padding:28px 24px;
            text-align:center;
        ">
            <div style="font-family:'Space Mono',monospace;font-size:9px;letter-spacing:3px;color:#475569;margin-bottom:12px;">
                RISK SCORE
            </div>
            <div style="font-family:'Syne',sans-serif;font-size:64px;font-weight:800;letter-spacing:-3px;color:{clr};line-height:1;">
                {score:.0f}
            </div>
            <div style="font-family:'Space Mono',monospace;font-size:10px;color:#334155;margin-top:4px;">
                out of 100
            </div>
            <div style="margin-top:18px;">
                <span class="risk-badge {badge_class(level)}">{level} Risk</span>
            </div>
            <div style="
                margin-top:18px;
                font-family:'Space Mono',monospace;font-size:9px;letter-spacing:2px;
                color:#334155;border-top:1px solid #1E293B;padding-top:14px;
            ">
                ACCOUNT ID
                <div style="font-size:12px;color:#64748B;margin-top:4px;">{selected_id}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        st.markdown(f"""
        <div class="{alert_class(level)}" style="height:100%;min-height:200px;">
            <div style="font-family:'Space Mono',monospace;font-size:9px;letter-spacing:3px;color:{clr};margin-bottom:12px;">
                DETECTION ALERT
            </div>
            <div style="font-family:'Syne',sans-serif;font-size:15px;font-weight:600;color:#E2E8F0;margin-bottom:16px;line-height:1.5;">
                {row['Alert']}
            </div>
            <div style="font-family:'Space Mono',monospace;font-size:9px;letter-spacing:3px;color:#475569;margin-bottom:8px;">
                RECOMMENDED ACTION
            </div>
            <div style="font-family:'Syne',sans-serif;font-size:13px;color:#CBD5E1;line-height:1.6;">
                {recommended_action(level)}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Risk tier breakdown
    st.markdown('<div class="sec-heading">Portfolio Intelligence · Risk Tier Heatmap</div>', unsafe_allow_html=True)

    bins = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    labels = [f"{b}-{bins[i+1]}" for i, b in enumerate(bins[:-1])]
    results["Score_Band"] = pd.cut(results["Risk_Score"], bins=bins, labels=labels, include_lowest=True)
    band_counts = results["Score_Band"].value_counts().sort_index().reset_index()
    band_counts.columns = ["Band", "Count"]

    band_colors = []
    for b in band_counts["Band"]:
        lo = int(str(b).split("-")[0])
        if lo >= 80: band_colors.append("#FF2D78")
        elif lo >= 50: band_colors.append("#FF8C00")
        elif lo >= 20: band_colors.append("#EAB308")
        else: band_colors.append("#00FFA3")

    fig_band = go.Figure(go.Bar(
        x=band_counts["Band"].astype(str),
        y=band_counts["Count"],
        marker=dict(color=band_colors, line=dict(width=0)),
        text=band_counts["Count"],
        textposition="outside",
        textfont=dict(family="Space Mono, monospace", size=9, color="#64748B"),
        hovertemplate="Band: %{x}<br>Accounts: %{y}<extra></extra>",
        name="",
    ))
    fig_band.update_layout(
        **PLOT_LAYOUT,
        title="Account Count by Risk Score Band",
        xaxis_title="Risk Score Band",
        yaxis_title="Count",
    )
    st.plotly_chart(fig_band, use_container_width=True)


# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div style="
    margin-top: 60px;
    border-top: 1px solid #0F1F2E;
    padding-top: 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 10px;
">
    <div style="font-family:'Space Mono',monospace;font-size:10px;color:#1E293B;">
        MULEGUARD AI · v3.1.0 · FINANCIAL CRIME INTELLIGENCE PLATFORM
    </div>
    <div style="font-family:'Space Mono',monospace;font-size:10px;color:#1E293B;">
        XGBoost · SHAP · Iterative Imputer · Risk Scoring Engine
    </div>
</div>
""", unsafe_allow_html=True)