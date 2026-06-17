import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats

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
# CUSTOM CSS — TEMA AKADEMIK PREMIUM
# ==================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    * { font-family: 'Inter', sans-serif; }

    .stApp { background-color: #0B1120; color: #CBD5E1; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0F1C36 0%, #0B1120 100%);
        border-right: 1px solid #1E3A5F;
    }
    [data-testid="stSidebar"] * { color: #CBD5E1 !important; }

    /* Page header banner */
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
    .page-banner .subtitle span { color: #3B82F6; font-weight: 600; }

    /* Section heading */
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

    /* KPI Cards */
    .kpi-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 8px; }
    .kpi-card {
        background: linear-gradient(145deg, #0F1C36 0%, #162040 100%);
        border: 1px solid #1E3A5F;
        border-radius: 14px;
        padding: 22px 20px;
        transition: all 0.25s ease;
        position: relative;
        overflow: hidden;
    }
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: var(--accent);
        border-radius: 14px 14px 0 0;
    }
    .kpi-card:hover { transform: translateY(-4px); border-color: #2563EB; box-shadow: 0 12px 32px rgba(37,99,235,0.2); }
    .kpi-label { font-size: 11px; font-weight: 600; color: #475569; text-transform: uppercase; letter-spacing: 1.2px; margin-bottom: 10px; }
    .kpi-value { font-size: 28px; font-weight: 700; color: var(--accent); line-height: 1.1; }
    .kpi-sub { font-size: 11px; color: #475569; margin-top: 8px; }
    .kpi-trend { font-size: 11px; margin-top: 6px; }
    .kpi-trend.up { color: #22C55E; } .kpi-trend.down { color: #EF4444; } .kpi-trend.neutral { color: #F59E0B; }

    /* Insight Cards */
    .insight-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin: 12px 0; }
    .insight-card {
        background: #0F1C36;
        border: 1px solid #1E3A5F;
        border-left: 4px solid var(--accent);
        border-radius: 10px;
        padding: 16px 18px;
    }
    .insight-card .ic-label { font-size: 10px; font-weight: 700; color: var(--accent); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 6px; }
    .insight-card .ic-val { font-size: 20px; font-weight: 700; color: #E2E8F0; }
    .insight-card .ic-desc { font-size: 11px; color: #64748B; margin-top: 4px; }

    /* Stat table */
    .stat-table { width: 100%; border-collapse: collapse; font-size: 13px; }
    .stat-table th { background: #0F1C36; color: #3B82F6; font-weight: 600; padding: 10px 14px; text-align: left; border-bottom: 2px solid #1E3A5F; font-size: 11px; text-transform: uppercase; letter-spacing: 0.8px; }
    .stat-table td { padding: 10px 14px; color: #CBD5E1; border-bottom: 1px solid #1E3A5F; }
    .stat-table tr:last-child td { border-bottom: none; }
    .stat-table tr:hover td { background: #0F1C36; }
    .stat-table .val { font-weight: 600; color: #93C5FD; text-align: right; }

    /* Risk badge */
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

    /* Research box */
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

    /* Divider */
    .divider { height: 1px; background: linear-gradient(90deg, transparent, #1E3A5F, transparent); margin: 28px 0; }

    /* Tab override */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; background: transparent; border-bottom: 2px solid #1E3A5F; padding-bottom: 0; }
    .stTabs [data-baseweb="tab"] {
        background: #0B1120;
        border-radius: 8px 8px 0 0;
        color: #64748B;
        padding: 10px 22px;
        font-size: 13px;
        font-weight: 500;
        border: 1px solid #1E3A5F;
        border-bottom: none;
        margin-bottom: -2px;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(180deg, #1D4ED8 0%, #1E3A8A 100%);
        color: #FFFFFF;
        font-weight: 700;
        border-color: #2563EB;
    }

    /* Slider */
    .stSlider > div > div > div { background: #1D4ED8 !important; }

    /* Selectbox */
    .stSelectbox > div > div { background: #0F1C36; border: 1px solid #1E3A5F; color: #CBD5E1; }

    /* Dataframe */
    .stDataFrame { border: 1px solid #1E3A5F; border-radius: 10px; overflow: hidden; }

    /* Info/warning/error banners */
    .stAlert { border-radius: 10px; }

    h1, h2, h3 { color: #E2E8F0 !important; }
    hr { border: none; height: 1px; background: #1E3A5F; margin: 24px 0; }

    /* Sidebar radio buttons */
    .stRadio label { color: #94A3B8 !important; font-size: 13px; }

    /* Footer */
    .footer { text-align: center; padding: 32px; color: #334155; border-top: 1px solid #1E3A5F; margin-top: 48px; font-size: 12px; }
    .footer strong { color: #475569; }
</style>
""", unsafe_allow_html=True)

# ==================================================
# PLOTLY TEMPLATE
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
        xaxis=dict(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR),
        yaxis=dict(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR),
    )
    return fig

# ==================================================
# LOAD DATA
# ==================================================
@st.cache_data
def load_data():
    df = pd.read_csv("Data_Pengeluaran_Mahasiswa.csv", sep=";")
    df.columns = df.columns.str.strip()
    return df

try:
    df = load_data()

    COL_INCOME = "Pemasukan / Uang Saku Bulanan"
    COL_TOTAL  = "Total_Pengeluaran_Bulanan"
    COL_MAKAN  = "Makan_Bulanan"
    COL_TRANS  = "Transport_Bulanan"
    COL_HIBUR  = "Hiburan_Bulanan"
    COL_AKAD   = "Pengeluaran Akademik dan Kas Bulanan"
    COL_PULSA  = "Pengeluaran Pulsa & Kuota Bulanan"
    COL_ONLINE = "Pengeluaran Belanja Online Bulanan"
    COL_SEMS   = "Semester Saat Ini"
    COL_TING   = "Status Tempat Tinggal"
    COL_SRC    = "Sumber Pendapatan Utama"
    COL_PAY    = "Apa metode pembayaran yang paling sering Anda gunakan?"

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
        sems_opt = ["Semua"] + sorted(df[COL_SEMS].unique().tolist())
        sems_sel = st.selectbox("Semester", sems_opt)
        ting_opt = ["Semua"] + sorted(df[COL_TING].unique().tolist())
        ting_sel = st.selectbox("Tempat Tinggal", ting_opt)

        st.markdown("---")
        st.markdown(f"""
        <div style='background:#0F1C36;border:1px solid #1E3A5F;border-radius:10px;padding:14px;font-size:12px;color:#64748B;'>
        📁 <strong style='color:#3B82F6'>Dataset Info</strong><br><br>
        Responden: <strong style='color:#93C5FD'>{len(df)} mahasiswa</strong><br>
        Institusi: UIN K.H. Abdurrahman Wahid<br>
        Periode: 2026<br>
        Metode: Monte Carlo Simulation
        </div>
        """, unsafe_allow_html=True)

    # Apply filter
    dff = df.copy()
    if sems_sel != "Semua": dff = dff[dff[COL_SEMS] == sems_sel]
    if ting_sel != "Semua": dff = dff[dff[COL_TING] == ting_sel]

    # ==================================================
    # CALCULATIONS
    # ==================================================
    mean_income  = dff[COL_INCOME].mean()
    std_income   = dff[COL_INCOME].std()
    mean_expense = dff[COL_TOTAL].mean()
    std_expense  = dff[COL_TOTAL].std()
    selisih      = mean_income - mean_expense
    deficit_real = (dff[COL_TOTAL] > dff[COL_INCOME]).sum()
    deficit_pct_real = deficit_real / len(dff) * 100

    # Monte Carlo
    np.random.seed(seed_val)
    sim_expense = np.random.normal(loc=mean_expense, scale=std_expense, size=n_sim)
    sim_deficit = (sim_expense > mean_income)
    prob_deficit = sim_deficit.mean() * 100
    surplus_cnt  = (~sim_deficit).sum()
    deficit_cnt  = sim_deficit.sum()

    # Paired T-Test
    t_stat, p_val = stats.ttest_rel(dff[COL_INCOME], dff[COL_TOTAL])

    # Expense breakdown
    exp_cats = {
        "Makan & Minum": dff[COL_MAKAN].mean(),
        "Hiburan": dff[COL_HIBUR].mean(),
        "Transportasi": dff[COL_TRANS].mean(),
        "Belanja Online": dff[COL_ONLINE].mean(),
        "Pulsa & Kuota": dff[COL_PULSA].mean(),
        "Akademik & Kas": dff[COL_AKAD].mean(),
    }
    exp_total_cat = sum(exp_cats.values())
    exp_colors = [ACCENT_BLUE, ACCENT_AMBER, ACCENT_GREEN, ACCENT_PURPLE, "#22D3EE", "#FB923C"]

    # Risk level
    if prob_deficit > 60:
        risk_class = "risk-high"; risk_label = "Tinggi 🔴"; risk_color = ACCENT_RED
    elif prob_deficit > 30:
        risk_class = "risk-med"; risk_label = "Sedang 🟡"; risk_color = ACCENT_AMBER
    else:
        risk_class = "risk-low"; risk_label = "Rendah 🟢"; risk_color = ACCENT_GREEN

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
        </div>""", unsafe_allow_html=True)
    with kc2:
        st.markdown(f"""
        <div class="kpi-card" style="--accent:#22C55E">
            <div class="kpi-label">💰 Rata-rata Pemasukan</div>
            <div class="kpi-value" style="font-size:20px">Rp {mean_income:,.0f}</div>
            <div class="kpi-sub">Uang Saku Bulanan</div>
            <div class="kpi-trend up">σ = Rp {std_income:,.0f}</div>
        </div>""", unsafe_allow_html=True)
    with kc3:
        st.markdown(f"""
        <div class="kpi-card" style="--accent:#EF4444">
            <div class="kpi-label">💸 Rata-rata Pengeluaran</div>
            <div class="kpi-value" style="font-size:20px">Rp {mean_expense:,.0f}</div>
            <div class="kpi-sub">Total Bulanan</div>
            <div class="kpi-trend down">σ = Rp {std_expense:,.0f}</div>
        </div>""", unsafe_allow_html=True)
    with kc4:
        st.markdown(f"""
        <div class="kpi-card" style="--accent:{risk_color}">
            <div class="kpi-label">⚠️ Probabilitas Defisit</div>
            <div class="kpi-value">{prob_deficit:.2f}%</div>
            <div class="kpi-sub">{n_sim:,} Iterasi Monte Carlo</div>
            <div class="kpi-trend down"><span class="risk-badge {risk_class}">Risiko {risk_label}</span></div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    kd1, kd2, kd3 = st.columns(3)
    with kd1:
        trend_cls = "down" if selisih < 0 else "up"
        trend_icon = "📉" if selisih < 0 else "📈"
        st.markdown(f"""
        <div class="kpi-card" style="--accent:#A78BFA">
            <div class="kpi-label">{trend_icon} Selisih (Gap)</div>
            <div class="kpi-value" style="font-size:22px;color:{'#EF4444' if selisih < 0 else '#22C55E'}">
                Rp {abs(selisih):,.0f}
            </div>
            <div class="kpi-sub">{'Defisit' if selisih < 0 else 'Surplus'} per bulan</div>
            <div class="kpi-trend {trend_cls}">{'⬇ Pengeluaran > Pemasukan' if selisih < 0 else '⬆ Pemasukan > Pengeluaran'}</div>
        </div>""", unsafe_allow_html=True)
    with kd2:
        st.markdown(f"""
        <div class="kpi-card" style="--accent:#F59E0B">
            <div class="kpi-label">👤 Defisit Riil (Data Aktual)</div>
            <div class="kpi-value">{deficit_pct_real:.1f}%</div>
            <div class="kpi-sub">{deficit_real} dari {len(dff)} responden</div>
            <div class="kpi-trend down">Pengeluaran > Uang Saku</div>
        </div>""", unsafe_allow_html=True)
    with kd3:
        h0_decision = "H₀ Diterima" if p_val > 0.05 else "H₀ Ditolak"
        sig_color = "#22C55E" if p_val > 0.05 else "#EF4444"
        st.markdown(f"""
        <div class="kpi-card" style="--accent:#22D3EE">
            <div class="kpi-label">🔬 Uji-T Berpasangan</div>
            <div class="kpi-value" style="font-size:22px;color:{sig_color}">{h0_decision}</div>
            <div class="kpi-sub">p-value = {p_val:.4f} | α = 0.05</div>
            <div class="kpi-trend neutral">t-statistic = {t_stat:.4f}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ==================================================
    # TABS
    # ==================================================
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 BAB III — Statistika Deskriptif",
        "📈 Visualisasi Data",
        "🎲 Simulasi Monte Carlo",
        "🔬 Analisis Probabilitas",
        "📝 BAB IV — Penutup & Insight"
    ])

    # ============================
    # TAB 1: STATISTIKA DESKRIPTIF
    # ============================
    with tab1:
        st.markdown("""
        <div class="section-heading">
            <div class="icon">📊</div>
            <h2>Tabel 3.1 — Statistika Deskriptif</h2>
            <span class="badge">BAB III</span>
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

            # Semester
            sem_data = dff[COL_SEMS].value_counts().reset_index()
            sem_data.columns = ["Semester", "Jumlah"]
            fig_sem = px.bar(sem_data, x="Semester", y="Jumlah",
                             color_discrete_sequence=[ACCENT_BLUE])
            fig_sem = apply_theme(fig_sem, "Distribusi Semester", 200)
            fig_sem.update_traces(marker_line_color=GRID_COLOR, marker_line_width=0.5)
            st.plotly_chart(fig_sem, use_container_width=True)

            # Tempat tinggal
            ting_data = dff[COL_TING].value_counts().reset_index()
            ting_data.columns = ["Status", "Jumlah"]
            fig_ting = px.bar(ting_data, x="Jumlah", y="Status", orientation="h",
                              color_discrete_sequence=[ACCENT_PURPLE])
            fig_ting = apply_theme(fig_ting, "Status Tempat Tinggal", 210)
            st.plotly_chart(fig_ting, use_container_width=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        c3, c4 = st.columns(2)
        with c3:
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
            src_data = dff[COL_SRC].value_counts().reset_index()
            src_data.columns = ["Sumber", "Jumlah"]
            src_data["Sumber"] = src_data["Sumber"].replace({"kluarga jg tp opsional": "Keluarga (Opsional)"})
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
            <h2>Gambar 3.1 — Bar Chart Perbandingan Pemasukan vs Pengeluaran</h2>
            <span class="badge">VISUALISASI</span>
        </div>
        """, unsafe_allow_html=True)

        # Bar chart income vs expense per respondent (sorted)
        df_sorted = dff[[COL_INCOME, COL_TOTAL]].copy()
        df_sorted["Responden"] = range(1, len(df_sorted) + 1)
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

        c5, c6 = st.columns(2)
        with c5:
            st.markdown("""
            <div class="section-heading" style="margin-top:0">
                <div class="icon">🥧</div>
                <h2>Gambar 3.2 — Proporsi Pengeluaran per Kategori</h2>
            </div>
            """, unsafe_allow_html=True)
            pie_labels = list(exp_cats.keys())
            pie_vals   = list(exp_cats.values())
            pie_pcts   = [v / exp_total_cat * 100 for v in pie_vals]
            fig_pie = go.Figure(data=[go.Pie(
                labels=pie_labels, values=pie_vals, hole=0.42,
                marker=dict(colors=exp_colors, line=dict(color=CHART_BG, width=2)),
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
                <h2>Rincian Nominal Pengeluaran per Kategori</h2>
            </div>
            """, unsafe_allow_html=True)
            df_cat = pd.DataFrame({
                "Kategori": pie_labels,
                "Rata-rata (Rp)": pie_vals,
                "Proporsi (%)": pie_pcts
            }).sort_values("Rata-rata (Rp)", ascending=True)
            fig_hbar = go.Figure()
            fig_hbar.add_trace(go.Bar(
                x=df_cat["Rata-rata (Rp)"], y=df_cat["Kategori"],
                orientation="h",
                marker=dict(color=exp_colors[::-1], line=dict(color=CHART_BG, width=1)),
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
            fig_box.add_trace(go.Box(y=dff[col], name=cat, boxmean="sd"))
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
            <h2>Gambar 3.3 — Histogram Simulasi Monte Carlo</h2>
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

        # Histogram Monte Carlo
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
            # Gauge
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
            # Donut
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
            # CDF
            sim_sorted = np.sort(sim_expense)
            cdf = np.arange(1, n_sim + 1) / n_sim
            fig_cdf = go.Figure()
            fig_cdf.add_trace(go.Scatter(x=sim_sorted, y=cdf * 100, mode="lines",
                                          line=dict(color=ACCENT_BLUE, width=2), name="CDF"))
            fig_cdf.add_vline(x=mean_income, line_dash="dash", line_color=ACCENT_AMBER,
                              annotation_text=f"Threshold", annotation_font_color=ACCENT_AMBER)
            threshold_cdf = np.interp(mean_income, sim_sorted, cdf) * 100
            fig_cdf.add_hline(y=threshold_cdf, line_dash="dot", line_color=ACCENT_RED,
                              annotation_text=f"{threshold_cdf:.1f}%", annotation_font_color=ACCENT_RED)
            fig_cdf.update_layout(xaxis_title="Pengeluaran (Rp)", yaxis_title="CDF (%)")
            apply_theme(fig_cdf, "Cumulative Distribution Function", 320)
            st.plotly_chart(fig_cdf, use_container_width=True)

        # Tabel 3.3
        st.markdown("""
        <div class="section-heading">
            <div class="icon">📋</div>
            <h2>Tabel 3.3 — Hasil Simulasi Monte Carlo</h2>
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
        <tr><td>Probabilitas Kantong Kering</td><td class="val" style="color:{risk_color}">{prob_deficit:.2f}%</td></tr>
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
            <h2>Tabel 3.2 — Uji-T Berpasangan (Paired Sample T-Test)</h2>
            <span class="badge">INFERENSI STATISTIK</span>
        </div>
        """, unsafe_allow_html=True)

        c12, c13 = st.columns([1, 1])
        with c12:
            h0_color = "#22C55E" if p_val > 0.05 else "#EF4444"
            h0_text  = "H₀ Diterima" if p_val > 0.05 else "H₀ Ditolak"
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
                <p>Nilai p-value <strong style='color:#60A5FA'>{p_val:.4f} > 0.05</strong> sehingga H₀ diterima.
                Perbedaan rata-rata pemasukan dan pengeluaran <strong>tidak signifikan secara statistik</strong>,
                kemungkinan disebabkan adanya outlier pemasukan ekstrem (Rp 9.000.000) dan ukuran sampel
                yang relatif kecil (n={len(dff)}). Meski demikian, secara deskriptif defisit tetap terjadi
                pada <strong style='color:#EF4444'>{deficit_pct_real:.1f}%</strong> responden.</p>
            </div>
            """, unsafe_allow_html=True)

        with c13:
            # Scatter income vs expense
            dff_plot = dff.copy()
            dff_plot["Status"] = np.where(dff_plot[COL_TOTAL] > dff_plot[COL_INCOME], "❌ Defisit", "✅ Surplus")
            fig_sc = px.scatter(dff_plot, x=COL_INCOME, y=COL_TOTAL,
                                color="Status", color_discrete_map={"❌ Defisit": ACCENT_RED, "✅ Surplus": ACCENT_GREEN},
                                hover_data=[COL_SEMS, COL_TING])
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
        num_cols = [COL_INCOME, COL_TOTAL, COL_MAKAN, COL_TRANS, COL_HIBUR, COL_AKAD, COL_PULSA, COL_ONLINE]
        col_labels = ["Pemasukan", "Total Pnglrn", "Makan", "Transport", "Hiburan", "Akademik", "Pulsa", "Online"]
        corr_df = dff[num_cols].corr()
        corr_df.columns = col_labels
        corr_df.index = col_labels
        fig_heat = px.imshow(corr_df, text_auto=".2f", color_continuous_scale="Blues",
                             aspect="auto", zmin=-1, zmax=1)
        fig_heat.update_traces(textfont=dict(size=11))
        apply_theme(fig_heat, "", 400)
        st.plotly_chart(fig_heat, use_container_width=True)

    # ============================
    # TAB 5: PENUTUP & INSIGHT
    # ============================
    with tab5:
        st.markdown("""
        <div class="section-heading">
            <div class="icon">💡</div>
            <h2>BAB IV — Penutup: Kesimpulan, Insight, dan Rekomendasi</h2>
            <span class="badge">PENUTUP</span>
        </div>
        """, unsafe_allow_html=True)

        # 3 Key Findings
        st.markdown("""
        <div class="insight-row">
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:14px;margin:12px 0">
            <div class="insight-card" style="--accent:#EF4444">
                <div class="ic-label">🔴 Temuan 1 — Defisit Sistemik</div>
                <div class="ic-val">{deficit_pct_real:.1f}%</div>
                <div class="ic-desc">responden mencatat pengeluaran melebihi pemasukan, defisit rata-rata Rp {abs(selisih):,.0f}/bulan</div>
            </div>
            <div class="insight-card" style="--accent:#F59E0B">
                <div class="ic-label">🟡 Temuan 2 — Dominasi Pos Makan</div>
                <div class="ic-val">46.5%</div>
                <div class="ic-desc">porsi makan & minum mendominasi, diikuti hiburan 19.8% yang melebihi transportasi 17.5%</div>
            </div>
            <div class="insight-card" style="--accent:{risk_color}">
                <div class="ic-label">{'🔴' if prob_deficit>60 else '🟡'} Temuan 3 — Risiko Monte Carlo</div>
                <div class="ic-val">{prob_deficit:.2f}%</div>
                <div class="ic-desc">probabilitas defisit dari {n_sim:,} iterasi simulasi — sekitar {prob_deficit/10:.0f} dari 10 bulan berpotensi defisit</div>
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
                    <li>Kesenjangan pemasukan-pengeluaran sebesar <strong>Rp 242.352/bulan</strong></li>
                    <li>Uji-T menunjukkan perbedaan tidak signifikan (p=0.4031 > 0.05),
                        namun deskriptif membuktikan 73.5% responden defisit</li>
                    <li>Monte Carlo mengkonfirmasi probabilitas defisit <strong>64.25%</strong>
                        — sinyal risiko finansial nyata</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="research-box">
                <h4>💡 Insight Utama</h4>
                <ul>
                    <li>Proporsi pengeluaran tertinggi untuk makan & minum (46.5%) dan hiburan (19.8%)</li>
                    <li>Alokasi hiburan melampaui biaya esensial seperti transportasi dan akademik</li>
                    <li>Fenomena ini mencerminkan pola konsumtif Gen Z akibat kemudahan transaksi digital</li>
                    <li>Defisit bukan anomali matematis, melainkan representasi rendahnya literasi keuangan</li>
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
                        (n ≥ 100) untuk meminimalkan dampak outlier pada uji statistik</li>
                    <li><strong style="color:#60A5FA">Intervensi Digital:</strong> Kembangkan aplikasi
                        tracking pengeluaran yang terintegrasi dengan sistem kampus</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

            # Auto-generated conclusion box
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
