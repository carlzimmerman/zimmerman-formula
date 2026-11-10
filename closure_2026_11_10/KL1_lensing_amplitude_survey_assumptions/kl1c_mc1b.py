#!/usr/bin/env python3
"""KL1 PART C, AMENDMENT C1 (post hoc, fe976ca7d3): MUTATE arm MC1b. f = 0.2 across the stack's mass range (choice (a)) must move
R_tot at k 5 by at least 0.02 against C1 off (A3, RB1's ladder). Reads the layouts kl1c_gas.py saved; computes nothing new.

  python3 kl1c_mc1b.py     -> kl1c_mc1b_MUTATE.json, kl1c_mc1b_MUTATE.out
kappa = 1/2 FITTED; footings never pooled; not theory closed; adopts nothing."""
import os, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
G = json.load(open(os.path.join(HERE, "kl1c_gas.json"))); M = json.load(open(os.path.join(HERE, "kl1c_gas_MUTATE.json"))); K = np.array(G["k"])
RES = dict(lane="KL1", arm="MC1b (MUTATE, AMENDMENT C1, post hoc)", amendment="fe976ca7d3", note="kappa = 1/2 FITTED; not theory closed", rows={}); OUT = []
for ft in ("canonical", "alt"):
    off = np.array(G["rows"][ft]["A3_NR"]["R_tot"]); mut = np.array(M["rows"][ft]["MC1"]["R_tot"])
    d = {str(k): float(np.interp(k, K, mut) - np.interp(k, K, off)) for k in (1.0, 3.0, 5.0)}
    RES["rows"][ft] = dict(dR=d, bites=bool(abs(d["5.0"]) >= 0.02))
    OUT.append(f"[{ft}] MC1b f = 0.2 in the stack's range against C1 off: R_tot moves {d['1.0']:+.3f} at k 1, {d['3.0']:+.3f} at k 3, {d['5.0']:+.3f} at k 5 -> "
               f"{'bites' if RES['rows'][ft]['bites'] else 'DOES NOT BITE'} (line 0.02 at k 5)")
print("\n".join(OUT))
json.dump(RES, open(os.path.join(HERE, "kl1c_mc1b_MUTATE.json"), "w"), indent=1)
open(os.path.join(HERE, "kl1c_mc1b_MUTATE.out"), "w").write("\n".join(OUT) + "\n")
