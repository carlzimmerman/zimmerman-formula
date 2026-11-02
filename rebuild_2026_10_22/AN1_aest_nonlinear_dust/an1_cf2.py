#!/usr/bin/env python3
"""AN1 post-result (A2): does the strict-line (1e-4) fold converge with N? Run: python3 an1_cf2.py checks"""
import os, sys
sys.argv = [sys.argv[0], "x"]
import an1
d = list(an1.integrate.__defaults__); d[0] = 1e-4; an1.integrate.__defaults__ = tuple(d)
rows = []
for key, mu, amp in [("1e12", 0.0156, 1.0), ("1e12", 10.0, 1.0), ("1e12", 56.6, 1.0), ("1e12", 1.0, 3.0), ("1e15", 1.0, 1.0), ("1e15", 56.6, 1.0), ("1e15", 1.0, 3.0)]:
    for N in (750, 3000):
        rows.append(dict(key=key, mu=mu, foot="canonical", amp=amp, N=N))
an1.run_list(rows, os.path.join(an1.HERE, "an1_cf2.jsonl"))
