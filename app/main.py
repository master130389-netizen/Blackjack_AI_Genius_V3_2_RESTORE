# Blackjack AI Genius - Kivy client (demo)
# Includes button "Consiglia Puntata" which requests bet suggestion only when pressed.
import json, os, threading, time
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock

CONFIG_FILE = os.path.join(os.path.dirname(__file__), "config.json")

def load_config():
    if os.path.exists(CONFIG_FILE):
        return json.load(open(CONFIG_FILE, "r", encoding='utf-8'))
    return {"server_url":"", "language":"it", "premium":False}

class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation='vertical'
        self.add_widget(Label(text="Blackjack AI Genius", font_size='20sp'))
        self.status = Label(text="Stato: pronto")
        self.add_widget(self.status)
        # Buttons: suggest move (always), request bet (explicit)
        self.suggest_move_btn = Button(text="Suggerisci mossa")
        self.suggest_move_btn.bind(on_release=self.on_suggest_move)
        self.add_widget(self.suggest_move_btn)
        self.suggest_bet_btn = Button(text="Consiglia puntata (premi per ricevere suggerimento puntata)")
        self.suggest_bet_btn.bind(on_release=self.on_suggest_bet)
        self.add_widget(self.suggest_bet_btn)
        self.info = Label(text="Premi Suggerisci mossa per ricevere la mossa. Premi Consiglia puntata per ricevere solo la puntata.")
        self.add_widget(self.info)

    def _call_server(self, payload, callback):
        cfg = load_config()
        url = cfg.get('server_url','').rstrip('/')
        if not url:
            # local mode simulation
            Clock.schedule_once(lambda dt: callback({'move':'stand','split_recommended':False,'true_count':0.0,'edge_est':0.0,'confidence':0.5,'explain':'Modalità locale - suggerimento demo'}), 0)
            return
        import requests
        try:
            r = requests.post(url + '/suggest_move', json=payload, timeout=5)
            if r.status_code==200:
                callback(r.json())
            else:
                callback({'error':f'Server error {r.status_code}'})
        except Exception as e:
            callback({'error':str(e)})

    def on_suggest_move(self, instance):
        # prepare payload from UI (demo values)
        payload = {"player_cards":["A","7"], "dealer_upcard":"9", "running_count":0, "cards_seen_count":0, "shoe_decks":6.0, "bankroll":1000, "bet_min":1, "request_bet": False, "user_profile":"standard"}
        self.status.text = "Richiesta suggerimento..."
        threading.Thread(target=self._call_server, args=(payload, self._on_response)).start()

    def on_suggest_bet(self, instance):
        payload = {"player_cards":["A","7"], "dealer_upcard":"9", "running_count":0, "cards_seen_count":0, "shoe_decks":6.0, "bankroll":1000, "bet_min":1, "request_bet": True, "user_profile":"standard"}
        self.status.text = "Richiesta suggerimento puntata..."
        threading.Thread(target=self._call_server, args=(payload, self._on_response)).start()

    def _on_response(self, data):
        # run in main thread
        def upd(dt):
            if 'error' in data:
                self.status.text = "Errore: " + str(data['error'])
                return
            move = data.get('move','-')
            bet = data.get('bet_suggestion', None)
            tc = data.get('true_count',0.0)
            edge = data.get('edge_est',0.0)
            explain = data.get('explain','')
            if bet is not None:
                self.status.text = f"Suggerimento: {move.upper()} | Puntata suggerita: {bet}€ | TC={tc} | edge={edge}"
            else:
                self.status.text = f"Suggerimento: {move.upper()} | TC={tc} | edge={edge}"
            # Premium TTS - if premium and server provides TTS/audio URL, play it (demo: use local TTS)
            cfg = load_config()
            if cfg.get('premium', False):
                # On Android you'd call native TTS; here we just simulate text change
                self.info.text = "Voice (Ava): " + move.upper() + " — " + explain
        Clock.schedule_once(upd, 0)

class BJApp(App):
    def build(self):
        return MainScreen()

if __name__ == '__main__':
    BJApp().run()
