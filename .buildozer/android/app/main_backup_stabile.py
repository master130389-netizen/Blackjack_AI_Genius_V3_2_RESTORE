from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.anchorlayout import AnchorLayout
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.gridlayout import GridLayout
from kivy.uix.modalview import ModalView

Window.clearcolor = (0, 0, 0, 1)

# Classe per il menù laterale
class SideMenu(ModalView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.6, 1)
        self.auto_dismiss = True
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)

        layout.add_widget(Label(text="📘 Menu", font_size='22sp', halign='left', size_hint_y=None, height=50))
        layout.add_widget(Button(text="🏠 Home", on_release=self.dismiss))
        layout.add_widget(Button(text="🎯 Training Base", on_release=self.dismiss))
        layout.add_widget(Button(text="🧠 Conteggio Carte", on_release=self.dismiss))
        layout.add_widget(Button(text="📊 Statistiche", on_release=self.dismiss))
        layout.add_widget(Button(text="⚙️ Impostazioni", on_release=self.dismiss))

        self.add_widget(layout)

# Icona hamburger
class IconButton(ButtonBehavior, Image):
    pass

# Schermata principale
class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root = BoxLayout(orientation='vertical', padding=15, spacing=10)

        # Barra superiore con menù
        top_bar = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=10)
        menu_icon = IconButton(source='assets/menu.png', size_hint=(None, None), size=(40, 40))
        menu_icon.bind(on_release=lambda x: self.open_menu())
        title = Label(text="Blackjack AI Genius", font_size='22sp', bold=True, halign='center')
        top_bar.add_widget(menu_icon)
        top_bar.add_widget(title)

        # Corpo principale
        body = BoxLayout(orientation='vertical', spacing=12)
        body.add_widget(Label(text="Stato: pronto", font_size='18sp', halign='center', size_hint_y=None, height=40))
        body.add_widget(Label(text="Suggerimento: HIT | TC=0.3 | edge=+1.2%", font_size='16sp', halign='center', size_hint_y=None, height=35))

        # Pulsanti
        buttons = GridLayout(cols=1, spacing=10, size_hint_y=None)
        buttons.bind(minimum_height=buttons.setter('height'))

        btn_move = Button(text="💡 Suggerisci mossa", font_size='16sp', background_color=(0.3, 0.3, 0.3, 1), on_press=lambda x: self.remove_focus(x))
        btn_bet = Button(text="🎯 Consiglia puntata", font_size='16sp', background_color=(0.2, 0.5, 0.7, 1), on_press=lambda x: self.remove_focus(x))

        buttons.add_widget(btn_move)
        buttons.add_widget(btn_bet)

        # Info finale
        body.add_widget(buttons)
        body.add_widget(Label(
            text="Premi i pulsanti per ricevere i consigli sulle mosse e sulle puntate.",
            font_size='14sp', halign='center', valign='middle'
        ))

        # Scrolling se necessario
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(body)

        root.add_widget(top_bar)
        root.add_widget(scroll)

        self.add_widget(root)
        self.menu = SideMenu()

    def open_menu(self):
        self.menu.open()

    def remove_focus(self, button):
        button.background_color = (button.background_color[0], button.background_color[1], button.background_color[2], 1)

# App principale
class BlackjackApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        return sm

if __name__ == '__main__':
    BlackjackApp().run()
