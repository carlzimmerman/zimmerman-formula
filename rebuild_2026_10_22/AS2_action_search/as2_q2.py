#!/usr/bin/env python3
"""AS2 G4 cells: Q2 on the AQUAL form and on the two-field form, both footings, E0-E3, with UX1's solver (imported read only) and UX1's settings.
Checkpoint per cell in as2_q2.json. Resumes. No timing written. kappa = 1/2 FITTED."""
import json, math, os, sys
import numpy as np
from scipy.integrate import solve_ivp
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(HERE, "..", "UX1_action_class"))
import ux1_q2 as U
GM = 1.32712440018e20; AU = 1.495978707e11; RSAT = 9.5826 * AU; HEES = 9.0e-27; GNE = 6.913e-11
GEK = {"E1": 1.9 * 9.36e-11, "E2": 2.2 * 9.36e-11, "E3": 2.6 * 9.36e-11}
OUT = os.path.join(HERE, "as2_q2.json")
res = json.load(open(OUT)) if os.path.exists(OUT) else {}
def yof(e, a):
    if e == "E0":
        return GNE / a
    x = GEK[e] / a
    return x ** 2 / (1 + x)
rr = np.geomspace(1e-5, 10, 400)
def rhs(ln, Y_):
    r = np.exp(ln); H = 1 / r ** 2
    return [r * Y_[1] / (r ** 2 / U.dk_("bimond", H)), r * (H / U.k_("bimond", H)) * 6 * Y_[0]]
r0 = rr[0]; W0 = 1 / U.dk_("bimond", 1 / r0 ** 2)
ff = solve_ivp(rhs, [np.log(r0), np.log(rr[-1])], [r0 ** 3, r0 ** 2 * W0 * 3 * r0 ** 2], t_eval=np.log(rr), rtol=1e-10, atol=1e-30).y[0]
E2 = json.load(open(os.path.join(REPO, "doors_push_2026_10_22/E2_field_equation/e2_field_equation_results.json")))
for foot, a, ae2, key in (("canonical", 9.3603e-11, 9.36e-11, "canonical|none"), ("alt", 1.1312e-10, 1.13e-10, "alt|none")):
    for e in ("E0", "E1", "E2", "E3"):
        k = f"aqual|{foot}|{e}"
        if k not in res:
            s = U.Solver("aqual", yof(e, ae2), r_in=1e-4, r_out=1e4, per_dec=60, Nt=96).solve()
            q = s.q0() * ae2 ** 1.5 / math.sqrt(GM)
            res[k] = dict(Q2=float(q), over_Hees=abs(q) / HEES, E2=E2["R1"][key]["cells"][e]["Q2_AQUAL"], ratio_E2=float(q / E2["R1"][key]["cells"][e]["Q2_AQUAL"]), converged=s.converged)
            json.dump(res, open(OUT, "w"), indent=1, sort_keys=True); print(k, res[k], flush=True)
        k = f"twofield|{foot}|{e}"
        if k not in res:
            unit = a ** 1.5 / math.sqrt(GM); rs = RSAT / math.sqrt(GM / a)
            b = U.Solver("bimond", yof(e, a), r_in=0.01, r_out=1e3, per_dec=60, Nt=96).solve(maxit=800)
            rb, qq = b.q_of_r(); RM = 0.1
            cm = -np.interp(RM, rb, qq) * RM ** 2 / 3
            cs = cm * np.exp(np.interp(np.log(rs), np.log(rr), np.log(ff))) / np.interp(np.log(RM), np.log(rr), ff)
            q = -3 * cs / rs ** 2 * unit
            res[k] = dict(Q2=float(q), over_Hees=abs(q) / HEES, converged=b.converged, last_step=float(b.step))
            json.dump(res, open(OUT, "w"), indent=1, sort_keys=True); print(k, res[k], flush=True)
        k = f"qumond|{foot}|{e}"
        if k not in res:
            q = E2["R1"][key]["cells"][e]["Q2_QUMOND_A"]
            res[k] = dict(Q2=q, over_Hees=abs(q) / HEES, source="E2 JSON [REC]")
            json.dump(res, open(OUT, "w"), indent=1, sort_keys=True)
print("done")
