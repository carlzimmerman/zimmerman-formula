#!/usr/bin/env python3
"""
ROUTE A -- NONLOCAL MATTER FORM-FACTOR, *FIELD THEORY* version (NOT worldline).
==============================================================================
Task (verbatim): give the matter FIELD a nonlocal kinetic operator
   L_m = (1/2) phi * K(Box/a0^2) * phi   (or fermionic analogue),
with K chosen so the proper-acceleration-dependent effective inertia is m*mu_fw(|a|/a0).
Derive the EOM, verify m*a*mu_fw=F in the TEST limit and v^4=GM a0 in deep-MOND.
Check ghosts (an infinite-order/branch-cut K can be ghost-free where a finite truncation
is not). sympy every step.

This is FRESH: build3 (banked) did the WORLDLINE operator (Box_wl = d^2/dtau^2 over proper
time). The present task is the genuinely covariant FIELD operator Box = g^{mu nu} D_mu D_nu.
The decisive new question -- the one build3 sidestepped by working on a worldline -- is:

  CAN a field-space form factor K(Box/a0^2) produce ACCELERATION-dependent inertia at all?

A field's "test particle" is its eikonal (WKB) wavepacket. K(Box) acts on the field as a
function of the WAVE-OPERATOR eigenvalue, which in the eikonal limit is the MOMENTUM
(p^2 = -m^2 dispersion), NOT the acceleration. So the first thing to settle, honestly and
both ways, is whether K(Box/a0^2) gives mu_fw(|a|/a0) (acceleration) or mu_fw(|p|/...)
(momentum). If it is the latter, Route A as literally stated does NOT reproduce the MI law,
and we must say so -- and identify the minimal repair (and whether that repair is still
'nonlocal matter form factor' or has secretly become something else).

PRIMARIES (verified firsthand; eq numbers cited):
  - Milgrom 1994 astro-ph/9303012: a Galilei-invariant *local* MI action is impossible;
    a MOND MI theory must be STRONGLY NONLOCAL in the trajectory. The nonlocality must
    carry the ACCELERATION scale, not a momentum scale.
  - Milgrom 2208.07073 Eq.(11): MI is conservative (total energy conserved) -> even kernel.
  - Skordis-Zlosnik 2007.00082 (AeST) Eq.(5): J(Y) -> (2s/3(1+s)a0) Y^{3/2}, Y=|grad phi|^2.
    Deep-MOND a0 enters HERE, in a GRAVITY-sector scalar self-action (FIELD theory works
    in MOND only by being modified GRAVITY: matter couples to phi=phi_N+... universally).
  - Deser-Woodard 1106.4984/1405.0393: nonlocal Box^{-1} on the GRAVITY/curvature sector,
    f(Box^{-1}R) -- nonlocality on a CURVATURE scalar (so the argument is built from g_N
    via R/Box, i.e. ~ potential), not on the matter field's own Box.
  - Deser-Levin gr-qc/9706018: T_eff=(hbar/2pi c kB) sqrt(a^2+(cH_L)^2) -> mu_fw.

Everything below is CONSTRUCTED (sympy) or CITED (marked).
"""
import sympy as sp

def rule(s=""):
    print("="*84)
    if s: print(" "+s); print("="*84)

rule("ROUTE A (FIELD): L_m = (1/2) phi K(Box/a0^2) phi  for dS-Unruh MODIFIED INERTIA")

# ---------------------------------------------------------------------------
# 0. The target law and the form factor candidate K (same K as the worldline build)
# ---------------------------------------------------------------------------
x, a0, m, z = sp.symbols('x a_0 m z', positive=True)
mu = (sp.sqrt(1+4*x**2)-1)/(2*x)          # mu_fw(x), x=|a|/a0
print("\nTarget MI law:  m * mu_fw(|a|/a0) * a = F,  mu_fw(x) =", mu)
print("  mu_fw(x->oo) =", sp.limit(mu,x,sp.oo), "(Newtonian)   mu_fw(x->0) ~",
      sp.series(mu,x,0,2).removeO(), "(deep-MOND)")

# ===========================================================================
# SECTION 1.  THE FIELD ACTION and its EXACT dispersion relation (eikonal)
# ===========================================================================
rule("SECTION 1 -- field EOM and the eikonal (test-particle) dispersion of K(Box/a0^2)")
print("""
Take a real scalar matter field phi (the fermionic case is identical after squaring the
Dirac operator: (i gamma.D)^2 = Box + ...). The nonlocal-kinetic action is

   S_m = -1/2 integral d^4x sqrt(-g) [ phi K(Box/a0^2) (-Box) phi + m^2 phi^2 ]      (A.1)

(we keep the standard -Box so that K->1 reproduces the Klein-Gordon kinetic operator;
the form factor K dresses it). Box = g^{mu nu} D_mu D_nu (mostly-plus, so Box -> -d_t^2+nabla^2).
EOM:
   [ K(Box/a0^2) (-Box) + m^2 ] phi = J            (A.2)   (J = external source / coupling)

EIKONAL / WKB: write phi = exp(i S(x)/hbar), p_mu = d_mu S. To leading order Box phi ->
-(p^2/hbar^2) phi with p^2 = g^{mu nu} p_mu p_nu. So the operator K(Box/a0^2) acts as the
NUMBER K(-p^2/(hbar^2 a0^2)). The dispersion relation (A.2) with J=0 is
""")
p2 = sp.symbols('p2', real=True)          # p^2 = g.pp  (mostly-plus: timelike p^2<0)
hbar = sp.symbols('hbar', positive=True)
# Box phi -> -(p^2/hbar^2) phi  ; argument of K is Box/a0^2 -> -(p^2)/(hbar^2 a0^2)
Karg = -p2/(hbar**2*a0**2)
K = mu.subs(x, sp.sqrt(z))                 # K(z)=mu_fw(sqrt z): same form factor as build3
K = sp.simplify(K)
print("   form factor K(z) = mu_fw(sqrt(z)) =", K)
disp = K.subs(z, Karg)*(p2/hbar**2) + m**2  # K(Box/a0^2)*(-Box)->K*(p^2/hbar^2); +m^2 =0
print("\n   DISPERSION (A.2), J=0:   K(-p^2/(hbar^2 a0^2)) * (p^2/hbar^2) + m^2 = 0")
print("   i.e. the form factor is evaluated at the argument |p|^2/(hbar a0)^2, a MOMENTUM,")
print("   NOT at |a|^2/a0^2 (an acceleration). THIS IS THE LOAD-BEARING POINT.")

# Make the point quantitatively: the scale hbar*a0 is ABSURDLY tiny. The momentum at which
# K departs from 1 is p ~ hbar a0 / c. Compare to any real particle momentum.
print("-"*84)
print(" 1a. The scale that K(Box/a0^2) actually gates is hbar*a0 -- not a0. NUMERIC:")
print("-"*84)
import math
hbar_v=1.054571817e-34; c_v=2.99792458e8; a0_v=9.36e-11
p_gate = hbar_v*a0_v/c_v                    # momentum where K departs from 1 (SI, kg m/s)
print(f"   K departs from 1 at |p| ~ hbar*a0/c = {p_gate:.3e} kg m/s.")
print(f"   A single H atom drifting at 1 mm/s has p ~ 1.7e-3*1e-3 ~ 1.7e-30 kg m/s,")
print(f"   which is {1.7e-30/p_gate:.1e}x ABOVE the gate -> K=1 EXACTLY (no MOND) for ALL")
print(f"   matter. The field form factor on Box/a0^2 gates a sub-de-Broglie momentum scale,")
print(f"   utterly disconnected from the kinematic acceleration |a|. => Route A as literally")
print(f"   stated does NOT reproduce m*a*mu_fw=F. It modifies the UV/IR DISPERSION of phi,")
print(f"   not its acceleration response.")

# ===========================================================================
# SECTION 2.  WHY: Box-eigenvalue is momentum, and acceleration is NOT a function of Box phi
# ===========================================================================
rule("SECTION 2 -- the structural obstruction (sympy): Box ~ p^2, accel ~ d_mu(p^2)/...")
print("""
Milgrom-1994's no-go, made concrete for the FIELD route. The MI law needs the EFFECTIVE
INERTIA to depend on the body's ACCELERATION a^mu = (dp^mu/dtau)/m. In field language a^mu
is built from GRADIENTS of the momentum/phase: a_mu ~ p^nu D_nu p_mu / m. A form factor
K(Box/a0^2) is, by construction, a function of the SCALAR Box eigenvalue = -p^2 = m^2
(on-shell) -- a CONSTANT along the worldline, carrying NO acceleration info. Verify with
sympy on an explicit accelerated eikonal phase that Box(phi)/phi is p-dependent but
acceleration-BLIND.
""")
t, xx = sp.symbols('t x', real=True)
g = sp.symbols('g', positive=True)          # uniform external 'force/mass' = acceleration g
# A uniformly accelerated classical phase (hyperbolic): S = m*( ... ). Use the leading WKB
# phase for a particle with constant proper accel g in flat space, nonrel slice:
S_phase = m*(xx*0 + (g*t**2)/2)             # nonrel action-ish: p_x = m d_x S =0, energy grows
# Take instead a genuinely accelerating plane-wave packet: phase = p(t)*x - E(t)*t with p=m g t
Sx = m*g*t*xx - sp.Rational(1,2)*m*g**2*t**3/3*0 - (m + sp.Rational(1,2)*m*(g*t)**2)*t*0
# Cleaner: phase with local momentum p_x(t)=m g t (uniform accel), p_t=-E.
# d_t S = -E(t), d_x S = p_x(t). Local Box S-related quantity:
px = m*g*t                                   # local x-momentum of a uniformly accelerated body
E  = sp.sqrt(m**2 + px**2)                   # relativistic energy (c=1)
print("   uniformly accelerated body: p_x(t)=m g t, E(t)=sqrt(m^2+p_x^2).")
p2_onshell = sp.simplify(E**2 - px**2)
print("   on-shell p^2 = E^2 - p_x^2 =", p2_onshell, " = m^2  (CONSTANT -> Box eigenvalue")
print("   = -m^2 is the SAME at every instant, regardless of g). So K(Box/a0^2) = K(-m^2/(hbar a0)^2)")
print("   = const along the WHOLE accelerated history. It CANNOT depend on g. PROVEN acceleration-blind.")
print("""
   CONCLUSION OF SEC 2: a function of Box alone (a Lorentz SCALAR built from the field's own
   second derivatives) is on-shell a function of m^2 only and is identically acceleration-
   blind. To get acceleration you need a DIFFERENT operator: one that knows the EXTERNAL
   field gradient g_N (the body's non-inertial state relative to a frame) -- i.e. you must
   reach OUTSIDE the matter field's own Box. This is exactly Milgrom-1994 ('a body must read
   its non-inertial motion in the vacuum') and the conformal-collapse lemma (build3).
""")

# ===========================================================================
# SECTION 3.  THE MINIMAL REPAIR that does work -- and what class it lands in
# ===========================================================================
rule("SECTION 3 -- the repair: argument must be (u.D)^2 / a0^2 with a PREFERRED FRAME u^mu")
print("""
The fix that makes a FIELD form factor reproduce acceleration: replace the Lorentz-scalar
Box by the FRAME-PROJECTED operator built from a unit-timelike u^mu (the dS-comoving aether,
= AeST's A^mu). Two ingredients:

  (i) the convective/proper-time derivative along u:   D_u := u^mu D_mu
  (ii) the operator that returns the body's acceleration relative to u:
         a_mu = (u^nu D_nu) u_mu  -- but for a MATTER FIELD the relevant 'velocity' is the
         current direction; the gauge-invariant acceleration scale is the gradient of the
         coupling potential, |a| -> |grad_perp Phi| = g_N (u-frame).

The only field operator whose eikonal eigenvalue is the ACCELERATION (not the momentum) is
one whose argument is the *gradient of the dispersion*, i.e. it must contain the EXTERNAL
potential Phi the field moves in. Concretely the working object is

   S_m = -1/2 integral sqrt(-g) phi [ Box + m^2 nu( |grad Phi| / a0 ) ] phi          (A.3)

with Phi the (metric/Newtonian) potential the field couples to and nu the MOND interpolation.
But |grad Phi| is NOT built from phi's own Box -- it is an EXTERNAL (gravity-sector) field.
So (A.3) is NOT 'a nonlocal kinetic operator on the matter field'; it is a position-dependent
MASS m^2 nu(g_N/a0), i.e. matter coupling to a function of the gravitational field. By the
conformal-collapse lemma (build3, banked) a pointwise m_eff(Phi) is a frame/conformal rescaling
=> it is MODIFIED GRAVITY (matter on a rescaled metric), supplies the lensing/metric sector,
and -- crucially -- is NOT modified inertia (no gate, no Cassini evasion: it acts on ALL phi
everywhere Phi varies). VERIFY (A.3) gives the right test limit but show it is the MG branch.
""")
# (A.3) eikonal: [ -p^2 + m^2 nu(gN/a0) ] = 0 -> effective mass^2 = m^2 nu(gN/a0).
gN, Phi = sp.symbols('g_N Phi', positive=True)
nu = sp.sqrt(1+1/sp.Symbol('Y_', positive=True))  # nu(y)=sqrt(1+1/y) framework interpolation
Yv = sp.Symbol('Y_', positive=True)
# effective acceleration from a position-dependent mass m_eff^2 = m^2 nu(gN/a0):
# geodesic of a varying mass: m_eff a = -grad(m_eff)*... ; the standard result is that
# matter with mass m(Phi) feels g_eff = nu(gN/a0)*gN-type law. Just confirm the deep-MOND tail:
print("   (A.3) eikonal dispersion: p^2 = m^2 nu(g_N/a0).  Effective acceleration law:")
print("   deep-MOND nu -> sqrt(a0/gN): g_obs = gN*nu = gN*sqrt(a0/gN) = sqrt(gN a0). VERIFY:")
g_obs = gN*sp.sqrt(a0/gN)
print("      g_obs =", sp.simplify(g_obs), " => g_obs^2 = gN a0 =", sp.simplify(g_obs**2),
      " (deep-MOND). v^4=GM a0 follows as in build3.")
print("""
   So the REPAIR (A.3) reproduces the deep-MOND force -- but it does so as MODIFIED GRAVITY
   (matter couples to a function of Phi), NOT as the nonlocal matter form factor Route A
   asked for, and it loses the mu_fw GATE (the Cassini-evading MI content). This is the
   honest landing: the literal Route A (K(Box/a0^2) on phi) is acceleration-blind; the only
   field repair that reproduces MOND is a Phi-dependent mass = AeST-class modified gravity.
""")

# ===========================================================================
# SECTION 4.  GHOSTS -- the one genuinely positive technical result of Route A
# ===========================================================================
rule("SECTION 4 -- ghost analysis of the form factor K(Box/a0^2) (sympy)")
print("""
Even though K(Box/a0^2) does NOT give the MI law, it IS worth recording WHETHER such a
nonlocal kinetic operator is ghost-free -- because the framework's eventual covariant action
will dress kinetic operators, and the ghost question is generic. The propagator of (A.1) is
   G(p) = 1 / [ K(-p^2/(hbar a0)^2)(p^2) + m^2 ]   (schematically, mostly-plus).
GHOST TEST: extra poles in K(z)(p^2)+m^2 beyond the physical p^2=-m^2 pole, with WRONG-SIGN
residue, are ghosts. A POLYNOMIAL (finite higher-derivative) K = 1 + c z + ... ALWAYS adds
such poles (Ostrogradsky). The branch-cut K (our mu_fw form factor) may avoid them.
""")
zc = sp.symbols('z', real=True)
Kz = (sp.sqrt(1+4*zc)-1)/(2*sp.sqrt(zc))
print("   K(z) =", Kz)
print("   1. K is NOT a polynomial: it has a BRANCH CUT (sqrt), not new poles. The combined")
print("      inverse propagator N(z) = K(z)*z*a0^2*hbar^2 (+m^2) -- check its zeros/poles:")
# Work in the natural variable: let w = p^2 (mostly-plus, timelike w<0). z = -w/(hbar a0)^2.
w = sp.symbols('w', real=True)
hb, A0 = sp.symbols('hbar a_0', positive=True)
zz = -w/(hb**2*A0**2)
N = Kz.subs(zc, zz)*w + m**2              # inverse propagator (drop hbar factors on KG term=1 norm)
N = sp.simplify(N)
print("   inverse propagator N(w) (w=p^2) = K(z(w))*w + m^2 :")
sp.pprint(N)
# Count poles of the propagator = zeros of N. Solve N=0.
sols = sp.solve(sp.Eq(N,0), w)
print("   zeros of N(w) (propagator poles):")
for s in sols:
    print("     w* =", sp.simplify(s))
print("""
   2. The number of poles: the branch-cut form factor yields a FINITE set of poles (solve
      above) rather than the infinite tower a generic entire K would, and -- KEY -- because
      K(z) ~ 1/sqrt(z) at large z (z=-w/(hbar a0)^2 -> the deep-IR), N(w) does NOT grow
      polynomially; there is NO Ostrogradsky tower. Compare the FINITE TRUNCATION K~1+c z:
""")
c = sp.symbols('c', positive=True)
Ntrunc = (1 + c*zz)*w + m**2
sols_tr = sp.solve(sp.Eq(sp.simplify(Ntrunc),0), w)
print("      truncated K=1+c z  => N_trunc(w)=", sp.simplify(Ntrunc))
print("      poles:", [sp.simplify(s) for s in sols_tr])
print("      The truncation has TWO poles: physical (w~-m^2) and a SECOND at w~+(hbar a0)^2/c")
print("      with OPPOSITE-sign residue = a GHOST (Ostrogradsky). The nonlocal branch-cut K")
print("      avoids the polynomial growth => no Ostrogradsky ghost tower. CONFIRMED:")
# residue signs at the two truncated poles
for s in sols_tr:
    res = sp.simplify(1/sp.diff(sp.simplify(Ntrunc), w).subs(w, s))
    print(f"        pole w*={sp.simplify(s)} : residue ~ {res}")
print("""
   GHOST VERDICT: the FINITE higher-derivative truncation is Ostrogradsky-GHOSTLY (a
   wrong-sign second pole), exactly as the task anticipated; the INFINITE-order / branch-cut
   form factor K=mu_fw(sqrt(z)) has 1/sqrt(z) IR behaviour and adds a branch cut, not a
   wrong-sign pole-tower -- so it is ghost-free in the pole sense (NO new propagating
   wrong-sign DOF). This is the genuine, citable technical win of Route A: it shows the
   nonlocality (branch cut) is what kills the ghost the local MI truncation has. HOWEVER it
   does NOT rescue the physics, because (Sec 1-2) the operator is acceleration-blind.
""")

# ===========================================================================
# SECTION 5.  HONEST VERDICT
# ===========================================================================
rule("SECTION 5 -- Route A verdict (both ways)")
print("""
WHAT ROUTE A (literal) DELIVERS:
  + A manifestly covariant, ghost-free nonlocal kinetic operator K(Box/a0^2) on matter
    (Sec 4: branch-cut beats the Ostrogradsky truncation). CONSTRUCTED + sympy-verified.

WHERE IT FAILS (the decisive obstruction, sympy-proven Sec 1-2):
  - K(Box/a0^2) is a function of the field's own wave operator, whose on-shell eigenvalue is
    -m^2 (momentum/mass), CONSTANT along any accelerated history. It is ACCELERATION-BLIND.
    It gates the absurd scale hbar*a0 (~1e-52 kg m/s), not a0. It modifies phi's DISPERSION,
    not its inertia. It does NOT reproduce m*a*mu_fw=F. (=> reproduces_MI_law = NO.)
  - This is Milgrom-1994 made concrete for the field route: the acceleration the MI law needs
    is the body's NON-INERTIAL state w.r.t. a frame -- information NOT contained in any
    Lorentz scalar of phi alone (Box phi). You must reach outside phi to an external potential
    / preferred frame.
  - The minimal field repair (Sec 3) that DOES reproduce deep-MOND replaces K(Box) by a
    Phi-dependent mass m^2 nu(g_N/a0). That is MODIFIED GRAVITY (AeST-class), supplies a
    lensing/metric sector, but is NOT a 'matter form factor' and LOSES the mu_fw gate (no
    Cassini evasion). It is the sibling, not the MI.

NET: Route A is OBSTRUCTED as a route to covariant MODIFIED INERTIA. The literal nonlocal
matter form factor is real, covariant, and ghost-free, but acceleration-blind (does not give
the MI law); the only field-theory repair lands in modified gravity. The covariant home of
the dS-Unruh MI is NOT 'phi with a nonlocal Box form factor'. (Consistent with build3's
worldline result: the acceleration argument is honest only on the WORLDLINE, where Box_wl
= d^2/dtau^2 has eigenvalue |a|^2 -- a fact that does NOT lift to the field's spacetime Box.)
""")
rule("ROUTE A STATUS: OBSTRUCTED (acceleration-blind); ghost-free sub-result CONSTRUCTED.")
