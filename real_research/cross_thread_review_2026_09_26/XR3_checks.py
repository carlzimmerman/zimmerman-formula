#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
XR3_checks -- small numerical checks behind XR3_obligations.md (cross-thread review, 2026-09-26).

Read-only with respect to every other file in the repository: this script imports nothing from the repo, reruns
no lane, and writes only its own stdout (redirect to XR3_checks.out). Runtime: a few seconds.

WHAT IT CHECKS (each number is quoted in XR3_obligations.md)
  K1  nu_mono's splice (definition in the recipe's user-decision block / L340 A1): where the max() switches branch,
      the value of C_L there, and the left/right values of dC_L/dy (the "next constitutive derivative").
  K2  the largest |log10(nu_mono/nu_RAR)| and where it sits; whether nu_mono == nu_RAR all the way to y_p.
  K3  the response/inertia variable of the lead track's D1/D3 analysis, E = 2C/(1+C), for nu_mono in both
      directions over y in [1e-12, 1e12] (the exact-law obstruction needs E < 0).
  K4  the L340 frozen scalar block N = 2 - alpha(1+C): the small-y value where N = 0 (static-gain pole) at both
      ends of L340's alpha_c window, for the transverse (C_T = nu - 1) and longitudinal (C_L = h') directions.
  K5  c_s^2 = B N/((2+3B) D) of the same block, unfiltered (k -> 0 side, the largest C), at sample y.
  K6  the MOND-normalised gate coupling b = B/(M^2 Lambda) at a galaxy's gate edge (order of magnitude: only the
      constitutive part a0^2 (Q - Z) of the lead track's B = dL0/df is kept; kappa = 1/2 so a0^2/Lambda = 1/(32 pi)
      in c = 1 units), with y_edge from DE1's edge table at the linear gate (p = 1, x_c0 = 2.5, M_b = 1e11,
      canonical), and whether the lead track's published SUFFICIENT inequalities for the concave repair
      (closure_doors_2026_09_26/environment_gate/REPORT.md sec. 3) can be met with c_2 <= 0.067 (L340's window top).
      Infeasible sufficient inequalities are NOT an instability: they only say the witness does not cover that b.

Run from the repository root:  python3 real_research/cross_thread_review_2026_09_26/XR3_checks.py
"""
import math
import numpy as np
import sympy as sp
from scipy.optimize import brentq

np.seterr(all="ignore")                              # overflow of exp(sqrt(y)) at y >~ 5e5 on L340's grid is harmless
P = lambda *a: print(*a, flush=True)

# ----------------------------------------------------------------------------------------------- the kernel (a0 = 1)
def h_rar(y):
    y = np.asarray(y, float)
    with np.errstate(over="ignore", invalid="ignore"):
        return np.where(y < 1e4, y / np.expm1(np.sqrt(np.clip(y, 1e-300, 1e4))), 0.0)

ys_ = sp.symbols("y", positive=True)
z_ = sp.sqrt(ys_)
h_sym = ys_ / (sp.exp(z_) - 1)
dh_sym = sp.diff(h_sym, ys_)
d2h_sym = sp.diff(h_sym, ys_, 2)
dh_rar = sp.lambdify(ys_, dh_sym, "numpy")
d2h_rar = sp.lambdify(ys_, d2h_sym, "numpy")

def dh_stable(y):    # h'_RAR(y) = [2(e^z - 1) - z e^z] / [2 (e^z - 1)^2], z = sqrt(y), written with expm1
    z = math.sqrt(y); em = math.expm1(z)
    return (2 * em - z * (1 + em)) / (2 * em * em)

Y_P = brentq(lambda y: float(dh_rar(y)), 1.0, 5.0)
H_P = float(h_rar(Y_P))
DELTA = 0.05
tail = lambda y: DELTA * H_P / (y + Y_P)
Y_STAR = brentq(lambda y: float(dh_rar(y)) - tail(y), 1.0, Y_P)

# L340's own construction of h_mono (same grid, same trapezoid), so K2 compares like with like
LYG = np.linspace(-12, 12, 240001); YG = 10 ** LYG
DHM = np.maximum(np.nan_to_num(dh_rar(YG), nan=0.0), tail(YG))
HM = float(h_rar(YG[0])) + np.concatenate([[0.0], np.cumsum(0.5 * (DHM[1:] + DHM[:-1]) * np.diff(YG))])
def h_mono(y):
    return np.interp(np.log10(np.asarray(y, float)), LYG, HM)
def nu_mono(y):
    y = np.asarray(y, float); return 1.0 + h_mono(y) / y
def nu_rar(y):
    y = np.asarray(y, float); return 1.0 / (-np.expm1(-np.sqrt(y)))
def CL_mono(y):
    y = np.asarray(y, float)
    return np.maximum(np.nan_to_num(dh_rar(y), nan=0.0), tail(y))

P("=" * 100); P("K1  nu_mono's splice"); P("=" * 100)
P(f"  y_p (phantom peak of nu_RAR) = {Y_P:.10f},  h_p = {H_P:.10f} a0,  delta = {DELTA}")
P(f"  branch switch y* (h'_RAR = delta h_p/(y+y_p)) = {Y_STAR:.10f}   (below y_p: nu_mono = nu_RAR only for y <= y*)")
CL_star = tail(Y_STAR)
left = float(d2h_rar(Y_STAR)); right = -DELTA * H_P / (Y_STAR + Y_P) ** 2
P(f"  C_L(y*) = {CL_star:.10f}   dC_L/dy left = {left:.10f}   right = {right:.10f}   jump = {right - left:+.6f}")
P("  -> C_L is continuous and positive; its derivative jumps: nu_mono's phantom is C^1 in h' (C^{1,1}), not C^2.")

P("\n" + "=" * 100); P("K2  nu_mono vs nu_RAR"); P("=" * 100)
yy = np.logspace(-3, 4, 70001)
d = np.log10(nu_mono(yy) / nu_rar(yy))
i = int(np.argmax(np.abs(d)))
P(f"  max |log10(nu_mono/nu_RAR)| on 1e-3..1e4 = {abs(d[i]):.5f} dex at y = {yy[i]:.2f}   (L340 A1 stored: 0.0104 dex at 14.3)")
band = (yy > Y_STAR) & (yy <= Y_P)
P(f"  on (y*, y_p]: max |log10(nu_mono/nu_RAR)| = {np.abs(d[band]).max():.2e} dex (nonzero, tiny)")
yb = np.logspace(-3, np.log10(Y_STAR) - 1e-3, 2000)
P(f"  on [1e-3, y*): max |log10(nu_mono/nu_RAR)| = {np.abs(np.log10(nu_mono(yb) / nu_rar(yb))).max():.2e} dex (grid/trapezoid level)")

P("\n" + "=" * 100); P("K3  E = 2C/(1+C) for nu_mono (the lead track's D1/D3 variable; its exact-law obstruction needs E < 0)"); P("=" * 100)
yw = np.logspace(-12, 12, 24001)
CT = nu_mono(yw) - 1.0; CLv = CL_mono(yw)
ET = 2 * CT / (1 + CT); EL = 2 * CLv / (1 + CLv)
P(f"  C_T in [{CT.min():.3e}, {CT.max():.3e}],  C_L in [{CLv.min():.3e}, {CLv.max():.3e}]")
P(f"  E_T in [{ET.min():.3e}, {ET.max():.6f}],  E_L in [{EL.min():.3e}, {EL.max():.6f}]   -> 0 < E < 2 at every y sampled")
x = 2.0
P(f"  contrast, exact mu_exp at x = 2: E_L = 2(1-x)e^-x = {2 * (1 - x) * math.exp(-x):+.6f} (negative: the obstruction)")
P(f"  regular (r = 0) branch restoring coefficient 2(2-E)/E > 0 for 0 < E < 2: min over samples = "
  f"{min((2 * (2 - ET) / ET).min(), (2 * (2 - EL) / EL).min()):.3e}")

P("\n" + "=" * 100); P("K4  L340 frozen block: the small-y zero of N = 2 - alpha(1 + C)"); P("=" * 100)
for al in (9.6240479669e-14, 3.2e-9):
    # nu_mono = nu_RAR for y < y*, so use the closed forms there (L340's grid starts at 1e-12); expm1 keeps precision
    yT = brentq(lambda y: float(nu_rar(y)) - 2.0 / al, 1e-45, 1e-3, xtol=1e-60, rtol=1e-14)
    yL = brentq(lambda y: 1.0 + dh_stable(y) - 2.0 / al, 1e-45, 1e-3, xtol=1e-60, rtol=1e-14)
    P(f"  alpha_c = {al:.3e}: transverse N = 0 at y = {yT:.3e} (~(alpha/2)^2 = {(al / 2) ** 2:.3e}); "
      f"longitudinal at y = {yL:.3e} (~(alpha/4)^2 = {(al / 4) ** 2:.3e})")
P("  below these y the frozen block's static gain has a pole and N < 0; every zero of the filtered field has such a")
P("  neighbourhood (tiny, and far inside the heat-filter scale, so the frozen-coefficient reading does not apply there).")

P("\n" + "=" * 100); P("K5  c_s^2 of the same block, unfiltered C = C_T (the largest C a mode can see), alpha_c = 1e-9"); P("=" * 100)
al = 1e-9
for B in (7.3e-3, 0.067):
    row = []
    for y in (1e-6, 1e-4, 1e-2, 1.0, 1e2, 1e4):
        C = float(nu_mono(y)) - 1.0
        D = al + (al + 2) * C; N = 2 - al * (1 + C)
        cs2 = B * N / ((2 + 3 * B) * D)
        row.append(f"y={y:g}: c_s/c={math.sqrt(cs2):.3g}")
    P(f"  c_2 = {B}: " + "; ".join(row))
P("  -> superluminal where C is small (allowed under criterion B), -> 0 as y -> 0 (no uniform lower bound).")

P("\n" + "=" * 100); P("K6  MOND-normalised gate coupling b at the gate edge vs the lead track's sufficient window"); P("=" * 100)
def QmZ(y):          # Q(Z) - Z = 2 int_0^y h_mono(s) ds, Z = y^2
    s = np.logspace(-14, np.log10(y), 20001)
    return 2 * np.trapz(h_mono(s), s)
# DE1 edge table, p = 1, x_c0 = 2.5, canonical, M_b = 1e11: r_e/r_flag, with y_flag = 0.1 (point-mass exterior)
RATIO = {0.5: 23.81, 1.0: 13.34, 1.5: 7.81, 2.0: 4.84, 2.5: 3.17, 3.0: 2.17, 3.5: 1.54, 4.0: 1.13}
XC = 0.6862 * 2.5                                  # x_c = Omega_L0 x_c0 (lead track's normalisation remark)
R3 = math.sqrt(3.0)
def feasible(b, eps, xc, c2max=0.067):
    C0 = 1 + 729 / (64 * xc ** 2 * eps ** 2)
    best = None
    for dl in np.linspace(1e-4, c2max, 2000):
        eta = 160 * C0 * b + 84672 * R3 * C0 * b ** 2 / (dl * math.sqrt(eps))
        if eta * math.pi >= 1:                      # eta pi < 1
            continue
        need_c2 = b * (528 * R3 / math.sqrt(eps) + 36 / (xc * eps)) + 2 * math.pi * eta / 3 + dl
        if best is None or need_c2 < best[0]:
            best = (need_c2, dl, eta)
    return best
P(f"  x_c = Omega_L0 x_c0 = {XC:.4f}; witness in the lead track's report: b = 1e-10 at eps = x_c = 1")
for zz, rr in RATIO.items():
    y_e = 0.1 / rr ** 2
    b = QmZ(y_e) / (32 * math.pi)
    out = []
    for eps in (1.0, 10.0, 100.0):
        best = feasible(b, eps, XC)
        out.append(f"eps={eps:g}: " + ("none" if best is None else f"c2 >= {best[0]:.3g}"))
    P(f"  z = {zz:3.1f}: y_edge = {y_e:.2e}, b ~ {b:.2e};  smallest c_2 the sufficient inequalities allow: " + ", ".join(out))
P("  -> the published constant-B witness covers low-z galaxy edges; at z >~ 2.5-3 (y_edge >~ 0.01) the sufficient")
P("     window needs c_2 above L340's window top (0.067) at eps ~ 1, and larger eps shifts the z ~ 0 threshold by")
P("     1 + eps Lambda^2/K^4. The actual reduced operator at the MOND-normalised B has to be computed (calc 3).")

P("\nZ check: sqrt(32 pi/3) = %.6f (kappa = 1/2 restated; Z^2 = 8 pi/(3 kappa^2))" % math.sqrt(32 * math.pi / 3))
