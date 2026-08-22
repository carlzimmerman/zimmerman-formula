"""
CMC lapse-fixing equation with the MOND term, and its well-posedness.

Stress-energy of the MOND term  L = -(1/8 pi G) a0^2 U(X),  X = h^ij d_i Phi d_j Phi / a0^2:
  T_mn = (1/8 pi G)[ 2 U'(X) d_mu Phi d_nu Phi - g_mn a0^2 U(X) ].
Because Phi has NO normal derivative (no Phi-dot), with n^mu d_mu Phi = 0:
  E   = T_nn                = a0^2 U /(8 pi G)
  S_ij= T_ij               = (1/8 pi G)[2 U' d_i Phi d_j Phi - h_ij a0^2 U]
  S   = h^ij S_ij          = (a0^2/8 pi G)(2 X U' - 3 U)

CMC lapse-fixing: d_t K = C(t) spatially constant, K=q uniform, gives
  -D^2 N + N [ K_ij K^ij + 4 pi G (E+S) ] = -C(t).
Operator (-D^2 + V) with V = K_ij K^ij + 4 pi G (E+S) is uniquely invertible
(positive-definite) iff V >= 0 (and >0 somewhere).  Check the MOND piece of V.
"""
import sympy as sp

y = sp.symbols('y', positive=True)          # y == X
Uprime = sp.sqrt(y)/sp.sqrt(1+y)
U = sp.sqrt(y*(1+y)) - sp.asinh(sp.sqrt(y))

# 4 pi G (E+S)_MOND  with E=(a0^2/8piG)U, S=(a0^2/8piG)(2 y U' - 3 U):
# E+S = (a0^2/8piG)(2 y U' - 2 U) = (a0^2/4piG)(yU' - U)
# => 4 pi G (E+S) = a0^2 (y U' - U)
V_over_a0sq = sp.simplify(y*Uprime - U)
print("V_MOND / a0^2 = yU'-U =", V_over_a0sq)
print("  value at y=0 :", sp.limit(V_over_a0sq, y, 0))
print("  derivative   :", sp.simplify(sp.diff(V_over_a0sq, y)),
      "  (= y U'' >= 0  => monotone increasing from 0 => V_MOND >= 0)")
print("  y->oo        :", sp.limit(V_over_a0sq, y, sp.oo))

# Independent check of E+S via explicit trace, treating a single gradient dir:
a0, g = sp.symbols('a0 g', positive=True)   # g = |DPhi|, so X = g^2/a0^2
X = g**2/a0**2
Efac = a0**2*U.subs(y, X)/(8*sp.pi)          # drop 1/G (cancels), keep 8 pi
Sfac = (2*Uprime.subs(y, X)*g**2 - 3*a0**2*U.subs(y, X))/(8*sp.pi)
EplusS = sp.simplify(Efac + Sfac)
want   = sp.simplify(a0**2*(X*Uprime.subs(y, X) - U.subs(y, X))/(4*sp.pi))
print("\nE+S check (should be 0):", sp.simplify(EplusS - want))
print("\nCONCLUSION: V_MOND >= 0 everywhere => the MOND term ADDS positive")
print("definiteness to the lapse operator -D^2 + V.  Lapse-fixing WELL-POSED.")
