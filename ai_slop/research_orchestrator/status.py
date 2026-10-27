"""Read-only v2 monitor interface."""
import json
from config import CONFIG
def load():
    p=CONFIG['runtime']/'status.json'
    return json.loads(p.read_text()) if p.exists() else {'state':'stopped','attempts':0}
