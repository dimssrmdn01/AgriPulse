import streamlit as st
import pandas as pd
import database
import style

st.set_page_config(page_title="Gambir | Log Komunitas", page_icon="🍃", layout="wide")
style.apply_design_tokens()

# ============================================================
# HEADER
# ============================================================
st.markdown('<div class="ap-eyebrow">Tier 3 · Data Komunitas</div>', unsafe_allow_html=True)
st.markdown('<div class="ap-header">Log Harga <em style="color: var(--gambir);">Gambir</em></div>', unsafe_allow_html=True)
st.markdown(
    '<div class="ap-sub">Belum ada data harga gambir yang terstruktur secara nasional — jadi kita bangun sendiri. '
    'Masukkan harga jual/beli yang kamu lihat hari ini di lapangan, dan bantu bangun transparansi harga '
    'bareng-bareng untuk petani dan pengepul lain.</div>',
    unsafe_allow_html=True
)

# ============================================================
# DATA
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
        return pd.DataFrame() 

df_raw = load_data()

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
# LOG HISTORI
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