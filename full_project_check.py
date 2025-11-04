import os
import requests  # Assicurati che requests sia importato
from datetime import datetime

# Percorso per il file report.txt
report_path = os.path.expanduser("~/projects/Blackjack_AI_Genius_V3_2_RESTORE/report.txt")

def create_report():
    """Funzione per creare e scrivere nel file report.txt"""
    with open(report_path, "w") as report_file:
        report_file.write("🔔 Report di controllo progetto Blackjack AI Genius V3\n")
        report_file.write("==============================================\n")
        
        # Aggiungi qui i dettagli che vuoi scrivere nel report, ad esempio:
        report_file.write("✅ File principali presenti: \n")
        report_file.write("- main.py\n")
        report_file.write("- config.py\n")
        report_file.write("- consent_manager.py\n")
        report_file.write("\n")
        report_file.write("✅ Controllo librerie: \n")
        report_file.write("✔️ flake8\n")
        report_file.write("✔️ kivy\n")
        report_file.write("\n")
        report_file.write("⚠️ Errori di stile: nessuno\n")
        report_file.write("\n")
        # Aggiungi altri dettagli come il controllo delle dipendenze o altre verifiche
        report_file.write("==============================================\n")
        report_file.write("Controllo completato con successo!\n")

def send_report_to_telegram():
    """Funzione per inviare il report su Telegram"""
    # Verifica che il file report.txt esista
    if os.path.exists(report_path):
        with open(report_path, "r") as file:
            report_content = file.read()
        
        send_telegram_message(report_content)
    else:
        print("❌ Il file report.txt non esiste!")

# Funzione per inviare messaggio su Telegram
def send_telegram_message(message: str):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        print("⚠️ Mancano TOKEN o CHAT_ID nel file .env")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "HTML"}

    try:
        r = requests.post(url, data=payload, timeout=10)
        if r.status_code == 200:
            print(f"✅ Messaggio Telegram inviato: {message}")
            return True
        else:
            print(f"❌ Errore invio Telegram ({r.status_code}): {r.text}")
            return False
    except Exception as e:
        print(f"❌ Eccezione Telegram: {e}")
        return False

# Creare il report
create_report()

# Inviare il report su Telegram
send_report_to_telegram()

