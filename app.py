import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random
import string

# ═══════════════════════════════════════════════════════════════
#  PAGE CONFIGURATION
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Hyundai Assembly Line QA & OPEX Analytics",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════
#  ENTERPRISE CSS - DARK INDUSTRIAL THEME
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;700&display=swap');

/* ── Hide Streamlit Chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── Root Variables (Dark Industrial Automotive Theme) ── */
:root {
    --obsidian-950: #0A0A0F;
    --obsidian-900: #12121A;
    --obsidian-800: #1A1A28;
    --obsidian-700: #22223A;
    --charcoal-800: #1E2228;
    --charcoal-700: #262C35;
    --charcoal-600: #313842;
    --charcoal-500: #3F4752;
    --slate-400:    #94A3B8;
    --slate-300:    #CBD5E1;
    --slate-200:    #E2E8F0;
    --slate-100:    #F1F5F9;
    --neon-blue:    #0EA5E9;
    --neon-cyan:    #06B6D4;
    --neon-sky:     #38BDF8;
    --amber-500:    #F59E0B;
    --amber-400:    #FBBF24;
    --red-500:      #EF4444;
    --red-400:      #F87171;
    --green-500:    #10B981;
    --green-400:    #34D399;
    --text-pri:     #F1F5F9;
    --text-sec:     #94A3B8;
    --text-mut:     #64748B;
    --border:       rgba(14,165,233,0.12);
    --border-md:    rgba(14,165,233,0.18);
    --r-xl: 16px;
    --r-lg: 12px;
    --r-md: 8px;
    --shadow: 0 4px 32px rgba(0,0,0,0.6), 0 2px 8px rgba(0,0,0,0.5);
}

/* ── App Background ── */
.stApp {
    background: linear-gradient(160deg, #0A0A0F 0%, #12121A 40%, #1A1A28 100%);
    font-family: 'Inter', system-ui, sans-serif;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #12121A 0%, #0A0A0F 100%) !important;
    border-right: 1px solid var(--border-md) !important;
}
[data-testid="stSidebar"] * { color: var(--text-sec) !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { 
    color: var(--text-pri) !important; 
    font-weight: 800 !important;
}
[data-testid="stSidebar"] .stMultiSelect > label {
    color: var(--text-sec) !important; 
    font-size: 0.75rem !important; 
    font-weight: 700 !important; 
    text-transform: uppercase; 
    letter-spacing: 0.08em; 
}

/* ── Metrics (Neon Blue Industrial Theme) ── */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(18,18,26,0.95) 0%, rgba(26,26,40,0.9) 100%) !important;
    border: 1px solid var(--border-md) !important;
    border-radius: var(--r-xl) !important;
    padding: 22px 24px !important;
    box-shadow: var(--shadow) !important;
    position: relative !important;
    overflow: hidden !important;
}
[data-testid="stMetric"]::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; height: 3px;
    background: linear-gradient(90deg, var(--neon-blue), var(--neon-cyan));
}
[data-testid="stMetricLabel"] > div {
    font-family: 'Inter', sans-serif !important;
    font-size: 0.68rem !important;
    font-weight: 800 !important;
    color: var(--text-mut) !important;
    text-transform: uppercase !important;
    letter-spacing: 0.12em !important;
}
[data-testid="stMetricValue"] > div {
    font-family: 'Inter', sans-serif !important;
    font-size: 2.0rem !important;
    font-weight: 900 !important;
    color: var(--text-pri) !important;
    letter-spacing: -0.04em !important;
}
[data-testid="stMetricDelta"] > div {
    font-size: 0.70rem !important;
    font-weight: 700 !important;
}
[data-testid="stMetricDelta"][data-color="positive"] { color: var(--green-400) !important; }
[data-testid="stMetricDelta"][data-color="negative"] { color: var(--red-400) !important; }

/* ── Plotly ── */
.js-plotly-plot .plotly { background: transparent !important; }

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    border: 1px solid var(--border) !important;
    border-radius: var(--r-lg) !important;
    overflow: hidden !important;
}

/* ── Markdown ── */
.main [data-testid="stMarkdownContainer"] h1,
.main [data-testid="stMarkdownContainer"] h2,
.main [data-testid="stMarkdownContainer"] h3 { 
    color: var(--text-pri) !important; 
    font-weight: 900 !important;
}
.main [data-testid="stMarkdownContainer"] p { color: var(--text-sec) !important; }
.main [data-testid="stMarkdownContainer"] strong { color: var(--neon-sky) !important; }
.main [data-testid="stMarkdownContainer"] code {
    background: rgba(14,165,233,0.1) !important;
    color: var(--neon-cyan) !important;
    border-radius: 4px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.82em !important;
    padding: 2px 7px !important;
}

/* ── Divider ── */
hr { border-color: var(--border-md) !important; margin: 24px 0 !important; }

/* ── Column gaps ── */
[data-testid="column"] { padding: 0 8px !important; }

/* ── Animation ── */
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(24px); }
    to { opacity: 1; transform: translateY(0); }
}
[data-testid="stMetric"] {
    animation: fadeUp 0.5s ease both;
}
[data-testid="stMetric"]:nth-child(1) { animation-delay: 0.06s; }
[data-testid="stMetric"]:nth-child(2) { animation-delay: 0.12s; }
[data-testid="stMetric"]:nth-child(3) { animation-delay: 0.18s; }
[data-testid="stMetric"]:nth-child(4) { animation-delay: 0.24s; }

/* ── Subheader ── */
[data-testid="stSubheader"] { 
    color: var(--text-pri) !important; 
    font-weight: 900 !important; 
    font-size: 1.1rem !important;
}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
#  DATA GENERATION
# ═══════════════════════════════════════════════════════════════
@st.cache_data
def generate_assembly_data(num_records=1000):
    """
    Generate highly realistic Hyundai assembly line QA dataset.
    82% Pass rate, 18% Rework rate.
    """
    np.random.seed(42)
    random.seed(42)
    
    # Date range: last 7 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=6)
    date_range = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Models
    models = ['Tucson', 'Elantra', 'Sonata', 'Santa Fe']
    model_weights = [0.30, 0.35, 0.20, 0.15]  # Production mix
    
    # Assembly stages
    stages = ['Welding', 'Paint Shop', 'General Assembly', 'Final Inspection']
    
    # Defect types with realistic rework costs
    defect_cost_map = {
        'None':                  0,
        'Paint Blemish':       150,
        'Panel Gap':           220,
        'Electrical Fault':    480,
        'Transmission Sensor': 820,
        'Engine Mount':        650
    }
    
    data = []
    
    for i in range(num_records):
        # Random VIN (17 characters, alphanumeric)
        vin = ''.join(random.choices(string.ascii_uppercase + string.digits, k=17))
        
        # Random date from last 7 days
        date = random.choice(date_range)
        
        # Model (weighted)
        model = np.random.choice(models, p=model_weights)
        
        # Assembly stage
        stage = random.choice(stages)
        
        # Status: 82% Pass, 18% Rework
        status = 'Passed' if random.random() < 0.82 else 'Rework Required'
        
        # Defect type and cost
        if status == 'Passed':
            defect_type = 'None'
            rework_cost = 0
        else:
            # Weighted defect distribution (more common defects have higher probability)
            defect_types = ['Paint Blemish', 'Panel Gap', 'Electrical Fault', 
                          'Transmission Sensor', 'Engine Mount']
            defect_weights = [0.35, 0.30, 0.20, 0.10, 0.05]
            defect_type = np.random.choice(defect_types, p=defect_weights)
            rework_cost = defect_cost_map[defect_type]
            
            # Add some variance to rework cost (±15%)
            variance = rework_cost * np.random.uniform(-0.15, 0.15)
            rework_cost = int(rework_cost + variance)
        
        data.append({
            'VIN': vin,
            'Date': date,
            'Model': model,
            'Assembly_Stage': stage,
            'Status': status,
            'Defect_Type': defect_type,
            'Rework_Cost_USD': rework_cost
        })
    
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])
    return df

# ═══════════════════════════════════════════════════════════════
#  PLOTLY THEME
# ═══════════════════════════════════════════════════════════════
PLOTLY_LAYOUT = dict(
    template="plotly_dark",
    font_family="Inter, system-ui, sans-serif",
    font_color="#94A3B8",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=10, r=10, t=40, b=10),
    legend=dict(
        bgcolor="rgba(14,165,233,0.05)",
        bordercolor="rgba(14,165,233,0.15)",
        borderwidth=1,
        font=dict(color="#CBD5E1", size=11),
    ),
    title_font=dict(size=14, color="#F1F5F9", family="Inter"),
    xaxis=dict(
        gridcolor="rgba(14,165,233,0.08)",
        linecolor="rgba(14,165,233,0.12)",
        tickfont=dict(color="#64748B", size=10),
        showgrid=True,
    ),
    yaxis=dict(
        gridcolor="rgba(14,165,233,0.08)",
        linecolor="rgba(14,165,233,0.12)",
        tickfont=dict(color="#64748B", size=10),
        showgrid=True,
    ),
)
NEON_BLUE = "#0EA5E9"
NEON_CYAN = "#06B6D4"
NEON_SKY  = "#38BDF8"
AMBER     = "#FBBF24"
RED       = "#F87171"

# ═══════════════════════════════════════════════════════════════
#  HEADER
# ═══════════════════════════════════════════════════════════════
st.markdown("""
<div style="
    background: linear-gradient(135deg, rgba(14,165,233,0.12) 0%, rgba(18,18,26,0.8) 100%);
    border: 1px solid rgba(14,165,233,0.20);
    border-left: 4px solid #0EA5E9;
    border-radius: 18px;
    padding: 26px 34px;
    margin-bottom: 32px;
    display: flex; align-items: center; justify-content: space-between;
    flex-wrap: wrap; gap: 16px;
">
    <div>
        <div style="font-family:'Inter',sans-serif; font-size:2.0rem; font-weight:900;
                    color:#F1F5F9; letter-spacing:-0.04em; line-height:1.1; margin-bottom:7px;">
            🏭 Hyundai Assembly Line QA & OPEX Analytics Engine
        </div>
        <div style="font-family:'Inter',sans-serif; font-size:0.90rem; color:#94A3B8; line-height:1.5;">
            Real-time production quality monitoring, defect tracking, and operational expenditure analysis
        </div>
    </div>
    <div style="display:flex; gap:12px; align-items:center; flex-wrap:wrap;">
        <span style="
            font-family:'Inter',sans-serif; font-size:0.68rem; font-weight:900;
            color:#38BDF8; background:rgba(14,165,233,0.15); border:1px solid rgba(56,189,248,0.3);
            padding:7px 16px; border-radius:99px; text-transform:uppercase; letter-spacing:.12em;
            display:flex; align-items:center; gap:7px;">
            <span style="width:7px;height:7px;background:#38BDF8;border-radius:50%;
                         box-shadow:0 0 10px #38BDF8;display:inline-block"></span>
            LIVE PRODUCTION
        </span>
        <span style="
            font-family:'Inter',sans-serif; font-size:0.68rem; font-weight:900;
            color:#FBBF24; background:rgba(251,191,36,0.12); border:1px solid rgba(251,191,36,0.25);
            padding:7px 16px; border-radius:99px; letter-spacing:.06em;">
            Models: Tucson • Elantra • Sonata • Santa Fe
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
#  LOAD DATA
# ═══════════════════════════════════════════════════════════════
df_full = generate_assembly_data(1000)

# ═══════════════════════════════════════════════════════════════
#  SIDEBAR - FILTERS
# ═══════════════════════════════════════════════════════════════
with st.sidebar:
    # Logo area
    st.markdown("""
    <div style="text-align:center; padding: 12px 0 20px;">
        <div style="font-size:3.2rem; margin-bottom:10px;">🏭</div>
        <div style="font-family:'Inter',sans-serif; font-size:1.1rem; font-weight:900;
                    color:#F1F5F9; letter-spacing:-0.03em;">Hyundai QA</div>
        <div style="font-family:'Inter',sans-serif; font-size:0.68rem; font-weight:900;
                    color:#0EA5E9; text-transform:uppercase; letter-spacing:.16em;">Analytics v3.1</div>
        <div style="margin-top:14px; padding:6px 16px; border-radius:99px;
                    background:rgba(14,165,233,0.12); border:1px solid rgba(14,165,233,0.25);
                    display:inline-block; font-size:0.68rem; font-weight:800; color:#38BDF8;">
            Production Floor Monitor
        </div>
    </div>
    <hr style="border-color:rgba(14,165,233,0.15); margin: 0 0 20px;">
    """, unsafe_allow_html=True)

    st.header("📊 Dashboard Filters")
    
    # Date range filter
    date_options = sorted(df_full['Date'].dt.date.unique())
    selected_dates = st.multiselect(
        "Select Date Range",
        options=date_options,
        default=date_options,
        help="Filter production data by date"
    )
    
    # Model filter
    model_options = sorted(df_full['Model'].unique())
    selected_models = st.multiselect(
        "Select Vehicle Models",
        options=model_options,
        default=model_options,
        help="Filter by specific Hyundai models"
    )
    
    st.markdown("---")
    
    # Info card
    st.markdown("""
    <div style="
        background:rgba(14,165,233,0.08); border:1px solid rgba(14,165,233,0.18);
        border-radius:12px; padding:16px 18px; margin-top:8px;
    ">
        <div style="font-family:'Inter',sans-serif; font-size:0.70rem; font-weight:900;
                    color:#0EA5E9; text-transform:uppercase; letter-spacing:.12em; margin-bottom:8px;">
            System Engineer
        </div>
        <div style="font-family:'Inter',sans-serif; font-size:0.90rem; font-weight:800;
                    color:#F1F5F9;">Lokesh Kumar</div>
        <div style="font-size:0.72rem; color:#94A3B8; margin-top:4px;">
            Automotive Analytics & Quality Systems
        </div>
    </div>
    <div style="font-family:'Inter',sans-serif; font-size:0.68rem; color:#64748B;
                margin-top:14px; padding-left:2px; line-height:1.7;">
        Enterprise-grade dashboard for floor managers tracking FTT yield, defect patterns, and OPEX optimization.
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
#  APPLY FILTERS
# ═══════════════════════════════════════════════════════════════
df_filtered = df_full[
    (df_full['Date'].dt.date.isin(selected_dates)) &
    (df_full['Model'].isin(selected_models))
].copy()

# ═══════════════════════════════════════════════════════════════
#  CALCULATE METRICS
# ═══════════════════════════════════════════════════════════════
total_production = len(df_filtered)
total_passed     = len(df_filtered[df_filtered['Status'] == 'Passed'])
total_rework     = len(df_filtered[df_filtered['Status'] == 'Rework Required'])
ftt_yield        = (total_passed / total_production * 100) if total_production > 0 else 0
total_rework_cost = df_filtered['Rework_Cost_USD'].sum()

# Critical bottleneck: Stage with most defects
defect_by_stage = df_filtered[df_filtered['Status'] == 'Rework Required']['Assembly_Stage'].value_counts()
critical_bottleneck = defect_by_stage.index[0] if len(defect_by_stage) > 0 else "N/A"
bottleneck_count = defect_by_stage.iloc[0] if len(defect_by_stage) > 0 else 0

# ═══════════════════════════════════════════════════════════════
#  TOP KPI GRID
# ═══════════════════════════════════════════════════════════════
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

with kpi1:
    st.metric(
        "🚗 Total Production Volume",
        f"{total_production:,}",
        f"{len(selected_dates)} days"
    )

with kpi2:
    ftt_delta = "✓ Target Met" if ftt_yield >= 82 else "⚠ Below Target"
    delta_color = "normal" if ftt_yield >= 82 else "inverse"
    st.metric(
        "✅ First Time Through (FTT) Yield",
        f"{ftt_yield:.1f}%",
        ftt_delta,
        delta_color=delta_color
    )

with kpi3:
    st.metric(
        "💰 Total Rework OPEX",
        f"${total_rework_cost:,}",
        f"{total_rework} units"
    )

with kpi4:
    st.metric(
        "🔧 Critical Bottleneck",
        critical_bottleneck,
        f"{bottleneck_count} defects",
        delta_color="inverse"
    )

st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
#  SECTION LABEL HELPER
# ═══════════════════════════════════════════════════════════════
def section_label(text):
    st.markdown(f"""
    <div style="font-family:'Inter',sans-serif; font-size:0.70rem; font-weight:900;
                color:#64748B; text-transform:uppercase; letter-spacing:.14em;
                margin:0 0 16px; padding-left:2px;">
        {text}
    </div>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
#  VISUALIZATION ROW 1: TREND + FINANCIAL
# ═══════════════════════════════════════════════════════════════
section_label("Quality Performance & Financial Impact Analysis")

viz_col1, viz_col2 = st.columns([1, 1], gap="large")

with viz_col1:
    st.markdown("""
    <div style="font-family:'Inter',sans-serif; font-size:0.95rem; font-weight:900;
                color:#F1F5F9; margin-bottom:14px; letter-spacing:-0.01em;">
        📈 Daily FTT Yield Trend (Last 7 Days)
    </div>""", unsafe_allow_html=True)
    
    # Calculate daily FTT yield
    df_daily = df_filtered.groupby('Date').agg({
        'Status': lambda x: (x == 'Passed').sum() / len(x) * 100
    }).reset_index()
    df_daily.columns = ['Date', 'FTT_Yield']
    df_daily = df_daily.sort_values('Date')
    
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=df_daily['Date'],
        y=df_daily['FTT_Yield'],
        mode='lines+markers',
        name='FTT Yield %',
        line=dict(color=NEON_BLUE, width=3),
        marker=dict(size=8, color=NEON_CYAN, line=dict(width=2, color=NEON_SKY)),
        fill='tozeroy',
        fillcolor='rgba(14,165,233,0.12)',
        hovertemplate='<b>%{x|%b %d}</b><br>FTT Yield: %{y:.1f}%<extra></extra>'
    ))
    
    # Add target line at 82%
    fig_trend.add_hline(
        y=82, 
        line_dash='dash', 
        line_color='#34D399', 
        line_width=2,
        annotation_text="Target: 82%",
        annotation_font_color='#34D399',
        annotation_font_size=10
    )
    
    fig_trend.update_layout(
        **PLOTLY_LAYOUT,
        height=320,
        xaxis_title="Production Date",
        yaxis_title="FTT Yield (%)",
        yaxis_range=[0, 100],
        showlegend=False,
    )
    st.plotly_chart(fig_trend, use_container_width=True)

with viz_col2:
    st.markdown("""
    <div style="font-family:'Inter',sans-serif; font-size:0.95rem; font-weight:900;
                color:#F1F5F9; margin-bottom:14px; letter-spacing:-0.01em;">
        💵 Rework Cost Breakdown by Defect Type
    </div>""", unsafe_allow_html=True)
    
    # Calculate total cost by defect type
    df_defect_cost = df_filtered[df_filtered['Status'] == 'Rework Required'].groupby('Defect_Type').agg({
        'Rework_Cost_USD': 'sum'
    }).reset_index().sort_values('Rework_Cost_USD', ascending=True)
    
    fig_cost = go.Figure()
    fig_cost.add_trace(go.Bar(
        y=df_defect_cost['Defect_Type'],
        x=df_defect_cost['Rework_Cost_USD'],
        orientation='h',
        marker=dict(
            color=df_defect_cost['Rework_Cost_USD'],
            colorscale=[[0, NEON_BLUE], [0.5, NEON_CYAN], [1, AMBER]],
            line=dict(color=NEON_SKY, width=1.5)
        ),
        text=df_defect_cost['Rework_Cost_USD'].apply(lambda x: f'${x:,.0f}'),
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Total Cost: $%{x:,.0f}<extra></extra>'
    ))
    
    fig_cost.update_layout(
        **PLOTLY_LAYOUT,
        height=320,
        xaxis_title="Total Rework Cost (USD)",
        yaxis_title="",
        showlegend=False,
    )
    st.plotly_chart(fig_cost, use_container_width=True)

st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
#  VISUALIZATION ROW 2: PRODUCTION MIX
# ═══════════════════════════════════════════════════════════════
section_label("Production Volume Distribution")

viz_col3, viz_col4 = st.columns([1, 1.5], gap="large")

with viz_col3:
    st.markdown("""
    <div style="font-family:'Inter',sans-serif; font-size:0.95rem; font-weight:900;
                color:#F1F5F9; margin-bottom:14px; letter-spacing:-0.01em;">
        🚙 Production Mix by Model
    </div>""", unsafe_allow_html=True)
    
    df_model_mix = df_filtered['Model'].value_counts().reset_index()
    df_model_mix.columns = ['Model', 'Count']
    
    fig_donut = px.pie(
        df_model_mix, 
        names='Model', 
        values='Count',
        hole=0.55,
        color='Model',
        color_discrete_sequence=[NEON_BLUE, NEON_CYAN, NEON_SKY, AMBER]
    )
    fig_donut.update_traces(
        textposition='outside', 
        textinfo='label+percent',
        marker=dict(line=dict(color='rgba(0,0,0,0.4)', width=2.5)),
        hovertemplate="<b>%{label}</b><br>Units: %{value:,}<br>Share: %{percent}<extra></extra>"
    )
    fig_donut.update_layout(
        **PLOTLY_LAYOUT,
        showlegend=False,
        height=320,
        annotations=[dict(
            text=f'{total_production:,}<br><span style="font-size:0.7em">Total Units</span>',
            x=0.5, y=0.5,
            font_size=20,
            showarrow=False,
            font_color='#F1F5F9'
        )]
    )
    st.plotly_chart(fig_donut, use_container_width=True)

with viz_col4:
    st.markdown("""
    <div style="font-family:'Inter',sans-serif; font-size:0.95rem; font-weight:900;
                color:#F1F5F9; margin-bottom:14px; letter-spacing:-0.01em;">
        🔍 Defect Distribution by Assembly Stage
    </div>""", unsafe_allow_html=True)
    
    df_stage_defects = df_filtered[df_filtered['Status'] == 'Rework Required']['Assembly_Stage'].value_counts().reset_index()
    df_stage_defects.columns = ['Stage', 'Defect_Count']
    
    fig_stage = go.Figure()
    fig_stage.add_trace(go.Bar(
        x=df_stage_defects['Stage'],
        y=df_stage_defects['Defect_Count'],
        marker=dict(
            color=df_stage_defects['Defect_Count'],
            colorscale=[[0, NEON_CYAN], [0.6, AMBER], [1, RED]],
            line=dict(color=NEON_SKY, width=1.5)
        ),
        text=df_stage_defects['Defect_Count'],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Defects: %{y}<extra></extra>'
    ))
    
    fig_stage.update_layout(
        **PLOTLY_LAYOUT,
        height=320,
        xaxis_title="Assembly Stage",
        yaxis_title="Defect Count",
        showlegend=False,
    )
    st.plotly_chart(fig_stage, use_container_width=True)

st.markdown("<div style='height:32px'></div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
#  ACTIVE REWORK LOG
# ═══════════════════════════════════════════════════════════════
section_label("Actionable Floor Data — Priority Rework Queue")

st.markdown("""
<div style="font-family:'Inter',sans-serif; font-size:0.95rem; font-weight:900;
            color:#F1F5F9; margin-bottom:14px; letter-spacing:-0.01em;">
    🔧 Active Rework Log (Sorted by Cost — Floor Manager Priority View)
</div>""", unsafe_allow_html=True)

df_rework = df_filtered[df_filtered['Status'] == 'Rework Required'].copy()
df_rework = df_rework.sort_values('Rework_Cost_USD', ascending=False)
df_rework_display = df_rework[['VIN', 'Date', 'Model', 'Assembly_Stage', 'Defect_Type', 'Rework_Cost_USD']].copy()
df_rework_display['Date'] = df_rework_display['Date'].dt.strftime('%Y-%m-%d')
df_rework_display.columns = ['VIN', 'Date', 'Model', 'Assembly Stage', 'Defect Type', 'Rework Cost (USD)']

st.dataframe(
    df_rework_display,
    use_container_width=True,
    hide_index=True,
    height=400
)

st.markdown(f"""
<div style="
    background: linear-gradient(135deg, rgba(14,165,233,0.10) 0%, rgba(18,18,26,0.6) 100%);
    border: 1px solid rgba(14,165,233,0.22); border-left: 3px solid #0EA5E9;
    border-radius: 14px; padding: 18px 22px; margin-top: 20px;
    font-family: 'Inter', sans-serif;
">
    <div style="font-size:0.72rem;font-weight:900;color:#64748B;
                text-transform:uppercase;letter-spacing:.12em;margin-bottom:10px">
        📋 Floor Manager Action Summary
    </div>
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin-top:12px">
        <div>
            <div style="font-size:0.70rem;color:#94A3B8;margin-bottom:4px">Units Requiring Rework</div>
            <div style="font-size:1.4rem;font-weight:900;color:#F87171">{total_rework}</div>
        </div>
        <div>
            <div style="font-size:0.70rem;color:#94A3B8;margin-bottom:4px">Total OPEX Impact</div>
            <div style="font-size:1.4rem;font-weight:900;color:#FBBF24">${total_rework_cost:,}</div>
        </div>
        <div>
            <div style="font-size:0.70rem;color:#94A3B8;margin-bottom:4px">Avg. Cost per Rework</div>
            <div style="font-size:1.4rem;font-weight:900;color:#38BDF8">${int(total_rework_cost / total_rework) if total_rework > 0 else 0}</div>
        </div>
    </div>
    <div style="margin-top:16px;padding:12px 16px;background:rgba(14,165,233,0.08);
                border-radius:10px;font-size:0.80rem;color:#94A3B8;line-height:1.7">
        <strong style="color:#38BDF8">Recommendation:</strong> Prioritize high-cost rework items (Transmission Sensor, Engine Mount) 
        for immediate floor attention. Paint Shop showing elevated defect rate — consider process audit.
    </div>
</div>""", unsafe_allow_html=True)
