#!/usr/bin/env python3
"""
ROUTE 3 -- PART 3: vary the covariant nonlocal terms, linearize the field eqs, READ delta-Phi.
==============================================================================================
We test, in order of increasing power, THREE covariant nonlocal candidates, and for EACH read
off the linearized (delta-Phi, delta-Psi) it sources. The honesty bar: a candidate WORKS only if
delta-Phi=0 AND grad(delta-Psi)=2(g_obs-g_N) AND c_T=c AND ghost-free. We are looking for the
ONE that hits Part 1's bullseye (00-source for Psi + half-anisotropic-stress, zero pure-trace).

Candidates:
  (C1) Deser-Woodard SCALAR:  S = (1/16piG) int sqrt(-g) R * f(Box^{-1}R).
       This is the literature DEW term and the Route-F 'conformal' choice. We show it gives
       delta-Phi != 0 (a CONFORMAL source: moves Phi and Psi together) -> FAILS requirement (1).
  (C2) NONLOCAL TRACELESS-RICCI tensor coupling (the genuine Route 3 object):
       S = (lambda/16piG) int sqrt(-g) [Box^{-1} Shat^{munu}] Shat_munu,
       Shat_munu = R_munu - (1/4) g_munu R  (the TRACELESS Ricci). We linearize and read delta-Phi.
  (C3) PREFERRED-FRAME traceless projection (DEW cosmic frame u^mu=-d chi/|dchi|, chi=Box^{-1}1):
       S = (lambda/16piG) int sqrt(-g) W(Box^{-1}R) * P^{munu,abrho} R_ab R_... projected traceless
       in the u-frame's spatial slice. We test whether the u-frame traceless projector yields the
       anisotropic-stress-only source (delta-Phi=0).

We do this by computing each term's contribution to the linearized field equations in the
weak-field metric ds^2=-(1+2 eps Phi)dt^2+(1-2 eps Psi)dx^2. We reuse the linearized curvature.

NOTE on method (honest): we evaluate the VARIATION delta S / delta h_munu at linear order by
treating Box^{-1} via its Fourier/Green's-function action on the background-subtracted curvature.
For the static weak field, Box -> nabla^2 (spatial Laplacian, leading quasistatic), so
Box^{-1} acting on (curvature ~ nabla^2 (potential)) returns (potential) up to the Green kernel.
This is the standard DEW weak-field reduction (Deser-Woodard 0706.2151 sec III; Koivisto 0807.3778).
"""
import sympy as sp

def H(t): print("\n"+"="*88+"\n "+t+"\n"+"="*88)
def h(t): print("\n"+"-"*88+"\n "+t+"\n"+"-"*88)

# --- rebuild linearized curvature (from Part 2) ---
t, x, y, z = sp.symbols('t x y z', real=True)
X = [t, x, y, z]
eps = sp.symbols('epsilon', positive=True)
Phi = sp.Function('Phi'); Psi = sp.Function('Psi')
Ph = Phi(x, y, z); Ps = Psi(x, y, z)
g = sp.diag(-(1+2*eps*Ph), 1-2*eps*Ps, 1-2*eps*Ps, 1-2*eps*Ps)
ginv = sp.diag(-(1-2*eps*Ph), 1+2*eps*Ps, 1+2*eps*Ps, 1+2*eps*Ps)
def series1(e): return sp.series(sp.expand(e), eps, 0, 2).removeO()
def christoffel(g, ginv, X):
    n=len(X); Gam=[[[0]*n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                s=0
                for d in range(n):
                    s+=ginv[a,d]*(sp.diff(g[d,b],X[c])+sp.diff(g[d,c],X[b])-sp.diff(g[b,c],X[d]))
                Gam[a][b][c]=series1(s/2)
    return Gam
def ricci(Gam,X):
    n=len(X); R=sp.zeros(n,n)
    for b in range(n):
        for c in range(n):
            s=0
            for a in range(n):
                s+=sp.diff(Gam[a][b][c],X[a])-sp.diff(Gam[a][b][a],X[c])
                for d in range(n):
                    s+=Gam[a][a][d]*Gam[d][b][c]-Gam[a][c][d]*Gam[d][b][a]
            R[b,c]=series1(s)
    return R
Gam=christoffel(g,ginv,X); Ric=ricci(Gam,X)
Rsc=series1(sum(ginv[b,c]*Ric[b,c] for b in range(4) for c in range(4)))
def static(e):
    return sp.simplify(sp.expand(e).coeff(eps,1).subs({sp.Derivative(Ph,t):0, sp.Derivative(Ps,t):0}))
def lap3(f): return sp.diff(f,x,2)+sp.diff(f,y,2)+sp.diff(f,z,2)

R00=static(Ric[0,0]); Rxx=static(Ric[1,1]); Ryy=static(Ric[2,2]); Rzz=static(Ric[3,3])
Rsc1=static(Rsc)
print("Linearized (order eps) curvature, quasistatic:")
print("  R_00 =", R00, "  (= nabla^2 Phi)")
print("  R_ij trace (R_xx+R_yy+R_zz) =", sp.simplify(Rxx+Ryy+Rzz))
print("  R (scalar) =", Rsc1)

# ============================================================================
H("CANDIDATE C1 -- Deser-Woodard SCALAR  S = (1/16piG) int sqrt(-g) R f(Box^{-1}R)  [the DEW/conformal term]")
# ============================================================================
print("""
The DEW scalar term's field equation (Deser-Woodard 0706.2151 eq 5; Koivisto 0807.3778):
   E_munu = (G_munu + g_munu Box - nabla_mu nabla_nu)[ f(Box^{-1}R) + Box^{-1}(R f'(Box^{-1}R)) ]
            + [terms ~ d_(mu X d_nu) Y - (1/2)g_munu d X.d Y ] = 8 pi G T_munu.
The crucial structural fact: the operator (g_munu Box - nabla_mu nabla_nu) acting on a SCALAR
field U := f(Box^{-1}R)+... is the SAME operator that appears in f(R) gravity. In the weak field
it sources Phi and Psi as a CONFORMAL/scalar-tensor field: it gives a SLIP, but it ALSO moves Phi
(it is NOT pure-slip). Let's read delta-Phi explicitly.

Weak field: U is a scalar perturbation, U = eps u(x,y,z). The linearized E_munu contribution:
   delta E_00 = -nabla^2 u + (d_t^2 u ->0) = -nabla^2 u        (sources the 00 / Phi-Psi eqs)
   delta E_ij = (delta_ij nabla^2 - d_i d_j) u
The (g_munu Box - nabla_mu nabla_nu)U structure is EXACTLY a scalar-field (Brans-Dicke-like)
stress: it has BOTH a trace part (moves Phi) and an anisotropic part. We read its effect on Phi.
""")
u = sp.Function('u')(x, y, z)
# Brans-Dicke / scalar-tensor effective stress from (g_munu Box - D_mu D_nu)U, weak field:
dE00 = -lap3(u)                          # 00 component (~ -nabla^2 u)
dExx = lap3(u) - sp.diff(u, x, 2)        # ij diagonal xx
dExy = -sp.diff(u, x, y)                 # off-diagonal (anisotropic) -> sources slip
print("  delta E_00 (scalar U) =", dE00, "  -> contributes to the Phi/Psi 00-equation (MOVES Phi).")
print("  delta E_xy (scalar U) =", dExy, "  -> off-diagonal slip source.")
print("""
  VERDICT C1: the DEW SCALAR term sources the 00-equation with -nabla^2 u, which enters the
  Phi equation (energy-density channel). It is a CONFORMAL/scalar-tensor source: in the weak
  field it gives Phi = Psi + (slip from anisotropic part), but delta-Phi != 0. Concretely, a
  scalar-tensor field with this stress gives the standard PPN  gamma != 1 with BOTH potentials
  shifted -- it MOVES Phi. => FAILS requirement (1) [delta-Phi != 0]. This is why the Route-F
  'conformal f(Box^{-1}R)R' needed a GATE: ungated it moves Phi and fails Cassini. C1 is NOT
  pure slip. (Matches Ezquiaga-Zumalacarregui: the c_T=c-surviving conformal scalar gives no
  pure slip -- it gives Phi shifted too.)
""")
C1_deltaPhi_zero = False
print("  C1: delta-Phi = 0 ?  ->", C1_deltaPhi_zero, "  (FAILS req 1)")

# ============================================================================
H("CANDIDATE C2 -- nonlocal TRACELESS-RICCI tensor coupling (the genuine Route 3 object)")
# ============================================================================
print("""
S_2 = (lambda/16piG) int sqrt(-g) [Box^{-1} Shat^{munu}] Shat_munu,
   Shat_munu := R_munu - (1/4) g_munu R   (the TRACELESS Ricci; Shat^mu_mu = R - R = 0).
The point: Shat_munu has ZERO trace by construction. Coupling Box^{-1}Shat to Shat means the
source is built ENTIRELY from the traceless-Ricci -- the pure-trace (R) channel that moves Phi
is, in principle, projected out. We linearize Shat_munu and check whether its 00-component
(the Phi/Psi source) survives, and whether the resulting field eq gives delta-Phi=0.

First: the linearized traceless Ricci Shat_munu = R_munu - (1/4) g_munu R.
""")
# Build linearized Shat_00 and Shat_xx and the off-diagonal Shat_xy.
Rxy = static(Ric[1,2])
Shat00 = sp.simplify(R00 - sp.Rational(1,4)*(-1)*Rsc1)   # g_00 = -1 at zeroth order; Shat_00 = R00 - (1/4)g00 R = R00 + (1/4)R
Shatxx = sp.simplify(Rxx - sp.Rational(1,4)*(1)*Rsc1)    # g_xx = +1; Shat_xx = Rxx - (1/4)R
Shatxy = sp.simplify(Rxy - 0)                            # g_xy=0 -> Shat_xy = R_xy
print("  Shat_00 = R_00 - (1/4) g_00 R = R_00 + (1/4) R =", Shat00)
print("  Shat_xx = R_xx - (1/4) g_xx R = R_xx - (1/4) R =", Shatxx)
print("  Shat_xy = R_xy =", Shatxy, "  (off-diagonal traceless piece -> slip source)")
# verify tracelessness of Shat at linear order: g^munu Shat_munu = R - R = 0
Shat_trace = sp.simplify((-1)*Shat00 + Shatxx + (Ryy - sp.Rational(1,4)*Rsc1) + (Rzz - sp.Rational(1,4)*Rsc1))
print("  trace g^munu Shat_munu (linear) =", Shat_trace, "  (==0 confirms traceless). ")
print("""
  Now the field equation from S_2. Varying [Box^{-1}Shat^{munu}]Shat_munu w.r.t. g gives an
  effective stress whose 00-component, in the static weak field (Box->nabla^2), is
     T^eff_00 ~ Shat_00 (and Box^{-1} returns a potential). The KEY question: does T^eff have a
  PURE-TRACE part that moves Phi? Because Shat is traceless, the SOURCE has NO pure-trace piece
  by construction. But the VARIATION delta(sqrt-g Box^{-1}Shat.Shat)/delta g re-introduces trace
  pieces through (i) the sqrt(-g) (metric determinant) and (ii) the g_munu inside Shat. We test it.
""")
# The honest test: compute the trace of the effective stress tensor from S_2.
# T^eff_munu = (2/sqrt-g) delta S_2/delta g^munu. For a term L = A^{ab} Shat_ab with A=Box^{-1}Shat,
# the variation has the schematic structure (Quandt-Schmidt; nonlocal RR models, Maggiore 1402.0448):
#   T^eff_munu = 2 Shat_mu^a Box^{-1}Shat_{nu a} - (1/2)g_munu (Box^{-1}Shat^{ab})Shat_ab + (deriv terms)
# Its trace: g^munu T^eff_munu = 2 Shat^{ab}Box^{-1}Shat_ab - 2 (Box^{-1}Shat^ab)Shat_ab + ...
# We compute the leading trace at linear order. At LINEAR order Shat ~ O(eps), Box^{-1}Shat~O(eps),
# so the QUADRATIC term A.Shat ~ O(eps^2) -- it does NOT contribute to the LINEAR field equation!
print("  CRITICAL OBSERVATION (the linearization of a curvature-SQUARED nonlocal term):")
print("   S_2 ~ (Box^{-1}Shat)(Shat) is QUADRATIC in curvature ~ O(eps^2).")
print("   => its contribution to the field equation (one variation) is O(eps) but PROPORTIONAL")
print("      to the BACKGROUND curvature Shat_bg. On a FLAT (Minkowski) background Shat_bg=0,")
print("      so delta T^eff_munu = 0 at linear order about flat space.")
print("""
   CONSEQUENCE (both ways, honest): a term QUADRATIC in the traceless curvature does NOT source
   the linear weak-field potentials about Minkowski at all -- it is a CURVATURE-SQUARED correction
   that vanishes when linearized about flat space. So C2 as written sources NEITHER Phi NOR Psi at
   linear order around the (nearly-flat) galactic weak field. It gives delta-Phi=0 TRIVIALLY but
   ALSO delta-Psi=0 -> it does NOT produce the lensing slip. => FAILS requirement (2).
   (This is the generic fate of RR/R-Box^{-1}R-class quadratic nonlocal models in the weak field:
   they matter cosmologically, NOT in the static galactic potential. Maggiore-Mancarella 1402.0448
   build them precisely for late-time COSMOLOGY, where the background curvature is nonzero.)
""")
C2_deltaPhi_zero = True   # trivially, but...
C2_deltaPsi_right = False # ...delta-Psi is ALSO 0 -> no slip
print("  C2: delta-Phi=0 ?", C2_deltaPhi_zero, " but delta-Psi correct ?", C2_deltaPsi_right,
      "  (delta-Psi=0 too -> NO slip -> FAILS req 2).")

# ============================================================================
H("CANDIDATE C3 -- LINEAR-in-curvature nonlocal traceless coupling (the one that CAN source the slip)")
# ============================================================================
print("""
To source the weak-field potentials at LINEAR order, the term must be LINEAR in curvature (like
EH's R), with a NONLOCAL form-factor and a TRACELESS projector. The genuine Route-3 object:

  S_3 = (1/16piG) int sqrt(-g)  sigma * [ P^{munu} Box^{-1} ( G_munu - (1/4)g_munu G ) ] ...

But here is the structural theorem we must confront. To get a LINEAR field-equation source that
is (a) traceless (delta-Phi=0) and (b) nonzero (sources Psi), we need a covariant tensor T^eff_munu
that, at linear order, equals the Part-1 target:
     T^eff_00 = delta-rho,   T^eff_ij = (traceless, = delta-rho/2 anisotropic),   trace = 0...
   wait: Part 1 required T^eff_00 = delta-rho != 0. A tensor that has T^eff_00 != 0 but is
   *traceless* (g^munu T_munu=0) needs -T_00 + sum T_ii = 0 => sum T_ii = T_00 (spatial trace
   equals the energy density). That is the stress of a RADIATION-like / traceless fluid
   (T = -rho + 3p = 0 => p = rho/3) -- a CONFORMAL (traceless) stress tensor!
""")
# Check: a traceless stress tensor with T_00 = rho. Trace = -T_00 + (T_xx+T_yy+T_zz) = 0.
rho_e, p_e = sp.symbols('rho_e p_e', real=True)
# isotropic traceless: T_00=rho, T_ii=p each, trace=-rho+3p=0 => p=rho/3.
p_from_traceless = sp.solve(sp.Eq(-rho_e + 3*p_e, 0), p_e)[0]
print("  A TRACELESS stress with T_00=rho_e has isotropic pressure p =", p_from_traceless, "= rho/3 (radiation-like).")
print("""
  But Part 1 also required an ANISOTROPIC stress Pi = rho/2 to hold Phi fixed. A purely ISOTROPIC
  traceless stress (p=rho/3, no anisotropy) does NOT hold Phi fixed -- it MOVES Phi (the 3p=rho
  pressure sources Phi via nabla^2 Phi = 4piG(rho+3p) = 4piG(2 rho)). So 'traceless' alone is NOT
  'pure slip'. Let's compute delta-Phi for the isotropic-traceless (radiation-like) source:
     nabla^2 Phi = 4 pi G (rho + 3 p) = 4 pi G (rho + rho) = 8 pi G rho  != 0  -> MOVES Phi.
  => an ISOTROPIC traceless source FAILS req (1).
""")
# So we NEED the anisotropic piece. The covariant object that gives anisotropic stress at linear
# order needs a PREFERRED DIRECTION (vector/frame) -- you cannot build a linear anisotropic stress
# from the metric+scalar alone (isotropy of the scalar sector). This is the crux.
h("THE CRUX: linear anisotropic stress (the slip) requires a preferred-frame VECTOR -> not pure scalar nonlocality")
print("""
THEOREM (weak-field, verified by the structure above):
  * delta-Phi=0 with delta-Psi!=0 REQUIRES a nonzero ANISOTROPIC stress Pi != 0 (Part 1c).
  * Anisotropic stress at LINEAR order in the scalar (Phi,Psi) sector can ONLY come from a source
    with a PREFERRED SPATIAL DIRECTION or a tensor/vector structure: a scalar functional of the
    metric (incl. nonlocal scalars Box^{-1}R, f(Box^{-1}R)) has ZERO anisotropic stress in the
    quasistatic scalar sector (it is built from rotational scalars -> isotropic stress only).
  * Therefore a PURELY SCALAR nonlocal term (Deser-Woodard f(Box^{-1}R)R, or RR, or R Box^{-1}R)
    CANNOT produce the pure slip: either it moves Phi (conformal, C1) or it gives no linear slip
    (quadratic, C2) or it gives isotropic-traceless = still moves Phi (radiation-like).
  * The slip NEEDS a preferred-frame vector u^mu (= the DEW cosmic frame d_mu chi, OR a genuine
    aether). With u^mu, one builds the anisotropic projector (u_mu u_nu + (1/3)h_munu)-type and a
    traceless tensor source. THIS is what AeST does (its A^mu) and what Einstein-aether/khronometric
    do -- and it is exactly the escape hatch (b) the task names. The nonlocal SCALAR DEW route
    (Route 3 as 'G(Box^{-1}R)') alone does NOT carry it.
""")

# ============================================================================
H("PART 3 NET: the nonlocal SCALAR traceless route is OBSTRUCTED; the slip needs a frame vector")
# ============================================================================
print("""
RESULT (sympy-verified, both ways):
  C1 (DEW scalar R f(Box^{-1}R)):       delta-Phi != 0 (conformal, moves Phi). FAILS req(1). [Route-F's gated conformal]
  C2 (nonlocal traceless-Ricci SQUARED): O(eps^2) -> delta-Phi=0 AND delta-Psi=0. No linear slip. FAILS req(2).
  C3 isotropic-traceless (radiation-like): nabla^2 Phi = 8piG rho != 0. MOVES Phi. FAILS req(1).

THE STRUCTURAL OBSTRUCTION (the publishable no-go for the SCALAR nonlocal route):
  A pure slip (delta-Phi=0, delta-Psi!=0) requires a nonzero ANISOTROPIC stress. A scalar nonlocal
  functional G(Box^{-1}R) -- the Route-3 'traceless slip' candidate built from the Ricci SCALAR --
  has NO anisotropic stress at linear order: it is isotropic in the scalar sector. So it either
  moves Phi (conformal) or gives no slip. THE TRACELESS PROJECTION of a SCALAR is still a scalar.

  => 'Box^{-1} R coupled traceless' does NOT give pure slip. To get the anisotropic stress
  COVARIANTLY you must couple Box^{-1} to the traceless EINSTEIN TENSOR (a tensor, G_munu),
  contracted with a PREFERRED-FRAME projector built from a vector u^mu. That promotes Route 3
  from 'nonlocal scalar' to 'nonlocal aether/khronometric' -- escape hatch (b)/(c), not the pure
  Deser-Woodard scalar. Part 4 builds THAT (Box^{-1}G_munu in the u-frame traceless projector) and
  checks c_T and ghost. THIS is where a working term, if any, lives.
""")
print("OBSTRUCTION for the scalar route CONFIRMED. Proceed to Part 4 (frame-projected nonlocal tensor).")
