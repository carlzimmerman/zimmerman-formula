#!/usr/bin/env python3
"""NP2 Stage 3: runs ../RQ3_acceptance_v2/acceptance.py unedited, from its own source, with this lane as its working directory, so results and caches land here (NP1's np1_stage3 pattern).
Usage: np2_stage3.py candidates/x.py [--no-keys] [--no-bullet]. kappa = 1/2 FITTED; not theory closed."""
import hashlib, os, sys
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.join(os.path.dirname(HERE), "RQ3_acceptance_v2", "acceptance.py"); TXT = open(SRC).read(); SHA = hashlib.sha256(TXT.encode()).hexdigest()[:16]
if __name__ == "__main__":
    n = {"__file__": os.path.join(HERE, "acceptance.py"), "__name__": "__main__"}; print("RQ3 acceptance.py sha256", SHA, flush=True); exec(compile(TXT, SRC, "exec"), n)
