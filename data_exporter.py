import os
import json
import csv
import io
import zipfile
import datetime
import traceback
from config import (
    LOG_FOLDER, BACKUP_FOLDER, EXPORT_INCLUDE_CSV,
    EXPORT_FILENAME_PREFIX, TELEGRAM_NOTIFY_EXPORT,
    ANONYMIZE_USER_DATA
)
from telegram_manager import send_telegram_message

TRAINING_JSON = os.path.join(LOG_FOLDER, "training_log.json")


def _read_json_safely(path: str):
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def _anonymize(records):
    # Placeholder: al momento non inseriamo dati personali;
    # qui potremmo offuscare ID/username in fasi future.
    if not ANONYMIZE_USER_DATA:
        return records
    return records  # nessun campo PII oggi


def _csv_from_records(records):
    output = io.StringIO()
    fieldnames = ["timestamp", "event", "value", "tc", "edge", "theme"]
    writer = csv.DictWriter(output, fieldnames=fieldnames)
    writer.writeheader()
    for r in records:
        writer.writerow({
            "timestamp": r.get("timestamp"),
            "event": r.get("event"),
            "value": r.get("value"),
            "tc": r.get("tc"),
            "edge": r.get("edge"),
            "theme": r.get("theme"),
        })
    return output.getvalue()


def build_export_bundle():
    """
    Crea uno ZIP con:
    - training_log.json (eventi)
    - training_log.csv (riassunto) se attivo
    - README.txt (spiega come leggere i dati)
    Ritorna: path allo ZIP creato.
    """
    os.makedirs(BACKUP_FOLDER, exist_ok=True)

    # Leggi e (eventualmente) anonimizza
    records = _anonymize(_read_json_safely(TRAINING_JSON))

    # Prepara contenuti in memoria
    ts = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
    zip_name = f"{EXPORT_FILENAME_PREFIX}_{ts}.zip"
    zip_path = os.path.join(BACKUP_FOLDER, zip_name)

    readme_text = (
        "Blackjack AI Genius — Export dati utente (fase 3.5)\n\n"
        "- training_log.json: eventi completi\n"
        "- training_log.csv: riassunto tabellare (se presente)\n\n"
        "Note: non includiamo dati personali. Questo export serve a te per analisi e storicizzazione.\n")

    try:
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
            # JSON
            zf.writestr(
                "training_log.json",
                json.dumps(
                    records,
                    indent=2,
                    ensure_ascii=False))
            # CSV opzionale
            if EXPORT_INCLUDE_CSV:
                csv_text = _csv_from_records(records)
                zf.writestr("training_log.csv", csv_text)
            # README
            zf.writestr("README.txt", readme_text)

        if TELEGRAM_NOTIFY_EXPORT:
            try:
                send_telegram_message(f"✅ Export bundle creato: {zip_name}")
            except Exception:
                pass

        return zip_path

    except Exception:
        try:
            send_telegram_message("❌ Export bundle fallito (zip).")
        except Exception:
            pass
        raise
