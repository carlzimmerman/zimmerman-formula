"""CFG750: is the central black hole a cold-energy drain? Criteria: FROZEN_CRITERIA.md (66c117bc4).
Shells: r'' = -M_N/r^2 + (m_out^3 - m_in^3)/(3 dm r^4) + L^2/r^3, M_N = M_b + M_bh; sink r < r_s adds mass to M_bh.
kappa = 1/2 FITTED; the cold energy's mass is required; no particle species; not "theory closed".
Run:  OMP_NUM_THREADS=1 nice -n 10 python3 cfg750.py <A|B|K1>
"""
import os, sys, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
case = sys.argv[1]
N, RS, R0, DT, TEND, MB, SEED = 4000, 0.1, 200.0, 0.002, 4000.0, 1.0, 1e-4
lmax = 0.0 if case == "A" else 0.1
SINK = case != "K1"
rng = np.random.default_rng(750)
dm = (R0 - RS) / N
q = (np.arange(N) + 0.5) / N
r = (RS ** 3 + q * (R0 ** 3 - RS ** 3)) ** (1 / 3); v = np.zeros(N)
vc2 = lambda rr: rr * (1 / rr ** 2 + 1 / rr)
L2 = (rng.uniform(0, lmax, N) * r * np.sqrt(vc2(r))) ** 2
alive = np.ones(N, bool); Mbh = SEED; swallowed_E = 0.0
def accel(r, al, MN):
    idx = np.where(al)[0]; o = idx[np.argsort(r[idx])]; rs = r[o]
    mi = dm * np.arange(len(o))
    a_s = -MN / rs ** 2 + ((mi + dm) ** 3 - mi ** 3) / (3 * dm * rs ** 4) + L2[o] / rs ** 3
    a = np.zeros(N); a[o] = a_s; return a
def energy(r, v, al, MN):
    idx = np.where(al)[0]; o = idx[np.argsort(r[idx])]; rs = r[o]; mo = dm * (np.arange(len(o)) + 1)
    E = 0.5 * dm * np.sum(v[o] ** 2 + L2[o] / rs ** 2) - dm * MN * np.sum(1 / rs)
    E += np.sum(mo[:-1] ** 3 * (rs[:-1] ** -3 - rs[1:] ** -3)) / 9 + mo[-1] ** 3 * rs[-1] ** -3 / 9
    return float(E)
E0 = energy(r, v, alive, MB + Mbh); a = accel(r, alive, MB + Mbh)
hist, marks = {}, [100, 500, 1000, 2000, 4000]
for n in range(int(TEND / DT)):
    v += 0.5 * DT * a; r += DT * v
    if SINK:
        hit = alive & (r < RS)
        if hit.any():
            swallowed_E += float(np.sum(0.5 * dm * (v[hit] ** 2 + L2[hit] / r[hit] ** 2) - dm * (MB + Mbh) / r[hit]))
            Mbh += dm * hit.sum(); alive &= ~hit
    else:
        low = alive & (r < RS); r[low] = 2 * RS - r[low]; v[low] = -v[low]
    a = accel(r, alive, MB + Mbh); v += 0.5 * DT * a
    t = round((n + 1) * DT, 6)
    if t in marks:
        hist[str(t)] = Mbh
rs = np.sort(r[alive])
m_over_r = {str(R): float(dm * np.searchsorted(rs, R) / (R * np.sqrt(MB + Mbh))) for R in (2.0, 5.0, 10.0)}   # law: m = sqrt(M_N) r
res = dict(case=case, M_bh_final=Mbh, ratio=Mbh / MB, growth=Mbh - SEED, history=hist,
           late_growth_frac=(Mbh - hist.get("2000", Mbh)) / max(Mbh - SEED, 1e-30),
           bound_cold=float(dm * np.sum(alive & (r < 1000))), escaped=float(dm * np.sum(alive & (r >= 1000))),
           m_over_r_law=m_over_r, E0=E0, E_end_plus_swallowed=energy(r, v, alive, MB + Mbh) + swallowed_E)
json.dump(res, open(os.path.join(HERE, f"cfg750_{case}.json"), "w"), indent=1); print(json.dumps(res))
