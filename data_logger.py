# -*- coding: utf-8 -*-
"""
data_logger.py
Sistema di logging dati e eventi per Blackjack AI Genius V3 (versione PC).
"""

import os
import json
from datetime import datetime
from telegram_manager import notify_success, notify_error

# === Percorsi ===
BASE_DIR = os.getcwd()
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOG_DIR, "data_log.json")

# === Funzioni di supporto ===
def _load_logs():
    """Carica i log esistenti o restituisce una lista vuota."""
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def _save_logs(logs):
    """Salva i log in formato JSON."""
    try:
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[Log Error] Errore nel salvataggio JSON: {e}")

# === Logger principale ===
def log_event(event_type: str, message: str, extra=None):
    """
    Registra un evento nel file JSON e invia eventuale notifica Telegram.
    """
    data = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": event_type,
        "message": message,
        "extra": extra or {}
    }

    logs = _load_logs()
    logs.append(data)
    _save_logs(logs)

    # Log su terminale
    print(f"[LOG] {event_type.upper()} → {message}")

    # Notifiche Telegram automatiche
    try:
        if event_type.lower() in ("error", "exception", "crash"):
            notify_error(f"Errore registrato: {message}")
        elif event_type.lower() in ("export", "success"):
            notify_success(f"Operazione completata: {message}")
    except Exception as e:
        print(f"[Telegram Warning] Invio fallito: {e}")

# === Shortcut dedicato agli errori ===
def log_error(message: str, extra=None):
    """Shortcut per errori critici."""
    log_event("error", message, extra)
