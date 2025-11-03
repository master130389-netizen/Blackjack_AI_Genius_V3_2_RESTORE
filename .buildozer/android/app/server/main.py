# Blackjack AI Genius - Hybrid Engine (FastAPI)
from fastapi import FastAPI, Header
from pydantic import BaseModel
from typing import Optional, List
import json, os, math, time

app = FastAPI(title='Blackjack AI Genius - Hybrid Engine')

# engine store
DATA_FILE = os.path.join(os.path.dirname(__file__), 'engine_store.json')
EDGE_FILE = os.path.join(os.path.dirname(__file__), 'edge_lookup.json')
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump({'tc_stats':{}, 'hands_logged':[]}, f)
if not os.path.exists(EDGE_FILE):
    # default fallback edge map
    default = {str(k):v for k,v in { -5:-0.02, -4:-0.015, -3:-0.01, -2:-0.005, -1:-0.002, 0:0.0, 1:0.005, 2:0.01, 3:0.015, 4:0.02, 5:0.025, 6:0.03}.items()}
    with open(EDGE_FILE, 'w', encoding='utf-8') as f:
        json.dump(default, f, indent=2)

def read_store():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)
def write_store(d):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(d, f, indent=2)

def read_edge_map():
    with open(EDGE_FILE, 'r', encoding='utf-8') as f:
        return {int(k):v for k,v in json.load(f).items()}

# helpers
def hand_total(cards):
    total=0; aces=0
    for c in cards:
        s=str(c).upper()
        if s in ['J','Q','K']: total+=10
        elif s=='A': total+=11; aces+=1
        else:
            try: total+=int(s)
            except: pass
    while total>21 and aces>0:
        total-=10; aces-=1
    return total

def dealer_value(card):
    c=str(card).upper()
    if c in ['J','Q','K']: return 10
    if c=='A': return 11
    try: return int(c)
    except: return 0

def estimate_decks_remaining(cards_seen_count, shoe_decks):
    cards_total = shoe_decks * 52.0
    decks_remaining = max(0.5, (cards_total - cards_seen_count) / 52.0)
    return decks_remaining

def calculate_true_count(running_count, cards_seen_count, shoe_decks):
    decks_rem = estimate_decks_remaining(cards_seen_count, shoe_decks)
    return running_count / decks_rem

# simple basic strategy stub
def basic_strategy(player_cards, dealer_up):
    total = hand_total(player_cards)
    if len(player_cards)==2 and player_cards[0]==player_cards[1] and player_cards[0] in ['A','8']:
        return 'split'
    if total>=17: return 'stand'
    if 13<=total<=16:
        if dealer_value(dealer_up) in [2,3,4,5,6]: return 'stand'
        return 'hit'
    if total==12:
        if dealer_value(dealer_up) in [4,5,6]: return 'stand'
        return 'hit'
    return 'hit'

# bet sizing (fractional Kelly)
SD_PER_UNIT = 1.15
VAR_PER_UNIT = SD_PER_UNIT**2
def kelly_bet(bankroll, edge_est, fraction=0.5, bet_min=1.0, max_bet_pct=0.05):
    if edge_est<=0: return 0.0
    k_frac = edge_est / VAR_PER_UNIT
    applied = fraction * k_frac
    bet = applied * bankroll
    max_bet = max(bet_min, max_bet_pct * bankroll)
    bet = max(bet_min, min(bet, max_bet))
    return round(bet,2)

# API models
class SuggestIn(BaseModel):
    player_cards: List[str]
    dealer_upcard: str
    running_count: int = 0
    cards_seen_count: int = 0
    shoe_decks: float = 6.0
    bankroll: float = 1000.0
    bet_min: float = 1.0
    request_bet: bool = False
    user_profile: Optional[str] = "standard"

class SuggestOut(BaseModel):
    move: str
    split_recommended: Optional[bool] = False
    bet_suggestion: Optional[float] = None
    true_count: float = 0.0
    edge_est: float = 0.0
    confidence: float = 0.0
    explain: Optional[str] = None

@app.post("/suggest_move", response_model=SuggestOut)
def suggest_move(payload: SuggestIn):
    tc = calculate_true_count(payload.running_count, payload.cards_seen_count, payload.shoe_decks)
    base = basic_strategy(payload.player_cards, payload.dealer_upcard)
    edge_map = read_edge_map()
    edge_est = edge_map.get(int(math.floor(tc)), 0.0)
    bet_suggestion = None
    if payload.request_bet:
        bet_suggestion = kelly_bet(payload.bankroll, edge_est, fraction=0.5, bet_min=payload.bet_min)
        if payload.user_profile=='prudente':
            bet_suggestion = round(bet_suggestion*0.5,2)
        elif payload.user_profile=='aggressivo':
            bet_suggestion = round(min(bet_suggestion*1.5, payload.bankroll*0.1),2)
    confidence = min(1.0, max(0.0, 0.5 + 0.1*tc))
    explain = f"TC={tc:.2f}; base={base}; edge_est={edge_est:.3%}"
    return {"move":base, "split_recommended": (base=='split'), "bet_suggestion":bet_suggestion, "true_count":round(tc,2), "edge_est":round(edge_est,4), "confidence":round(confidence,2), "explain":explain}

class OutcomeIn(BaseModel):
    player_cards: List[str]
    dealer_upcard: str
    bet: float
    profit: float
    running_count: int
    cards_seen_count: int
    shoe_decks: float = 6.0

@app.post("/log_outcome")
def log_outcome(payload: OutcomeIn):
    store = read_store()
    tc = calculate_true_count(payload.running_count, payload.cards_seen_count, payload.shoe_decks)
    tc_bin = int(math.floor(tc))
    stats = store.get('tc_stats', {})
    bin_entry = stats.get(str(tc_bin), {"count":0, "ema_edge":0.0})
    observed = (payload.profit / payload.bet) if payload.bet>0 else 0.0
    alpha = 0.05
    prev = bin_entry.get('ema_edge', 0.0)
    count = bin_entry.get('count', 0) + 1
    new_ema = alpha*observed + (1-alpha)*prev
    bin_entry['ema_edge'] = new_ema
    bin_entry['count'] = count
    stats[str(tc_bin)] = bin_entry
    store['tc_stats'] = stats
    store.setdefault('hands_logged', []).append({"ts":time.time(), "tc":tc, "bet":payload.bet, "profit":payload.profit})
    write_store(store)
    return {"ok":True, "tc_bin":tc_bin, "ema_edge":new_ema, "count":count}

@app.get("/simulate_edge_map")
def simulate_edge_map():
    # runs a quick Monte Carlo to build a coarse map TC -> edge (demo)
    import random, math
    edge_map = {}
    for tc in range(-6,11):
        # simulate many hands and estimate edge per unit
        trials = 2000
        bet_unit = 1.0
        sd_unit = 1.15
        results = []
        for _ in range(trials):
            r = random.gauss(0.01*tc*bet_unit, sd_unit*bet_unit)  # simplistic scaling
            results.append(r)
        # edge per unit is mean / bet_unit
        edge_map[tc] = sum(results)/len(results)/bet_unit
    # save file
    with open(os.path.join(os.path.dirname(__file__), 'edge_lookup.json'), 'w', encoding='utf-8') as f:
        json.dump({str(k):v for k,v in edge_map.items()}, f, indent=2)
    return {"ok":True, "edge_map_sample": {k:edge_map[k] for k in sorted(list(edge_map.keys()))[:7]} }
