from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.properties import BooleanProperty

# Colori base (dark/light)
THEME = {
    "bg": (0, 0, 0, 1),  # sfondo nero
    "fg": (1, 1, 1, 1),  # testo bianco
    "btn": (0.1, 0.1, 0.1, 1),  # pulsanti grigio scuro
    "btn_press": (0.2, 0.2, 0.2, 1),  # colore quando premuto
}

Window.clearcolor = THEME["bg"]


# =======================
# BOTTONI E MENU
# =======================
class MenuButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_normal = ""
        self.background_color = THEME["btn"]
        self.color = THEME["fg"]
        self.font_size = "18sp"

    def on_press(self):
        self.background_color = THEME["btn_press"]

    def on_release(self):
        self.background_color = THEME["btn"]
        return super().on_release()


class DrawerMenu(BoxLayout):
    """Menù laterale scorrevole"""
    visible = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.size_hint_x = None
        self.width = dp(220)
        self.pos_hint = {"x": -1}
        self.spacing = dp(10)
        self.padding = [dp(10), dp(20)]
        self.build_menu()

    def build_menu(self):
        self.clear_widgets()
        self.add_widget(Label(text="⚙️ Menu", color=THEME["fg"], font_size="20sp", size_hint_y=None, height=dp(50)))
        buttons = [
            ("📘 Training Base", self.menu_action),
            ("🧠 AI Coach", self.menu_action),
            ("📊 Statistiche", self.menu_action),
            ("🏆 Modalità Sfida", self.menu_action),
            ("❓ Guida", self.menu_action),
        ]
        for text, action in buttons:
            btn = MenuButton(text=text, size_hint_y=None, height=dp(50))
            btn.bind(on_release=action)
            self.add_widget(btn)

    def menu_action(self, instance):
        print(f"[MENU] Hai selezionato: {instance.text}")


# =======================
# SCHERMATA PRINCIPALE
# =======================
class MainScreen(Screen):
    def __init__(self, app, **kwargs):
        super().__init__(**kwargs)
        self.app = app
        self.layout = BoxLayout(orientation="vertical", spacing=dp(10), padding=dp(10))
        self.build_ui()
        self.add_widget(self.layout)

    def build_ui(self):
        layout = self.layout

        # Header con bottone menu + label centrato
        header = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(60),
            padding=[dp(8), dp(5)],
            spacing=dp(10)
        )

        menu_btn = MenuButton(text="≡", size_hint=(None, None), width=dp(60), height=dp(50))
        menu_btn.bind(on_release=lambda *_: self.app.toggle_menu())
        header.add_widget(menu_btn)

        status_lbl = Label(
            text="Stato: pronto",
            color=THEME["fg"],
            font_size="18sp",
            halign="center",
            valign="middle",
        )
        status_lbl.bind(size=lambda obj, val: setattr(obj, "text_size", val))
        header.add_widget(status_lbl)

        # Aggiungi spazio vuoto a destra per bilanciare il layout
        header.add_widget(Widget(size_hint_x=None, width=dp(60)))
        layout.add_widget(header)

        # Corpo centrale
        center_box = BoxLayout(orientation="vertical", spacing=dp(15))

        suggestion = Label(
            text="Suggerimento: STAND | TC=0.0 | edge=0%",
            color=THEME["fg"],
            font_size="16sp",
            halign="center",
            valign="middle"
        )
        suggestion.bind(size=lambda obj, val: setattr(obj, "text_size", val))
        center_box.add_widget(suggestion)

        buttons = [
            "Consiglia mossa",
            "Consiglia puntata",
            "Reset mano",
        ]

        for text in buttons:
            btn = MenuButton(text=text, size_hint_y=None, height=dp(50))
            btn.bind(on_release=self.button_action)
            center_box.add_widget(btn)

        layout.add_widget(center_box)

    def button_action(self, instance):
        print(f"[AZIONE] Hai premuto: {instance.text}")


# =======================
# APP PRINCIPALE
# =======================
class BlackjackApp(App):
    def build(self):
        self.drawer = DrawerMenu()
        root = FloatLayout()
        self.sm = ScreenManager()
        self.main_screen = MainScreen(app=self, name="main")
        self.sm.add_widget(self.main_screen)
        root.add_widget(self.sm)
        root.add_widget(self.drawer)
        return root

    def toggle_menu(self):
        if self.drawer.visible:
            self.drawer.pos_hint = {"x": -1}
        else:
            self.drawer.pos_hint = {"x": 0}
        self.drawer.visible = not self.drawer.visible
        self.drawer.parent.do_layout()


# =======================
# AVVIO APP
# =======================
if __name__ == "__main__":
    BlackjackApp().run()
