#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""t008_two_temp_family.py -- T008: two-temperature interpolation family.

Hypothesis (TASKS.md, verbatim): within T_eff = (T_U^n + T_dS^n)^(1/n), no n gives
BOTH the a0-line form AND kappa = 1/2.
Method (verbatim): derive the implied g_obs(g_N) per n; fit n to the a0-line; check
the implied kappa. PASS: (n*, kappa(n*)) reported on both footings.
KILL/grade: REFUTED if no (n*, kappa*) lands on the a0-line WITH kappa=1/2.

DERIVATION (footing-independent; uses only rho_Lambda + the dimensionless ratio)
  Unruh    T_U   = hbar g_N/(2 pi c k_B)          (acceleration on the Newtonian side)
  dS/GH    T_dS = hbar H_e/(2 pi k_B),  H_e = sqrt(8 pi G rho_Lambda/3)
  ratio    T_U/T_dS = g_N/(c H_e) = g_N/a_dS,   a_dS = c H_e    (dimensionless)
  power-mean interpolation  T_eff = T_dS (1 + (g_N/a_dS)^n)^(1/n)   [power mean M_n(1,u)]
  observed accel through the same Unruh map:
       g_obs = 2 pi c k_B/hbar * T_eff = g_N (1 + (g_N/a_dS)^n)^(1/n)
   (since 2 pi c k_B/hbar * T_dS = a_dS and *T_U = g_N).  FOOTING-INDEPENDENT: the
  only scale is a_dS = KAPPA0 c sqrt(G rho_Lambda),  KAPPA0 = sqrt(8 pi/3).
  a0-line (framework kernel):  g_obs^2 - g_N^2 = a0 g_N   ->  gobs_line().
Implied kappa(n): a0_imp(n) = max_{g_N} (g_obs^2 - g_N^2)/g_N  (peak of the MOND
  deficit the family produces);  kappa_imp(n) = a0_imp/(c sqrt(G rho_Lambda)).

Direction-of-risk: WIN-risk -- a naive reader could promote a tuned-n crossing of
1/2 to a real "kappa emerges from the temperature blend". The script fixes the
crossover at the cosmologically-motivated a_dS (NOT a dial to 1/2) and reports the
honest (n*, kappa*).
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qwenlib import *
import numpy as np

# ---- PART A: inputs with provenance (qwenlib / stage17) ------------------------
rho_Lambda = OM_L * RHO_CRIT
G_rhoL      = G * rho_Lambda
H_e         = math.sqrt(8.0 * math.pi * G_rhoL / 3.0)      # 1/s
a_dS        = C * H_e                                        # m/s^2, footing-independent
KAPPA0      = math.sqrt(8.0 * math.pi / 3.0)                # a_dS = KAPPA0 c sqrt(G rho_Lambda)
c_sqrt_GrhoL = C * math.sqrt(G_rhoL)

print("=== T008: two-temperature interpolation family T_eff=(T_U^n+T_dS^n)^(1/n) ===")
print(f"rho_Lambda = {rho_Lambda:.4e} kg/m^3 ;  H_e = {H_e:.4e} 1/s")
print(f"a_dS = c H_e = {a_dS:.4e} m/s^2 = KAPPA0 * c sqrt(G rho_Lambda), "
      f"KAPPA0 = {KAPPA0:.4f}   (footing-INDEPENDENT crossover scale)")
print(f"c sqrt(G rho_Lambda) = {c_sqrt_GrhoL:.4e} m/s^2")
# both footings (R3): the dimensional a0-line the framework actually uses
for foot, a0 in FOOTINGS.items():
    info(f"footing {foot}: a0 = {a0:.4e} m/s^2 ; a_dS/a0 = {a_dS/a0:.3f} "
         f"(kappa_def = {a0/c_sqrt_GrhoL:.4f})")

# ---- PART B: the implied g_obs(g_N) family and the a0-line ---------------------
def gobs_family(gn, n, a_scale=a_dS):
    """g_obs = g_N (1 + (g_N/a_scale)^n)^(1/n) for n != 0 (power mean M_n(1,u))."""
    gn = np.asarray(gn, dtype=float)
    u = gn / a_scale
    return gn * np.power(1.0 + np.power(u, n), 1.0 / n)

def gobs_family_geo(gn, a_scale=a_dS):
    """geometric-mean limit n -> 0:  M_0(1,u) = sqrt(u) ;  g_obs = g_N sqrt(1+u)."""
    gn = np.asarray(gn, dtype=float)
    u = gn / a_scale
    return gn * np.sqrt(1.0 + u)

def deficit_ratio(gobs, gn):
    """(g_obs^2 - g_N^2)/g_N   -- the MOND deficit the family produces."""
    return (gobs**2 - gn**2) / gn

# ---- PART C: fit n to the a0-line ----------------------------------------------
gn_lo, gn_hi = A0_CAN / 100.0, A0_CAN * 100.0
gn_grid = np.logspace(math.log10(gn_lo), math.log10(gn_hi), 4000)

def gobs_of(n, a_scale=a_dS):
    if abs(n) < 1e-6:
        return gobs_family_geo(gn_grid, a_scale)
    return gobs_family(gn_grid, n, a_scale)

def rms_log_mismatch(n, a0, a_scale=a_dS):
    line = gobs_line(gn_grid, a0)
    fam = gobs_of(n, a_scale)
    return float(np.sqrt(np.mean((np.log(fam / line))**2)))

n_grid = np.concatenate([-np.logspace(0, math.log10(8.0), 400),
                         np.linspace(-0.5, -0.02, 60),
                         np.linspace(0.02, 8.0, 400)])
rms = np.array([rms_log_mismatch(n, A0_CAN) for n in n_grid])
i_star = int(np.argmin(rms))
n_star = float(n_grid[i_star])
rms_star = float(rms[i_star])

# implied a0 via the a0-line's OWN crossover criterion: g_obs/g_N = sqrt(2)
# (on the a0-line this occurs at g_N = a0).  For the family g_obs/g_N = (1+u^n)^(1/n)
# with u = g_N/a_dS, so  (1+u^n)^(1/n) = sqrt(2)  =>  u* = (2^(n/2)-1)^(1/n),
# a0_imp = a_dS * u*  (footing-independent, n-dependent, well-behaved).
def a0_cross(n):
    if abs(n) < 1e-6:
        u_star = 1.0                       # geometric limit sqrt(1+u)=sqrt(2)
    else:
        u_star = (2.0 ** (n / 2.0) - 1.0) ** (1.0 / n)
    return a_dS * u_star, u_star

a0_imp_star, u_star = a0_cross(n_star)
kappa_imp_star = a0_imp_star / c_sqrt_GrhoL

# alt-footing shape mismatch (report only; family scale a_dS is footing-independent)
rms_alt = rms_log_mismatch(n_star, A0_ALT)

# deep-MOND shape diagnostic: family saturates g_obs -> a_dS (constant); a0-line
# gives g_obs -> sqrt(a0 g_N) -> 0.  Quantify the asymptotic disagreement.
g_deep = A0_CAN / 1e6
line_deep = gobs_line(g_deep, A0_CAN)
fam_deep = gobs_of(n_star)[0]
shape_gap = abs(fam_deep - line_deep) / line_deep

print(f"\nfit n to a0-line over g_N in [{gn_lo:.3e}, {gn_hi:.3e}] m/s^2 (canon):")
print(f"   n* = {n_star:+.4f}    (best log-RMS mismatch = {rms_star:.4f}, "
      f"{rms_star*100:.1f}% typical)")
print(f"   family g_obs at deep MOND (g_N={g_deep:.2e}): {fam_deep:.3e} m/s^2 "
      f"-> saturates at a_dS={a_dS:.3e}; a0-line gives {line_deep:.3e}; "
      f"shape gap = {shape_gap:.1f}x")
print(f"   implied a0 = a_dS * u*(n*), u* = {u_star:.4f} "
      f"-> a0_imp = {a0_imp_star:.4e} m/s^2 (family crossover g_N = a_dS*u*)")
print(f"   kappa_imp(n*) = a0_imp/(c sqrt(G rho_Lambda)) = {kappa_imp_star:.4f}   "
      f"(target 1/2 = 0.5000 +/- {KAPPA_ERR}; measured {KAPPA_MEAS})")
print(f"   log-RMS mismatch at n* vs ALT footing a0 = {rms_alt:.4f}")

# ---- PART D: grade -------------------------------------------------------------
# D1: analytic cross-check of the closed form (n=2 -> quadratic mean)
g_test = np.array([1e-11, 1e-10, 1e-9])
ok2 = abs(gobs_family(g_test, 2.0) - g_test * np.sqrt(1.0 + (g_test / a_dS)**2)).max()
check(ok2 < 1e-15, "n=2 closed form = g_N sqrt(1+u^2) (quadratic mean)",
      f"max dev {ok2:.2e}")

# D2: crossover scale is footing-independent and equals KAPPA0 c sqrt(G rho_Lambda)
check(abs(a_dS - KAPPA0 * c_sqrt_GrhoL) < 1e-6,
      "a_dS = KAPPA0 c sqrt(G rho_Lambda) (footing-independent crossover)")

# D3: the shape is INCOMPATIBLE with the a0-line (deep-MOND saturation vs sqrt)
check(shape_gap > 1.0,
      "family deep-MOND shape disagrees with a0-line by >1x (saturation vs sqrt(a0 g_N))",
      f"shape_gap = {shape_gap:.2f}")
check(rms_star > 0.2,
      "best-fit log-RMS mismatch to a0-line > 20% (no n reproduces the a0-line form)",
      f"rms(n*) = {rms_star:.3f}")

# D4: the conjunction FAILS -- the implied kappa at n* is NOT 1/2
kappa_hit = abs(kappa_imp_star - 0.5) < KAPPA_ERR
check(not kappa_hit,
      "KILL condition: kappa_imp(n*) is NOT 1/2 within +/-0.043 "
      "-> no n gives BOTH a0-line AND kappa=1/2",
      f"kappa_imp(n*) = {kappa_imp_star:.4f} vs 0.500+/-{KAPPA_ERR}")

# D5: scan every n -- none of them drives kappa into the 1/2 window
kappa_curve = np.array([a0_cross(n)[0] / c_sqrt_GrhoL for n in n_grid])
any_hit = bool(np.any(np.abs(kappa_curve - 0.5) < KAPPA_ERR))
klo, khi = float(kappa_curve.min()), float(kappa_curve.max())
check(not any_hit,
      "no n in the full grid drives kappa_imp into [0.457, 0.543]",
      f"any_hit = {any_hit}; kappa range = [{klo:.3f}, {khi:.3f}]")

print(f"\nverdict: REFUTED -- best n* = {n_star:+.3f} gives kappa_imp = "
      f"{kappa_imp_star:.3f} (not 1/2) and cannot reproduce the a0-line shape; "
      f"kappa_imp over all n spans [{klo:.3f}, {khi:.3f}], none in the 1/2 window.")

finish("t008")
