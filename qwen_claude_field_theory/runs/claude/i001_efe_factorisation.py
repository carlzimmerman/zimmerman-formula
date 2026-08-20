#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
i001_efe_factorisation.py
=========================
I001 -- DOES THE EXTERNAL-FIELD EFFECT FACTORISE AGAINST A DENSITY-DEPENDENT a0?

THE QUESTION.  Every ghost-free (legal) kernel saturates: the anomalous acceleration on a
test body tends to a CONSTANT u_inf = s a0 as y = g_bar/a0 -> infinity.  At 1 AU that is a
constant sunward force, and it is ~3.9e4 x the published Saturn anomalous-precession limit
at s = 1/2.  The standing ledger relieves that by a committed EFE factor 119-189x, applied
MULTIPLICATIVELY on top of any a0 suppression from the promotion a0^2(Q) = kappa^2 G(-K(Q)).
This script asks whether the two COMPOUND (the hoped-for win: a smaller local a0 raises
g_ext/a0, which should deepen the EFE) -- and, first, whether the 119-189x exists at all.

WHAT IS DERIVED HERE, NOT IMPORTED
  * the legal family's exact local law and its anchors (a0-line at s=1/2, simple at s=1),
  * the external field g_ext from v_c and R_0 (not quoted),
  * the linearised AQUAL operator around the saturated spherical background (L, T),
  * the l=1 penetration ODE for a uniform external field, integrated numerically with the
    EXACT background coefficients, from 1 AU out past the MOND radius,
  * a PERTURBATION-FREE flux bound on the anomaly at 1 AU that holds for ANY g_ext,
  * the promotion's local a0 suppression, and the galaxy-side cost of the same suppression,
    profiled on the real 175-galaxy SPARC rotmod set.

GATE (task item b): the machinery must reproduce the committed 119-189x at constant a0.
It does NOT.  It returns 1.000.  The gate is reported FAILED and every downstream number is
labelled accordingly.  The provenance of 119-189x is reproduced and shown to be a scalar-
addition artefact -- which is also the finding already committed to this repo in
real_research/reviews/mi_efe_escape_and_ch23_withdrawn_2026.py (2026-08-02 closure audit),
reached there by a completely different route (vector orbit-averaging).  Two independent
derivations agree.

ANTI-MANUFACTURE DISCIPLINE.  Corrections are applied in BOTH directions:
  - AGAINST the framework: the EFE relief is 1.0x, not 119-189x (gap widens ~150x).
  - FOR the framework: the brief's galaxy floor s >= 0.558 comes from a closed form that
    matches neither anchor; on the anchored family the floor is s >= 0.435 (gap narrows 1.28x).
  - The galaxy side is re-profiled under the SAME a0 suppression, because SPARC galaxies sit
    in external fields and finite densities too.  If it moves both sides, nothing is gained.

Exit 0 only if every numbered check passes.
"""
from __future__ import annotations

import glob
import math
import os
import sys

import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import iv

# ---------------------------------------------------------------------------------------
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SPARC_DIR = os.path.join(REPO, "real_research", "data", "sparc_data")

FAILED: list[str] = []
NCHK = [0]


def check(cond, label, detail=""):
    NCHK[0] += 1
    ok = bool(cond)
    print(f"  [{'ok' if ok else 'FAIL'}] {label}" + (f"\n         {detail}" if detail else ""))
    if not ok:
        FAILED.append(label)
    return ok


def banner(t):
    print("\n" + "=" * 100)
    print(f"  {t}")
    print("=" * 100)


# ---------------------------------------------------------------------------------------
# CONSTANTS.  Both footings carried for every dimensional number, per standing rule.
c = 2.99792458e8
G = 6.67430e-11
GM_SUN = 1.32712440018e20
AU = 1.495978707e11
KPC = 3.0856775814913673e19
YR = 3.15576e7
ARCSEC = 206264.806247

A0_CANON = 9.3619e-11
A0_ALT = 1.1279e-10
FOOTINGS = {"canonical": A0_CANON, "alt": A0_ALT}

# Milky Way rotation input (the brief's values; g_ext is DERIVED from them below).
V_C = 233.0e3
R_0 = 8.2 * KPC

# Promotion / dark-sector densities (same convention as the committed
# real_research/reviews/a0_local_ephemeris_2026.py, so the machinery can be cross-checked).
RHO_DM0 = 0.265 * 9.47e-27               # cosmic mean dark density, kg/m^3
RHO_LOCAL = 0.4 * 1.7827e-27 * 1e6       # 0.4 GeV/cm^3 -> kg/m^3
NU0_TASK = 2.36e-6                       # RAR-flatness bound quoted in the task brief
NU0_COMMITTED = {"ceiling": 1.77e-4, "floor": 2.14e-5}   # the older committed pair

# Ledger numbers TAKEN ON INPUT from the task brief (not re-derived from a primary source
# here; the ephemeris LIMIT itself is back-derived below and flagged as uncited).
SATURN_RATIO_BARE = 39424.0              # x the anomalous-precession limit at s = 1/2, pre-EFE
EFE_COMMITTED = (119.0, 189.0)           # the committed multiplicative relief
GAP_BRIEF = 233.0


# =======================================================================================
banner("A  THE LEGAL FAMILY -- fixed by its own anchors, not by the brief's closed form")

print(r"""  Quasi-static scalar sector:  div[ J_Y(|grad chi|^2) grad chi ] = 4 pi Ghat rho.
  Spherical symmetry + Gauss  =>  the LOCAL algebraic law   J_Y(u^2) u = g_bar.
  Legal closed-form family    J_Y = v/(1 - v/s),  v = |grad chi|/a0,  so with U = u/a0:

        U^2 / (1 - U/s) = y        <=>        U_s(y) = [ sqrt(y^2/s^2 + 4y) - y/s ] / 2

  and the exact saturation identity  s - U = s U^2 / y  (used below; it is cancellation-free).
""")


def U_s(y, s):
    """Legal-family anomaly U = u/a0.  Written to avoid catastrophic cancellation at y >> 1."""
    y = np.asarray(y, dtype=float)
    q = y / s
    return 2.0 * y / (np.sqrt(q * q + 4.0 * y) + q)


def s_minus_U(y, s):
    """s - U_s(y,s), evaluated WITHOUT cancellation (it is ~1e-9 of s at 1 AU, so the naive
    subtraction loses every significant digit in float64)."""
    y = np.asarray(y, dtype=float)
    q = y / s
    D = np.sqrt(q * q + 4.0 * y)
    sD_minus_y = 4.0 * s * s * y / (np.sqrt(y * y + 4.0 * s * s * y) + y)   # = s*D - y
    return sD_minus_y / (D + q)


def U_brief(y, s):
    """The closed form written in the task brief: U = s sqrt(y)/(s + sqrt y)."""
    y = np.asarray(y, dtype=float)
    return s * np.sqrt(y) / (s + np.sqrt(y))


ygrid = np.geomspace(1e-8, 1e10, 4001)
for s in (0.25, 0.5, 1.0, 2.0):
    U = U_s(ygrid, s)
    # law in its cancellation-free form:  y (s - U) = s U^2   <=>   U^2/(1 - U/s) = y
    resid = float(np.max(np.abs(ygrid * s_minus_U(ygrid, s) - s * U ** 2) / (s * U ** 2)))
    idn = float(np.max(np.abs(s_minus_U(ygrid, s) - s * U ** 2 / ygrid) / (s * U ** 2 / ygrid)))
    check(resid < 1e-13 and idn < 1e-13,
          f"A1(s={s}) U_s solves the local law y(s-U) = s U^2 to rel {resid:.2e} over 18 decades in y",
          "" if s != 0.25 else "evaluated through the cancellation-free s-U identity; the naive "
                               "1 - U/s form is pure round-off once y > 1e8")

y = np.geomspace(1e-6, 1e4, 2001)
check(np.max(np.abs(U_s(y, 0.5) - (np.sqrt(y ** 2 + y) - y)) / U_s(y, 0.5)) < 1e-11,
      "A2a ANCHOR 1: s = 1/2 IS the a0-line, U = sqrt(y^2+y) - y, matched directly over 10 decades",
      "i.e. g_obs^2 = g_bar^2 + a0 g_bar -- Carl's signature relation, recovered from J_Y = v/(1-2v)")

ybig = np.geomspace(1e-6, 1e10, 2001)
Ub = U_s(ybig, 0.5)
check(float(np.max(np.abs(Ub ** 2 - 2.0 * ybig * s_minus_U(ybig, 0.5)) / Ub ** 2)) < 1e-13,
      "A2b and to y = 1e10 via the a0-line's own cancellation-free identity U^2 = 2y(1/2 - U)",
      "which is (U+y)^2 = y^2 + y rearranged -- the direct form in A2a is round-off beyond y ~ 1e6")

ysm = np.geomspace(1e-6, 1e4, 2001)
g_simple = ysm + U_s(ysm, 1.0)
g_simple_ref = (ysm + np.sqrt(ysm ** 2 + 4.0 * ysm)) / 2.0
check(np.max(np.abs(g_simple - g_simple_ref) / g_simple_ref) < 1e-11,
      "A3  ANCHOR 2: s = 1 IS the standard 'simple' kernel, g_obs = (g_bar + sqrt(g_bar^2+4 a0 g_bar))/2")

u2 = float(U_s(2.0, 0.5))
check(abs(u2 - 0.4495) < 5e-4,
      f"A4  U(y=2) at s=1/2 is {u2:.4f} -- the brief's own 0.449, so the brief's GALAXY-side number "
      f"was computed on THIS family")

small = float(U_s(1e-10, 0.5) / math.sqrt(1e-10))
big = float(U_s(1e12, 0.5))
check(abs(small - 1.0) < 1e-4 and abs(big - 0.5) < 1e-8 and float(U_s(1e12, 0.5) / 1e12) < 1e-11,
      f"A5  legality limits hold: U/sqrt(y) -> {small:.6f} as y->0; U -> {big:.9f} = s as y->inf; U/y -> 0",
      "monotone increasing throughout, so the longitudinal mode is not a ghost")

ub2 = float(U_brief(2.0, 0.5))
ub_line = np.max(np.abs(U_brief(y, 0.5) - (np.sqrt(y ** 2 + y) - y)))
check(abs(ub2 - u2) > 0.05 and ub_line > 0.05,
      f"A6  DISCREPANCY RECORDED (not silently absorbed): the brief's closed form s sqrt(y)/(s+sqrt y) "
      f"gives U(2)={ub2:.4f}, not {u2:.4f}, and is NOT the a0-line at s=1/2",
      "it is in the legal class but hits neither anchor; the anchored family above is used throughout, "
      "and section E re-derives the galaxy floor on it")


# =======================================================================================
banner("B  MACHINERY GATE ON THE GALAXY SIDE -- real SPARC, the brief's own dex triple")


def load_sparc():
    rows = []
    for fn in sorted(glob.glob(os.path.join(SPARC_DIR, "*_rotmod.dat"))):
        try:
            d = np.genfromtxt(fn, comments="#")
        except Exception:
            continue
        if d.ndim != 2 or d.shape[1] < 6:
            continue
        R, Vo, eV, Vg, Vd, Vb = (d[:, i] for i in range(6))
        rows.append((R * KPC, Vo, eV, Vg, Vd, Vb))
    return rows


ROWS = load_sparc()
check(len(ROWS) == 175, f"B1  SPARC rotmod set loaded: {len(ROWS)} galaxies (expect 175)")


def rar_scatter(a0, s, ups_d, ups_b_ratio=1.4):
    """Committed convention of real_research/rar_framework_a0_mlfit.py: weighted log-residual rms."""
    res, w = [], []
    for Rm, Vo, eV, Vg, Vd, Vb in ROWS:
        V2 = np.sign(Vg) * Vg ** 2 + ups_d * Vd ** 2 + ups_b_ratio * ups_d * Vb ** 2
        gb = V2 * 1e6 / Rm
        go = (Vo * 1e3) ** 2 / Rm
        ok = (gb > 0) & (go > 0) & np.isfinite(gb) & np.isfinite(go) & (Vo > 0)
        pred = gb[ok] + a0 * U_s(gb[ok] / a0, s)
        res += list(np.log10(go[ok]) - np.log10(pred))
        fr = np.clip(eV[ok], 1, None) / np.clip(Vo[ok], 1, None)
        w += list(1.0 / fr ** 2)
    res, w = np.array(res), np.array(w)
    return float(np.sqrt(np.sum(w * res ** 2) / np.sum(w)))


UPS_GRID = np.linspace(0.20, 1.50, 53)


def profile_ups(a0, s):
    v = [rar_scatter(a0, s, u) for u in UPS_GRID]
    i = int(np.argmin(v))
    return v[i], float(UPS_GRID[i])


print(f"  {'s':>6}{'Upsilon*':>11}{'dex':>9}   brief")
brief_triple = {0.5: 0.1083, 1.0: 0.1009, 2.0: 0.0998}
got = {}
for s in (0.5, 1.0, 2.0):
    d, u = profile_ups(A0_CANON, s)
    got[s] = d
    print(f"  {s:>6.1f}{u:>11.3f}{d:>9.4f}   {brief_triple[s]:.4f}")
check(all(abs(got[s] - brief_triple[s]) < 6e-4 for s in brief_triple),
      "B2  *** GATE PASSED on the galaxy side: the anchored family + Upsilon refit reproduces the "
      "brief's 0.1083 / 0.1009 / 0.0998 dex triple to <6e-4 ***",
      "so the family, the data path and the weighting convention here are the corpus's own")


# =======================================================================================
banner("C  THE EXTERNAL FIELD, DERIVED -- and its SCALAR part on the framework's own kernel")

g_ext = V_C ** 2 / R_0
check(abs(g_ext - 2.1456e-10) / 2.1456e-10 < 5e-4,
      f"C1  g_ext DERIVED from v_c = {V_C/1e3:.0f} km/s at R_0 = {R_0/KPC:.1f} kpc: "
      f"g_ext = v_c^2/R_0 = {g_ext:.4e} m/s^2",
      "identical to the 2.1456e-10 convention already carried in real_research/reviews/"
      "mi_efe_escape_and_ch23_withdrawn_2026.py -- an independent cross-check of the input")

print(f"\n  The EFE acts through grad chi, so what matters is the external SCALAR field u_ext,")
print(f"  not g_ext.  Split g_ext = g_bar,gal + u_ext using the framework's own kernel:\n")
print(f"  {'footing':<12}{'s':>5}{'y_gal':>10}{'g_bar,gal':>13}{'u_ext':>13}{'u_ext/a0':>11}{'u_ext/(s a0)':>14}")
U_EXT = {}
for fname, a0 in FOOTINGS.items():
    for s in (0.5, 1.0):
        lo, hi = 1e-6, 1e6
        for _ in range(300):
            mid = math.sqrt(lo * hi)
            if a0 * (mid + float(U_s(mid, s))) < g_ext:
                lo = mid
            else:
                hi = mid
        y_gal = math.sqrt(lo * hi)
        ue = a0 * float(U_s(y_gal, s))
        U_EXT[(fname, s)] = (y_gal, ue)
        print(f"  {fname:<12}{s:>5.2f}{y_gal:>10.4f}{a0*y_gal:>13.4e}{ue:>13.4e}"
              f"{ue/a0:>11.4f}{ue/(s*a0):>14.4f}")

y_mw, ue_mw = U_EXT[("canonical", 0.5)]
check(0.40 < ue_mw / A0_CANON < 0.48 and 1.5 < y_mw < 2.5,
      f"C2  the external SCALAR field at the Sun is u_ext = {ue_mw/A0_CANON:.3f} a0 = "
      f"{ue_mw/(0.5*A0_CANON)*100:.1f}% of the saturation value s a0",
      "NOT small compared with the internal saturated field -- so the EFE is NOT obviously "
      "negligible here, and the idea's premise is worth taking seriously before it is tested")
check(1.0 < y_mw < 4.0,
      f"C3  the Sun sits at y_MW = g_bar/a0 = {y_mw:.3f} -- INSIDE the RAR's transition region",
      "this fact is used in section F: the ephemeris and the Milky Way RAR point sample the SAME "
      "local dark density, hence the SAME promoted a0")


# =======================================================================================
banner("D  THE EFE, DERIVED -- linearised AQUAL around the saturated spherical background")

print(r"""  Perturb  chi -> chi + psi  about the spherical background grad chi = u(r) rhat:
      delta[J_Y d_i chi] = J_Y d_i psi + 2 J_YY (d_k chi d_k psi) d_i chi
  so the medium is an anisotropic dielectric with
      LONGITUDINAL  L = J_Y + 2 Y J_YY      TRANSVERSE  T = J_Y.
  For J_Y = v/(1-v/s), using the exact identity s - v = s v^2 / y, these reduce to

      T(r) = y / v            L(r) = (2s - v) y^2 / (s v^3)          [cancellation-free]

  and the field equation for psi = f(r) cos(theta) (the l=1 mode a uniform external field
  excites) is           d/dr [ r^2 L f' ] = 2 T f .
""")


def LT_of_y(yv, s):
    v = U_s(yv, s)
    T = yv / v
    L = (2.0 * s - v) * yv * yv / (s * v ** 3)
    return float(L), float(T)


# D1a: verify L = J_Y + 2 Y J_YY by a direct numerical derivative of J_Y(Y).  Parametrised by v
# (not by y) so the test points sit safely inside (0, s) and the FD is not evaluated where
# J_Y = s v/(s-v) is itself round-off.
def J_Y_of_v(v, s):
    return s * v / (s - v)


worst_fd = 0.0
for s in (0.5, 1.0):
    for frac in (0.1, 0.3, 0.5, 0.7, 0.9):
        v = frac * s
        Yv = v ** 2
        h = Yv * 1e-6
        JY = J_Y_of_v(v, s)
        JYY = (J_Y_of_v(math.sqrt(Yv + h), s) - J_Y_of_v(math.sqrt(Yv - h), s)) / (2 * h)
        L_num, T_num = JY + 2 * Yv * JYY, JY
        L_cf = s * v * (2 * s - v) / (s - v) ** 2
        T_cf = s * v / (s - v)
        worst_fd = max(worst_fd, abs(L_num - L_cf) / L_cf, abs(T_num - T_cf) / T_cf)
check(worst_fd < 1e-6,
      f"D1a L = J_Y + 2 Y J_YY = s v(2s-v)/(s-v)^2 and T = J_Y = s v/(s-v), verified against a "
      f"numerical dJ_Y/dY to rel {worst_fd:.2e} (2 s-values x 5 points spanning v/s = 0.1..0.9)")

# D1b: and the change of variable to y, which is what the ODE actually uses.  Both forms are
# evaluated through the cancellation-free s-U identity so the test is meaningful at y = 6e7.
worst_cv = 0.0
for s in (0.5, 1.0):
    for yv in (1e-2, 1.0, 1e2, 1e5, 1e8):
        v = float(U_s(yv, s))
        smv = float(s_minus_U(yv, s))
        L_v, T_v = s * v * (2 * s - v) / smv ** 2, s * v / smv
        L_y, T_y = LT_of_y(yv, s)
        worst_cv = max(worst_cv, abs(L_v - L_y) / L_y, abs(T_v - T_y) / T_y)
check(worst_cv < 1e-12,
      f"D1b change of variable using y = s v^2/(s-v): T = y/v and L = (2s-v) y^2/(s v^3), agreeing "
      f"with the v-form to rel {worst_cv:.2e} out to y = 1e8",
      "these y-forms carry no subtraction at all, which is why the ODE below is trustworthy at 1 AU")

r1 = AU
y1 = {f: GM_SUN / (a0 * r1 ** 2) for f, a0 in FOOTINGS.items()}
print(f"\n  {'footing':<12}{'y(1 AU)':>13}{'s':>5}{'s-v (headroom)':>17}{'L/T':>13}")
for fname, a0 in FOOTINGS.items():
    for s in (0.5, 1.0):
        yv = y1[fname]
        v = float(U_s(yv, s))
        L, T = LT_of_y(yv, s)
        print(f"  {fname:<12}{yv:>13.4e}{s:>5.2f}{s-v:>17.4e}{L/T:>13.4e}")
yv = y1["canonical"]
v = float(U_s(yv, 0.5))
L, T = LT_of_y(yv, 0.5)
check(L / T > 1e7 and abs((L / T) - (2 * 0.5 - v) / (0.5 - v)) / (L / T) < 1e-6,
      f"D2  the saturated medium is stiff along the background field by L/T = {L/T:.3e} at 1 AU",
      "large longitudinal stiffness is exactly what screens an imposed external field -- "
      "this is the mechanism the idea hoped for, and it is REAL; section D3-D5 prices it")


# --- D3: integrate the l=1 penetration ODE with the exact coefficients -------------------
def penetration(s, a0, x_match, x_in):
    """Regular l=1 response to a uniform field. x = r/r_M.  Returns delta(x_in)/U_ext."""
    def coeffs(x):
        yv = 1.0 / x ** 2
        return LT_of_y(yv, s)

    def rhs(x, Z):
        f, q = Z
        L, T = coeffs(x)
        return [q / (x * x * L), 2.0 * T * f]

    L0, _ = coeffs(x_in)
    Z0 = [x_in ** 3, 3.0 * x_in ** 4 * L0]           # the unique regular branch, f ~ r^3
    sol = solve_ivp(rhs, [x_in, x_match], Z0, rtol=1e-11, atol=1e-300, method="Radau")
    f_in, q_in = Z0
    f_m, q_m = sol.y[0][-1], sol.y[1][-1]
    Lm, _ = coeffs(x_match)
    fp_in = q_in / (x_in ** 2 * L0)
    fp_m = q_m / (x_match ** 2 * Lm)
    amp_in = max(abs(fp_in), f_in / x_in)            # |grad psi| scale at 1 AU
    amp_m = max(abs(fp_m), f_m / x_match)            # |grad psi| scale where it matches g_ext
    return amp_in / amp_m


rM = math.sqrt(GM_SUN / A0_CANON)
check(abs(rM / AU - 7958.8) / 7958.8 < 1e-3,
      f"D3  MOND radius of the Sun r_M = sqrt(GM/a0) = {rM/AU:.1f} AU (canonical); "
      f"{math.sqrt(GM_SUN/A0_ALT)/AU:.1f} AU (alt)")

print(f"\n  {'footing':<11}{'s':>5}{'r_match':>12}{'delta(1AU)/U_ext':>20}")
pen = []
for fname, a0 in FOOTINGS.items():
    rMf = math.sqrt(GM_SUN / a0)
    xin = AU / rMf
    for s in (0.5, 1.0):
        for xm in (0.3, 0.737, 1.0, 1.5):
            p = penetration(s, a0, xm, xin)
            pen.append(p)
            print(f"  {fname:<11}{s:>5.2f}{xm*rMf/AU:>10.0f}AU{p:>20.4e}")
check(max(pen) < 1e-5,
      f"D4  *** THE EXTERNAL FIELD IS SCREENED, NOT THE ANOMALY. *** Its residual at 1 AU is "
      f"{min(pen):.2e} - {max(pen):.2e} of U_ext across both footings, s in (1/2, 1) and a "
      f"5x range of matching radius",
      "the regular branch of the l=1 equation is f ~ r^3, so delta ~ U_ext (r/r_M)^2: the "
      "saturated scalar sector expels the galactic field from the inner solar system")

# analytic cross-check of the numeric ODE in the deep regime
s = 0.5
rMf = math.sqrt(GM_SUN / A0_CANON)
k = s * math.sqrt(2.0)                                # in units of 1/r_M
xs = np.geomspace(AU / rMf, 0.05, 12)


def f_num_profile(s, a0, xs):
    rMf = math.sqrt(GM_SUN / a0)
    xin = xs[0]

    def coeffs(x):
        return LT_of_y(1.0 / x ** 2, s)

    def rhs(x, Z):
        L, T = coeffs(x)
        return [Z[1] / (x * x * L), 2.0 * T * Z[0]]

    L0, _ = coeffs(xin)
    sol = solve_ivp(rhs, [xin, xs[-1]], [xin ** 3, 3 * xin ** 4 * L0],
                    t_eval=xs, rtol=1e-12, atol=1e-300, method="Radau")
    return sol.y[0]


fn = f_num_profile(s, A0_CANON, xs)
fa = xs ** 1.5 * iv(1.5, k * xs)
ratio = (fn / fa)
check(np.max(np.abs(ratio / ratio[0] - 1.0)) < 2e-3,
      f"D5  the numerical ODE matches the deep-regime analytic solution f = r^(3/2) I_(3/2)(k r) "
      f"with k = s sqrt(2)/r_M to {np.max(np.abs(ratio/ratio[0]-1.0)):.1e} over 2.6 decades in r",
      "an independent check that the integrator, the coefficients and the regular branch are right")

slope = np.polyfit(np.log(xs[:6]), np.log(fn[:6]), 1)[0]
check(abs(slope - 3.0) < 5e-3,
      f"D6  the regular branch scales as f ~ r^{slope:.4f} (exactly r^3), so the penetrating field "
      f"delta ~ r^2 -- at 1 AU that is (1/{rMf/AU:.0f})^2 = {(AU/rMf)**2:.2e}")

# --- D7: the PERTURBATION-FREE bound.  This is the one that cannot be argued with. -------
print(r"""
  A bound with NO perturbation theory and NO assumption about g_ext.  Integrating the field
  equation over a ball of radius r gives, exactly,
        <  J_Y(v^2) v cos(alpha)  >_sphere  =  y            (alpha = angle to rhat)
  because a uniform external field is divergence-free and carries zero net flux.  With
  G(v) = s v^2/(s-v) (i.e. G = U_s^{-1}) and cos(alpha) <= 1,
        max_sphere G(v)  >=  <G(v) cos alpha>  =  y     =>     max_sphere v  >=  U_s(y).
""")
for fname, a0 in FOOTINGS.items():
    for s in (0.5, 1.0):
        yv = GM_SUN / (a0 * AU ** 2)
        vmin = float(U_s(yv, s))
        print(f"  {fname:<11} s={s:.2f}  max_sphere |grad chi| >= {vmin:.12f} a0 = "
              f"s a0 (1 - {float(s_minus_U(yv, s))/s:.3e})")
yv = GM_SUN / (A0_CANON * AU ** 2)
defect = float(s_minus_U(yv, 0.5)) / 0.5
check(defect < 1e-8,
      f"D7  *** RIGOROUS: whatever the external field does, somewhere on the 1-AU sphere the "
      f"anomaly is at least s a0 (1 - {defect:.2e}). The EFE cannot suppress the saturated tail "
      f"by more than {defect:.1e} in relative terms. ***",
      "flux conservation alone; no linearisation, no kernel choice beyond legality")

# D8: the cap headroom (s - v) and the penetrating field both scale as r^2, so the linearisation
# is uniformly marginal rather than divergent.  Tested, not asserted.
rMc = math.sqrt(GM_SUN / A0_CANON)
xtest = np.array([AU / rMc, 3 * AU / rMc, 10 * AU / rMc, 30 * AU / rMc])
head = np.array([float(s_minus_U(1.0 / x ** 2, 0.5)) for x in xtest])


def penetrating_amp(s, a0, xs):
    """|grad psi| of the regular l=1 branch, up to one overall constant, at each x."""
    rMf = math.sqrt(GM_SUN / a0)
    xin = xs[0]

    def coeffs(x):
        return LT_of_y(1.0 / x ** 2, s)

    def rhs(x, Z):
        L, T = coeffs(x)
        return [Z[1] / (x * x * L), 2.0 * T * Z[0]]

    L0, _ = coeffs(xin)
    sol = solve_ivp(rhs, [xin, xs[-1] * 1.0001], [xin ** 3, 3 * xin ** 4 * L0],
                    t_eval=xs, rtol=1e-12, atol=1e-300, method="Radau")
    out = []
    for i, x in enumerate(xs):
        L, _ = coeffs(x)
        fp = sol.y[1][i] / (x * x * L)
        out.append(max(abs(fp), sol.y[0][i] / x))
    return np.array(out)


amp = penetrating_amp(0.5, A0_CANON, xtest)
rat = amp / head
check(float(np.max(rat) / np.min(rat) - 1.0) < 0.02,
      f"D8  self-consistency, TESTED: the cap headroom (s - v) and the penetrating field both scale "
      f"as r^2, so their ratio is r-independent to {np.max(rat)/np.min(rat)-1:.2e} over 1 -> 30 AU",
      "=> the linearisation is uniformly marginal, never divergent: the exact nonlinear answer "
      "differs from D4 by an O(1) factor with the SAME r^2 law. The induced tilt of the anomaly at "
      f"1 AU is ~{ue_mw/A0_CANON*float(np.median(pen))/0.5:.1e} rad either way")


# =======================================================================================
banner("E  THE GATE (task item b): can this machinery reproduce the committed 119-189x?")

EFE_RELIEF_DERIVED = 1.0 / (1.0 - max(pen) - defect)
check(EFE_RELIEF_DERIVED < 1.001,
      f"E1  *** GATE FAILED. *** This machinery returns an EFE relief of {EFE_RELIEF_DERIVED:.9f}x "
      f"on the saturated sunward anomaly. It does NOT reproduce {EFE_COMMITTED[0]:.0f}-"
      f"{EFE_COMMITTED[1]:.0f}x. Everything downstream is reported under a FAILED gate.")

print(r"""
  PROVENANCE of 119-189x, reproduced so the failure is diagnosed rather than asserted.
  The committed construction is SCALAR:
        a_tot = (g_in + g_ex) nu(g_in + g_ex),   a_obs = a_tot - g_ex nu(g_ex),
        anomaly = a_obs - g_in
  which adds a fixed-direction external vector to a sunward internal one as if collinear.
""")
BOUND_EARTH = 3.66e-14                   # Sereno & Jetzer 2006 Earth 2-sigma, as carried by the corpus
print(f"  {'footing':<11}{'g_ext':>13}{'scalar anom':>14}{'bare s a0':>12}{'suppression':>13}"
      f"{'=> x over':>11}")
scalar_supp, implied = [], []
for fname, a0 in FOOTINGS.items():
    for gex in (1.8e-10, g_ext):
        r_mars = 1.5237 * AU
        g_in = GM_SUN / r_mars ** 2

        def nu_a0line(g, a0=a0):
            return math.sqrt(1.0 + a0 / g)

        a_tot = (g_in + gex) * nu_a0line(g_in + gex)
        a_obs = a_tot - gex * nu_a0line(gex)
        anom = a_obs - g_in
        supp = (a0 / 2) / anom
        over = anom / BOUND_EARTH                 # footing-consistent: this row's own a0
        scalar_supp.append(supp)
        implied.append(over)
        print(f"  {fname:<11}{gex:>13.4e}{anom:>14.4e}{a0/2:>12.4e}{supp:>13.3f}{over:>11.0f}")
check(min(implied) < EFE_COMMITTED[1] * 1.3 and max(implied) > EFE_COMMITTED[0] * 0.7,
      f"E2  the scalar construction is REPRODUCED: it yields suppressions "
      f"{min(scalar_supp):.2f}-{max(scalar_supp):.2f}x, i.e. {min(implied):.0f}-{max(implied):.0f}x over "
      f"the Earth bound (each row on its OWN footing), straddling the committed "
      f"{EFE_COMMITTED[0]:.0f}-{EFE_COMMITTED[1]:.0f}x band",
      "so the number is arithmetically real; what is wrong is its vector content")

NPH = 400000
phase = np.linspace(0.0, 2 * math.pi, NPH, endpoint=False)
check(abs(float(np.cos(phase).mean())) < 1e-12,
      f"E3  and it is wrong: every g_ext-carried term enters the SUNWARD projection through "
      f"<g_ext . rhat> = <cos(phase)> = {float(np.cos(phase).mean()):.1e} over an orbit. A fixed-"
      f"direction field cannot cancel a co-rotating one",
      "this is precisely the finding already committed in real_research/reviews/"
      "mi_efe_escape_and_ch23_withdrawn_2026.py (check E1a) by orbit-averaging. That route and the "
      "nonlinear screening route here are INDEPENDENT and agree: relief = 1.000")


# =======================================================================================
banner("F  ITEM (c): the promotion a0 -> a0(rho), and what it costs on the GALAXY side")


def a0_ratio(nu0, dens_ratio):
    nu = nu0 * dens_ratio
    return float(((1.0 + nu0 ** 2) / (1.0 + nu ** 2)) ** 0.25)


DR_LOCAL = RHO_LOCAL / RHO_DM0
check(abs(DR_LOCAL - 2.84e5) / 2.84e5 < 0.05,
      f"F1  rho_local/rho_dm0 = {DR_LOCAL:.3e} (0.4 GeV/cm^3 vs Omega_dm rho_crit)")

r_ceil, r_floor = a0_ratio(NU0_COMMITTED["ceiling"], DR_LOCAL), a0_ratio(NU0_COMMITTED["floor"], DR_LOCAL)
check(abs(r_ceil - 0.141) < 0.006 and abs(r_floor - 0.403) < 0.012,
      f"F2  machinery cross-check against the committed real_research/reviews/a0_local_ephemeris_2026.py: "
      f"a0_loc/a0 = {r_ceil:.4f} (nu0 ceiling 1.77e-4) / {r_floor:.4f} (floor 2.14e-5) -- its A3 values")

r_task = a0_ratio(NU0_TASK, DR_LOCAL)
check(abs(r_task - 0.911) < 0.01,
      f"F3  *** at the RAR-flatness bound the task states, nu0 <= {NU0_TASK:.2e}, the local suppression is "
      f"only a0_loc/a0 = {r_task:.4f}, i.e. a relief of {1/r_task:.3f}x -- not 2.5-7x ***",
      "the tighter nu0 bound is what guts the promotion: a0 is nearly environment-INDEPENDENT at "
      "solar-neighbourhood densities")

need = GAP_BRIEF
nu_need = math.sqrt(need ** 4 * (1 + NU0_TASK ** 2 * DR_LOCAL ** 2) - 1.0)
dens_need = nu_need / NU0_TASK / DR_LOCAL
check(dens_need > 1e4,
      f"F4  to supply the whole {need:.0f}x from the promotion alone would need the dark density at 1 AU "
      f"to exceed the ambient local value by {dens_need:.2e}x",
      f"= {dens_need*RHO_LOCAL:.2e} kg/m^3, only {dens_need*RHO_LOCAL*(4/3)*math.pi*AU**3/1.989e30:.1e} "
      f"M_sun inside 1 AU, so it is NOT excluded by planetary dynamics -- but it is NOT COMPUTED here "
      f"either. Flagged as the single surviving door, not claimed")

print(r"""
  THE ANTI-MANUFACTURE CHECK.  SPARC galaxies sit at finite dark density too, so the SAME
  promotion suppresses a0 there.  Both sides constrain the same physical quantity: the 1-AU
  anomaly is s a0_local(solar) and the galaxy requirement is on the anomaly at a FIXED ABSOLUTE
  g_bar = 2 a0, which the model gives as f a0 U_s(2/f, s) with a0_eff = f a0.  Done
  deterministically -- no fit, no grid edge to hide in.
""")


def s_min_galaxy(f, target=0.4):
    """smallest s meeting  f U_s(2/f, s) >= target  (anomaly >= 0.4 a0 at g_bar = 2 a0)."""
    if f * math.sqrt(2.0 / f) < target:            # ceiling U_s <= sqrt(y), see F5a
        return math.inf
    lo, hi = 1e-4, 1e10
    for _ in range(400):
        m = math.sqrt(lo * hi)
        if f * float(U_s(2.0 / f, m)) < target:
            lo = m
        else:
            hi = m
    return math.sqrt(lo * hi)


yy = np.geomspace(1e-6, 1e8, 400)
ceil_ok = all(float(np.max(U_s(yy, s) / np.sqrt(yy))) <= 1.0 + 1e-12 for s in (0.25, 0.5, 1, 10, 1e4))
f_impossible = (0.4 ** 2) / 2.0
check(ceil_ok and abs(f_impossible - 0.08) < 1e-9,
      f"F5a within the family U_s(y,s) <= sqrt(y) for EVERY s (the denominator sqrt(q^2+4y)+q >= "
      f"2 sqrt y), so f a0 U_s(2/f,s) <= a0 sqrt(2f). The galaxy requirement is therefore "
      f"UNSATISFIABLE AT ANY s once f < {f_impossible:.3f}",
      "a global a0 suppression does not merely fail to help galaxies -- past 12.5x it kills them")

print(f"  {'f':>10}{'s_min(f)':>13}{'s_min x f':>13}   verdict")
rows_f = []
for f in (1.0, 0.5, 0.2, 0.1, 0.05, 1.0 / GAP_BRIEF):
    sm = s_min_galaxy(f)
    rows_f.append((f, sm))
    if math.isinf(sm):
        print(f"  {f:>10.5f}{'inf':>13}{'inf':>13}   NO legal s meets the RAR")
    else:
        print(f"  {f:>10.5f}{sm:>13.4f}{sm*f:>13.5f}")
fin = [(f, sm) for f, sm in rows_f if math.isfinite(sm)]
prods = [sm * f for f, sm in fin]
check(all(prods[i] <= prods[i + 1] * 1.0001 for i in range(len(prods) - 1)) and prods[-1] > 1.05 * prods[0],
      f"F5b *** THE PROMOTION MOVES BOTH SIDES -- AND MOVES THE GALAXY SIDE FURTHER. *** The product "
      f"s_min x f (which is exactly what the ephemeris bounds) does not stay fixed as f falls: it "
      f"RISES, {prods[0]:.4f} -> {prods[-1]:.4f} from f = 1 to f = {fin[-1][0]:.2f}",
      "so suppressing a0 buys strictly LESS than nothing, unless a0 is suppressed MORE at 1 AU than "
      "in the galaxies -- and the required extra is the whole factor, not a part of it")

print(f"\n  Supporting fit (illustrative, NOT the load-bearing step -- s is a flat direction at low f):")
print(f"  {'f':>10}{'s*':>10}{'Upsilon*':>11}{'dex':>9}")
S_GRID = np.geomspace(0.15, 200.0, 40)
prof = {}
for f in (1.0, 0.5, 0.2):
    best = (9e9, None, None)
    for s in S_GRID:
        d, u = profile_ups(A0_CANON * f, s)
        if d < best[0]:
            best = (d, s, u)
    prof[f] = best
    print(f"  {f:>10.3f}{best[1]:>10.3f}{best[2]:>11.3f}{best[0]:>9.4f}")
check(prof[0.2][0] > prof[1.0][0] * 1.3,
      f"F6  and independently, the RAR itself bounds f without reference to s: the deep-MOND arm "
      f"g_obs -> sqrt(f a0 g_bar) is s-INDEPENDENT, so f cannot hide in s. Weighted scatter degrades "
      f"{prof[1.0][0]:.4f} -> {prof[0.2][0]:.4f} dex at f = 0.2, refitting s AND Upsilon",
      "galaxies cannot absorb even a 5x global a0 suppression, let alone 233x")

check(1.0 < y_mw < 4.0 and abs(a0_ratio(NU0_TASK, DR_LOCAL) - r_task) < 1e-12,
      f"F7  the location argument, which needs no fit: the Sun sits at R_0 = {R_0/KPC:.1f} kpc at "
      f"y = {y_mw:.2f}, i.e. the ephemeris is performed INSIDE a Milky Way RAR point, in the same "
      f"0.4 GeV/cm^3 environment",
      "so f_solar = f_galaxy identically, and the differential gain from the promotion is exactly 1.000 "
      "unless the dark density at 1 AU is enhanced over the ambient value -- see F4")


# =======================================================================================
banner("G  ITEM (d): the total, against the 233x that has to be closed")

# Re-derive the galaxy floor on the ANCHORED family (a correction that FAVOURS the framework).
lo, hi = 1e-3, 10.0
for _ in range(200):
    mid = 0.5 * (lo + hi)
    if float(U_s(2.0, mid)) < 0.4:
        lo = mid
    else:
        hi = mid
s_floor_anchored = 0.5 * (lo + hi)
s_floor_brief = 0.558
check(0.40 < s_floor_anchored < 0.47,
      f"G1  CORRECTION IN THE FRAMEWORK'S FAVOUR: the brief's galaxy floor s >= {s_floor_brief:.3f} comes "
      f"from the closed form flagged in A6. On the ANCHORED family, U_s(2) >= 0.4 gives "
      f"s >= {s_floor_anchored:.4f}",
      f"that narrows the gap by {s_floor_brief/s_floor_anchored:.2f}x before anything else is done")

# ephemeris side: rebuild the precession arithmetic from the brief's own formula.
SAT = dict(a=9.5826 * AU, e=0.0565, T=29.4571 * YR)
n_sat = 2 * math.pi / SAT["T"]
u_inf = 0.5 * A0_CANON
dw = u_inf * math.sqrt(1 - SAT["e"] ** 2) / (n_sat * SAT["a"])
dw_as_cy = dw * 100 * YR * ARCSEC
limit_implied = dw_as_cy / SATURN_RATIO_BARE
check(2.5 < dw_as_cy < 4.0,
      f"G2  the brief's own formula, evaluated: Saturn dvarpi/dt = u_inf sqrt(1-e^2)/(n a) = "
      f"{dw_as_cy:.3f} arcsec/cy at s = 1/2 (canonical); {dw_as_cy*A0_ALT/A0_CANON:.3f} (alt)",
      f"the brief's {SATURN_RATIO_BARE:.0f}x therefore implies a limit of {limit_implied*1e3:.3f} mas/cy. "
      f"That limit is BACK-DERIVED from the brief, NOT cited here -- no source is invented for it")

s_allow_efe = (0.5 / (SATURN_RATIO_BARE / EFE_COMMITTED[1]), 0.5 / (SATURN_RATIO_BARE / EFE_COMMITTED[0]))
s_allow_noefe = 0.5 / SATURN_RATIO_BARE
gap_with_efe = s_floor_anchored / max(s_allow_efe)
gap_no_efe = s_floor_anchored / s_allow_noefe
check(abs(gap_with_efe - GAP_BRIEF / (s_floor_brief / s_floor_anchored)) / gap_with_efe < 0.15,
      f"G3  with the committed EFE the gap is {gap_with_efe:.0f}x (the brief's {GAP_BRIEF:.0f}x, corrected "
      f"downward by the G1 floor); with the EFE relief set to the DERIVED 1.000 it is {gap_no_efe:.3e}x")

total_raw = EFE_RELIEF_DERIVED / r_task
total_diff = EFE_RELIEF_DERIVED * 1.0
print(f"\n  {'contribution':<48}{'reduction':>14}")
print("  " + "-" * 62)
print(f"  {'EFE, derived here (D4/D7, gate E1 FAILED)':<48}{EFE_RELIEF_DERIVED:>13.4f}x")
print(f"  {'promotion at nu0 <= 2.36e-6, raw (F3)':<48}{1/r_task:>13.4f}x")
print(f"  {'promotion, DIFFERENTIAL vs galaxies (F5/F7)':<48}{1.0:>13.4f}x")
print("  " + "-" * 62)
print(f"  {'TOTAL, raw (most generous reading)':<48}{total_raw:>13.4f}x")
print(f"  {'TOTAL, differential (the honest reading)':<48}{total_diff:>13.4f}x")
print(f"  {'REQUIRED to close the gap':<48}{gap_with_efe:>13.1f}x")

check(total_raw < gap_with_efe,
      f"G4  *** KILL. *** Total reduction {total_raw:.3f}x (raw) / {total_diff:.3f}x (differential) "
      f"against the {gap_with_efe:.0f}x required. The two effects do not compound; the EFE term is not "
      f"there to compound with")

# --- G5: the gap without ANY family parametrisation -------------------------------------
y_1au = GM_SUN / (A0_CANON * AU ** 2)
# The class-level statement uses ONLY monotonicity, so verify monotonicity is what legality gives,
# and that Route A -- the kernel that would escape -- is the one that violates it.
mono = all(bool(np.all(np.diff(U_s(np.geomspace(1e-6, 1e9, 6000), s)) > 0)) for s in (0.25, 0.5, 1, 2))
yA = np.geomspace(1e-3, 1e3, 20000)
U_routeA = yA * (1.0 / (1.0 - np.exp(-np.sqrt(yA))) - 1.0)
iA = int(np.argmax(U_routeA))
routeA_falls = bool(U_routeA[iA] > U_routeA[-1] * 1.001) and 2.0 < yA[iA] < 3.0
check(mono and routeA_falls,
      f"G5  PARAMETRISATION-FREE VERSION (so the verdict does not rest on the s-family): every legal U "
      f"is monotone increasing (verified over 15 decades, 4 s-values), while Route A peaks at "
      f"U = {U_routeA[iA]:.4f} at y = {yA[iA]:.3f} and then FALLS -- its illegality confirmed here",
      f"so RAR: U(y~2) >= 0.4  =>  U(y = {y_1au:.2e}) >= 0.4  =>  the 1-AU anomaly is >= 0.4 a0 = "
      f"{0.4*A0_CANON:.3e} m/s^2 for EVERY legal kernel = {0.4/0.5*SATURN_RATIO_BARE:.0f}x the Saturn "
      f"limit, with no free function left. The only escape is a U that falls at large y -- which is "
      f"exactly Route A, and exactly the ghost")

check(EFE_RELIEF_DERIVED < 1.001 and total_raw < 2.0,
      "G6  DIRECTION OF THE RESULT: ADVERSE, and adverse beyond the idea's own KILL criterion -- the "
      "idea does not merely fail to close the gap, it removes the relief the standing ledger was "
      "already banking")


# =======================================================================================
banner("VERDICT")
print(f"""
  IDEA I001 -- does the EFE factorise against a density-dependent a0?   ANSWER: the question is
  moot, because the EFE term it wanted to compound with does not exist.

  1. GATE (b) FAILED.  Deriving the EFE for the legal family rather than importing it, the relief
     on the saturated sunward anomaly is {EFE_RELIEF_DERIVED:.6f}x, not {EFE_COMMITTED[0]:.0f}-{EFE_COMMITTED[1]:.0f}x.
     Two independent derivations agree: (i) the l=1 penetration ODE with exact background
     coefficients gives delta ~ U_ext (r/r_M)^2, screening the galactic field by ~1e7 at 1 AU
     (D4-D6); (ii) flux conservation bounds the 1-AU anomaly below by s a0 (1 - {defect:.1e}) for ANY
     external field, with no perturbation theory at all (D7).  The committed 119-189x is reproduced
     (E2) and diagnosed as a scalar-addition artefact (E3) -- the same conclusion already committed
     in real_research/reviews/mi_efe_escape_and_ch23_withdrawn_2026.py by a different route.

  2. The idea's physical intuition was RIGHT about the mechanism and WRONG about its sign for this
     observable.  The saturated medium is stiff (L/T = {L/T:.1e} at 1 AU, D2) -- but that stiffness
     EXPELS the external field from the solar system rather than using it to cancel the anomaly.
     Screening the EFE away leaves the bare s a0, which is the whole problem.

  3. The promotion supplies {1/r_task:.3f}x at nu0 <= {NU0_TASK:.2e} (F3), and WORSE than zero differentially.
     The Sun sits at y = {y_mw:.2f} INSIDE a Milky Way RAR point in the same 0.4 GeV/cm^3 environment, so
     f_solar = f_galaxy identically (F7).  Both sides constrain the same product s x a0_local, and as
     f falls the galaxy side's required product RISES ({prods[0]:.4f} -> {prods[-1]:.4f}, F5b) and becomes
     unsatisfiable at ANY s below f = {f_impossible:.3f}, because U_s <= sqrt(y) caps the family (F5a).  It
     moves both sides -- and moves the galaxy side further.  Exactly the failure the brief warned of.

  4. NET: the gap widens.  Corrected for the G1 floor it stands at {gap_with_efe:.0f}x with the committed
     EFE and {gap_no_efe:.2e}x without it, against a total available reduction of {total_raw:.3f}x.

  5. NOT COMPUTED, and left open rather than closed: the dark-sector density at 1 AU relative to the
     ambient galactic value.  Everything above assumes they are equal (the committed convention).  A
     solar-system enhancement of ~{dens_need:.0e}x would supply the whole factor, is not excluded by
     planetary dynamics ({dens_need*RHO_LOCAL*(4/3)*math.pi*AU**3/1.989e30:.0e} M_sun inside 1 AU), and is the one surviving door.  Also not
     computed: the extra force from grad a0 if such a gradient existed.

  6. What this does NOT touch: the a0 coefficient, lensing, the CMB pass, the RAR fit, the BTFR, the
     no-ghost theorem, c_T = 1.  It touches the ephemeris ledger only -- and it says that ledger has
     been carrying a relief it is not entitled to.
""")

n = len(FAILED)
print(f"I001 CHECKS: {NCHK[0]-n}/{NCHK[0]} passed" + ("" if not n else f";  FAILED: {FAILED}"))
sys.exit(1 if FAILED else 0)
