#!/usr/bin/env python3
"""
F6 -- SSB GOLDSTONE NORMALIZATION door on kappa=1/2.

Question: The framework is a preferred-frame theory: SO(4,1)->SO(3,1) (de Sitter
boost breaking), or equivalently an aether/khronon u^mu spontaneously broken.
Does the Nambu-Goldstone / condensate kinetic-term normalization fix kappa=1/2?

a0 = (c/2) sqrt(G rho_Lambda) = c^2 sqrt(Lambda/(32 pi)) = cH_Lambda / Z,
Z = 2 sqrt(8 pi/3). The lone free number is kappa = 1/2 = the coefficient OUTSIDE
sqrt(G rho_Lambda).

TWO GATES:
  G1 (anti-circularity): the structure must be FORCED by the framework's OWN
     dS/MM/aether/dS-Unruh content, not inserted to yield 1/2.
  G2 (scale-fraction): the 1/2 must be the SAME 1/2 as kappa -- the coupling
     OUTSIDE sqrt(G rho_Lambda) -- NOT a field-normalization convention, a VEV,
     or a vacuum energy (double-counts rho_Lambda).

kappa kept SYMBOLIC throughout. We test whether the Goldstone normalization
forces it.
"""

import sympy as sp

print("=" * 78)
print("F6 -- SSB GOLDSTONE NORMALIZATION: does it force kappa = 1/2 ?")
print("=" * 78)

# ----------------------------------------------------------------------------
# Symbols
# ----------------------------------------------------------------------------
c, G, Lambda, rho_L, H_L = sp.symbols('c G Lambda rho_L H_L', positive=True)
kappa = sp.symbols('kappa', positive=True)   # the lone free OUTSIDE coefficient
F, f, v = sp.symbols('F f v', positive=True)  # Goldstone decay constant / VEV
Z = sp.symbols('Z', positive=True)

# Framework dictionary (de Sitter, MM):  rho_L = Lambda c^2/(8 pi G),  Lambda=3 H_L^2/c^2
rho_L_expr = Lambda * c**2 / (8 * sp.pi * G)
Lambda_expr = 3 * H_L**2 / c**2

# a0 with kappa symbolic
a0 = kappa * c * sp.sqrt(G * rho_L)
a0_in_Lambda = a0.subs(rho_L, rho_L_expr)
a0_in_Lambda = sp.simplify(a0_in_Lambda)
print("\n[setup] a0 = kappa c sqrt(G rho_L) =", a0_in_Lambda, "  (kappa symbolic)")

# Solve for Z := cH_Lambda / a0
cH = c * H_L
a0_in_HL = a0_in_Lambda.subs(Lambda, Lambda_expr)
a0_in_HL = sp.simplify(a0_in_HL)
Z_of_kappa = sp.simplify(cH / a0_in_HL)
print("[setup] Z = cH_Lambda/a0 =", Z_of_kappa)
print("        at kappa=1/2:  Z =", sp.simplify(Z_of_kappa.subs(kappa, sp.Rational(1,2))),
      " =?= 2 sqrt(8pi/3) =", sp.simplify(2*sp.sqrt(sp.Rational(8,3)*sp.pi)))
print("        => kappa is purely the OUTSIDE multiplier; 8pi/3 lives inside the root.")

# ----------------------------------------------------------------------------
# STEP 1.  The canonical Goldstone kinetic normalization 1/2 (d phi)^2.
#          Is its 1/2 the same object as kappa?
# ----------------------------------------------------------------------------
print("\n" + "-" * 78)
print("STEP 1.  Canonical Goldstone kinetic term  L = (1/2)(d phi)^2 .")
print("-" * 78)

# A Nambu-Goldstone field pi is introduced as the phase of the order parameter.
# Standard CCWZ / sigma-model normalization:  Phi = (v + ...) e^{i pi/F}, and the
# kinetic term is L = (1/2) F^2 (d (pi/F))^2 = (1/2)(d pi)^2 for canonically
# normalized pi.  The "1/2" here is the FIELD-NORMALIZATION half.

# Field rescaling test: pi -> alpha * pi changes the coefficient 1/2 -> 1/(2 alpha^2).
alpha = sp.symbols('alpha', positive=True)
pi_t = sp.Function('pi')
t = sp.symbols('t')
half = sp.Rational(1, 2)

# Coefficient of the kinetic term under canonical rescaling pi_canon = alpha*pi_phys
coeff_canon = half                      # L = 1/2 (d pi_canon)^2
coeff_after_rescale = half / alpha**2   # in terms of pi_phys = pi_canon/alpha
print("L = 1/2 (d pi)^2 ;  under pi -> pi/alpha the coefficient 1/2 -> 1/(2 alpha^2) =",
      coeff_after_rescale)
print("=> the kinetic 1/2 is RESCALABLE: it is a field-normalization convention,")
print("   NOT a physical (rescaling-invariant) coupling.  This is the textbook fact")
print("   that the overall field normalization carries no physics until coupled to a")
print("   fixed external current.  GATE G2 test below.")

# ----------------------------------------------------------------------------
# STEP 2.  GATE G2: is the kinetic 1/2 the SAME 1/2 as kappa?
#          kappa multiplies sqrt(G rho_Lambda); it sets the value of a0.
#          The kinetic 1/2 multiplies (d pi)^2; it sets the canonical normalization
#          of the Goldstone field.  Dimensional + structural comparison.
# ----------------------------------------------------------------------------
print("\n" + "-" * 78)
print("STEP 2.  GATE G2 (scale-fraction): is the kinetic 1/2 == kappa ?")
print("-" * 78)

# kappa is dimensionless and multiplies an ACCELERATION sqrt(G rho_L) [=L T^-2].
# The kinetic 1/2 multiplies (d pi)^2; pi is the Goldstone, dimensionful but its
# normalization is absorbed into F (decay constant).  Structurally:
#
#   a0 = kappa * c * sqrt(G rho_L)     <- kappa OUTSIDE the root, multiplies a SCALE
#   L_kin = (1/2) (d pi)^2              <- 1/2 multiplies a FIELD-SQUARED, rescalable
#
# Decisive structural separation:  rescale the Goldstone field pi -> pi/alpha.
# The kinetic 1/2 changes (-> 1/(2 alpha^2)).  Does a0 change?  a0 has NO pi in it
# (the Goldstone is the massless mode; a0 is the symmetry-breaking SCALE in front of
# sqrt(G rho_L)).  So a field rescaling that moves the kinetic 1/2 leaves a0 (hence
# kappa) untouched => they are DIFFERENT objects.
print("Field rescaling pi -> pi/alpha:")
print("   kinetic coeff:  1/2  ->  1/(2 alpha^2)   (CHANGES)")
print("   a0 = kappa c sqrt(G rho_L):  NO pi-dependence  ->  UNCHANGED")
print("   => kappa is INVARIANT under the rescaling that moves the kinetic 1/2.")
print("   => the kinetic 1/2 and kappa are STRUCTURALLY DIFFERENT halves.")
print("   GATE G2: FAILED (different kind of half -- field-normalization, not coupling).")

# ----------------------------------------------------------------------------
# STEP 3.  The decay-constant / VEV route: does the SSB scale set a0?
#          In SSB, the Goldstone decay constant F (or VEV v) sets the scale.
#          Could a0 = kappa * (something) with kappa fixed by F's relation to rho_L?
# ----------------------------------------------------------------------------
print("\n" + "-" * 78)
print("STEP 3.  Decay-constant / VEV route: does F (or v) fix kappa ?")
print("-" * 78)

# For SO(4,1)->SO(3,1) the broken generators are the 4 de Sitter boosts; the
# Goldstones are a 4-vector (the aether/khronon tilt).  For an aether/khronon the
# kinetic term is (M^2/2)(d u)^2-type with a mass scale M.  The relevant scale that
# the framework's own content provides is rho_Lambda (the dS vacuum energy) and
# equivalently H_Lambda.  The SSB scale of the preferred frame is set by the dS
# radius:  the symmetry-breaking 'order parameter' is the timelike vector u^mu whose
# existence is the cosmological rest frame, normalized u^2 = -c^2 (a CONSTRAINT, not
# a dynamical VEV magnitude).

# Khronometric/Horava: the khronon kinetic term is (1/(16 pi G_aether)) * 3-tensor
# of dimensionless c_i.  The OVERALL prefactor (the Goldstone decay constant squared
# F^2 ~ M_Planck^2) is the analog of 1/16piG -- and the prior ghost-freedom verdict
# already proved it cancels from every physical (sign/ratio/speed) condition.

# Could F be tied to rho_L?  Test: if F^2 = beta * rho_L^(1/2) * (dim factors), does
# beta force kappa?  The Goldstone decay constant is a FREE input of the EFT (its
# value is the SSB scale, not fixed by the symmetry).  Goldstone's theorem fixes the
# EXISTENCE and masslessness of pi and the FORM of its couplings (derivative,
# 1/F suppressed), but NEVER the magnitude of F.
print("Goldstone's theorem fixes: (a) existence of pi, (b) masslessness,")
print("   (c) derivative coupling form (1/F per pi).  It does NOT fix |F| or |v|.")
print("   The SSB scale F is a FREE input (the order-parameter magnitude).")
print("   => even if a0 were written a0 = kappa c sqrt(G rho_L) with F somewhere,")
print("      Goldstone structure constrains the FORM, never the OUTSIDE number kappa.")

# Concrete: u^2 = -c^2 is a CONSTRAINT (unit-timelike aether). The constraint fixes
# the NORM of u, not a kinetic prefactor. The '1' in u^2=-c^2 (or the c^2) is a
# normalization convention of the vector, reabsorbable -- and it is the SAME kind of
# rescalable normalization as the kinetic 1/2, NOT the coupling kappa.
print("\nUnit-timelike constraint u^2 = -c^2: fixes the NORM of u (a convention),")
print("   reabsorbable into u -> u/|u|; it is rescalable, not the coupling kappa.")

# ----------------------------------------------------------------------------
# STEP 4.  Could the SSB VEV double-count rho_Lambda?  (GATE G2 second prong)
# ----------------------------------------------------------------------------
print("\n" + "-" * 78)
print("STEP 4.  Double-count guard: does the SSB 'vacuum energy' re-use rho_Lambda?")
print("-" * 78)
# In SSB the order-parameter potential V(phi) has a vacuum energy V(<phi>) = the
# condensate energy. In the preferred-frame/de Sitter breaking the relevant vacuum
# energy IS the dS vacuum energy rho_Lambda (that's what sources Lambda, i.e. the
# cosmological constant = the SSB condensate energy of the de Sitter vacuum).
# So any '1/2' harvested from V(<phi>) = (1/2) m^2 v^2-type is built from rho_L,
# which is ALREADY SPENT in sqrt(G rho_L) inside a0. Re-using it for kappa
# double-counts rho_Lambda.
print("V(<phi>) = condensate vacuum energy.  For dS breaking this IS rho_Lambda")
print("   (the cosmological constant = the de Sitter vacuum/condensate energy).")
print("   rho_Lambda is ALREADY inside a0 = kappa c sqrt(G rho_Lambda).")
print("   => any 1/2 from V(<phi>) = (1/2) m^2 v^2 re-uses rho_Lambda")
print("      => DOUBLE-COUNTS rho_Lambda.  GATE G2 second prong: FAILED.")

# ----------------------------------------------------------------------------
# STEP 5.  GATE G1 (anti-circularity): is the breaking pattern FORCED, and would
#          ANY forced pattern yield 1/2 non-circularly?
# ----------------------------------------------------------------------------
print("\n" + "-" * 78)
print("STEP 5.  GATE G1 (anti-circularity): is SO(4,1)->SO(3,1) FORCED, and does it")
print("         yield 1/2 WITHOUT inserting it?")
print("-" * 78)
# The breaking pattern SO(4,1)->SO(3,1) (a preferred cosmic frame) is genuinely
# FORCED by the framework: the dS group SO(4,1) is broken to the Lorentz subgroup
# SO(3,1) by the cosmological rest frame / the timelike aether u^mu. The number of
# broken generators = dim SO(4,1) - dim SO(3,1) = 10 - 6 = 4 (the dS boosts) =>
# 4 Goldstones (the aether tilt 4-vector, 3 physical after the constraint).
dim_so41 = sp.Rational(5*4, 2)   # dim SO(5)=SO(4,1) = 10
dim_so31 = sp.Rational(4*3, 2)   # dim SO(4)=SO(3,1) = 6
n_broken = dim_so41 - dim_so31
print(f"dim SO(4,1) = {dim_so41}, dim SO(3,1) = {dim_so31}, broken generators = {n_broken}")
print("   => 4 Goldstones (de Sitter boost / aether-tilt 4-vector).  Pattern FORCED. G1 form OK.")
print("   BUT: the COUNT of Goldstones (=4) is an INTEGER, not 1/2; nothing in the")
print("   coset structure SO(4,1)/SO(3,1) produces a 1/2 -- the only rationals are")
print("   the integer dimensions and the rescalable kinetic 1/2.")

# Coleman-Mandula / disjointness reminder (gravity<->flavor disjoint) -- the SSB
# here is gravitational (the cosmic frame), with no internal flavor charge to supply
# a fractional weight.
print("   No fractional weight available from the coset: dims are 10,6,4 (integers).")

# ----------------------------------------------------------------------------
# SUMMARY
# ----------------------------------------------------------------------------
print("\n" + "=" * 78)
print("SUMMARY -- F6 verdict")
print("=" * 78)
print("""
The canonical Goldstone kinetic 1/2 in L = (1/2)(d pi)^2 EXISTS and is real, but:

  * GATE G2 (scale-fraction) FAILS three ways:
      (a) the kinetic 1/2 is RESCALABLE (pi->pi/alpha sends 1/2 -> 1/(2 alpha^2))
          while kappa is INVARIANT under that rescaling -- different objects;
      (b) the SSB decay constant F / VEV v is a FREE input (Goldstone's theorem
          fixes existence+masslessness+derivative-coupling FORM, never |F|);
      (c) any 1/2 from the condensate vacuum energy V(<phi>) re-uses rho_Lambda
          (the dS vacuum energy = the cosmological constant), DOUBLE-COUNTING the
          rho_Lambda already inside a0 = kappa c sqrt(G rho_Lambda).

  * GATE G1 (anti-circularity): the SO(4,1)->SO(3,1) breaking IS forced (4 dS-boost
    Goldstones), but the coset yields only INTEGER dimensions (10,6,4) -- no 1/2.

  * This is the SAME scale-fraction wall that closed ghost-freedom, unitarity,
    holography, CKN-dof, and topological-eta: kappa is the OVERALL action
    normalization OUTSIDE sqrt(G rho_Lambda); the Goldstone normalization (the
    kinetic 1/2, the decay constant F, the VEV) lives INSIDE the field structure
    and is rescalable / free / double-counting -- it can never reach the outside
    multiplier.  Precisely the ghost-freedom result: the Goldstone decay constant
    F^2 ~ M_Planck^2 ~ 1/16piG is the OVERALL prefactor that cancels from every
    sign/ratio/speed condition.

VERDICT: HITS-WALL.  The kinetic 1/2 is the 'conventional 1/2, rescalable, not the
coupling' half, exactly as anticipated.  Computed both ways: no non-circular path
from Goldstone normalization to kappa=1/2.
""")
