# -*- coding: utf-8 -*-

# Palette base (RGBA 0..1)
def rgba(hex_color, a=1.0):
    hex_color = hex_color.lstrip("#")
    r = int(hex_color[0:2], 16) / 255.0
    g = int(hex_color[2:4], 16) / 255.0
    b = int(hex_color[4:6], 16) / 255.0
    return (r, g, b, a)

def get_contrasting_text(bg_rgb):
    # bg_rgb = (r,g,b,a) -> uso solo r,g,b
    r, g, b = bg_rgb[:3]
    # luminanza semplice
    lum = 0.299 * r + 0.587 * g + 0.114 * b
    return (1,1,1,1) if lum < 0.5 else (0,0,0,1)

# === COLOR THEMES CONFIG ===
from kivy.utils import get_color_from_hex as rgba

THEMES = {
    "Dark Mode": {
        "background": rgba("#121212"),
        "primary": rgba("#1E88E5"),
        "primary_text": (1, 1, 1, 1),
        "accent": rgba("#00C853"),
        "danger": rgba("#E53935"),
        "surface": rgba("#1E88E5"),
        "text": (1, 1, 1, 1),
        "on_primary": (1, 1, 1, 1)
    },
    "Deep Blue": {
        "background": rgba("#0D47A1"),
        "primary": rgba("#1565C0"),
        "primary_text": (1, 1, 1, 1),
        "accent": rgba("#00E5FF"),
        "danger": rgba("#FF5252"),
        "surface": rgba("#1565C0"),
        "text": (1, 1, 1, 1),
        "on_primary": (1, 1, 1, 1)
    },
    "Classic Green": {
        "background": rgba("#1B5E20"),
        "primary": rgba("#2E7D32"),
        "primary_text": (1, 1, 1, 1),
        "accent": rgba("#AEEA00"),
        "danger": rgba("#D32F2F"),
        "surface": rgba("#2E7D32"),
        "text": (1, 1, 1, 1),
        "on_primary": (1, 1, 1, 1)
    },
    "Light Gray": {
        "background": rgba("#EEEEEE"),
        "primary": rgba("#90A4AE"),
        "primary_text": (0, 0, 0, 1),
        "accent": rgba("#26A69A"),
        "danger": rgba("#D32F2F"),
        "surface": rgba("#90A4AE"),
        "text": (0, 0, 0, 1),
        "on_primary": (0, 0, 0, 1)
    },
    "Vegas Gold": {
        "background": rgba("#C5A200"),
        "primary": rgba("#9E8C00"),
        "primary_text": (0, 0, 0, 1),
        "accent": rgba("#FFEE58"),
        "danger": rgba("#B71C1C"),
        "surface": rgba("#9E8C00"),
        "text": (0, 0, 0, 1),
        "on_primary": (0, 0, 0, 1)
    }
}
