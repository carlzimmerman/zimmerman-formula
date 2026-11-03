#!/usr/bin/env python3
"""Runs ../RQ3_acceptance_v2/acceptance.py unedited for HX1, from its own source, with this lane as its working directory. Usage: hx1_acc.py candidates/x.py [--no-bullet]"""
import hashlib, os
HERE = os.path.dirname(os.path.abspath(__file__)); SRC = os.path.join(os.path.dirname(HERE), "RQ3_acceptance_v2", "acceptance.py"); TXT = open(SRC).read(); SHA = hashlib.sha256(TXT.encode()).hexdigest()
def load():
    n = {"__file__": os.path.join(HERE, "acceptance.py"), "__name__": "rq3_in_hx1"}; exec(compile(TXT, SRC, "exec"), n); return n
if __name__ == "__main__":
    n = {"__file__": os.path.join(HERE, "acceptance.py"), "__name__": "__main__"}; print("RQ3 acceptance.py sha256", SHA, flush=True); exec(compile(TXT, SRC, "exec"), n)
