#!/usr/bin/env python3
"""CR2_core_scale_origin (FROZEN_CRITERIA.md): where S ~ M^0.24 comes from; self-coupling row. All inputs read from the record's tables."""
import json, math, os
import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
HERE = os.path.dirname(os.path.abspath(__file__))
T = np.array([[9.97, 68.6, 51.6, 85.0], [10.59, 102.7, 81.0, 124.2], [11.13, 143.2, 118.4, 199.8], [11.76, 150.2, 97.9, 190.5], [12.11, 215.1, 136.6, 272.1], [12.27, 411.7, 181.6, 596.0]])
LM = np.array([11., 12, 13, 14, 15]); SC = np.log10([3.83, 6.84, 11.95, 20.48, 34.71])
x, y = T[:, 0], np.log10(T[:, 1]); sig = (np.log10(T[:, 3]) - np.log10(T[:, 2])) / 4; w = 1 / sig ** 2
xb = (w * x).sum() / w.sum(); slope = (w * (x - xb) * y).sum() / (w * (x - xb) ** 2).sum(); es = 1 / math.sqrt((w * (x - xb) ** 2).sum())
out = dict(ET1=dict(slope=slope, err=es))
lin3 = np.polyfit(LM[:3], SC[:3], 1); quad3 = np.polyfit(LM, SC, 2)
T1 = dict(table_slope_11_15=(SC[-1] - SC[0]) / 4, table_slope_11_13=(SC[2] - SC[0]) / 2); T2 = {}
for lab, f in (("lin", lambda m: np.where(m < 13, np.polyval(lin3, m), np.interp(m, LM, SC))), ("quad", lambda m: np.polyval(quad3, m))):
    for sh in (0.0, 0.1):
        g = f(x + sh); s = (w * (x - xb) * g).sum() / (w * (x - xb) ** 2).sum()
        A = 10 ** ((w * (y - g)).sum() / w.sum()); c2 = float((w * (y - g - math.log10(A)) ** 2).sum())
        T1[f"{lab}_shift{sh}"] = dict(sigma_coll_slope=s, z=(s - slope) / es, within_2sigma=bool(abs(s - slope) < 2 * es))
        T2[f"{lab}_shift{sh}"] = dict(A=A, chi2=c2, per_bin=[float(10 ** (a - b)) for a, b in zip(y, g)])
T1["ORIGIN_IS_COLLAPSE"] = all(v["within_2sigma"] for k, v in T1.items() if isinstance(v, dict))
out["T1"] = T1
def c2b(b):
    a = (w * (y - b * x)).sum() / w.sum(); return float((w * (y - a - b * x) ** 2).sum())
T2["chi2_exponents"] = {str(round(b, 3)): c2b(b) for b in (0.0, slope, 1 / 3, 2 / 3, 1.0)}
A = T2["lin_shift0.0"]["A"]; fe = {"1e12": 21.80, "1e13": 14.85, "1e14": 14.22}
T2["A_over_fc_eta"] = {k: A / v for k, v in fe.items()}; T2["native_S"] = {"1e12": 21.80 * 6.84, "1e13": 14.85 * 11.95, "1e14": 14.22 * 20.48}
out["T2"] = T2
q = 3 * slope; eq = 3 * es; n = 2 * q - 1
out["T3"] = dict(q=q, q_err=eq, n=n, n_err=2 * eq, z_OS1={"can_0.892": (0.892 - q) / eq, "alt_0.748": (0.748 - q) / eq}, z_dwarf_cap={"can_0.13": (0.13 - q) / eq, "alt_0.22": (0.22 - q) / eq}, row_J="R5 pass (Kn >> 1), R6 slope pass on SPARC, dwarfs EXCLUDE (OS1), R7 FAIL")
# T4
F = lambda z: (6 / (4 * math.pi ** 2)) * quad(lambda t: t * t / math.cosh(0.5 * math.sqrt(t * t + z * z)) ** 2, 0, 200, limit=200)[0]
R, MP = 5.272, 0.938272; res = {}
for Ts in (130.0, 200.0):
    for c in (0.1, 1.0, 10.0):
        fn = lambda m: (m / MP) * c * F(m / Ts) - R
        ms = np.linspace(1, 30000, 3000); v = [fn(m) for m in ms]; roots = [brentq(fn, ms[i], ms[i + 1]) for i in range(len(ms) - 1) if v[i] * v[i + 1] < 0]
        res[f"T{int(Ts)}_c{c}"] = roots
all_heavy = [r[-1] for r in res.values() if r]
out["T4"] = dict(roots_GeV=res, heavy_root_range=[min(all_heavy), max(all_heavy)], note="the light root is q-order-one, m ~ 5 GeV/c; the heavy root is Boltzmann suppressed")
out["T4"]["heavy_ge_floor_556"] = bool(min(all_heavy) >= 556); out["T4"]["heavy_ge_floor_685"] = bool(min(all_heavy) >= 685)
# T5, GeV units
CM2G = 4.5787e3  # GeV^-3 per cm^2/g
rows = {"p5_can": dict(a=7 / 8, m0=1.3e13, EL=2.24e-12, s=0.1545, n=0.800, floor=556.0), "p7_alt": dict(a=13 / 8, m0=5.7e6, EL=2.46e-12, s=0.1058, n=0.571, floor=685.0)}
T5 = {}
for k, r in rows.items():
    M = lambda m: r["EL"] * (r["m0"] / m) ** r["a"]
    b = lambda m, v: math.sqrt(r["s"] * CM2G * m * (v / 70.5) ** (-r["n"]) / math.pi)
    grid = {str(m): dict(M_GeV=M(m), bM_20=b(m, 20) * M(m), bM_1000=b(m, 1000) * M(m)) for m in (r["floor"], 1000.0, 3000.0, 1e4)}
    best = b(r["floor"], 1000) * M(r["floor"])
    T5[k] = dict(grid=grid, VALID=bool(best >= 1), bM_1000_at_floor=best, m_needed_for_bM1_at_1000=brentq(lambda m: b(m, 1000) * M(m) - 1, 1e-6, 1e8))
out["T5"] = T5
json.dump(out, open(os.path.join(HERE, "cr2_results.json"), "w"), indent=1); print(json.dumps(out, indent=1))
# T6, AMENDMENT_A1, reported only; X80's table
fc = 0.84055; rr = dict(m=[10., 11., 12.], S=[44.2, 79.1, 134.9], eta_S=[23.19, 20.37, 20.83], eta_c=[29.26, 24.34, 25.94])
Sc = [a / b for a, b in zip(rr["S"], rr["eta_S"])]; conv = [fc * e * s for e, s in zip(rr["eta_c"], Sc)]
sl = lambda v: (math.log10(v[-1]) - math.log10(v[0])) / 2
T6 = dict(sigma_coll_x80=Sc, exponent_smooth=sl(rr["S"]), exponent_converged=sl(conv), z_smooth=(sl(rr["S"]) - slope) / es, z_converged=(sl(conv) - slope) / es, S_cold_converged=conv,
          need_over_native={f"{a:.2f}": float(10 ** s / np.interp(a, rr["m"], conv)) if a <= 12 else None for a, s in zip(x, y)})
json.dump(T6, open(os.path.join(HERE, "cr2_t6_results.json"), "w"), indent=1); print("T6", json.dumps(T6, indent=1))
