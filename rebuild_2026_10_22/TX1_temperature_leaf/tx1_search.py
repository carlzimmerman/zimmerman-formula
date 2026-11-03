#!/usr/bin/env python3
"""TX1 search: BK2's bk2_search.main by import with s2. python3 -I tx1_search.py FOOT ARM LEVEL. ARM real|c1|c2|c3|label|p1|p2|mutate. LEVEL T0 1500, TL0 15000, TL1 30000. BK2's L2 code path (inside-search G3 test), T5 skipped by pre-marking. Chunks: chunks/L2_FOOT_ARM_LEVEL. SIGTERM checkpoints. kappa = 1/2 FITTED; not theory closed."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tx1_lib import *
foot, arm, lev = sys.argv[1:4]; cap = dict(T0=1500, TL0=15000, TL1=30000)[lev]; S = install((arm, cap)); mode = "mutate" if arm == "mutate" else f"{arm}_{lev}"
W = os.path.join(LANE, "chunks", f"L2_{foot}_{mode}"); os.makedirs(W, exist_ok=True); d = os.path.join(W, "done.txt")
if not os.path.exists(d): open(d, "w").write("\n".join(t5_tags()) + "\n")
sys.argv = ["bk2_search.py", foot, mode, "L2"]; S.main()
