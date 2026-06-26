#!/usr/bin/env python3
"""
agentT4 part 4 — reproduce the 2308.08738 'lambda ~ (1/4)*4^3 = 16' and 'Lambda_w ~ 42 a*^2'
statements, and prove the route's lambda CANNOT be 64*pi (the only value matching Carl's Z).

2308.08738 sec 3.3 (verbatim-ish):
  "A reordering in the spin connection term will produce a constant of the order (1/4)*4^3
   added to the dimensionless lambda = Lambda/(8piGhbar kappa)^2 ..."
  "Lambda_w ~ 42 (8piGhbar kappa)^2"  and  "a0 = (1/4) sqrt(Lambda_w)" (eq 35).

(1/4)*4^3 = 16.  But then the numeric estimate uses 42, not 16. And eq 35 uses 1/4, eq 32
of 2311 uses sqrt(2*.../lambda). These are mutually inconsistent prefactors.
"""
import sympy as sp

print("=== 2308.08738 self-consistency of '16' vs '42' vs eq35 prefactor 1/4 ===")
val_16 = sp.Rational(1,4)*4**3
print("  (1/4)*4^3 =", val_16, "  <- the stated 'order' of the reordering constant")
print("  but the numeric Lambda_w uses 42, i.e. lambda~42 (factor", sp.N(42/val_16,3), "larger than 16)")

# eq 35 says a0 = (1/4) sqrt(Lambda_w).  Compare to eq 32 of 2311: a0 = sqrt(2 Lambda/lambda).
# If both describe the same a0 and Lambda, then 1/4 = sqrt(2/lambda) => lambda = 32.
lam_from_eq35 = sp.solve(sp.Eq(sp.Rational(1,4), sp.sqrt(2/sp.symbols('l',positive=True))), sp.symbols('l',positive=True))
print("  Forcing eq35 (a0=1/4 sqrt L) == eq32 (a0=sqrt(2L/lambda)) => lambda =", lam_from_eq35,
      " (yet another value: 32, vs 3, vs 16, vs 42)")

print("\n=== Z_eff for each of the paper's own quoted lambda/prefactor variants ===")
Z_carl = sp.sqrt(sp.Rational(32)*sp.pi/3)
# Generic: a0 = A * sqrt(Lambda); Z_eff = sqrt(1/3)/A
def Zeff(A): return sp.N(sp.sqrt(sp.Rational(1,3))/A, 6)
print("  Z_carl =", sp.N(Z_carl,6))
print("  2311 eq32 lambda=3 :  A=sqrt(2/3),  Z_eff =", Zeff(sp.sqrt(sp.Rational(2,3))))
print("  2308 eq35 (1/4)    :  A=1/4,        Z_eff =", Zeff(sp.Rational(1,4)))
print("  2308 lambda=42 eq32:  A=sqrt(2/42), Z_eff =", Zeff(sp.sqrt(sp.Rational(2,42))))
print("  2308 lambda=16 eq32:  A=sqrt(2/16), Z_eff =", Zeff(sp.sqrt(sp.Rational(2,16))))

print("\n=== Can a finite Clifford commutator EVER yield lambda = 64*pi (Carl's match)? ===")
print("  Required lambda for Z_eff = Z_carl (via eq32, Z_eff=sqrt(lambda/6)):")
print("     lambda = 6 * Z_carl^2 = 6 * 32pi/3 = 64 pi =", sp.N(64*sp.pi,8))
print("  Every Clifford/Weyl-ordering contraction of gamma^{IJ}gamma^{KL} with a")
print("  Kronecker/metric pair-delta is a TRACE of products of gamma-matrices =>")
print("  an INTEGER (times the rep dim 4, divided by 4) => RATIONAL. It has no pi.")
print("  The mu-sum (=4), the range counts (6 or 16), the prefactor (1/4,1/8,1/16,1/32)")
print("  are all rational. PRODUCT of rationals is rational. 64*pi is transcendental.")
print("  => NO operator-ordering/Weyl chain in this finite-dim Clifford algebra can")
print("     produce lambda=64pi. The route's Z_eff is ALGEBRAIC-rational-rooted, Carl's")
print("     Z=sqrt(32pi/3) is transcendental. STRUCTURAL non-match, independent of which")
print("     of {3,16,32,42} is 'right'.")

print("\n=== Numerical a0 sanity at hadronic kappa (does the route even land near 9.36e-11?) ===")
# Paper: kappa^{1/3} ~ below 100 MeV..1 GeV gives a0 in the right ballpark only with
# 'error of several orders of magnitude' (their own words). The VALUE of Lambda is NOT
# predicted; kappa is tuned to hit it. Confirm the structural point, not a precision claim.
print("  Paper's own statement: a0, Lambda reproduced only 'with the current error of")
print("  several orders of magnitude' and only IF kappa is tuned to a sub-100-MeV scale.")
print("  => Lambda's VALUE is an INPUT (via kappa), not an output. a* = 8piGhbar*kappa")
print("     fixes a*; lambda fixes Lambda/a*^2; but kappa itself is free (set by demanding")
print("     a* ~ a0). Self-consistency does NOT close it: see part-5 note.")
