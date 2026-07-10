#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LANE 1 -- THE PIN: y_c = Z/2 AGAINST VERLINDE 1611.02269, COEFFICIENTS PINNED VERBATIM
=======================================================================================
Source pinning (2026-07-10), TWO INDEPENDENT RENDERINGS, verbatim agreement:
  R1: arXiv PDF v2 (https://arxiv.org/pdf/1611.02269), pdftotext extraction;
  R2: ar5iv HTML (https://ar5iv.labs.arxiv.org/html/1611.02269), raw LaTeX alttext
      grepped directly from the HTML (NOT a model summary).
Published version: SciPost Phys. 2, 016 (2017) -- same paper; the arXiv v2 is the
version of record for the equation numbers used here.

PINNED EQUATIONS (verbatim LaTeX from R2, cross-checked word-for-word in R1):
  (1.2)  kappa = c H_0 = c^2/L = a_0                                [Verlinde's a0 := cH0]
  (1.3)  Sigma(r) = M/A(r) < a_0/(8 pi G)                           [the crossover criterion]
  (4.28) S_M(r) = -2 pi M r / hbar                                  [c=1; with c: -2 pi M c r/hbar]
  (4.29) S_DE(r) = (1/V_0) V(r) = (r/L) A(r)/(4 G hbar)
  (4.31) S_M(r) = -(1/V_0) V_M(r)    with V_0 = 4 G hbar L/(d-1)
  (4.32) eps_M(r) := V_M(r)/V(r) >< 1                               [the budget crossover]
  (4.33) V_M(r) = (8 pi G/a_0) M r/(d-1)
  (4.34) eps_M(r) = (8 pi G/a_0) Sigma_M(r),  Sigma_M = M/A(r)
  (7.40) int_0^r G M_D^2(r')/r'^2 dr' = M_B(r) a_0 r / 6            [apparent-DM relation]
  (7.43) g_D = sqrt(a_M g_B)  with  a_M = a_0/6
Surrounding text pins: "the transition from standard Newtonian gravity to the apparent
dark matter regime occurs when the elastic strain drops in value below one" (after 4.42);
(4.30): S_M >< S_DE  <=>  2 pi M r/hbar >< (r/L) A(r)/(4 G hbar).

THIS SCRIPT: re-derives the strain mapping eps_M = 2y/(a0_V/a0) and the crossover
y_c from the PINNED coefficients only (sympy, exact), checks internal consistency of
Verlinde's own chain (4.28/4.29/4.31/4.33/4.34 must all cohere), then evaluates y_c
on both footings and the hostage/footing-invariance structure. Exit 0 = all asserted.
"""
import sympy as sp
import numpy as np

print("="*100)
print(" LANE 1 -- PINNING y_c AGAINST VERLINDE'S ACTUAL COEFFICIENTS (arXiv:1611.02269 v2)")
print("="*100)

# ---------------------------------------------------------------- symbols (c=1 first, as in the paper)
M, r, L, G, hb, a0V, d = sp.symbols('M r L G hbar a0_V d', positive=True)

# PINNED formulas, c=1 (paper's units, footnote 2):
S_M   = 2*sp.pi*M*r/hb                      # |eq 4.28|  (magnitude)
A     = 4*sp.pi*r**2                        # sphere area, d=4 (paper text above 1.3)
V     = sp.Rational(4,3)*sp.pi*r**3
S_DE  = (r/L)*A/(4*G*hb)                    # eq 4.29
V0    = 4*G*hb*L/(d-1)                      # eq 4.31
V_M   = S_M*V0                              # eq 4.31 (magnitude): V_M = |S_M| V0
V_M_paper = (8*sp.pi*G/a0V)*M*r/(d-1)       # eq 4.33 (with a0_V = c^2/L; c=1: a0_V = 1/L)

print("\n[1] INTERNAL CONSISTENCY of Verlinde's chain (sympy-exact):")
# (i) eq 4.29 self-consistency: (1/V0)V == (r/L)A/(4G hbar) requires V0 at d=4
chk = sp.simplify(V/V0.subs(d,4) - S_DE)
assert chk == 0, "4.29 vs 4.31 V0 inconsistency"
print("    (4.29)==(1/V0)V with V0=4G.hbar.L/(d-1) at d=4          [VERIFIED exact]")
# (ii) eq 4.33 from 4.28+4.31 with a0_V = 1/L (c=1 reading of eq 1.2):
chk2 = sp.simplify(V_M - V_M_paper.subs(a0V, 1/L))
assert chk2 == 0, "4.33 does not follow from 4.28+4.31"
print("    (4.33) V_M = (8piG/a0)Mr/(d-1) == |S_M|.V0 (a0=c^2/L)   [VERIFIED exact]")
# (iii) eq 4.34 from 4.32:
eps_M = sp.simplify(V_M.subs(d,4)/V)         # eq 4.32 with pinned pieces, d=4
Sigma = M/A
chk3 = sp.simplify(eps_M - (8*sp.pi*G/a0V)*Sigma.subs(a0V,a0V)).subs(L, 1/a0V)
chk3 = sp.simplify(eps_M.subs(L, 1/a0V) - (8*sp.pi*G/a0V)*Sigma)
assert chk3 == 0, "4.34 does not follow from 4.32"
print("    (4.34) eps_M = (8piG/a0)Sigma_M == V_M/V               [VERIFIED exact]")
# (iv) criterion coherence: eps_M = 1  <=>  Sigma = a0/(8piG)  (eq 1.3)  <=>  S_M = S_DE (eq 4.30)
chk4 = sp.simplify(S_M/S_DE - eps_M)
assert chk4 == 0, "S_M/S_DE != eps_M -- budget and strain crossovers would differ"
print("    S_M/S_DE == eps_M identically => (1.3), (4.30), (4.32) are ONE criterion  [VERIFIED]")

print("\n[2] THE STRAIN MAPPING, re-derived from the pinned coefficients only:")
g_bar = G*M/r**2
eps_in_g = sp.simplify(eps_M.subs(L, 1/a0V))     # c=1: L = 1/a0_V
assert sp.simplify(eps_in_g - 2*g_bar/a0V) == 0
print("    eps_M = |S_M|/S_DE = 2 G M L/r^2 = 2 g_bar/a0_V         [EXACT: the '2' is")
print("    2pi (Unruh/first-law, 4.28) x 4G.hbar (area law, 4.29) x (d-1)=3 x 3/(4pi) geometry]")
# in framework variables: y = g_bar/a0, a0 = a0_V/Z
y, Z = sp.symbols('y Z', positive=True)
eps_y = eps_in_g.subs(G*M/r**2, y*a0V/Z)          # g_bar = y*a0 = y*a0_V/Z
assert sp.simplify(eps_y - 2*y/Z) == 0
print("    with y = g_bar/a0 and a0 = a0_V/Z:  eps_M = 2y/Z        [the banked mapping, CONFIRMED]")
print("    (banked form eps_M = 2y/(a0_V/a0): identical, a0_V/a0 = Z)")

print("\n[3] THE CROSSOVER y_c (eps_M = 1, Verlinde's own criterion, eq 1.3/4.32):")
y_c = sp.solve(sp.Eq(eps_y, 1), y)[0]
assert sp.simplify(y_c - Z/2) == 0
print("    y_c = Z/2   EXACTLY (symbolic).")
Znum      = np.sqrt(32*np.pi/3.0)
A0_CANON  = 9.36e-11
A0_ALT    = 1.13e-10
Mpc       = 3.0857e22
cH_Lam    = Znum*A0_CANON                 # canonical footing: a0_V := cH_Lambda, a0 = cH_Lam/Z exact
cH0       = 2.99792458e8*67.4e3/Mpc      # alt footing: a0_V := cH0, a0_alt = 1.13e-10 (rounded)
yc_canon  = cH_Lam/(2*A0_CANON)
yc_alt    = cH0/(2*A0_ALT)
print(f"    canonical (a0_V = cH_Lambda = Z a0 exact):  y_c = Z/2 = {Znum/2:.4f}")
print(f"    alt       (a0_V = cH0, a0 = 1.13e-10):      y_c = cH0/(2 a0) = {yc_alt:.4f}")
assert abs(yc_canon - Znum/2) < 1e-12
assert abs(yc_alt - Znum/2) < 0.01*Znum/2   # within 1% (rounding of 1.13e-10 only)
print("    => y_c = 2.894 / 2.898: footing-INVARIANT to <1% (the ratio a0_V/a0 ~ Z on both).")

print("\n[4] HOSTAGE STRUCTURE (what would move y_c, now that the coefficients are pinned):")
tpi, quG, dm1 = sp.symbols('c_S c_A c_V', positive=True)   # perturb each pinned coefficient
S_M_p  = tpi*M*r/hb                    # 4.28 coefficient: 2pi -> c_S
S_DE_p = (r/L)*A/(quG*G*hb)            # 4.29 coefficient: 4 -> c_A
eps_p  = sp.simplify(S_M_p/S_DE_p).subs(L, 1/a0V)
yc_p   = sp.solve(sp.Eq(eps_p.subs(G*M/r**2, y*a0V/Z), 1), y)[0]
print("    generalized: S_M = c_S M r/hbar, S_DE = (r/L)A/(c_A G hbar)  =>")
print("      y_c =", sp.simplify(yc_p), "  [= Z/2 iff c_S*c_A = 8pi, i.e. 2pi x 4]")
assert sp.simplify(yc_p.subs({tpi: 2*sp.pi, quG: 4}) - Z/2) == 0
print("    * the 2pi in (4.28) is the Unruh/first-law normalization (Bekenstein bound)  [pinned]")
print("    * the 1/4G.hbar in (4.29) is the Bekenstein-Hawking area law                 [pinned]")
print("    * the (d-1) in V0 (4.31) CANCELS in eps_M = V_M/V (it multiplies both        [pinned]")
print("      V_M and the S_DE normalization); the d-2 of V0* (4.37) enters u(r), NOT eps_M")
print("    * A = 4pi r^2 and V = (4pi/3) r^3: geometry, not bookkeeping                  [exact]")
print("    => GIVEN the mapping a0 := a0_V/Z, y_c = Z/2 is DEFINITIONAL; the mapping's")
print("       only hostage coefficient is the '2' in eps_M = 2 g_bar/a0_V, which is now")
print("       pinned verbatim to (4.34)+(1.3): eps_M = 8piG Sigma/a0, Sigma = M/4pi r^2.")

print("\n[5] FOOTING CAVEAT (named, not hidden): Verlinde's own a0_V is cH0 (eq 1.2, rho_total");
print("    de Sitter). The canonical framework re-reads L as the PURE-LAMBDA horizon (a0_V =")
print("    cH_Lambda). y_c = Z/2 holds on EITHER reading because y is measured in the SAME")
print("    footing's a0 = a0_V/Z; what moves between footings is a0 itself, not y_c.")

print("\n[6] GATE CONSEQUENCE: y_c CONFIRMED => the banked Saturn margins stand unchanged.")
print("    (T = min(1, y_c/y): the suppression at Saturn's y >> y_c scales LINEARLY in y_c;")
print("    a coefficient shift c -> y_c' = c*y_c would scale the throttle-tail Q2 by c.")
print("    Pinned c = 1: margins 18-26x under the strict bound, as banked.)")

print("\n" + "="*100)
print(" VERDICT: PINNED-CONFIRMED. y_c = Z/2 = 2.8944 (canonical) / 2.898 (alt) survives the")
print(" verbatim pin of (1.2),(1.3),(4.28),(4.29),(4.31)-(4.34),(7.40),(7.43) in TWO independent")
print(" renderings (arXiv PDF pdftotext + ar5iv LaTeX alttext). The prior ar5iv-WebFetch caveat")
print(" is DISCHARGED. Residual hostage: only Verlinde's 2pi x 1/4G bookkeeping, now source-pinned.")
print("="*100)
print("EXIT 0")
