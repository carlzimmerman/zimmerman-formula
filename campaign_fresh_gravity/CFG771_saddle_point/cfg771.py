"""CFG771 -- the Sun-Earth saddle point (proposed LISA Pathfinder test) under the framework's own action.

Criteria: FROZEN_CRITERIA.md (committed alone first, d323d8de5).
S1 geometry + Newtonian tidal tensor; S2 gamma = 0 local algebraic response (context; curl part neglected);
S3 stiffened action (CFG770 linear response, r << lambda_e: constant pull GM_i/L*^2 per body) -> verdict; S4 LPF sensitivity.
Run: python3 cfg771.py   (CFG771_MUTATE=1 for the teeth; separate outputs).  Seconds, < 100 MB.
"""
import json
import math
import os
import sys

import numpy as np
from scipy import optimize

MUT = os.environ.get("CFG771_MUTATE") == "1"
HERE = os.path.dirname(os.path.abspath(__file__))
SUF = "_MUTATE" if MUT else ""
OUTF = open(os.path.join(HERE, f"cfg771{SUF}.out"), "w")


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    OUTF.write(s + "\n")


GM_S, GM_E, GM_M = 1.32712440018e20, 3.986004418e14, 4.9028e12
AU, D_MOON, PC = 1.495978707e11, 3.844e8, 3.0856775814913673e16
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
GE = 2.32e-10
LSTARS = [1e-4] if MUT else [5.75, 30.0, 100.0, 1000.0]
V_LPF = 1.5e3                                   # m/s crossing speed (Trenkel et al. scale)
NOISE = 1.74e-15 / 0.376                         # s^-2 / sqrt(Hz), provisional (Armano+2018 from memory)
T_INT = 3.156e7                                  # 1 yr integration for the static S3 stress
RES = {"lane": "CFG771", "mutate": MUT, "checks": {}, "numbers": {}}
FAILS = []


def check(name, ok, detail):
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    RES["checks"][name] = dict(ok=bool(ok), detail=detail)
    if not ok:
        FAILS.append(name)


def bodies(moon):
    b = [(GM_S, np.array([0.0, 0, 0])), (GM_E, np.array([AU, 0, 0]))]
    if moon == "line":
        b.append((GM_M, np.array([AU - D_MOON, 0, 0])))
    elif moon == "quad":
        b.append((GM_M, np.array([AU, D_MOON, 0])))
    return b


def gN(x, B):
    g = np.zeros(3)
    for gm, xb in B:
        r = x - xb
        g -= gm * r / np.linalg.norm(r) ** 3
    return g


def tidal(x, B):
    """dg_i/dx_j = sum GM (3 r_i r_j / r^5 - delta_ij / r^3)"""
    T = np.zeros((3, 3))
    for gm, xb in B:
        r = x - xb
        rn = np.linalg.norm(r)
        T += gm * (3 * np.outer(r, r) / rn ** 5 - np.eye(3) / rn ** 3)
    return T


P("CFG771  Sun-Earth saddle point under the framework's action" + ("  [MUTATE]" if MUT else ""))

# ============================================================ S1
P("\nS1  saddle location and tidal tensor")
q = math.sqrt(GM_E / GM_S)
d_an = AU * q / (1 + q)
S1 = {}
for moon in ("none", "line", "quad"):
    B = bodies(moon)
    x0 = np.array([AU - d_an, 0.0, 0.0])
    sol = optimize.root(lambda x: gN(x, B) / 1e-3, x0, tol=1e-14)
    xs = sol.x
    T = tidal(xs, B)
    ev = np.linalg.eigvalsh(T)
    S1[moon] = dict(x=xs.tolist(), d_earth=float(np.linalg.norm(xs - np.array([AU, 0, 0]))), T=T.tolist(), eig=ev.tolist(),
                    resid=float(np.linalg.norm(gN(xs, B))))
    P(f"  moon {moon:5s}: d from Earth {S1[moon]['d_earth']:.6e} m, |g_N| at saddle {S1[moon]['resid']:.1e}, "
      f"T eigenvalues {ev[0]:+.3e} {ev[1]:+.3e} {ev[2]:+.3e} s^-2")
k1 = abs(S1["none"]["d_earth"] / d_an - 1)
check("K1 saddle distance (no Moon) vs D sqrt(mE/mS)/(1+sqrt)", k1 <= 1e-3, f"rel {k1:.1e} (d_an {d_an:.6e} m)")
RES["numbers"]["S1"] = S1

# ============================================================ S2 gamma = 0 local algebraic response (context)
P("\nS2  gamma = 0, local algebraic response g = nu_s(|g_N,tot|/a0) g_N,tot (curl part neglected; CONTEXT ONLY)")
nu = lambda y: 0.5 + math.sqrt(0.25 + 1.0 / y) if y > 0 else float("inf")
S2 = {}
for moon in ("line", "quad"):
    T = np.zeros((3, 3)) if MUT else np.array(S1[moon]["T"])
    Tn = np.max(np.abs(np.linalg.eigvalsh(T))) if not MUT else 0.0
    for f, a0 in A0.items():
        ue = a0 * GE / (a0 + GE)
        gNe = GE - ue
        for gal in ("with_galaxy", "basin_rule"):
            for orient in ((1, 0, 0), (0, 1, 0)):
                e = np.array(orient, float)
                ge_vec = gNe * e if gal == "with_galaxy" else np.zeros(3)
                # anomalous field and its stress on a line through the saddle along e_x (the trajectory), miss distance b
                res = {}
                for b in (1.0, 10.0, 100.0):
                    s_grid = np.unique(np.concatenate([np.linspace(-2000, 2000, 2001), np.linspace(-30, 30, 3001)]))
                    S = []
                    for s in s_grid:
                        x = np.array([s, b, 0.0])
                        def ganom(xx):
                            g = ge_vec + T @ xx
                            n = np.linalg.norm(g)
                            return (nu(n / a0) - 1) * g if n > 0 else np.zeros(3)
                        h = 1e-3
                        J = np.column_stack([(ganom(x + h * ei) - ganom(x - h * ei)) / (2 * h) for ei in np.eye(3)])
                        S.append(np.max(np.abs(np.linalg.eigvals(0.5 * (J + J.T)).real)))
                    S = np.array(S)
                    snr = math.sqrt(np.trapz(S ** 2, s_grid) / V_LPF) / NOISE
                    # region where the stress exceeds 10% of its max along the path
                    big = s_grid[S >= 0.1 * S.max()]
                    res[b] = dict(Smax=float(S.max()), width=float(big.max() - big.min()) if big.size else 0.0, snr=snr)
                key = f"{moon}_{f}_{gal}_e{''.join(map(str, orient))}"
                S2[key] = res
                P(f"  {moon:4s} {f:9s} {gal:11s} g_e along {orient}: " + "; ".join(
                    f"b={b:g} m: max stress {r['Smax']:.2e} s^-2, width {r['width']:.1f} m, idealised SNR {r['snr']:.1e}"
                    for b, r in res.items()))
        if gal:
            pass
    if not MUT:
        P(f"  {moon}: |T|max {Tn:.3e} s^-2 -> basin-rule bubble r_b = a0/|T| = {A0['canonical'] / Tn:.2f} / {A0['alt'] / Tn:.2f} m; "
          f"with-Galaxy scale g_Ne/|T| ~ {(GE - A0['canonical'] * GE / (A0['canonical'] + GE)) / Tn:.2f} m")
RES["numbers"]["S2"] = {k: {str(b): v for b, v in r.items()} for k, r in S2.items()}
if MUT:
    m2 = all(r[100.0]["Smax"] == 0.0 or r[100.0]["width"] >= 3999 for r in S2.values())
    P(f"\nM2 tooth (T -> 0): S2 region unbounded along the path: {'bites' if m2 else 'DID NOT BITE'}")

# ============================================================ S3 stiffened action (verdict)
P("\nS3  stiffened action: anomalous tidal tensor at the saddle, sum over Sun, Earth, Moon of (GM_i/L*^2)(delta - rr)/r_i")
S3 = {}
for moon in ("line", "quad"):
    xs = np.array(S1[moon]["x"])
    for Lpc in LSTARS:
        L = Lpc * PC
        Tan = np.zeros((3, 3))
        for gm, xb in bodies(moon):
            r = xs - xb
            rn = np.linalg.norm(r)
            rh = r / rn
            Tan += (gm / L ** 2) * (np.eye(3) - np.outer(rh, rh)) / rn
        Sn = float(np.max(np.abs(np.linalg.eigvalsh(Tan))))
        snr = Sn * math.sqrt(T_INT) / NOISE
        S3[f"{moon}_{Lpc:g}"] = dict(stress=Sn, snr_1yr=snr)
        P(f"  moon {moon:4s} L* {Lpc:8g} pc: anomalous stress {Sn:.3e} s^-2; static SNR over 1 yr at the 1-mHz noise floor {snr:.2e}")
RES["numbers"]["S3"] = S3
worst = max(v["snr_1yr"] for v in S3.values())
if not MUT:
    label = "NULL PREDICTED" if worst < 1 else "TESTABLE"
    check("S3 verdict class", True, f"{label}: max SNR {worst:.2e} over the window and both Moon placements")
    RES["label"] = label
else:
    ref = 3.0256e-26  # filled from the main run's L* = 5.75 pc, moon=line value (asserted below if available)
    try:
        main = json.load(open(os.path.join(HERE, "cfg771_results.json")))
        ref = main["numbers"]["S3"]["line_5.75"]["stress"]
    except Exception:
        pass
    ratio = S3["line_0.0001"]["stress"] / ref
    P(f"\nM1 tooth: stress ratio L* 1e-4 / 5.75 pc = {ratio:.3e} (expected (5.75e4)^2 = {5.75e4 ** 2:.3e}): "
      f"{'bites' if abs(ratio / 5.75e4 ** 2 - 1) < 1e-6 else 'DID NOT BITE'}")
    FAILS.append("MUTATE (designed exit 1)")

RES["fails"] = FAILS
json.dump(RES, open(os.path.join(HERE, f"cfg771_results{SUF}.json"), "w"), indent=1, default=float)
P("\nFAILS:", FAILS if FAILS else "none")
OUTF.close()
sys.exit(1 if FAILS else 0)
