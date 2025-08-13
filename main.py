import time
import requests
from bs4 import BeautifulSoup
import os

# Telegram bilgilerini Railway ortam değişkenlerinden alıyoruz
BOT_TOKEN = os.getenv("BOT_TOKEN")  # Telegram Bot token
CHAT_ID = os.getenv("CHAT_ID")      # Telegram Chat ID

# Passo sayfası URL'si
PASSO_URL = "https://www.passo.com.tr/tr/kategori/futbol-mac-biletleri/4615"

# Bildirim gönderen fonksiyon
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("Telegram gönderim hatası:", e)

# Sayfayı kontrol eden fonksiyon
def check_passo():
    try:
        r = requests.get(PASSO_URL, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        page_text = soup.get_text().lower()

        # Maç sayfası var mı?
        if "türkiye - ispanya" in page_text:
            send_telegram_message("✅ Türkiye - İspanya sayfası açıldı!")
            
            # Bilet satışı başladı mı?
            if "satın al" in page_text or "bilet al" in page_text:
                send_telegram_message("🎟️ Türkiye - İspanya bilet satışı başladı!")
        else:
            print("Maç sayfası henüz eklenmemiş.")
    except Exception as e:
        print("Hata:", e)

if __name__ == "__main__":
    while True:
        check_passo()
        time.sleep(60)  # 1 dakikada bir kontrol
