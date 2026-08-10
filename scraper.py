import os
import time
from datetime import datetime
from email.utils import parsedate_to_datetime
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

import database

# ============================================================
# 1. Setup API Key & LLM (Groq)
# ============================================================
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    print(" Peringatan: GROQ_API_KEY tidak ditemukan di .env!")

llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0)

prompt = PromptTemplate.from_template(
    """Kamu adalah analis pasar komoditas. Baca judul dan cuplikan berita ini,
    lalu tentukan sentimen pasarnya terhadap harga komoditas.

    Balas HANYA dalam format persis seperti ini, tanpa penjelasan tambahan:
    Label: <Positif/Negatif/Netral>
    Skor: <angka antara -1.0 sampai 1.0>

    Judul Berita: {title}
    Cuplikan: {description}
    """
)
sentiment_chain = prompt | llm

KOMODITAS_MAP = {
    1: "Harga Karet Dunia OR Ekspor Karet Indonesia",
    2: "Ekspor Pinang OR Harga Pinang Indonesia",
    3: "Harga Gambir OR Ekspor Gambir Sumbar OR Petani Gambir",
}

REQUEST_HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; AgriPulseBot/1.0)"}


def fetch_news(keyword, limit=5):
    """Mengambil berita terbaru dari Google News RSS untuk satu keyword."""
    print(f"\n Mencari berita untuk: {keyword}...")
    url = f"https://news.google.com/rss/search?q={quote(keyword)}&hl=id&gl=ID&ceid=ID:id"

    try:
        response = requests.get(url, timeout=10, headers=REQUEST_HEADERS)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f" Gagal mengambil RSS untuk '{keyword}': {e}")
        return []

    try:
        soup = BeautifulSoup(response.content, features="xml")
    except Exception as e:
        print(f" Gagal parsing RSS untuk '{keyword}': {e}")
        return []

    articles = soup.find_all("item")
    results = []

    for a in articles[:limit]:
        title = a.title.text if a.title else None
        link = a.link.text if a.link else None
        if not title or not link:
            continue  

        source = a.source.text if a.source else "Tidak diketahui"
        pub_date_raw = a.pubDate.text if a.pubDate else None
        description = a.description.text if a.description else ""

        try:
            pub_date = parsedate_to_datetime(pub_date_raw).strftime("%Y-%m-%d %H:%M:%S")
        except Exception:
            pub_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        results.append({
            "title": title,
            "url": link,
            "source": source,
            "pub_date": pub_date,
            "description": description,
        })

    return results


def analyze_sentiment(title, description):
    """Minta LLM balas label + skor sentimen. Fallback ke Netral/0.0 kalau gagal."""
    try:
        response = sentiment_chain.invoke({"title": title, "description": description})
        text = response.content.strip()

        label = "Netral"
        score = 0.0

        for line in text.splitlines():
            line = line.strip()
            if line.lower().startswith("label:"):
                candidate = line.split(":", 1)[1].strip().title()
                if candidate in ["Positif", "Negatif", "Netral"]:
                    label = candidate
            elif line.lower().startswith("skor:"):
                try:
                    score = float(line.split(":", 1)[1].strip())
                    score = max(-1.0, min(1.0, score))  # clamp ke -1..1
                except ValueError:
                    pass

        return label, score

    except Exception as e:
        print(f"Error AI, fallback ke Netral: {e}")
        return "Netral", 0.0


def process_and_save_news():
    """Mengambil berita, menganalisis sentimen, dan menyimpan ke Supabase Cloud."""
    # database.py sekarang menggunakan Supabase, bukan lagi SQLite
    
    for comm_id, keyword in KOMODITAS_MAP.items():
        try:
            news_list = fetch_news(keyword)
        except Exception as e:
            print(f"❌ Melewati komoditas id={comm_id} karena error: {e}")
            continue

        for news in news_list:
            # 1. Cek duplikat ke Supabase berdasarkan URL
            check = database.supabase.table("news_articles").select("id").eq("url", news["url"]).execute()
            if len(check.data) > 0:
                continue # Skip jika berita sudah ada di Cloud

            # 2. Analisis Sentimen
            sentiment_label, sentiment_score = analyze_sentiment(
                news["title"], news["description"]
            )

            # 3. Insert data ke Supabase Cloud
            try:
                database.supabase.table("news_articles").insert({
                    "commodity_id": comm_id,
                    "title": news["title"],
                    "url": news["url"],
                    "source_name": news["source"],
                    "published_date": news["pub_date"],
                    "sentiment_label": sentiment_label,
                    "sentiment_score": sentiment_score,
                    "summary": news["description"][:500]
                }).execute()
                print(f"☁️ Tersimpan di Cloud [{sentiment_label} / {sentiment_score:+.1f}]: {news['title']}")
            except Exception as e:
                print(f"⚠️ Gagal menyimpan ke Cloud: {e}")

        time.sleep(1.5) 
        
    print("\n🎉 Scraping dan Injeksi Sentimen ke Cloud Selesai!")

if __name__ == "__main__":
    process_and_save_news()