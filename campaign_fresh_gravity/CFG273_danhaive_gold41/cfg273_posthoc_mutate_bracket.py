#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG273 POST HOC (labelled; written and run AFTER the MUTATE=1 run FAILED its count clause): why do fewer rows have a root when every M_dyn is multiplied by 4?
Reporting only: nothing in the frozen measurement depends on this file.  For every row without a root in the mutated run it computes, by the closed-form inversion of nu_mono for the row's own (D, g_bar),
the s* that the row would have, and compares it with the solver's bracket (log10 s in [-3, +3]).  kappa = 1/2 FITTED.
"""
import os, sys, json, math
sys.dont_write_bytecode = True
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "HZQ_common"))
import hzq_core as H
main = json.load(open(os.path.join(HERE, "cfg273_stageB_results.json")))["numbers"]["rows"]
mut = json.load(open(os.path.join(HERE, "cfg273_stageB_MUTATE1_results.json")))["numbers"]["rows"]
ids = [k for k in main if k.isdigit()]


def inv_nu(Dv):
    lo, hi = -25.0, 25.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if float(H.NU(np.array([math.exp(mid)]))[0]) > Dv: lo = mid
        else: hi = mid
    return math.exp(0.5 * (lo + hi))


lost, gained, out = [], [], []
for k in ids:
    a, b = main[k], mut[k]
    if (not a["no_root"]) and b["no_root"]: lost.append(k)
    if a["no_root"] and (not b["no_root"]): gained.append(k)
    if b["no_root"]:
        Dm = b["D"]
        s_closed = (b["GB"] / inv_nu(Dm) / H.A0C) if Dm > 1 else float("nan")
        out.append((k, Dm, s_closed))
print(f"main run: {sum(1 for k in ids if not main[k]['no_root'])} rows with a root; mutated run: {sum(1 for k in ids if not mut[k]['no_root'])}; lost {len(lost)}, gained {len(gained)}")
print("rows without a root in the mutated run: id, mutated D, closed-form s* (nan if D <= 1):")
for k, Dm, s in out:
    print(f"   {k}: D {Dm:.2f}  closed-form s* {s:.4g}  {'ABOVE the solver bracket (s > 1000)' if (np.isfinite(s) and s > 1000) else ('no root (D <= 1)' if not np.isfinite(s) else 'inside the bracket')}")
above = [k for k, Dm, s in out if np.isfinite(s) and s > 1000]
print(f"summary: {len(above)} of the {len(out)} rows without a root in the mutated run have a closed-form s* above 1000 (the solver's upper bracket log10 s = +3); the others have D <= 1")
open(os.path.join(HERE, "cfg273_posthoc_mutate_bracket.out"), "w").write("")
