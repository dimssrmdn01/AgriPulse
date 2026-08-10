import streamlit as st
import pandas as pd
import database  # Mengambil koneksi dari file database.py

st.set_page_config(page_title="Gambir | Log Komunitas", page_icon="🍃", layout="wide")

# ============================================================
# DESIGN TOKENS (senada dengan Home — jangan diubah sendiri-sendiri
# di tiap halaman; idealnya ini nanti dipindah ke satu file
# style.py/components.py yang di-import bersama supaya tidak drift)
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

  --gambir: #A34A3A;
  --gambir-bg: rgba(163,74,58,0.12);
  --good: #7BA05B;
  --good-bg: rgba(123,160,91,0.12);
  --pending: #C1943D;
  --pending-bg: rgba(193,148,61,0.12);
  --bad: #B0554A;
  --bad-bg: rgba(176,85,74,0.10);

  --font-display: 'Fraunces', Georgia, serif;
  --font-sans: 'IBM Plex Sans', sans-serif;
  --font-mono: 'IBM Plex Mono', monospace;
}

.stApp{ background: var(--bg); color: var(--text); font-family: var(--font-sans); }
.block-container{ padding-top: 2.5rem; max-width: 1100px; }
section[data-testid="stSidebar"]{ background: var(--bg-soft); border-right: 1px solid var(--border-soft); }

/* ---- Header ---- */
.ap-eyebrow{
  font-family: var(--font-mono); font-size: 12px; letter-spacing: 0.16em;
  text-transform: uppercase; color: var(--gambir); margin-bottom: 12px;
}
.ap-header{
  font-family: var(--font-display); font-weight: 600; font-size: 38px;
  color: var(--text); margin-bottom: 10px; line-height: 1.1;
}
.ap-header em{ font-style: italic; color: var(--gambir); }
.ap-sub{ font-size: 15.5px; color: var(--text-dim); line-height: 1.65; max-width: 680px; margin-bottom: 8px; }

.ap-divider{ border: none; border-top: 1px solid var(--border-soft); margin: 30px 0; }

.ap-section-label{
  font-family: var(--font-mono); font-size: 12px; letter-spacing: 0.14em;
  text-transform: uppercase; color: var(--text-faint); margin-bottom: 6px;
}
.ap-section-title{
  font-family: var(--font-display); font-weight: 600; font-size: 21px;
  color: var(--text); margin-bottom: 18px;
}

/* ---- Stat strip ---- */
.ap-stat{
  background: var(--surface); border: 1px solid var(--border-soft);
  border-radius: 12px; padding: 16px 18px; height: 100%;
}
.ap-stat-label{
  font-family: var(--font-mono); font-size: 11px; letter-spacing: 0.08em;
  text-transform: uppercase; color: var(--text-faint); margin-bottom: 8px;
}
.ap-stat-value{
  font-family: var(--font-mono); font-size: 24px; font-weight: 600; color: var(--text);
}
.ap-stat-value.accent{ color: var(--gambir); }

/* ---- Form card ---- */
div[data-testid="stForm"]{
  background: var(--surface);
  border: 1px solid var(--border-soft);
  border-radius: 14px;
  padding: 8px 6px 4px;
}
div[data-testid="stForm"] label p{ color: var(--text-dim) !important; font-size: 13.5px; }
div[data-testid="stForm"] input,
div[data-testid="stForm"] textarea,
div[data-testid="stForm"] div[data-baseweb="select"] > div{
  background: var(--bg-soft) !important;
  border-color: var(--border) !important;
  color: var(--text) !important;
  border-radius: 8px !important;
}
div[data-testid="stFormSubmitButton"] button{
  background: var(--gambir) !important;
  color: var(--bg) !important;
  border: none !important;
  border-radius: 8px !important;
  font-weight: 600 !important;
  width: 100%;
}
div[data-testid="stFormSubmitButton"] button:hover{ opacity: 0.9; }

/* ---- Custom alert boxes (ganti st.success/st.error default) ---- */
.ap-alert{
  border-radius: 10px; padding: 12px 16px; font-size: 14px;
  margin-top: 10px; border-left: 3px solid;
}
.ap-alert.ok{ background: var(--good-bg); border-color: var(--good); color: var(--text); }
.ap-alert.err{ background: var(--bad-bg); border-color: var(--bad); color: var(--text); }

/* ---- Ledger / log entries ---- */
.ap-empty{
  background: var(--surface); border: 1px dashed var(--border);
  border-radius: 12px; padding: 28px; text-align: center;
  color: var(--text-dim); font-size: 14px;
}
.ap-log-entry{
  display: flex; align-items: center; gap: 16px;
  padding: 14px 4px; border-bottom: 1px solid var(--border-soft);
}
.ap-log-entry:last-child{ border-bottom: none; }
.ap-log-price{
  font-family: var(--font-mono); font-weight: 600; font-size: 17px;
  color: var(--text); min-width: 118px;
}
.ap-log-meta{ flex: 1; min-width: 0; }
.ap-log-region{ font-size: 14.5px; color: var(--text); font-weight: 500; }
.ap-log-note{ font-size: 12.5px; color: var(--text-faint); margin-top: 2px; }
.ap-log-time{
  font-family: var(--font-mono); font-size: 11.5px; color: var(--text-faint);
  white-space: nowrap;
}
.ap-badge{
  font-family: var(--font-mono); font-size: 10.5px; font-weight: 600;
  letter-spacing: 0.04em; text-transform: uppercase;
  padding: 4px 10px; border-radius: 999px; white-space: nowrap;
  border: 1px solid transparent;
}
.ap-badge.approved{ background: var(--good-bg); color: var(--good); border-color: var(--good); }
.ap-badge.pending{ background: var(--pending-bg); color: var(--pending); border-color: var(--pending); }
.ap-badge.rejected{ background: var(--bad-bg); color: var(--bad); border-color: var(--bad); }
</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================
st.markdown('<div class="ap-eyebrow">Tier 3 · Data Komunitas</div>', unsafe_allow_html=True)
st.markdown('<div class="ap-header">Log Harga <em>Gambir</em></div>', unsafe_allow_html=True)
st.markdown(
    '<div class="ap-sub">Belum ada data harga gambir yang terstruktur secara nasional — jadi kita bangun sendiri. '
    'Masukkan harga jual/beli yang kamu lihat hari ini di lapangan, dan bantu bangun transparansi harga '
    'bareng-bareng untuk petani dan pengepul lain.</div>',
    unsafe_allow_html=True
)

# ============================================================
# DATA (dimuat lebih awal supaya bisa dipakai di ringkasan statistik)
# ============================================================
def load_data():
    response = database.supabase.table("crowdsource_submissions") \
        .select("*") \
        .eq("commodity_id", 3) \
        .order("submission_date", desc=True) \
        .limit(50) \
        .execute()
    
    if response.data:
        return pd.DataFrame(response.data)
    else:
        return pd.DataFrame() # Return dataframe kosong jika belum ada data

df_raw = load_data()

# ---- Ringkasan statistik singkat ----
if not df_raw.empty:
    total_laporan = len(df_raw)
    harga_median = df_raw['submitted_price'].median()
    lokasi_teraktif = df_raw['region'].mode().iloc[0] if not df_raw['region'].mode().empty else "-"
else:
    total_laporan, harga_median, lokasi_teraktif = 0, None, "-"

s1, s2, s3 = st.columns(3)
with s1:
    st.markdown(f"""
    <div class="ap-stat">
      <div class="ap-stat-label">Total Laporan</div>
      <div class="ap-stat-value">{total_laporan}</div>
    </div>""", unsafe_allow_html=True)
with s2:
    harga_display = f"Rp {harga_median:,.0f}".replace(',', '.') if harga_median else "—"
    st.markdown(f"""
    <div class="ap-stat">
      <div class="ap-stat-label">Median Harga Terlapor</div>
      <div class="ap-stat-value accent">{harga_display}</div>
    </div>""", unsafe_allow_html=True)
with s3:
    st.markdown(f"""
    <div class="ap-stat">
      <div class="ap-stat-label">Lokasi Teraktif</div>
      <div class="ap-stat-value" style="font-size:17px;">{lokasi_teraktif}</div>
    </div>""", unsafe_allow_html=True)

st.markdown('<hr class="ap-divider">', unsafe_allow_html=True)

# ============================================================
# FORM INPUT CROWDSOURCING
# ============================================================
st.markdown('<div class="ap-section-label">Kontribusi Data</div>', unsafe_allow_html=True)
st.markdown('<div class="ap-section-title">📝 Laporkan Harga Lapangan</div>', unsafe_allow_html=True)

with st.form("form_gambir", clear_on_submit=True):
    col1, col2 = st.columns(2)

    with col1:
        harga = st.number_input("Harga per Kg (Rp)", min_value=0, step=1000, placeholder="Contoh: 35000")
        lokasi = st.text_input("Lokasi (Desa/Kecamatan)", placeholder="Contoh: Pangkalan Koto Baru")

    with col2:
        kualitas = st.selectbox("Kualitas/Kondisi", ["Kering (Kualitas Ekspor)", "Kering Biasa", "Basah", "Campuran"])
        catatan = st.text_input("Catatan Tambahan (Opsional)", placeholder="Misal: Pengepul besar lagi tutup")

    submitted = st.form_submit_button("Kirim Laporan Harga")

    if submitted:
        if harga > 1000 and lokasi:
            try:
                # Insert data langsung ke Supabase Cloud
                database.supabase.table("crowdsource_submissions").insert({
                    "commodity_id": 3,
                    "submitted_price": harga,
                    "region": lokasi,
                    "submitter_note": f"[{kualitas}] {catatan}"
                }).execute()
                
                st.markdown(
                    '<div class="ap-alert ok">✅ Mantap! Laporan hargamu berhasil masuk ke database komunitas (Cloud).</div>',
                    unsafe_allow_html=True
                )
            except Exception as e:
                st.markdown(
                    f'<div class="ap-alert err">⚠️ Gagal menyimpan ke cloud: {e}</div>',
                    unsafe_allow_html=True
                )
        else:
            st.markdown(
                '<div class="ap-alert err">⚠️ Pastikan nominal harga wajar dan lokasi sudah diisi ya!</div>',
                unsafe_allow_html=True
            )

st.markdown('<hr class="ap-divider">', unsafe_allow_html=True)

# ============================================================
# LOG HISTORI — ditampilkan sebagai "buku catatan", bukan tabel biasa
# ============================================================
st.markdown('<div class="ap-section-label">Riwayat</div>', unsafe_allow_html=True)
st.markdown('<div class="ap-section-title">📖 Log Laporan Komunitas</div>', unsafe_allow_html=True)

STATUS_LABEL = {
    "approved": ("Tervalidasi", "approved"),
    "pending": ("Menunggu Verifikasi", "pending"),
    "rejected": ("Ditolak", "rejected"),
}

if not df_raw.empty:
    df_view = df_raw.copy()
    df_view['submission_date'] = pd.to_datetime(df_view['submission_date']).dt.strftime('%d %b %Y, %H:%M')

    entries_html = []
    for _, row in df_view.iterrows():
        harga_fmt = f"Rp {row['submitted_price']:,.0f}".replace(',', '.')
        label, cls = STATUS_LABEL.get(row['status'], ("Menunggu Verifikasi", "pending"))
        note = row['submitter_note'] if row['submitter_note'] else "—"
        entries_html.append(f"""
        <div class="ap-log-entry">
          <div class="ap-log-price">{harga_fmt}</div>
          <div class="ap-log-meta">
            <div class="ap-log-region">{row['region']}</div>
            <div class="ap-log-note">{note}</div>
          </div>
          <div class="ap-badge {cls}">{label}</div>
          <div class="ap-log-time">{row['submission_date']}</div>
        </div>
        """)

    st.markdown(f'<div>{"".join(entries_html)}</div>', unsafe_allow_html=True)

    with st.expander("Lihat sebagai tabel mentah (untuk export/analisis)"):
        df_table = df_view.rename(columns={
            'submission_date': 'Waktu Lapor',
            'submitted_price': 'Harga (Rp/Kg)',
            'region': 'Lokasi',
            'submitter_note': 'Kualitas & Catatan',
            'status': 'Status Validasi'
        })
        st.dataframe(df_table, use_container_width=True, hide_index=True)
else:
    st.markdown("""
    <div class="ap-empty">
      Belum ada data harga yang dilaporkan.<br>
      <b>Yuk, jadi yang pertama menyumbang data hari ini!</b>
    </div>
    """, unsafe_allow_html=True)