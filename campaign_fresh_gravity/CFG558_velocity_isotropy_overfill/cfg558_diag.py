#!/usr/bin/env python3
"""CFG558 post-freeze diagnostic (no label depends on it): why V3 blows up in the cluster cells.
Evaluates V3's sigma_*^2 on the IC-E (law-profile, Jeans velocities) state at t = 0 in every cell, against FIX-2's sigma_J^2,
and prints the early r_99 growth of the cluster runs from cfg558_results.json. Run: OMP_NUM_THREADS=1 nice -n 10 python3 cfg558_diag.py"""
import os, json, numpy as np
import cfg558 as M
T = M.T544; HERE = os.path.dirname(os.path.abspath(__file__)); out = {}
for s in T.SYS:
    for f in T.FOOT:
        k = f"{s}_{f}"; c = T.make_cell(s, f); rng = np.random.default_rng(T.SEED)
        r, vr, L, m = T.make_ic(c, "E", rng); toy = M.Toy558(c, "v3"); toy.m = m
        mc = m * np.histogram(r, toy.rf)[0]; rho = mc / toy.V
        s2v, _, _, _ = M.v3_target(c, toy.rf, toy.rc, toy.dr, mc, rho, toy.rhoph, True)
        s2f, _, _, _ = M.v3_target(c, toy.rf, toy.rc, toy.dr, mc, rho, toy.rhoph, False)
        occ = rho > 0; i = int(np.argmax(np.where(occ, s2v, 0)))
        out[k] = dict(max_sigma_star2_over_Vf2=float(s2v[occ].max()), at_r_over_rstar=float(toy.rc[i]),
                      n_particles_in_bin=int(round(mc[i] / m)), rho_over_rhoph=float(rho[i] / toy.rhoph[i]),
                      fix2_sigma2_there=float(s2f[i]), ratio=float(s2v[i] / s2f[i]))
J = json.load(open(os.path.join(HERE, "cfg558_results.json")))
for nm in ("cluster_can|v3_over_base", "cluster_can|v3_C_al1.0", "cluster_alt|v3_C_al1.0", "MW_can|v3_over_inj"):
    out["r99_series|" + nm] = [(round(q["t"], 2), round(q["r99"], 3)) for q in J["runs"][nm]["series"][:12]]
for k, v in out.items():
    print(k, v)
json.dump(out, open(os.path.join(HERE, "cfg558_diag.json"), "w"), indent=1)
