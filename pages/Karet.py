import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta
import database

st.set_page_config(page_title="Karet | Predictive Analysis", page_icon="🌾", layout="wide")

# ============================================================
# DESIGN TOKENS (Senada dengan Home)
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600&family=IBM+Plex+Sans:wght@400;500;600&display=swap');

:root{
  --bg: #211814;
  --surface: #2C221C;
  --border-soft: rgba(242,233,222,0.10);
  --text: #F2E9DE;
  --text-dim: #B8A793;
  --karet: #E7DCC4;
  
  --good: #7BA05B;
  --bad: #B0554A;
  --neutral: #C1943D;
  
  --font-display: 'Fraunces', serif;
  --font-sans: 'IBM Plex Sans', sans-serif;
}

.stApp { background: var(--bg); color: var(--text); font-family: var(--font-sans); }
.ap-header { font-family: var(--font-display); font-size: 36px; color: var(--text); font-weight: 600; margin-bottom: 8px; }
.ap-sub { font-size: 16px; color: var(--text-dim); line-height: 1.6; margin-bottom: 32px; }
.ap-highlight { color: var(--karet); font-style: italic; }

.metric-card {
    background: var(--surface);
    border: 1px solid var(--border-soft);
    border-radius: 12px;
    padding: 20px;
    text-align: center;
}
.metric-value { font-size: 28px; font-weight: 600; font-family: var(--font-display); color: var(--text); }
.metric-label { font-size: 12px; color: var(--text-dim); text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px;}
</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================
st.markdown('<div class="ap-header">🌾 Prediksi Harga <span class="ap-highlight">Karet</span></div>', unsafe_allow_html=True)
st.markdown('<div class="ap-sub">Tier 1: Analisis harga menggunakan gabungan pergerakan harga futures global (SICOM) dan sentimen berita terkini.</div>', unsafe_allow_html=True)

# ============================================================
# AMBIL DATA SENTIMEN DARI DATABASE
# ============================================================
def get_karet_sentiment():
    # Menarik berita Karet (commodity_id = 1) dari Supabase Cloud
    response = database.supabase.table("news_articles") \
        .select("title, source_name, published_date, sentiment_label, sentiment_score") \
        .eq("commodity_id", 1) \
        .order("scraped_at", desc=True) \
        .limit(10) \
        .execute()
    
    if response.data:
        return pd.DataFrame(response.data)
    else:
        return pd.DataFrame()

df_news = get_karet_sentiment()

# Hitung Rata-rata Skor Sentimen
if not df_news.empty:
    avg_score = df_news['sentiment_score'].mean()
    if avg_score > 0.2:
        market_mood = "Bullish (Positif)"
        mood_color = "var(--good)"
    elif avg_score < -0.2:
        market_mood = "Bearish (Negatif)"
        mood_color = "var(--bad)"
    else:
        market_mood = "Sideways (Netral)"
        mood_color = "var(--neutral)"
else:
    avg_score = 0.0
    market_mood = "Menunggu Data"
    mood_color = "var(--text-dim)"

# ============================================================
# METRIK UTAMA
# ============================================================
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f'<div class="metric-card"><div class="metric-label">Sentimen Pasar AI</div><div class="metric-value" style="color: {mood_color};">{market_mood}</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-card"><div class="metric-label">Rata-rata Skor Berita</div><div class="metric-value">{avg_score:+.2f}</div></div>', unsafe_allow_html=True)
with col3:
    # Simulasi harga penutupan futures
    st.markdown('<div class="metric-card"><div class="metric-label">Harga Futures (Simulasi)</div><div class="metric-value">Rp 14.250 / Kg</div></div>', unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# GRAFIK HISTORI HARGA (SIMULASI UNTUK UI)
# ============================================================
st.subheader("📈 Tren Harga Futures (30 Hari Terakhir)")
# Karena kita belum punya API finance berbayar, kita generate dummy data yang realistis
dates = [datetime.today() - timedelta(days=x) for x in range(30, 0, -1)]
# Membuat tren harga yang fluktuatif di kisaran 13.000 - 15.000
np.random.seed(42)
prices = 14000 + np.random.randn(30).cumsum() * 150 

df_price = pd.DataFrame({"Tanggal": dates, "Harga (Rp)": prices})

fig = px.line(df_price, x="Tanggal", y="Harga (Rp)", line_shape="spline")
fig.update_layout(
    plot_bgcolor="rgba(0,0,0,0)", 
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="#F2E9DE",
    margin=dict(l=0, r=0, t=10, b=0),
    xaxis=dict(showgrid=False),
    yaxis=dict(gridcolor="#4A392F")
)
fig.update_traces(line_color="#E7DCC4", line_width=3)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ============================================================
# TABEL ANALISIS SENTIMEN BERITA TERBARU
# ============================================================
st.subheader("📰 Radar Sentimen Berita")
if not df_news.empty:
    # Memformat tabel agar lebih rapi
    df_display = df_news.copy()
    
    # Fungsi warna untuk skor
    def color_score(val):
        color = '#7BA05B' if val > 0 else '#B0554A' if val < 0 else '#C1943D'
        return f'color: {color}; font-weight: bold;'
    
    df_display = df_display.rename(columns={
        'title': 'Judul Berita',
        'source_name': 'Sumber',
        'sentiment_label': 'Label',
        'sentiment_score': 'Skor AI'
    })
    
    # Menampilkan tabel interaktif di Streamlit
    st.dataframe(
        df_display[['Judul Berita', 'Sumber', 'Label', 'Skor AI']].style.applymap(color_score, subset=['Skor AI']),
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("Belum ada berita yang di-scrape. Jalankan scraper.py terlebih dahulu.")