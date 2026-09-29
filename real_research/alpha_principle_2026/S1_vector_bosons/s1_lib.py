"""s1_lib.py -- shared library for S1 scripts 3 and 4 (mode sums for the scalar, the W_y polarization and the coupled {W_x, W_z} sector of the charged Proca field).

Conventions (H = c = 1, conformal frame, see S1_PREREGISTRATION.md and s1_1_structure.py):
  phase-space vector X = (fields..., momenta...), H = X^dagger h X, dX/dtau = J h X, J = [[0,1],[-1,0]]; vacuum covariance Gamma (real symmetric, Gamma = Re Sum U U^dagger),
  purity Gamma J Gamma = J/4, evolution Gamma' = A Gamma + Gamma A^T, A = J h.
  kinds:  'scalar' : h = diag(P^2 + M^2 [- 2/tau^2 tagged order 2], 1)     (Kobayashi-Afshordi minimal scalar, the regression target)
          'y'      : h = diag(P^2 + M^2, 1)                                (Proca W_y, no a''/a)
          'xz'     : X = (W_x, W_z, Pi_x, Pi_z), h from H = |Pi|^2 + |P x W|^2 + M^2|W|^2 + |P.Pi + G W_z|^2/M^2, G = c*lambda/tau^2 (script 1, A3)
  P = (k_perp, p), p = k_z + lambda/tau, M^2 = mu^2/tau^2.
  Current: J_z/e = Tr[(d_p h) Gamma] - c d/dtau Tr[Ppol Gamma]  (script 1, A6);  Ppol = -[2G|W_z|^2 + (P.Pi) Wc_z + c.c.]/M^2 for the xz block.
  f := Int k^2 dk Int_{-1}^{1} dr Tr[...] = -f_KA (sign found in script 3, C2).
Adiabatic schemes: 'alg' (all algebraic dependence of h is order 0), 'F1' (the G terms of h are order 1 and order 2; F = dA).
"""
import math
import numpy as np
import sympy as sp

tau_s, kz_s, kp_s, lam_s, mu_s = sp.symbols("tau kz kp lam mu", real=True)
p_s, G_s = sp.symbols("p_s G_s", real=True)
J_CACHE = {}


def Jmat(n):
    if n not in J_CACHE:
        J_CACHE[n] = np.block([[np.zeros((n, n)), np.eye(n)], [-np.eye(n), np.zeros((n, n))]])
    return J_CACHE[n]


class Model:
    """kind in {'scalar','y','xz'}; c in {0,1} (Pauli strength; 1 = g=2); scheme in {'alg','F1'}."""

    def __init__(self, kind, c=1, scheme="alg", jmax=4):
        self.nopol = scheme.endswith("_nopol")            # control: drop the polarization (Pauli magnetization) current  -d/dtau P_pol
        scheme = scheme.replace("_nopol", "")
        self.kind, self.c, self.scheme = kind, c, scheme
        self.jmax = jmax
        pt = kz_s + lam_s / tau_s                                 # kinetic momentum
        M2 = mu_s**2 / tau_s**2
        Gt = c * lam_s / tau_s**2
        P2 = kp_s**2 + p_s**2
        eps = sp.Symbol("eps")
        Mm = sp.Symbol("Msym", positive=True)
        self.n = None
        if kind == "scalar":
            self.n = 2
            h = sp.Matrix([[P2 + Mm**2 + eps**2 * (-2 / tau_s**2), 0], [0, 1]])
            Q_P = None
        elif kind == "y":
            self.n = 2
            h = sp.Matrix([[P2 + Mm**2, 0], [0, 1]])
            Q_P = None
        elif kind == "xz":
            self.n = 4
            Gs = G_s
            tagG = eps if scheme == "F1" else 1
            # X = (Wx, Wz, Pix, Piz); cvec: coefficients of (P.Pi + G Wz) on X ; u: coefficients of (p Wx - kp Wz)
            cvec = sp.Matrix([0, tagG * Gs, kp_s, p_s])
            u = sp.Matrix([p_s, -kp_s, 0, 0])
            h = sp.diag(Mm**2, Mm**2, 1, 1) + u * u.T + cvec * cvec.T / Mm**2
            # polarization bilinear  Ppol = -[2 G |Wz|^2 + (P.Pi) Wc_z + c.c.]/M^2   (order: G terms tagged like above)
            Q_P = sp.zeros(4, 4)
            Q_P[1, 1] = -2 * tagG * Gs / Mm**2
            Q_P[1, 2] = Q_P[2, 1] = -kp_s / Mm**2
            Q_P[1, 3] = Q_P[3, 1] = -p_s / Mm**2
            Q_P = c * Q_P
            if self.nopol:
                Q_P = None
        else:
            raise ValueError(kind)
        # tag decomposition h = h0 + eps h1 + eps^2 h2
        hp = [sp.simplify(h.applyfunc(lambda e: sp.diff(e, eps, i).subs(eps, 0) / sp.factorial(i))) for i in range(3)]
        dph = [hh.diff(p_s) for hh in hp]
        sub = {p_s: pt, Mm: mu_s / (-tau_s), G_s: c * lam_s / tau_s**2}
        self.hs = [hh.subs(sub) for hh in hp]
        self.dphs = [dd.subs(sub) for dd in dph]
        if Q_P is not None:
            QPt = [sp.simplify(Q_P.applyfunc(lambda e: sp.diff(e, eps, i).subs(eps, 0) / sp.factorial(i))) if scheme == "F1" else (Q_P if i == 0 else sp.zeros(4, 4)) for i in range(3)]
            self.QPs = [q.subs(sub) for q in QPt]
        else:
            self.QPs = [sp.zeros(self.n, self.n) for _ in range(3)]
        args = (tau_s, kz_s, kp_s, lam_s, mu_s)
        L = lambda e: sp.lambdify(args, e, "numpy", cse=True)
        self.h_f = [[L(self.hs[i].diff(tau_s, m)) for m in range(jmax + 1)] for i in range(3)]
        self.dph_f = [L(self.dphs[i]) for i in range(3)]
        self.QP_f = [[L(self.QPs[i].diff(tau_s, m)) for m in range(2)] for i in range(3)]
        self.hasP = Q_P is not None
        # dressed frame U(tau): X_c = U X_d, balanced (see module docstring of s1_3)
        pt_, M_ = pt, mu_s / (-tau_s)
        Pn = sp.sqrt(kp_s**2 + pt_**2)
        om = sp.sqrt(Pn**2 + M_**2)
        if kind in ("scalar", "y"):
            sT = 1 / sp.sqrt(om)
            U = sp.diag(sT, 1 / sT)
        else:
            Lh = sp.Matrix([kp_s, pt_]) / Pn
            Th = sp.Matrix([pt_, -kp_s]) / Pn
            R = sp.Matrix.hstack(Lh, Th)
            sL, sT = sp.sqrt(om) / M_, 1 / sp.sqrt(om)
            S1 = sp.diag(sL, sT)
            S2 = sp.diag(1 / sL, 1 / sT)
            U = sp.zeros(4, 4)
            U[:2, :2] = R * S1
            U[2:, 2:] = R * S2
        self.U_f = L(U)
        self.Up_f = L(U.diff(tau_s))
        self.Ad_f = None
        if kind == "xz":
            # Analytic dressed generator (no numerical cancellation): X_c = Rhat V_s X_d, rotation to (L,T), then balanced scaling V_s = diag(sL, sT, 1/sL, 1/sT).
            #   A_d = J h_d - V_s^{-1} (Rhat^T Rhat') V_s - diag(sL'/sL, sT'/sT, -sL'/sL, -sT'/sT),   h_d = V_s h_rot V_s,
            #   H_rot = |Pi_L|^2 + |Pi_T|^2 + (P^2+M^2)|W_T|^2 + M^2|W_L|^2 + |P Pi_L + g_L W_L + g_T W_T|^2 / M^2,  g_L = G p/P, g_T = -G k_perp/P.
            Gt_ = c * lam_s / tau_s**2
            gL, gT = Gt_ * pt_ / Pn, -Gt_ * kp_s / Pn
            cr = sp.Matrix([gL, gT, Pn, 0])
            hrot = sp.diag(M_**2, Pn**2 + M_**2, 1, 1) + cr * cr.T / M_**2
            Vs = sp.diag(sL, sT, 1 / sL, 1 / sT)
            hd = Vs * hrot * Vs
            Jm = sp.Matrix([[0, 0, 1, 0], [0, 0, 0, 1], [-1, 0, 0, 0], [0, -1, 0, 0]])
            Rm = sp.Matrix.hstack(Lh, Th)
            RtRp = (Rm.T * Rm.diff(tau_s)).applyfunc(sp.simplify)
            rot = sp.zeros(4, 4)
            rot[:2, :2] = RtRp
            rot[2:, 2:] = RtRp
            Ad = Jm * hd - Vs.inv() * rot * Vs - sp.diag(sL.diff(tau_s) / sL, sT.diff(tau_s) / sT, -sL.diff(tau_s) / sL, -sT.diff(tau_s) / sT)
            self.Ad_f = L(Ad)
            # analytic dressed-frame current operators (no cancellations): rotated vectors u_r = (0,P,0,0), u_pr = (kp/P, p/P,0,0), c_r = (gL, gT, P, 0), c_pr = (0,0,p/P,-kp/P)
            Vv = lambda v: sp.Matrix([Vs[i, i] * v[i] for i in range(4)])
            u_r = Vv(sp.Matrix([0, Pn, 0, 0]))
            u_pr = Vv(sp.Matrix([kp_s / Pn, pt_ / Pn, 0, 0]))
            c_r = Vv(sp.Matrix([gL, gT, Pn, 0]))
            c_pr = Vv(sp.Matrix([0, 0, pt_ / Pn, -kp_s / Pn]))
            Qd = u_pr * u_r.T + u_r * u_pr.T + (c_pr * c_r.T + c_r * c_pr.T) / M_**2
            wz = Vv(sp.Matrix([pt_ / Pn, -kp_s / Pn, 0, 0]))
            pip = Vv(sp.Matrix([0, 0, Pn, 0]))
            QPd = c * (-(2 * Gt_ * wz * wz.T + wz * pip.T + pip * wz.T) / M_**2) if (c != 0 and not self.nopol) else sp.zeros(4, 4)
            self.Qd_f = L(Qd)
            self.QPd_f = L(QPd)
            self.QPdp_f = L(QPd.diff(tau_s))

    # ------------------------------------------------------------------ numerics
    def hj(self, tau, kz, kp, lam, mu):
        """h jets: hj[i][m] = d^m h_i / dtau^m (numpy)."""
        a = (tau, kz, kp, lam, mu)
        return [[np.array(self.h_f[i][m](*a), dtype=float) for m in range(self.jmax + 1)] for i in range(3)]

    def h_total(self, tau, kz, kp, lam, mu):
        a = (tau, kz, kp, lam, mu)
        return sum(np.array(self.h_f[i][0](*a), dtype=float) for i in range(3))

    def U(self, tau, kz, kp, lam, mu):
        a = (tau, kz, kp, lam, mu)
        return np.array(self.U_f(*a), dtype=float), np.array(self.Up_f(*a), dtype=float)

    def A_dressed(self, tau, kz, kp, lam, mu):
        """A_d = U^{-1}(A U - U') for the exact ODE in the dressed frame."""
        a = (tau, kz, kp, lam, mu)
        if self.Ad_f is not None:
            return np.array(self.Ad_f(*a), dtype=float)
        U = np.array(self.U_f(*a), dtype=float)
        Up = np.array(self.Up_f(*a), dtype=float)
        h = sum(np.array(self.h_f[i][0](*a), dtype=float) for i in range(3))
        A = Jmat(self.n // 2) @ h
        # U^{-1} via solve (well conditioned by construction)
        return np.linalg.solve(U, A @ U - Up)


# ------------------------------------------------------------------ adiabatic machinery
def _sym_basis(n):
    B = []
    for i in range(n):
        for j in range(i, n):
            E = np.zeros((n, n))
            E[i, j] = 1
            E[j, i] = 1
            B.append(E)
    return B


_BASIS = {}


def _solve_sym(A0, G0, rhs_L, rhs_P, n, want_purity=True):
    """symmetric X with A0 X + X A0^T = rhs_L and G0 J X + X J G0 = rhs_P (least squares over the symmetric parametrisation)."""
    if n not in _BASIS:
        _BASIS[n] = _sym_basis(n)
    Bs = _BASIS[n]
    J = Jmat(n // 2)
    cols = []
    for E in Bs:
        c1 = (A0 @ E + E @ A0.T).ravel()
        c2 = (G0 @ J @ E + E @ J @ G0).ravel() if want_purity else np.zeros(0)
        cols.append(np.concatenate([c1, c2]))
    Mtx = np.array(cols).T
    rhs = np.concatenate([rhs_L.ravel(), rhs_P.ravel() if want_purity else np.zeros(0)])
    x, res, rank, sv = np.linalg.lstsq(Mtx, rhs, rcond=1e-13)
    X = sum(xi * E for xi, E in zip(x, Bs))
    resid = np.linalg.norm(Mtx @ x - rhs) / max(1e-300, np.linalg.norm(rhs) + 1e-300)
    return X, resid


def gamma0_closed(h):
    n2 = h.shape[0]
    J = Jmat(n2 // 2)
    w, V = np.linalg.eigh(h)
    hh = (V * np.sqrt(w)) @ V.T
    hi = (V / np.sqrt(w)) @ V.T
    K = hh @ J @ hh
    w2, Uu = np.linalg.eigh(K.T @ K)
    absK = (Uu * np.sqrt(np.maximum(w2, 0))) @ Uu.T
    return 0.5 * hi @ absK @ hi


def _prod_jet(X, Y, m):
    """m-th derivative of X*Y from jets X[0..], Y[0..]."""
    return sum(math.comb(m, j) * X[j] @ Y[m - j] for j in range(m + 1))


def adiabatic_jets(hj, order=2, S=None):
    """hj[i][m] (tags i = 0,1,2 ; jets m = 0,1,2) in the frame where they are given.  Returns Gam[n][m] (n = 0..order, m = 0..order-n) as arrays."""
    n = hj[0][0].shape[0]
    J = Jmat(n // 2)
    NJ = len(hj[0])
    A = [[J @ hj[i][m] for m in range(NJ)] for i in range(3)]
    Gam = [[None] * (order + 2) for _ in range(order + 1)]
    resid = 0.0
    # order 0
    G0 = gamma0_closed(hj[0][0])
    Gam[0][0] = G0
    A0 = A[0][0]
    for m in range(1, order + 1):
        rhsL = np.zeros((n, n))
        for j in range(1, m + 1):
            rhsL -= math.comb(m, j) * (A[0][j] @ Gam[0][m - j] + Gam[0][m - j] @ A[0][j].T)
        rhsP = np.zeros((n, n))
        for j in range(1, m):
            rhsP -= math.comb(m, j) * (Gam[0][j] @ J @ Gam[0][m - j])
        X, r_ = _solve_sym(A0, G0, rhsL, rhsP, n)
        Gam[0][m] = X
        resid = max(resid, r_)
    # orders 1..order
    for nn in range(1, order + 1):
        for m in range(0, order - nn + 1):
            # L(Gam_nn^{(m)}) = R^{(m)} - sum_{j=1}^m C(m,j)[A0^{(j)} Gam_nn^{(m-j)} + ...],  R = Gam_{nn-1}' - sum_{i=1}^{nn}(A_i Gam_{nn-i} + Gam_{nn-i} A_i^T)
            Rm = Gam[nn - 1][m + 1].copy()
            for i in range(1, min(nn, 2) + 1):
                for j in range(m + 1):
                    Rm -= math.comb(m, j) * (A[i][j] @ Gam[nn - i][m - j] + Gam[nn - i][m - j] @ A[i][j].T)
            for j in range(1, m + 1):
                Rm -= math.comb(m, j) * (A[0][j] @ Gam[nn][m - j] + Gam[nn][m - j] @ A[0][j].T)
            # purity: sum_{i+j=nn} sum_l C(m,l) Gam_i^{(l)} J Gam_j^{(m-l)} = 0
            rhsP = np.zeros((n, n))
            for i in range(0, nn + 1):
                jn = nn - i
                for l in range(m + 1):
                    if i == 0 and l == 0:
                        continue           # unknown term (with j = nn, l' = m)
                    if jn == 0 and l == m:
                        continue
                    rhsP -= math.comb(m, l) * (Gam[i][l] @ J @ Gam[jn][m - l])
            X, r_ = _solve_sym(A0, G0, Rm, rhsP, n)
            Gam[nn][m] = X
            resid = max(resid, r_)
    return Gam, resid


def current_series(model, tau, kz, kp, lam, mu, order=2):
    """Adiabatic series of the current integrand  Tr[dph Gamma] - d/dtau Tr[QP Gamma]  through total order `order`, evaluated in the balanced constant-S frame.
    Returns (series list per order, Gamma orders in the balanced frame, S, residual)."""
    U, _ = model.U(tau, kz, kp, lam, mu)
    hj = model.hj(tau, kz, kp, lam, mu)
    n = model.n
    # balanced frame: h_b^{(m)} = U^T h^{(m)} U (U is symplectic: U^T J U = J)
    hb = [[U.T @ hj[i][m] @ U for m in range(len(hj[i]))] for i in range(3)]
    Gam, resid = adiabatic_jets(hb, order=order)
    a = (tau, kz, kp, lam, mu)
    dph = [U.T @ np.array(model.dph_f[i](*a), dtype=float) @ U for i in range(3)]
    QP = [[U.T @ np.array(model.QP_f[i][m](*a), dtype=float) @ U for m in range(2)] for i in range(3)]
    # NB: QP' (m = 1) as computed is d/dtau of the Cartesian-frame matrix; the constant-S transform is the correct one at this instant.
    ser = np.zeros(order + 1)
    for nn in range(order + 1):
        s = 0.0
        for i in range(0, min(nn, 2) + 1):
            j = nn - i
            s += np.trace(dph[i] @ Gam[j][0])
        if model.hasP and nn >= 1:
            for i in range(0, min(nn - 1, 2) + 1):
                j = nn - 1 - i
                s -= np.trace(QP[i][1] @ Gam[j][0]) + np.trace(QP[i][0] @ Gam[j][1])
        ser[nn] = s
    return ser, Gam, U, resid


def current_exact(model, tau, kz, kp, lam, mu, Gam_b, U):
    """Exact-state current.  For the xz block the dressed-frame analytic operators are used (numerically stable);
    Gam_b is the dressed-frame covariance Gamma_d at this instant (= balanced-frame covariance)."""
    if getattr(model, "Ad_f", None) is not None:
        a = (tau, kz, kp, lam, mu)
        Qd = np.array(model.Qd_f(*a), dtype=float)
        val = np.trace(Qd @ Gam_b)
        if model.hasP:
            Ad = np.array(model.Ad_f(*a), dtype=float)
            QP0 = np.array(model.QPd_f(*a), dtype=float)
            QP1 = np.array(model.QPdp_f(*a), dtype=float)
            val -= np.trace(QP1 @ Gam_b) + np.trace(QP0 @ (Ad @ Gam_b + Gam_b @ Ad.T))
        return val
    return _current_exact_cartesian(model, tau, kz, kp, lam, mu, Gam_b, U)


def _current_exact_cartesian(model, tau, kz, kp, lam, mu, Gam_b, U):
    """Tr[dph Gamma] - d/dtau Tr[QP Gamma] for the EXACT covariance Gamma_b (balanced frame at this instant: Gamma_c = U Gamma_b U^T)."""
    a = (tau, kz, kp, lam, mu)
    h_c = model.h_total(*a)
    n = model.n
    J = Jmat(n // 2)
    dph = sum(U.T @ np.array(model.dph_f[i](*a), dtype=float) @ U for i in range(3))
    val = np.trace(dph @ Gam_b)
    if model.hasP:
        QP0 = sum(U.T @ np.array(model.QP_f[i][0](*a), dtype=float) @ U for i in range(3))
        QP1 = sum(U.T @ np.array(model.QP_f[i][1](*a), dtype=float) @ U for i in range(3))
        A_b = np.linalg.solve(U, J @ h_c @ U)                # exact Cartesian A, transformed by the constant U
        val -= np.trace(QP1 @ Gam_b) + np.trace(QP0 @ (A_b @ Gam_b + Gam_b @ A_b.T))
    return val
