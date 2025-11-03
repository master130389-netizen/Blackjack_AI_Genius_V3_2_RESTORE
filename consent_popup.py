from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.core.window import Window
from telegram_manager import send_telegram_message
from data_logger import log_event
from consent_manager import save_consent

class ConsentPopup(Popup):
    def __init__(self, on_close_callback, **kwargs):
        super().__init__(**kwargs)
        self.title = "Consenso al trattamento dati"
        self.size_hint = (0.9, 0.55)
        self.auto_dismiss = False
        self.on_close_callback = on_close_callback

        layout = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(10))
        msg = (
            "L’app può raccogliere dati tecnici (log anonimi) per migliorare "
            "l’intelligenza artificiale e la stabilità.\n\n"
            "Vuoi consentire il trattamento dei dati?"
        )
        layout.add_widget(Label(text=msg, halign="center", valign="middle",
                                text_size=(Window.width * 0.8, None)))

        btns = BoxLayout(spacing=dp(10), size_hint_y=None, height=dp(50))
        yes_btn = Button(text="✅ Consento", background_color=(0,0.6,0,1))
        no_btn = Button(text="❌ Non consento", background_color=(0.6,0,0,1))
        btns.add_widget(no_btn)
        btns.add_widget(yes_btn)
        layout.add_widget(btns)
        self.add_widget(layout)

        yes_btn.bind(on_release=lambda *_: self._save(True))
        no_btn.bind(on_release=lambda *_: self._save(False))

    def _save(self, accepted: bool):
        save_consent(accepted)
        log_event("user_consent", "accepted" if accepted else "declined")
        try:
            send_telegram_message(
                "✅ Consenso accettato" if accepted else "⚠️ Consenso rifiutato")
        except Exception:
            pass
        self.dismiss()
        if callable(self.on_close_callback):
            self.on_close_callback(accepted)
