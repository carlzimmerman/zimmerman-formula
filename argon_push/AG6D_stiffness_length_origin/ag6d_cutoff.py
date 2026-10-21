#!/usr/bin/env python3
"""AG6D Part C1: if the FREE cold medium carries the stiffness (Part A: c_s^2 = 2 pi G L*^2 rho_bar, k_J,phys = sqrt2/L*),
its linear growth is cut off. FROZEN_CRITERIA.md section 4 (b94d6b89b).

  dc'' + (2 + dlnH/dlna) dc' = 1.5 Om(a) [ fc dc (1 - (L* k/a)^2/2) + fb db ]      (' = d/dln a, k comoving)
  db = 0 for a < 1/1091, then pressureless with the same gravity term.
Each mode starts at horizon entry (k = aH/c) with dc = 1, dc' = 1 (sensitivity 0 and 2); reference: same with L* = 0.
T(k) = dm(L*)/dm(0) at a = 1/50. Reported: k_1/2, M_1/2, and L*_IC = largest L* with T(k_Ny) >= 0.9, k_Ny = pi*1024/200 h/Mpc.

POST-HOC VARIANT (disclosed; not in the frozen text): the Newtonian c_s^2 = gamma rho_bar exceeds c^2 at early times
(at z > ~6e4-7e5 inside the window). Variant "cap" limits the pressure term to c_s^2 <= c^2/3. The frozen class is read from
the uncapped run; the variant is reported as a sensitivity.
Controls: K1 T(0.05/Mpc; 24 pc) = 1 within 1e-3; K2 Meszaros growing mode D = 1 + 3y/2 within 1e-5.
MUTATE (AG6D_MUTATE=1): gamma = 0 (T == 1); the class must change -> exit 1 by design.
"""
import json, os, sys, time
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

MUT = os.environ.get("AG6D_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
HERE = os.path.dirname(os.path.abspath(__file__))
out_lines = []


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    out_lines.append(s)


h = 0.677
Om = 0.31
Or = 4.15e-5 / h**2
OL = 1 - Om - Or
fc = 5.364 / 6.364
fb = 1 / 6.364
H0c = h / 2997.92458          # H0/c in 1/Mpc
a_dec = 1 / 1091.0
a_end = 1 / 50.0
kNy_hMpc = np.pi * 1024 / 200.0
kNy = kNy_hMpc * h            # 1/Mpc
a_eq = Or / Om


def E2(a, OmL=OL):
    return Om / a**3 + Or / a**4 + OmL


def kH(a):
    return a * np.sqrt(E2(a)) * H0c


def a_entry(k):
    return np.exp(brentq(lambda x: np.log(kH(np.exp(x))) - np.log(k), -30, np.log(a_end)))


def rhs_factory(k, Lmpc, cap, fcv=fc, fbv=fb, OmL=OL, baryons=True):
    def rhs(x, s):
        a = np.exp(x)
        e2 = Om / a**3 + Or / a**4 + OmL
        dlnH = (-3 * Om / a**3 - 4 * Or / a**4) / (2 * e2)
        oma = Om / a**3 / e2
        J = 0.5 * (Lmpc * k / a)**2
        press = 1.5 * oma * fcv * J
        if cap:
            kh = a * np.sqrt(e2) * H0c
            press = min(press, (k / kh)**2 / 3.0)
        dc, dc1, db, db1 = s
        fr = -(2 + dlnH)
        ddc = fr * dc1 + 1.5 * oma * (fcv * dc + fbv * db) - press * dc
        if baryons and a >= a_dec:
            ddb = fr * db1 + 1.5 * oma * (fcv * dc + fbv * db)
        else:
            ddb = 0.0
        return [dc1, ddc, db1 if (baryons and a >= a_dec) else 0.0, ddb]
    return rhs


def grow(k, Lpc, cap=False, d1=1.0):
    Lmpc = 0.0 if MUT else Lpc * 1e-6
    aH = a_entry(k)
    rhs = rhs_factory(k, Lmpc, cap)
    s0 = [1.0, d1, 0.0, 0.0]
    xs = [np.log(aH)]
    if aH < a_dec:
        xs.append(np.log(a_dec))
    xs.append(np.log(a_end))
    s = s0
    for x0, x1 in zip(xs[:-1], xs[1:]):
        sol = solve_ivp(rhs, (x0, x1), s, method="DOP853", rtol=1e-9, atol=1e-13)
        if not sol.success:
            raise RuntimeError(sol.message)
        s = sol.y[:, -1]
    return fc * s[0] + fb * s[2]


_ref = {}


def T(k, Lpc, cap=False, d1=1.0):
    key = (round(k, 12), d1)
    if key not in _ref:
        _ref[key] = grow(k, 0.0, False, d1)
    return grow(k, Lpc, cap, d1) / _ref[key]


res = {"lane": "AG6D", "part": "C1", "mutate": MUT,
       "inputs": {"h": h, "Om": Om, "Or": Or, "fc": fc, "a_dec": a_dec, "a_end": a_end, "kNy_hMpc": kNy_hMpc, "kNy_Mpc": kNy}}
t0 = time.time()

# ---------------- K2: Meszaros ------------------------------------------------------------------------------
def k2():
    rhs = rhs_factory(1.0, 0.0, False, fcv=1.0, fbv=0.0, OmL=0.0, baryons=False)
    y0, y1 = 1e-3, 100.0
    x0, x1 = np.log(y0 * a_eq), np.log(y1 * a_eq)
    sol = solve_ivp(rhs, (x0, x1), [1 + 1.5 * y0, 1.5 * y0, 0, 0], method="DOP853", rtol=1e-11, atol=1e-14, dense_output=True)
    ys = np.logspace(-3, 2, 30)
    num = sol.sol(np.log(ys * a_eq))[0]
    return float(np.max(np.abs(num / (1 + 1.5 * ys) - 1)))


k2err = k2()
P(f"K2 Meszaros growing mode: max |D_num/(1+3y/2) - 1| = {k2err:.2e}  -> {'PASS' if k2err < 1e-5 else 'FAIL'}")
k1T = T(0.05, 24.0)
P(f"K1 T(k=0.05/Mpc, L*=24 pc) = {k1T:.6f}  -> {'PASS' if abs(k1T-1) < 1e-3 else 'FAIL'}")
res["K1"] = {"T": k1T, "pass": abs(k1T - 1) < 1e-3}
res["K2"] = {"err": k2err, "pass": k2err < 1e-5}

# ---------------- T(k) tables -------------------------------------------------------------------------------
Ls = [24.0, 50.0, 100.0, 300.0, 1000.0]
kgrid = np.logspace(np.log10(0.05), np.log10(200.0), 49)
rho_m0 = Om * 2.775e11 * h**2  # Msun / Mpc^3
tables = {}


def khalf(Lpc, cap, d1, grid=kgrid):
    prev_k, prev_T = None, None
    rows = []
    small = 0
    for k in grid:
        t = T(k, Lpc, cap, d1)
        rows.append((float(k), float(t)))
        if prev_T is not None and prev_T >= 0.5 > t:
            # log-linear interpolation
            f = (np.log(prev_T) - np.log(0.5)) / (np.log(prev_T) - np.log(max(t, 1e-300)))
            kh_ = float(np.exp(np.log(prev_k) + f * (np.log(k) - np.log(prev_k))))
            return kh_, rows
        prev_k, prev_T = k, t
        small = small + 1 if t < 1e-3 else 0
    return None, rows


for cap in (False, True):
    lab = "cap" if cap else "frozen"
    tables[lab] = {}
    P(f"\n=== T(k) at z = 49, variant {lab} ({'c_s^2 <= c^2/3, POST HOC' if cap else 'uncapped, as frozen'}) ===")
    for Lpc in Ls:
        kh_, rows = khalf(Lpc, cap, 1.0)
        Mh = (4 * np.pi / 3) * rho_m0 * (np.pi / kh_)**3 if kh_ else None
        kJeq = np.sqrt(2) * a_eq / (Lpc * 1e-6)
        TkNy = T(kNy, Lpc, cap, 1.0)
        sens = {}
        for d1 in (0.0, 2.0):
            g2 = np.logspace(np.log10(0.05), np.log10(200.0), 25)
            sens[d1] = khalf(Lpc, cap, d1, grid=g2)[0]
        tables[lab][f"{Lpc:.0f}"] = {"k_half_Mpc": kh_, "k_half_hMpc": kh_ / h if kh_ else None, "M_half_Msun": Mh,
                                     "k_Jeans_at_aeq_Mpc": kJeq, "T_kNy": TkNy, "k_half_d1_0": sens[0.0],
                                     "k_half_d1_2": sens[2.0], "rows": rows}
        P(f"  L* = {Lpc:6.0f} pc: k_1/2 = {kh_ if kh_ else float('nan'):.3f} /Mpc = {(kh_/h) if kh_ else float('nan'):.3f} h/Mpc "
          f"(IC d' = 0 / 2: {sens[0.0] if sens[0.0] else float('nan'):.3f} / {sens[2.0] if sens[2.0] else float('nan'):.3f}); "
          f"M_1/2 = {Mh if Mh else float('nan'):.2e} Msun; sqrt2 a_eq/L* = {kJeq:.3f} /Mpc; T(k_Ny = {kNy_hMpc:.2f} h/Mpc) = {TkNy:.4f}"
          f"   [{time.time()-t0:.0f} s]")

# ---------------- L*_IC ------------------------------------------------------------------------------------
LIC = {}
for cap in (False, True):
    for d1 in ((1.0, 0.0, 2.0) if not cap else (1.0,)):
        lab = ("cap" if cap else "frozen") + f"_d1={d1:g}"
        grid = np.logspace(0, 3, 31)
        Tg = [T(kNy, L, cap, d1) for L in grid]
        idx = next((i for i, t in enumerate(Tg) if t < 0.9), None)
        if idx is None:
            val = ">= 1000"
            num = 1000.0
        elif idx == 0:
            val = "< 1"
            num = 1.0
        else:
            lo, hi = np.log(grid[idx - 1]), np.log(grid[idx])
            num = float(np.exp(brentq(lambda x: T(kNy, np.exp(x), cap, d1) - 0.9, lo, hi, xtol=1e-4)))
            val = f"{num:.2f}"
        mono = bool(np.all(np.diff(Tg) <= 1e-9))
        LIC[lab] = {"L_IC_pc": num, "label": val, "T_monotone_in_L": mono, "T_grid": list(map(float, Tg))}
        P(f"L*_IC ({lab}): {val} pc  (T(k_Ny) monotone in L* on the grid: {mono})   [{time.time()-t0:.0f} s]")
res["tables"] = tables
res["L_IC"] = LIC


def cls_of(v):
    if v >= 1000.0:
        return "NO CONFLICT"
    if v >= 24.0:
        return f"NARROWS THE WINDOW to [24, {v:.0f}] pc"
    return "CONFLICT"


frozen_cls = cls_of(LIC["frozen_d1=1"]["L_IC_pc"])
res["class_frozen"] = frozen_cls
res["class_cap_variant"] = cls_of(LIC["cap_d1=1"]["L_IC_pc"])
P(f"\nCLASS (frozen, uncapped, IC d'=1): {frozen_cls}")
P(f"   post-hoc cap variant: {res['class_cap_variant']}; IC sensitivity: d'=0 {cls_of(LIC['frozen_d1=0']['L_IC_pc'])}, "
  f"d'=2 {cls_of(LIC['frozen_d1=2']['L_IC_pc'])}")
ok = res["K1"]["pass"] and res["K2"]["pass"]
if MUT:
    P("MUTATE run (gamma = 0): the class above must read NO CONFLICT; compare with the real run's class -> exit 1 by design")
with open(os.path.join(HERE, f"ag6d_cutoff_results{TAG}.json"), "w") as fh:
    json.dump(res, fh, indent=1, default=float)
with open(os.path.join(HERE, f"ag6d_cutoff{TAG}.out"), "w") as fh:
    fh.write("\n".join(out_lines) + "\n")
sys.exit(1 if (MUT or not ok) else 0)
