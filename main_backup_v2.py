import os
import zipfile
import datetime
from telegram_manager import send_telegram_message, send_telegram_file

def create_backup_zip():
    """Crea un file ZIP con i log e lo invia su Telegram"""
    try:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_name = f"backup_{timestamp}.zip"
        backup_dir = "backups"
        os.makedirs(backup_dir, exist_ok=True)

        # Crea ZIP
        with zipfile.ZipFile(os.path.join(backup_dir, zip_name), "w") as zipf:
            for filename in ["training_log.json", "error_log.txt"]:
                if os.path.exists(filename):
                    zipf.write(filename)
        
        zip_path = os.path.join(backup_dir, zip_name)
        send_telegram_message("📦 Backup in corso...")
        if send_telegram_file(zip_path, caption=f"Backup esportato: {zip_name}"):
            send_telegram_message("✅ Backup esportato con successo!")
        else:
            send_telegram_message("⚠️ Errore durante l’invio del file ZIP.")

        return True

    except Exception as e:
        send_telegram_message(f"❌ Errore backup: {e}")
        return False
