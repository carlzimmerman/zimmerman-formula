#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""CFG275 post hoc (written AFTER the measurement; changes nothing): which ring made the frozen control M5 fail, and is the paper's 'consistent within the errors' met when the V_c errors are included?
Reads the digitised CSV (velocity columns) and prints per-ring differences in units of (i) the V_rot error bar (the frozen M5 reading) and (ii) V_rot and V_c (MCMC-figure) errors in quadrature. kappa = 1/2 is FITTED. No verdict words."""
import os, sys, math
sys.dont_write_bytecode = True
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__))
d = pd.read_csv(os.path.join(HERE, "lin2024_rings_digitised.csv"))
g = lambda s: d[d["series"] == s].sort_values("ring").reset_index(drop=True)
rot, con, var, fit = g("V_rot (3DFIT)"), g("V_c (constant sigma_v)"), g("V_c (varying sigma_v)"), g("V_c (mass-model fit input)")
out = []
P = lambda s: (print(s), out.append(s))
P("ring | R_kpc | (Vc_const - Vrot)/err_Vrot | (Vc_var - Vrot)/err_Vrot | frozen reading uses max(err_lo, err_hi) of V_rot | quadrature with the fit-input V_c error")
for k in range(5):
    e = max(rot.loc[k, "err_lo_kms"], rot.loc[k, "err_hi_kms"]); ef = max(fit.loc[k, "err_lo_kms"], fit.loc[k, "err_hi_kms"]); q = math.hypot(e, ef)
    P(f"  {k + 1} | {rot.loc[k, 'R_kpc']:.2f} | {(con.loc[k, 'V_kms'] - rot.loc[k, 'V_kms']) / e:+.2f} | {(var.loc[k, 'V_kms'] - rot.loc[k, 'V_kms']) / e:+.2f} | V_rot error (lo, hi) {rot.loc[k, 'err_lo_kms']:.1f}, {rot.loc[k, 'err_hi_kms']:.1f} | const {(con.loc[k, 'V_kms'] - rot.loc[k, 'V_kms']) / q:+.2f}, var {(var.loc[k, 'V_kms'] - rot.loc[k, 'V_kms']) / q:+.2f}")
vr = (var["V_kms"] - rot["V_kms"]).abs() / np.maximum(rot["err_lo_kms"], rot["err_hi_kms"])
P(f"frozen M5 reading: max |V_c(varying) - V_rot| / error = {float(vr.max()):.2f} at ring {int(vr.idxmax()) + 1} (limit 1); the V_c actually used by the lane is the fit-input series (= the constant-sigma series within 0.33 km/s)")
open(os.path.join(HERE, "cfg275_posthoc_m5.out"), "w").write("\n".join(out) + "\n")
