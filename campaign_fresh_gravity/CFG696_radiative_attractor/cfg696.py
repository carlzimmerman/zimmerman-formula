"""CFG696: does the polarization field relax onto the law's profile by radiating P waves? (M1a attractor + M2b energy ledger)

Criteria: FROZEN_CRITERIA.md (committed alone, 30a4ff252). Point mass, CFG691 units. v = s q:
    v_tt = v'' - 2 v/s^2 - v|v|/s + 1/s,   v(0) = 0,   outgoing at s = S:  v_t = -v_s + 1/s^2  (static asymptote 1 - 1/s).
Lagrangian density L = v_t^2/2 - v_s^2/2 - v^2/s^2 - |v|^3/(3s) + v/s  =>  E = int e ds, dE/dt = (v_s v_t)|_S.
kappa = 1/2 FITTED; footings never pooled; the cold energy's mass is required; no particle species; not "theory closed".

Run:  OMP_NUM_THREADS=1 nice -n 10 python3 cfg696.py      (CFG696_MUTATE=1: reflecting boundary, flux omitted; exit 1 iff both bite)
"""
import os, sys, json, math

import numpy as np
from scipy.integrate import solve_bvp

HERE = os.path.dirname(os.path.abspath(__file__))
LANES = os.path.dirname(HERE)
MUT = os.environ.get("CFG696_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
OUT = open(os.path.join(HERE, f"cfg696{TAG}.out"), "w")
RES = {"lane": "CFG696", "criteria": "30a4ff252", "mutate": MUT, "checks": {}, "numbers": {}}


def P_(s=""):
    print(s, flush=True)
    OUT.write(s + "\n")


def check(key, ok, detail):
    RES["checks"][key] = dict(ok=bool(ok), detail=detail)
    P_(f"  [{'PASS' if ok else 'FAIL'}] {key}: {detail}")
    return bool(ok)


P_(__doc__.strip())

# ---------------------------------------------------------------- static profile (CFG691's BVP)
def f(t, y):
    s = np.exp(t)
    return np.vstack([y[1], -y[1] + 2.0 * y[0] + s ** 2 * y[0] * np.abs(y[0]) - 1.0])


tt = np.linspace(math.log(1e-4), math.log(1e4), 4001)
ss = np.exp(tt)
SOL = solve_bvp(f, lambda ya, yb: np.array([ya[1] - (ya[0] - 0.5), yb[0] - (1e-4 - 1e-8)]), tt,
                np.vstack([1 / (ss + 2), -ss / (ss + 2) ** 2]), tol=1e-8, max_nodes=200000)
c691 = json.load(open(os.path.join(LANES, "CFG691_stiffness_window", "cfg691_results.json")))["numbers"]["profile"]["S_table"]
dS = max(abs(float(k) * float(SOL.sol(math.log(float(k)))[0]) - v) for k, v in c691.items())

S_MAX, DS, DT, T_END = 200.0, 0.02, 0.01, 2000.0
s = np.arange(0, S_MAX + DS / 2, DS)
N = s.size
si = s.copy(); si[0] = 1.0                                             # avoid 0 division (v(0) = 0 enforced)
q_st = np.where(s > 0, np.array([float(SOL.sol(math.log(max(x, 1e-4)))[0]) for x in s]), 0.5)
v_st = s * q_st


def accel(v):
    a = np.zeros_like(v)
    a[1:-1] = (v[2:] - 2 * v[1:-1] + v[:-2]) / DS ** 2 - 2 * v[1:-1] / si[1:-1] ** 2 - v[1:-1] * np.abs(v[1:-1]) / si[1:-1] + 1 / si[1:-1]
    return a


# K1: the discrete operator's static residual on CFG691's profile
res = accel(v_st)
band = (s >= 0.1) & (s <= 50)
k1_rel = float(np.max(np.abs(res[band]) / (1 / si[band])))
check("K1 static profile = CFG691 BVP (S table), discrete residual relative to the source <= 1e-3",
      dS <= 1e-6 and k1_rel <= 1e-3, f"|dS| {dS:.1e}; discrete residual / (1/s) max on [0.1, 50] = {k1_rel:.1e}")


def energy(v, vt):
    vs = np.gradient(v, DS)
    e = 0.5 * vt ** 2 + 0.5 * vs ** 2 + np.where(s > 0, v ** 2 / si ** 2 + np.abs(v) ** 3 / (3 * si) - v / si, 0.0)
    return float(np.trapz(e, s))


def run(v0, reflecting=False, label=""):
    v_old = v0.copy(); v_old[0] = 0.0
    v = v_old + 0.5 * DT ** 2 * accel(v_old)                          # v_t(0) = 0
    v[0] = 0.0
    if reflecting:
        v[-1] = v_st[-1]
    else:
        v[-1] = v_old[-1] + DT * (-(v_old[-1] - v_old[-2]) / DS + 1 / S_MAX ** 2)
    E0 = energy(v_old, np.zeros_like(v_old))
    flux_int, t, rows = 0.0, DT, []
    marks = {500.0, 1000.0, 1500.0, 2000.0}
    nsteps = int(round(T_END / DT))
    for n in range(1, nsteps):
        v_new = 2 * v - v_old + DT ** 2 * accel(v)
        v_new[0] = 0.0
        if reflecting:
            v_new[-1] = v_st[-1]
        else:
            v_new[-1] = v[-1] + DT * (-(v[-1] - v[-2]) / DS + 1 / S_MAX ** 2)
        vt_S = (v_new[-1] - v_old[-1]) / (2 * DT)
        vs_S = (v[-1] - v[-2]) / DS
        flux_int += -vs_S * vt_S * DT                                    # energy leaving through S (dE/dt = v_s v_t)
        v_old, v = v, v_new
        t = (n + 1) * DT
        if any(abs(t - m) < DT / 2 for m in marks) or n == nsteps - 1:
            vt = (v - v_old) / DT
            q = np.where(s > 0, v / si, 0.0)
            err = float(np.max(np.abs(q[band] - q_st[band]) / q_st[band]))
            E = energy(v, vt)
            rows.append(dict(t=round(t, 2), max_rel_err=err, E=E, dE=E0 - E, flux_out=flux_int, Mc50=float(50 * np.interp(50, s, v))))
            P_(f"    {label:24s} t = {t:7.1f}: max|q - q_static|/q_static on [0.1,50] = {err:.3e};  E0 - E = {E0 - E:+.5e};  "
               f"radiated = {flux_int:+.5e};  bound charge s*v at s=50: {50 * np.interp(50, s, v):.3f} (static {50 * np.interp(50, s, v_st):.3f})")
    return rows


INIT = {"(i) zero": np.zeros(N), "(ii) 2x static": 2 * v_st, "(iii) 0.5x static": 0.5 * v_st, "(iv) 1 - exp(-s)": 1 - np.exp(-s)}
A1, A2 = {}, {}
P_(f"\nA1/A2  grid ds = {DS}, dt = {DT}, S = {S_MAX}, t_end = {T_END}; {'REFLECTING (M1)' if MUT else 'outgoing'} boundary")
for k, v0 in INIT.items():
    rows = run(v0, reflecting=MUT, label=k)
    last, mid = rows[-1], rows[1]
    A1[k] = dict(final=last["max_rel_err"], mid=mid["max_rel_err"], ok=bool(last["max_rel_err"] <= 0.01 and last["max_rel_err"] <= mid["max_rel_err"]))
    flux = 0.0 if MUT else last["flux_out"]                              # M2: flux omitted when MUTATE
    bal = abs(last["dE"] - flux) / max(abs(last["dE"]), 1e-12)
    A2[k] = dict(dE=last["dE"], radiated=last["flux_out"], rel_mismatch=bal, ok=bool(bal <= 0.01))
    RES["numbers"][k] = rows
a1 = check("A1 every non-law initial state relaxes to the law's profile (<= 1% on [0.1, 50] at t = 2000, decreasing)",
           all(v["ok"] for v in A1.values()), "; ".join(f"{k}: {v['final']:.2e}" for k, v in A1.items()))
a2 = check("A2 energy lost = energy radiated by outgoing P waves (within 1%)", all(v["ok"] for v in A2.values()),
           "; ".join(f"{k}: mismatch {v['rel_mismatch']:.2e}" for k, v in A2.items()))
RES["numbers"]["A1"] = A1; RES["numbers"]["A2"] = A2

# ---------------------------------------------------------------- A4 timescales (reported)
P_("\nA4  (reported) physical relaxation time = t_code * l_gamma / c_P, l_gamma = L*^2 / (2 r_M), L* = 5.75 pc, a0 = 9.36e-11")
G, MSUN, PC, C = 6.6743e-11, 1.98847e30, 3.0856775814913673e16, 2.99792458e8
t_code = next((r["t"] for r in RES["numbers"]["(i) zero"] if r["max_rel_err"] <= 0.01), None)
for name, M in (("galaxy 1e10 Msun", 1e10 * MSUN), ("Sun", MSUN)):
    ell = (5.75 * PC) ** 2 / (2 * math.sqrt(G * M / 9.3603e-11))
    for cp in (C, 1e-3 * C):
        if t_code:
            P_(f"    {name:17s} l_gamma {ell / PC:.3g} pc; c_P = {cp / C:g} c: t_relax ~ {t_code * ell / cp / 3.156e7:.3g} yr "
               f"(code time {t_code}; scale-free in s, so the relaxed region grows at c_P)")
P_("    I (equivalently c_P) is not fixed by any gate so far: a constant, unless c_P = c is derived.")

if MUT:
    bites = dict(M1=not a1, M2=not a2)
    RES["mutate_bites"] = bites
    P_(f"\nMUTATE: {bites}")
    rc = 1 if all(bites.values()) else 0
else:
    RES["verdict"] = dict(M1a="PASS" if a1 else "FAIL", M2b="PASS" if a2 else "FAIL")
    P_(f"\nVERDICT: M1a {RES['verdict']['M1a']}; M2b {RES['verdict']['M2b']}")
    rc = 0
json.dump(RES, open(os.path.join(HERE, f"cfg696_results{TAG}.json"), "w"), indent=1, default=float)
OUT.close()
sys.exit(rc)
