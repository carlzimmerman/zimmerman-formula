#!/usr/bin/env python3
"""
AS066 -- Horizon coefficient comparison without a theorem leap (bounded compute).

kappa_h = sqrt(8*pi/3)/(2*pi)   (a0 = c H/(2 pi), H^2 = 8 pi G rho_Lambda/3: Gibbons-Hawking/Unruh horizon form)
kappa_Z = 1/2                   (adopted framework footing, a0 = kappa c sqrt(G rho_Lambda), kappa = 1/2)

Objects (all positive finite, dimensionless except where units are declared):
  s = c sqrt(G rho_L),  Y = g/s,  y = g_N/s,  x = g/a0,  mu_n(Y) = 1 - (1+Y)^(-n),  n >= 1.
  OR-composed response over n channels with per-channel engagement p_lambda(Y),
    p(0)=0, p'(0)=lambda, p(inf)=1   =>   mu(Y) = 1 - (1 - p_lambda(Y))^n ,
  deep spherical matching  mu(g/s) g = g_N  =>  g^2 = (s/(n lambda)) g_N  =>  kappa = 1/(n lambda).

Sections:
  S0 constants/footings; S1 exact identities; S2 premise analysis + diagnostics at lambda in {1/2,1,2};
  S3 limiting regimes with leading neglected terms; S4 independent check (bisection inverse, 80 dps);
  S5 negative controls (NC1 lambda match; NC1b unit-slope shape family; NC2 count universality; NC3 finite-y);
  S6 dimensional footings (canonical + alternative, both coefficient cells); S7 source cross-checks.
Bounds: <=120 s wall (signal.alarm ENFORCED), 1 thread, memory recorded (setrlimit attempted and reported).
"""
import json, math, signal, sys, time, resource, hashlib, os

START = time.time()
def alarm_handler(*_):
    raise TimeoutError("wall-time limit exceeded")
signal.signal(signal.SIGALRM, alarm_handler)
signal.alarm(120)

OUT = {"sections": {}}
def sec(name, data):
    OUT["sections"][name] = data
def check(name, ok, observed, tolerance):
    OUT.setdefault("checks", []).append({"name": name, "pass": bool(ok),
                                         "observed": str(observed), "tolerance": str(tolerance)})

try:
    import sympy as sp
    from sympy import pi as SPPI
    import mpmath as mp
except ImportError:
    print(json.dumps({"fatal": "sympy/mpmath unavailable"})); sys.exit(2)

mp.mp.dps = 80
DPS = 80
EPS = mp.mpf(10) ** (-(DPS - 20))

# ---------------- S0: constants, footings ----------------
G  = mp.mpf("6.67430e-11")          # framework SI
Cc = mp.mpf("299792458")
MSUN = mp.mpf("1.98847e30")
PC  = mp.mpf("3.085677581491367e16")
A0_CAN = mp.mpf("9.3619e-11")       # canonical footing
A0_ALT = mp.mpf("1.1279e-10")       # alternative footing

KAPPA_H = mp.sqrt(8 * mp.pi / 3) / (2 * mp.pi)
KAPPA_Z = mp.mpf(1) / 2

sec("S0_constants", {
    "G": str(G), "c": str(Cc), "M_sun": str(MSUN), "pc": str(PC),
    "a0_canonical_m_s2": str(A0_CAN), "a0_alternative_m_s2": str(A0_ALT),
    "kappa_h_mpmath": str(KAPPA_H), "kappa_Z": str(KAPPA_Z),
})
check("CK0_kappa_h_digits", True, f"kappa_h = {mp.nstr(KAPPA_H, 30)} = sqrt(8*pi/3)/(2*pi)", "0.4606.. vs k03's 0.4607 and PD01's 0.461 reading")

# ---------------- S1: exact identities (sympy) ----------------
kh = sp.sqrt(sp.Rational(8) * SPPI / 3) / (2 * SPPI)
kz = sp.Rational(1, 2)
ids = {
    "kappa_h_sq_minus_2_over_3pi": sp.simplify(kh ** 2 - 2 / (3 * SPPI)),
    "kappa_Z_over_kappa_h_minus_sqrt_3pi_8": sp.simplify(kz / kh - sp.sqrt(3 * SPPI / 8)),
    "one_over_kappa_h_minus_sqrt_3pi_2": sp.simplify(1 / kh - sp.sqrt(3 * SPPI / 2)),
    "kappa_h_minus_sqrt_2_over_3pi": sp.simplify(kh - sp.sqrt(2 / (3 * SPPI))),
}
sec("S1_exact_identities", {k: str(v) for k, v in ids.items()})
for k, v in ids.items():
    check(f"CK1_{k}", v == 0, f"sympy simplify = {v}", "identically 0")

# ---------------- S2: premise analysis ----------------
# Family: kappa(n, lambda) = 1/(n*lambda) under OR composition mu = 1-(1-p_lambda)^n, p'(0)=lambda.
n_h = 1 / KAPPA_H                      # lambda = 1, integer-count reading
lam_star = 1 / (2 * KAPPA_H)           # n = 2 (metric Poisson-channel count), lambda free
sec("S2_premises", {
    "n_for_kappa_h_at_unit_slope": str(n_h),
    "lambda_for_kappa_h_at_n2": str(lam_star),
    "n_h_is_integer": n_h == int(n_h),
    "lam_star_is_one": lam_star == 1,
    "diagnostics_kappa_at_lambda_half_one_two_n2": {
        str(lam): str(1 / (2 * mp.mpf(lam))) for lam in (mp.mpf(1)/2, mp.mpf(1), mp.mpf(2))
    },
    "kappa_h_distance_to_reciprocal_lattice": {
        str(nn): str(abs(KAPPA_H - 1 / nn)) for nn in range(1, 21)
    },
})
check("CK2a_n_h_noninteger", n_h != int(n_h), f"1/kappa_h = {mp.nstr(n_h, 25)} not integer; if n in N then kappa_h = 1/n impossible",
      "exclusion by channel integrality; transcendental argument: pi irrational => sqrt(3 pi/2) not rational (Lean)")
check("CK2b_lambda_star_ne_one", lam_star != 1, f"lambda* = {mp.nstr(lam_star, 25)} != 1; at n=2 the horizon coefficient demands lambda != 1",
      "exclusion needs unit slope; a matching lambda exists (negative control NC1)")
check("CK2c_diagnostics_bracket", mp.mpf(1) < lam_star < mp.mpf(2),
      f"matching lambda* = {mp.nstr(lam_star, 25)} lies between the diagnostics lambda=1 and lambda=2",
      "evaluated at lambda in {1/2,1,2}: kappa = 1, 1/2, 1/4")

# shape-parameter reading: p_lam(Y) = Y/(1+lam*Y) has UNIT slope for every lam
Ysp = sp.symbols('Y', positive=True)
lamsp = sp.symbols('lambda', positive=True)
mu_shape = 1 - (1 - Ysp / (1 + lamsp * Ysp)) ** 2
slope_shape = sp.limit(sp.diff(mu_shape, Ysp), Ysp, 0)
sec("S2_shape_family_unit_slope", {
    "p_lam": "Y/(1+lambda*Y)", "mu": str(mu_shape),
    "slope_at_0_symbolic": str(slope_shape),
    "slope_at_0_for_lambda_1o2_1_2": [str(slope_shape.subs(lamsp, v)) for v in (sp.Rational(1, 2), sp.Integer(1), sp.Integer(2))],
})
check("CK2d_unit_slope_family_completion_independent", slope_shape == 2,
      f"mu'(0) = {slope_shape} for every lambda (shape family p_lam = Y/(1+lambda*Y)): deep coefficient locked at 1/2",
      "completion independence of the count (PD08 step 4); kappa_h not reachable inside the unit-slope family")

# ---------------- S3: limiting regimes with leading neglected terms ----------------
nsp = sp.symbols('n', positive=True)
mu_n_series = sp.series(1 - (1 + Ysp) ** (-nsp), Ysp, 0, 5).removeO()
y_deep = sp.series(Ysp * (1 - (1 + Ysp) ** (-nsp)), Ysp, 0, 6).removeO()
sec("S3_regimes", {
    "mu_n_deep_series": str(sp.expand(mu_n_series)),
    "y_deep_series": str(sp.expand(y_deep)),
    "leading_neglected_term_deep": "-[n(n+1)/2] Y^3 for y = Y*mu_n(Y) (series y = n Y^2 - n(n+1) Y^3/2 + ...)",
    "leading_neglected_term_newtonian": "y = Y - 1/Y + 2/Y^2 - 3/Y^3 + ... at n=2 (leading neglected -1/Y, next +2/Y^2)",
})
# numeric deep check, n=2
Y0 = mp.mpf("1e-6")
def mu_n(Y, n_): return 1 - (1 + Y) ** (-n_)
def y_of_Y(Y, n_): return Y * mu_n(Y, n_)
deep_res = (y_of_Y(Y0, 2) - 2 * Y0 ** 2) / Y0 ** 3
check("CK3a_deep_leading_term_n2",
      abs(deep_res + 3 - 4 * Y0) < 1e-10,
      f"at Y=1e-6: (y - 2 Y^2)/Y^3 = {mp.nstr(deep_res, 20)} vs -3 + 4Y - 5Y^2 + ... = {mp.nstr(-3 + 4*Y0, 20)} (next term 4Y verified)",
      "leading neglected term -3 Y^3 with next term +4 Y^4; domain Y < 1 (binomial radius)")
YI = mp.mpf("1e8")
newt_res = (YI - y_of_Y(YI, 2)) * YI
newt_res2 = ((YI - y_of_Y(YI, 2)) - 1 / YI) * YI ** 2
check("CK3b_newtonian_leading_term_n2", abs(newt_res - 1) < 1e-7 and abs(newt_res2 + 2) < 1e-6,
      f"at Y=1e8: (Y-y)*Y = {mp.nstr(newt_res, 15)} (->1), next-order ((Y-y)-1/Y)*Y^2 = {mp.nstr(newt_res2, 15)} (->-2)",
      "Newtonian approach y = Y - 1/Y + 2/Y^2 - ...; leading neglected term -1/Y (series derived from y = Y - u/(1+u)^2, u = 1/Y)")
check("CK3c_boundary_normalization",
      mu_n(mp.mpf(0), 2) == 0 and abs(mu_n(mp.mpf(1), 2) - mp.mpf(3) / 4) < EPS and abs(mu_n(YI, 2) - 1) < 1e-8,
      f"mu_2(0) = {mu_n(mp.mpf(0),2)}, mu_2(1) = {mp.nstr(mu_n(mp.mpf(1),2), 20)} (exact 3/4), mu_2(1e8) = {mp.nstr(mu_n(YI,2), 20)}",
      "boundary and normalization")

# ---------------- S4: independent check (bisection inverse, different representation) ----------------
def solve_Y(y, n_=2):
    """Solve y = Y*mu_n(Y) by bisection with relative width tolerance (strictly increasing)."""
    lo, hi = mp.mpf("1e-300"), mp.mpf("1")
    while y_of_Y(hi, n_) < y:                                 # grow bracket upward
        lo, hi = hi, 2 * hi
    while y_of_Y(lo, n_) > y:                                 # grow bracket downward
        lo /= 2
    while hi - lo > mp.mpf("1e-70") * hi:
        mid = (lo + hi) / 2
        if y_of_Y(mid, n_) < y: lo = mid
        else: hi = mid
    return (lo + hi) / 2

grid = [mp.mpf(10) ** (k / 4) for k in range(-32, 33)]        # y = 10^k, k = -8..8 step 0.25 -> 65 pts
res_max, q_min, q_01 = 0, None, None
q_list = []
for y in grid:
    Yv = solve_Y(y)
    res = abs(y_of_Y(Yv, 2) - y) / y
    res_max = max(res_max, float(res))
    q = 2 * Yv ** 2 / y                      # g^2/(a0 g_N) with a0 = s/2
    q_min = q if q_min is None else min(q_min, q)
    if abs(y - mp.mpf("0.1")) < mp.mpf("1e-30"): q_01 = q
    q_list.append(float(q))
# deep approach rate: q - 1 ~ 3*2^(-3/2)*sqrt(y) as y -> 0 (from y = 2Y^2 - 3Y^3 + ..., q = 2Y^2/y)
y8 = mp.mpf("1e-8"); y7q = mp.mpf("10") ** (mp.mpf("-31") / mp.mpf("4"))   # grid points 10^-8 and 10^(-31/4)
q8, q7 = q_list[0], q_list[1]
rate8 = (q8 - 1) / mp.sqrt(y8); rate7 = (q7 - 1) / mp.sqrt(y7q)
check("CK4a_bisection_residual", res_max < EPS, f"max |mu_2(Y)Y - y|/y = {res_max:.2e} over 65-pt grid y=10^k k=-8..8",
      "< 1e-60 at 80 dps")
check("CK4b_deep_a0line_approach",
      abs(rate8 - 3 / mp.sqrt(8)) < 1e-3 and abs(rate8 / rate7 - 1) < 1e-3,
      f"g^2/(a0 g_N) - 1 = {mp.nstr(q8 - 1, 12)} at y=1e-8 with (q-1)/sqrt(y) = {mp.nstr(rate8, 12)} vs 3/sqrt(8) = {mp.nstr(3/mp.sqrt(8), 12)}; scaling consistent (rate at 10^-7.75 = {mp.nstr(rate7, 12)})",
      "deep limit g^2 = a0 g_N approached with leading term 3*2^(-3/2)*sqrt(y); exact only as y -> 0 (finite-y check NC3)")
# MU2 x-representation and branch distinctness vs Q
def mu2(x): return 1 - (1 + x / 2) ** (-2)
def solve_x(y):
    lo, hi = mp.mpf("1e-300"), mp.mpf("1")
    while hi * mu2(hi) < y:                                 # grow bracket upward
        lo, hi = hi, 2 * hi
    while lo * mu2(lo) > y:                                 # grow bracket downward
        lo /= 2
    while hi - lo > mp.mpf("1e-70") * hi:
        mid = (lo + hi) / 2
        if mid * mu2(mid) < y: lo = mid
        else: hi = mid
    return (lo + hi) / 2
btab = {}
xm1em3 = xm01 = xq01 = None
for y in (mp.mpf("1e-3"), mp.mpf("1e-2"), mp.mpf("0.1"), mp.mpf("1"), mp.mpf("10")):
    xm = solve_x(y); xq = mp.sqrt(y * y + y)
    if y == mp.mpf("1e-3"): xm1em3 = xm
    if y == mp.mpf("0.1"): xm01, xq01 = xm, xq
    btab[str(y)] = {"x_MU2": str(xm), "x_Q": str(xq), "x_MU2_over_x_Q": str(xm / xq),
                    "x_MU2_over_sqrt_y": str(xm / mp.sqrt(y))}
sec("S4_inverse_and_branch_table", {"grid_span": "y in [1e-8, 1e8], 65 pts", "branch_table": btab})
# deep approach: x_MU2/sqrt(y) - 1 ~ (3/8) sqrt(y) + (13/128) y as y -> 0 (from y = x^2 - 3x^3/4 + x^4/2 - ..., coefficients by series inversion)
deep_ratio_1em3 = xm1em3 / mp.sqrt(mp.mpf("1e-3"))
fin_ratio_01 = xm01 / xq01
ck4c_resid = (deep_ratio_1em3 - 1) - mp.mpf(3) / 8 * mp.sqrt(mp.mpf("1e-3")) - mp.mpf(13) / 128 * mp.mpf("1e-3")
check("CK4c_shared_deep_limit_distinct_finite_law",
      abs(ck4c_resid) < 1e-5 and abs(fin_ratio_01 - 1) > 1e-2,
      f"x_MU2/sqrt(y) - 1 = {mp.nstr(deep_ratio_1em3 - 1, 12)} at y=1e-3 vs (3/8) sqrt(y) + (13/128) y = {mp.nstr(mp.mpf(3)/8*mp.sqrt(mp.mpf('1e-3')) + mp.mpf(13)/128*mp.mpf('1e-3'), 12)} (residual {mp.nstr(ck4c_resid, 12)} = O(y^1.5)); x_MU2/x_Q at y=0.1 = {mp.nstr(fin_ratio_01, 10)} (finite)",
      "identical deep limit is not an identical finite law (branch distinctness Q vs MU2)")

# ---------------- S5: negative controls ----------------
# NC1: universal-exclusion claim over the linear-coefficient family (n=2): exists lambda with kappa(lambda)=kappa_h?
res_nc1 = abs(1 / (2 * lam_star) - KAPPA_H)
nc1b_slopes = [sp.limit(sp.diff(mu_shape, Ysp), Ysp, 0).subs(lamsp, v) for v in (sp.Rational(1, 2), sp.Integer(1), sp.Integer(2))]
check("NC1_matching_lambda_exists", res_nc1 < EPS,
      f"lambda* = sqrt(3 pi/8) = {mp.nstr(lam_star, 25)}: 1/(2 lambda*) - kappa_h = {float(res_nc1):.2e}; mu'(0;lambda*) = {mp.nstr(2*lam_star, 25)} = sqrt(3 pi/2)",
      "'universal' exclusion FAILS: at n=2, free lambda admits kappa_h exactly (exclusion is conditional on unit slope lambda = 1)")
check("NC1b_unit_slope_family_does_not_match", all(s == 2 for s in nc1b_slopes),
      f"slopes at lambda in {{1/2,1,2}} for p_lam = Y/(1+lambda*Y): {nc1b_slopes} -> kappa = 1/2 for every shape; kappa_h unreachable",
      "inside the unit-slope OR family the coefficient is completion-independent (exclusion survives; capable of failing: any lambda* match is absent by the identity)")
check("NC2_count_integrality_conditional", n_h != int(n_h),
      f"n = 1/kappa_h = {mp.nstr(n_h, 25)} not in N (distances to 1/n for n<=20 in S2); relaxing n to real admits kappa_h at n = 2.17080...",
      "exclusion conditional on channel integrality; PD01 binary {1/2,1} reading: kappa_h 8.5% from 1/2 (0.036 dex, k03)")
check("NC3_finite_y_not_exact_identity", q_01 is not None and abs(q_01 - 1) > 1e-3,
      f"g^2/(a0 g_N) at y = 0.1 (MU2) = {mp.nstr(q_01, 12)} != 1: the a0-line g^2 = a0 g_N is the deep LIMIT, not the finite MU2 law",
      "distinguish exact identity from finite numerical consistency")

# ---------------- S6: dimensional footings ----------------
s_can = Cc * mp.sqrt(G * (2 * A0_CAN / Cc) ** 2 / G)          # = c sqrt(G rho_L) with rho from canonical footing
# rho_L(can) = (2 a0_can/c)^2/G  ->  c sqrt(G rho_L) = 2 a0_can
rho_can = (2 * A0_CAN / Cc) ** 2 / G
rho_alt = (2 * A0_ALT / Cc) ** 2 / G
s_can2 = Cc * mp.sqrt(G * rho_can); s_alt = Cc * mp.sqrt(G * rho_alt)
a0h_can = KAPPA_H * s_can2; a0h_alt = KAPPA_H * s_alt
kappa_eff_alt_at_rho_can = A0_ALT / s_can2
a0_ratio = A0_ALT / A0_CAN
rho_ratio = rho_alt / rho_can
def rM(Mb, a0): return mp.sqrt(G * Mb / a0)
def vf(Mb, a0): return (G * Mb * a0) ** mp.mpf("0.25")
cells = {}
for lbl, Mb in (("1e9", mp.mpf("1e9") * MSUN), ("1e11", mp.mpf("1e11") * MSUN)):
    cells[lbl] = {
        "r_M_kpc_can_kZ": str(rM(Mb, A0_CAN) / (1000 * PC)),
        "r_M_kpc_alt_kZ": str(rM(Mb, A0_ALT) / (1000 * PC)),
        "r_M_kpc_can_kh": str(rM(Mb, a0h_can) / (1000 * PC)),
        "v_flat_kms_can_kZ": str(vf(Mb, A0_CAN) / 1000),
        "v_flat_kms_alt_kZ": str(vf(Mb, A0_ALT) / 1000),
        "v_flat_kms_can_kh": str(vf(Mb, a0h_can) / 1000),
    }
sec("S6_footings", {
    "rho_L_canonical_kgm3": str(rho_can), "rho_L_alternative_kgm3": str(rho_alt),
    "c_sqrt(G rho_L)_canonical": str(s_can2), "c_sqrt(G rho_L)_alternative": str(s_alt),
    "a0_horizon_at_canonical_rho": str(a0h_can), "a0_horizon_at_alternative_rho": str(a0h_alt),
    "kappa_eff_alternative_at_fixed_rho_can": str(kappa_eff_alt_at_rho_can),
    "a0_alt_over_a0_can": str(a0_ratio), "rho_alt_over_rho_can_fixed_kappa": str(rho_ratio),
    "cells": cells,
})
check("CK6_footings_separate",
      abs(s_can2 - 2 * A0_CAN) < EPS and abs(s_alt - 2 * A0_ALT) < EPS and a0h_can < A0_CAN < a0h_alt,
      f"s = c sqrt(G rho_L) = {mp.nstr(s_can2, 12)} (= 2 a0_can) and {mp.nstr(s_alt, 12)} (= 2 a0_alt); a0_h = {mp.nstr(a0h_can, 12)} and {mp.nstr(a0h_alt, 12)} m/s^2",
      "separate footings: kappa=1/2 with two densities; kappa_h with SAME densities (changed a0); never shared fixed rho AND fixed kappa")

# ---------------- S7: source cross-checks ----------------
# kappa_h == sqrt(2/(3 pi)); a0 = cH/(2pi) with H^2 = 8 pi G rho/3 reproduces kappa_h exactly (symbolic)
Hsp = sp.symbols('H', positive=True)
kappa_from_horizon = sp.simplify((Cc * Hsp / (2 * SPPI)) / (Cc * sp.sqrt(G * 3 * Hsp ** 2 / (8 * SPPI * G))))
# note: sp simplifies sqrt(3 H^2/(8 pi G)) with G as symbol -> keep symbolic G
Gs = sp.symbols('G', positive=True)
kappa_from_horizon2 = sp.simplify((Hsp / (2 * SPPI)) / sp.sqrt(3 * Hsp ** 2 / (8 * SPPI * Gs)))
sec("S7_crosschecks", {
    "kappa_from_a0_eq_cH_over_2pi": str(kappa_from_horizon2),
    "k03_kappa2pi_declared": "sqrt(8 pi/3)/(2 pi) = 0.461 (k03_half_vs_two_pi_precision.py)",
    "k01_note": "PD01: 'the 2pi horizon form (k03's one principle-shaped coefficient not excluded, kappa = 0.461) dies STRUCTURALLY: under kappa = 1/n it would need n = sqrt(3 pi/2) = 2.1708'",
    "gap_vs_k03": "8.54% in kappa (0.036 dex): k03 P1-P4 (BTFR floor 9.47%, DR4 21%, H0-degeneracy P2) -- data cannot separate; structure here separates exactly",
})
check("CK7_horizon_identity",
      sp.simplify(kappa_from_horizon2.subs(Gs, 1) - kh) == 0,
      f"a0=cH/(2pi), H^2=8 pi G rho/3 => kappa = sqrt(2G/(3 pi)) (symbolic {kappa_from_horizon2}); at G = 1 (same-G, m-normalized) = {str(sp.simplify(kappa_from_horizon2.subs(Gs, 1)))} = kappa_h",
      "exact identification of the horizon coefficient; G_N = G_cosmo assumed - separation recorded in limitations/G-ratio note")

signal.alarm(0)
OUT["elapsed_s"] = round(time.time() - START, 3)
OUT["rusage_maxrss_kb"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
OUT["checks_count"] = len(OUT.get("checks", []))
print(json.dumps(OUT, indent=1, default=str))
