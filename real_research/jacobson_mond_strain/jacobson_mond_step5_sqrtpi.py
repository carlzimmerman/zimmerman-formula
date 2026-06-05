#!/usr/bin/env python3
"""
STEP 5 -- Bookkeeping: where does sqrt(pi) live, and does ANY prescription pin kappa=1/2?
=========================================================================================
The hard constraint: sqrt(32pi/3) is NOT in Q(pi); the irreducible sqrt(pi) can come ONLY
from sqrt(G rho_L) ~ sqrt(Lambda) (the density step). A genuine closure must leave a leftover
RATIONAL = exactly 1/2.  Here we (i) confirm the density step supplies sqrt(8pi/3), (ii) check
each prescription's leftover for being a pure rational, (iii) test the framework's ACTUAL claim
(the surface-gravity 'reach c in 2 free-fall times' reading) for forcing.
"""
import sympy as sp
G, M, Lam, c, hbar = sp.symbols('G M Lambda c hbar', positive=True)
pi = sp.pi

H_L  = c*sp.sqrt(Lam/3)
R_dS = c/H_L
rho_L = Lam*c**2/(8*pi*G)

print("="*78)
print("STEP 5: sqrt(pi) bookkeeping and the framework's own surface-gravity claim")
print("="*78)

# (i) the density step: a0 = kappa c sqrt(G rho_L). Factor out sqrt(Lambda):
expr = c*sp.sqrt(G*rho_L)               # the kappa=1 baseline
expr = sp.simplify(expr)
print("\n(i) c sqrt(G rho_L) =", expr)
# = c * sqrt(Lambda c^2/8pi) = c^2 sqrt(Lambda)/sqrt(8pi) = c^2 sqrt(Lambda) * 1/(2 sqrt(2pi))
print("    = c^2 sqrt(Lambda) / sqrt(8 pi).  The sqrt(pi) is HERE (1/sqrt(8pi)).")
print("    Z = cH_L / (kappa c sqrt(G rho_L)) = sqrt(8pi/3)/kappa.")
Z_of_kappa = sp.simplify(c*H_L/(sp.Symbol('kappa',positive=True)*expr))
print("    Z(kappa) =", Z_of_kappa, "  => Z = sqrt(8pi/3)/kappa.")
print("    For Z = sqrt(32pi/3): kappa = sqrt(8pi/3)/sqrt(32pi/3) = sqrt(8/32) = 1/2. EXACT.")
kap_needed = sp.sqrt(sp.Rational(8,1)*pi/3)/sp.sqrt(sp.Rational(32,1)*pi/3)
print("    check kappa_needed =", sp.simplify(kap_needed), " (pure rational 1/2, pi cancels). GOOD.")

print("""
(ii) THE CONSTRAINT RESTATED: the density step sqrt(G rho_L) ALREADY supplies the full
     sqrt(8pi/3) (verified). So a closure must produce a a0 of the form
         a0 = (RATIONAL) x c sqrt(G rho_L),  RATIONAL = 1/2,
     i.e. the matching must NOT inject any further pi.  Now: every prescription that
     gave a clean (M-independent) answer is checked for whether its kappa is a pure
     rational equal to 1/2:
""")
# Prescription C result from Step 4: a0 = 6 sqrt(3) sqrt(Lambda) c^2, kappa = 12 sqrt(6) sqrt(pi)
kapC = 12*sp.sqrt(6)*sp.sqrt(pi)
print("   Prescription C: kappa =", kapC, "=", float(kapC))
print("     -> contains sqrt(pi): NOT a pure rational. VIOLATES the constraint AND != 1/2.")
print("     (It injected an EXTRA sqrt(pi) via the horizon mass M_dS ~ 1/sqrt(Lambda),")
print("      whose own sqrt-structure double-counts the density sqrt(pi). Disqualified.)")

print("""
(iii) THE FRAMEWORK'S ACTUAL CLAIM (GEOMETRIC_ORIGIN_OF_A0.md, Reading 3):
      a0 = c^2/(2 R) with R = c/sqrt(G rho_L) = sqrt(8pi/3) c/H_L  (cosmic free-fall radius).
      'The 2 is the surface-gravity / reach-c factor: a horizon of radius R has surface
       gravity c^2/2R.'  Test: is the 1/2 FORCED by the horizon, or inserted?
""")
R_ff = c/sp.sqrt(G*rho_L)        # cosmic free-fall radius
a0_surfgrav = c**2/(2*R_ff)
a0_surfgrav = sp.simplify(a0_surfgrav)
print("   a0 = c^2/(2 R_ff) =", a0_surfgrav)
kap_sg = sp.simplify(a0_surfgrav/(c*sp.sqrt(G*rho_L)))
print("   => kappa =", kap_sg, " -- yes, this IS 1/2, BUT the 1/2 is the literal '2' in")
print("      'c^2/2R', i.e. INSERTED by writing surface gravity as c^2/2R. Check whether R_ff")
print("      is a real Schwarzschild horizon of its enclosed mass:")
# enclosed mass in radius R_ff at density rho_L:
M_enc = sp.Rational(4,3)*pi*R_ff**3*rho_L
M_sch = R_ff*c**2/(2*G)           # mass whose Schwarzschild radius is R_ff
ratio = sp.simplify(M_enc/M_sch)
print("      M_enclosed(R_ff)/M_Schwarzschild(R_ff) =", ratio, "= 8pi/3 =", float(ratio))
print("""      R_ff is NOT the Schwarzschild radius of its enclosed mass (off by 8pi/3). So
      'c^2/2R' is a surface gravity BY ANALOGY only; the 1/2 is a kinematic convention,
      not a horizon-forced quarter. EXACTLY the prior verdict. The MOND flux route does
      not change this: it never produced the 1/2 -- it produced M-dependence or 52.1.""")

print("""
================================================================================
STEP 5 VERDICT: kappa=1/2 is NOT forced by the Jacobson/first-law MOND route.
  - density step supplies the full sqrt(8pi/3) (the only legit sqrt(pi) source): OK
  - but the leftover prefactor is NOT pinned to 1/2 by any matching:
       * local Jacobson flux: a0 absent (8pi fixed by Unruh/BH; a0 is matter data)
       * energy-balance / first law: a0 comes out M-dependent (M^-3, M^-1) -- no closure
       * horizon self-energy: kappa = 12 sqrt(6) sqrt(pi) = 52.1 (wrong number, extra sqrt(pi))
       * framework's c^2/2R: kappa=1/2 but the 1/2 is INSERTED (R not a real horizon)
  => FREEDOM PERSISTS. Same null as homogeneous, by a DIFFERENT (and sharper) mechanism:
     the cubic vertex's M^{3/2} scaling is incommensurate with the first law's M^1.
================================================================================""")
