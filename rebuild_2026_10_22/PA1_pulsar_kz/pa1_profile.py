#!/usr/bin/env python3
"""PA1 part 2: forms A, Q, R on UX5's solver at pulsar heights, R0, in-prior cells with form A's v_c in line. python3 pa1_profile.py FOOT [--mutate]. --mutate sets nu = 1 in form Q only. Writes only here. kappa = 1/2 FITTED; not theory closed."""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__)); UX5 = os.path.join(HERE, "..", "UX5_mw_stellar_mass"); sys.path.insert(0, UX5)
from ux5_core import *
HERE = os.path.dirname(os.path.abspath(__file__))  # ux5_core exports its own HERE
foot = sys.argv[1]; mut = "--mutate" in sys.argv; a0 = A0[foot]
Z = np.array([0.05, 0.1, 0.2, 0.3, 0.5, 0.8, 1.1, 1.5]); NS = 24
rows = [json.loads(l) for l in open(os.path.join(UX5, "cache", f"{foot}_1.0.jsonl"))]
s = [r for r in rows if r["inp"] and r["A"]["L1"]]; s.sort(key=lambda r: (r["box"], r["sb"], r["mbb"], r["rd"], r.get("ht", 0), r.get("hk", 0), r.get("fk", 0)))
idx = set(np.linspace(0, len(s) - 1, NS).astype(int).tolist()); gap = [r["A"]["K0"] - r["R"]["K0"] for r in s]
idx |= {int(np.argmin(gap)), int(np.argmax(gap)), int(np.argmin([r["A"]["K0"] for r in s])), int(np.argmin([r["R"]["K0"] for r in s])), int(np.argmax([r["R"]["K0"] for r in s]))}
g, Mu = grid(a0); LU = Lapl(g); conv = a0 / (2 * math.pi * PS.G_SI) / ns["SIGU"]; a0k = a0 * PS.KPC / 1e6
def prof(Phi):
    dr, dt = g.grad_cells(Phi); dz = np.cos(g.t2d) * dr - np.sin(g.t2d) * dt
    return g.interp_cells(dz, np.full_like(Z, R0), Z) * conv
out = []
for i in sorted(idx):
    c = s[i]; rhof, _ = rho_struct(c["sb"], c["mbb"], c["rd"], c.get("ht"), c.get("hk"), c.get("fk"), c.get("rdk"))
    rho1 = g.rho_axisym(lambda R, z: rhof(R, z) / Mu, nq=4); PhiN = LU.newton(rho1); KN = prof(PhiN)
    KQ = prof(LU.qumond(PhiN, mut)); vb = L.vc_plane(ns, g, PhiN, a0, np.array([R0])); gb = vb ** 2 / R0; gc = float(((0.5 + np.sqrt(0.25 + a0k / gb) - 1) * gb)[0]); KR = KN + gc * Z / R0 / KZU
    pr = PS.Problem(g, rho1, 2 * float(np.sum(rho1 * g.vol)), 0.0, Lam=0.0); Phi, res, it = pr.solve_aqual(); KA = prof(Phi)
    out.append(dict(i=i, box=c["box"], cached_A=c["A"]["K0"], cached_Q=c["Q"]["K0"], cached_R=c["R"]["K0"], KN=KN.tolist(), KA=KA.tolist(), KQ=KQ.tolist(), KR=KR.tolist(), res=float(res)))
name = f"pa1_profile_{foot}{'_MUTATE' if mut else ''}.json"; json.dump(dict(Z=Z.tolist(), n_cells=len(s), cells=out), open(os.path.join(HERE, name), "w"), indent=0)
print(name, len(out), "of", len(s))
