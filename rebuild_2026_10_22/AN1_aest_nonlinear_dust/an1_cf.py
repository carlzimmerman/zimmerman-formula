#!/usr/bin/env python3
"""AN1 post-result robustness (AMENDMENT A2): rerun P1 A1/A2 rows, both footings, with the fold line tightened 1e-2 -> 1e-4,
to see whether a row called a fold keeps closing or bounces. Separate output. Run: python3 an1_cf.py checks"""
import json, os, sys
sys.argv = [sys.argv[0], "x"]
import an1
d = list(an1.integrate.__defaults__)
d[0] = 1e-4
an1.integrate.__defaults__ = tuple(d)
rows = [c for c in an1.grid() if c.get("KB", 0) == 0 and c.get("MGdiv", 1) == 1]
an1.run_list(rows, os.path.join(an1.HERE, "an1_cf1e-4.jsonl"))
