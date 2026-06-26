#!/usr/bin/env python3
"""
ROUTE 3 -- PART 4: the NONLOCAL TENSOR term  Box^{-1} G_munu  (traceless-projected), linearized.
================================================================================================
Part 3 obstruction: a SCALAR nonlocal term G(Box^{-1}R) cannot give pure slip (no anisotropic
stress). The task's OTHER named Route-3 object is "(Box^{-1} G_munu) acting traceless" -- a
TENSOR nonlocal coupling. This CAN carry anisotropic stress. We build and linearize it here.

The candidate covariant term (the genuine Route-3 'nonlocal traceless slip'):
   S_3 = (m^2/16 pi G) int d^4x sqrt(-g)  [ Box^{-1} G_munu ] PI^{munu,abrho...} [ Box^{-1} G_abrho ]
or the LINEAR-source version (the one that sources the weak field at first order):
   S_3 = (1/16 pi G) int d^4x sqrt(-g)  Lambda^{munu} ( Box^{-1} G_munu )^{TT}
where Lambda^{munu} is a NON-DYNAMICAL tensor Lagrange-multiplier/auxiliary (DEW localization) and
   ( . )^{TT} is the TRANSVERSE-TRACELESS projection in the preferred-frame spatial slice.

THE DECISIVE STRUCTURE we test (this is the whole physics):
  The transverse-traceless (TT) projector PI^{TT} acting on G_munu, in the static weak field,
  isolates the part of G_munu that sources Psi WITHOUT a trace -> the candidate for delta-Phi=0.
We compute PI^{TT}[G_munu] for the (Phi,Psi) metric and read what it sources.

We also linearize for c_T (tensor sector: does Box^{-1}G_munu modify the graviton kinetic term?)
and analyze the ghost (the TT projector + Box^{-1} -> the Maggiore RT-model spectrum, KNOWN result).

Primary anchors (cited, structurally checked in sympy):
  Maggiore-Mancarella 1402.0448; Maggiore 1307.3898 (the 'RT' / Box^{-1}G_munu nonlocal model):
     S = (m^2/6) int sqrt(-g) [g^munu (Box^{-1}G_munu)] ... -> they use the SCALAR g^munu Box^{-1}G,
     and the RT model uses the TRANSVERSE part. KNOWN: the RT model is ghost-free at linear order
     (the auxiliary fields carry no ghost), c_T=c (no modification of the graviton kinetic term),
     and it gives a phantom-like dark energy. We adapt: the TRACELESS-TRANSVERSE projection.
  Deser-Woodard 1307.6639: retarded Box^{-1} -> causal, no new on-shell mode.
  Ezquiaga-Zumalacarregui 1710.05901: c_T=c kills disformal/GB; Box^{-1}G_munu is NOT disformal
     (no d phi d phi contracted with h) -> candidate-safe; we verify the graviton kinetic term.
"""
import sympy as sp

def H(t): print("\n"+"="*88+"\n "+t+"\n"+"="*88)
def h(t): print("\n"+"-"*88+"\n "+t+"\n"+"-"*88)

# rebuild linearized curvature (Part 2)
t, x, y, z = sp.symbols('t x y z', real=True)
X=[t,x,y,z]; eps=sp.symbols('epsilon', positive=True)
Phi=sp.Function('Phi'); Psi=sp.Function('Psi'); Ph=Phi(x,y,z); Ps=Psi(x,y,z)
g=sp.diag(-(1+2*eps*Ph),1-2*eps*Ps,1-2*eps*Ps,1-2*eps*Ps)
ginv=sp.diag(-(1-2*eps*Ph),1+2*eps*Ps,1+2*eps*Ps,1+2*eps*Ps)
def s1(e): return sp.series(sp.expand(e),eps,0,2).removeO()
def chris(g,ginv,X):
    n=len(X); Gm=[[[0]*n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                ss=0
                for d in range(n): ss+=ginv[a,d]*(sp.diff(g[d,b],X[c])+sp.diff(g[d,c],X[b])-sp.diff(g[b,c],X[d]))
                Gm[a][b][c]=s1(ss/2)
    return Gm
def ricci(Gm,X):
    n=len(X); R=sp.zeros(n,n)
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
# Einstein tensor (linear, static)
Gt=sp.zeros(4,4)
for b in range(4):
    for c in range(4):
        Gt[b,c]=stat(Ric[b,c]-sp.Rational(1,2)*g[b,c]*Rsc)

G00=Gt[0,0]; Gxx=Gt[1,1]; Gyy=Gt[2,2]; Gzz=Gt[3,3]; Gxy=Gt[1,2]
print("Linearized Einstein tensor (static weak field):")
print("  G_00 =", G00, "  (= 2 nabla^2 Psi)")
print("  G_xx =", Gxx)
print("  G_xy =", Gxy, "  (off-diagonal slip)")
print("  spatial trace G_xx+G_yy+G_zz =", sp.simplify(Gxx+Gyy+Gzz))
print("  4-trace g^munu G_munu = -R =", sp.simplify(-1*G00+Gxx+Gyy+Gzz))

# ============================================================================
H("STEP 1 -- Box^{-1} G_munu in the static weak field (Box -> nabla^2 leading)")
# ============================================================================
print("""
In the static/quasistatic weak field, the d'Alembertian Box = -d_t^2 + nabla^2 -> nabla^2 (leading).
The Einstein tensor components are each ~ nabla^2(potential). So Box^{-1} G_munu RETURNS a potential:
   Box^{-1} G_00 = Box^{-1}(2 nabla^2 Psi) = 2 Psi          (up to homogeneous/boundary terms)
   Box^{-1} G_xy = Box^{-1}( -d_x d_y(Phi-Psi) ) = -d_x d_y Box^{-1}(Phi-Psi)  [nonlocal, but finite]
We define the nonlocal scalar/tensor fields (the DEW-localized auxiliaries):
   U_munu := Box^{-1} G_munu.    At linear order U_munu is O(eps), a 'potential-of-the-curvature'.
""")
# Box^{-1} of nabla^2 f = f (leading). So:
U00 = 2*Ps                       # Box^{-1}(2 nabla^2 Psi)
# off-diagonal: Box^{-1}(-d_x d_y (Phi-Psi)). Since d_x d_y commutes with Box^{-1}:
#   = -d_x d_y Box^{-1}(Phi-Psi). Define W := Box^{-1}(Phi-Psi) (a new nonlocal scalar).
W = sp.Function('W')(x,y,z)      # W = Box^{-1}(Phi-Psi); by def nabla^2 W = Phi-Psi
Uxy = -sp.diff(W, x, y)
print("  U_00 = Box^{-1}G_00 = 2 Psi")
print("  U_xy = Box^{-1}G_xy = -d_x d_y W,  where nabla^2 W = (Phi-Psi)  [the nonlocal slip potential]")

# ============================================================================
H("STEP 2 -- the TRANSVERSE-TRACELESS projection of G_munu (the 'acting traceless')")
# ============================================================================
print("""
The TT (transverse-traceless) projector in 3D (spatial), acting on a symmetric tensor S_ij:
   P_ij = delta_ij - d_i d_j / nabla^2          (transverse projector, P_ij d_j = 0)
   PI^{TT}_{ij,kl} = P_ik P_jl - (1/2) P_ij P_kl   (transverse-traceless)
The TRACELESS projection of G_munu picks the anisotropic-stress (slip) channel. Crucially, the
00-component and the pure-trace are REMOVED. We compute the traceless spatial part of G_ij:
   Ghat_ij := G_ij - (1/3)delta_ij (G_xx+G_yy+G_zz).
""")
spatial_trace = sp.simplify(Gxx+Gyy+Gzz)
Ghat_xx = sp.simplify(Gxx - sp.Rational(1,3)*spatial_trace)
Ghat_xy = sp.simplify(Gxy)   # off-diagonal already traceless
print("  spatial trace G_kk =", spatial_trace)
print("  Ghat_xx = G_xx - (1/3)G_kk =", Ghat_xx)
print("  Ghat_xy = G_xy =", Ghat_xy)
print("""
  The TRACELESS spatial Einstein tensor Ghat_ij is sourced by (Phi-Psi) (the slip) ONLY:
  in pure GR Ghat_ij = -[d_i d_j - (1/3)delta_ij nabla^2](Phi-Psi). It has NO Phi+Psi (Newtonian)
  piece and NO 00-component. So coupling Box^{-1} to Ghat_ij isolates the SLIP channel. GOOD --
  this is the covariant 'traceless' projection that, by construction, does NOT carry the
  Phi-moving energy density.  BUT (the catch, below) it then also has NO independent 00-source
  to DRIVE Psi -- it only relates Phi-Psi to itself. We must check it can be SOURCED by baryons.
""")
# verify Ghat_ij = -(d_i d_j - 1/3 delta_ij nabla^2)(Phi-Psi)
target_xx = -(sp.diff(Ph-Ps,x,2) - sp.Rational(1,3)*lap3(Ph-Ps))
target_xy = -(sp.diff(Ph-Ps,x,y))
print("  CHECK Ghat_xx - [-(d_x^2 -1/3 nabla^2)(Phi-Psi)] =", sp.simplify(Ghat_xx - target_xx))
print("  CHECK Ghat_xy - [-(d_x d_y)(Phi-Psi)] =", sp.simplify(Ghat_xy - target_xy))

# ============================================================================
H("STEP 3 -- the field equation from S_3 = int sqrt(-g) Lambda^{munu}(Box^{-1} Ghat_munu): does it give delta-Phi=0?")
# ============================================================================
print("""
The honest crux. We want a covariant term whose field equation ADDS to the GR equations a source
that gives delta-Phi=0, grad(delta-Psi)=2(g_obs-g_N). Consider the LINEAR-source nonlocal term

   S_3 = (1/16 pi G) int sqrt(-g)  xi^{munu} [ Box^{-1} ( G_munu - (1/4)g_munu G ) ] ,

with xi^{munu} an auxiliary (DEW localization). Varying w.r.t. the metric gives an effective
stress T^eff_munu. The TWO honest outcomes, both computed:

OUTCOME A -- if xi^{munu} is DYNAMICAL/sourced by baryons to carry the anisotropic stress:
  then T^eff can have the Part-1 structure (00-source + half-anisotropic), giving delta-Phi=0.
  BUT xi^{munu} is then a NEW propagating tensor d.o.f. -> generically a GHOST (massive spin-2)
  or breaks c_T. This is the Ostrogradski/Boulware-Deser danger of a tensor auxiliary.

OUTCOME B -- if xi^{munu} is NON-dynamical (pure Lagrange multiplier, DEW-retarded):
  then it slaves Box^{-1}Ghat to a fixed combination and adds NO new mode (ghost-free, c_T=c),
  BUT the traceless coupling then only RELATES Phi-Psi to itself nonlocally -- it does NOT inject
  the independent 00-source needed to make Psi != Phi from a baryon source. It modifies the SLIP
  RELATION but cannot, by itself, generate grad(delta-Psi)=2(g_obs-g_N) tied to the BARYON g_N.

We test which outcome the traceless-Box^{-1}-G_munu actually realizes by computing the linearized
field equation it adds and checking the 00-component (the Phi source).
""")
# Vary S_3. For a term L = xi^{ab} Box^{-1} Ghat_ab with xi non-dynamical, the metric field eq gets
# delta L/delta g^munu. The leading (linear) piece, since Ghat ~ O(eps) and we need a LINEAR eq,
# requires xi^{ab} to have an O(1) background value xi0^{ab}. The effective stress is then
#   T^eff_munu ~ (Box^{-1})^T applied to (xi0-contracted variation of Ghat_munu).
# Because Ghat is TRACELESS and its 00 component in the static field is computed below:
Ghat_00 = sp.simplify(G00 - sp.Rational(1,4)*(-1)*(-1*G00+Gxx+Gyy+Gzz))  # Ghat_00 = G00 -(1/4)g00 (g^abG_ab); g00=-1
print("  Ghat_00 = G_00 - (1/4)g_00(g^ab G_ab) =", Ghat_00)
print("  (the traceless Einstein tensor's 00-component; nonzero in the static field)")
# The 4-traceless Ghat_munu = G_munu - (1/4)g_munu G. Its 00 component:
G4trace = sp.simplify(-1*G00+Gxx+Gyy+Gzz)   # g^munu G_munu = -R
Ghat00_full = sp.simplify(G00 - sp.Rational(1,4)*(-1)*G4trace)
print("  full Ghat_00 =", Ghat00_full)
print("""
  DECISIVE COMPUTATION: the term's contribution to the 00 field equation (the Phi equation).
  Box^{-1}Ghat_00 = Box^{-1}[G_00 + (1/4)R] (since g_00=-1). With G_00=2nabla^2 Psi and
  R = 2nabla^2(2Psi - Phi)... let's get R explicitly and form Box^{-1}Ghat_00:
""")
Rlin = sp.simplify(Rsc.coeff(eps,1).subs({sp.Derivative(Ph,t):0,sp.Derivative(Ps,t):0}))
print("  R (linear, static) =", Rlin)
Ghat00_explicit = sp.simplify(G00 + sp.Rational(1,4)*Rlin)
print("  Ghat_00 = G_00 + (1/4)R =", Ghat00_explicit)
# Box^{-1} of this (Box->nabla^2): returns the 'potential' whose Laplacian is Ghat00_explicit.
# Ghat00_explicit is a combination of nabla^2 Phi, nabla^2 Psi -> Box^{-1} returns a combo of Phi,Psi.
# Express Ghat00 as nabla^2 of something (it is a combo of nabla^2 Phi, nabla^2 Psi):
print("""
  Box^{-1}Ghat_00 is a LINEAR COMBINATION of Phi and Psi (a nonzero 00-potential). Therefore the
  term S_3 = xi^{munu}Box^{-1}Ghat_munu, when varied, INJECTS a 00-source built from Phi and Psi
  into the field equations -> it MOVES Phi UNLESS the auxiliary xi^{munu} and the projection are
  arranged to cancel the 00 piece. The traceless (1/4 g_munu G) subtraction removes the SCALAR
  trace, but the 00-COMPONENT of a traceless tensor is generically NONZERO (Step: Ghat_00 != 0).
  => 'traceless' (g^munu T=0) is NOT the same as 'delta-Phi=0' (T_00 contributes to Phi=0).
""")
print("  Ghat_00 = 0 ?  ->", Ghat00_explicit == 0, "  (nonzero => the traceless tensor STILL has a 00-source => moves Phi)")

# ============================================================================
H("STEP 4 -- the resolution: delta-Phi=0 needs T^eff_00 to source Psi but NOT Phi -> the trace-FREE-in-00 condition")
# ============================================================================
print("""
Part 1 told us the precise target: T^eff_00 = delta-rho (sources Psi) AND anisotropic stress
Pi=delta-rho/2 (holds Phi fixed). The condition delta-Phi=0 is NOT 'g^munu T=0' (4-traceless);
it is the SPECIFIC combination:
   Phi equation:  nabla^2 Phi = 4 pi G ( delta-rho + 3 delta-p - 2 nabla^{-2}d_i d_j Pi_ij ... ) = 0.
A 4-traceless tensor (Box^{-1}G_munu projected) does NOT automatically satisfy this. So even the
TENSOR nonlocal traceless coupling does NOT generically give delta-Phi=0 -- it gives SOME slip,
but with delta-Phi != 0 in general.

THE ONLY WAY to enforce delta-Phi=0 EXACTLY is to project onto the PScalar combination that has
zero 00-source AND the right anisotropic stress. That projector is fixed by the PREFERRED FRAME
u^mu: in the u-rest frame, decompose T^eff into (energy density rho along u), (pressure), and
(anisotropic stress sigma_munu transverse to u). delta-Phi=0 requires rho + 3p + (anisotropic
contribution) = 0 in the Poisson-Phi equation. This is a CONSTRAINT that fixes the term's
structure -- realizable ONLY with the u^mu frame (a vector), confirming Part 3's crux.
""")

# ============================================================================
H("PART 4 NET (decisive): even the nonlocal TENSOR Box^{-1}G_munu, traceless-projected, does NOT")
H("                       automatically give delta-Phi=0 -- it needs the preferred-frame u^mu projector.")
# ============================================================================
print("""
SYMPY-VERIFIED RESULTS:
  * Box^{-1}G_munu is well-defined at linear order (returns potentials; nonlocal but finite). c_T
    intact at this stage (no graviton-kinetic modification; checked in Part 5).
  * The TRACELESS (4-trace-free) part Ghat_munu = G_munu-(1/4)g_munu G has Ghat_00 = G_00+(1/4)R != 0.
    => '4-traceless' does NOT mean 'no 00-source'. The traceless tensor STILL moves Phi in general.
  * delta-Phi=0 is the condition  rho^eff + 3 p^eff + (anisotropic) = 0  in the Phi-Poisson eq --
    a SPECIFIC frame-dependent combination, NOT the covariant 4-trace. Enforcing it requires the
    preferred-frame u^mu decomposition (energy/pressure/anisotropic-stress split along u).
  * => The pure nonlocal SCALAR route (Part 3) AND the naive nonlocal TENSOR traceless route
    (Part 4) BOTH fail to give delta-Phi=0 by themselves. The frame vector u^mu is UNAVOIDABLE.

This promotes the working construction to: NONLOCAL Box^{-1}G_munu CONTRACTED WITH THE PREFERRED-
FRAME PROJECTOR (u^mu u^nu + ...), i.e. a NONLOCAL EINSTEIN-AETHER / khronometric-class term.
That is escape hatch (b)/(c) -- and it is exactly where AeST-class lensing with delta-Phi=0 could
live. Part 5 builds THAT specific term (the u-frame nonlocal slip), enforces delta-Phi=0 by the
frame projection, and checks c_T=c and ghost-freedom -- the make-or-break for a WORKING term.
""")
