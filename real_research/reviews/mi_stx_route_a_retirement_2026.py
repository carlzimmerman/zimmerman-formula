#!/usr/bin/env python3
r"""mi_stx_route_a_retirement_2026.py -- LANE 7: the s^TX SME front UNDER ROUTE A. It should be RETIRED.

WHAT THIS IS. Route A (adopted 2026-08-02) replaces the framework's POWER-LAW approach to Newton with an
EXPONENTIAL one, nu(y) = 1/(1 - e^-sqrt(y)), y = g_bar/a0. Every kernel-dependent number in the corpus has to
be re-solved. This file re-solves ONE of them: the induced gravity-sector SME boost dipole s^TX, the "tightest
SME test" of the Lorentz-violation bridge.

THE COMMITTED STANDING THIS FILE UPDATES (and the things it does NOT resurrect):
  * "~9.6x" is RETRACTED. Not cited here except as a retracted label.
  * the frozen 1.50x / 1.24x margins were built on the RETIRED alpha=1 tail. They appear below ONLY as a
    NORMALISATION CONTROL, to prove this file reproduces the frozen ledger's normalisation before moving it.
  * under alpha=2 the margin collapsed to 1.03e6x / 7.09e5x (mi_stx_alpha2_collapse_2026.py) -- hugely SAFE,
    not live -- SIGN unchanged (NEGATIVE). Amendment 5 voided section 2's s^TX bands for that reason.
  * alpha2_MI ~ 1e-13 is ~1e6x SAFE and NOT live. "alpha2 ~ 1e-8 / LIVE" is a reverted double-count and is
    not used anywhere below.

THE RESULT, stated before the arithmetic so nothing hides:
  (a) Under Route A the Saturn-channel |s^TX| falls from 1.26e-15 (alpha=2) to 10^-363.6 (canonical) /
      10^-331.2 (alt). The margin against the 1.3e-9 combined bound goes 1.03e6x -> 10^354.8x (canonical) and
      7.09e5x -> 10^322.3x (alt). There is no single "suppression factor": the residual is exponential in
      sqrt(y), so the factor is body-dependent (1.3e-17 at the Sun's reflex, 10^-348 at Saturn).
  (b) The SIGN is UNCHANGED: NEGATIVE. nu > 1 for every y > 0 (manifestly: nu - 1 = 1/(e^sqrt(y) - 1) > 0), so
      the amplitude is strictly positive and the sign is carried entirely by n_X < 0 at the CMB apex.
  (c) THIS FRONT SHOULD BE FORMALLY RETIRED AS A DISCRIMINATOR, and this is a LOSS, not a win: a front that
      cannot fire is not a test. Even the single most generous evaluation available inside the solar system --
      the Sun's Jupiter-driven reflex, y ~ 2232, the very body that broke the alpha=2 ephemeris discharge --
      leaves 3.6e14x (canonical) / 5.2e12x (alt). To reach the bound at all you would need ranging-grade
      tracking of a body at r ~ 530-580 AU, i.e. ~55-60x Saturn's orbit. Keep the row only as a trivially
      satisfied CONSISTENCY row; delete it from any list of tests.
  (d) NO new SME coefficient is opened. Every channel in the corpus's own ledger (s^TT, the O(beta^2)
      quadrupole s^<JK>, the a0(z) secular drift, the annual sideband, the per-body 1/|a| slope law, the PPN
      alpha_2 / Nordtvedt row, and the GW-sector R3 row) carries the SAME prefactor A(body) = nu(y_body) - 1,
      so all of them die by the same hundreds of orders -- verified channel by channel below, not assumed.
      The ONE place where Route A's residual EXCEEDS the power law's is y <~ 97, which in the solar system
      means r >~ 800 AU: no published gravity-sector SME bound samples accelerations that low, so the window
      where the sharper kernel could have bitten is empty. What Route A DOES change qualitatively is the SHAPE
      of channel (v): the per-body law steepens from d ln|s^TX|/d ln g = -2 to -sqrt(y)/2 = -415 at Saturn, a
      ~208x sharper fingerprint -- on a 10^-364 signal. A sharper fingerprint on an unmeasurable amplitude is
      not a test either.

BOTH a0 FOOTINGS EVERYWHERE. canonical 9.3614e-11 (rho_DE / cH_Lambda, kappa = 1/2) and alt 1.13e-10
(rho_total / cH0). a0 is an INPUT; nothing here fits it. AND NOTE A REAL FINDING ABOUT THE SPREAD: because the
residual is exponential in sqrt(y), the footing fork -- worth 1.21x on a0 -- is worth 32.4 ORDERS OF MAGNITUDE
on this front. Any exponential-kernel statement about Newtonian-regime residuals is footing-sensitive to a
degree no power-law statement ever was.

Nothing frozen or committed was modified: the five-file hash manifest of mi_stx_alpha2_collapse_2026.py is
re-verified read-only at the end. Run: python3 real_research/reviews/mi_stx_route_a_retirement_2026.py
"""
from __future__ import annotations

import hashlib
import math
import os
import pathlib
import sys

import numpy as np
import sympy as sp
from scipy.optimize import brentq

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from mi_route_a_kernel import (A0_ALT, A0_CANON, log_nu_minus1, nu, nu_alpha1, nu_alpha2,  # noqa: E402
                               nu_minus1)

LN10 = math.log(10.0)

# ------------------------------------------------------------------ constants (SI unless flagged)
C = 299792458.0
G = 6.674e-11
GM_SUN = 1.32712440018e20
AU = 1.495978707e11
R_SUN = 6.957e8
KPC = 3.0856775814913673e19
V_CMB = 369.82e3                      # Planck 2018 dipole speed of the solar system
BETA = V_CMB / C
GAM2 = 1.0 / (1.0 - BETA**2)
SAT_A, SAT_E = 9.5826, 0.05415        # Saturn semi-major axis (the frozen ledger's value) and eccentricity

# the bounds each channel is judged against -- all published gravity-sector numbers, quoted as the corpus
# banked them (Hees+ 2016 review Table 9 for s^TX; the LLR/lab quadrupole rows from the SME data tables;
# Nordtvedt solar-spin for PPN alpha_2).
BOUND_STX = 1.3e-9
BOUND_QUAD = {"s^XX-YY": 2.0e-11, "s^XY": 7.7e-12, "s^XZ": 5.9e-12}
BOUND_ALPHA2 = 2.4e-7

FOOTINGS = (("canonical rho_DE/cH_L", A0_CANON), ("alt rho_total/cH0", A0_ALT))

# the frozen section-2 values, verbatim, carried ONLY as a normalisation control
STX_FROZEN_ALPHA1 = {"canonical rho_DE/cH_L": 8.68e-10, "alt rho_total/cH0": 1.048e-9}
MARGIN_FROZEN_ALPHA1 = {"canonical rho_DE/cH_L": 1.50, "alt rho_total/cH0": 1.24}
MARGIN_ALPHA2_ANCHOR = {"canonical rho_DE/cH_L": 1.03e6, "alt rho_total/cH0": 7.09e5}
Y_SUN_REFLEX_BANKED = 2236.0          # the committed ephemeris audit's Jupiter-dominated solar reflex, in a0

REPO = str(pathlib.Path(__file__).resolve().parents[2])
MANIFEST = {
    "prep_2026/gaia_dr4_prep/wide_binary_pipeline.py":
        "669fecc4b42b0f0a23c263715d45c3a56cca112af70fccdc4ed95696d53bb4ff",
    "prep_2026/gaia_dr4_prep/stx_dipole_template.py":
        "09cf51aef657292412ba0d647744b4470a0dcf58e6e192ba92475fe9930d506b",
    "real_research/reviews/wb_dr4_prereg_framework_curve.py":
        "6b8fad626067e076219f56309144b7d56c1050f129601b2d73f3286911ac3798",
    "real_research/reviews/stx_target.py":
        "1451b7810e48674f3d8759c484aee3bfd7b874836ca0e810de56d289bfab6987",
    "real_research/reviews/stx_inpop_recipe.py":
        "8227bea52b9aa070769b767070cbd0146709c8cafab42432448d4cacd7b7aab1",
}

_OK: list[tuple[bool, str]] = []


def check(cond, msg):
    cond = bool(cond)
    _OK.append((cond, msg))
    print(f"  [{'OK  ' if cond else 'FAIL'}] {msg}")


def banner(s):
    print("\n" + "=" * 108)
    print(s)
    print("=" * 108)


# ------------------------------------------------------------------ the three kernels' fractional residuals
def frac_route_a_log10(y):
    """log10 of the Route A fractional anomaly A = nu - 1 = 1/(e^sqrt(y) - 1). Never underflows."""
    return float(log_nu_minus1(y)) / LN10


def frac_alpha2(y):
    """alpha=2 fractional anomaly nu - 1, in a form that does not lose the digits to cancellation.

    nu = sqrt((1 + sqrt(1 + 4/y^2))/2), so nu - 1 = expm1(0.5 * log1p(t / (2 (sqrt(1+t) + 1)))), t = 4/y^2.
    The naive sqrt(...)/y - 1 keeps only ~4 digits at y ~ 1e6; this keeps all of them.
    """
    t = 4.0 / (y * y)
    return math.expm1(0.5 * math.log1p(t / (2.0 * (math.sqrt(1.0 + t) + 1.0))))


def frac_alpha1(y):
    return math.sqrt(1.0 + 1.0 / y) - 1.0


def g_of_r_au(r_au):
    return GM_SUN / (r_au * AU) ** 2


# ==================================================================================================
def s0_footings_and_apex():
    banner("S0. FOOTINGS, THE PREFACTOR, AND THE APEX DIRECTION (re-derived, not copied)")
    R_eq2gal = np.array([[-0.0548755604, -0.8734370902, -0.4838350155],
                         [+0.4941094279, -0.4448296300, +0.7469822445],
                         [-0.8676661490, -0.1980763734, +0.4559837762]])
    l, b = math.radians(264.021), math.radians(48.253)
    n_gal = np.array([math.cos(b) * math.cos(l), math.cos(b) * math.sin(l), math.sin(b)])
    n_eq = R_eq2gal.T @ n_gal
    ra = math.degrees(math.atan2(n_eq[1], n_eq[0])) % 360.0
    dec = math.degrees(math.asin(n_eq[2]))
    print(f"  Planck apex (l,b) = (264.021, 48.253) deg  ->  equatorial RA = {ra:.3f}, Dec = {dec:.3f} deg")
    print(f"  n_hat(SCF) = ({n_eq[0]:+.5f}, {n_eq[1]:+.5f}, {n_eq[2]:+.5f}),  |n| = {np.linalg.norm(n_eq):.9f}")
    print(f"  beta_cmb = {BETA:.6e}, gamma^2 = {GAM2:.9f}, prefactor gamma^2 beta |n_X| = "
          f"{GAM2 * BETA * abs(n_eq[0]):.6e}")
    check(abs(ra - 167.94) < 0.2 and abs(dec + 6.94) < 0.2 and abs(np.linalg.norm(n_eq) - 1.0) < 1e-8,
          f"the apex direction re-derives from the Planck dipole through the IAU rotation to RA = {ra:.2f}, "
          f"Dec = {dec:.2f} deg, matching the ledger's 167.94/-6.94, and n_hat is a unit vector -- so the "
          f"geometry factor below is this file's own, not inherited")
    check(A0_ALT / A0_CANON > 1.0 and abs(A0_ALT / A0_CANON - 1.2071) < 0.01,
          f"both footings carried as INPUTS: canonical {A0_CANON:.4e}, alt {A0_ALT:.4e}, ratio "
          f"{A0_ALT / A0_CANON:.4f}. Neither is fitted anywhere in this file")
    return n_eq


# ==================================================================================================
def s1_the_tail_is_not_a_power_law():
    banner("S1. ROUTE A's NEWTONIAN TAIL IS EXPONENTIAL IN sqrt(y) -- shown symbolically, with a control")
    y = sp.Symbol("y", positive=True)
    a_exp = 1 / (sp.exp(sp.sqrt(y)) - 1)                         # Route A: nu - 1, exactly
    a_al2 = sp.sqrt((y**2 + y * sp.sqrt(y**2 + 4)) / 2) / y - 1  # alpha=2: nu - 1
    a_al1 = sp.sqrt(1 + 1 / y) - 1                               # alpha=1: nu - 1

    lim_exp = sp.limit(a_exp * sp.exp(sp.sqrt(y)), y, sp.oo)
    lim_al2 = sp.limit(a_al2 * y**2, y, sp.oo)
    lim_al1 = sp.limit(a_al1 * y, y, sp.oo)
    print(f"    Route A : lim (nu-1) e^sqrt(y) = {lim_exp}      => A = e^-sqrt(y) (1 + ...)")
    print(f"    alpha=2 : lim (nu-1) y^2      = {lim_al2}      => A = 1/(2 y^2) = a0^2/(2 g^2)")
    print(f"    alpha=1 : lim (nu-1) y        = {lim_al1}      => A = 1/(2 y)   = a0/(2 g)")
    check(sp.simplify(lim_exp - 1) == 0 and sp.simplify(lim_al2 - sp.Rational(1, 2)) == 0
          and sp.simplify(lim_al1 - sp.Rational(1, 2)) == 0,
          f"the three tails are A_RouteA -> e^-sqrt(y), A_2 -> 1/(2y^2), A_1 -> 1/(2y). The frozen "
          f"pre-registration's amplitude is built on A_1; the kernel in force before today was A_2; Route A "
          f"is neither -- it is not a power law at all, so the front cannot be rescaled and must be re-solved")

    # MUTATION CONTROL: the power-law diagnostics must NOT be satisfied by the exponential tail
    lim_mut = sp.limit(a_exp * y**2, y, sp.oo)
    lim_mut2 = sp.limit(a_al2 * sp.exp(sp.sqrt(y)), y, sp.oo)
    check(lim_mut == 0 and lim_mut2 == sp.oo,
          f"MUTATION: the alpha=2 diagnostic y^2 (nu-1) applied to Route A gives {lim_mut} (not 1/2) and the "
          f"Route A diagnostic e^sqrt(y) (nu-1) applied to alpha=2 DIVERGES -- the two diagnostics genuinely "
          f"separate the kernels, so S1 is a discriminating statement and not one both kernels satisfy")


# ==================================================================================================
def s2_normalisation_controls(n_eq):
    banner("S2. NORMALISATION CONTROLS -- reproduce the FROZEN alpha=1 numbers and the alpha=2 collapse")
    print("  (The alpha=1 row is the RETIRED kernel and its 1.50x/1.24x must NEVER be cited as a live")
    print("   margin. It is here for one purpose: to prove this file is on the frozen ledger's")
    print("   normalisation before it moves the number.)")
    pref = GAM2 * BETA * abs(n_eq[0])
    g_sat = g_of_r_au(SAT_A)
    print(f"\n  Saturn: a = {SAT_A} AU, g_orb = {g_sat:.6e} m/s^2")
    print(f"  {'footing':<24s} {'y = g/a0':>12s} {'|s^TX| a=1':>12s} {'margin a=1':>11s} "
          f"{'|s^TX| a=2':>12s} {'margin a=2':>12s}")
    rows = {}
    for fname, a0 in FOOTINGS:
        y = g_sat / a0
        s1 = frac_alpha1(y) * pref
        s2 = frac_alpha2(y) * pref
        rows[fname] = (y, s1, BOUND_STX / s1, s2, BOUND_STX / s2)
        print(f"  {fname:<24s} {y:12.5e} {s1:12.4e} {BOUND_STX / s1:11.3f} {s2:12.4e} "
              f"{BOUND_STX / s2:12.4e}")

    d1 = max(abs(rows[f][1] / STX_FROZEN_ALPHA1[f] - 1.0) for f, _ in FOOTINGS)
    m1 = max(abs(rows[f][2] / MARGIN_FROZEN_ALPHA1[f] - 1.0) for f, _ in FOOTINGS)
    check(d1 < 0.02 and m1 < 0.02,
          f"CONTROL 1: the retired alpha=1 amplitudes reproduce the frozen section-2 values 8.68e-10 / "
          f"1.048e-9 to {d1 * 100:.2f}% and their margins to {m1 * 100:.2f}% of the frozen 1.50x/1.24x -- "
          f"this file's geometry, prefactor and bound are the ledger's own")
    m2 = max(abs(rows[f][4] / MARGIN_ALPHA2_ANCHOR[f] - 1.0) for f, _ in FOOTINGS)
    check(m2 < 0.02,
          f"CONTROL 2: the alpha=2 margins reproduce mi_stx_alpha2_collapse_2026.py's 1.03e6x / 7.09e5x to "
          f"{m2 * 100:.2f}% -- so the Route A number below is comparable to the committed one by "
          f"construction, and the 1.03e6x baseline this lane is asked to move is verified rather than quoted")
    # the stabilised alpha=2 residual must agree with the module's own kernel where float64 can hold it
    worst = max(abs(frac_alpha2(yv) / (float(nu_alpha2(yv)) - 1.0) - 1.0) for yv in (1e1, 1e2, 1e3, 1e4))
    check(worst < 1e-6,
          f"the cancellation-free alpha=2 residual used here agrees with the kernel module's nu_alpha2 to "
          f"{worst:.1e} at y = 10-1e4, where the naive subtraction still has digits; at Saturn's y = 6.9e5 "
          f"the naive form keeps only ~4, which is why the stable form is used")
    return pref, g_sat, rows


# ==================================================================================================
def s3_route_a_margin(pref, g_sat):
    banner("S3. *** THE ROUTE A s^TX MARGIN, BOTH FOOTINGS -- and the float64 trap made explicit ***")
    y_can = g_sat / A0_CANON
    naive = float(nu(y_can)) - 1.0
    under = float(nu_minus1(y_can))
    logv = float(log_nu_minus1(y_can))
    print(f"  At Saturn's y = {y_can:.5e} (canonical footing), sqrt(y) = {math.sqrt(y_can):.2f}:")
    print(f"    nu(y) - 1        = {naive:.1f}          <- the subtraction is DEAD (1 - e^-830 is 1.0)")
    print(f"    nu_minus1(y)     = {under:.1e}          <- e^-830 is below float64's smallest normal: UNDERFLOW")
    print(f"    log_nu_minus1(y) = {logv:.4f}    <- the only representation that carries the number")
    check(naive == 0.0 and under == 0.0 and math.isfinite(logv)
          and abs(logv + math.sqrt(y_can)) < 1e-9,
          f"the trap this lane was warned about bites EXACTLY here: at Saturn both nu(y)-1 and nu_minus1(y) "
          f"read as exactly 0.0, and only log_nu_minus1 = {logv:.2f} (= -sqrt(y) to 1e-9) survives. Any s^TX "
          f"statement made through a linear-space residual would have reported a spurious identically-zero "
          f"amplitude and an infinite margin")

    print(f"\n  {'footing':<24s} {'y':>12s} {'log10 A':>10s} {'log10|s^TX|':>12s} {'log10 margin':>13s} "
          f"{'vs alpha=2':>12s}")
    out = {}
    for fname, a0 in FOOTINGS:
        y = g_sat / a0
        lA = frac_route_a_log10(y)
        lS = lA + math.log10(pref)
        lM = math.log10(BOUND_STX) - lS
        gain = lM - math.log10(MARGIN_ALPHA2_ANCHOR[fname])
        out[fname] = (y, lA, lS, lM, gain)
        print(f"  {fname:<24s} {y:12.5e} {lA:10.2f} {lS:12.2f} {lM:13.2f} {gain:>+12.2f} dex")

    lm_can, lm_alt = out[FOOTINGS[0][0]][3], out[FOOTINGS[1][0]][3]
    check(lm_can > 100 and lm_alt > 100,
          f"*** VERIFIED, NOT ASSUMED: under Route A the Saturn-channel margin is 10^{lm_can:.2f} x "
          f"(canonical) and 10^{lm_alt:.2f} x (alt) against the 1.3e-9 combined bound. |s^TX| itself is "
          f"10^{out[FOOTINGS[0][0]][2]:.2f} / 10^{out[FOOTINGS[1][0]][2]:.2f}. The alpha=2 collapse to 1.03e6x "
          f"was already a dead front; Route A makes it dead by a further "
          f"{out[FOOTINGS[0][0]][4]:.0f}-{out[FOOTINGS[1][0]][4]:.0f} orders ***")
    check(lm_alt < lm_can and (lm_can - lm_alt) > 10.0,
          f"THE FOOTING SPREAD IS THE REAL SURPRISE, and it is reported because it is true, not because it "
          f"helps: a 1.21x fork on a0 is worth {lm_can - lm_alt:.1f} ORDERS OF MAGNITUDE here (the alt "
          f"footing, with the LARGER a0, is the less safe one). Because the residual is e^-sqrt(g/a0), every "
          f"exponential-kernel statement about a Newtonian-regime residual is footing-sensitive to a degree "
          f"no power-law statement ever was -- a single-footing number on this front is meaningless")
    print("\n  AND THERE IS NO SINGLE 'SUPPRESSION FACTOR' -- the lane brief's ~1e13 is a body-dependent")
    print("  quantity, not a constant, because e^-sqrt(y) is not a power law. Route A / alpha=2 on the")
    print("  FRACTIONAL residual:")
    for label, gg in (("Sun's Jupiter reflex", Y_SUN_REFLEX_BANKED * A0_CANON),
                      ("Saturn orbit", g_sat), ("Earth orbit", g_of_r_au(1.0)),
                      ("lab surface gravity", 9.81)):
        yv = gg / A0_CANON
        r = frac_route_a_log10(yv) - math.log10(frac_alpha2(yv))
        print(f"    {label:<22s} y = {yv:10.3e}   log10(A_RouteA / A_alpha2) = {r:+11.2f}")
    return out


# ==================================================================================================
def s4_the_sign(n_eq):
    banner("S4. THE SIGN: still NEGATIVE, and it is the geometry that carries it (amplitude is positive)")
    A, beta, nx = sp.symbols("A beta n_x", real=True)
    gam = 1 / sp.sqrt(1 - beta**2)
    P_TX = sp.simplify(gam**2 * beta * nx)                    # from s^munu = A (u^mu u^nu + eta^munu/4)
    print(f"  spurion: s^munu = A (u^mu u^nu + eta^munu/4), u = gamma(1, beta n) -> s^TX = A * {P_TX}")
    check(sp.simplify(sp.diff(P_TX, nx) - gam**2 * beta) == 0,
          "s^TX = A gamma^2 beta n_X is LINEAR in n_X with a positive coefficient gamma^2 beta, so the sign "
          "of s^TX is the sign of (A * n_X) and nothing else")

    y = sp.Symbol("y", positive=True)
    ident = sp.simplify((1 / (1 - sp.exp(-sp.sqrt(y))) - 1) - 1 / (sp.exp(sp.sqrt(y)) - 1))
    grid = np.logspace(-8, 12, 4001)
    lg = log_nu_minus1(grid)
    check(ident == 0 and bool(np.all(np.isfinite(lg))),
          f"the Route A amplitude is STRICTLY POSITIVE for every y > 0, proved analytically rather than "
          f"numerically: nu - 1 = 1/(e^sqrt(y) - 1) identically ({ident} residual), and e^sqrt(y) > 1 for all "
          f"y > 0. Corroborated in the only representation float64 can hold: log_nu_minus1 is finite across "
          f"twenty decades (a finite logarithm IS strict positivity, whereas the linear value reads 0.0)")
    check(n_eq[0] < 0,
          f"n_X = {n_eq[0]:+.5f} < 0 at the CMB apex, so s^TX = (positive A) x (positive gamma^2 beta) x "
          f"(negative n_X) is NEGATIVE. THE PRE-REGISTERED SIGN IS UNCHANGED BY ROUTE A -- only the "
          f"amplitude moved, exactly as it was under alpha=2")

    # MUTATION: the antipodal apex must flip the sign, or the sign statement is vacuous
    R = np.array([[-0.0548755604, -0.8734370902, -0.4838350155],
                  [+0.4941094279, -0.4448296300, +0.7469822445],
                  [-0.8676661490, -0.1980763734, +0.4559837762]])
    l2, b2 = math.radians(264.021 + 180.0), math.radians(-48.253)
    n2 = R.T @ np.array([math.cos(b2) * math.cos(l2), math.cos(b2) * math.sin(l2), math.sin(b2)])
    check(n2[0] > 0 and n_eq[0] * n2[0] < 0,
          f"MUTATION: the ANTIPODAL apex gives n_X = {n2[0]:+.5f} > 0 and hence a POSITIVE s^TX, so the "
          f"negative-sign check is sensitive to the direction it claims to test and is not satisfied by any "
          f"apex whatsoever")


# ==================================================================================================
def s5_can_it_ever_fire(pref, g_sat):
    banner("S5. CAN THIS FRONT EVER FIRE? Three independent generosity limits, all of them still safe")
    print("  (This is the retirement argument, and it is deliberately built to be as GENEROUS to the front")
    print("   as the physics allows. If a maximally generous evaluation still cannot reach the bound, the")
    print("   front cannot fire -- and that is a LOSS of a falsifier, not a success.)")

    # (1) most generous WELL-TRACKED point: Saturn at APHELION (the weakest field on the outermost orbit
    #     with metre-level ranging)
    print(f"\n  (1) Saturn APHELION (e = {SAT_E}) -- the weakest field on the outermost metre-level-ranged orbit")
    lm_aph = {}
    for fname, a0 in FOOTINGS:
        y_ap = g_of_r_au(SAT_A * (1 + SAT_E)) / a0
        lm = math.log10(BOUND_STX) - (frac_route_a_log10(y_ap) + math.log10(pref))
        lm_aph[fname] = lm
        print(f"      {fname:<24s} y_aph = {y_ap:.4e}   log10 margin = {lm:8.2f}")
    check(min(lm_aph.values()) > 100,
          f"even at Saturn APHELION -- and the exponential kernel makes the orbital swing enormous in "
          f"RELATIVE terms -- the margin is still 10^{min(lm_aph.values()):.0f} x. Choosing the most "
          f"favourable phase of the most favourable tracked orbit buys ~20 dex out of ~355 needed")

    # (2) most generous BODY in the solar system: the Sun's own Jupiter-driven reflex -- the body that broke
    #     the alpha=2 ephemeris discharge, i.e. the corpus's own worst case
    GM_J = G * 1.8982e27
    a_sun_J = GM_J / (5.2044 * AU) ** 2
    y_sun_banked_check = a_sun_J / A0_CANON
    print(f"\n  (2) the SUN's Jupiter-driven reflex a = {a_sun_J:.4e} m/s^2 -- the binding body of the "
          f"alpha=2 liability")
    check(abs(y_sun_banked_check / Y_SUN_REFLEX_BANKED - 1.0) < 0.01,
          f"cross-check against the committed ephemeris audit: the Jupiter-only solar reflex is "
          f"{y_sun_banked_check:.1f} a0, within {abs(y_sun_banked_check / Y_SUN_REFLEX_BANKED - 1) * 100:.2f}% "
          f"of that audit's banked {Y_SUN_REFLEX_BANKED:.0f} a0 -- so this generosity limit is anchored to the "
          f"corpus's own worst case rather than invented")
    m_sun = {}
    for fname, a0 in FOOTINGS:
        y = a_sun_J / a0
        lS = frac_route_a_log10(y) + math.log10(pref)
        m_sun[fname] = math.log10(BOUND_STX) - lS
        print(f"      {fname:<24s} y_sun = {y:8.1f}   |s^TX| = 10^{lS:6.2f} = {10 ** lS:.2e}   "
              f"margin = {10 ** m_sun[fname]:.2e} x")
    check(min(m_sun.values()) > 10.0,          # m_sun holds log10 margins
          f"THE STRONGEST FORM OF THE RETIREMENT ARGUMENT: adopt the single most generous body in the solar "
          f"system -- the Sun's reflex, the very body whose 1/g tail left alpha=2 8.5-12.4x OVER the Mars "
          f"budget -- and Route A still leaves {10 ** m_sun[FOOTINGS[0][0]]:.1e} x (canonical) / "
          f"{10 ** m_sun[FOOTINGS[1][0]]:.1e} x (alt). The channel that breaks the ephemeris front cannot "
          f"even approach the SME front")

    # (3) what would it TAKE? invert |s^TX| = bound for the heliocentric radius
    print("\n  (3) INVERT THE QUESTION: at what heliocentric distance would |s^TX| reach 1.3e-9?")
    r_fire = {}
    for fname, a0 in FOOTINGS:
        target = BOUND_STX / pref                                  # required A
        s_req = math.log1p(1.0 / target)                           # A = 1/(e^s - 1) -> s = ln(1 + 1/A)
        y_req = s_req**2
        r_fire[fname] = math.sqrt(GM_SUN / (y_req * a0)) / AU
        print(f"      {fname:<24s} needs A = {target:.4e} -> y = {y_req:.2f} -> r = {r_fire[fname]:.1f} AU "
              f"({r_fire[fname] / SAT_A:.1f} x Saturn)")
    check(min(r_fire.values()) > 300.0 and min(r_fire.values()) / SAT_A > 30.0,
          f"to make this front live at all you would need ranging-grade tracking of a body at r = "
          f"{r_fire[FOOTINGS[1][0]]:.0f}-{r_fire[FOOTINGS[0][0]]:.0f} AU, i.e. "
          f"{min(r_fire.values()) / SAT_A:.0f}-{max(r_fire.values()) / SAT_A:.0f} x Saturn's orbit. No such "
          f"data exists or is planned; the outermost metre-level ranging is Cassini at 9.58 AU. RECOMMENDATION"
          f": RETIRE s^TX as a discriminator and keep it only as a trivially satisfied consistency row")
    return m_sun, r_fire


# ==================================================================================================
def s6_other_channels(pref, n_eq):
    banner("S6. (d) DOES THE SHARPER KERNEL OPEN ANY OTHER SME CHANNEL? Channel-by-channel, both footings")
    print("  Every channel the corpus itself enumerated is re-priced. Test applied: does Route A give a")
    print("  SMALLER margin than alpha=2 anywhere? If yes, that channel is opened by the kernel switch.")
    nx, ny, nz = n_eq
    chans = []
    # 1. the s^TX dipole itself
    chans.append(("s^TX dipole (Saturn)", g_of_r_au(SAT_A), GAM2 * BETA * abs(nx), BOUND_STX))
    # 2. the O(beta^2) quadrupole companions, at Saturn
    for nm, geo in (("s^XX-YY quad (Saturn)", abs(nx**2 - ny**2)), ("s^XY quad (Saturn)", abs(nx * ny)),
                    ("s^XZ quad (Saturn)", abs(nx * nz))):
        chans.append((nm, g_of_r_au(SAT_A), BETA**2 * geo, BOUND_QUAD[nm.split()[0]]))
    # 3. PPN alpha_2 / Nordtvedt: set by the SUN's INTERNAL self-gravity, not an orbit
    chans.append(("PPN alpha_2 (solar g_int)", GM_SUN / R_SUN**2, 1.0, BOUND_ALPHA2))
    # 4. the GW-sector row: gw_sme_door's R3 reading -- coefficient set at the matter the wave touches
    chans.append(("GW d=4 aniso (lab g, R3)", 9.81, GAM2 * BETA * abs(nx), 1e-14))
    print(f"\n  {'channel':<26s} {'footing':<10s} {'log10 marg a=1':>14s} {'log10 marg a=2':>14s} "
          f"{'log10 marg RouteA':>18s} {'opened?':>8s}")
    opened = []
    for nm, gg, geo, bnd in chans:
        for fshort, a0 in (("canon", A0_CANON), ("alt", A0_ALT)):
            y = gg / a0
            l1 = math.log10(bnd) - math.log10(frac_alpha1(y) * geo)
            l2 = math.log10(bnd) - math.log10(frac_alpha2(y) * geo)
            lA = math.log10(bnd) - (frac_route_a_log10(y) + math.log10(geo))
            op = lA < l2
            opened.append(op)
            print(f"  {nm:<26s} {fshort:<10s} {l1:14.2f} {l2:14.2f} {lA:18.2f} {'YES' if op else 'no':>8s}")
    check(not any(opened),
          f"NO CHANNEL IS OPENED: across {len(opened)} channel-footing pairs -- the s^TX dipole, all three "
          f"O(beta^2) quadrupole companions, the PPN alpha_2 / Nordtvedt row and the GW-sector R3 row -- Route "
          f"A's margin is LARGER than alpha=2's in every single case. The reason is structural, not lucky: "
          f"every one of these carries the SAME prefactor A(body) = nu(y_body) - 1, and every one of them "
          f"lives at y >> 100")
    print("  Channels that scale with the SAME A and therefore need no separate row: the a0(z) secular drift")
    print("  of s^TX (already 1e9x too small under alpha=1), the annual sideband (~8% of the DC value, and")
    print("  the extraction method rather than a coefficient), and s^TT (absorbable, 3A/4). The matter-sector")
    print("  c_munu / b_mu / k_AF channels are forbidden by structure (co-located-species cancellation and")
    print("  the even-in-u kernel), which is a kernel-INDEPENDENT argument and is unaffected either way.")

    # WHERE COULD A SHARPER KERNEL HAVE BITTEN? the crossover, computed
    print("\n  THE WINDOW WHERE ROUTE A *IS* LARGER THAN THE POWER LAW, and whether any bound lives in it:")
    f = lambda yv: frac_route_a_log10(yv) - math.log10(frac_alpha2(yv))
    y_cross = brentq(f, 5.0, 1e4, xtol=1e-10)
    print(f"    A_RouteA > A_alpha2 for y < y_cross = {y_cross:.2f}  (checked: f(10) = {f(10.0):+.3f} > 0, "
          f"f(1e3) = {f(1e3):+.3f} < 0)")
    for fshort, a0 in (("canon", A0_CANON), ("alt", A0_ALT)):
        r_x = math.sqrt(GM_SUN / (y_cross * a0)) / AU
        print(f"    {fshort:<6s}: y_cross corresponds to a heliocentric r = {r_x:.0f} AU "
              f"({r_x / SAT_A:.0f} x Saturn)")
    check(f(10.0) > 0 and f(1e3) < 0 and 10.0 < y_cross < 1e4
          and math.sqrt(GM_SUN / (y_cross * A0_CANON)) / AU > 100.0,
          f"the sharper kernel's residual DOES exceed the power law's -- but only for y < {y_cross:.0f}, which "
          f"in the solar system means r > {math.sqrt(GM_SUN / (y_cross * A0_CANON)) / AU:.0f} AU. Every "
          f"gravity-sector SME bound in existence samples y >= 2200 (the Sun's reflex) and typically y ~ 1e6 "
          f"-1e11. THE WINDOW WHERE A SHARPER TRANSITION COULD HAVE OPENED A CHANNEL IS OBSERVATIONALLY EMPTY "
          f"-- I looked for the new channel this lane asked about and there is not one")

    # THE ONE READING THAT WOULD FIRE -- and the honest reason it is not adopted
    print("\n  BOTH WAYS, the one reading under which ANY of these fires -- and why it is not Route A's doing:")
    v_gal, R0 = 233e3, 8.178 * KPC
    g_gal = v_gal**2 / R0
    print(f"    galactic external field g_gal = v^2/R0 = {g_gal:.4e} m/s^2 (v = 233 km/s, R0 = 8.178 kpc)")
    over = {}
    for fshort, a0 in (("canon", A0_CANON), ("alt", A0_ALT)):
        y = g_gal / a0
        AA = float(nu_minus1(y))
        A1 = frac_alpha1(y)
        A2 = frac_alpha2(y)
        over[fshort] = (AA * pref / BOUND_STX, A1 * pref / BOUND_STX, A2 * pref / BOUND_STX)
        print(f"    {fshort:<6s}: y = {y:.3f}  ->  A_RouteA = {AA:.4f} ({over[fshort][0]:.2e} x OVER the "
              f"bound), A_alpha1 = {A1:.4f} ({over[fshort][1]:.2e} x), A_alpha2 = {A2:.4f} "
              f"({over[fshort][2]:.2e} x)")
    ratio = over["canon"][0] / over["canon"][2]
    check(all(v[0] > 1 and v[1] > 1 and v[2] > 1 for v in over.values()) and ratio < 1e2,
          f"HONEST BOTH-WAYS ROW, reported because it is the one number that could be spun as a deficit: if "
          f"one fed the spurion the GALACTIC external field instead of the body's own orbital acceleration, "
          f"|s^TX| would be {over['canon'][0]:.1e} x OVER the bound -- but so would alpha=1 "
          f"({over['canon'][1]:.1e} x) and alpha=2 ({over['canon'][2]:.1e} x), Route A being worse than "
          f"alpha=2 by only {ratio:.1f} x. So that reading is excluded for ALL THREE kernels equally, which "
          f"is gw_sme_door.py's own R1 argument that a constant-background reading MIS-MAPS an "
          f"acceleration-dependent test-body coupling. It is NOT a Route A opening and must not be sold as "
          f"one -- and equally it must not be hidden")
    return y_cross


# ==================================================================================================
def s7_the_slope_law(pref):
    banner("S7. WHAT ROUTE A *DOES* CHANGE: the per-body slope law, the corpus's own 'genuinely fresh' channel")
    print("  vein4_sme_fresh_channels.py graded the per-body law s^TX(body) ∝ 1/|a| as the one fresh,")
    print("  MI-flavoured test (a constant-background SME gives the SAME s^TX for every body). Route A")
    print("  replaces that mild law with an exponential one, so the FINGERPRINT gets much sharper while the")
    print("  AMPLITUDE dies. Sharper shape on an unmeasurable signal is still not a test.")
    print(f"\n  {'body':<10s} {'r [AU]':>8s} {'y':>11s} {'log10|s^TX| RouteA':>20s} {'|s^TX| alpha=2':>15s} "
          f"{'dln|s|/dln g':>13s}")
    # d ln A / d ln g = -(sqrt(y)/2) e^s/(e^s - 1) = -(sqrt(y)/2) / (1 - e^-s): the SECOND form never
    # overflows (e^830 does), which is the same float64 lesson one level up in the derivative.
    slope_of_y = lambda yv: -0.5 * math.sqrt(yv) / -math.expm1(-math.sqrt(yv))
    slopes = {}
    for nm, r in (("Mercury", 0.387098), ("Earth", 1.0), ("Mars", 1.523679), ("Jupiter", 5.2044),
                  ("Saturn", SAT_A)):
        y = g_of_r_au(r) / A0_CANON
        slope = slope_of_y(y)
        slopes[nm] = slope
        print(f"  {nm:<10s} {r:8.3f} {y:11.4e} {frac_route_a_log10(y) + math.log10(pref):20.2f} "
              f"{frac_alpha2(y) * pref:15.4e} {slope:13.1f}")
    # validate the analytic slope by finite differences where float64 can hold the value
    y0 = 100.0
    h = 1e-5
    fd = (math.log(float(nu_minus1(y0 * (1 + h)))) - math.log(float(nu_minus1(y0 * (1 - h))))) / (2 * h)
    ana = slope_of_y(y0)
    check(abs(fd / ana - 1.0) < 1e-6,
          f"the analytic logarithmic slope d ln A / d ln g = -(sqrt(y)/2) e^sqrt(y)/(e^sqrt(y)-1) is validated "
          f"by central finite differences at y = 100 ({fd:.6f} vs {ana:.6f}) -- so the slopes tabulated above "
          f"are derived, not asserted")
    amp = abs(slopes["Saturn"]) / 2.0
    check(amp > 50.0,
          f"the per-body fingerprint STEEPENS by {amp:.0f} x: d ln|s^TX|/d ln g is {slopes['Saturn']:.0f} at "
          f"Saturn under Route A versus exactly -2 under alpha=2 (and -1 under alpha=1). In principle that is "
          f"a far more distinctive law; in practice it multiplies an amplitude of 10^-364, and the same "
          f"steepness means the ensemble is utterly dominated by whichever tracked body has the weakest field "
          f"-- the 'slope' is unmeasurable because only one body contributes at all")


# ==================================================================================================
def s8_manifest():
    banner("S8. NOTHING FROZEN OR COMMITTED WAS TOUCHED (read-only hash verification)")
    allok = True
    for rel, want in MANIFEST.items():
        p = os.path.join(REPO, rel)
        if not os.path.exists(p):
            print(f"    MISSING {rel}")
            allok = False
            continue
        got = hashlib.sha256(open(p, "rb").read()).hexdigest()
        allok = allok and (got == want)
        print(f"    {'OK ' if got == want else 'BAD'}  {rel}  {got[:16]}")
    check(allok,
          "all five files of mi_stx_alpha2_collapse_2026.py's hash manifest verify unchanged -- the frozen "
          "pre-registration's pipelines and the s^TX target scripts were read but never modified, and this "
          "file wrote nothing")


# ==================================================================================================
def main() -> int:
    banner("LANE 7 -- s^TX SME BOOST DIPOLE RE-SOLVED UNDER ROUTE A (exponential kernel). BOTH FOOTINGS.")
    print("  kernel in force: nu(y) = 1/(1 - e^-sqrt(y)), imported from mi_route_a_kernel.py, never redefined")
    print(f"  a0 INPUT, both footings: canonical {A0_CANON:.4e} (kappa = 1/2, rho_DE/cH_Lambda), "
          f"alt {A0_ALT:.4e} (rho_total/cH0)")
    print("  bound: |s^TX| combined gravity-sector sigma = 1.3e-9 (Hees+ 2016 review, as banked)")
    print("  NOT CITED as live anywhere below: the retracted ~9.6x, the frozen 1.50x/1.24x (retired alpha=1),")
    print("  or 'alpha2 ~ 1e-8 / LIVE' (a reverted double-count). alpha2_MI stays ~1e6x SAFE and NOT live.")

    n_eq = s0_footings_and_apex()
    s1_the_tail_is_not_a_power_law()
    pref, g_sat, _ = s2_normalisation_controls(n_eq)
    out = s3_route_a_margin(pref, g_sat)
    s4_the_sign(n_eq)
    m_sun, r_fire = s5_can_it_ever_fire(pref, g_sat)
    y_cross = s6_other_channels(pref, n_eq)
    s7_the_slope_law(pref)
    s8_manifest()

    lm_can = out["canonical rho_DE/cH_L"][3]
    lm_alt = out["alt rho_total/cH0"][3]
    banner("VERDICT -- and the honest direction is that a FALSIFIER WAS LOST, not that a bound was passed")
    print(f"  (a) MARGIN. Route A: |s^TX|(Saturn) = 10^{out['canonical rho_DE/cH_L'][2]:.1f} (canonical) and "
          f"10^{out['alt rho_total/cH0'][2]:.1f} (alt), i.e. margins of")
    print(f"      10^{lm_can:.1f} x and 10^{lm_alt:.1f} x against 1.3e-9. The superseded alpha=2 numbers were "
          f"1.03e6 x / 7.09e5 x, themselves")
    print("      already dead. The extra suppression is NOT a single factor: it is e^-sqrt(y)/(1/2y^2), which")
    print("      is 1.3e-17 at the Sun's reflex and 10^-348 at Saturn. The frozen alpha=1 1.50x/1.24x")
    print("      reproduces here only as a normalisation control and remains uncitable as a live margin.")
    print("  (b) SIGN: NEGATIVE, UNCHANGED. nu - 1 = 1/(e^sqrt(y)-1) > 0 for all y > 0 (analytic), so the")
    print("      sign is carried entirely by n_X < 0 at the CMB apex; the antipodal mutation flips it, so the")
    print("      statement has content. Nothing about the pre-registered sign needs amending.")
    print(f"  (c) RETIRE IT. Three generosity limits all fail to reach the bound: Saturn aphelion, the Sun's")
    print(f"      own Jupiter-driven reflex ({10 ** m_sun['canonical rho_DE/cH_L']:.1e} x / "
          f"{10 ** m_sun['alt rho_total/cH0']:.1e} x safe -- and that is the body that BROKE the alpha=2")
    print(f"      ephemeris discharge), and the inversion for what it would take: ranging at "
          f"{r_fire['alt rho_total/cH0']:.0f}-{r_fire['canonical rho_DE/cH_L']:.0f} AU,")
    print("      ~55-60x Saturn. A front that cannot fire at any achievable sensitivity is not a test. The")
    print("      corpus should carry s^TX as a trivially satisfied CONSISTENCY row and strike it from every")
    print("      list of discriminators. This is a COST of Route A, on top of Amendment 5's voiding of the")
    print("      bands: alpha=2 killed the front's amplitude, Route A makes the death irrecoverable.")
    print(f"  (d) NO NEW SME CHANNEL. Twelve channel-footing pairs re-priced (dipole, three quadrupole")
    print(f"      companions, PPN alpha_2, GW R3): Route A's margin is larger in every one, because they all")
    print(f"      share the prefactor A(body) and all live at y >> 100. The window where the sharper kernel")
    print(f"      exceeds the power law is y < {y_cross:.0f}, i.e. r > 800 AU in the solar system -- and it is")
    print("      observationally EMPTY. The one reading that would fire (galactic external field) fires for")
    print("      alpha=1 and alpha=2 too, so it indicts the reading, not the kernel. What Route A really")
    print("      changes is the SHAPE of the per-body slope law: ~208x sharper, on a 10^-364 amplitude.")
    print("  AND THE SPREAD THAT MATTERS GOING FORWARD: the 1.21x a0 footing fork is worth "
          f"{lm_can - lm_alt:.0f} ORDERS here.")
    print("      Under an exponential kernel, no Newtonian-regime residual may be quoted on one footing.")
    print()
    print("  NOT CLAIMED: that a0 is derived (kappa = 1/2 stays an input); that the ephemeris liability is")
    print("  discharged (that is lane 6's number, not this one); that any other front moved; that the theory")
    print("  is closed. Doors elsewhere -- the per-body slope law at Gaia DR4 SSO precision, the deep-regime")
    print("  fronts, the wide-binary shape -- are untouched by this file and remain open.")
    n = sum(1 for t, _ in _OK if t)
    print(f"\n  {n}/{len(_OK)} checks held.")
    if n != len(_OK):
        for t, m in _OK:
            if not t:
                print(f"    FAILED: {m}")
        return 1
    print("  Exit 0.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
