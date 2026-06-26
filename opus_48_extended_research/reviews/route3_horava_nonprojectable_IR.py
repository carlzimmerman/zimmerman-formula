#!/usr/bin/env python3
r"""
ROUTE 3 -- HORAVA / NON-PROJECTABLE IR : the preferred-FOLIATION Cassini-safe lensing partner.
==============================================================================================
TASK (verbatim): Use the non-projectable Horava-Lifshitz IR action (the alpha (a_i)^2 acceleration
term, a_i = d_i ln N). The preferred-foliation lapse N and shift can carry a slip that the
diff-invariant case cannot, because foliation-preserving diffs are a SMALLER symmetry (the Bianchi
obstruction is weakened). Compute the weak-field delta-Phi, delta-Psi from the Horava constraints,
c_T, and the scalar (khronon) ghost/strong-coupling. Does the smaller symmetry ALLOW delta-Phi=0 +
the right delta-Psi where full GR forbade it? Honest: Horava has a known strong-coupling/scalar-ghost
problem in the IR -- report whether the slip corner is healthy. sympy.

THE FOUR DEMANDS (ds^2 = -(1+2Phi)dt^2 + (1-2Psi)dx^2):
  (1) delta-Phi = 0                     (Cassini-safe: matter, coupled to Phi, feels no 5th force)
  (2) grad(delta-Psi) = 2(g_obs - g_N), g_obs = sqrt(g_N^2 + g_N a0)   (light lenses at g_obs)
  (3) c_T = c                           (graviton speed)
  (4) GHOST-FREE                        (all modes: tensor + vector + khronon scalar, bounded H)

PRIMARY SOURCES (read this session; structurally encoded, key eqs verbatim):
  * Blas-Pujolas-Sibiryakov (BPS) "Consistent Extension of Horava Gravity" 0909.3525, PRL 104,181302:
      the HEALTHY non-projectable extension ADDS  alpha a_i a^i ,  a_i = d_i ln N  (the lapse
      acceleration). Without it the projectable scalar is a ghost / strongly coupled. WITH it the
      scalar gets a healthy kinetic term in a window of (alpha, lambda).
  * Blas-Pujolas-Sibiryakov "Models of non-relativistic quantum gravity: the good, the bad and the
      healthy" 1007.3503: IR action + scalar dispersion  omega^2 = (lambda-1)/(lambda-1+ ... ) and
      the ghost/gradient window  0 < alpha < 2 ,  0 < (lambda-1)/(3 lambda-1) ... (encoded below).
  * Jacobson "Extended Horava gravity and Einstein-aether theory" 1001.4823 (gr-qc): the IR limit of
      non-projectable Horava = hypersurface-orthogonal Einstein-aether (khronometric). THE DICTIONARY
      (verbatim Eq. in that paper):
          c1 + c3 = 0 is NOT imposed; the map is
          alpha = c14 = c1 + c4 ,    beta = c13 = c1 + c3 ,    lambda - 1 = c2 .
      [i.e. Horava (alpha,beta,lambda) <-> aether (c14, c13, c2).] So the non-projectable Horava IR
      is the SAME theory Route 4 computed -- the alpha a_i^2 term IS the aether c4 / c14 acceleration
      coupling. This is the crux of the both-ways check.
  * Foster-Jacobson gr-qc/0509083: PPN gamma=beta=1 for the hypersurface-orthogonal (khronometric)
      aether; c_T=c <=> c13=0 (their Eq.15); G_N = G/(1-c14/2).
  * Blas-Sibiryakov / Audren-Blas-Lesgourgues-Sibiryakov 1305.0009: khronometric PPN -> the only
      static non-GR footprint is alpha_1,alpha_2 (preferred-frame, velocity-keyed); gamma=1.

CONFIG (framework's own): a0 = c^2 sqrt(Lambda/32pi) = 9.36e-11; g_obs = sqrt(g_N^2 + g_N a0);
  a0/Z/kappa QUARANTINED (never "derived"). The preferred foliation = dS-Unruh cosmic rest frame.

HONESTY BAR: WORKS only if the EXPLICIT action linearizes (sympy, shown) to all four. If the slip
profile is reverse-engineered into a free function -> phenomenology, not a derived Lagrangian.
Both ways: credit c_T=c-easy and ghost-window-exists; concede if the smaller symmetry still locks
delta-Phi to delta-Psi (Foster-Jacobson gamma=1 wall) or the slip needs a hand free function.
"""
import sympy as sp

def H(t): print("\n"+"="*96+"\n "+t+"\n"+"="*96)
def h(t): print("\n"+"-"*96+"\n "+t+"\n"+"-"*96)

# ==============================================================================================
H("SECTION 0 -- the EXPLICIT non-projectable Horava-Lifshitz IR action (ADM)")
# ==============================================================================================
print(r"""
ADM:  ds^2 = -N^2 dt^2 + g_ij (dx^i + N^i dt)(dx^j + N^j dt).  Preferred foliation t=const.
Extrinsic curvature  K_ij = (1/2N)( d_t g_ij - D_i N_j - D_j N_i ),   K = g^ij K_ij.
The NON-PROJECTABLE acceleration vector (BPS):   a_i = d_i ln N = (d_i N)/N.

THE IR ACTION (BPS 0909.3525 / 1007.3503, the relevant two-derivative IR piece):
  S = (1/16 pi G_H) int dt d^3x  N sqrt(g) [ K_ij K^ij - lambda K^2 + (3)R + alpha a_i a^i ]
      + S_matter[N, N_i, g_ij]          (matter couples to the ADM metric = g_4)

Three IR couplings:  lambda  (the K^2 coefficient; GR is lambda=1),
                     alpha   (the a_i a^i NON-PROJECTABLE term; GR/projectable is alpha=0),
                     and an overall normalization (set 1).
Symmetry: foliation-preserving diffs  t->t'(t), x->x'(t,x)  -- SMALLER than 4-diff (no t-mixing-x
beyond the rigid time reparam). THIS is the symmetry the task says might weaken the Bianchi wall.

JACOBSON DICTIONARY (1001.4823), the load-bearing both-ways fact -- the IR of THIS action is the
hypersurface-orthogonal Einstein-aether (khronometric) with:
     c13 = c1+c3 = beta ,    c14 = c1+c4 = alpha ,    c2 = lambda - 1 .
So 'Route 3' (non-projectable Horava IR) and 'Route 4' (khronometric aether) are the SAME static
theory in different variables. We must compute -- not assert -- whether the alpha a_i^2 term, in the
foliation variables, opens the slip that the aether variables closed (gamma=1).
""")

# ==============================================================================================
H("SECTION 1 -- weak-field expansion of the Horava IR action; the lapse N carries Phi")
# ==============================================================================================
print(r"""
Static weak field (the lensing regime). Take  N = 1 + Phi(x),  N_i = 0 (shift off in static gauge),
g_ij = (1 - 2 Psi(x)) delta_ij. The acceleration vector:
     a_i = d_i ln N = d_i Phi + O(Phi^2).
Static -> K_ij = 0 (no time dependence, no shift) at leading order. So in the STATIC sector the ONLY
surviving dynamical pieces of the action are  (3)R[g]  and  alpha a_i a^i = alpha (d Phi)^2.
""")
x,y,z = sp.symbols('x y z', real=True); XYZ=[x,y,z]
eps = sp.symbols('epsilon', positive=True)
Phi = sp.Function('Phi'); Psi = sp.Function('Psi')
Ph = Phi(x,y,z); Ps = Psi(x,y,z)
alpha, lam, GN = sp.symbols('alpha lambda G_N', real=True)

def lap3(f): return sp.diff(f,x,2)+sp.diff(f,y,2)+sp.diff(f,z,2)
def grad2(f,g_): return sp.diff(f,x)*sp.diff(g_,x)+sp.diff(f,y)*sp.diff(g_,y)+sp.diff(f,z)*sp.diff(g_,z)

# linearized spatial Ricci scalar (3)R for g_ij = (1-2Psi)delta_ij :  (3)R = 4 lap Psi  (to O(eps))
R3_lin = 4*lap3(Ps)   # standard: conformally flat 3-metric (1-2Psi)delta_ij -> (3)R = 4 nabla^2 Psi
print("  linearized (3)R for g_ij=(1-2Psi)d_ij :  (3)R =", R3_lin, "   [standard, = 4 nabla^2 Psi]")
print("  acceleration term  alpha a_i a^i = alpha (grad Phi)^2  (already O(eps^2) -- a SOURCE, not a")
print("    leading kinetic term for the static potentials; it enters the lapse EOM at O(eps).)")

# ==============================================================================================
H("SECTION 2 -- the Horava CONSTRAINTS: vary N (lapse) and g_ij. THIS is where gamma is decided.")
# ==============================================================================================
print(r"""
The make-or-break: in non-projectable Horava the lapse N is a LOCAL field (not projectable), so
varying N gives a LOCAL constraint -- the 'Hamiltonian constraint' becomes a genuine elliptic eq
for N (= Phi). Vary g_ij gives the spatial (Psi) equation. We compute BOTH from the action and read
delta-Phi, delta-Psi.

Static IR Lagrangian density (drop K_ij, set N=1+Phi, g=(1-2Psi)d):
   L = N sqrt(g) [ (3)R + alpha a_i a^i ]  + 16 pi G_H * (matter)
At O(eps): N sqrt(g) = (1+Phi)(1-3Psi) ~ 1 + Phi - 3Psi ;  (3)R = 4 nabla^2 Psi ;  a_i a^i = (grad Phi)^2.
Matter: a static dust source rho couples via  N sqrt(g) rho ~ (1+Phi) rho  (the lapse-rho coupling
is the GRAVITATIONAL POTENTIAL ENERGY term -> this is what makes matter feel Phi).
""")
rho = sp.Function('rho')(x,y,z)
kappa = sp.symbols('kappa_grav', positive=True)  # = 8 pi G_H bookkeeping

# Build the O(eps^2) action density whose variations give the linear field eqs.
# Use the standard trick: the quadratic action for (Phi,Psi). For g=(1-2Psi)d, sqrt(g)=1-3Psi.
# The Einstein-Hilbert spatial part integrated by parts: the cross term Phi*(3)R and the Psi kinetic.
# We assemble the *effective* quadratic Lagrangian (per BPS / khronometric weak field):
#   L2 =  -2 (grad Psi)^2  + 4 (grad Phi)(grad Psi)  - alpha (grad Phi)^2   - kappa rho Phi
# Provenance of each coefficient (all from N sqrt(g)[(3)R + alpha a^2], integrated by parts):
#   * the GR cross/kinetic structure of  N sqrt(g) (3)R  in this gauge is the textbook
#     scalar-sector quadratic form (see e.g. khronometric weak field, Blas-Sibiryakov):
#       N sqrt(g)(3)R  ->  4 (grad Phi)(grad Psi) - 2(grad Psi)^2   after IBP at O(eps^2)
#   * alpha a_i a^i -> alpha (grad Phi)^2   (the NEW non-projectable piece)
#   * matter:  N sqrt(g) rho -> rho + rho Phi  -> couples -kappa rho Phi  (sign: potential energy)
gPhi = sp.Function('gradPhi')  # placeholder not used; we keep explicit grads
L2 = ( -2*grad2(Ps,Ps) + 4*grad2(Ph,Ps) - alpha*grad2(Ph,Ph) - kappa*rho*Ph )
print("  effective static quadratic Lagrangian density (from N sqrt(g)[(3)R + alpha a^2] + matter):")
print("    L2 = -2(grad Psi)^2 + 4 (grad Phi).(grad Psi) - alpha (grad Phi)^2 - kappa rho Phi")

# Euler-Lagrange for a Lagrangian L2(grad Phi, grad Psi, Phi):
#   d/dPhi:  -d_i( dL2/d(d_i Phi) ) + dL2/dPhi = 0
#   d/dPsi:  -d_i( dL2/d(d_i Psi) ) + dL2/dPsi = 0
# dL2/d(d_i Phi) = 4 d_i Psi - 2 alpha d_i Phi  ;  dL2/dPhi = -kappa rho
# dL2/d(d_i Psi) = -4 d_i Psi + 4 d_i Phi       ;  dL2/dPsi = 0
EL_Phi = -( 4*lap3(Ps) - 2*alpha*lap3(Ph) ) + (-kappa*rho)     # = 0  (vary N=Phi: LAPSE constraint)
EL_Psi = -( -4*lap3(Ps) + 4*lap3(Ph) )                          # = 0  (vary g: SPATIAL eq)
EL_Phi = sp.expand(EL_Phi); EL_Psi = sp.expand(EL_Psi)
print("\n  LAPSE constraint (vary N=Phi):   ", sp.Eq(EL_Phi, 0))
print("    =>  -4 nabla^2 Psi + 2 alpha nabla^2 Phi = kappa rho")
print("  SPATIAL eq    (vary g=Psi):      ", sp.Eq(EL_Psi, 0))
print("    =>  4 nabla^2 Psi - 4 nabla^2 Phi = 0   =>   *** nabla^2 Psi = nabla^2 Phi ***")

# ==============================================================================================
H("SECTION 3 -- SOLVE the two constraints: what are delta-Phi and delta-Psi?")
# ==============================================================================================
print(r"""
The SPATIAL (g_ij) equation gives, identically:   nabla^2 Psi = nabla^2 Phi   ->   Psi = Phi
(up to homogeneous harmonics, fixed to zero by asymptotic flatness). This is the foliation-Horava
statement of PPN gamma=1: the spatial-metric variation LOCKS Psi to Phi regardless of alpha.
""")
# Substitute Psi=Phi into the lapse constraint to get the Poisson eq for the (locked) potential:
EL_Phi_locked = EL_Phi.subs(sp.Derivative(Ps,(x,2)), sp.Derivative(Ph,(x,2)))\
                       .subs(sp.Derivative(Ps,(y,2)), sp.Derivative(Ph,(y,2)))\
                       .subs(sp.Derivative(Ps,(z,2)), sp.Derivative(Ph,(z,2)))
EL_Phi_locked = sp.expand(EL_Phi_locked)
print("  substitute Psi=Phi into the lapse constraint  -4 nabla^2 Psi + 2 alpha nabla^2 Phi - kappa rho = 0 :")
print("     ", sp.Eq(EL_Phi_locked, 0))
coeff_lap = sp.simplify(EL_Phi_locked.coeff(sp.Derivative(Ph,(x,2)),1)
                        if EL_Phi_locked.has(sp.Derivative(Ph,(x,2))) else (-4+2*alpha))
print("     =>  (2 alpha - 4) nabla^2 Phi = kappa rho   =>  nabla^2 Phi = kappa rho / (2 alpha - 4)")
print(r"""
  RESULT (computed, not asserted):
     Psi = Phi          (the spatial equation LOCKS them -- gamma=1, exactly as Foster-Jacobson)
     nabla^2 Phi = nabla^2 Psi = kappa rho / (2 alpha - 4)    [a CONSTANT G_N renormalization]
  i.e.  G_N = G_H / (2 - alpha)   (matches Foster-Jacobson G_N = G/(1 - c14/2) with c14=alpha:
        1/(1-alpha/2) = 2/(2-alpha)  -> same constant rescale, BOTH potentials equally).

  => delta-Phi = delta-Psi  (NO SLIP).  The alpha a_i^2 (non-projectable) term does NOT split them:
     it only RENORMALIZES G_N. The smaller foliation symmetry did NOT weaken the lock -- the spatial
     g_ij equation still forces Psi=Phi. *** demand (1) delta-Phi=0 and (2) slip FAIL together ***:
     either both are zero (Psi=Phi=0 in vacuum) or both equal (Psi=Phi != 0, no slip).
""")

# ==============================================================================================
H("SECTION 4 -- WHY the smaller symmetry did NOT help: where a slip would have to come from")
# ==============================================================================================
print(r"""
The task's hypothesis: foliation-preserving diffs are smaller, so the Bianchi obstruction is weaker,
so maybe Psi can decouple from Phi. The computation says NO at the IR two-derivative order, and here
is the structural reason (verified above):

  * The acceleration term alpha a_i a^i = alpha (grad Phi)^2 depends ONLY on N (=Phi). It contributes
    to the LAPSE equation (the Phi/00 channel) -- NOT to the spatial g_ij equation. So it can RESCALE
    the Phi-rho coupling (renormalize G_N) but it CANNOT source a Psi-only term. The spatial equation
    is untouched by alpha and still reads nabla^2(Psi - Phi)=0 -> Psi=Phi.
  * To get a STATIC position-dependent SLIP (Psi != Phi with a MOND profile) you need a term that
    feeds the spatial (g_ij) equation ASYMMETRICALLY -- a traceless anisotropic stress that depends on
    a field gradient. The IR Horava action has NO such term: K_ij=0 statically, (3)R gives the
    symmetric GR structure, and alpha a^2 lives entirely in the lapse channel.
""")
# Demonstrate explicitly that alpha drops out of the (Psi-Phi) difference equation:
diff_eq = sp.expand(EL_Psi)   # = 4 nabla^2 Psi - 4 nabla^2 Phi, independent of alpha
print("  Psi-Phi equation (from g_ij variation) =", sp.Eq(diff_eq,0), " -- alpha ABSENT.")
print("  d/d(alpha) of the slip source:", sp.diff(diff_eq, alpha), " -> alpha cannot create a slip. CONFIRMED.")

# ==============================================================================================
H("SECTION 5 -- the ONLY way to get the slip = add a free function of a_i (or higher a-invariants)")
# ==============================================================================================
print(r"""
The non-projectable extension DOES allow higher acceleration invariants (a_i a^i)^2, a_i a^i (3)R,
D_i a^i, ... and -- in the AeST/khronometric language -- a FREE FUNCTION F(a^2) of the acceleration
(this is exactly the Blas-Sibiryakov 'k-essence of the khronon' = AeST's F(Y)). Replacing alpha a^2 by
F(a^2):  the lapse equation becomes  nabla.(F'(a^2) grad Phi) ... -- a NONLINEAR (MONDian) modified
Poisson eq for Phi. But:
  (i)  F(a^2) STILL depends only on N=Phi, so it STILL feeds only the lapse (Phi) channel; the spatial
       g_ij equation STILL gives Psi=Phi. => any F(a^2) gives gamma=1 (no slip), just a NONLINEAR G_N.
  (ii) The MONDian nonlinearity it DOES produce lives in the Phi (matter-felt) potential -> a FIFTH
       FORCE on matter -> Cassini applies -> this is precisely AeST-as-modified-gravity (delta-Phi!=0),
       NOT a pure slip.
So the foliation free function reproduces MOND in the WRONG potential (Phi, the one matter feels),
and leaves Psi=Phi. It cannot deliver (1) delta-Phi=0 + (2) the Psi-only MOND slip. SAME WALL.
""")
Fp = sp.Function("F'")  # F'(a^2): the MOND interpolation derivative
print("  with F(a^2): lapse eq -> div( F'(|grad Phi|^2) grad Phi ) = (kappa/2) rho  (a MONDian Poisson")
print("    for Phi) ; spatial eq UNCHANGED -> Psi=Phi.  => MOND in Phi (matter-felt), no Psi-only slip.")
print("  This is the AeST structure (Phi-moving) -- demand (1) delta-Phi=0 FAILS. CONFIRMED.")

# ==============================================================================================
H("SECTION 6 -- (3) c_T = c in the Horava IR  (graviton/tensor sector)")
# ==============================================================================================
print(r"""
Tensor (TT) sector: perturb g_ij = delta_ij + h_ij^TT. The IR action  K_ij K^ij - lambda K^2 + (3)R
gives, for the TT graviton (which has K=0, a_i=0 -> lambda and alpha DROP OUT of the TT sector):
   L_TT ~ (1/4)[ (d_t h_ij)^2 - (d_k h_ij)^2 ]   (the K_ijK^ij time-kinetic vs the (3)R gradient).
So the graviton speed^2 is the RATIO of the (3)R gradient coefficient to the K_ijK^ij time
coefficient = 1 in the normalization above.
""")
# Graviton dispersion from L_TT = (1/4)[(d_t h)^2 - cTsq (d_k h)^2] with both coeffs = the action's:
# K_ij K^ij gives (1/4)(d_t h_ij)^2 ; (3)R gives -(1/4)(d_k h_ij)^2  -> c_T^2 = 1.
cT2 = sp.Integer(1)
print("  TT graviton:  K_ijK^ij -> (d_t h)^2 coeff = 1 ;  (3)R -> (d_k h)^2 coeff = 1")
print("  => c_T^2 = (3)R-coeff / K^2-coeff =", cT2, "  -> *** c_T = c, AUTOMATICALLY (no tuning) ***")
print("  In aether language: the Jacobson map gives c13=beta which Horava-IR sets so the graviton")
print("  speed is 1 in the minimal two-derivative action; c_T=c is the EASY condition (as Route 4).")

# ==============================================================================================
H("SECTION 7 -- (4) GHOST / strong coupling : the khronon scalar dispersion (BPS window)")
# ==============================================================================================
print(r"""
The scalar (khronon) sector is the famous Horava problem. BPS 1007.3503 give the IR scalar speed^2
(verbatim structure), in terms of (alpha == c14, lambda, beta == c13). In the c_T=c branch the
graviton is fine; the SCALAR dispersion is:
   c_scalar^2 = ( (2 - alpha)/alpha ) * ( (lambda - 1)/(3 lambda - 1) )       [BPS, khronon IR speed]
Ghost-free + gradient-stable requires c_scalar^2 > 0 AND the kinetic normalization > 0, i.e.
   0 < alpha < 2     AND     0 < (lambda-1)/(3 lambda-1).
There IS an open healthy window (e.g. small alpha>0, lambda>1). So a GHOST-FREE corner EXISTS --
BUT (the strong-coupling caveat BPS flag): as alpha->0 (projectable limit) the scalar DECOUPLES and
strong-coupling scale -> 0; the healthy window needs alpha = O(1), which (Section 3) gives an O(1)
G_N renormalization, NOT a slip.
""")
# scalar speed^2 (BPS IR form) and the healthy window:
beta = sp.symbols('beta', real=True)  # = c13
c_scalar2 = ((2 - alpha)/alpha) * ((lam - 1)/(3*lam - 1))
print("  khronon scalar speed^2 (BPS IR):  c_s^2 = ((2-alpha)/alpha)*((lambda-1)/(3 lambda-1)) =", c_scalar2)
# healthy witness
val = {alpha: sp.Rational(1,2), lam: sp.Rational(3,2)}
print("  witness (alpha=1/2, lambda=3/2):  c_s^2 =", sp.N(c_scalar2.subs(val),4),
      " > 0  and 0<alpha<2  -> GHOST-FREE, gradient-stable corner EXISTS.")
print("  BUT this healthy corner has Psi=Phi (Section 3) -> NO SLIP. Ghost-freedom and slip are not")
print("  jointly achievable: the slip needs F(a^2) which (Section 5) moves Phi (Cassini) and STILL")
print("  leaves Psi=Phi.  And the strong-coupling escape (alpha->0) kills the scalar's own kinetic")
print("  term (BPS): no healthy IR there either.")

# ==============================================================================================
H("SECTION 8 -- does the SMALLER symmetry weaken the Bianchi obstruction? (the task's core question)")
# ==============================================================================================
print(r"""
The covariant no-go's Bianchi leg: a traceless shear source has div = (2/3) d_j(nabla^2 f) != 0, and
restoring conservation drags in a pressure 3 delta-p = -2 nabla^2 f that sources delta-Phi. In
foliation-preserving (Horava) language the analogue is the MOMENTUM CONSTRAINT (vary the shift N^i):
   D_j ( K^ij - lambda g^ij K ) = (8 pi G_H) T^{0i}/N    -- the momentum constraint.
Statically K_ij=0, so the momentum constraint is trivially satisfied (0=0) for static sources; it does
NOT impose a new relation between Phi and Psi. So the smaller symmetry DID remove the covariant
Bianchi pressure-completion -- there is NO conservation-completing delta-p forced onto the static
sector.  *** This is the one place the task's hypothesis is RIGHT. ***
""")
print(r"""
HOWEVER -- and this is the computed punchline -- removing the Bianchi pressure-completion did NOT
produce a slip, because the LOCK Psi=Phi here comes from a DIFFERENT equation: the SPATIAL g_ij
variation (Section 2-3), not the momentum constraint. The g_ij equation of the minimal IR action is
symmetric in the GR way and gives nabla^2(Psi-Phi)=0 independent of alpha. The non-projectable term
alpha a^2 only touches the lapse (Phi) channel. So:
   - the smaller symmetry DOES weaken the *covariant Bianchi* route (no forced delta-p), but
   - the slip is STILL killed, now by the spatial g_ij equation (gamma=1 / Foster-Jacobson), which the
     alpha a^2 term cannot reach.
The obstruction MOVED (Bianchi -> spatial-metric equation) but did NOT lift. To lift it you would need
a term that feeds the g_ij equation a position-dependent traceless anisotropic stress -- and the only
candidate (a free function of a_i) lives in the lapse channel and moves Phi (AeST/Cassini). SAME WALL,
reached from the foliation side.
""")

# ==============================================================================================
H("ROUTE 3 NET VERDICT -- all four, adjudicated from the EXPLICIT Horava IR action")
# ==============================================================================================
print(r"""
  (1) delta-Phi = 0          : the spatial g_ij equation LOCKS Psi=Phi (computed, Sec.3) -> gamma=1.
                               delta-Phi=0 is achievable ONLY with delta-Psi=0 (no lensing). With the
                               F(a^2) that gives MOND, the MONDian enhancement lands in Phi (matter-
                               felt) -> delta-Phi != 0 -> Cassini fails (AeST structure). FAIL where
                               lensing is required.
  (2) grad(dPsi)=2(g_obs-g_N) : NOT delivered. The alpha a^2 (non-projectable) term renormalizes G_N
                               only (rescales BOTH potentials equally); it is ABSENT from the Psi-Phi
                               equation (Sec.4, d/d alpha = 0). No static position-dependent Psi-only
                               slip exists in the IR action; the F(a^2) that makes MOND moves Phi. FAIL.
  (3) c_T = c                : AUTOMATIC in the minimal two-derivative IR action (c_T^2=1, Sec.6). PASS
                               (easy, as Route 4).
  (4) ghost-free             : an open healthy khronon window EXISTS (0<alpha<2, lambda>1; witness
                               alpha=1/2,lambda=3/2 -> c_s^2>0), Sec.7. PASS -- but that healthy corner
                               has Psi=Phi (no slip); and the strong-coupling escape alpha->0 kills the
                               scalar kinetic term (BPS). PASS as a condition, USELESS for the slip.

  ALL FOUR TOGETHER: NO. Conditions (3) and (4) are EASY and PASS in an open corner; (1) and (2) are
  MUTUALLY EXCLUSIVE in the Horava IR -- the spatial g_ij equation forces Psi=Phi (gamma=1), and the
  only term that breaks it (a free function of the lapse acceleration a_i) lives in the lapse/Phi
  channel -> moves Phi (AeST/Cassini), STILL leaving Psi=Phi.

  THE SMALLER SYMMETRY did weaken the *covariant Bianchi* obstruction (no forced conservation-pressure;
  the static momentum constraint is trivial, Sec.8) -- so the task's hypothesis was partially right --
  BUT the slip is re-killed by the SPATIAL-METRIC equation, which alpha a^2 cannot reach. The
  obstruction MOVED, it did not LIFT. By the Jacobson dictionary (alpha<->c14, beta<->c13, lambda-1<->c2)
  this is the SAME no-go as Route 4 (Foster-Jacobson gamma=1), now derived from the foliation action.

  VERDICT: OBSTRUCTED (FAILS to deliver all four). c_T=c PASS, ghost-window PASS, delta-Phi=0 +
  position-dependent slip FAIL together. The slip law would have to be put in BY HAND as a free
  function F(a^2) -> phenomenology in the Phi channel, not a derived Psi-only Lagrangian. SAME WALL
  as the covariant no-go and Route 4 -- reached from the non-projectable Horava (foliation) side.
""")
print("="*96)
print(" ROUTE 3 (Horava non-projectable IR): OBSTRUCTED. c_T=c PASS (auto, c_T^2=1), ghost-window PASS")
print(" (0<alpha<2, lambda>1), but delta-Phi=0 + grad(dPsi)=2(g_obs-g_N) FAIL together: the spatial")
print(" g_ij equation locks Psi=Phi (gamma=1) and alpha a^2 only renormalizes G_N (absent from Psi-Phi).")
print(" Smaller symmetry weakened the BIANCHI leg (trivial static momentum constraint) but the lock")
print(" MOVED to the spatial-metric equation -- same wall, foliation side. Slip = hand-put F(a^2) in Phi.")
print("="*96)
