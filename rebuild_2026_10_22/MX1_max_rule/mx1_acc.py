#!/usr/bin/env python3
"""Runs RQ3's acceptance.py, logic unedited, with outputs and caches redirected into this lane. Usage: python3 mx1_acc.py cand_P.py [--no-keys] [--no-bullet]"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); RQ = os.path.join(os.path.dirname(HERE), "RQ3_acceptance_v2"); p = os.path.join(RQ, "acceptance.py"); s = open(p).read(); OUTD = os.path.join(HERE, "acc")
a = 'HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); REPO'; assert s.count(a) == 1; s = s.replace(a, f'OUTD = {OUTD!r}; ' + a)
for x in ('os.path.join(HERE, "cache_crg"', 'os.path.join(HERE, f"cache_keys"', 'os.path.join(HERE, "results"', 'os.path.join(HERE, "cache_keys"'):
    assert s.count(x) >= 1, x; s = s.replace(x, x.replace("HERE,", "OUTD,"))
g = {"__name__": "__main__", "__file__": p}; exec(compile(s, p, "exec"), g)
