#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""t009 -- The pi-free theorem, formalized (a parity argument in sympy).

Hypothesis (TASKS.md, verbatim):
  "kappa is pi-free (committed) AND any derivation producing kappa as a ratio of
   horizon areas/entropies must carry pi -- so the derivation class
   'pure horizon-geometry ratios' is EXCLUDED."
Method (verbatim): "formalize as a parity argument in sympy over the generator set
  {A_horizon, S, T, hbar, c, G, Lambda}."
PASS: "the obstruction proof script or its refutation."
This is a STRUCTURAL theorem (a parity/degree argument), NOT a numeric coincidence
hunt: there is no target number to coincide with -- kappa is the quantity being
EXCLUDED -- so no mm_search / FDR window is defined. The only "search" is the
falsification search for a NON-TRIVIAL pi-free universal horizon constant, which
is the KILL condition; its lattice is pre-registered in REGISTRY_FDR.md (T009 row).

CONJUNCT (1)  kappa is pi-free.  COMMITTED, not derived: kappa is a fitted
  dimensionless number (KAPPA_MEAS=0.551+/-0.043; 1/2 ADOPTED), no pi appears in
  its determination.  We do NOT claim kappa=1/2 is derived.
CONJUNCT (2)  every pure horizon-geometry ratio that is pi-free is either the
  trivial constant 1 or carries a FREE geometric/curvature parameter (a horizon
  scale R, or the Lambda scale), hence is NOT a universal constant and cannot
  derive kappa.  => the derivation class "pure horizon-geometry ratios" is EXCLUDED.

THE PARITY ARGUMENT (the crux, done in sympy with a FORMAL pi symbol Pi_s so the
exponent of pi is tracked EXACTLY and never simplified away):
  Generators (standard horizon-geometry relations):
      A = 4*Pi_s*R^2            horizon area         -> pi^+1, dim [L^2]
      Lp2 = hbar*G/c^3          Planck area         -> pi^0 , dim [L^2]
      S = A/(4*Lp2)             Bekenstein-Hawking  -> pi^+1, dim [-] (dimensionless)
      E = hbar*c/(2*Pi_s*R)     Unruh/dS thermal energy (T*k_B, pi^-1)
                                -> pi^-1, dim [M L^2 T^-2]
  A "pure horizon-geometry ratio" is a monomial M = A^a S^b E^d (a,b,d integers).
  - dimensionless  <=>  dim(M) = a*dim(A)+b*dim(S)+d*dim(E) = 0
                       = (2a+2d, d, -2d) = 0  <=>  d = 0 and a = 0  =>  M = S^b
  - pi-free        <=>  pi_parity(M) = a + b - d = 0.  With a=d=0 => b = 0 => M = 1.
  THEOREM: the ONLY dimensionless, pi-free, parameter-free monomial in
      {A,S,E} is the trivial M = 1.  A ratio of LIKE geometries (e.g. S(R1)/S(R2)
      = (R1/R2)^2) is pi-free (pi cancels) but carries the FREE parameter R1/R2,
      so it is not universal.  Hence no non-trivial pi-free universal horizon
      constant exists, and kappa (a non-trivial pi-free universal constant) cannot
      be a pure horizon-geometry ratio.  EXCLUSION CONFIRMED.

KILL / REFUTED: if the pre-registered lattice contains a monomial that is
  dimensionless AND pi-free AND parameter-free AND non-trivial (!= 1), that WOULD
  be a genuine pi-free universal horizon constant able to be tuned to kappa -> the
  exclusion FAILS and the hypothesis is REFUTED.

Direction-of-risk: WIN-risk -- a non-trivial pi-free universal horizon constant
  would dress kappa (a FITTED constant, NOT derived) in a geometric derivation the
  framework actually lacks; the honest DEFICIT-side result is that only the trivial
  1 survives, confirming kappa is NOT horizon-derivable.  We are therefore
  suspicious of ANY non-trivial survivor.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from qwenlib import *     # constants, kernel, check/info/finish, FOOTINGS, KAPPA_MEAS
import numpy as np
import sympy as sp

# ------------------------------------------------------------------------------
# PART A -- formal generators (sympy, with a FORMAL pi so pi-parity is exact)
# ------------------------------------------------------------------------------
Pi_s   = sp.Symbol('Pi_s', positive=True)     # FORMAL pi (NOT sp.pi): exponent is exact
R      = sp.Symbol('R',      positive=True)   # a horizon radius (the free scale)
R_LAMB = sp.Symbol('R_Lambda', positive=True) # the Lambda scale c*sqrt(3/Lambda) (2nd scale)
hbar   = sp.Symbol('hbar',   positive=True)   # universal, pi-free
c      = sp.Symbol('c',      positive=True)   # universal, pi-free
G      = sp.Symbol('G',      positive=True)   # universal, pi-free
kB     = sp.Symbol('kB',     positive=True)   # universal, pi-free

Lp2 = hbar * G / c**3            # Planck area, pi^0
A   = 4 * Pi_s * R**2           # horizon area,  pi^+1, dim [L^2]
S   = A / (4 * Lp2)            # BH entropy,    pi^+1, dim [-]
E   = hbar * c / (2 * Pi_s * R)  # Unruh/dS thermal energy (T*k_B), pi^-1, dim [M L^2 T^-2]

# dimension vectors [m, kg, s] (temperature folded as E=T*k_B so a dimensionless
# number can be formed; a bare T has dimension [K] and cannot form one alone)
DIM = {A: (2, 0, 0), S: (0, 0, 0), E: (2, 1, -2)}

def dim_of(a, b, d):
    m = a*DIM[A][0] + b*DIM[S][0] + d*DIM[E][0]
    k = a*DIM[A][1] + b*DIM[S][1] + d*DIM[E][1]
    s = a*DIM[A][2] + b*DIM[S][2] + d*DIM[E][2]
    return (m, k, s)

def is_dimensionless(a, b, d):
    return dim_of(a, b, d) == (0, 0, 0)

def pexp(expr, sym):
    """exponent of `sym` in a rational (monomial) expression, via sympy."""
    e = sp.cancel(expr)
    num, den = sp.fraction(e)
    return sp.degree(num, sym) - sp.degree(den, sym)

def pi_parity(a, b, d):
    """pi-exponent of the monomial A^a S^b E^d, computed in sympy (exact)."""
    M = (A**a) * (S**b) * (E**d)
    return pexp(M, Pi_s)

def is_pi_free(a, b, d):
    return pi_parity(a, b, d) == 0

def free_params(a, b, d):
    """geometric/curvature scales that survive after dropping pi -> 'free params'."""
    M = (A**a) * (S**b) * (E**d)
    e = sp.cancel(M.subs({Pi_s: 1}))     # drop pi, keep R and R_Lambda dependence
    return [s for s in (R, R_LAMB) if e.has(s)]

# ------------------------------------------------------------------------------
# PART B -- positive controls: the parity tracker must DISTINGUISH pi from not-pi
# ------------------------------------------------------------------------------
# (b1) pi-CARRYING horizon ratios (the textbook ones) must have pi-parity != 0:
check(pi_parity(0, 1, 0) == 1,
      "S (Bekenstein-Hawking entropy) carries pi: pi-parity +1",
      f"pi_parity(S) = {pi_parity(0,1,0)}")
check(pi_parity(1, 0, 0) == 1,
      "A/Lp2 = 4*pi (area / Planck-area) carries pi: pi-parity +1",
      f"pi_parity(A) = {pi_parity(1,0,0)}")
check(pi_parity(0, 0, 1) == -1,
      "E (Unruh/dS thermal energy) carries 1/pi: pi-parity -1",
      f"pi_parity(E) = {pi_parity(0,0,1)}")
# (b2) the KEY nuance: a ratio of LIKE geometries is pi-free BUT parameterized.
#     S(R1)/S(R2) = (R1/R2)^2: pi cancels (parity 0) yet carries the free ratio R1/R2.
S_ratio = S / S.subs(R, R_LAMB)     # entropy of a horizon of radius R vs one of radius R_Lambda
par_Sratio = pexp(sp.cancel(S_ratio), Pi_s)
fp_Sratio = free_params(0, 0, 0) if False else [s for s in (R, R_LAMB) if sp.cancel(S_ratio.subs({Pi_s:1})).has(s)]
check(par_Sratio == 0,
      "pi cancels in a ratio of LIKE horizons S(R)/S(R_Lambda): pi-parity 0",
      f"pi_parity = {par_Sratio}")
check(len(fp_Sratio) >= 1,
      "but S(R)/S(R_Lambda) carries a FREE geometric parameter (R/R_Lambda) -> NOT universal",
      f"free params = {fp_Sratio}")
# (b3) the only parameter-free pi-free dimensionless survivor is the trivial 1:
check(is_dimensionless(0, 0, 0) and is_pi_free(0, 0, 0) and free_params(0, 0, 0) == [],
      "the trivial monomial 1 (a=b=d=0) is the lone pi-free, dimensionless, parameter-free survivor",
      "value = 1, no free params")
# and the trivial 1 is NOT kappa (neither the adopted 1/2 nor the fitted 0.551):
KAPPA_ADOPTED = 0.5
check(abs(1.0 - KAPPA_ADOPTED) > 1e-12 and abs(1.0 - KAPPA_MEAS) > 1e-12,
      "the trivial survivor 1 != kappa_adopted(0.5) and != kappa_measured(0.551)",
      f"1 vs {KAPPA_ADOPTED} vs {KAPPA_MEAS}")

# ------------------------------------------------------------------------------
# PART C -- the pre-registered lattice: the falsification (KILL) search.
#           Enumerate the monomial class M = A^a S^b E^d over a bounded exponent
#           lattice; collect every (dimensionless AND pi-free) survivor and prove
#           each is either trivial (=1, parameter-free) or carries a free param.
#           Lattice pre-registered in REGISTRY_FDR.md (T009 row, 2026-08-17).
# ------------------------------------------------------------------------------
EXP_RANGE = list(range(-2, 3))           # a, b, d in {-2,-1,0,1,2}  (pre-registered)
lattice_n = len(EXP_RANGE) ** 3
survivors = []        # (a,b,d, dimless, pifree, free_params, value_if_universal)
N_dimless_pifree = 0
N_paramfree_nontrivial = 0              # KILL counter: a non-trivial universal pi-free constant
for a in EXP_RANGE:
    for b in EXP_RANGE:
        for d in EXP_RANGE:
            if (a, b, d) == (0, 0, 0):
                continue               # skip the trivial 1 (already handled in PART B)
            dl = is_dimensionless(a, b, d)
            pf = is_pi_free(a, b, d)
            if dl and pf:
                N_dimless_pifree += 1
                fps = free_params(a, b, d)
                survivors.append((a, b, d, fps))
                if fps == [] and not (a == 0 and b == 0 and d == 0):
                    N_paramfree_nontrivial += 1
                    # a parameter-free non-trivial pi-free constant: evaluate it
                    M = (A**a) * (S**b) * (E**d)
                    try:
                        val = complex(M.subs({Pi_s: 1.0, R: 1.0, R_LAMB: 1.0,
                                             hbar: 1.0, c: 1.0, G: 1.0, kB: 1.0}))
                    except Exception:
                        val = None
                    info(f"KILL-candidate monomial a={a} b={b} d={d} "
                         f"pi-free dimless parameter-free -> value={val}",
                         "would be a non-trivial universal pi-free constant"
                         if val is not None else "unevaluable")

info(f"lattice |EXP_RANGE|^3 = {lattice_n} monomials (a,b,d in {-2}..{2})",
     f"dimensionless AND pi-free survivors (excluding the trivial 1): {N_dimless_pifree}")
if N_dimless_pifree:
    shown = ", ".join(f"({a},{b},{d}) free={fps if fps else 'TRIVIAL'}"
                      for (a, b, d, fps) in survivors[:12])
    info("the dimensionless+pi-free survivors are:", shown
         + (" ..." if N_dimless_pifree > 12 else ""))

# every pi-free dimensionless survivor must be parameterized (or the trivial 1):
all_parameterized = all((len(fps) >= 1) for (_, _, _, fps) in survivors)
check(all_parameterized,
      "THEOREM: every non-trivial dimensionless pi-free horizon-geometry monomial "
      "carries a free geometric/curvature parameter (R or Lambda scale) -> not universal",
      f"all {N_dimless_pifree} survivors parameterized"
      if all_parameterized else f"VIOLATION: {N_paramfree_nontrivial} parameter-free survivor(s)")

# ------------------------------------------------------------------------------
# PART D -- grade: PASS = the obstruction proof (or its refutation).
# ------------------------------------------------------------------------------
check(N_paramfree_nontrivial == 0,
      f"PASS/KILL: {N_paramfree_nontrivial} parameter-free non-trivial pi-free universal "
      f"horizon constant(s) found (KILL iff >0)",
      "EXCLUSION CONFIRMED: the only pi-free dimensionless universal horizon "
      "constant is the trivial 1, which != kappa" if N_paramfree_nontrivial == 0
      else "REFUTED: a non-trivial pi-free universal horizon constant exists -> class NOT excluded")

# ------------------------------------------------------------------------------
# PART E -- both footings: this is a STRUCTURAL argument, footing-independent.
# ------------------------------------------------------------------------------
for fname, a0 in FOOTINGS.items():
    info(f"footing {fname}: a0 = {a0:.4e} m/s^2 -> N/A",
         "pi-parity is a structural property of the generator algebra; no "
         "dimensional scale (rho_Lambda, a0) enters, so both footings are irrelevant")

finish("t009")
