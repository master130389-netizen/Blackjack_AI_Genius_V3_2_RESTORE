import json
import os
from datetime import datetime
from telegram_manager import notify_success, notify_error

LOG_FILE = os.path.join("logs", "data_log.json")
os.makedirs("logs", exist_ok=True)


def log_event(event_type, message, extra=None):
    """Registra un evento nel file JSON e invia notifica Telegram in modo sicuro."""
    data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": event_type,
        "message": message,
        "extra": extra or {}
    }

    try:
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                logs = json.load(f)
        else:
            logs = []

        logs.append(data)

        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)

        print(f"📝 Log registrato: {event_type} - {message}")

        # Notifica Telegram
        if event_type.lower() in ["error", "crash", "exception"]:
            notify_error(f"⚠️ {message}")
        elif event_type.lower() in ["export", "success"]:
            notify_success(f"✅ {message}")

    except Exception as e:
        print(f"❌ Errore nel log_event: {e}")
        notify_error(f"Errore durante la registrazione log: {e}")
