from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout

def get_guide_widget():
    text = """💡 Guida alle Mosse:

• STAND → resta fermo con mano forte
• HIT → prendi un’altra carta
• DOUBLE → raddoppia la puntata
• SPLIT → dividi coppie uguali in due mani
• SURRENDER → rinuncia e perdi metà della puntata"""

    box = BoxLayout(orientation='vertical', padding=20, spacing=10, size_hint_y=None)
    label = Label(text=text, font_size='18sp', halign='left', valign='top', size_hint_y=None)
    label.bind(texture_size=label.setter('size'))
    box.add_widget(label)

    scroll = ScrollView(size_hint=(1, 1))
    scroll.add_widget(box)
    return scroll
