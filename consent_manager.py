import os
import json
from kivy.app import App
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.metrics import dp
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
    try:
        data = {"granted": granted}
        path = _consent_path()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f)
    except Exception as e:
        print("Errore salvataggio consenso:", e)


def show_consent_popup(callback):
    layout = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(15))
    lbl = Label(
        text="L’app può raccogliere dati tecnici anonimi per migliorare l’intelligenza artificiale.\n\nVuoi consentire il trattamento dei dati?",
        halign="center",
        valign="middle")
    layout.add_widget(lbl)
    btns = BoxLayout(size_hint_y=None, height=dp(60), spacing=dp(10))
    deny = Button(text="Non consento", background_color=(0.7, 0, 0, 1))
    allow = Button(text="Consento", background_color=(0, 0.6, 0, 1))
    btns.add_widget(deny)
    btns.add_widget(allow)
    layout.add_widget(btns)
    popup = Popup(title="Consenso al trattamento dati", content=layout,
                  size_hint=(0.9, None), height=dp(300), auto_dismiss=False)
    deny.bind(on_release=lambda *_: (_handle_response(False, popup, callback)))
    allow.bind(on_release=lambda *_: (_handle_response(True, popup, callback)))
    popup.open()


def _handle_response(granted, popup, callback):
    save_consent(granted)
    callback(granted)
    popup.dismiss()
