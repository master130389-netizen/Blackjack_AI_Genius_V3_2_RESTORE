import os
import json
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.core.window import Window
from config import get_app_path

CONSENT_FILE_NAME = "consent.json"


def _consent_path():
    folder = get_app_path("logs")
    return os.path.join(folder, CONSENT_FILE_NAME)


def get_consent_state():
    try:
        path = _consent_path()
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data.get("granted", False), data
    except Exception:
        pass
    return False, {}


def save_consent(granted):
    """Salva il consenso su file JSON"""
    try:
        data = {"granted": granted}
        path = _consent_path()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f)
    except Exception as e:
        print("Errore salvataggio consenso:", e)


def show_consent_popup(callback):
    """Mostra il popup per il consenso al trattamento dati"""

    layout = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(15))

    # Messaggio principale, migliorato e centrato
    msg = Label(
        text=(
            "🤖 L'app può raccogliere alcuni dati tecnici anonimi per migliorare "
            "l'intelligenza artificiale.\n\n"
            "Fornendo il consenso, permetterai all'AI di apprendere dal tuo stile "
            "di gioco e offrirti suggerimenti sempre più precisi e personalizzati."
        ),
        halign="center",
        valign="middle",
        color=(1, 1, 1, 1)
    )
    msg.bind(size=lambda obj, val: setattr(obj, "text_size", val))
    layout.add_widget(msg)

    # Pulsanti
    btns = BoxLayout(size_hint_y=None, height=dp(60), spacing=dp(10))
    deny = Button(
        text="❌ Non consento",
        background_color=(0.7, 0, 0, 1),
        bold=True
    )
    allow = Button(
        text="✅ Consento",
        background_color=(0, 0.6, 0, 1),
        bold=True
    )
    btns.add_widget(deny)
    btns.add_widget(allow)
    layout.add_widget(btns)

    # Popup (centrato e proporzionato)
    popup = Popup(
        title="Consenso al trattamento dati",
        content=layout,
        size_hint=(0.95, None),
        height=dp(300),
        auto_dismiss=False
    )

    deny.bind(on_release=lambda *_: _handle_response(False, popup, callback))
    allow.bind(on_release=lambda *_: _handle_response(True, popup, callback))

    # Apertura popup consenso (senza tentare di centrare manualmente la finestra)
    try:
        popup.open()
        print("✅ Popup consenso aperto correttamente.")
    except Exception as e:
        print("⚠️ Errore durante l'apertura del popup consenso:", e)

def _handle_response(granted, popup, callback):
    """Gestisce la risposta dell’utente"""
    save_consent(granted)
    callback(granted)
    popup.dismiss()
