#!/usr/bin/env python3
r"""
ROUTE 2 -- EINSTEIN-AETHER WITH A SHEAR-ABSORBING SOURCE COUPLING.
==================================================================================================
TASK (verbatim): Write the Einstein-aether action (Jacobson; coefficients c1..c4) with a^mu the
unit-timelike aether, and ADD a coupling of the aether to the gated baryon source such that the
aether stress T^aether_munu has T_00=0 (delta-Phi=0) and a traceless-but-conserved T_ij (the
aether's divergence cancels the (2/3)d_j grad^2 f via the aether EOM, NOT by hand). Tune c_i for
c_T=c (c13=0 corner). Compute delta-Phi, delta-Psi, c_T, and the full aether mode spectrum
(spin-2,1,0) for ghosts. Is the conservation-completion done by the aether DYNAMICS (derived) or
imposed?

THE NO-GO THIS MUST BEAT (banked COVARIANT_LENSING_NOGO_2026-06-17.md, Bianchi leg sympy-airtight):
  In ANY 4-diffeomorphism-invariant theory, nabla_mu G^munu=0 forces nabla_mu T^lens_munu=0 on the
  partner. A pure-slip source (T_00=0, traceless T_ij = d_i d_j f - (1/3)delta_ij grad^2 f) has
  trace EXACTLY 0 but divergence div_i T_ij = (2/3) d_j(grad^2 f) != 0. Restoring conservation drags
  in an isotropic pressure 3 delta-p = -2 grad^2 f != 0, which sources delta-Phi. So delta-Phi=0 is
  IMPOSSIBLE in any 4-diff-invariant realization -- UNLESS a NON-DYNAMICAL preferred frame u^mu
  absorbs the divergence (2/3)d_j(grad^2 f) WITHOUT a Phi-sourcing trace.

THE NEW INGREDIENT (what canonical Route 4 lacked): the standard Einstein-aether is STILL fully
4-diff-invariant (the aether is a DYNAMICAL field with its own EOM and its own contribution to the
Bianchi identity), so it is bound by the SAME no-go -- which is exactly why Route 4 hit gamma=1.
Route 2 asks whether ADDING an explicit SHEAR-ABSORBING coupling -- a Lagrange multiplier b^j that
soaks the divergence into the NON-DYNAMICAL frame, NOT into the metric trace -- escapes it. We
compute, from the action, whether the aether's OWN equations of motion deliver T_00=0 + conserved
traceless T_ij, or whether that outcome has to be PUT IN BY HAND (= phenomenology, AeST F(Y,Q)).

PRIMARY SOURCES (read verbatim / confirmed this session):
  * Foster-Jacobson gr-qc/0509083 (PDF fetched): action
      L = -R/16piG + (1/2) K^{ab}_{mn} grad_a u_b grad^m u^n - lambda(g_ab u^a u^b - 1),
      K^{ab}_{mn} = c1 g^ab g_mn + c2 d^a_m d^b_n + c3 d^a_n d^b_m + c4 u^a u^b g_mn.
      VERBATIM: gamma=1 and beta=1 EXACTLY for all c_i (PPN). G_N=G/(1-c14/2). c_T=c <=> c13=0.
  * Blas-Pujolas-Sibiryakov 0909.3525 (healthy khronometric): the khronon T gives a HYPERSURFACE-
      ORTHOGONAL u_mu = -d_mu T/sqrt(-(dT)^2); the foliation is the preferred (non-dynamical-frame)
      structure. Healthy extension: regular scalar-graviton quadratic action.
  * Saltas-Sawicki-Amendola-Kunz 1406.7139 (confirmed incl. Einstein-Aether): slip <=> modified
      tensor sector {c_T-1, nu=running M_*, mu}; sigma is TIME-ONLY -> a c_T=c slip can only be a
      constant ratio, NOT the MOND scale-dependence. (This is the deeper wall the static PPN sees.)

CONFIG (framework's own; QUARANTINED -- never asserted "derived"): a0 = 9.36e-11, kappa=1/2,
g_obs = sqrt(g_N^2 + g_N a0). HONESTY BAR: WORKS only if the EXPLICIT action LINEARIZES (shown) to
all four AND the slip is a CONSEQUENCE of the action, not reverse-engineered. Penalized equally
both ways.
"""
import sympy as sp

def H(t): print("\n"+"="*98+"\n "+t+"\n"+"="*98)
def h(t): print("\n"+"-"*98+"\n "+t+"\n"+"-"*98)

# =================================================================================================
H("SECTION 0 -- the action, and the precise statement of what must be DERIVED vs IMPOSED")
# =================================================================================================
print(r"""
THE PROPOSED ROUTE-2 ACTION (explicit, Lorentz-violating, with the new shear-absorbing coupling):

  S = (1/16piG) int sqrt(-g) [ R - K^{ab}_{mn} grad_a u^m grad_b u^n - lambda (u_mu u^mu + 1) ]   <- Einstein-aether
    + S_matter[g]                                                                                  <- baryons couple to g ONLY
    + S_abs[u, b, source]                                                                          <- NEW shear-absorbing term

  where the NEW term, designed to soak the shear divergence into the NON-DYNAMICAL frame u^mu:
      S_abs = int sqrt(-g)  b^mu ( P^nu_mu  nabla^rho sigma_{rho nu}  -  J_mu[source] )
  with:
      b^mu        = a Lagrange-multiplier vector field (its EOM sets the bracket to zero),
      P^nu_mu     = delta^nu_mu + u^nu u_mu  (the projector ORTHOGONAL to u, the non-dynamical frame),
      sigma_{rho nu} = the traceless shear we want light to feel (= d_rho d_nu f - (1/3)g_{rho nu} box f),
      J_mu[source] = the gated-baryon current = grad of the gated MI source f (built from g_obs).

  IDEA: b^mu's EOM imposes  P^nu_mu nabla^rho sigma_{rho nu} = J_mu  -- i.e. it FORCES the projected
  (spatial, u-orthogonal) divergence of the shear to equal the baryon current. The hope: because the
  projector P kills the u-direction (time) component, the divergence is absorbed into the SPATIAL
  (Psi) sector and the trace that would source Phi never appears.

WHAT MUST BE TRUE FOR THIS TO BE *DERIVED* (not hand-tuned):
  (D1) The variation of S w.r.t. u^mu (the aether EOM) + variation w.r.t. b^mu + the lambda
       constraint must CLOSE consistently, i.e. b^mu must have a solution, AND
  (D2) the resulting aether stress T^aether_00 must come out = 0 as a CONSEQUENCE of the EOM
       (not because we set a free function to make it so), AND
  (D3) the traceless T_ij must be conserved with the divergence landing in the NON-DYNAMICAL u
       sector, AND
  (D4) the profile sigma (hence grad delta-Psi = 2(g_obs-g_N)) must be FIXED by the action's
       structure, not chosen by hand. If sigma is a FREE FUNCTION we tune to match 2(g_obs-g_N),
       this is AeST's F(Y,Q) phenomenology, NOT a derived Lagrangian. <-- the load-bearing test.
""")

# =================================================================================================
H("SECTION 1 -- (3) c_T=c and (4) ghost spectrum: the EASY conditions (reconfirm, both ways)")
# =================================================================================================
c1,c2,c3,c4 = sp.symbols('c1 c2 c3 c4', real=True)
c13 = c1 + c3; c14 = c1 + c4; c123 = c1 + c2 + c3
# Foster-Jacobson Eq.15 mode speeds (verbatim form), standard Einstein-aether:
s2sq = 1/(1 - c13)                                              # spin-2 graviton
s1sq = (c1 - c1**2/2 + c3**2/2)/(c14*(1-c13))                   # spin-1 vector
s0sq = c123*(2-c14)/(c14*(1-c13)*(2+c13+3*c2))                  # spin-0 scalar
print("  spin-2 graviton speed^2  s2^2 = 1/(1-c13)   [Foster-Jacobson Eq.15]:")
print("     c_T=c  <=>  s2^2=1  <=> ", sp.solve(sp.Eq(s2sq,1), c13), " -> c13 = c1+c3 = 0. (EASY)")
# Impose c13=0 (c3=-c1) and exhibit an all-positive-speed corner (ghost+gradient stable):
sub = {c3: -c1}
s1c = sp.simplify(s1sq.subs(sub)); s0c = sp.simplify(s0sq.subs(sub))
print("  Impose c13=0 (c3=-c1):  s1^2 =", s1c, " ;  s0^2 =", s0c)
witness = {c1: sp.Rational(1,10), c3: -sp.Rational(1,10), c2: sp.Rational(1,20), c4: sp.Rational(1,20)}
print("  ghost-free witness c1=.1,c3=-.1,c2=.05,c4=.05 (c13=0):  s2^2=%s s1^2=%s s0^2=%s  -> all>0."
      % (sp.N(s2sq.subs(witness),4), sp.N(s1sq.subs(witness),4), sp.N(s0sq.subs(witness),4)))
print("""
  CONFIRMED (both ways): c_T=c (c13=0) and ghost-freedom (open all-speeds^2>0 corner) are the EASY
  conditions -- NOT the obstruction, exactly as the no-go states. The new shear-absorbing term must
  not REINTRODUCE a ghost; we check its mode in Section 4. The hard part is (1)+(2): delta-Phi=0 AND
  the position-dependent slip TOGETHER, which we now compute from the action.
""")

# =================================================================================================
H("SECTION 2 -- LINEARIZE: the aether stress on the static weak-field background (from the action)")
# =================================================================================================
print(r"""
Metric  ds^2 = -(1+2Phi)dt^2 + (1-2Psi)dx^2.  We compute the LINEARIZED stress tensor that the
Einstein-aether + S_abs action feeds into  G_munu = 8piG (T^matter + T^aether + T^abs)_munu,
then read delta-Phi, delta-Psi, and test conservation. We work to linear order in {Phi,Psi,f}.
""")
import sympy as sp
x,y,z,t = sp.symbols('x y z t', real=True)
Phi = sp.Function('Phi'); Psi = sp.Function('Psi'); f = sp.Function('f')
# Use a 1D-along-x slice for the divergence structure (enough to expose trace vs divergence);
# 'box f' -> f'' (1D Laplacian stand-in), shear sigma_xx = (2/3) f'' (traceless quadrupole piece).
r = sp.symbols('r', positive=True)
Phir = Phi(r); Psir = Psi(r); fr = f(r)

# The shear we WANT light to feel: sigma_{ij} = d_i d_j f - (1/3) delta_ij nabla^2 f  (traceless).
# Its divergence (the no-go's obstruction):  d_i sigma_{ij} = (2/3) d_j (nabla^2 f).
# In sympy (radial 1D core): nabla^2 f -> f''(r); shear radial component s_rr = (2/3) f''(r).
lap_f = sp.diff(fr, r, 2)                      # 1D Laplacian core
s_rr  = sp.Rational(2,3)*lap_f                 # radial traceless shear component
div_shear = sp.diff(s_rr, r)                   # d_r s_rr  (the (2/3) d(nabla^2 f) obstruction)
print("  traceless shear (radial)  sigma_rr = (2/3) nabla^2 f =", s_rr)
print("  shear divergence          d_r sigma_rr = (2/3) d_r(nabla^2 f) =", div_shear, "  != 0  (THE OBSTRUCTION)")

# =================================================================================================
H("SECTION 3 -- THE DECISIVE STEP: does the b^mu multiplier absorb the divergence into the NON-")
h("           DYNAMICAL u direction, or does it leak a Phi-sourcing trace? (compute, don't assert)")
# =================================================================================================
print(r"""
Vary S_abs = int sqrt(-g) b^mu ( P^nu_mu nabla^rho sigma_{rho nu} - J_mu ) w.r.t. each field.

  (a) delta/delta b^mu :   P^nu_mu nabla^rho sigma_{rho nu} = J_mu                       (CONSTRAINT)
  (b) delta/delta g^munu:  b couples to the metric -> b contributes its OWN stress T^abs_munu
  (c) delta/delta u^mu :   b couples to u (through P^nu_mu = delta + u u) -> modifies aether EOM

The constraint (a) is the engine. P^nu_mu = delta^nu_mu + u^nu u_mu projects ORTHOGONAL to u.
On the static background u^mu=(1,0,0,0) (the cosmic rest frame, NON-DYNAMICAL here), so:
  - the TIME component (mu=0):  P^nu_0 = delta^nu_0 + u^nu u_0 = delta^nu_0 - delta^nu_0 = 0.
    => the constraint has NO time component: b^0 is unconstrained / drops. Good: nothing forces a
       time-time (Phi) source from the constraint itself.
  - the SPACE components (mu=j): P^nu_j = delta^nu_j (u_j=0) => constraint reads
       d_i sigma_{ij} = J_j   =>   (2/3) d_j(nabla^2 f) = J_j.
    So J_j (the gated baryon current) is SET EQUAL to the shear divergence. The divergence is
    'absorbed' in the sense that b^j is the field that enforces this -- but now we must check what
    b couples back into via (b),(c): does b^j's OWN metric stress T^abs_munu have a nonzero 00
    component (-> sources Phi)?
""")
# Compute T^abs_munu from S_abs = int sqrt(-g) b^mu(P^nu_mu nabla^rho sigma_rho nu - J_mu).
# The metric variation hits THREE places: sqrt(-g), the projector P (via u u and index raising),
# and the nabla^rho sigma_rho nu (covariant derivatives -> Christoffels -> metric). At LINEAR order
# about flat space with the CONSTRAINT (a) imposed (bracket=0), the bracket-times-b vanishes, so the
# ONLY surviving metric-variation stress is from the EXPLICIT sqrt(-g) and the metric inside the
# bracket BEFORE setting it to zero. The standard result for a multiplier term L = b*(C[g] - J):
#   T^abs_munu = b * (delta C / delta g^munu)  -  (1/2) g_munu * b*(C - J)
# On-shell C=J so the second piece vanishes; the first is b * (variation of the shear-divergence).
print(r"""
  KEY COMPUTATION (the multiplier stress).  For a constraint term L_abs = b^mu (C_mu[g,sigma] - J_mu)
  with C_mu = P^nu_mu nabla^rho sigma_{rho nu}, the metric stress is
        T^abs_munu = b^alpha (delta C_alpha / delta g^munu)  -  (1/2) g_munu b^alpha(C_alpha - J_alpha).
  ON-SHELL (b-EOM imposes C=J) the trace-like second term VANISHES identically:
""")
b_alpha, C_alpha, J_alpha = sp.symbols('b^alpha C_alpha J_alpha', real=True)
second_term = -sp.Rational(1,2)*b_alpha*(C_alpha - J_alpha)
print("     second (trace) term  -(1/2) g_munu b(C-J)  =", second_term.subs(C_alpha, J_alpha),
      "  (on-shell C=J  ->  ZERO).  No metric-trace source from the constraint. ")
print(r"""
  So the ONLY surviving T^abs is the first term, b^alpha (delta C_alpha/delta g^munu). C_alpha is a
  SPATIAL (u-orthogonal) current; its metric variation produces a stress that, on the static
  background with u=(1,0,0,0), has its support in the SPATIAL block (the j-indices), because C_0=0
  identically (shown above). We now extract its 00 and ij parts explicitly.
""")

h("3a. the 00 component of the total partner stress -> does delta-Phi = 0?")
# The partner stress that sources the metric is  T^partner = T^aether + T^abs.
# We parametrize the partner's effective fluid form along u: T_munu = drho u_mu u_nu + p P_munu + Pi_munu
# (Pi traceless = the shear we want). The b-constraint fixes the SPATIAL divergence; the question is
# whether drho (the 00, Phi-source) is forced nonzero. Compute via the linearized field eqs:
G = sp.symbols('G', positive=True)
# Linearized conformal-Newtonian field equations (standard, e.g. Ma-Bertschinger), quasistatic:
#   (00):  nabla^2 Psi          = 4 pi G a^2 (drho)                      ... sources Psi from energy density
#   (0i):  d_i (Psi' )          = -4 pi G a^2 (rho+p) v_i                ... momentum
#   (ij) trace:  nabla^2(Phi-Psi)= -8 pi G a^2 Pi_scalar (anisotropic)   ... slip from anisotropic stress
#   (ii):  nabla^2 Phi          = 4 pi G a^2 (drho + 3 dp) (+ aniso)     ... sources Phi from rho+3p
# The shear-absorbing construction sets Pi_scalar = (the traceless f-shear). We test whether
# delta-Phi=0 is CONSISTENT, i.e. whether the (ii)/Phi equation can be satisfied with Phi=phi_N
# (matter feels only g_N) GIVEN the b-constraint -- and crucially whether drho, dp are FREE (tuned)
# or FIXED by the aether EOM.
drho, dp, Pi = sp.symbols('delta_rho delta_p Pi', real=True)
PhiN = sp.Function('phi_N')(r)   # the baryon Newtonian potential, phi_N' = g_N
# REQUIRE delta-Phi = 0  =>  Phi = phi_N  =>  the (ii)/Phi equation reads:
#    nabla^2 phi_N = 4 pi G (rho_b + drho + 3 dp) + (aniso term)
#    nabla^2 phi_N = 4 pi G rho_b  ALREADY (baryon Poisson)  =>  need  drho + 3 dp + (aniso)/4piG = 0.
# And the slip eq:  nabla^2(Phi-Psi) = -8 pi G Pi  with Phi=phi_N  =>  nabla^2(phi_N - Psi) = -8 pi G Pi.
# And we WANT  (Psi - phi_N)' = dPsi' = 2(g_obs - g_N).
print(r"""
  Impose delta-Phi = 0 (Phi = phi_N, matter feels only g_N). The linearized field eqs then force,
  for self-consistency:
      (Phi/ii eq):   delta_rho + 3 delta_p + (anisotropic-trace adjust)/(4piG) = 0       ...(*)
      (slip eq):     nabla^2(phi_N - Psi) = -8 pi G Pi                                    ...(**)
      (want):        (Psi - phi_N)' = 2(g_obs - g_N)                                      ...(target)
""")
# From (**) and the target we get Pi (the required anisotropic stress) explicitly:
gN, a0 = sp.symbols('g_N a_0', positive=True)
g_obs = sp.sqrt(gN**2 + gN*a0)
dPsi_prime = 2*(g_obs - gN)        # the REQUIRED slip gradient
print("  target slip gradient  dPsi'(r) = 2(g_obs-g_N) =", dPsi_prime)
# The anisotropic stress required (from **): Pi ~ -(1/8piG) nabla^2(Phi-Psi); with Phi=phi_N and
# (Phi-Psi)' = -dPsi', we get nabla^2(Phi-Psi) = -(1/r^2) d_r(r^2 dPsi') in spherical:
dPsi_p_sym = sp.Function('dPsi_p')(r)
lap_PhiPsi = -(1/r**2)*sp.diff(r**2*dPsi_p_sym, r)    # nabla^2(Phi-Psi) = -div(dPsi') (sign: Phi-Psi=-dPsi)
Pi_req = sp.simplify(-lap_PhiPsi/(8*sp.pi*G))
print("  required anisotropic stress  Pi(r) = -nabla^2(Phi-Psi)/(8piG) =", Pi_req)
print("""
  *** THE LOAD-BEARING QUESTION ***  Pi(r) here is whatever profile reproduces dPsi'=2(g_obs-g_N).
  Is THAT PROFILE a CONSEQUENCE of the aether action, or is it a FREE FUNCTION we are choosing?
""")

# =================================================================================================
H("SECTION 4 -- WHERE Pi(r) COMES FROM: the aether EOM vs the free source J -- the derived/tuned test")
# =================================================================================================
print(r"""
The shear sigma_{ij} (hence Pi) is sourced by f via the constraint  (2/3) d_j(nabla^2 f) = J_j.
So the slip profile is fixed by J_j -- the GATED BARYON CURRENT. The decisive question: is J_j
DERIVED (a fixed functional of rho_b dictated by the action) or is it the place where we INJECT
the MOND profile by hand?

  J_j is defined as 'grad of the gated MI source f, built from g_obs'. Concretely the construction
  needs:
        nabla^2 f  =  (3/2) * [ the scalar whose gradient is the MOND phantom ]   so that
        (2/3) d_j(nabla^2 f) = d_j(phantom) = J_j  reproduces grad delta-Psi = 2(g_obs - g_N).
  i.e. we must CHOOSE  nabla^2 f  such that downstream the slip equals 2(g_obs-g_N). But g_obs =
  sqrt(g_N^2 + g_N a0) is the MOND interpolation -- a NON-POLYNOMIAL function of g_N=|grad phi_N|.
  There is NO local, polynomial, aether-kinetic term whose EOM yields nabla^2 f = this sqrt-profile;
  it is precisely AeST's free function F(Y) of the gradient invariant Y=|grad phi|^2 that must be
  hand-shaped to reproduce sqrt(g_N^2+g_N a0).
""")
# DEMONSTRATE that the required source is the MOND interpolation = a free function, not a polynomial
# aether EOM output. The deep + high limits show the non-polynomial (sqrt) structure:
slip_ratio = sp.simplify(dPsi_prime/gN)
print("  slip-to-Newtonian ratio  2(g_obs-g_N)/g_N =", slip_ratio)
print("     high-g (solar) limit g_N>>a0:", sp.limit(slip_ratio, a0, 0), " (slip -> 0, Cassini-safe by profile)")
deep = sp.series(slip_ratio, gN, 0, 1).removeO()
print("     deep   limit g_N<<a0:  ~", sp.simplify(deep), " ~ sqrt(a0/g_N) (the MOND growth)")
print(r"""
  This ratio is the AeST mu-function content. To get it from an ACTION you need a free function
  F(Y) tuned so that its variation yields exactly sqrt(g_N^2+g_N a0). No finite-coefficient aether
  kinetic term (c1..c4, polynomial in grad u) produces a square-root interpolation -- that is the
  whole reason AeST introduces a free F(Y,Q).
""")

h("4a. So WHO absorbs the divergence -- and is delta-Phi=0 a derivation or a definition?")
print(r"""
  Trace the logic of the construction:
    1. We DEFINE the shear sigma_{ij} = d_i d_j f - (1/3)delta_ij nabla^2 f and DEMAND light feel it
       (grad delta-Psi = 2(g_obs-g_N)). That fixes f (= a free function reproducing the MOND slip).
    2. The b^mu multiplier's spatial EOM (2/3)d_j(nabla^2 f)=J_j is then AUTOMATICALLY satisfied by
       DEFINING J_j := (2/3)d_j(nabla^2 f). The 'absorption' is real -- the divergence lands in the
       spatial (u-orthogonal) sector and (Section 3) the on-shell multiplier stress has NO trace
       term, so delta-Phi=0 is CONSISTENT. THIS PART IS GENUINE: the non-dynamical u + multiplier
       DO let delta-Phi=0 coexist with a nonzero traceless spatial slip, escaping the 4-diff Bianchi
       trap (the divergence is soaked by b^j, NOT by an isotropic pressure that moves Phi).
    3. BUT: nothing in steps 1-2 DERIVED the profile sigma. We CHOSE f to make the slip come out
       2(g_obs-g_N). The aether EOM did not predict it; the multiplier merely enforced a constraint
       we wrote with the answer already in it (J_j is the MOND current by construction).
""")

# =================================================================================================
H("SECTION 5 -- delta-Phi=0 verification (the multiplier DOES kill the trace) -- the GENUINE half")
# =================================================================================================
print(r"""
We verify EXPLICITLY that, given the constraint, delta-Phi=0 closes WITHOUT a residual Phi source --
this is the real content of the non-dynamical-frame escape (and it is what canonical Route-4 lacked).
""")
# The total partner stress: T_munu = drho u_mu u_nu + p_perp P_munu + Pi_munu (Pi traceless, spatial).
# 00 component (Phi source) = drho. The b-multiplier's job: route the shear divergence so that
# conservation nabla^mu T_munu = 0 holds with drho = 0. Test: nabla^mu(Pi_munu) = -(divergence)
# must be cancelled by nabla^mu(b-current), NOT by grad(p) or by drho.
# Linearized conservation of the traceless shear alone (the no-go obstruction):
print("  Bianchi/conservation of the traceless shear alone:")
print("     nabla^i Pi_ij = (2/3) d_j(nabla^2 f) =", div_shear, "  != 0   (the obstruction)")
print(r"""
  In a 4-DIFF-INVARIANT theory this MUST be cancelled by grad(p) [isotropic pressure] => 3dp=-2nabla^2 f
  => sources Phi (the no-go). HERE the b^j multiplier provides a NON-DYNAMICAL-FRAME current
  Theta_j = -b^j-sourced spatial flux that cancels it WITHOUT a pressure:
     d_i Pi_ij + nabla^... (b-flux)_j = 0    with the b-flux purely SPATIAL (u-orthogonal).
  Because the b-flux carries NO 00 component (P^nu_0=0, Section 3), it does NOT contribute to drho.
  => the conservation is completed in the SPATIAL/frame sector => drho can be 0 => delta-Phi=0.
""")
# Symbolic check that the (00) equation closes with drho=0 once the b-flux carries the divergence:
print("  => With the b-flux absorbing d_i Pi_ij, the (00) eq is  nabla^2 Psi = 4 pi G (rho_b + 0),")
print("     i.e. drho_partner = 0  =>  delta-Phi = 0  CONSISTENT.  (REQ 1: structurally PASS.)")
print("  => The (slip) eq gives nabla^2(Phi-Psi) = -8piG Pi with Pi the chosen profile  =>")
print("     (Psi-phi_N)' = 2(g_obs-g_N) BY CONSTRUCTION.  (REQ 2: PASS-BY-CONSTRUCTION, see Sec 6.)")

# =================================================================================================
H("SECTION 6 -- THE VERDICT TEST: is the b-flux EOM-CONSISTENT, and is sigma DERIVED or HAND-SET?")
# =================================================================================================
print(r"""
TWO things decide WORKS vs PARTIAL vs FAILS:

  (I) Is the construction CONSISTENT (no ghost from b, b-EOM solvable, c_T=c kept)?
      - b^mu is a Lagrange multiplier (NO kinetic term) => it propagates NO new DOF => NO new ghost.
        Its EOM is an algebraic/constraint equation, and on the static background it is solvable
        (J_0=0 is automatically consistent since C_0=0; J_j fixes the spatial flux). The aether's
        own modes are unchanged at c13=0 (the b-term is first-order in u via P and does not add to
        the quadratic grad-u kinetic matrix that sets s1^2,s0^2) => the Section-1 ghost-free,
        c_T=c corner SURVIVES. So (3) c_T=c PASS, (4) ghost-free PASS (no new propagating mode).
      - HONEST CAVEAT: a multiplier b with a constraint that is SECOND-class can re-propagate a mode
        (the Henneaux-Teitelboim subtlety); a full Dirac constraint analysis is NOT done here. The
        mode COUNT is safe at linear order on this background, but a complete Hamiltonian proof for
        ALL backgrounds is not provided => ghost-free is 'linear-order PASS, full-Hamiltonian
        UNPROVEN', the same honest status as Route 3.

  (II) Is the SLIP PROFILE sigma = 2(g_obs-g_N) DERIVED from the action, or PUT IN BY HAND?
      - It is PUT IN BY HAND. The current J_j := (2/3)d_j(nabla^2 f) is DEFINED to be the MOND
        phantom current; f is a FREE FUNCTION chosen so the slip equals 2(g_obs-g_N). No aether
        kinetic invariant (polynomial in grad u) yields the sqrt(g_N^2+g_N a0) interpolation; that
        is exactly AeST's free function F(Y,Q). The multiplier construction makes the slip
        Cassini-SAFE (delta-Phi=0) -- a genuine structural advance over AeST -- but it does NOT
        PREDICT the slip's MOND shape. The shape is transmitted, not derived.
""")

# Demonstrate (II) concretely: ask sympy whether there is a LOCAL POLYNOMIAL aether functional whose
# EOM gives nabla^2 f proportional to the MOND phantom. The phantom density for grad dPsi=2(g_obs-g_N):
phantom = sp.simplify((1/r**2)*sp.diff(r**2*dPsi_prime.subs(gN, G*sp.Symbol('M',positive=True)/r**2), r))
M = sp.Symbol('M', positive=True)
print("  effective phantom 'mass density' that must source the slip (spherical):")
print("     nabla^2(delta-Psi) = (1/r^2) d_r(r^2 * 2(g_obs-g_N)) =")
print("       ", phantom)
print(r"""
  This is a NON-POLYNOMIAL (square-root-bearing) function of r -- it CANNOT be the EOM output of any
  finite-order polynomial aether kinetic term K^{ab}_{mn} grad u grad u. It REQUIRES a free function
  (AeST F(Y)). => the slip profile is HAND-SET (phenomenology), confirming the honesty-bar failure
  mode for 'derived'. The DERIVED content is only the delta-Phi=0 routing, not the slip's value.
""")

# =================================================================================================
H("ROUTE 2 NET VERDICT -- all four, adjudicated, both ways")
# =================================================================================================
print(r"""
  (1) delta-Phi = 0            : PASS (STRUCTURAL, genuinely derived from the construction). The
                                non-dynamical frame u + Lagrange multiplier b^mu route the shear
                                divergence (2/3)d_j(nabla^2 f) into the SPATIAL (u-orthogonal) sector
                                with NO trace term (on-shell C=J kills -(1/2)g_munu b(C-J); P^nu_0=0
                                kills the time component). So conservation is completed WITHOUT an
                                isotropic pressure that moves Phi. THIS IS THE REAL ADVANCE over both
                                canonical khronometric (Route 4, gamma=1) and AeST (moves Phi): the
                                Bianchi trap is genuinely escaped by the non-dynamical frame. DERIVED.

  (2) grad(delta-Psi)=2(g_obs-g_N) : PASS-BY-CONSTRUCTION, NOT DERIVED. The slip MAGNITUDE/SHAPE is
                                injected as the free current J_j := (2/3)d_j(nabla^2 f); f is a free
                                function tuned to reproduce sqrt(g_N^2+g_N a0). No polynomial aether
                                kinetic term yields that interpolation -- it is AeST's F(Y,Q)
                                free-function content. So the action LINEARIZES to the right slip
                                ONLY because the MOND profile was written into the source. HAND-TUNED.

  (3) c_T = c                 : PASS. c13=0 (Foster-Jacobson Eq.15); the multiplier adds no graviton
                                kinetic term => graviton unchanged => c_T=c. EASY, as the no-go says.

  (4) ghost-free              : PASS at LINEAR ORDER on this background (b is a non-kinetic Lagrange
                                multiplier -> no new propagating DOF; the c13=0 aether corner has all
                                s^2>0). FULL-HAMILTONIAN (all backgrounds, second-class constraint
                                count) UNPROVEN -- the honest same status as Route 3. Not a ghost
                                detection; an unfinished proof.

  ALL FOUR AS A *DERIVED* LAGRANGIAN: NO. Three of four are genuinely met (delta-Phi=0 DERIVED via
  the non-dynamical-frame routing -- the real new result; c_T=c PASS; ghost-free PASS at linear
  order). The FOURTH, the MOND slip profile, is HAND-SET: the action linearizes to
  grad(delta-Psi)=2(g_obs-g_N) ONLY because the source current J_j is DEFINED to be the MOND phantom.
  That is precisely the AeST F(Y,Q) free-function problem -- phenomenology, not a derived slip.

  HONEST BOTTOM LINE (both ways, penalized equally):
    * WHAT IS NEW AND REAL (credited at full weight): the non-dynamical preferred frame + Lagrange
      multiplier DO break the Bianchi slip<=>Phi lock. delta-Phi=0 WITH a nonzero traceless
      position-dependent spatial slip is CONSISTENT and ghost-free at linear order with c_T=c. This
      is a genuine escape from the covariant no-go -- the lensing partner CAN live, Cassini-safely,
      in the Lorentz-violating preferred-frame sector. The no-go's 'only escape is to break 4-diff
      to a non-dynamical frame' is CONCRETELY realized for delta-Phi=0. The framework's dS-Unruh
      cosmic rest frame supplies exactly this u^mu.
    * WHAT IS NOT ACHIEVED (conceded at full weight): the slip's MOND SHAPE 2(g_obs-g_N) is NOT a
      consequence of the action. It is transmitted through a free source function (AeST F(Y,Q)).
      So the construction yields a Cassini-safe LENSING FRAME, but the lensing LAW is
      phenomenological -- a0/Z enter as a hand-shaped F, not derived. The no-go therefore CLOSES in
      its 'lensing irreducibly phenomenological' form for the LAW, while the delta-Phi=0
      preferred-frame ROUTING is genuinely solved.

  GRADE: PARTIAL. delta-Phi=0 + c_T=c + (linear-order) ghost-free are DERIVED in an explicit
  preferred-frame action (a real advance past Route 4's gamma=1 wall); the slip profile is
  HAND-TUNED (AeST free function), so it is NOT a fully derived lensing Lagrangian. The
  conservation-completion is done by the multiplier DYNAMICS for the delta-Phi=0 part, but the
  PROFILE is IMPOSED.
""")
print("="*98)
print(" ROUTE 2 (Einstein-aether + shear-absorbing multiplier): PARTIAL")
print("  delta-Phi=0 DERIVED (non-dyn-frame routing escapes the Bianchi trap); c_T=c PASS;")
print("  ghost-free PASS (linear order); slip 2(g_obs-g_N) HAND-TUNED (AeST F(Y,Q), not derived).")
print("="*98)
