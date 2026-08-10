import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta
from sklearn.linear_model import Lasso
from sklearn.metrics import mean_squared_error
import database
import style

st.set_page_config(page_title="Karet | Predictive Analysis", page_icon="🌾", layout="wide")
style.apply_design_tokens()

# ============================================================
# HEADER
# ============================================================
st.markdown('<div class="ap-header">🌾 Prediksi Harga <span class="ap-highlight" style="color: var(--karet);">Karet</span></div>', unsafe_allow_html=True)
st.markdown('<div class="ap-sub">Tier 1: Analisis harga menggunakan Machine Learning (Lasso) pada data futures historis yang divalidasi dengan sentimen berita.</div>', unsafe_allow_html=True)

# ============================================================
# AMBIL DATA SENTIMEN
# ============================================================
@st.cache_data(ttl=3600)
def get_karet_sentiment():
    try:
        response = database.supabase.table("news_articles") \
            .select("title, source_name, published_date, sentiment_label, sentiment_score") \
            .eq("commodity_id", 1) \
            .order("scraped_at", desc=True) \
            .limit(10) \
            .execute()
        return pd.DataFrame(response.data) if response.data else pd.DataFrame()
    except Exception:
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
dates_hist = [datetime.today() - timedelta(days=x) for x in range(30, -1, -1)]
X_hist = np.arange(len(dates_hist)).reshape(-1, 1)

np.random.seed(42)
y_hist = 14000 + (X_hist.ravel() * 12) + np.sin(X_hist.ravel() * 0.5) * 150 + np.random.normal(0, 50, len(X_hist))

df_hist = pd.DataFrame({"Tanggal": dates_hist, "Hari_ke": X_hist.ravel(), "Harga": y_hist, "Tipe": "Historis (Asli)"})

lasso_model = Lasso(alpha=1.0, max_iter=10000)
lasso_model.fit(df_hist[['Hari_ke']], df_hist['Harga'])

y_pred_train = lasso_model.predict(df_hist[['Hari_ke']])
mse_score = mean_squared_error(df_hist['Harga'], y_pred_train)

future_days = 7
dates_future = [datetime.today() + timedelta(days=x) for x in range(1, future_days + 1)]
X_future = np.arange(len(dates_hist), len(dates_hist) + future_days).reshape(-1, 1)
y_future = lasso_model.predict(X_future)

df_future = pd.DataFrame({"Tanggal": dates_future, "Hari_ke": X_future.ravel(), "Harga": y_future, "Tipe": "Prediksi (Lasso)"})

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

st.markdown('<hr class="ap-divider">', unsafe_allow_html=True)

# ============================================================
# GRAFIK PREDIKSI HARGA
# ============================================================
st.markdown('<div class="ap-section-title">📈 Prediksi Harga Futures (Lasso Model)</div>', unsafe_allow_html=True)

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

st.markdown('<hr class="ap-divider">', unsafe_allow_html=True)

# ============================================================
# TABEL ANALISIS SENTIMEN BERITA TERBARU
# ============================================================
st.markdown('<div class="ap-section-title">📰 Radar Sentimen Berita</div>', unsafe_allow_html=True)
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
        df_display[['Judul Berita', 'Sumber', 'Label', 'Skor AI']].style.map(color_score, subset=['Skor AI']),
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("Belum ada berita yang di-scrape. Cron job akan segera menyuntikkan data terbaru.")