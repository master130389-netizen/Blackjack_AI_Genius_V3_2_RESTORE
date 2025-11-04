import os
import requests

def send_telegram_message(message: str):
    """Invia un messaggio tramite Telegram."""
    token = os.getenv("TELEGRAM_TOKEN")  # Recupera il token di Telegram
    chat_id = os.getenv("TELEGRAM_CHAT_ID")  # Recupera l'ID chat di Telegram

    if not token or not chat_id:
        print("⚠️ Mancano TOKEN o CHAT_ID nel file .env")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}

    try:
        r = requests.post(url, data=payload, timeout=10)  # Invia la richiesta a Telegram
        if r.status_code == 200:
            print(f"✅ Messaggio Telegram inviato: {message}")
            return True
        else:
            print(f"❌ Errore invio Telegram ({r.status_code}): {r.text}")
            return False
    except Exception as e:
        print(f"❌ Eccezione Telegram: {e}")
        return False

# Verifica se il file contenente il report è presente e carica i dati
report_path = "report.txt"
if os.path.exists(report_path):
    try:
        with open(report_path, "r") as file:
            report_content = file.read()
    except Exception as e:
        print(f"❌ Errore nel leggere report.txt: {e}")
        report_content = "Errore nel leggere il report."
else:
    report_content = "❌ Il file report.txt non esiste."

# Invia il messaggio di Telegram con il contenuto del report
send_telegram_message(report_content)
