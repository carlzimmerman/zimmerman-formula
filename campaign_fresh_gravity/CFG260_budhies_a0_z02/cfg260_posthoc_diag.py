#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG260 POST HOC (labelled; written and run AFTER the one frozen measurement, reads the widths): is the offset of the implied a0 a question about the gravity law, or about the width -> V -> baryon chain?
Model-independent test: D = g_obs / g_bar < 1 means the measured circular acceleration at R_HI is BELOW the Newtonian value of the baryons alone, which no gravity law (MOND, a dark halo, a vacuum field) produces.
Reported for the primary set PC and the ladder / profile-type rows, in both width frames, with the declared recipe and with the stars set to zero (gas-only baryons, a lower bound on M_b).
Reporting only: nothing in the frozen measurement depends on this file.  kappa = 1/2 FITTED; no sentence says the data favour a law.
"""
import os, sys, json, math
sys.dont_write_bytecode = True
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import cfg260_core as C

LOG = []
def P(s=""):
    print(s, flush=True); LOG.append(str(s))

GALS = C.load_galaxies(widths=True)
A0 = C.A0["canonical"]
SUB = dict(C.SUBSETS)
P("CFG260 POST HOC: D = g_obs / g_bar at R_HI from the widths (the table's widths, the frozen recipe), fraction below the Newtonian value (D < 1) and below the local-law value nu(y) (s = 1)")
P(f"  {'set':6s} {'frame':8s} {'N':>4s} | D quantiles 5/25/50/75/95 | frac D<1 | frac D<nu(y) | median D/nu(y) | s* gas-only (stars set to zero) | s* with the declared recipe")
OUT = {}
for key in ("PC", "PC125", "PC15", "P", "S4", "S5"):
    for fname, k in (("observed", 1), ("rest", 0)):
        sel = [g for g in GALS if SUB[key](g)]
        a = C.Arr(sel); W = np.array([g["w50"] for g in sel])
        rec = dict(C.REC0, k=k)
        d = C.derive(a, W, rec); ok = d["ok"]
        D = d["D"][ok]; y = d["y"][ok]
        nuy = C.nuv(C.NU, y)
        # gas-only baryons: M* = 0 (the 'tau_ms' knob cannot reach zero, so set M* by a large negative shift)
        rg = dict(rec, tau_ms=-9.0)
        lg, ug, _ = C.s_star(a, W, rg)
        l0, u0, _ = C.s_star(a, W, rec)
        OUT[f"{key}|{fname}"] = dict(n=int(ok.sum()), D_q=np.percentile(D, [5, 25, 50, 75, 95]).tolist(), frac_D_lt1=float((D < 1).mean()), frac_D_lt_nu=float((D < nuy).mean()), med_D_over_nu=float(np.median(D / nuy)),
                                     s_gas_only=10 ** lg, s_gas_only_noroot=bool(ug), s_recipe=10 ** l0, s_recipe_noroot=bool(u0))
        o = OUT[f"{key}|{fname}"]
        P(f"  {key:6s} {fname:8s} {o['n']:4d} | {np.round(o['D_q'], 2).tolist()} | {o['frac_D_lt1']:.2f} | {o['frac_D_lt_nu']:.2f} | {o['med_D_over_nu']:.2f} | {o['s_gas_only']:.3f}{' (no root)' if ug else ''} | {o['s_recipe']:.3f}{' (no root)' if u0 else ''}")
json.dump(OUT, open(os.path.join(HERE, "cfg260_posthoc_diag_results.json"), "w"), indent=1)
open(os.path.join(HERE, "cfg260_posthoc_diag.out"), "w").write("\n".join(LOG) + "\n")
