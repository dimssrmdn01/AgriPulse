import streamlit as st
import database 

st.set_page_config(
    page_title="AgriPulse | Tracker Komoditas",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# DESIGN TOKENS
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500;600&display=swap');

:root{
  --bg: #211814;
  --bg-soft: #2A1F19;
  --surface: #2C221C;
  --border: #4A392F;
  --border-soft: rgba(242,233,222,0.10);
  --text: #F2E9DE;
  --text-dim: #B8A793;
  --text-faint: #806F5F;

  --karet: #E7DCC4;
  --karet-bg: rgba(231,220,196,0.08);
  --pinang: #C1622D;
  --pinang-bg: rgba(193,98,45,0.12);
  --gambir: #A34A3A;
  --gambir-bg: rgba(163,74,58,0.12);

  --good: #7BA05B;
  --font-display: 'Fraunces', Georgia, serif;
  --font-sans: 'IBM Plex Sans', sans-serif;
  --font-mono: 'IBM Plex Mono', monospace;
}

/* ---- Base app surface ---- */
.stApp{
  background:
    radial-gradient(ellipse 70% 40% at 15% 0%, rgba(193,98,45,0.10), transparent 60%),
    radial-gradient(ellipse 60% 40% at 85% 10%, rgba(163,74,58,0.08), transparent 60%),
    var(--bg);
  font-family: var(--font-sans);
  color: var(--text);
}
section[data-testid="stSidebar"]{
  background: var(--bg-soft);
  border-right: 1px solid var(--border-soft);
}
.block-container{ padding-top: 2.5rem; max-width: 1180px; }

/* ---- Hero ---- */
.ap-eyebrow{
  font-family: var(--font-mono);
  font-size: 12px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--pinang);
  margin-bottom: 14px;
  opacity: 0;
  animation: apFadeUp .7s ease forwards;
}
.ap-hero-title{
  font-family: var(--font-display);
  font-weight: 600;
  font-size: clamp(36px, 5vw, 56px);
  line-height: 1.08;
  letter-spacing: -0.01em;
  color: var(--text);
  margin: 0 0 16px 0;
  opacity: 0;
  animation: apFadeUp .7s ease .08s forwards;
}
.ap-hero-title em{
  font-style: italic;
  color: var(--pinang);
}
.ap-hero-sub{
  font-size: 16.5px;
  line-height: 1.65;
  color: var(--text-dim);
  max-width: 620px;
  opacity: 0;
  animation: apFadeUp .7s ease .16s forwards;
}
@keyframes apFadeUp{ from{opacity:0; transform: translateY(10px);} to{opacity:1; transform: translateY(0);} }

.ap-divider{
  border: none;
  border-top: 1px solid var(--border-soft);
  margin: 36px 0 32px 0;
}

.ap-section-label{
  font-family: var(--font-mono);
  font-size: 12px;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: var(--text-faint);
  margin-bottom: 6px;
}
.ap-section-title{
  font-family: var(--font-display);
  font-weight: 600;
  font-size: 24px;
  color: var(--text);
  margin-bottom: 6px;
}
.ap-section-desc{
  color: var(--text-dim);
  font-size: 14.5px;
  line-height: 1.6;
  max-width: 680px;
  margin-bottom: 30px;
}

/* ---- Commodity cards ---- */
.ap-card{
  background: var(--surface);
  border: 1px solid var(--border-soft);
  border-radius: 14px;
  padding: 26px 24px 22px;
  height: 100%;
  position: relative;
  transition: transform .25s ease, border-color .25s ease;
}
.ap-card:hover{
  transform: translateY(-3px);
  border-color: var(--accent-color, var(--border));
}
.ap-card-top{
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  margin-bottom: 18px;
}
.ap-card-icon{
  width: 42px; height: 42px;
  border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  font-size: 20px;
  background: var(--accent-bg);
}
/* ---- Stamp badge: signature element ---- */
.ap-stamp{
  font-family: var(--font-mono);
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--accent-color);
  border: 1.5px dashed var(--accent-color);
  border-radius: 999px;
  padding: 5px 11px;
  transform: rotate(-4deg);
  white-space: nowrap;
  opacity: 0.85;
}
.ap-card-name{
  font-family: var(--font-display);
  font-weight: 600;
  font-size: 20px;
  color: var(--text);
  margin-bottom: 2px;
}
.ap-card-status{
  font-family: var(--font-mono);
  font-size: 13px;
  color: var(--accent-color);
  margin-bottom: 14px;
}
.ap-card-meta{
  font-family: var(--font-mono);
  font-size: 12px;
  color: var(--text-faint);
  margin-bottom: 14px;
  padding-bottom: 14px;
  border-bottom: 1px solid var(--border-soft);
}
.ap-card-caption{
  font-size: 13.5px;
  line-height: 1.6;
  color: var(--text-dim);
}

/* ---- Footer CTA ---- */
.ap-cta{
  background: var(--surface);
  border: 1px solid var(--border-soft);
  border-left: 3px solid var(--pinang);
  border-radius: 10px;
  padding: 18px 22px;
  font-size: 14.5px;
  color: var(--text-dim);
  margin-top: 8px;
}
.ap-cta b{ color: var(--text); }

@media (prefers-reduced-motion: reduce){
  *{ animation: none !important; transition: none !important; }
}
</style>
""", unsafe_allow_html=True)

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