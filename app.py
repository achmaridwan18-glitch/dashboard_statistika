import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go

# ==================================================
# KONFIGURASI HALAMAN
# ==================================================

st.set_page_config(
    page_title="Dashboard Analisis Defisit Keuangan Mahasiswa",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dashboard Analisis Defisit Keuangan Mahasiswa")
st.markdown("""
Dashboard ini digunakan untuk menganalisis kondisi keuangan mahasiswa
berdasarkan data pengeluaran bulanan serta simulasi Monte Carlo untuk
mengukur probabilitas terjadinya defisit keuangan.
""")

# ==================================================
# LOAD DATA
# ==================================================

@st.cache_data
def load_data():
    return pd.read_csv(
        "Data_Pengeluaran_Mahasiswa.csv",
        sep=";"
    )

try:

    df = load_data()

    df.columns = df.columns.str.strip()

    kolom_pemasukan = "Pemasukan / Uang Saku Bulanan"
    kolom_pengeluaran = "Total_Pengeluaran_Bulanan"

    # ==================================================
    # VALIDASI DATA
    # ==================================================

    if kolom_pemasukan not in df.columns:
        st.error(f"Kolom '{kolom_pemasukan}' tidak ditemukan.")
        st.stop()

    if kolom_pengeluaran not in df.columns:
        st.error(f"Kolom '{kolom_pengeluaran}' tidak ditemukan.")
        st.stop()

    # ==================================================
    # SIDEBAR
    # ==================================================

    st.sidebar.header("⚙ Pengaturan Simulasi")

    jumlah_simulasi = st.sidebar.slider(
        "Jumlah Simulasi Monte Carlo",
        1000,
        50000,
        10000,
        1000
    )

    # ==================================================
    # STATISTIK DASAR
    # ==================================================

    mean_income = df[kolom_pemasukan].mean()
    mean_expense = df[kolom_pengeluaran].mean()
    std_expense = df[kolom_pengeluaran].std()

    selisih = mean_income - mean_expense

    # ==================================================
    # MONTE CARLO
    # ==================================================

    np.random.seed(42)

    simulasi = np.random.normal(
        mean_expense,
        std_expense,
        jumlah_simulasi
    )

    defisit = simulasi > mean_income

    probabilitas_defisit = (
        defisit.sum() / jumlah_simulasi
    ) * 100

    # ==================================================
    # KPI
    # ==================================================

    st.subheader("📌 Ringkasan Utama")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Jumlah Responden",
        len(df)
    )

    col2.metric(
        "Rata-rata Pemasukan",
        f"Rp {mean_income:,.0f}"
    )

    col3.metric(
        "Rata-rata Pengeluaran",
        f"Rp {mean_expense:,.0f}"
    )

    col4.metric(
        "Probabilitas Defisit",
        f"{probabilitas_defisit:.2f}%"
    )

    st.divider()

    # ==================================================
    # HISTOGRAM PEMASUKAN
    # ==================================================

    colA, colB = st.columns(2)

    with colA:

        st.subheader("📈 Distribusi Pemasukan")

        fig, ax = plt.subplots(figsize=(6,4))

        ax.hist(
            df[kolom_pemasukan],
            bins=20
        )

        ax.set_xlabel("Pemasukan")
        ax.set_ylabel("Frekuensi")

        st.pyplot(fig)

    # ==================================================
    # HISTOGRAM PENGELUARAN
    # ==================================================

    with colB:

        st.subheader("📉 Distribusi Pengeluaran")

        fig, ax = plt.subplots(figsize=(6,4))

        ax.hist(
            df[kolom_pengeluaran],
            bins=20
        )

        ax.set_xlabel("Pengeluaran")
        ax.set_ylabel("Frekuensi")

        st.pyplot(fig)

    # ==================================================
    # BOXPLOT
    # ==================================================

    st.subheader("📦 Perbandingan Pemasukan dan Pengeluaran")

    fig, ax = plt.subplots(figsize=(8,5))

    ax.boxplot(
        [
            df[kolom_pemasukan],
            df[kolom_pengeluaran]
        ],
        labels=["Pemasukan","Pengeluaran"]
    )

    st.pyplot(fig)

    # ==================================================
    # HEATMAP KORELASI
    # ==================================================

    st.subheader("🔥 Heatmap Korelasi")

    numeric_df = df.select_dtypes(include=np.number)

    if len(numeric_df.columns) > 1:

        fig, ax = plt.subplots(figsize=(10,6))

        sns.heatmap(
            numeric_df.corr(),
            annot=True,
            cmap="Blues",
            ax=ax
        )

        st.pyplot(fig)

    else:
        st.info("Tidak cukup kolom numerik untuk membuat heatmap.")

    # ==================================================
    # MONTE CARLO
    # ==================================================

    st.subheader("🎲 Simulasi Monte Carlo")

    fig, ax = plt.subplots(figsize=(10,5))

    ax.hist(
        simulasi,
        bins=50,
        alpha=0.7
    )

    ax.axvline(
        mean_income,
        color="red",
        linestyle="--",
        linewidth=3,
        label="Rata-rata Pemasukan"
    )

    ax.set_title(
        "Distribusi Simulasi Pengeluaran Mahasiswa"
    )

    ax.legend()

    st.pyplot(fig)

    # ==================================================
    # GAUGE CHART
    # ==================================================

    st.subheader("🚨 Tingkat Risiko Defisit")

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=probabilitas_defisit,
            title={"text":"Probabilitas Defisit (%)"},
            gauge={
                "axis":{"range":[0,100]},
                "steps":[
                    {"range":[0,30]},
                    {"range":[30,60]},
                    {"range":[60,100]}
                ]
            }
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ==================================================
    # DATASET
    # ==================================================

    st.subheader("📋 Dataset")

    st.dataframe(df)

    # ==================================================
    # STATISTIK DESKRIPTIF
    # ==================================================

    st.subheader("📑 Statistik Deskriptif")

    st.dataframe(
        df.describe()
    )

    # ==================================================
    # KESIMPULAN
    # ==================================================

    st.subheader("📝 Kesimpulan")

    if probabilitas_defisit < 30:

        st.success(
            f"""
            Probabilitas defisit sebesar {probabilitas_defisit:.2f}%.
            Risiko defisit tergolong rendah sehingga kondisi keuangan
            mahasiswa relatif stabil.
            """
        )

    elif probabilitas_defisit < 60:

        st.warning(
            f"""
            Probabilitas defisit sebesar {probabilitas_defisit:.2f}%.
            Risiko defisit tergolong sedang sehingga mahasiswa perlu
            mengelola pengeluaran secara lebih efektif.
            """
        )

    else:

        st.error(
            f"""
            Probabilitas defisit sebesar {probabilitas_defisit:.2f}%.
            Risiko defisit tergolong tinggi sehingga mahasiswa berpotensi
            mengalami kekurangan dana bulanan.
            """
        )

except Exception as e:

    st.error(f"Terjadi kesalahan: {e}")
