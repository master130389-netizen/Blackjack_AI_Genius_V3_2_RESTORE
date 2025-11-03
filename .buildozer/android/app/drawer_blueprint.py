from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class DrawerMenu(BoxLayout):
    def __init__(self, on_select_callback=None, **kwargs):
        super().__init__(orientation='vertical', spacing=10, padding=10, **kwargs)
        self.callback = on_select_callback

        self.add_widget(Label(text='⚙️ Menu Principale', font_size='20sp', size_hint_y=None, height=60))

        buttons = [
            ("🎓 Modalità Training", "training"),
            ("🧠 AI Boost", "boost"),
            ("📊 Statistiche", "stats"),
            ("🌐 Impostazioni", "settings"),
            ("📘 Guida alle Mosse", "guide"),
            ("💬 Feedback & Supporto", "feedback")
        ]

        for text, action in buttons:
            btn = Button(text=text, size_hint_y=None, height=50)
            btn.bind(on_release=lambda instance, a=action: self.on_select(a))
            self.add_widget(btn)

    def on_select(self, action):
        if self.callback:
            self.callback(action)
