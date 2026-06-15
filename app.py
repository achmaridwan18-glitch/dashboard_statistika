import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi halaman
st.set_page_config(
    page_title="Dashboard Analisis Pengeluaran Mahasiswa",
    layout="wide"
)

st.title("📊 Dashboard Analisis Defisit Keuangan Mahasiswa")
st.markdown(
    "Eksplorasi probabilitas defisit keuangan mahasiswa menggunakan simulasi Monte Carlo."
)

# Load Data
@st.cache_data
def load_data():
    return pd.read_csv("Data_Pengeluaran_Mahasiswa.csv")

try:
    df = load_data()

    # Bersihkan nama kolom
    df.columns = df.columns.str.strip()

    # Nama kolom dataset
    kolom_pemasukan = "Pemasukan / Uang Saku Bulanan"
    kolom_pengeluaran = "Total_Pengeluaran_Bulanan"

    # Validasi kolom
    if kolom_pemasukan not in df.columns:
        st.error(f"Kolom '{kolom_pemasukan}' tidak ditemukan.")
        st.stop()

    if kolom_pengeluaran not in df.columns:
        st.error(f"Kolom '{kolom_pengeluaran}' tidak ditemukan.")
        st.stop()

    # Statistik dasar
    mean_pemasukan = df[kolom_pemasukan].mean()
    mean_pengeluaran = df[kolom_pengeluaran].mean()
    std_pengeluaran = df[kolom_pengeluaran].std()

    selisih = mean_pemasukan - mean_pengeluaran

    # KPI
    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Rata-rata Pemasukan",
        f"Rp {mean_pemasukan:,.0f}"
    )

    col2.metric(
        "Rata-rata Pengeluaran",
        f"Rp {mean_pengeluaran:,.0f}"
    )

    col3.metric(
        "Selisih",
        f"Rp {selisih:,.0f}"
    )

    st.divider()

    # Monte Carlo
    st.subheader("🎲 Simulasi Monte Carlo")

    jumlah_simulasi = st.slider(
        "Jumlah Simulasi",
        1000,
        50000,
        10000,
        1000
    )

    np.random.seed(42)

    simulasi_pengeluaran = np.random.normal(
        mean_pengeluaran,
        std_pengeluaran,
        jumlah_simulasi
    )

    defisit = simulasi_pengeluaran > mean_pemasukan

    probabilitas_defisit = (
        defisit.sum() / jumlah_simulasi
    ) * 100

    st.warning(
        f"Probabilitas mahasiswa mengalami defisit keuangan sebesar "
        f"**{probabilitas_defisit:.2f}%**"
    )

    # Histogram
    st.subheader("📈 Distribusi Hasil Simulasi")

    fig, ax = plt.subplots(figsize=(10, 5))

    ax.hist(
        simulasi_pengeluaran,
        bins=50,
        alpha=0.8
    )

    ax.axvline(
        mean_pemasukan,
        linestyle="--",
        linewidth=2,
        label=f"Rata-rata Pemasukan (Rp {mean_pemasukan:,.0f})"
    )

    ax.set_xlabel("Nominal Pengeluaran")
    ax.set_ylabel("Frekuensi")
    ax.legend()

    st.pyplot(fig)

except Exception as e:
    st.error(f"Terjadi kesalahan: {e}")
