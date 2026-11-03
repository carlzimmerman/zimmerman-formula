#!/usr/bin/env python3
"""TX1 MW and Bullet: BK2's bk2_dear.py source by exec, unedited on disk; chunks here. Bullet s2 = s2(14 keV) x g_gas/g_b, 14 keV PROVISIONAL. python3 -I tx1_dear.py mw|bullet FOOT LIST.json OUT.json. kappa = 1/2 FITTED; not theory closed."""
import os, shutil, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tx1_lib import *
BK = os.path.join(RB, "BK2_dimensional_law_search"); s = open(os.path.join(BK, "bk2_dear.py")).read(); a = 'HERE = os.path.dirname(os.path.abspath(__file__)); RB = os.path.dirname(HERE); sys.path.insert(0, HERE)'; assert s.count(a) == 1; s = s.replace(a, f'HERE = {LANE!r}; RB = {RB!r}; sys.path.insert(0, {BK!r})')
b = "rm = rB * KPC; L_ = dict(gs=gs, gg=gg, gb=g, r=rm,"; assert s.count(b) == 1; s = s.replace(b, f"rm = rB * KPC; L_ = dict(s2={14 * KT2S!r} * gg / np.maximum(g, 1e-300), gs=gs, gg=gg, gb=g, r=rm,")
os.makedirs(os.path.join(LANE, "chunks"), exist_ok=True); w, foot = sys.argv[1:3]
if w == "mw":
    c = os.path.join(LANE, "chunks", f"dear_mw_{foot}.json")
    if not os.path.exists(c): shutil.copyfile(os.path.join(BK, "chunks", f"dear_mw_{foot}.json"), c)
exec(compile(s, "bk2_dear_tx1", "exec"), {"__name__": "__main__", "__file__": os.path.join(LANE, "x.py")})
