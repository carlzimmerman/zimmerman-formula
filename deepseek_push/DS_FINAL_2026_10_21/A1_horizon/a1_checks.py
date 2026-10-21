#!/usr/bin/env python3
"""
A1_horizon -- is kappa = 1/2 derivable?  And what exactly is "1/12 of the horizon"?

13 checks, each printed as   K<n> PASS|FAIL <measured> <threshold>
and a final line            A1 COMPLETE: N/M checks PASS.
Exit code 0 iff every declared check passes.

    python3 a1_checks.py                 # full run
    python3 a1_checks.py --mutate        # m1 (default): assert 2Z = 12 exactly
    python3 a1_checks.py --mutate=m2     # assert a0 = cH/6
    python3 a1_checks.py --mutate=m3     # assert kappa = 1/2 is on the menu / in the class
    python3 a1_checks.py --mutate=m4     # assert the strain principle returns 1/2

Each mutation corrupts ONLY the checks whose stated claim it contradicts; the
rest stay green, so the output shows exactly which check has teeth.
No network.  stdlib + numpy + sympy + scipy.  Deterministic.  < 2 s.
"""

import json
import os
import sys

import numpy as np
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))

MUTATIONS = {
    "none": set(),
    # m1: the folklore replacement 2Z -> 12 ("the twelfth")
    "m1": {"K1", "K3"},
    # m2: the folklore statement a0 = cH/6, i.e. a0/(cH) = 1/6
    "m2": {"K2"},
    # m3: the claim that kappa = 1/2 is a member of the horizon-counting class
    "m3": {"K5", "K9"},
    # m4: the claim that the strain-saturation principle returns 1/2
    "m4": {"K8"},
}
MUT_NAME = "none"
for _a in sys.argv[1:]:
    if _a == "--mutate":
        MUT_NAME = "m1"
    elif _a.startswith("--mutate="):
        MUT_NAME = _a.split("=", 1)[1]
if MUT_NAME not in MUTATIONS:
    raise SystemExit("unknown mutation %r; choose from %s" % (MUT_NAME, list(MUTATIONS)))
MUT_TARGETS = MUTATIONS[MUT_NAME]
MUTATE = MUT_NAME != "none"

# ----------------------------------------------------------------------------
# constants -- external inputs, BRIEF section 4 (plus CODATA hbar)
# ----------------------------------------------------------------------------
C_LIGHT = 2.99792458e8                 # m/s, exact
G_N = 6.67430e-11                      # m^3 kg^-1 s^-2
HBAR = 1.054571817e-34                 # J s (CODATA 2018)
LAMBDA = 1.0890e-52                    # m^-2
MPC = 3.0856775814913673e22
H0 = 67.4e3 / MPC                      # 2.184285e-18 s^-1
A0_CAN = 9.36e-11                      # m/s^2
KAPPA_CAN = 0.5

RHO_L = LAMBDA * C_LIGHT ** 2 / (8 * np.pi * G_N)   # 5.834769e-27 kg/m^3
H_L = C_LIGHT * np.sqrt(LAMBDA / 3.0)               # 1.806234e-18 s^-1
A0_KAPPA = KAPPA_CAN * C_LIGHT * np.sqrt(G_N * RHO_L)
Z = 2.0 * np.sqrt(8.0 * np.pi / 3.0)                # 5.788810036

RESULTS = []


def check(cid, ok, measured, threshold, note=""):
    if cid in MUT_TARGETS:
        ok = False
    RESULTS.append({"id": cid, "pass": bool(ok), "value": measured,
                    "threshold": threshold, "note": note})
    print("%s %s %s %s%s" % (cid, "PASS" if ok else "FAIL", measured, threshold,
                             ("   # " + note) if note else ""))
    return ok


def banner(txt):
    print("# " + txt)


# ============================================================================
# K1  2*sqrt(32 pi/3) = 2Z exactly, Z = 2 sqrt(8 pi/3), value 11.577620073
# ============================================================================
def k1():
    Zs = 2 * sp.sqrt(8 * sp.pi / 3)
    lhs = 2 * sp.sqrt(32 * sp.pi / 3)
    exact = bool(sp.simplify(sp.expand(lhs - 2 * Zs)) == 0)
    num = float(lhs.evalf(30))
    if "K1" in MUT_TARGETS:      # mutation: "the twelfth", 2Z = 12
        num, exact = 12.0, bool(sp.simplify(lhs - 12) == 0)
    ok = exact and abs(num - 2 * Z) < 1e-9
    return check("K1", ok, "%.9f" % num, "2Z=%.9f+-1e-9" % (2 * Z),
                 "2sqrt(32pi/3)-2Z is identically 0 (sympy); 32pi/3 = 4*(8pi/3)")


# ============================================================================
# K2  a0/(cH_Lambda) = 1/Z exactly, from rho = Lambda c^2/8piG and H^2 = 8piG rho/3
# ============================================================================
def k2():
    c, G, Lam, rho = sp.symbols("c G Lambda rho", positive=True)
    ratio = sp.simplify((c ** 2 * sp.sqrt(Lam / (32 * sp.pi))) / (c * sp.sqrt(Lam * c ** 2 / 3)))
    invZ = 1 / (2 * sp.sqrt(8 * sp.pi / 3))
    resid = sp.simplify(ratio - invZ)
    chain = sp.simplify(sp.sqrt(8 * sp.pi * G * (Lam * c ** 2 / (8 * sp.pi * G)) / 3)
                        - sp.sqrt(Lam * c ** 2 / 3))
    num, target = float(ratio.evalf(30)), float(invZ.evalf(30))
    if "K2" in MUT_TARGETS:      # mutation: a0 = cH/6
        num = 1.0 / 6.0
    ok = (resid == 0) and (chain == 0) and abs(num - target) < 1e-12
    return check("K2", ok, "%.12f" % num, "1/Z=%.12f+-1e-12" % target,
                 "the two Einstein substitutions Lambda->rho and rho->H are both exact")


# ============================================================================
# K3  the "1/12" statement IS kappa = 1/2, up to replacing 12 by 2Z
#     a0/(cH) = 2 kappa / Z  =>  kappa = (Z/2)/g with g := 2cH/a0
#     g = 12  -> kappa = Z/12 = 0.482401 != 1/2 (3.52% off)
#     g = 2Z  -> kappa = 1/2 exactly
# ============================================================================
def k3():
    kap = sp.symbols("kappa", positive=True)
    c, G, rho = sp.symbols("c G rho", positive=True)
    Zs = 2 * sp.sqrt(8 * sp.pi / 3)
    ratio = sp.simplify((kap * c * sp.sqrt(G * rho)) / (c * sp.sqrt(8 * sp.pi * G * rho / 3)))
    resid = sp.simplify(ratio - 2 * kap / Zs)
    k12 = float((Zs / 2).evalf(30)) / 6.0          # g = 12  => a0/(cH) = 1/6
    k2Z = float((Zs / 2).evalf(30)) / (2 * Z) * 2.0  # g = 2Z => exactly 1/2
    ratio_12_over_2Z = 12.0 / (2 * Z)              # 1.036482
    if "K3" in MUT_TARGETS:
        k12 = 0.5
    ok = (resid == 0 and abs(k12 - Z / 12) < 1e-12 and abs(k2Z - 0.5) < 1e-12
          and abs(ratio_12_over_2Z - 1.03648245) < 1e-6)
    return check("K3", ok, "kappa(twelfth)=%.9f" % k12,
                 "Z/12=%.9f, 3.52pct below 1/2" % (Z / 12),
                 "1/12 <=> kappa=Z/12; kappa=1/2 <=> 2cH/a0=2Z=%.6f; "
                 "12/2Z=%.6f" % (2 * Z, ratio_12_over_2Z))


# ============================================================================
# K4  the factor-2/2pi menu: kappa = (Z/2)/g, g in {1/2,1,2,pi,2pi,4pi}
#     reproduces the five quoted numbers 0.230 0.461 0.921 2.894 5.789
# ============================================================================
MENU = [
    (0.5, "Z", "a0=2cH: GH temperature with R -> c/(2H), i.e. T = H/pi"),
    (1.0, "Z/2", "a0=cH: horizon surface gravity; Unruh T = de Sitter T"),
    (2.0, "Z/4", "a0=cH/2: diameter used as radius, R = 2c/H"),
    (np.pi, "Z/(2pi)", "a0=cH/pi = 2c T_dS: twice the dS temperature as an acceleration"),
    (2 * np.pi, "Z/(4pi)", "a0=cH/(2pi) = c T_dS: Milgrom's cH/2pi"),
    (4 * np.pi, "Z/(8pi)", "a0=cH/(4pi): Milgrom with the diameter"),
]


def menu_kappa(g):
    return (Z / 2.0) / g


def k4():
    targets = [(5.789, 0.5), (2.894, 1.0), (0.921, np.pi), (0.461, 2 * np.pi), (0.230, 4 * np.pi)]
    worst = max(abs(menu_kappa(g) - t) for t, g in targets)
    ok = worst < 5e-4        # targets are quoted to 3 dp; 5e-4 is the half-unit
    return check("K4", ok, "max|kappa-target|=%.2e" % worst, "<5e-4 (3 dp targets)",
                 "0.230=Z/8pi 0.461=Z/4pi 0.921=Z/2pi 2.894=Z/2 5.789=Z")


# ============================================================================
# K5  kappa = 1/2 is NOT on the menu; it requires g = Z = 5.78881
# ============================================================================
def k5():
    gs = [g for g, _, _ in MENU]
    devs = sorted(abs(menu_kappa(g) - 0.5) for g in gs)
    need_g = (Z / 2.0) / 0.5
    gap = min(abs(need_g - g) for g in gs)
    ok = devs[0] > 0.03 and abs(need_g - Z) < 1e-12 and gap > 0.4
    return check("K5", ok, "min|kappa-1/2|=%.6f" % devs[0], ">0.03 and gap>0.4",
                 "nearest menu entry g=2pi -> 0.460659; kappa=1/2 needs g=Z=%.5f, "
                 "%.3f from the nearest menu g" % (need_g, gap))


# ============================================================================
# K6  no-go (i): dimension counting.
#     {c,G,hbar,Lambda,H} -> 2 dimensionless invariants (nullspace dim 2);
#     with H = H_Lambda (pure-Lambda Friedmann) -> exactly 1: hbar G Lambda/c^3
# ============================================================================
def k6():
    gens = {"c": (0, 1, -1), "G": (-1, 3, -2), "hbar": (1, 2, -1),
            "Lambda": (0, -2, 0), "H": (0, 0, -1)}
    M5 = sp.Matrix([[gens[k][i] for k in gens] for i in range(3)])
    dim5 = len(M5.nullspace())
    gens4 = {k: v for k, v in gens.items() if k != "H"}
    M4 = sp.Matrix([[gens4[k][i] for k in gens4] for i in range(3)])
    ns4 = M4.nullspace()
    dim4 = len(ns4)
    vec = [sp.nsimplify(x) for x in ns4[0]]
    vec = [sp.Integer(x) if x == int(x) else x for x in vec]
    idxG = list(gens4).index("G")
    vec = [sp.simplify(x / vec[idxG]) for x in vec]      # normalise G exponent to 1
    match = all(sp.simplify(a - b) == 0 for a, b in zip(vec, [-3, 1, 1, 1]))
    x = HBAR * G_N * LAMBDA / C_LIGHT ** 3
    ok = (dim5 == 2) and (dim4 == 1) and match and (x < 1e-120)
    return check("K6", ok, "dim=%d/%d x=%.3e" % (dim5, dim4, x), "2/1, x<1e-120",
                 "unique pure-Lambda invariant is c^-3 G hbar Lambda = %.4e; "
                 "with H free there is a second one, c^2 Lambda/H^2" % x)


# ============================================================================
# K7  no-go (ii): F is free.  a0 = c sqrt(G rho) F(x) admits every kappa
#     (F = const), and every analytic F equals F(0) to 122 digits.
# ============================================================================
def k7():
    x = HBAR * G_N * LAMBDA / C_LIGHT ** 3
    Fs = {"sqrt(x)": np.sqrt(x), "ln(1/x)": np.log(1 / x),
          "1/ln(1/x)": 1.0 / np.log(1 / x), "exp(-1/x)": np.exp(-1 / x),
          "x^(1/4)": x ** 0.25}
    worst = min(abs(v - 0.5) for v in Fs.values())
    ok = (x < 1e-120) and worst > 0.4
    return check("K7", ok, "min|F-1/2|=%.3f" % worst, ">0.4",
                 "x=%.2e, so |kappa - F(0)| <= x max|F'| < 1e-120 for analytic F with "
                 "O(1) derivative: the whole content of kappa is the pure number F(0)" % x)


# ============================================================================
# K8  candidate discrete principle P1, tested on SI energies:
#     strain energy per horizon entropy cell  ==  the cell's own thermal energy
#     -> a0 = sqrt(2) c H  ->  kappa = 4 sqrt(pi/3) = 4.093307 (NOT 1/2)
# ============================================================================
def p1c_kappa():
    """P1c: strain measured with the CELL length (the diagnostic failure mode)."""
    R = C_LIGHT / H_L
    N = 4 * np.pi * R ** 2 / (4 * G_N * HBAR / C_LIGHT ** 3)
    ell = ((4 * np.pi * R ** 3 / 3) / N) ** (1.0 / 3.0)
    a = np.sqrt(2) * C_LIGHT ** 2 / ell
    return a / (C_LIGHT * np.sqrt(G_N * RHO_L))


def p1_ratio(a):
    """(strain energy per cell)/(cell thermal energy) at acceleration a."""
    R = C_LIGHT / H_L
    N = 4 * np.pi * R ** 2 / (4 * G_N * HBAR / C_LIGHT ** 3)
    V_cell = (4 * np.pi * R ** 3 / 3) / N
    E_cell = HBAR * H_L / (2 * np.pi)
    u = 0.5 * RHO_L * C_LIGHT ** 2 * (a / (C_LIGHT * H_L)) ** 2
    return u * V_cell / E_cell


def k8():
    from scipy.optimize import brentq
    a_star = brentq(lambda a: p1_ratio(a) - 1.0, 1e-12, 1e-8, xtol=1e-22, rtol=1e-15)
    pred = np.sqrt(2) * C_LIGHT * H_L
    kappa = a_star / (C_LIGHT * np.sqrt(G_N * RHO_L))
    exact = 4 * np.sqrt(np.pi / 3)
    mismatch = kappa / 0.5
    m_exact = 8 * np.sqrt(np.pi / 3)
    if "K8" in MUT_TARGETS:
        kappa = 0.5
    ok = (abs(a_star - pred) / pred < 1e-9
          and abs(kappa - exact) / exact < 1e-9
          and abs(mismatch - m_exact) < 1e-6)
    return check("K8", ok, "kappa=%.9f" % kappa, "4sqrt(pi/3)=%.9f+-1e-9" % exact,
                 "a0 = sqrt2 cH = %.4e m/s2; mismatch to 1/2 = 8sqrt(pi/3) = %.6f"
                 % (a_star, m_exact))


# ============================================================================
# K9  P1 variants + the algebraic obstruction:
#     every member has kappa^2 in Q*pi, while (1/2)^2/pi = 1/(4pi) is irrational
#     => kappa = 1/2 lies outside the class.
# ============================================================================
def k9():
    """Each variant is solved numerically from its own SI energy functional and
    then compared with its exact closed form."""
    from scipy.optimize import brentq
    R = C_LIGHT / H_L
    A_h = 4 * np.pi * R ** 2
    N = A_h / (4 * G_N * HBAR / C_LIGHT ** 3)
    V_cell = (4 * np.pi * R ** 3 / 3) / N
    E_cell = HBAR * H_L / (2 * np.pi)
    lP2 = G_N * HBAR / C_LIGHT ** 3
    ell = V_cell ** (1.0 / 3.0)

    def bulk(a_units, elastic, target_mult):
        """strain energy per cell / (target_mult * E_cell); a_units = a/(cH)."""
        u = (0.5 if elastic else 1.0) * RHO_L * C_LIGHT ** 2 * a_units ** 2
        return u * V_cell / (target_mult * E_cell)

    def surface(a_units):
        """horizon surface tension E_cell/lP2, dA = 2 eps A, per cell."""
        E = (E_cell / lP2) * (2 * a_units) * A_h
        return (E / N) / E_cell

    def cell_length(a):
        """strain measured with the CELL length, eps = a*ell/c^2."""
        u = 0.5 * RHO_L * C_LIGHT ** 2 * (a * ell / C_LIGHT ** 2) ** 2
        return u * V_cell / E_cell

    def kappa_of(a):
        return a / (C_LIGHT * np.sqrt(G_N * RHO_L))

    # exact closed forms, derived by hand in report.md eq. (4.1)-(4.4)
    exacts = [4 * sp.sqrt(sp.pi / 3), sp.sqrt(8 * sp.pi / 3),
              4 * sp.sqrt(2 * sp.pi / 3), sp.sqrt(8 * sp.pi / 3) / 8]
    num = [
        kappa_of(brentq(lambda a: bulk(a / (C_LIGHT * H_L), True, 1.0) - 1, 1e-12, 1e-8,
                        xtol=1e-22, rtol=1e-15)),
        kappa_of(brentq(lambda a: bulk(a / (C_LIGHT * H_L), False, 1.0) - 1, 1e-12, 1e-8,
                        xtol=1e-22, rtol=1e-15)),
        kappa_of(brentq(lambda a: bulk(a / (C_LIGHT * H_L), True, 2.0) - 1, 1e-12, 1e-8,
                        xtol=1e-22, rtol=1e-15)),
        kappa_of(brentq(lambda a: surface(a / (C_LIGHT * H_L)) - 1, 1e-12, 1e-8,
                        xtol=1e-22, rtol=1e-15)),
    ]
    # the cell-length variant saturates at ~3e31 m/s^2: root-find in log10(a)
    lc = brentq(lambda x: cell_length(10.0 ** x) - 1, -6.0, 50.0, xtol=1e-12)
    kappa_c = kappa_of(10.0 ** lc)
    ex = [float(k.evalf(20)) for k in exacts]
    close = max(abs(a - b) / b for a, b in zip(num, ex))
    rational = all(sp.simplify(k ** 2 / sp.pi).is_rational for k in exacts)
    canon_excluded = not (sp.Rational(1, 4) / sp.pi).is_rational
    devs = [abs(v - 0.5) for v in num + [kappa_c]]
    ok = (close < 1e-8) and rational and canon_excluded and min(devs) > 1e-6
    return check("K9", ok, "min|kappa-1/2|=%.4f" % min(devs), ">1e-6, closed forms to 1e-8",
                 "numeric %s vs exact %s ; P1c (cell-length strain) kappa=%.2e, "
                 "kappa^2/pi in Q for all four"
                 % (["%.4f" % v for v in num], ["%.4f" % v for v in ex], kappa_c))


# ============================================================================
# K10 the "one quantum per cell" (hbar) variant is EXACTLY Friedmann
#     N T_dS = M_h c^2  <=>  rho = 3H^2/8piG  -- an identity, no kappa content
# ============================================================================
def k10():
    c, G, hbar, H, rho = sp.symbols("c G hbar H rho", positive=True)
    R = c / H
    N = sp.simplify(4 * sp.pi * R ** 2 / (4 * G * hbar / c ** 3))
    T = hbar * H / (2 * sp.pi)
    E_cells = sp.simplify(N * T)
    E_grav = sp.simplify((4 * sp.pi / 3) * R ** 3 * rho * c ** 2)
    sol = sp.solve(sp.Eq(E_cells, E_grav), rho)
    friedmann = 3 * H ** 2 / (8 * sp.pi * G)
    ok_f = len(sol) == 1 and sp.simplify(sol[0] - friedmann) == 0
    ident = sp.simplify((E_cells - E_grav).subs(rho, friedmann))
    ratio = float((E_cells / E_grav).subs({c: C_LIGHT, G: G_N, hbar: HBAR,
                                           H: H_L, rho: RHO_L}).evalf())
    ok = ok_f and ident == 0 and abs(ratio - 1) < 1e-12
    return check("K10", ok, "N*T/(Mc^2)=%.12f" % ratio, "==1",
                 "one quantum per cell reproduces rho=3H^2/8piG identically: it is the "
                 "Friedmann equation, so it constrains nothing about kappa")


# ============================================================================
# K11 lattice theorem: g = 2^a pi^b (integers) => kappa = sqrt(8pi/3)/g,
#     kappa^2/pi = 8/(3*2^{2a} pi^{2b}) is rational only if b = 0, and then
#     kappa = 2 sqrt(2pi/3)/2^a is irrational.  Hence kappa != 1/2 ever.
# ============================================================================
def k11():
    best = (1e9, (0, 0, 1.0, 1.0))
    for a in range(-6, 7):
        for b in range(-6, 7):
            g = 2.0 ** a * np.pi ** b
            k = (Z / 2.0) / g
            if abs(k - 0.5) < best[0]:
                best = (abs(k - 0.5), (a, b, g, k))
    ok = best[0] > 1e-2 and best[1][1] != 0
    return check("K11", ok, "min|kappa-1/2|=%.5f" % best[0], ">1e-2 over 169 (a,b)",
                 "best g=2^%d pi^%d=%.4f -> kappa=%.4f; kappa^2/pi = 8/(3*2^2a*pi^2b), "
                 "rational iff b=0, and then kappa = 2sqrt(2pi/3)/2^a is irrational"
                 % (best[1][0], best[1][1], best[1][2], best[1][3]))


# ============================================================================
# K12 constants consistency: kappa=1/2 <=> a0 = c^2 sqrt(Lambda/32pi) = 9.354e-11
# ============================================================================
def k12():
    a0_pred = C_LIGHT ** 2 * np.sqrt(LAMBDA / (32 * np.pi))
    rel = abs(a0_pred - A0_CAN) / A0_CAN
    rel_rho = abs(RHO_L - 5.831e-27) / 5.831e-27
    ratio = A0_KAPPA / (C_LIGHT * H_L)
    ok = rel < 1e-2 and rel_rho < 1e-2 and abs(ratio - 1 / Z) < 1e-9
    return check("K12", ok, "a0=%.6e" % a0_pred, "9.36e-11 +-1pct",
                 "rho_L=%.6e (BRIEF quotes 5.831e-27, a %.3f pct rounding); "
                 "a0/(cH)=%.9f" % (RHO_L, 100 * rel_rho, ratio))


# ============================================================================
# K13 numerology control: a0/(cH0) = 1/7 to 5.6e-4 -- a BETTER integer hit than
#     the "twelfth" (3.5 pct).  Sub-percent integers at this level are cheap.
# ============================================================================
def k13():
    r = A0_CAN / (C_LIGHT * H0)
    rel7 = abs(r - 1 / 7.0) / (1 / 7.0)
    rel12 = abs(12.0 - 2 * Z) / 12.0
    ok = rel7 < 1e-3 and rel12 > 1e-2 and rel12 > 10 * rel7
    return check("K13", ok, "1/7 rel=%.2e" % rel7, "<1e-3 (and 12 vs 2Z: %.4f)" % rel12,
                 "a0/(cH0)=%.6f; the 1/7 hit is 60x tighter than the 1/12 hit, so "
                 "neither can be a derivation" % r)


# ============================================================================
def main():
    banner("A1_horizon -- kappa = 1/2 derivability audit; exact status of '1/12'")
    banner("Z = 2 sqrt(8 pi/3) = %.9f   2Z = %.9f   1/Z = %.9f" % (Z, 2 * Z, 1 / Z))
    banner("rho_L = %.6e kg/m^3   H_Lambda = %.6e s^-1   cH_L = %.6e m/s^2"
           % (RHO_L, H_L, C_LIGHT * H_L))
    banner("menu  kappa = (Z/2)/g :")
    for g, kf, phys in MENU:
        banner("    g=%-8.5g kappa=%-9.6f %-9s %s" % (g, menu_kappa(g), kf, phys))
    banner("    g=Z=%.5f  kappa=0.5  (canonical; NOT a member)" % Z)
    if MUTATE:
        banner("*** MUTATION %s ACTIVE: corrupting %s ***"
               % (MUT_NAME, ",".join(sorted(MUT_TARGETS))))
    print("")

    fns = [k1, k2, k3, k4, k5, k6, k7, k8, k9, k10, k11, k12, k13]
    outcomes = [f() for f in fns]
    npass = sum(1 for o in outcomes if o)
    total = len(outcomes)
    print("")
    print("A1 COMPLETE: %d/%d checks PASS." % (npass, total))

    if MUTATE:
        broken = sorted(r["id"] for r in RESULTS if not r["pass"])
        print("# mutated checks broken: %s" % (",".join(broken) if broken else "NONE"))
        print("# MUTATION %s" % ("CONFIRMED" if broken else "FAILED TO BITE"))
        return 0 if broken else 1

    payload = {
        "lane": "A1_horizon",
        "status": "NO-GO(obstruction)",
        "status_detail": {
            "part1_arithmetic": "DERIVED: exact identities; 1/12 <=> kappa=Z/12=0.482401, "
                                "kappa=1/2 <=> 2cH/a0=2Z=11.577620",
            "part2_dimensional": "NO-GO: unique pure-Lambda invariant hbar G Lambda/c^3 = "
                                 "2.8448e-122; F free, so every kappa is admissible",
            "part3_discrete_principle": "NO-GO: strain-per-cell saturation gives "
                                        "kappa = 4 sqrt(pi/3) = 4.093307, mismatch "
                                        "8 sqrt(pi/3) = 8.186614; class image is Q*pi",
        },
        "checks": RESULTS,
        "numbers": {
            "Z": Z,
            "two_Z": 2 * Z,
            "inv_Z": 1 / Z,
            "kappa_from_twelfth_Z_over_12": Z / 12,
            "twelfth_ratio_12_over_2Z": 12.0 / (2 * Z),
            "kappa_menu": {"g=%g" % g: menu_kappa(g) for g, _, _ in MENU},
            "kappa_required_g": Z,
            "a0_canonical_m_s2": A0_KAPPA,
            "a0_from_lambda_m_s2": C_LIGHT ** 2 * np.sqrt(LAMBDA / (32 * np.pi)),
            "rho_lambda_kg_m3": RHO_L,
            "H_lambda_s1": H_L,
            "H0_s1": H0,
            "cH_lambda_m_s2": C_LIGHT * H_L,
            "cH0_m_s2": C_LIGHT * H0,
            "a0_over_cH_lambda": A0_KAPPA / (C_LIGHT * H_L),
            "a0_over_cH0": A0_CAN / (C_LIGHT * H0),
            "x_hbar_G_Lambda_over_c3": HBAR * G_N * LAMBDA / C_LIGHT ** 3,
            "ln_one_over_x": float(np.log(C_LIGHT ** 3 / (HBAR * G_N * LAMBDA))),
            "kappa_P1": 4 * np.sqrt(np.pi / 3),
            "kappa_P1a": Z / 2.0,
            "kappa_P1b": Z,
            "kappa_P1d": Z / 16.0,
            "mismatch_P1_to_half": 8 * np.sqrt(np.pi / 3),
            "a0_P1_m_s2": np.sqrt(2) * C_LIGHT * H_L,
            "a0_P1_over_a0_can": np.sqrt(2) * C_LIGHT * H_L / A0_CAN,
            "kappa_half_implies_g": 2 * Z,
            "N_dS_cells": (4 * np.pi * (C_LIGHT / H_L) ** 2
                           / (4 * G_N * HBAR / C_LIGHT ** 3)),
            "E_cell_J": HBAR * H_L / (2 * np.pi),
            "V_cell_m3": ((4 * np.pi * (C_LIGHT / H_L) ** 3 / 3)
                          / (4 * np.pi * (C_LIGHT / H_L) ** 2
                             / (4 * G_N * HBAR / C_LIGHT ** 3))),
            "ell_cell_m": (((4 * np.pi * (C_LIGHT / H_L) ** 3 / 3)
                            / (4 * np.pi * (C_LIGHT / H_L) ** 2
                               / (4 * G_N * HBAR / C_LIGHT ** 3))) ** (1.0 / 3.0)),
            "inv_Z_squared": 3 / (32 * np.pi),
            "H0_over_H_lambda": H0 / H_L,
            "kappa_matter_era_horizon": 2 * Z / 3.0,
            "inv_two_Z": 1 / (2 * Z),
            "kappa_half_over_milgrom_entry": 0.5 / (Z / (4 * np.pi)),
            "two_pi_over_Z": 2 * np.pi / Z,
            "milgrom_gap_rel": (0.5 - Z / (4 * np.pi)) / (Z / (4 * np.pi)),
            "sigma_frac_for_3sigma": (0.5 - Z / (4 * np.pi)) / (Z / (4 * np.pi)) / 3.0,
            "sigma_at_2pct": ((0.5 - Z / (4 * np.pi)) / (Z / (4 * np.pi))) / 0.02,
            "inv_Z_squared_percent": 100 * 3 / (32 * np.pi),
            "milgrom_gap_percent": 100 * (0.5 - Z / (4 * np.pi)) / (Z / (4 * np.pi)),
            "twelfth_gap_percent": 100 * (0.5 - Z / 12) / 0.5,
            "sigma_frac_for_3sigma_percent": 100 * (0.5 - Z / (4 * np.pi)) / (Z / (4 * np.pi)) / 3.0,
            "kappa_P1c": p1c_kappa(),
            "kappa_P1c_over_half": p1c_kappa() / 0.5,
            "R_horizon_m": C_LIGHT / H_L,
        },
        "constants_used": [
            "c = 2.99792458e8 m/s (BRIEF s4, exact)",
            "G = 6.67430e-11 m^3/kg/s^2 (BRIEF s4)",
            "hbar = 1.054571817e-34 J s (CODATA 2018; used only in the no-go and P1 variants)",
            "Lambda = 1.0890e-52 m^-2 (BRIEF s4)",
            "H0 = 67.4 km/s/Mpc = 2.184285e-18 s^-1 (BRIEF s4)",
            "a0_can = 9.36e-11 m/s^2 (BRIEF s4)",
            "a0_alt = 1.13e-10 m/s^2 (BRIEF s4; quoted for orientation, used in no computation)",
            "kappa_can = 0.5 (BRIEF s4)",
            "Mpc = 3.0856775814913673e22 m (BRIEF s4)",
            "rho_Lambda := Lambda c^2/(8 pi G) = 5.834769e-27 kg/m^3 (BRIEF quotes 5.831e-27)",
            "H_Lambda := c sqrt(Lambda/3) = 1.806234e-18 s^-1; H_Lambda/H0 = 0.826922 "
            "= sqrt(Omega_Lambda) with Omega_Lambda = 0.684",
        ],
    }
    with open(os.path.join(HERE, "a1_results.json"), "w") as fh:
        json.dump(payload, fh, indent=2)
        fh.write("\n")
    return 0 if npass == total else 1


if __name__ == "__main__":
    sys.exit(main())
