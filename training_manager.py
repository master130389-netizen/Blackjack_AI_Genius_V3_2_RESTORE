import os
from datetime import datetime
from telegram_manager import notify_ai_status, notify_error

LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_PATH = os.path.join(LOG_DIR, "ai_activity.txt")


def _log_ai_event(event: str):
    """Scrive un evento AI nel log locale."""
    try:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {event}\n")
    except Exception as e:
        notify_error(f"Errore scrittura log AI: {e}")


def start_training():
    """Simula l'avvio di un training AI reale."""
    try:
        event = "⚙️ Avvio training AI"
        _log_ai_event(event)
        notify_ai_status(event)

        # --- simulazione lavoro AI ---
        import time
        time.sleep(2)  # simulazione processo

        result = "✅ Training completato con successo"
        _log_ai_event(result)
        notify_ai_status(result)

    except Exception as e:
        notify_error(f"❌ Errore durante training AI: {e}")
        _log_ai_event(f"❌ Errore training AI: {e}")


def analyze_hand(hand_data):
    """Esegue analisi probabilistica di una mano di gioco."""
    try:
        event = f"🃏 Analisi mano: {hand_data}"
        _log_ai_event(event)
        notify_ai_status(event)

        # Simulazione di analisi
        import random
        score = round(random.uniform(0.1, 0.95), 2)

        result = f"💡 Probabilità di vincita stimata: {score * 100}%"
        _log_ai_event(result)
        notify_ai_status(result)
        return score

    except Exception as e:
        notify_error(f"❌ Errore durante analisi AI: {e}")
        _log_ai_event(f"❌ Errore analisi AI: {e}")
        return None
