import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import math
import os

# ==================================================
# KONFIGURASI HALAMAN
# ==================================================
st.set_page_config(
    page_title="Analisis Defisit Finansial Mahasiswa UIN Pekalongan",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# CUSTOM CSS — TEMA AKADEMIK PREMIUM (FULL DARK)
# ==================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* { font-family: 'Inter', sans-serif; }

/* === MAIN BACKGROUND - FIX WHITE AREAS === */
.stApp {
    background-color: #0B1120 !important;
    color: #CBD5E1 !important;
}

/* Main container */
[data-testid="stMainBlock"] { background-color: #0B1120 !important; }
[data-testid="stHeader"] { background-color: #0B1120 !important; }
section[data-testid="stSidebar"] + div { background-color: #0B1120 !important; }

/* === FIX ALL WHITE STREAMLIT DEFAULTS === */
[data-testid="stBaseButton-header"],
[data-testid="stBaseButton-secondary"],
[data-testid="stBaseButton-primary"] {
    background-color: #0F1C36 !important;
    color: #CBD5E1 !important;
}

/* === Sidebar === */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0F1C36 0%, #0B1120 100%) !important;
    border-right: 1px solid #1E3A5F;
}
[data-testid="stSidebar"] * { color: #CBD5E1 !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #93C5FD !important; }

/* === Selectbox / Inputs DARK MODE === */
.stSelectbox > div > div,
.stMultiSelect > div > div,
.stNumberInput input,
.stTextInput input,
.stTextArea textarea {
    background-color: #0F1C36 !important;
    color: #CBD5E1 !important;
    border: 1px solid #1E3A5F !important;
    border-radius: 8px !important;
}

.stSelectbox label,
.stSlider label,
.stNumberInput label {
    color: #94A3B8 !important;
}

/* Selectbox dropdown */
[data-baseweb="select"] > div {
    background-color: #0F1C36 !important;
    color: #CBD5E1 !important;
}

[data-baseweb="select"] ul {
    background-color: #0F1C36 !important;
}

[data-baseweb="select"] ul li {
    background-color: #0F1C36 !important;
    color: #CBD5E1 !important;
}

[data-baseweb="select"] ul li:hover {
    background-color: #1E3A5F !important;
}

/* === DataFrame - FIX WHITE === */
.stDataFrame {
    background-color: #0F1C36 !important;
    border: 1px solid #1E3A5F !important;
    border-radius: 10px !important;
    overflow: hidden;
}

.stDataFrame > div {
    background-color: #0F1C36 !important;
}

.stDataFrame [data-testid="stDataFrameResizable"] {
    background-color: #0F1C36 !important;
}

/* === Radio / Checkbox === */
.stRadio label,
.stCheckbox label {
    color: #CBD5E1 !important;
}

.stRadio > div {
    flex-direction: column !important;
}

/* === Slider === */
.stSlider > div > div > div {
    background-color: #1D4ED8 !important;
}

/* === Tabs DARK === */
.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: transparent !important;
    border-bottom: 2px solid #1E3A5F;
    padding-bottom: 0;
}

.stTabs [data-baseweb="tab"] {
    background: #0B1120 !important;
    border-radius: 8px 8px 0 0;
    color: #94A3B8 !important;
    padding: 10px 22px;
    font-size: 13px;
    font-weight: 500;
    border: 1px solid #1E3A5F;
    border-bottom: none;
    margin-bottom: -2px;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(180deg, #1D4ED8 0%, #1E3A8A 100%) !important;
    color: #FFFFFF !important;
    font-weight: 700;
    border-color: #2563EB !important;
}

/* === Alerts DARK === */
.stAlert {
    background-color: #0F1C36 !important;
    border: 1px solid #1E3A5F !important;
    border-radius: 10px !important;
    color: #CBD5E1 !important;
}

div[data-testid="stAlert"] {
    background-color: #0F1C36 !important;
}

/* Success / Warning / Error */
[data-baseweb="notification"] {
    background-color: #0F1C36 !important;
    border: 1px solid #1E3A5F !important;
}

/* === Typography === */
h1, h2, h3, h4, h5, h6 {
    color: #E2E8F0 !important;
}

p, span, li {
    color: #CBD5E1 !important;
}

hr {
    border: none;
    height: 1px;
    background: #1E3A5F !important;
    margin: 24px 0;
}

/* === Page banner === */
.page-banner {
    background: linear-gradient(135deg, #0F2044 0%, #1A3A6E 50%, #0F2044 100%);
    border: 1px solid #2563EB;
    border-radius: 16px;
    padding: 28px 36px;
    margin-bottom: 32px;
    box-shadow: 0 8px 32px rgba(37, 99, 235, 0.2);
}
.page-banner h1 {
    font-size: 22px !important;
    font-weight: 700;
    color: #93C5FD !important;
    margin: 0 0 6px 0 !important;
    border: none !important;
    padding: 0 !important;
}
.page-banner .subtitle {
    font-size: 13px;
    color: #64748B;
    letter-spacing: 0.5px;
}
.page-banner .subtitle span {
    color: #3B82F6;
    font-weight: 600;
}

/* === Section heading === */
.section-heading {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 36px 0 20px 0;
}
.section-heading .icon {
    width: 36px; height: 36px;
    background: linear-gradient(135deg, #1D4ED8, #2563EB);
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 18px; flex-shrink: 0;
}
.section-heading h2 {
    font-size: 17px !important;
    font-weight: 600 !important;
    color: #E2E8F0 !important;
    margin: 0 !important;
    border: none !important;
}
.section-heading .badge {
    margin-left: auto;
    background: #1E3A5F;
    color: #60A5FA;
    font-size: 11px;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 20px;
    letter-spacing: 0.5px;
}

/* === KPI Cards === */
.kpi-card {
    background: linear-gradient(145deg, #0F1C36 0%, #162040 100%);
    border: 1px solid #1E3A5F;
    border-radius: 14px;
    padding: 22px 20px;
    transition: all 0.25s ease;
    position: relative;
    overflow: hidden;
    height: 100%;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: var(--accent);
    border-radius: 14px 14px 0 0;
}
.kpi-card:hover {
    transform: translateY(-4px);
    border-color: #2563EB;
    box-shadow: 0 12px 32px rgba(37,99,235,0.2);
}
.kpi-label {
    font-size: 11px; font-weight: 600;
    color: #94A3B8;
    text-transform: uppercase;
    letter-spacing: 1.2px;
    margin-bottom: 10px;
}
.kpi-value {
    font-size: 28px; font-weight: 700;
    color: var(--accent);
    line-height: 1.1;
}
.kpi-sub {
    font-size: 11px;
    color: #64748B;
    margin-top: 8px;
}
.kpi-trend {
    font-size: 11px;
    margin-top: 6px;
}
.kpi-trend.up { color: #22C55E; }
.kpi-trend.down { color: #EF4444; }
.kpi-trend.neutral { color: #F59E0B; }

/* === Insight Cards === */
.insight-card {
    background: #0F1C36;
    border: 1px solid #1E3A5F;
    border-left: 4px solid var(--accent);
    border-radius: 10px;
    padding: 16px 18px;
}
.insight-card .ic-label {
    font-size: 10px; font-weight: 700;
    color: var(--accent);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 6px;
}
.insight-card .ic-val {
    font-size: 20px; font-weight: 700;
    color: #E2E8F0;
}
.insight-card .ic-desc {
    font-size: 11px;
    color: #94A3B8;
    margin-top: 4px;
}

/* === Stat table === */
.stat-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
    background: #0F1C36 !important;
}
.stat-table th {
    background: #0F1C36 !important;
    color: #3B82F6 !important;
    font-weight: 600;
    padding: 10px 14px;
    text-align: left;
    border-bottom: 2px solid #1E3A5F;
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}
.stat-table td {
    padding: 10px 14px;
    color: #CBD5E1 !important;
    border-bottom: 1px solid #1E3A5F;
    background: #0F1C36 !important;
}
.stat-table tr:last-child td { border-bottom: none; }
.stat-table tr:hover td { background: #162040 !important; }
.stat-table .val {
    font-weight: 600;
    color: #93C5FD !important;
    text-align: right;
}

/* === Risk badge === */
.risk-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.5px;
}
.risk-high { background: rgba(239,68,68,0.15); color: #EF4444; border: 1px solid rgba(239,68,68,0.3); }
.risk-med { background: rgba(245,158,11,0.15); color: #F59E0B; border: 1px solid rgba(245,158,11,0.3); }
.risk-low { background: rgba(34,197,94,0.15); color: #22C55E; border: 1px solid rgba(34,197,94,0.3); }

/* === Research box === */
.research-box {
    background: linear-gradient(135deg, #0F1C36, #0D2137);
    border: 1px solid #1E3A5F;
    border-radius: 12px;
    padding: 24px;
    margin: 12px 0;
}
.research-box h4 { color: #60A5FA; font-size: 14px; font-weight: 600; margin: 0 0 10px 0; }
.research-box p, .research-box li { color: #94A3B8; font-size: 13px; line-height: 1.7; }
.research-box ul { padding-left: 18px; margin: 8px 0; }

/* === Divider === */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #1E3A5F, transparent);
    margin: 28px 0;
}

/* === Footer === */
.footer {
    text-align: center;
    padding: 32px;
    color: #94A3B8;
    border-top: 1px solid #1E3A5F;
    margin-top: 48px;
    font-size: 12px;
    background: #0B1120;
}
.footer strong { color: #60A5FA; }

/* === Info Box === */
.info-box {
    background: #0F1C36 !important;
    border: 1px solid #1E3A5F !important;
    border-radius: 10px;
    padding: 14px;
    font-size: 12px;
    color: #64748B;
}

/* === Plotly fix for dark theme === */
.js-plotly-plot {
    background-color: #0F1C36 !important;
    border-radius: 10px;
}

/* Responsive */
@media (max-width: 768px) {
    .kpi-value { font-size: 22px; }
    .page-banner h1 { font-size: 18px !important; }
    .page-banner { padding: 18px; }
}
</style>
""", unsafe_allow_html=True)

# ==================================================
# PLOTLY TEMPLATE - DARK THEME
# ==================================================
CHART_BG = "#0F1C36"
PLOT_BG = "#0B1120"
FONT_COLOR = "#CBD5E1"
GRID_COLOR = "#1E3A5F"
ACCENT_BLUE = "#3B82F6"
ACCENT_RED = "#EF4444"
ACCENT_GREEN = "#22C55E"
ACCENT_AMBER = "#F59E0B"
ACCENT_PURPLE = "#A78BFA"

def apply_theme(fig, title="", height=380):
    fig.update_layout(
        title=dict(text=title, font=dict(size=14, color="#93C5FD"), x=0),
        paper_bgcolor=CHART_BG,
        plot_bgcolor=PLOT_BG,
        font=dict(color=FONT_COLOR, size=12),
        height=height,
        margin=dict(l=16, r=16, t=48 if title else 20, b=16),
        legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor=GRID_COLOR, font=dict(size=11)),
        xaxis=dict(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR, color=FONT_COLOR),
        yaxis=dict(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR, color=FONT_COLOR),
    )
    return fig

# ==================================================
# LOAD DATA - AUTO DETECT
# ==================================================
@st.cache_data
def load_data():
    candidates = [
        "Data_Pengeluaran_Mahasiswa.csv",
        "data_pengeluaran_mahasiswa.csv",
        "Data Pengeluaran Mahasiswa.csv",
    ]
    for fname in candidates:
        if os.path.exists(fname):
            # Coba berbagai separator
            for sep in [";", ",", "\t"]:
                try:
                    df = pd.read_csv(fname, sep=sep)
                    if len(df.columns) > 1:
                        df.columns = df.columns.str.strip()
                        return df
                except:
                    continue
    raise FileNotFoundError("File CSV tidak ditemukan.")

# ==================================================
# MAIN LOGIC
# ==================================================
try:
    df = load_data()
    
    # === AUTO-DETECT KOLOM BERDASARKAN KATA KUNCI ===
    def find_col(df, keywords, exclude=None):
        for col in df.columns:
            col_lower = col.lower()
            if any(kw.lower() in col_lower for kw in keywords):
                if exclude and any(ex.lower() in col_lower for ex in exclude):
                    continue
                return col
        return None
    
    COL_INCOME = find_col(df, ["Pemasukan", "Uang Saku", "Income", "Penerimaan"])
    COL_TOTAL = find_col(df, ["Total_Pengeluaran", "Total Pengeluaran", "TotalPengeluaran", "Total Expense"])
    COL_MAKAN = find_col(df, ["Makan"])
    COL_TRANS = find_col(df, ["Transport"])
    COL_HIBUR = find_col(df, ["Hiburan", "Entertainment"])
    COL_AKAD = find_col(df, ["Akademik", "Kas"])
    COL_PULSA = find_col(df, ["Pulsa", "Kuota"])
    COL_ONLINE = find_col(df, ["Belanja Online", "Online"])
    COL_SEMS = find_col(df, ["Semester"])
    COL_TING = find_col(df, ["Tempat Tinggal", "Tinggal"])
    COL_SRC = find_col(df, ["Sumber Pendapatan", "Sumber"])
    COL_PAY = find_col(df, ["Metode Pembayaran", "Pembayaran"])
    
    # Validasi kolom penting
    if not COL_INCOME or not COL_TOTAL:
        st.error("❌ Kolom Pemasukan atau Total Pengeluaran tidak ditemukan di dataset Anda.")
        st.info(f"💡 **Kolom yang terdeteksi di CSV:** {df.columns.tolist()}")
        st.info("Pastikan dataset memiliki kolom yang mengandung kata 'Pemasukan/Uang Saku' dan 'Total Pengeluaran'.")
        st.stop()
    
    # Pastikan data numerik
    df[COL_INCOME] = pd.to_numeric(df[COL_INCOME], errors='coerce')
    df[COL_TOTAL] = pd.to_numeric(df[COL_TOTAL], errors='coerce')
    df = df.dropna(subset=[COL_INCOME, COL_TOTAL])
    
    # ==================================================
    # SIDEBAR
    # ==================================================
    with st.sidebar:
        st.markdown("## 🎓 Kontrol Dashboard")
        st.markdown("---")
        st.markdown("### 🔬 Simulasi Monte Carlo")
        n_sim = st.slider("Jumlah Iterasi", 1000, 50000, 10000, 1000,
                         help="Semakin banyak iterasi = hasil semakin akurat")
        seed_val = st.number_input("Random Seed", value=42, min_value=0, max_value=999,
                                  help="Seed tetap = hasil reproducible")
        
        st.markdown("---")
        st.markdown("### 🔍 Filter Data")
        
        sems_sel = "Semua"
        if COL_SEMS:
            sems_opt = ["Semua"] + sorted([str(x) for x in df[COL_SEMS].unique().tolist()])
            sems_sel = st.selectbox("Semester", sems_opt)
        
        ting_sel = "Semua"
        if COL_TING:
            ting_opt = ["Semua"] + sorted([str(x) for x in df[COL_TING].unique().tolist()])
            ting_sel = st.selectbox("Tempat Tinggal", ting_opt)
        
        st.markdown("---")
        st.markdown(f"""
        <div class="info-box">
        📁 <strong style="color:#3B82F6">Dataset Info</strong><br><br>
        Responden: <strong style="color:#93C5FD">{len(df)} mahasiswa</strong><br>
        Institusi: UIN K.H. Abdurrahman Wahid<br>
        Periode: 2026<br>
        Metode: Monte Carlo Simulation
        </div>
        """, unsafe_allow_html=True)
    
    # Apply filter
    dff = df.copy()
    if COL_SEMS and sems_sel != "Semua":
        dff = dff[dff[COL_SEMS].astype(str) == str(sems_sel)]
    if COL_TING and ting_sel != "Semua":
        dff = dff[dff[COL_TING].astype(str) == str(ting_sel)]
    
    if len(dff) == 0:
        st.warning("⚠️ Tidak ada data yang cocok dengan filter yang dipilih.")
        st.stop()
    
    # ==================================================
    # CALCULATIONS
    # ==================================================
    mean_income = dff[COL_INCOME].mean()
    std_income = dff[COL_INCOME].std()
    mean_expense = dff[COL_TOTAL].mean()
    std_expense = dff[COL_TOTAL].std()
    selisih = mean_income - mean_expense
    deficit_real = (dff[COL_TOTAL] > dff[COL_INCOME]).sum()
    deficit_pct_real = deficit_real / len(dff) * 100
    
    # Monte Carlo
    np.random.seed(seed_val)
    sim_expense = np.random.normal(loc=mean_expense, scale=std_expense, size=n_sim)
    sim_deficit = (sim_expense > mean_income)
    prob_deficit = sim_deficit.mean() * 100
    surplus_cnt = (~sim_deficit).sum()
    deficit_cnt = sim_deficit.sum()
    
    # Paired T-Test manual
    diff = dff[COL_INCOME].values - dff[COL_TOTAL].values
    n_t = len(diff)
    mean_diff = diff.mean()
    std_diff = diff.std(ddof=1) if n_t > 1 else 0
    se_diff = std_diff / math.sqrt(n_t) if n_t > 0 else 0
    t_stat = mean_diff / se_diff if se_diff > 0 else 0
    
    def _betacf(a, b, x, max_iter=300, eps=3e-12):
        qab, qap, qam = a + b, a + 1.0, a - 1.0
        c, d = 1.0, 1.0 - qab * x / qap
        if abs(d) < 1e-30: d = 1e-30
        d = 1.0 / d; h = d
        for m in range(1, max_iter + 1):
            m2 = 2 * m
            aa = m * (b - m) * x / ((qam + m2) * (a + m2))
            d = 1.0 + aa * d
            d = (1e-30 if abs(d) < 1e-30 else d); d = 1.0 / d
            c = 1.0 + aa / c
            c = (1e-30 if abs(c) < 1e-30 else c)
            h *= d * c
            aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
            d = 1.0 + aa * d
            d = (1e-30 if abs(d) < 1e-30 else d); d = 1.0 / d
            c = 1.0 + aa / c
            c = (1e-30 if abs(c) < 1e-30 else c)
            delta = d * c; h *= delta
            if abs(delta - 1.0) < eps: break
        return h
    
    def _betai(a, b, x):
        if x <= 0: return 0.0
        if x >= 1: return 1.0
        lb = math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)
        if x < (a + 1.0) / (a + b + 2.0):
            return math.exp(a * math.log(x) + b * math.log(1.0 - x) - lb) * _betacf(a, b, x) / a
        return 1.0 - math.exp(b * math.log(1.0 - x) + a * math.log(x) - lb) * _betacf(b, a, 1.0 - x) / b
    
    def t_pvalue(t, df_):
        if df_ <= 0: return 1.0
        x = df_ / (df_ + t * t)
        return min(max(_betai(df_ / 2.0, 0.5, x), 0.0), 1.0)
    
    p_val = t_pvalue(abs(t_stat), n_t - 1) if n_t > 1 else 1.0
    
    # Expense breakdown (jika kolom ada)
    exp_cats = {}
    if COL_MAKAN and COL_MAKAN in dff.columns: exp_cats["Makan & Minum"] = pd.to_numeric(dff[COL_MAKAN], errors='coerce').mean()
    if COL_HIBUR and COL_HIBUR in dff.columns: exp_cats["Hiburan"] = pd.to_numeric(dff[COL_HIBUR], errors='coerce').mean()
    if COL_TRANS and COL_TRANS in dff.columns: exp_cats["Transportasi"] = pd.to_numeric(dff[COL_TRANS], errors='coerce').mean()
    if COL_ONLINE and COL_ONLINE in dff.columns: exp_cats["Belanja Online"] = pd.to_numeric(dff[COL_ONLINE], errors='coerce').mean()
    if COL_PULSA and COL_PULSA in dff.columns: exp_cats["Pulsa & Kuota"] = pd.to_numeric(dff[COL_PULSA], errors='coerce').mean()
    if COL_AKAD and COL_AKAD in dff.columns: exp_cats["Akademik & Kas"] = pd.to_numeric(dff[COL_AKAD], errors='coerce').mean()
    
    exp_total_cat = sum(v for v in exp_cats.values() if not pd.isna(v))
    exp_colors = [ACCENT_BLUE, ACCENT_AMBER, ACCENT_GREEN, ACCENT_PURPLE, "#22D3EE", "#FB923C"]
    
    # Risk level
    if prob_deficit > 60:
        risk_class = "risk-high"
        risk_label = "Tinggi 🔴"
        risk_color = ACCENT_RED
    elif prob_deficit > 30:
        risk_class = "risk-med"
        risk_label = "Sedang 🟡"
        risk_color = ACCENT_AMBER
    else:
        risk_class = "risk-low"
        risk_label = "Rendah 🟢"
        risk_color = ACCENT_GREEN
    
    # ==================================================
    # PAGE BANNER
    # ==================================================
    st.markdown(f"""
    <div class="page-banner">
        <h1>📊 Analisis Probabilitas Defisit Finansial Mahasiswa</h1>
        <div class="subtitle">
            Studi Kasus: <span>UIN K.H. Abdurrahman Wahid Pekalongan</span> &nbsp;|&nbsp;
            Pendekatan: <span>Simulasi Monte Carlo</span> &nbsp;|&nbsp;
            Program Studi: <span>Sains Data</span> &nbsp;|&nbsp;
            Tahun: <span>2026</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ==================================================
    # KPI ROW
    # ==================================================
    st.markdown("""
    <div class="section-heading">
        <div class="icon">📌</div>
        <h2>Executive Summary</h2>
        <span class="badge">OVERVIEW</span>
    </div>
    """, unsafe_allow_html=True)
    
    kc1, kc2, kc3, kc4 = st.columns(4)
    with kc1:
        st.markdown(f"""
        <div class="kpi-card" style="--accent:#3B82F6">
            <div class="kpi-label">👥 Total Responden</div>
            <div class="kpi-value">{len(dff)}</div>
            <div class="kpi-sub">Mahasiswa Aktif</div>
            <div class="kpi-trend neutral">n ≥ 30 → CLT Valid</div>
        </div>
        """, unsafe_allow_html=True)
    with kc2:
        st.markdown(f"""
        <div class="kpi-card" style="--accent:#22C55E">
            <div class="kpi-label">💰 Rata-rata Pemasukan</div>
            <div class="kpi-value" style="font-size:20px">Rp {mean_income:,.0f}</div>
            <div class="kpi-sub">Uang Saku Bulanan</div>
            <div class="kpi-trend up">σ = Rp {std_income:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    with kc3:
        st.markdown(f"""
        <div class="kpi-card" style="--accent:#EF4444">
            <div class="kpi-label">💸 Rata-rata Pengeluaran</div>
            <div class="kpi-value" style="font-size:20px">Rp {mean_expense:,.0f}</div>
            <div class="kpi-sub">Total Bulanan</div>
            <div class="kpi-trend down">σ = Rp {std_expense:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)
    with kc4:
        st.markdown(f"""
        <div class="kpi-card" style="--accent:{risk_color}">
            <div class="kpi-label">⚠️ Probabilitas Defisit</div>
            <div class="kpi-value">{prob_deficit:.2f}%</div>
            <div class="kpi-sub">{n_sim:,} Iterasi Monte Carlo</div>
            <div class="kpi-trend down"><span class="risk-badge {risk_class}">Risiko {risk_label}</span></div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    
    kd1, kd2, kd3 = st.columns(3)
    with kd1:
        trend_cls = "down" if selisih < 0 else "up"
        trend_icon = "📉" if selisih < 0 else "📈"
        selisih_color = '#EF4444' if selisih < 0 else '#22C55E'
        selisih_label = 'Defisit' if selisih < 0 else 'Surplus'
        trend_text = '⬇ Pengeluaran > Pemasukan' if selisih < 0 else '⬆ Pemasukan > Pengeluaran'
        st.markdown(f"""
        <div class="kpi-card" style="--accent:#A78BFA">
            <div class="kpi-label">{trend_icon} Selisih (Gap)</div>
            <div class="kpi-value" style="font-size:22px;color:{selisih_color}">
                Rp {abs(selisih):,.0f}
            </div>
            <div class="kpi-sub">{selisih_label} per bulan</div>
            <div class="kpi-trend {trend_cls}">{trend_text}</div>
        </div>
        """, unsafe_allow_html=True)
    with kd2:
        st.markdown(f"""
        <div class="kpi-card" style="--accent:#F59E0B">
            <div class="kpi-label">👤 Defisit Riil (Data Aktual)</div>
            <div class="kpi-value">{deficit_pct_real:.1f}%</div>
            <div class="kpi-sub">{deficit_real} dari {len(dff)} responden</div>
            <div class="kpi-trend down">Pengeluaran > Uang Saku</div>
        </div>
        """, unsafe_allow_html=True)
    with kd3:
        h0_decision = "H₀ Diterima" if p_val > 0.05 else "H₀ Ditolak"
        sig_color = "#22C55E" if p_val > 0.05 else "#EF4444"
        st.markdown(f"""
        <div class="kpi-card" style="--accent:#22D3EE">
            <div class="kpi-label">🔬 Uji-T Berpasangan</div>
            <div class="kpi-value" style="font-size:22px;color:{sig_color}">{h0_decision}</div>
            <div class="kpi-sub">p-value = {p_val:.4f} | α = 0.05</div>
            <div class="kpi-trend neutral">t-statistic = {t_stat:.4f}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # ==================================================
    # TABS
    # ==================================================
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Statistika Deskriptif",
        "📈 Visualisasi Data",
        "🎲 Simulasi Monte Carlo",
        "🔬 Analisis Probabilitas",
        "📝 Insight & Penutup"
    ])
    
    # ============================
    # TAB 1: STATISTIKA DESKRIPTIF
    # ============================
    with tab1:
        st.markdown("""
        <div class="section-heading">
            <div class="icon">📊</div>
            <h2>Tabel — Statistika Deskriptif</h2>
            <span class="badge">DESKRIPTIF</span>
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns([1, 1])
        with c1:
            st.markdown("""
            <table class="stat-table">
            <tr><th>Statistik</th><th>Pemasukan (Rp)</th><th>Pengeluaran (Rp)</th></tr>
            """, unsafe_allow_html=True)
            stats_data = {
                "Rata-rata (Mean)": (dff[COL_INCOME].mean(), dff[COL_TOTAL].mean()),
                "Median": (dff[COL_INCOME].median(), dff[COL_TOTAL].median()),
                "Standar Deviasi": (dff[COL_INCOME].std(), dff[COL_TOTAL].std()),
                "Nilai Minimum": (dff[COL_INCOME].min(), dff[COL_TOTAL].min()),
                "Nilai Maksimum": (dff[COL_INCOME].max(), dff[COL_TOTAL].max()),
                "Skewness": (dff[COL_INCOME].skew(), dff[COL_TOTAL].skew()),
                "Kurtosis": (dff[COL_INCOME].kurtosis(), dff[COL_TOTAL].kurtosis()),
            }
            rows = ""
            for label, (vi, ve) in stats_data.items():
                if label in ("Skewness", "Kurtosis"):
                    rows += f"<tr><td>{label}</td><td class='val'>{vi:.3f}</td><td class='val'>{ve:.3f}</td></tr>"
                else:
                    rows += f"<tr><td>{label}</td><td class='val'>Rp {vi:,.0f}</td><td class='val'>Rp {ve:,.0f}</td></tr>"
            st.markdown(rows + "</table>", unsafe_allow_html=True)
        
        with c2:
            st.markdown("""
            <div class="section-heading" style="margin-top:0">
                <div class="icon">📋</div>
                <h2>Profil Demografi Responden</h2>
            </div>
            """, unsafe_allow_html=True)
            
            if COL_SEMS:
                sem_data = dff[COL_SEMS].value_counts().reset_index()
                sem_data.columns = ["Semester", "Jumlah"]
                fig_sem = px.bar(sem_data, x="Semester", y="Jumlah",
                                color_discrete_sequence=[ACCENT_BLUE])
                fig_sem = apply_theme(fig_sem, "Distribusi Semester", 200)
                st.plotly_chart(fig_sem, use_container_width=True)
            
            if COL_TING:
                ting_data = dff[COL_TING].value_counts().reset_index()
                ting_data.columns = ["Status", "Jumlah"]
                fig_ting = px.bar(ting_data, x="Jumlah", y="Status", orientation="h",
                                 color_discrete_sequence=[ACCENT_PURPLE])
                fig_ting = apply_theme(fig_ting, "Status Tempat Tinggal", 210)
                st.plotly_chart(fig_ting, use_container_width=True)
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        c3, c4 = st.columns(2)
        with c3:
            if COL_PAY:
                pay_data = dff[COL_PAY].value_counts().reset_index()
                pay_data.columns = ["Metode", "Jumlah"]
                fig_pay = go.Figure(data=[go.Pie(
                    labels=pay_data["Metode"], values=pay_data["Jumlah"],
                    hole=0.5, marker=dict(colors=[ACCENT_BLUE, ACCENT_AMBER, ACCENT_GREEN]),
                    textinfo="label+percent", textposition="outside"
                )])
                apply_theme(fig_pay, "Metode Pembayaran Dominan", 300)
                st.plotly_chart(fig_pay, use_container_width=True)
        
        with c4:
            if COL_SRC:
                src_data = dff[COL_SRC].value_counts().reset_index()
                src_data.columns = ["Sumber", "Jumlah"]
                fig_src = px.bar(src_data, x="Jumlah", y="Sumber", orientation="h",
                                color_discrete_sequence=[ACCENT_GREEN, ACCENT_BLUE, ACCENT_AMBER, ACCENT_PURPLE])
                fig_src = apply_theme(fig_src, "Sumber Pendapatan Utama", 300)
                st.plotly_chart(fig_src, use_container_width=True)
    
    # ============================
    # TAB 2: VISUALISASI DATA
    # ============================
    with tab2:
        st.markdown("""
        <div class="section-heading">
            <div class="icon">📈</div>
            <h2>Bar Chart Perbandingan Pemasukan vs Pengeluaran</h2>
            <span class="badge">VISUALISASI</span>
        </div>
        """, unsafe_allow_html=True)
        
        df_sorted = dff[[COL_INCOME, COL_TOTAL]].copy()
        df_sorted = df_sorted.sort_values(COL_TOTAL)
        df_sorted["Responden"] = range(1, len(df_sorted) + 1)
        
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            name="Pemasukan", x=df_sorted["Responden"],
            y=df_sorted[COL_INCOME], marker_color=ACCENT_BLUE, opacity=0.85
        ))
        fig_bar.add_trace(go.Bar(
            name="Pengeluaran", x=df_sorted["Responden"],
            y=df_sorted[COL_TOTAL], marker_color=ACCENT_RED, opacity=0.85
        ))
        fig_bar.add_hline(y=mean_income, line_dash="dash", line_color=ACCENT_GREEN,
                         annotation_text=f"Rata-rata Pemasukan: Rp {mean_income:,.0f}",
                         annotation_font_color=ACCENT_GREEN)
        fig_bar.add_hline(y=mean_expense, line_dash="dot", line_color=ACCENT_RED,
                         annotation_text=f"Rata-rata Pengeluaran: Rp {mean_expense:,.0f}",
                         annotation_position="bottom right", annotation_font_color=ACCENT_RED)
        fig_bar.update_layout(barmode="group", xaxis_title="Responden (Diurutkan berdasar Pengeluaran)",
                              yaxis_title="Jumlah (Rp)")
        apply_theme(fig_bar, "", 420)
        st.plotly_chart(fig_bar, use_container_width=True)
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        if exp_cats:
            c5, c6 = st.columns(2)
            with c5:
                st.markdown("""
                <div class="section-heading" style="margin-top:0">
                    <div class="icon">🥧</div>
                    <h2>Proporsi Pengeluaran per Kategori</h2>
                </div>
                """, unsafe_allow_html=True)
                pie_labels = list(exp_cats.keys())
                pie_vals = [v for v in exp_cats.values() if not pd.isna(v)]
                fig_pie = go.Figure(data=[go.Pie(
                    labels=pie_labels, values=pie_vals, hole=0.42,
                    marker=dict(colors=exp_colors[:len(pie_labels)], line=dict(color=CHART_BG, width=2)),
                    textinfo="label+percent", textposition="outside",
                    textfont=dict(size=11)
                )])
                apply_theme(fig_pie, "", 380)
                fig_pie.add_annotation(
                    text=f"<b>Rp {exp_total_cat:,.0f}</b><br>Total/Bln",
                    x=0.5, y=0.5, showarrow=False,
                    font=dict(size=12, color="#CBD5E1"),
                    align="center"
                )
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with c6:
                st.markdown("""
                <div class="section-heading" style="margin-top:0">
                    <div class="icon">📊</div>
                    <h2>Rincian Nominal per Kategori</h2>
                </div>
                """, unsafe_allow_html=True)
                pie_pcts = [v / exp_total_cat * 100 if exp_total_cat > 0 else 0 for v in pie_vals]
                df_cat = pd.DataFrame({
                    "Kategori": pie_labels,
                    "Rata-rata (Rp)": pie_vals,
                    "Proporsi (%)": pie_pcts
                }).sort_values("Rata-rata (Rp)", ascending=True)
                fig_hbar = go.Figure()
                fig_hbar.add_trace(go.Bar(
                    x=df_cat["Rata-rata (Rp)"], y=df_cat["Kategori"],
                    orientation="h",
                    marker=dict(color=exp_colors[::-1][:len(pie_labels)], line=dict(color=CHART_BG, width=1)),
                    text=[f"Rp {v:,.0f} ({p:.1f}%)" for v, p in zip(df_cat["Rata-rata (Rp)"], df_cat["Proporsi (%)"])],
                    textposition="outside", textfont=dict(size=10, color="#CBD5E1")
                ))
                fig_hbar.update_layout(xaxis_title="Jumlah (Rp)", yaxis_title="")
                apply_theme(fig_hbar, "", 380)
                st.plotly_chart(fig_hbar, use_container_width=True)
            
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        c7, c8 = st.columns(2)
        with c7:
            st.markdown("**Distribusi Pemasukan Mahasiswa**")
            fig_h1 = go.Figure()
            fig_h1.add_trace(go.Histogram(x=dff[COL_INCOME], nbinsx=15, name="Pemasukan",
                                          marker_color=ACCENT_BLUE, opacity=0.75))
            fig_h1.add_vline(x=mean_income, line_dash="dash", line_color=ACCENT_GREEN,
                            annotation_text=f"Mean: Rp {mean_income:,.0f}", annotation_font_color=ACCENT_GREEN)
            apply_theme(fig_h1, "", 300)
            fig_h1.update_layout(xaxis_title="Pemasukan (Rp)", yaxis_title="Frekuensi", bargap=0.05)
            st.plotly_chart(fig_h1, use_container_width=True)
        with c8:
            st.markdown("**Distribusi Pengeluaran Mahasiswa**")
            fig_h2 = go.Figure()
            fig_h2.add_trace(go.Histogram(x=dff[COL_TOTAL], nbinsx=15, name="Pengeluaran",
                                          marker_color=ACCENT_RED, opacity=0.75))
            fig_h2.add_vline(x=mean_expense, line_dash="dash", line_color=ACCENT_AMBER,
                            annotation_text=f"Mean: Rp {mean_expense:,.0f}", annotation_font_color=ACCENT_AMBER)
            apply_theme(fig_h2, "", 300)
            fig_h2.update_layout(xaxis_title="Pengeluaran (Rp)", yaxis_title="Frekuensi", bargap=0.05)
            st.plotly_chart(fig_h2, use_container_width=True)
        
        # Boxplot
        fig_box = go.Figure()
        fig_box.add_trace(go.Box(y=dff[COL_INCOME], name="Pemasukan", marker_color=ACCENT_BLUE, boxmean="sd"))
        fig_box.add_trace(go.Box(y=dff[COL_TOTAL], name="Pengeluaran", marker_color=ACCENT_RED, boxmean="sd"))
        for cat, col in [("Makan", COL_MAKAN), ("Transportasi", COL_TRANS), ("Hiburan", COL_HIBUR)]:
            if col and col in dff.columns:
                fig_box.add_trace(go.Box(y=pd.to_numeric(dff[col], errors='coerce'), name=cat, boxmean="sd"))
        fig_box.update_layout(yaxis_title="Jumlah (Rp)")
        apply_theme(fig_box, "Boxplot Distribusi Semua Variabel Keuangan", 380)
        st.plotly_chart(fig_box, use_container_width=True)
    
    # ============================
    # TAB 3: MONTE CARLO
    # ============================
    with tab3:
        st.markdown("""
        <div class="section-heading">
            <div class="icon">🎲</div>
            <h2>Histogram Simulasi Monte Carlo</h2>
            <span class="badge">SIMULASI</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="research-box">
            <h4>⚙️ Parameter Simulasi</h4>
            <p>Simulasi Monte Carlo dijalankan dengan <strong style='color:#60A5FA'>{n_sim:,} iterasi</strong>
            menggunakan distribusi normal <strong style='color:#60A5FA'>N(μ = Rp {mean_expense:,.0f},
            σ = Rp {std_expense:,.0f})</strong> dengan random seed = {seed_val} untuk menjamin
            reprodusibilitas hasil. Setiap skenario dibandingkan terhadap ambang batas rata-rata
            uang saku <strong style='color:#22C55E'>Rp {mean_income:,.0f}</strong>.
            Pengeluaran yang melebihi batas ini dikategorikan sebagai <strong style='color:#EF4444'>defisit</strong>.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        fig_mc = go.Figure()
        fig_mc.add_trace(go.Histogram(
            x=sim_expense[sim_expense <= mean_income],
            nbinsx=60, name="✅ Surplus",
            marker_color=ACCENT_GREEN, opacity=0.7
        ))
        fig_mc.add_trace(go.Histogram(
            x=sim_expense[sim_expense > mean_income],
            nbinsx=60, name="❌ Defisit",
            marker_color=ACCENT_RED, opacity=0.7
        ))
        fig_mc.add_vline(x=mean_income, line_dash="dash", line_color="#FBBF24", line_width=3,
                        annotation_text=f"Ambang Batas Pemasukan: Rp {mean_income:,.0f}",
                        annotation_font_color="#FBBF24", annotation_font_size=12)
        fig_mc.add_vline(x=mean_expense, line_dash="dot", line_color=ACCENT_RED, line_width=2,
                        annotation_text=f"Mean Pengeluaran: Rp {mean_expense:,.0f}",
                        annotation_position="bottom right", annotation_font_color=ACCENT_RED)
        fig_mc.update_layout(barmode="overlay", xaxis_title="Pengeluaran Simulasi (Rp)", yaxis_title="Frekuensi")
        apply_theme(fig_mc, f"Distribusi {n_sim:,} Skenario Pengeluaran — Monte Carlo N(μ, σ)", 440)
        st.plotly_chart(fig_mc, use_container_width=True)
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        c9, c10, c11 = st.columns(3)
        with c9:
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number+delta",
                value=prob_deficit,
                number={"suffix": "%", "font": {"size": 48, "color": risk_color}},
                delta={"reference": 50, "relative": False,
                       "decreasing": {"color": ACCENT_GREEN},
                       "increasing": {"color": ACCENT_RED}},
                title={"text": "Probabilitas Defisit", "font": {"size": 14, "color": "#93C5FD"}},
                gauge={
                    "axis": {"range": [0, 100], "tickcolor": FONT_COLOR},
                    "bar": {"color": risk_color, "thickness": 0.28},
                    "steps": [
                        {"range": [0, 30], "color": "#064E3B"},
                        {"range": [30, 60], "color": "#78350F"},
                        {"range": [60, 100], "color": "#7F1D1D"}
                    ],
                    "threshold": {"line": {"color": "white", "width": 3}, "thickness": 0.75, "value": prob_deficit}
                }
            ))
            fig_gauge.update_layout(paper_bgcolor=CHART_BG, font_color=FONT_COLOR, height=320,
                                    margin=dict(l=16, r=16, t=48, b=16))
            st.plotly_chart(fig_gauge, use_container_width=True)
        
        with c10:
            fig_donut = go.Figure(data=[go.Pie(
                labels=["✅ Surplus", "❌ Defisit"],
                values=[surplus_cnt, deficit_cnt],
                hole=0.55,
                marker=dict(colors=[ACCENT_GREEN, ACCENT_RED], line=dict(color=CHART_BG, width=2)),
                textinfo="label+percent", textposition="outside"
            )])
            fig_donut.add_annotation(
                text=f"<b>{prob_deficit:.1f}%</b><br>Defisit",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=16, color=ACCENT_RED), align="center"
            )
            apply_theme(fig_donut, f"Distribusi Hasil {n_sim:,} Simulasi", 320)
            st.plotly_chart(fig_donut, use_container_width=True)
        
        with c11:
            sim_sorted = np.sort(sim_expense)
            cdf = np.arange(1, n_sim + 1) / n_sim
            fig_cdf = go.Figure()
            fig_cdf.add_trace(go.Scatter(x=sim_sorted, y=cdf * 100, mode="lines",
                                        line=dict(color=ACCENT_BLUE, width=2), name="CDF"))
            fig_cdf.add_vline(x=mean_income, line_dash="dash", line_color=ACCENT_AMBER,
                            annotation_text="Threshold", annotation_font_color=ACCENT_AMBER)
            threshold_cdf = np.interp(mean_income, sim_sorted, cdf) * 100
            fig_cdf.add_hline(y=threshold_cdf, line_dash="dot", line_color=ACCENT_RED,
                            annotation_text=f"{threshold_cdf:.1f}%", annotation_font_color=ACCENT_RED)
            fig_cdf.update_layout(xaxis_title="Pengeluaran (Rp)", yaxis_title="CDF (%)")
            apply_theme(fig_cdf, "Cumulative Distribution Function", 320)
            st.plotly_chart(fig_cdf, use_container_width=True)
        
        # Tabel hasil simulasi
        st.markdown("""
        <div class="section-heading">
            <div class="icon">📋</div>
            <h2>Tabel — Hasil Simulasi Monte Carlo</h2>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <table class="stat-table" style="max-width:600px">
        <tr><th>Parameter Simulasi</th><th>Nilai</th></tr>
        <tr><td>Jumlah Iterasi</td><td class="val">{n_sim:,}</td></tr>
        <tr><td>Mean Pengeluaran (μ)</td><td class="val">Rp {mean_expense:,.0f}</td></tr>
        <tr><td>Standar Deviasi (σ)</td><td class="val">Rp {std_expense:,.0f}</td></tr>
        <tr><td>Ambang Batas (Rata-rata Uang Saku)</td><td class="val">Rp {mean_income:,.0f}</td></tr>
        <tr><td>Jumlah Skenario Defisit</td><td class="val">{deficit_cnt:,}</td></tr>
        <tr><td>Probabilitas Defisit</td><td class="val" style="color:{risk_color}">{prob_deficit:.2f}%</td></tr>
        <tr><td>Random Seed</td><td class="val">{seed_val} (reproducible)</td></tr>
        </table>
        """, unsafe_allow_html=True)
    
    # ============================
    # TAB 4: ANALISIS PROBABILITAS
    # ============================
    with tab4:
        st.markdown("""
        <div class="section-heading">
            <div class="icon">🔬</div>
            <h2>Uji-T Berpasangan (Paired Sample T-Test)</h2>
            <span class="badge">INFERENSI STATISTIK</span>
        </div>
        """, unsafe_allow_html=True)
        
        c12, c13 = st.columns([1, 1])
        with c12:
            h0_color = "#22C55E" if p_val > 0.05 else "#EF4444"
            h0_text = "H₀ Diterima" if p_val > 0.05 else "H₀ Ditolak"
            st.markdown(f"""
            <table class="stat-table">
            <tr><th>Parameter</th><th>Nilai</th></tr>
            <tr><td>Rata-rata Pemasukan</td><td class="val">Rp {mean_income:,.0f}</td></tr>
            <tr><td>Rata-rata Pengeluaran</td><td class="val">Rp {mean_expense:,.0f}</td></tr>
            <tr><td>T-Statistic</td><td class="val">{t_stat:.4f}</td></tr>
            <tr><td>P-Value</td><td class="val">{p_val:.4f}</td></tr>
            <tr><td>Taraf Signifikansi (α)</td><td class="val">0.05</td></tr>
            <tr><td>Keputusan</td><td class="val" style="color:{h0_color}">{h0_text}</td></tr>
            </table>
            """, unsafe_allow_html=True)
            
            st.markdown(f"""
            <div class="research-box" style="margin-top:16px">
                <h4>📐 Interpretasi Uji-T</h4>
                <p>Nilai p-value <strong style='color:#60A5FA'>{p_val:.4f}</strong> {"> 0.05" if p_val > 0.05 else "≤ 0.05"} sehingga H₀ {"diterima" if p_val > 0.05 else "ditolak"}.
                Perbedaan rata-rata pemasukan dan pengeluaran <strong>{"tidak signifikan secara statistik" if p_val > 0.05 else "signifikan secara statistik"}</strong>.
                Meski demikian, secara deskriptif defisit tetap terjadi pada <strong style='color:#EF4444'>{deficit_pct_real:.1f}%</strong> responden.</p>
            </div>
            """, unsafe_allow_html=True)
        
        with c13:
            dff_plot = dff.copy()
            dff_plot["Status"] = np.where(dff_plot[COL_TOTAL] > dff_plot[COL_INCOME], "❌ Defisit", "✅ Surplus")
            hover_cols = [c for c in [COL_SEMS, COL_TING] if c]
            fig_sc = px.scatter(dff_plot, x=COL_INCOME, y=COL_TOTAL,
                               color="Status", color_discrete_map={"❌ Defisit": ACCENT_RED, "✅ Surplus": ACCENT_GREEN},
                               hover_data=hover_cols)
            max_val = max(dff[COL_INCOME].max(), dff[COL_TOTAL].max()) * 1.05
            fig_sc.add_shape(type="line", x0=0, y0=0, x1=max_val, y1=max_val,
                            line=dict(color=ACCENT_AMBER, width=2, dash="dash"))
            fig_sc.add_annotation(text="Garis Keseimbangan (Pemasukan = Pengeluaran)",
                                 x=max_val * 0.6, y=max_val * 0.65,
                                 showarrow=False, font=dict(color=ACCENT_AMBER, size=10))
            fig_sc.update_layout(xaxis_title="Pemasukan (Rp)", yaxis_title="Pengeluaran (Rp)")
            apply_theme(fig_sc, "Scatter Plot: Pemasukan vs Pengeluaran per Responden", 420)
            st.plotly_chart(fig_sc, use_container_width=True)
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        # Heatmap korelasi
        st.markdown("""
        <div class="section-heading">
            <div class="icon">🔥</div>
            <h2>Heatmap Korelasi Variabel Keuangan</h2>
        </div>
        """, unsafe_allow_html=True)
        
        num_cols = [c for c in [COL_INCOME, COL_TOTAL, COL_MAKAN, COL_TRANS, COL_HIBUR, COL_AKAD, COL_PULSA, COL_ONLINE] if c in dff.columns]
        if len(num_cols) >= 2:
            dff_num = dff[num_cols].apply(pd.to_numeric, errors='coerce')
            col_labels = [c.replace("_", " ").replace(" Bulanan", "") for c in num_cols]
            corr_df = dff_num.corr()
            corr_df.columns = col_labels
            corr_df.index = col_labels
            fig_heat = px.imshow(corr_df, text_auto=".2f", color_continuous_scale="Blues",
                                aspect="auto", zmin=-1, zmax=1)
            fig_heat.update_traces(textfont=dict(size=11))
            apply_theme(fig_heat, "", 400)
            st.plotly_chart(fig_heat, use_container_width=True)
        else:
            st.info("ℹ️ Tidak cukup kolom numerik untuk membuat heatmap korelasi.")
    
    # ============================
    # TAB 5: PENUTUP & INSIGHT
    # ============================
    with tab5:
        st.markdown("""
        <div class="section-heading">
            <div class="icon">💡</div>
            <h2>Kesimpulan, Insight, dan Rekomendasi</h2>
            <span class="badge">PENUTUP</span>
        </div>
        """, unsafe_allow_html=True)
        
        # 3 Key Findings
        food_pct = (exp_cats.get("Makan & Minum", 0) / exp_total_cat * 100) if exp_total_cat > 0 else 0
        enter_pct = (exp_cats.get("Hiburan", 0) / exp_total_cat * 100) if exp_total_cat > 0 else 0
        
        st.markdown(f"""
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:12px 0">
            <div class="insight-card" style="--accent:#EF4444">
                <div class="ic-label">🔴 Temuan 1 — Defisit Sistemik</div>
                <div class="ic-val">{deficit_pct_real:.1f}%</div>
                <div class="ic-desc">responden mencatat pengeluaran melebihi pemasukan, defisit rata-rata Rp {abs(selisih):,.0f}/bulan</div>
            </div>
            <div class="insight-card" style="--accent:#F59E0B">
                <div class="ic-label">🟡 Temuan 2 — Dominasi Pos Makan</div>
                <div class="ic-val">{food_pct:.1f}%</div>
                <div class="ic-desc">porsi makan & minum mendominasi pengeluaran, diikuti hiburan {enter_pct:.1f}%</div>
            </div>
            <div class="insight-card" style="--accent:{risk_color}">
                <div class="ic-label">{'🔴' if prob_deficit > 60 else '🟡'} Temuan 3 — Risiko Monte Carlo</div>
                <div class="ic-val">{prob_deficit:.2f}%</div>
                <div class="ic-desc">probabilitas defisit dari {n_sim:,} iterasi simulasi</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        c14, c15 = st.columns(2)
        with c14:
            st.markdown("""
            <div class="research-box">
                <h4>📌 Kesimpulan Penelitian</h4>
                <p>Mayoritas mahasiswa UIN K.H. Abdurrahman Wahid Pekalongan rentan mengalami
                ketidakseimbangan finansial. Terdapat kesenjangan antara rata-rata uang saku bulanan
                dengan rata-rata total pengeluaran, yang menghasilkan defisit sistemik.</p>
                <ul>
                    <li>Kesenjangan pemasukan-pengeluaran sebesar <strong>Rp {:,.0f}/bulan</strong></li>
                    <li>Uji-T menunjukkan <strong>{}</strong> (p={:.4f} {} 0.05)</li>
                    <li>Monte Carlo mengkonfirmasi probabilitas defisit <strong>{:.2f}%</strong></li>
                </ul>
            </div>
            """.format(abs(selisih), "perbedaan tidak signifikan" if p_val > 0.05 else "perbedaan signifikan", p_val, ">" if p_val > 0.05 else "≤", prob_deficit), unsafe_allow_html=True)
            
            st.markdown("""
            <div class="research-box">
                <h4>💡 Insight Utama</h4>
                <ul>
                    <li>Proporsi pengeluaran tertinggi untuk makan & minum dan hiburan</li>
                    <li>Alokasi hiburan cenderung melampaui biaya esensial</li>
                    <li>Fenomena ini mencerminkan pola konsumtif Gen Z akibat kemudahan transaksi digital</li>
                    <li>Defisit mencerminkan rendahnya literasi keuangan mahasiswa</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with c15:
            st.markdown("""
            <div class="research-box">
                <h4>🎯 Rekomendasi Tindak Lanjut</h4>
                <ul>
                    <li><strong style="color:#60A5FA">Mahasiswa:</strong> Terapkan metode budgeting
                    50/30/20, catat pengeluaran harian, bedakan kebutuhan vs keinginan</li>
                    <li><strong style="color:#60A5FA">Institusi Kampus:</strong> Rancang program edukasi
                    literasi keuangan berbasis data riil mahasiswa</li>
                    <li><strong style="color:#60A5FA">Penelitian Lanjutan:</strong> Perbesar sampel
                    (n ≥ 100) untuk meminimalkan dampak outlier</li>
                    <li><strong style="color:#60A5FA">Intervensi Digital:</strong> Kembangkan aplikasi
                    tracking pengeluaran yang terintegrasi dengan sistem kampus</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            if prob_deficit >= 60:
                conclusion_type = "error"
                conclusion_text = f"🔴 Probabilitas defisit {prob_deficit:.2f}% — RISIKO TINGGI. Audit pengeluaran non-prioritas dan cari alternatif pendapatan tambahan."
            elif prob_deficit >= 30:
                conclusion_type = "warning"
                conclusion_text = f"🟡 Probabilitas defisit {prob_deficit:.2f}% — RISIKO SEDANG. Terapkan metode budgeting 50/30/20 dan catat pengeluaran harian."
            else:
                conclusion_type = "success"
                conclusion_text = f"🟢 Probabilitas defisit {prob_deficit:.2f}% — RISIKO RENDAH. Pertahankan pola budgeting yang baik dan tingkatkan literasi finansial."
            
            if conclusion_type == "error":
                st.error(conclusion_text)
            elif conclusion_type == "warning":
                st.warning(conclusion_text)
            else:
                st.success(conclusion_text)
        
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown("### 📋 Dataset Mentah")
        st.dataframe(dff, use_container_width=True, height=300)
    
    # ==================================================
    # FOOTER
    # ==================================================
    st.markdown("""
    <div class="footer">
        <strong>📊 Analisis Probabilitas Defisit Finansial Mahasiswa</strong><br>
        Simulasi Monte Carlo | UIN K.H. Abdurrahman Wahid Pekalongan | Program Studi Sains Data 2026<br>
        Penulis: Achmad Ridwan (60125008) | Dosen Pengampu: Umi Mahmudah, M.Sc., Ph.D.
    </div>
    """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"❌ Terjadi kesalahan sistem: {e}")
    import traceback
    st.code(traceback.format_exc())
    st.info("Pastikan file `Data_Pengeluaran_Mahasiswa.csv` berada di folder yang sama dengan script ini.")
