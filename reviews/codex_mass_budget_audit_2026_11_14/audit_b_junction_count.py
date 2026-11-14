#!/usr/bin/env python3
"""Independent recount of the XJ1 one-sided density ratio N_in/N_out at the k = 2, 3 caustic junctions.
XJ1's library is imported read-only only for the halo population, the caustic radius R_set (rsurf_com on XJ1's shell runs)
and, on the cluster branch only, the layout function. On the galaxy branch the one-sided slopes are computed here
analytically: inside d/dr[min(phantom, Mcold) + rem r/rta], outside t Mcold dM_L/dr / Mta (central difference on M_L).
Under pure advection with a standing interior and a growing front, N_in/N_out < 1 requires outflow (v_out = Rdot (1 - N_in/N_out)).
  nice -n 19 python3 -I -B reviews/codex_mass_budget_audit_2026_11_14/audit_b_junction_count.py
Prints per-group and total counts (kept as audit_b_junction_count.out); a JSON copy goes to scratch/ (not committed). Footings side by side, never pooled.
kappa = 1/2 FITTED; not theory closed. Adopts nothing."""
import os, sys, json, math
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[v] = "1"
sys.dont_write_bytecode = True
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO, "closure_2026_11_14", "XJ1_exact_junction_zero_velocity_surface"))
import xj1_lib2 as XL                                      # read-only
XL.install()
Z = XL.X.rec(); F, L = Z["F"], Z["L"]
G, h, FB = F["G"], F["h"], F["FB"]
res = {}; tot = dict(n=0, degenerate=0, outflow=0, inflow=0, near=0)
for foot in XL.FOOTS:
    for z in [0.0] + list(XL.ZB):
        Z["set_z"](z); vs = XL.X.vstar(foot, z); a0 = F["a0c"](foot); X = F["Xsh"](foot)
        for k in (2, 3):
            c = dict(n=0, degenerate=0, outflow=0, inflow=0, near=0, cluster=0)
            for hb in L["HB"]:
                if F["v_vir"](hb) > vs: continue
                R = XL.rsurf_com(hb, foot, z, XL.COL_K[k], 1.0)
                if R <= 0: continue
                galaxy = not (F["v_vir"](hb) > Z["VST"][foot])
                rta, Mta = hb["rta"], hb["Mta"]
                if galaxy:
                    Mcold = (1 - FB) * Mta; Mb = Mcold / X
                    ph = lambda r: math.sqrt(0.25 * Mb * Mb + Mb * r * r * a0 / (G * h)) - 0.5 * Mb
                    rem = max(Mcold - min(ph(rta), Mcold), 0.0)
                    CB = min(ph(R), Mcold) + rem * R / rta
                    dph = (Mb * R * a0 / (G * h)) / math.sqrt(0.25 * Mb * Mb + Mb * R * R * a0 / (G * h)) if ph(R) < Mcold else 0.0
                    si = dph + rem / rta
                    ML = lambda r: float(F["M_L"](hb, r))
                    CR = Mcold * ML(R) / Mta; T = Mcold
                    e = 1e-6 * R
                    dCR = Mcold / Mta * (ML(R + e) - ML(R - e)) / (2 * e)
                else:
                    c["cluster"] += 1
                    CUR = Z["CUR"]; og = F["rgrid"]; e = 1e-6
                    nodes = np.array([R * (1 - e), R, R * (1 + e), rta])
                    try:
                        F["rgrid"] = lambda hh, rm, nodes=nodes: nodes.copy()
                        CUR[0] = 0.0
                        rb, mb, _ = Z["layout"](hb, foot, mode="B"); rr, mr, _ = Z["layout"](hb, foot, mode="Rb")
                    finally:
                        F["rgrid"] = og
                    cb = mb - Z["Bar"](hb, foot, rb); cr = mr - Z["Bar"](hb, foot, rr)
                    CB, CBm = np.interp([R, R * (1 - e)], rb, cb); CR, CRp = np.interp([R, R * (1 + e)], rr, cr)
                    T = float(cr[-1]); si = (CB - CBm) / (R * e); dCR = (CRp - CR) / (R * e)
                den = T - CR
                t = 1.0 if den <= 0 else (T - CB) / den
                so = t * dCR
                c["n"] += 1
                if so <= 1e-10 * Mta / R:
                    c["degenerate"] += 1; continue
                q = si / so
                if q < 0.999: c["outflow"] += 1
                elif q > 1.001: c["inflow"] += 1
                else: c["near"] += 1
            res[f"{foot}|{z}|k{k}"] = c
            for kk in tot: tot[kk] += c[kk]
        print(foot, z, {k: res[f"{foot}|{z}|k{k}"] for k in (2, 3)}, flush=True)
out = dict(totals=tot, groups=res, note="kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
os.makedirs(os.path.join(HERE, "scratch"), exist_ok=True)
json.dump(out, open(os.path.join(HERE, "scratch", "audit_b_junction_count.json"), "w"), indent=1)
print("TOTAL", tot)
print("kappa = 1/2 FITTED; not theory closed. Adopts nothing.")
