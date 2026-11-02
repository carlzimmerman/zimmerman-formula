#!/usr/bin/env python3
"""PA1: forms Q and R at all heights, every in-prior cell, as C3 requires. Form A only in pa1_profile.py; Q/A checked there. python3 pa1_allcells.py FOOT. kappa = 1/2 FITTED; not theory closed."""
import sys, os, json
HERE0 = os.path.dirname(os.path.abspath(__file__)); UX5 = os.path.join(HERE0, "..", "UX5_mw_stellar_mass"); sys.path.insert(0, UX5)
from ux5_core import *
foot = sys.argv[1]; a0 = A0[foot]; Z = np.array([0.05, 0.1, 0.2, 0.3, 0.5, 0.8, 1.1, 1.5])
rows = [r for r in (json.loads(l) for l in open(os.path.join(UX5, "cache", f"{foot}_1.0.jsonl"))) if r["inp"]]
g, Mu = grid(a0); LU = Lapl(g); conv = a0 / (2 * math.pi * PS.G_SI) / ns["SIGU"]; a0k = a0 * PS.KPC / 1e6
def prof(Phi):
    dr, dt = g.grad_cells(Phi); dz = np.cos(g.t2d) * dr - np.sin(g.t2d) * dt
    return g.interp_cells(dz, np.full_like(Z, R0), Z) * conv
KQ, KR, D = [], [], 0.0
for c in rows:
    rhof, _ = rho_struct(c["sb"], c["mbb"], c["rd"], c.get("ht"), c.get("hk"), c.get("fk"), c.get("rdk"))
    PhiN = LU.newton(g.rho_axisym(lambda R, z: rhof(R, z) / Mu, nq=4)); KN = prof(PhiN); q = prof(LU.qumond(PhiN))
    vb = L.vc_plane(ns, g, PhiN, a0, np.array([R0])); gb = vb ** 2 / R0; gc = float(((0.5 + np.sqrt(0.25 + a0k / gb) - 1) * gb)[0]); r = KN + gc * Z / R0 / KZU
    KQ.append(q.tolist()); KR.append(r.tolist()); D = max(D, abs(q[6] - c["Q"]["K0"]), abs(r[6] - c["R"]["K0"]))
json.dump(dict(Z=Z.tolist(), n=len(rows), max_recover=D, KQ=KQ, KR=KR), open(os.path.join(HERE0, f"pa1_all_{foot}.json"), "w"))
print(foot, len(rows), D)
