import os
import platform

# === FUNZIONE PERCORSO CROSS-PLATFORM (PC / ANDROID) ===


def get_app_path(subfolder=""):
    """
    Restituisce il percorso base per salvataggi (PC o Android)
    """
    base = os.path.expanduser("~")

    # Percorso simulato Android (per test su PC)
    android_path = os.path.join(
        base,
        "projects/Blackjack_AI_Genius_V3_2_RESTORE/android_storage/Download/BlackjackAI")

    # Su Android reale, Buildozer sostituirà con
    # /storage/emulated/0/Download/BlackjackAI
    if "ANDROID_STORAGE" in os.environ or "ANDROID_ARGUMENT" in os.environ:
        android_path = "/storage/emulated/0/Download/BlackjackAI"

    final_path = os.path.join(android_path,
                              subfolder) if subfolder else android_path
    os.makedirs(final_path, exist_ok=True)
    return final_path


# === CARTELLE E LOG ===
PROJECT_ROOT = os.path.expanduser(
    "~/projects/Blackjack_AI_Genius_V3_2_RESTORE")
LOG_FOLDER = os.path.join(PROJECT_ROOT, "logs")
os.makedirs(LOG_FOLDER, exist_ok=True)

# Impostazioni rotazione log
LOG_MAX_BYTES = 1_500_000    # ~1.5 MB per file
LOG_ROTATE_KEEP = 3          # quanti file di log tenere


# === TELEGRAM CONFIG ===
# (Verranno caricati dal file .env o, se assenti, useranno i valori di default)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "INSERISCI_IL_TUO_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "INSERISCI_IL_TUO_CHAT_ID")

# Se True, invia notifica su Telegram dopo l'export dei dati
TELEGRAM_NOTIFY_EXPORT = True


# === IMPOSTAZIONI BACKUP ===
BACKUP_FOLDER = os.path.expanduser("~/apk_builds")
os.makedirs(BACKUP_FOLDER, exist_ok=True)


# === PRIVACY / CONSENSO ===
CONSENT_FILE = os.path.join(PROJECT_ROOT, "user_consent.json")


# === IMPOSTAZIONI EXPORT DATI ===
EXPORT_INCLUDE_JSON = True     # includi file JSON di log
EXPORT_INCLUDE_CSV = True      # includi versione CSV
EXPORT_INCLUDE_README = True   # includi file README.txt nel bundle
EXPORT_FILENAME_PREFIX = "BlackjackAI_DataExport_"

# Se True, anonimizza i dati utente (es. nome, ID, device) nei log esportati
ANONYMIZE_USER_DATA = True
