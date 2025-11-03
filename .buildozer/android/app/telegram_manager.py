import requests
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID

def send_telegram_message(message):
    """Invia un messaggio di testo al bot Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    try:
        response = requests.post(url, data=data)
        return response.status_code == 200
    except Exception as e:
        print(f"Errore Telegram: {e}")
        return False

def send_telegram_file(file_path, caption="Backup file"):
    """Invia un file .zip o .txt al bot Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendDocument"
    try:
        with open(file_path, "rb") as f:
            data = {"chat_id": TELEGRAM_CHAT_ID, "caption": caption}
            files = {"document": f}
            response = requests.post(url, data=data, files=files)
        return response.status_code == 200
    except Exception as e:
        print(f"Errore invio file Telegram: {e}")
        return False
