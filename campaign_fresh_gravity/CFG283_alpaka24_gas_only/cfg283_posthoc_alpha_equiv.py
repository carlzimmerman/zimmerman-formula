#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG283 POST-HOC addendum (written AFTER the main run, MUTATE=1 and the SELFTEST were committed; NOT a frozen item): the CO conversion alpha_CO at which ADF22.5's measured g_obs
is reproduced exactly (median residual zero, CFG223's estimator) by each law's a0 at z = 3.094: FLAT (s = 1), the rival a0 ~ H(z) and CFG223's PROXY curve.  Closed form on the main run's committed
g_obs and the B1 g_bar (g_bar is linear in alpha_CO for a fixed disc): s*(alpha) is solved by bisection on log alpha.  Inputs are read from cfg283_stageB_results.json (the main run).
It adds no data and no knob; it reads the main run's numbers in the units a reader can compare with the two declared conversions (0.8 lower limit, 4.36 Galactic).  kappa = 1/2 is FITTED.  No verdict words.
"""
import os, sys, json, math
sys.dont_write_bytecode = True
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); CFG = os.path.dirname(HERE); REPO = os.path.dirname(CFG)
sys.path.insert(0, os.path.join(CFG, "HZQ_common"))
import hzq_core as H

main = json.load(open(os.path.join(HERE, "cfg283_stageB_results.json")))["numbers"]["rows"]["B1"]
GO, GB1, Z = main["GO"], main["GB"], main["z"]
LOG = []
def P(s=""):
    print(s); LOG.append(str(s))
P("CFG283 POST-HOC addendum (written after the main run, MUTATE=1 and the SELFTEST were committed; not a frozen item): the CO conversion alpha_CO at which each law reproduces the measured g_obs of ADF22.5 exactly"); P("")
P(f"inputs from the main run: g_obs {GO:.4e}, g_bar(B1, alpha 0.8) {GB1:.4e}, z {Z:.3f}")

def log_s(alpha):
    gb = GB1 * alpha / 0.8
    ls, st = H.s_status(np.array([GO / gb]), np.array([gb]))
    return ls, st

rows = []
for nm in ("FLAT", "H(z)", "PROXY"):
    s_law = H.LAWS[nm](Z)
    lo, hi = math.log10(0.8), math.log10(GO / GB1 * 0.8) - 1e-9            # alpha from the lower limit up to the floor boundary D = 1
    for _ in range(200):
        mid = 0.5 * (lo + hi); ls, st = log_s(10 ** mid)
        if st == "root" and ls > math.log10(s_law): lo = mid                # s* too high: more gas needed
        else: hi = mid
    a = 10 ** (0.5 * (lo + hi)); ls, st = log_s(a)
    M = a * 3.0e10
    rows.append(dict(law=nm, s_law=s_law, alpha_CO=a, M_gas=M, check_log10_s=ls - math.log10(s_law), status=st))
    P(f"  {nm:6s} s = {s_law:.3f}: alpha_CO = {a:.3f} (M_gas {M:.3e} Msun; {a / 0.8:.2f} x the lower limit, {a / 4.36:.2f} x the Galactic value); check log10 s*/s_law {ls - math.log10(s_law):+.2e} ({st})")
da = math.log10(rows[0]["alpha_CO"] / rows[1]["alpha_CO"])
P(f"\n  the FLAT and H(z) laws need conversions that differ by {da:.3f} dex; the two declared conversions differ by {math.log10(4.36 / 0.8):.3f} dex (0.8 -> 4.36), and the floor boundary (D = 1) is alpha_CO = {main['alpha_D1']:.3f}.")
open(os.path.join(HERE, "cfg283_posthoc_alpha_equiv.out"), "w").write("\n".join(LOG).replace(REPO, "<repo>") + "\n")
json.dump(dict(rows=rows, dex_between_FLAT_and_Hz=da), open(os.path.join(HERE, "cfg283_posthoc_alpha_equiv_results.json"), "w"), indent=1)
