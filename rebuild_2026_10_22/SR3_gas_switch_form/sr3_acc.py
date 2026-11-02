#!/usr/bin/env python3
"""Runs RQ3's acceptance.py, source unchanged but for its location, with results and caches in this lane. Usage: sr3_acc.py candidates/x.py. kappa = 1/2 FITTED; not theory closed."""
import os, sys
sys.dont_write_bytecode = True
H = os.path.dirname(os.path.abspath(__file__)); RQ = os.path.join(os.path.dirname(H), "RQ3_acceptance_v2"); A = H; sys.path.insert(0, RQ)
s = open(os.path.join(RQ, "acceptance.py")).read(); a = "HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE)"; assert s.startswith(s[:s.index(a)]) and s.count(a) == 2; s = s.replace(a, f"HERE = {A!r}; RB = {os.path.dirname(H)!r}", 1)
b = "sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))"; assert s.count(b) == 1; s = s.replace(b, f"sys.path.insert(0, {RQ!r})")
os.chdir(A); sys.argv = ["acceptance.py"] + sys.argv[1:]; exec(compile(s, "acceptance.py", "exec"), {"__name__": "__main__", "__file__": os.path.join(A, "acceptance.py")})
