#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
KM3 -- C-H/K AT FIRST POST-NEWTONIAN ORDER: the second item on L340's open list ("the full 1PN metric of C-H/K
(beta_PPN, zetas) -- NOT computed").  Support computation for the lead track; no file of that track is edited.

WHY THE SOLAR SYSTEM REDUCES TO THE KHRONON SECTOR
  L340: on static slices K = 0, so the c_2 K^2 term and its first variation vanish; C-H's MOND sector acts on the
  heat-FILTERED field, which in the Solar System stays below the ephemeris floors (L340 S1: 0.031/0.045 pc canonical);
  L342's bound-region switch is fully on there (x ~ 1e6 >> x_c), so it changes nothing.  What is left at 1PN is the
  khronometric sector S = (1/16 pi G) Int N sqrt(gamma) [K_ij K^ij - (1 + c_2) K^2 + R3 + alpha_c a_i a^i], with the
  filtered MOND remainder as a bounded correction.

WHAT THIS LANE COMPUTES
  P1 gamma_PPN = 1: the static linear equations (KM1's, derived from the action) give lapse = spatial potential for
     any source without anisotropic stress; G_N = G/(1 - alpha_c/2).
  P2 beta_PPN = 1, DERIVED: the static spherically symmetric second-order field equations of the khronometric action
     (Euler-Lagrange, symbolic, isotropic gauge N = e^n, gamma_ij = e^{2 zeta} delta_ij), with the exterior fixed at
     first order by P1 (n = -m/r, zeta = m/r), force the O(m^2/r^2) coefficients: b(8 - 4 alpha_c) = 0 => b = 0 =>
     g_00 = -(1 - 2U + 2U^2) exactly as GR; zeta_2 = (alpha_c - 2)/8 (alpha_c = 0: -1/4, isotropic Schwarzschild).
  P3 alpha_1 = -4 alpha_c, alpha_2 = alpha_c (alpha_c - c_2)/(2 c_2) (BPS 2011 with beta = 0; reproduced against
     Yagi+14 by L333) across L340's window alpha_c in (1e-13, 3.2e-9), c_2 in (7.3e-3, 0.067), against LLR |alpha_1|
     < 1e-4 and pulsars |alpha_2| < 1.6e-9.
  P4 alpha_3 = zeta_1..4 = 0 (a diffeomorphism-invariant action is semi-conservative: Will, TEGP sec. 4.4) and
     xi = 0 (no Whitehead term in the khronometric action; Foster 2006 for the aether class) -- documentary.
  P5 Nordtvedt: eta_N = 4 beta - gamma - 3 - (10/3) xi - alpha_1 + (2/3) alpha_2 - (2/3) zeta_1 - (1/3) zeta_2
     = (11/3) alpha_c to leading order, against LLR |eta_N| < 4.4e-4; Mercury (2 + 2 gamma - beta)/3 = 1.
  P6 the filtered MOND remainder at 1PN: its Newtonian-order size is capped by L340's floors; its 1PN correction is
     that times U ~ 1e-8 -- documentary.
  MUTATE=1 imposes a Brans-Dicke-like exterior gamma = 2 in P2: the same equations then give beta = 3/2 and P2 must
  FAIL (rc = 1).

Run from the repository root:  python3 real_research/khronon_momentum_2026/KM3_chk_one_pn.py
"""
import os, sys, json, math
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "KM3_chk_one_pn"
P = lambda *a: print(*a, flush=True)
CH, OUT = [], {"lane": "KM3", "mutate": MUTATE, "checks": {}, "numbers": {}}


def check(name, measured, ok, reading="", load_bearing=True):
    ok = bool(ok)
    CH.append((name, ok, load_bearing))
    OUT["checks"][name] = {"ok": ok, "measured": str(measured), "load_bearing": load_bearing}
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def banner(t):
    P("\n" + "=" * 104); P(t); P("=" * 104)


# ============================================================================================ P1
banner("P1  gamma_PPN = 1 FROM THE STATIC LINEAR EQUATIONS (KM1's, from the action)")
k, G, al, rho = sp.symbols("k G alpha_c rho", positive=True)
ph, ps = sp.symbols("phi psi")
# KM1 static (omega = 0): Hamiltonian 4 k^2 psi - 2 alpha k^2 phi ... in Fourier with lap -> -k^2; trace eq: 4(-k^2 phi + k^2 psi) = 0
eqH = -16 * sp.pi * G * rho + 2 * al * k ** 2 * ph - 4 * k ** 2 * ps
eqT = -4 * k ** 2 * ph + 4 * k ** 2 * ps
s1 = sp.solve([eqH, eqT], [ph, ps], dict=True)[0]
phiN = -4 * sp.pi * G * rho / k ** 2
gamma_ppn = sp.simplify(s1[ps] / s1[ph])
GN_ratio = sp.simplify(s1[ph] / phiN)
P(f"    static solution: phi = {sp.factor(s1[ph])}, psi = {sp.factor(s1[ps])}  ->  psi/phi = {gamma_ppn}, "
  f"G_N/G = {GN_ratio}")
OUT["numbers"]["P1"] = {"gamma": str(gamma_ppn), "GN_over_G": str(GN_ratio)}
check("P1 static lapse = spatial potential => gamma_PPN = 1; Newton's constant renormalised G_N = G/(1 - alpha_c/2)",
      f"gamma = {gamma_ppn}; G_N/G = {GN_ratio}", gamma_ppn == 1 and sp.simplify(GN_ratio - 1 / (1 - al / 2)) == 0,
      "no anisotropic stress in the static khronometric sector")

# ============================================================================================ P2
banner("P2  beta_PPN FROM THE STATIC SECOND-ORDER FIELD EQUATIONS (derived symbolically)")
r, m, e = sp.symbols("r m e", positive=True)
n = sp.Function("n")(r); z = sp.Function("zeta")(r)
lapz = sp.diff(z, r, 2) + 2 * sp.diff(z, r) / r
# N sqrt(gamma)[R3 + alpha a^2] r^2 with N = e^n, gamma = e^{2 zeta} delta: R3 = -e^{-2 zeta}(4 lap zeta + 2 zeta'^2),
# a_i a^i = e^{-2 zeta} n'^2  ->  r^2 e^{n + zeta}[-(4 lap zeta + 2 zeta'^2) + alpha n'^2]
Lr = r ** 2 * sp.exp(n + z) * (-(4 * lapz + 2 * sp.diff(z, r) ** 2) + al * sp.diff(n, r) ** 2)
E_n, E_z = [ee.lhs for ee in sp.euler_equations(Lr, [n, z], [r])]
b, c1, d = sp.symbols("b c1 d")
c1_val = 2 if MUTATE else gamma_ppn                      # the exterior gamma fixed at first order by P1 (MUTATE: 2)
sub = {n: e * (-m / r) + e ** 2 * (b * m ** 2 / r ** 2), z: e * (c1 * m / r) + e ** 2 * (d * m ** 2 / r ** 2)}
orders = {}
for nm, E in (("E_n", E_n), ("E_z", E_z)):
    ser = sp.series(E.subs(sub).doit(), e, 0, 3).removeO()
    orders[nm] = [sp.simplify(ser.coeff(e, kk)) for kk in (1, 2)]
    P(f"    {nm}:  O(e) = {orders[nm][0]};  O(e^2) = {orders[nm][1]}")
eq2 = [sp.numer(sp.together(orders[nm][1])).subs(c1, c1_val) for nm in ("E_n", "E_z")]
sol2 = sp.solve(eq2, [b, d], dict=True)[0]
beta_ppn = sp.simplify(1 + sol2[b])
d_val = sp.simplify(sol2[d])
gr_ctrl = sp.simplify(d_val.subs(al, 0))
P(f"    with the exterior gamma = {c1_val}: b = {sol2[b]}, d = {d_val}  ->  beta_PPN = 1 + b = {beta_ppn}")
P(f"    GR control (alpha_c = 0): d = {gr_ctrl}  (isotropic Schwarzschild: e^(2 zeta) = (1 + m/2r)^4 -> d = -1/4)")
OUT["numbers"]["P2"] = {"first_order_identically_zero": all(orders[nm][0] == 0 for nm in orders),
                        "b": str(sol2[b]), "d": str(d_val), "beta": str(beta_ppn), "gamma_used": str(c1_val)}
check("P2 the static second-order field equations force b = 0: beta_PPN = 1 exactly for every alpha_c, and the "
      "alpha_c = 0 limit is isotropic Schwarzschild (d = -1/4)", f"beta = {beta_ppn}; d = {d_val}; GR d = {gr_ctrl}",
      beta_ppn == 1 and gr_ctrl == sp.Rational(-1, 4),
      "g_00 = -(1 - 2U + 2U^2) as in GR; the khronon's alpha a^2 term only renormalises G and the spatial O(U^2)")

# ============================================================================================ P3-P5
banner("P3-P5  THE PREFERRED-FRAME PARAMETERS, THE ZERO PARAMETERS, NORDTVEDT, MERCURY")
rows = {}
for acv in (1e-13, 1e-11, 3.2e-9):
    for c2v in (7.3e-3, 0.067):
        a1 = -4 * acv
        a2 = acv * (acv - c2v) / (2 * c2v)
        beta_v, gamma_v, xi_v, z1, z2 = 1.0, 1.0, 0.0, 0.0, 0.0
        etaN = 4 * beta_v - gamma_v - 3 - (10 / 3) * xi_v - a1 + (2 / 3) * a2 - (2 / 3) * z1 - (1 / 3) * z2
        rows[f"alpha_c={acv:g}/c2={c2v:g}"] = {"alpha1": a1, "alpha2": a2, "eta_N": etaN}
        P(f"    alpha_c = {acv:.1e}, c2 = {c2v:.1e}: alpha_1 = {a1:+.2e}, alpha_2 = {a2:+.2e}, eta_N = {etaN:+.2e}")
mercury = (2 + 2 * 1 - 1) / 3
bounds_ok = all(abs(v["alpha1"]) < 1e-4 and abs(v["alpha2"]) <= 1.6e-9 * 1.0001 and abs(v["eta_N"]) < 4.4e-4
                for v in rows.values())
P(f"    alpha_3 = zeta_1..4 = 0 (semi-conservative: covariant action); xi = 0 (no Whitehead term); "
  f"Mercury (2 + 2 gamma - beta)/3 = {mercury}")
OUT["numbers"]["P3_P5"] = {"rows": rows, "mercury_factor": mercury}
check("P3-P5 across L340's window: |alpha_1| <= 1.3e-8 (LLR 1e-4), |alpha_2| <= 1.6e-9 (pulsars, the window's own "
      "edge), eta_N = (11/3) alpha_c <= 1.2e-8 (LLR 4.4e-4); Mercury's factor exactly 1",
      {kk: f"a1 {v['alpha1']:.1e} a2 {v['alpha2']:.1e} etaN {v['eta_N']:.1e}" for kk, v in rows.items() if "3.2e-09" in kk},
      bounds_ok and mercury == 1.0, "the whole 1PN metric is GR's up to alpha_1, alpha_2 of order 1e-9")
check("P4 (documentary) alpha_3 = zeta_1..4 = 0 and xi = 0 for a diffeomorphism-invariant khronometric action",
      "Will TEGP sec. 4.4 (semi-conservative theories); Foster 2006 (aether class)", True, "", load_bearing=False)

# ============================================================================================ P6
banner("P6  THE FILTERED MOND REMAINDER AT 1PN (documentary)")
U_saturn = 6.674e-11 * 1.989e30 / (2.998e8 ** 2 * 9.58 * 1.496e11)
P(f"    U at Saturn = {U_saturn:.2e}: the MOND remainder's 1PN correction is (its Newtonian-order size, already inside")
P("    L340's ephemeris floors) x U ~ 1e-9 -- below every 1PN observable by many orders")
OUT["numbers"]["P6"] = {"U_saturn": U_saturn}
check("P6 (documentary) the filtered MOND remainder enters 1PN only as (floor-bounded anomaly) x U ~ 1e-9",
      f"U_Saturn = {U_saturn:.2e}", True, "", load_bearing=False)

# ============================================================================================ verdict
banner("VERDICT")
P("""  L340's second open item is closed at the level computed: in the Solar System C-H/K's 1PN metric is GR's.
  gamma_PPN = 1 and beta_PPN = 1 are DERIVED from the khronometric field equations (beta from the static second-order
  solution, with isotropic Schwarzschild as the control); alpha_3 = zeta_i = 0 and xi = 0 by the structure of the
  action; alpha_1 = -4 alpha_c and alpha_2 ~ -alpha_c/2 are <= 1e-8 across the window; Nordtvedt eta_N = (11/3) alpha_c.
  The filtered MOND remainder enters only at (floor) x U.  What stays open on L340's list: nonlinear
  well-posedness, the dark sector and clusters; FRW is being worked by L341-L342.""")

n_fail = sum(1 for _, ok, lb in CH if lb and not ok)
OUT["n_checks"], OUT["n_fail_load_bearing"] = len(CH), n_fail
outname = f"{SLUG}_results{'_MUTATE' if MUTATE else ''}.json"
json.dump(OUT, open(os.path.join(HERE, outname), "w"), indent=1, default=str)
P(f"\n  {sum(1 for _, ok, _ in CH if ok)}/{len(CH)} checks pass; load-bearing failures: {n_fail}; wrote {outname}")
sys.exit(0 if n_fail == 0 else 1)
