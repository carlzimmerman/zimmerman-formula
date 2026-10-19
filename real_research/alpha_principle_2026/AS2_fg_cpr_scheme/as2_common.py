"""Lane AS2 shared machinery (see AS2_PREREGISTRATION.md and its Amendment 1).

Reuses AS1 by import: the lane-B downstream (as1_common.downstream_P) and, for f_g, AS1's flat-space bilinear action
(EH + photon kinetic blocks with the graviton gauge fixing switched off, and the F-bar vertices sqrt(g) g g F F, which are gauge independent).
New here: CPR's f(R) York Hessians in the gauge rho = 0, alpha = 0, beta -> infinity with ghosts, third ghost and Jacobians (CPR 0805.2909 sec. VII,
eqs. grop / xiquadratic / scalarpart / ghop / faerge), the trace-priming of CPR eq. (8) with Sigma = 0 (h and TT unprimed), heat-kernel
coefficients on S^4 up to b_4 derived from the S^4 spectra, the type-I matter traces, the R^0..R^2 projection with the d_t f', d_t f'' terms,
and the flat-space R^2 + CPR-gauge f_g.
Units: k = 1 throughout (P_k = 1 on the support z < 1 of the Litim regulator, d_t P_k = d_t R_k = 2, R_k(z) = 1 - z there).
"""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import numpy as np
import sympy as sp

HERE = Path(__file__).resolve().parent
AS1 = HERE.parent / "AS1_fg_r2_truncation"
if str(AS1) not in sys.path:
    sys.path.insert(0, str(AS1))
import as1_common as C1          # noqa: E402  lane-B downstream by import (via AS1)
import as1_g1_fg_flat as FG1     # noqa: E402  AS1 flat-space graviton-photon action

R, z, t = sp.symbols("R z t", real=True)
F0, F1, F2, dF0, dF1, dF2 = sp.symbols("F0 F1 F2 dF0 dF1 dF2", real=True)   # f, f', f'' at the background and their d_t at fixed R
bg = sp.Symbol("beta_g", positive=True)                                       # CPR gauge parameter beta (limit -> infinity)
g0, g1, g2, gd0, gd1, gd2 = sp.symbols("g0 g1 g2 gdot0 gdot1 gdot2", real=True)  # CPR couplings g_i (k = 1) and their dimensionful d_t
NS, ND, NV = sp.symbols("N_S N_D N_V", real=True)
P = sp.Integer(1)
DP = sp.Integer(2)
D = sp.Symbol("D", real=True)    # placeholder for the Laplacian eigenvalue in Hessians

# ---------------------------------------------------------------- heat kernel on S^4 from the spectra (Euler-Maclaurin)
def em_coeffs(Dl, mu, l0, extra=None):
    """b_{2n}/R^n, n = 0,1,2, of Tr exp(-s Delta) = (4 pi)^-2 V sum_n b_{2n} s^n on S^4 of radius 1 (R = 12), for the spectrum
    eigenvalue mu(l) (units 1/r^2), multiplicity Dl(l), l >= l0.  Euler-Maclaurin: sum_{m>=0} F(l0+m) = int_0^inf F + F(l0)/2
    - sum_k B_2k/(2k)! F^(2k-1)(l0); with polynomial Dl only k <= 3 can reach t^0.  extra: list of (mult, mu) single modes to add."""
    l, x = sp.symbols("l x", real=True)
    F = Dl(l) * sp.exp(-t * mu(l))
    # integral: complete the square mu(l) = (l + 3/2)^2 - c, so int_{l0}^inf = exp(t c) [int_0^inf - int_0^{x0}] in x = l + 3/2
    poly = sp.Poly(sp.expand(Dl(x - sp.Rational(3, 2))), x)
    x0 = l0 + sp.Rational(3, 2)
    I_inf = 0
    for (n,), a in poly.terms():
        I_inf += a * sp.gamma(sp.Rational(n + 1, 2)) / (2 * t**sp.Rational(n + 1, 2))
    I_low = sp.integrate(sp.series(poly.as_expr() * sp.exp(-t * x**2), t, 0, 3).removeO(), (x, 0, x0))
    shift = sp.exp(-t * (mu(l).subs(l, x - sp.Rational(3, 2)) - x**2).subs(x, 0))   # exp(t c)
    K = sp.series(shift * (I_inf - I_low), t, 0, 2).removeO()
    K += sp.series(F.subs(l, l0) / 2, t, 0, 2).removeO()
    for k in range(1, 5):
        K -= sp.bernoulli(2 * k) / sp.factorial(2 * k) * sp.series(sp.diff(F, l, 2 * k - 1).subs(l, l0), t, 0, 2).removeO()
    if extra:
        for mult, m_ in extra:
            K += sp.series(mult * sp.exp(-t * m_), t, 0, 2).removeO()
    K = sp.expand(K)
    out = []
    for n in range(3):
        a_n = K.coeff(t, n - 2)
        out.append(sp.nsimplify(6 * a_n / sp.Integer(12)**n))
    return tuple(out)


def spectra_heat_kernels():
    """S, VT, TT from CPR table taba2 (d = 4); 1-forms V = VT + gradients of non-constant scalars at mu_l(0) - R/4 (R/4 = 3 at r = 1)."""
    S = em_coeffs(lambda l: (2 * l + 3) * (l + 1) * (l + 2) / 6, lambda l: l * (l + 3), 0)
    VT = em_coeffs(lambda l: l * (l + 3) * (2 * l + 3) / 2, lambda l: l * (l + 3) - 1, 1)
    TT = em_coeffs(lambda l: sp.Rational(5, 6) * (l + 4) * (l - 1) * (2 * l + 3), lambda l: l * (l + 3) - 2, 2)
    # 1-forms: transverse part + longitudinal part (scalars l >= 1 with eigenvalue l(l+3) - 3)
    L = em_coeffs(lambda l: (2 * l + 3) * (l + 1) * (l + 2) / 6, lambda l: l * (l + 3) - 3, 1)
    V = tuple(sp.nsimplify(a + b) for a, b in zip(VT, L))
    return {"S": S, "VT": VT, "TT": TT, "V": V}


HK_TABLE_CPR = {"S": (1, sp.Rational(1, 6), sp.Rational(29, 2160)), "V": (4, sp.Rational(2, 3), sp.Rational(43, 1080)),
                "VT": (3, sp.Rational(1, 4), -sp.Rational(7, 1440)), "TT": (5, -sp.Rational(5, 6), -sp.Rational(1, 432))}


def gamma_matrices():
    s1 = sp.Matrix([[0, 1], [1, 0]]); s2 = sp.Matrix([[0, -sp.I], [sp.I, 0]]); s3 = sp.Matrix([[1, 0], [0, -1]]); i2 = sp.eye(2)
    def kron(A, B):
        return sp.Matrix(sp.BlockMatrix([[A[i, j] * B for j in range(2)] for i in range(2)]))
    # Euclidean: {gamma_a, gamma_b} = 2 delta_ab
    return [kron(s1, s1), kron(s1, s2), kron(s1, s3), kron(s2, i2)]


def vassilevich_bare(bundle):
    """(a0, a2/R, a4/R^2) of the bare Laplacian -nabla^2 (E = 0) on S^4 from Vassilevich sec. 4.1 (a0nobou, a2nobou, a4nobou):
    a4 = (1/360) tr(5R^2 - 2 Ric^2 + 2 Riem^2 + 30 Omega_ij Omega_ij), box terms vanish on S^4.  Riem_abcd = (R/12)(d_ac d_bd - d_ad d_bc)."""
    Rs = sp.Symbol("Rs", positive=True)
    Riem = lambda a, b, c, d: Rs / 12 * (int(a == c) * int(b == d) - int(a == d) * int(b == c))
    Riem2 = sum(Riem(a, b, c, d)**2 for a in range(4) for b in range(4) for c in range(4) for d in range(4))
    Ric2 = 4 * (Rs / 4)**2
    if bundle == "S":
        dim, trO2 = 1, 0
    elif bundle == "V":   # (Omega_ij)^a_b = R^a_{b ij}
        dim = 4
        trO2 = sum(Riem(a, b, i, j) * Riem(b, a, i, j) for a in range(4) for b in range(4) for i in range(4) for j in range(4))
    elif bundle == "spinor":   # Omega_ij = (1/4) R_ijab gamma_a gamma_b
        dim = 4
        G = gamma_matrices()
        trO2 = 0
        for i in range(4):
            for j in range(4):
                Om = sp.zeros(4, 4)
                for a in range(4):
                    for b in range(4):
                        Om += sp.Rational(1, 4) * Riem(i, j, a, b) * G[a] * G[b]
                trO2 += (Om * Om).trace()
    a4 = sp.simplify((dim * (5 * Rs**2 - 2 * Ric2 + 2 * Riem2) + 30 * trO2) / 360)
    return (dim, sp.Rational(dim, 6), sp.nsimplify(sp.simplify(a4 / Rs**2)))


# ---------------------------------------------------------------- traces to O(R^2) with CPR's priming
def Q(n, W):
    if n == 0:
        return W.subs(z, 0)
    return sp.integrate(sp.expand(z**(n - 1) * W), (z, 0, 1)) / sp.gamma(n)


def trace_R2(field, W, HK, nexcl=0, order=2):
    """(16 pi^2 / V) Tr_field W(Delta; R) to O(R^order): b0 Q2(W) + b2 Q1(W) + b4 Q0(W) expanded in R, minus excluded modes
    (16 pi^2/V) sum_l D_l W(lambda_l) = (R^2/24) nexcl W(0; 0) + O(R^3)."""
    b0, b2, b4 = HK[field]
    W = sp.sympify(W)
    Wk = [sp.simplify(W.subs(R, 0))]
    if order >= 1:
        Wk.append(sp.simplify(sp.diff(W, R).subs(R, 0)))
    if order >= 2:
        Wk.append(sp.simplify(sp.diff(W, R, 2).subs(R, 0) / 2))
    c = [b0 * Q(2, Wk[0])]
    if order >= 1:
        c.append(b0 * Q(2, Wk[1]) + b2 * Q(1, Wk[0]))
    if order >= 2:
        c.append(b0 * Q(2, Wk[2]) + b2 * Q(1, Wk[1]) + b4 * Q(0, Wk[0]) - sp.Rational(nexcl, 24) * Wk[0].subs(z, 0))
    return sum(sp.simplify(ci) * R**i for i, ci in enumerate(c))


# ---------------------------------------------------------------- CPR f(R) Hessian in the gauge rho = 0, alpha = 0, G = beta D^2 (d = 4)
def cpr_blocks(mutate2=False):
    """TT, xi and (h, sigma) Hessians (CPR grop, xiquadratic, scalarpart with rho = 0, alpha = 0); D = -nabla^2 eigenvalue.
    (alpha + beta nabla^2) -> -beta D on transverse vectors and -beta (D - R/4) inside the scalar block (CPR's (nabla^2 + R/d))."""
    TT = -sp.Rational(1, 2) * (F1 * (D - R / 3) + F0)
    XI = (D - R / 4) * ((-bg * D) * (D - R / 4) + R / 2 * F1 - F0)
    f2hh = 0 if mutate2 else F2
    Hhh = sp.Rational(1, 8) * (sp.Rational(9, 2) * f2hh * (D - R / 3)**2 + sp.Rational(3, 2) * F1 * (D - R / 3) - R / 2 * F1 + F0)
    Hhs = sp.Rational(3, 16) * (3 * F2 * (D - R / 3) + F1) * D * (D - R / 3)
    Hss = sp.Rational(3, 8) * (sp.Rational(3, 2) * F2 * D * (D - R / 3) + F1 * D / 2 + R / 2 * F1 - F0
                               + sp.Rational(3, 2) * (D - R / 3) * (-bg * (D - R / 4))) * D * (D - R / 3)
    return TT, XI, sp.Matrix([[Hhh, Hhs], [Hhs, Hss]])


def dtR(Hm, with_eta):
    """d_t R_k for the block: d_P H(P) d_tP + sum_X dX d_X [H(P) - H(z)], X in (f, f', f''); the gauge parameter does not run."""
    HP = Hm.subs(D, P)
    out = DP * sp.diff(Hm, D).subs(D, P)
    if with_eta:
        for X, dX in ((F0, dF0), (F1, dF1), (F2, dF2)):
            out += dX * (sp.diff(Hm, X).subs(D, P) - sp.diff(Hm, X).subs(D, z))
    return HP, out


def limit_beta(expr):
    expr = sp.together(expr)
    num, den = sp.fraction(expr)
    pn = sp.Poly(sp.expand(num), bg); pd = sp.Poly(sp.expand(den), bg)
    if pn.degree() > pd.degree():
        raise RuntimeError("beta -> infinity limit diverges")
    if pn.degree() < pd.degree():
        return sp.Integer(0)
    return sp.simplify(pn.LC() / pd.LC())


def gravity_W(with_eta=True, mutate2=False):
    """Return list of (name, weight, field, nexcl, W) for metric fluctuations, ghosts, third ghost and Jacobians, beta -> infinity taken."""
    TT, XI, S = cpr_blocks(mutate2)
    parts = []
    HP, dR = dtR(sp.Matrix([[TT]]), with_eta)
    parts.append(("TT", sp.Rational(1, 2), "TT", 0, sp.simplify(dR[0, 0] / HP[0, 0]), "graviton"))
    HP, dR = dtR(sp.Matrix([[XI]]), with_eta)
    parts.append(("xi", sp.Rational(1, 2), "VT", 10, limit_beta(dR[0, 0] / HP[0, 0]), "graviton"))
    HP, dR = dtR(S, with_eta)
    M = HP.inv() * dR
    parts.append(("h (unprimed, CPR eq. 8)", sp.Rational(1, 2), "S", 0, limit_beta(M[0, 0]), "graviton"))
    parts.append(("sigma", sp.Rational(1, 2), "S", 6, limit_beta(M[1, 1]), "graviton"))
    L = lambda J: sp.simplify(DP * sp.diff(sp.log(J), D).subs(D, P))
    parts += [("ghost c^T", -1, "VT", 10, L(D * (D - R / 4)), "ghost"),
              ("ghost c", -1, "S", 6, L((D - R / 4) * (D - R / 3) * D), "ghost"),
              ("third ghost b^T", sp.Rational(1, 2), "VT", 10, L(D), "ghost"),
              ("third ghost b", sp.Rational(1, 2), "S", 6, L(D * (D - R / 4)), "ghost"),
              ("J_V", -sp.Rational(1, 2), "VT", 10, L(D - R / 4), "jacobian"),
              ("J_S", -sp.Rational(1, 2), "S", 6, L(D * (D - R / 3)), "jacobian"),
              ("J_c", 1, "S", 6, L(D), "jacobian"),
              ("J_b", -sp.Rational(1, 2), "S", 6, L(D), "jacobian")]
    return parts


def f_subs(order_f=2):
    """f(R) = g0 + g1 R + g2 R^2 (g2 = 0 for n = 1): background values of f, f', f'' and their d_t at fixed R."""
    G2 = g2 if order_f == 2 else 0
    GD2 = gd2 if order_f == 2 else 0
    return {F0: g0 + g1 * R + G2 * R**2, F1: g1 + 2 * G2 * R, F2: 2 * G2,
            dF0: gd0 + gd1 * R + GD2 * R**2, dF1: gd1 + 2 * GD2 * R, dF2: 2 * GD2}


def X_gravity(HK, with_eta=True, mutate1=False, mutate2=False, order_f=2, detail=False):
    parts = gravity_W(with_eta, mutate2)
    sub = f_subs(order_f)
    X = 0
    det = []
    for name, wgt, fld, nex, W, kind in parts:
        w = -wgt if (mutate1 and kind == "graviton") else wgt
        c = trace_R2(fld, sp.simplify(w * W.subs(sub)), HK, nex)
        X += c
        det.append((name, c))
    return (sp.expand(X), det) if detail else sp.expand(X)


def X_matter(HK):
    """Type-I matter (exception (a)): scalars (1/2)Tr_S[2/P]; Dirac -(1/2)Tr_spinor[2/(P + R/4)]; vectors (Feynman)
    (1/2)Tr_V[2/(P + R/4)] - Tr_S[2/P].  Unconstrained fields: no primes."""
    sc = trace_R2("S", sp.Integer(1), HK)
    di = trace_R2("spinor", -1 / (1 + R / 4), HK)
    ve = trace_R2("V", 1 / (1 + R / 4), HK) + trace_R2("S", sp.Integer(-2), HK)
    return sp.expand(NS * sc + ND * di + NV * ve), (sp.expand(sc), sp.expand(di), sp.expand(ve))


def george(order_f=2):
    """CPR eq. 'george' (Sigma = 0): the braces Y(R~), with (d_t f~' + 2 f~' - 2 R~ f~'') -> d_t f'|_R and (d_t f~'' - 2 R~ f~''') -> d_t f''|_R."""
    s = f_subs(order_f)
    f, fp, fpp = s[F0], s[F1], s[F2]
    Df1, Df2 = s[dF1], s[dF2]
    Rt = R
    Y = (-1008 * (511 * Rt**2 - 360 * Rt - 1080) / (Rt - 3)
         - 2016 * (607 * Rt**2 - 360 * Rt - 2160) / (Rt - 4)
         + 20 * ((311 * Rt**3 - 126 * Rt**2 - 22680 * Rt + 45360) * Df1 - 252 * (Rt**2 + 360 * Rt - 1080) * fp) / (3 * f - (Rt - 3) * fp)
         + (1008 * (29 * Rt**2 + 360 * Rt + 1080) * fp + 4 * (185 * Rt**3 + 3654 * Rt**2 + 22680 * Rt + 45360) * Df1
            - 2016 * (29 * Rt**3 + 273 * Rt**2 - 3240) * fpp - 9 * (181 * Rt**4 + 3248 * Rt**3 + 15288 * Rt**2 - 90720) * Df2)
         / (fpp * (Rt - 3)**2 + 2 * f + (3 - 2 * Rt) * fp))
    return Y


def taylor(expr, n=2):
    return [sp.simplify(sp.diff(expr, R, i).subs(R, 0) / sp.factorial(i)) for i in range(n + 1)]


# ---------------------------------------------------------------- projection and beta functions
def beta_system(X, order_f):
    """d g_i/dt (dimensionful, k = 1) = [R^i] X/(16 pi^2), solved together with the d_t f', d_t f'' terms; returns d_t g~_i = gdot_i - (4-2i) g~_i."""
    cs = taylor(X, order_f)
    unknowns = [gd0, gd1] + ([gd2] if order_f == 2 else [])
    eqs = [sp.Eq(unknowns[i], cs[i] / (16 * sp.pi**2)) for i in range(order_f + 1)]
    sol = sp.solve(eqs, unknowns, dict=True)[0]
    return [sp.simplify(sol[unknowns[i]] - (4 - 2 * i) * [g0, g1, g2][i]) for i in range(order_f + 1)]


def to_glb(gt):
    """CPR couplings -> (g, lambda, b): g = -1/(16 pi g1), lambda = -g0/(2 g1), b = g2."""
    g0v, g1v = gt[0], gt[1]
    out = [-1 / (16 * np.pi * g1v), -g0v / (2 * g1v)]
    if len(gt) > 2:
        out.append(gt[2])
    return out


def from_glb(v):
    g_, l_ = v[0], v[1]
    g1v = -1 / (16 * np.pi * g_)
    out = [-2 * l_ * g1v, g1v]
    if len(v) > 2:
        out.append(v[2])
    return out


def admissible(glb):
    g_, l_ = glb[0], glb[1]
    b_ = glb[2] if len(glb) > 2 else 0.0
    return g_ > 0 and (1 - 2 * l_) > 0 and (1 - 4 * l_ / 3 - 96 * np.pi * g_ * b_) > 0


def find_roots(betas, order_f, grid=True, extra_starts=()):
    from scipy.optimize import fsolve
    syms = [g0, g1, g2][:order_f + 1]
    f = sp.lambdify(syms, betas, "numpy")
    J = sp.lambdify(syms, sp.Matrix(betas).jacobian(syms), "numpy")
    starts = list(extra_starts)
    if grid:
        gs = np.geomspace(0.05, 40, 10); ls = np.linspace(-45, 0.45, 15)
        bs = [0.0] + [s * 10.0**e for e in range(-4, 3) for s in (1, -1)]
        for G_ in gs:
            for L_ in ls:
                if order_f == 2:
                    for B_ in bs:
                        starts.append(from_glb([G_, L_, B_]))
                else:
                    starts.append(from_glb([G_, L_]))
    roots = []
    for x0 in starts:
        try:
            with np.errstate(all="ignore"):
                sol, info, ier, _ = fsolve(lambda v: np.array(f(*v), dtype=float),
                                           np.array(x0, dtype=float), fprime=lambda v: np.array(J(*v), dtype=float),
                                           full_output=True, xtol=1e-14, maxfev=400)
        except Exception:
            continue
        if ier != 1 or not np.all(np.isfinite(sol)):
            continue
        res = np.max(np.abs(np.array(f(*sol), dtype=float)))
        if res > 1e-12 or abs(sol[1]) < 1e-12:
            continue
        if not any(np.allclose(sol, r, rtol=1e-6, atol=1e-12) for r in roots):
            roots.append(sol)
    return roots, f, J


def in_domain(glb):
    """Domain g in (0,50), lambda in (-50,0.5), b in (-1e3,1e3).  'Within 5 percent of a domain edge' is read per finite bound:
    g > 47.5, lambda < -47.5, lambda > 0.475, |b| > 950 (the bound g > 0 is the admissibility condition itself, not flagged)."""
    g_, l_ = glb[0], glb[1]
    ok = 0 < g_ < 50 and -50 < l_ < 0.5
    edge = g_ > 47.5 or l_ < -47.5 or l_ > 0.475
    if len(glb) > 2:
        ok = ok and -1e3 < glb[2] < 1e3
        edge = edge or abs(glb[2]) > 950
    return ok, edge


def crit_exponents(J, root):
    M = np.array(J(*root), dtype=float)
    return np.sort_complex(-np.linalg.eigvals(M))


# ---------------------------------------------------------------- flat-space f_g in CPR's gauge with the R^2 term
def fg_flat_cpr(mutate2=False, xi_sym=True):
    """f_g from the F-bar^2 coefficient of the graviton-photon trace (AS1 method), CPR gauge rho = 0, alpha = 0, |beta| -> infinity,
    regulator q^2 -> P_k in the kinetic matrix (q^4 -> P_k^2), eta terms d_t f' (P - q^2) and d_t f'' (graviton only).
    Returns (f_g as a function of F0, F1, F2, dF1, dF2, e, xi), info dict."""
    s = sp.Symbol("s", positive=True)
    B, V1, V2, hm, hp, am, ap = FG1.bilinear_action(s)
    # AS1 action in f(R) language: Z_N -> -F1, 2 lambda Z_N -> F0 (i.e. lambda -> -F0/(2 F1)); graviton gauge fixing off (a_gf = 0)
    B = B.subs(FG1.agf, 0).subs({FG1.lam: -F0 / (2 * F1)}).subs({FG1.g: -1 / (16 * sp.pi * F1)})
    Hm, _ = FG1.hmat("hm")
    Hp, _ = FG1.hmat("hp")
    tr = lambda H: sum(H[i, i] for i in range(4))
    # R^2 term (1/2) f'' (R^(1))^2, R^(1)(q) = -q_m q_n h_mn + q^2 h = s (tr h - h_33) for q = kappa e_4
    f2 = 0 if mutate2 else F2
    B += sp.Rational(1, 2) * f2 * s**2 * (tr(Hm) - Hm[3, 3]) * (tr(Hp) - Hp[3, 3])
    # CPR gauge fixing (1/2) chi (beta d^2) chi, chi_nu = d^mu h_mu nu - (1/4) d_nu h -> -(beta/2) s^2 |qhat.h - qhat tr h /4|^2
    chim = [Hm[3, m] - sp.Rational(1, 4) * (1 if m == 3 else 0) * tr(Hm) for m in range(4)]
    chip = [Hp[3, m] - sp.Rational(1, 4) * (1 if m == 3 else 0) * tr(Hp) for m in range(4)]
    B += -bg / 2 * s**2 * sum(chim[m] * chip[m] for m in range(4))
    Phim = hm + am
    Phip = hp + ap
    n = len(Phim)
    Mk = sp.Matrix(n, n, lambda i, j: sp.diff(B, Phim[i], Phip[j]))
    M1 = sp.Matrix(n, n, lambda i, j: sp.diff(V1, Phim[i], Phip[j]))
    M2 = sp.Matrix(n, n, lambda i, j: sp.diff(V2, Phim[i], Phip[j]))
    kap = FG1.kap
    MkP = Mk.subs(s, P)
    dR = sp.diff(Mk, s).subs(s, P) * DP
    # eta terms on the graviton block only: d_t f' d_{f'}[M(P) - M(s)] + d_t f'' d_{f''}[M(P) - M(s)]
    for X, dX in ((F1, dF1), (F2, dF2)):
        dR[:10, :10] += dX * (sp.diff(Mk[:10, :10], X).subs(s, P) - sp.diff(Mk[:10, :10], X))
    dR = dR.subs(s, kap**2)
    G = sp.zeros(n, n)
    G[:10, :10] = MkP[:10, :10].inv()
    G[10:, 10:] = MkP[10:, 10:].inv()
    T = -sp.Rational(1, 2) * (G * M2 * G * dR).trace() + sp.Rational(1, 2) * (G * M1 * G * M1 * G * dR).trace()
    T = sp.together(sp.expand(T))
    num, den = sp.fraction(T)
    pn = sp.Poly(sp.expand(num), bg); pd = sp.Poly(sp.expand(den), bg)
    info = {"deg_num": pn.degree(), "deg_den": pd.degree()}
    if pn.degree() > pd.degree():
        info["divergent"] = True
        return None, info
    info["divergent"] = False
    Tlim = (pn.coeff_monomial(bg**pd.degree()) if pn.degree() == pd.degree() else 0) / pd.LC()
    # beta -> -infinity: same leading-coefficient ratio when degrees are equal (sign of beta^deg cancels) -> identical; recorded
    info["minus_inf_equal"] = True
    Tlim = sp.expand(Tlim)
    C = sp.zeros(6, 6)
    for a_, A in enumerate(FG1.Fs):
        C[a_, a_] = Tlim.coeff(A, 2)
        for b_, Bv in enumerate(FG1.Fs):
            if a_ != b_:
                C[a_, b_] = Tlim.coeff(A, 1).coeff(Bv, 1) / 2
    dual = {0: (5, 1), 1: (4, -1), 2: (3, 1)}
    star = sp.zeros(6, 6)
    for i_, (j_, sg) in dual.items():
        star[i_, j_] = sg; star[j_, i_] = sg
    info["parity_ok"] = sp.simplify((C * star).trace()) == 0
    trC = sp.simplify(C.trace())
    cFF = sp.integrate(sp.expand(trC / 12 * kap**3 / (8 * sp.pi**2)), (kap, 0, 1))
    fg = sp.simplify(2 * FG1.e**2 * cFF)
    return fg, info


def classify2(P_, P_ref, labels=("AGREES", "CLOSER", "NO IMPROVEMENT")):
    """AS2 frozen classes: AGREES |Delta| <= 2%; CLOSER |Delta| > 2% and |P - t| < |P_ref - t| (P_ref None -> 44.12); else NO IMPROVEMENT."""
    agrees, closer, noimp = labels
    t_ = C1.ALPHA_INV0
    delta = (P_ - t_) / t_
    if abs(delta) <= 0.02:
        return agrees, delta
    ref_miss = abs(P_ref - t_) if P_ref is not None else C1.EH_MISS_QUOTED
    if abs(P_ - t_) < ref_miss:
        return closer, delta
    return noimp, delta
