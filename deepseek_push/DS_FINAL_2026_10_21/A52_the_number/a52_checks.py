#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A52 -- WHAT PHYSICAL QUANTITY EQUALS 2 sqrt(32 pi/3) = 11.5776 ?

The number is fixed by the framework.  With

    Z := sqrt(32 pi/3) = 2 sqrt(8 pi/3) = 5.7888100365 ,
    a0 = kappa c sqrt(G rho_Lambda) ,  rho_Lambda = Lambda c^2/(8 pi G) ,

one has identically

    a0/(c H_Lambda) = 2 kappa / Z      <=>      2 c H_Lambda / a0 = Z / kappa ,

so kappa = 1/2 *is* 2 c H_Lambda/a0 = 2Z = sqrt(128 pi/3) = 11.577620073.

This lane asks a different question from A1 (counting), A27 (the factor two) and
A34 (dimensions): not "can kappa be derived from a count", but "is 11.5776 the
value of some *other* physical quantity -- does the irrational have an
independent meaning, a formula of its own?"

Four things are done:

  (1) a candidate table of closed forms of order 10 in gravitational and
      thermodynamic physics, each computed to 10 digits, with the 6-digit hit
      set and the misses (K2-K5);
  (2) for every exact hit, the physical statement and its prediction, plus the
      operational test "does the identification fix kappa, or a product that
      leaves kappa free?" (K6-K8);
  (3) a look-elsewhere control: a declared grammar of simple expressions built
      from {2,3,4,5,8,pi,sqrt2,sqrt3,e} with up to three operations, the counts
      of 1 %, 0.1 % and 0.01 % hits, integer targets, 200 random targets, and
      the resulting base rate and trial factor (K12-K15);
  (4) the verdict: the number is a *measurable ratio* with exactly one physical
      identity, and that identity is kappa = 1/2 restated; it is not a count
      (it is irrational), and any count that hits it fixes only the product
      beta sqrt(chi) = 1/kappa (A27).  K9, K10, K16, K17 close the remaining
      routes (integer, "twelfth", vacuum-invariant, folklore a0 = cH/6).

Usage:  python3 a52_checks.py [--mutate[=M1|M2|M3|M4]]
Exit 0 iff all declared checks PASS.

Constants: BRIEF section 4 (c, G, H0, Lambda, a0_can, Mpc, pc) plus
hbar = 1.054571817e-34 J s (CODATA 2018, declared, used only for S_dS) and the
measured kappa = 0.417 +/- 0.095 (CFG493 via A15, external input).  No fitted
constant is introduced here.
"""

import os
import sys
import json
import math
import random

import sympy as sp

OUTDIR = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------------------------------
# constants -- BRIEF section 4, plus two declared externals
# --------------------------------------------------------------------------
C_LIGHT = 2.99792458e8            # m/s            (BRIEF 4)
G_N = 6.67430e-11                 # m^3 kg^-1 s^-2 (BRIEF 4)
H0 = 2.1843e-18                   # s^-1           (BRIEF 4, 67.4 km/s/Mpc)
LAMBDA = 1.0890e-52               # m^-2           (BRIEF 4)
A0_CAN = 9.36e-11                 # m/s^2          (BRIEF 4, canonical footing)
KAPPA_MEAS = 0.417                # CFG493 via A15 (external)
KAPPA_SIG = 0.095                 # CFG493 via A15 (external)
HBAR = 1.054571817e-34            # J s            (CODATA 2018, declared)
MPC = 3.0856775814913673e22       # m              (BRIEF 4)
PC = 3.0856775814913673e16        # m              (BRIEF 4)

CONSTANTS = [
    "c = 2.99792458e8 m/s (BRIEF 4)",
    "G = 6.67430e-11 m^3 kg^-1 s^-2 (BRIEF 4)",
    "H0 = 2.1843e-18 s^-1 (BRIEF 4)",
    "Lambda = 1.0890e-52 m^-2 (BRIEF 4)",
    "a0_can = 9.36e-11 m/s^2 (BRIEF 4)",
    "hbar = 1.054571817e-34 J s (CODATA 2018, declared; only S_dS uses it)",
    "kappa_meas = 0.417 +/- 0.095 (CFG493 via A15, external)",
    "kappa_can = 1/2 (BRIEF 4)",
    "1 pc = 3.0856775814913673e16 m; 1 Mpc = 3.0856775814913673e22 m (BRIEF 4)",
]

# --------------------------------------------------------------------------
# mutation switches
# --------------------------------------------------------------------------
MUT = "none"
for _arg in sys.argv[1:]:
    if _arg.startswith("--mutate"):
        MUT = _arg.split("=", 1)[1] if "=" in _arg else "M1"

RESULTS = []


def hdr(title):
    print("\n-- %s %s" % (title, "-" * max(4, 66 - len(title))))


def check(cid, ok, measured, threshold, note=""):
    RESULTS.append({"id": cid, "pass": bool(ok), "value": str(measured),
                    "threshold": str(threshold), "note": note})
    print("%-5s %s %-56s %-38s %s"
          % (cid, "PASS" if ok else "FAIL", str(measured), str(threshold),
             ("[%s]" % note) if note else ""))


# --------------------------------------------------------------------------
# the exact object under study
# --------------------------------------------------------------------------
Z_EXACT = sp.sqrt(32 * sp.pi / 3)                 # 5.788810036465...
TARGET_EXACT = 2 * Z_EXACT                        # 11.577620072932...
TARGET = float(TARGET_EXACT)


def dev(x, t=TARGET):
    """relative deviation of x from the target"""
    return (x - t) / t


# ==========================================================================
# K1 -- the identity, exactly
# ==========================================================================
def k1():
    hdr("K1 the identity: 2 sqrt(32 pi/3) = 4 sqrt(8 pi/3) = sqrt(128 pi/3)")
    forms = {
        "2 sqrt(32 pi/3)": 2 * sp.sqrt(32 * sp.pi / 3),
        "4 sqrt(8 pi/3)": 4 * sp.sqrt(8 * sp.pi / 3),
        "sqrt(128 pi/3)": sp.sqrt(128 * sp.pi / 3),
        "8 sqrt(2 pi/3)": 8 * sp.sqrt(2 * sp.pi / 3),
    }
    resid = {k: sp.simplify(v - TARGET_EXACT) for k, v in forms.items()}
    ok = all(r == 0 for r in resid.values())
    check("K1", ok,
          "value=%.10f ; max|residual|=%s"
          % (TARGET, max(abs(float(r)) for r in resid.values())),
          "all residuals exactly 0",
          "four spellings, one number")
    return {"target_value": TARGET,
            "Z_value": float(Z_EXACT),
            "residuals": {k: str(r) for k, r in resid.items()},
            "n_forms": len(forms)}


# ==========================================================================
# K2 -- the candidate table (task list + physically motivated entries)
# ==========================================================================
def k2():
    hdr("K2 closed-form candidates of order 10, to 10 digits")
    # (label, sympy expression, is it a rewrite of the target?, what it is)
    tgt_rewrite = "rewrite"
    cands = [
        ("2 sqrt(32 pi/3)", 2 * sp.sqrt(32 * sp.pi / 3), tgt_rewrite,
         "the target itself (definition)"),
        ("4 sqrt(8 pi/3)", 4 * sp.sqrt(8 * sp.pi / 3), tgt_rewrite,
         "4 x the inverse Friedmann coefficient"),
        ("sqrt(128 pi/3)", sp.sqrt(128 * sp.pi / 3), tgt_rewrite,
         "same number, factored"),
        ("8 sqrt(2 pi/3)", 8 * sp.sqrt(2 * sp.pi / 3), tgt_rewrite,
         "same number, factored"),
        ("sqrt(32 pi/3)", sp.sqrt(32 * sp.pi / 3), "no",
         "half the target: cH/a0"),
        ("8 pi/3", 8 * sp.pi / 3, "no", "Friedmann coefficient"),
        ("2 pi sqrt(8/3)", 2 * sp.pi * sp.sqrt(sp.Rational(8, 3)), "no",
         "2 pi x sqrt(Friedmann)"),
        ("16 pi/3", 16 * sp.pi / 3, "no", "4 x Friedmann"),
        ("4 pi", 4 * sp.pi, "no", "solid angle of S^2"),
        ("4 pi/3", 4 * sp.pi / 3, "no", "ball-volume factor"),
        ("sqrt(4 pi/3)", sp.sqrt(4 * sp.pi / 3), "no",
         "Jeans mass coefficient (4 pi/3)^(1/2)"),
        ("Vol S2 / Vol B2", 4, "no", "surface/volume ratio, n=2 (= n/R)"),
        ("Vol S3 / Vol B3", 3 * sp.pi / 2, "no", "surface/volume ratio, n=3"),
        ("Vol S4 / Vol B4", sp.Rational(16, 3), "no", "surface/volume ratio, n=4"),
        ("Vol S5 / Vol B5", 15 * sp.pi / 8, "no", "surface/volume ratio, n=5"),
        ("Vol S4 / Vol S2", 2 * sp.pi / 3, "no", "sphere-volume ratio"),
        ("Vol B4 / Vol B2", 3 * sp.pi / 8, "no", "ball-volume ratio"),
        ("(V_H/V_P)^(1/6)", None, "no", "Hubble/Planck volume, sixth root"),
        ("12", sp.Integer(12), "no", "cH_L/6 (Verlinde-form); SM gauge generators"),
        ("11", sp.Integer(11), "no", "M-theory dimensions"),
        ("10", sp.Integer(10), "no", "dS4 Killing vectors; Weyl components"),
        ("4 pi - 1", 4 * sp.pi - 1, "no", "chance near-hit (no physics)"),
        ("e^sqrt(6)", sp.exp(sp.sqrt(6)), "no", "chance near-hit (no physics)"),
        ("2^(7/2)", 2 ** sp.Rational(7, 2), "no", "chance near-hit"),
        ("pi^2 + 2", sp.pi ** 2 + 2, "no", "chance near-hit"),
        ("3 pi + 2", 3 * sp.pi + 2, "no", "chance near-hit"),
    ]

    # Hubble volume / Planck volume to the 1/6
    V_ratio = (4 * sp.pi / 3) * (C_LIGHT / H0) ** 3 / ((4 * sp.pi / 3) * (sp.sqrt(HBAR * G_N / C_LIGHT ** 3)) ** 3)
    vh_vp_sixth = float(V_ratio) ** (1.0 / 6.0)

    tgt = 12.0 if MUT == "M1" else TARGET
    rows = []
    for lab, ex, kind, meaning in cands:
        if ex is None:
            val = vh_vp_sixth
            exact = False
        else:
            val = float(ex)
            exact = (sp.simplify(ex - TARGET_EXACT) == 0)
            if exact:
                kind = "rewrite"
        d = dev(val, tgt)
        rows.append({"expr": lab, "value": val, "rel_dev": d,
                     "abs_dev": abs(d), "kind": kind,
                     "meaning": meaning, "hit6": abs(d) < 5e-7})
    rows.sort(key=lambda r: r["abs_dev"])
    print("    %-20s %-18s %-12s %s" % ("expression", "value (10 dp)", "rel. dev", "what it is"))
    for r in rows:
        vtxt = ("%.10f" % r["value"]) if abs(r["value"]) < 1e6 else ("%.4e" % r["value"])
        dtxt = ("%+12.6f%%" % (100 * r["rel_dev"])) if abs(r["rel_dev"]) < 100 else "(not of order 10)"
        print("    %-20s %-18s %-14s  %s%s"
              % (r["expr"], vtxt, dtxt, r["meaning"],
                 "   <== 6-digit HIT" if r["hit6"] else ""))
    hits = [r for r in rows if r["hit6"]]
    nonrewrite = [r for r in hits if (r["kind"] != "rewrite" and MUT != "M1")]
    if MUT == "M1":
        nonrewrite = [r for r in hits if r["expr"] == "12"]
    n_distinct_hit_values = len({round(r["value"], 6) for r in hits})
    ok = (len(nonrewrite) == 0 and len(hits) == 4 and n_distinct_hit_values == 1)
    check("K2", ok,
          "hits=%d (distinct values=%d), non-rewrite hits=%d, closest miss=%.4f%%"
          % (len(hits), n_distinct_hit_values, len(nonrewrite),
             100 * min(r["abs_dev"] for r in rows if not r["hit6"])),
          "0 non-rewrite hits at 6 digits; all hits are one value",
          "4 spellings, 1 number, 0 independent formulas")
    return {"rows": rows,
            "n_hits6": len(hits), "n_distinct_hit_values": n_distinct_hit_values,
            "n_nonrewrite_hits": len(nonrewrite),
            "closest_miss_expr": min((r for r in rows if not r["hit6"]),
                                     key=lambda r: r["abs_dev"])["expr"],
            "closest_miss_dev": min(r["abs_dev"] for r in rows if not r["hit6"]),
            "vh_vp_sixth": vh_vp_sixth}


# ==========================================================================
# K3 -- sphere volumes and their ratios, n = 2..5
# ==========================================================================
def k3():
    hdr("K3 volumes of S^n and B^n (n=2..5) and every pairwise ratio")
    n = sp.symbols("n", positive=True, integer=True)

    def volS(k):
        return 2 * sp.pi ** (sp.Rational(k + 1, 2)) / sp.gamma(sp.Rational(k + 1, 2))

    def volB(k):
        return sp.pi ** (sp.Rational(k, 2)) / sp.gamma(sp.Rational(k, 2) + 1)

    tab = {}
    for k in range(2, 6):
        tab["Vol S%d" % k] = float(volS(k))
        tab["Vol B%d" % k] = float(volB(k))
    ratios = {}
    for a in range(2, 6):
        for b in range(2, 6):
            if a != b:
                ratios["S%d/S%d" % (a, b)] = float(volS(a) / volS(b))
                ratios["B%d/B%d" % (a, b)] = float(volB(a) / volB(b))
            ratios["S%d/B%d" % (a, b)] = float(volS(a) / volB(b))
    allv = dict(tab)
    allv.update(ratios)
    hits = {k: v for k, v in allv.items() if abs(dev(v)) < 1e-6}
    near = sorted(ratios.items(), key=lambda kv: abs(dev(kv[1])))[:4]
    max_ratio = max(ratios.values())
    max_ratio_expr = max(ratios, key=ratios.get)
    print("    volumes: " + ", ".join("%s=%.6f" % (k, tab[k]) for k in sorted(tab)))
    print("    nearest ratios: " + ", ".join("%s=%.6f (%+.2f%%)"
                                             % (k, v, 100 * dev(v)) for k, v in near))
    print("    largest ratio in the family: %.6f (%s)" % (max_ratio, max_ratio_expr))
    ok = (len(hits) == 0 and max_ratio < 0.9 * TARGET)
    check("K3", ok,
          "hits=%d ; max ratio=%.6f (%s) ; nearest dev=%.2f%%"
          % (len(hits), max_ratio, max_ratio_expr,
             100 * min(abs(dev(v)) for v in ratios.values())),
          "0 hits; every sphere ratio < 0.9 x target",
          "the whole sphere-volume family tops out at pi^2 = 9.870")
    return {"volumes": tab, "n_ratios": len(ratios), "n_hits": len(hits),
            "max_value": max_ratio, "max_expr": max_ratio_expr,
            "nearest": [(k, v, dev(v)) for k, v in near]}


# ==========================================================================
# K4 -- the solid angle 4 pi and its fractions
# ==========================================================================
def k4():
    hdr("K4 the solid angle 4 pi and its fractions")
    fam = {}
    for k in range(1, 9):
        fam["4pi/%d" % k] = 4 * math.pi / k
        fam["2pi*%d" % k] = 2 * math.pi * k
        fam["4pi*%d/3" % k] = 4 * math.pi * k / 3
    fam["4pi"] = 4 * math.pi
    fam["4pi/3"] = 4 * math.pi / 3
    fam["16pi/3"] = 16 * math.pi / 3
    fam["4pi^2/3"] = 4 * math.pi ** 2 / 3
    hits = {k: v for k, v in fam.items() if abs(dev(v)) < 1e-6}
    best = min(fam.items(), key=lambda kv: abs(dev(kv[1])))
    print("    4pi = %.10f  (dev %+.4f%%)" % (4 * math.pi, 100 * dev(4 * math.pi)))
    print("    nearest member: %s = %.10f (dev %+.4f%%)" % (best[0], best[1], 100 * dev(best[1])))
    ok = (len(hits) == 0 and abs(dev(best[1])) > 0.08)
    check("K4", ok,
          "hits=%d ; 4pi dev=%+.4f%% ; nearest dev=%.4f%%"
          % (len(hits), 100 * dev(4 * math.pi), 100 * abs(dev(best[1]))),
          "0 hits; nearest member > 8% away",
          "4 pi = 12.5664 is 8.54% high; no fraction of it lands on 11.58")
    return {"four_pi": 4 * math.pi, "four_pi_dev": dev(4 * math.pi),
            "n_members": len(fam), "n_hits": len(hits),
            "nearest": best[0], "nearest_val": best[1], "nearest_dev": dev(best[1])}


# ==========================================================================
# K5 -- thermodynamic / gravitational candidates of order 10
# ==========================================================================
def k5():
    hdr("K5 thermodynamic and gravitational candidates of order 10")
    # de Sitter static patch
    H_L = C_LIGHT * math.sqrt(LAMBDA / 3.0)
    S_dS = math.pi * C_LIGHT ** 5 / (G_N * HBAR * H_L ** 2)   # A/(4 l_P^2)
    A_over_lP2 = 4 * S_dS
    V_P = (4 * math.pi / 3) * (math.sqrt(HBAR * G_N / C_LIGHT ** 3)) ** 3
    V_H = (4 * math.pi / 3) * (C_LIGHT / H0) ** 3
    sixth = (V_H / V_P) ** (1.0 / 6.0)
    items = {
        "Jeans (4pi/3)^(1/2)": math.sqrt(4 * math.pi / 3),
        "(V_H/V_P)^(1/6)": sixth,
        "S_dS = A/4l_P^2": S_dS,
        "A_H/l_P^2": A_over_lP2,
        "S_dS^(1/2)": math.sqrt(S_dS),
        "S_dS^(1/4)": S_dS ** 0.25,
        "log2 S_dS": math.log2(S_dS),
        "Killing vectors dS4": 10.0,
        "Weyl components 4D": 10.0,
        "Riemann components 4D": 20.0,
        "graviton polarisations": 2.0,
        "spacetime dimensions": 4.0,
        "N_eff": 3.046,
        "g_* (SM)": 106.75,
        "1/alpha_em": 137.035999,
        "12 (SM gauge generators)": 12.0,
        "11 (M-theory dimensions)": 11.0,
    }
    hits = {k: v for k, v in items.items()
            if 0.5 < v < 30 and abs(dev(v)) < 1e-6}
    o10 = {k: v for k, v in items.items() if 8.0 <= v <= 16.0}
    best = min(o10.items(), key=lambda kv: abs(dev(kv[1])))
    for k in ["Jeans (4pi/3)^(1/2)", "S_dS = A/4l_P^2", "A_H/l_P^2",
              "log2 S_dS", "Killing vectors dS4", "Weyl components 4D",
              "(V_H/V_P)^(1/6)"]:
        print("    %-24s %.10g   (dev %+.3e)" % (k, items[k], dev(items[k])))
    print("    closest O(10) item: %s = %.6f (dev %+.4f%%)"
          % (best[0], best[1], 100 * dev(best[1])))
    ok = (len(hits) == 0 and abs(dev(best[1])) > 0.03)
    check("K5", ok,
          "hits=%d ; closest O(10)=%s at %.4f%%"
          % (len(hits), best[0], 100 * abs(dev(best[1]))),
          "0 hits; closest O(10) > 3% away",
          "static-patch dof are 1e122 or 10, never 11.58")
    return {"items": {k: v for k, v in items.items()},
            "n_hits": len(hits), "closest_o10": best[0],
            "closest_o10_dev": dev(best[1]),
            "S_dS": S_dS, "A_over_lP2": A_over_lP2, "sixth_root": sixth,
            "H_Lambda": H_L}


# ==========================================================================
# K6 -- the one exact identification, and what it fixes
# ==========================================================================
def k6():
    hdr("K6 the exact identification: 2cH_L/a0 = 4 sqrt(8 pi/3) <=> kappa=1/2")
    kap = sp.symbols("kappa", positive=True)
    c, G, Lam = sp.symbols("c G Lambda", positive=True)
    rho = Lam * c ** 2 / (8 * sp.pi * G)
    denom = sp.Integer(1) if MUT == "M2" else sp.Integer(3)
    H = sp.sqrt(8 * sp.pi * G * rho / denom)
    a0 = kap * c * sp.sqrt(G * rho)

    r1 = sp.simplify(2 * c * H / a0 - 2 * sp.sqrt(8 * sp.pi / 3) / kap)
    r2 = sp.simplify(a0 - kap * c ** 2 * sp.sqrt(Lam / (8 * sp.pi)))
    r3 = sp.simplify((2 * c * H / a0).subs(kap, sp.Rational(1, 2))
                     - 4 * sp.sqrt(8 * sp.pi / 3))
    # numbers
    H_L = C_LIGHT * math.sqrt(LAMBDA / 3.0)
    a0_num = C_LIGHT ** 2 * math.sqrt(LAMBDA / (32 * math.pi))
    ratio = 2 * C_LIGHT * H_L / a0_num
    ok = (r1 == 0 and r2 == 0 and r3 == 0
          and abs(ratio - TARGET) / TARGET < 1e-12
          and abs(a0_num - 9.3541734858e-11) / 9.3541734858e-11 < 1e-9)
    check("K6", ok,
          "residuals (%s,%s,%s) ; 2cH/a0=%.10f ; a0=%.6e"
          % (r1, r2, r3, ratio, a0_num),
          "exact identity; kappa=1/2 <=> target",
          "this is P3 restated, not a new equation")
    return {"residual_ratio": str(r1), "residual_a0": str(r2),
            "residual_at_half": str(r3),
            "H_Lambda": H_L, "a0_kappa_half": a0_num, "ratio": ratio}


# ==========================================================================
# K7 -- the same number as a length ratio
# ==========================================================================
def k7():
    hdr("K7 the same number as a ratio of lengths")
    H_L = C_LIGHT * math.sqrt(LAMBDA / 3.0)
    a0_num = C_LIGHT ** 2 * math.sqrt(LAMBDA / (32 * math.pi))
    L_MOND = C_LIGHT ** 2 / a0_num
    r_H = C_LIGHT / H_L
    q = L_MOND / (r_H / 2)
    q2 = L_MOND / r_H
    kap = sp.symbols("kappa", positive=True)
    c, G, Lam = sp.symbols("c G Lambda", positive=True)
    rho = Lam * c ** 2 / (8 * sp.pi * G)
    H = sp.sqrt(8 * sp.pi * G * rho / 3)
    a0 = kap * c * sp.sqrt(G * rho)
    resid = sp.simplify((c ** 2 / a0) / ((c / H) / 2) - 2 * c * H / a0)
    ok = (resid == 0 and abs(q - TARGET) / TARGET < 1e-12
          and abs(q2 - float(Z_EXACT)) / float(Z_EXACT) < 1e-12)
    check("K7", ok,
          "L_MOND/(r_H/2)=%.10f ; L_MOND/r_H=%.10f ; residual=%s"
          % (q, q2, resid),
          "exact; both ratios reproduce Z and 2Z",
          "unique meaning: MOND length in half-horizon radii")
    return {"L_MOND_m": L_MOND, "L_MOND_Gpc": L_MOND / MPC / 1e3,
            "r_H_m": r_H, "r_H_Gpc": r_H / MPC / 1e3,
            "L_over_half_rH": q, "L_over_rH": q2,
            "residual": str(resid)}


# ==========================================================================
# K8 -- the product test: does a hit fix kappa, or a product?
# ==========================================================================
def k8():
    hdr("K8 product test: kappa = 1/(beta sqrt(chi)) and N = 2 sqrt(8pi/3) beta sqrt(chi)")
    beta, chi, kap = sp.symbols("beta chi kappa", positive=True)
    # A27's identity, restated for N := 2 c H / a0
    N_of = 2 * sp.sqrt(8 * sp.pi / 3) * beta * sp.sqrt(chi)
    kap_of = 1 / (beta * sp.sqrt(chi))
    resid_ident = sp.simplify(N_of.subs(beta, 1 / (kap * sp.sqrt(chi)))
                              - 2 * sp.sqrt(8 * sp.pi / 3) / kap)
    # level set N = 11.5776  =>  beta sqrt(chi) = 2
    rhs = sp.solve(sp.Eq(N_of, 4 * sp.sqrt(8 * sp.pi / 3)), beta)
    beta_of_chi = sp.simplify(rhs[0])          # = 2/sqrt(chi)
    # the two named geometries
    k_21 = sp.simplify(kap_of.subs({beta: 2, chi: 1}))
    k_14 = sp.simplify(kap_of.subs({beta: 1, chi: 4}))
    # how many geometries satisfy it: one equation, two unknowns -> a curve
    n_eq, n_unk = 1, 2
    ok = (resid_ident == 0 and k_21 == sp.Rational(1, 2)
          and k_14 == sp.Rational(1, 2)
          and sp.simplify(beta_of_chi - 2 / sp.sqrt(chi)) == 0
          and (n_unk - n_eq) == 1)
    check("K8", ok,
          "beta=2/sqrt(chi) ; kappa(2,1)=%s ; kappa(1,4)=%s ; dim(level set)=%d"
          % (k_21, k_14, n_unk - n_eq),
          "one equation, two unknowns -> 1-parameter family",
          "a hit fixes the product beta sqrt(chi) = 2, i.e. kappa by definition")
    # what the product does and does not buy
    vals = [(b, float(sp.simplify(kap_of.subs({beta: b, chi: 4 / b ** 2}))))
            for b in (1.0, 1.5, 2.0, 3.0)]
    return {"identity_residual": str(resid_ident),
            "beta_of_chi": str(beta_of_chi),
            "kappa_at_2_1": str(k_21), "kappa_at_1_4": str(k_14),
            "level_set_dim": n_unk - n_eq,
            "examples": vals}


# ==========================================================================
# K9 -- irrationality, and the integer test
# ==========================================================================
def k9():
    hdr("K9 irrational: no integer count can equal it")
    p, q = sp.symbols("p q", positive=True)
    # if 4 sqrt(8 pi/3) = p/q then pi = 3 p^2/(128 q^2), rational: contradiction
    pi_expr = sp.solve(sp.Eq(sp.Integer(128) * sp.pi / 3, (p / q) ** 2), sp.pi)[0]
    rational_form = sp.simplify(pi_expr - 3 * p ** 2 / (128 * q ** 2)) == 0
    n11 = abs(dev(11.0))
    n12 = abs(dev(12.0))
    hits = [k for k in range(8, 17) if abs(dev(float(k))) < 0.01]
    ok = (rational_form and len(hits) == 0 and min(n11, n12) > 0.03)
    check("K9", ok,
          "pi = %s (rational in p,q) ; integer hits in [8,16]=%d ; "
          "11:%+.2f%% 12:%+.2f%%"
          % (pi_expr, len(hits), 100 * dev(11.0), 100 * dev(12.0)),
          "irrationality proof + no integer within 1%",
          "11.58 lies between 11 and 12; neither is within 3.5%")
    return {"pi_solved": str(pi_expr), "rational_form": rational_form,
            "n_integer_hits_1pct": len(hits),
            "dev_11": dev(11.0), "dev_12": dev(12.0)}


# ==========================================================================
# K10 -- where "12" comes from, and the 1/7 / 14 controls
# ==========================================================================
def k10():
    hdr("K10 the twelfth: 12 = 2 x round(2 sqrt(8 pi/3)); the 14 control")
    ratio_12 = 12.0 / TARGET
    exact_ratio = float(sp.sqrt(sp.Integer(27) / (8 * sp.pi)))
    kap12 = float(Z_EXACT) / 12.0
    R12 = 108.0 / (8 * math.pi)
    a0_12 = C_LIGHT * C_LIGHT * math.sqrt(LAMBDA / 108.0)
    H_L = C_LIGHT * math.sqrt(LAMBDA / 3.0)
    a0_exact = C_LIGHT ** 2 * math.sqrt(LAMBDA / (32 * math.pi))
    # H0 footing, canonical a0: 2 c H0 / a0_can
    N_H0 = 2 * C_LIGHT * H0 / A0_CAN
    dev14 = abs(N_H0 - 14.0) / 14.0
    ok = (abs(ratio_12 - exact_ratio) < 1e-12
          and abs(kap12 - 0.4824008) < 1e-7
          and abs(R12 - 4.29718) < 1e-5
          and dev14 < 1e-3)
    check("K10", ok,
          "12/2Z=%.10f ; kappa(12)=%.7f ; R(12)=%.5f ; |2cH0/a0-14|/14=%.2e"
          % (ratio_12, kap12, R12, dev14),
          "closed forms exact; 14-hit %.0fx tighter than 12"
          % (abs(dev(12.0)) / dev14),
          "the twelfth is 2 x round(5.7888): rounding, not counting")
    print("    round(2 sqrt(8 pi/3)) = round(%.6f) = 6  ->  2 x 6 = 12"
          % float(Z_EXACT))
    print("    exact 2Z = %.6f ; 12 is %+.3f%% ; 4pi = %.6f is %+.3f%%"
          % (TARGET, 100 * (12 / TARGET - 1), 4 * math.pi,
             100 * (4 * math.pi / TARGET - 1)))
    print("    H0 footing with a0_can: 2cH0/a0 = %.6f, i.e. the integer 14 to %.4f%%"
          % (N_H0, 100 * (N_H0 / 14 - 1)))
    return {"twelve_over_target": ratio_12,
            "twelve_over_target_exact": exact_ratio,
            "kappa_from_12": kap12, "R_from_12": R12,
            "a0_from_12": a0_12, "a0_exact": a0_exact,
            "a0_12_dev": (a0_12 - a0_exact) / a0_exact,
            "N_with_H0_can": N_H0, "dev_from_14": dev14,
            "twelve_over_fourteen": abs(dev(12.0)) / dev14,
            "fourpi_dev": 4 * math.pi / TARGET - 1}


# ==========================================================================
# K11 -- measurement status: is the number observed?
# ==========================================================================
def k11():
    hdr("K11 measurement status of 2cH_L/a0")
    km, ks = KAPPA_MEAS, KAPPA_SIG
    if MUT == "M4":
        km, ks = 0.500, 0.005
    N_of = float(Z_EXACT) / km
    sig_N = float(Z_EXACT) * ks / km ** 2
    z_target = abs(N_of - TARGET) / sig_N
    z_12 = abs(N_of - 12.0) / sig_N
    # sigma(kappa) needed for a 3-sigma separation of 2Z from 12
    sig_kappa_needed = (abs(12.0 - TARGET) / 3.0) * km ** 2 / float(Z_EXACT)
    ok = (z_target < 1.0 and z_12 < 1.0 and sig_kappa_needed * 10 < ks)
    check("K11", ok,
          "N(kappa_meas)=%.3f+-%.3f ; z(2Z)=%.2f ; z(12)=%.2f ; "
          "sigma_kappa(3sig)=%.5f vs %.3f"
          % (N_of, sig_N, z_target, z_12, sig_kappa_needed, ks),
          "both within 1 sigma; need 10x better kappa",
          "the data cannot tell 11.5776 from 12 today")
    return {"N_measured": N_of, "sigma_N": sig_N,
            "z_target": z_target, "z_twelve": z_12,
            "sigma_kappa_needed_3sigma": sig_kappa_needed,
            "sigma_kappa_current": ks,
            "improvement_needed": ks / sig_kappa_needed}


# ==========================================================================
# the declared pool grammar  (used by K12-K15)
# ==========================================================================
POOL_LO, POOL_HI = 0.05, 5000.0


def _pkey(v):
    return "%.10g" % v


def build_pool(maxlev=3):
    """Every expression with <= maxlev operations from the declared atoms.

    Ops: + - * / (binary) and sqrt (unary).  Each counts as one operation.
    Intermediate values are pruned to [0.05, 5000]; that rule is declared in the
    report.  Values are deduplicated at 10 significant digits (the value set is
    what the look-elsewhere density is about); the generated-expression count is
    kept separately.
    """
    atoms = [("2", 2.0), ("3", 3.0), ("4", 4.0), ("5", 5.0), ("8", 8.0),
             ("pi", math.pi), ("sqrt2", math.sqrt(2)), ("sqrt3", math.sqrt(3)),
             ("e", math.e)]
    levels = [[] for _ in range(maxlev + 1)]
    seen = [set() for _ in range(maxlev + 1)]
    for lab, v in atoms:
        k = _pkey(v)
        if k not in seen[0]:
            seen[0].add(k)
            levels[0].append((v, lab, 0))
    n_generated = len(levels[0])
    per_level = []
    for lev in range(1, maxlev + 1):
        gen = 0
        for (v, s, _l) in levels[lev - 1]:
            if v > 0:
                r = math.sqrt(v)
                if POOL_LO <= r <= POOL_HI:
                    gen += 1
                    k = _pkey(r)
                    if k not in seen[lev]:
                        seen[lev].add(k)
                        levels[lev].append((r, "sqrt(%s)" % s, lev))
        for i in range(lev):
            j = lev - 1 - i
            for (v1, s1, _l1) in levels[i]:
                for (v2, s2, _l2) in levels[j]:
                    for op in ("+", "-", "*", "/"):
                        if op == "/" and abs(v2) < 1e-12:
                            continue
                        if op == "+":
                            r = v1 + v2
                        elif op == "-":
                            r = v1 - v2
                        elif op == "*":
                            r = v1 * v2
                        else:
                            r = v1 / v2
                        gen += 1
                        if not (POOL_LO <= r <= POOL_HI):
                            continue
                        k = _pkey(r)
                        if k not in seen[lev]:
                            seen[lev].add(k)
                            levels[lev].append((r, "(%s%s%s)" % (s1, op, s2), lev))
        n_generated += gen
        per_level.append({"level": lev, "generated": gen,
                          "distinct": len(levels[lev])})
    nodes = [n for lv in levels for n in lv]
    return nodes, n_generated, per_level


_POOL = None


def pool():
    global _POOL
    if _POOL is None:
        _POOL = build_pool(3)
    return _POOL


# ==========================================================================
# K12 -- the look-elsewhere pool
# ==========================================================================
def k12():
    hdr("K12 look-elsewhere pool: <=3 operations from 9 atoms")
    nodes, n_gen, per_level = pool()
    vals = [v for (v, s, l) in nodes]
    win = [v for v in vals if TARGET * 0.9 <= v <= TARGET * 1.1]
    h1 = [(abs(dev(v)), v, s, l) for (v, s, l) in nodes if abs(dev(v)) <= 0.01]
    h01 = [h for h in h1 if h[0] <= 0.001]
    h001 = [h for h in h1 if h[0] <= 0.0001]
    h1.sort()
    if MUT == "M3":
        n_hits = 0
    else:
        n_hits = len(h1)
    frac = n_hits / float(len(win))
    print("    generated=%d  distinct values=%d  in window [%.3f,%.3f]: %d"
          % (n_gen, len(vals), TARGET * 0.9, TARGET * 1.1, len(win)))
    for pl in per_level:
        n_l = sum(1 for (v, s, l) in nodes if l == pl["level"])
        h_l = sum(1 for (v, s, l) in nodes
                  if l == pl["level"] and abs(dev(v)) <= 0.01)
        print("    level %d: generated %7d  distinct %7d  hits@1%% %4d"
              % (pl["level"], pl["generated"], n_l, h_l))
    print("    hits within 1%%: %d (%.2f%% of window) ; 0.1%%: %d ; 0.01%%: %d"
          % (n_hits, 100 * frac, len(h01), len(h001)))
    if h1:
        print("    closest: %.8f  dev %.3e  %s" % (h1[0][1], h1[0][0], h1[0][2]))
    ok = (frac > 0.05 and n_hits > 200)
    check("K12", ok,
          "hits@1%%=%d of %d window values (%.1f%%) ; hits@0.01%%=%d"
          % (n_hits, len(win), 100 * frac, len(h001)),
          "base rate > 5% of the window",
          "a 1% coincidence is the norm, not the exception")
    return {"n_generated": n_gen, "n_distinct": len(vals),
            "window_n": len(win), "n_hits_1pct": n_hits,
            "n_hits_01pct": len(h01), "n_hits_001pct": len(h001),
            "frac_1pct": frac,
            "per_level": per_level,
            "closest": {"value": h1[0][1], "dev": h1[0][0], "expr": h1[0][2]}
            if h1 else None}


# ==========================================================================
# K13 -- matched controls: integers, random targets, exact hits
# ==========================================================================
def k13():
    hdr("K13 matched controls: integer targets and 200 random targets")
    nodes, n_gen, _ = pool()
    vals = [v for (v, s, l) in nodes]

    def hits(T, tol=0.01):
        return sum(1 for v in vals if abs(v - T) / T <= tol)

    def exact(T):
        return sum(1 for v in vals if abs(v - T) < 1e-9)

    ex = {T: exact(float(T)) for T in (4, 10, 11, 12, 13)}
    ex_target = exact(TARGET)
    random.seed(20261021)
    rt = [random.uniform(10.5, 12.7) for _ in range(200)]
    counts = sorted(hits(T) for T in rt)
    mean = sum(counts) / len(counts)
    var = sum((x - mean) ** 2 for x in counts) / (len(counts) - 1)
    sd = math.sqrt(var)
    n_t = hits(TARGET)
    z = (n_t - mean) / sd
    pct = sum(1 for x in counts if x <= n_t) / float(len(counts))
    print("    exact hits: 4->%d 10->%d 11->%d 12->%d 13->%d ; target->%d"
          % (ex[4], ex[10], ex[11], ex[12], ex[13], ex_target))
    print("    hits@1%%: 12 -> %d ; target -> %d ; random targets: mean %.1f "
          "median %.1f sd %.1f [%d,%d]"
          % (hits(12.0), n_t, mean, counts[100], sd, counts[0], counts[-1]))
    print("    target z-score %.2f, percentile %.0f%%" % (z, 100 * pct))
    ok = (abs(z) < 2.0 and ex_target == 0 and min(ex.values()) >= 3)
    check("K13", ok,
          "z=%.2f (pct %.0f%%) ; exact hits at integers=%d..%d ; at target=0"
          % (z, 100 * pct, min(ex.values()), max(ex.values())),
          "|z|<2 ; integers hit exactly, target never",
          "the target is statistically an ordinary point of the pool")
    return {"exact_integer_hits": {str(k): v for k, v in ex.items()},
            "exact_target_hits": ex_target,
            "hits_12": hits(12.0), "hits_target": n_t,
            "random_mean": mean, "random_sd": sd,
            "random_min": counts[0], "random_max": counts[-1],
            "z": z, "percentile": pct,
            "n_random": len(rt)}


# ==========================================================================
# K14 -- look-elsewhere probability
# ==========================================================================
def k14():
    hdr("K14 look-elsewhere: how many trials does a 'hit' take?")
    d = RESULTS[-2]     # K12's numbers are in the returned dict; recompute here
    nodes, n_gen, _ = pool()
    vals = [v for (v, s, l) in nodes]
    win = [v for v in vals if TARGET * 0.9 <= v <= TARGET * 1.1]
    h = sum(1 for v in vals if abs(dev(v)) <= 0.01)
    p = h / float(len(win))
    m12 = 1 - (1 - p) ** 12
    m1 = p
    m3 = math.log(0.0027) / math.log(1 - p)
    m5 = math.log(5.733e-7) / math.log(1 - p)
    print("    p(hit | one candidate) = %.4f" % p)
    print("    P(>=1 hit | m=1)=%.3f  m=12)=%.3f" % (m1, m12))
    print("    candidates needed: 3sigma %.1f, 5sigma %.1f" % (m3, m5))
    ok = (p > 0.05 and m12 > 0.5 and m3 < 100)
    check("K14", ok,
          "p=%.3f ; P(>=1|m=12)=%.2f ; m(3sig)=%.1f ; m(5sig)=%.1f"
          % (p, m12, m3, m5),
          "p>5%; 12 candidates give >50% chance of a hit",
          "the task's own list is expected to produce ~1.2 hits")
    return {"p_hit": p, "P_any_m1": m1, "P_any_m12": m12,
            "m_3sigma": m3, "m_5sigma": m5,
            "expected_hits_in_12": 12 * p}


# ==========================================================================
# K15 -- the best chance hit vs the best physical near-miss
# ==========================================================================
def k15():
    hdr("K15 the best chance hit beats every physical near-miss")
    nodes, n_gen, _ = pool()
    best = min(((abs(dev(v)), v, s, l) for (v, s, l) in nodes),
               key=lambda t: t[0])
    best_phys = min(abs(dev(12.0)), abs(dev(4 * math.pi)), abs(dev(11.0)))
    ratio = best_phys / best[0]
    print("    best pool hit: %.10f  dev %.2e  %s" % (best[1], best[0], best[2]))
    print("    best physical near-miss: dev %.2e ; ratio %.0f x"
          % (best_phys, ratio))
    ok = (best[0] < 1e-4 and ratio > 1000)
    check("K15", ok,
          "pool best dev=%.2e ; physical best=%.2e ; ratio=%.0f"
          % (best[0], best_phys, ratio),
          "chance hit 1000x tighter than any physical candidate",
          "a 3-op expression with no meaning wins by three orders")
    return {"pool_best_dev": best[0], "pool_best_value": best[1],
            "pool_best_expr": best[2], "physical_best_dev": best_phys,
            "ratio": ratio}


# ==========================================================================
# K16 -- no O(10) number exists in the vacuum data
# ==========================================================================
def k16():
    hdr("K16 no O(10) dimensionless invariant in {c,G,hbar,Lambda,H}")
    # rows: (L, T, M) exponents
    rows = [(1, -1, 0),      # c
            (3, -2, -1),     # G
            (2, -1, 1),      # hbar
            (-2, 0, 0),      # Lambda
            (0, -1, 0)]      # H
    # columns are the five variables, rows the (L,T,M) dimension components
    Mx = sp.Matrix(rows).T          # 3 x 5
    ns = Mx.nullspace()
    dim_free = len(ns)
    # imposing H = H_Lambda leaves one invariant: hbar G Lambda / c^3
    x = HBAR * G_N * LAMBDA / C_LIGHT ** 3
    log10x = math.log10(x)
    print("    nullspace dim = %d (two invariants); with H=H_Lambda only x remains"
          % dim_free)
    print("    x = hbar G Lambda / c^3 = %.4e  (log10 = %.2f)" % (x, log10x))
    ok = (dim_free == 2 and x < 1e-120 and log10x < -120)
    check("K16", ok,
          "nullspace dim=%d ; x=%.3e (log10=%.1f)" % (dim_free, x, log10x),
          "dim 2 free, 1 after Friedmann; x < 1e-120",
          "an analytic F(x) is constant to 122 digits: no O(10) number")
    return {"nullspace_dim": dim_free,
            "invariant_x": x, "log10_x": log10x,
            "basis": [str(v.T) for v in ns]}


# ==========================================================================
# K17 -- the folklore divisors: cH/6, cH/2pi, and the footing
# ==========================================================================
def k17():
    hdr("K17 the folklore divisors: a0 = cH_L/6 and cH_L/2pi")
    H_L = C_LIGHT * math.sqrt(LAMBDA / 3.0)
    a0_exact = C_LIGHT ** 2 * math.sqrt(LAMBDA / (32 * math.pi))
    a0_ver = C_LIGHT * H_L / 6.0
    a0_mil = C_LIGHT * H_L / (2 * math.pi)
    a0_H0 = C_LIGHT * H0 / float(Z_EXACT)
    print("    exact    a0 = cH_L/%.4f = %.6e  (dev %+.3f%%)"
          % (float(Z_EXACT), a0_exact, 0.0))
    print("    cH_L/6   (Verlinde form)  = %.6e  (dev %+.3f%%)"
          % (a0_ver, 100 * (a0_ver / a0_exact - 1)))
    print("    cH_L/2pi (Milgrom form)   = %.6e  (dev %+.3f%%)"
          % (a0_mil, 100 * (a0_mil / a0_exact - 1)))
    print("    H0 footing (kappa=1/2)    = %.6e  (dev %+.3f%% vs H_L)"
          % (a0_H0, 100 * (a0_H0 / a0_exact - 1)))
    ok = (a0_mil < a0_ver < a0_exact
          and (1 - a0_ver / a0_exact) > 0.03
          and (1 - a0_mil / a0_exact) > 0.07
          and (a0_H0 / a0_exact - 1) > 0.2)
    check("K17", ok,
          "a0: %.4e < %.4e < %.4e ; H0 shift %+.1f%%"
          % (a0_mil, a0_ver, a0_exact, 100 * (a0_H0 / a0_exact - 1)),
          "both divisors > Z, so both a0 < exact ; footing > 20%",
          "both folklore divisors (6, 2pi) exceed Z = 5.7888; neither is derived")
    return {"a0_exact": a0_exact, "a0_verlinde": a0_ver,
            "a0_milgrom": a0_mil, "a0_H0_footing": a0_H0,
            "dev_verlinde": a0_ver / a0_exact - 1,
            "dev_milgrom": a0_mil / a0_exact - 1,
            "dev_H0_footing": a0_H0 / a0_exact - 1}


# ==========================================================================
# driver
# ==========================================================================
def main():
    print("A52 -- WHAT PHYSICAL QUANTITY EQUALS 2 sqrt(32 pi/3) = 11.5776 ?")
    print("mutation = %s" % MUT)
    numbers = {}
    fns = (k1, k2, k3, k4, k5, k6, k7, k8, k9, k10,
           k11, k12, k13, k14, k15, k16, k17)
    for fn in fns:
        numbers[fn.__name__.upper()] = fn()

    n_pass = sum(1 for r in RESULTS if r["pass"])
    n_tot = len(RESULTS)
    print("\nA52 COMPLETE: %d/%d checks PASS." % (n_pass, n_tot))

    # mutation confirmation
    if MUT != "none":
        broke = [r["id"] for r in RESULTS if not r["pass"]]
        if broke:
            print("MUTATION CONFIRMED (%s): broken checks %s" % (MUT, ",".join(broke)))
        else:
            print("MUTATION NOT DETECTED (%s)" % MUT)

    d = numbers
    display = {
        "target": "%.10f" % d["K1"]["target_value"],
        "Z": "%.10f" % d["K1"]["Z_value"],
        "a0_over_cH": "%.5f" % (1.0 / d["K1"]["Z_value"]),
        "a0_over_2cH": "%.5f" % (0.5 / d["K1"]["Z_value"]),
        "A_over_lP2": "%.4e" % d["K5"]["A_over_lP2"],
        "log2_S_dS": "%.1f" % d["K5"]["items"]["log2 S_dS"],
        "N_with_H0_can": "%.6f" % d["K10"]["N_with_H0_can"],
        "pool_frac_total": "%.2f" % (100.0 * d["K12"]["n_hits_1pct"] / d["K12"]["n_distinct"]),
        "sigma_kappa_rel_pct": "%.2f"
        % (100.0 * d["K11"]["sigma_kappa_needed_3sigma"] / KAPPA_MEAS),
        "e_sqrt6_dev_pct": "%.4f" % (100.0 * abs(dev(math.exp(math.sqrt(6))))),
        "fourpim1_dev_pct": "%.4f" % (100.0 * abs(dev(4 * math.pi - 1))),
        "pool_closest_pct": "%.5f" % (100.0 * d["K12"]["closest"]["dev"]),
        "R12_numerator_108": 108,
        "n_hits6": d["K2"]["n_hits6"],
        "n_distinct_hit_values": d["K2"]["n_distinct_hit_values"],
        "closest_miss_expr": d["K2"]["closest_miss_expr"],
        "closest_miss_pct": "%.2f" % (100 * d["K2"]["closest_miss_dev"]),
        "four_pi": "%.10f" % d["K4"]["four_pi"],
        "four_pi_dev_pct": "%.2f" % (100 * d["K4"]["four_pi_dev"]),
        "sphere_max": "%.6f" % d["K3"]["max_value"],
        "sphere_max_expr": d["K3"]["max_expr"],
        "S_dS": "%.4e" % d["K5"]["S_dS"],
        "sixth_root": "%.4e" % d["K5"]["sixth_root"],
        "closest_o10": d["K5"]["closest_o10"],
        "closest_o10_pct": "%.2f" % (100 * d["K5"]["closest_o10_dev"]),
        "a0_kappa_half": "%.10e" % d["K6"]["a0_kappa_half"],
        "ratio_2cH_a0": "%.10f" % d["K6"]["ratio"],
        "L_MOND_Gpc": "%.2f" % d["K7"]["L_MOND_Gpc"],
        "r_H_Gpc": "%.2f" % d["K7"]["r_H_Gpc"],
        "L_over_half_rH": "%.10f" % d["K7"]["L_over_half_rH"],
        "L_over_rH": "%.10f" % d["K7"]["L_over_rH"],
        "level_set_dim": d["K8"]["level_set_dim"],
        "dev_11_pct": "%.2f" % (100 * d["K9"]["dev_11"]),
        "dev_12_pct": "%.2f" % (100 * d["K9"]["dev_12"]),
        "twelve_ratio": "%.10f" % d["K10"]["twelve_over_target"],
        "kappa_from_12": "%.7f" % d["K10"]["kappa_from_12"],
        "R_from_12": "%.5f" % d["K10"]["R_from_12"],
        "a0_from_12": "%.6e" % d["K10"]["a0_from_12"],
        "dev14": "%.4f%%" % (100 * d["K10"]["dev_from_14"]),
        "twelve_over_fourteen": "%.0f" % d["K10"]["twelve_over_fourteen"],
        "S_dS_sqrt": "%.3e" % d["K5"]["items"]["S_dS^(1/2)"],
        "S_dS_quarter": "%.3e" % d["K5"]["items"]["S_dS^(1/4)"],
        "N_measured": "%.3f" % d["K11"]["N_measured"],
        "sigma_N": "%.3f" % d["K11"]["sigma_N"],
        "z_target": "%.2f" % d["K11"]["z_target"],
        "z_12": "%.2f" % d["K11"]["z_twelve"],
        "sigma_kappa_needed": "%.5f" % d["K11"]["sigma_kappa_needed_3sigma"],
        "improvement_needed": "%.1f" % d["K11"]["improvement_needed"],
        "pool_generated": d["K12"]["n_generated"],
        "pool_distinct": d["K12"]["n_distinct"],
        "pool_window": d["K12"]["window_n"],
        "pool_hits_1pct": d["K12"]["n_hits_1pct"],
        "pool_hits_01pct": d["K12"]["n_hits_01pct"],
        "pool_hits_001pct": d["K12"]["n_hits_001pct"],
        "pool_frac_1pct": "%.3f" % d["K12"]["frac_1pct"],
        "pool_closest_expr": d["K12"]["closest"]["expr"],
        "pool_closest_dev": "%.2e" % d["K12"]["closest"]["dev"],
        "exact_hits_12": d["K13"]["exact_integer_hits"]["12"],
        "exact_hits_target": d["K13"]["exact_target_hits"],
        "hits_12": d["K13"]["hits_12"],
        "random_mean": "%.1f" % d["K13"]["random_mean"],
        "random_sd": "%.1f" % d["K13"]["random_sd"],
        "random_min": d["K13"]["random_min"],
        "random_max": d["K13"]["random_max"],
        "z_pool": "%.2f" % d["K13"]["z"],
        "percentile": "%.0f" % (100 * d["K13"]["percentile"]),
        "p_hit": "%.4f" % d["K14"]["p_hit"],
        "P_any_12": "%.3f" % d["K14"]["P_any_m12"],
        "m_3sigma": "%.1f" % d["K14"]["m_3sigma"],
        "m_5sigma": "%.1f" % d["K14"]["m_5sigma"],
        "expected_in_12": "%.2f" % d["K14"]["expected_hits_in_12"],
        "pool_best_dev": "%.2e" % d["K15"]["pool_best_dev"],
        "pool_best_expr": d["K15"]["pool_best_expr"],
        "ratio_chance": "%.0f" % d["K15"]["ratio"],
        "invariant_x": "%.4e" % d["K16"]["invariant_x"],
        "log10_x": "%.1f" % d["K16"]["log10_x"],
        "a0_verlinde": "%.6e" % d["K17"]["a0_verlinde"],
        "a0_milgrom": "%.6e" % d["K17"]["a0_milgrom"],
        "a0_H0": "%.6e" % d["K17"]["a0_H0_footing"],
        "dev_verlinde_pct": "%.2f" % (100 * d["K17"]["dev_verlinde"]),
        "dev_milgrom_pct": "%.2f" % (100 * d["K17"]["dev_milgrom"]),
        "dev_H0_pct": "%.1f" % (100 * d["K17"]["dev_H0_footing"]),
    }

    out = {"lane": "A52",
           "status": "NO-GO(obstruction)",
           "verdict": "the number is a measurable ratio (2cH_L/a0 = L_MOND/(r_H/2)) "
                      "with exactly one physical identity, and that identity is "
                      "kappa = 1/2 restated; it is irrational, so it is not a count, "
                      "and any product that hits it leaves kappa fixed only by "
                      "definition. As a derivation of kappa it is numerology.",
           "mutation": MUT, "n_checks": n_tot, "n_pass": n_pass,
           "checks": RESULTS, "numbers": numbers,
           "report_display": display,
           "constants_used": CONSTANTS}
    suffix = "" if MUT == "none" else "_" + MUT
    with open(os.path.join(OUTDIR, "a52_results%s.json" % suffix), "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    return 0 if n_pass == n_tot else 1


if __name__ == "__main__":
    sys.exit(main())
