import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# 1. Konfigurasi Utama Halaman Dashboard
st.set_page_config(page_title="Dashboard Analisis Pengeluaran", layout="wide")
st.title("📊 Dashboard Analisis Defisit Keuangan Mahasiswa")
st.markdown("Eksplorasi probabilitas defisit keuangan berdasarkan simulasi stokastik Monte Carlo.")

# 2. Fungsi Cerdas untuk Mendeteksi dan Membaca Berkas Secara Otomatis
@st.cache_data
def load_data_otomatis():
    kata_kunci = "Data_Pengeluaran_Bulanan_Bersih"
    semua_berkas = os.listdir('.')
    berkas_target = None
    
    # Mencari berkas yang mengandung nama data Anda
    for berkas in semua_berkas:
        if kata_kunci in berkas:
            berkas_target = berkas
            break
            
    if not berkas_target:
        raise FileNotFoundError("Berkas data tidak ditemukan di folder aktif Anda. Pastikan berkas data berada satu folder dengan file app.py.")
        
    # Mencoba membaca berkas berdasarkan format aslinya
    if berkas_target.endswith('.csv') or 'csv' in berkas_target.lower():
        return pd.read_csv(berkas_target)
    else:
        try:
            return pd.read_excel(berkas_target)
        except Exception:
            # Jika gagal membaca sebagai Excel, paksa baca sebagai CSV (antitesis salah ekstensi)
            return pd.read_csv(berkas_target)

# 3. Eksekusi Komputasi Data dan Penanganan Hambatan
try:
    df = load_data_otomatis()
    
    # Membersihkan spasi gaib pada nama kolom jika ada
    df.columns = df.columns.str.strip()
    
    nama_kolom_pemasukan = 'Pemasukan / Uang Saku Bulanan'
    nama_kolom_pengeluaran = 'Total_Pengeluaran_Bulanan'
    
    # Validasi keberadaan kolom data utama
    if nama_kolom_pemasukan not in df.columns or nama_kolom_pengeluaran not in df.columns:
        st.error(f"Struktur kolom tidak sesuai! Kolom yang terdeteksi di berkas Anda adalah: {list(df.columns)}")
        st.stop()
        
    # Ekstraksi Parameter Statistika Deskriptif
    mean_pengeluaran = df[nama_kolom_pengeluaran].mean()
    std_pengeluaran = df[nama_kolom_pengeluaran].std()
    mean_pemasukan = df[nama_kolom_pemasukan].mean()
    selisih = mean_pemasukan - mean_pengeluaran

    # Menampilkan Ringkasan Metrik Utama (KPI Cards)
    col1, col2, col3 = st.columns(3)
    col1.metric("Rata-rata Pemasukan", f"Rp {mean_pemasukan:,.0f}")
    col2.metric("Rata-rata Pengeluaran", f"Rp {mean_pengeluaran:,.0f}")
    col3.metric("Defisit Rata-rata", f"Rp {selisih:,.0f}")

    st.divider()

    # 4. Komputasi Distribusi Simulasi Monte Carlo
    st.subheader("🎲 Simulasi Monte Carlo (Probabilitas Defisit)")
    jumlah_simulasi = st.slider("Pilih Jumlah Iterasi Simulasi:", 1000, 50000, 10000, 1000)

    np.random.seed(42)
    simulasi_pengeluaran = np.random.normal(mean_pengeluaran, std_pengeluaran, jumlah_simulasi)
    kebobolan = simulasi_pengeluaran > mean_pemasukan
    probabilitas = (kebobolan.sum() / jumlah_simulasi) * 100

    st.warning(f"💡 Berdasarkan {jumlah_simulasi:,} skenario, probabilitas mahasiswa mengalami defisit keuangan adalah **{probabilitas:.2f}%**")

    # 5. Visualisasi Grafik Distribusi Frekuensi
    st.subheader("📈 Distribusi Frekuensi Hasil Simulasi")
    fig, ax = plt.subplots(figsize=(11, 5))
    
    # Plot histogram skenario
    ax.hist(simulasi_pengeluaran, bins=50, color='#87CEFA', edgecolor='white', alpha=0.8)
    ax.axvline(mean_pemasukan, color='#DC143C', linestyle='dashed', linewidth=3, 
               label=f'Batas Uang Saku (Rp {mean_pemasukan:,.0f})')
    
    ax.set_title('Fenomena Defisit: Rata-rata Uang Saku vs Pengeluaran Mahasiswa', fontsize=14, fontweight='bold', pad=15)
    ax.set_xlabel('Nominal (Rupiah)')
    ax.set_ylabel('Frekuensi Skenario')
    ax.legend()
    sns.despine(left=True, bottom=False)
    
    st.pyplot(fig)

except Exception as error_sistem:
    st.error(f"🛑 Kendala Deteksi Sistem: {error_sistem}")
    st.info("Solusi: Pastikan berkas data Anda dan berkas 'app.py' berada di dalam satu folder workspace yang sama di VS Code.")