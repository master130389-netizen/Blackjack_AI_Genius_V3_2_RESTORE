import os
import subprocess
import sys
from datetime import datetime
from telegram_notify import send_telegram_message

# === CONFIG ===
PROJECT_PATH = os.path.expanduser("~/projects/Blackjack_AI_Genius_V3_2_RESTORE")
REQUIRED_FILES = [
    "main.py",
    "config.py",
    "telegram_manager.py",
    "data_logger.py",
    "data_exporter.py",
    "consent_manager.py",
    "consent_popup.py",
]

REQUIRED_LIBS = ["kivy", "requests"]

# === FUNZIONI ===
def check_files():
    missing = [f for f in REQUIRED_FILES if not os.path.exists(os.path.join(PROJECT_PATH, f))]
    return missing

def check_dependencies():
    missing_libs = []
    for lib in REQUIRED_LIBS:
        try:
            __import__(lib)
        except ImportError:
            missing_libs.append(lib)
    return missing_libs

def run_flake8():
    try:
        result = subprocess.run(
            ["flake8", "."],
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    except Exception as e:
        return f"Errore flake8: {e}"

def main():
    missing_files = check_files()
    missing_libs = check_dependencies()
    lint_report = run_flake8()

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report = f"📋 <b>Controllo progetto Blackjack AI Genius V3</b>\n🕐 Ora: {now}\n\n"

    if missing_files:
        report += f"❌ File mancanti:\n- " + "\n- ".join(missing_files) + "\n\n"
    else:
        report += "✅ Tutti i file principali sono presenti.\n\n"

    if missing_libs:
        report += f"⚠️ Librerie mancanti: {', '.join(missing_libs)}\n\n"
    else:
        report += "✅ Tutte le librerie principali installate.\n\n"

    if lint_report:
        report += f"⚠️ Errori di stile o sintassi trovati:\n{lint_report[:800]}...\n\n"
    else:
        report += "✅ Nessun errore di stile rilevato.\n\n"

    if not missing_files and not missing_libs and not lint_report:
        report += "🎉 <b>Progetto completamente stabile!</b>"
    else:
        report += "🔍 Controlla i dettagli sopra prima di procedere."

    print(report)
    send_telegram_message(report)

if __name__ == "__main__":
    main()

