"""CFG749: does orbital motion of the cold energy spoil the law? Criteria: FROZEN_CRITERIA.md.
CFG748 dynamics + centrifugal L_i^2/r^3 (G = a0 = M_b = 1). Run: python3 cfg749.py <lambda>
kappa = 1/2 FITTED; the cold energy's mass is required; no particle species; not "theory closed".
"""
import os, sys, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
N, RMIN, R0, DT, TEND, CORE = 4000, 0.5, 200.0, 0.005, 6000.0, 0.5
RAD = [2.0, 5.0, 10.0, 20.0]
lam = float(sys.argv[1])
dm = (R0 - CORE) / N; q = (np.arange(N) + 0.5) / N
r = (RMIN ** 3 + q * (R0 ** 3 - RMIN ** 3)) ** (1 / 3); v = np.zeros(N)
vc2 = lambda rr: rr * (1 / rr ** 2 + 1 / rr)
L2 = (lam * r * np.sqrt(vc2(r))) ** 2
def masses(r):
    o = np.argsort(r); return o, r[o], CORE + dm * np.arange(N)
def accel(r):
    o, rs, mi = masses(r)
    a_s = -1 / rs ** 2 + ((mi + dm) ** 3 - mi ** 3) / (3 * dm * rs ** 4)
    a = np.empty(N); a[o] = a_s; return a + L2 / r ** 3
def energy(r, v):
    o, rs, mi = masses(r); mo = mi + dm
    E = 0.5 * dm * np.sum(v ** 2 + L2 / r ** 2) - dm * np.sum(1 / rs)
    E += CORE ** 3 * (RMIN ** -3 - rs[0] ** -3) / 9 + np.sum(mo[:-1] ** 3 * (rs[:-1] ** -3 - rs[1:] ** -3)) / 9 + mo[-1] ** 3 * rs[-1] ** -3 / 9
    return float(E)
E0 = energy(r, v); a = accel(r); S, VT = [], []
for n in range(int(TEND / DT)):
    v += 0.5 * DT * a; r += DT * v
    low = r < RMIN; r[low] = 2 * RMIN - r[low]; v[low] = -v[low]
    a = accel(r); v += 0.5 * DT * a
    t = (n + 1) * DT
    if t >= 5000 and n % 200 == 0:
        rs = np.sort(r); S.append([(CORE + dm * np.searchsorted(rs, R)) / R for R in RAD])
        VT.append([float(np.mean((L2 / r ** 2)[(r > 0.8 * R) & (r < 1.2 * R)] / vc2(R))) if np.any((r > 0.8 * R) & (r < 1.2 * R)) else float('nan') for R in RAD])
res = dict(lam=lam, dE_rel=abs(energy(r, v) - E0) / abs(E0), m_over_r=dict(zip(map(str, RAD), map(float, np.mean(S, axis=0)))),
           vt2_over_vc2=dict(zip(map(str, RAD), map(float, np.nanmean(VT, axis=0)))))
res["predicted"] = {k: float(np.sqrt(max(0.0, 1 - x))) for k, x in res["vt2_over_vc2"].items()}
json.dump(res, open(os.path.join(HERE, f"cfg749_lam{lam:g}.json"), "w"), indent=1); print(json.dumps(res))
