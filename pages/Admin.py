import streamlit as st
import pandas as pd
import database
import style

st.set_page_config(page_title="Admin | Moderasi Gambir", page_icon="🔐", layout="wide")
style.apply_design_tokens()

# ============================================================
# SISTEM LOGIN SEDERHANA
# ============================================================
def check_password():
    """Mengembalikan `True` jika user punya password yang benar."""
    def password_entered():
        if st.session_state["password"] == st.secrets["ADMIN_PASS"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.markdown('<div class="ap-header">🔐 Area Terbatas</div>', unsafe_allow_html=True)
        st.text_input("Masukkan Password Admin:", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.markdown('<div class="ap-header">🔐 Area Terbatas</div>', unsafe_allow_html=True)
        st.text_input("Masukkan Password Admin:", type="password", on_change=password_entered, key="password")
        st.error("⚠️ Password salah!")
        return False
    return True

if check_password():
    # ============================================================
    # DASHBOARD MODERASI
    # ============================================================
    st.markdown('<div class="ap-header">🛡️ Panel Moderasi Data <span style="color: var(--gambir);">Gambir</span></div>', unsafe_allow_html=True)
    st.markdown('<div class="ap-sub">Review laporan harga dari komunitas sebelum dipublikasikan untuk menghitung median harga nasional.</div>', unsafe_allow_html=True)
    st.markdown('<hr class="ap-divider">', unsafe_allow_html=True)

    response = database.supabase.table("crowdsource_submissions") \
        .select("*") \
        .eq("commodity_id", 3) \
        .eq("status", "pending") \
        .order("submission_date", desc=True) \
        .execute()
    
    df_pending = pd.DataFrame(response.data) if response.data else pd.DataFrame()

    if not df_pending.empty:
        st.markdown(f'<div class="ap-section-title">Tertunda ({len(df_pending)} Laporan)</div>', unsafe_allow_html=True)
        
        for idx, row in df_pending.iterrows():
            with st.container():
                col1, col2, col3 = st.columns([4, 1, 1])
                
                with col1:
                    harga_fmt = f"Rp {row['submitted_price']:,.0f}".replace(',', '.')
                    st.markdown(f"""
                    <div style="background: var(--surface); padding: 15px; border-radius: 8px; border: 1px solid var(--border-soft);">
                        <strong style="font-size: 18px; color: var(--text);">{harga_fmt}</strong> &mdash; <span style="color: var(--text-dim);">{row['region']}</span><br>
                        <span style="font-size: 13px; color: var(--text-faint);">Catatan: {row['submitter_note']}</span>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    if st.button("✅ Approve", key=f"app_{row['id']}", use_container_width=True):
                        database.supabase.table("crowdsource_submissions").update({"status": "approved"}).eq("id", row['id']).execute()
                        st.rerun()
                
                with col3:
                    if st.button("❌ Reject", key=f"rej_{row['id']}", use_container_width=True):
                        database.supabase.table("crowdsource_submissions").update({"status": "rejected"}).eq("id", row['id']).execute()
                        st.rerun()
                st.markdown("<br>", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="ap-empty">
             Mantap! Tidak ada laporan harga yang butuh direview saat ini.<br>
            Semua data sudah tervalidasi.
        </div>
        """, unsafe_allow_html=True)
