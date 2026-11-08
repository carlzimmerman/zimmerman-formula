#!/usr/bin/env python3
"""CMB1 reported reading (not graded): baryons-only chi2_PA profile over omega_b in [0.03, 0.20] (footing h), ln A
optimized by bounded Brent at each (omega_b, n_s) for n_s in {0.97, 1.30}, tau 0.06. Checks that block C's B fit did
not miss a high-omega_b minimum. kappa = 1/2 FITTED; not theory closed."""
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cmb1 import theory, PA, footing_h, FOOT, dump, NOTE
from scipy.optimize import minimize_scalar
out = dict(note=NOTE)
for foot in FOOT:
    rows = []
    for ob in (0.03, 0.05, 0.08, 0.12, 0.20):
        for ns in (0.97, 1.30):
            p = lambda lnA: dict(h=footing_h(foot, ob, 0.0), ob=ob, oc=1e-7, lnA=lnA, ns=ns, tau=0.06)
            r = minimize_scalar(lambda x: PA(theory(p(x)))["PA"], bounds=(1.5, 4.5), method="bounded", options=dict(maxiter=18, xatol=0.02))
            rows.append(dict(ob=ob, ns=ns, lnA=float(r.x), chi2=float(r.fun))); print(foot, rows[-1], flush=True)
    out[foot] = rows
dump("ob_scan.json", out)
