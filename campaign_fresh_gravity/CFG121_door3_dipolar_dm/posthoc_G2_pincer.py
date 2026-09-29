#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
POST-HOC (written after the C1 numbers were seen; NOT part of the frozen criteria; labelled as such).
Question: how much Q^2/kappa_I does the declared dipole medium tolerate in linear growth (worst deviation <= 5% at z = 10, all four k, all
three amplitudes, both dipole ICs), and how does that compare with the Q^2/kappa_I >= 140 (f_track = 1) that B3 needs and with my hand estimate
of the free-dipole growth modification 1 + 1.5 Omega_c Q^2/kappa_I (H10)?  Also reports the measured modification at small Q^2/kappa_I.
Uses the planar solver of C_cosmology_growth.py (functions exec'd, main part skipped).  Exit 0.
"""
import os, sys, math, json
import numpy as np
import cfg121_common as C
HERE = C.HERE
src = open(os.path.join(HERE, "C_cosmology_growth.py")).read().split("def load_pstar")[0]
ns = {"__name__": "c_solver", "__file__": os.path.join(HERE, "C_cosmology_growth.py")}
exec(compile(src, "C_cosmology_growth.py(solver part)", "exec"), ns)
run, KS, AMPS, OC, OM = ns["run"], ns["KS"], ns["AMPS"], ns["OC"], ns["OM"]
FB, FD = ns["OB"] / OM, OC / OM
_r = {}


def ref(k, A):
    if (k, A) not in _r:
        _r[(k, A)] = run(k, A, "V_B", 0.0, 1.0, "cold", 100.0, 10.0)
    return _r[(k, A)]


def worst(variant, Q, kap, ks=KS, amps=AMPS, ics=("cold", "eq")):
    w = 0.0
    for k in ks:
        for A in amps:
            rf = ref(k, A)
            for ic in ics:
                r0 = run(k, A, variant, Q, kap, ic, 100.0, 10.0)
                if r0["collapsed"]:
                    return float("inf")
                tb, td = r0["ab"] / rf["ab"], r0["aD"] / rf["aD"]
                tt = (FB * r0["ab"] + FD * r0["aD"]) / (FB * rf["ab"] + FD * rf["aD"])
                w = max(w, abs(tb - 1), abs(td - 1), abs(tt - 1))
    return w


out = ["POST-HOC G2 pincer check (not frozen)"]
PSTAR = json.load(open(os.path.join(HERE, "B_budget_pincer_results.json")))["numbers"]["Pstar"]
print(out[0])
for variant in ("V_U", "V_B"):
    for pname, (Q, kap) in (("central", (1.0, 1.0)), ("star", (PSTAR[variant]["Q"], PSTAR[variant]["kappa_I"]))):
        for ic in ("cold", "eq"):
            w = worst(variant, Q, kap, ics=(ic,))
            line = f"  {variant} {pname:7s} (Q={Q:.4g}, kappa_I={kap:.3g}) dipole IC = {ic:4s}: worst growth deviation {w:.4g}  ({'PASS' if w <= 0.05 else 'FAIL'} at 5%)"
            print(line)
            out.append(line)
res = {}
for variant in ("V_U", "V_B"):
    lo, hi = 0.0, 1.0
    while worst(variant, hi, 1.0, ics=("cold",)) <= 0.05 and hi < 1e4:
        lo, hi = hi, hi * 2
    for _ in range(14):
        mid = 0.5 * (lo + hi)
        if worst(variant, mid, 1.0, ics=("cold",)) <= 0.05:
            lo = mid
        else:
            hi = mid
    Qmax = lo
    res[variant] = Qmax
    line = f"  {variant}: largest Q (kappa_I = 1, cold dipole IC only) with worst growth deviation <= 5%: Q_max = {Qmax:.4g}  (Q^2/kappa_I = {Qmax ** 2:.4g});  B3 needs Q^2/kappa_I >= 140 (f = 1); ratio needed/allowed = {140.0 / max(Qmax ** 2, 1e-30):.3g}"
    print(line)
    out.append(line)
# measured modification at small Q (V_U, k = 10, A = 1e-3, cold IC) vs hand estimate
for variant in ("V_U", "V_B"):
    for Q in (0.05, 0.1, 0.2, 0.5, 1.0):
        rf = ref(10.0, 1e-3)
        r0 = run(10.0, 1e-3, variant, Q, 1.0, "cold", 100.0, 10.0)
        tt = (FB * r0["ab"] + FD * r0["aD"]) / (FB * rf["ab"] + FD * rf["aD"]) - 1.0
        tb = r0["ab"] / rf["ab"] - 1.0
        td = r0["aD"] / rf["aD"] - 1.0
        line = f"  {variant} Q = {Q}: measured growth modification: baryons {tb:+.4f}, medium {td:+.4f}, total {tt:+.4f};  hand estimate 1.5 Omega_c Q^2/kappa_I = {1.5 * OC * Q ** 2:.4f}"
        print(line)
        out.append(line)
json.dump(dict(Qmax=res), open(os.path.join(HERE, "posthoc_G2_pincer_results.json"), "w"))
open(os.path.join(HERE, "posthoc_G2_pincer.out"), "w").write("\n".join(out) + "\n")
