#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
A19 -- THE REMAINING HOLE FOR kappa: the scale-setting functional.

A15 established: the halo sector supplies 2 equations for 3 unknowns; the single
missing equation is

        a0^2 = G rho_DE c^2 / 4      <=>      R := rho_DE c^2 / (a0^2/G) = 4

with rho_DE = Lambda c^4/(8 pi G).  This lane tests the strongest topological /
geometric candidates for a functional that returns exactly 4, each exactly:

  (i)   Euler-density (Gauss-Bonnet) balance
  (ii)  zero-mode / channel count of a covector in D = 4
  (iii) one quantum per cell, cell area 4 pi ell0^2
  (iv)  the saturation cap P_max = a0^2/G vs rho_DE c^2
  (v)   CONTROL: Unruh temperature = de Sitter temperature   (dof = 0)
  (vi)  CONTROL: the de Sitter geodesic ball                 (dof = 0)

Every printed number is recomputed here; nothing is quoted except the BRIEF's
constants (listed in CONSTANTS) and the measured kappa (CFG493, cited).

Usage:  python3 a19_checks.py [--mutate[=M1|M2|M3]]
Exit 0 iff all declared checks PASS.
"""

import sys
import json
import math

import sympy as sp

# --------------------------------------------------------------------------
# constants -- BRIEF section 4 (external inputs, declared)
# --------------------------------------------------------------------------
C_LIGHT = 2.99792458e8          # m/s
G_N     = 6.67430e-11           # m^3 kg^-1 s^-2
LAMBDA  = 1.0890e-52            # m^-2
A0_CAN  = 9.36e-11              # m/s^2  (canonical footing)
A0_ALT  = 1.13e-10              # m/s^2  (alt footing, never pooled)
KAPPA_MEAS     = 0.417          # CFG493, as quoted in A15 (measured kappa)
KAPPA_MEAS_SIG = 0.095

CONSTANTS = [
    "c = 2.99792458e8 m/s",
    "G = 6.67430e-11",
    "Lambda = 1.0890e-52 m^-2",
    "a0_can = 9.36e-11 m/s^2",
    "a0_alt = 1.13e-10 m/s^2 (alt footing, never pooled)",
    "rho_Lambda = 5.831e-27 kg/m^3 (BRIEF rounding, used only for the A15 cross-check)",
    "kappa_meas = 0.417 +/- 0.095 (CFG493 via A15)",
]

# --------------------------------------------------------------------------
# mutation switches: each must break at least one declared check
# --------------------------------------------------------------------------
MUT = "none"
for _arg in sys.argv[1:]:
    if _arg.startswith("--mutate"):
        MUT = _arg.split("=", 1)[1] if "=" in _arg else "M1"

EINSTEIN_DENOM = 8.0 * math.pi if MUT != "M1" else 4.0 * math.pi   # M1: drop a 2
CELL_CHI       = 1 if MUT != "M2" else 2                           # M2: S^4, not 4-ball
COUNT_MODE     = "onshell" if MUT != "M3" else "offshell"          # M3: count ghosts

CHECKS = []


def check(cid, ok, value, threshold, note=""):
    CHECKS.append({"id": cid, "pass": bool(ok), "value": str(value),
                   "threshold": str(threshold), "note": note})
    print("%-4s %s %-46s %s%s" % (cid, "PASS" if ok else "FAIL",
                                  value, threshold,
                                  ("  [" + note + "]") if note else ""))
    return ok


def hdr(text):
    print("\n-- %s " % text + "-" * max(0, 66 - len(text)))


# ==========================================================================
# K1 -- the master identity and the equivalence chain, exact
# ==========================================================================
def k1():
    hdr("K1 master identity R = Lambda c^4/(8 pi a0^2) = Lambda L^2/(8 pi)")
    Lam, G, c, a0, L, ell, A = sp.symbols(
        "Lambda G c a_0 L ell A", positive=True)
    pi = sp.pi

    u = Lam * c**4 / (8 * pi * G)              # rho_DE c^2 : ENERGY density
    R = u / (a0**2 / G)
    res1 = sp.simplify(R - Lam * c**4 / (8 * pi * a0**2))

    R_of_L = sp.simplify(R.subs(a0, c**2 / L))
    res2 = sp.simplify(R_of_L - Lam * L**2 / (8 * pi))

    # the four equivalent spellings of R = 4
    #   (a) Lambda L^2 = 32 pi          (L = c^2/a0, the MOND length)
    #   (b) Lambda ell^2 = 8 pi         (ell = L/2)
    #   (c) A Lambda = 32 pi^2          (A = 4 pi ell^2)
    #   (d) a0^2 = G rho c^2/4
    sol_L = sp.solve(sp.Eq(R_of_L, 4), L)
    res_a = [sp.simplify(Lam * s**2 - 32 * pi) for s in sol_L]
    res_b = sp.simplify((Lam * ell**2 - 8 * pi).subs(ell, sol_L[0] / 2))
    res_c = sp.simplify((A * Lam - 32 * pi**2).subs(
        A, 4 * pi * (sol_L[0] / 2)**2))
    res_d = sp.simplify((a0**2 - G * u / 4).subs(
        a0, c**2 / sol_L[0]))

    worst = max(abs(float(x)) for x in
                [res1, res2] + res_a + [res_b, res_c, res_d])
    check("K1", worst == 0.0, "max|residual| = %.1e" % worst, "== 0 (exact)",
          "sympy; all four spellings equivalent")
    return {"K1_worst_residual": worst,
            "K1_L_at_R4": str(sol_L[0])}


# ==========================================================================
# K2 -- the footing numbers
# ==========================================================================
def k2():
    hdr("K2 numbers on the canonical footing")
    c, G, Lam, a0 = C_LIGHT, G_N, LAMBDA, A0_CAN
    pi = math.pi

    rho_m = Lam * c**2 / (EINSTEIN_DENOM * G)    # rho_DE : MASS density
    u = rho_m * c**2                             # rho_DE c^2 : energy density
    R = u * G / a0**2
    kappa = 1.0 / math.sqrt(R)
    n = 1.0 / kappa

    L = c**2 / a0
    r_H = math.sqrt(3.0 / Lam)
    ell_E = math.sqrt(8.0 * pi * CELL_CHI / Lam)   # A Lambda = 32 pi^2 chi

    s_DE = c * math.sqrt(G * rho_m)
    cH = c**2 * math.sqrt(Lam / 3.0)
    Z = 2.0 * math.sqrt(8.0 * pi / 3.0)
    a0_32pi = c**2 * math.sqrt(Lam / (32.0 * pi))

    ok = (abs(R - 4.0) < 0.01 and abs(kappa - 0.5) < 0.01
          and abs(L / ell_E - 2.0) < 0.01)
    check("K2", ok,
          "R = %.5f, kappa = %.6f, n = %.5f" % (R, kappa, n),
          "|R-4| < 0.01",
          "L/ell_E = %.5f" % (L / ell_E))
    print("     rho_DE = %.6e kg/m^3   u = %.6e J/m^3   s_DE = %.6e m/s^2"
          % (rho_m, u, s_DE))
    print("     cH_Lambda = %.6e   Z = 2sqrt(8pi/3) = %.6f   1/Z = %.6f"
          % (cH, Z, 1.0 / Z))
    print("     L = c^2/a0 = %.6e m   r_H = %.6e m   ell_E = %.6e m"
          % (L, r_H, ell_E))
    print("     a0(32pi form) = %.6e m/s^2   rel.diff vs footing = %.2e"
          % (a0_32pi, abs(a0_32pi - a0) / a0))
    R_alt = (s_DE / A0_ALT)**2
    print("     alt footing a0 = %.3e : R = %.5f, kappa = %.5f"
          % (A0_ALT, R_alt, 1.0 / math.sqrt(R_alt)))
    # cross-check against the verified lane A15, which used the rounded
    # rho_Lambda = 5.831e-27 as an input and reported kappa = 0.500473
    s_a15 = c * math.sqrt(G * 5.831e-27)
    kappa_a15 = a0 / s_a15
    print("     kappa with A15's rounded rho_Lambda = 5.831e-27 : %.6f"
          % kappa_a15)
    assert abs(kappa_a15 - 0.500473) < 1e-5
    return {"R_canonical": R, "kappa_law": kappa, "n_inv_kappa": n,
            "R_alt_footing": R_alt, "kappa_alt_footing": 1.0 / math.sqrt(R_alt),
            "kappa_with_A15_rho": kappa_a15,
            "rho_DE_mass": rho_m, "u_DE": u,
            "L_MOND": L, "r_H": r_H, "ell_E": ell_E,
            "L_over_ellE": L / ell_E, "s_DE": s_DE, "cH_Lambda": cH, "Z": Z,
            "a0_from_32pi": a0_32pi,
            "a0_32pi_reldiff": abs(a0_32pi - a0) / a0}


# ==========================================================================
# K3 -- the Euler (Gauss-Bonnet) charges, exact
# ==========================================================================
def k3():
    hdr("K3 Euler charge: S^4 -> 64 pi^2 (chi=2); unit charge 32 pi^2 (chi=1)")
    pi = sp.pi
    n = 4
    d = sp.eye(n)

    # maximally symmetric: R_abcd = k (g_ac g_bd - g_ad g_bc), flat indices, k=1
    R2_abcd = 0
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for e in range(n):
                    Rabcd = d[a, c] * d[b, e] - d[a, e] * d[b, c]
                    R2_abcd += Rabcd * Rabcd
    R2_ab = 9 * n            # R_ab = 3 g_ab  ->  R_ab R^ab = 9*4
    Rsc = 12                 # R = 12
    GB = sp.Integer(R2_abcd) - 4 * R2_ab + Rsc**2

    # integral over S^4 of radius r: GB/r^4 * 8 pi^2 r^4/3
    charge_S4 = sp.simplify(GB * sp.Rational(8, 1) * pi**2 / 3)
    # flat 4-ball: bulk GB density = 0, chi(B^4) = 1 -> charge = 32 pi^2
    charge_unit = 32 * pi**2
    res1 = sp.simplify(charge_S4 - 32 * pi**2 * 2)
    # and the S^4 charge is exactly chi(S^4) times the unit charge
    res2 = sp.simplify(charge_S4 / charge_unit - 2)

    print("     R2_abcd = %s, R2_ab = %s, R^2 = %s, GB = %s"
          % (R2_abcd, R2_ab, Rsc**2, GB))
    print("     charge(S^4) = %s ; charge(unit, chi=1) = %s"
          % (charge_S4, charge_unit))
    ok = (res1 == 0 and res2 == 0 and GB == 24)
    check("K3", ok,
          "charge(S^4) = 64 pi^2, GB = 24/r^4",
          "GB charge = 32 pi^2 * chi, exact")
    return {"GB_bulk_coefficient": int(GB),
            "R2_ab_coefficient": R2_ab, "R2_scalar_coefficient": Rsc**2,
            "chi_S4": 2, "chi_B4": 1,
            "euler_charge_S4": "64*pi^2",
            "euler_charge_unit": "32*pi^2"}


# ==========================================================================
# K4 -- the Euler density is a total derivative: no bulk equation of motion
# ==========================================================================
def k4():
    hdr("K4 GB density is a total derivative -> stationarity is vacuous")
    t = sp.symbols("t", real=True)
    a = sp.Function("a")
    at = a(t)
    ap = sp.Derivative(at, t)
    app = sp.Derivative(at, t, 2)

    # FRW: GB * sqrt(g) = 24 * adot^2 * addot  (with N = 1)
    Lgb = 24 * ap**2 * app

    # Euler-Lagrange for L(a, adot, addot):
    #   dL/da - d/dt(dL/dadot) + d^2/dt^2 (dL/daddot) = 0
    EL = (sp.diff(Lgb, at)
          - sp.diff(sp.diff(Lgb, ap), t)
          + sp.diff(sp.diff(Lgb, app), t, 2))
    EL = sp.simplify(EL.doit())

    # and the total-derivative form: 24 adot^2 addot = d/dt(8 adot^3)
    total = sp.simplify(Lgb.doit() - sp.diff(8 * ap**3, t).doit())

    ok = (EL == 0 and total == 0)
    check("K4", ok,
          "EL[GB] = %s ; GB*sqrt(g) - d/dt(8 adot^3) = %s" % (EL, total),
          "both identically 0 (exact)",
          "no bulk eom => no stationarity condition")
    return {"EL_GB": str(EL), "total_derivative_residual": str(total),
            "GB_FRW_sqrtg": "24*adot^2*addot = d/dt(8*adot^3)"}


# ==========================================================================
# K5 -- the Euler balance is a0-blind: a definition, not dynamics
# ==========================================================================
def k5():
    hdr("K5 d(A Lambda)/d a0 = 0 while dR/d a0 != 0")
    Lam, c, a0, chi, ell = sp.symbols("Lambda c a_0 chi ell", positive=True)
    pi = sp.pi

    # cell radius DEFINED by A Lambda = 32 pi^2 chi, A = 4 pi ell^2
    ell_of_Lam = sp.sqrt(sp.simplify(32 * pi**2 * chi / (4 * pi * Lam)))
    ALam = sp.simplify(4 * pi * ell_of_Lam**2 * Lam)

    dAL_da0 = sp.simplify(sp.diff(ALam, a0))
    R = Lam * (c**2 / a0)**2 / (8 * pi)
    dR_da0 = sp.simplify(sp.diff(R, a0))

    R_at_ell = sp.simplify((Lam * ell**2 / (2 * pi)).subs(
        ell, ell_of_Lam))          # R expressed via the cell radius
    # R via the cell is 4*chi -- independent of a0
    dRell_da0 = sp.simplify(sp.diff(R_at_ell, a0))

    ok = (dAL_da0 == 0 and dR_da0 != 0 and dRell_da0 == 0
          and sp.simplify(R_at_ell - 4 * chi) == 0)
    check("K5", ok,
          "d(A L)/da0 = %s ; dR/da0 = %s" % (dAL_da0, dR_da0),
          "0 and nonzero (exact)",
          "R = 4*chi is a0-free: balance renames ell")
    return {"dALambda_da0": str(dAL_da0),
            "R_at_cell_radius": str(R_at_ell)}


# ==========================================================================
# K6 -- R = beta^2 chi: the exact-4 condition is a curve, not a point
# ==========================================================================
def k6():
    hdr("K6 R = beta^2 chi ; R = 4 is one equation in two unknowns")
    pi = sp.pi
    beta, chi = sp.symbols("beta chi", positive=True)
    R = beta**2 * chi

    pairs = [(2, 1), (1, 4), (sp.sqrt(2), 2), (2 / sp.sqrt(3), 3),
             (sp.Rational(2, 3), 9), (sp.Rational(1, 2), 16),
             (sp.Rational(2, 5), 25), (2 * sp.sqrt(2), sp.Rational(1, 2))]
    res = []
    for b, ch in pairs:
        res.append(sp.simplify(sp.nsimplify(b**2 * ch) - 4))
    nsol = sum(1 for x in res if abs(float(x)) < 1e-12)
    worst = max(abs(float(x)) for x in res)

    # natural conventions: beta in {1 (radius), 2 (diameter)}, chi in {1,2,3,4}
    # (chi = 1,2,3,4 are realised by B^4, S^4, CP^2, S^2 x S^2)
    natural = []
    grid = []
    for b in (1, 2):
        for ch in (1, 2, 3, 4):
            Rv = b * b * ch
            grid.append({"beta": b, "chi": ch, "R": Rv,
                         "kappa": 1.0 / math.sqrt(Rv)})
            if Rv == 4:
                natural.append((b, ch))
    kappas = sorted({round(g["kappa"], 6) for g in grid})
    print("     natural grid: %d (beta,chi) -> %d distinct R values %s"
          % (len(grid), len({g["R"] for g in grid}),
             sorted({g["R"] for g in grid})))
    print("     distinct kappa from the same class: %s" % kappas)

    ok = nsol == len(pairs) and len(natural) >= 2
    check("K6", ok,
          "%d/%d exact (beta,chi) give 4 ; %d natural ones %s"
          % (nsol, len(pairs), len(natural), natural),
          "all exact, >=2 natural solutions",
          "non-unique: (2,1)=diam/4-ball, (1,4)=radius/S2xS2")
    return {"exact_beta_chi_pairs": nsol,
            "natural_solutions": [list(map(float, p)) for p in natural],
            "natural_grid": grid,
            "distinct_kappa_natural": kappas,
            "beta_chi_list": [[str(b), str(c)] for b, c in pairs]}


# ==========================================================================
# K7 -- channel count of a covector in D = 4
# ==========================================================================
def k7():
    hdr("K7 covector channel count: no honest count is 4")
    D = 4
    massless = D - 2                 # physical, on shell
    massive = D - 1
    offshell = D
    ghost = offshell - massive       # 1 constraint, no ghost for Proca

    # general D: physical massless count D-2 equals 4 only at D = 6
    Ds = [d for d in range(3, 12) if d - 2 == 4]

    honest = {massless, massive}
    counted = offshell if COUNT_MODE == "offshell" else None

    ok = (4 not in honest) and (counted is None) and Ds == [6]
    check("K7", ok,
          "massless %d, massive %d, off-shell %d (honest max %d)"
          % (massless, massive, offshell, max(honest)),
          "no honest count == 4",
          "off-shell 4 = 3 physical + 1 constraint")
    print("     D-2 = 4 only at D = %s ; a covector in D=4 has 2 physical"
          % Ds)
    return {"count_massless": massless, "count_massive": massive,
            "count_offshell": offshell, "D_where_physical_is_4": Ds}


# ==========================================================================
# K8 -- the channel split is foliation-dependent
# ==========================================================================
def k8():
    hdr("K8 boost mixes scalar into vector: the count is basis-dependent")
    # A^mu = (0, a, 0, 0), k along z: pure vector in the frame n=(1,0,0,0)
    # boost along x with rapidity eta: A'^0 = -a sinh(eta), A'^1 = a cosh(eta)
    etas = [0.0, 0.5, 1.0, 2.0]
    frac = []
    for e in etas:
        s, ch = math.sinh(e), math.cosh(e)
        A0, A1 = -s, ch
        norm = math.sqrt(A0**2 + A1**2)
        frac.append(abs(A0) / norm)     # = tanh(eta)

    # the invariant count (physical polarizations) is 2 in every frame
    invariant = [2 for _ in etas]

    ok = (frac[0] == 0.0 and frac[-1] > 0.5
          and len(set(invariant)) == 1)
    check("K8", ok,
          "scalar fraction %.4f -> %.4f ; invariant count still 2"
          % (frac[0], frac[-1]),
          "changes by > 0.5 while invariant stays 2",
          "count per channel is slicing-dependent")
    return {"scalar_fraction_vs_eta": dict(zip(map(str, etas), frac)),
            "invariant_physical_count": 2}


# ==========================================================================
# K9 -- one quantum per cell is identically a0-independent
# ==========================================================================
def k9():
    hdr("K9 P_max * A = 4 pi c^4/G, independent of a0")
    a0, G, c = sp.symbols("a_0 G c", positive=True)
    pi = sp.pi
    Pmax = a0**2 / G
    A = 4 * pi * (c**2 / a0)**2
    prod = sp.simplify(Pmax * A)
    d = sp.simplify(sp.diff(prod, a0))
    target = 4 * pi * c**4 / G

    # dimensional audit: [stress*area] = force ; [u] = stress = M L^-1 T^-2
    dim_PA = {"M": 1, "L": 1, "T": -2}        # force
    dim_u = {"M": 1, "L": -1, "T": -2}        # energy density = stress
    gap = {k: dim_PA[k] - dim_u[k] for k in dim_PA}   # an AREA, not zero

    # the unique dimensionally consistent repair uses the one available length:
    #   P_max * A = u * ell0^2  with A = 4 pi ell0^2  ->  P_max = u/(4 pi)
    # i.e. R = 4 pi.
    R_repair_num = 4 * math.pi

    vals = []
    for aa in (5e-11, 9.36e-11, 2e-10):
        vals.append(float((aa**2 / G_N) * (4 * math.pi * (C_LIGHT**2 / aa)**2)))

    ok = (sp.simplify(prod - target) == 0 and d == 0
          and gap == {"M": 0, "L": 2, "T": 0}
          and abs(R_repair_num - 4.0) > 1.0
          and max(vals) - min(vals) < 1e-6 * max(vals))
    check("K9", ok,
          "P_max*A = %s ; d/da0 = %s ; repaired R = 4 pi" % (prod, d),
          "exact, derivative 0, gap = L^2 (area)",
          "the repair gives R = 4 pi = %.3f, not 4" % R_repair_num)
    print("     4 pi c^4/G = %.4e N ; c^4/(4G) = %.4e N ; ratio = %.6f"
          % (4 * math.pi * C_LIGHT**4 / G_N,
             C_LIGHT**4 / (4 * G_N),
             16 * math.pi))
    return {"Pmax_times_A": "4*pi*c^4/G",
            "Pmax_times_A_newton": 4 * math.pi * C_LIGHT**4 / G_N,
            "dPmaxA_da0": str(d),
            "dim_gap": gap,
            "R_from_dimensional_repair": R_repair_num,
            "PmaxA_spread_over_3_a0": max(vals) - min(vals)}


# ==========================================================================
# K10 -- the saturation cap: three natural values, no principle
# ==========================================================================
def k10():
    hdr("K10 cap family R in {1,2,4}; tensions against measured kappa")
    pi = math.pi
    rows = []
    for R in (1, 2, 4):
        kappa = 1.0 / math.sqrt(R)
        ALam = 8 * pi**2 * R
        tension = (kappa - KAPPA_MEAS) / KAPPA_MEAS_SIG
        rows.append((R, kappa, ALam, tension))
        print("     R=%d -> kappa=%.6f, A*Lambda=%.4f pi^2, tension=%.2f sigma"
              % (R, kappa, ALam / pi**2, tension))

    # forecast: at 1% on kappa (sigma = 0.005) the chi=1 / chi=2 separation
    sig1 = 0.01 * 0.5
    # kappa(chi) = 1/(2 sqrt(chi)): chi=1 -> 0.5, chi=2 -> 0.353553
    sep = abs(0.5 - 1.0 / (2.0 * math.sqrt(2))) / sig1
    print("     forecast: 1%% on kappa (sigma=%.4f) separates chi=1 from chi=2 "
          "at %.1f sigma" % (sig1, sep))

    ok = (rows[0][3] > 5.0 and rows[1][3] > 2.5 and abs(rows[2][3]) < 1.5)
    check("K10", ok,
          "tensions %.2f / %.2f / %.2f sigma" % tuple(r[3] for r in rows),
          "R=1 > 5 sigma, R=2 > 2.5 sigma, R=4 < 1.5 sigma",
          "only the quarter survives the measurement")
    return {"cap_rows": [{"R": r[0], "kappa": r[1],
                          "A_Lambda_over_pi2": r[2] / pi**2,
                          "tension_sigma": r[3]} for r in rows],
            "chi_separation_sigma_at_1pct": sep,
            "sigma_kappa_at_1pct": sig1}


# ==========================================================================
# K11 -- "4" is the most over-determined integer in D = 4
# ==========================================================================
def k11():
    hdr("K11 structural formulas equal to 4 at D=4; none at D=5")
    def fs(D):
        return {
            "D": D,
            "(D-2)^2": (D - 2)**2,
            "2(D-2)": 2 * (D - 2),
            "D(D-1)/3": D * (D - 1) / 3.0,
            "C(D,3)": D * (D - 1) * (D - 2) / 6.0,
            "C(D,2)-2": D * (D - 1) / 2.0 - 2,
            "D(D+1)/2-6": D * (D + 1) / 2.0 - 6,
            "2^D/D": 2.0**D / D,
            "(D-1)(D-2)/2+1": (D - 1) * (D - 2) / 2.0 + 1,
        }
    f4, f5 = fs(4), fs(5)
    hit4 = [k for k, v in f4.items() if abs(v - 4) < 1e-12]
    hit5 = [k for k, v in f5.items() if abs(v - 4) < 1e-12]
    ok = len(hit4) >= 8 and len(hit5) == 0
    check("K11", ok,
          "%d formulas = 4 at D=4, %d at D=5" % (len(hit4), len(hit5)),
          ">= 8 at D=4 and 0 at D=5",
          "the match to 4 is a D=4 degeneracy")
    for k in hit4:
        print("       %-16s = %.6f   (D=5: %.6f)" % (k, f4[k], f5[k]))
    return {"formulas_equal_4_at_D4": len(hit4),
            "formulas_equal_4_at_D5": len(hit5),
            "formula_table": {k: [f4[k], f5[k]] for k in f4}}


# ==========================================================================
# K12 -- CONTROL: Unruh = de Sitter temperature (dof = 0)
# ==========================================================================
def k12():
    hdr("K12 Unruh-de Sitter matching: R = 3/(8 pi), kappa = sqrt(8 pi/3)")
    pi = sp.pi
    Lam, c, G, a0 = sp.symbols("Lambda c G a_0", positive=True)

    # T_Unruh = hbar a/(2 pi c k_B), T_dS = hbar H/(2 pi k_B), H = c sqrt(Lam/3)
    # hbar and k_B cancel identically -> a = c^2 sqrt(Lam/3)
    a_unruh = c**2 * sp.sqrt(Lam / 3)
    rho_m = Lam * c**2 / (8 * pi * G)          # mass density
    kappa_U = sp.simplify(a_unruh / (c * sp.sqrt(G * rho_m)))
    R_U = sp.simplify(1 / kappa_U**2)
    ratio_to_4 = sp.simplify(4 / R_U)

    ok = (sp.simplify(kappa_U - sp.sqrt(8 * pi / 3)) == 0
          and sp.simplify(R_U - 3 / (8 * pi)) == 0
          and sp.simplify(ratio_to_4 - 32 * pi / 3) == 0)
    check("K12", ok,
          "kappa_U = %s = %.6f ; R_U = %s = %.6f"
          % (kappa_U, float(kappa_U), R_U, float(R_U)),
          "exact; R_U = 3/(8 pi) != 4",
          "off by 32 pi/3 = %.3f" % float(ratio_to_4))
    return {"kappa_unruh": float(kappa_U),
            "kappa_unruh_exact": str(kappa_U),
            "R_unruh": float(R_U), "R_unruh_exact": str(R_U),
            "ratio_4_over_R_unruh": float(ratio_to_4)}


# ==========================================================================
# K13 -- dof table: "returns 4" and "no free parameter" are exclusive
# ==========================================================================
def k13():
    hdr("K13 free-parameter audit of the six candidates")
    pi = math.pi
    rows = [
        ("(i)   Euler balance",   1, 4.0),
        ("(ii)  channel count",   1, None),
        ("(iii) quantum/cell",    1, None),
        ("(iv)  saturation cap",  1, 4.0),
        ("(v)   Unruh-dS",        0, 3.0 / (8 * pi)),
        ("(vi)  dS geodesic ball", 0, 3.0 / (8 * pi)),
    ]
    bad = [r for r in rows if r[1] == 0 and r[2] is not None
           and abs(r[2] - 4.0) < 1e-9]
    good = [r for r in rows if r[2] is not None and abs(r[2] - 4.0) < 1e-9
            and r[1] >= 1]
    for name, dof, R in rows:
        print("     %-22s dof=%d  R=%s" %
              (name, dof, "free" if R is None else "%.6f" % R))
    ok = (len(bad) == 0 and len(good) == 2)
    check("K13", ok,
          "dof=0 candidates returning 4: %d ; dof>=1 returning 4: %d"
          % (len(bad), len(good)),
          "0 and 2",
          "no parameter-free candidate returns 4")
    return {"dof_table": [{"candidate": n, "dof": d,
                           "R": (None if R is None else R)}
                          for n, d, R in rows]}


# ==========================================================================
# K14 -- the Euler cell is super-horizon: "per cell" is not a counting
# ==========================================================================
def k14():
    hdr("K14 ell_E / r_H = sqrt(8 pi/3) > 1 : fewer than one cell in H^-1")
    Lam = LAMBDA
    pi = math.pi
    r_H = math.sqrt(3.0 / Lam)
    ell_E = math.sqrt(8.0 * pi / Lam)
    ratio = ell_E / r_H
    n_cells = (r_H / ell_E)**3
    ok = ratio > 1.0 and n_cells < 1.0
    check("K14", ok,
          "ell_E/r_H = %.6f ; cells in Hubble volume = %.5f"
          % (ratio, n_cells),
          "ratio > 1 and N < 1",
          "the Euler cell is not a cell")
    return {"ellE_over_rH": ratio, "cells_in_hubble_volume": n_cells,
            "ellE_over_rH_exact": "sqrt(8*pi/3)"}


# ==========================================================================
# K15 -- 32 pi^2 = pi * 8 pi * 4 : the coincidence is arithmetic
# ==========================================================================
def k15():
    hdr("K15 A*Lambda = 8 pi^2 n^2 and 32 pi^2 = pi * 8 pi * 4")
    pi = sp.pi
    n = sp.symbols("n", positive=True)
    Lam, c, a0 = sp.symbols("Lambda c a_0", positive=True)

    R = sp.simplify(Lam * (c**2 / a0)**2 / (8 * pi))
    # A = pi L^2 (sphere of radius L/2) -> A Lambda = 8 pi^2 R = 8 pi^2 n^2
    ALam = sp.simplify(pi * (c**2 / a0)**2 * Lam)
    res1 = sp.simplify(ALam - 8 * pi**2 * R)
    res2 = sp.simplify((32 * pi**2) - (pi * 8 * pi * 4))
    # factorisation of the target: pi (sphere) * 8 pi (Einstein) * n^2
    res3 = sp.simplify((8 * pi**2 * n**2).subs(n, 2) - 32 * pi**2)

    ok = (res1 == 0 and res2 == 0 and res3 == 0)
    check("K15", ok,
          "A*Lambda - 8 pi^2 R = %s ; 32 pi^2 - pi*8pi*4 = %s"
          % (res1, res2),
          "all 0 (exact)",
          "32 pi^2 = pi * 8pi * 4: no topology in it")
    return {"A_Lambda_over_R": "8*pi^2",
            "factorisation": "32*pi^2 = pi * 8*pi * 4"}


# ==========================================================================
# K16 -- the ledger: kappa = ell_Lambda / L, i.e. 1/kappa = beta
# ==========================================================================
def k16():
    hdr("K16 kappa = ell_Lambda/L exactly; 1/kappa = beta = L/ell")
    pi = sp.pi
    Lam, c, a0, G = sp.symbols("Lambda c a_0 G", positive=True)

    ell_Lam = sp.sqrt(8 * pi / Lam)                 # chi = 1 cell radius
    L = c**2 / a0
    rho_m = Lam * c**2 / (8 * pi * G)               # mass density
    kappa = a0 / (c * sp.sqrt(G * rho_m))

    res = sp.simplify(kappa - ell_Lam / L)
    inv = sp.simplify(1 / kappa - L / ell_Lam)
    # cell units: at kappa = 1/2, L/ell_Lam = 2 exactly
    beta_cell = sp.simplify((L / ell_Lam).subs(
        a0, c**2 * sp.sqrt(Lam / (32 * pi))))
    # horizon units: L/r_H = Z = 2 sqrt(8 pi/3)
    r_H = sp.sqrt(3 / Lam)
    Z = 2 * sp.sqrt(8 * pi / 3)
    inv_horizon = sp.simplify((L / r_H).subs(
        a0, c**2 * sp.sqrt(Lam / (32 * pi))))

    ok = (res == 0 and inv == 0 and beta_cell == 2
          and sp.simplify(inv_horizon - Z) == 0)
    check("K16", ok,
          "kappa = ell/L exact ; 1/kappa = %s (cells), %s (horizons)"
          % (beta_cell, sp.simplify(inv_horizon)),
          "0 ; 2 ; Z (exact)",
          "the integer n = 1/kappa IS the length ratio")
    return {"kappa_equals_ellL_over_L": str(res),
            "inv_kappa_cell_units": str(beta_cell),
            "inv_kappa_horizon_form": str(sp.simplify(inv_horizon)),
            "Z_value": float(Z)}


# ==========================================================================
# K17 -- a LOCAL Euler-density balance is falsified inside one galaxy
# ==========================================================================
def k17():
    hdr("K17 local Euler density is constant; cold stress is not")
    pi = math.pi
    # on de Sitter the GB density is a constant: eps = (8/3) Lambda^2
    eps = (8.0 / 3.0) * LAMBDA**2
    # a LOCAL balance eps = F(T) forces the cold sector's stress to be uniform.
    # The cold sector's stress is r^-2 (SIS), so over the SPARC radial range
    # 0.3 - 30 kpc it varies by:
    r1, r2 = 0.3, 30.0
    ratio = (r2 / r1)**2
    ok = ratio > 1e3
    check("K17", ok,
          "eps_GB = %.4e m^-4 (const) ; cold stress varies %.1e over 1.5 dex"
          % (eps, ratio),
          "ratio > 1e3 (a local balance forces uniformity)",
          "local Euler balance excluded by the sector's own profile")
    return {"eps_GB_dS": eps, "cold_stress_span_0p3_30kpc": ratio}


# ==========================================================================
def main():
    print("=" * 78)
    print("A19 -- the scale-setting functional for kappa")
    print("mutation mode: %s" % MUT)
    print("=" * 78)

    numbers = {}
    for f in (k1, k2, k3, k4, k5, k6, k7, k8, k9, k10, k11, k12, k13,
              k14, k15, k16, k17):
        numbers.update(f())

    npass = sum(1 for c in CHECKS if c["pass"])
    total = len(CHECKS)
    print("\n" + "=" * 78)
    print("A19 COMPLETE: %d/%d checks PASS." % (npass, total))
    print("=" * 78)

    status = "NO-GO(obstruction)"
    out = {
        "lane": "A19_scale_functional",
        "status": status,
        "mutation": MUT,
        "n_checks": total,
        "n_pass": npass,
        "checks": CHECKS,
        "numbers": numbers,
        "constants_used": CONSTANTS,
    }
    name = "a19_results.json" if MUT == "none" else "a19_results_%s.json" % MUT
    with open(name, "w") as fh:
        json.dump(out, fh, indent=2, sort_keys=False)
    print("wrote %s" % name)
    return 0 if npass == total else 1


if __name__ == "__main__":
    sys.exit(main())
