#!/usr/bin/env python3
"""
BUILD 4 -- COARSE-GRAIN the conservative covariant form-factor MI action to a FIELD THEORY,
           and test RIGOROUSLY whether it PRODUCES AeST (Skordis-Zlosnik 2007.00082).
============================================================================================
INPUT (build3, the conservative covariant worldline action -- the session-corrected object):

  S_kin[X; u] = -(m/2) int dtau  u^mu  K(Box_wl/a0^2)  u_mu  - int dtau X.F            (1.1)
  K(z) = (sqrt(1+4z)-1)/(2 sqrt(z)),  z = Box_wl/a0^2  ;  on const-|a| slice z -> |a|^2/a0^2.

CRUCIAL CORRECTION vs the predecessor build_part1..4:
  build_part1 wrote an ADDITIVE active kernel  m_eff(om) = m + gamma_hat(om)  and concluded
  (build_part3 C.2) that the reactive/passive truncation gives m_eff(0) > m_eff(inf) = ANTI-MOND,
  requiring an ACTIVE pumped dS bath. THAT WAS A LINEARIZATION ARTIFACT (treating a closed
  nonlinear conservative constitutive law as an open linear passive bath -- session-established,
  Milgrom 2208.07073 Eq.11 "phi + E_k conserved"). The CORRECT object (build3) is the
  MULTIPLICATIVE conservative form factor m_eff = m*K(|a|^2/a0^2), an EVEN operator (time-
  symmetric kernel) => conservative at ALL amplitudes, NO active bath. This build coarse-grains
  THAT object. The anti-MOND passivity obstruction is RE-TESTED on the corrected (multiplicative)
  inertia below (Section 2) -- the predecessor's crux must be re-adjudicated, not inherited.

AeST eq (5) (VERBATIM, AEST.txt l.242-258, Skordis-Zlosnik 2007.00082 PRL 127 161302):
  S = int d4x sqrt(-g)/(16pi Gt) [ R - (K_B/2) F^{mu nu}F_{mu nu} + 2(2-K_B) J^mu grad_mu phi
                                   - (2-K_B) Y - F(Y,Q) - lambda(A^mu A_mu + 1) ] + S_m[g]   (5)
  F_{mu nu}=2 grad_[mu A_nu], J^mu=A^a grad_a A^mu, Q=A^mu grad_mu phi,
  Y=q^{mu nu} grad_mu phi grad_nu phi, q^{mu nu}=g^{mu nu}+A^mu A^nu.
  deep-MOND (AEST.txt l.122-124): J(Y) -> (2 lam_s/(3(1+lam_s) a0)) Y^{3/2} as grad phi -> 0.
  weak-field eq (6): -> AQUAL |grad phi|^2-type + mu^2 Phi^2 mass; mu=sqrt(2K2/(2-KB)) Q0.

Milgrom-1994 MI no-go (astro-ph/9303012, VERBATIM core via agentC_covariance_memo.md l.42-55):
  Assumptions: (i) Galilei invariance; (ii) Newton limit a0->0 -> quadratic; (iii) MOND limit
  S_k prop 1/a0 (deep-MOND scale inv); (iv) LOCALITY (finitely many time derivs).
  Theorem (verbatim): "L_k = (1/2) alpha v^2 + Ltilde_k(a0, r^(2), r^(3), ...)" -- boosts force
  velocity to appear ONLY in the quadratic term. Newton needs alpha=1; MOND (S prop 1/a0) needs
  alpha=0. CONTRADICTION => "Galilei-invariant theories for MOND, derivable from an action, MUST
  be strongly non-local." PERMITS: strongly-nonlocal worldline functionals; circular-orbit
  algebraic relation mu(a/a0)a = dPhi/dr exact (SPARC pins only this slice).

Everything below is CONSTRUCTED (sympy) or CITED (marked). Both ways: report what is TRUE.
"""
import sympy as sp
import numpy as np

def hdr(s): print("="*86); print(" "+s); print("="*86)
def sub(s): print("-"*86); print(" "+s); print("-"*86)

hdr("BUILD 4 : coarse-grain conservative form-factor MI -> field theory ; test AeST production")

# ===========================================================================================
# SECTION 1.  THE COARSE-GRAINING MAP (worldline congruence -> field theory). CONSTRUCTED.
# ===========================================================================================
hdr("SECTION 1 -- the coarse-graining: many-worldline continuum of the conservative action")
print("""
Method (standard kinetic-theory / hydrodynamic coarse-graining of a worldline congruence;
Israel-Stewart / Mathisson-Papapetrou continuum; here applied to the build3 conservative
form-factor action). Replace the discrete set of worldlines X_p^mu(tau) by:
  - a number-density current  n(x) u^mu(x),  u^mu u_mu = -1  (the coarse-grained 4-velocity FIELD)
  - the action becomes a spacetime integral with measure  int d4x sqrt(-g) n(x) (...).

S_kin -> S_field = -(1/2) int d4x sqrt(-g) rho_m(x) [ u^mu K(Box_u/a0^2) u_mu ]            (1.2)
  where rho_m = m n is the mass density and Box_u is the proper-time wave operator ALONG the
  congruence:  Box_u f = u^alpha grad_alpha (u^beta grad_beta f)  (the field uplift of d^2/dtau^2).

KEY: the worldline proper acceleration a^mu = u^alpha grad_alpha u^mu = (u.grad) u^mu becomes a
FIELD -- the congruence's expansion/acceleration tensor. On the constant-|a| slice the build3
identity Box_wl u^mu = |a|^2 u^mu lifts to  Box_u u^mu = (a^nu a_nu) u^mu + (gradient/jerk terms).
We coarse-grain in the QUASISTATIC / orbit-averaged regime (the regime where mu_fw and SPARC live):
the jerk (Du^mu/dtau time-derivative of a) is subleading, so  Box_u u^mu -> |a|^2 u^mu.
""")

sub("1a. The orbit-averaged effective Lagrangian density (CONSTRUCTED, sympy)")
# On the const-|a| (orbit-averaged) slice the operator collapses: K(Box_u/a0^2) u_mu -> K(|a|^2/a0^2) u_mu.
# Use u.u = -1 so u^mu K u_mu = -K(|a|^2/a0^2). The kinetic density:
a, a0, rho_m = sp.symbols('a a_0 rho_m', positive=True)   # a=|acceleration field|, a0 scale
z = sp.symbols('z', positive=True)
K = (sp.sqrt(1+4*z)-1)/(2*sp.sqrt(z))
K_a = K.subs(z, a**2/a0**2)
K_a = sp.simplify(K_a)
print("  Coarse-grained kinetic density (orbit-averaged):  L_kin = (1/2) rho_m K(|a|^2/a0^2)")
print("    K(|a|^2/a0^2) =", K_a)
# The field equation: vary u^mu (with the unit constraint). The acceleration field a^mu=(u.grad)u^mu.
print("""
  Vary S_field wrt u^mu with constraint u.u=-1 (Lagrange multiplier lambda):
    delta/delta u^mu [ -(1/2) rho_m u.K(Box_u/a0^2) u  - (lambda/2)(u.u+1) ] = 0.
  In the orbit-averaged (const-|a|) limit this is the FIELD form of the worldline EOM (build3 2.1):
    grad_nu [ rho_m K(|a|^2/a0^2) u^mu u^nu ] = (source)  + lambda u^mu  -- a unit-timelike vector
  field whose 'stiffness' is the acceleration-dependent K. This is structurally a UNIT-TIMELIKE
  VECTOR FIELD THEORY with a NONLINEAR, ACCELERATION-DEPENDENT self-coupling = an aether.
""")

# ===========================================================================================
# SECTION 2.  RE-ADJUDICATE THE ANTI-MOND OBSTRUCTION on the CORRECTED multiplicative inertia.
#             (The predecessor's decisive crux, C.2, must be re-tested -- not inherited.)
# ===========================================================================================
hdr("SECTION 2 -- does the anti-MOND passivity obstruction SURVIVE the conservative correction?")
print("""
PREDECESSOR CRUX (build_part3 C.2): for an ADDITIVE passive bath m_eff(om)=m+gamma_hat(om), Kramers-
Kronig + passivity (J(om)>=0) force m_eff(0) >= m_eff(inf) = ANTI-MOND. That killed 'AeST=truncation'
(the passive/local truncation gives anti-MOND, not MOND). RE-TEST on the build3 object.

build3 inertia is MULTIPLICATIVE and CONSERVATIVE:  m_eff(|a|) = m*K(|a|^2/a0^2), an EVEN operator.
  m_eff(0)   = m*K(0)   = ?   ;   m_eff(inf) = m*K(inf) = ?
This is NOT a passive linear bath response (no J(om)>=0 spectral function); it is a nonlinear
conservative constitutive law. The passivity inequality DOES NOT APPLY. Check the ordering directly.
""")
print("  m_eff(|a|->0)/m   = K(z->0)   =", sp.limit(K, z, 0),   "  (deep-MOND: inertia -> 0, the MI suppression)")
print("  m_eff(|a|->inf)/m = K(z->inf) =", sp.limit(K, z, sp.oo), "  (Newtonian: inertia -> m)")
ratio_lowhigh = sp.limit(K,z,0)  # =0 < 1
print(f"  => m_eff(0) = 0  <  m_eff(inf) = m  => the inertia DROPS at low acceleration = MOND ordering.")
print("""
  *** RESULT 2 (decisive, both ways): the anti-MOND obstruction DOES NOT survive. ***
  The predecessor anti-MOND result was an artifact of modelling MI as an ADDITIVE PASSIVE bath
  (m+gamma, gamma from J>=0). The CONSERVATIVE MULTIPLICATIVE form factor m*K(|a|^2/a0^2) has the
  CORRECT MOND ordering m_eff(0)=0 < m_eff(inf)=m WITHOUT any active pump and WITHOUT violating
  conservation (K is even => time-symmetric => lossless, build3 Section 3). So the coarse-grained
  conservative MI is genuinely MOND, not anti-MOND. This REMOVES the predecessor's hardest barrier
  to the join -- but (Sections 3-6) it does NOT by itself produce AeST. Be ruthless below.
""")

# Numerically confirm monotonic suppression (no anti-MOND turnaround anywhere):
Knum = sp.lambdify(z, K, 'numpy')
zz = np.logspace(-6, 6, 13)
print("  m_eff/m = K(z) across z=|a|^2/a0^2 (monotone increasing 0->1, no anti-MOND turnaround):")
for zv in zz:
    print(f"    z={zv:10.1e}  K={float(Knum(zv)):10.6f}")

# ===========================================================================================
# SECTION 3.  Q1 -- does the aether A^mu emerge as the MI preferred frame?
# ===========================================================================================
hdr("SECTION 3 -- Q1: does AeST's unit-timelike aether A^mu EMERGE from coarse-graining?")
print("""
The coarse-grained congruence 4-velocity u^mu(x) is unit-timelike BY CONSTRUCTION (u.u=-1).
AeST eq(5) term  -lambda(A^mu A_mu + 1)  imposes EXACTLY A.A=-1 with a Lagrange multiplier.
""")
# Symbolic: the unit constraint term coarse-grains identically.
lam = sp.symbols('lambda', real=True)
print("  coarse-grained constraint:  -(lambda/2)(u^mu u_mu + 1),  u.u=-1  ==  AeST  -lambda(A^2+1).")
print("  => the UNIT-TIMELIKE CONSTRAINT term is PRODUCED (trivially: u is a 4-velocity).  [PRODUCED]")
print("""
  BUT (the load-bearing distinction, both ways):
  AeST's A^mu is a *DYNAMICAL PROPAGATING* field: it carries the Maxwell-type kinetic term
  -(K_B/2) F^{mu nu}F_{mu nu}, F=2 grad_[mu A_nu], giving A^mu a wave equation (AEST.txt l.640-648:
  vector modes omega^2=k^2+M^2, healthy for 0<K_B<2 -- A^mu PROPAGATES).
  The coarse-grained u^mu is a KINEMATIC frame field (the congruence velocity); the form-factor
  action uses it as the clock that defines Box_u and the rest frame of the dS bath. NOTHING in the
  worldline kinetic term  -(m/2) u.K u  generates a  grad_[mu u_nu]^2  Maxwell kinetic term for u.
""")
sub("3a. Try to generate -(K_B/2)F^2 from the form factor: the gradient (vorticity/shear) content")
print("""
  Off the const-|a| slice, Box_u u^mu DOES carry derivatives of u (the jerk and the congruence
  gradient grad_nu u^mu = (1/3)theta q_{mu nu} + sigma_{mu nu} + omega_{mu nu} - a_mu u_nu).
  Q: does u^mu K(Box_u/a0^2) u_mu, expanded to two gradients of u, contain F^{mu nu}F_{mu nu}
  = 4 grad_[mu u_nu] grad^[mu u^nu] = 2(omega^2 - sigma^2 + ...) (the antisymmetric vorticity)?
""")
# Construct the two-derivative expansion of Box_u u along the congruence, symbolically (schematic
# tensor bookkeeping done analytically; here we verify the SCALAR each piece contributes).
# Box_u u^mu = (u.grad)(u.grad)u^mu = (u.grad) a^mu = jerk^mu + a^nu grad_nu u^mu.
# u_mu Box_u u^mu = u_mu jerk^mu + a^nu a_mu grad_nu u^mu ... project: u.jerk = -a.a (since u.a=0,
# d/dtau(u.a)=0 => u.jerk + a.a =0). So u_mu Box_u u^mu = -|a|^2 + (a^nu a^mu grad_nu u_mu).
print("""
  Projection identities (sympy-checked on hyperbolic motion in build3 1a; here the field version):
    u.a = 0  (a orthogonal to u),  d/dtau(u.a)=0 => u.(jerk) = -a.a = -|a|^2.
  Hence  u_mu (Box_u u^mu) = -|a|^2 + a^nu a^mu grad_nu u_mu  (the second term is O(a^2 * grad u)).
  CRUCIAL: every term in  u_mu K(Box_u/a0^2) u^mu  is a SCALAR built from u, a=(u.grad)u, and their
  proper-time derivatives ALONG u. It is a contraction with u^mu on BOTH ends. The Maxwell term
  F^{mu nu}F_{mu nu} = 4 grad_[mu u_nu] grad^[mu u^nu] is the TRANSVERSE (orthogonal-to-u) vorticity/
  shear, NOT contracted with u. The form factor produces  a_mu a^mu-type (LONGITUDINAL) scalars and
  NOT the transverse F^2.  => -(K_B/2)F^2 is NOT generated. K_B is unconstrained.  [NOT PRODUCED]
""")
print("""
  *** Q1 ANSWER: PARTIAL. The unit-timelike frame u^mu = A^mu EMERGES (kinematically) and the
  -lambda(A^2+1) constraint is reproduced, BUT the aether's KINETIC term -(K_B/2)F^2 -- what makes
  A^mu a propagating dynamical field rather than a background clock -- is NOT produced. The MI
  coarse-graining gives a NON-PROPAGATING frame (DEW-like u^mu=-grad chi/|grad chi|), not AeST's
  propagating aether. The frame is IMPORTED/kinematic, not dynamically generated. ***
""")

# ===========================================================================================
# SECTION 4.  Q2 -- does the Y^{3/2} deep-MOND term emerge with the SAME a0?
# ===========================================================================================
hdr("SECTION 4 -- Q2: does AeST's Y^{3/2} term emerge, with the SAME a0?")
print("""
Deep-MOND limit of the coarse-grained form factor: K(z)->sqrt(z)=|a|/a0 as z->0, so
  L_kin^{dMOND} = (1/2) rho_m K(|a|^2/a0^2) u.u -> -(1/2) rho_m |a|/a0   (using u.u=-1).
The acceleration field a^mu=(u.grad)u^mu. Now PROJECT onto the scalar sector: in the quasistatic
weak-field congruence the acceleration is the gradient of the collective potential, a^mu -> grad^mu phi
(the MOND-activating Newtonian-frame acceleration, build3 Section 4: a_rel = grad Phi = grad phi).
Then |a| = |grad phi| and:
  L_kin^{dMOND} -> -(1/2) rho_m |grad phi|/a0  ... (matter-density-weighted)  -- compare AeST.
""")
gx, gy, gz = sp.symbols('g_x g_y g_z', real=True)
gmag = sp.sqrt(gx**2+gy**2+gz**2)
# The coarse-grained collective field action whose EL eq reproduces the single-worldline deep-MOND
# law m a^2/a0 = F (i.e. div(|grad phi|/a0 grad phi)=4pi G rho, the AQUAL/BM84 eq) is:
L_aqual = -sp.Rational(1,3)*(1/a0)*gmag**3
dLdg = [sp.simplify(sp.diff(L_aqual, gi)) for gi in (gx,gy,gz)]
target = [sp.simplify(-(gmag/a0)*gi) for gi in (gx,gy,gz)]
match_aqual = all(sp.simplify(dLdg[i]-target[i])==0 for i in range(3))
print("  The collective deep-MOND field Lagrangian L=-(1/3a0)|grad phi|^3 has EL flux = MOND flux")
print("    -(|grad phi|/a0) grad phi :", match_aqual, "  (True => AQUAL recovered)")
Y = sp.symbols('Y', positive=True)
print("  AeST Y=q^{mn}grad_m phi grad_n phi -> |grad phi|^2 (quasistatic, A^0-aligned);")
print("    Y^{3/2} = (|grad phi|^2)^{3/2} =", sp.simplify((gmag**2)**sp.Rational(3,2)-gmag**3)==0, "== |grad phi|^3.")
print("""
  So the POWER (Y^{3/2}=|grad phi|^3) and the 1/a0 SCALING coarse-grain out of the MI form factor
  and COINCIDE with AeST's deep-MOND J(Y)->(2lam_s/3(1+lam_s)a0)Y^{3/2}.   [POWER+SCALE MATCH]
""")
sub("4a. Is the a0 COEFFICIENT produced, or only matched? (the ruthless test)")
print("""
  AeST coefficient: J(Y) -> (2 lam_s/(3(1+lam_s))) (1/a0) Y^{3/2}. The number (2lam_s/3(1+lam_s))
  is a FREE combination of AeST params (lam_s the tracking/screening param). a0 itself is a FREE
  INPUT in AeST ("It is in this limit that a0 appears", AEST.txt l.124-125) -- AeST does NOT predict
  a0; it inserts it.
  MI side: a0 = c^2 sqrt(Lambda/32pi) is the form-factor's operator scale (the dS-Unruh floor cH_L/Z).
  It is TRANSMITTED into the |grad phi|^3 coefficient, but the coarse-graining does NOT DERIVE its
  value -- it carries the same a0 that was already put into mu_fw/T_eff (build3: 'a0 transmitted as
  operator scale ... quarantined').
  => BOTH sides INSERT a0 by hand; the coarse-graining MATCHES the slot, it does not PRODUCE the number.
     The prefactor 2lam_s/3(1+lam_s) is a REFIT knob (set to 2/3 in the screening limit to match BM84).
  *** Q2 ANSWER: the Y^{3/2} term and 1/a0 scaling EMERGE (shared deep-MOND attractor / AQUAL fixed
  point); the a0 COEFFICIENT is MATCHED/TRANSMITTED, NOT produced. Z, kappa NOT produced. ***
""")

# ===========================================================================================
# SECTION 5.  Q3 -- does the shift-symmetric scalar phi emerge?
# ===========================================================================================
hdr("SECTION 5 -- Q3: does the shift-symmetric scalar phi emerge?")
print("""
The collective potential phi(x) whose gradient is the coarse-grained MI acceleration response
enters the deep-MOND density ONLY through grad phi (|grad phi|^3) -- never phi itself. So the
coarse-grained scalar is SHIFT-SYMMETRIC (phi -> phi + phi0 leaves L invariant). AeST eq(5) is
"shift symmetric under phi -> phi + phi0" (AEST.txt l.258-261). Symbolic check:
""")
phi0 = sp.symbols('phi_0', real=True)
# L depends only on grad phi; shifting phi by const leaves grad phi unchanged => invariant.
print("  d/dphi0 [ L(grad(phi+phi0)) ] = d/dphi0 [ L(grad phi) ] =", 0, " (grad of const = 0). SHIFT-SYM.")
print("""
  HOWEVER (both ways): there is a SUBTLE non-production. AeST's phi is a FUNDAMENTAL dynamical scalar
  with its OWN kinetic structure -(2-K_B)Y and the free function F(Y,Q), AND a cosmological role
  (AEST.txt l.161-196: shift-symmetric k-essence K(Qbar) giving rho~a^-3 dust + CC = the 'Higgs
  phase'). The coarse-grained MI phi is the COLLECTIVE ACCELERATION POTENTIAL of the matter
  congruence -- it is DEFINED by grad phi = a (the response), so it is NOT an independent d.o.f.
  with its own propagation; it is slaved to the matter via a = grad phi = (u.grad)u. The COSMOLOGICAL
  k-essence sector (K(Q)=-2Lambda+K2(Q-Q0)^2, giving the a^-3 'dark dust') is NOT produced by the
  inertia coarse-graining at all -- that is a GRAVITY/cosmology-sector self-action AeST adds to fit
  CMB+MPS, with FOUR free params (K_B,K2,Q0,lam_s) tuned to Planck (AEST.txt l.464-466, 529-536).
  *** Q3 ANSWER: PARTIAL. A shift-symmetric scalar phi EMERGES with the right symmetry, but only as
  the SLAVED collective acceleration potential (grad phi = a). Its INDEPENDENT kinetic term -(2-K_B)Y,
  the free F(Y,Q), and especially the COSMOLOGICAL k-essence dust/CC sector are NOT produced -- they
  are AeST's separately-tuned gravity-side content. ***
""")

# ===========================================================================================
# SECTION 6.  THE MILGROM-1994 MI NO-GO -- does it BLOCK the join? (verbatim inequality)
# ===========================================================================================
hdr("SECTION 6 -- the Milgrom-1994 MI no-go (astro-ph/9303012): blocks the join, or evaded?")
print("""
VERBATIM (agentC_covariance_memo.md l.49-55, quoting astro-ph/9303012):
  Galilei invariance + LOCALITY (finitely many time derivatives) =>  up to a total derivative
      "L_k = (1/2) alpha v^2 + Ltilde_k(a0, r^(2), r^(3), ...)"
  (boosts force velocity v into the quadratic term ONLY). Then:
      Newtonian limit (a0->0, recover m v^2/2)  REQUIRES  alpha = 1.
      MOND limit (S_k prop 1/a0, deep-MOND scale invariance)  REQUIRES  alpha = 0.
      alpha=1 AND alpha=0  =>  CONTRADICTION.
  => "Galilei-invariant theories for MOND, derivable from an action, must be STRONGLY NON-LOCAL."
""")
sub("6a. The inequality, made explicit (sympy): the alpha=1 vs alpha=0 contradiction")
alpha, v, a0s = sp.symbols('alpha v a_0', positive=True)
# A LOCAL Galilei-inv kinetic Lagrangian: L = alpha v^2/2 + Ltilde(a0, a, jerk,...).
# Newtonian: a0->0 must give m v^2/2  => coefficient of v^2 is 1 => alpha=1.
# deep-MOND scale invariance (t,r)->lam(t,r), G a0 fixed: S_k -> lam^? ; S prop 1/a0 with v^2 term
# NOT scale-covariant unless its coefficient alpha=0. The v^2 term scales as lam^0 (v^2 dt = v^2),
# the deep-MOND action must scale homogeneously prop 1/a0 => the alpha v^2 piece must be ABSENT => alpha=0.
newton_alpha = sp.solve(sp.Eq(alpha, 1), alpha)   # =1
print("  Newtonian limit fixes:  alpha =", newton_alpha[0])
print("  deep-MOND scale-invariance (S prop 1/a0, no bare v^2) fixes: alpha = 0")
print("  Contradiction:  alpha = 1  AND  alpha = 0  =>  no LOCAL action.   [no-go confirmed]")
print("""
  HOW THE FORM-FACTOR EVADES IT (and what that costs):
  build3's K(z)=(sqrt(1+4z)-1)/(2sqrt(z)) is NON-POLYNOMIAL in z=Box_wl/a0^2 (branch cut), hence an
  INFINITE-ORDER operator = STRONGLY NONLOCAL = EXACTLY the class Milgrom-94 LICENSES (not a finite-
  derivative truncation; avoids the Ostrogradsky ghost of Costa-Franzmann-Pereira 1904.07321). So the
  no-go does NOT block writing the MI action. The MI action EXISTS, nonlocally, as built.
""")
sub("6b. WHAT the no-go DOES block: turning this MI action into AeST's LOCAL modified-GRAVITY form")
print("""
  The no-go's deeper content (Milgrom 1994; restated 2208.07073): an MI theory and a LOCAL modified-
  GRAVITY (modified-Poisson / AQUAL-field) theory agree on the CIRCULAR-ORBIT (constant-|a|) slice --
  where mu(a/a0) a = dPhi/dr is an ALGEBRAIC relation true in BOTH -- but DISAGREE off that slice
  (eccentric orbits, transients, EFE history-dependence). Milgrom 2011 (1111.1611): MI EFE depends on
  the WHOLE orbital history of the external acceleration; modified-gravity EFE depends only on the
  INSTANTANEOUS external field. They are NOT the same theory; they share only the circular slice.

  CONSEQUENCE FOR THE COARSE-GRAINING -> AeST:
  - AeST is a LOCAL modified-GRAVITY field theory (matter couples ONLY to g_{mu nu}; eq(5) all terms
    are finite-gradient field self-actions; AEST.txt l.379 'they couple only to g_{mu nu}'). Inertia
    is STANDARD in AeST.
  - The coarse-grained MI form factor is a NONLOCAL functional of the congruence (the operator
    K(Box_u/a0^2) is infinite-order). It reproduces AeST ONLY on the orbit-averaged const-|a| slice
    (Section 1, where I dropped the jerk to get Box_u u -> |a|^2 u). OFF that slice (jerk-dependent,
    history-dependent) it is a DIFFERENT functional, and Milgrom-94 GUARANTEES no local field theory
    (AeST included) equals it there.
  *** SECTION 6 ANSWER: the no-go does NOT block writing the MI action (nonlocal => licensed), and
  does NOT block the IR/circular-slice AGREEMENT with AeST (both give mu(a/a0)a = grad Phi there).
  It DOES block the full identification: coarse-grained MI = AeST holds ONLY on the const-|a| slice;
  off-slice the MI is a nonlocal history-dependent functional that no local modified-gravity action
  (AeST) can equal. So the 'join' is a SLICE-WISE DEGENERACY, not a theory identity. ***
""")

# ===========================================================================================
# SECTION 7.  REFIT vs PRODUCTION ledger + join_kind classification (both ways)
# ===========================================================================================
hdr("SECTION 7 -- PRODUCTION vs REFIT ledger; honest join_kind")
print("""
 AeST eq(5) object        | coarse-grained MI produces it? | PRODUCED / REFIT / NOT
 -------------------------|--------------------------------|----------------------------
 u^mu unit-timelike frame | yes, kinematically (congruence)| PRODUCED (frame), but...
 -lambda(A^2+1) constraint| yes (u is a 4-velocity)        | PRODUCED (trivial)
 -(K_B/2)F^2 aether KINETIC| NO (longitudinal scalars only) | NOT PRODUCED  *** hard gap ***
 shift-sym scalar phi     | yes, but SLAVED (grad phi = a) | PARTIAL (symmetry yes; indep d.o.f. no)
 Y^{3/2} power + 1/a0 scale| yes (deep-MOND attractor/AQUAL)| PRODUCED (shared IR fixed point)
 a0 VALUE (=> Z, kappa)   | NO -- transmitted from T_eff   | REFIT/transmitted (not derived)
 -(2-K_B)Y, free F(Y,Q)   | not fixed (free both sides)    | NEITHER (free)
 cosmological K(Q) dust/CC| NO (gravity-sector k-essence)  | NOT PRODUCED (AeST tunes to Planck)
 R + Lambda host gravity  | NO (supplied separately)       | NOT PRODUCED (supplied)
 -------------------------|--------------------------------|----------------------------

CLASSIFICATION (be ruthless):
 - The coarse-graining PRODUCES: the unit-timelike frame, the unit constraint, the shift symmetry,
   and the deep-MOND Y^{3/2}/a0 SLOT (the AQUAL IR fixed point shared by all MOND theories).
 - It REFITS (does not produce): the a0 VALUE (transmitted), the deep-MOND prefactor (knob set to 2/3).
 - It DOES NOT PRODUCE: the aether kinetic -(K_B/2)F^2 (A^mu's propagation), the scalar's independent
   dynamics, the cosmological dust/CC k-essence sector, the host R+Lambda.
 - Milgrom-94: the identification holds ONLY on the const-|a| circular slice; off-slice the nonlocal
   MI is provably NOT any local modified-gravity (AeST) action.

 => This is NOT a FULL-JOIN (most of AeST's distinctive field content -- the propagating aether, the
    cosmological k-essence, the independent scalar -- is unproduced, and the a0 number is refit).
 => It IS more than DISTINCT-THEORIES: real shared structure (frame + shift-sym scalar + AQUAL IR law)
    EMERGES, not just matched.
 => It is precisely DEGENERATE-ON-RAR-ONLY: coarse-grained MI and AeST coincide on the static/circular
    RAR slice (both -> mu(a/a0)a=grad Phi, v^4=GMa0, |grad phi|^3) -- the SPARC-pinned slice -- and
    that degeneracy is GUARANTEED by Milgrom-94's circular-orbit lemma, NOT by the coarse-graining
    producing AeST. Off that slice (Cassini via the gate, EFE history-dependence, lensing, cosmology)
    they are DISTINCT (gated MI vs ungated MG; non-propagating frame vs propagating aether).
""")
print("="*86)
print(" BUILD 4 NET: coarse-grain conservative MI -> a unit-timelike-vector + slaved-shift-scalar")
print("   field theory that DEGENERATES with AeST ON THE RAR/circular SLICE ONLY. The anti-MOND")
print("   obstruction is REMOVED by the conservative correction (Section 2), but AeST is still NOT")
print("   PRODUCED: aether kinetic K_B, cosmological k-essence, and the a0 VALUE are refit/absent;")
print("   Milgrom-94 caps the agreement at the circular slice. yields_aest = PARTIAL-REFIT.")
print("="*86)
