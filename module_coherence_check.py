import os
import importlib
import traceback
from datetime import datetime
from telegram_notify import send_telegram_message

# === CONFIGURAZIONE ===
PROJECT_PATH = os.path.expanduser("~/projects/Blackjack_AI_Genius_V3_2_RESTORE")

# Moduli principali da verificare
MODULES = [
    "main",
    "data_logger",
    "telegram_manager",
    "training_manager",
    "config",
    "consent_manager",
    "data_exporter",
    "main_backup_v2",
]

# Funzioni chiave da controllare (nome modulo: elenco funzioni)
REQUIRED_FUNCTIONS = {
    "data_logger": ["log_event"],
    "telegram_manager": ["send_telegram_message"],
    "main_backup_v2": ["create_backup_zip"],
    "data_exporter": ["build_export_bundle"],
}

def check_imports():
    errors = []
    for module in MODULES:
        try:
            importlib.import_module(module)
        except Exception as e:
            errors.append(f"❌ Errore import modulo '{module}': {e}")
    return errors

def check_functions():
    errors = []
    for module_name, funcs in REQUIRED_FUNCTIONS.items():
        try:
            mod = importlib.import_module(module_name)
            for func in funcs:
                if not hasattr(mod, func):
                    errors.append(f"⚠️ Modulo '{module_name}' manca funzione '{func}'")
        except Exception as e:
            errors.append(f"❌ Errore accesso funzioni in '{module_name}': {e}")
    return errors

def simulate_main_run():
    """Prova ad avviare main.py per vedere se crasha"""
    try:
        with open(os.path.join(PROJECT_PATH, "main.py")) as f:
            code = compile(f.read(), "main.py", "exec")
            exec(code, {})
        return []
    except Exception as e:
        return [f"💥 Errore avvio main.py: {e}\n{traceback.format_exc()}"]

def main():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report_lines = [f"📦 <b>Controllo coerenza moduli Blackjack AI Genius V3</b>",
                    f"🕐 Ora: {now}\n"]

    import_errors = check_imports()
    func_errors = check_functions()
    runtime_errors = simulate_main_run()

    total_errors = import_errors + func_errors + runtime_errors

    if not total_errors:
        report_lines.append("✅ Tutti i moduli e funzioni risultano coerenti.")
    else:
        report_lines.append("⚠️ Errori o incoerenze trovate:\n" + "\n".join(total_errors))

    full_report = "\n".join(report_lines)
    print(full_report)
    send_telegram_message(full_report)

if __name__ == "__main__":
    main()
