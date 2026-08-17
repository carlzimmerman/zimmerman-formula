#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""t004_response_function_scan.py -- T004: no linear-response function (Boltzmann,
Wigner, Gaussian smearing sigma in [0.1,10]) in the dS-Unruh balance yields kappa=1/2
UNTUNED.

Hypothesis (TASKS.md): no linear-response function in the dS-Unruh balance yields
kappa = 1/2 untuned.
Method: numeric balance integral per response; solve for the implied kappa.
PASS criteria (verbatim): the scan table + NULL/verdict.
KILL criteria (verbatim): an UNTUNED 1/2 appears -> CANDIDATE + escalate.
Search: YES -- the Gaussian sigma sweep. Pre-registered in REGISTRY_FDR.md on 2026-08-17
(3 untuned natural params; the sigma sweep is a DIAGNOSTIC dial, excluded from the
untuned count).
Direction-of-risk: WIN-risk -- a naive reader could promote a tuned Gaussian-sigma
crossing of 1/2 to a real emergence; the script separates TUNED (sigma dialed to hit
1/2) from UNTUNED (Boltzmann/Wigner as-stated, Gaussian sigma=1).
"""
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qwenlib import *
import numpy as np

# ---- PART A: inputs with provenance -------------------------------------------------
# Framework: a0 = kappa * c * sqrt(G rho_Lambda).  dS accel a_dS = c H_e,
# H_e = sqrt(8 pi G rho_Lambda / 3) (Gibbons-Hawking).  Unruh T_U = hbar a/(2 pi c k_B);
# dS T_dS = hbar c H_e/(2 pi k_B).  Balance T_U(a_phys) = T_dS with the response-corrected
# physical acceleration a_phys = c H_e * m_R, where m_R = response-weighted mean of the
# dimensionless x = a/a_dS:   m_R = [integral x R(x) dx] / [integral R(x) dx].
# Substituting a0 = c H_e m_R  =>  kappa = m_R * c H_e / (c sqrt(G rho_Lambda))
#                            = m_R * H_e / sqrt(G rho_Lambda)
#                            = m_R * sqrt(8 pi / 3)        [H_e = sqrt(8pi/3) sqrt(G rho_Lambda)]
# So kappa_implied = KAPPA0 * m_R,  KAPPA0 = sqrt(8 pi / 3).  This is FOOTING-INDEPENDENT
# (uses only rho_Lambda and the dimensionless m_R).  The dimensional a0/a_dS are still
# reported on BOTH footings (R3).
rho_Lambda = OM_L * RHO_CRIT                       # qwenlib / stage17
G_rhoL     = G * rho_Lambda
H_e        = math.sqrt(8.0 * math.pi * G_rhoL / 3.0)   # 1/s
a_dS       = C * H_e                                  # m/s^2, footing-independent
KAPPA0     = math.sqrt(8.0 * math.pi / 3.0)          # no-response coefficient ~2.903

print("=== T004: dS-Unruh response-function scan ===")
print(f"rho_Lambda = {rho_Lambda:.4e} kg/m^3 ;  H_e = {H_e:.4e} 1/s ;  a_dS = c H_e = {a_dS:.4e} m/s^2")
# both footings (R3): the dimensional a0 the framework actually uses, and the kappa it
# implies by the bare a0 = kappa c sqrt(G rho_Lambda) definition (a bookkeeping cross-check).
c_sqrt_GrhoL = C * math.sqrt(G_rhoL)
for foot, a0 in FOOTINGS.items():
    info(f"footing {foot}: a0 = {a0:.4e} m/s^2 -> kappa_def = {a0/c_sqrt_GrhoL:.4f}; "
         f"a_dS/a0 = {a_dS/a0:.4f}")

# ---- response functions R(x), x = a/a_dS dimensionless ------------------------------
def R_boltz(x):
    return np.exp(-x)

def R_wigner(x):
    x = np.asarray(x, dtype=float)
    out = np.zeros_like(x)
    m = (x >= 0.0) & (x <= 1.0)
    out[m] = 1.0 - x[m]**2
    return out

def R_gauss(x, s):
    x = np.asarray(x, dtype=float)
    return np.exp(-x * x / (2.0 * s * s))

def m_R(R, x_max=50.0, n=400001):
    """response-weighted mean of x:  m_R = integral x R(x) dx / integral R(x) dx."""
    xs = np.linspace(0.0, x_max, n)
    Rv = R(xs)
    num = np.trapz(xs * Rv, xs)
    den = np.trapz(Rv, xs)
    return num / den

# ---- PART B: the scan ---------------------------------------------------------------
KAP = 0.5                       # the 1/2 to look for (ADOPTED; measured 0.551+-0.043)
TOL = KAPPA_ERR                # 0.043 hit window (the kappa measurement error)

rows = []
mB = m_R(R_boltz)
kB = KAPPA0 * mB
rows.append(("Boltzmann e^-x", "natural", mB, kB))
mW = m_R(R_wigner, x_max=1.0, n=400001)
kW = KAPPA0 * mW
rows.append(("Wigner (1-x^2)Th", "natural", mW, kW))

# Gaussian: sweep sigma in [0.1, 10] (diagnostic dial) + the natural sigma=1
sigma_grid = np.logspace(math.log10(0.1), math.log10(10.0), 200)
k_gauss = np.array([KAPPA0 * m_R(lambda x, s=s: R_gauss(x, s), x_max=60.0) for s in sigma_grid])
mG1 = m_R(lambda x: R_gauss(x, 1.0), x_max=60.0)
rows.append(("Gaussian sigma=1", "natural", mG1, KAPPA0 * mG1))

print(f"\n{'response':<22}{'param':<9}{'m_R':>10}{'kappa_imp':>12}")
print("-" * 53)
for name, param, mR, k in rows:
    flag = "  <-- |k-0.5|<0.043" if abs(k - KAP) < TOL else ""
    print(f"{name:<22}{param:<9}{mR:>10.4f}{k:>12.4f}{flag}")

# ---- PART C: grade ------------------------------------------------------------------
# C1: analytic cross-checks of the no-response coefficient and the fixed-form means
check(abs(KAPPA0 - math.sqrt(8.0 * math.pi / 3.0)) < 1e-9, "KAPPA0 analytic = sqrt(8 pi/3)")
check(abs(mB - 1.0) < 1e-3, "Boltzmann m_R = 1.000 (Gamma(2)/Gamma(1))", f"m_R={mB:.4f}")
check(abs(mW - 0.375) < 1e-3, "Wigner m_R = 0.375 (3/8 analytic)", f"m_R={mW:.4f}")
check(abs(mG1 - math.sqrt(2.0 / math.pi)) < 1e-3,
      "Gaussian m_R(sigma=1) = sqrt(2/pi)", f"m_R={mG1:.4f}")

# C2: the UNTUNED test -- does 1/2 appear at a NATURAL parameter?
# Natural params: Boltzmann/Wigner as-stated, Gaussian sigma=1 (unit default).
natural_k = [kB, kW, KAPPA0 * mG1]
untuned_hit = any(abs(k - KAP) < TOL for k in natural_k)
check(not untuned_hit,
      "NO untuned 1/2: no natural param (Boltz/Wigner/sigma=1) lands in [0.457,0.543]",
      "natural kappas = " + ", ".join(f"{k:.4f}" for k in natural_k))

# C3: the Gaussian 1/2 IS reachable but ONLY at a TUNED sigma -> a dial, excluded.
# FDR diagnostic (pre-registered): report the sigma sweep honestly.
n_match = int(np.sum(np.abs(k_gauss - KAP) < TOL))
# count distinct crossing clusters (a monotone dial gives exactly one)
cross = np.diff(np.sign(k_gauss - KAP)) != 0
n_cross = int(np.sum(cross))
k_rng = k_gauss.max() - k_gauss.min()
p_chance = (2.0 * TOL) / k_rng if k_rng > 0 else 0.0
n_expected = len(sigma_grid) * p_chance
print(f"\nFDR (Gaussian sigma sweep, N={len(sigma_grid)} in [0.1,10], "
      f"hit=|kappa-0.5|<{TOL:.3f}):")
print(f"   grid points in window: {n_match};  independent crossing clusters: {n_cross};  "
      f"{n_expected:.2f} expected by chance over the {k_rng:.2f}-wide kappa range")
if n_cross > 0:
    hit_sigmas = sigma_grid[np.abs(k_gauss - KAP) < TOL]
    info(f"tuned sigma for kappa=1/2: {hit_sigmas[0]:.4f}..{hit_sigmas[-1]:.4f} "
         "(a single dial crossing -- NOT a natural parameter, excluded from untuned count)")
check(n_cross <= 1, "Gaussian kappa(sigma) is monotone: at most one 1/2 crossing (a dial)",
      f"crossings={n_cross}")

# C4: KILL fires only on an UNTUNED 1/2; none here -> verdict is NULL
check(not untuned_hit,
      "KILL condition (untuned 1/2) does NOT fire -> verdict NULL (scan complete, "
      "no untuned match; the only 1/2 is a tuned Gaussian-sigma dial)",
      "N_untuned_hits = 0")

finish("t004")
