import json, os

STATS_FILE = "user_stats.json"

def load_stats():
    if not os.path.exists(STATS_FILE):
        return {"games_played": 0, "correct_moves": 0, "wrong_moves": 0, "accuracy": 0.0}
    with open(STATS_FILE, "r") as f:
        return json.load(f)

def save_stats(data):
    with open(STATS_FILE, "w") as f:
        json.dump(data, f, indent=4)

def update_stats(correct: bool):
    data = load_stats()
    data["games_played"] += 1
    if correct:
        data["correct_moves"] += 1
    else:
        data["wrong_moves"] += 1
    total = data["games_played"]
    data["accuracy"] = round((data["correct_moves"] / total) * 100, 1) if total > 0 else 0
    save_stats(data)
