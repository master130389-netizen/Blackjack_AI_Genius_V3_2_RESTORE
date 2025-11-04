import json
import os
import datetime
import traceback
from config import get_app_path
from telegram_manager import send_telegram_message

LOG_FILE = os.path.join(get_app_path("logs"), "training_log.json")


def log_event(event_type, value=None, tc=None, edge=None, theme=None):
    """Salva un evento nel file JSON con data/ora e parametri."""
    try:
        os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
        data = {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "event": event_type,
            "value": value,
            "tc": tc,
            "edge": edge,
            "theme": str(theme)
        }
        logs = []
        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                try:
                    logs = json.load(f)
                except Exception:
                    logs = []
        logs.append(data)
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)
    except Exception:
        error_text = f"Errore nel salvataggio log_event: {traceback.format_exc()}"
        print(error_text)
        try:
            send_telegram_message(error_text)
        except Exception:
            pass
