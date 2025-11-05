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

# ========== CLASSE DRAWER LATERALE ==========
from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.metrics import dp
from kivy.animation import Animation

class SideDrawer(ModalView):
    """Drawer laterale sinistro con animazione e chiusura automatica."""
    def init(self, parent, theme, **kwargs):
        super().init(**kwargs)
        self.parent_ref = parent
        self.theme = theme
        self.size_hint = (0.8, 1)
        self.background_color = (0, 0, 0, 0)
        self.auto_dismiss = True

        # Layout principale
        box = BoxLayout(orientation="vertical", spacing=dp(10), padding=dp(15))
        box.canvas.before.clear()
        with box.canvas.before:
            from kivy.graphics import Color, Rectangle
            Color(*self.theme['surface'], 1)
            self.bg_rect = Rectangle(size=box.size, pos=box.pos)
            box.bind(size=self._update_rect, pos=self._update_rect)

        # === Pulsanti nel drawer ===
        items = [
            ("🏠  Home", self.close_drawer),
            ("🎨  Change Theme", self.parent_ref.change_theme),
            ("💾  Export Data", self.parent_ref.export_data),
            ("⚙️  Settings", self.close_drawer),
        ]

        for text, callback in items:
            btn = Button(
                text=text,
                size_hint_y=None,
                height=dp(45),
                background_color=(0, 0, 0, 0),
                color=self.theme['text'],
                halign='left',
                valign='middle'
            )
            btn.bind(on_release=lambda instance, cb=callback: self._on_button_press(cb))
            box.add_widget(btn)

        self.add_widget(box)

    def _update_rect(self, instance, value):
        self.bg_rect.size = instance.size
        self.bg_rect.pos = instance.pos

    def _on_button_press(self, callback):
        self.dismiss()
        Clock.schedule_once(lambda dt: callback(None), 0.2)

    def open_drawer(self):
        """Anima l'apertura del drawer da sinistra"""
        self.opacity = 0
        super().open()
        Animation(opacity=1, duration=0.2).start(self)

    def close_drawer(self, *args):
        """Anima la chiusura"""
        anim = Animation(opacity=0, duration=0.15)
        anim.bind(on_complete=lambda *x: self.dismiss())
        anim.start(self)

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
    def init(self, **kwargs):
        super().init(**kwargs)
        from kivy.metrics import dp
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.label import Label
        from kivy.uix.button import Button
        from kivy.uix.floatlayout import FloatLayout
        from kivy.uix.anchorlayout import AnchorLayout

        # === Layout principale ===
        self.theme_names = list(THEMES.keys())
        self.theme_idx = 0
        self.current_theme = THEMES[self.theme_names[self.theme_idx]]

        root = FloatLayout()
        self.add_widget(root)

        # === Bottone menù ☰ (in alto a sinistra) ===
        self.menu_btn = Button(
            text="☰",
            size_hint=(None, None),
            size=(dp(50), dp(50)),
            pos_hint={"x": 0.02, "top": 0.98},
            background_color=(0, 0, 0, 0),
            color=self.current_theme['text'],
            font_size='24sp'
        )
        self.menu_btn.bind(on_release=lambda *x: self.drawer.open_drawer())
        root.add_widget(self.menu_btn)

        # === Etichetta centrale titolo app ===
        self.title_lbl = Label(
            text="🧠 Blackjack AI Genius V3",
            size_hint=(None, None),
            size=(dp(300), dp(50)),
            pos_hint={"center_x": 0.5, "top": 0.96},
            color=self.current_theme['text'],
            font_size='18sp',
            bold=True
        )
        root.add_widget(self.title_lbl)

        # === Pulsante Export Data ===
        self.export_btn = Button(
            text="Export Data",
            size_hint=(0.4, None),
            height=dp(45),
            pos_hint={"center_x": 0.5, "y": 0.05},
            background_normal='',
            background_color=self.current_theme['primary'],
            color=self.current_theme['on_primary'],
            bold=True
        )
        self.export_btn.bind(on_release=self.export_data)
        root.add_widget(self.export_btn)

        # === Crea il Drawer laterale sinistro ===
        self.drawer = SideDrawer(self, self.current_theme)

        # === Label di stato (in basso) ===
        self.status_lbl = Label(
            text="Ready",
            size_hint=(1, None),
            height=dp(30),
            pos_hint={"center_x": 0.5, "y": 0},
            color=self.current_theme['text'],
            font_size='14sp'
        )
        root.add_widget(self.status_lbl)

    # === Funzione di cambio tema ===
    def change_theme(self, *args):
        self.theme_idx = (self.theme_idx + 1) % len(THEMES)
        selected = self.theme_names[self.theme_idx]
        self.current_theme = THEMES[selected]

        # Aggiorna i colori di tutti gli elementi
        self.menu_btn.color = self.current_theme['text']
        self.title_lbl.color = self.current_theme['text']
        self.status_lbl.color = self.current_theme['text']
        self.export_btn.background_color = self.current_theme['primary']
        self.export_btn.color = self.current_theme['on_primary']

        notify_success(f"Tema cambiato in: {selected}")
        log_event("change_theme", f"Tema attivo: {selected}")

    # === Funzione Export ===
    def export_data(self, instance):
        try:
            instance.text = "📦 Exporting..."
            instance.disabled = True
            export_all()
            instance.text = "✅ Exported!"
            self.status_lbl.text = "Export completed successfully"
            notify_success("Dati esportati con successo!")
        except Exception as e:
            instance.text = "❌ Export failed"
            self.status_lbl.text = f"Errore export: {e}"
            log_event("error", f"Errore export: {e}")
            notify_error(f"❌ Errore export: {e}")
        finally:
            Clock.schedule_once(lambda dt: self._reset_export_button(instance), 3)

    def _reset_export_button(self, instance):
        instance.text = "Export Data"
        instance.disabled = False
        instance.state = "normal"
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
