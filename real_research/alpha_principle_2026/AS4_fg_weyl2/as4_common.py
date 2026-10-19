"""Lane AS4 shared machinery (AS4_PREREGISTRATION.md): Benedetti-Machado-Saueressig (BMS, arXiv:0902.4630) EH + C^2 + R^2 truncation
on a generic Einstein background, type-I SM matter, flat-space f_g with the C^2 term, by import of AS1/AS2 pieces.

Conventions: k = 1; on the support of the optimized cutoff P = 1, d_t P = 2, R_k(z) = 1 - z.  Couplings u0..u3 (dimensionful at k = 1 =
dimensionless g0..g3); their scale derivatives at fixed R are U0d..U3d (dimensionful), related to the dimensionless ones by
d_t g_i = U_id - d_i g_i with d = (4, 2, 0, 0).  BMS operator convention (eq. Hexp): Delta_sL = -D^2 - Q_s with Q0 = 0, Q1 = R/4 (on vectors),
Q2 = 2 Riem (on symmetric tensors), heat-kernel a2 = tr(R/6 + Q).  Projection basis {1, R, R^2, Riem^2} on Einstein spaces (Ric = R/4)."""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import itertools
import numpy as np
import sympy as sp

HERE = Path(__file__).resolve().parent
for d in (HERE.parent / "AS2_fg_cpr_scheme", HERE.parent / "AS1_fg_r2_truncation"):
    if str(d) not in sys.path:
        sys.path.insert(0, str(d))
import as2_common as A2     # noqa: E402  (AS2 machinery: Q, limit_beta, classify2, gamma_matrices, downstream via C1)
C1 = A2.C1
FG1 = A2.FG1

R, z = A2.R, A2.z
D = sp.Symbol("D", real=True)
bg = A2.bg
U0, U1, U2, U3 = sp.symbols("u0 u1 u2 u3", real=True)
U0d, U1d, U2d, U3d = sp.symbols("u0dot u1dot u2dot u3dot", real=True)
RW = sp.Symbol("Riem2", positive=True)      # Riem^2 = R_abcd R^abcd as an independent invariant on Einstein spaces
NS, ND, NV = A2.NS, A2.ND, A2.NV
P = sp.Integer(1)
DP = sp.Integer(2)
Q = A2.Q


# ---------------------------------------------------------------- explicit algebraic Einstein curvature with a Weyl part
def weyl_tensor(seed):
    """An explicit rational algebraic Weyl tensor (Riemann symmetries + first Bianchi + traceless) in an orthonormal Euclidean frame."""
    rng = np.random.default_rng(seed)
    T = np.array(rng.integers(-5, 6, size=(4, 4, 4, 4)), dtype=object)
    T = np.vectorize(sp.Integer)(T)
    K = np.empty((4, 4, 4, 4), dtype=object)
    for a, b, c, d in itertools.product(range(4), repeat=4):
        K[a, b, c, d] = T[a, b, c, d] - T[b, a, c, d] - T[a, b, d, c] + T[b, a, d, c]
    K2 = np.empty_like(K)
    for a, b, c, d in itertools.product(range(4), repeat=4):
        K2[a, b, c, d] = K[a, b, c, d] + K[c, d, a, b]
    K3 = np.empty_like(K)
    for a, b, c, d in itertools.product(range(4), repeat=4):     # remove the totally antisymmetric part (first Bianchi)
        K3[a, b, c, d] = K2[a, b, c, d] - sp.Rational(1, 3) * (K2[a, b, c, d] + K2[a, c, d, b] + K2[a, d, b, c])
    Ric = np.array([[sum(K3[a, b, a, d] for a in range(4)) for d in range(4)] for b in range(4)], dtype=object)
    Rs = sum(Ric[i, i] for i in range(4))
    dl = lambda i, j: 1 if i == j else 0
    W = np.empty_like(K)
    for a, b, c, d in itertools.product(range(4), repeat=4):
        W[a, b, c, d] = (K3[a, b, c, d]
                         - sp.Rational(1, 2) * (dl(a, c) * Ric[b, d] - dl(a, d) * Ric[b, c] - dl(b, c) * Ric[a, d] + dl(b, d) * Ric[a, c])
                         + Rs / 6 * (dl(a, c) * dl(b, d) - dl(a, d) * dl(b, c)))
    return W


def riemann_einstein(W, Rs):
    dl = lambda i, j: 1 if i == j else 0
    Rm = np.empty_like(W)
    for a, b, c, d in itertools.product(range(4), repeat=4):
        Rm[a, b, c, d] = W[a, b, c, d] + Rs / 12 * (dl(a, c) * dl(b, d) - dl(a, d) * dl(b, c))
    return Rm


def weyl_checks(W):
    ok_sym = all(W[a, b, c, d] == -W[b, a, c, d] == -W[a, b, d, c] == W[c, d, a, b] for a, b, c, d in itertools.product(range(4), repeat=4))
    ok_bianchi = all(W[a, b, c, d] + W[a, c, d, b] + W[a, d, b, c] == 0 for a, b, c, d in itertools.product(range(4), repeat=4))
    ok_trace = all(sum(W[a, b, a, d] for a in range(4)) == 0 for b in range(4) for d in range(4))
    W2 = sum(W[a, b, c, d]**2 for a, b, c, d in itertools.product(range(4), repeat=4))
    return ok_sym and ok_bianchi and ok_trace and W2 != 0, W2


# ---------------------------------------------------------------- Vassilevich a4 on bundles over an Einstein space -> (Riem^2, R^2) coefficients
def _a4_bundle(kind, Rm, Rs, E_kind=None):
    """(1/360) tr[60 R E + 180 E^2 + (5R^2 - 2Ric^2 + 2Riem^2) 1 + 30 Omega_ij Omega_ij] (box terms integrate to zero);
    E as in D = -(nabla^2 + E).  kind in {scalar, vector, sym2, spinor}; E_kind: None, 'BMS1' (E = R/4), 'BMS2' (E h = 2 Riem h)."""
    Riem2 = sum(Rm[a, b, c, d]**2 for a, b, c, d in itertools.product(range(4), repeat=4))
    Ric2 = 4 * (Rs / 4)**2
    if kind == "scalar":
        dim, trE, trE2, trO2 = 1, 0, 0, 0
    elif kind == "vector":
        dim = 4
        trO2 = sum(Rm[a, b, i, j] * Rm[b, a, i, j] for a, b, i, j in itertools.product(range(4), repeat=4))
        e = Rs / 4 if E_kind == "BMS1" else 0
        trE, trE2 = 4 * e, 4 * e**2
    elif kind == "spinor":
        dim = 4
        G = A2.gamma_matrices()
        trO2 = 0
        for i, j in itertools.product(range(4), repeat=2):
            Om = sp.zeros(4, 4)
            for a, b in itertools.product(range(4), repeat=2):
                Om += sp.Rational(1, 4) * Rm[i, j, a, b] * G[a] * G[b]
            trO2 += (Om * Om).trace()
        trE, trE2 = 0, 0
    elif kind == "sym2":
        basis = [(a, b) for a in range(4) for b in range(a, 4)]
        def mat(h):
            Mx = sp.zeros(4, 4)
            for (a, b), v in h.items():
                Mx[a, b] += v
                if a != b:
                    Mx[b, a] += v
            return Mx
        def coords(Mx):
            return [Mx[a, b] for (a, b) in basis]
        def as_matrix(op):
            cols = []
            for (a, b) in basis:
                cols.append(coords(op(mat({(a, b): 1}))))
            return sp.Matrix(cols).T
        def Eop(h):
            return sp.Matrix(4, 4, lambda m, n: 2 * sum(Rm[m, a, n, b] * h[a, b] for a in range(4) for b in range(4)))
        def Oop(i, j):
            return lambda h: sp.Matrix(4, 4, lambda m, n: sum(Rm[m, r, i, j] * h[r, n] + Rm[n, r, i, j] * h[m, r] for r in range(4)))
        dim = 10
        Em = as_matrix(Eop) if E_kind == "BMS2" else sp.zeros(10, 10)
        trE, trE2 = Em.trace(), (Em * Em).trace()
        trO2 = 0
        for i, j in itertools.product(range(4), repeat=2):
            Om = as_matrix(Oop(i, j))
            trO2 += (Om * Om).trace()
    a4 = (60 * Rs * trE + 180 * trE2 + dim * (5 * Rs**2 - 2 * Ric2 + 2 * Riem2) + 30 * trO2) / 360
    a2 = dim * Rs / 6 + trE
    return dim, sp.expand(a2), sp.expand(a4)


def heat_kernels_einstein(seed=7):
    """Return HK[field] = (b0, b2/R, b4_R2, b4_Riem2) for BMS's Lichnerowicz operators (0, 1, 2 unconstrained; 1T, 2T via h1T, h2T)
    and for the bare matter Laplacians (S, spinor, V), all on a generic Einstein space, plus the Weyl-tensor check flag."""
    W = weyl_tensor(seed)
    okW, W2 = weyl_checks(W)
    Rs = sp.Symbol("Rs")
    Rm = riemann_einstein(W, Rs)
    out = {}
    for name, kind, ek in (("0", "scalar", None), ("1", "vector", "BMS1"), ("2", "sym2", "BMS2"),
                           ("S", "scalar", None), ("spinor", "spinor", None), ("V", "vector", None)):
        dim, a2, a4 = _a4_bundle(kind, Rm, Rs, ek)
        # a4 = c_W |W|^2 + c_R2 Rs^2 ; Riem^2 = |W|^2 + Rs^2/6  ->  a4 = c_W Riem^2 + (c_R2 - c_W/6) Rs^2
        a4p = sp.Poly(a4, Rs)
        c0 = a4p.coeff_monomial(1)
        c2 = a4p.coeff_monomial(Rs**2)
        assert a4p.coeff_monomial(Rs) == 0
        cW = sp.nsimplify(c0 / W2)
        out[name] = (dim, sp.nsimplify(sp.expand(a2 / Rs)), sp.nsimplify(c2 - cW / 6), cW)
    # York relations on Einstein spaces without KV/CKV (BMS eqs. h1T, h2T): Tr_1T = Tr_1 - Tr_0[Delta_0L - R/2];
    # Tr_2T = Tr_2 - Tr_1 - Tr_0[Delta_0L - R/2].  A shift Delta -> Delta - c R: b2 -> b2 + c b0 R, b4 -> b4 + c R b2 + c^2 R^2 b0 / 2.
    def shift(hk, c):
        b0, b2, b4R, b4W = hk
        return (b0, b2 + c * b0, b4R + c * b2 + c**2 * b0 / 2, b4W)
    s0 = shift(out["0"], sp.Rational(1, 2))
    out["1T"] = tuple(sp.nsimplify(x - y) for x, y in zip(out["1"], s0))
    out["2T"] = tuple(sp.nsimplify(x - y - w) for x, y, w in zip(out["2"], out["1"], s0))
    return out, okW


HK_BMS_PRINTED = {   # BMS eq. Hexp table and eq. d4heat: (tr a0, tr a2 / R, R^2 coeff of tr a4, Riem^2 coeff of tr a4)
    "0": (1, sp.Rational(1, 6), sp.Rational(1, 80), sp.Rational(1, 180)),
    "1": (4, sp.Rational(5, 3), sp.Rational(41, 120), -sp.Rational(11, 180)),
    "2": (10, sp.Rational(2, 3), -sp.Rational(1, 24), sp.Rational(19, 18)),
    "1T": (3, 1, sp.Rational(29, 240), -sp.Rational(1, 15)),
    "2T": (5, -sp.Rational(5, 3), -sp.Rational(29, 48), sp.Rational(10, 9)),
}


def trace_E(field, W, HK):
    """(16 pi^2/V) Tr_field W(Delta) on an Einstein space, projected on {1, R, R^2, Riem^2}: returns dict."""
    b0, b2, b4R, b4W = HK[field]
    W = sp.sympify(W)
    W0 = sp.simplify(W.subs(R, 0))
    W1 = sp.simplify(sp.diff(W, R).subs(R, 0))
    W2 = sp.simplify(sp.diff(W, R, 2).subs(R, 0) / 2)
    return {"1": sp.simplify(b0 * Q(2, W0)),
            "R": sp.simplify(b0 * Q(2, W1) + b2 * Q(1, W0)),
            "R2": sp.simplify(b0 * Q(2, W2) + b2 * Q(1, W1) + b4R * Q(0, W0)),
            "W": sp.simplify(b4W * Q(0, W0))}


def add(a, b, w=1):
    return {k: a.get(k, 0) + w * b.get(k, 0) for k in ("1", "R", "R2", "W")}


# ---------------------------------------------------------------- BMS Hessians (Table T.1), traces with the eta terms
def bms_W_list(mutate1=False, mutate2=False, eta=True):
    """List of (name, weight, field, W(z;R)) for every entry of BMS Table T.1 (beta -> infinity taken where it appears)."""
    ub = 2 * U2 - U3 / 3
    c2 = 0 if mutate2 else 2 * U3
    HTT = c2 * D**2 - (ub * R + U1) * D - U1 * R / 2 - U0
    Hxi = -bg * (D + R / 4) * D**2 - (U1 * R + 2 * U0) * D
    Hhh = sp.Rational(1, 8) * (18 * U2 * D**2 + 3 * (U1 - 2 * U2 * R) * D + 2 * U0)
    Hss = (-bg / 16 * (3 * D - R)**2 * (D - R / 4) * D
           + sp.Rational(1, 8) * (6 * U2 * D**2 + U1 * D - U1 * R - 2 * U0) * (3 * D - R) * D)
    Hhs = sp.Rational(1, 8) * (U1 + 6 * U2 * D) * (3 * D - R) * D
    coup = ((U0, U0d), (U1, U1d), (U2, U2d), (U3, U3d))
    def Wblock(Hm):
        HP = Hm.subs(D, P)
        dR = DP * sp.diff(Hm, D).subs(D, P)
        if eta:
            for X, dX in coup:
                dR += dX * (sp.diff(Hm, X).subs(D, P) - sp.diff(Hm, X).subs(D, z))
        return HP, dR
    gsign = -1 if mutate1 else 1
    out = []
    HP, dR = Wblock(sp.Matrix([[HTT]]))
    out.append(("S_2T: h^T h^T", gsign * sp.Rational(1, 2), "2T", sp.simplify(dR[0, 0] / HP[0, 0]), "grav"))
    HP, dR = Wblock(sp.Matrix([[Hxi]]))
    out.append(("xi", sp.Rational(1, 2), "1T", A2.limit_beta(dR[0, 0] / HP[0, 0]), "gauge"))
    S = sp.Matrix([[Hhh, Hhs], [Hhs, Hss]])
    HP, dR = Wblock(S)
    M = HP.inv() * dR
    out.append(("S_hh: h h", gsign * sp.Rational(1, 2), "0", A2.limit_beta(M[0, 0]), "grav"))
    out.append(("sigma", sp.Rational(1, 2), "0", A2.limit_beta(M[1, 1]), "gauge"))
    L = lambda J: sp.simplify(DP * sp.diff(sp.log(J), D).subs(D, P))
    out += [("C-ghost C^T", -1, "1T", L(D), "u"), ("C-ghost eta", -1, "0", L((3 * D - R) * D), "u"),
            ("B-ghost B^T", -1, "1T", L(D + R / 4), "u"), ("B-ghost B", -1, "0", L((D - R / 4) * D), "u"),
            ("third ghost b^T", sp.Rational(1, 2), "1T", L(D + R / 4), "u"), ("third ghost b", sp.Rational(1, 2), "0", L((D - R / 4) * D), "u"),
            ("aux zeta^T", sp.Rational(1, 2), "1T", L(D), "u"), ("aux omega", sp.Rational(1, 2), "0", L((3 * D - R) * D), "u"),
            ("aux c^T", -1, "1T", L(D), "u"), ("aux c", -1, "0", L((3 * D - R) * D), "u"),
            ("aux s", 1, "0", L(D), "u"), ("aux t", 1, "0", L(D), "u"), ("aux chi", -1, "0", L(D), "u"), ("aux phi", sp.Rational(1, 2), "0", L(D), "u")]
    return out


def bms_traces(HK, mutate1=False, mutate2=False, eta=True, eh=False):
    """Return dict with the expanded S_2T, S_hh and universal (S_1T + S_0) parts (16 pi^2/V units).  eh=True sets u2 = u3 = 0 (and their
    d_t) first (BMS EH truncation: Table T.1 with the higher-derivative couplings zero, App. A last paragraph)."""
    sub = {U2: 0, U3: 0, U2d: 0, U3d: 0} if eh else {}
    res = {"S_2T": {}, "S_hh": {}, "S_1T": {}, "S_0": {}}
    for name, wgt, fld, W, kind in bms_W_list(mutate1, mutate2, eta):
        t = trace_E(fld, sp.simplify(wgt * W.subs(sub)), HK)
        key = "S_2T" if fld == "2T" and kind == "grav" else ("S_hh" if kind == "grav" else ("S_1T" if fld == "1T" else "S_0"))
        res[key] = add(res[key], t)
    return res


def matter_type_I(HK):
    """Type-I matter on the Einstein space: scalars (1/2)Tr_0[2/P]; Dirac -(1/2)Tr_spinor[2/(P + R/4)];
    vectors (Feynman) (1/2)Tr_V[2/(P + R/4)] - Tr_0[2/P]."""
    sc = trace_E("S", sp.Integer(1), HK)
    di = trace_E("spinor", -1 / (1 + R / 4), HK)
    ve = add(trace_E("V", 1 / (1 + R / 4), HK), trace_E("S", sp.Integer(-2), HK))
    return sc, di, ve


def beta_system(total, eh=False):
    """LHS (letter eq. E-ansatz): d_t[u0 + u1 R + (u2 - u3/6) R^2 + u3 Riem^2] = total/(16 pi^2).  Returns d_t g_i (dimensionless)."""
    k = 16 * sp.pi**2
    if eh:
        sol = sp.solve([sp.Eq(U0d, total["1"] / k), sp.Eq(U1d, total["R"] / k)], [U0d, U1d], dict=True)[0]
        return [sp.cancel(sp.together(sol[U0d] - 4 * U0)), sp.cancel(sp.together(sol[U1d] - 2 * U1))]
    eqs = [sp.Eq(U0d, total["1"] / k), sp.Eq(U1d, total["R"] / k), sp.Eq(U2d - U3d / 6, total["R2"] / k), sp.Eq(U3d, total["W"] / k)]
    sol = sp.solve(eqs, [U0d, U1d, U2d, U3d], dict=True)[0]
    return [sp.simplify(sol[U0d] - 4 * U0), sp.simplify(sol[U1d] - 2 * U1), sp.simplify(sol[U2d]), sp.simplify(sol[U3d])]


def beta_numeric(total, eh=False):
    """Numerical beta functions: the projected RHS is linear in the d_t of the couplings, T_c = a_c(u) + sum_j b_cj(u) udot_j; the LHS of
    letter eq. E-ansatz gives L udot = T/(16 pi^2) with L = rows (1), (R), (R^2: udot2 - udot3/6), (Riem^2: udot3).  Solved per evaluation.
    Returns f(g) -> d_t g (dimensionless), g = (g0, g1[, g2, g3])."""
    keys = ["1", "R"] if eh else ["1", "R", "R2", "W"]
    us = [U0, U1] if eh else [U0, U1, U2, U3]
    uds = [U0d, U1d] if eh else [U0d, U1d, U2d, U3d]
    a = [total[c].subs({x: 0 for x in uds}) for c in keys]
    b = [[sp.diff(total[c], x) for x in uds] for c in keys]
    fa = sp.lambdify(us, a, "numpy")
    fb = sp.lambdify(us, b, "numpy")
    L = np.eye(len(keys))
    if not eh:
        L[2, 3] = -1.0 / 6.0
    dims = np.array([4.0, 2.0] if eh else [4.0, 2.0, 0.0, 0.0])
    k = 16 * np.pi**2
    def f(gv):
        gv = np.asarray(gv, dtype=float)
        av = np.array(fa(*gv), dtype=float)
        bv = np.array(fb(*gv), dtype=float)
        ud = np.linalg.solve(L - bv / k, av / k)
        return ud - dims * gv
    return f


def jac_num(f, x, rel=1e-6):
    x = np.asarray(x, dtype=float)
    n = len(x)
    Jm = np.zeros((n, n))
    for j in range(n):
        h = rel * max(abs(x[j]), 1e-6)
        xp, xm = x.copy(), x.copy()
        xp[j] += h; xm[j] -= h
        Jm[:, j] = (f(xp) - f(xm)) / (2 * h)
    return Jm


def find_roots_num(f, starts):
    from scipy.optimize import fsolve
    roots = []
    for x0 in starts:
        try:
            with np.errstate(all="ignore"):
                sol, info, ier, _ = fsolve(f, np.array(x0, dtype=float), full_output=True, xtol=1e-14, maxfev=2000)
        except Exception:
            continue
        if ier != 1 or not np.all(np.isfinite(sol)) or abs(sol[1]) < 1e-12:
            continue
        try:
            if np.max(np.abs(f(sol))) > 1e-12:
                continue
        except Exception:
            continue
        if not any(np.allclose(sol, r, rtol=1e-6, atol=1e-12) for r in roots):
            roots.append(sol)
    return roots


def crit_num(f, r):
    return np.sort_complex(-np.linalg.eigvals(jac_num(f, r)))


# ---------------------------------------------------------------- BMS printed closed forms (App. C, optimized cutoff)
def Ups(p, n, u, v, w):
    return 1 / (sp.gamma(n + 1) * (u + v + w)**p)


def Upst(p, n, l, u, v, w):
    zz = sp.Symbol("zz")
    return sp.integrate(zz**(n - 1) * (1 + zz)**l * (1 - zz), (zz, 0, 1)) / sp.gamma(n) / (u + v + w)**p


def bms_printed_blocks(ns=0):
    """Printed blocks in our (16 pi^2/V) density units, with BMS's dimensionless d_t g_i expressed through our dimensionful U_id:
    gdot1 = U1d - 2 u1, gdot2 = U2d, gdot3 = U3d."""
    g0, g1, g2, g3 = U0, U1, U2, U3
    gd1, gd2, gd3 = U1d - 2 * U1, U2d, U3d
    gb = 2 * g2 - g3 / 3
    gdb = 2 * gd2 - gd3 / 3
    phi = 2
    Phi = lambda p_, n_: sp.Rational(1, 1) / sp.gamma(n_ + 1)        # Phi^p_n(0), optimized cutoff
    a = (6 * g2, g1, sp.Rational(2, 3) * g0)
    U = lambda p_, n_, m_: Ups(p_, n_, *a)
    Ut = lambda p_, n_, m_, l_: Upst(p_, n_, l_, *a)
    C1_ = 24 * g2 * U(1, 2, 1) + 2 * g1 * U(1, 2, 0) + 6 * gd2 * Ut(1, 2, 0, 1) + (2 * g1 + gd1) * Ut(1, 2, 0, 0)
    C2_ = (4 * g2 * (12 * g2 * U(2, 2, 2) - U(1, 2, 0) + U(1, 1, 1) + g1 * U(2, 2, 1)) + sp.Rational(1, 3) * g1 * U(1, 1, 0)
           - gd2 * (2 * Ut(1, 2, 0, 0) - 12 * g2 * Ut(2, 2, 1, 1) - Ut(1, 1, 0, 1))
           + (2 * g1 + gd1) * (2 * g2 * Ut(2, 2, 1, 0) + sp.Rational(1, 6) * Ut(1, 1, 0, 0)))
    C3_ = ((12 * g2 + g1) * phi + 6 * gd2 + 2 * g1 + gd1) / (6 * g2 + g1 + sp.Rational(2, 3) * g0)
    C4_ = (g2 * (96 * g2**2 * U(3, 2, 3) - 8 * g2 * (U(2, 2, 1) - U(2, 1, 2) - g1 * U(3, 2, 2)) + sp.Rational(2, 3) * (g1 * U(2, 1, 1) - U(1, 1, 0)))
           + gd2 * (24 * g2**2 * Ut(3, 2, 2, 1) - 2 * g2 * (2 * Ut(2, 2, 1, 0) - Ut(2, 1, 1, 1)) - sp.Rational(1, 3) * Ut(1, 1, 0, 0))
           + g2 * (2 * g1 + gd1) * (4 * g2 * Ut(3, 2, 2, 0) + sp.Rational(1, 3) * Ut(2, 1, 1, 0)) + sp.Rational(1, 80) * C3_)
    b = (2 * g3, -g1, -g0)
    V_ = lambda p_, n_, m_: Ups(p_, n_, *b)
    Vt = lambda p_, n_, m_, l_: Upst(p_, n_, l_, *b)
    tC1 = 40 * g3 * V_(1, 2, 1) - 10 * g1 * V_(1, 2, 0) + 10 * gd3 * Vt(1, 2, 0, 1) - 5 * (2 * g1 + gd1) * Vt(1, 2, 0, 0)
    tC2 = (10 * gb * (4 * g3 * V_(2, 2, 2) - V_(1, 2, 0) - g1 * V_(2, 2, 1))
           + 5 * g1 * (4 * g3 * V_(2, 2, 1) + sp.Rational(2, 3) * V_(1, 1, 0) - g1 * V_(2, 2, 0)) - sp.Rational(40, 3) * g3 * V_(1, 1, 1)
           + 5 * gd3 * (2 * gb * Vt(2, 2, 1, 1) + g1 * Vt(2, 2, 0, 1) - sp.Rational(2, 3) * Vt(1, 1, 0, 1))
           - 5 * (2 * g1 + gd1) * (gb * Vt(2, 2, 1, 0) - sp.Rational(1, 3) * Vt(1, 1, 0, 0) + sp.Rational(1, 2) * g1 * Vt(2, 2, 0, 0))
           - 5 * gdb * Vt(1, 2, 0, 0))
    tC3 = ((4 * g3 - g1) * phi + 2 * gd3 - (2 * g1 + gd1)) / (2 * g3 - g1 - g0)
    tC4 = (5 * gb * g1 * (8 * g3 * V_(3, 2, 2) - V_(2, 2, 0) - 2 * g1 * V_(3, 2, 1) + sp.Rational(2, 3) * V_(2, 1, 1))
           + sp.Rational(10, 3) * gb * (V_(1, 1, 0) - 4 * g3 * V_(2, 1, 2)) - sp.Rational(20, 3) * g1 * g3 * V_(2, 1, 1)
           + 5 * gb**2 * (8 * g3 * V_(3, 2, 3) - 2 * V_(2, 2, 1) - 2 * g1 * V_(3, 2, 2))
           + 5 * g1**2 * (2 * g3 * V_(3, 2, 1) + sp.Rational(1, 3) * V_(2, 1, 0) - sp.Rational(1, 2) * g1 * V_(3, 2, 0))
           + 5 * (2 * g1 + gd1) * (gb * (sp.Rational(1, 3) * Vt(2, 1, 1, 0) - g1 * Vt(3, 2, 1, 0) - gb * Vt(3, 2, 2, 0))
                                   + sp.Rational(1, 6) * g1 * Vt(2, 1, 0, 0) - sp.Rational(1, 4) * g1**2 * Vt(3, 2, 0, 0))
           + 5 * gd3 * (gb * (2 * gb * Vt(3, 2, 2, 1) + 2 * g1 * Vt(3, 2, 1, 1) - sp.Rational(2, 3) * Vt(2, 1, 1, 1))
                        - sp.Rational(1, 3) * g1 * Vt(2, 1, 0, 1) + sp.Rational(1, 2) * g1**2 * Vt(3, 2, 0, 1))
           - 5 * gdb * (gb * Vt(2, 2, 1, 0) + sp.Rational(1, 2) * g1 * Vt(2, 2, 0, 0) - sp.Rational(1, 3) * Vt(1, 1, 0, 0))
           - sp.Rational(29, 48) * tC3)
    Shh = {"1": C1_ / 2, "R": C2_ / 2, "W": C3_ / 360, "R2": C4_ / 2}
    S2T = {"1": tC1 / 2, "R": tC2 / 2, "W": sp.Rational(10, 9) * tC3 / 2, "R2": tC4 / 2}
    S0 = {"1": -Phi(1, 2), "R": -sp.Rational(1, 6) * (Phi(1, 1) + 2 * Phi(2, 2)), "R2": -(sp.Rational(phi, 160) + Phi(2, 1) / 18 + Phi(3, 2) / 9),
          "W": -sp.Rational(phi, 360)}
    S1T = {"1": -3 * Phi(1, 2), "R": -Phi(1, 1), "R2": -sp.Rational(29, 480) * phi, "W": sp.Rational(phi, 30)}
    Smat = {"1": Phi(1, 2), "R": Phi(1, 1) / 6, "R2": sp.Rational(phi, 2) / 80, "W": sp.Rational(phi, 2) / 180}
    return {"S_hh": Shh, "S_2T": S2T, "S_0": S0, "S_1T": S1T, "S_matter": Smat}


def bms_printed_EH(ns):
    """BMS eqs. betaEH / etaEH / BEH (optimized cutoff): returns (beta_g, beta_lambda) in (g, lambda)."""
    g, lam = sp.symbols("g lambda", real=True)
    Phi = lambda p_, n_, w: 1 / (sp.gamma(n_ + 1) * (1 + w)**p_)
    Pt = lambda p_, n_, w: 1 / (sp.gamma(n_ + 2) * (1 + w)**p_)
    B1 = (ns - 7) * Phi(1, 1, 0) - 2 * Phi(2, 2, 0) + Phi(1, 1, -sp.Rational(4, 3) * lam) - 10 * Phi(1, 1, -2 * lam) - 15 * Phi(2, 2, -2 * lam)
    B2 = 5 * Pt(1, 1, -2 * lam) + sp.Rational(15, 2) * Pt(2, 2, -2 * lam) - sp.Rational(1, 2) * Pt(1, 1, -sp.Rational(4, 3) * lam)
    B3 = (ns - 4) * Phi(1, 2, 0) + Phi(1, 2, -sp.Rational(4, 3) * lam) + 5 * Phi(1, 2, -2 * lam)
    eta = g * B1 / (6 * sp.pi - g * B2)
    bg_ = (2 + eta) * g
    bl_ = (eta - 2) * lam + g / (2 * sp.pi) * B3 - g / (4 * sp.pi) * eta * (5 * Pt(1, 2, -2 * lam) + Pt(1, 2, -sp.Rational(4, 3) * lam))
    return g, lam, sp.simplify(bg_), sp.simplify(bl_)


# ---------------------------------------------------------------- roots
def to_glb(gt):
    out = [-1 / (16 * np.pi * gt[1]), -gt[0] / (2 * gt[1])]
    return out + list(gt[2:])


def from_glb(v):
    g1 = -1 / (16 * np.pi * v[0])
    return [-2 * v[1] * g1, g1] + list(v[2:])


def denominators(gt):
    g0, g1 = gt[0], gt[1]
    g2 = gt[2] if len(gt) > 2 else 0.0
    g3 = gt[3] if len(gt) > 3 else 0.0
    return 2 * g3 - g1 - g0, -(6 * g2 + g1 + 2 * g0 / 3)


def admissible(gt):
    glb = to_glb(gt)
    d2, d0 = denominators(gt)
    return glb[0] > 0 and d2 > 0 and d0 > 0


def in_domain(gt):
    glb = to_glb(gt)
    g_, l_ = glb[0], glb[1]
    ok = 0 < g_ < 50 and -50 < l_ < 0.5
    edge = g_ > 47.5 or l_ < -47.5 or l_ > 0.475
    for x in glb[2:]:
        ok = ok and -1e3 < x < 1e3
        edge = edge or abs(x) > 950
    return ok, edge


def find_roots(betas, nvar, starts):
    from scipy.optimize import fsolve
    syms = [U0, U1, U2, U3][:nvar]
    f = sp.lambdify(syms, betas, "numpy")
    J = sp.lambdify(syms, sp.Matrix(betas).jacobian(syms), "numpy")
    roots = []
    for x0 in starts:
        try:
            with np.errstate(all="ignore"):
                sol, info, ier, _ = fsolve(lambda v: np.array(f(*v), dtype=float), np.array(x0, dtype=float),
                                           fprime=lambda v: np.array(J(*v), dtype=float), full_output=True, xtol=1e-14, maxfev=500)
        except Exception:
            continue
        if ier != 1 or not np.all(np.isfinite(sol)) or abs(sol[1]) < 1e-12:
            continue
        if np.max(np.abs(np.array(f(*sol), dtype=float))) > 1e-12:
            continue
        if not any(np.allclose(sol, r, rtol=1e-6, atol=1e-12) for r in roots):
            roots.append(sol)
    return roots, f, J


def grid_starts(nvar):
    gs = np.geomspace(0.05, 40, 10)
    ls = np.linspace(-45, 0.45, 15)
    b2 = [0.0] + [s * 10.0**e for e in range(-4, 3) for s in (1, -1)]
    b3 = [0.0] + [s * 10.0**e for e in range(-3, 1) for s in (1, -1)]
    out = []
    for G_ in gs:
        for L_ in ls:
            if nvar == 2:
                out.append(from_glb([G_, L_]))
            else:
                for x2 in b2:
                    for x3 in b3:
                        out.append(from_glb([G_, L_, x2, x3]))
    return out


def crit(J, r):
    return np.sort_complex(-np.linalg.eigvals(np.array(J(*r), dtype=float)))


# ---------------------------------------------------------------- flat-space f_g with the C^2 term (kernel restriction) + numeric beta check
def fg_flat_bms(mutate2=False):
    """f_g(u0, u1, u2, u3, u1dot, u2dot, u3dot) by restriction to ker(gauge fixing) (TT + conformal mode + photon), AS3 method,
    with the flat quadratic action u0 (sqrt g)^(2) + u1 (sqrt g R)^(2) + (u2 - 2u3/3)(R^(1))^2 + 2 u3 (R^(1)_mn)^2."""
    s = sp.Symbol("s", positive=True)
    B, V1, V2, hm, hp, am, ap = FG1.bilinear_action(s)
    B = B.subs(FG1.agf, 0).subs({FG1.lam: -U0 / (2 * U1)}).subs({FG1.g: -1 / (16 * sp.pi * U1)})
    Hm, _ = FG1.hmat("hm"); Hp, _ = FG1.hmat("hp")
    tr = lambda H: sum(H[i, i] for i in range(4))
    q3 = lambda m: 1 if m == 3 else 0
    R1 = lambda H: s * (tr(H) - H[3, 3])
    Rmn = lambda H: [[sp.Rational(1, 2) * s * (-q3(m) * H[3, n] - q3(n) * H[3, m] + H[m, n] + q3(m) * q3(n) * tr(H)) for n in range(4)] for m in range(4)]
    c3 = 0 if mutate2 else 2 * U3
    Rm_m, Rm_p = Rmn(Hm), Rmn(Hp)
    B += (U2 - sp.Rational(2, 3) * U3) * R1(Hm) * R1(Hp) + c3 * sum(Rm_m[m][n] * Rm_p[m][n] for m in range(4) for n in range(4))
    chim = [Hm[3, m] - sp.Rational(1, 4) * q3(m) * tr(Hm) for m in range(4)]
    chip = [Hp[3, m] - sp.Rational(1, 4) * q3(m) * tr(Hp) for m in range(4)]
    GF = -sp.Rational(1, 2) * s**2 * sum(chim[m] * chip[m] for m in range(4))
    Phim, Phip = hm + am, hp + ap
    n = 14
    Mk = sp.Matrix(n, n, lambda i, j: sp.diff(B, Phim[i], Phip[j]))
    Agf = sp.Matrix(n, n, lambda i, j: sp.diff(GF, Phim[i], Phip[j]))
    M1 = sp.Matrix(n, n, lambda i, j: sp.diff(V1, Phim[i], Phip[j]))
    M2 = sp.Matrix(n, n, lambda i, j: sp.diff(V2, Phim[i], Phip[j]))
    idx = {pq: i for i, pq in enumerate(FG1.pairs)}
    def vec(d):
        v = [0] * n
        for kk, c in d.items():
            v[idx[kk]] += c
        return v
    th = sp.Rational(1, 3)
    cols = [vec({(0, 1): 1}), vec({(0, 2): 1}), vec({(1, 2): 1}),
            vec({(0, 0): 1, (3, 3): th}), vec({(1, 1): 1, (3, 3): th}), vec({(2, 2): 1, (3, 3): th})]
    cols += [[0] * 10 + [1 if j == kk else 0 for j in range(4)] for kk in range(4)]
    E = sp.Matrix(cols).T
    ker_ok = sp.simplify(Agf * E) == sp.zeros(n, 10)
    # exact reduction to TT + photon (verified): the conformal mode h = phi delta (kernel combination diag0 + diag1 + diag2) does not mix
    # with the TT modes in the kinetic matrix (spin 0 vs spin 2) and has no h-a vertex (Maxwell is conformally invariant); its M2 entries
    # are TT-conformal off-diagonal only, which cannot contribute to tr[G M2 G dR] with block-diagonal G and dR.
    Ett = sp.Matrix([cols[0], cols[1], cols[2], [a - b for a, b in zip(cols[3], cols[4])],
                     [a + b - 2 * c for a, b, c in zip(cols[3], cols[4], cols[5])]]).T
    Econf = sp.Matrix([[a + b + c for a, b, c in zip(cols[3], cols[4], cols[5])]]).T
    Eph = sp.Matrix(cols[6:]).T
    red_ok = (sp.simplify(Econf.T * Mk * Ett) == sp.zeros(1, 5) and sp.simplify(Econf.T * M1 * Eph) == sp.zeros(1, 4)
              and sp.simplify(Eph.T * M1 * Econf) == sp.zeros(4, 1) and sp.simplify(Econf.T * M2 * Econf) == sp.zeros(1, 1)
              and sp.simplify(Econf.T * Mk * Eph) == sp.zeros(1, 4))
    ker_ok = ker_ok and red_ok
    E9 = Ett.row_join(Eph)
    kap = FG1.kap
    MkP = (E9.T * Mk * E9).subs(s, 1)
    dR = (E9.T * sp.diff(Mk, s) * E9).subs(s, 1) * 2
    for X, dX in ((U1, U1d), (U2, U2d), (U3, U3d)):
        blk = (E9.T * sp.diff(Mk, X) * E9)[:5, :5]
        dR[:5, :5] += dX * (blk.subs(s, 1) - blk)
    dR = dR.subs(s, kap**2)
    G = sp.zeros(9, 9)
    G[:5, :5] = MkP[:5, :5].inv(); G[5:, 5:] = MkP[5:, 5:].inv()
    G = G.applyfunc(sp.cancel)
    trC = 0
    for A_ in range(6):      # T(e_A) = C_AA: one field-strength component at a time
        fsub = {F: (1 if i == A_ else 0) for i, F in enumerate(FG1.Fs)}
        m1 = (E9.T * M1 * E9).subs(fsub)
        m2 = (E9.T * M2 * E9).subs(fsub)
        TA = -sp.Rational(1, 2) * (G * m2 * G * dR).trace() + sp.Rational(1, 2) * (G * m1 * G * m1 * G * dR).trace()
        trC += sp.cancel(sp.together(TA))
    cFF = sp.integrate(sp.expand(sp.cancel(trC) / 12 * kap**3 / (8 * sp.pi**2)), (kap, 0, 1))
    fg = sp.factor(sp.cancel(2 * FG1.e**2 * cFF))
    mats = dict(Mk=Mk, Agf=Agf, M1=M1, M2=M2, s=s)
    return fg, ker_ok, mats


def fg_numeric_full(mats, vals, beta_val, dps=40):
    """Full 14 x 14 traces at FINITE beta (gauge fixing beta * Agf added to the kinetic matrix and to the regulator), numeric couplings
    'vals' (dict of sympy symbols -> numbers), mpmath precision; f_g = 2 e^2 cFF with Gauss-Legendre in kappa (exact for polynomials)."""
    import mpmath as mp
    mp.mp.dps = dps
    s = mats["s"]
    Mk = mats["Mk"] + bg * mats["Agf"]
    kap = FG1.kap
    # exact rational inputs (a float coupling would enter sympy's evalf as a 15-digit Float and limit the precision of the
    # beta-sized cancellations; that produced a noise floor growing like beta in the second trial run)
    subs = {k_: sp.Rational(float(v_)) if not isinstance(v_, (int, sp.Integer, sp.Rational)) else v_ for k_, v_ in vals.items()}
    subs[bg] = sp.Rational(beta_val)
    MkP = Mk.subs(s, 1)
    dR = sp.diff(Mk, s).subs(s, 1) * 2
    for X, dX in ((U1, U1d), (U2, U2d), (U3, U3d)):
        blk = sp.diff(Mk[:10, :10], X)
        dR[:10, :10] += dX * (blk.subs(s, 1) - blk)
    nodes, weights = np.polynomial.legendre.leggauss(12)
    total = mp.mpf(0)
    MkPn = _to_mp(MkP.subs(subs), dps)
    G = mp.inverse(MkPn)
    for x, wq in zip(nodes, weights):
        kv = mp.mpf(x) / 2 + mp.mpf(1) / 2
        sub2 = dict(subs); sub2[kap] = sp.Rational(float(x)) / 2 + sp.Rational(1, 2)
        dRn = _to_mp(dR.subs(s, kap**2).subs(sub2), dps)
        acc = mp.mpf(0)
        for A_ in range(6):
            fsub = {F: (1 if i == A_ else 0) for i, F in enumerate(FG1.Fs)}
            M1n = _to_mp(mats["M1"].subs(sub2).subs(fsub), dps)
            M2n = _to_mp(mats["M2"].subs(sub2).subs(fsub), dps)
            Tv = -mp.mpf(1) / 2 * _tr(G * M2n * G * dRn) + mp.mpf(1) / 2 * _tr(G * M1n * G * M1n * G * dRn)
            acc += Tv
        total += mp.mpf(wq) / 2 * kv**3 * acc
    cFF = total / 12 / (8 * mp.pi**2)
    return 2 * mp.mpf(vals[FG1.e])**2 * cFF


def _to_mp(Ms, dps):
    import mpmath as mp
    out = mp.matrix(Ms.rows, Ms.cols)
    for i in range(Ms.rows):
        for j in range(Ms.cols):
            re_, im_ = sp.N(Ms[i, j], dps).as_real_imag()
            out[i, j] = mp.mpc(mp.mpf(str(sp.N(re_, dps))), mp.mpf(str(sp.N(im_, dps))))
    return out


def _tr(Mx):
    import mpmath as mp
    return mp.re(sum(Mx[i, i] for i in range(Mx.rows)))
