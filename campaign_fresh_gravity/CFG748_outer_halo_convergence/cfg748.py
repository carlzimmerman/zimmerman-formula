"""CFG748: does the outer halo converge onto the law given time and mass? Criteria: FROZEN_CRITERIA.md (3eedeacd4).
CFG747 dynamics: r'' = -1/r^2 + (m_out^3 - m_in^3)/(3 dm r^4) (G = a0 = M_b = 1); R0 = 200, t_end = 10000.
kappa = 1/2 FITTED; the cold energy's mass is required; no particle species; not "theory closed".
Run:  OMP_NUM_THREADS=1 nice -n 10 python3 cfg748.py [state]   (state in law|uniform|half|mutate; one process per state)
"""
import os, sys, json
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
N, RMIN, R0, DT, TEND, CORE = 4000, 0.5, 200.0, 0.005, 10000.0, 0.5
RAD = [2.0, 5.0, 10.0, 20.0, 50.0]
WIN = [(1000, 2000), (3000, 4000), (5000, 6000), (7000, 8000), (9000, 10000)]
state = sys.argv[1]
MUT = state == "mutate"
kind = "uniform" if MUT else state
mtot = (R0 - CORE) * (0.5 if kind == "half" else 1.0)
dm = mtot / N; q = (np.arange(N) + 0.5) / N
r = (RMIN ** 3 + q * (R0 ** 3 - RMIN ** 3)) ** (1 / 3) if kind == "uniform" else RMIN + q * (R0 - RMIN)
v = np.zeros(N)
def masses(r):
    o = np.argsort(r); return o, r[o], CORE + dm * np.arange(N)
def accel(r):
    o, rs, mi = masses(r); a_s = -1 / rs ** 2
    if not MUT: a_s = a_s + ((mi + dm) ** 3 - mi ** 3) / (3 * dm * rs ** 4)
    a = np.empty(N); a[o] = a_s; return a
def energy(r, v):
    o, rs, mi = masses(r); mo = mi + dm
    E = 0.5 * dm * np.sum(v ** 2) - dm * np.sum(1 / rs)
    if not MUT:
        E += CORE ** 3 * (RMIN ** -3 - rs[0] ** -3) / 9 + np.sum(mo[:-1] ** 3 * (rs[:-1] ** -3 - rs[1:] ** -3)) / 9 + mo[-1] ** 3 * rs[-1] ** -3 / 9
    return float(E)
E0 = energy(r, v); a = accel(r)
acc = {w: [] for w in WIN}
for n in range(int(TEND / DT)):
    v += 0.5 * DT * a; r += DT * v
    low = r < RMIN; r[low] = 2 * RMIN - r[low]; v[low] = -v[low]
    a = accel(r); v += 0.5 * DT * a
    t = (n + 1) * DT
    if n % 200 == 0:
        for w in WIN:
            if w[0] <= t <= w[1]:
                rs = np.sort(r); acc[w].append([(CORE + dm * np.searchsorted(rs, R)) / R for R in RAD])
E1 = energy(r, v)
res = dict(state=state, dE_rel=abs(E1 - E0) / abs(E0), escaped=float(np.sum(r > 5000) * dm),
           windows={f"{w[0]}-{w[1]}": dict(zip(map(str, RAD), map(float, np.mean(acc[w], axis=0)))) for w in WIN})
json.dump(res, open(os.path.join(HERE, f"cfg748_{state}.json"), "w"), indent=1)
print(json.dumps(res))
