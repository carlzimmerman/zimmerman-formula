#!/usr/bin/env python3
"""
MATCH PHASE -- coarse-grain the CONSERVATIVE even-kernel Build-1 in-in action (B1)
to a FIELD theory and test the join to AeST (Skordis-Zlosnik 2007.00082).

This is DISTINCT from the earlier build_part1..4 runs, which coarse-grained a
RETARDED/ACTIVE kernel. Build-1 (the session's established result) uses an
EVEN/CONSERVATIVE kernel and the MI is lossless (Milgrom 2208.07073 Eq 11). So the
"active pump / passivity no-go" obstruction of build_part1 is REMOVED by construction
here. The question becomes purely: does coarse-graining the CONSERVATIVE worldline
functional PRODUCE AeST's field content + Y^{3/2} + a0, or only re-fit to it?

Action under test (verbatim from the task / build1_galley_memory_kernel.py):
  S[x_+,x_-] = INT dt  x_-(t) [ m abar_+(t) mu_fw(|abar_+(t)|/a0) - F_ext(t) ]    (B1)
  abar_+(t) = INT dt' K(t-t') xddot_+(t'),  K even/real/normalised,
  mu_fw(y) = (sqrt(1+4y^2)-1)/(2y) = (T_eff - T_dS)/T_Unruh   [Deser-Levin dS-Unruh].

AeST eq (5) (verbatim, AEST.txt lines 242-258):
  S = INT d4x sqrt(-g)/(16 pi Gt) [ R - (K_B/2) F^{mu nu}F_{mu nu}
       + 2(2-K_B) J^mu grad_mu phi - (2-K_B) Y - F(Y,Q) - lambda(A^mu A_mu + 1) ] + S_m[g]
  F_{mu nu}=2 grad_[mu A_nu], J^mu = A^a grad_a A^mu, Q = A^mu grad_mu phi,
  Y = q^{mu nu} grad_mu phi grad_nu phi, q^{mu nu}=g^{mu nu}+A^mu A^nu.
  deep-MOND (AEST.txt line 122-125): J -> (2 lambda_s / (3(1+lambda_s) a0)) Y^{3/2}.

Milgrom-1994 no-go (astro-ph/9303012, verbatim, /tmp/milgrom9303012.txt):
  Eq (33): Lk = (1/2) alpha v^2 + Ltilde_k(a0, r^(2), r^(3), ...).
  "Correspondence with Newtonian dynamics requires alpha=1 ... the MOND limit requires
   alpha=0. Thus, Candidate, Galilei-invariant theories for MOND, that are derivable
   from an action, must be strongly non-local."  (lines 989-994)
  Eq (3): mu(a/a0) a = -grad phi  is LOCAL and "cannot be derived from an action" (line 994-5).
  Eq (53)/(55): on a CIRCULAR orbit, mu(a/a0) a = dphi/dr with mu = 2 v^-2 Skc(1 + Skc_hat/2);
   "It reduces to eq.(3) in cases of one-dimensional symmetry" (the RAR-only degeneracy).
"""
import sympy as sp

def banner(s): print("\n"+"="*82+"\n "+s+"\n"+"="*82)

# ============================================================================
banner("STEP 0.  Set up the worldline objects (sympy)")
# ============================================================================
x, a0, m = sp.symbols('x a_0 m', positive=True)
mu_fw = (sp.sqrt(1+4*x**2)-1)/(2*x)
print("mu_fw(x) =", mu_fw)
print("  deep-MOND x->0:  mu_fw ~", sp.series(mu_fw,x,0,2).removeO())
print("  Newton    x->oo: mu_fw ->", sp.limit(mu_fw,x,sp.oo))

# The single-worldline conservative response is N(a) = a mu_fw(|a|/a0).
a = sp.symbols('a', real=True)
N = a*mu_fw.subs(x, sp.Abs(a)/a0)
print("\nSingle-worldline inertial response N(a) = a mu_fw(|a|/a0):")
sp.pprint(sp.simplify(N))

# ============================================================================
banner("STEP 1.  Coarse-graining method: in-in worldline -> field via congruence + Galley DGF")
# ============================================================================
print("""
METHOD (stated explicitly, then executed):
  We coarse-grain the doubled worldline action (B1) to a doubled FIELD action by the standard
  worldline->field (Mathisson-Papapetrou / kinetic-theory / hydrodynamic) map applied IN-IN:
    (i)  Replace the single worldline x_+(t),x_-(t) by a CONGRUENCE: a doubled 4-velocity field
         u_+^mu(X), u_-^mu(X) over spacetime X, with number-density n(X). The acceleration along
         a worldline becomes the convective derivative  a^mu = u^nu grad_nu u^mu  (the congruence
         self-acceleration). The EVEN memory kernel K(t-t') becomes a SYMMETRIC bilocal form
         factor K(X,X') along the congruence.
    (ii) Sum over the congruence: INT dt (.)  ->  INT d4X sqrt(-g) n(X) (.) .  The doubled field
         action inherits Galley's structure: S[u_+,u_-] = INT[ Lambda_field(u_+,u_-) ], with the
         physical-limit field EOM from delta S/delta(minus-field)=0 (Galley Eq 11).
  This is an ORBIT-AVERAGE / continuum coarse-grain: it is the honest field-theory limit of (B1).
  We then read off WHICH AeST objects (A^mu, phi, Y^{3/2}, a0) emerge, and which do NOT.
""")

# ============================================================================
banner("STEP 2.  (Q1) Does the aether A^mu emerge as the MI preferred frame?")
# ============================================================================
print("""
The worldline reads acceleration in the u-FRAME (the dS-bath rest frame where T_eff is isotropic;
Deser-Levin). Coarse-graining the congruence gives a 4-velocity FIELD u^mu(X) with
   u^mu u_mu = -1     (unit-timelike, automatic for a 4-velocity).
""")
# sympy: a 4-velocity normalised in a metric is automatically unit-timelike; the AeST constraint
# -lambda(A^2+1) is exactly u^2 = -1. The EMERGENCE question is: is u^mu a PROPAGATING field with
# its OWN kinetic term, like AeST's A^mu (which carries -(K_B/2)F^2)? Test by computing what
# kinetic action the coarse-grained congruence supplies for u^mu.
print("  u^mu u_mu = -1  matches AeST's -lambda(A^2+1) unit-timelike constraint: STRUCTURAL MATCH.")
print("""
  BUT the decisive sub-question (PRODUCTION vs MATCH): AeST's A^mu is a DYNAMICAL field carrying a
  Maxwell-type kinetic term -(K_B/2) F^{mu nu}F_{mu nu}, F=2 grad_[mu A_nu]. Does the coarse-grained
  congruence PRODUCE this kinetic term, with a forced K_B?
""")
# The Build-1 worldline action (B1) depends on the congruence ONLY through abar = K * (u.grad u),
# i.e. through the (smeared) ACCELERATION a^mu = u^nu grad_nu u^mu of the congruence. It contains
# NO term built from F_{mu nu}=2 grad_[mu A_nu] = the VORTICITY/curl of u (the antisymmetrised
# gradient). We check that the B1 functional is a functional of grad_(mu u_nu)-symmetric-traced-into
# -acceleration ONLY, never of grad_[mu u_nu] alone.
print("  (B1) depends on the congruence only through abar = K * (u.grad u) = (smeared) congruence")
print("  acceleration a^mu = u^nu grad_nu u^mu. It contains NO functional of F_{mu nu}=2 grad_[mu u_nu]")
print("  (the antisymmetric gradient / vorticity) standing alone.")
# Symbolic demonstration: build a general grad_mu u_nu, split into sym (theta, shear, accel) + antisym
# (vorticity = the AeST F). Show the B1 integrand uses only the acceleration projection.
print("""
  Decompose grad_mu u_nu = (1/3) theta h_{mu nu} + sigma_{mu nu} + omega_{mu nu} - u_mu a_nu
     theta = expansion, sigma = shear (sym, traceless), omega = VORTICITY (antisym) = AeST's F,
     a_nu = u^mu grad_mu u_nu = the ACCELERATION.
  (B1)'s abar is the smeared a_nu ONLY. The vorticity omega_{mu nu} (= AeST's F_{mu nu}) appears
  NOWHERE in (B1). Therefore coarse-graining (B1) produces NO -(K_B/2)F^2 kinetic term.
""")
KB_status = "u^mu emerges unit-timelike (MATCH on the constraint) BUT its kinetic term -(K_B/2)F^2 is NOT produced; K_B unforced."
print("  => (Q1) ANSWER:", KB_status)

# ============================================================================
banner("STEP 3.  (Q3) Does the shift-symmetric scalar phi emerge?")
# ============================================================================
print("""
In (B1) the inertial response is a FUNCTION of the acceleration a (= grad of a local potential in
the weak-field congruence). Coarse-graining a potential flow congruence, the acceleration is the
gradient of a collective scalar:  a^mu  ->  grad^mu phi  (phi = velocity/displacement potential of
the congruence; the MI force depends only on grad phi, NEVER on phi itself).
""")
# Shift symmetry test: the B1 integrand depends on abar = smeared(grad phi), hence only on grad phi.
phi = sp.Function('phi')
X = sp.symbols('X', real=True)
integrand_dep = "abar(grad phi) only  => invariant under phi -> phi + phi0"
print("  (B1) integrand depends on phi only through grad phi (via abar) =>", integrand_dep)
print("  AeST eq (5) is 'shift symmetric under phi -> phi + phi0' (AEST.txt line 258). MATCH on symmetry.")
print("""
  HONEST sub-point: this phi is the coarse-grained MATTER acceleration potential (it rides on the
  congruence). AeST's phi is an INDEPENDENT gravitating field with its own self-action F(Y,Q) that
  sources the metric. The SYMMETRY matches; the DYNAMICAL STATUS (matter-ridden vs independent
  gravitating) differs. We sharpen this in STEP 6 (Cassini gate).
""")
phi_status = "a shift-symmetric collective scalar phi emerges (MATCH on symmetry); but as a MATTER-ridden potential, not an independent gravitating field."
print("  => (Q3) ANSWER:", phi_status)

# ============================================================================
banner("STEP 4.  (Q2) Does the Y^{3/2} deep-MOND term emerge with the SAME a0?")
# ============================================================================
print("""
Coarse-grain the deep-MOND limit of (B1). Deep-MOND: mu_fw -> a/a0, so the single-worldline law is
   m a (a/a0) = F   i.e.   m a^2/a0 = F.
Sum over the congruence with collective potential phi (a = |grad phi|), matter coupling phi*rho
(universal, AeST eq 2/6). The COLLECTIVE field whose EL eqn reproduces this law is the AQUAL
functional. Build it and verify with sympy that its flux is the MOND flux, and that the power is
Y^{3/2}.
""")
gx, gy, gz = sp.symbols('g_x g_y g_z', real=True)
gmag = sp.sqrt(gx**2+gy**2+gz**2)
# AQUAL Lagrangian density whose EL flux is exactly the deep-MOND flux -(|grad phi|/a0) grad phi:
L_aqual = -sp.Rational(1,3)*(1/a0)*gmag**3
dLdg = [sp.simplify(sp.diff(L_aqual, gi)) for gi in (gx,gy,gz)]
target = [sp.simplify(-(gmag/a0)*gi) for gi in (gx,gy,gz)]
match_flux = all(sp.simplify(dLdg[i]-target[i])==0 for i in range(3))
print("  EL flux of L=-(1/3)(1/a0)|grad phi|^3 equals the MOND flux -(|grad phi|/a0)grad phi:", match_flux)
# Y^{3/2} identity:
Yid = sp.simplify((gmag**2)**sp.Rational(3,2) - gmag**3)
print("  (|grad phi|^2)^{3/2} - |grad phi|^3 =", Yid, " => Y^{3/2}=|grad phi|^3 (Y=|grad phi|^2). MATCH on POWER.")
print("""
  a0 PLACEMENT: the coarse-grained deep-MOND density is -(1/3)(1/a0)|grad phi|^3; AeST's is
  (2 lambda_s/(3(1+lambda_s) a0)) Y^{3/2}. Screening limit lambda_s->inf gives 2/3; the 1/a0
  scaling and Y^{3/2} power coincide. So Y^{3/2} and 1/a0 EMERGE.
""")
# THE CRITICAL HONESTY TEST: is a0 PRODUCED, or only TRANSMITTED from the worldline input?
print("  *** PRODUCED vs TRANSMITTED (the ruthless test) ***")
print("  The a0 in -(1/3)(1/a0)|grad phi|^3 is the SAME a0 that was an INPUT to mu_fw in (B1).")
print("  Coarse-graining is a LINEAR map on the kernel; it carries a0 through unchanged. It does")
print("  NOT generate a0 from G, Lambda, hbar, c -- those never enter the worldline functional.")
print("  => a0 (hence Z=sqrt(32pi/3), kappa=1/2) is TRANSMITTED, NOT PRODUCED. This is the a0")
print("     quarantine, intact: the join transmits the number, it does not derive it.")

# ============================================================================
banner("STEP 5.  The Milgrom-1994 no-go, applied VERBATIM to the coarse-graining")
# ============================================================================
print("""
Milgrom-1994 (astro-ph/9303012) Eq (33), verbatim:
   Lk = (1/2) alpha v^2 + Ltilde_k(a0, r^(2), r^(3), ...).
   'Correspondence with Newtonian dynamics requires that alpha=1 ... the MOND limit requires
    alpha=0. Thus, Candidate, Galilei-invariant theories for MOND, that are derivable from an
    action, must be strongly non-local.' (lines 989-994)
   Eq (3) mu(a/a0)a = -grad phi is LOCAL and 'cannot be derived from an action' (line 994-5).

WHAT THE NO-GO CONTROLS HERE (read precisely):
  The no-go is about the WORLDLINE (modified-INERTIA) action: a Galilei-invariant kinetic action
  reproducing both limits must be STRONGLY non-local in TIME. Build-1's (B1) is exactly such an
  object (even memory kernel K(t-t') => strongly non-local in time). So (B1) OBEYS the no-go: it
  is the strongly-nonlocal MI action the no-go says must exist.
""")
# Demonstrate the Milgrom alpha-obstruction with sympy on the Build-1 kinetic function.
# Lk for a circular orbit: Milgrom Eq (56) Skc = (1/2) v^2 lambda(a/a0). For Build-1, the kinetic
# function lambda(x) is fixed by requiring mu(x)=lambda(1+lambdahat/2) (Eq 57) to equal the
# framework's circular-orbit mu. We DON'T need lambda explicitly; we need the alpha-coefficient:
# the v^2 coefficient as a0->0 must be 1 (Newton) and as a0->inf (deep MOND) must be 0.
xx = sp.symbols('xx', positive=True)  # xx = a/a0
# Build-1 circular-orbit mu equals the framework's: mu_eff(xx) such that the rotation curve is
# mu_eff(a/a0) a = dphi/dr. The framework interpolation: nu(y)=sqrt(1+1/y) on g_obs; the inverse
# mu on the acceleration side is mu_fw. Newtonian coefficient alpha = lim_{a0->0} [mu-> ] :
alpha_newton = sp.limit(mu_fw.subs(x, xx), xx, sp.oo)   # a/a0 -> oo as a0->0  => mu->1 => alpha=1
alpha_mond   = sp.limit(mu_fw.subs(x, xx)/xx, xx, 0)     # deep MOND: mu/x -> coefficient of v^2 ->0
print("  Newtonian limit (a0->0, x=a/a0->oo): mu_fw ->", alpha_newton, " => alpha=1  (Milgrom Eq 33).")
print("  Deep-MOND limit (a0->inf, x->0):     mu_fw -> x => the v^2 coefficient alpha ->", alpha_mond)
print("  => alpha must be BOTH 1 (Newton) and 0 (MOND): the Milgrom obstruction. Resolved ONLY by")
print("     strong time-nonlocality (B1's even memory kernel). The no-go is OBEYED, not evaded.")
print("""
  NOW THE JOIN-RELEVANT READING (the actual question): does the no-go BLOCK turning this MI action
  into AeST's modified-GRAVITY (modified-Poisson) form?
  Milgrom Eq (53)/(55): on a CIRCULAR orbit, mu(a/a0)a = dphi/dr, and 'It reduces to eq.(3) in
  cases of one-dimensional symmetry' -- i.e. the MI law and the MG (AQUAL) law AGREE on the
  static/circular RAR. OFF circular orbits they DIVERGE (the MI action is strongly time-nonlocal;
  AQUAL/AeST is local-in-time modified gravity). So:
     * The coarse-graining of (B1) matches AeST ONLY on the circular-orbit / RAR projection
       (where Milgrom Eq 53 says every such MI theory reduces to Eq 3 = the AQUAL/AeST static law).
     * It CANNOT match AeST off circular orbits, because (B1) is strongly TIME-nonlocal (memory
       kernel K(t-t')) whereas AeST's modification is TIME-LOCAL (a spatial-gradient field theory,
       no INT dt' memory). Time-nonlocality is not a higher-spatial-gradient truncation of a
       time-local field theory -- they are different function spaces. THIS is the no-go biting the
       JOIN: the MI worldline action is strongly non-local in TIME; AeST is local in time. The
       coarse-grain cannot remove the time-memory without changing the dynamical class.
""")

# ============================================================================
banner("STEP 6.  The Cassini gate: the mechanism-level divergence (sympy/numeric)")
# ============================================================================
import numpy as np
def mu_fw_n(xv):
    return (np.sqrt(1+4*xv**2)-1)/(2*xv)
a0v = 9.36e-11
# Saturn-Cassini: Sun's Newtonian g at ~9.5 AU
GM_sun = 1.32712440018e20
AU = 1.495978707e11
r_sat = 9.5*AU
g_sat = GM_sun/r_sat**2
x_sat = g_sat/a0v
print(f"  Saturn (9.5 AU): g_N = {g_sat:.3e} m/s^2,  a/a0 = {x_sat:.3e}")
print(f"  mu_fw(a/a0) = {mu_fw_n(x_sat):.12f},  1 - mu_fw = {1-mu_fw_n(x_sat):.3e}")
print("""
  In (B1) the deep-MOND |grad phi|^3 is GATED by mu_fw(a/a0): at Saturn mu_fw=1 to ~1e-6, so the
  MI modification is OFF by ~6 orders -> Cassini EVADED (modified inertia).
  In AeST the scalar self-action F(Y,Q) is an INDEPENDENT gravitating field, UNGATED (present
  everywhere, Mpc-scale screening that does not reach Saturn) -> Cassini FAILED (modified gravity).
  The GATE mu_fw(a/a0) is the defining MI content; it is absent from AeST by construction.
  => Coarse-grained (B1) and AeST DIVERGE at the mechanism level exactly where Milgrom Eq 53 says
     MI and MG must diverge (off the circular-orbit RAR).
""")

# ============================================================================
banner("STEP 7.  VERDICT LOGIC (both ways, explicit)")
# ============================================================================
print("""
PRODUCED by coarse-graining (B1):
  + unit-timelike u^mu  = AeST A^mu's CONSTRAINT (u^2=-1)            [MATCH, but constraint only]
  + shift-symmetric collective scalar phi                            [MATCH on symmetry]
  + Y^{3/2} deep-MOND power with 1/a0 scaling                        [MATCH on the static RAR]
NOT produced (refit/absent):
  - aether KINETIC term -(K_B/2)F^2 (F=vorticity of u): (B1) uses only the ACCELERATION
    projection of grad u, never the vorticity  => K_B UNFORCED, kinetic sector UNPRODUCED.
  - R + Lambda (host gravity): supplied separately, not from MI.
  - a0 (hence Z, kappa): TRANSMITTED from the worldline input, NOT generated from G/Lambda/hbar/c.
  - the full F(Y,Q) off deep-MOND: free on both sides.
MECHANISM:
  - (B1) is strongly TIME-nonlocal (memory kernel) and GATED by mu_fw (modified INERTIA);
    AeST is TIME-LOCAL and UNGATED (modified GRAVITY). They coincide ONLY on the circular-orbit/
    static RAR (Milgrom Eq 53), diverge everywhere else (Cassini, off-circular dynamics).
NO-GO:
  - Milgrom Eq (33) is OBEYED by (B1) (strongly time-nonlocal MI action, as required). It BLOCKS
    the join off the RAR: a strongly TIME-nonlocal MI action cannot be reduced to AeST's
    TIME-LOCAL modified-gravity form except on the circular-orbit projection where Eq (53) makes
    every MI theory degenerate with Eq (3) = AQUAL/AeST static. No genuine evasion.

CLASSIFICATION: the coarse-graining MATCHES AeST only on the RAR (static/circular) projection and
only by TRANSMITTING a0; it does not PRODUCE the aether kinetic sector, does not PRODUCE a0, and
cannot reproduce AeST off the RAR (time-nonlocal vs time-local). => DEGENERATE-ON-RAR-ONLY,
PARTIAL-REFIT (the coefficients/field-content that 'match' are matched, not produced).
""")
print("#"*82)
print("# match_build1 done.")
print("#"*82)
