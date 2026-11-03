#!/usr/bin/env python3
"""KT21 pre-data systematic: how much the ln-median of projected vtilde moves between two separation bins from (a) an
eccentricity-index change of 0.2 between them, (b) a triple-contamination difference of 2 points (5 vs 3 percent, the
record's +|N(0,1)| model), (c) velocity noise (allowance). Newtonian Kepler orbits, f(e) ~ e^alpha, uniform mean
anomaly, random orientation. Reads no wide-binary data. python3 kt21_sys.py. kappa = 1/2 FITTED; not theory closed."""
import json, math, os
import numpy as np
from scipy.optimize import newton
HERE = os.path.dirname(os.path.abspath(__file__)); rng = np.random.default_rng(2026110301); N = 400000; OUT = []
def P(s): print(s, flush=True); OUT.append(s)
def orbits(alpha, n):
    """unit a, unit GM. returns r_sky, v_sky, r3d."""
    e = rng.uniform(0, 1, n) ** (1 / (alpha + 1)); Mn = rng.uniform(0, 2 * math.pi, n)
    E = Mn.copy()
    for _ in range(60): E = E - (E - e * np.sin(E) - Mn) / (1 - e * np.cos(E))
    r = 1 - e * np.cos(E); x = np.cos(E) - e; y = np.sqrt(1 - e * e) * np.sin(E)
    vx = -np.sin(E) / r; vy = np.sqrt(1 - e * e) * np.cos(E) / r
    ci = rng.uniform(-1, 1, n); si = np.sqrt(1 - ci * ci); w = rng.uniform(0, 2 * math.pi, n)
    X = x * np.cos(w) - y * np.sin(w); Y = x * np.sin(w) + y * np.cos(w); VX = vx * np.cos(w) - vy * np.sin(w); VY = vx * np.sin(w) + vy * np.cos(w)
    rs = np.hypot(X, Y * ci); vs = np.hypot(VX, VY * ci); return rs, vs, r
def lnmed(alpha, ftrip=0.0):
    rs, vs, _ = orbits(alpha, N); vt = vs / np.sqrt(1 / rs)
    if ftrip > 0: t = rng.uniform(0, 1, N) < ftrip; vt = np.where(t, vt + np.abs(rng.normal(0, 1, N)), vt)
    return math.log(np.median(vt))
res = {}
base = {a: lnmed(a) for a in (0.8, 1.0, 1.2, 1.4, 1.6)}
for a, v in base.items(): P(f"alpha {a}: median vtilde {math.exp(v):.4f}")
da = max(abs(base[a + 0.2] - base[a]) for a in (1.0, 1.2, 1.4) if a + 0.2 in base)
P(f"(a) max |d ln median| for d alpha 0.2 over alpha 1.0-1.6: {da:.4f}")
dt = abs(lnmed(1.2, 0.05) - lnmed(1.2, 0.03)); P(f"(b) triples 5 vs 3 percent at alpha 1.2: {dt:.4f}")
dn = 0.003; P(f"(c) noise allowance: {dn:.4f}")
sys_tot = math.sqrt(da * da + dt * dt + dn * dn); P(f"sigma_sys on Q = {sys_tot:.4f}")
res.update(median_by_alpha={str(a): math.exp(v) for a, v in base.items()}, d_alpha=da, d_trip=dt, d_noise=dn, sigma_sys=sys_tot)
open(os.path.join(HERE, "kt21_sys.out"), "w").write("\n".join(OUT) + "\n"); json.dump(res, open(os.path.join(HERE, "kt21_sys.json"), "w"), indent=1)
