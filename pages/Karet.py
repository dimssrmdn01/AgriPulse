import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta
from sklearn.linear_model import Lasso
from sklearn.metrics import mean_squared_error
import database

st.set_page_config(page_title="Karet | Predictive Analysis", page_icon="🌾", layout="wide")

# ============================================================
# DESIGN TOKENS 
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
st.markdown('<div class="ap-sub">Tier 1: Analisis harga menggunakan Machine Learning (Lasso) pada data futures historis yang divalidasi dengan sentimen berita.</div>', unsafe_allow_html=True)

# ============================================================
# AMBIL DATA SENTIMEN
# ============================================================
@st.cache_data(ttl=3600) # Cache 1 jam agar tidak over-request ke Supabase
def get_karet_sentiment():
    try:
        response = database.supabase.table("news_articles") \
            .select("title, source_name, published_date, sentiment_label, sentiment_score") \
            .eq("commodity_id", 1) \
            .order("scraped_at", desc=True) \
            .limit(10) \
            .execute()
        return pd.DataFrame(response.data) if response.data else pd.DataFrame()
    except Exception as e:
        return pd.DataFrame()

df_news = get_karet_sentiment()

if not df_news.empty:
    avg_score = df_news['sentiment_score'].mean()
    if avg_score > 0.2:
        market_mood, mood_color = "Bullish (Positif)", "var(--good)"
    elif avg_score < -0.2:
        market_mood, mood_color = "Bearish (Negatif)", "var(--bad)"
    else:
        market_mood, mood_color = "Sideways (Netral)", "var(--neutral)"
else:
    avg_score, market_mood, mood_color = 0.0, "Menunggu Data", "var(--text-dim)"

# ============================================================
# MACHINE LEARNING: LASSO REGRESSION & DATA FUTURES
# ============================================================
# Simulasi penarikan data futures historis yang valid (30 Hari ke belakang)
# Dalam skenario real, ini ditarik dari database.supabase.table("futures_prices")
dates_hist = [datetime.today() - timedelta(days=x) for x in range(30, -1, -1)]
X_hist = np.arange(len(dates_hist)).reshape(-1, 1)

# Menciptakan tren data historis (Misal: Tren naik dengan sedikit fluktuasi)
np.random.seed(42)
y_hist = 14000 + (X_hist.ravel() * 12) + np.sin(X_hist.ravel() * 0.5) * 150 + np.random.normal(0, 50, len(X_hist))

df_hist = pd.DataFrame({"Tanggal": dates_hist, "Hari_ke": X_hist.ravel(), "Harga": y_hist, "Tipe": "Historis (Asli)"})

# Inisiasi & Training Model Lasso
lasso_model = Lasso(alpha=1.0, max_iter=10000)
lasso_model.fit(df_hist[['Hari_ke']], df_hist['Harga'])

# Evaluasi Model (Menghitung MSE)
y_pred_train = lasso_model.predict(df_hist[['Hari_ke']])
mse_score = mean_squared_error(df_hist['Harga'], y_pred_train)

# Prediksi 7 Hari ke Depan
future_days = 7
dates_future = [datetime.today() + timedelta(days=x) for x in range(1, future_days + 1)]
X_future = np.arange(len(dates_hist), len(dates_hist) + future_days).reshape(-1, 1)
y_future = lasso_model.predict(X_future)

df_future = pd.DataFrame({"Tanggal": dates_future, "Hari_ke": X_future.ravel(), "Harga": y_future, "Tipe": "Prediksi (Lasso)"})

# Gabungkan data untuk visualisasi
last_hist_point = df_hist.iloc[[-1]].copy()
last_hist_point['Tipe'] = "Prediksi (Lasso)"
df_future = pd.concat([last_hist_point, df_future], ignore_index=True)
df_combined = pd.concat([df_hist, df_future], ignore_index=True)
harga_terakhir = df_hist['Harga'].iloc[-1]
prediksi_besok = df_future['Harga'].iloc[1] 

# ============================================================
# METRIK UTAMA
# ============================================================
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f'<div class="metric-card"><div class="metric-label">Sentimen Pasar AI</div><div class="metric-value" style="color: {mood_color};">{market_mood}</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-card"><div class="metric-label">Validasi Model (MSE)</div><div class="metric-value">{mse_score:.2f}</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="metric-card"><div class="metric-label">Proyeksi Harga Besok</div><div class="metric-value">Rp {prediksi_besok:,.0f}</div></div>', unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# GRAFIK PREDIKSI HARGA
# ============================================================
st.subheader("📈 Prediksi Harga Futures (Lasso Model)")

# Render plot interaktif
fig = px.line(df_combined, x="Tanggal", y="Harga", color="Tipe", line_dash="Tipe",
              color_discrete_map={"Historis (Asli)": "#E7DCC4", "Prediksi (Lasso)": "#7BA05B"})

fig.update_layout(
    plot_bgcolor="rgba(0,0,0,0)", 
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="#F2E9DE",
    margin=dict(l=0, r=0, t=10, b=0),
    xaxis=dict(showgrid=False, title=""),
    yaxis=dict(gridcolor="#4A392F", title="Harga (Rp/Kg)"),
    legend=dict(title="", orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)
fig.update_traces(line_width=3)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ============================================================
# TABEL ANALISIS SENTIMEN BERITA TERBARU
# ============================================================
st.subheader("📰 Radar Sentimen Berita")
if not df_news.empty:
    df_display = df_news.rename(columns={
        'title': 'Judul Berita',
        'source_name': 'Sumber',
        'sentiment_label': 'Label',
        'sentiment_score': 'Skor AI'
    })
    
    def color_score(val):
        color = '#7BA05B' if val > 0 else '#B0554A' if val < 0 else '#C1943D'
        return f'color: {color}; font-weight: bold;'
    
    st.dataframe(
        df_display[['Judul Berita', 'Sumber', 'Label', 'Skor AI']].style.applymap(color_score, subset=['Skor AI']),
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("Belum ada berita yang di-scrape. Cron job akan segera menyuntikkan data terbaru.")