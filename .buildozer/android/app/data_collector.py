# === data_collector.py ===
import os, json, datetime

DATA_DIR = "data"
DATA_FILE = os.path.join(DATA_DIR, "training_data.json")

def ensure_data_folder():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def log_training_sample(action_type, player_cards, dealer_card, tc, edge, result=None):
    """
    Registra una mano/decisione nel file di addestramento.
    action_type: es. "move" / "bet"
    player_cards: es. "A,8"
    dealer_card: es. "6"
    tc: true count stimato (float/int)
    edge: vantaggio stimato in %
    result: esito opzionale ("win"/"loss"/"push" o None)
    """
    ensure_data_folder()
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sample = {
        "timestamp": now,
        "action": action_type,
        "player_cards": player_cards,
        "dealer_card": dealer_card,
        "true_count": tc,
        "edge": edge,
        "result": result
    }

    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump([sample], f, indent=2, ensure_ascii=False)
    else:
        with open(DATA_FILE, "r+", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except Exception:
                data = []
            data.append(sample)
            f.seek(0)
            json.dump(data, f, indent=2, ensure_ascii=False)

def get_training_stats():
    """Numero totale di record disponibili per l'addestramento."""
    ensure_data_folder()
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return len(data)
        except Exception:
            return 0
    return 0
