#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
R01 -- CERTIFY THE ACTUAL ACTIVE-DENSITY ASYMPTOTE (L304 surrogate audit).

Target (from FOLLOWUP_PACKETS.md R01):  for B,D>0, 0<K<2 and u>0, prove
    rho_act = (w-1)*rho = (2/3)(2-K) D u^3
from the displayed rho and w, and with u(B+u) = A/r, A>0, prove
    r*u -> A/B   and   r^3 * rho_act -> (2/3)(2-K) D (A/B)^3.

Load-bearing status: L304 V4 reads its fitted slope 0.58 as "M_act ~ sqrt(r)"
(gate 0.4-0.7) and L311 V2 builds the r^{1/8} velocity-rise prediction on
M_act = K sqrt(r).  R01/R02 test whether the fitted power is a finite-window
artifact of the exact C/r^3 shell (M ~ M0 + 4 pi C ln(r/r0), NOT sqrt r).
"""
import json, os, math
import numpy as np
import sympy as sp

OUT = {"lane": "R01", "checks": {}, "numbers": {}}
CH = []

def check(name, measured, ok, reading=""):
    CH.append(bool(ok)); OUT["checks"][name] = {"ok": ok, "measured": str(measured)}
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    print(f"         measured: {measured}")
    if reading: print(f"         reading:  {reading}")

# ---------------------------------------------------------------- exact (sympy)
K, B, D, u, A, r = sp.symbols("K B D u A r", positive=True)
rho = (2 - K) * D * (B * u ** 2 + sp.Rational(2, 3) * u ** 3)
w1 = (sp.Rational(2, 3) * u) / (B + sp.Rational(2, 3) * u)
rho_act = sp.simplify(w1 * rho)
target = sp.Rational(2, 3) * (2 - K) * D * u ** 3
resid = sp.simplify(rho_act - target)
check("N1 the exact factorization cancels B + 2u/3: (w-1)*rho = (2/3)(2-K) D u^3 identically",
      f"residual = {resid}", resid == 0,
      "exact for every u>0, not an asymptotic statement")

u_root = 2 * A / (r * (B + sp.sqrt(B ** 2 + 4 * A / r)))
ru = sp.simplify(u_root * r)
ru_lim = sp.limit(ru, r, sp.oo)
check("N2 the rationalized root gives r*u -> A/B at large r",
      f"r*u = {ru}; limit = {ru_lim}", sp.simplify(ru_lim - A / B) == 0,
      "u ~ A/(B r) deep-corner; the positive root keeps ru monotone and avoids cancellation")

r3ra = sp.simplify(r ** 3 * (sp.Rational(2, 3) * (2 - K) * D * u_root ** 3))
r3ra_lim = sp.limit(r3ra, r, sp.oo)
C_sym = sp.Rational(2, 3) * (2 - K) * D * (A / B) ** 3
check("N3 the asymptotic active shell: r^3 rho_act -> (2/3)(2-K) D (A/B)^3",
      f"limit = {r3ra_lim}; target = {C_sym}", sp.simplify(r3ra_lim - C_sym) == 0,
      "rho_act ~ C/r^3 exactly at the deep corner: M_act ~ M0 + 4 pi C ln r, NOT sqrt r")

# ---------------------------------------------------------------- numeric on L304's profile
G, a0, KBn = 6.6743e-11, 9.3619e-11, 0.2
Bn = (2 - KBn) / (2 - 2.5e-5)
a0t = a0 / Bn ** 2
KPC = 3.0856775814913673e19
MSUN = 1.98892e30
M = 6e10 * MSUN

# L304's own profile:  u(B+u) = g / ((2-K) a0t),  g = a0 sqrt(gN/a0) = sqrt(a0 gN) = sqrt(a0 G M)/r
A_num = math.sqrt(a0 * G * M) / ((2 - KBn) * a0t)          # so u(B+u) = A_num / r  (m)
C_num = (2 / 3) * (2 - KBn) * a0t ** 2 * (A_num / Bn) ** 3  # the asymptotic shell constant (1/m^2... units of rho*r^3)
D_num = a0t ** 2

rkpc = np.logspace(3, 5, 200)                               # L304's V4 window: 1 Mpc .. 100 Mpc
r = rkpc * KPC
s = (G * M / r ** 2) / a0
g = a0 * np.sqrt(np.maximum(s, 0))
uu = (-Bn + np.sqrt(np.maximum(Bn ** 2 + 4 * g / ((2 - KBn) * a0t), 0))) / 2
rho_act_num = (2 / 3) * (2 - KBn) * D_num * uu ** 3          # exact factorization
r3_rho = r ** 3 * rho_act_num
r3_asym = np.full_like(r, C_num)
# relative approach of r^3 rho_act to the asymptotic constant on the window tail:
rel = np.abs(r3_rho / r3_asym - 1.0)
tail = rel[150:]

check("N4 on L304's own window (1-100 Mpc, MW) the profile is already the C/r^3 shell: "
      "r^3 rho_act within 1% of the asymptotic constant at the window end",
      f"median |rel-1| on the outer 25% = {np.median(tail):.3e}, max = {np.max(tail):.3e}",
      np.max(tail) < 0.01,
      "the deep corner is reached inside the fitted window, so the window fit must see the log shell")

# M_act(<r) two ways: (a) L304's cumulative integral starting AT the first grid point (M0 = 0);
# (b) the exact shell law from an interior anchor.  L304 integrates from index 0 -> interior mass set to zero.
Mact_zero0 = np.array([4 * np.pi * np.trapz(rho_act_num[:i + 1] * r[:i + 1] ** 2, r[:i + 1])
                       for i in range(0, len(r), 10)])
sl_z0 = float(np.polyfit(np.log(r[::10][Mact_zero0 > 0]), np.log(Mact_zero0[Mact_zero0 > 0]), 1)[0])
OUT["numbers"]["slope_zeroM0_window"] = sl_z0

# pure-log shell on the same sampled interval, zero mass at the lower cutoff (r0 = 1 Mpc):
# (skip the zero-mass point at the first grid node, exactly as L304's Mact > 0 filter does)
C_in = C_num
r0 = rkpc[0] * KPC
Mlog = 4 * np.pi * C_in * np.log(r / r0)
mpos = Mlog[::10] > 0
sl_log = float(np.polyfit(np.log(r[::10][mpos]), np.log(Mlog[::10][mpos]), 1)[0])
OUT["numbers"]["slope_pure_log_same_window"] = sl_log

check("N5 the fitted 0.58 IS the pure-log window artifact: a pure C/r^3 shell integrated with "
      "zero mass at the lower cutoff fits r^0.578 on L304's exact sampled interval and step",
      f"L304-style fit {sl_z0:.3f}; pure-log fit {sl_log:.3f}",
      abs(sl_log - 0.578) < 0.01,
      "the same window, the same zero-M0 convention: no sqrt(r) law is needed to produce 0.58")

# ---------------------------------------------------------------- the honest law
# With the interior mass tracked (integrate from an inner radius where the shell starts, e.g. 0.1 kpc),
# M_act(r) = M0 + 4 pi C ln(r/r0):  the fit exponent is then window- and M0-dependent.
r_in = np.logspace(-1, 5, 400) * KPC
ss = (G * M / r_in ** 2) / a0
gg = a0 * np.sqrt(np.maximum(ss, 0))
uu_i = (-Bn + np.sqrt(np.maximum(Bn ** 2 + 4 * gg / ((2 - KBn) * a0t), 0))) / 2
rho_i = (2 / 3) * (2 - KBn) * D_num * uu_i ** 3
cum = np.array([4 * np.pi * np.trapz(rho_i[:j + 1] * r_in[:j + 1] ** 2, r_in[:j + 1])
                for j in range(0, len(r_in), 4)])
r_a = r_in[::4]
# interior mass below the 1-100 Mpc window (integrated on the fine grid up to 1 Mpc):
i_win = np.min(np.nonzero(r_a >= rkpc[0] * KPC)[0])
M0_true = float(cum[i_win - 1])
w_win = r_a[i_win:] >= rkpc[0] * KPC
sl_full = float(np.polyfit(np.log(r_a[i_win:][w_win][5:]), np.log(cum[i_win:][w_win][5:]), 1)[0])
OUT["numbers"]["M0_below_1Mpc"] = M0_true
OUT["numbers"]["slope_with_M0_window60pc"] = sl_full
# the log-shape check: M - M0 vs ln r must be linear on the window's converged tail:
lnr = np.log(r_a[i_win:][w_win][5:])
fit = np.polyfit(lnr, cum[i_win:][w_win][5:] - M0_true, 1)
pred = np.polyval(fit, lnr)
rel_resid = float(np.max(np.abs(pred - (cum[i_win:][w_win][5:] - M0_true)))
                  / max(np.ptp(cum[i_win:][w_win][5:]), 1e-300))
check("N6 with the interior mass tracked, the active mass follows the LOG shell, not sqrt(r): "
      "the max relative residual of a linear fit in ln r is below 0.1% on the window's tail",
      f"M0(<1 Mpc) = {M0_true:.3e} kg; max relative residual = {rel_resid:.2e}",
      rel_resid < 1e-3,
      "M_act = M0 + 4 pi C ln(r/r0); the sqrt reading of L304 V4 / L311 V2 is a window artifact")

# ---------------------------------------------------------------- remainder bound (N7)
# |r^3 rho_act - C| <= 3 C A/(B^2 r) + O(1/r^2):  verify numerically the bound constant.
alpha = A_num / (Bn ** 2)                                   # meters
bound = 3 * C_num * alpha / r
ratio = np.abs(r3_rho - C_num) / np.maximum(bound, 1e-300)
check("N7 the finite-radius remainder bound holds: |r^3 rho_act - C| <= 3 C A/(B^2 r) on the window",
      f"max |resid|/bound = {np.max(ratio):.3f} (<= 1)",
      np.max(ratio) < 1.0,
      "a usable remainder bound for R02's finite-window correction of the shell integral")

# ---------------------------------------------------------------- verdict
print("\nR01 COMPLETE:", f"{sum(CH)}/{len(CH)} checks PASS")
json.dump(OUT, open(os.path.splitext(os.path.abspath(__file__))[0] + "_results.json", "w"), indent=1, default=str)
import sys; sys.exit(0 if all(CH) else 1)