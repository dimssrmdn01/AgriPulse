import streamlit as st
import pandas as pd
import plotly.express as px
import database
import style

st.set_page_config(page_title="Pinang | Trend Indicator", page_icon="🌰", layout="wide")
style.apply_design_tokens()

# ============================================================
# HEADER
# ============================================================
st.markdown('<div class="ap-header">🌰 Tren Ekspor <span class="ap-highlight" style="color: var(--pinang);">Pinang</span></div>', unsafe_allow_html=True)
st.markdown('<div class="ap-sub">Tier 2: Indikator arah pergerakan pasar berdasarkan dinamika volume ekspor tahunan dan sentimen perdagangan global.</div>', unsafe_allow_html=True)

# ============================================================
# AMBIL DATA SENTIMEN
# ============================================================
def get_pinang_sentiment():
    response = database.supabase.table("news_articles") \
        .select("title, source_name, published_date, sentiment_label, sentiment_score") \
        .eq("commodity_id", 2) \
        .order("scraped_at", desc=True) \
        .limit(10) \
        .execute()
    
    if response.data:
        return pd.DataFrame(response.data)
    else:
        return pd.DataFrame()

df_news = get_pinang_sentiment()

if not df_news.empty:
    avg_score = df_news['sentiment_score'].mean()
    if avg_score > 0.15:
        market_mood = "Tren Menguat 📈"
        mood_color = "var(--good)"
    elif avg_score < -0.15:
        market_mood = "Tren Melemah 📉"
        mood_color = "var(--bad)"
    else:
        market_mood = "Tren Stabil ➖"
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
    st.markdown(f'<div class="metric-card"><div class="metric-label">Indikator Tren AI</div><div class="metric-value" style="color: {mood_color};">{market_mood}</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-card"><div class="metric-label">Sentimen Berita Ekspor</div><div class="metric-value">{avg_score:+.2f}</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="metric-card"><div class="metric-label">Est. Harga FOB (BPS)</div><div class="metric-value">Rp 12.800 / Kg</div></div>', unsafe_allow_html=True)

st.markdown('<hr class="ap-divider">', unsafe_allow_html=True)

# ============================================================
# GRAFIK HISTORI TAHUNAN (SIMULASI DATA BPS/FOB)
# ============================================================
st.markdown('<div class="ap-section-title">📊 Histori Harga Ekspor (FOB) 5 Tahun Terakhir</div>', unsafe_allow_html=True)
st.write("Data harga pinang memiliki volatilitas tinggi antar musim panen. Grafik di bawah merepresentasikan rata-rata harga Free On Board (FOB) tahunan.")

data_tahun = ["2022", "2023", "2024", "2025", "2026 (YTD)"]
data_harga = [14200, 8500, 9200, 11500, 12800]

df_fob = pd.DataFrame({"Tahun": data_tahun, "Harga Rata-rata (Rp/Kg)": data_harga})

fig = px.bar(df_fob, x="Tahun", y="Harga Rata-rata (Rp/Kg)", text="Harga Rata-rata (Rp/Kg)")
fig.update_traces(texttemplate='Rp %{text:,.0f}', textposition='outside', marker_color='#C1622D')
fig.update_layout(
    plot_bgcolor="rgba(0,0,0,0)", 
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="#F2E9DE",
    margin=dict(l=0, r=0, t=30, b=0),
    yaxis=dict(showgrid=True, gridcolor="#4A392F", range=[0, 18000]),
    xaxis=dict(showgrid=False)
)
st.plotly_chart(fig, use_container_width=True)

st.markdown('<hr class="ap-divider">', unsafe_allow_html=True)

# ============================================================
# TABEL ANALISIS SENTIMEN BERITA TERBARU
# ============================================================
st.markdown('<div class="ap-section-title">📰 Radar Sentimen Ekspor</div>', unsafe_allow_html=True)
if not df_news.empty:
    df_display = df_news.copy()
    
    def color_score(val):
        color = '#7BA05B' if val > 0 else '#B0554A' if val < 0 else '#C1943D'
        return f'color: {color}; font-weight: bold;'
    
    df_display = df_display.rename(columns={
        'title': 'Judul Berita',
        'source_name': 'Sumber',
        'sentiment_label': 'Label',
        'sentiment_score': 'Skor AI'
    })
    
    st.dataframe(
        df_display[['Judul Berita', 'Sumber', 'Label', 'Skor AI']].style.map(color_score, subset=['Skor AI']),
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("Belum ada berita yang di-scrape. Jalankan scraper.py terlebih dahulu.")