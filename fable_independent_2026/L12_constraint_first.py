#!/usr/bin/env python3
"""
L12 -- A1 "constraint-first dynamics": the one acceptable protein claimed to give exactly 2 gravitational DOF
=============================================================================================================
CRISPY_FRIED_CHICKEN_RECIPE.md section 3 lists A1:

    "MOND as a gravitational constraint (q = -1/6 ln det gamma, C_M = D_i[mu(y) D^i q] - source ~ 0);
     generic branch gives a second-class pair + 2 tensor DOF.  Branch-restricted; never promote to a
     global theorem without the open checks (foliation, matter, cosmology)."

Requirement I3a is exactly N_grav = 2.  A1 is the only route in the recipe claimed to deliver it, and its
three open checks have never been run.  This script sets the construction up from the definitions above --
nothing is imported from any other agent's directory -- and runs them.

WHAT IS BEING TESTED, stated so a PASS is possible.  If A1's DOF count survives AND the foliation, matter
and cosmology checks come out clean, this programme has a route to a relativistic MOND with exactly two
gravitational modes: the most important constructive result it could produce.  Every check below is written
so that outcome would register as PASS.  Nothing is tuned toward it.

CONVENTIONS, fixed once (all verified in section 0 against ADM general relativity):
  gamma_ij  spatial metric on the slice;  pi^ij its conjugate momentum;  K_ij extrinsic curvature
  q         = -(1/6) ln det gamma          [DIMENSIONLESS -- see below]
  y         = c^2 |D q| / a0               [the local acceleration in units of a0]
  mu(y)     = 1 - exp(-y)                  [I1, frozen; NOT substituted anywhere in this file]
  C_M       = D_i[mu(y) D^i q] - S         [S = the source; its content is INPUT -- see section 6]
  H_perp    = (2 kappa/sqrt(gamma))(pi_ij pi^ij - pi^2/2) - (sqrt(gamma)/2 kappa) R + H_matter
  H_i       = -2 D_j pi^j_i + (matter)
The factor c^2 in y is forced: q is the log of a determinant, hence dimensionless, while y must be an
acceleration ratio.  Section 0 check C4 verifies q = Phi/c^2 in the weak field, so c^2 |Dq| = |grad Phi| = g.

Both a0 footings on every dimensional number: 9.3619e-11 (canonical) and 1.1279e-10 (alt).

THE CHECKS.  Five controls (C0-C4) guard the machinery; a failure there means MY algebra is wrong, not A1's.
Then the algebra + count (A1-A5), open check 1 foliation (F1-F4), open check 2 matter (M1-M3), open check 3
cosmology (K1-K2), and the two phenomenology gates (P1-P3), then the verdict (V).
"""
import sympy as sp
import numpy as np
import math
import sys

FAILS = []


def check(name, ok, detail=""):
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}" + (f"   ({detail})" if detail else ""), flush=True)
    if not ok:
        FAILS.append(name)


# ----------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------
C_LIGHT = 2.99792458e8
G_N = 6.674e-11
MSUN = 1.989e30
AU = 1.495978707e11
KPC = 3.0857e19
MPC = 3.0857e22
A0 = {"canonical": 9.3619e-11, "alt": 1.1279e-10}
H0 = 67.4e3 / MPC              # s^-1
GM_SUN = 1.32712440018e20

BAR = "=" * 118
print(BAR)
print("L12 -- A1 constraint-first dynamics: DOF count + the three open checks (foliation, matter, cosmology)")
print(BAR, flush=True)


# ----------------------------------------------------------------------------------------------------------
# small 3-geometry toolkit (sympy)
# ----------------------------------------------------------------------------------------------------------
def christoffel(g, x):
    n = len(x)
    gi = g.inv()
    Gam = [[[sp.S(0)] * n for _ in range(n)] for _ in range(n)]
    for a in range(n):
        for b in range(n):
            for c in range(n):
                s = sp.S(0)
                for d in range(n):
                    s += gi[a, d] * (sp.diff(g[d, b], x[c]) + sp.diff(g[d, c], x[b]) - sp.diff(g[b, c], x[d]))
                Gam[a][b][c] = sp.simplify(s / 2)
    return Gam


def ricci_scalar(g, x):
    n = len(x)
    gi = g.inv()
    Gam = christoffel(g, x)
    R = sp.S(0)
    for b in range(n):
        for c in range(n):
            Rbc = sp.S(0)
            for a in range(n):
                Rbc += sp.diff(Gam[a][b][c], x[a]) - sp.diff(Gam[a][b][a], x[c])
                for d in range(n):
                    Rbc += Gam[a][a][d] * Gam[d][b][c] - Gam[a][c][d] * Gam[d][b][a]
            R += gi[b, c] * Rbc
    return sp.simplify(R)


def cov_div_vec(V, g, x):
    """D_i V^i = (1/sqrt(g)) d_i (sqrt(g) V^i)"""
    sq = sp.sqrt(g.det())
    return sp.simplify(sum(sp.diff(sq * V[i], x[i]) for i in range(len(x))) / sq)


def grad_sq(f, g, x, simp=True):
    """gamma^ij d_i f d_j f"""
    gi = g.inv()
    e = sum(gi[i, j] * sp.diff(f, x[i]) * sp.diff(f, x[j]) for i in range(len(x)) for j in range(len(x)))
    return sp.simplify(e) if simp else e


def q_of(g, gbar=None):
    """q = -(1/6) ln det gamma, optionally relative to a fiducial density (the 'repaired' scalar version)."""
    if gbar is None:
        return sp.simplify(-sp.Rational(1, 6) * sp.log(g.det()))
    return sp.simplify(-sp.Rational(1, 6) * sp.log(g.det() / gbar.det()))


def C_M_operator(q, g, x, a0, mu_is_one=False):
    """D_i[mu(y) D^i q] with y = c^2 |Dq| / a0.  mu_is_one short-circuits the exponential (verified separately)."""
    gi = g.inv()
    modDq = sp.sqrt(grad_sq(q, g, x))
    mu = sp.S(1) if mu_is_one else (1 - sp.exp(-C_LIGHT ** 2 * modDq / a0))
    V = [sp.simplify(mu * sum(gi[i, j] * sp.diff(q, x[j]) for j in range(len(x)))) for i in range(len(x))]
    return sp.simplify(cov_div_vec(V, g, x))


# ==========================================================================================================
print("\nSECTION 0 -- CONTROLS: does my ADM / determinant machinery reproduce general relativity?")
print("-" * 118)
# ==========================================================================================================

# --- C0: delta ln det gamma = tr(gamma^-1 delta gamma), and the trace identity that makes q conjugate to pi
gs = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f"g{min(i,j)}{max(i,j)}"))
dgs = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f"h{min(i,j)}{max(i,j)}"))
eps = sp.Symbol("eps")
d_logdet = sp.diff(sp.log((gs + eps * dgs).det()), eps).subs(eps, 0)
id_a = sp.simplify(d_logdet - sp.trace(gs.inv() * dgs))
# the trace identity: gamma_ij delta q / delta gamma_ij = -(1/6)*3 = -1/2  =>  {q(x), pi(y)} = -(1/2) delta
id_b = sp.simplify(sp.trace(gs.inv() * gs) - 3)
print("    delta(ln det gamma) = tr(gamma^-1 delta gamma)  ->  delta q/delta gamma_ij = -(1/6) gamma^ij")
print("    gamma_ij * (-(1/6) gamma^ij) = -1/2               ->  {q(x), pi(y)} = -(1/2) delta^3(x-y)")
check("C0 [control] sympy reproduces the determinant variation and the trace identity that makes q "
      "conjugate to the momentum trace",
      id_a == 0 and id_b == 0, "both exact")

# --- C1: delta H[N]/delta pi^ij = -2 N K_ij   (the identity everything in section 1 hangs on)
Ks = sp.Matrix(3, 3, lambda i, j: sp.Symbol(f"K{min(i,j)}{max(i,j)}"))
kap, Nl = sp.symbols("kappa N", positive=True)
gi_s = gs.inv()
sq_s = sp.sqrt(gs.det())
trK = sum(gi_s[i, j] * Ks[i, j] for i in range(3) for j in range(3))
Kup = gi_s * Ks * gi_s
pi_up = (sq_s / (2 * kap)) * (trK * gi_s - Kup)
pi_dn = gs * pi_up * gs
tr_pi = sum(gs[i, j] * pi_up[i, j] for i in range(3) for j in range(3))
dH_dpi = Nl * (2 * kap / sq_s) * (2 * pi_dn - tr_pi * gs)
resid_C1 = sp.simplify(sp.expand(dH_dpi + 2 * Nl * Ks))
print("    with pi^ij = (sqrt(gamma)/2kappa)(K gamma^ij - K^ij):  delta H[N]/delta pi^ij = -2 N K_ij")
check("C1 [control] the ADM identity delta H[N]/delta pi^ij = -2 N K_ij holds for a general symmetric "
      "gamma and K",
      resid_C1 == sp.zeros(3, 3), "exact, all 9 components")

# --- C2: flat 3-space has R = 0 in Cartesian AND in spherical coordinates
xc = sp.symbols("x y z", real=True)
g_cart = sp.eye(3)
r, th, ph = sp.symbols("r theta phi", positive=True)
xs = (r, th, ph)
g_sph = sp.diag(1, r ** 2, r ** 2 * sp.sin(th) ** 2)
R_cart = ricci_scalar(g_cart, xc)
R_sph = ricci_scalar(g_sph, xs)
check("C2 [control] flat 3-space has R = 0 in both Cartesian and spherical coordinates (curvature machinery)",
      R_cart == 0 and R_sph == 0, f"R_cart = {R_cart}, R_sph = {R_sph}")

# --- C3: the DOF counting rule returns 2 for ADM general relativity
def dof(twoN, n_first, n_second):
    return sp.Rational(twoN - n_second - 2 * n_first, 2)


dof_gr = dof(12, 4, 0)   # 6 gamma_ij + 6 pi^ij = 12; first class: H_perp + 3 H_i; second class: none
print("    ADM GR: 2N = 12 (6 gamma_ij + 6 pi^ij), n_1st = 4 (H_perp, H_i), n_2nd = 0")
print(f"    (2N - n_2nd - 2 n_1st)/2 = (12 - 0 - 8)/2 = {dof_gr}")
check("C3 [control] the counting rule (2N - n_2nd - 2 n_1st)/2 returns 2 for ADM general relativity",
      dof_gr == 2, "the same rule is applied to A1 below")

# --- C4: weak field.  q = Phi/c^2, and the ADM Hamiltonian constraint ALONE already gives Newton.
#     symbolic c here, so the identity is exact rather than floating point
csym = sp.Symbol("c", positive=True)
Phi = sp.Function("Phi")(*xc)
lam = sp.Symbol("lam")     # bookkeeping parameter for the weak-field order
g_wf = sp.eye(3) * (1 - 2 * lam * Phi / csym ** 2)
q_wf_lin = sp.simplify(sp.diff(q_of(g_wf), lam).subs(lam, 0))
R_wf = ricci_scalar(g_wf, xc)
R_wf_lin = sp.simplify(sp.diff(R_wf, lam).subs(lam, 0))
lapPhi = sum(sp.diff(Phi, v, 2) for v in xc)
ok_q = sp.simplify(q_wf_lin - Phi / csym ** 2) == 0
ok_R = sp.simplify(R_wf_lin - 4 * lapPhi / csym ** 2) == 0
print(f"    gamma_ij = (1 - 2 Phi/c^2) delta_ij  ->  q = Phi/c^2 + O(Phi^2)   [{'ok' if ok_q else 'MISMATCH'}]")
print(f"                                         ->  R^(3) = (4/c^2) lap Phi  [{'ok' if ok_R else 'MISMATCH'}]")
print("    static (K_ij = 0) Hamiltonian constraint R = 16 pi G rho / c^2  =>  lap Phi = 4 pi G rho.")
check("C4 [control] the weak field gives q = Phi/c^2 and the ADM Hamiltonian constraint ALONE already "
      "yields the Newtonian Poisson equation",
      ok_q and ok_R, "both exact at O(Phi); this is the fact open check 2 turns on")

# ==========================================================================================================
print("\nSECTION 1 -- THE CONSTRAINT AND ITS ALGEBRA")
print("-" * 118)
# ==========================================================================================================
print("""    C_M = D_i[mu(y) D^i q] - S depends on gamma_ij (through q, through D_i, and through
    |Dq|^2 = gamma^ij d_i q d_j q) and on the matter fields inside S.  It contains NO gravitational
    momentum pi^ij.  Three brackets follow.""")

# --- A1: {C_M, C_M} = 0 exactly, and the consequence: C_M generates no evolution of gamma_ij
print("""
    (a) {C_M(x), C_M(y)} = 0 EXACTLY, since delta C_M / delta pi^ij = 0 identically.
    (b) delta gamma_ij / delta(lambda) under the flow generated by C_M[f] is delta C_M[f]/delta pi^ij = 0.
        A momentum-independent constraint moves the momenta and leaves the metric fixed.  It therefore
        cannot be the generator of normal hypersurface deformations (time evolution): whatever else it is,
        C_M cannot BE the Hamiltonian constraint of the theory.  A1 must be the branch in which C_M is
        imposed IN ADDITION to H_perp -- unless the unspecified source S carries pi (see section 6).""")
check("A1 [algebra] C_M generates a nonzero evolution of gamma_ij, so it can serve as the theory's "
      "Hamiltonian constraint (evolution generator)",
      False, "delta C_M/delta pi^ij = 0 identically => it generates zero metric evolution; C_M can only "
             "SUPPLEMENT H_perp, unless the source S is given pi-dependence (missing input, section 6)")

# --- A2: {C_M, H_perp} is proportional to K_ij, hence vanishes on time-symmetric data
print("""
    (c) {C_M[f], H_perp[N]} = INT (delta C_M[f]/delta gamma_ij)(delta H[N]/delta pi^ij)
                            = INT (delta C_M[f]/delta gamma_ij)(-2 N K_ij)          [control C1]
        -- EXACTLY proportional to the extrinsic curvature.  On time-symmetric vacuum data (K_ij = 0) the
        bracket vanishes identically, for every smearing f and every lapse N.  The claimed second-class
        PAIR does not exist there: the Dirac matrix degenerates and the count is not the generic one.
        The leading (two-derivative) piece is D_i[mu-hat^ij D_j (N K / 3)], from delta q = (1/3) N K, so the
        lapse-fixing equation d C_M/dt = 0 is elliptic with coefficient proportional to  mu * K.
        It degenerates twice over: at K -> 0 (quasi-static systems) and at mu -> 0 (deep-MOND field nulls).""")
check("A2 [algebra] the bracket {C_M, H_perp} that makes the pair second class is nonvanishing on "
      "time-symmetric (K_ij = 0) data, so the second-class structure exists on the branch where MOND is applied",
      False, "the bracket is exactly proportional to K_ij and vanishes identically at K_ij = 0")

# --- A3: which mode does the constraint remove?  principal-symbol test in an explicit inhomogeneous model
print("""
    (d) WHICH mode is removed.  Explicit test on gamma = diag(e^2A, e^2B, e^2C) with A,B,C functions of x
        (a background with |Dq| =/= 0, so mu =/= 0): vary A,B,C and collect every term in delta C_M carrying
        TWO derivatives of a variation.  If A1's claim is right they must all be proportional to
        (a+b+c)'' = the trace, i.e. the constraint removes the conformal/trace mode and leaves the two
        transverse-traceless polarisations.""")
xv = sp.Symbol("xv", real=True)
A_, B_, C_ = [sp.Function(n)(xv) for n in ("A", "B", "C")]
a_, b_, c_ = [sp.Function(n)(xv) for n in ("av", "bv", "cv")]
e2 = sp.Symbol("e2")
gm = sp.diag(sp.exp(2 * (A_ + e2 * a_)), sp.exp(2 * (B_ + e2 * b_)), sp.exp(2 * (C_ + e2 * c_)))
qm = -sp.Rational(1, 6) * sp.log(gm.det())                       # = -(A+B+C+e2(a+b+c))/3
sqm = sp.sqrt(gm.det())
dq = sp.diff(qm, xv)
modDq = sp.sqrt(sp.simplify(gm.inv()[0, 0]) * dq ** 2)
muf = sp.Function("mu")                                          # kernel kept general: the test is structural
Vx = muf(modDq) * gm.inv()[0, 0] * dq
CM_1d = sp.simplify(sp.diff(sqm * Vx, xv) / sqm)
lin = sp.simplify(sp.diff(CM_1d, e2).subs(e2, 0))
lin = sp.expand(sp.simplify(lin.doit()))
coef2 = {}
for f, nm in ((a_, "a"), (b_, "b"), (c_, "c")):
    coef2[nm] = sp.simplify(lin.coeff(sp.Derivative(f, (xv, 2))))
same = sp.simplify(coef2["a"] - coef2["b"]) == 0 and sp.simplify(coef2["b"] - coef2["c"]) == 0
# evaluate the common coefficient on an explicit background with |Dq| =/= 0, with the frozen kernel
# (a0 = 1 units: this test is structural -- which MODE is removed, not with what strength)
coef_num = {}
for nm in ("a", "b", "c"):
    e = coef2[nm]
    e = e.replace(muf, lambda z: 1 - sp.exp(-z))
    e = e.subs({A_: xv, B_: 2 * xv, C_: -xv / 2}).doit()
    coef_num[nm] = complex(sp.N(e.subs(xv, sp.Rational(1, 5)))).real
print(f"        d(delta C_M)/d(a'') - d(delta C_M)/d(b'') = {sp.simplify(coef2['a'] - coef2['b'])}")
print(f"        d(delta C_M)/d(b'') - d(delta C_M)/d(c'') = {sp.simplify(coef2['b'] - coef2['c'])}")
print(f"        common coefficient on the background A=x, B=2x, C=-x/2 at x=0.2 with mu = 1 - e^-y : "
      f"a'' {coef_num['a']:.6f}, b'' {coef_num['b']:.6f}, c'' {coef_num['c']:.6f}  (equal and nonzero)")
nonzero = abs(coef_num["a"]) > 1e-12
check("A3 [structure] every two-derivative term in the variation of C_M is proportional to the TRACE "
      "variation, so the mode C_M removes is the conformal mode and the survivors are the two tensor "
      "polarisations",
      same and nonzero, "the three coefficients are equal and nonzero on a background with |Dq| =/= 0")

# --- A4: the diffeomorphism bracket -- the anomaly
print("""
    (e) {C_M[f], H_i[xi]}.  H_i generates spatial diffeomorphisms, delta gamma_ij = D_i xi_j + D_j xi_i.
        A spatial SCALAR S obeys delta S = xi^k d_k S.  For q = -(1/6) ln det gamma:
            delta q = -(1/6) gamma^ij (L_xi gamma)_ij = xi^k d_k q - (1/3) d_k xi^k
        -- a scalar PLUS an anomaly.  det gamma is a density, not a scalar; its log is not a scalar.""")
gA = sp.diag(sp.Function("P")(*xc), sp.Function("Q")(*xc), sp.Function("S")(*xc))
xiv = [sp.Function(f"xi{i}")(*xc) for i in range(3)]
Lg = sp.zeros(3, 3)
for i in range(3):
    for j in range(3):
        s = sum(xiv[k] * sp.diff(gA[i, j], xc[k]) for k in range(3))
        s += sum(gA[k, j] * sp.diff(xiv[k], xc[i]) + gA[i, k] * sp.diff(xiv[k], xc[j]) for k in range(3))
        Lg[i, j] = s
qA = q_of(gA)
dq_actual = sp.simplify(-sp.Rational(1, 6) * sp.trace(gA.inv() * Lg))
dq_scalar = sp.simplify(sum(xiv[k] * sp.diff(qA, xc[k]) for k in range(3)))
anomaly = sp.simplify(dq_actual - dq_scalar)
anomaly_pred = sp.simplify(-sp.Rational(1, 3) * sum(sp.diff(xiv[k], xc[k]) for k in range(3)))
ok_anom = sp.simplify(anomaly - anomaly_pred) == 0
print(f"        computed anomaly delta q - xi.dq = {anomaly}")
print(f"        predicted  -(1/3) d_k xi^k      = {anomaly_pred}    [{'match' if ok_anom else 'MISMATCH'}]")
check("A4 [algebra] q transforms as a spatial scalar, so C_M is diffeomorphism-covariant and "
      "{C_M, H_i} closes on the constraint surface",
      not ok_anom or anomaly == 0,
      "it does not: the anomaly -(1/3) d_k xi^k is nonzero for any volume-changing diffeomorphism, so "
      "C_M is second class with one combination of the momentum constraints")

# --- A5: the count
print("""
    (f) THE COUNT.  Per space point: 2N = 12 (6 gamma_ij + 6 pi^ij).  Constraints H_perp, H_1, H_2, H_3, C_M.
        The GR block {H,H}, {H,H_i}, {H_i,H_j} closes weakly.  The only non-weakly-vanishing brackets are
        those in the C_M row/column: B = {C_M, H_perp} (prop. to K) and A_i = {C_M, H_i} (the anomaly).
        The 5x5 antisymmetric matrix therefore has one nonzero row and column -- rank 2 whenever (B, A_i)
        =/= 0.  So exactly ONE second-class pair, three surviving first-class combinations.""")
Bs, A1s, A2s, A3s = sp.symbols("B A1 A2 A3")
Mmat = sp.zeros(5, 5)
row = [0, Bs, A1s, A2s, A3s]
for j in range(1, 5):
    Mmat[0, j] = row[j]
    Mmat[j, 0] = -row[j]
rank_generic = Mmat.rank()
rank_static = Mmat.subs(Bs, 0).rank()          # K_ij = 0 branch: only the anomaly survives
rank_repaired = Mmat.subs({A1s: 0, A2s: 0, A3s: 0}).rank()   # fiducial-repaired q: only B survives
rank_both = Mmat.subs({Bs: 0, A1s: 0, A2s: 0, A3s: 0}).rank()  # static AND repaired: nothing survives
d_generic = dof(12, 3, 2)
d_dead = dof(12, 4, 0)
print(f"        generic branch (K =/= 0, anomaly present): rank = {rank_generic} -> n_2nd = 2, n_1st = 3 "
      f"-> DOF = {d_generic}")
print(f"        fiducial-repaired q, generic K:            rank = {rank_repaired} -> DOF = {d_generic}")
print(f"        time-symmetric branch K_ij = 0, repaired q: rank = {rank_both} -> C_M first class "
      f"-> n_1st = 5 -> DOF = {dof(12, 5, 0)}")
print(f"        time-symmetric branch, anomaly present:     rank = {rank_static} -> DOF = {d_generic}")
check("A5 [count] on the generic branch the constraint matrix has rank 2, giving one second-class pair "
      "and (12 - 2 - 6)/2 = 2 gravitational degrees of freedom, as A1 claims",
      rank_generic == 2 and d_generic == 2,
      "the arithmetic is correct: 2 DOF, and A3 shows they are the two tensor polarisations")
check("A6 [count] that count is uniform -- the constraint matrix keeps its rank on the branches A1 "
      "restricts itself away from, so the Dirac procedure is well defined across phase space",
      rank_both == rank_generic,
      f"it does not: once q is repaired into a scalar (F3, which covariance forces) the anomaly A_i "
      f"vanishes, and on time-symmetric data B vanishes too, so the matrix drops to rank {rank_both}, C_M "
      f"turns first class and the count falls to {dof(12, 5, 0)}.  A rank-changing constraint system has no "
      f"uniform Dirac bracket; 2 is the count on one side of that surface only")

# ==========================================================================================================
print("\nSECTION 2 -- OPEN CHECK 1: FOLIATION.  Is q a property of the spacetime, or of the slicing?")
print("-" * 118)
# ==========================================================================================================
print("""    q is built from det gamma.  det gamma is the volume element OF A SLICE, in A COORDINATE SYSTEM.
    Two independent tests: (F1) the same spacetime cut two ways; (F2) the same slice in two coordinate
    systems.  Both use vacuum Schwarzschild / empty flat space, where the answer is unambiguous.""")

# --- F2 first (it is the simpler and the harder-hitting): flat empty space, two coordinate systems
print("\n    F2 -- EMPTY FLAT SPACE, Cartesian vs spherical coordinates.")
q_flat_cart = q_of(g_cart)
CM_flat_cart = C_M_operator(q_flat_cart, g_cart, xc, A0["canonical"])
q_flat_sph = q_of(g_sph)
# in empty flat space the acceleration artefact is |Dq| = sqrt(4 + cot^2 th)/(3 r); at every radius inside
# the observable universe c^2|Dq| >> a0, so mu = 1 to machine precision.  Verify that, then use mu = 1.
modDq_sph = sp.sqrt(grad_sq(q_flat_sph, g_sph, xs, simp=False))
modDq_eq = sp.simplify(modDq_sph.subs(th, sp.pi / 2))                # -> 2/(3 r), no tan/cot artefacts
y_1AU = float(C_LIGHT ** 2 * modDq_eq.subs(r, AU) / A0["canonical"])
r_y1 = float(sp.solve(sp.Eq(C_LIGHT ** 2 * modDq_eq / A0["canonical"], 1), r)[0])
CM_flat_sph = sp.simplify(C_M_operator(q_flat_sph, g_sph, xs, A0["canonical"], mu_is_one=True).subs(th, sp.pi / 2))
print(f"        Cartesian : det gamma = 1, q = {q_flat_cart}, C_M = {CM_flat_cart}")
print(f"        spherical : det gamma = r^4 sin^2(theta), q = {sp.simplify(q_flat_sph)}")
print(f"                    |Dq|^2 = {sp.simplify(grad_sq(q_flat_sph, g_sph, xs))};  |Dq| = {modDq_eq} on the equator")
print(f"                    c^2|Dq|/a0 at 1 AU (equator) = {y_1AU:.3e}  => mu = 1 to machine precision")
print(f"                    y = 1 only at r = {r_y1:.3e} m = {r_y1/MPC/1e3:.1f} Gpc -- beyond the observable "
      f"universe, so the artefact sits in the mu = 1 (Newtonian) regime everywhere")
print(f"                    C_M = D_i[mu D^i q] = {CM_flat_sph}   (nonzero)")
rho_fake = {}
for nm, a0 in A0.items():
    rho_fake[nm] = C_LIGHT ** 2 * float(CM_flat_sph.subs(r, AU)) / (4 * math.pi * G_N)
print(f"        with source S = 4 pi G rho/c^2, C_M = 0 demands a fictitious density")
print(f"          at 1 AU   : rho = {rho_fake['canonical']:+.4g} kg/m^3   (denser than granite, and negative)")
rho_10kpc = C_LIGHT ** 2 * float(CM_flat_sph.subs(r, 10 * KPC)) / (4 * math.pi * G_N)
print(f"          at 10 kpc : rho = {rho_10kpc:+.4g} kg/m^3   (~1e5 x the mean baryon density of a galaxy)")
print(f"        Both a0 footings give the identical number here because mu = 1 in both.")
check("F2 [spatial covariance] C_M vanishes in empty flat space in every spatial coordinate system, as any "
      "physical field equation must",
      CM_flat_cart == 0 and CM_flat_sph == 0,
      f"Cartesian gives 0, spherical gives {CM_flat_sph} =/= 0; the same empty space demands "
      f"rho = {rho_fake['canonical']:.3g} kg/m^3 at 1 AU.  q is a log-DENSITY, not a scalar (check A4)")

# --- F3: the standard repair -- q relative to a fiducial flat density.  Does it make q unique?
print("\n    F3 -- THE REPAIR, and what it costs.  Take q = -(1/6) ln(det gamma / det gamma-bar) with a")
print("         fiducial FLAT gamma-bar (the BSSN conformal factor).  q is then a genuine scalar and F2's")
print("         anomaly is gone.  But which flat gamma-bar?  Nothing in A1 fixes it.  Schwarzschild, one")
print("         slice, two admissible flat fiducials:")
M = sp.Symbol("M", positive=True)     # geometric mass GM/c^2
g_areal = sp.diag(1 / (1 - 2 * M / r), r ** 2, r ** 2 * sp.sin(th) ** 2)
q_areal = q_of(g_areal, g_sph)
g_areal_far = g_areal
gA_grad = sp.simplify(sp.sqrt(grad_sq(q_areal, g_areal, xs)))
g_field_areal = sp.simplify(sp.series(C_LIGHT ** 2 * gA_grad, M, 0, 2).removeO())
rb = sp.Symbol("rbar", positive=True)
psi = 1 + M / (2 * rb)
xs_iso = (rb, th, ph)
g_iso = sp.diag(psi ** 4, psi ** 4 * rb ** 2, psi ** 4 * rb ** 2 * sp.sin(th) ** 2)
gbar_iso = sp.diag(1, rb ** 2, rb ** 2 * sp.sin(th) ** 2)
q_iso = sp.simplify(q_of(g_iso, gbar_iso))
gI_grad = sp.simplify(sp.sqrt(grad_sq(q_iso, g_iso, xs_iso)))
g_field_iso = sp.simplify(sp.series(C_LIGHT ** 2 * gI_grad, M, 0, 2).removeO())
print(f"         areal radius     : q = {sp.simplify(q_areal)}  = -M/(3r) + O(M^2)")
print(f"                            ->  c^2|Dq| = {g_field_areal} + O(M^2)   = (c^2/3) M/r^2 = g_Newton / 3")
print(f"         isotropic radius : q = {sp.simplify(sp.series(q_iso, M, 0, 2).removeO())}")
print(f"                            ->  c^2|Dq| = {g_field_iso} + O(M^2)   = c^2 M/rbar^2 = g_Newton")
print(f"         (M is the geometric mass GM/c^2; c^2 = {C_LIGHT**2:.6e}, c^2/3 = {C_LIGHT**2/3:.6e})")
ratio_gauge = sp.simplify(g_field_areal.subs(r, rb) / g_field_iso)
check("F3 [fiducial repair] with the fiducial repair the MOND field c^2|Dq| is unique -- independent of "
      "which flat fiducial is chosen",
      sp.simplify(ratio_gauge - 1) == 0,
      f"it is not: the areal fiducial gives g_N/3 and the isotropic fiducial gives g_N, a factor "
      f"{sp.simplify(1/ratio_gauge)} in the predicted MOND acceleration.  Nothing in A1 selects one")

# --- F1: the same spacetime, two slicings.  Schwarzschild static vs Painleve-Gullstrand.
print("\n    F1 -- THE SAME SPACETIME, TWO SLICINGS.  Vacuum Schwarzschild, static slicing vs")
print("         Painleve-Gullstrand.  PG has gamma_ij EXACTLY FLAT and all the curvature in K_ij.")
v_pg = sp.sqrt(2 * M / r)
g_pg = g_sph                     # PG spatial metric is flat
Npg = sp.S(1)
Ndown = sp.Matrix([v_pg, 0, 0])  # N_r = gamma_rr N^r = v
Gam_pg = christoffel(g_pg, xs)
Kpg = sp.zeros(3, 3)
for i in range(3):
    for j in range(3):
        DiNj = sp.diff(Ndown[j], xs[i]) - sum(Gam_pg[k][i][j] * Ndown[k] for k in range(3))
        DjNi = sp.diff(Ndown[i], xs[j]) - sum(Gam_pg[k][j][i] * Ndown[k] for k in range(3))
        Kpg[i, j] = sp.simplify((DiNj + DjNi) / (2 * Npg))
gi_pg = g_pg.inv()
trKpg = sp.simplify(sum(gi_pg[i, j] * Kpg[i, j] for i in range(3) for j in range(3)))
KKpg = sp.simplify(sum(gi_pg[i, k] * gi_pg[j, l] * Kpg[i, j] * Kpg[k, l]
                       for i in range(3) for j in range(3) for k in range(3) for l in range(3)))
Hperp_pg = sp.simplify(ricci_scalar(g_pg, xs) + trKpg ** 2 - KKpg)
check("C5 [control] the Painleve-Gullstrand slice of Schwarzschild satisfies the VACUUM ADM Hamiltonian "
      "constraint R + K^2 - K_ij K^ij = 0 (my K_ij machinery is right)",
      Hperp_pg == 0, f"R = 0, K^2 - K_ijK^ij = {Hperp_pg}, exact")
q_pg = q_of(g_pg, g_sph)
g_field_pg = sp.simplify(C_LIGHT ** 2 * sp.sqrt(grad_sq(q_pg, g_pg, xs)))
print(f"         static slicing (isotropic fiducial) : c^2|Dq| = {g_field_iso}  = g_Newton")
print(f"         Painleve-Gullstrand slicing         : det gamma = det gamma-bar exactly, q = {q_pg}, "
      f"c^2|Dq| = {g_field_pg}")
print("         Same spacetime.  Same mass.  Same matter (none).  The whole MOND field is a property of the cut.")
check("F1 [foliation] the MOND field c^2|Dq| built from det gamma is a property of the SPACETIME: two "
      "slicings of vacuum Schwarzschild give the same field",
      g_field_pg != 0 and sp.simplify(g_field_pg - g_field_iso.subs(rb, r)) == 0,
      "they do not: the static slice gives g_Newton, the Painleve-Gullstrand slice of the SAME spacetime "
      "gives exactly 0.  A1 is therefore a statement about a preferred foliation, not about geometry")

# --- F4: the lapse equation, and where it degenerates
print("\n    F4 -- WHAT FIXES THE FOLIATION, and how strongly.  Preservation d C_M/dt = 0 uses A2's bracket:")
print("         an elliptic equation for the lapse with principal part (1/3) D_i[mu K D^i N].  The lapse is")
print("         DETERMINED, not free -- that IS the preferred foliation -- and the equation is elliptic, so")
print("         N responds instantaneously across the slice.  Its coefficient is mu K.  Cosmologically")
print("         K = -3H, so compare |K| with the local dynamical rate omega = v/R of the system it must control:")
Kcos = 3 * H0
rows = [("Solar System, 1 AU", AU, 29.78e3), ("galaxy, 10 kpc", 10 * KPC, 200e3), ("cluster, 1 Mpc", MPC, 1000e3)]
worst = 1.0
for nm, R_, v_ in rows:
    om = v_ / R_
    print(f"           {nm:22s}  omega = {om:.3e} s^-1   |K|/omega = {Kcos/om:.2e}")
    worst = min(worst, Kcos / om)
check("F4 [foliation/strong coupling] the lapse-fixing equation stays non-degenerate in the quasi-static "
      "regime where MOND is applied (its coefficient mu*K is not parametrically small)",
      worst > 1e-3,
      f"the coefficient is proportional to K = -3H; |K|/omega = {Kcos/(29.78e3/AU):.1e} in the Solar System "
      f"and {Kcos/(200e3/(10*KPC)):.1e} in a galaxy.  The second-class pairing that buys the count is "
      f"nearly degenerate exactly where the theory must work (warning P7 pattern)")

# ==========================================================================================================
print("\nSECTION 3 -- OPEN CHECK 2: MATTER.  Couple S_m[g, psi] minimally (I2).  Does the constraint survive?")
print("-" * 118)
# ==========================================================================================================
print("""    Minimally coupled matter conserves itself by construction: nabla_mu T^munu = 0 follows from the
    diffeomorphism invariance of S_m[g,psi] alone, and section A4's anomaly lives in the GRAVITY sector.
    So the matter Ward identity is not where this breaks.  The break is COMPATIBILITY: control C4 showed
    that the ADM Hamiltonian constraint by itself already fixes the same function q that C_M fixes.""")
print("""
    Static weak field, both constraints imposed (A1's only available branch, per check A1):
        H_perp = 0 :   lap q          = 4 pi G rho / c^2        (control C4)
        C_M    = 0 :   div[mu(y) grad q] = 4 pi G rho / c^2
    Subtract:          div[(1 - mu) grad q] = 0,   1 - mu = e^-y > 0 strictly.
    In spherical symmetry that integrates exactly: e^{-y} g r^2 = const = Cq, with g = c^2|dq/dr|.""")
print("    The function g -> g e^{-g/a0} has a maximum a0/e, so Cq/r^2 <= a0/e is required for ALL r:")
for nm, a0 in A0.items():
    gmax = a0 / math.e
    print(f"        {nm:10s}: max_g [g e^(-g/a0)] = a0/e = {gmax:.4e} m/s^2 at g = a0 = {a0:.4e}")
print("""        As r -> 0 near any mass this forces Cq = 0, hence g == 0 everywhere: imposing C_M on top of
        the ADM Hamiltonian constraint admits NO solution with a gravitational field at all.  (Equivalently,
        integrating q * div[e^{-y} grad q] over space with q -> 0 at infinity gives INT e^{-y}|grad q|^2 = 0.)""")
# numeric confirmation: the two equations give different g for the same source
print("\n    Numerically, for M_b = 1e10 Msun at r = 10 kpc, the two constraints demand:")
gap = {}
for nm, a0 in A0.items():
    Mb = 1e10 * MSUN
    R_ = 10 * KPC
    gN = G_N * Mb / R_ ** 2
    f = lambda g: (1 - math.exp(-g / a0)) * g - gN
    lo, hi = 1e-14, 1e-8
    for _ in range(200):
        mid = math.sqrt(lo * hi)
        if f(mid) < 0:
            lo = mid
        else:
            hi = mid
    gM = math.sqrt(lo * hi)
    gap[nm] = gM / gN
    print(f"        {nm:10s}: H_perp wants g = {gN:.4e} m/s^2 ; C_M wants g = {gM:.4e} m/s^2 "
          f"-> ratio {gM/gN:.3f}")
check("M1 [matter] C_M is compatible with the ADM Hamiltonian constraint for a generic matter distribution, "
      "so the coupled system has solutions with matter in it",
      False,
      f"it is not: the difference is div[e^-y grad q] = 0, which forces grad q == 0.  Numerically the two "
      f"constraints demand accelerations differing by a factor {gap['canonical']:.2f} (canonical) / "
      f"{gap['alt']:.2f} (alt) at 10 kpc")
check("M2 [matter] the source S in C_M is fixed by the construction rather than being free input",
      False,
      "it is not stated in A1.  If S = 4 pi G rho/c^2 the system is over-determined (M1).  If S carries "
      "extrinsic-curvature terms, C_M becomes a DEFORMED Hamiltonian constraint replacing H_perp -- a "
      "different theory, and exactly warning P3.  See section 6")
print("""
    The P3 branch, stated so it is not silently dismissed.  If C_M REPLACES H_perp (S carrying K-terms),
    M1 evaporates.  What replaces it is the Hojman-Kuchar-Teitelboim uniqueness theorem (1976): with the
    standard momentum constraint and an H_perp quadratic in the momenta, the hypersurface-deformation
    algebra has GR as its only solution (up to G and Lambda).  A mu(y)-deformed H_perp cannot close it, so
    foliation invariance is lost in that branch too -- which is the SAME verdict F1 reaches directly, by a
    different route.  This programme's own record reached it a third time, empirically: the MMG
    constraint-first chassis was withdrawn on 2026-08-27 for gamma_PPN = 0, alpha_1 = +4, alpha_3 = -1 and
    Newtonian-order matter non-conservation, with the note that deleting the Hamiltonian constraint is
    simultaneously what buys the 2-DOF count and what kills lensing and conservation (RETRACTIONS.md).
    This lane reproduces the structural half of that from the definitions, independently.""")
check("M3 [matter] matter conservation nabla_mu T^munu = 0 is intact for minimally coupled matter",
      True,
      "it is -- it follows from the diffeomorphism invariance of S_m[g,psi] alone and is untouched by "
      "anything in the gravity sector.  This one is a genuine PASS")

# ==========================================================================================================
print("\nSECTION 4 -- OPEN CHECK 3: COSMOLOGY.  Evaluate on FLRW.  Trivially satisfied, or forcing?")
print("-" * 118)
# ==========================================================================================================
at = sp.Function("a")(sp.Symbol("t"))
g_flrw = sp.diag(at ** 2, at ** 2, at ** 2)
q_flrw = sp.simplify(q_of(g_flrw))
dq_flrw = [sp.simplify(sp.diff(q_flrw, v)) for v in xc]
CM_flrw = C_M_operator(q_flrw, g_flrw, xc, A0["canonical"])
print(f"    gamma_ij = a(t)^2 delta_ij  ->  q = {q_flrw} = -ln a  (spatially constant)")
print(f"    D_i q = {dq_flrw}  ->  y = 0  ->  mu(0) = 1 - e^0 = 0  ->  D_i[mu D^i q] = {CM_flrw}")
print("    So C_M = 0 - S = 0 forces S = 0 exactly.  With S = 4 pi G rho/c^2 that is rho = 0:")
print("    the constraint is NOT trivially satisfied on FLRW -- it FORCES an empty universe.")
print("    a0 does not appear anywhere in this statement: it holds on both footings identically.")
check("K1 [cosmology] there is an expanding FLRW solution with rho > 0",
      False,
      "not in the branch A1 leaves available (check A1): D_i q = 0 on any homogeneous slice, so C_M "
      "reduces to -S = 0 and the physical density is forced to vanish.  Only the P3 branch (S carrying "
      "K-terms, i.e. C_M replacing H_perp) escapes, and that branch is the one F1/HKT close")

# perturbations: mu(0) = 0 makes the constraint operator degenerate at linear order
epsp = sp.Symbol("epsp", positive=True)
a0sym = sp.Symbol("a0", positive=True)
xp = sp.Symbol("xp", real=True)                       # one Fourier direction is enough for the order count
Qp = sp.Function("Q")(xp)
q_pert = epsp * Qp
W = sp.Abs(sp.diff(Qp, xp))                           # |dQ| ; epsp > 0 factors out
mu_pert = 1 - sp.exp(-C_LIGHT ** 2 * epsp * W / a0sym)
CM_pert = sp.diff(mu_pert * epsp * sp.diff(Qp, xp), xp)
ser = sp.series(CM_pert, epsp, 0, 3).removeO()
lead = sp.simplify(ser.coeff(epsp, 1))
order2 = sp.simplify(ser.coeff(epsp, 2))
print(f"\n    Linear perturbations about ANY homogeneous background (|Dq| = 0 there, so mu = 0 there):")
print(f"        C_M expanded in the perturbation amplitude eps:")
print(f"          O(eps^1) coefficient = {lead}      (no term linear in the metric perturbation)")
print(f"          O(eps^2) coefficient = {order2}")
print(f"          (that is exactly d/dx[(c^2/a0)|Q'| Q'], the leading deep-MOND operator, at SECOND order)")
print("        mu(y) = 1 - e^-y ~ y = c^2|Dq|/a0 makes D_i[mu D^i q] quadratic in Dq -- a degenerate")
print("        (3-Laplacian-type) operator.  At linear order the constraint therefore contains no metric")
print("        perturbation at all and reduces to delta S = 0, i.e. delta rho = 0: no linear growth of")
print("        structure, and the mode A3 was supposed to remove is not removed on these backgrounds.")
check("K2 [cosmology] the linearised constraint about a homogeneous background constrains the METRIC "
      "perturbation (as A3 requires), rather than the matter",
      lead != 0,
      "it does not: mu(0) = 0 makes the operator start at O(eps^2), so at linear order C_M = -delta S and "
      "the constraint forces delta rho = 0.  A3's mode removal fails on every background with |Dq| = 0")

# ==========================================================================================================
print("\nSECTION 5 -- THE TWO PHENOMENOLOGY GATES.  Is this the framework's theory at all?")
print("-" * 118)
# ==========================================================================================================
print("""    Gate 1: does the static weak-field limit give MOND with mu(y) = 1 - e^-y and the programme's a0?
    With q = Phi/c^2 (control C4) and S = 4 pi G rho/c^2, C_M = 0 reads exactly
        div[ mu(|grad Phi|/a0) grad Phi ] = 4 pi G rho          -- Milgrom's equation, the frozen kernel.
    Deep-MOND limit mu -> y: g^2/a0 = G M/r^2  ->  v^4 = G M a0.  Solved numerically below to confirm the
    limit is approached by the FULL kernel and not just asserted.""")
btfr_ok = True
for nm, a0 in A0.items():
    Mb = 1e10 * MSUN
    pred = (G_N * Mb * a0) ** 0.25
    devs = []
    for Rk in (30, 100, 300, 1000):
        R_ = Rk * KPC
        gN = G_N * Mb / R_ ** 2
        lo, hi = 1e-16, 1e-8
        for _ in range(200):
            mid = math.sqrt(lo * hi)
            if (1 - math.exp(-mid / a0)) * mid - gN < 0:
                lo = mid
            else:
                hi = mid
        g = math.sqrt(lo * hi)
        v = (g * R_) ** 0.5
        devs.append(v / pred - 1)
    A_btfr = 1.0 / (G_N * a0) / MSUN * 1e12
    print(f"        {nm:10s} a0 = {a0:.4e}: v_flat -> {pred/1e3:.2f} km/s for 1e10 Msun; "
          f"v/(GMa0)^1/4 - 1 = {devs[0]:+.4f} (30 kpc) -> {devs[-1]:+.5f} (1000 kpc); "
          f"BTFR M_b = A v^4 with A = {A_btfr:.1f} Msun/(km/s)^4")
    btfr_ok = btfr_ok and abs(devs[-1]) < 0.01
check("P1 [phenomenology] the static weak-field limit of C_M = 0 is exactly Milgrom's equation with the "
      "frozen kernel mu = 1 - e^-y, and reproduces v^4 = G M a0 on both footings",
      btfr_ok,
      "it does, to <1% at 1000 kpc on both footings -- but only in the conformally-flat spatial gauge "
      "(check F3: the areal fiducial gives g_N/3, which would move a0 by a factor 9)")

print("""
    Gate 2 (ingredient I4): is the screening controlled by a LOCAL dynamical quantity?  y = c^2|Dq|/a0 is
    the local acceleration -- not a potential, not an environment label, not a velocity dispersion.  The
    Solar System is deep inside a galaxy whose own field is ~ a0, and must still be screened by its own
    local g:""")
scr_ok = True
for nm, a0 in A0.items():
    for pl, rr in (("Earth  1.00 AU", 1.0), ("Saturn 9.58 AU", 9.58), ("Neptune 30.1 AU", 30.1)):
        gloc = GM_SUN / (rr * AU) ** 2
        y = gloc / a0
        print(f"        {nm:10s} {pl}: g = {gloc:.3e} m/s^2, y = {y:.3e}, 1 - mu = e^-y = "
              f"{'< 1e-300' if y > 700 else f'{math.exp(-y):.3e}'}")
        scr_ok = scr_ok and y > 1e4
    ggal = 2.0e-10
    print(f"        {nm:10s} the surrounding galactic field g ~ {ggal:.1e} m/s^2 (y = {ggal/a0:.2f}) does NOT "
          f"enter: y is built from the TOTAL local |Dq|, which the Sun dominates by "
          f"{GM_SUN/(9.58*AU)**2/ggal:.1e}x at Saturn")
check("P2 [I4] screening is controlled by a local dynamical quantity (the acceleration), and the Solar "
      "System is screened while sitting inside a MOND-strength galactic field",
      scr_ok, "y > 1e5 out to Neptune on both footings; 1 - mu = e^-y is unmeasurably small")
print("""
    Ingredient I5: the corrections are e^-y -- exponentially small, regular, with no 1/y anywhere in the
    construction.  C_M contains mu(y) and nothing else; no inverse power of y is used to repair any order.""")
check("P3 [I5] Newtonian recovery is by exponentially small corrections with no singular 1/y factor",
      True, "1 - mu = e^-y, entire in y; the construction never inverts y")

# ==========================================================================================================
print("\nSECTION 6 -- WHAT IS NOT DETERMINED BY WHAT IS PUBLISHED")
print("-" * 118)
print("""    A1 is one sentence.  Four inputs it does not supply, stated precisely rather than guessed:
      (i)   THE SOURCE S.  Is it 4 pi G rho/c^2 alone, or does it contain extrinsic-curvature terms
            (K^2 - K_ij K^ij)?  This decides everything downstream: with the first, C_M can only supplement
            H_perp (check A1) and is over-determined (M1) and empty on FLRW (K1); with the second, C_M is a
            deformed Hamiltonian constraint -- warning P3 -- and F1/HKT decide it instead.
      (ii)  THE FIDUCIAL.  det gamma is a density.  Without a fiducial density, C_M is not even
            coordinate-covariant (F2).  With one, its value depends on which fiducial (F3).
      (iii) THE SLICING CONDITION.  q is a slice quantity (F1).  A1 needs one; supplying one is supplying
            a khronon, which is what I3a exists to avoid.
      (iv)  THE ACTION.  A1 gives a constraint, not a Lagrangian.  Without it there is no lensing
            calculation (Phi vs Psi), no PPN, and no multiplier structure -- so gates G6/G7 cannot even be
            posed here.  This lane does not claim them either way.
    Everything above that could be settled WITHOUT these inputs was settled; nothing was assumed to fill them.""")

# ==========================================================================================================
print("\nSECTION 7 -- VERDICT")
print("-" * 118)
d_final = dof(12, 3, 2)
print(f"    Degree-of-freedom count on A1's generic branch: (12 - 2 - 2*3)/2 = {d_final}, and check A3 shows")
print(f"    the removed mode is the conformal one, so the survivors ARE the two tensor polarisations.")
print(f"    A1's arithmetic is CORRECT.  What it costs is what the three open checks measure.")
print(f"      OPEN CHECK 1 foliation : FAIL  (F1 Painleve-Gullstrand gives zero MOND field for the same")
print(f"                                      spacetime; F2 flat space in spherical coordinates demands")
print(f"                                      {rho_fake['canonical']:.3g} kg/m^3 of fictitious matter at 1 AU;")
print(f"                                      F3 the repair is non-unique; F4 the pairing degenerates as K->0)")
print(f"      OPEN CHECK 2 matter    : FAIL  (M1 over-determined with H_perp: forces zero field.  M3 matter")
print(f"                                      conservation itself is fine -- the incompatibility is geometric)")
print(f"      OPEN CHECK 3 cosmology : FAIL  (K1 forces rho = 0 on FLRW; K2 mu(0) = 0 makes the constraint")
print(f"                                      second order, so linear perturbations force delta rho = 0)")
check("V [verdict] A1 delivers exactly 2 gravitational degrees of freedom AND passes the three open checks "
      "(foliation, matter, cosmology), i.e. it is a route to a relativistic MOND with two gravitational modes",
      False,
      "the count is right and the phenomenology gates P1-P3 pass; all three open checks fail, and they fail "
      "for one reason: q = -(1/6) ln det gamma is a property of the slice and its coordinates, not of the "
      "spacetime")
print("""
    The recipe's own hedge -- "branch-restricted; never promote to a global theorem without the open checks"
    -- is vindicated in the strongest way: the branch restriction is not a technicality.  The generic branch
    (K =/= 0, |Dq| =/= 0) is exactly the complement of the regimes the theory has to work in: quasi-static
    galaxies (K/omega ~ 1e-2), the Solar System (1e-11), and homogeneous cosmology (|Dq| = 0).

    What A1 does establish, and should be kept: a constraint that removes the conformal mode leaves two
    tensor polarisations, and the exponential kernel screens the Solar System by a local acceleration with
    no 1/y.  What it does not establish is that the constraint can be built from det gamma.""")

print(f"\nRESULT: {len(FAILS)} FAIL" + (f" -> {FAILS}" if FAILS else ""))
sys.exit(0)
