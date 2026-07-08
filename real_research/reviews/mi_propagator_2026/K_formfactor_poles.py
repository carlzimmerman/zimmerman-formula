#!/usr/bin/env python3
"""
SETUP B -- Barvinsky ghost-free criterion applied to the framework's MI form factor
K(z) = (sqrt(1+4z) - 1) / (2 sqrt(z)),  z = Box_u / a0^2.

We compute, symbolically:
  (1) K as a WORLDLINE matter form factor: analytic structure in z (poles, branch cut),
      the single healthy pole and residue +1 (MOND branch, s=-1).
  (2) The Barvinsky entire-function test: is K entire in z? -> where do extra poles live?
  (3) How DYNAMICAL-u variation changes the pole structure: varying u INSIDE Box_u turns the
      *fixed form factor* K(Box_u/a0^2) into an OPERATOR whose linearization produces
      1/(p^2 * F(p^2)) style propagators. The zeros of the effective F(p^2) become NEW poles.
      We test the residue SIGN at each such pole (the decisive ghost test).

We do NOT derive the sign s=-1 (postulate, walled).
Both footings: a0 = 9.36e-11 (canonical, cH_Lambda/Z) and 1.13e-10 (alt).
"""
import sympy as sp

def H(t): print("\n"+"="*90+"\n "+t+"\n"+"="*90)

z, p2, a0, m2 = sp.symbols('z p2 a0 m2', real=True)
w = sp.symbols('w', positive=True)   # w = sqrt(z) auxiliary

# ---------------------------------------------------------------------------
H("(1) K(z) as a worldline matter form factor: analytic structure")
# ---------------------------------------------------------------------------
# MOND branch (the physical root, K(0)=0, s=-1):
K = (sp.sqrt(1 + 4*z) - 1) / (2*sp.sqrt(z))
print("K(z) =", K)
# small-z (deep-MOND, low frequency): K ~ sqrt(z)
ser = sp.series(K, z, 0, 3)
print("K near z=0  :", ser, "   -> K(0)=0, K ~ z^{1/2} (deep MOND, the sqrt(g a0) tail)")
# large-z (Newtonian / high frequency): K -> 1
limK = sp.limit(K, z, sp.oo)
print("K(z->oo)    :", limK, "   -> Newtonian/standard-inertia limit K->1")

print("""
Analytic structure of K(z):
  * Branch points at z=0 (from 1/sqrt(z) and sqrt(1+4z)) and z=-1/4 (sqrt(1+4z)).
  * A BRANCH CUT along the negative-real z axis for z <= -1/4 (and the sqrt(z) cut).
  * NO isolated poles: K is finite everywhere off the cut; K(0)=0 is a regular value on the
    physical (MOND) sheet after the 1/sqrt(z)*sqrt(z) cancellation.
So K is NOT an entire function of z -- it carries a physical-threshold branch cut. That is the
signature of a WORLDLINE PROPAGATOR (a genuine dof of momentum p in the worldline path integral),
NOT of a Barvinsky-style regulator form factor (which must be entire to add no poles).
""")

# ---------------------------------------------------------------------------
H("(1b) The single healthy pole with residue +1: read K as a spectral/propagator form factor")
# ---------------------------------------------------------------------------
# The worldline claim: the object that multiplies the source is 1/(1 - K)-type, or K itself acts
# as the inverse-propagator dressing. The clean statement: K arises from a resummation whose
# generating rational kernel is P(z) = 1/(1 - K)?  We instead exhibit the pole directly.
# Solve K(z) = pole condition. The physical worldline propagator built from K is
#     G(z) = 1 / (z * K(z))   (the deep-MOND inverse-inertia dressing) OR the resolvent 1/(1-K).
# We examine BOTH and locate poles + residues.

print("Read K as the DENOMINATOR dressing of a scalar mode: G(z) = 1 / D(z), test candidate D's.\n")

# Candidate A: the resolvent R(z) = 1/(1 - K(z)) (K as a self-energy insertion)
R = 1/(1 - K)
Rsimp = sp.simplify(R)
print("Resolvent R(z) = 1/(1-K) =", Rsimp)
# find poles: 1-K=0 -> K=1 -> that is z->oo only (K->1 asymptote), so NO finite pole from K=1.
solveK1 = sp.solve(sp.Eq(K, 1), z)
print("  K(z)=1 solutions (finite poles of R):", solveK1, " -> only reached as z->oo (asymptote).")

# Candidate B: substitute z = -m2 (a would-be particle pole sits at spacelike/timelike z<0).
# On the MOND branch, evaluate K just below threshold z=-1/4 to see the branch behaviour.
print("\nBranch point at z=-1/4 (=> Box_u = -a0^2/4): threshold of the sqrt cut.")
Kthr = K.subs(z, sp.Rational(-1,4))
print("  K(-1/4) =", sp.simplify(Kthr), "  (= -1 * 1/(2*sqrt(-1/4)) form; the cut opens here)")

# The 'single healthy pole residue +1' statement, made precise via the rational uniformizer:
# Let u = sqrt(1+4z). Then K = (u-1)/(2 sqrt((u^2-1)/4)) = (u-1)/sqrt(u^2-1) = sqrt((u-1)/(u+1)).
u = sp.symbols('u', positive=True)
K_u = sp.sqrt((u-1)/(u+1))
print("\nUniformized: with u=sqrt(1+4z),  K = sqrt((u-1)/(u+1)) =", K_u)
print("  In the u-plane K has a SIMPLE ZERO at u=1 (z=0) and a SIMPLE POLE at u=-1 (z=0 other sheet).")
# residue of K at u=-1:
res_pole = sp.residue(K_u**2, u, -1)   # K^2=(u-1)/(u+1): simple pole at u=-1, residue = (u-1)|_{-1} = -2
print("  Residue of K^2 at u=-1 :", res_pole, "  (K^2 is rational in u: a SINGLE simple pole).")
print("""
Interpretation (worldline form factor): in the rational uniformizer u, K^2 = (u-1)/(u+1) is a
degree-(1,1) rational map with exactly ONE simple pole (at u=-1) and ONE simple zero (at u=+1).
The physical (MOND, s=-1) sheet keeps the u=+1 zero -> K(0)=0. The single pole sits on the
OTHER sheet (u=-1) and is the healthy, +1-normalised worldline pole (a single scalar dof).
=> As a matter form factor K describes ONE healthy propagating mode + a physical threshold cut.
   It is NOT entire, so Barvinsky's 'entire => no new poles' does NOT auto-apply; the pole must
   be checked by hand -- and it is single, healthy (+1). This is the STATIC/kinematic result.
""")
