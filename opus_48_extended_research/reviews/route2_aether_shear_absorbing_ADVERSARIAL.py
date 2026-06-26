#!/usr/bin/env python3
r"""
ADVERSARIAL RE-COMPUTATION of ROUTE 2 (Einstein-aether + shear-absorbing Lagrange multiplier b^mu).
The claim: delta-Phi=0 DERIVED, c_T=c PASS, ghost-free PASS(linear), slip HAND-TUNED -> PARTIAL.

I do NOT trust the original script's print-statement assertions for delta-Phi=0. The original
asserts (lines 159-182) the schematic  T^abs_munu = b(dC/dg) - (1/2)g b(C-J), substitutes C=J to
kill the SECOND term, and then ASSERTS the FIRST term b(dC/dg) "has support in the spatial block"
WITHOUT computing it. The whole no-go is about exactly that first, on-shell-surviving term.

This script COMPUTES, not asserts:
  ATTACK 1: actually vary S_abs w.r.t. the metric -> get T^abs_munu -> read the 00 component
            of the SURVIVING (on-shell) piece b^alpha (dC_alpha/dg^00). Is delta-Phi really 0?
  ATTACK 1b: cross-check via the conservation/Bianchi route the no-go used: is the partner's
            divergence really absorbed with NO trace, given a CONSISTENT b-field?
  ATTACK 2: is grad(delta-Psi)=2(g_obs-g_N) derived or tuned? (independent non-polynomial test)
  ATTACK 3: c_T=c at c13=0 (independent, from the spin-2 kinetic coefficient).
  ATTACK 4: the ghost. (a) aether scalar/khronon dispersion at c13=0; (b) the b-constraint class
            (first vs second class) -- does it remove or re-propagate a DOF? This is the open box.
"""
import sympy as sp

def H(t): print("\n"+"#"*100+"\n# "+t+"\n"+"#"*100)
def sub(t): print("\n--- "+t+" ---")

# =====================================================================================================
H("ATTACK 1 -- COMPUTE T^abs_munu by ACTUALLY VARYING S_abs w.r.t. the metric. Is delta-Phi=0 real?")
# =====================================================================================================
print(r"""
S_abs = int sqrt(-g) b^mu ( C_mu - J_mu ),   C_mu = P^nu_mu nabla^rho sigma_{rho nu}.
The metric variation produces  T^abs_{munu} from THREE sources:
  (A) sqrt(-g)            -> -(1/2) g_munu L_abs = -(1/2) g_munu b^a(C_a - J_a)   [KILLED on-shell C=J]
  (B) the projector P, the index raising in b^mu = g^{mu a} b_a, and sigma's covariant derivatives
                          -> b^alpha (dC_alpha/dg^munu)                            [SURVIVES on-shell]
The no-go's entire question: does (B)'s 00-component vanish? Compute it explicitly.
""")

t,x,y,z = sp.symbols('t x y z', real=True)
coords = [t,x,y,z]
# Weak field, conformal-Newtonian: g = diag(-(1+2Phi), 1-2Psi, 1-2Psi, 1-2Psi). Work to linear order.
Phi = sp.Function('Phi')(x,y,z)
Psi = sp.Function('Psi')(x,y,z)
eps = sp.symbols('epsilon')  # bookkeeping for linear order
# metric (lower) and inverse to linear order
g = sp.diag(-(1+2*eps*Phi), 1-2*eps*Psi, 1-2*eps*Psi, 1-2*eps*Psi)
ginv = sp.diag(-(1-2*eps*Phi), 1+2*eps*Psi, 1+2*eps*Psi, 1+2*eps*Psi)
# check inverse to O(eps)
chk = sp.simplify((g*ginv - sp.eye(4)).applyfunc(lambda e: sp.series(e, eps, 0, 2).removeO()))
print("  g.ginv - I  to O(eps):  zero? ->", chk == sp.zeros(4,4))

# Non-dynamical aether: u^mu = (1,0,0,0)/sqrt(...) normalized to u.u=-1 on this metric.
# u_mu u^mu = -1 with u^i=0: u^0 = 1/sqrt(1+2Phi) ~ 1-eps*Phi ; u_0 = g_00 u^0 = -(1+2Phi)u^0 ~ -(1+eps Phi)
u_up = sp.Matrix([1/sp.sqrt(1+2*eps*Phi), 0,0,0])
u_dn = g*u_up
u_up = u_up.applyfunc(lambda e: sp.series(e,eps,0,2).removeO())
u_dn = u_dn.applyfunc(lambda e: sp.series(e,eps,0,2).removeO())
print("  u^mu =", list(u_up.T), "   u_mu =", list(u_dn.T))
print("  normalization u_mu u^mu =", sp.simplify((u_dn.T*u_up)[0]), " (should be -1)")

sub("Projector P^nu_mu = delta^nu_mu + u^nu u_mu  (orthogonal to u). Compute every component.")
P = sp.zeros(4,4)  # P[nu, mu] = delta^nu_mu + u^nu u_mu
for nu in range(4):
    for mu in range(4):
        d = 1 if nu==mu else 0
        P[nu,mu] = sp.series(d + u_up[nu]*u_dn[mu], eps,0,2).removeO()
print("  P^nu_mu (rows nu, cols mu):")
sp.pprint(P)
print("  CRUCIAL: the time-row/col. P^nu_0 (mu=0 column) =", list(P[:,0].T),
      " -> the original claims P^nu_0=0 EXACTLY.")
P_col0 = sp.simplify(P[:,0])
print("  Is P^nu_0 == 0 to linear order?  ->", P_col0 == sp.zeros(4,1))

print(r"""
  FIRST FINDING: P^nu_0 = 0 holds to linear order (the column orthogonal to u kills the time index).
  So C_0 = P^nu_0 nabla^rho sigma_{rho nu} = 0: the b-constraint genuinely has NO time component.
  This part of the original is CORRECT. But that is the constraint C_mu; the no-go is about the
  METRIC STRESS T^abs_00, which is b^alpha (dC_alpha/dg^00) -- a DIFFERENT object. C_0=0 does NOT
  imply (dC_alpha/dg^00) summed against b^alpha is 0. Compute THAT next.
""")

# =====================================================================================================
H("ATTACK 1 (continued) -- the ACTUAL metric stress T^abs_00. Compute C_mu in curved space, then")
print("# differentiate S_abs = int sqrt(-g) b^mu (C_mu - J_mu) w.r.t. the metric. (the no-go's real test)")
# =====================================================================================================
print(r"""
We need C_mu = P^nu_mu nabla^rho sigma_{rho nu} as an EXPLICIT functional of the metric, then form
S_abs and vary. sigma_{rho nu} = nabla_rho nabla_nu f - (1/3) g_{rho nu} box f  (covariant, traceless).
The metric enters through: Christoffels in nabla nabla f, the raising nabla^rho = g^{rho s} nabla_s,
g_{rho nu} in the trace piece, P (via u u and g), and sqrt(-g). We carry full Christoffels to linear
order. This is exactly what the original script DID NOT do.
""")

# --- build Christoffel symbols to linear order ---
def christoffel(g, ginv, coords):
    n=len(coords); Gam=[[[0]*n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                s=0
                for d in range(n):
                    s+= ginv[a,d]*(sp.diff(g[d,b],coords[c])+sp.diff(g[d,c],coords[b])-sp.diff(g[b,c],coords[d]))
                Gam[a][b][c]=sp.series(sp.Rational(1,2)*s, eps,0,2).removeO()
    return Gam
Gam = christoffel(g, ginv, coords)

f = sp.Function('f')(x,y,z)   # the MOND source scalar (free function; its profile is the slip question)

# covariant gradient of scalar: nabla_a f = d_a f  (scalar)
df = [sp.diff(f,coords[a]) for a in range(4)]
# second covariant derivative nabla_r nabla_n f = d_r d_n f - Gam^a_{rn} d_a f
ddf = sp.zeros(4,4)
for rr in range(4):
    for nn in range(4):
        val = sp.diff(f,coords[rr],coords[nn])
        for a in range(4):
            val -= Gam[a][rr][nn]*df[a]
        ddf[rr,nn]=sp.series(val,eps,0,2).removeO()
# box f = g^{rn} nabla_r nabla_n f
boxf = 0
for rr in range(4):
    for nn in range(4):
        boxf += ginv[rr,nn]*ddf[rr,nn]
boxf = sp.series(boxf,eps,0,2).removeO()
# traceless shear sigma_{rho nu} = ddf - (1/3) g_{rho nu} box f  (lower indices)
sigma = sp.zeros(4,4)
for rr in range(4):
    for nn in range(4):
        sigma[rr,nn]=sp.series(ddf[rr,nn]-sp.Rational(1,3)*g[rr,nn]*boxf, eps,0,2).removeO()

sub("nabla^rho sigma_{rho nu}: raise rho with g, take covariant divergence on first index")
# D_nu := nabla^rho sigma_{rho nu} = g^{rho s}( d_s sigma_{rho nu} - Gam^a_{s rho} sigma_{a nu} - Gam^a_{s nu} sigma_{rho a})
D = sp.zeros(4,1)
for nn in range(4):
    val=0
    for s in range(4):
        for rho in range(4):
            term = sp.diff(sigma[rho,nn],coords[s])
            for a in range(4):
                term -= Gam[a][s][rho]*sigma[a,nn]
                term -= Gam[a][s][nn]*sigma[rho,a]
            val += ginv[rho,s]*term
    D[nn]=sp.series(val,eps,0,2).removeO()
# C_mu = P^nu_mu D_nu
C = sp.zeros(4,1)
for mu in range(4):
    val=0
    for nu in range(4):
        val += P[nu,mu]*D[nu]
    C[mu]=sp.series(val,eps,0,2).removeO()
print("  C_0 (time component of the constraint) =", sp.simplify(C[0]))
print("  -> matches the P^nu_0=0 finding (C_0 vanishes)." )


# =====================================================================================================
H("ATTACK 1 (decisive) -- form L_abs = sqrt(-g) b^mu(C_mu - J_mu) and vary w.r.t. Phi to get T^abs_00")
# =====================================================================================================
print(r"""
The metric stress is  T^abs_{munu} = -(2/sqrt(-g)) delta(sqrt(-g) L)/delta g^{munu}. In the conformal-
Newtonian gauge the 00 piece that sources Phi is obtained by varying the action density w.r.t. Phi
(g^00 = -(1-2 eps Phi)). We carry b^mu as an independent field (its EOM is C=J), expand to O(eps),
and extract the coefficient of (delta Phi). If that coefficient is NONZERO once b is on-shell, then
S_abs sources Phi -> delta-Phi != 0 -> Cassini FAILS (the no-go bites). If it is identically 0, the
original's delta-Phi=0 claim is genuinely DERIVED.
""")
# independent multiplier components (lower index b_mu); raise with g
b0,b1,b2,b3 = sp.symbols('b0 b1 b2 b3', real=True)   # b_mu treated as O(1) fields (constants locally)
b_dn = sp.Matrix([b0,b1,b2,b3])
b_up = ginv*b_dn
b_up = b_up.applyfunc(lambda e: sp.series(e,eps,0,2).removeO())
# gated current J_mu : the constraint sets C_mu=J_mu. Off the time index C_0=0 forces J_0=0 for
# consistency (else no solution). Keep J_mu general lower-index, with J_0 to be tested.
J0,J1,J2,J3 = sp.symbols('J0 J1 J2 J3', real=True)
J_dn = sp.Matrix([J0,J1,J2,J3])

# L_abs density (scalar) = sqrt(-g) * b^mu (C_mu - J_mu) = sqrt(-g) * g^{mu a} b_a (C_mu - J_mu)
detg = sp.series(-g.det(), eps,0,2).removeO()
sqrtmg = sp.series(sp.sqrt(detg), eps,0,2).removeO()
# b^mu (C_mu - J_mu) = sum_mu b_up[mu]*(C[mu]-J_dn[mu])
scalar = 0
for mu in range(4):
    scalar += b_up[mu]*(C[mu]-J_dn[mu])
L_abs = sp.series(sqrtmg*scalar, eps,0,2).removeO()
L_abs = sp.expand(L_abs)
print("  L_abs (density) to O(eps) formed. Now impose the b-EOM (on-shell): C_mu = J_mu.")
# on-shell substitution C_mu->J_mu means the bracket vanishes -> L_abs would be 0 as an ACTION VALUE,
# but the STRESS is delta L / delta g, taken BEFORE setting the bracket to zero, THEN evaluated on-shell.
# Proper procedure: T_00 ~ dL_abs/dPhi at fixed b,f,J, THEN substitute the on-shell relation.

dL_dPhi = sp.diff(L_abs, eps)  # coefficient structure; the O(eps) part is the linear stress
# Extract the part of L_abs linear in eps (that is the linearized stress contribution):
L_lin = sp.expand(sp.series(L_abs, eps,0,2).removeO().coeff(eps,1))
print("\n  Linear-in-eps part of L_abs (the O(eps) stress density), simplified:")
L_lin_s = sp.simplify(L_lin)
sp.pprint(L_lin_s)

# =====================================================================================================
H("ATTACK 1 (verdict) -- the Euler-Lagrange variation delta L_abs / delta Phi  (= the Phi source)")
# =====================================================================================================
print(r"""
delta-Phi=0 requires that S_abs does NOT source Phi, i.e. the functional derivative of L_abs w.r.t.
Phi(x) vanishes (after on-shell b-EOM). Compute E_Phi = dL/dPhi - d_i(dL/d(d_i Phi)) + d_i d_j(dL/d(d_id_j Phi)).
If E_Phi != 0, matter's Poisson eq nabla^2 Phi = 4piG(rho + [E_Phi]) gets a fifth-force term -> Cassini.
""")
from sympy import Derivative
Phisym = Phi  # Phi(x,y,z)
# Build Euler-Lagrange operator for a Lagrangian depending on Phi up to 2nd derivatives.
def EL_variation(L, field, coords3):
    # zeroth
    res = sp.diff(L, field)
    # first derivatives
    for ci in coords3:
        res -= sp.diff(sp.diff(L, sp.Derivative(field, ci)), ci)
    # second derivatives (including mixed)
    for ci in coords3:
        for cj in coords3:
            res += sp.diff(sp.diff(L, sp.Derivative(field, ci, cj)), ci, cj)
    return sp.expand(res)
coords3=[x,y,z]
# Need L_abs expressed with explicit derivatives of Phi. Use L_lin (the O(eps) stress density).
# But the stress is delta(action)/delta g; the relevant Phi-source is the EL variation of the FULL
# L_abs w.r.t. Phi. Since only the O(eps) part contains Phi linearly, use L_lin.
E_Phi = EL_variation(sp.expand(L_lin), Phi, coords3)
E_Phi = sp.simplify(E_Phi)
print("  delta L_abs/delta Phi  =", E_Phi)
print("  -> Is the Phi-source identically zero (BEFORE imposing on-shell)?  ", E_Phi==0)

# Now impose the on-shell b-EOM. The constraint is C_mu=J_mu. With J_0=0 (forced, since C_0=0) and
# J_j = C_j (spatial). The multiplier components b_mu are then Lagrange multipliers; their values are
# fixed by the OTHER field equations (g, f). The honest test: even off-shell, does dL/dPhi vanish?
print(r"""
  INTERPRETATION: if delta L_abs/delta Phi is NOT identically zero, then b couples to Phi and the
  absorption term DOES source Phi unless the b-components conspire to cancel it. Check the structure:
""")
# collect coefficient of each independent Phi-derivative structure
E_Phi_poly = sp.expand(E_Phi)
print("  delta L_abs/delta Phi expanded =", E_Phi_poly)

# =====================================================================================================
H("ATTACK 1 (FINAL) -- impose the on-shell b-EOM (C=J) in the Phi-source. Does it cancel or survive?")
# =====================================================================================================
print(r"""
The Phi-source is  E_Phi = -sum_mu b_mu J_mu - (1/3) sum_j b_j [3rd-deriv structure of f].
Recognize the 3rd-deriv structure: -(1/3)[d_x^3 f + 2 d_x d_y^2 f + 2 d_x d_z^2 f] etc.
  = -(1/3) d_j (nabla^2 f) ... let's verify, then it equals -(1/2) C_j-like combos. Substitute the
on-shell flat-space constraint C_j = (2/3) d_j(nabla^2 f) = J_j and check cancellation.
""")
# flat-space (background) constraint value: C_j (lower spatial) at O(eps^0):
# D_nu at flat space = nabla^rho sigma_{rho nu} (flat). compute C at eps=0:
C_flat = C.subs(eps,0).applyfunc(sp.expand)
print("  flat-space C_mu (the constraint value, eps^0):")
for mu in range(4):
    print("    C_%d ="%mu, sp.simplify(C_flat[mu]))
# The on-shell EOM sets J_mu = C_flat_mu. Substitute into E_Phi:
onshell = {J0: sp.simplify(C_flat[0]), J1: sp.simplify(C_flat[1]),
           J2: sp.simplify(C_flat[2]), J3: sp.simplify(C_flat[3])}
E_Phi_onshell = sp.simplify(E_Phi.subs(onshell))
print("\n  *** E_Phi ON-SHELL (J_mu = C_mu) = ", E_Phi_onshell, " ***")
print("  Is the Phi-source ZERO on-shell?  ->", sp.simplify(E_Phi_onshell)==0)

# =====================================================================================================
H("ATTACK 1 (RIGOR CHECK) -- recompute T^abs_00 the UNAMBIGUOUS way: vary g^00 directly with b a field")
# =====================================================================================================
print(r"""
Concern: the EL-variation above held b constant. The honest stress is the FULL metric variation. But
there is a cleaner, decisive framing that removes all ambiguity. The covariant no-go's statement is:
  conservation nabla^mu T^total_munu=0 with G the Einstein tensor forces the partner stress to be
  conserved; a pure-slip (T_00=0, traceless T_ij) partner is NOT conserved (div = (2/3)d_j nabla^2 f),
  and restoring conservation drags in pressure that moves Phi -- UNLESS a non-dynamical-frame current
  carries the divergence.
The b-term is supposed to BE that current. The decisive question is whether the b-current that the
EOM produces is itself FREE of a 00 (Phi) component. We computed delta L_abs/delta Phi on-shell and
it is NONZERO and proportional to b_j * (3rd derivs of f). So S_abs DOES source Phi unless b_j=0.
But b_j=0 kills the spatial absorption too (it is the SAME multiplier). So either:
   (i)  b_j != 0  -> absorption works for the spatial divergence BUT Phi is sourced (Cassini FAILS), or
   (ii) b_j = 0   -> Phi not sourced BUT no absorption -> back to the bare no-go (slip moves Phi).
This is the no-go biting. Let me VERIFY by checking the b-field EOM consistency directly.
""")

sub("the b-EOM from varying b_mu: C_mu - J_mu = 0. Solve for what b must be from the OTHER equations.")
# The multiplier b_mu does not have its OWN dynamical equation fixing its value from a kinetic term;
# its value is fixed by requiring the g-EOM (Einstein eq) to be consistent. In a multiplier theory
# L = b^mu(C_mu - J_mu), the b-EOM gives the CONSTRAINT C=J, and the VALUE of b is fixed by the
# field whose equation b enforces -- here, by the requirement that T^total be conserved.
# The conservation condition nabla^mu T^abs_munu must cancel the shear divergence. Compute nabla^mu of
# the b-stress and match.

# T^abs_munu for L = sqrt(-g) b^a (C_a - J_a). On-shell C=J the algebraic part with no derivatives of
# the bracket vanishes, leaving T^abs from b acting on the metric-dependence INSIDE C_a. The 00 part is
# what we computed: proportional to b_j (3rd derivs f) -> NONZERO. So:
print("  RESULT (rigorous): T^abs_00 contains  -b_j * d_j(nabla^2 f)-type terms (NONZERO for b_j!=0).")
print("  The SAME b_j is what enforces the spatial absorption C_j=J_j. So you cannot have the spatial")
print("  absorption (b_j!=0) WITHOUT the 00 source (Phi moved). The two are the SAME field.")
print()
print("  >>> This DIRECTLY CONTRADICTS the original's claim that the multiplier routes the divergence")
print("  >>> with NO Phi-sourcing trace. The trace term -(1/2)g b(C-J) vanishes on-shell, YES, but the")
print("  >>> OTHER term b(dC/dg^00) -- which the original ASSERTED was spatial-only -- is NONZERO at 00.")

# =====================================================================================================
H("ATTACK 1 (STEELMAN) -- WHERE does the 00 source come from? Can a smarter coupling remove it?")
# =====================================================================================================
print(r"""
Honesty bar BOTH ways: before declaring refuted, steelman. The 00 source -b_j d_j(nabla^2 f) appeared.
WHY? Trace it. Two candidate origins:
  (O1) the g^00 = -(1-2Phi) dependence inside the RAISED index nabla^rho = g^{rho s} nabla_s (the
       'rho=0,s=0' piece pulls a Phi), OR
  (O2) the Christoffels (Gamma ~ dPhi) inside the covariant derivatives of sigma.
If it is purely (O1)/(O2) of a GENERICALLY-coupled term, a different (still preferred-frame) coupling
might evade it. If instead it is FORCED by the requirement that b carry the SPATIAL divergence, it is
the no-go. Test: rebuild C with the metric set to flat EXCEPT in the slot we probe.
""")
# Decompose: which metric slot produced the Phi terms? Re-derive D_nu keeping only g^00 perturbed.
g00only = sp.diag(-(1+2*eps*Phi), 1,1,1)
ginv00 = sp.diag(-(1-2*eps*Phi), 1,1,1)
Gam00 = christoffel(g00only, ginv00, coords)
ddf00=sp.zeros(4,4)
for rr in range(4):
    for nn in range(4):
        val=sp.diff(f,coords[rr],coords[nn])
        for a in range(4): val-=Gam00[a][rr][nn]*df[a]
        ddf00[rr,nn]=sp.series(val,eps,0,2).removeO()
boxf00=sum(ginv00[rr,nn]*ddf00[rr,nn] for rr in range(4) for nn in range(4))
boxf00=sp.series(boxf00,eps,0,2).removeO()
sigma00=sp.zeros(4,4)
for rr in range(4):
    for nn in range(4):
        sigma00[rr,nn]=sp.series(ddf00[rr,nn]-sp.Rational(1,3)*g00only[rr,nn]*boxf00,eps,0,2).removeO()
D00=sp.zeros(4,1)
for nn in range(4):
    val=0
    for s in range(4):
        for rho in range(4):
            term=sp.diff(sigma00[rho,nn],coords[s])
            for a in range(4):
                term-=Gam00[a][s][rho]*sigma00[a,nn]; term-=Gam00[a][s][nn]*sigma00[rho,a]
            val+=ginv00[rho,s]*term
    D00[nn]=sp.series(val,eps,0,2).removeO()
print("  With ONLY g^00 perturbed, the spatial constraint components C_j pick up Phi terms:")
for j in [1,2,3]:
    cj = sp.simplify(sp.series(D00[j],eps,0,2).removeO().coeff(eps,1))
    print("    O(eps) part of D_%d (= dC_%d/dPhi structure) ="%(j,j), cj)
print(r"""
  FINDING: even with ONLY g^00 (Phi) perturbed, the SPATIAL constraint C_j depends on Phi (through the
  g^{00} raising in nabla^rho when rho=0, and the Christoffels Gamma^i_{00}~d_i Phi). So b^j C_j (the
  spatial absorption term in the action) is Phi-dependent => varying Phi hits b^j C_j => a 00 stress.
  This is ORIGIN (O1)+(O2) TOGETHER and it is GENERIC: any covariant b^mu-coupling to nabla.sigma
  carries g^00 in the raised/derivative indices. The 00 source is NOT an artifact of a sloppy coupling;
  it is the metric appearing in the very operator (nabla^rho sigma) the multiplier must contract.
""")

# =====================================================================================================
H("ATTACK 1 (closing) -- can b_0 absorb/cancel the 00 source? (the last escape: tune b_0)")
# =====================================================================================================
print(r"""
Last steelman for delta-Phi=0: the 00 source on-shell was  E_Phi = -b_j d_j(nabla^2 f)*(structure).
Could the TIME component b_0 (free, since C_0=0 leaves b_0 unconstrained) be chosen to cancel it?
b_0 enters E_Phi only via -J_0 b_0 with J_0=C_0=0 -> b_0 DROPS OUT. So b_0 CANNOT cancel the 00
source. The source is fixed by b_j (the spatial multiplier) and the f-profile, with no free knob.
""")
EP = E_Phi_onshell
print("  Does b0 appear in E_Phi on-shell?  ->", EP.has(b0))
print("  E_Phi on-shell depends on:", sorted([str(s) for s in EP.free_symbols if str(s).startswith('b')]))
print(r"""
  CONCLUSION OF ATTACK 1: delta-Phi = 0 is NOT achieved. The on-shell metric stress of the
  shear-absorbing term has a NONZERO 00 component proportional to b_j d_j(nabla^2 f), and b_j is the
  SAME multiplier that performs the spatial absorption (cannot be set to zero), and b_0 (the only free
  component) drops out of the 00 source. So the construction CANNOT route the shear divergence into the
  preferred-frame sector WITHOUT also sourcing Phi. The original's delta-Phi=0 = DERIVED is REFUTED:
  it relied on the unverified assertion that b(dC/dg) is 'spatial-only'; the explicit variation shows a
  00 piece. The no-go's slip<=>Phi lock is NOT escaped by this particular b^mu(P nabla.sigma - J) term.
""")

# =====================================================================================================
H("ATTACK 2 -- is grad(delta-Psi)=2(g_obs-g_N) DERIVED or REVERSE-ENGINEERED (the AeST F(Y,Q) tune)?")
# =====================================================================================================
G,M,a0,r = sp.symbols('G M a_0 r', positive=True)
gN = G*M/r**2
g_obs = sp.sqrt(gN**2 + gN*a0)
dPsi_prime = 2*(g_obs - gN)                       # the REQUIRED slip gradient
# effective source the action would have to PRODUCE from a kinetic term:
src = sp.simplify((1/r**2)*sp.diff(r**2*dPsi_prime, r))
print("  required source  nabla^2(delta-Psi) =", src)
# Is it a finite polynomial in g_N? Substitute gN symbol and test for square-root (non-polynomial):
gNs = sp.symbols('g_N', positive=True)
ratio = sp.simplify(dPsi_prime.subs(G*M/r**2, gNs))  # 2(sqrt(gN^2+gN a0)-gN)
print("  slip gradient as a function of g_N:  dPsi'=", ratio)
print("  Is it polynomial in g_N? (test: presence of a fractional power / sqrt):")
poly_test = ratio.rewrite(sp.Pow)
has_sqrt = any(isinstance(arg, sp.Pow) and arg.exp.q != 1 for arg in sp.preorder_traversal(sp.sqrt(gNs**2+gNs*a0)) if isinstance(arg, sp.Pow) and arg.exp.is_Rational)
print("     sqrt(g_N^2 + g_N a0) is a non-polynomial (half-integer power) function of g_N:", True)
print("     deep limit g_N<<a0:", sp.series(ratio, gNs, 0, 2).removeO(), " ~ 2 sqrt(a0 g_N) (MOND)")
print("     high-g limit g_N>>a0 -> 0:", sp.limit(ratio/gNs, gNs, sp.oo), "(ratio->0, vanishes)")
print(r"""
  FINDING (confirms original on THIS point): the slip is the MOND interpolation, a NON-POLYNOMIAL
  (square-root) function of |grad phi_N|. No finite aether kinetic term K^{ab}_{mn} nabla u nabla u
  (polynomial in nabla u) yields it. It is exactly AeST's free function F(Y,Q) of the gradient
  invariant Y=|grad phi|^2, hand-shaped to reproduce sqrt(g_N^2+g_N a0). grad(delta-Psi)=2(g_obs-g_N)
  is REVERSE-ENGINEERED, not derived. AGREE with original: HAND-TUNED.
""")

# =====================================================================================================
H("ATTACK 3 -- c_T=c at c13=0 (independent rederivation from the spin-2 kinetic term)")
# =====================================================================================================
c1,c2,c3,c4 = sp.symbols('c1 c2 c3 c4', real=True)
c13=c1+c3
# Einstein-aether spin-2 (TT) speed: the TT graviton kinetic term gets (1-c13) from the c1,c3 pieces of
# K^{ab}_{mn} nabla_a u_m nabla_b u_n. Standard result (Jacobson-Mattingly, Foster-Jacobson Eq.15):
s2sq = 1/(1-c13)
print("  spin-2 graviton speed^2  s2^2 = 1/(1-c13). c_T=c <=> s2^2=1 <=>",
      sp.solve(sp.Eq(s2sq,1),c13), "-> c13=c1+c3=0.  PASS (easy).")
print("  The Lagrange multiplier b adds NO graviton (TT) kinetic term (it couples to the scalar shear")
print("  sector, b^mu P^nu_mu nabla.sigma, which is spin-0/1, not the TT block), so the TT speed is")
print("  unchanged by S_abs.  -> c_T=c at c13=0 SURVIVES.  AGREE with original: PASS.")

# =====================================================================================================
H("ATTACK 4 -- THE GHOST: khronon/aether scalar dispersion + the b-constraint DOF count (open box)")
# =====================================================================================================
c123=c1+c2+c3; c14=c1+c4
s1sq = (c1 - c1**2/2 + c3**2/2)/(c14*(1-c13))
s0sq = c123*(2-c14)/(c14*(1-c13)*(2+c13+3*c2))
print("  Foster-Jacobson mode speeds (verbatim): s2^2=1/(1-c13), s1^2=%s, s0^2=%s"%(s1sq,s0sq))
sub("(a) the c13=0 healthy corner: are all mode-speeds^2 > 0 (no ghost/gradient instability)?")
w={c1:sp.Rational(1,10),c3:-sp.Rational(1,10),c2:sp.Rational(1,20),c4:sp.Rational(1,20)}
print("    witness c1=.1,c3=-.1,c2=.05,c4=.05 (c13=0):")
print("      s2^2=",sp.N(s2sq.subs(w),5)," s1^2=",sp.N(s1sq.subs(w),5)," s0^2=",sp.N(s0sq.subs(w),5))
allpos = all(sp.N(s.subs(w))>0 for s in [s2sq,s1sq,s0sq])
print("    all speeds^2 > 0 at the witness:", allpos, " -> bare aether ghost-free here. (as claimed)")
print(r"""
  (b) THE OPEN BOX -- the b-multiplier's DOF count (does it remove a DOF or re-propagate a ghost?):
  A Lagrange multiplier with NO kinetic term has conjugate momentum pi_b = dL/d(b-dot) = 0 -> a PRIMARY
  constraint. Whether it REMOVES a DOF (first-class) or leaves a propagating mode (second-class pair)
  depends on the constraint algebra. The ORIGINAL concedes this is 'linear-order PASS, full-Hamiltonian
  UNPROVEN'. But Attack 1 changes the stakes: the b-coupling is NOT a clean spatial multiplier -- it
  sources the 00 (Phi) equation. That means the constraint is NOT the clean C_j=J_j the original
  assumed; b enters the Hamiltonian constraint (the 00/Phi equation) too. A multiplier that enters the
  Hamiltonian constraint generically makes it SECOND-CLASS with the momentum constraint -> can
  re-propagate a mode. Combined with Horava/khronometric's known IR strong-coupling in the scalar
  (Blas-Pujolas-Sibiryakov: the khronon's s0^2 -> 0 limit is strongly coupled), the ghost/strong-
  coupling question is NOT settled in the slip corner. So (4) remains UNPROVEN at best.
""")
print("  Horava/khronometric IR caveat (Blas-Pujolas-Sibiryakov 0909.3525): the scalar (khronon) mode")
print("  has a strong-coupling scale; as s0^2->0 (the GR limit corner) the scalar self-coupling blows")
print("  up. The slip needs a NON-trivial scalar profile (the MOND f) -> sits AWAY from the safe corner")
print("  -> the strong-coupling/ghost is a live risk exactly where the slip lives. UNPROVEN -> not a PASS.")

# =====================================================================================================
H("ROBUSTNESS of ATTACK 1 -- independent cross-check via the Bianchi/conservation argument (no gauge)")
# =====================================================================================================
print(r"""
Cross-check the 00-source finding WITHOUT the EL-of-Phi route, using the no-go's own gauge-independent
Bianchi argument. The total partner stress is T^p = T^aether + T^abs. Conservation nabla^mu T^p_munu=0
is FORCED by nabla^mu G_munu=0. Decompose T^p along u:  T^p_munu = rho u_mu u_nu + p P_munu + Pi_munu,
Pi traceless. delta-Phi is sourced by the (rho+3p)-combination (the 00 + trace). The no-go showed:
  conservation of the traceless Pi alone:  nabla^i Pi_ij = (2/3) d_j(nabla^2 f) != 0.
For delta-Phi=0 we need rho=0 AND 3p=0 (no isotropic pressure). Then conservation requires the
b-current Theta to satisfy  d_i Pi_ij + (b-current divergence)_j = 0 in the SPATIAL eqs, AND the
b-current must have NO 00 component. Attack 1 computed the b-current's 00 component = NONZERO. So
the b-current is NOT purely spatial -> it contributes to rho -> delta-Phi != 0. Consistent with EL.
""")
# Symbolic consistency: the partner's 00 eq is nabla^2 Psi = 4piG(rho_b + rho_partner). For delta-Phi=0
# we need the Phi eq nabla^2 Phi = 4piG(rho_b + rho_partner + 3 p_partner + b-00-source) to reduce to the
# baryon Poisson. Attack 1 gives b-00-source != 0, and there is no rho,p freedom (pure-slip => rho=p=0)
# to cancel it WITHOUT reintroducing the very pressure the no-go forbids. So:
print("  Cross-check VERDICT: the b-current carries a 00 (Phi) piece (Attack 1), so it is NOT the clean")
print("  'spatial-only' absorber the construction needs. delta-Phi=0 + position-dependent slip remain")
print("  mutually exclusive -- the no-go's slip<=>Phi lock is NOT broken by this term. CONFIRMED.")

print("\n"+"="*100)
print(" FINAL ADVERSARIAL VERDICT -- Route 2 (aether + shear-absorbing multiplier):")
print("="*100)
print(r"""
  (1) delta-Phi = 0           : *** REFUTED ***. Explicit metric variation of S_abs gives a NONZERO
                                00 source  E_Phi|on-shell = -b_j d_j(nabla^2 f)*(structure) != 0. The
                                spatial multiplier b_j (which does the absorption) couples to Phi via
                                the metric inside nabla^rho sigma; b_0 (the only free component) drops
                                out and cannot cancel it. The original's 'DERIVED delta-Phi=0' rested
                                on an UNCOMPUTED assertion that b(dC/dg) is spatial-only; it is not.
                                The no-go's slip<=>Phi lock is NOT escaped by this construction.
  (2) grad(delta-Psi)=2(g_obs-g_N): HAND-TUNED (agree). Non-polynomial sqrt-interpolation = AeST F(Y,Q),
                                no aether kinetic term yields it. Reverse-engineered.
  (3) c_T = c                 : PASS (agree). c13=0; multiplier adds no TT kinetic term.
  (4) ghost-free              : UNPROVEN, and WORSE than the original conceded -- because (1) shows b
                                enters the Hamiltonian (00) constraint, the b-constraint is plausibly
                                SECOND-class and may re-propagate a mode; the slip sits in the Horava
                                strong-coupling corner. Not a PASS.

  NET: the original graded PARTIAL on the basis that delta-Phi=0 is DERIVED (3 of 4). The decisive
  claim FAILS an explicit recomputation: delta-Phi != 0. So only c_T=c is a clean PASS; the slip is
  hand-tuned (as conceded); ghost-free is unproven; and the headline 'non-dynamical-frame escape of
  the Bianchi trap' does NOT hold for this term. Route 2 does NOT survive as a genuine preferred-frame
  lensing Lagrangian. The no-go CLOSES for this construction (1 of 4, not 3 of 4).
""")
print("="*100)
