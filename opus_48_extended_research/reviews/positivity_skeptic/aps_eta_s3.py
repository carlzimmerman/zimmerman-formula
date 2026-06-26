"""
COMPUTE-A: APS eta-invariant of the Dirac operator on the de Sitter horizon S^3.

Framework: a0 = c^2 sqrt(Lambda/32pi) = (c/2) sqrt(G rho_DE) = cH_Lambda / Z,
           Z = sqrt(32pi/3) = 2 sqrt(8pi/3).
The sqrt(8pi/3) inside the root is FORCED. The LONE free number is kappa = 1/2
(the '2' in a0 = (c/2)...), i.e. the OUTSIDE coefficient.

Question: does an APS eta-invariant / index / fixed-point boundary term on the
dS-horizon Dirac operator OUTPUT 1/2 from the geometry/spectrum, NON-circularly
(kappa kept symbolic, never input by hand)?

ANTI-CIRCULARITY GATE: kappa stays symbolic. The topological invariant must
produce 1/2 from the S^3 / S^4 / SO(4,1) structure ALONE.
"""
import sympy as sp
from sympy import Rational, sqrt, pi, oo, nsimplify, zeta, Symbol, gamma, S

# -----------------------------------------------------------------------------
# (0) The framework numbers, kappa kept SYMBOLIC
# -----------------------------------------------------------------------------
kappa = sp.Symbol('kappa', positive=True)         # the lone free number, SYMBOLIC
# a0 = kappa * c * sqrt(G rho_DE);  Z = 2 sqrt(6) sqrt(pi) / (3 kappa)
# at kappa=1/2: Z = sqrt(32pi/3). We NEVER set kappa=1/2 by hand.
Z_sym = 2*sqrt(6)*sqrt(pi)/(3*kappa)
print("Z(kappa) =", Z_sym, "   -> at kappa=1/2:", Z_sym.subs(kappa, Rational(1,2)),
      "=", sp.nsimplify(Z_sym.subs(kappa, Rational(1,2))**2))
print("Target a0/cH ratio = 1/Z(kappa) =", sp.simplify(1/Z_sym))
print()

# =============================================================================
# (1) DIRAC OPERATOR ON THE ROUND S^3 (radius = dS horizon radius R)
# =============================================================================
# Standard result (Hitchin; Camporesi-Higuchi gr-qc/9505009; Trautman):
# On S^3 (radius R) with the round metric and the STANDARD (trivial, i.e. the
# unique) spin structure, the Dirac operator eigenvalues are
#     lambda_n = +/- (n + 3/2) / R ,   n = 0,1,2,...
# with multiplicity (n+1)(n+2) for EACH sign.
# (Equivalently lambda = +/-(k+3/2), k>=0.)
#
# Spectrum is SYMMETRIC under lambda -> -lambda with equal multiplicities, so
# the spectral asymmetry (eta) is naively ZERO.  We verify, then probe whether a
# non-trivial structure / flux breaks it.
print("="*70)
print("(1) ROUND S^3 DIRAC SPECTRUM (standard spin structure)")
print("="*70)
n = sp.symbols('n', integer=True, nonnegative=True)
eig_plus  = (n + Rational(3,2))     # in units of 1/R
mult      = (n + 1)*(n + 2)
print("eigenvalues:  +/-(n+3/2),  n>=0 ;  multiplicity (n+1)(n+2) each sign")
for k in range(4):
    print(f"   n={k}: |lambda|={eig_plus.subs(n,k)},  mult={mult.subs(n,k)}")
print("Spectrum is symmetric (+ and - identical multiplicities).")

# eta-function:  eta(s) = sum_lambda sign(lambda) |lambda|^{-s}
# For a symmetric spectrum every + term cancels its - partner termwise => eta(s)=0
# identically, hence eta(0)=0 and the spectral asymmetry vanishes.
print("\n  -> Spectral asymmetry: + and - cancel termwise => eta(s) == 0,  eta(0)=0.")
print("     ker(D) on round S^3 is empty (no harmonic spinors, lambda_min=3/2>0)")
print("     => h = dim ker = 0,  reduced eta-bar = (eta(0)+h)/2 = 0.")
print("\n  HONEST: the BARE round S^3 gives eta=0, eta-bar=0.  NO 1/2 here.")
print("  This is the circularity trap: a hand-inserted flux to force 1/2 = circular.")
print("  The dS horizon, however, is NOT a bare S^3 -- it carries the SO(4,1)")
print("  connection. We must check whether the FRAMEWORK's OWN structure breaks")
print("  the +/- symmetry. Done in step (3) below.")
