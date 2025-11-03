import os
import requests
from datetime import datetime

def load_env():
    """Carica manualmente le variabili dal file .env"""
    env_path = os.path.expanduser("~/projects/Blackjack_AI_Genius_V3_2_RESTORE/.env")
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.strip() and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    os.environ[key] = value

def send_telegram_message(message: str):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("⚠️ Mancano TOKEN o CHAT_ID nel file .env")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}

    try:
        r = requests.post(url, data=payload, timeout=10)
        if r.status_code == 200:
            print(f"✅ Messaggio Telegram inviato: {message}")
            return True
        else:
            print(f"❌ Errore invio Telegram ({r.status_code}): {r.text}")
            return False
    except Exception as e:
        print(f"❌ Eccezione Telegram: {e}")
        return False


if __name__ == "__main__":
    load_env()  # Carica manualmente il file .env
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    send_telegram_message(f"🔔 Test messaggio automatico dal tuo server Ubuntu!\nOra: {now}")
