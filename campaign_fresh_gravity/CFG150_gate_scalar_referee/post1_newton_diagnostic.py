#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG150 post1 -- POST HOC.  Written after the frozen main run, whose R4 row reported 12 background solves that did not
reach the frozen residual line (1e-13) within 60 Newton iterations (largest final residual 0.21; diagonal shifts up to
tau = 1e3).  This script changes no frozen number.  It asks:
  Q1  which layers, labels and trial mu the unconverged solves belong to (the frozen root searches are deterministic, so
      re-running them with every background solve logged reproduces the same calls);
  Q2  whether a more patient solve (continuation in B over 16 steps, up to 400 Newton iterations each) converges there,
      and whether it changes the sign of Lambda (the stability decision) at those trial mu;
  Q3  whether any layer's mu_min changes when every trial solve uses the patient fallback, and so whether mu_uni changes;
  Q4  whether all 24 layers are stable just above the frozen mu_uni (1.0001 x) with patient solves (mu_uni = the largest
      layer mu_min, as the headline needs).
It imports cfg150_referee.py (its frozen-criteria hash check runs on import) and uses its functions unchanged.
Outputs: post1_newton_diagnostic.out and post1_newton_diagnostic_results.json next to this file.
kappa = 1/2 and Omega_c h^2 stay fitted. Nothing here says the data favour either model, or that the theory is closed.
"""
import os
import sys
import json
import math
import time
import importlib.util

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
os.environ.pop("MUTATE", None)
spec = importlib.util.spec_from_file_location("cfg150_referee", os.path.join(HERE, "cfg150_referee.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
import numpy as np  # noqa: E402

T0 = time.time()
LOG = open(os.path.join(HERE, "post1_newton_diagnostic.out"), "w")


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.write(s + "\n")
    LOG.flush()


P(__doc__.strip())
P(f"\n  frozen criteria sha256 checked on import: {m.SPEC_SHA_SEEN}")
m.setup()

_orig_solve = m.solve_bg
CTX = {}
CALLS = []


def logged_solve(g, mu, m2, bc, **kw):
    chi, info = _orig_solve(g, mu, m2, bc, **kw)
    CALLS.append(dict(layer=CTX.get("layer"), label=CTX.get("label"), x=math.log10(mu), it=info["it"], res=info["res"],
                      conv=info["conv"], shift=info["shift"], ls=info["ls"]))
    return chi, info


def patient_solve(g, mu, m2, bc, **kw):
    """The frozen solve first; if it misses the residual line, continuation in B over 16 steps, 400 iterations each."""
    chi, info = _orig_solve(g, mu, m2, bc, stats=None)
    if info["conv"]:
        return chi, info
    chi_c, _ = _orig_solve(g, mu, m2, bc, Bs=0.0, stats=None)
    inf2 = None
    for kb in range(1, 17):
        chi_c, inf2 = _orig_solve(g, mu, m2, bc, Bs=kb / 16.0, start=chi_c, maxit=400, stats=None)
    inf2 = dict(inf2)
    inf2["fallback"] = True
    return chi_c, inf2


def lam_at(L, x, label, solver):
    """Lambda(10^x) for layer L at m2 = 1e-12 with the given background solver; also the solve info."""
    g = L.bg(m.NBG_SEARCH)
    bc = m.bc_tuple(g, label)
    mu = 10.0 ** x
    chi, info = solver(g, mu, m.M2, bc)
    wins = L.wins(m.NW_SEARCH)
    lam = min(m.win_lambda(w, mu, w.ag * m.M2 / (w.ag + m.M2) - w.Bg * m.Wfun(np.interp(w.sg, g.s, chi))[2]) for w in wins)
    return lam, info


# ---------------------------------------------------------------------------------------------- Q1: reproduce and log
P("\nQ1  the frozen root searches at m2 = 1e-12, re-run with every background solve logged")
LAY = {}
frozen_mu = {}
for z, Mb, foot in m.LAYERS:
    L = m.Layer(z, Mb, foot)
    LAY[L.key] = L
m.solve_bg = logged_solve
for label in ("D", "N"):
    for k, L in LAY.items():
        CTX.update(layer=k, label=label)
        rec = m.layer_mu_min(L, m.M2, label)
        frozen_mu[f"{label}/{k}"] = rec["mu"]
        L._bg.pop(m.NBG_SEARCH, None)
m.solve_bg = _orig_solve
bad = [c for c in CALLS if not c["conv"]]
P(f"    {len(CALLS)} background solves in the searches; {len(bad)} unconverged")
for c in bad:
    root = frozen_mu[f"{c['label']}/{c['layer']}"]
    P(f"    {c['label']} {c['layer']:22s} x = {c['x']:.6f} (root at {math.log10(root):.6f}; distance {c['x'] - math.log10(root):+.4f} "
      f"decades): iterations {c['it']}, final residual {c['res']:.2e}, largest shift tau {c['shift']:g}, halvings {c['ls']}")
mu_uni_frozen = max(v for kk, v in frozen_mu.items() if kk.startswith("D/"))
P(f"    reproduced mu_uni(D) = {mu_uni_frozen:.6e}, mu_uni(N) = {max(v for kk, v in frozen_mu.items() if kk.startswith('N/')):.6e}")

# ---------------------------------------------------------------------------------------------- Q2: patient solves there
P("\nQ2  at each unconverged trial mu: the patient solve (continuation in B, 16 x 400 iterations) and the sign of Lambda")
q2 = []
for c in bad:
    L = LAY[c["layer"]]
    lam_f, inf_f = lam_at(L, c["x"], c["label"], lambda g, mu, m2, bc: _orig_solve(g, mu, m2, bc, stats=None))
    lam_p, inf_p = lam_at(L, c["x"], c["label"], patient_solve)
    same = (lam_f > 0) == (lam_p > 0)
    q2.append(dict(layer=c["layer"], label=c["label"], x=c["x"], lam_frozen=lam_f, lam_patient=lam_p, same_sign=same,
                   patient_conv=inf_p["conv"], patient_res=inf_p["res"]))
    P(f"    {c['label']} {c['layer']:22s} x = {c['x']:.6f}: Lambda frozen {lam_f:+.4e} (res {inf_f['res']:.1e}); patient "
      f"{lam_p:+.4e} (converged {inf_p['conv']}, res {inf_p['res']:.1e}); same sign {same}")
    L._bg.pop(m.NBG_SEARCH, None)

# ---------------------------------------------------------------------------------------------- Q3: mu_min with patient solves
P("\nQ3  layers with an unconverged solve: mu_min recomputed with the patient solver at every trial mu")
q3 = {}
aff = sorted({(c["label"], c["layer"]) for c in bad})
m.solve_bg = lambda g, mu, m2, bc, **kw: patient_solve(g, mu, m2, bc)
for label, k in aff:
    L = LAY[k]
    t1 = time.time()
    rec = m.layer_mu_min(L, m.M2, label)
    fz = frozen_mu[f"{label}/{k}"]
    q3[f"{label}/{k}"] = dict(frozen=fz, patient=rec["mu"], rel=rec["mu"] / fz - 1, nonmonotone=rec["nonmonotone"],
                              below_unstable=rec["below_unstable"])
    P(f"    {label} {k:22s}: frozen {fz:.6e}; patient {rec['mu']:.6e} ({rec['mu'] / fz - 1:+.2e}); monotone probes "
      f"{not rec['nonmonotone']}; below unstable {rec['below_unstable']}   {time.time() - t1:.1f}s")
    L._bg.pop(m.NBG_SEARCH, None)
m.solve_bg = _orig_solve
new_uni = {lab: max((q3.get(f"{lab}/{k}", {}).get("patient") or frozen_mu[f"{lab}/{k}"]) for k in LAY) for lab in ("D", "N")}
P(f"    mu_uni with the patient values: D {new_uni['D']:.6e}, N {new_uni['N']:.6e} (frozen {mu_uni_frozen:.6e})")

# ---------------------------------------------------------------------------------------------- Q4: all stable just above mu_uni
P("\nQ4  every layer at 1.0001 x the frozen mu_uni, with patient solves (D and N)")
q4 = {}
x_up = math.log10(1.0001 * mu_uni_frozen)
for label in ("D", "N"):
    worst = None
    for k, L in LAY.items():
        lam, info = lam_at(L, x_up, label, patient_solve)
        q4[f"{label}/{k}"] = dict(lam=lam, conv=info["conv"])
        if worst is None or lam < worst[1]:
            worst = (k, lam)
        L._bg.pop(m.NBG_SEARCH, None)
    nst = sum(1 for kk, v in q4.items() if kk.startswith(label + "/") and v["lam"] > 0)
    ncv = sum(1 for kk, v in q4.items() if kk.startswith(label + "/") and v["conv"])
    P(f"    {label}: stable {nst}/24, converged {ncv}/24; smallest Lambda {worst[1]:+.4e} Pa ({worst[0]})")

OUT = dict(lane="CFG150 post1 (post hoc)", n_calls=len(CALLS), unconverged=bad, Q2=q2, Q3=q3, mu_uni_patient=new_uni,
           mu_uni_frozen=mu_uni_frozen, Q4=q4, elapsed_s=round(time.time() - T0, 1))
with open(os.path.join(HERE, "post1_newton_diagnostic_results.json"), "w") as fh:
    json.dump(m.clean(OUT), fh, indent=1)
P(f"\n  wrote post1_newton_diagnostic_results.json; elapsed {time.time() - T0:.0f}s")
P("  kappa = 1/2 and Omega_c h^2 stay fitted. Nothing here says the data favour either model, or that the theory is closed.")
LOG.close()
