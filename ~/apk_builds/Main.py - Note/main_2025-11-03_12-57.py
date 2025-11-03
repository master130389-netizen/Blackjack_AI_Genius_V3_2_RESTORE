import os, random, traceback, datetime, sys
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.metrics import dp
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle, Line
from kivy.properties import ListProperty
from kivy.clock import Clock

# === DATA LOGGER (fase 3.1) ===
from data_logger import log_event

# === BACKUP & TELEGRAM (fase 3.3) ===
from main_backup_v2 import create_backup_zip
from telegram_manager import send_telegram_message

# === FILE DI LOG ERRORI ===
LOG_FILE = "error_log.txt"

def log_error(err_msg: str):
    """Salva errori in un file con data e ora"""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{now}] {err_msg}\n")

# === GESTORE GLOBALE DEGLI ERRORI ===
def handle_exception(exc_type, exc_value, exc_traceback):
    error_details = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    log_error(error_details)
    print("Errore gestito, controlla il file error_log.txt")

sys.excepthook = handle_exception

# === TEMI ===
THEME_DARK = {
    "bg": (0, 0, 0, 1),
    "fg": (1, 1, 1, 1),
    "btn": (0.2, 0.2, 0.2, 1),
    "btn_press": (0.35, 0.45, 0.65, 1),
    "menu_bg": (0.1, 0.1, 0.1, 1),
    "close_btn": (1, 0, 0, 1),
}

THEME_LIGHT = {
    "bg": (1, 1, 1, 1),
    "fg": (0, 0, 0, 1),
    "btn": (0.9, 0.9, 0.9, 1),
    "btn_press": (0.75, 0.75, 0.85, 1),
    "menu_bg": (0.85, 0.85, 0.85, 1),
    "close_btn": (1, 0, 0, 1),
}

THEME_FILE = "theme_config.txt"

def load_theme():
    """Carica il tema salvato nel file di configurazione"""
    try:
        if os.path.exists(THEME_FILE):
            with open(THEME_FILE, "r", encoding="utf-8") as f:
                if f.read().strip().lower() == "light":
                    return THEME_LIGHT
    except Exception:
        pass
    return THEME_DARK

def save_theme(is_light: bool):
    """Salva il tema scelto (light/dark)"""
    with open(THEME_FILE, "w", encoding="utf-8") as f:
        f.write("light" if is_light else "dark")

CURRENT_THEME = load_theme()
Window.clearcolor = CURRENT_THEME["bg"]

# === BOXLAYOUT CON SFONDO ===
class ColoredBoxLayout(BoxLayout):
    background_color = ListProperty([0, 0, 0, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            self._bg_color_instr = Color(rgba=self.background_color)
            self._bg_rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_bg, pos=self._update_bg, background_color=self._update_bg_color)

    def _update_bg(self, *args):
        self._bg_rect.size = self.size
        self._bg_rect.pos = self.pos

    def _update_bg_color(self, *args):
        self._bg_color_instr.rgba = self.background_color

# === PULSANTI CON ANIMAZIONE ===
class MenuButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ""
        self.size_hint_y = None
        self.height = dp(55)
        self.bold = True
        self.update_theme()
        Window.bind(on_resize=lambda *a: self._resize_text())

    def update_theme(self):
        self.background_color = CURRENT_THEME["btn"]
        self.color = CURRENT_THEME["fg"]
        self._resize_text()

    def _resize_text(self, *args):
        base = min(Window.width / 28, 22)
        self.font_size = f"{base}sp"

    def animate_color(self, new_color, duration=0.15):
        Animation.cancel_all(self)
        Animation(background_color=new_color, duration=duration, transition='out_quad').start(self)

    def on_press(self):
        self.animate_color(CURRENT_THEME["btn_press"])

    def on_release(self):
        self.animate_color(CURRENT_THEME["btn"])
        return super().on_release()

# === PULSANTE X ROSSA ===
class CloseButton(Widget):
    def __init__(self, on_close, **kwargs):
        super().__init__(**kwargs)
        self.on_close = on_close
        self.size_hint = (None, None)
        self.size = (dp(40), dp(40))
        self.bind(pos=self._redraw, size=self._redraw)
        with self.canvas:
            self.bg_color = Color(*CURRENT_THEME["close_btn"])
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
            self.x_color = Color(1, 1, 1, 1)
            self.line1 = Line(points=[], width=3)
            self.line2 = Line(points=[], width=3)
        self._redraw()

    def _redraw(self, *args):
        x, y = self.pos
        w, h = self.size
        self.bg_rect.pos, self.bg_rect.size = (x, y), (w, h)
        m = dp(8)
        self.line1.points = [x + m, y + m, x + w - m, y + h - m]
        self.line2.points = [x + m, y + h - m, x + w - m, y + m]

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.on_close()
            return True
        return super().on_touch_down(touch)

# === SCHERMATA PRINCIPALE ===
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.menu_open = False
        self.all_buttons = []

        pad = dp(Window.width * 0.04)
        self.layout = BoxLayout(orientation='vertical', padding=pad, spacing=dp(10))
        with self.layout.canvas.before:
            self._root_bg_color = Color(rgba=CURRENT_THEME["bg"])
            self.bg_rect = Rectangle(size=self.layout.size, pos=self.layout.pos)
        self.layout.bind(size=self._update_bg, pos=self._update_bg)

        # HEADER
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(60), spacing=dp(10))
        left_box = BoxLayout(orientation='horizontal', size_hint_x=None, width=dp(80))
        self.menu_btn = MenuButton(text="Menu")
        self.menu_btn.bind(on_release=lambda *_: self.toggle_menu())
        left_box.add_widget(self.menu_btn)
        header.add_widget(left_box)

        center_box = BoxLayout(orientation='horizontal')
        self.status_lbl = Label(
            text="Stato: pronto",
            color=(0, 1, 0, 1),
            font_size="18sp",
            halign="center",
            valign="middle",
            bold=True
        )
        self.status_lbl.bind(size=lambda obj, val: setattr(obj, "text_size", val))
        center_box.add_widget(self.status_lbl)
        header.add_widget(center_box)
        header.add_widget(Widget(size_hint_x=None, width=dp(80)))
        self.layout.add_widget(header)

        # PULSANTI PRINCIPALI
        actions = [
            ("Consiglia mossa", self.consiglia_mossa),
            ("Consiglia puntata", self.consiglia_puntata),
            ("Reset mano", self.reset_mano)
        ]
        for text, func in actions:
            btn = MenuButton(text=text)
            btn.bind(on_release=lambda instance, f=func: f())
            self.layout.add_widget(btn)
            self.all_buttons.append(btn)

        # OUTPUT
        self.output_lbl = Label(
            text="",
            color=CURRENT_THEME["fg"],
            font_size="16sp",
            halign="center",
            valign="middle",
            bold=True
        )
        self.output_lbl.bind(size=lambda obj, val: setattr(obj, "text_size", val))
        self.layout.add_widget(self.output_lbl)
        self.add_widget(self.layout)

        # MENU LATERALE
        self.menu_layout = ColoredBoxLayout(
            orientation='vertical',
            size_hint=(None, 1),
            width=dp(250),
            pos_hint={'x': -1, 'y': 0},
            padding=dp(10),
            spacing=dp(8),
            background_color=CURRENT_THEME["menu_bg"]
        )

        top_bar = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40))
        top_bar.add_widget(Widget())
        close_btn = CloseButton(on_close=self.toggle_menu)
        top_bar.add_widget(close_btn)
        self.menu_layout.add_widget(top_bar)

        for label in ["Training base", "Conteggio carte", "Strategia base"]:
            b = MenuButton(text=label)
            self.menu_layout.add_widget(b)
            self.all_buttons.append(b)

        # === NUOVO PULSANTE EXPORT DATA (corretto) ===
        self.export_btn = MenuButton(text="Export Data")
        self.export_btn.bind(on_release=self.export_data)
        self.menu_layout.add_widget(self.export_btn)
        self.all_buttons.append(self.export_btn)

        theme_btn = MenuButton(text="Cambia tema")
        theme_btn.bind(on_release=self.toggle_theme)
        self.menu_layout.add_widget(theme_btn)
        self.all_buttons.append(theme_btn)

        self.add_widget(self.menu_layout)

    # === FUNZIONE EXPORT CORRETTA ===
    def export_data(self, instance):
        try:
            instance.text = "📦 Esportazione..."
            instance.disabled = True
            create_backup_zip()
            send_telegram_message("✅ Backup esportato con successo!")
            log_event("export_data", "success", None, None, CURRENT_THEME)
            instance.text = "✅ Esportato!"
        except Exception as e:
            send_telegram_message(f"❌ Errore export: {e}")
            log_error(traceback.format_exc())
            instance.text = "❌ Errore!"
        finally:
            # Ripristino dopo 2 secondi
            Clock.schedule_once(lambda dt: self._reset_export_button(instance), 2)

    def _reset_export_button(self, instance):
        instance.text = "Export Data"
        instance.disabled = False
        instance.state = "normal"

    # === AGGIORNA SFONDO ===
    def _update_bg(self, *args):
        self.bg_rect.size = self.layout.size
        self.bg_rect.pos = self.layout.pos

    # === CAMBIO TEMA ===
    def toggle_theme(self, *args):
        global CURRENT_THEME
        going_to_light = (CURRENT_THEME is THEME_DARK)
        CURRENT_THEME = THEME_LIGHT if going_to_light else THEME_DARK
        save_theme(CURRENT_THEME is THEME_LIGHT)
        Window.clearcolor = CURRENT_THEME["bg"]
        self._root_bg_color.rgba = CURRENT_THEME["bg"]
        self.refresh_theme()
        log_event("cambia_tema", "Light" if going_to_light else "Dark", None, None, CURRENT_THEME)

    def refresh_theme(self):
        for btn in self.all_buttons:
            if isinstance(btn, MenuButton):
                btn.update_theme()
        self.output_lbl.color = CURRENT_THEME["fg"]
        self.menu_layout.background_color = CURRENT_THEME["menu_bg"]
        self.status_lbl.color = (0, 1, 0, 1)

    # === FUNZIONI DI GIOCO ===
    def consiglia_mossa(self):
        try:
            mosse = ["HIT", "STAND", "DOUBLE", "SPLIT"]
            scelta = random.choice(mosse)
            tc = round(random.uniform(-1.5, 2.5), 1)
            edge = round(random.uniform(-5, 5), 1)
            self.output_lbl.text = f"Suggerimento: {scelta} | TC={tc} | edge={edge}%"
            self.status_lbl.text = "Stato: calcolato"
            self.status_lbl.color = (0, 0.7, 1, 1)
            log_event("consiglia_mossa", scelta, tc, edge, CURRENT_THEME)
        except Exception:
            log_error(traceback.format_exc())
            self.status_lbl.text = "Errore: calcolo mossa"
            self.status_lbl.color = (1, 0, 0, 1)

    def consiglia_puntata(self):
        try:
            edge = round(random.uniform(-5, 5), 1)
            bet = "x2 base bet" if edge > 1 else "½ base bet" if edge < -1 else "base bet"
            self.output_lbl.text = f"Consiglio puntata: {bet} (edge {edge}%)"
            self.status_lbl.text = "Stato: pronto"
            self.status_lbl.color = (0, 1, 0, 1)
            log_event("consiglia_puntata", bet, 0, edge, CURRENT_THEME)
        except Exception:
            log_error(traceback.format_exc())
            self.status_lbl.text = "Errore: puntata"
            self.status_lbl.color = (1, 0, 0, 1)

    def reset_mano(self):
        try:
            self.output_lbl.text = ""
            self.status_lbl.text = "Stato: pronto"
            self.status_lbl.color = (0, 1, 0, 1)
        except Exception:
            log_error(traceback.format_exc())
            self.status_lbl.text = "Errore: reset"
            self.status_lbl.color = (1, 0, 0, 1)

    # === MENU LATERALE ===
    def toggle_menu(self):
        Animation(pos_hint={'x': 0 if not self.menu_open else -1, 'y': 0}, duration=0.3).start(self.menu_layout)
        self.menu_open = not self.menu_open

# === SCHERMATA ROOT ===
class RootUI(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(MainScreen(name="main"))

# === APP ===
class BlackjackApp(App):
    def build(self):
        return RootUI()

if __name__ == '__main__':
    BlackjackApp().run()
