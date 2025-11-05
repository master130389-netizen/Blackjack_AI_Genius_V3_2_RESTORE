from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.core.window import Window
import traceback, os

# === SISTEMA DI CRASH REPORT TELEGRAM ===
import sys
import traceback
from telegram_manager import notify_error, notify_success

def handle_exception(exc_type, exc_value, exc_traceback):
    """Gestisce errori globali e invia notifica Telegram."""
    if issubclass(exc_type, KeyboardInterrupt):
        # ignora Ctrl+C
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    error_text = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    print("❌ Crash rilevato:\n", error_text)
    notify_error(f"❌ Crash in Blackjack AI Genius V3:\n{error_text[:800]}")

# Imposta il crash handler globale
sys.excepthook = handle_exception

# === Importa moduli reali (se disponibili) ===

# (test temporaneo per verificare Telegram - rimuovi dopo)


# === Importa moduli reali (se disponibili) ===
try:
    from telegram_manager import notify_success, notify_error
    from data_logger import log_event, log_error
    from data_collector import create_backup_zip, build_export_bundle
except Exception as e:
    print(f"⚠️ Modalità debug: moduli non trovati ({e})")
    def notify_success(msg): print(f"[NOTIFY_SUCCESS] {msg}")
    def notify_error(msg): print(f"[NOTIFY_ERROR] {msg}")
    def log_event(*a, **k): pass
    def log_error(*a, **k): pass
    def create_backup_zip(): print("🗜️ [DEBUG] Creazione ZIP fittizia...")
    def build_export_bundle(): 
        path = "/tmp/fake_bundle.zip"
        with open(path, "w") as f: f.write("fake data")
        return path


# === SCHERMATA PRINCIPALE ===
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from kivy.metrics import dp
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.label import Label
        from kivy.uix.button import Button

        pad = dp(20)
        self.layout = BoxLayout(orientation="vertical", padding=pad, spacing=dp(10))

        # === LABEL DI STATO ===
        self.status_lbl = Label(
            text="Stato: pronto",
            color=(0, 1, 0, 1),
            font_size="18sp",
            halign="center",
            valign="middle",
            bold=True
        )
        self.status_lbl.bind(size=lambda obj, val: setattr(obj, "text_size", val))

        # === PULSANTE EXPORT ===
        self.export_btn = Button(text="📦 Export Data", size_hint=(1, 0.15))
        self.export_btn.bind(on_release=self.export_data)

        # === PULSANTE AI BOOST ===
        self.ai_btn = Button(text="🎯 AI Boost / Calcola mossa", size_hint=(1, 0.15))
        self.ai_btn.bind(on_release=self.activate_ai_boost)

        self.layout.add_widget(self.status_lbl)
        self.layout.add_widget(self.export_btn)
        self.layout.add_widget(self.ai_btn)
        self.add_widget(self.layout)

    # === FUNZIONE EXPORT ===
    def export_data(self, instance):
        """Gestisce l’esportazione reale e invia notifica Telegram."""
        try:
            instance.text = "⏳ Esportazione in corso..."
            instance.disabled = True
            self.status_lbl.text = "Esportazione in corso..."
            self.status_lbl.color = (1, 1, 0, 1)

            from data_collector import build_export_bundle
            from telegram_manager import notify_success, notify_error

            bundle_path = build_export_bundle()
            file_name = os.path.basename(bundle_path)
            notify_success(f"✅ Export completato con successo! File: {file_name}")

            self.status_lbl.text = f"Esportazione completata: {file_name}"
            self.status_lbl.color = (0, 1, 0, 1)
            instance.text = "✅ Esportato!"

        except Exception as e:
            from telegram_manager import notify_error
            notify_error(f"❌ Errore durante export: {e}")
            self.status_lbl.text = f"Errore export: {e}"
            self.status_lbl.color = (1, 0, 0, 1)
            instance.text = "❌ Errore!"

        finally:
            from kivy.clock import Clock
            Clock.schedule_once(lambda dt: self._reset_btn(instance), 3)

    # === FUNZIONE AI BOOST ===
    def activate_ai_boost(self, instance):
        """Simula l’attivazione AI con feedback locale e Telegram."""
        try:
            instance.text = "🤖 AI in corso..."
            instance.disabled = True
            self.status_lbl.text = "Calcolo probabilità in corso..."
            self.status_lbl.color = (1, 1, 0, 1)

            from training_manager import start_training, analyze_hand
            from telegram_manager import notify_ai_status, notify_error

            start_training()
            score = analyze_hand({"player": ["10", "A"], "dealer": ["6"]})
            if score is not None:
                percent = round(score * 100, 1)
                msg = f"💡 Probabilità di vincita: {percent}%"
                self.status_lbl.text = msg
                self.status_lbl.color = (0, 1, 0, 1)
                notify_ai_status(f"📊 {msg}")
            else:
                raise ValueError("Risultato AI non disponibile")

        except Exception as e:
            notify_error(f"❌ Errore AI Boost: {e}")
            self.status_lbl.text = f"Errore AI: {e}"
            self.status_lbl.color = (1, 0, 0, 1)

        finally:
            from kivy.clock import Clock
            Clock.schedule_once(lambda dt: self._reset_btn(instance), 4)

    def _reset_btn(self, instance):
        instance.text = "📦 Export Data" if "Export" in instance.text else "🎯 AI Boost / Calcola mossa"
        instance.disabled = False

# === ROOT e APP ===
class RootUI(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(MainScreen(name="main"))


class BlackjackApp(App):
    def build(self):
        print("📱 Avvio Blackjack AI Genius V3 - UI completa")
        Clock.schedule_interval(lambda dt: print("App viva..."), 2)
        return RootUI()


if __name__ == "__main__":
    print("✅ Avvio Blackjack AI Genius V3 - Fase 2.2")
    BlackjackApp().run()
    print("🧠 Fine programma Blackjack.")
