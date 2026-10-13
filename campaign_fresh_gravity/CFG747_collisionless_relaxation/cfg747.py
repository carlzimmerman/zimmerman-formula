"""CFG747: can collisionless cold energy relax onto the law's profile? Criteria: FROZEN_CRITERIA.md (ce642f4f2).
Radial shells; units G = a0 = M_b = 1. Energy E = sum KE - sum dm/r + (1/3) int m^3/r^4 dr (self-gravity cancelled by the critical
tether); exact discrete force a_i = -1/r_i^2 + (m_i^3 - m_{i-1}^3)/(3 dm r_i^4). Fixed inner cold core 0.5 inside r_min = 0.5.
kappa = 1/2 FITTED; the cold energy's mass is required; no particle species; not "theory closed".
Run:  OMP_NUM_THREADS=1 nice -n 10 python3 cfg747.py      (CFG747_MUTATE=1: no cold-energy force; exit 1 iff the control collapses)
"""
import os, sys, json, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("CFG747_MUTATE", "0") == "1"; TAG = "_MUTATE" if MUT else ""
N, RMIN, R0, DT, TEND, CORE = 4000, 0.5, 50.0, 0.005, 3000.0, 0.5
lines = [__doc__.strip()]
def P_(s): print(s, flush=True); lines.append(s)

def init(kind):
    mtot = R0 - CORE if kind in ("law", "uniform") else (1.5 if kind == "1.5x" else 0.5) * (R0 - CORE)
    dm = mtot / N; q = (np.arange(N) + 0.5) / N
    if kind == "uniform":
        r = (RMIN ** 3 + q * (R0 ** 3 - RMIN ** 3)) ** (1 / 3)
    else:
        r = RMIN + q * (R0 - RMIN)                          # m_shells(r) proportional to (r - 0.5): law shape scaled
    return r, np.zeros(N), dm

def masses(r, dm):
    order = np.argsort(r); rs = r[order]
    m_in = CORE + dm * np.arange(N)                         # mass strictly inside each sorted shell (+ core)
    return order, rs, m_in

def accel(r, dm):
    order, rs, m_in = masses(r, dm)
    m_out = m_in + dm
    a_s = -1 / rs ** 2
    if not MUT:
        a_s = a_s + (m_out ** 3 - m_in ** 3) / (3 * dm * rs ** 4)
    a = np.empty(N); a[order] = a_s
    return a

def energy(r, v, dm):
    order, rs, m_in = masses(r, dm)
    E = 0.5 * dm * np.sum(v ** 2) - dm * np.sum(1 / rs)
    if not MUT:
        m_out = m_in + dm
        # (1/3) int m^3/r^4: core-only between RMIN and first shell, then m_out between consecutive shells, to infinity
        E += (CORE ** 3) * (RMIN ** -3 - rs[0] ** -3) / 9
        E += np.sum(m_out[:-1] ** 3 * (rs[:-1] ** -3 - rs[1:] ** -3)) / 9 + m_out[-1] ** 3 * rs[-1] ** -3 / 9
    return float(E)

# K1: force vs finite difference of the discrete energy (one shell)
r0, v0, dm0 = init("uniform")
i = 1234; h = 1e-6
rp = r0.copy(); rp[i] += h; rm = r0.copy(); rm[i] -= h
fd = -(energy(rp, v0, dm0) - energy(rm, v0, dm0)) / (2 * h) / dm0
an = accel(r0, dm0)[i]
k1 = abs(fd / an - 1) <= 1e-6
P_(f"K1 force from finite differences of E vs analytic: {fd:.9e} vs {an:.9e} (rel {abs(fd / an - 1):.1e}): {'PASS' if k1 else 'FAIL'}")

RAD = [2.0, 5.0, 10.0, 20.0]
res, r1_ok, k2_ok = {"K1": bool(k1)}, True, True
for kind in (["law"] if MUT else ["law", "uniform", "1.5x", "0.5x"]):
    r, v, dm = init(kind)
    E0 = energy(r, v, dm)
    a = accel(r, dm)
    samples = []
    nsteps = int(TEND / DT)
    for n in range(nsteps):
        v += 0.5 * DT * a; r += DT * v
        low = r < RMIN; r[low] = 2 * RMIN - r[low]; v[low] = -v[low]
        a = accel(r, dm); v += 0.5 * DT * a
        t = (n + 1) * DT
        if t >= 2000 and n % 200 == 0:
            rs = np.sort(r); samples.append([(CORE + dm * np.searchsorted(rs, R)) / R for R in RAD])
    E1 = energy(r, v, dm)
    dE = abs(E1 - E0) / abs(E0)
    order, rs, m_in = masses(r, dm)
    pot = -dm * np.sum(1 / rs)
    ke = 0.5 * dm * np.sum(v ** 2)
    esc = float(np.sum(r > 1000) * dm)
    mr = np.mean(samples, axis=0) if samples else [float('nan')] * 4
    final_m2 = (CORE + dm * np.searchsorted(np.sort(r), 2.0)) / 2.0
    res[kind] = dict(dE_rel=dE, m_over_r=dict(zip(map(str, RAD), map(float, mr))), KE=ke, pot_baryon=pot, escaped_mass=esc, final_m2_over_2=float(final_m2))
    k2_ok &= dE <= 1e-3
    if kind != "law":
        r1_ok &= all(abs(x - 1) <= 0.10 for x in mr)
    P_(f"{kind:8s}: dE/E {dE:.1e}; time-avg m/r at r = 2/5/10/20: " + " / ".join(f"{x:.3f}" for x in mr) +
       f"; KE {ke:.3g}, baryon potential energy {pot:.3g}; escaped mass {esc:.3g}; final m(2)/2 {final_m2:.3f}")
if MUT:
    bite = res["law"]["final_m2_over_2"] > 1.5
    P_(f"MUTATE: control collapses without the cold-energy force (m(2)/2 > 1.5): {bite}"); rc = 1 if bite else 0
else:
    ctrl = all(abs(x - 1) <= 0.01 for x in res["law"]["m_over_r"].values())
    res["verdict"] = dict(K1=k1, K2=k2_ok, control=ctrl, R1="PASS" if r1_ok else "FAIL")
    P_(f"K2 energy conservation <= 1e-3: {k2_ok}; control (law) stays within 1%: {ctrl}; R1 relaxation onto the law: {'PASS' if r1_ok else 'FAIL'}")
    json.dump(res, open(os.path.join(HERE, "cfg747_results.json"), "w"), indent=1, default=lambda o: bool(o) if isinstance(o, np.bool_) else float(o)); rc = 0
open(os.path.join(HERE, f"cfg747{TAG}.out"), "w").write("\n".join(lines) + "\n"); sys.exit(rc)
