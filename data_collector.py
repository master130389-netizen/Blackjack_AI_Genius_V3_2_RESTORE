import os
import zipfile
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
EXPORTS_DIR = BASE_DIR / "exports"
EXPORTS_DIR.mkdir(exist_ok=True)

def create_backup_zip():
    """Crea un file ZIP con log e dati dell'app."""
    zip_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    zip_path = EXPORTS_DIR / zip_name

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for folder, _, files in os.walk(BASE_DIR):
            for file in files:
                if file.endswith(".txt") or file.endswith(".json") or file.endswith(".log"):
                    file_path = Path(folder) / file
                    arcname = file_path.relative_to(BASE_DIR)
                    zipf.write(file_path, arcname)

    return zip_path

def build_export_bundle():
    """Crea un bundle finale da inviare o salvare."""
    return str(create_backup_zip())
