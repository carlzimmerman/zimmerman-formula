"""CFG744: does radiative relaxation reach galaxy scales? Criteria: FROZEN_CRITERIA.md (3cfc8fd02).
kappa = 1/2 FITTED; footings never pooled; the cold energy's mass is required; no particle species; not "theory closed".
Run:  OMP_NUM_THREADS=1 nice -n 10 python3 cfg744.py      (CFG744_MUTATE=1: reflecting boundary; exit 1 iff s0 = 80 never relaxes)
"""
import os, sys, json, math
import numpy as np
from scipy.integrate import solve_bvp
HERE = os.path.dirname(os.path.abspath(__file__)); LANES = os.path.dirname(HERE); sys.path.insert(0, LANES)
import CFG4_common as C4  # noqa: E402
MUT = os.environ.get("CFG744_MUTATE", "0") == "1"; TAG = "_MUTATE" if MUT else ""
lines = [__doc__.strip()]
def P_(s): print(s, flush=True); lines.append(s)
def f(t, y):
    s = np.exp(t); return np.vstack([y[1], -y[1] + 2.0 * y[0] + s ** 2 * y[0] * np.abs(y[0]) - 1.0])
tt = np.linspace(math.log(1e-4), math.log(1e4), 4001); ss = np.exp(tt)
SOL = solve_bvp(f, lambda ya, yb: np.array([ya[1] - (ya[0] - 0.5), yb[0] - (1e-4 - 1e-8)]), tt, np.vstack([1 / (ss + 2), -ss / (ss + 2) ** 2]), tol=1e-8, max_nodes=200000)
S_MAX, DS, DT, T_END = 400.0, 0.05, 0.025, 4000.0
s = np.arange(0, S_MAX + DS / 2, DS); si = s.copy(); si[0] = 1.0
q_st = np.where(s > 0, np.array([float(SOL.sol(math.log(max(x, 1e-4)))[0]) for x in s]), 0.5); v_st = s * q_st
def accel(v):
    a = np.zeros_like(v)
    a[1:-1] = (v[2:] - 2 * v[1:-1] + v[:-2]) / DS ** 2 - 2 * v[1:-1] / si[1:-1] ** 2 - v[1:-1] * np.abs(v[1:-1]) / si[1:-1] + 1 / si[1:-1]
    return a
S0 = [10, 20, 40, 80]
masks = {k: (s >= 0.8 * k) & (s <= 1.2 * k) for k in S0}
v_old = 2 * v_st.copy(); v_old[0] = 0
v = v_old + 0.5 * DT ** 2 * accel(v_old); v[0] = 0
last_above = {k: 0.0 for k in S0}
n_steps = int(T_END / DT)
for n in range(1, n_steps):
    vn = 2 * v - v_old + DT ** 2 * accel(v); vn[0] = 0
    vn[-1] = v_st[-1] if MUT else v[-1] + DT * (-(v[-1] - v[-2]) / DS + 1 / S_MAX ** 2)
    v_old, v = v, vn
    if n % 40 == 0:
        t = n * DT; q = v / si
        for k in S0:
            e = float(np.mean(np.abs(q[masks[k]] - q_st[masks[k]]) / q_st[masks[k]]))
            if e > 0.01: last_above[k] = t
t1 = {k: (last_above[k] if last_above[k] < T_END - 1 else None) for k in S0}
for k in S0:
    P_(f"N1  s0 = {k:3d}: t_1% = {t1[k]}   (theory sqrt(2) s0^1.5 = {math.sqrt(2) * k ** 1.5:.0f})")
res = {"t1pct": {str(k): t1[k] for k in S0}}
if MUT:
    P_(f"MUTATE: s0 = 80 never relaxes within t_end: {t1[80] is None}"); rc = 1 if t1[80] is None else 0
else:
    ks = [k for k in S0 if t1[k]]; slope = float(np.polyfit(np.log(ks), np.log([t1[k] for k in ks]), 1)[0])
    A = float(np.exp(np.mean([math.log(t1[k]) - 1.5 * math.log(k) for k in ks])))
    n1 = 1.2 <= slope <= 1.8
    P_(f"N1  log-log slope = {slope:.3f} (PASS iff in [1.2, 1.8]): {n1};  A (t = A s0^1.5) = {A:.3f}")
    G, C, MSUN, PC, YR = 6.6743e-11, 2.99792458e8, 1.98847e30, 3.0856775814913673e16, 3.15576e7
    Ls = json.load(open(os.path.join(LANES, "CFG691_stiffness_window", "cfg691_results.json")))["numbers"]["G_SS"]["canonical"]["Lmin_pc"] * PC
    def u_of(gN, a0):
        g = 0.5 * (gN + math.sqrt(gN * gN + 4 * gN * a0)); return g - gN
    ok_a, ok_b, N2 = True, True, {}
    for ft in C4.FOOTS:
        a0 = C4.A0[ft]
        for lm in (9, 10, 11):
            M = 10 ** lm * MSUN
            for y in (0.1, 1.0):
                r = math.sqrt(G * M / (y * a0)); h = r * 1e-5
                m2u = lambda rr: rr * rr * u_of(G * M / rr ** 2, a0)
                rho = (m2u(r + h) - m2u(r - h)) / (2 * h) / (4 * math.pi * G * r * r)
                ell = Ls ** 2 / (2 * math.sqrt(G * M / a0)); s0 = r / ell
                cp_a = math.sqrt(2 * math.pi * G * Ls ** 2 * rho)
                ta = A * s0 ** 1.5 * ell / cp_a / YR / 1e9; tb = A * s0 ** 1.5 * ell / C / YR / 1e9
                ok_a &= ta <= 4.6; ok_b &= tb <= 4.6
                t_cross = r / cp_a / YR / 1e9                                   # REPORTED (added after the first run): most optimistic, one crossing at c_P
                N2[f"{ft}|{lm}|{y}"] = dict(s0=s0, c_P_medium=cp_a, t_medium_Gyr=ta, t_light_Gyr=tb, t_medium_one_crossing_Gyr=t_cross)
                P_(f"    reported: medium, one crossing r/c_P = {t_cross:.3g} Gyr (exponent-free lower bound)")
                P_(f"N2  {ft:9s} M_b 1e{lm}, y {y}: s0 {s0:.2e}; (a) medium c_P {cp_a:.3g} m/s -> t {ta:.3g} Gyr; (b) c_P = c -> t {tb:.3g} Gyr")
    res.update(slope=slope, A=A, N2=N2, verdict=dict(scaling="PASS" if n1 else "FAIL", medium="PASS" if ok_a else "FAIL", light_field="PASS" if ok_b else "FAIL"))
    P_(f"VERDICT: scaling {res['verdict']['scaling']}; (a) cold-medium identification {res['verdict']['medium']}; (b) independent light field {res['verdict']['light_field']}")
    json.dump(res, open(os.path.join(HERE, "cfg744_results.json"), "w"), indent=1); rc = 0
open(os.path.join(HERE, f"cfg744{TAG}.out"), "w").write("\n".join(lines) + "\n"); sys.exit(rc)
