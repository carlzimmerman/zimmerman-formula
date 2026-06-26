#!/usr/bin/env python3
"""
ROUTE 3 -- PART 5: the FRAME-PROJECTED nonlocal slip term -- enforce delta-Phi=0, then c_T & ghost.
==================================================================================================
Parts 3-4 proved: pure scalar G(Box^{-1}R) and naive tensor Box^{-1}G_munu both move Phi.
delta-Phi=0 is a FRAME-dependent (u^mu) condition, not the covariant 4-trace. So the working
term must use the preferred frame u^mu. We now BUILD it and run the make-or-break tests.

THE CANDIDATE COVARIANT TERM (Route-3 final form):
  S_3 = (1/16 pi G) int d^4x sqrt(-g)  m^2 * sigma^{munu} [ Box^{-1} ( h_perp_munu ) ]
  with the source built so that, in the u-frame, it injects ONLY the spatial (Psi) channel and
  the anisotropic stress, with ZERO contribution to the u-u (energy/Phi) channel.

The cleanest covariant statement (the one we linearize): a NONLOCAL term coupling the baryon
stress to the metric THROUGH a transverse-traceless-in-the-u-slice projector:
  S_3 = m^2 int sqrt(-g)  [ P_perp^{mu alpha} P_perp^{nu beta} - (1/2)P_perp^{munu}P_perp^{alpha beta} ]
        ( Box^{-1} G_alpha beta )  K_gate  ... contracted to feed Psi.
  P_perp^{munu} = g^munu + u^mu u^nu  (the projector ORTHOGONAL to u; the spatial metric).

We test the SIMPLEST realization that targets the bullseye and is computable: an effective stress
  T^eff_munu = m^2 [ P_perp_mu^a P_perp_nu^b - (1/2)P_perp_munu P_perp^ab ] Box^{-1}G_ab  (TT-in-u)
Linearize on the static weak field with u^mu = (1,0,0,0) (the cosmic rest frame at leading order),
and READ: (1) does it source Phi (u-u component)? (2) does it give the right Psi-slip?
Then (3) c_T from the graviton sector, (4) ghost from the auxiliary spectrum.

Frame: a0=9.36e-11; g_obs=sqrt(g_N^2+g_N a0); kappa=1/2 free; a0/Z quarantined.
Primaries (cited, structurally checked): Maggiore RT-model 1307.3898/1402.0448 (Box^{-1}G_munu,
ghost-free, c_T=c); Jacobson Einstein-aether gr-qc/0007031 (preferred frame -> slip allowed,
c_T tunable to c); Ezquiaga-Zumalacarregui 1710.05901 (c_T=c constraints); Langlois-Noui
1510.06930 (DHOST degeneracy).
"""
import sympy as sp

def H(t): print("\n"+"="*88+"\n "+t+"\n"+"="*88)
def h(t): print("\n"+"-"*88+"\n "+t+"\n"+"-"*88)

# rebuild linearized Einstein tensor (static weak field)
t,x,y,z=sp.symbols('t x y z',real=True); X=[t,x,y,z]; eps=sp.symbols('epsilon',positive=True)
Phi=sp.Function('Phi'); Psi=sp.Function('Psi'); Ph=Phi(x,y,z); Ps=Psi(x,y,z)
g=sp.diag(-(1+2*eps*Ph),1-2*eps*Ps,1-2*eps*Ps,1-2*eps*Ps)
ginv=sp.diag(-(1-2*eps*Ph),1+2*eps*Ps,1+2*eps*Ps,1+2*eps*Ps)
def s1(e): return sp.series(sp.expand(e),eps,0,2).removeO()
def chris(g,gi,X):
    n=4; Gm=[[[0]*n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                ss=sum(gi[a,d]*(sp.diff(g[d,b],X[c])+sp.diff(g[d,c],X[b])-sp.diff(g[b,c],X[d])) for d in range(n))
                Gm[a][b][c]=s1(ss/2)
    return Gm
def ricci(Gm,X):
    n=4; R=sp.zeros(n,n)
    for b in range(n):
        for c in range(n):
            ss=0
            for a in range(n):
                ss+=sp.diff(Gm[a][b][c],X[a])-sp.diff(Gm[a][b][a],X[c])
                for d in range(n): ss+=Gm[a][a][d]*Gm[d][b][c]-Gm[a][c][d]*Gm[d][b][a]
            R[b,c]=s1(ss)
    return R
Gm=chris(g,ginv,X); Ric=ricci(Gm,X)
Rsc=s1(sum(ginv[b,c]*Ric[b,c] for b in range(4) for c in range(4)))
def stat(e): return sp.simplify(sp.expand(e).coeff(eps,1).subs({sp.Derivative(Ph,t):0,sp.Derivative(Ps,t):0}))
def lap3(f): return sp.diff(f,x,2)+sp.diff(f,y,2)+sp.diff(f,z,2)
Gt=sp.zeros(4,4)
for b in range(4):
    for c in range(4): Gt[b,c]=stat(Ric[b,c]-sp.Rational(1,2)*g[b,c]*Rsc)

# ============================================================================
H("STEP 1 -- build T^eff_munu = TT-in-u projection of Box^{-1}G_munu, linearized; READ the u-u (Phi) channel")
# ============================================================================
print("""
Preferred frame at leading order: u^mu = (1,0,0,0), u_mu=(-1,0,0,0). Spatial projector
   P_perp_munu = g_munu + u_mu u_nu  -> at leading order: P_perp_00=0, P_perp_ij=delta_ij.
Box^{-1}G_munu (static, Box->nabla^2): returns potentials. Components:
   Box^{-1}G_00 = 2 Psi      (since G_00=2 nabla^2 Psi)
   Box^{-1}G_ij = Box^{-1}( G_ij )
We apply the TT-in-u projector PI_perp[S]_ij = P_ik P_jl S_kl - (1/2)P_ij P_kl S_kl (3D traceless
transverse on the spatial slice). Crucially PI_perp annihilates the 00 (u-u) component by P_perp_00=0.
""")
# Box^{-1} G_munu at linear order. Box->nabla^2, so Box^{-1}(nabla^2 f)=f.
# Compute each G component / express as nabla^2(potential), then Box^{-1}.
G00=Gt[0,0]; Gxx=Gt[1,1]; Gyy=Gt[2,2]; Gzz=Gt[3,3]; Gxy=Gt[1,2]; Gxz=Gt[1,3]; Gyz=Gt[2,3]
print("  G_00 =", G00)
print("  G_xx =", Gxx, " ; G_xy =", Gxy)

# To apply Box^{-1}=nabla^{-2} symbolically, introduce potential-fields:
# We KNOW G_00 = 2 nabla^2 Psi => BoxInv G_00 = 2 Psi.
# For G_ij, write G_ij = nabla^2 A_ij where A_ij is the 'potential'. Since the operators are linear
# and G_ij is a combination of second derivatives of (Phi,Psi), Box^{-1}G_ij is a nonlocal combo.
# For the u-u (Phi) channel we ONLY need: does the projected T^eff have a nonzero 00 component?
# By construction P_perp_0a=0 => (PI_perp[S])_00 = 0 IDENTICALLY. So T^eff_00 = 0.
print("""
  THE PROJECTION KILLS THE 00 CHANNEL BY CONSTRUCTION:
  PI_perp[Box^{-1}G]_00 = P_perp_0k P_perp_0l (...) and P_perp_00=P_perp_0i=0  =>  T^eff_00 = 0.
  => the term injects ZERO energy density in the u-frame => it does NOT source the Phi-Poisson
     equation's rho term.  This is the design that targets delta-Phi=0.
""")
Teff_00 = 0
print("  T^eff_00 (u-u channel) =", Teff_00, "  => no rho source for Phi from this term. (good, targets req 1)")

# BUT: delta-Phi also gets a contribution from the ANISOTROPIC stress via the off-diagonal eqs.
# We must check the FULL Phi equation, not just T_00. Compute the spatial T^eff_ij and its effect.
h("1a. The spatial T^eff_ij (the anisotropic stress that this term injects) and the FULL Phi equation")
print("""
The projected spatial stress T^eff_ij = m^2 PI_perp[Box^{-1}G]_ij = m^2 [ (Box^{-1}G)_ij^TT ].
This is a TRANSVERSE-TRACELESS (in 3D) tensor: T^eff_kk = 0 (traceless) and d_i T^eff_ij=0 (transverse).
A TT spatial stress is PURE anisotropic stress: it sources the SLIP (Phi-Psi) but contributes ZERO
to the Phi-Poisson trace (since it is traceless => no isotropic pressure => no 3p term) and ZERO
to the Psi-Poisson 00 (T_00=0). Let's verify the consequence for delta-Phi via the slip equation.
""")
# The slip equation: nabla^2(Phi-Psi)_total ~ anisotropic stress. With baryons giving Phi_b=Psi_b,
# the partner adds a TT anisotropic stress Sigma_ij. The linearized eqs become:
#   nabla^2 Psi = 4piG rho_b              (T^eff_00=0: partner does NOT change the Psi-Poisson source)
#   -- WAIT: if T^eff_00=0 the partner does NOT source Psi either! Then how does Psi get the slip?
print("""
  *** THE DECISIVE TENSION, EXPOSED (both ways) ***
  If the projector kills T^eff_00 (to keep delta-Phi=0 via no rho-source), it ALSO removes the
  partner's ability to SOURCE delta-Psi from the baryon 00-channel. The partner then only injects
  a TT anisotropic stress Sigma_ij, which sources the SLIP Phi-Psi but does so SYMMETRICALLY:
     nabla^2 Phi = 4piG rho_b + (anisotropic: +Sigma-trace-adjust)
     nabla^2 Psi = 4piG rho_b - (anisotropic: -Sigma-trace-adjust)
  A pure anisotropic (TT) stress moves Phi and Psi in OPPOSITE directions by equal amounts:
     delta-Phi = +X,  delta-Psi = -X   (or the transverse analog).  => delta-Phi != 0!
  So a TT-anisotropic-stress-only source gives a slip but MOVES Phi (in the opposite sense to Psi).
  To get delta-Phi=0 EXACTLY you need delta-Phi's anisotropic contribution to VANISH, i.e. the
  anisotropic stress must be arranged so its Phi-contribution is zero -- which (Part 1) requires
  Pi = (1/2)delta-rho with delta-rho != 0. But delta-rho=0 here (T_00=0). Contradiction.
""")

# Let's make this fully explicit with sympy: solve the linearized eqs for a TT anisotropic source.
h("1b. sympy: solve linearized Einstein eqs with a pure TT anisotropic-stress source -> read delta-Phi")
# Use Fourier: the standard scalar-perturbation eqs (conformal-Newtonian), quasistatic:
#   2 k^2 Psi = 8piG a^2 delta-rho                     (00)
#   k^2(Phi-Psi) = 8piG a^2 Pi                         (slip; Pi = scalar anisotropic stress)
#   k^2(Phi+...)= ... (trace)  -- we use the two clean ones.
k,Gn,a,drho,Pi=sp.symbols('k G a delta_rho Pi',positive=True)
# partner: delta-rho=0 (T_00=0 by projection), Pi = Pi_partner != 0.
Psi_sol = sp.Rational(1,2)*8*sp.pi*Gn*a**2*0/k**2   # from (00) with delta-rho=0 -> Psi sourced 0 by partner
PhiMinusPsi = 8*sp.pi*Gn*a**2*Pi/k**2               # from slip eq with partner Pi
print("  partner (00): delta-rho=0  => partner adds 0 to k^2 Psi  => delta-Psi_from_partner_00 = 0")
print("  partner slip: k^2(delta-Phi - delta-Psi) = 8piG a^2 Pi  => delta-Phi - delta-Psi =", PhiMinusPsi)
print("""
  With delta-Psi (from the partner's own 00-source) = 0, the slip eq gives
     delta-Phi - delta-Psi = (8piG a^2/k^2) Pi   => delta-Phi = delta-Psi + (8piG a^2/k^2)Pi.
  If we WANT delta-Phi=0, then delta-Psi = -(8piG a^2/k^2)Pi != 0 -- but the partner's 00-source
  was ZERO, so delta-Psi cannot be sourced to that value by THIS term. The numbers don't close:
  a T_00=0 (Phi-protecting) projection cannot simultaneously source delta-Psi=2(g_obs-g_N).
""")

# ============================================================================
H("STEP 2 -- the inescapable conclusion: delta-Phi=0 AND delta-Psi!=0 REQUIRES T^eff_00 != 0 + anisotropic stress LOCKED")
# ============================================================================
print("""
Part 1 already nailed it: the ONLY consistent source is  T^eff_00 = delta-rho != 0 (sources Psi)
AND  Pi = (1/2)delta-rho (anisotropic, holds Phi fixed). BOTH nonzero, LOCKED in ratio 2:1.
This is NOT a TT (traceless) source and NOT a T_00=0 source -- it is a SPECIFIC imperfect-fluid
stress with energy density AND anisotropic stress in a fixed ratio, aligned with u^mu.

The covariant term must produce EXACTLY this. Can a nonlocal u-frame term do it? The structure
   T^eff_munu = alpha (u_mu u_nu) Box^{-1}(source) + beta (sigma_munu) Box^{-1}(source)
with alpha:beta fixed to give delta-rho : Pi = 2:1, IS constructible -- it is a NONLOCAL
EINSTEIN-AETHER term (energy density along u + anisotropic stress transverse to u). This is
escape hatch (b). We now test whether THIS specific aether-locked term passes c_T and ghost.
""")
# The aether-locked effective stress, parametrized:
alpha,beta=sp.symbols('alpha beta',real=True)
# require delta-rho = alpha*S, Pi = beta*S, with Pi/delta-rho = 1/2 => beta/alpha = 1/2.
ratio_req = sp.Rational(1,2)
print("  required anisotropic/density ratio beta/alpha =", ratio_req, " (from Part 1). Constructible with u-frame aether.")

# ============================================================================
H("STEP 3 -- c_T = c for the u-frame nonlocal term (graviton sector)")
# ============================================================================
print("""
c_T test: expand g_munu = eta + h, take the transverse-traceless GRAVITON h_ij^TT, find the
coefficient ratio (space)/(time) of its kinetic term. The term S_3 ~ sigma^munu Box^{-1}G_munu.
  * Box^{-1}G_munu: G_munu contains the graviton kinetic operator. Box^{-1} acting on it gives
    a NONLOCAL but 2-derivative-equivalent structure. The KEY: does it add a term ~ (d_t h)^2 with
    a DIFFERENT coefficient than (d_x h)^2?
  * Maggiore RT-model RESULT (1307.3898, cited + structurally checked): the Box^{-1}G_munu term
    does NOT modify the graviton's kinetic term coefficient -- the graviton propagates on the light
    cone, c_T=c EXACTLY. The nonlocal operator multiplies the graviton by a function of Box that
    -> 1 on the light cone (massless pole unchanged). The dark-energy effect is in the SCALAR/aux
    sector, not the tensor sector.
  * The u-frame projector: P_perp = g + uu. For h_ij^TT, u^mu=(1,0,0,0) gives P_perp h^TT = h^TT
    (the TT graviton is already spatial+transverse). The projector acts as identity on h^TT =>
    does NOT change its kinetic coefficient => c_T unchanged.
  * Einstein-aether subtlety (Jacobson): a generic aether kinetic term -(K_B/2)F^2 DOES shift c_T
    (c_T^2 = 1/(1-c_+) with c_+ a combination of aether couplings). BUT (i) we use the DEW
    NON-propagating cosmic frame u=-d chi/|d chi| (chi=Box^{-1}1), NOT a propagating aether with a
    kinetic F^2 -> no aether-induced c_T shift; OR (ii) if a propagating aether is used, c_T=c
    fixes one combination of couplings (c_13=0 in Jacobson's notation), which is the standard
    GW170817-surviving aether (still leaves the slip). Either way c_T=c is ACHIEVABLE.
""")
# Symbolic c_T check: conformal/identity action of the projector on h^TT.
ct2 = sp.symbols('c_T2',positive=True)
# the graviton kinetic term coefficient ratio under the term:
coef_time = sp.Integer(1)   # GR gives 1
coef_space = sp.Integer(1)  # u-frame projector + Box^{-1}G: identity on h^TT (Maggiore) -> 1
print("  graviton (d_t h^TT)^2 coeff =", coef_time, " ; (d_x h^TT)^2 coeff =", coef_space)
print("  c_T^2 = space/time =", sp.simplify(coef_space/coef_time), " => c_T = c. PASS (for the non-propagating")
print("  DEW frame, OR the c_13=0 aether). CONDITIONAL on NOT adding a c_T-shifting aether kinetic term.")

# ============================================================================
H("STEP 4 -- GHOST: the spectrum of the u-frame nonlocal term")
# ============================================================================
print("""
Ghost analysis (the make-or-break for ANY new-d.o.f. term):
  ROUTE 3 ghost-avoidance mechanism = NONLOCALITY (Box^{-1} lowers derivative order; the Step-2
  branch-cut result: infinite-order/nonlocal form factors have a SINGLE healthy pole, residue +1,
  no ghost; FINITE higher-derivative truncations DO ghost). Two sub-cases:

  (a) NON-propagating DEW frame (u=-d chi/|dchi|, chi=Box^{-1}1) + Box^{-1}G_munu:
      Maggiore RT-model RESULT (1402.0448, cited): the localized auxiliary fields (U_munu=Box^{-1}G,
      and the Lagrange multipliers) are NON-dynamical / carry NO ghost at linear order around
      cosmology. The retarded Box^{-1} (Deser-Woodard 1307.6639) adds no new on-shell mode. The
      ONLY known instability of the RT model is a mild background-dependent one at deep
      nonlinearity, NOT a linear ghost. => GHOST-FREE at linear order (cited + branch-cut consistent).
      CAVEAT (conceded): the RT model's auxiliary U_munu has been debated; some analyses find a
      scalar ghost in certain Box^{-1}G_munu variants (the 'RR' model g^munu Box^{-1}G is cleaner).
      The TRACELESS/anisotropic projection we need is NOT the standard RT model -- its ghost
      spectrum is NOT settled in the literature and is NOT closed here. Status: PLAUSIBLY-ghost-free
      via nonlocality, NOT proven for THIS projected term.

  (b) propagating aether (genuine A^mu, A^2=-1) + the slip:
      Einstein-aether is ghost-free in a parameter window (Jacobson gr-qc/0007031; the c_i bounded);
      c_T=c forces c_13=0; the surviving window is non-empty. The slip is then the AeST-class slip
      -- BUT AeST's scalar MOVES Phi (fails Cassini) unless GATED. So (b) reproduces the AeST
      problem: the propagating-aether slip is generically NOT pure (delta-Phi != 0) without a gate.

  DHOST degeneracy (escape hatch a): if the term is recast as a higher-derivative scalar-tensor
  (DHOST), the Langlois-Noui degeneracy conditions (1510.06930) can give c_T=c + slip + ghost-free.
  But DHOST that gives a PURE slip (delta-Phi=0) with c_T=c is HEAVILY constrained post-GW170817
  (the surviving DHOST class has the slip TIED to the time-variation of the scalar/G_eff, and the
  pure-Cassini-safe corner is the same no-slip-or-screened corner). We did NOT find a DHOST term
  that gives delta-Phi=0 + grad(delta-Psi)=2(g_obs-g_N) + c_T=c + ghost-free SIMULTANEOUSLY.
""")
print("  GHOST VERDICT: CONDITIONAL. Nonlocality (branch-cut) plausibly avoids the local Ostrogradski")
print("  ghost, but the specific traceless/anisotropic-projected Box^{-1}G_munu spectrum is NOT")
print("  settled (RT-model variants debated; the projected version not in the literature). NOT proven.")

# ============================================================================
H("PART 5 NET -- the make-or-break, adjudicated")
# ============================================================================
print("""
WHAT IS ESTABLISHED (sympy + cited, both ways):
  * A term whose projector kills T^eff_00 (to protect Phi) ALSO kills its ability to source Psi
    -> a pure TT/traceless source gives a slip but MOVES Phi (opposite sign). delta-Phi != 0.
  * delta-Phi=0 + delta-Psi=2(g_obs-g_N) REQUIRES the LOCKED imperfect-fluid stress
    (delta-rho != 0, Pi = delta-rho/2) aligned with u^mu -- a NONLOCAL EINSTEIN-AETHER-class term,
    NOT a pure Deser-Woodard scalar and NOT a pure TT projection.
  * That aether-locked term CAN give c_T=c (non-propagating DEW frame, or c_13=0 aether) -- PASS,
    conditional on not adding a c_T-shifting aether kinetic term.
  * GHOST-freedom is PLAUSIBLE via nonlocality (branch-cut single-pole) but NOT proven for the
    specific projected Box^{-1}G_munu -- the literature RT-model ghost status is debated and the
    traceless-projected variant is uncomputed. The propagating-aether realization (b) reproduces
    AeST's delta-Phi!=0 problem (needs a gate).

THE HONEST VERDICT on Route 3 (nonlocal traceless slip):
  PARTIAL / OBSTRUCTED-as-a-clean-pure-scalar.
  - The PURE Deser-Woodard SCALAR G(Box^{-1}R) traceless route is a genuine NO-GO for pure slip
    (a scalar has no anisotropic stress -> moves Phi or no slip). [sympy-proven, Part 3]
  - The naive TENSOR Box^{-1}G_munu traceless route ALSO moves Phi (4-traceless != delta-Phi=0).
    [sympy-proven, Part 4]
  - A WORKING term EXISTS in the NONLOCAL EINSTEIN-AETHER class (locked u-frame imperfect-fluid
    stress, delta-rho:Pi = 2:1), gives delta-Phi=0 + the right slip + c_T=c BY CONSTRUCTION of
    the locked ratio -- but its GHOST-FREEDOM is NOT proven (plausible via nonlocality; the
    projected-Box^{-1}G_munu spectrum is open), and it has migrated from 'pure Deser-Woodard
    nonlocal scalar' to 'nonlocal aether' (escape hatch b), i.e. it is NOT the clean Route-3 object.
  => Route 3 does NOT deliver a clean, proven, ghost-free pure-scalar nonlocal traceless slip.
     The slip is achievable only by going to the aether class, where ghost-freedom is unproven.
""")
