from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.animation import Animation

class SplashScreen(Screen):
    def on_enter(self):
        title = Label(text="🂡 Blackjack AI Genius", font_size='32sp', opacity=0)
        subtitle = Label(text="Powered by AI Genius Engine", font_size='18sp', opacity=0, pos_hint={'center_y': 0.4})
        self.add_widget(title)
        self.add_widget(subtitle)

        Animation(opacity=1, d=1).start(title)
        Animation(opacity=1, d=1, t='out_quad').start(subtitle)
        Clock.schedule_once(lambda dt: setattr(self.manager, 'current', 'main'), 2.5)
