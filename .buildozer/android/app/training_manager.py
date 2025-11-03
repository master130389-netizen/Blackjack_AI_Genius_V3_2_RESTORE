# === training_manager.py ===
import os, json, csv
from data_collector import DATA_FILE, ensure_data_folder, get_training_stats
from telegram_manager import send_telegram_message  # già usato per gli export/backup

EXPORT_DIR = "data"
EXPORT_FILE = os.path.join(EXPORT_DIR, "training_export.csv")

def analyze_training_data():
    """
    Legge training_data.json e crea un CSV pronto per analisi/ML.
    Invia una notifica Telegram di riepilogo.
    """
    ensure_data_folder()

    if not os.path.exists(DATA_FILE):
        msg = "❌ Nessun dato di training disponibile."
        try: send_telegram_message(msg)
        except: pass
        return msg

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception:
        data = []

    if not data:
        msg = "⚠️ Nessun record utile trovato."
        try: send_telegram_message(msg)
        except: pass
        return msg

    # Esporta CSV
    os.makedirs(EXPORT_DIR, exist_ok=True)
    with open(EXPORT_FILE, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["timestamp", "action", "player_cards", "dealer_card", "true_count", "edge", "result"])
        for row in data:
            writer.writerow([
                row.get("timestamp",""),
                row.get("action",""),
                row.get("player_cards",""),
                row.get("dealer_card",""),
                row.get("true_count",""),
                row.get("edge",""),
                row.get("result","")
            ])

    total = get_training_stats()
    msg = f"📊 Training export completato: {total} record salvati in {EXPORT_FILE}"
    try: send_telegram_message(msg)
    except: pass
    return f"✅ Analisi completata. {total} record esportati in {EXPORT_FILE}"

