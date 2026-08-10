import streamlit as st
from supabase import create_client
import os

# Coba ambil dari st.secrets (untuk Streamlit Cloud), 
# jika gagal, ambil dari os.environ (untuk lokal)
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
except (KeyError, FileNotFoundError):
    # Fallback untuk penggunaan lokal jika pakai dotenv
    from dotenv import load_dotenv
    load_dotenv()
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")

if not url or not key:
    raise ValueError("⚠️ SUPABASE_URL atau SUPABASE_KEY tidak ditemukan!")

# Inisialisasi client Supabase
supabase = create_client(url, key)