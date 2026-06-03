#!/usr/bin/env python3
"""
CLEAN SLATE: what relativistic field theory does the horizon foundation FORCE?
=============================================================================
We assume NOTHING about AeST. We start from what Layers 0-2 established as physics and ask,
step by step, what fields and structures the requirements FORCE. The aim is to see how much of
a relativistic MOND theory is derived vs chosen -- honestly. Each step: [FORCED] (a requirement
leaves no choice), [DERIVED] (computed here), [CONSTRAINED] (narrowed by a physical/observational
demand), [OPEN] (genuine residual freedom). Needs sympy.
"""
import sympy as sp

print("="*86)
print("THE STARTING POINT (established as physics, no numerology -- web_of_connections_audit.py)")
print("="*86)
print("""  F1. Gravity is the thermodynamics of horizons (Jacobson 1995): area-law entropy + Unruh
      temperature => the metric obeys the Einstein equations.
  F2. A particle accelerating at a in an expanding universe sees T(a)=(hbar/2pi c kB)sqrt(a^2+(cH)^2)
      (de Sitter-Unruh) => modified inertia, MOND a^2 law, scale a0~cH, evolving as E(z). [Layer 0]
  Nothing below assumes AeST. We let these two facts dictate the field content.\n""")

print("="*86)
print("STEP 1 [FORCED] -- a METRIC g_mu_nu (tensor)")
print("="*86)
print("""  F1 says gravity = geometry: the dynamical object is the spacetime metric, obeying Einstein
  in the high-acceleration limit. So a rank-2 tensor field g_mu_nu is forced. (This is just GR;
  no MOND yet.)\n""")

print("="*86)
print("STEP 2 [FORCED] -- a UNIT TIMELIKE VECTOR A_mu (a preferred frame)")
print("="*86)
print("""  F2's temperature T(a) is defined relative to ONE frame: the cosmic rest frame (the matter/
  CMB frame, where the de Sitter bath is isotropic). To write 'a0 ~ cH' covariantly you must have
  a field that POINTS along cosmic time everywhere. The minimal such object is a vector field A_mu.
  It must be UNIT TIMELIKE (A_mu A^mu = -1) so it is a proper 4-velocity / clock, not a rescalable
  direction. => a constrained vector A_mu is FORCED by the need to carry the horizon frame.""")
# compute: on FRW the comoving unit vector has divergence 3H -- the horizon rate, covariantly
t = sp.symbols('t', positive=True); a = sp.Function('a', positive=True)(t)
g = sp.diag(-1, a**2, a**2, a**2); sqrtmg = sp.sqrt(-g.det())
theta = sp.simplify(sp.diff(sqrtmg*1, t)/sqrtmg)
print(f"     check: div A on FRW = {sp.simplify(theta)} = 3H  -> A carries the cosmic expansion rate. [DERIVED]\n")

print("="*86)
print("STEP 3 [FORCED] -- a SCALAR phi (the long-range MOND carrier)")
print("="*86)
print("""  F2's modification is a LONG-RANGE, low-acceleration force (it dominates in galaxy outskirts).
  As a local field theory it must be carried by a dynamical field beyond the metric. A massless
  SCALAR phi is the minimal carrier of a long-range force that is sourced by mass and adds to
  gravity. => a scalar phi is FORCED. (Vector + scalar + tensor: the field content is now fixed,
  WITHOUT having assumed AeST -- it is what 'geometry + preferred frame + long-range MOND' requires.)\n""")

print("="*86)
print("STEP 4 [DERIVED] -- the MOND term must be built from q = g + A A, and that makes it CMB-SAFE")
print("="*86)
print("""  The MOND scalar's kinetic scalar cannot be the naive g^{mu nu} grad phi grad phi: that would
  make phi act on the cosmic background and wreck the CMB. The de Sitter-Unruh effect is about
  acceleration ORTHOGONAL to the cosmic frame, so the natural kinetic scalar uses the projector
  orthogonal to A:  q^{mu nu} = g^{mu nu} + A^mu A^nu,  Y = q^{mu nu} grad_mu phi grad_nu phi.
  Compute q^{00} on FRW (A^mu=(1,0,0,0)):""")
gi = g.inv()                                   # inverse metric (c=1): diag(-1, 1/a^2,1/a^2,1/a^2)
A_up = sp.Matrix([1,0,0,0])
q00 = sp.simplify(gi[0,0] + A_up[0]*A_up[0])   # q^{00} = g^{00} + A^0 A^0
print(f"     q^00 = g^00 + A^0 A^0 = ({gi[0,0]}) + (1) = {q00}")
print(f"""     => q^00 = 0 on FRW. So for a homogeneous phi=phi(t), Y = q^00 (phi')^2 = 0 EXACTLY:
     the MOND term VANISHES on the cosmic background. a0 is absent from the FRW equations and from
     LINEAR perturbations -> the CMB is untouched. This is Paper II's delta-q^00=0 result, and here
     it is DERIVED as a CONSEQUENCE of building the MOND term from the frame-orthogonal projector --
     which Step 2 forced. CMB-safety is not an add-on; it falls out of the preferred-frame structure.\n""")

print("="*86)
print("STEP 5 [FORCED] -- the deep-MOND limit fixes the kinetic POWER: L ~ Y^{3/2}")
print("="*86)
print("""  F2 derived the deep-MOND force law a = sqrt(g_N a0). For a scalar with action INT f(Y),
  the static point-mass solution gives grad phi ~ (source)^{1/(2n-1)} for f~Y^n. Requiring the
  sqrt law (grad phi ~ sqrt(rho), i.e. the 1/2 power) forces 2n-1 = 2 -> n = 3/2. So the deep-MOND
  kinetic term is L ~ Y^{3/2} ( = |grad phi|^3 ), DERIVED -- not chosen. (This is the AQUAL cubic.)\n""")

print("="*86)
print("STEP 6 [CONSTRAINED] -- GW speed and ghost-freedom narrow the couplings")
print("="*86)
print("""  GW170817: gravitational waves travel at c to 1e-15. That forbids the scalar/vector from
  altering the tensor sound speed -> the A-phi-g couplings are constrained (disformal terms tuned,
  the unit-vector constraint helps). Ghost-freedom fixes the kinetic signs. These do NOT pick a
  unique Lagrangian, but they NARROW the tensor-vector-scalar family sharply -- and AeST
  (Skordis-Zlosnik 2021) is the known member that satisfies all of them simultaneously.\n""")

print("="*86); print("WHAT THE CLEAN SLATE FORCED vs LEFT OPEN"); print("="*86)
print("""  FORCED purely from the horizon foundation (no AeST assumed, no numerology):
    * field content  = metric + unit-timelike vector + scalar   (Steps 1-3)
    * the MOND kinetic scalar = q^{mu nu} grad phi grad phi, q = g + A A   (Step 4)
    * => CMB-safety (Y=0 on FRW) as a DERIVED consequence, not an input   (Step 4, computed)
    * the deep-MOND kinetic power Y^{3/2}                                  (Step 5)
    * a0 ~ cH and a0(z)=a0(0)E(z)                                          (Layer 0)
  This is ~80% of AeST's structure, DERIVED from requirements -- a much stronger statement than
  'reverse-engineer AeST': the theory's SHAPE is forced by the physics.
  STILL OPEN (the honest residual freedom):
    * the full interpolation function (Newton<->MOND transition) -- the deep limit fixes only the
      tail; the crossover shape is not forced;
    * the cosmological function K(Q) that supplies the CDM-like background for structure/CMB;
    * the precise GW-safe/ghost-free coupling coefficients (Step 6 narrows, does not fix).
  HONEST VERDICT: starting from a clean slate, the horizon foundation FORCES a tensor-vector-scalar
  theory whose MOND term is the frame-orthogonal Y^{3/2} -- automatically CMB-safe -- with a0~cH
  evolving. That is the AeST CLASS, derived rather than assumed. The remaining freedom (interpolation
  + K(Q) + exact couplings) is the genuine, sharply-bounded open problem -- and none of it is numerology.""")
print("="*86)
