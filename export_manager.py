# -*- coding: utf-8 -*-
"""
export_manager.py
Gestione esportazione log e dati per Blackjack AI Genius V3 (versione PC).
"""

import os
import zipfile
from datetime import datetime
from telegram_manager import notify_success, notify_error

EXPORT_DIR = os.path.join(os.getcwd(), "exports")
LOG_DIR = os.path.join(os.getcwd(), "logs")
os.makedirs(EXPORT_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

def _zip_logs() -> str:
    """Crea un file ZIP con tutti i log e restituisce il percorso."""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        zip_path = os.path.join(EXPORT_DIR, f"Blackjack_AI_Export_{timestamp}.zip")

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for root, _, files in os.walk(LOG_DIR):
                for f in files:
                    file_path = os.path.join(root, f)
                    arc_name = os.path.relpath(file_path, LOG_DIR)
                    zf.write(file_path, arcname=arc_name)

        return zip_path
    except Exception as e:
        raise RuntimeError(f"Errore durante la creazione ZIP: {e}")

def export_all() -> str:
    """
    Esegue l'esportazione completa dei dati log.
    - Crea un archivio ZIP
    - Invia notifica Telegram
    - Restituisce percorso ZIP
    """
    try:
        zip_path = _zip_logs()
        size_kb = os.path.getsize(zip_path) / 1024

        msg = f"Export completato: {os.path.basename(zip_path)} ({size_kb:.1f} KB)"
        notify_success(msg)
        print(f"[Export] {msg}")
        return zip_path

    except Exception as e:
        notify_error(f"Export fallito: {e}")
        print(f"[Export Error] {e}")
        return None
