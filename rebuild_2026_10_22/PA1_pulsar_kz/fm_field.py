#!/usr/bin/env python3
"""PA1 A1 stage 1: a_R, a_z (mm/s/yr) of N, A, Q, R at every pulsar position and at the Sun, eligible cells. python3 -I fm_field.py FOOT. Heavy part preemptible: per-cell checkpoint. kappa = 1/2 FITTED; not theory closed."""
import sys, os, json
H = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, H); import fm_lib as FL
UX5 = os.path.join(H, "..", "UX5_mw_stellar_mass"); sys.path.insert(0, UX5)
from ux5_core import *
foot = sys.argv[1]; a0 = A0[foot]; MM = a0 / (1e-3 / (365.25 * 86400))
B, All = FL.load("binary"), FL.load("all")
def pts(s, zs=0.0, ds=1.0): R, z, n, x, y = FL.geom(s["l"], s["b"], s["d"] * ds, zs); return R, z
Rb, zb = pts(B); Ra, za = pts(All); RR = np.r_[Rb, Ra, R0]; ZZ = np.r_[zb, za, 0.0]; AZ = np.abs(ZZ); SG = np.sign(ZZ)
rows = [r for r in (json.loads(l) for l in open(os.path.join(UX5, "cache", f"{foot}_1.0.jsonl"))) if r["inp"] and r["A"]["L1"] and r["R"]["L1"]]
rows.sort(key=lambda r: (r["box"], r["sb"], r["mbb"], r["rd"], r.get("ht", 0), r.get("hk", 0), r.get("fk", 0)))
g, Mu = grid(a0); LU = Lapl(g)
def field(Phi):
    dr, dt = g.grad_cells(Phi); dz = np.cos(g.t2d) * dr - np.sin(g.t2d) * dt; dR = np.sin(g.t2d) * dr + np.cos(g.t2d) * dt
    return -g.interp_cells(dR, RR, AZ) * MM, -g.interp_cells(dz, RR, AZ) * SG * MM, dR, dz
os.makedirs(os.path.join(H, "cache"), exist_ok=True); fn = os.path.join(H, "cache", f"field_{foot}.jsonl"); nd = sum(1 for _ in open(fn)) if os.path.exists(fn) else 0
k = lambda dz, R=R0, Z=1.1: float(g.interp_cells(dz, np.array([R]), np.array([Z]))[0]) * a0 / (2 * math.pi * PS.G_SI) / ns["SIGU"]
with open(fn, "a") as w:
    for i, c in enumerate(rows):
        if i < nd: continue
        rhof, _ = rho_struct(c["sb"], c["mbb"], c["rd"], c.get("ht"), c.get("hk"), c.get("fk"), c.get("rdk"))
        rho1 = g.rho_axisym(lambda R, z: rhof(R, z) / Mu, nq=4); PhiN = LU.newton(rho1); NR, Nz, dRN, dzN = field(PhiN); QR, Qz, _, dzQ = field(LU.qumond(PhiN))
        pr = PS.Problem(g, rho1, 2 * float(np.sum(rho1 * g.vol)), 0.0, Lam=0.0); Phi, res, it = pr.solve_aqual(); AR, Az, _, dzA = field(Phi)
        yb = g.interp_cells(dRN, RR, np.zeros_like(RR)); gc = (0.5 + np.sqrt(0.25 + 1 / np.maximum(yb, 1e-30)) - 1) * yb * MM
        RRa = NR - gc; Rz = Nz - gc * ZZ / RR
        gc0 = gc[-1] / MM; KRv = k(dzN) + gc0 * 1.1 / R0 * a0 / (2 * math.pi * PS.G_SI) / ns["SIGU"]
        w.write(json.dumps(dict(i=i, box=c["box"], c=c["A"]["K0"], cR=c["R"]["K0"], KA=k(dzA), KQ=k(dzQ), KR=KRv, res=float(res), N=[NR.tolist(), Nz.tolist()], A=[AR.tolist(), Az.tolist()], Q=[QR.tolist(), Qz.tolist()], R=[RRa.tolist(), Rz.tolist()])) + "\n"); w.flush()
# AQUAL nu->1 limit: density x 1e8, potential / 1e8. Fixes PA1's unmet form A MUTATE.
c = rows[len(rows) // 2]; rhof, _ = rho_struct(c["sb"], c["mbb"], c["rd"], c.get("ht"), c.get("hk"), c.get("fk"), c.get("rdk")); rho1 = g.rho_axisym(lambda R, z: rhof(R, z) / Mu, nq=4); PhiN = LU.newton(rho1); _, _, _, dzN = field(PhiN)
pr = PS.Problem(g, rho1 * 1e8, 2e8 * float(np.sum(rho1 * g.vol)), 0.0, Lam=0.0); Phi, res, it = pr.solve_aqual(); _, _, _, dzM = field(Phi / 1e8)
json.dump(dict(n=len(rows), nb=len(Rb), na=len(Ra), KN=k(dzN), KA_mut=k(dzM), KA_cached=c["A"]["K0"], res=float(res), it=int(it)), open(os.path.join(H, f"fm_field_{foot}.json"), "w"), indent=1); print(foot, len(rows))
