# -*- coding: utf-8 -*-
"""
Blackjack AI Genius V3 – versione PC stabile (fase 4.2)
Drawer laterale + AI Boost + Export + Tema dinamico
"""

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.modalview import ModalView
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
import traceback

# === Moduli interni ===
from theme_config import THEMES, get_contrasting_text
from data_logger import log_event, log_error
from export_manager import export_all
from telegram_manager import notify_success, notify_error

# === Drawer laterale ===
class SideDrawer(ModalView):
    def __init__(self, parent_screen, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, 1)
        self.width = dp(220)
        self.auto_dismiss = True
        self.background_color = (0, 0, 0, 0)
        self.parent_screen = parent_screen

        layout = BoxLayout(orientation="vertical", padding=dp(10), spacing=dp(8))
        self.add_widget(layout)
        self.buttons = []

        items = [
            ("Home", self.dismiss),
            ("Change Theme", parent_screen.change_theme),
            ("Export Data", parent_screen.export_data),
            ("AI Didactic", self.dismiss),
            ("Review Bonus", self.dismiss),
            ("Exit", self.dismiss),
        ]

        for txt, cb in items:
            b = Button(text=txt, size_hint_y=None, height=dp(45))
            b.bind(on_release=lambda inst, c=cb: c())
            layout.add_widget(b)
            self.buttons.append(b)

    def apply_theme(self, theme):
        for b in self.buttons:
            b.background_normal = ""
            b.background_down = ""
            b.background_color = theme["primary"]
            b.color = theme["primary_text"]


# === Schermata principale ===
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_names = list(THEMES.keys())
        self.theme_idx = 0
        self.current_theme = THEMES[self.theme_names[self.theme_idx]]
        self.ai_boost_active = False

        self.root_layout = FloatLayout()
        self.add_widget(self.root_layout)

        # === Sfondo ===
        with self.root_layout.canvas.before:
            Color(*self.current_theme["background"])
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_bg, pos=self._update_bg)

        # === Pulsante Menu ☰ ===
        self.menu_btn = Button(
            text="☰",
            size_hint=(None, None),
            size=(dp(55), dp(55)),
            pos_hint={"x": 0.02, "top": 0.98},
            background_normal="",
            background_color=self.current_theme["primary"],
            color=self.current_theme["primary_text"],
            font_size="26sp",
        )
        self.menu_btn.bind(on_release=self.open_drawer)
        self.root_layout.add_widget(self.menu_btn)

        # === Pulsante AI Boost ===
        self.ai_btn = Button(
            text="AI Boost",
            size_hint=(None, None),
            size=(dp(120), dp(55)),
            pos_hint={"x": 0.18, "top": 0.98},
            background_normal="",
            background_color=self.current_theme["accent"],
            color=self.current_theme["primary_text"],
            font_size="18sp",
            bold=True
        )
        self.ai_btn.bind(on_release=self.toggle_ai_boost)
        self.root_layout.add_widget(self.ai_btn)

        # === Etichetta titolo ===
        self.title_lbl = Label(
            text="Blackjack AI Genius V3",
            pos_hint={"center_x": 0.5, "top": 0.93},
            color=self.current_theme["primary_text"],
            font_size="22sp",
            bold=True
        )
        self.root_layout.add_widget(self.title_lbl)

        # === Pulsante Export ===
        self.export_btn = Button(
            text="Export Data",
            size_hint=(0.4, None),
            height=dp(50),
            pos_hint={"center_x": 0.5, "y": 0.05},
            background_normal="",
            background_color=self.current_theme["primary"],
            color=self.current_theme["primary_text"],
            bold=True
        )
        self.export_btn.bind(on_release=self.export_data)
        self.root_layout.add_widget(self.export_btn)

        # === Label stato ===
        self.status_lbl = Label(
            text="Ready",
            size_hint=(1, None),
            height=dp(30),
            pos_hint={"center_x": 0.5, "y": 0},
            color=self.current_theme["primary_text"],
            font_size="14sp"
        )
        self.root_layout.add_widget(self.status_lbl)

        # === Drawer laterale ===
        self.drawer = SideDrawer(self)

        # Applica il tema iniziale
        self.apply_theme()

    # === Gestione background ===
    def _update_bg(self, *args):
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos

    # === Gestione Drawer ===
    def open_drawer(self, *args):
        self.drawer.open()

    # === Cambio tema ===
    def change_theme(self, *args):
        try:
            self.theme_idx = (self.theme_idx + 1) % len(self.theme_names)
            self.current_theme = THEMES[self.theme_names[self.theme_idx]]
            self.apply_theme()
            msg = f"Tema cambiato in: {self.theme_names[self.theme_idx]}"
            self.status_lbl.text = msg
            log_event("change_theme", msg)
            notify_success(msg)
        except Exception as e:
            log_error(f"Errore cambio tema: {e}")
            self.status_lbl.text = "Errore cambio tema"

    def apply_theme(self):
        theme = self.current_theme
        Color(*theme["background"])
        self.bg_rect.size = self.size
        self.bg_rect.pos = self.pos
        for btn in [self.menu_btn, self.export_btn, self.ai_btn]:
            btn.background_color = theme["primary"]
            btn.color = theme["primary_text"]
        self.drawer.apply_theme(theme)
        self.status_lbl.color = theme["primary_text"]
        self.title_lbl.color = theme["primary_text"]

    # === AI Boost ===
    def toggle_ai_boost(self, *args):
        self.ai_boost_active = not self.ai_boost_active
        if self.ai_boost_active:
            self.ai_btn.background_color = self.current_theme["accent"]
            self.status_lbl.text = "AI Boost attivo"
            notify_success("AI Boost attivato")
        else:
            self.ai_btn.background_color = self.current_theme["primary"]
            self.status_lbl.text = "AI Boost disattivato"
            notify_error("AI Boost disattivato")

    # === Export Data ===
    def export_data(self, *args):
        try:
            self.status_lbl.text = "Export in corso..."
            path = export_all()
            log_event("export", f"Export completato: {path}")
            self.status_lbl.text = "Export completato"
            notify_success("Export completato con successo")
        except Exception as e:
            log_error(f"Errore export: {e}")
            self.status_lbl.text = "Export fallito"
            notify_error(f"Errore export: {e}")


# === App Root ===
class RootUI(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(MainScreen(name="main"))


class BlackjackApp(App):
    title = "Blackjack AI Genius V3"
    def build(self):
        notify_success("Avvio Blackjack AI Genius V3 - Drawer laterale stabile")
        return RootUI()


if __name__ == "__main__":
    try:
        BlackjackApp().run()
    except Exception as e:
        log_error(f"Crash globale: {e}")
        notify_error(f"Crash in App principale: {e}")
