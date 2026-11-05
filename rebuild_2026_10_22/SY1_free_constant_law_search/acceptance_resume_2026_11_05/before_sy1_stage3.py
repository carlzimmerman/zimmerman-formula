#!/usr/bin/env python3
"""SY1 Stage 3: runs ../RQ3_acceptance_v2/acceptance.py unedited, from its own source, with this lane as its working directory, so its results and caches land here. Usage: sy1_stage3.py candidates/x.py [--no-keys] [--no-bullet]. Exposes RQ3 for sy1_read's gate 5. kappa = 1/2 FITTED; not theory closed."""
import hashlib, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.join(os.path.dirname(HERE), "RQ3_acceptance_v2", "acceptance.py"); TXT = open(SRC).read(); SHA = hashlib.sha256(TXT.encode()).hexdigest()[:16]
def load():
    n = {"__file__": os.path.join(HERE, "acceptance.py"), "__name__": "rq3_in_sy1"}; exec(compile(TXT, SRC, "exec"), n); return n
if __name__ == "__main__":
    n = {"__file__": os.path.join(HERE, "acceptance.py"), "__name__": "__main__"}; print("RQ3 acceptance.py sha256", SHA, flush=True); exec(compile(TXT, SRC, "exec"), n)
