"""CFG776 -- the frozen relic (H-FR): cold energy tethered at a system's peak condensed mass, evolved after the loss under
CFG747's own collisionless dynamics.  Criteria: FROZEN_CRITERIA.md (committed alone first, e2863f3ae).
Units G = a0 = M_now = 1 (CFG747).  Sudden loss: start at rest on the law profile of the peak mass p, m = sqrt(p) (r - RMIN) + CORE.
Run: OMP_NUM_THREADS=1 nice -n 10 python3 cfg776.py   (CFG776_MUTATE=1: no cubic push).  ~10 min, < 100 MB.
kappa = 1/2 FITTED; the cold energy's mass is required; no particle species; not "theory closed".
"""
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
MUT = os.environ.get("CFG776_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
N, RMIN, R0, DT, CORE = 4000, 0.5, 50.0, 0.005, 0.5
TSNAP = [50, 100, 150, 200, 300, 500, 1000, 2000, 3000]
RAD = [2.0, 5.0, 8.0, 11.0, 25.0]
LINES = [__doc__.strip()]


def P(s):
    print(s, flush=True)
    LINES.append(s)


def init(p):
    mtot = math.sqrt(p) * (R0 - CORE)
    dm = mtot / N
    q = (np.arange(N) + 0.5) / N
    r = RMIN + q * (R0 - RMIN)
    return r, np.zeros(N), dm


def accel(r, dm):
    order = np.argsort(r)
    rs = r[order]
    m_in = CORE + dm * np.arange(N)
    a_s = -1 / rs ** 2
    if not MUT:
        a_s = a_s + ((m_in + dm) ** 3 - m_in ** 3) / (3 * dm * rs ** 4)
    a = np.empty(N)
    a[order] = a_s
    return a


def energy(r, v, dm):
    rs = np.sort(r)
    m_in = CORE + dm * np.arange(N)
    E = 0.5 * dm * np.sum(v ** 2) - dm * np.sum(1 / rs)
    if not MUT:
        m_out = m_in + dm
        E += (CORE ** 3) * (RMIN ** -3 - rs[0] ** -3) / 9
        E += np.sum(m_out[:-1] ** 3 * (rs[:-1] ** -3 - rs[1:] ** -3)) / 9 + m_out[-1] ** 3 * rs[-1] ** -3 / 9
    return float(E)


RES = {"lane": "CFG776", "mutate": MUT, "runs": {}}
for p in ([2.0] if MUT else [1.0, 1.5, 2.0, 3.0]):
    r, v, dm = init(p)
    E0 = energy(r, v, dm)
    a = accel(r, dm)
    snaps = {}
    win = {T: [] for T in TSNAP}                       # average m/r over [0.9T, T] to suppress orbital ringing
    nsteps = int(TSNAP[-1] / DT)
    for n in range(nsteps):
        v += 0.5 * DT * a
        r += DT * v
        low = r < RMIN
        r[low] = 2 * RMIN - r[low]
        v[low] = -v[low]
        a = accel(r, dm)
        v += 0.5 * DT * a
        t = (n + 1) * DT
        if n % 100 == 0:
            for T in TSNAP:
                if 0.9 * T <= t <= T:
                    rs = np.sort(r)
                    win[T].append([(CORE + dm * np.searchsorted(rs, R)) / R for R in RAD])
    for T in TSNAP:
        mr = np.mean(win[T], axis=0)
        f = (mr - 1) / (math.sqrt(p) - 1) if p > 1 else mr - 1
        snaps[str(T)] = dict(m_over_r=[float(x) for x in mr], relic_fraction=[float(x) for x in f])
    dE = abs(energy(r, v, dm) - E0) / abs(E0)
    RES["runs"][str(p)] = dict(snaps=snaps, dE=dE)
    P(f"p {p}: dE/E {dE:.1e}")
    for T in TSNAP:
        s = snaps[str(T)]
        P(f"   t {T:5d}: m/r at r = " + "/".join(f"{x:.3f}" for x in s["m_over_r"]) + "   relic fraction " +
          "/".join(f"{x:+.3f}" for x in s["relic_fraction"]) + f"   (r = {'/'.join(str(x) for x in RAD)})")

if MUT:
    s = RES["runs"]["2.0"]["snaps"]["3000"]["m_over_r"]
    held = all(abs(x - math.sqrt(2.0)) > 0.2 for x in s[:3])
    P(f"MUTATE (no push): m/r at t 3000 = {s}; relic NOT expelled / profile not the law: {'bites' if held else 'DID NOT BITE'}")
    open(os.path.join(HERE, f"cfg776{TAG}.out"), "w").write("\n".join(LINES) + "\n")
    json.dump(RES, open(os.path.join(HERE, f"cfg776_results{TAG}.json"), "w"), indent=1)
    sys.exit(1)

# ---------------------------------------------------------------- controls
law = RES["runs"]["1.0"]["snaps"]
k1 = all(abs(x - 1) <= 0.01 for T in TSNAP for x in law[str(T)]["m_over_r"][:4])
k2 = all(v["dE"] <= 1e-3 for v in RES["runs"].values())
P(f"\nK1 p = 1 control within 1% at r <= 11 for all t: {k1};  K2 dE/E <= 1e-3 every run: {k2}")

# ---------------------------------------------------------------- physical clocks + KiDS prediction
G, MSUN, KPC, GYR = 6.674e-11, 1.989e30, 3.0857e19, 3.156e16
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}


def tacconi_p(z, lmstar):
    lmu = 0.12 - 3.62 * (math.log10(1 + z) - 0.66) ** 2 - 0.35 * (lmstar - 10.7)
    return (1 + 10 ** lmu) / 0.9


def relic_f(p, t, rr):
    """interpolate the relic fraction from the run nearest in p (exact for bracket p), in log t and log r."""
    keys = [1.5, 2.0, 3.0]
    pk = min(keys, key=lambda k: abs(k - p))
    S = RES["runs"][str(pk)]["snaps"]
    ts = np.array(TSNAP, float)
    tt = min(max(t, ts[0]), ts[-1])
    F = np.array([S[str(T)]["relic_fraction"] for T in TSNAP])       # (t, r)
    col = np.array([np.interp(math.log(tt), np.log(ts), F[:, j]) for j in range(len(RAD))])
    rq = min(max(rr, RAD[0]), RAD[-1])
    return float(np.interp(math.log(rq), np.log(RAD), col)), pk, t > ts[-1]


p_prim = tacconi_p(1.5, 10.8)
P(f"\nD3 peak ratio (Tacconi+18 MS scaling, PROVISIONAL coefficients): z_q 1.5, logM* 10.8 -> mu {p_prim * 0.9 - 1:.3f}, p = {p_prim:.3f};"
  f"  z_q 1.0 -> p = {tacconi_p(1.0, 10.8):.3f}; z_q 2.0 -> p = {tacconi_p(2.0, 10.8):.3f}")
RK = [50.0, 70.71, 100.0]
T1 = {}
for f, a0 in A0.items():
    for lmb in (10.5, 11.0, 11.5):
        M = 10 ** lmb * MSUN
        rM = math.sqrt(G * M / a0)
        t0 = math.sqrt(rM / a0)
        for tau in (8.0, 10.0):
            n = tau * GYR / t0
            for plab, p in (("tacconi", p_prim), ("1.5", 1.5), ("2", 2.0), ("3", 3.0)):
                d = []
                for R in RK:
                    x = R * KPC / rM
                    fr, pk, capped = relic_f(p, n, x)
                    m_law = x
                    m_rel = x * (1 + fr * (math.sqrt(p) - 1))
                    d.append(math.log10((1 + m_rel) / (1 + m_law)))
                D = float(np.mean(d))
                pred = -0.027 + D
                T1[f"{f}|{lmb}|{tau}|{plab}"] = dict(r_M_kpc=rM / KPC, t0_Myr=t0 / GYR * 1e3, n=n, Delta=D, pred=pred,
                                                    Z=(0.280 - pred) / 0.083, x_K=[R * KPC / rM for R in RK])
    P(f"\nT1 {f}: (pred = -0.027 + Delta; obs +0.280 +- 0.083)")
    for lmb in (10.5, 11.0, 11.5):
        for tau in (8.0, 10.0):
            row = [T1[f"{f}|{lmb}|{tau}|{pl}"] for pl in ("tacconi", "1.5", "2", "3")]
            P(f"  logM_b {lmb} tau {tau:4.1f} Gyr: r_M {row[0]['r_M_kpc']:.1f} kpc, t0 {row[0]['t0_Myr']:.0f} Myr, n {row[0]['n']:.0f}, "
              f"K radii {'/'.join(f'{x:.1f}' for x in row[0]['x_K'])} r_M | pred (Tacconi p {p_prim:.2f}) {row[0]['pred']:+.3f} (Z {row[0]['Z']:+.2f})"
              f"; p 1.5/2/3: " + "/".join(f"{x['pred']:+.3f}" for x in row[1:]))
prim = [T1[f"{f}|11.0|10.0|tacconi"] for f in A0]
t1 = any(abs(x["Z"]) < 2 for x in prim)
P(f"\nT1 HEADLINE (logM_b 11.0, tau 10 Gyr, Tacconi p): canonical {prim[0]['pred']:+.3f} (Z {prim[0]['Z']:+.2f}), alt {prim[1]['pred']:+.3f} "
  f"(Z {prim[1]['Z']:+.2f}) -> {'PASS' if t1 else 'FAIL'}")

# ---------------------------------------------------------------- T2 UFD erasure
P("\nT2 UFD erasure (relic fraction at 25 r_M; n capped at the simulated 3000 t0)")
T2 = {}
for f, a0 in A0.items():
    for lm in (3, 4, 5):
        M = 10 ** lm * MSUN
        rM = math.sqrt(G * M / a0)
        t0 = math.sqrt(rM / a0)
        n = 13 * GYR / t0
        fr, pk, capped = relic_f(3.0, n, 25.0)
        T2[f"{f}|{lm}"] = dict(t0_Myr=t0 / GYR * 1e3, n=n, relic_25=fr, capped=capped)
        P(f"  {f:9s} logM {lm}: t0 {t0 / GYR * 1e3:.2f} Myr, n {n:.0f}{' (capped 3000)' if capped else ''}: relic fraction at 25 r_M {fr:+.3f}")
t2 = all(abs(v["relic_25"]) <= 0.1 for v in T2.values())
P(f"T2: relic erased in UFDs (|f| <= 0.1): {t2} -> " + ("H-FR cannot explain the UFDs; their +0.33 dex failure stands" if t2 else "frozen line fails: |f| > 0.1 (sign shown: negative = DEFICIT below the law, not survival)"))

RES.update(dict(K1=k1, K2=k2, p_tacconi=p_prim, T1=T1, T1_pass=t1, T2=T2, T2_erased=t2))
json.dump(RES, open(os.path.join(HERE, "cfg776_results.json"), "w"), indent=1, default=lambda o: bool(o) if isinstance(o, np.bool_) else float(o))
open(os.path.join(HERE, "cfg776.out"), "w").write("\n".join(LINES) + "\n")
sys.exit(0 if (k1 and k2) else 1)
