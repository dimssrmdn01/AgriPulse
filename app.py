import streamlit as st
import database 
import style

st.set_page_config(
    page_title="AgriPulse | Tracker Komoditas",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Terapkan desain sistem untuk Home
style.apply_design_tokens(is_home=True)

# ============================================================
# HERO
# ============================================================
st.markdown("""
<div class="ap-eyebrow">Denyut Pasar dari Kebun ke Layar</div>
<div class="ap-hero-title">AgriPulse <em>Commodity Intelligence</em></div>
<div class="ap-hero-sub">
  Pemantauan harga dan analisis sentimen untuk tiga komoditas rakyat &mdash;
  <b>Karet, Pinang, dan Gambir</b> &mdash; merangkum data pasar global hingga
  laporan langsung dari petani dan pengepul di lapangan.
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="ap-divider">', unsafe_allow_html=True)

# ============================================================
# STATUS INFRASTRUKTUR DATA
# ============================================================
st.markdown("""
<div class="ap-section-label">Arsitektur Data</div>
<div class="ap-section-title">Status Infrastruktur per Komoditas</div>
<div class="ap-section-desc">
  Ketersediaan data untuk tiap komoditas jauh berbeda satu sama lain.
  AgriPulse memakai pendekatan bertingkat (multi-tier) dan jujur menampilkan
  tingkat keandalan tiap sumber &mdash; bukan menyamaratakan semua sebagai "prediksi".
</div>
""", unsafe_allow_html=True)

commodities = [
    {
        "icon": "🌾",
        "name": "Karet",
        "tier": "TIER 1 · PREDIKTIF",
        "status": "Model Machine Learning",
        "meta": "Sumber: Harga futures harian (SICOM/TOCOM)",
        "caption": "Memanfaatkan pergerakan harga futures di bursa komoditas global dan analisis sentimen berita untuk memprediksi arah harga.",
        "accent": "var(--karet)",
        "accent_bg": "var(--karet-bg)",
    },
    {
        "icon": "🌰",
        "name": "Pinang",
        "tier": "TIER 2 · INDIKATIF",
        "status": "Trend Indicator",
        "meta": "Sumber: Data ekspor FOB musiman (BPS)",
        "caption": "Fokus pada klasifikasi tren pasar (naik/turun/stabil) dari agregasi volume ekspor tahunan dan dinamika permintaan negara tujuan.",
        "accent": "var(--pinang)",
        "accent_bg": "var(--pinang-bg)",
    },
    {
        "icon": "🍃",
        "name": "Gambir",
        "tier": "TIER 3 · KOMUNITAS",
        "status": "Crowdsourced Log",
        "meta": "Sumber: Laporan langsung petani/pengepul",
        "caption": "Mengatasi minimnya data terstruktur dengan membangun basis data harga mandiri lewat kontribusi langsung dari lapangan.",
        "accent": "var(--gambir)",
        "accent_bg": "var(--gambir-bg)",
    },
]

cols = st.columns(3, gap="medium")
for col, c in zip(cols, commodities):
    with col:
        st.markdown(f"""
        <div class="ap-card" style="--accent-color:{c['accent']}; --accent-bg:{c['accent_bg']};">
          <div class="ap-card-top">
            <div class="ap-card-icon">{c['icon']}</div>
            <div class="ap-stamp">{c['tier']}</div>
          </div>
          <div class="ap-card-name">{c['name']}</div>
          <div class="ap-card-status">{c['status']}</div>
          <div class="ap-card-meta">{c['meta']}</div>
          <div class="ap-card-caption">{c['caption']}</div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# CTA / NAVIGASI
# ============================================================
st.markdown("""
<div class="ap-cta">
  👈 Gunakan <b>Sidebar</b> di sebelah kiri untuk membuka halaman detail tiap
  komoditas, atau untuk ikut melaporkan harga terkini di daerahmu.
</div>
""", unsafe_allow_html=True)