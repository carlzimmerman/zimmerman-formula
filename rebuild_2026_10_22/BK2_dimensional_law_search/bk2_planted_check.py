#!/usr/bin/env python3
"""BK2 planted recovery at level L1: is the planted form among the hits, and does it pass G2-G5 LINE. Harvest stopped early by choice, partial counts in planted_L1_partial.out. kappa = 1/2 FITTED; not theory closed."""
import json
from bk2_lib import *
import bk2_read as Rd
W = os.path.join(HERE, "chunks", "L1_canonical_planted"); N, oa, oD = Rd.names(W); iA = {n: i for i, n in enumerate(N["A"])}; pos = {o: i for i, o in enumerate(oa)}; A = [n for n in N["A"] if n.startswith("I5((gb)") and "(a0)" in n][:3]; B = [n for n in N["A"] if "gg**2" in n and "a0**-1" in n and "pi**2" in n]; print(A, B)
want = {(pos[iA[a]], pos[iA[b]]) for a in A for b in B} | {(pos[iA[b]], pos[iA[a]]) for a in A for b in B}; found = []
for ln in open(os.path.join(W, "hits.jsonl")):
    if not ln.startswith('["T2p"'): continue
    h = json.loads(ln)
    if (h[1], h[2]) in want: found.append(h)
print("hits matching the plant", found[:4]); Gt = Rd.Gates("canonical", "planted"); s = Rd.hit_str(found[0], N, oa, oD)[0]; c = Gt.full_cheap(s); print(s, "G3", c["G3"]["mean"], c["G3"]["rms"], c["G3"]["line"], "G2", c["G2"]["rms"], c["G2"]["line"], "G5", c["G5"]["mean"], c["G5"]["rms"], c["G5"]["line"], "G4", c["G4"]["rms"], c["G4"]["line"]); assert c["G3"]["rms"] < 1e-6 and c["G2"]["rms"] < 1e-6 and c["G5"]["rms"] < 1e-6 and c["G4"]["rms"] < 1e-6; print("RECOVERED")
