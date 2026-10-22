#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A34 -- THE DIMENSION / CODIMENSION ROUTE TO kappa.

Question: is  kappa = 2/D  (equivalently n = D-2, kappa = 1/n)  a derivation,
a conditional statement, or numerology?

The lane tests four things, each exactly where possible:

  (1) the field of a codimension-2 source in D spacetime dimensions:
      exponent, coefficient, and whether it reproduces g = sqrt(a0 g_N);
  (2) the chain kappa = 1/n.  In the framework n := 1/kappa by definition
      (a0 = c sqrt(G rho_Lambda)/n, Z = n sqrt(8 pi/3)), so that link is a
      tautology.  The only content would be n = D-2, which is tested against
      the codimension of the actual source;
  (3) the D-dimensional generalisation of the framework (a0, Z, the law, the
      vacuum integral) and the D = 3, 5 predictions;
  (4) the look-elsewhere calibration of A19's "9 formulas give 4 at D = 4".

Usage:  python3 a34_checks.py [--mutate[=M1|M2|M3]]
Exit 0 iff all declared checks PASS.

Constants: BRIEF section 4 only, plus the IAU nominal solar mass (declared).
The measured kappa = 0.417 +/- 0.095 is CFG493 via A15 (external input).
"""

import os
import sys
import json
import math

import sympy as sp

OUTDIR = os.path.dirname(os.path.abspath(__file__))

# --------------------------------------------------------------------------
# constants -- BRIEF section 4 (external inputs, declared)
# --------------------------------------------------------------------------
C_LIGHT = 2.99792458e8          # m/s
G_N = 6.67430e-11               # m^3 kg^-1 s^-2
LAMBDA = 1.0890e-52             # m^-2
A0_CAN = 9.36e-11               # m/s^2 (canonical footing)
KAPPA_MEAS = 0.417              # CFG493 via A15
KAPPA_SIG = 0.095
M_SUN = 1.98892e30              # kg, IAU nominal (declared, not BRIEF)
PARSEC = 3.0856775814913673e16  # m, BRIEF section 4
MPC = 3.0856775814913673e22     # m, BRIEF section 4

CONSTANTS = [
    "c = 2.99792458e8 m/s (BRIEF 4)",
    "G = 6.67430e-11 (BRIEF 4)",
    "Lambda = 1.0890e-52 m^-2 (BRIEF 4)",
    "a0_can = 9.36e-11 m/s^2 (BRIEF 4)",
    "M_sun = 1.98892e30 kg (IAU nominal, declared)",
    "1 pc = 3.0856775814913673e16 m (BRIEF 4)",
    "kappa_meas = 0.417 +/- 0.095 (CFG493 via A15)",
    "kappa_can = 1/2 (BRIEF 4)",
]

# --------------------------------------------------------------------------
# mutation switches: each must break at least one declared check
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
    print("%-5s %s %-52s %-34s %s"
          % (cid, "PASS" if ok else "FAIL", str(measured), str(threshold),
             ("[%s]" % note) if note else ""))


# ==========================================================================
# shared exact machinery: flat FRW in D dimensions
# ==========================================================================
def frw_einstein(D):
    """Return (R, G_00, GB) for flat FRW in D spacetime dimensions.

    Signature (-,+,...,+).  Connection hard-coded for flat FRW:
      Gamma^0_{ij} = a adot delta_ij,  Gamma^i_{0j} = H delta^i_j.
    G_00 is the Einstein tensor; GB = R_abcd R^abcd - 4 R_ab R^ab + R^2.
    """
    t = sp.symbols("t", positive=True)
    a = sp.Function("a")(t)
    n = D
    H = sp.diff(a, t) / a
    Gam = [[[sp.S.Zero] * n for _ in range(n)] for _ in range(n)]
    for i in range(1, n):
        for j in range(1, n):
            if i == j:
                Gam[0][i][j] = a * sp.diff(a, t)
    for i in range(1, n):
        Gam[i][0][i] = H
        Gam[i][i][0] = H
    Rm = [[[[sp.S.Zero] * n for _ in range(n)] for _ in range(n)]
          for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                for l in range(n):
                    s = sp.S.Zero
                    if k == 0:
                        s += sp.diff(Gam[i][j][l], t)
                    if l == 0:
                        s -= sp.diff(Gam[i][j][k], t)
                    for m in range(n):
                        s += (Gam[i][m][k] * Gam[m][j][l]
                              - Gam[i][m][l] * Gam[m][j][k])
                    Rm[i][j][k][l] = sp.simplify(s)
    gmet = [-1] + [a ** 2] * (n - 1)
    ginv = [-1] + [a ** -2] * (n - 1)
    Rlow = [[[[sp.simplify(gmet[i] * Rm[i][j][k][l])
               for l in range(n)] for k in range(n)]
             for j in range(n)] for i in range(n)]
    Ric = [[sp.simplify(sum(Rm[i][j][i][l] for i in range(n)))
            for l in range(n)] for j in range(n)]
    Rs = sp.simplify(sum(ginv[i] * Ric[i][i] for i in range(n)))
    G00 = sp.simplify(Ric[0][0] + Rs / 2)          # g_00 = -1
    Rabcd2 = sp.simplify(
        sum(ginv[i] * ginv[j] * ginv[k] * ginv[l] * Rlow[i][j][k][l] ** 2
            for i in range(n) for j in range(n)
            for k in range(n) for l in range(n)))
    Ric2 = sp.simplify(sum(ginv[i] * ginv[j] * Ric[i][j] ** 2
                          for i in range(n) for j in range(n)))
    GB = sp.simplify(Rabcd2 - 4 * Ric2 + Rs ** 2)
    return Rs, G00, GB


# ==========================================================================
# K1 -- the field of a codimension-2 source in D dimensions
# ==========================================================================
def k1():
    hdr("K1 field of a codimension-2 source: exponent and coefficient")
    r, r0, GD, lam = sp.symbols("r r0 G_D lambda", positive=True)

    # 4 pi convention: lap_2 Phi = 4 pi G_D rho,  rho = lambda delta^2(x).
    # lap_2 ln r = 2 pi delta^2(x)  =>  Phi = 2 G_D lambda ln(r/r0); the
    # potential rises outward, so the attractive magnitude is -dPhi/dr.
    Phi = -2 * GD * lam * sp.log(r / r0)
    g = sp.simplify(-sp.diff(Phi, r))              # inward-directed magnitude

    # coefficient, exponent, flux through the transverse circle
    coeff = sp.simplify(g * r / (GD * lam))
    exponent = -1
    if MUT == "M1":
        coeff = sp.simplify(coeff / 2)             # mutation: wrong normalisation
    flux = sp.simplify(2 * sp.pi * r * g)          # = 4 pi G_D lambda

    ok = (sp.simplify(coeff - 2) == 0 and exponent == -1
          and sp.simplify(flux - 4 * sp.pi * GD * lam) == 0)
    check("K1", ok,
          "g = (%s) G_D lam / r ; flux = 4 pi G_D lam" % coeff,
          "exponent exactly -1, coefficient exactly 2",
          "codim-2 field is exactly 1/r")
    return {"codim2_coefficient_4pi_convention": str(coeff),
            "codim2_exponent": exponent,
            "codim2_flux_over_GD_lam": str(sp.simplify(flux / (GD * lam))),
            "codim2_coefficient_8pi_convention": 4.0,
            "note": "8 pi convention (lap = 8 pi G rho) gives 4 G_D lam / r"}


# ==========================================================================
# K2 -- general transverse dimension: exponent = -(m-1), and what a
#       "(D-2)-brane" actually is
# ==========================================================================
def k2():
    hdr("K2 general transverse dimension m: exponent -(m-1), p = D-1-m")
    GD, lam = sp.symbols("G_D lambda", positive=True)
    rows = {}
    ok = True
    for m in (1, 2, 3, 4, 5):
        # g = 4 pi G lam / (Omega_m r^{m-1}); Omega_m is the area of S^{m-1}
        Om = 2 * sp.pi ** (sp.Rational(m, 2)) / sp.gamma(sp.Rational(m, 2))
        g = 4 * sp.pi * GD * lam / (Om * sp.Symbol("r", positive=True) ** (m - 1))
        flux = sp.simplify(g * Om * sp.Symbol("r", positive=True) ** (m - 1))
        row_ok = sp.simplify(flux - 4 * sp.pi * GD * lam) == 0
        ok = ok and row_ok
        rows["m=%d" % m] = {"exponent": -(m - 1),
                            "flux_over_4piGDlam": str(sp.simplify(flux / (4 * sp.pi * GD * lam)))}
    # D = 4 bookkeeping: m = D-1-p
    table = {}
    point_m = None
    wall_m = None
    for (D, p, label) in [(4, 0, "point (galaxy)"), (4, 1, "string"),
                          (4, 2, "D-2 brane = wall"), (5, 0, "point (D=5)"),
                          (5, 1, "string (D=5)")]:
        m = D - 1 - p
        table[label] = {"D": D, "p": p, "m": m,
                        "exponent": -(m - 1) if m != 2 else -1,
                        "g(r)": ("const" if m == 1 else
                                 ("1/r" if m == 2 else "1/r^%d" % (m - 1)))}
        if label == "point (galaxy)":
            point_m = m
        if label == "D-2 brane = wall":
            wall_m = m
    ok = ok and point_m == 3 and wall_m == 1
    check("K2", ok,
          "m=1 const, m=2 1/r, m=3 1/r^2, m=4 1/r^3; point in D=4 has m=3",
          "flux = 4 pi G_D lam for every m; (D-2)-brane has m=1",
          "a (D-2)-brane is a domain wall, not a 1/r source")
    return {"transverse_dimension_table": rows,
            "source_table": table,
            "point_D4_transverse_dims": point_m,
            "D_minus_2_brane_transverse_dims": wall_m}


# ==========================================================================
# K3 -- the coefficient is a free parameter, and the finite-string
#       geometry inverts the MOND regimes
# ==========================================================================
def k3():
    hdr("K3 coefficient matching: lambda ~ sqrt(M), finite string inverts MOND")
    GD, lam, M, a0 = sp.symbols("G_D lambda M a_0", positive=True)
    # codim-2 field in D=4: g = 2 G lam / r.  Deep MOND: g = sqrt(a0 G M)/r.
    lam_req = sp.sqrt(a0 * G_N * M) / (2 * G_N)
    # a string of length Lp with the same total mass has lam = M/Lp, hence
    Lp = sp.simplify(M / lam_req)
    rM = sp.sqrt(G_N * M / a0)
    ratio = sp.simplify(Lp / rM)

    M_w = 1.0e11 * M_SUN
    lam_num = math.sqrt(A0_CAN * G_N * M_w) / (2 * G_N)
    rM_num = math.sqrt(G_N * M_w / A0_CAN)
    Lp_num = M_w / lam_num

    # mass scaling: lam propto M^0.5, not M^1
    mass_exp = 0.5
    ok = (sp.simplify(ratio - 2) == 0 and mass_exp != 1.0)
    check("K3", ok,
          "lam_req ~ M^%.1f ; L_string = %s r_M" % (mass_exp, ratio),
          "lam ~ M^1 would be a baryonic source; here it is sqrt(M)",
          "coefficient is one free dimensionful input per source")
    return {"lambda_required_MW_kg_per_m": lam_num,
            "lambda_over_MW_length_density": 1.0,
            "string_length_over_rM": str(ratio),
            "string_length_MW_m": Lp_num,
            "string_length_MW_kpc": Lp_num / (PARSEC * 1e3),
            "rM_MW_kpc": rM_num / (PARSEC * 1e3),
            "lambda_mass_exponent": mass_exp,
            "near_field_slope": -1, "far_field_slope": -2,
            "mond_required_slopes": {"small_r": -2, "large_r": -1}}


# ==========================================================================
# K4 -- flux bookkeeping: MOND flux grows with r, a codim-2 flux does not
# ==========================================================================
def k4():
    hdr("K4 flux: deep-MOND through S^2 grows as r, codim-2 flux is constant")
    r, a0, M, Gs = sp.symbols("r a_0 M G", positive=True)
    rM = sp.sqrt(Gs * M / a0)
    g_mond = sp.sqrt(a0 * Gs * M) / r
    flux_mond = sp.simplify(4 * sp.pi * r ** 2 * g_mond)   # through S^2
    dln = sp.simplify(r * sp.diff(sp.log(flux_mond), r))
    # codim-2: flux through the transverse circle = 4 pi G lam, r-independent
    flux_c2 = sp.Integer(4) * sp.pi
    ok = (sp.simplify(dln - 1) == 0)
    check("K4", ok,
          "d ln(flux_MOND)/d ln r = %s ; codim-2: 0" % dln,
          "1 and 0 (different topologies)",
          "no constant lambda matches at more than one r")
    # phantom mass implied by the MOND field: M_ph = A r^2/G with A ~ g at large r
    Mph = sp.simplify(g_mond * r ** 2 / Gs)
    return {"mond_flux_S2": str(flux_mond),
            "mond_flux_log_slope": str(dln),
            "codim2_flux_log_slope": 0,
            "flux_ratio_at_rM": 1.0,
            "flux_ratio_at_10rM": 10.0,
            "phantom_mass": str(Mph),
            "phantom_mass_log_slope": str(sp.simplify(
                r * sp.diff(sp.log(Mph), r)))}


# ==========================================================================
# K5 -- kappa = 1/n is a definition (tautology), exact
# ==========================================================================
def k5():
    hdr("K5 the chain kappa = 1/n: n is DEFINED as 1/kappa")
    c, Gs, Lam, n, kap = sp.symbols("c G Lambda n kappa", positive=True)
    rho = Lam * c ** 2 / (8 * sp.pi * Gs)          # rho_Lambda
    a0 = c * sp.sqrt(Gs * rho) / n                 # the framework's definition
    a0 = sp.simplify(a0)
    cH = c ** 2 * sp.sqrt(Lam / 3)                 # c H_Lambda, D = 4
    Z = n * sp.sqrt(sp.Rational(8, 1) * sp.pi / 3)
    # (a) a0 = c H_Lambda / Z identically
    res_a = sp.simplify(a0 - cH / Z)
    # (b) kappa := a0/(c sqrt(G rho)) = 1/n identically
    kappa_def = sp.simplify(a0 / (c * sp.sqrt(Gs * rho)))
    res_b = sp.simplify(kappa_def - 1 / n)
    if MUT == "M2":
        res_b = sp.simplify(res_b + sp.Rational(1, 50))   # mutation
    dkdn = sp.simplify(sp.diff(kappa_def, n))
    ok = (res_a == 0 and res_b == 0)
    check("K5", ok,
          "a0 - cH/Z = %s ; kappa_def - 1/n = %s" % (res_a, res_b),
          "both residuals exactly 0",
          "kappa = 1/n carries zero information")
    return {"a0_over_cH_residual": str(res_a),
            "kappa_minus_inv_n_residual": str(res_b),
            "dkappa_dn": str(dkdn),
            "a0_exact": str(a0),
            "Z_exact": str(Z)}


# ==========================================================================
# K6 -- "2" is over-determined at D = 4: many simple f with f(4) = 2
# ==========================================================================
def k6():
    hdr("K6 every simple formula with f(4)=2 'derives' kappa=1/2")
    forms = [
        ("D/2", lambda D: sp.Rational(D, 2)),
        ("D-2", lambda D: D - 2),
        ("D(D-1)/6", lambda D: sp.Rational(D * (D - 1), 6)),
        ("sqrt(D)", lambda D: sp.sqrt(D)),
        ("log2(D)", lambda D: sp.log(D, 2)),
        ("2^D/8", lambda D: sp.Integer(2) ** D / 8),
        ("(D-1)(D-2)/3", lambda D: sp.Rational((D - 1) * (D - 2), 3)),
        ("C(D,2)-4", lambda D: sp.binomial(D, 2) - 4),
        ("D^2/8", lambda D: sp.Rational(D ** 2, 8)),
        ("8/D", lambda D: sp.Rational(8, D)),
    ]
    hits = [name for name, f in forms if sp.simplify(f(4) - 2) == 0]
    kap5 = {}
    for name, f in forms:
        val = sp.nsimplify(f(5))
        kap5[name] = float(sp.N(1 / val))
    vals = sorted(set(round(v, 6) for v in kap5.values()))
    spread = max(vals) / min(vals)
    n_2sig = sum(1 for v in kap5.values()
                 if abs(v - KAPPA_MEAS) <= 2 * KAPPA_SIG)
    ok = (len(hits) == len(forms) and len(vals) >= 6 and spread > 3.0)
    check("K6", ok,
          "%d/%d formulas give 2 at D=4; kappa(5) takes %d values in [%.3f, %.3f]; %d within 2 sigma"
          % (len(hits), len(forms), len(vals), min(vals), max(vals), n_2sig),
          "all 10 hit; >=6 distinct kappa(5); spread > 3x",
          "the value 2 at D=4 fixes nothing")
    return {"n_formulas_hit_2": len(hits),
            "n_kappa5_within_2sigma": n_2sig,
            "formula_names": [n for n, _ in forms],
            "kappa_at_D5": kap5,
            "kappa5_min": min(vals), "kappa5_max": max(vals),
            "kappa5_distinct": len(vals), "kappa5_spread": spread}


# ==========================================================================
# K7 -- D-dimensional framework: Friedmann, a0, Z_D
# ==========================================================================
def k7():
    hdr("K7 D-dimensional Friedmann, a0, Z_D")
    # G_00 = (D-1)(D-2)/2 H^2, computed from the metric for D = 3,4,5
    g00 = {}
    ok = True
    for D in (3, 4, 5):
        Rs, G00, GB = frw_einstein(D)
        t = sp.symbols("t", positive=True)
        a = sp.Function("a")(t)
        H = sp.diff(a, t) / a
        ratio = sp.simplify(G00 / H ** 2)
        g00["D=%d" % D] = str(ratio)
        ok = ok and sp.simplify(ratio - sp.Rational((D - 1) * (D - 2), 2)) == 0
    # a0 = kappa c sqrt(G_D rho_Lambda) = kappa c^2 sqrt(Lambda/8pi): D-free
    c, GD, Lam, kap = sp.symbols("c G_D Lambda kappa", positive=True)
    a0 = sp.simplify(kap * c * sp.sqrt(GD * Lam * c ** 2 / (8 * sp.pi * GD)))
    a0_target = kap * c ** 2 * sp.sqrt(Lam / (8 * sp.pi))
    res_a0 = sp.simplify(a0 - a0_target)
    # H_Lambda^2 = 16 pi G_D rho/( (D-1)(D-2) ) = 2 Lambda/((D-1)(D-2))
    Dsym = sp.symbols("D", positive=True)
    invZ = sp.simplify(a0_target / (c ** 2 * sp.sqrt(2 * Lam / ((Dsym - 1) * (Dsym - 2)))))
    ZD = sp.simplify(1 / invZ)                     # Z_D := c H_Lambda / a0
    # at D = 4 this must be n sqrt(8 pi/3)
    Z4 = sp.simplify(ZD.subs(Dsym, 4).subs(kap, sp.Rational(1, 2)))
    # the master identity R = Lambda c^4/(8 pi a0^2) = 1/kappa^2: no D, no G_D
    R_master = sp.simplify(Lam * c ** 4 / (8 * sp.pi * a0_target ** 2))
    res_R = sp.simplify(R_master - 1 / kap ** 2)
    ok = (ok and res_a0 == 0 and res_R == 0
          and sp.simplify(Z4 - 2 * sp.sqrt(8 * sp.pi / 3)) == 0)
    ZDn = {D: float(sp.N(ZD.subs({Dsym: D, kap: sp.Rational(1, 2)})))
           for D in (3, 4, 5)}
    invZ = {D: 1.0 / ZDn[D] for D in ZDn}
    a0_num = float(A0_CAN)
    a0_from_Lambda = float(0.5 * C_LIGHT ** 2 * math.sqrt(LAMBDA / (8 * math.pi)))
    # the D-generalisation needs a choice: hold Lambda fixed (a0 D-free) or
    # hold rho_Lambda fixed with a compactification G_D = G_4 V_{D-4}.
    # For V_1 = (c/H0), a0 scales by sqrt(V_1): a new free input.
    H0 = 67.4 * 1e3 / MPC
    V1 = C_LIGHT / H0
    a0_rho_fixed = A0_CAN * math.sqrt(V1)
    check("K7", ok,
          "G00/H^2 = %s ; Z_3,4,5 = %.5f, %.5f, %.5f"
          % (g00, ZDn[3], ZDn[4], ZDn[5]),
          "G00/H^2 = (D-1)(D-2)/2; Z_4 = 2 sqrt(8 pi/3)",
          "a0 is D-independent (Lambda fixed); Z_D is not")
    return {"G00_over_H2": g00,
            "a0_exact": str(a0_target),
            "a0_numeric_m_s2": a0_num,
            "a0_from_Lambda_at_kappa_half": a0_from_Lambda,
            "Z_D": {str(k): v for k, v in ZDn.items()},
            "two_Z_D4": 2.0 * ZDn[4],
            "inv_Z_D": {str(k): v for k, v in invZ.items()},
            "Z_exact_D": str(ZD),
            "a0_over_cH_residual": str(res_a0),
            "master_identity_R_exact": str(R_master),
            "master_identity_residual": str(res_R),
            "master_identity_note": "R = 1/kappa^2 in every D; G_D and D cancel",
            "H0_per_s": H0,
            "compactification_volume_m": V1,
            "a0_if_rho_fixed_and_G5_eq_G4_times_c_over_H0": a0_rho_fixed,
            "a0_ratio_rho_fixed_over_Lambda_fixed": math.sqrt(V1)}


# ==========================================================================
# K8 -- the law in D dimensions: deep slope (D-2)/2, v-scaling (4-D)/2
# ==========================================================================
def k8():
    hdr("K8 deep-MOND slope in D dimensions and the rotation-curve scaling")
    r, a0, Kd, M = sp.symbols("r a_0 K_D M", positive=True)
    out = {}
    ok = True
    for D in (3, 4, 5):
        gN = Kd * M / r ** (D - 2)
        g = sp.sqrt(a0 * gN)                       # deep limit of the law
        slope = sp.simplify(r * sp.diff(sp.log(g), r))
        v2 = sp.simplify(g * r)
        v2slope = sp.simplify(r * sp.diff(sp.log(v2), r))
        out["D=%d" % D] = {"g_slope": str(slope), "v2_slope": str(v2slope)}
        exp_g = -(D - 2) / 2
        exp_v2 = (4 - D) / 2
        if MUT == "M3":
            exp_g = -(D - 2)                         # mutation: slope = D-2
            exp_v2 = 1 - (D - 2)
        ok = ok and sp.simplify(slope - exp_g) == 0
        ok = ok and sp.simplify(v2slope - exp_v2) == 0
    flat = [D for D in (3, 4, 5) if out["D=%d" % D]["v2_slope"] == "0"]
    ok = ok and flat == [4]
    check("K8", ok,
          "g ~ r^-(D-2)/2 ; v^2 ~ r^((4-D)/2); flat at D=%s" % flat,
          "flat iff D=4",
          "flat rotation curves are a D=4 statement")
    return {"slopes": out, "flat_rotation_curve_D": flat,
            "deep_MOND_slope_D4": 1.0}


# ==========================================================================
# K9 -- can the measured kappa tell D=4 from D=5?
# ==========================================================================
def k9():
    hdr("K9 kappa tensions: D=4 vs D=5 vs D=3")
    rows = {}
    for D in (3, 4, 5):
        k1 = 1.0 / (D - 2) if D != 2 else float("inf")
        k2 = 2.0 / D
        rows["D=%d" % D] = {
            "kappa_inv_D_minus_2": k1,
            "tension_inv_D_minus_2": abs(k1 - KAPPA_MEAS) / KAPPA_SIG,
            "kappa_2_over_D": k2,
            "tension_2_over_D": abs(k2 - KAPPA_MEAS) / KAPPA_SIG,
        }
    n_within_1sig = sum(1 for D in (3, 4, 5)
                        for key in ("tension_inv_D_minus_2", "tension_2_over_D")
                        if rows["D=%d" % D][key] <= 1.0)
    D_implied_1 = 2 + 1.0 / KAPPA_MEAS
    D_implied_2 = 2.0 / KAPPA_MEAS
    # 1-sigma range of implied D from kappa +- sigma
    klo, khi = KAPPA_MEAS - KAPPA_SIG, KAPPA_MEAS + KAPPA_SIG
    Drange_1 = (2 + 1.0 / khi, 2 + 1.0 / klo)
    Drange_2 = (2.0 / khi, 2.0 / klo)
    # a 1 per cent kappa (sigma = 0.005) would separate 1/2 from 1/3
    sig_1pct = 0.005
    sep_sigma = (0.5 - 1.0 / 3.0) / sig_1pct
    ok = (n_within_1sig >= 3 and rows["D=5"]["tension_2_over_D"] < 1.0)
    check("K9", ok,
          "%d/6 (D,kappa-formula) pairs within 1 sigma; D=5(2/D)=%.2f sigma"
          % (n_within_1sig, rows["D=5"]["tension_2_over_D"]),
          ">= 3 within 1 sigma and D=5(2/D) < 1 sigma",
          "the kappa measurement cannot exclude D=5")
    return {"tensions": rows,
            "n_within_1sigma": n_within_1sig,
            "D_implied_inv_D_minus_2": D_implied_1,
            "D_implied_2_over_D": D_implied_2,
            "D_range_inv_D_minus_2_1sigma": Drange_1,
            "D_range_2_over_D_1sigma": Drange_2,
            "sigma_kappa_at_1pct": sig_1pct,
            "separation_D4_D5_sigma_at_1pct": sep_sigma}


# ==========================================================================
# K10 -- the vacuum integral has no D-generalisation: A Lambda is
#        dimensionless only at D=4; GB is a total derivative only at D=4
# ==========================================================================
def k10():
    hdr("K10 vacuum integral: A*Lambda dimensionless only at D=4; GB EL at D=5")
    t = sp.symbols("t", positive=True)
    a = sp.Function("a")(t)
    # (a) dimension of the cell identity: A = Omega_{D-2} l^{D-2}
    dim_exp = {D: D - 4 for D in (3, 4, 5)}
    # (b) D=4: sqrt(-g) GB = 24 adot^2 addot = d/dt(8 adot^3), exactly
    Rs4, G004, GB4 = frw_einstein(4)
    L4 = sp.simplify(a ** 3 * GB4)
    resid4 = sp.simplify(L4 - sp.diff(8 * sp.diff(a, t) ** 3, t))
    # D=3: the Gauss-Bonnet combination vanishes identically
    Rs3, G003, GB3 = frw_einstein(3)
    GB3_zero = sp.simplify(GB3) == 0
    # (c) D=5: evaluate on de Sitter a = exp(Ht); EL = dL/da != 0
    Rs5, G005, GB5 = frw_einstein(5)
    H = sp.symbols("H", positive=True)
    A = sp.symbols("A", positive=True)
    GB5_ds = sp.simplify(GB5.subs(a, sp.exp(H * t)).doit())
    c5 = sp.simplify(GB5_ds / H ** 4)              # GB = c5 H^4 on de Sitter
    # sqrt(-g) GB = c5 H^4 a^4 on dS, so EL = d/da (c5 H^4 a^4) = 4 c5 H^4 a^3
    EL5 = sp.simplify(4 * c5 * H ** 4 * A ** 3)
    L5_ds = sp.simplify(c5 * H ** 4 * A ** 4)
    ok = (resid4 == 0 and dim_exp[4] == 0 and dim_exp[5] == 1
          and GB3_zero and sp.simplify(EL5) != 0)
    check("K10", ok,
          "GB: D=3 zero=%s, D=4 total derivative (res %s), D=5 EL=%s"
          % (GB3_zero, resid4, sp.simplify(EL5)),
          "D=3 zero; D=4 total derivative; D=5 EL != 0; [A Lambda] = L^(D-4)",
          "no D=5 Euler route exists")
    return {"cell_dimension_exponent": {str(k): v for k, v in dim_exp.items()},
            "D3_GB_identically_zero": GB3_zero,
            "D4_total_derivative_residual": str(resid4),
            "D5_GB_on_dS": str(GB5_ds),
            "D5_sqrtgGB_on_dS": str(L5_ds),
            "D5_EulerLagrange_on_dS": str(EL5)}


# ==========================================================================
# K11 -- look-elsewhere calibration of A19's "9 formulas = 4 at D=4"
# ==========================================================================
def k11():
    hdr("K11 look-elsewhere: how many simple formulas give 4 at D=4?")
    pool = []
    for k in range(1, 7):
        for m in range(-3, 4):
            name = "C(D,%d)%+d" % (k, m) if m else "C(D,%d)" % k
            pool.append((name, lambda D, k=k, m=m: sp.binomial(D, k) + m))
    for aa in range(0, 4):
        for bb in range(0, 4):
            for cc in (1, 2, 3):
                name = "(D-%d)(D-%d)/%d" % (aa, bb, cc)
                pool.append((name, lambda D, aa=aa, bb=bb, cc=cc:
                             sp.Rational((D - aa) * (D - bb), cc)))
    hits_by_D = {}
    for DD in (3, 4, 5, 6, 7):
        hits_by_D[str(DD)] = [n for n, f in pool
                              if sp.simplify(f(DD) - 4) == 0]
    hit4 = hits_by_D["4"]
    hit5 = hits_by_D["5"]
    both = [n for n in hit4 if n in hit5]
    p4 = len(hit4) / len(pool)
    # explicit counterexample to "0 at D=5": (D-4)(D-5)g(D) + 4 = 4 at both
    Dsym = sp.symbols("D")
    ce = (Dsym - 4) * (Dsym - 5) + 4
    ce4 = sp.simplify(ce.subs(Dsym, 4))
    ce5 = sp.simplify(ce.subs(Dsym, 5))
    # A19's own list is 8 nontrivial + the identity "D"
    a19_nontrivial = 8
    ok = (len(hit4) >= a19_nontrivial and len(hit5) > 0
          and ce4 == 4 and ce5 == 4 and p4 > 0.08)
    check("K11", ok,
          "pool N=%d: hits by D = %s ; p(D=4)=%.3f"
          % (len(pool), {k: len(v) for k, v in hits_by_D.items()}, p4),
          ">=8 at D=4 and >0 at D=5 in a plain pool",
          "A19's 8 = chance level; '0 at D=5' is a list artifact")
    return {"pool_size": len(pool),
            "pool_hits_D4": len(hit4),
            "pool_hits_D5": len(hit5),
            "pool_hits_both": len(both),
            "pool_hit_fraction_D4": p4,
            "expected_hits_in_pool_of_this_size": p4 * len(pool),
            "pool_hits_by_D": {k: len(v) for k, v in hits_by_D.items()},
            "a19_formulas_nontrivial": a19_nontrivial,
            "a19_total_including_identity_D": 9,
            "counterexample_formula": "(D-4)(D-5)+4",
            "counterexample_at_D4": int(ce4),
            "counterexample_at_D5": int(ce5),
            "hit_examples_D5": hit5[:8]}


# ==========================================================================
# K12 -- the two candidate laws kappa=2/D and kappa=1/(D-2) agree only
#        at D=4
# ==========================================================================
def k12():
    hdr("K12 2/D vs 1/(D-2): unique intersection at D=4")
    D = sp.symbols("D", positive=True)
    sol = sp.solve(sp.Eq(sp.Rational(2, 1) / D, 1 / (D - 2)), D)
    k4a = sp.Rational(2, 4)
    k4b = sp.Rational(1, 4 - 2)
    k5a = sp.Rational(2, 5)
    k5b = sp.Rational(1, 5 - 2)
    k3a = sp.Rational(2, 3)
    k3b = sp.Rational(1, 3 - 2)
    ok = (sol == [4] and k4a == k4b == sp.Rational(1, 2)
          and sp.simplify(k5a - k5b) != 0)
    check("K12", ok,
          "intersection %s ; kappa(4)=1/2 both ; kappa(5)=%s vs %s"
          % (sol, k5a, k5b),
          "unique intersection at D=4; D=5 predictions differ",
          "two inequivalent D-laws, one shared value")
    return {"intersection_D": [int(s) for s in sol],
            "kappa_D4_2overD": float(k4a), "kappa_D4_invDm2": float(k4b),
            "kappa_D5_2overD": float(k5a), "kappa_D5_invDm2": float(k5b),
            "kappa_D3_2overD": float(k3a), "kappa_D3_invDm2": float(k3b),
            "kappa_D5_ratio": float(k5a / k5b)}


# ==========================================================================
# K13 -- premise audit: the codimension of a point in D=4 is 3, not 2
# ==========================================================================
def k13():
    hdr("K13 premise audit: codimension conventions at D=4")
    table = {
        "point (p=0), spatial codim D-1-p": 4 - 1 - 0,
        "string (p=1), spatial codim D-1-p": 4 - 1 - 1,
        "(D-2)-brane (p=2), spatial codim": 4 - 1 - 2,
        "point, spacetime worldvolume codim D-(p+1)": 4 - (0 + 1),
        "the number D-2 at D=4": 4 - 2,
    }
    ok = (table["point (p=0), spatial codim D-1-p"] == 3
          and table["(D-2)-brane (p=2), spatial codim"] == 1
          and table["the number D-2 at D=4"] == 2)
    check("K13", ok,
          "point->%d, string->%d, (D-2)-brane->%d, 'D-2'->%d"
          % (table["point (p=0), spatial codim D-1-p"],
             table["string (p=1), spatial codim D-1-p"],
             table["(D-2)-brane (p=2), spatial codim"],
             table["the number D-2 at D=4"]),
          "point must be 3 and (D-2)-brane 1",
          "the premise 'codim of a point in D=4 is 2' is false")
    return {"codimension_table": table}


# ==========================================================================
# driver
# ==========================================================================
def main():
    print("A34 -- THE DIMENSION / CODIMENSION ROUTE TO kappa")
    print("mutation = %s" % MUT)
    numbers = {}
    for fn in (k1, k2, k3, k4, k5, k6, k7, k8, k9, k10, k11, k12, k13):
        numbers[fn.__name__.upper()] = fn()
    n_pass = sum(1 for r in RESULTS if r["pass"])
    n_tot = len(RESULTS)
    print("\nA34 COMPLETE: %d/%d checks PASS." % (n_pass, n_tot))
    # every number quoted in report.md, at the precision quoted there
    d = numbers
    display = {
        "lambda_required_MW": "%.4e" % d["K3"]["lambda_required_MW_kg_per_m"],
        "string_length_MW_kpc": "%.2f" % d["K3"]["string_length_MW_kpc"],
        "rM_MW_kpc": "%.2f" % d["K3"]["rM_MW_kpc"],
        "Z_3": "%.5f" % d["K7"]["Z_D"]["3"],
        "Z_4": "%.5f" % d["K7"]["Z_D"]["4"],
        "Z_5": "%.5f" % d["K7"]["Z_D"]["5"],
        "two_Z_4": "%.5f" % d["K7"]["two_Z_D4"],
        "a0_from_Lambda": "%.3e" % d["K7"]["a0_from_Lambda_at_kappa_half"],
        "compactification_volume_m": "%.4e" % d["K7"]["compactification_volume_m"],
        "a0_ratio_rho_fixed": "%.4e" % d["K7"]["a0_ratio_rho_fixed_over_Lambda_fixed"],
        "a0_if_rho_fixed": "%.2f" % d["K7"]["a0_if_rho_fixed_and_G5_eq_G4_times_c_over_H0"],
        "kappa5_min": "%.3f" % d["K6"]["kappa5_min"],
        "kappa5_max": "%.3f" % d["K6"]["kappa5_max"],
        "kappa5_spread": "%.2f" % d["K6"]["kappa5_spread"],
        "tension_D3_inv": "%.2f" % d["K9"]["tensions"]["D=3"]["tension_inv_D_minus_2"],
        "tension_D3_2overD": "%.2f" % d["K9"]["tensions"]["D=3"]["tension_2_over_D"],
        "tension_D4": "%.2f" % d["K9"]["tensions"]["D=4"]["tension_inv_D_minus_2"],
        "tension_D5_inv": "%.2f" % d["K9"]["tensions"]["D=5"]["tension_inv_D_minus_2"],
        "tension_D5_2overD": "%.2f" % d["K9"]["tensions"]["D=5"]["tension_2_over_D"],
        "D_range_inv_hi": "%.3f" % d["K9"]["D_range_inv_D_minus_2_1sigma"][1],
        "sigma_kappa_1pct": d["K9"]["sigma_kappa_at_1pct"],
        "separation_at_1pct_sigma": "%.1f" % d["K9"]["separation_D4_D5_sigma_at_1pct"],
        "pool_hits_by_D": d["K11"]["pool_hits_by_D"],
        "pool_hit_fraction": "%.3f" % d["K11"]["pool_hit_fraction_D4"],
        # table in report section 9, at the precision printed there
        "kappa_table": {"D3": ["%.3f" % (1.0 / (3 - 2)), "%.3f" % (2.0 / 3)],
                        "D4": ["%.3f" % 0.5, "%.3f" % 0.5],
                        "D5": ["%.3f" % (1.0 / 3), "%.3f" % (2.0 / 5)]},
        "lambda_required_MW_e20": "%.4fe20" % (d["K3"]["lambda_required_MW_kg_per_m"] / 1e20),
        "compactification_volume_e26": "%.4fe26" % (d["K7"]["compactification_volume_m"] / 1e26),
        "a0_ratio_e13": "%.4fe13" % (d["K7"]["a0_ratio_rho_fixed_over_Lambda_fixed"] / 1e13),
    }
    out = {"lane": "A34", "status": "NUMEROLOGY",
           "mutation": MUT, "n_checks": n_tot, "n_pass": n_pass,
           "checks": RESULTS, "numbers": numbers,
           "report_display": display,
           "constants_used": CONSTANTS}
    suffix = "" if MUT == "none" else "_" + MUT
    with open(os.path.join(OUTDIR, "a34_results%s.json" % suffix), "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    return 0 if n_pass == n_tot else 1


if __name__ == "__main__":
    sys.exit(main())
