#!/usr/bin/env python3
"""
A72_coefficient -- THE COEFFICIENT a0/(cH): IS IT 1/7 OR 1/(2*pi)?
==================================================================
The theory fixes a0 = kappa c sqrt(G rho_Lambda), K = 4 pi G, c = 1.  At the
canonical kappa = 1/2 this is a0 = c^2 sqrt(Lambda/32pi) = cH_Lambda/Z.
Two closed forms are on the table for the pure number a0/(cH):

   1/7    = 0.142857...   (x cH0, the observed Hubble rate; exact iff
                           Omega_Lambda = 32 pi/147 = 0.683884)
   1/(2pi)= 0.159155...   (the thermal-wavelength / quantum-carrier value)

WHAT THIS SCRIPT DOES
  Part 1: census of seven structural routes to a coefficient of order 0.1,
          each evaluated to 6+ digits and labelled DERIVATION / MATCH.
  Part 2: an independent look-elsewhere pool of 9,217,780 closed forms
          (up to 3 binary operations from {+,-,*,/,^} over the eleven atoms
          {1,2,3,4,5,7,8,pi,e,sqrt2,sqrt3}; 582,481 distinct values in the
          coefficient band), with hit counts, Monte-Carlo P(at least one hit),
          and the number of hits that any stated physical premise produces.
  Part 3: the sigma at which a future measurement separates the candidates,
          including A71's wide-binary forecast and SPARC at N = 1000.
  Part 4: the verdict, carried by the numbers.

21 checks, each printed as   C<n> PASS|FAIL <measured> <threshold>
and a final line             A72 COMPLETE: N/M checks PASS.
Exit code 0 iff every declared check passes.

    python3 a72_checks.py                        # full run
    A72_MUTATE=kappa_one python3 a72_checks.py   # one mutation (or --mutate=kappa_one)
    python3 a72_checks.py --list-mutations

Deterministic, no network, stdlib + numpy + scipy + sympy, < 60 s.
Every mutation changes ONE input; see MUTATE.md for the kill matrix.
"""

import json
import math
import os
import sys

import numpy as np
import sympy as sp
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))

# ===========================================================================
# constants -- BRIEF section 4, plus the measured numbers of A71 / A51
# ===========================================================================
C_LIGHT = 2.99792458e8
G_N = 6.67430e-11
HBAR = 1.054571817e-34          # CODATA 2018
K_B = 1.380649e-23              # SI exact
LAMBDA = 1.0890e-52             # m^-2  (BRIEF s4)
MPC = 3.0856775814913673e22
H0 = 67.4e3 / MPC               # 2.184285e-18 s^-1

A0_CAN = 9.36e-11               # BRIEF s4, 3 s.f.
A0_MEAS = 8.544e-11             # A71 joint fit
SIG_A0 = 2.73e-11               # A71 joint fit (31.9% coherent floor included)
KAPPA_P3_MEAS = 0.37765         # A71, rho_crit convention
SIG_P3_STAT = 0.02579           # A71
SIG_P3_TOT = 0.12069            # A71 (31.2% floor included)
KAPPA_DE_MEAS = 0.4564          # A71, rho_DE convention
SIG_DE_STAT = 0.0312            # A71, statistical
OMEGA_L_PLANCK = 0.6847         # Planck 2018 (external input, as in A71)
SIG_OMEGA_L_PLANCK = 0.0073

H_L = C_LIGHT * math.sqrt(LAMBDA / 3.0)
RHO_L = LAMBDA * C_LIGHT ** 2 / (8 * math.pi * G_N)
OMEGA_L = (H_L / H0) ** 2
CH_L = C_LIGHT * H_L
CH_0 = C_LIGHT * H0
Z = 2 * math.sqrt(8 * math.pi / 3)          # 5.788810036
INV_Z = 1.0 / Z                              # 0.172747075
TWO_PI = 2 * math.pi
A0_TH = C_LIGHT ** 2 * math.sqrt(LAMBDA / (32 * math.pi))   # kappa = 1/2

# A71's forecast precisions in kappa (P3 convention)
SIG_FORECAST = {
    "current joint (A71)": SIG_P3_TOT,
    "wide binary, full DR4 catalogue": 0.040,
    "wide binary + joint": 0.0605,
    "SPARC at N = 1000": 0.118,
}
N_PAIRS_REF = 30000.0        # A71's DR4 catalogue, for the N ~ sigma^-2 scaling

# ===========================================================================
# mutations -- each changes exactly ONE input
# ===========================================================================
MUTATIONS = {
    "kappa_one":       {"kappa": 1.0},          # the theory's kappa 1/2 -> 1
    "omega_quarter":   {"omega_l": 0.25},       # Omega_Lambda -> 1/4
    "hubble_for_ds":   {"h_ds": "__H0__"},      # de Sitter temperature uses H0
    "thin_pool":       {"pool_ops": 2},         # pool truncated to <= 2 ops
    "sigma_small":     {"sigma_a0": 1e-12},     # the a0 error -> 1e-12
    "two_pi_is_Z":     {"two_pi_thermal": "__Z__"},   # 2pi -> Z in lambda_T
    "route_1_7":       {"extra_route": "__SEVEN__"},  # a route that "gives" 1/7
    "omega_rational":  {"omega_solution": 41.0 / 60.0},
    "unruh_no2pi":     {"unruh_2pi": 1.0},      # drop the 2pi of T_Unruh
    "komar_one":       {"komar": 1.0},          # N_bulk = E/kT, not 2E/kT
    "wb_better":       {"sig_wb": 0.008},       # a wide-binary forecast 5x better
    "de_naive":        {"de_sqrt": False},      # kappa_DE = kappa_P3/Omega_L
}

MUT_NAME = "none"
_args = list(sys.argv[1:])
for _a in _args:
    if _a == "--mutate":
        MUT_NAME = "kappa_one"
    elif _a.startswith("--mutate="):
        MUT_NAME = _a.split("=", 1)[1]
    elif _a == "--list-mutations":
        print("\n".join(sorted(MUTATIONS)))
        raise SystemExit(0)
# the environment form:  A72_MUTATE=kappa_one python3 a72_checks.py
if os.environ.get("A72_MUTATE"):
    MUT_NAME = os.environ["A72_MUTATE"].strip()
if MUT_NAME != "none" and MUT_NAME not in MUTATIONS:
    raise SystemExit("unknown mutation %r; choose from %s"
                     % (MUT_NAME, sorted(MUTATIONS)))
MUT = MUT_NAME
MUTATE = MUT != "none"

# ---------------------------------------------------------------------------
# the live parameter set: defaults, then the one mutated input
# ---------------------------------------------------------------------------
PARAMS = {
    "kappa": 0.5,
    "omega_l": OMEGA_L,
    "h_ds": H_L,
    "two_pi_thermal": TWO_PI,
    "unruh_2pi": TWO_PI,
    "sigma_a0": SIG_A0,
    "pool_ops": 5,                 # number of binary operations in the pool
    "omega_solution": None,
    "extra_route": None,
    "komar": 2.0,
    "sig_wb": 0.040,
    "de_sqrt": True,
}
if MUTATE:
    for _k, _v in MUTATIONS[MUT].items():
        if _v == "__H0__":
            _v = H0
        elif _v == "__Z__":
            _v = Z
        elif _v == "__SEVEN__":
            _v = CH_0 / 7.0
        PARAMS[_k] = _v

KAPPA = PARAMS["kappa"]
OM_L = PARAMS["omega_l"]
H_DS = PARAMS["h_ds"]
TP_TH = PARAMS["two_pi_thermal"]
UNRUH_2PI = PARAMS["unruh_2pi"]
SIG_A0_LIVE = PARAMS["sigma_a0"]
KOMAR = PARAMS["komar"]
SIG_WB = PARAMS["sig_wb"]

RESULTS = []


def check(cid, ok, value, threshold, note=""):
    RESULTS.append({"id": cid, "pass": bool(ok), "value": value,
                    "threshold": threshold, "note": note})
    print("%-4s %-4s %-64s %-30s %s"
          % (cid, "PASS" if ok else "FAIL", value, threshold, note))
    return bool(ok)


def banner(txt):
    print(txt)


def relerr(a, b):
    return abs(a - b) / abs(b) if b != 0 else float("inf")


# ===========================================================================
# C1 -- the exact ratio law a0/(cH_L) = 2 kappa / Z, checked in SI
# ===========================================================================
def c1():
    a0_si = KAPPA * C_LIGHT * math.sqrt(G_N * RHO_L)
    route_a = a0_si / CH_L                       # SI, from the BRIEF constants
    kap, c, G, rho = sp.symbols("kappa c G rho", positive=True)
    Zs = 2 * sp.sqrt(8 * sp.pi / 3)
    resid = sp.simplify((kap * c * sp.sqrt(G * rho))
                        / (c * sp.sqrt(8 * sp.pi * G * rho / 3))
                        - 2 * kap / Zs)
    # the published value at kappa = 1/2, from the algebra alone
    route_b = float(2 * sp.Rational(1, 2) / Zs)
    ok = (resid == 0) and relerr(route_a, route_b) < 1e-12
    return check("C1", ok, "a0/cHL=%.9f vs 1/Z=%.9f; resid=%s"
                 % (route_a, route_b, resid),
                 "residual 0; rel < 1e-12",
                 "kappa=1/2 <=> a0/(cH_Lambda)=1/Z=0.172747 (A62 K3 reproduced)")


# ===========================================================================
# C2 -- a0/(cH0) = kappa sqrt(3 Omega_L/8pi); equals 1/7 to 6.1e-5
# ===========================================================================
def c2():
    a0_si = KAPPA * C_LIGHT * math.sqrt(G_N * RHO_L)
    route_a = a0_si / CH_0
    route_b = KAPPA * math.sqrt(3.0 * OM_L / (8.0 * math.pi))
    one_seventh = 1.0 / 7.0
    ok = (relerr(route_a, route_b) < 1e-9
          and relerr(route_a, one_seventh) < 1e-3)
    return check("C2", ok, "a0/cH0=%.9f vs k sqrt(3Om/8pi)=%.9f; vs 1/7 rel=%.2e"
                 % (route_a, route_b, relerr(route_a, one_seventh)),
                 "1e-9 to the identity, <1e-3 to 1/7",
                 "a0/(cH0) is NOT a pure number: it carries sqrt(Omega_Lambda)")


# ===========================================================================
# C3 -- 1/7 exactly <=> Omega_Lambda = 32 pi / 147 (exact solve vs root find)
# ===========================================================================
def c3():
    k = sp.Rational(1, 2)
    x = sp.symbols("x", positive=True)
    sol = sp.solve(sp.Eq(k * sp.sqrt(3 * x / (8 * sp.pi)), sp.Rational(1, 7)), x)
    exact = sol[0] if len(sol) == 1 else sp.nan
    if PARAMS["omega_solution"] is not None:
        exact = sp.Rational(PARAMS["omega_solution"]).limit_denominator(10 ** 6)
    f = lambda om: 0.5 * math.sqrt(3.0 * om / (8.0 * math.pi)) - 1.0 / 7.0
    num = brentq(f, 0.30, 0.95) if f(0.30) * f(0.95) < 0 else float("nan")
    ok = (relerr(float(exact), num) < 1e-9
          and relerr(float(exact), 32 * math.pi / 147.0) < 1e-15)
    return check("C3", ok, "Omega*=%.9f (exact) vs %.9f (brentq); 32pi/147=%.9f"
                 % (float(exact), num, 32 * math.pi / 147.0),
                 "relerr < 1e-9; exact = 32pi/147",
                 "the 1/7 is a statement about Omega_Lambda, not about a0")


# ===========================================================================
# C4 -- the theory's coefficient 1/Z and the thermal 1/(2pi) are NOT equal
# ===========================================================================
def c4():
    route_theory = INV_Z
    route_thermal = 1.0 / TP_TH
    diff = abs(route_theory - route_thermal) / route_thermal
    ok = diff > 0.05
    return check("C4", ok, "1/Z=%.9f vs 1/(2pi)=%.9f; rel diff=%.6f"
                 % (route_theory, route_thermal, diff),
                 "rel diff > 0.05",
                 "kappa=1/2 is 8.55% above the thermal value in the cH_L frame")


# ===========================================================================
# C5 -- a quantum carrier saturates at exactly cH/(2pi), mass-independent
# ===========================================================================
def c5():
    hbar, c, m, H, kB = sp.symbols("hbar c m H k_B", positive=True)
    T = hbar * H / (2 * sp.pi * kB)
    ell = hbar / (m * c)
    a_sat = sp.simplify(kB * T / (m * ell))
    resid = sp.simplify(a_sat - c * H / (2 * sp.pi))
    m1, m2 = 1e-30, 1e-20
    def a_num(mm):
        Tm = HBAR * H_DS / (TWO_PI * K_B)
        lm = HBAR / (mm * C_LIGHT)
        return K_B * Tm / (mm * lm)
    a1, a2 = a_num(m1), a_num(m2)
    target = CH_L / TWO_PI
    ok = (resid == 0 and relerr(a1, a2) < 1e-12
          and relerr(a1, target) < 1e-9)
    return check("C5", ok, "a_sat=%.6e (m=1e-30) = %.6e (m=1e-20); target %.6e"
                 % (a1, a2, target),
                 "resid 0; mass-indep <1e-12; =cH_L/2pi",
                 "the coefficient 1/(2pi) IS derived, with no free parameter, "
                 "from a quantum carrier at T_dS (A62 K14)")


# ===========================================================================
# C6 -- Unruh temperature matching: a = 2 pi c k_B T_dS / hbar = cH (dead)
# ===========================================================================
def c6():
    a_over_cH = UNRUH_2PI / TWO_PI
    a_val = UNRUH_2PI * C_LIGHT * K_B * (HBAR * H_DS / (TWO_PI * K_B)) / HBAR
    ok = relerr(a_over_cH, 1.0) < 1e-12 and relerr(a_val, CH_L) < 1e-9
    return check("C6", ok, "a_U/(cH_L)=%.9f; a_U=%.6e" % (a_over_cH, a_val),
                 "= 1 to 1e-12",
                 "route (b): coefficient exactly 1 -> kappa = Z/2, 16.7 sigma dead")


# ===========================================================================
# C7 -- holographic equipartition N_surf = N_bulk IS Friedmann
# ===========================================================================
def c7():
    c, G, rho, H, hbar, kB, lP2 = sp.symbols("c G rho H hbar k_B lP2", positive=True)
    N_sur = 4 * sp.pi * (c / H) ** 2 / lP2
    V = (4 * sp.pi / 3) * (c / H) ** 3
    T = hbar * H / (2 * sp.pi * kB)
    E_K = 2 * rho * c ** 2 * V
    N_bulk = 2 * E_K / (kB * T)
    eq = sp.simplify((N_sur - N_bulk).subs(lP2, G * hbar / c ** 3))
    sol = sp.solve(sp.Eq(eq, 0), rho)
    resid = sp.simplify(sol[0] - 3 * H ** 2 / (8 * sp.pi * G)) if sol else sp.nan
    # E_K = (rho + 3P/c^2) V = 2 rho V for pure Lambda;  N_bulk = 2 E_K/(k_B T)
    Ns = 4 * math.pi * (C_LIGHT / H_L) ** 2 / (HBAR * G_N / C_LIGHT ** 3)
    Nb = KOMAR * 2.0 * (RHO_L * C_LIGHT ** 2 * (4 * math.pi / 3) * (C_LIGHT / H_L) ** 3) \
        / (HBAR * H_L / (2 * math.pi))
    ratio = Nb / Ns
    ok = (resid == 0) and relerr(ratio, 1.0) < 1e-10
    return check("C7", ok, "N_surf=N_bulk <=> rho=3H^2/8piG (resid %s); N_b/N_s=%.12f"
                 % (resid, ratio),
                 "resid 0; ratio 1 to 1e-10",
                 "route (d): equipartition has no content beyond Friedmann")


# ===========================================================================
# C8 -- surface gravity/2pi = Unruh at T_dS/2pi = cH_L/(2pi), and != cH0/(2pi)
# ===========================================================================
def c8():
    route_a = CH_L / TP_TH                                # surface gravity / 2pi
    T_target = (HBAR * H_DS / (TWO_PI * K_B)) / TWO_PI    # T_dS / 2pi
    route_b = UNRUH_2PI * C_LIGHT * K_B * T_target / HBAR
    route_h0 = CH_0 / TWO_PI
    ratio_to_h0 = route_a / route_h0
    ok = (relerr(route_a, route_b) < 1e-14
          and relerr(ratio_to_h0, math.sqrt(OMEGA_L)) < 1e-9
          and abs(route_a - route_h0) / route_h0 > 0.05)
    return check("C8", ok, "A=%.6e B=%.6e; A/(cH0/2pi)=%.9f (sqrtOm=%.9f)"
                 % (route_a, route_b, ratio_to_h0, math.sqrt(OMEGA_L)),
                 "A=B 1e-14; ratio sqrt(Om) 1e-9; A!=cH0/2pi",
                 "routes (e) and (f) are the same number: 1/(2pi) is inserted, "
                 "not derived")


# ===========================================================================
# C9 -- the observed Omega_Lambda vs 32pi/147 vs Planck
# ===========================================================================
def c9():
    target = 32 * math.pi / 147.0
    d_planck = abs(OMEGA_L_PLANCK - target) / SIG_OMEGA_L_PLANCK
    ok = relerr(OM_L, target) < 1e-3 and d_planck < 0.5
    return check("C9", ok, "Om_L=%.8f vs 32pi/147=%.8f rel=%.2e; Planck dist=%.3f sigma"
                 % (OM_L, target, relerr(OM_L, target), d_planck),
                 "rel < 1e-3; Planck dist < 0.5 sigma",
                 "Omega_Lambda = 32pi/147 is 0.11 sigma from Planck -- a "
                 "coincidence, not a prediction")


# ===========================================================================
# C10 -- no rational count reproduces Omega*: 32pi/147 is irrational
# ===========================================================================
def c10():
    exact = 32 * math.pi / 147.0
    if PARAMS["omega_solution"] is not None:
        exact = float(PARAMS["omega_solution"])
    f = lambda om: 0.5 * math.sqrt(3.0 * om / (8.0 * math.pi)) - 1.0 / 7.0
    num = brentq(f, 0.30, 0.95) if f(0.30) * f(0.95) < 0 else float("nan")
    best = (9e9, 1, 1)
    for q in range(1, 1001):
        p = int(round(exact * q))
        if p <= 0:
            continue
        d = abs(exact - p / q)
        if d < best[0]:
            best = (d, p, q)
    is_irr = not sp.sympify(sp.Integer(32) * sp.pi / 147).is_rational
    ok = relerr(exact, num) < 1e-9 and best[0] > 1e-8 and is_irr is True
    return check("C10", ok, "closest p/q (q<=1000): %d/%d, |d|=%.3e; irrational=%s"
                 % (best[1], best[2], best[0], is_irr),
                 "|d| > 1e-8; 32pi/147 not rational",
                 "any integer cell count gives Omega_L in Q, but 1/7 needs "
                 "32pi/147 = (8pi/3)(2/7)^2, which is not in Q")


# ===========================================================================
# THE POOL
# ===========================================================================
ATOMS = np.array([1.0, 2.0, 3.0, 4.0, 5.0, 7.0, 8.0,
                  math.pi, math.e, math.sqrt(2.0), math.sqrt(3.0)])
ATOM_NAMES = ["1", "2", "3", "4", "5", "7", "8", "pi", "e", "sqrt2", "sqrt3"]
NA = 11


def _div(x, y):
    with np.errstate(divide="ignore", invalid="ignore"):
        return x / y


def _pow(x, y):
    with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
        r = np.power(np.abs(x), y)
    return np.where((x > 0) & np.isfinite(r), r, np.nan)


def _comb(x, y, axis, nops):
    parts = [x + y, x - y, x * y, _div(x, y)]
    if nops >= 5:
        parts.append(_pow(x, y))
    return np.stack(parts, axis=axis)


def build_pool(nops=5):
    """All closed forms with <= 3 binary operations over the 11 atoms.

    Returns (forms_array, n_forms).  Five tree shapes for three operations,
    two for two, one for one."""
    out = []
    a2 = ATOMS.reshape(NA, 1)
    b2 = ATOMS.reshape(1, NA)
    v1 = _comb(a2, b2, 0, nops)                       # (nops, 11, 11)  a o b
    out.append(v1.ravel())
    c3 = ATOMS.reshape(1, 1, 1, NA)
    p2a = _comb(v1[:, :, :, None], c3, 3, nops).ravel()            # (a o b) o c
    p2b = _comb(ATOMS.reshape(NA, 1, 1, 1), v1[None, :, :, :], 0, nops).ravel()
    out += [p2a, p2b]
    d6 = ATOMS.reshape(1, 1, 1, 1, 1, 1, NA)
    a6 = ATOMS.reshape(NA, 1, 1, 1, 1, 1)
    # S1 ((a o b) o c) o d
    out.append(_comb(_comb(v1[:, :, :, None], c3, 3, nops)[:, :, :, :, :, None],
                     d6, 5, nops).ravel())
    # S2 (a o (b o c)) o d
    out.append(_comb(_comb(ATOMS.reshape(NA, 1, 1, 1), v1[None, :, :, :], 0, nops)
                     [:, :, :, :, :, None], d6, 5, nops).ravel())
    # S3 a o ((b o c) o d)
    bc_d = _comb(v1[:, :, :, None], d6, 3, nops)
    out.append(_comb(a6, bc_d[None, :, :, :, :, :], 0, nops).ravel())
    # S4 a o (b o (c o d))
    cd = _comb(ATOMS.reshape(NA, 1), ATOMS.reshape(1, NA), 0, nops)
    b_cd = _comb(ATOMS.reshape(NA, 1, 1, 1), cd[None, :, :, :], 0, nops)
    out.append(_comb(a6, b_cd[None, :, :, :, :, :], 0, nops).ravel())
    # S5 (a o b) o (c o d)
    out.append(_comb(v1[:, :, :, None, None, None],
                     cd[None, None, None, :, :, :], 3, nops).ravel())
    vals = np.concatenate(out)
    return vals, vals.size


def dedupe(vals, lo=1e-3, hi=1e3, tol=1e-11):
    v = vals[np.isfinite(vals) & (vals > lo) & (vals < hi)]
    v.sort()
    mask = np.zeros(v.size, dtype=bool)
    mask[0] = True
    last = v[0]
    for i in range(1, v.size):
        if v[i] - last > tol * v[i]:
            mask[i] = True
            last = v[i]
    return v[mask]


_RAW, _NFORMS = build_pool(int(PARAMS["pool_ops"]))
POOL_FORMS = int(_NFORMS)
POOL = dedupe(_RAW)
POOL_N = int(POOL.size)
del _RAW


def count_near(target, frac, pool=None):
    p = POOL if pool is None else pool
    lo, hi = target * (1 - frac), target * (1 + frac)
    return int(np.searchsorted(p, hi, "right") - np.searchsorted(p, lo, "left"))


def simple_forms(maxops=2):
    """Closed forms with <= 2 operations, as (value, description) -- used only
    to measure description length, never for the counts."""
    rec = []
    one = [(ATOMS[i], ATOM_NAMES[i]) for i in range(NA)]
    for i in range(NA):
        for j in range(NA):
            for sym, fn in (("+", lambda x, y: x + y), ("-", lambda x, y: x - y),
                            ("*", lambda x, y: x * y), ("/", lambda x, y: x / y),
                            ("^", lambda x, y: (abs(x) ** y if x > 0 else float("nan")))):
                v = fn(ATOMS[i], ATOMS[j])
                if np.isfinite(v) and v > 0:
                    rec.append((v, "(%s%s%s)" % (ATOM_NAMES[i], sym, ATOM_NAMES[j])))
    if maxops >= 2:
        for i in range(NA):
            for j in range(NA):
                for sym, fn in (("+", lambda x, y: x + y), ("-", lambda x, y: x - y),
                                ("*", lambda x, y: x * y), ("/", lambda x, y: x / y)):
                    v = fn(ATOMS[i], ATOMS[j])
                    if not (np.isfinite(v) and v > 0):
                        continue
                    for k in range(NA):
                        for sym2, fn2 in (("+", lambda x, y: x + y),
                                          ("-", lambda x, y: x - y),
                                          ("*", lambda x, y: x * y),
                                          ("/", lambda x, y: x / y)):
                            w = fn2(v, ATOMS[k])
                            if np.isfinite(w) and w > 0:
                                rec.append((w, "(%s%s%s)%s%s"
                                            % (ATOM_NAMES[i], sym, ATOM_NAMES[j],
                                               sym2, ATOM_NAMES[k])))
    return rec


SIMPLE = simple_forms(2)


def simplest_hits(target, frac, n=4, exclude_exact=True):
    hits = []
    seen = set()
    for v, d in SIMPLE:
        if abs(v - target) / target < frac:
            if exclude_exact and abs(v - target) / target < 1e-12:
                continue
            key = round(v, 12)
            if key in seen:
                continue
            seen.add(key)
            hits.append((len(d), v, d))
    hits.sort()
    return hits[:n]


def closest_simple(target):
    """The nearest <= 2-operation closed form that is NOT the target itself."""
    best = (9e9, "", 0.0)
    for v, d in SIMPLE:
        r = abs(v - target) / target
        if r < 1e-12:
            continue
        if r < best[0]:
            best = (r, d, v)
    return best


# ===========================================================================
# C11 -- the pool and its hit counts
# ===========================================================================
def c11():
    t17 = CH_0 / 7.0 / CH_0            # 1/7 as a pure number
    t2p = 1.0 / TWO_PI
    h1 = count_near(t17, 0.01)
    h2 = count_near(t2p, 0.01)
    h1b = count_near(t17, 0.001)
    h2b = count_near(t2p, 0.001)
    h1c = count_near(t17, 1e-4)
    h2c = count_near(t2p, 1e-4)
    ok = (POOL_N >= 200000) and (h1c >= 1) and (h2c >= 1)
    return check("C11", ok,
                 "forms=%d distinct=%d | 1/7: %d/%d/%d | 1/2pi: %d/%d/%d"
                 % (POOL_FORMS, POOL_N, h1, h1b, h1c, h2, h2b, h2c),
                 "distinct>=200000; >=1 hit at 0.01% for both",
                 "both candidates are matched, at every window, by hundreds of "
                 "closed forms: a match carries no information")


# ===========================================================================
# C12 -- calibration: is the density near the candidate typical?
# ===========================================================================
def c12():
    rng = np.random.default_rng(72)
    tg = np.exp(rng.uniform(math.log(0.10), math.log(0.25), 300))
    counts = np.array([count_near(float(t), 0.01) for t in tg])
    mu, sd = float(counts.mean()), float(counts.std())
    c17 = count_near(1.0 / 7.0, 0.01)
    c2p = count_near(1.0 / TWO_PI, 0.01)
    z17 = (c17 - mu) / (sd if sd > 0 else 1.0)
    z2p = (c2p - mu) / (sd if sd > 0 else 1.0)
    ok = (abs(z17) < 3) and (abs(z2p) < 3) and POOL_N >= 200000
    return check("C12", ok, "1/7 z=%.2f, 1/2pi z=%.2f (random mean %.1f +- %.1f)"
                 % (z17, z2p, mu, sd),
                 "|z| < 3 for both; pool >= 200000",
                 "neither candidate sits in an unusually dense or empty part of "
                 "the pool")


# ===========================================================================
# C13 -- the route census: how many stated premises produce each candidate
# ===========================================================================
def route_table():
    """Every structural route, as an a0 in SI plus its coefficient frame."""
    rows = []
    rows.append(("R1 closure/Friedmann, kappa=1/2",
                 A0_TH, "1/Z x cH_L"))
    rows.append(("R2 thermal wavelength, T_dS (Gibbons-Hawking)",
                 CH_L / TWO_PI, "1/(2pi) x cH_L"))
    rows.append(("R3 thermal wavelength, apparent horizon",
                 CH_0 / TWO_PI, "1/(2pi) x cH0"))
    rows.append(("R4 Unruh matching T_U = T_dS",
                 CH_L, "1 x cH_L"))
    rows.append(("R5 surface gravity of the dS horizon",
                 CH_L, "1 x cH_L"))
    rows.append(("R6 thermal de Broglie lambda=2pi/T",
                 CH_L / (4 * math.pi ** 2), "1/(4pi^2) x cH_L"))
    rows.append(("R7 equipartition deficit at Om_m=0.3162",
                 0.4743 * CH_0, "0.4743 x cH0"))
    rows.append(("R8 Verlinde volume law cH0/6",
                 CH_0 / 6.0, "1/6 x cH0"))
    if PARAMS["extra_route"] is not None:
        rows.append(("R9 (mutant) a route that returns 1/7",
                     float(PARAMS["extra_route"]), "1/7 x cH0"))
    return rows


def route_pure():
    """Every structural route as a PURE NUMBER (both frames), plus its a0."""
    rows = [
        ("closure/Friedmann kappa=1/2 (cH_L)", INV_Z, A0_TH),
        ("closure in the cH0 frame (cH0)", A0_TH / CH_0, A0_TH),
        ("thermal wavelength T_dS (cH_L)", 1.0 / TWO_PI, CH_L / TWO_PI),
        ("thermal, apparent horizon (cH0)", 1.0 / TWO_PI, CH_0 / TWO_PI),
        ("thermal in the cH0 frame (cH0)", (CH_L / TWO_PI) / CH_0, CH_L / TWO_PI),
        ("Unruh matching T_U=T_dS (cH_L)", 1.0, CH_L),
        ("surface gravity / 2pi (cH_L)", 1.0 / TWO_PI, CH_L / TWO_PI),
        ("thermal de Broglie 4pi^2 (cH_L)", 1.0 / (4 * math.pi ** 2),
         CH_L / (4 * math.pi ** 2)),
        ("equipartition deficit 0.4743 (cH0)", 0.4743, 0.4743 * CH_0),
        ("Verlinde volume 1/6 (cH0)", 1.0 / 6.0, CH_0 / 6.0),
    ]
    if PARAMS["extra_route"] is not None:
        rows.append(("(mutant) a route that returns 1/7", float(PARAMS["extra_route"]) / CH_0,
                     float(PARAMS["extra_route"])))
    return rows


def c13():
    rows = route_pure()
    t17, t2p = 1.0 / 7.0, 1.0 / TWO_PI
    n17 = sum(1 for _, v, _ in rows if abs(v - t17) / t17 < 1e-9)
    n2p = sum(1 for _, v, _ in rows if abs(v - t2p) / t2p < 1e-9)
    closest = min(rows, key=lambda r: abs(r[1] - t17) / t17)
    d_close = abs(closest[1] - t17) / t17
    vals = sorted(set(round(a, 12) for _, _, a in rows))
    ok = (n17 == 0) and (n2p >= 1) and (len(vals) >= 5)
    return check("C13", ok,
                 "routes =1/7: %d ; =1/(2pi): %d ; closest to 1/7: %s (%.2e); distinct a0: %d"
                 % (n17, n2p, closest[0], d_close, len(vals)),
                 "n(1/7)=0 exact and n(1/2pi)>=1 and >=5 distinct a0",
                 "no stated premise produces 1/7 exactly; the closest is the "
                 "closure at 6.1e-5 -- the 32pi/147 coincidence restated")


# ===========================================================================
# C14 -- the two candidates are indistinguishable at the current precision
# ===========================================================================
def c14():
    a17 = CH_0 / 7.0
    a2p = CH_L / TWO_PI
    delta = a17 - a2p
    sig_now = delta / SIG_A0_LIVE
    ok = (abs(sig_now) < 1.0) and (delta / A0_MEAS > 0.05)
    return check("C14", ok, "delta_a0=%.6e (%.5f of a0); separation=%.4f sigma"
                 % (delta, delta / A0_MEAS, sig_now),
                 "|separation| < 1 sigma and delta/a0 > 0.05",
                 "the two candidates differ by 8.55% in a0 and 0.27 sigma in the "
                 "current measurement")


# ===========================================================================
# C15 -- the record's 1.0422e-10 is cH0/(2pi), NOT the dS value cH_L/(2pi)
# ===========================================================================
def c15():
    a_route = C_LIGHT * H_DS / TP_TH
    a_record = CH_0 / TWO_PI
    ratio = a_route / a_record
    dist = (a_record - A0_MEAS) / SIG_A0_LIVE
    ok = (relerr(ratio, math.sqrt(OMEGA_L)) < 1e-9) and abs(dist) < 1.0
    return check("C15", ok, "a_route/a_record=%.9f (sqrtOm=%.9f); record dist=%.3f sigma"
                 % (ratio, math.sqrt(OMEGA_L), dist),
                 "ratio = sqrt(Om) to 1e-9; record within 1 sigma",
                 "attaching 1/(2pi) to H0 instead of H_Lambda moves a0 by 20.9%")


# ===========================================================================
# C16 -- what precision decides it: sigma(a0)/a0 and the pair count
# ===========================================================================
def c16():
    a17 = CH_0 / 7.0
    a2p = CH_L / TWO_PI
    dkP3 = abs(a17 - a2p) / A0_MEAS * KAPPA_P3_MEAS
    seps = {}
    for name, s in SIG_FORECAST.items():
        seps[name] = dkP3 / s
    seps["wide binary (live forecast)"] = dkP3 / SIG_WB
    sig_req = dkP3 / 3.0
    n_req = N_PAIRS_REF * (SIG_WB / sig_req) ** 2
    ok = (all(v < 1.0 for v in seps.values()) and 2e5 < n_req < 1e6)
    return check("C16", ok,
                 "dKappa=%.6f; seps %s; sigma_req(3sig)=%.5f; N=%.2e pairs"
                 % (dkP3, {k: round(v, 3) for k, v in seps.items()}, sig_req, n_req),
                 "every forecast < 1 sigma; 2e5 < N < 1e6",
                 "no measurement in the record's forecast set reaches 3 sigma")


# ===========================================================================
# C17 -- the likelihood ratio between the candidates
# ===========================================================================
def c17():
    a17 = CH_0 / 7.0
    a2p = CH_L / TWO_PI
    chi17 = ((a17 - A0_MEAS) / SIG_A0_LIVE) ** 2
    chi2p = ((a2p - A0_MEAS) / SIG_A0_LIVE) ** 2
    dchi = abs(chi17 - chi2p)
    lr = math.exp(-0.5 * dchi)
    ok = (dchi < 1.0) and (lr > 0.5)
    return check("C17", ok, "chi2(1/7)=%.4f chi2(1/2pi)=%.4f dchi2=%.4f LR=%.4f"
                 % (chi17, chi2p, dchi, lr),
                 "dchi2 < 1 and LR > 0.5",
                 "the data prefer the thermal value by a likelihood ratio of 1.04 "
                 "-- no evidence")


# ===========================================================================
# C18 -- the two readings cannot both be right: the thermal one needs
#        Omega_L = (2pi/7)^2 = 0.8059 if 1/7 is also to hold
# ===========================================================================
def c18():
    om_required = (TWO_PI / 7.0) ** 2
    dist = (om_required - OMEGA_L_PLANCK) / SIG_OMEGA_L_PLANCK
    ok = (dist > 5.0) and (relerr(32 * math.pi / 147.0, OM_L) < 1e-3)
    return check("C18", ok, "Om required by 1/7 & 1/(2pi) together=%.6f; %.1f sigma from Planck"
                 % (om_required, dist),
                 "> 5 sigma, and 32pi/147 within 1e-3 of the observed Om",
                 "the two coefficients are not two names for one number: they need "
                 "Omega_L = 0.6839 vs 0.8059")


# ===========================================================================
# C19 -- the pool densely interpolates the two candidates
# ===========================================================================
def c19():
    lo = CH_L / TWO_PI / CH_0          # 0.131610 in cH0 units
    hi = 1.0 / 7.0
    n_in = int(np.searchsorted(POOL, hi, "left") - np.searchsorted(POOL, lo, "right"))
    ok = n_in > 1000
    return check("C19", ok, "closed forms strictly between %.6f and %.6f: %d"
                 % (lo, hi, n_in),
                 "> 1000",
                 "the gap between the candidates is filled with closed forms: "
                 "interpolation is not discrimination")


# ===========================================================================
# C20 -- the two kappa conventions (A71's trap), reproduced
# ===========================================================================
def c20():
    kp3 = A0_MEAS * math.sqrt(8 * math.pi / 3) / CH_0
    factor = math.sqrt(OM_L) if PARAMS["de_sqrt"] else OM_L
    kde = kp3 / factor
    ok = (relerr(kp3, KAPPA_P3_MEAS) < 1e-3 and relerr(kde, KAPPA_DE_MEAS) < 1e-2
          and relerr(1.0 / factor, 1.0 / math.sqrt(OM_L)) < 1e-12)
    return check("C20", ok, "kappa_P3=%.6f kappa_DE=%.6f ratio=%.6f (1/sqrtOm=%.6f)"
                 % (kp3, kde, kde / kp3, 1.0 / math.sqrt(OM_L)),
                 "1e-3 / 1e-2 of A71; ratio = 1/sqrt(Om)",
                 "kappa_DE = kappa_P3/sqrt(Omega_L): the same a0 is 0.378 or 0.456")


# ===========================================================================
# C21 -- the decisive test: how many pool hits are DERIVABLE?
# ===========================================================================
def c21():
    route_vals = [v for _, v, _ in route_pure()]
    def n_deriv(target, frac):
        lo, hi = target * (1 - frac), target * (1 + frac)
        i0 = np.searchsorted(POOL, lo, "left")
        i1 = np.searchsorted(POOL, hi, "right")
        hits = POOL[i0:i1]
        nd = sum(1 for v in hits if any(abs(v - r) / r < 1e-9 for r in route_vals))
        return int(hits.size), int(nd)
    n1, d1 = n_deriv(1.0 / 7.0, 0.01)
    n2, d2 = n_deriv(1.0 / TWO_PI, 0.01)
    ok = (d1 == 0) and (d2 >= 1)
    return check("C21", ok, "1/7: %d hits, %d derivable | 1/(2pi): %d hits, %d derivable"
                 % (n1, d1, n2, d2),
                 "0 derivable for 1/7 and >=1 for 1/(2pi)",
                 "of the hundreds of matches, only the thermal one is the output "
                 "of a stated premise")


# ===========================================================================
# C22 -- Monte-Carlo P(at least one hit) for a random coefficient
# ===========================================================================
def c22():
    rng = np.random.default_rng(720)
    tg = np.exp(rng.uniform(math.log(0.10), math.log(0.25), 3000))
    out = {}
    for f in (0.01, 1e-3, 1e-4, 1e-5):
        cnt = np.array([count_near(float(t), f) for t in tg])
        out[f] = (float(cnt.mean()), float((cnt >= 1).mean()))
    p1 = out[1e-4][1]
    ok = (out[0.01][1] > 0.99) and (p1 > 0.5) and POOL_N >= 200000
    return check("C22", ok,
                 "P(>=1 hit): 1%%=%.4f 0.1%%=%.4f 0.01%%=%.4f 0.001%%=%.4f (mean counts %.1f/%.2f/%.2f/%.3f)"
                 % (out[0.01][1], out[1e-3][1], out[1e-4][1], out[1e-5][1],
                    out[0.01][0], out[1e-3][0], out[1e-4][0], out[1e-5][0]),
                 "P(1%)>0.99 and P(0.01%)>0.5",
                 "a 0.01% match is expected by chance for a random coefficient")
    return ok


# ===========================================================================
def main():
    banner("A72_coefficient -- a0/(cH): 1/7 or 1/(2pi)?   (K = 4 pi G, c = 1)")
    banner("cH0 = %.6e   cH_L = %.6e   Omega_L = %.8f   rho_L = %.6e"
           % (CH_0, CH_L, OMEGA_L, RHO_L))
    banner("Z = %.9f   1/Z = %.9f   1/(2pi) = %.9f   1/7 = %.9f"
           % (Z, INV_Z, 1.0 / TWO_PI, 1.0 / 7.0))
    banner("a0(kappa=1/2) = c^2 sqrt(L/32pi) = %.9e   a0/cH_L = %.9f   a0/cH0 = %.9f"
           % (A0_TH, A0_TH / CH_L, A0_TH / CH_0))
    banner("a0 = cH0/7 = %.9e ; cH_L/(2pi) = %.9e ; cH0/(2pi) = %.9e"
           % (CH_0 / 7.0, CH_L / TWO_PI, CH_0 / TWO_PI))
    banner("measured a0 = %.4e +- %.2e ; kappa_P3 = %.5f +- %.5f ; kappa_DE = %.4f +- %.4f"
           % (A0_MEAS, SIG_A0, KAPPA_P3_MEAS, SIG_P3_TOT, KAPPA_DE_MEAS, SIG_DE_STAT))
    banner("pool: %d closed forms -> %d distinct values in [1e-3,1e3]"
           % (POOL_FORMS, POOL_N))
    if MUTATE:
        banner("*** MUTATION %s ACTIVE: %s ***"
               % (MUT_NAME, PARAMS if False else MUTATIONS[MUT_NAME]))
    print("")

    fns = [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11,
           c12, c13, c14, c15, c16, c17, c18, c19, c20, c21, c22]
    outcomes = [f() for f in fns]
    npass = sum(1 for o in outcomes if o)
    total = len(outcomes)
    print("")
    print("A72 COMPLETE: %d/%d checks PASS." % (npass, total))

    if MUTATE:
        broken = sorted(r["id"] for r in RESULTS if not r["pass"])
        print("# mutated checks broken: %s" % (",".join(broken) if broken else "NONE"))
        print("# MUTATION %s" % ("CONFIRMED" if broken else "FAILED TO BITE"))
        return 1 if broken else 2

    # ---------------- numbers for the json ----------------
    a17 = CH_0 / 7.0
    a2p = CH_L / TWO_PI
    a2p_h0 = CH_0 / TWO_PI
    rows = route_table()
    kp3 = lambda a: a * math.sqrt(8 * math.pi / 3) / CH_0
    kde = lambda a: a * math.sqrt(8 * math.pi) / (CH_0 * math.sqrt(3 * OMEGA_L))
    sig_de_tot = SIG_P3_TOT / math.sqrt(OMEGA_L)
    table = []
    for name, a, frame in rows:
        table.append({
            "route": name, "frame": frame, "a0": a,
            "coef_cH_L": a / CH_L, "coef_cH0": a / CH_0,
            "kappa_P3": kp3(a), "kappa_DE": kde(a),
            "dist_P3_stat_sigma": (kp3(a) - KAPPA_P3_MEAS) / SIG_P3_STAT,
            "dist_P3_tot_sigma": (kp3(a) - KAPPA_P3_MEAS) / SIG_P3_TOT,
            "dist_DE_stat_sigma": (kde(a) - KAPPA_DE_MEAS) / SIG_DE_STAT,
            "dist_DE_tot_sigma": (kde(a) - KAPPA_DE_MEAS) / sig_de_tot,
            "in_falsifier_band_DE": 0.3415 <= kde(a) <= 0.5265,
        })
    dkP3 = abs(a17 - a2p) / A0_MEAS * KAPPA_P3_MEAS
    dkP3_h0 = abs(a17 - a2p_h0) / A0_MEAS * KAPPA_P3_MEAS
    seps = {k: dkP3 / v for k, v in SIG_FORECAST.items()}
    sig_req3 = dkP3 / 3.0
    sig_req5 = dkP3 / 5.0
    n_req3 = N_PAIRS_REF * (0.040 / sig_req3) ** 2
    n_req5 = N_PAIRS_REF * (0.040 / sig_req5) ** 2
    dgamma = 0.510 * sig_req3          # A71: dgamma_v/dkappa = 0.510 at 20 kAU

    payload = {
        "lane": "A72_coefficient",
        "status": "NO-GO(1/7) / CONDITIONAL(1/2pi) / DECIDABLE(3%)",
        "checks": RESULTS,
        "route_table": table,
        "numbers": {
            "Z": Z, "inv_Z": INV_Z, "two_pi": TWO_PI, "inv_two_pi": 1.0 / TWO_PI,
            "one_seventh": 1.0 / 7.0,
            "H0": H0, "H_lambda": H_L, "cH0": CH_0, "cH_lambda": CH_L,
            "rho_lambda": RHO_L, "omega_lambda": OMEGA_L,
            "omega_lambda_for_1over7": 32 * math.pi / 147.0,
            "omega_lambda_planck": OMEGA_L_PLANCK,
            "omega_lambda_planck_sigma": SIG_OMEGA_L_PLANCK,
            "dist_planck_to_32pi147_sigma":
                (OMEGA_L_PLANCK - 32 * math.pi / 147.0) / SIG_OMEGA_L_PLANCK,
            "a0_th": A0_TH, "a0_can": A0_CAN, "a0_meas": A0_MEAS, "sig_a0": SIG_A0,
            "a0_cH0_over_7": a17, "a0_cHL_over_2pi": a2p, "a0_cH0_over_2pi": a2p_h0,
            "a0_cHL_over_4pi2": CH_L / (4 * math.pi ** 2),
            "a0_over_cH_L_theory": A0_TH / CH_L,
            "a0_over_cH0_theory": A0_TH / CH_0,
            "a0_over_cH0_vs_1over7_rel": relerr(A0_TH / CH_0, 1.0 / 7.0),
            "dist_meas_to_1over7_sigma": (a17 - A0_MEAS) / SIG_A0,
            "dist_meas_to_2pi_dS_sigma": (a2p - A0_MEAS) / SIG_A0,
            "dist_meas_to_2pi_H0_sigma": (a2p_h0 - A0_MEAS) / SIG_A0,
            "dist_meas_to_cHL_sigma": (CH_L - A0_MEAS) / SIG_A0,
            "dist_meas_to_cH0_sigma": (CH_0 - A0_MEAS) / SIG_A0,
            "delta_a0_17_vs_2pi_dS": a17 - a2p,
            "delta_rel_17_vs_2pi_dS": (a17 - a2p) / a2p,
            "delta_a0_17_vs_2pi_H0": a17 - a2p_h0,
            "delta_rel_17_vs_2pi_H0": (a17 - a2p_h0) / a2p_h0,
            "sep_now_sigma": (a17 - a2p) / SIG_A0,
            "sep_now_sigma_H0_pair": (a17 - a2p_h0) / SIG_A0,
            "dchi2": abs(((a17 - A0_MEAS) / SIG_A0) ** 2
                         - ((a2p - A0_MEAS) / SIG_A0) ** 2),
            "likelihood_ratio": math.exp(-0.5 * abs(
                ((a17 - A0_MEAS) / SIG_A0) ** 2 - ((a2p - A0_MEAS) / SIG_A0) ** 2)),
            "kappa_P3_meas": KAPPA_P3_MEAS, "sig_P3_stat": SIG_P3_STAT,
            "sig_P3_tot": SIG_P3_TOT, "kappa_DE_meas": KAPPA_DE_MEAS,
            "sig_DE_stat": SIG_DE_STAT, "sig_DE_tot": sig_de_tot,
            "one_over_sqrt_omega": 1.0 / math.sqrt(OMEGA_L),
            "falsifier_band_DE": [0.3415, 0.5265],
            "delta_kappa_P3": dkP3, "delta_kappa_P3_H0pair": dkP3_h0,
            "sep_forecast_sigma": seps,
            "sigma_kappa_req_3sig": sig_req3,
            "sigma_kappa_req_5sig": sig_req5,
            "ratio_7_over_2pi": 7.0 / TWO_PI,
            "Z_over_4pi": Z / (4 * math.pi),
            "sqrt_2_over_3pi": math.sqrt(2.0 / (3.0 * math.pi)),
            "Z_over_4pi_minus_sqrt": Z / (4 * math.pi) - math.sqrt(2.0 / (3.0 * math.pi)),
            "mc_draws": 3000,
            "mc_range": [0.10, 0.25],
            "sigma_ratio_wb_over_req": 0.040 / sig_req3,
            "sig_a0_over_a0": SIG_A0 / A0_MEAS,
            "sig_kappa_over_kappa_forecast": {k: v / KAPPA_P3_MEAS
                                              for k, v in SIG_FORECAST.items()},
            "N_pairs_ratio_to_DR4": n_req3 / N_PAIRS_REF,
            "omega_lambda_req_precision_3sig":
                (OMEGA_L_PLANCK - 32 * math.pi / 147.0) / 3.0,
            "planck_sigma_over_required":
                SIG_OMEGA_L_PLANCK / ((OMEGA_L_PLANCK - 32 * math.pi / 147.0) / 3.0),
            "likelihood_ratio_inverse": 1.0 / math.exp(-0.5 * abs(
                ((a17 - A0_MEAS) / SIG_A0) ** 2 - ((a2p - A0_MEAS) / SIG_A0) ** 2)),
            "kappa_half_over_thermal": 0.5 / (Z / (4 * math.pi)),
            "kappa_half_over_thermal_rel": 0.5 / (Z / (4 * math.pi)) - 1.0,
            "dist_17_P3_stat": (kp3(a17) - KAPPA_P3_MEAS) / SIG_P3_STAT,
            "dist_thermal_P3_stat": (kp3(a2p) - KAPPA_P3_MEAS) / SIG_P3_STAT,
            "sigma_a0_over_a0_req_5sig": sig_req5 / KAPPA_P3_MEAS,
            "gamma_v_ref_20kAU": 1.1811,
            "sigma_gamma_over_gamma_req": dgamma / 1.1811,
            "sig_a0_stat": SIG_P3_STAT / KAPPA_P3_MEAS * A0_MEAS,
            "chi2_stat_1_7": ((a17 - A0_MEAS) / (SIG_P3_STAT / KAPPA_P3_MEAS * A0_MEAS)) ** 2,
            "chi2_stat_2pi_dS": ((a2p - A0_MEAS) / (SIG_P3_STAT / KAPPA_P3_MEAS * A0_MEAS)) ** 2,
            "LR_stat_2pi_over_1_7": math.exp(-0.5 * (
                ((a2p - A0_MEAS) / (SIG_P3_STAT / KAPPA_P3_MEAS * A0_MEAS)) ** 2
                - ((a17 - A0_MEAS) / (SIG_P3_STAT / KAPPA_P3_MEAS * A0_MEAS)) ** 2)),
            "sigma_kappa_req_3sig_H0pair": dkP3_h0 / 3.0,
            "sigma_a0_req_3sig_H0pair": dkP3_h0 / 3.0 / KAPPA_P3_MEAS * A0_MEAS,
            "sigma_a0_over_a0_req_3sig_H0pair": dkP3_h0 / 3.0 / KAPPA_P3_MEAS,
            "N_pairs_req_3sig_H0pair": N_PAIRS_REF * (SIG_WB / (dkP3_h0 / 3.0)) ** 2,
            "sigma_gamma_v_req_3sig_H0pair": 0.510 * dkP3_h0 / 3.0,
            "sigma_a0_req_3sig": sig_req3 / KAPPA_P3_MEAS * A0_MEAS,
            "sigma_a0_over_a0_req_3sig": sig_req3 / KAPPA_P3_MEAS,
            "N_pairs_req_3sig": n_req3, "N_pairs_req_5sig": n_req5,
            "sigma_gamma_v_req_3sig": dgamma,
            "sigma_kappa_wb": 0.040, "sigma_kappa_wb_joint": 0.0605,
            "sigma_kappa_sparc1000": 0.118,
            "pool_forms": POOL_FORMS, "pool_distinct": POOL_N,
            "hits_1_7": {w: count_near(1.0 / 7.0, w) for w in (0.01, 1e-3, 1e-4, 1e-5)},
            "hits_2pi": {w: count_near(1.0 / TWO_PI, w) for w in (0.01, 1e-3, 1e-4, 1e-5)},
            "hits_1_Z": {w: count_near(INV_Z, w) for w in (0.01, 1e-3, 1e-4, 1e-5)},
            "hits_between_candidates": int(
                np.searchsorted(POOL, 1.0 / 7.0, "left")
                - np.searchsorted(POOL, a2p / CH_0, "right")),
            "simplest_1_7": [{"desc": d, "value": v} for _, v, d in
                             simplest_hits(1.0 / 7.0, 1e-4, 5)],
            "simplest_2pi": [{"desc": d, "value": v} for _, v, d in
                             simplest_hits(1.0 / TWO_PI, 1e-4, 5)],
            "n_rivals_2op_1_7": len(simplest_hits(1.0 / 7.0, 1e-4, 10 ** 6)),
            "n_rivals_2op_2pi": len(simplest_hits(1.0 / TWO_PI, 1e-4, 10 ** 6)),
            "closest_2op_1_7": {"desc": closest_simple(1.0 / 7.0)[1],
                                "value": closest_simple(1.0 / 7.0)[2],
                                "rel": closest_simple(1.0 / 7.0)[0]},
            "closest_2op_2pi": {"desc": closest_simple(1.0 / TWO_PI)[1],
                                "value": closest_simple(1.0 / TWO_PI)[2],
                                "rel": closest_simple(1.0 / TWO_PI)[0]},
            "omega_required_both": (TWO_PI / 7.0) ** 2,
            "dist_omega_required_sigma":
                ((TWO_PI / 7.0) ** 2 - OMEGA_L_PLANCK) / SIG_OMEGA_L_PLANCK,
            "n_routes_1_7": sum(1 for _, v, _ in route_pure()
                                if abs(v - 1.0 / 7.0) * 7.0 < 1e-9),
            "n_routes_2pi": sum(1 for _, v, _ in route_pure()
                                if abs(v - 1.0 / TWO_PI) * TWO_PI < 1e-9),
        },
        "constants_used": [
            "c = 2.99792458e8 m/s (BRIEF s4)",
            "G = 6.67430e-11 m^3 kg^-1 s^-2 (BRIEF s4)",
            "hbar = 1.054571817e-34 J s (CODATA 2018)",
            "k_B = 1.380649e-23 J/K (SI exact)",
            "Lambda = 1.0890e-52 m^-2 (BRIEF s4)",
            "H0 = 67.4 km/s/Mpc = 2.184285e-18 s^-1 (BRIEF s4)",
            "a0_can = 9.36e-11 m/s^2 (BRIEF s4, 3 s.f.)",
            "a0_meas = 8.544e-11 +- 2.73e-11 m/s^2 (A71 joint fit)",
            "kappa_P3 = 0.37765 +- 0.12069 (A71, rho_crit convention)",
            "kappa_DE = 0.4564 +- 0.0312 stat (A71, rho_DE convention)",
            "Omega_Lambda (Planck) = 0.6847 +- 0.0073 (external, as in A71)",
            "forecast sigma(kappa): 0.040 (WB full DR4), 0.0605 (WB+joint), "
            "0.118 (SPARC N=1000) (A71 s8)",
            "dgamma_v/dkappa = 0.510 at 20 kAU (A71 s8 / A24)",
            "nothing fitted in this lane",
        ],
    }
    with open(os.path.join(HERE, "a72_results.json"), "w") as fh:
        json.dump(payload, fh, indent=2)
        fh.write("\n")
    return 0 if npass == total else 1


if __name__ == "__main__":
    sys.exit(main())
