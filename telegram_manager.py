import os
import threading
import requests
from datetime import datetime
from dotenv import load_dotenv
from pathlib import Path

# === Lettura sicura del file .env ===
BASE_DIR = Path(__file__).resolve().parent
env_path = BASE_DIR / ".env"
if env_path.exists():
    load_dotenv(dotenv_path=env_path)
else:
    print(f"⚠️ File .env non trovato in {env_path}")

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

LOG_PATH = os.path.join("logs", "telegram_log.txt")
os.makedirs("logs", exist_ok=True)

# === Verifica iniziale ===
if not BOT_TOKEN or not CHAT_ID:
    print("⚠️ Attenzione: variabili Telegram non trovate. Controlla il file .env")
else:
    print(f"✅ Variabili Telegram caricate correttamente:\nTOKEN={BOT_TOKEN[:10]}... CHAT_ID={CHAT_ID}")


# === Funzione principale di invio ===
def _send_message(prefix: str, text: str):
    """Invia un messaggio Telegram e salva un log locale."""
    def _worker():
        try:
            data = {"chat_id": CHAT_ID, "text": f"{prefix} {text}"}
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            r = requests.post(url, data=data, headers=headers, timeout=10)
            r.raise_for_status()
            print("🌐 Telegram API response:", r.status_code, r.text[:200])

            # Log su file
            with open(LOG_PATH, "a", encoding="utf-8") as f:
                f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {prefix} {text}\n")

            print(f"✅ Telegram SUCCESS → {prefix} {text}")

        except Exception as e:
            print(f"❌ Telegram ERROR: {e}")
            try:
                with open(LOG_PATH, "a", encoding="utf-8") as f:
                    f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ERROR: {e}\n")
            except Exception:
                pass

    _worker()


# === Funzioni pubbliche per notifiche ===
def notify_success(message: str):
    _send_message("✅ SUCCESS:", message)

def notify_error(message: str):
    _send_message("❌ ERROR:", message)
# === SISTEMA DI NOTIFICA AI STATUS ===
def notify_ai_status(message: str):
    """
    Invia aggiornamenti di stato AI, training, probabilità o strategia.
    Esempi:
        notify_ai_status("🤖 Training completato con successo")
        notify_ai_status("⚙️ AI Boost avviato per analisi mano corrente")
    """
    _send_message("🤖 AI STATUS:", message)

