import os
import subprocess
from datetime import datetime
from telegram_notify import send_telegram_message, load_env

# Carica .env per Telegram
load_env()

# Percorso progetto
project_path = "/home/mario/projects/Blackjack_AI_Genius_V3_2_RESTORE"

# Comando per controllare sintassi Python
def check_code():
    result = subprocess.run(["flake8", project_path], capture_output=True, text=True)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if result.returncode == 0:
        msg = f"✅ Controllo codice completato senza errori.\nOra: {now}"
    else:
        msg = f"⚠️ Errori rilevati nel codice!\n\n{result.stdout[:1000]}\n\nOra: {now}"

    print(msg)
    send_telegram_message(msg)

if __name__ == "__main__":
    check_code()
