import os
os.environ["KIVY_NO_CONSOLELOG"] = "1"  # Disattiva i log su terminale per evitare loop
os.environ["KIVY_GL_BACKEND"] = "sdl2"

from kivy.app import App
from kivy.uix.label import Label
from kivy.config import Config

# Imposta dimensioni e posizione finestra
Config.set("graphics", "resizable", "0")
Config.set("graphics", "width", "480")
Config.set("graphics", "height", "800")
Config.set("graphics", "position", "auto")

class TestKivy(App):
    def build(self):
        return Label(
            text="✅ Kivy funziona correttamente!",
            font_size="22sp",
            color=(0, 1, 0, 1)
        )

TestKivy().run()
