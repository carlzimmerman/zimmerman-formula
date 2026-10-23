#!/usr/bin/env python3
"""Does P3's strong-coupling estimate account for v3's weak-lapse regime? (FROZEN_CRITERIA.md, 30871e8eef)

P3's scales() and zP_of() are extracted verbatim from the hashed P3 script and run read-only.
W1 identity S <-> P3; W2 the Solar-System x; W3 P3's Solar-System rows with corrected inputs; W4 unscreened galaxy
interiors; W5(b) reproduction of P3's committed rows.  --mutate: W4 with M_kk = 1, du = a0 (weakening ignored).
"""
import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np
import sympy as sp

MUTATE = "--mutate" in sys.argv
HERE = Path(__file__).resolve().parent
P3DIR = HERE.parents[1] / "rebuild_2026_10_22" / "P3_v3_strong_field"
P3SRC = P3DIR / "p3_v3_strong_field.py"
SHA_FROZEN = "1aaf59addcc38ae61e20ff75ed1386857baa336a87a36e06e6241542cb67bb6d"
checks, out = [], {"mutate": MUTATE}


def record(name, ok, detail):
    checks.append({"check": name, "pass": bool(ok), "detail": detail})
    print(f"{name:4s} {'PASS' if ok else 'FAIL'}  {detail}")


src = P3SRC.read_text()
sha = hashlib.sha256(P3SRC.read_bytes()).hexdigest()
assert sha == SHA_FROZEN, f"P3 script changed: {sha}"
p3res = json.loads((P3DIR / "p3_v3_strong_field_results.json").read_text())
# constants exactly as P3 defines them (lines 41-50) and its E3 coefficients
c_SI, G_SI, GMSUN = 2.99792458e8, 6.67430e-11, 1.32712440018e20
PC = 3.0856775814913673e16
KPC, AU, LPLANCK = 1e3 * PC, 1.495978707e11, 1.616255e-35
A0 = {"canonical": 9.36e-11, "alt": 1.13e-10}
LSTARS = [20, 24, 90]
MU_K = 1.0 / (100 * KPC)
c_tt, c_zz, c_tilt = p3res["E3"]["c_tt"], p3res["E3"]["c_zz"], p3res["E3"]["c_tilt"]
SQK = math.sqrt(4 * math.pi) * LPLANCK
i0 = src.index("def scales(zh, zPh, gh")
i1 = src.index("sysres = {}", i0)
p3_funcs = src[i0:i1]
exec(p3_funcs)                                    # defines scales(), zP_of() verbatim
out["p3_sha256"] = sha
out["p3_extract_sha256"] = hashlib.sha256(p3_funcs.encode()).hexdigest()

# ================================================================ W1 identity
k, K, gL, ML, N0, Qb = sp.symbols("k K gamma_L M_L N0 Qbar", positive=True)
S_mine = -k ** 2 / (N0 * (K * ML + gL * k ** 2))            # v3 V2 closed form at kappa 1, mu 0, g0 0, k || P0
# re-derive it from the closed form itself rather than typing it: K S = -q/(N0 (1 + (gL/K) q)), q = k^2/M_L
q = k ** 2 / ML
S_closed = (-q / (N0 * (1 + (gL / K) * q))) / K
Mu = sp.Matrix([[0, sp.I * k / 2], [-sp.I * k / 2, -N0 * (K * ML + gL * k ** 2) / 2]])     # P3 E2(i), verbatim form
Schur_P3 = sp.simplify(Mu[0, 0] - Mu[0, 1] * Mu[1, 1] ** -1 * Mu[1, 0])
ZP = k ** 2 / (Qb ** 2 * (K * ML + gL * k ** 2))                                         # P3 E1
r1 = sp.simplify(S_closed - S_mine)
r2 = sp.simplify(S_closed + 2 * Schur_P3)
r3 = sp.simplify((-S_closed * N0 - Qb ** 2 * ZP).subs(N0, 1 / Qb))
record("W1", r1 == 0 and r2 == 0 and r3 == 0, f"S = -k^2/(N0(K M_L + gL k^2)): {r1}; S + 2 Schur(P3 E2(i)): {r2}; "
                                              f"-S N0 - Qbar^2 Z_P (N0 Qbar = 1): {r3}")

# ================================================================ W2 the Solar-System x
r, Ms, Kc = sp.symbols("r M K_c", positive=True)
psi = Kc * Ms / (4 * sp.pi * gL * r)                       # gamma_L lap(psi) = -K rho, point mass
phi_p = (Kc * Ms / (4 * sp.pi) + sp.integrate(Kc * psi * r ** 2, r)) / r ** 2   # Gauss: phi' = K(M + int psi dV)/(4 pi r^2)
lap_psi = sp.simplify(sp.diff(r ** 2 * sp.diff(psi, r), r) / r ** 2)
KP = sp.simplify(phi_p + gL * sp.diff(psi, r))             # K P = grad phi + gamma_L grad(D.P)  (P equation, u << a0)
divP_ok = sp.simplify(sp.diff(r ** 2 * KP / Kc, r) / r ** 2 - psi) == 0
KP_target = sp.simplify((Kc * Ms / (4 * sp.pi)) * Kc / (gL * 2))   # = K M/(4 pi L*^2) with gL = K L*^2/2
w2i = (lap_psi == 0) and divP_ok and sp.simplify(KP - KP_target) == 0
w2rows, w2ok = {}, True
for foot, a0 in A0.items():
    a0m = a0 / c_SI ** 2
    for Lpc in LSTARS:
        L = Lpc * PC
        u_sun = GMSUN / (c_SI ** 2 * L ** 2)
        u_p3 = 2 * (GMSUN / (AU * c_SI ** 2) + 3.986e14 / (6.371e6 * c_SI ** 2)) / L
        w2rows[f"{foot}|{Lpc}pc"] = {"u_sun/a0": u_sun / a0m, "u_P3(Eot-Wash)/a0": u_p3 / a0m}
        w2ok &= u_sun / a0m <= 1e-4
xes = {"1": 1.0, "1.69 (v_c 200 km/s, canonical)": (200e3) ** 2 / (8.2 * KPC) / A0["canonical"],
       "1.40 (v_c 202 km/s, alt)": (202e3) ** 2 / (8.2 * KPC) / A0["alt"], "2": 2.0, "3": 3.0}
ML_e = {kk: (1 + v) ** 2 for kk, v in xes.items()}
record("W2", w2i and w2ok, f"(i) linear screened point mass: lap(psi) = 0 off the source: {lap_psi == 0}; div P = psi: "
       f"{divP_ok}; K|P| = K M/(4 pi L*^2) = GM/(c^2 L*^2) exactly: {sp.simplify(KP - KP_target) == 0}; "
       f"(ii) Sun u0/a0 = " + ", ".join(f"{k_} {v['u_sun/a0']:.2e}" for k_, v in w2rows.items())
       + f"; P3's 2 Phi/L* / (a0/c^2) = {min(v['u_P3(Eot-Wash)/a0'] for v in w2rows.values()):.1f}-"
       f"{max(v['u_P3(Eot-Wash)/a0'] for v in w2rows.values()):.1f}; (iii) Galactic x_e "
       + ", ".join(f"{k_}: x {v:.3f}, M_L {ML_e[k_]:.2f}" for k_, v in xes.items()))
out["W2"] = {"rows": w2rows, "x_e": xes, "M_L": ML_e, "KP": str(KP)}

# ================================================================ W5(b) reproduction gate + W3 corrected rows


def p3_rows(foot, Lpc, u0_mode, Mkk_override=None):
    a0 = A0[foot]
    a0m = a0 / c_SI ** 2
    L = Lpc * PC
    hed = lambda Phi_c2: 2 * Phi_c2 / L ** 2
    phE = 3.986e14 / (6.371e6 * c_SI ** 2)
    phS = GMSUN / (AU * c_SI ** 2)
    phB = 2.59 * GMSUN / (8.79e8 * c_SI ** 2)
    sysd = {"Eot-Wash (38.6 um)": (1 / 38.6e-6, 1e-3, hed(phS + phE), 1e-6, 2 * (phS + phE) / L),
            "planets (1 AU)": (1 / AU, 2 * math.pi / 3.15576e7, hed(phS), 1e-6, 2 * phS / L),
            "double pulsar": (1 / 8.79e8, 2 * math.pi / (2.45 * 3600), hed(phB), 1e-6, 2 * phB / L)}
    res_ = {}
    for sname, (kk, om, dP, Qm1, u0_p3) in sysd.items():
        Qbar = 1 + Qm1
        if u0_mode == "p3":
            u0m, Mkk = u0_p3, 1.0
        else:
            xe = u0_mode
            u0m = a0m * xe / (1 + xe) + GMSUN / (c_SI ** 2 * L ** 2)
            Mkk = (1 + xe) ** 2 if Mkk_override is None else Mkk_override
        zPh = zP_of(kk, L, Mkk, Qbar)
        zh = zPh + MU_K ** 2
        gh = dP * (1 + dP * L ** 2 / 2) + MU_K ** 2 * Qm1 / Qbar
        res_[sname] = scales(zh, zPh, gh, kk, om, a0m, a0m - u0m, Mkk, L, Qbar)
    return res_


repro_worst, w3_worst_ratio, w3_worst_eps, w3_rows = 0.0, 0.0, 0.0, {}
v6_seen = True
for foot in A0:
    for Lpc in LSTARS:
        rp = p3_rows(foot, Lpc, "p3")
        for sname, s_ in rp.items():
            ref = p3res["E4"][f"{sname}|{foot}|{Lpc}pc"]["eps_max"]
            repro_worst = max(repro_worst, abs(s_["eps_max"] / ref - 1))
            v6_seen &= "V6 pidot^3 [W cubic]" not in s_["vertices"]
        for xk, xe in xes.items():
            for Mlab, Mo in (("M_L", None), ("M_T", 1 + xe)):
                rc = p3_rows(foot, Lpc, xe, Mo)
                for sname, s_ in rc.items():
                    ref = p3res["E4"][f"{sname}|{foot}|{Lpc}pc"]["eps_max"]
                    ratio = abs(s_["eps_max"] / ref - 1)
                    w3_worst_ratio = max(w3_worst_ratio, ratio)
                    w3_worst_eps = max(w3_worst_eps, s_["eps_max"])
                    v6 = s_["vertices"].get("V6 pidot^3 [W cubic]", {}).get("eps")
                    w3_rows[f"{sname}|{foot}|{Lpc}pc|x_e {xk}|{Mlab}"] = {"eps_max": s_["eps_max"], "ratio_minus_1": ratio,
                                                                         "V6_eps": v6, "worst": s_["worst_vertex"]}
record("W5b", repro_worst <= 1e-12 and v6_seen,
       f"P3's own inputs (u0 = 2 Phi/L*, M_kk = 1) reproduce its committed eps_max to {repro_worst:.1e}; V6 absent in "
       f"those rows: {v6_seen} (du = a0 - u0 < 0 -> skipped)")
v6_vals = [v["V6_eps"] for v in w3_rows.values()]
record("W3", w3_worst_eps <= 1e-2 and w3_worst_ratio <= 0.10,
       f"{len(w3_rows)} corrected rows (u0 = a0 x_e/(1+x_e) + Sun, M_kk = M_L or M_T, x_e 1-3): max eps {w3_worst_eps:.3e}; "
       f"max |eps/eps_P3 - 1| = {w3_worst_ratio:.1e}; V6 now computed in every row: {all(v is not None for v in v6_vals)}, "
       f"max V6 eps {max(v for v in v6_vals if v is not None):.1e}")
out["W3"] = w3_rows
out["W5b_repro_worst"] = repro_worst

# ================================================================ W4 unscreened galaxy interiors
GAL = {"G1 (1e11 Msun, a 2 kpc)": (1e11, 2.0), "G2 (1e12 Msun, a 3 kpc)": (1e12, 3.0),
       "G3 compact (1e11 Msun, a 0.3 kpc)": (1e11, 0.3)}
w4_rows, w4_max, trend = {}, (0.0, None), {"V1": [], "V5": []}
for gname, (Mg, ag) in GAL.items():
    GM = G_SI * Mg * 1.98892e30
    for foot, a0 in A0.items():
        a0m = a0 / c_SI ** 2
        for Lpc in LSTARS:
            L = Lpc * PC
            rr = np.logspace(np.log10(5 * L), np.log10(50 * KPC), 400)
            gN = GM / (rr + ag * KPC) ** 2
            xN = gN / a0
            xx = (xN + np.sqrt(xN ** 2 + 4 * xN)) / 2
            KPs = a0m * xx / (1 + xx)                               # K|P*| (1/m), AQUAL
            KDP = np.gradient(rr ** 2 * KPs, rr) / rr ** 2           # K D.P (1/m^2)
            vc = np.sqrt(a0 * xx * rr)
            for j in range(0, 400, 10):
                x_, r_ = float(xx[j]), float(rr[j])
                if MUTATE:
                    Mkk, du = 1.0, a0m
                else:
                    Mkk, du = (1 + x_) ** 2, a0m / (1 + x_)
                Qbar = 1 + 1e-6
                gh = KDP[j] * (1 + KDP[j] * L ** 2 / 2) + MU_K ** 2 * 1e-6 / Qbar
                for kk in (3 / r_, 30 / r_, 1 / L):
                    zPh = zP_of(kk, L, Mkk, Qbar)
                    s_ = scales(zPh + MU_K ** 2, zPh, gh, kk, vc[j] / r_, a0m, du, Mkk, L, Qbar)
                    if s_.get("G<=0"):
                        continue
                    key = f"{gname}|{foot}|{Lpc}pc|r {r_ / KPC:.3f} kpc|k r {kk * r_:.3g}"
                    w4_rows[key] = {"x": x_, "M_L": (1 + x_) ** 2, "eps_max": s_["eps_max"], "worst": s_["worst_vertex"],
                                    "eps_V1": s_["vertices"]["V1 pidot (grad pi)^2 [clock]"]["eps"],
                                    "eps_V5": s_["vertices"]["V5 pidot (grad pi)^2 [K(Q) dust]"]["eps"]}
                    w4_max = max(w4_max, (s_["eps_max"], key))
                    if gname.startswith("G3") and foot == "canonical" and Lpc == 24 and abs(kk * r_ - 3) < 1e-9:
                        trend["V1"].append((x_, w4_rows[key]["eps_V1"]))
                        trend["V5"].append((x_, w4_rows[key]["eps_V5"]))


def slope(pairs):
    a = np.array(pairs)
    sel = a[:, 0] > 3
    if sel.sum() < 3:
        return float("nan")
    return float(np.polyfit(np.log10((1 + a[sel, 0]) ** 2), np.log10(a[sel, 1]), 1)[0])


xmax = max(v["x"] for v in w4_rows.values())
record("W4", w4_max[0] <= 1e-2, f"{len(w4_rows)} galaxy-interior rows (r 5 L* - 50 kpc, x up to {xmax:.1f}, M_L up to "
                                f"{(1 + xmax) ** 2:.1f}): max eps {w4_max[0]:.3e} at {w4_max[1]}; d log eps / d log M_L "
                                f"(G3, k r 3, x > 3): V1 {slope(trend['V1']):+.2f}, V5 {slope(trend['V5']):+.2f}")
out["W4"] = {"max": w4_max, "x_max": xmax, "slope_V1": slope(trend["V1"]), "slope_V5": slope(trend["V5"]),
             "rows": w4_rows}

npass = sum(c["pass"] for c in checks)
out["checks"] = checks
out["summary"] = f"{npass}/{len(checks)} PASS"
print(out["summary"])
(HERE / ("p3_weak_lapse_results_MUTATE.json" if MUTATE else "p3_weak_lapse_results.json")).write_text(
    json.dumps(out, indent=1, default=str))
sys.exit(0 if npass == len(checks) else 1)
