#!/usr/bin/env python3
"""ADVERSARIAL RE-DERIVATION of y_c from the SciPost PUBLISHED version ONLY
(SciPost Phys. 2, 016 (2017), fetched independently 2026-07-10; equation
numbers are the SciPost continuous numbering, NOT the arXiv section numbering).

Pinned verbatim from verlinde_scipost.txt (pdftotext of the SciPost PDF):
  (2)   kappa = cH_0 = c^2/L = a_0                    [line 164]
  (3)   Sigma(r) = M/A(r) < a_0/(8 pi G)              [line 249]
  (28)  S_M(r) = -2 pi M r/hbar                       [line 883-885]
  (29)  S_DE(r) = (1/V_0)V(r) = (r/L) A(r)/(4 G hbar) [line ~900]
  (31)  V_0 = 4 G hbar L/(d-1)
  (32)  eps_M(r) = V_M(r)/V(r) >< 1
  (33)  V_M(r) = (8 pi G/a_0) M r/(d-1)
  (34)  eps_M(r) = (8 pi G/a_0) Sigma_M(r)
  (41)+(42)+text: "the expression (41) for eps(r) becomes identical to the
        quantity eps_M(r) introduced in (32)" and "the transition from standard
        Newtonian gravity to the apparent dark matter regime occurs when the
        elastic strain drops in value below one"  [lines 1055-1084]
        -- the (d-2)/(d-1) of V_0* (37) is absorbed BY VERLINDE HIMSELF (41).
  (7)/(102) g_D = sqrt(a_M g_B), a_M = a_0/6          [lines 310-315, 1857]
"""
import sympy as sp

M, r, L, G, hb, c = sp.symbols('M r L G hbar c', positive=True)

# --- chain from the published equations, c reinstated by dimensional analysis
# (28): S_M magnitude, with c: 2 pi M c r / hbar   (paper: "reinstated factors of c", line ~930)
S_M  = 2*sp.pi*M*c*r/hb
# (29): S_DE = (r/L) A/(4 G hbar) -- with c: entropy A c^3/(4 G hbar); A = 4 pi r^2 (d=4)
A    = 4*sp.pi*r**2
S_DE = (r/L)*A*c**3/(4*G*hb)

eps_M = sp.simplify(S_M/S_DE)                      # = |S_M|/S_DE
assert sp.simplify(eps_M - 2*G*M*L/(c**2*r**2)) == 0, "eps_M != 2GML/(c^2 r^2)"

# cross-check against (34)+(3): eps_M = (8 pi G/a0) Sigma, Sigma = M/(4 pi r^2), a0 = c^2/L
a0V = c**2/L                                        # eq (2)
eps_34 = (8*sp.pi*G/a0V)*(M/A)
assert sp.simplify(eps_M - eps_34) == 0, "(28)/(29) route disagrees with (34) route"

# in g_bar: eps_M = 2 g_bar / a0_V
g = sp.Symbol('g_bar', positive=True)
eps_g = eps_M.subs(G*M/r**2, g)
assert sp.simplify(eps_g - 2*g/a0V) == 0

# crossover eps_M = 1 (Verlinde's own criterion (3)==(30)==(32), one statement):
#   g_bar,c = a0_V/2.   Framework mapping a0 = a0_V/Z  =>  y_c = g_bar,c/a0 = Z/2.
y, Z = sp.symbols('y Z', positive=True)
yc = sp.solve(sp.Eq(eps_g.subs(g, y*a0V/Z), 1), y)[0]
assert sp.simplify(yc - Z/2) == 0, "y_c != Z/2"

# the ONLY hostage: had the strain been eps* (V_M* route, d-2 NOT absorbed),
# the coefficient would be 2*(d-1)/(d-2) = 3 at d=4  =>  y_c = Z/3 = 1.93.
# Verlinde absorbs it explicitly in (41); the crossover quantity is eps_M. Named, closed.
eps_star = eps_M * sp.Rational(3,2)   # (d-1)/(d-2) at d=4
yc_star = sp.solve(sp.Eq(eps_star.subs(G*M/r**2, y*a0V/Z), 1), y)[0]
assert sp.simplify(yc_star - Z/3) == 0

import numpy as np
Zn = np.sqrt(32*np.pi/3)
print(f"eps_M = 2 g_bar/a0_V  [published (28)/(29) == (34)/(3), one criterion]")
print(f"y_c = Z/2 = {Zn/2:.4f} (canonical, a0 := cH_Lam/Z exact)")
print(f"alt footing: cH0(67.4)/(2 x 1.13e-10) = {2.99792458e8*67.4e3/3.0857e22/(2*1.13e-10):.4f}")
print(f"killed alternative (strain=eps*, d-2 unabsorbed): y_c = Z/3 = {Zn/3:.4f} -- excluded by (41) verbatim")
print("ALL ASSERTS PASS -- EXIT 0")
