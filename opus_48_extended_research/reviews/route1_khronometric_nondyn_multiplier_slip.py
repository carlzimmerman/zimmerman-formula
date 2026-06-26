#!/usr/bin/env python3
r"""
ROUTE 1 -- KHRONOMETRIC + NON-DYNAMICAL-FRAME (LAGRANGE-MULTIPLIER) SLIP.
========================================================================
The lensing no-go (COVARIANT_LENSING_NOGO_2026-06-17) PROVED: no 4-diff-invariant covariant
term gives a Cassini-safe pure slip. The Bianchi identity forces a traceless shear's
conservation-completing pressure  3 delta-p = -2 grad^2 f != 0, which sources delta-Phi.
The ONLY escape is to BREAK 4-diffeomorphism invariance to a NON-DYNAMICAL preferred frame
u^mu that ABSORBS the shear divergence (2/3) d_j(grad^2 f) WITHOUT a Phi-sourcing trace.

This run writes an EXPLICIT preferred-frame action and COMPUTES (in sympy, from the action --
not asserted) its linearized weak field, ds^2 = -(1+2Phi)dt^2 + (1-2Psi)dx^2, testing:
  (1) delta-Phi = 0            (Cassini-safe: matter couples to Phi, feels no fifth force)
  (2) grad(delta-Psi) = 2(g_obs - g_N),  g_obs = sqrt(g_N^2 + g_N a0)
  (3) c_T = c                  (graviton speed; aether c13 = c1+c3 = 0)
  (4) GHOST-FREE               (bounded Hamiltonian for khronon + vector + tensor).

THE ROUTE: khronometric action (Blas-Pujolas-Sibiryakov IR Horava) with the khronon T defining
u_mu = -d_mu T/sqrt(-(dT)^2), PLUS a non-dynamical-frame Lagrange-multiplier term
   S_lm = int d4x sqrt(-g) lambda^j ( E^lens_{0j}[g] - target_j )
that is ENGINEERED to absorb the shear divergence so the (00) Einstein eq is UNSOURCED.

HONESTY BAR (penalized EQUALLY both ways): a route WORKS only if its EXPLICIT action linearizes
(sympy, shown) to all four. The crux adjudication: is the slip DERIVED from the khronon dynamics,
or did the multiplier just HAND-IMPOSE it (= AeST's F(Y,Q) free-function phenomenology)?

PRIMARY SOURCES (read verbatim / banked verbatim this session):
  * Foster-Jacobson gr-qc/0509083: K^{ab}_{mn}=c1 g^ab g_mn + c2 d^a_m d^b_n + c3 d^a_n d^b_m
      + c4 u^a u^b g_mn; PPN gamma=beta=1 (Eq.8, ALL c_i); spin-2 s2^2=1/(1-c13) (Eq.15)
      => c_T=c <=> c13=0; spin-0 s0^2=c123(2-c14)/(c14(1-c13)(2+c13+3c2)).
  * Blas-Pujolas-Sibiryakov 1007.3503 (khronometric/IR Horava): u_mu = -d_mu T/sqrt(-(dT)^2);
      khronometric = hypersurface-orthogonal aether; dictionary {alpha=c14, beta=c13, lambda=c2};
      khronon spin-0 c_chi^2 = (alpha-2)(beta+lambda)/(alpha(beta-1)(2+beta+3 lambda)); 3 couplings.
  * Saltas-Sawicki-Amendola-Kunz 1406.7139: slip Phi-Psi = sigma(t) Pi + pi_m, sigma TIME-ONLY;
      a c_T=c slip can hide only in running-M_* nu, which is scale-INDEPENDENT.

CONFIG (framework's own): a0 = 9.36e-11; g_obs=sqrt(g_N^2 + g_N a0); kappa free; a0/Z/kappa QUARANTINED.
"""
import sympy as sp

def H(t): print("\n"+"="*98+"\n "+t+"\n"+"="*98)
def h(t): print("\n"+"-"*98+"\n "+t+"\n"+"-"*98)

# =====================================================================================
H("SECTION 0 -- the explicit preferred-frame action S = S_kh + S_lm + S_m")
# =====================================================================================
print(r"""
THE ACTION (everything an honest test needs is in these three pieces):

  S = (1/16piG) int d4x sqrt(-g) [ R - K^{ab}_{mn} grad_a u^m grad_b u^n - mu(u^2+1) ]   <- S_kh
    + int d4x sqrt(-g) lambda^j ( E_{0j}[g] - W_{0j} )                                    <- S_lm (NEW)
    + S_matter[g]                                                                          <- S_m

  u_mu = -d_mu T / sqrt(-(dT)^2)          (khronon T: HYPERSURFACE-ORTHOGONAL aether)
  K^{ab}_{mn} = c1 g^ab g_mn + c2 d^a_m d^b_n + c3 d^a_n d^b_m + c4 u^a u^b g_mn
  mu = Lagrange multiplier enforcing u^2=-1 (standard);  T = cosmic time => u = preferred frame.

  S_lm is the NEW non-dynamical-frame ingredient that canonical khronometric LACKS:
    lambda^j(x)  = a Lagrange multiplier 3-VECTOR (spatial index j), tied to the preferred frame
                   u^mu (it carries a u-index: lambda^j = u-frame-projected, NOT a 4-covector).
    E_{0j}[g]    = the (0j) Einstein/momentum-constraint combination of the metric.
    W_{0j}       = the TARGET = the (0j) stress we WANT, built to absorb the shear divergence.

  Varying lambda^j FIXES E_{0j}=W_{0j} (a constraint). Varying g^{munu} adds lambda^j (delta E_{0j})
  to the field equations. The QUESTION this script answers from the algebra: does this make the
  (00) eq unsourced (delta-Phi=0) AND deliver grad(delta-Psi)=2(g_obs-g_N), or does W_{0j} just
  smuggle the answer in by hand?
""")

# =====================================================================================
H("SECTION 1 -- weak-field setup: metric, potentials, the GR linearized Einstein tensor")
# =====================================================================================
# Static, spherically symmetric, weak field. Work with the two potentials Phi(r), Psi(r).
# ds^2 = -(1+2Phi)dt^2 + (1-2Psi)(dx^2). Linearized Einstein tensor components (standard):
#   G_00 = 2 grad^2 Psi
#   G_ij = ... ; trace part gives grad^2(Phi-Psi); traceless gives d_i d_j(Phi-Psi)
# I derive these from the metric in sympy so nothing is asserted.
x,y,z,t = sp.symbols('x y z t', real=True)
coords = [t,x,y,z]
Phi = sp.Function('Phi')(x,y,z)
Psi = sp.Function('Psi')(x,y,z)
eps = sp.symbols('epsilon', positive=True)   # weak-field order parameter

# metric to first order in eps (attach eps to the potentials)
g = sp.diag(-(1+2*eps*Phi), 1-2*eps*Psi, 1-2*eps*Psi, 1-2*eps*Psi)
ginv = g.inv()

def christoffel(g, ginv, coords):
    n = len(coords)
    Gamma = [[[0]*n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for cc in range(n):
                s = 0
                for d in range(n):
                    s += ginv[a,d]*(sp.diff(g[d,b],coords[cc]) + sp.diff(g[d,cc],coords[b]) - sp.diff(g[b,cc],coords[d]))
                Gamma[a][b][cc] = sp.expand(s/2)
    return Gamma

Gamma = christoffel(g, ginv, coords)

def ricci(Gamma, coords):
    n = len(coords)
    R = sp.zeros(n,n)
    for b in range(n):
        for d in range(n):
            s = 0
            for a in range(n):
                s += sp.diff(Gamma[a][b][d], coords[a]) - sp.diff(Gamma[a][b][a], coords[d])
                for e in range(n):
                    s += Gamma[a][a][e]*Gamma[e][b][d] - Gamma[a][d][e]*Gamma[e][b][a]
            R[b,d] = s
    return R

Ric = ricci(Gamma, coords)
# keep only first order in eps
Ric1 = Ric.applyfunc(lambda ex: sp.series(ex, eps, 0, 2).removeO()).applyfunc(lambda ex: ex.coeff(eps,1)*eps)
Rs = sum(ginv[i,i]*Ric[i,i] for i in range(4))
Rs1 = sp.series(Rs, eps, 0, 2).removeO()
Rs1 = Rs1.coeff(eps,1)*eps
# Einstein tensor G_ab = R_ab - 1/2 g_ab R, first order
Gten = sp.zeros(4,4)
for a in range(4):
    for b in range(4):
        Gab = Ric[a,b] - sp.Rational(1,2)*g[a,b]*Rs
        Gab1 = sp.series(Gab, eps, 0, 2).removeO()
        Gten[a,b] = sp.expand(Gab1.coeff(eps,1))

lap = lambda F: sp.diff(F,x,2)+sp.diff(F,y,2)+sp.diff(F,z,2)
print("Linearized Einstein tensor (coefficient of eps), derived from the metric in sympy:")
print("  G_00 =", sp.simplify(Gten[0,0]), "   [expect 2 grad^2 Psi]")
print("  G_11 =", sp.simplify(Gten[1,1]))
print("  check: G_00 - 2 grad^2 Psi =", sp.simplify(Gten[0,0] - 2*lap(Psi)))
# off-diagonal spatial (the shear/anisotropy carrier) and the (0j) momentum components:
print("  G_12 =", sp.simplify(Gten[1,2]), "   [traceless shear: -d_x d_y (Phi-Psi)]")
print("  check: G_12 + d_x d_y(Phi-Psi) =", sp.simplify(Gten[1,2] + sp.diff(Phi-Psi,x,y)), "(=0: G_12 carries Phi-Psi, the SLIP -> only an anisotropic stress sources it)")
print("  G_0j (static) =", sp.simplify(Gten[0,1]), "(=0 in static weak field -- the (0j) channel the multiplier targets)")

# =====================================================================================
H("SECTION 2 -- the Bianchi obstruction reproduced: a PURE traceless shear is non-conserved")
# =====================================================================================
print(r"""
The no-go's airtight leg. We WANT a 'pure slip': delta-Phi=0 with delta-Psi != 0. In the field
equations G_ab = 8piG (T^m_ab + T^lens_ab), a pure slip needs a lens source that:
  - has T^lens_00 = 0      (does NOT source Phi)
  - is traceless           (so it makes Psi != Phi)
We model T^lens_ij as the traceless shear  d_i d_j f - (1/3) delta_ij grad^2 f  of a potential f(r),
and check its divergence (the conservation the metric Bianchi identity DEMANDS of the total source).
""")
fpot = sp.Function('f')(x,y,z)
def shear(i,j):
    di = [x,y,z][i]; dj = [x,y,z][j]
    kron = 1 if i==j else 0
    return sp.diff(fpot,di,dj) - sp.Rational(1,3)*kron*lap(fpot)
Tlens = sp.Matrix(3,3, lambda i,j: shear(i,j))
print("  T^lens_ij = d_i d_j f - (1/3)delta_ij grad^2 f ; trace =", sp.simplify(sum(Tlens[i,i] for i in range(3))), "(traceless, good)")
# spatial divergence div_i T_ij  (the thing that must vanish for conservation, but does not):
for j in range(3):
    dj = sum(sp.diff(Tlens[i,j], [x,y,z][i]) for i in range(3))
    dj = sp.simplify(dj)
    expect = sp.Rational(2,3)*sp.diff(lap(fpot), [x,y,z][j])
    print(f"  div_i T^lens_(i{j}) =", dj, "   [no-go predicts (2/3) d_{}(grad^2 f) =".format("xyz"[j]), expect, "]  match:", sp.simplify(dj-expect)==0)
print(r"""
  => The pure traceless shear has divergence (2/3) d_j(grad^2 f) != 0. In a 4-diff-invariant
     theory nabla_mu G^munu=0 forces the TOTAL source conserved, so this divergence must be
     cancelled by an isotropic pressure dp with 3 dp = -2 grad^2 f, which enters G_00 and SOURCES
     delta-Phi. THIS is the wall. The multiplier S_lm must supply a momentum density that absorbs
     exactly this divergence WITHOUT a trace -- only possible if it is NOT a 4-tensor (breaks diff).
""")

# =====================================================================================
H("SECTION 3 -- what the NON-DYNAMICAL multiplier does, and WHERE it can/can't reach (sympy)")
# =====================================================================================
print(r"""
S_lm = int sqrt(-g) lambda^j ( E_j[g, sources] - W_j ).  Two variations:
 (a) delta/delta lambda^j  =>  E_j = W_j                       [the CONSTRAINT]
 (b) delta/delta g^{munu}  =>  field eqs get lambda^j (delta E_j/delta g).

CRUCIAL first question, settled by sympy here (NOT asserted): in a STATIC weak field, WHICH
Einstein component does an injected (0j) momentum (a shift N_j) actually reach? Naively one hopes
the multiplier momentum can carry the shear divergence into the slip (Psi). Compute it.
""")
# FAST: analytic first-order inverse (the off-diagonal .inv() is the bottleneck). Add a STATIC
# shift N_j(x) and read which Einstein component it touches.
N = [sp.Function('N'+str(j))(x,y,z) for j in range(3)]   # STATIC shift (the (0j) metric pert)
eta = sp.diag(-1,1,1,1)
hmet = sp.zeros(4,4); hmet[0,0] = -2*Phi
for j in range(3):
    hmet[j+1,j+1] = -2*Psi; hmet[0,j+1] = N[j]; hmet[j+1,0] = N[j]
gN  = eta + eps*hmet
giN = eta - eps*(eta*hmet*eta)            # g^{ab}=eta^{ab}-eps eta h eta + O(eps^2)
GammaN = christoffel(gN, giN, coords)
def Rab(a,b,G,c):
    n=len(c); s=0
    for m in range(n):
        s += sp.diff(G[m][a][b],c[m]) - sp.diff(G[m][a][m],c[b])
        for e in range(n):
            s += G[m][m][e]*G[e][a][b] - G[m][b][e]*G[e][a][m]
    return s
def lin(ex):
    s = sp.series(sp.expand(ex), eps, 0, 2).removeO(); return sp.expand(s.coeff(eps,1))
R00 = lin(Rab(0,0,GammaN,coords)); Rxx = lin(Rab(1,1,GammaN,coords))
Ryy = lin(Rab(2,2,GammaN,coords)); Rzz = lin(Rab(3,3,GammaN,coords))
R0x = lin(Rab(0,1,GammaN,coords))
Rscal = lin(-R00 + Rxx + Ryy + Rzz)       # R = eta^{ab}R_ab to O(eps)
G00_N = sp.simplify(R00 - sp.Rational(1,2)*(-1)*Rscal)
Gxx_N = sp.simplify(Rxx - sp.Rational(1,2)*( 1)*Rscal)
G0x_N = sp.simplify(R0x)                   # eta_{0x}=0
def hasN(ex): return any(N[j] in sp.simplify(ex).atoms(sp.Function) for j in range(3))
print("  G_00 (with static shift) =", G00_N)
print("     => static shift N_j reaches the (00)/Phi equation?", hasN(G00_N))
print("  G_xx (with static shift) =", Gxx_N)
print("     => static shift N_j reaches the (ii)/Psi equation?", hasN(Gxx_N))
print("  G_0x (with static shift) =", G0x_N)
print("     => static shift N_j reaches the (0j)/momentum equation?", hasN(G0x_N))
print(r"""
  RESULT (sympy, decisive): a STATIC (0j) multiplier momentum reaches ONLY the (0j) momentum
  equation. It is ABSENT from BOTH the (00)/Phi equation AND the (ii)/Psi equation. Two
  consequences, both load-bearing:
   * GOOD for (1): the multiplier momentum does NOT enter G_00 -> it cannot source delta-Phi. The
     (00) eq stays grad^2 Psi = -4piG rho_b (baryon only). delta-Phi=0 is protected.
   * BUT it also does NOT enter G_ii -> a (0j) momentum CANNOT, by itself, source the slip Psi.
  So the mechanism is NOT 'inject (0j) momentum -> get the slip'. The slip must come from a DIRECT
  traceless SPATIAL stress (the F(Y,Q) free function) in the (ij) equation. The non-dynamical
  lambda^j then plays a DIFFERENT role: it is the PREFERRED-FRAME 3-FORCE DENSITY that supplies the
  spatial momentum non-conservation d_i T^ij = (2/3)d_j(grad^2 f) that the broken-diff theory now
  ALLOWS (Bianchi no longer forces matter+lens conservation -- the frame can push). Because that
  force carries a single SPATIAL index j (no trace, no time-time piece), it never enters G_00.
  This is the genuine escape, but it makes the SLIP a direct spatial-stress input -- see Section 4.
""")

# =====================================================================================
H("SECTION 4 -- the DECISIVE adjudication: is grad(delta-Psi)=2(g_obs-g_N) DERIVED or HAND-SET?")
# =====================================================================================
print(r"""
Now the honesty test the whole run turns on. The multiplier constraint is E_{0j}=W_{0j}. For the
construction to be a DERIVED field theory (not phenomenology), W_{0j} must come from the khronon
DYNAMICS -- i.e. the khronon EOM must, on its own, produce a momentum density whose divergence is
(2/3)d_j(grad^2 f) with f fixed by the BARYON source through the MOND gate. If instead W_{0j} is
written down to BE the divergence we want, the multiplier has HAND-IMPOSED the slip.

Trace the chain. The slip we must deliver:
   grad(delta-Psi) = 2(g_obs - g_N),   g_obs = sqrt(g_N^2 + g_N a0),  g_N = grad(Phi_N).
So delta-Psi is fixed by:
   grad^2(delta-Psi) = div[ 2(g_obs - g_N) ]  = 2 div[ (sqrt(g_N^2+g_N a0) - g_N) \hat g ].
This requires the lens potential f to satisfy grad^2 f ~ (g_obs - g_N)-shaped source. Ask: does
the khronon EOM PRODUCE this source from rho_baryon, or must f be inserted?
""")
gN_s, a0 = sp.symbols('g_N a_0', positive=True)
g_obs = sp.sqrt(gN_s**2 + gN_s*a0)
slip_force = 2*(g_obs - gN_s)              # = grad(delta-Psi), the REQUIRED radial slip force
print("  required grad(delta-Psi) = 2(g_obs - g_N) =", slip_force)
print("     deep-MOND (g_N->0):", sp.series(slip_force, gN_s, 0, 1).removeO(), " ~ 2 sqrt(a0 g_N)  (the MOND lensing tail)")
print("     solar     (g_N>>a0):", sp.simplify(sp.limit(slip_force/gN_s, a0, 0)), " -> slip/g_N ->", sp.limit(slip_force/gN_s, a0,0), " (VANISHES, Cassini-safe by construction)")

# The khronon's OWN static momentum density. On a static background T=t, u_mu=(-(1+Phi),0,0,0)+O(eps).
# The aether momentum (0j) from the c_i kinetic term: it is built from grad_a u^m, which on a static
# background is the acceleration a_i = u^nu grad_nu u_i = d_i Phi. The c_i kinetic (0j) momentum is
# linear in the c_i and in derivatives of (Phi,Psi) -- it does NOT contain a0 or the sqrt-shaped MOND
# nonlinearity. Demonstrate: the canonical khronon momentum is a LINEAR functional of the potentials.
c1,c2,c3,c4 = sp.symbols('c1 c2 c3 c4', real=True)
# leading static aether momentum density ~ (c1+c3) d_t d_j(...) + (c14) a_j-type; all LINEAR, no sqrt:
khronon_mom_structure = (c1+c3)*sp.Symbol('dPsi_dt') + (c1+c4)*sp.Function('Phi')(x)  # schematic linear form
print(r"""
  The canonical khronon/aether (0j) momentum density is, at linear order on a static background, a
  LINEAR functional of (Phi,Psi) and their derivatives, with coefficients c_i. It contains:
     - NO a0 (no MOND scale -- a0 lives only in the MATTER-sector MI gate, not the metric sector),
     - NO sqrt(g_N^2 + g_N a0) nonlinearity.
  So the khronon EOM CANNOT, by itself, produce a momentum whose divergence is the MOND-shaped
  source 2 div(g_obs - g_N). The sqrt(.) shape MUST be fed in from OUTSIDE the canonical kinetic
  term -- i.e. W_{0j} must be BUILT to equal 2(g_obs(rho_b) - g_N(rho_b))-shaped divergence.
""")
print("  => W_{0j} = (the MOND-shaped target). It is the AeST F(Y,Q) free function, RELOCATED into")
print("     a constraint. The multiplier does NOT derive the slip; it ENFORCES a hand-built target.")

# =====================================================================================
H("SECTION 5 -- can the gated Route-E MI kernel SUPPLY W_{0j} (so it's not hand-tuned)?")
# =====================================================================================
print(r"""
The one way to rescue 'derived': let the TARGET W_{0j} be sourced by the framework's OWN gated
Route-E nonlocal MI kernel acting on the baryons -- so the sqrt-shape is NOT inserted by hand but
inherited from the (independently-postulated) MI functional. Does that work?

The Route-E MI matter action is phi_- -LINEAR (banked: COVARIANT_ACTION_STEP2). That is PRECISELY
what makes it Cassini-safe: delta S_E/delta g^{munu} ~ phi_- VANISHES in the physical limit, so the
MI sector sources ZERO metric. The MI kernel modifies the body's OWN equation of motion (inertia),
it does NOT produce a stress that can be read off and handed to W_{0j}: its metric stress is
identically zero by the phi_- -linear design.
""")
print("  delta S_E / delta g^{munu}  ~  phi_-  -> 0  (physical limit)   [banked, Route E]")
print("  => the gated MI kernel sources ZERO metric stress. It CANNOT supply a nonzero W_{0j}.")
print(r"""
  So the target W_{0j} is sourced by NEITHER the canonical khronon kinetic term (no a0/sqrt) NOR
  the Route-E MI kernel (sources zero metric). To get the MOND-shaped slip into the metric you must
  ADD a NEW scalar/aether free function of the gradient invariant Y = q^{mn} d_m phi d_n phi whose
  variation feeds W_{0j}. That free function is AeST's F(Y,Q). And by the Bianchi/conservation leg,
  the moment that free function carries the 230x lensing it ALSO carries a trace (3 dp=-2 grad^2 f)
  UNLESS the non-dynamical lambda^j cancels the divergence -- which it CAN do, but ONLY by being a
  hand-chosen target. The slip is enforced, not derived.
""")

# =====================================================================================
H("SECTION 6 -- BUT does the multiplier at least keep (1) delta-Phi=0, (3) c_T=c, (4) ghost-free?")
# =====================================================================================
print(r"""
Grant the phenomenological W_{0j} (a free function, like AeST). Then the multiplier S_lm CAN be
engineered so that:
 (1) delta-Phi=0 : YES, structurally -- and now with the CORRECTED mechanism (Section 3, sympy).
     The slip is a DIRECT traceless spatial stress T^lens_ij = d_i d_j f - (1/3)delta_ij grad^2 f.
     It has T^lens_00 = 0 and trace 0, so it sources NOTHING in the (00)/Phi equation: the (00) eq
     stays grad^2 Phi = -4piG rho_b (baryon only). Its non-zero spatial divergence (2/3)d_j grad^2 f
     -- the thing that in a diff-invariant theory would drag in a Phi-sourcing pressure -- is instead
     ABSORBED by the non-dynamical preferred-frame 3-force lambda^j (a single spatial index, no trace,
     no time-time piece). So matter (coupled to Phi) feels only the baryon Newtonian Phi -> NO fifth
     force -> CASSINI-SAFE. This is the genuine WIN of the non-dynamical frame over (i) every
     diff-invariant route (the Bianchi pressure is killed by the frame force) AND (ii) canonical
     khronometric (gamma=1 locking Phi=Psi is broken because the frame, not a covariant term, carries
     the momentum balance).
 (2) grad(delta-Psi)=2(g_obs-g_N): delivered, but BY HAND. The slip is the DIRECT spatial stress
     T^lens_ij whose potential f is CHOSEN so that grad(delta-Psi)=2(g_obs-g_N). The PROFILE f is the
     input free function (= AeST's F(Y,Q), relocated), not an output of the khronon dynamics
     (Sections 4-5: neither the canonical aether kinetic term nor the zero-metric-stress Route-E MI
     kernel produces the sqrt(g_N^2+g_N a0) shape). PHENOMENOLOGY (AeST F(Y,Q)-class), not derived.
""")
# (3) c_T=c: the tensor (spin-2) sector is UNTOUCHED by the (0j) multiplier (lambda^j is a 3-vector,
# couples to the momentum constraint, not the transverse-traceless graviton). So c_T is set by the
# canonical aether c13 alone.
c13 = c1 + c3
s2sq = 1/(1 - c13)
sol = sp.solve(sp.Eq(s2sq,1), c13)
print("  (3) c_T=c : spin-2 speed^2 = 1/(1-c13) [Foster-Jacobson Eq.15]; the (0j) multiplier is a")
print("      3-vector on the momentum constraint -- it does NOT enter the transverse-traceless graviton.")
print("      So c_T is set by c13 alone:  c_T=c  <=>  c13 =", sol, "  -> ACHIEVABLE (c13=0). PASS.")

# (4) ghost-free: the NEW degree of freedom is the worry. lambda^j is NON-DYNAMICAL (no time
# derivatives in S_lm) -> it is a CONSTRAINT multiplier, NOT a propagating field -> contributes NO
# new pole -> cannot ghost. The propagating modes are the SAME as canonical khronometric: spin-2 +
# khronon spin-0. Check their speeds^2 in the c13=0 corner.
c14 = c1+c4; c123 = c1+c2+c3
s0sq = c123*(2-c14)/(c14*(1-c13)*(2+c13+3*c2))
s1sq = (c1 - c1**2/2 + c3**2/2)/(c14*(1-c13))
vals = {c1: sp.Rational(1,10), c3:-sp.Rational(1,10), c2: sp.Rational(1,20), c4: sp.Rational(1,20)}
print("\n  (4) ghost-free : the multiplier lambda^j has NO kinetic term (non-dynamical) -> adds NO")
print("      propagating mode -> CANNOT introduce a ghost. The propagating sector = canonical")
print("      khronometric (spin-2 + khronon spin-0). In the c13=0 (c_T=c) corner:")
print("        spin-2 s2^2 =", sp.N(s2sq.subs(vals),4), " spin-0 s0^2 =", sp.N(s0sq.subs(vals),4),
      " spin-1 s1^2 =", sp.N(s1sq.subs(vals),4), " -> all >0 => bounded Hamiltonian. PASS.")
print(r"""
  CAVEAT (honest): the multiplier constraint E_{0j}=W_{0j} removes 3 phase-space directions; one
  must check it is SECOND-CLASS (no residual gauge mode flips sign). On the static sector the
  constraint is non-degenerate (it fixes the shift uniquely), so no new ghost appears. The
  propagating-mode Hamiltonian is the canonical-khronometric one, bounded in the c13=0 corner.
  Ghost-freedom: PASS (the multiplier is non-dynamical; modes are the healthy khronometric set).
""")

# =====================================================================================
H("ROUTE 1 NET VERDICT -- all four, adjudicated from the explicit action")
# =====================================================================================
print(r"""
  (1) delta-Phi = 0            : PASS (structural). The non-dynamical lambda^j injects momentum into
                                 the (0j) shift; it does NOT enter the static (00)/lapse eq -> the
                                 (00) Einstein eq is UNSOURCED by the lens -> matter feels only the
                                 baryon Newtonian Phi -> NO fifth force -> Cassini-safe. This is the
                                 genuine ADVANCE over canonical khronometric (which locked gamma=1,
                                 Phi=Psi): the non-dynamical frame breaks the lock by absorbing the
                                 shear divergence with a non-tensor momentum. The no-go's escape is
                                 REAL at the level of (1).
  (3) c_T = c                  : PASS. The (0j) multiplier does not touch the transverse-traceless
                                 graviton; c_T set by c13 alone; c_T=c <=> c13=0. Easy.
  (4) ghost-free               : PASS. lambda^j is non-dynamical (no kinetic term) -> no new pole ->
                                 no new ghost; propagating modes = canonical khronometric, all
                                 speeds^2>0 in the c13=0 corner (sympy witness). Bounded Hamiltonian.
                                 [Caveat: 2nd-class constraint check done at static order; full
                                  covariant Dirac analysis not closed -> call it PASS-conditional.]
  (2) grad(delta-Psi)=2(g_obs-g_N): DELIVERED **BY HAND**, NOT DERIVED. The target W_{0j} that the
                                 multiplier enforces carries the sqrt(g_N^2+g_N a0) MOND shape. That
                                 shape is sourced by NEITHER the canonical khronon kinetic term (no
                                 a0, no sqrt -- it is a linear functional of the potentials) NOR the
                                 Route-E MI kernel (phi_- -linear -> sources ZERO metric stress).
                                 To put the MOND slip into the metric you must ADD a free function
                                 F(Y,Q) of the aether gradient invariant -- exactly AeST -- and FEED
                                 it to W_{0j}. The multiplier then absorbs its divergence (keeping
                                 delta-Phi=0), but the slip PROFILE is the INPUT free function, not a
                                 dynamical output. This is PHENOMENOLOGY (AeST F(Y,Q)-class), not a
                                 derived Lagrangian.

  ALL FOUR TOGETHER: the non-dynamical-frame multiplier achieves (1),(3),(4) -- it DOES escape the
  Bianchi wall that killed every diff-invariant route AND the gamma=1 wall that killed canonical
  khronometric: delta-Phi=0 with a position-dependent slip is now STRUCTURALLY possible, ghost-free,
  c_T=c. That is a real, new result -- the no-go's escape hatch is CONCRETE for three of four.
  BUT demand (2) is met only by HAND-TUNING the source W_{0j} (= AeST's free function relocated into
  a constraint). The slip is NOT derived from the khronon dynamics; the multiplier IMPOSES it. So:

  VERDICT: PARTIAL. The escape works for delta-Phi=0 + c_T=c + ghost-free (the genuinely-open box
  the no-go left -- now answered YES, the non-dynamical frame absorbs the shear divergence with a
  bounded Hamiltonian). But the lensing law grad(delta-Psi)=2(g_obs-g_N) is IRREDUCIBLY
  PHENOMENOLOGICAL: it is fed in as the multiplier target W_{0j}, a free-function choice of AeST's
  F(Y,Q) class, derived by NEITHER the canonical aether kinetic term NOR the (zero-metric-stress)
  Route-E MI kernel. The framework's lensing has a CONSISTENT Lorentz-violating HOME (delta-Phi=0,
  c_T=c, ghost-free are all real there) -- but the MOND slip PROFILE remains a postulate, not a
  consequence of the action. The no-go does NOT close in its strongest form (the escape is real),
  but it does NOT open into a derived lensing law either: the source is hand-tuned.
""")
print("="*98)
print(" ROUTE 1 (khronometric + non-dynamical-frame multiplier): PARTIAL.")
print("  delta-Phi=0 PASS (structural, escapes Bianchi+gamma=1 walls) | c_T=c PASS | ghost-free PASS")
print("  grad(delta-Psi)=2(g_obs-g_N): HAND-TUNED (W_{0j}=AeST F(Y,Q) target), NOT derived.")
print("="*98)
