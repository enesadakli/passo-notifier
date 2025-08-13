import time
import requests
from bs4 import BeautifulSoup
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

PASSO_URL = "https://www.passo.com.tr/tr/kategori/futbol-mac-biletleri/4615"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("Telegram gönderim hatası:", e)

def check_passo():
    try:
        r = requests.get(PASSO_URL, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        page_text = soup.get_text().lower()

        if "türkiye - ispanya" in page_text:
            print("✅ Maç sayfası bulundu.")
            send_telegram_message("✅ Türkiye - İspanya sayfası açıldı!")

            if "satın al" in page_text or "bilet al" in page_text:
                print("🎟️ Satış başladı.")
                send_telegram_message("🎟️ Türkiye - İspanya bilet satışı başladı!")
        else:
            print("Maç henüz eklenmemiş.")
    except Exception as e:
        print("Hata:", e)

if __name__ == "__main__":
    send_telegram_message("🚀 Bot çalışmaya başladı!")
    while True:
        check_passo()
        time.sleep(60)
