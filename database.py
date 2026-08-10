import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Muat variabel dari .env
load_dotenv()

# Ambil kunci dari environment
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")

if not url or not key:
    raise ValueError("⚠️ SUPABASE_URL atau SUPABASE_KEY tidak ditemukan di .env!")

# Inisialisasi koneksi ke Supabase Cloud
supabase: Client = create_client(url, key)