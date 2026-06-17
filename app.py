import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ==================================================
# KONFIGURASI HALAMAN
# ==================================================
st.set_page_config(
    page_title="Dashboard Analisis Defisit Keuangan Mahasiswa",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# CUSTOM CSS - TEMA MODERN DATA SCIENCE (POWER BI / TABLEAU STYLE)
# ==================================================
st.markdown("""
<style>
    /* Main Background */
    .stApp {
        background-color: #0F172A;
        color: #E2E8F0;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #1E293B;
        border-right: 2px solid #38BDF8;
    }
    
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #38BDF8 !important;
    }
    
    /* Premium KPI Cards */
    .metric-card {
        background: linear-gradient(135deg, #1E293B 0%, #334155 100%);
        padding: 25px 20px;
        border-radius: 12px;
        border: 2px solid #38BDF8;
        box-shadow: 0 4px 15px rgba(56, 189, 248, 0.15);
        text-align: center;
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .metric-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 8px 25px rgba(56, 189, 248, 0.3);
        border-color: #7DD3FC;
    }
    
    .metric-value {
        font-size: 32px;
        font-weight: bold;
        color: #38BDF8;
        margin: 15px 0 10px 0;
        text-shadow: 0 2px 4px rgba(56, 189, 248, 0.2);
    }
    
    .metric-label {
        font-size: 13px;
        color: #94A3B8;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        font-weight: 600;
    }
    
    .metric-sublabel {
        font-size: 11px;
        color: #64748B;
        margin-top: 8px;
    }
    
    /* Section Headers */
    h1 {
        color: #38BDF8 !important;
        font-weight: 700;
        border-bottom: 3px solid #38BDF8;
        padding-bottom: 12px;
        margin-bottom: 20px;
        text-shadow: 0 2px 8px rgba(56, 189, 248, 0.3);
    }
    
    h2 {
        color: #E2E8F0 !important;
        font-weight: 600;
        margin-top: 30px;
        margin-bottom: 20px;
    }
    
    h3 {
        color: #38BDF8 !important;
        font-weight: 500;
        margin-top: 20px;
    }
    
    /* Insight Box */
    .insight-box {
        background: linear-gradient(135deg, #1E293B 0%, #334155 100%);
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #38BDF8;
        margin: 15px 0;
        box-shadow: 0 2px 8px rgba(56, 189, 248, 0.1);
    }
    
    /* Plotly Chart Containers */
    .js-plotly-plot {
        background-color: #1E293B !important;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #1E293B;
        border-radius: 8px;
        color: #E2E8F0;
        padding: 10px 20px;
        border: 2px solid #334155;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #38BDF8;
        color: #0F172A;
        font-weight: 600;
    }
    
    /* Success/Warning/Error Messages */
    .stSuccess {
        background-color: #064E3B !important;
        color: #6EE7B7 !important;
        border-left: 5px solid #10B981 !important;
    }
    
    .stWarning {
        background-color: #78350F !important;
        color: #FCD34D !important;
        border-left: 5px solid #F59E0B !important;
    }
    
    .stError {
        background-color: #7F1D1D !important;
        color: #FCA5A5 !important;
        border-left: 5px solid #EF4444 !important;
    }
    
    /* Dividers */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #38BDF8, transparent);
        margin: 30px 0;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .metric-value { font-size: 24px; }
        .metric-label { font-size: 11px; }
        .metric-card { padding: 15px; }
        h1 { font-size: 24px; }
    }
    
    /* Button Styling */
    .stButton > button {
        background-color: #38BDF8;
        color: #0F172A;
        border: none;
        border-radius: 8px;
        font-weight: 600;
        padding: 10px 24px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #7DD3FC;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(56, 189, 248, 0.4);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 30px;
        color: #94A3B8;
        border-top: 2px solid #334155;
        margin-top: 50px;
    }
</style>
""", unsafe_allow_html=True)

# ==================================================
# LOAD DATA & AUTO-DETEKSI KOLOM (ANTI ERROR)
# ==================================================
@st.cache_data
def load_data():
    return pd.read_csv("Data_Pengeluaran_Mahasiswa.csv", sep=";")

try:
    df = load_data()
    
    # Bersihkan spasi di awal/akhir nama kolom dari CSV
    df.columns = df.columns.str.strip()
    
    # [SOLUSI PERMANEN] Auto-deteksi kolom berdasarkan kata kunci
    # Ini mencegah error akibat spasi tersembunyi atau typo di file CSV
    kolom_pemasukan = next((c for c in df.columns if "Pemasukan" in c or "Uang Saku" in c), None)
    kolom_pengeluaran = next((c for c in df.columns if "Pengeluaran" in c), None)

    if not kolom_pemasukan or not kolom_pengeluaran:
        st.error("❌ Kolom Pemasukan atau Pengeluaran tidak ditemukan di CSV Anda.")
        st.info(f"💡 **Kolom yang terbaca sistem:** {df.columns.tolist()}")
        st.stop()

    # ==================================================
    # SIDEBAR - PENGATURAN
    # ==================================================
    st.sidebar.markdown("## ⚙️ Pengaturan Simulasi")
    st.sidebar.markdown("---")
    
    jumlah_simulasi = st.sidebar.slider(
        "Jumlah Simulasi Monte Carlo",
        min_value=1000,
        max_value=50000,
        value=10000,
        step=1000,
        help="Semakin banyak simulasi, semakin akurat hasilnya"
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"""
    ### 📖 Informasi Dataset
    - **File:** `Data_Pengeluaran_Mahasiswa.csv`
    - **Kolom Pemasukan:** `{kolom_pemasukan}`
    - **Kolom Pengeluaran:** `{kolom_pengeluaran}`
    - **Total Data:** {len(df)} Baris
    """)

    # ==================================================
    # PERHITUNGAN STATISTIK & MONTE CARLO
    # ==================================================
    mean_income = df[kolom_pemasukan].mean()
    mean_expense = df[kolom_pengeluaran].mean()
    std_expense = df[kolom_pengeluaran].std()
    selisih = mean_income - mean_expense
    
    np.random.seed(42)
    simulasi = np.random.normal(loc=mean_expense, scale=std_expense, size=jumlah_simulasi)
    
    defisit = simulasi > mean_income
    probabilitas_defisit = (defisit.sum() / jumlah_simulasi) * 100
    surplus_count = (~defisit).sum()
    deficit_count = defisit.sum()

    # ==================================================
    # JUDUL DASHBOARD
    # ==================================================
    st.markdown("# 📊 Dashboard Analisis Defisit Keuangan Mahasiswa")
    st.markdown("### Simulasi Monte Carlo untuk Pengukuran Risiko Finansial")
    st.markdown("---")

    # ==================================================
    # EXECUTIVE SUMMARY - KPI CARDS
    # ==================================================
    st.markdown("## 📌 Executive Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">👥 Jumlah Responden</div>
            <div class="metric-value">{len(df)}</div>
            <div class="metric-sublabel">Mahasiswa</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">💰 Rata-rata Pemasukan</div>
            <div class="metric-value">Rp {mean_income:,.0f}</div>
            <div class="metric-sublabel">Per Bulan</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">💸 Rata-rata Pengeluaran</div>
            <div class="metric-value">Rp {mean_expense:,.0f}</div>
            <div class="metric-sublabel">Per Bulan</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        color_prob = "#EF4444" if probabilitas_defisit > 60 else "#F59E0B" if probabilitas_defisit > 30 else "#10B981"
        risk_label = "Tinggi" if probabilitas_defisit > 60 else "Sedang" if probabilitas_defisit > 30 else "Rendah"
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">⚠️ Probabilitas Defisit</div>
            <div class="metric-value" style="color: {color_prob};">{probabilitas_defisit:.2f}%</div>
            <div class="metric-sublabel">Risiko {risk_label}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")

    # ==================================================
    # TABS LAYOUT
    # ==================================================
    tab1, tab2, tab3, tab4 = st.tabs([
        "💰 Financial Overview", 
        "🚨 Risk Analytics", 
        "🔥 Analisis Korelasi", 
        "📝 Research Insights"
    ])

    # ==========================
    # TAB 1: FINANCIAL OVERVIEW
    # ==========================
    with tab1:
        colA, colB = st.columns(2)
        with colA:
            st.markdown("### 📈 Distribusi Pemasukan")
            fig_income = px.histogram(df, x=kolom_pemasukan, nbins=20, color_discrete_sequence=['#38BDF8'])
            fig_income.update_layout(paper_bgcolor='#1E293B', plot_bgcolor='#1E293B', font_color='#E2E8F0',
                                     xaxis_title="Pemasukan (Rp)", yaxis_title="Frekuensi", bargap=0.05)
            st.plotly_chart(fig_income, use_container_width=True)
        
        with colB:
            st.markdown("### 📉 Distribusi Pengeluaran")
            fig_expense = px.histogram(df, x=kolom_pengeluaran, nbins=20, color_discrete_sequence=['#EF4444'])
            fig_expense.update_layout(paper_bgcolor='#1E293B', plot_bgcolor='#1E293B', font_color='#E2E8F0',
                                      xaxis_title="Pengeluaran (Rp)", yaxis_title="Frekuensi", bargap=0.05)
            st.plotly_chart(fig_expense, use_container_width=True)

        colC, colD = st.columns(2)
        with colC:
            st.markdown("### 🎯 Scatter Plot: Pemasukan vs Pengeluaran")
            fig_scatter = px.scatter(df, x=kolom_pemasukan, y=kolom_pengeluaran, color_discrete_sequence=['#38BDF8'], trendline="ols")
            fig_scatter.update_layout(paper_bgcolor='#1E293B', plot_bgcolor='#1E293B', font_color='#E2E8F0',
                                      xaxis_title="Pemasukan (Rp)", yaxis_title="Pengeluaran (Rp)")
            st.plotly_chart(fig_scatter, use_container_width=True)
        
        with colD:
            st.markdown("### 📦 Boxplot Perbandingan")
            fig_box = go.Figure()
            fig_box.add_trace(go.Box(y=df[kolom_pemasukan], name="Pemasukan", marker_color='#38BDF8', boxmean=True))
            fig_box.add_trace(go.Box(y=df[kolom_pengeluaran], name="Pengeluaran", marker_color='#EF4444', boxmean=True))
            fig_box.update_layout(title="Perbandingan Pemasukan dan Pengeluaran", paper_bgcolor='#1E293B',
                                  plot_bgcolor='#1E293B', font_color='#E2E8F0', yaxis_title="Jumlah (Rp)")
            st.plotly_chart(fig_box, use_container_width=True)

    # ==========================
    # TAB 2: RISK ANALYTICS
    # ==========================
    with tab2:
        st.markdown("### 🎲 Distribusi Simulasi Monte Carlo")
        fig_monte = go.Figure()
        fig_monte.add_trace(go.Histogram(x=simulasi, nbinsx=50, name="Simulasi Pengeluaran", marker_color='#38BDF8', opacity=0.7))
        fig_monte.add_vline(x=mean_income, line_dash="dash", line_color="#EF4444", line_width=3,
                            annotation_text=f"Batas Pemasukan: Rp {mean_income:,.0f}", annotation_position="top right")
        fig_monte.update_layout(title=f"Distribusi {jumlah_simulasi:,} Simulasi Pengeluaran", paper_bgcolor='#1E293B',
                                plot_bgcolor='#1E293B', font_color='#E2E8F0', xaxis_title="Pengeluaran (Rp)", yaxis_title="Frekuensi")
        st.plotly_chart(fig_monte, use_container_width=True)

        colE, colF = st.columns(2)
        with colE:
            st.markdown("### 🚨 Gauge Chart: Tingkat Risiko Defisit")
            gauge_color = "#EF4444" if probabilitas_defisit > 60 else "#F59E0B" if probabilitas_defisit > 30 else "#10B981"
            fig_gauge = go.Figure(go.Indicator(
                mode="gauge+number", value=probabilitas_defisit,
                number={'suffix': '%', 'font': {'size': 40, 'color': gauge_color}},
                title={"text": "Probabilitas Defisit", 'font': {'size': 20}},
                gauge={
                    'axis': {'range': [0, 100], 'tickcolor': '#E2E8F0'},
                    'bar': {'color': gauge_color, 'thickness': 0.3},
                    'steps': [{'range': [0, 30], 'color': '#064E3B'}, {'range': [30, 60], 'color': '#78350F'}, {'range': [60, 100], 'color': '#7F1D1D'}],
                    'threshold': {'line': {'color': "white", 'width': 4}, 'thickness': 0.75, 'value': probabilitas_defisit}
                }
            ))
            fig_gauge.update_layout(paper_bgcolor='#1E293B', font_color='#E2E8F0', height=350)
            st.plotly_chart(fig_gauge, use_container_width=True)
        
        with colF:
            st.markdown("### 🍩 Donut Chart: Surplus vs Defisit")
            fig_donut = go.Figure(data=[go.Pie(
                labels=['✅ Surplus', '❌ Defisit'], values=[surplus_count, deficit_count], hole=0.45,
                marker={'colors': ['#10B981', '#EF4444']}, textinfo='label+percent', textposition='outside'
            )])
            fig_donut.update_layout(title=f"Distribusi Hasil Simulasi", paper_bgcolor='#1E293B', font_color='#E2E8F0', height=350)
            st.plotly_chart(fig_donut, use_container_width=True)

    # ==========================
    # TAB 3: ANALISIS KORELASI
    # ==========================
    with tab3:
        st.markdown("### 🔥 Heatmap Korelasi Variabel Numerik")
        numeric_df = df.select_dtypes(include=np.number)
        if len(numeric_df.columns) > 1:
            fig_heatmap = px.imshow(numeric_df.corr(), text_auto=".2f", color_continuous_scale='Blues', aspect='auto')
            fig_heatmap.update_layout(paper_bgcolor='#1E293B', plot_bgcolor='#1E293B', font_color='#E2E8F0')
            st.plotly_chart(fig_heatmap, use_container_width=True)
        else:
            st.info("ℹ️ Tidak cukup kolom numerik untuk membuat heatmap.")

    # ==========================
    # TAB 4: RESEARCH INSIGHTS
    # ==========================
    with tab4:
        st.markdown("### 💡 Insight Otomatis & Kesimpulan")
        
        insights = []
        if selisih > 0:
            insights.append({'icon': '✅', 'title': 'Kondisi Finansial Positif', 'text': f'Rata-rata mahasiswa memiliki surplus sebesar Rp {selisih:,.0f} per bulan.'})
        else:
            insights.append({'icon': '⚠️', 'title': 'Kondisi Finansial Negatif', 'text': f'Rata-rata mahasiswa mengalami defisit sebesar Rp {abs(selisih):,.0f} per bulan.'})
            
        if probabilitas_defisit < 30:
            insights.append({'icon': '🟢', 'title': 'Risiko Rendah', 'text': f'Probabilitas defisit hanya {probabilitas_defisit:.2f}%, stabilitas keuangan baik.'})
        elif probabilitas_defisit < 60:
            insights.append({'icon': '🟡', 'title': 'Risiko Sedang', 'text': f'Probabilitas defisit {probabilitas_defisit:.2f}% memerlukan pengelolaan pengeluaran lebih efektif.'})
        else:
            insights.append({'icon': '🔴', 'title': 'Risiko Tinggi', 'text': f'Probabilitas defisit {probabilitas_defisit:.2f}%, potensi besar kekurangan dana bulanan.'})
            
        for insight in insights:
            st.markdown(f"""
            <div class="insight-box">
                <h4>{insight['icon']} {insight['title']}</h4>
                <p>{insight['text']}</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 🎯 Kesimpulan Penelitian & Rekomendasi")
        if probabilitas_defisit < 30:
            st.success(f"**Probabilitas defisit {probabilitas_defisit:.2f}%**. Mayoritas mahasiswa stabil. Rekomendasi: Pertahankan pola budgeting dan tingkatkan literasi finansial.")
        elif probabilitas_defisit < 60:
            st.warning(f"**Probabilitas defisit {probabilitas_defisit:.2f}%**. Risiko sedang. Rekomendasi: Terapkan metode budgeting 50/30/20 dan catat pengeluaran harian.")
        else:
            st.error(f"**Probabilitas defisit {probabilitas_defisit:.2f}%**. Risiko tinggi. Rekomendasi: Audit pengeluaran non-prioritas dan cari alternatif pendapatan tambahan.")
            
        st.markdown("### 📋 Dataset Mentah")
        st.dataframe(df, use_container_width=True, height=300)

    # ==================================================
    # FOOTER
    # ==================================================
    st.markdown("---")
    st.markdown("""
    <div class="footer">
        <p><strong>📊 Dashboard Analisis Defisit Keuangan Mahasiswa</strong></p>
        <p>Developed with Streamlit & Plotly | Simulasi Monte Carlo</p>
    </div>
    """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"❌ Terjadi kesalahan sistem: {e}")
    st.markdown("### 📝 Panduan Troubleshooting:")
    st.markdown("""
    1. Pastikan file `Data_Pengeluaran_Mahasiswa.csv` ada di folder yang sama.
    2. Pastikan delimiter CSV adalah titik koma (`;`).
    3. Pastikan terdapat kolom yang mengandung kata "Pemasukan" atau "Uang Saku" dan "Pengeluaran".
    """)
