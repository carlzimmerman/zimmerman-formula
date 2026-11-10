#!/usr/bin/env python3
"""MK1 row 8 reading (reported, not graded; criteria b1fbded1e2, A1 916f4e0e22): the capped branch of a point mass at the mu_K values
the other rows produce. For log M_b 9, 10, 11 (X = PD1's share) and each mu_K: cap radius r_c, the dust's own mass as a fraction of the
share, mu_K r_c, and SCS1's reading (growing band k < mu_K / sqrt(1 - K m): it reaches inside the static state only if a Jeans
wavelength 2 pi / mu_K fits inside r_c).
    python3 mk1_row8.py -> mk1_row8.json / mk1_row8.out
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys, json, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import mk1_lib as LB
ONE = json.load(open(os.path.join(HERE, "..", "ONE1_counted_once", "one1.json")))
OUT = []
def P(s=""): print(s, flush=True); OUT.append(str(s))
MUS = [0.1, 1.0, 1.5, 5.62, 7.08, 198.25, 6223.0, 25118.9]   # mu* 8.9e6 is SCS1's own bracket (x_c would fall below the solver's XMIN)
RES = dict(lane="MK1", file="mk1_row8", note=LB.NOTE, rows={})
for f in LB.FOOT:
    X = float(ONE["foot"][f]["X"]); a0 = LB.A0[f]
    for lm in (9, 10, 11):
        rM = math.sqrt(LB.G * 10 ** lm * 1.989e30 / a0)
        ms = sorted(mu / LB.MPC * rM for mu in MUS)
        br = LB.capped_branch(ms, X)
        for mu, m, p in zip(sorted(MUS), ms, br):
            if not p["ok"]:
                P(f"[{f}] log M_b {lm} mu {mu:g}: no capped state ({p['reason']})"); continue
            rc = p["xc"] * rM; frac = float(p["kap"][-1]) / X
            fits = 2 * math.pi / (mu / LB.MPC) < rc
            RES["rows"][f"{f}|{lm}|{mu:g}"] = dict(m=m, xc=p["xc"], r_c_kpc=rc / 3.0857e19, dust_mass_over_share=frac, mu_rc=mu / LB.MPC * rc, jeans_wavelength_inside=bool(fits))
            P(f"[{f}] log M_b {lm} mu {mu:g}/Mpc: m {m:.3g}, r_c {rc / 3.0857e19:.4g} kpc (dust-free {math.sqrt(X * (X + 1)) * rM / 3.0857e19:.0f}), dust's own mass / share {frac:.3g}, "
              f"mu r_c {mu / LB.MPC * rc:.3f}; a Jeans wavelength fits inside r_c: {fits}")
P(LB.NOTE)
json.dump(RES, open(os.path.join(HERE, "mk1_row8.json"), "w"), indent=1)
open(os.path.join(HERE, "mk1_row8.out"), "w").write("\n".join(OUT) + "\n")
# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
