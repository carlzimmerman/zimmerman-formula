#!/usr/bin/env python3
"""CFG258 POST HOC (labelled): a larger-sample rerun of the C4 reactivity control after its frozen second clause failed in the main run (blind statistic +29.8 % against the frozen 'changes by less than 10 %', M_b = 150 mocks).
Same function (cfg258_preflight.blind_and_tot), 600 mocks per level and a different seed; Z_tot is read from the committed main run.  Not part of the frozen criteria; the main run's C4 FAIL stays as printed."""
import os, sys, json, math, time
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np
import cfg258_preflight as X

T0 = time.time()
LOG = []
def P(s=""):
    print(s, flush=True); LOG.append(str(s))

res = json.load(open(os.path.join(HERE, "cfg258_preflight_results.json")))
X.ANCHOR["canonical"] = X.anchor_library("canonical", X.NS_LIB)
z_off, z_B = res["C4"]["z_tot_off"], res["C4"]["z_tot_B"]
P("CFG258 POST HOC: the C4 reactivity control with 600 mocks per level (the frozen run used 150); seeds 4243 (OFF) and 4244 (B)")
b_off = X.blind_and_tot(None, "canonical", M_b=600, B=60, seed=4243)
b_B = X.blind_and_tot("B", "canonical", M_b=600, B=60, seed=4244)
P(f"  Z_tot (E1, main run): {z_off:.2f} -> {z_B:.2f} (ratio {z_B / z_off:.2f})")
P(f"  blind statistic, 600 mocks: {b_off:.2f} -> {b_B:.2f} (change {100 * (b_B / b_off - 1):+.1f} %); main run (150 mocks): {res['C4']['blind_off']:.2f} -> {res['C4']['blind_B']:.2f}")
P(f"  reading: the frozen clause 'changes by less than 10 %' " + ("holds" if abs(b_B / b_off - 1) < 0.10 else "does not hold") + "; the control's purpose (the blind statistic does not fall when shared systematics are added, while Z_tot does) " +
  ("is met" if (b_B / b_off > 0.9 and z_B < 0.5 * z_off) else "is NOT met"))
json.dump(dict(blind_off=b_off, blind_B=b_B, z_tot_off=z_off, z_tot_B=z_B), open(os.path.join(HERE, "cfg258_posthoc_c4_results.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg258_posthoc_c4.out"), "w").write("\n".join(LOG) + "\n")
