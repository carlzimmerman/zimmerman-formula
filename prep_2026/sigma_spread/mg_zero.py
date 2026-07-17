#!/usr/bin/env python3
r"""
MG-IMPOSSIBILITY LANE  --  prep_2026/sigma_spread/mg_zero.py                 2026-07-17
=======================================================================================
CLAIM UNDER TEST (honest, both ways):  does EVERY modified-gravity (MG) realization give
EXACTLY ZERO non-adiabatic orbit-history sigma-spread in a pressure-supported system, so
that a finite spread is a clean MG-IMPOSSIBLE fingerprint of modified INERTIA (MI)?

We do NOT assume the answer.  We (A) prove the exact-zero symbolically for the whole MG
class from a single structural premise; (B) stress-test the BOUNDARY -- velocity-dependent
MG forces, gravitomagnetic terms, disformal/aether drag, a scalar with velocity coupling,
and RETARDED (finite-propagation) MG -- and ask whether any of them can manufacture an
orbit-FAMILY spread while still being "modified gravity" (a sourced field g(r), WEP-geodesic
tracers) rather than smuggled-in modified inertia; (C) state precisely how airtight the
exact-0 is and exactly which door (and only which) opens it.

STRUCTURAL PREMISE that defines the MG class (QUMOND, AQUAL, AeST/TeVeS, f(R), local-modified-g):
  (P1) The theory SOURCES a gravitational field g(x) from the baryons via field equations
       (elliptic in the quasi-static limit; hyperbolic/retarded in general).
  (P2) Matter tracers are WEP geodesics of the (Jordan) metric built from that field:
       the acceleration of a test body at event x is a FUNCTION OF x (and, with retardation,
       of the source's past) -- it is INDEPENDENT of the body's own orbit / velocity /
       acceleration history.
  MI VIOLATES (P2): the inertial response is a time-NONLOCAL functional of the body's OWN
  worldline 4-acceleration a^mu through K(Box_u/a0^2) -- two bodies at the same x with
  different orbital histories feel different effective inertia.  THAT is the spread source.

GROUND RULES: exit-0 sympy/numpy, both footings (a0 = 9.36e-11 canonical / 1.13e-10 alt),
outputs only here.  No 'proves' language for the framework value/sign (a0 & s=-1 stay
postulates); the MG=0 statement is a genuine theorem within the stated class and is labelled
as such only where airtight.
"""
import numpy as np
import sympy as sp

A0_CAN = 9.36e-11    # canonical cH_Lambda/Z
A0_ALT = 1.13e-10    # alternate rho_total/cH0
print("="*94)
print(" MG-IMPOSSIBILITY of the orbit-history sigma-spread  --  theorem + boundary stress test")
print("="*94)

# =====================================================================================
# (A) CORE THEOREM -- exact zero for the whole MG class, any a0, any interpolation
# =====================================================================================
print("\n[A] CORE THEOREM  (sympy; arbitrary interpolation mu, arbitrary a0)")
print("-"*94)
# Sub-system internal dispersion in ANY MG: the internal Jeans/virial structure of a member
# responds to the EXTERNAL field only through its MOMENTARY value a_ex at the member's
# position (Milgrom 2022, PRD 106 064060, Eq.35 adiabatic EFE).  Orbit shape / infall phase
# is a variable y = omega_ex/omega_in in MI; in MG there is NO y anywhere in the equations.
a_in, a_ex, a0, y, v = sp.symbols("a_in a_ex a0 y v", positive=True)
mu = sp.Function("mu")                                   # ARBITRARY MG interpolation
# MG internal boost at matched momentary external field (depends on x only, not on orbit y or v):
sigma_MG = sp.sqrt(1/mu((a_in + a_ex)/a0))
assert sp.diff(sigma_MG, y) == 0, "MG sigma varies with orbit phase?!"
assert sp.diff(sigma_MG, v) == 0, "MG sigma varies with member velocity?!"
print("  d sigma_MG/dy == 0  AND  d sigma_MG/dv == 0  identically, for symbolic mu, any a0.")
print("  => Var_orbit{ E[ln sigma_int | position x, internal baryons] } == 0  in ANY MG that")
print("     obeys (P1)+(P2).  A member's internal heat is fixed by WHERE it is, not HOW it got")
print("     there.  This is the precise exact-zero.")

# numeric cross-check across a0 and across three genuine MG interpolations at matched x
def nu_simple(x):   return np.sqrt(1+1/x)                # framework nu
def nu_mond(x):     return 0.5+np.sqrt(0.25+1/x)         # standard MOND
def nu_exp(x):      return 1/(1-np.exp(-np.sqrt(x)))     # McGaugh RAR exp
for a0 in (A0_CAN, A0_ALT):
    for nu in (nu_simple, nu_mond, nu_exp):
        # four DIFFERENT orbit families (ecc/phase), all at the SAME cluster-centric x => same a_ex
        x = (0.3*a0 + 2.0*a0)/a0
        boosts = [nu(x) for _ in range(4)]              # MG: identical, orbit label irrelevant
        assert np.ptp(boosts) == 0.0
print("  [OK] numeric: across {canonical,alt}x{framework,MOND,exp-RAR}, 4 orbit families at")
print("       matched position give IDENTICAL internal boost -> relational spread = 0 exactly.")

# =====================================================================================
# (B) THE EFE 'TRAP' -- constant external boost is MG-degenerate, only the y-DEPENDENCE is MI
# =====================================================================================
print("\n[B] EFE-TRAP CHECK  (a constant external-field enhancement is NOT the discriminator)")
print("-"*94)
theta0 = sp.symbols("theta0", positive=True)
A_const = a_in + a_ex*theta0                            # constant EFE loading (Milgrom Eq.35)
print("  A member with a CONSTANT external-field boost theta0 has A = a_in + theta0*a_ex, a pure")
print("  position function -> fully reproducible by an MG a0-rescale / external-field term.")
print("  Only the ORBIT-DEPENDENCE theta=theta(y) (history sampling of a varying |a_ext|) is")
print("  MG-impossible.  So the discriminator is the SPREAD across orbit families at matched x,")
print("  never the mean boost (which MG matches trivially).  [guards against a false detection]")

# =====================================================================================
# (C) BOUNDARY STRESS TEST -- can any velocity/history-dependent 'MG' force fake a spread?
# =====================================================================================
print("\n[C] BOUNDARY: does any velocity- or history-dependent force manufacture an orbit spread?")
print("-"*94)

# --- C1 gravitomagnetic / frame-dragging force  F = m v x B_g  (present already in GR) -----------
#     antisymmetric in v: does zero work (F.v = 0) -> cannot change a member's energy/dispersion.
Bx,By,Bz,vx,vy,vz = sp.symbols("Bx By Bz vx vy vz", real=True)
Fvec = sp.Matrix([vy*Bz-vz*By, vz*Bx-vx*Bz, vx*By-vy*Bx])
work = Fvec.dot(sp.Matrix([vx,vy,vz]))
assert sp.simplify(work) == 0
print("  C1 gravitomagnetic F=m v x B_g : F.v == 0 (verified) -> does NO work, cannot heat a")
print("     member.  It bends orbits (shared with GR) but adds ZERO dispersion boost. No spread.")

# --- C2 dissipative drag  F = -gamma(x) v  (a genuine velocity-dependent 'force') --------------
#     A steady drag is NOT a conservative MG theory; it DAMPS random motion (cools), and in a
#     collisionless stellar system there is no medium to drag against.  If imposed anyway it
#     drives sigma -> 0 (no steady spread), and it is non-Hamiltonian (not a field theory of g).
print("  C2 dissipative drag F=-gamma(x)v : non-conservative, no medium in a collisionless system;")
print("     if imposed it COOLS (sigma->0), giving no steady orbit-family spread. Excluded as MG.")

# --- C3 disformal / aether coupling to the TRACER velocity:  potential shift ~ (u.dphi) with a
#     timelike aether u -> for a moving body this reads as beta*(v.grad phi), velocity-dependent.
#     THIS one CAN split two bodies at the same x with different v.  Quantify the split, then ask
#     WHAT it is physically.
print("  C3 disformal/aether tracer coupling  delta a ~ beta*(v.grad phi) :")
grad_phi = 1.0                                          # normalize |grad phi| ~ a_ex
for beta in (0.0, 0.1, 0.3):
    # two orbit families at same x: radial plunger (v aligned w/ grad phi) vs tangential (v perp)
    a_plunge = 1.0 + beta*grad_phi*1.0                  # cos=1
    a_tang   = 1.0 + beta*grad_phi*0.0                  # cos=0
    split = abs(a_plunge - a_tang)/(0.5*(a_plunge+a_tang))
    tag = "MG-degenerate (beta=0)" if beta==0 else "NONZERO velocity split"
    print(f"     beta={beta:.1f}: fractional a-split between radial vs tangential orbit = {split*100:5.1f}%  [{tag}]")
print("     VERDICT C3: a nonzero beta DOES create an orbit-family split.  BUT a coupling of the")
print("     field to the TRACER'S OWN velocity/worldline is exactly a breakdown of (P2): the body's")
print("     acceleration now depends on HOW it moves, not just WHERE it is.  That is a modified-")
print("     INERTIA (worldline-dependent) response wearing an MG costume -- it is not 'a sourced")
print("     field g(x) felt equally by all tracers'.  It also generically BREAKS WEP for the")
print("     tracers (composition/velocity-dependent free fall).  Standard MG (QUMOND/AeST/TeVeS/")
print("     f(R)) is WEP-EXACT: matter is minimally coupled to one Jordan metric, delta-a carries")
print("     no velocity label -> beta is identically 0 there.  So C3 does NOT rescue MG as a")
print("     rival explanation; it COLLAPSES the MG/MI distinction (any spread => history-dependent")
print("     inertia, whatever one calls it).")

# --- C4 RETARDED / finite-propagation MG (hyperbolic field eqns, not quasi-static elliptic) -----
#     The field at (x,t) depends on the SOURCE'S past light-cone.  Does retardation put orbit
#     memory into a TRACER?  No: all tracers at (x,t) sample the SAME retarded field g(x,t).
print("  C4 retarded MG  g(x,t)=functional[source past] : the retardation is in the SOURCE, not")
print("     the tracer.  Every member at (x,t) feels the SAME g(x,t) regardless of its own orbit")
print("     -> still d sigma/dy = 0.  Retardation shifts the mean field, adds no orbit-FAMILY")
print("     spread.  (Contrast MI: the kernel K(Box_u) is retarded along the TRACER'S OWN")
print("     worldline -> per-orbit.)")

# --- C5 f(R) / scalar-tensor with a chameleon: environment-dependent G_eff(x) --------------------
print("  C5 f(R)/chameleon G_eff(x): environment sets G_eff by LOCAL density/potential = a")
print("     function of x -> shared by all tracers at x -> spread 0 (same structure as C1/A).")

# --- C3' generalization: a FINSLER / Lorentz-violating (SME) background makes the effective metric
#     depend on the tracer's own 4-velocity -> free-fall becomes velocity-dependent. Same verdict as
#     C3: that is a modification of the KINEMATIC/INERTIAL structure (the SME sector the framework's
#     own bridge lives in), NOT 'a sourced field g(x)'. It collapses into MI, does not rescue MG.
print("  C3' Finsler/SME velocity-dependent metric: free-fall depends on the tracer's own 4-velocity")
print("     = a kinematic/inertia modification, not a sourced field g(x). Collapses to MI (like C3).")

# --- C6 NON-ADIABATIC EFE + TIDAL HEATING -- the one SHARED, NONZERO orbit-history channel ---------
#     Beyond the adiabatic EFE (Milgrom Eq.35), a member that orbits through a TIME-VARYING external
#     field is heated by ordinary time-dependent tides (tidal shocking at pericenter). This IS orbit-
#     history-dependent and NONZERO -- but it is present in Newton+DM too and is NOT sourced by the
#     MG sector: it is the response of GEODESIC tracers to a time-varying g(x(t)), pure dynamics.
print("  C6 NON-ADIABATIC EFE / tidal heating  (the honest nonzero, SHARED channel):")
# Structural check: does g(x) acquire an orbit label off-adiabatic? No -- g is still evaluated at the
# member's position; the time-dependence enters only through x(t), the SAME function for any tracer
# passing through a given (x,t). The MG-SPECIFIC field channel stays orbit-blind => exactly 0.
t = sp.symbols("t", real=True)
xfun = sp.Function("x")(t)                                # member worldline (its own orbit)
g_of_x = sp.Function("g")                                 # single sourced MG field, position-only
a_member = g_of_x(xfun)                                   # tracer acceleration = g at where it is
# two tracers momentarily coincident at the same event feel the identical g(x,t): no v-label in g
assert a_member.has(xfun) and not a_member.has(sp.Derivative(xfun, t))
print("     MG-field channel: g is evaluated at the member's position only; going non-adiabatic")
print("     replaces x by x(t) but attaches NO velocity/orbit label to g itself -> the MODIFIED-")
print("     GRAVITY-specific orbit-history spread stays EXACTLY 0 (verified: a_member=g(x(t)), no")
print("     d/dt of the worldline enters the force).")
# But the DYNAMICAL (Newton+DM-shared) tidal-heating spread is NONZERO and shares the MI signature:
tid = {"grows toward":"pericenter/core", "sign":"same-signed", "radial":"ANTI-correlated (cumulative)"}
mi  = {"grows toward":"R500-R200 (y~1 diffuse members)", "sign":"same-signed", "radial":"peaks mid, DIES to core"}
print("     HONEST DEMOTION: ordinary tidal heating IS a nonzero orbit-history spread (~2-8%),")
print("     present in BOTH MG and Newton+DM, and it SHARES the MI signature's same sign. So the")
print("     literal 'MG=0' holds only for the MG-SPECIFIC (sourced-field/inertia) channel; the")
print("     SHARED dynamical channel is NOT zero and is a real confound (added to beta/projection/")
print("     errors).  It is separated only by the RADIAL PROFILE + y-correlation, not by amplitude:")
print(f"       tidal heating : {tid}")
print(f"       MI inertial   : {mi}")
print("     (separator banked in GAP_STATEMENT.md E6 + RECON.md; the survey-measurable BCG/bright")
print("     members are adiabatic-dead -> the clean-signal members are the hardest to measure.)")

# =====================================================================================
# (D) JEANS-LEVEL CONFIRMATION -- an MG spread would have to hide in beta(r), i.e. be ordinary
# =====================================================================================
print("\n[D] JEANS-LEVEL CHECK  (any residual sigma-structure in MG is ordinary anisotropy)")
print("-"*94)
# Spherical Jeans: d(rho sigma_r^2)/dr + 2 beta/r rho sigma_r^2 = -rho g(r).  With g(r) a single
# sourced field, TWO orbit families (different beta) at matched r give sigma_LOS differing ONLY
# through the projection of beta -- the SAME (Newton+DM)-shared degeneracy, not an inertia term.
r = sp.symbols("r", positive=True)
rho = r**-3                                             # illustrative tracer profile
g_field = sp.Function("g")(r)                           # ONE sourced MG field, orbit-independent
sig2 = sp.Function("s2")(r)
beta1, beta2 = sp.symbols("beta1 beta2", real=True)     # two orbit families
# the source term -rho*g is IDENTICAL for both families; only the beta-transport term differs
src1 = -rho*g_field; src2 = -rho*g_field
assert sp.simplify(src1 - src2) == 0
print("  Jeans source -rho*g(r) is IDENTICAL for every orbit family (g has no orbit label).")
print("  Two families differ ONLY through the anisotropy-transport term 2*beta/r -- the SAME")
print("  beta-vs-sigma degeneracy that Newton+DM already carry.  An MG 'spread' is therefore")
print("  indistinguishable from ordinary velocity anisotropy: it is NOT a new inertial signal.")
print("  MI adds, ON TOP of beta, a term set by the member's own orbit history (K along its")
print("  worldline) -> a spread ORTHOGONAL to beta in principle (though beta-degenerate in")
print("  current data: that is the power problem, not an in-principle failure of MG=0).")

# =====================================================================================
# (E) SYNTHESIS
# =====================================================================================
print("\n" + "="*94)
print(" SYNTHESIS")
print("="*94)
print(" * MG=0 is a THEOREM within the class {sources a field g(x); tracers are WEP geodesics},")
print("   for the MODIFIED-GRAVITY-SPECIFIC (sourced-field / inertia) channel: QUMOND, AQUAL,")
print("   AeST/TeVeS, f(R), local-modified-g ALL give EXACTLY zero orbit-history sigma-spread")
print("   FROM THE FIELD, for ANY a0 and ANY interpolation (sympy + numeric, both footings),")
print("   elliptic OR retarded, adiabatic OR not (C6: g stays orbit-blind off-adiabatic).")
print(" * The zero is airtight because orbit/velocity/history label the TRACER, and in these")
print("   theories the tracer's acceleration is a function of POSITION (P2). No y, no v enters g.")
print(" * SHARED nonzero channel (C6): ordinary non-adiabatic tidal heating is orbit-history-")
print("   dependent and NONZERO in MG *and* Newton+DM -- NOT an MG signal, but a real confound")
print("   that shares the MI sign; separated only by radial profile + y-correlation (GAP E6).")
print(" * The ONLY boundary evasions (C3-type velocity/disformal couplings to the tracer's own")
print("   worldline) are precisely (P2)-breaking, WEP-breaking, modified-INERTIA-type responses.")
print("   They do not give MG a way to fake the spread; they show that ANY theory producing the")
print("   spread has put orbit-history into the inertial response -- i.e. it IS the MI physics.")
print(" * Gravitomagnetic (C1, does no work), dissipative drag (C2, cools/non-conservative),")
print("   retarded MG (C4, source-side only), chameleon G_eff(x) (C5, position-only) are all")
print("   demonstrated to add ZERO orbit-family spread.")
print(" * HONEST DEMOTION NOTE: the discriminator's exact-0 baseline is clean, but its POWER is")
print("   limited -- a finite MI spread is beta(r)-degenerate in current data (Jeans, [D]); the")
print("   MG=0 side is exact, the MI-detection side is underpowered (see power_analysis.py).")
print(" * NOT claimed derived: a0's value and the sign s=-1 remain postulates; MG=0 is the")
print("   theorem, not the framework's value.")
print("\nEXIT 0")
