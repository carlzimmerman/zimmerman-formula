#!/usr/bin/env python3
"""Read-only watcher: scientific claims are never inferred from counters."""
import json, sys
from config import CONFIG
def main():
    p=CONFIG['runtime']/'status.json'
    s=json.loads(p.read_text()) if p.exists() else {'state':'stopped','attempts':0}
    if '--prompt' in sys.argv:
        print('Report process state, candidates, tested doors and Lean checks separately. A pass is not scientific truth or novelty. Stopped can be intentional.')
    print(json.dumps(s,indent=2))
if __name__=='__main__': main()
