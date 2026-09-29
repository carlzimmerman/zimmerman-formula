#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG150 post2 -- POST HOC.  Written after all three frozen runs AND after opening CFG102's outputs.  It reads CFG102's
unrounded mu_uni(1e-12) from CFG102's committed cfg102_b_results.json (D) and cfg102_b_results_BCN.json (N), and evaluates
MY potentials and flagship force at exactly that mu, with my own solver unchanged (2^17 elements, as in the frozen costs).
This separates the potential comparison from the mu_uni comparison: CFG102 scored its costs at its own unrounded mu_uni,
while my frozen P-lines use the printed 1.474e28.  Second question: the frozen control L4 passed, but its Sun value sat
+0.27% from DE13's committed N1; is that the Laplacian estimate (DE13's np.gradient on DE12's grid against my 5-point
stencil at several steps, all at DE13's own mu_U)?  Third: on which layers can B |W''| exceed m2 (where the chi-only
energy can be non-convex; post1 traced the unconverged solves to two layers)?  It changes no frozen number.
Outputs: post2_costs_at_cfg102_mu.out and post2_costs_at_cfg102_mu_results.json next to this file.
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

T0 = time.time()
LOG = open(os.path.join(HERE, "post2_costs_at_cfg102_mu.out"), "w")


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    LOG.write(s + "\n")
    LOG.flush()


P(__doc__.strip())
P(f"\n  frozen criteria sha256 checked on import: {m.SPEC_SHA_SEEN}")
m.setup()
d102 = os.path.join(m.REPO, "campaign_fresh_gravity", "CFG102_gate_scalar_rederivation")
OUT = {}
FL = m.Case("flagship", 2.5, 1e11, "canonical")
SU = m.Case("Sun", 0.0, 6e10, "canonical", 8.0)
for label, suf in (("D", ""), ("N", "_BCN")):
    rows = json.load(open(os.path.join(d102, f"cfg102_b_results{suf}.json")))["rows"]
    k = [kk for kk in rows if abs(float(kk) / 1e-12 - 1) < 1e-9][0]
    r = rows[k]
    mu = r["mu_uni"]
    cf = m.cost(FL, mu, m.M2, label)
    cs = m.cost(SU, mu, m.M2, label)
    OUT[label] = dict(mu_cfg102=mu, mine=dict(PhiF=cf["Phi"], forceF=cf["force"], PhiS=cs["Phi"]),
                      cfg102=dict(PhiF=r["phiF"], forceF=r["forceF"], PhiS=r["phiSun"]),
                      rel=dict(PhiF=cf["Phi"] / r["phiF"] - 1, forceF=cf["force"] / r["forceF"] - 1, PhiS=cs["Phi"] / r["phiSun"] - 1),
                      newton=dict(flag=cf["newton"], sun=cs["newton"]))
    P(f"\n  [{label}] at CFG102's unrounded mu_uni = {mu:.10e} J/m:")
    P(f"      flagship potential: mine {cf['Phi']:+.8f}  CFG102 {r['phiF']:+.8f}  (rel {cf['Phi'] / r['phiF'] - 1:+.2e})")
    P(f"      flagship force:     mine {cf['force']:+.6f}  CFG102 {r['forceF']:+.6f}  (rel {cf['force'] / r['forceF'] - 1:+.2e})")
    P(f"      Sun potential:      mine {cs['Phi']:+.8e}  CFG102 {r['phiSun']:+.8e}  (rel {cs['Phi'] / r['phiSun'] - 1:+.2e})")
    P(f"      my Newton: flagship {cf['newton']['it']} iterations (res {cf['newton']['res']:.1e}); Sun {cs['newton']['it']} (res {cs['newton']['res']:.1e})")
dD = OUT["D"]["mine"]["PhiF"] - OUT["N"]["mine"]["PhiF"]
dC = OUT["D"]["cfg102"]["PhiF"] - OUT["N"]["cfg102"]["PhiF"]
P(f"\n  flagship D - N: mine {dD:+.6f}, CFG102 {dC:+.6f} (rel {dD / dC - 1:+.2e})")
OUT["flagship_D_minus_N"] = dict(mine=dD, cfg102=dC)

# ---------------------------------------------------------------------------------------------- the L4 Sun residual (+0.27%)
# Frozen L4 passed, but the Sun's N1 differed from DE13's committed 2.1257e8 by +0.27% (the flagship by +0.02%).  Is that the
# Laplacian estimate?  Evaluate lap t at the two radii (a) DE13's way: np.gradient twice on DE12's own 20000-point grid, then
# np.interp to the radius; (b) my 5-point stencil in s at several steps.  mu is DE13's own max mu_U (from its committed JSON),
# so any difference left is the Laplacian alone.
import numpy as np  # noqa: E402
de13, _ = m.read_committed_json("real_research/dark_energy_2026/DE13_gate_gradient_repair_results.json")
rows13 = de13["numbers"]["F1"]["rows"]
muU13 = max(rows13[k]["mu_U"] for k in rows13 if "1e+14" not in k)
refs = {"flagship": de13["numbers"]["form_i_cost"]["flagship r_F, z = 2.5, 1e11"],
        "Sun": de13["numbers"]["form_i_cost"]["the Sun, z = 0, 6e10 at 8 kpc"]}
L4x = {}
for case in (FL, SU):
    pr = case.prof
    r12 = np.geomspace(1.0, 2e4, 20000) * m.KPC
    t12 = pr.ev(r12)["t"]
    U12 = (t12 - 0.5) * 2 * m.W_GATE + 1                     # U from t (t = (U - 1)/(2w) + 1/2)
    lapU12 = np.gradient(r12 ** 2 * np.gradient(U12, r12), r12) / r12 ** 2
    lap_a = float(np.interp(case.r_eval, r12, lapU12)) * m.T_U   # lap t = t_U lap U
    se = math.log(case.r_eval / m.KPC)
    row = dict(de13_way=lap_a)
    for hs in (0.03, 0.01, 0.003, 0.001, 3e-4):
        tt = [float(pr.ev(np.array([m.KPC * math.exp(se + j * hs)]))["t"][0]) for j in (-2, -1, 0, 1, 2)]
        t_s = (-tt[4] + 8 * tt[3] - 8 * tt[1] + tt[0]) / (12 * hs)
        t_ss = (-tt[4] + 16 * tt[3] - 30 * tt[2] + 16 * tt[1] - tt[0]) / (12 * hs ** 2)
        row[f"5pt_h{hs:g}"] = (t_ss + t_s) / case.r_eval ** 2
    K = 4 * math.pi * m.C.G * pr.Cc * (muU13 / m.T_U ** 2) * m.T_U / pr.vf2   # |Phi|/v_f^2 per unit lap t
    L4x[case.name] = dict(DE13=refs[case.name], **{k: abs(K * v) for k, v in row.items()})
    P(f"\n  L4 {case.name}: |Phi|/v_f^2 with DE13's own mu_U = {muU13:.6e}: DE13 committed {refs[case.name]:.6e}")
    for k, v in row.items():
        P(f"      lap t by {k:12s}: |Phi| = {abs(K * v):.6e} (rel to DE13 {abs(K * v) / refs[case.name] - 1:+.2e})")
OUT["L4_laplacian"] = L4x

# ---------------------------------------------------------------------------------------------- where is the chi energy non-convex?
# post1 traced the 12 unconverged solves to the two z = 4, 1e12 layers.  Third question: on which layers can B |W''| exceed m2
# (the chi-only energy's local curvature m2 - B W'' can turn negative)?  B over each layer (2001 points in ln r across
# t in [0.004, 0.996]) times the step's largest |W''|, against m2 = 1e-12.
xs = np.linspace(1e-6, 1 - 1e-6, 200001)
W2max = float(np.max(np.abs(m.Wfun(xs)[2])))
conv = []
for z, Mb, f in m.LAYERS:
    L = m.Layer(z, Mb, f)
    rr = np.geomspace(L.rt[m.T_HI], L.rt[m.T_LO], 2001)
    Bv = L.prof.ev(rr)["B"]
    conv.append(dict(layer=L.key, B_min=float(Bv.min()), B_max=float(Bv.max()), ratio=float(Bv.max() * W2max / m.M2)))
conv.sort(key=lambda d: -d["ratio"])
P(f"\n  non-convexity: max |W''| = {W2max:.4f}; layers ranked by max B|W''|/m2 over the layer (m2 = 1e-12):")
for d in conv[:6]:
    P(f"      {d['layer']:22s} {d['ratio']:.3f}  (B {d['B_min']:.2e} .. {d['B_max']:.2e} Pa)")
P(f"      layers above 1: {sum(1 for d in conv if d['ratio'] > 1)} of 24")
OUT["nonconvex"] = dict(W2max=W2max, layers=conv)
OUT["elapsed_s"] = round(time.time() - T0, 1)
with open(os.path.join(HERE, "post2_costs_at_cfg102_mu_results.json"), "w") as fh:
    json.dump(m.clean(OUT), fh, indent=1)
P(f"\n  wrote post2_costs_at_cfg102_mu_results.json; elapsed {time.time() - T0:.0f}s")
P("  kappa = 1/2 and Omega_c h^2 stay fitted. Nothing here says the data favour either model, or that the theory is closed.")
LOG.close()
