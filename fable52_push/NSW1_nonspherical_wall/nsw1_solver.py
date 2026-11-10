#!/usr/bin/env python3
"""NSW1 solver library (criteria 052f87daad). TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.

A law-on region Omega with a sharp or smooth wall around baryons, Newton outside:
    div[K grad Phi] = 4 pi rho,   K = 1 - S / (1 + u),   u = |grad Phi|        (lengths r_M, fields a0, G M_b = 1)
Coordinates fitted to the wall: x = m X_w(mu), X_w(mu) = (R_w, z_w) the wall curve, s = ln m. Metric combinations
    A = (R_w / D) |X_w'|^2,  B = (R_w / D) X_w . X_w',  C = (R_w / D) |X_w|^2,  RD = R_w D,  D = |R_w z_w' - z_w R_w'|
give   flux through an s-face per dmu dphi   = m K (A Phi_s - B Phi_mu),
       flux through a mu-face per ds dphi    = m K (-B Phi_s + C Phi_mu),
       |grad Phi|^2 = (A Phi_s^2 - 2 B Phi_s Phi_mu + C Phi_mu^2) / (m^2 RD).
Finite volume, vertex-centred in s (nodes on both boundaries), cells on Gauss-Legendre nodes in mu. Exterior: Laplace with the
Dirichlet-to-Neumann map on the outer surface: confocal spheroidal harmonics for a spheroid ("conf"), the exterior multipole
series collocated on the surface for a star-shaped wall ("ray"), or a prescribed monopole flux ("far").
Newton with a complex-step Jacobian (9 colours). All fluxes are per radian of azimuth.
"""
import math
import numpy as np
from numpy.polynomial.legendre import leggauss, legvander, legder, legval
from scipy.sparse import coo_matrix, csc_matrix
from scipy.sparse.linalg import splu


# ------------------------------------------------------------------ the law and the wall pressure
def u_in(y):
    """the law's field for displacement y: u^2 / (1 + u) = y."""
    y = np.asarray(y, float); return 0.5 * y + np.sqrt(0.25 * y * y + y)
def nu(y): return u_in(y) / np.asarray(y, float)
def Jt(u): return u - np.log1p(u)                                   # J in units a0^2 / (4 pi G)
def Wsph(u): return u - np.log1p(u) - u * u / (2.0 * (1.0 + u) ** 2)  # SWT1's W
def Wg(u, n): return u - np.log1p(u) - n * n / (2.0 * (1.0 + u) ** 2)  # A2: wall pressure, interior magnitude u, normal part n


def interior_un(d, et):
    """interior field (u, n) just inside a sharp wall from the normal flux d and the tangential field et (both continuous):
    n u / (1 + u) = d, u^2 = n^2 + et^2. Newton in n, vectorised."""
    d = np.asarray(d, float); et = np.asarray(et, float)
    n = u_in(np.maximum(d, 1e-300)) + 0.0 * et
    for _ in range(200):
        u = np.sqrt(n * n + et * et)
        f = n * u / (1 + u) - d
        fp = u / (1 + u) + n * n / (u * (1 + u) ** 2)
        dn = f / fp
        n = np.maximum(n - dn, 0.5 * d)
        if np.all(np.abs(dn) <= 1e-15 * np.maximum(n, 1e-300)): break
    return np.sqrt(n * n + et * et), n


def wall_quad_pressure(d, et, sign=+1.0, nS=4001):
    """integral of J over S from 0 to 1 at fixed (d, et) by quadrature (no closed form used). sign = -1: the mutated law
    K = 1 + S / (1 + u) with the term -S J; returns the force per unit area (negative = inward) in a0^2 / (4 pi G)."""
    S = 0.5 * (1 - np.cos(np.pi * (np.arange(nS) + 0.5) / nS))        # Chebyshev-like nodes, midpoint weights below
    wS = 0.5 * np.pi / nS * np.sin(np.pi * (np.arange(nS) + 0.5) / nS)
    n = np.full_like(S, max(d, 1e-300))
    for _ in range(300):
        u = np.sqrt(n * n + et * et)
        K = 1 - sign * S / (1 + u)
        f = K * n - d
        fp = K + sign * S * n * n / (u * (1 + u) ** 2)
        dn = f / fp
        n = np.maximum(n - dn, 1e-300)
        if np.max(np.abs(dn) / np.maximum(n, 1e-300)) < 1e-15: break
    u = np.sqrt(n * n + et * et)
    return sign * float(np.sum(wS * Jt(u)))


# ------------------------------------------------------------------ wall geometry
class Spheroid:
    """m^2 = R^2 + z^2 / q^2 = a^2; mu = cos(eccentric angle). q = 1 is the sphere."""
    kind = "spheroid"
    def __init__(self, a, q): self.a, self.q = float(a), float(q)
    def coef(self, mu):
        a, q = self.a, self.q; om = 1 - mu * mu; h2 = mu * mu + q * q * om
        return dict(A=(a / q) * h2, B=-(a / q) * (1 - q * q) * mu * om, C=(a / q) * om * (om + q * q * mu * mu),
                    RD=np.full_like(mu, q * a ** 3), Rw=a * np.sqrt(om), zw=q * a * mu, Sarea=a * a * np.sqrt(h2),
                    Xabs=a * np.sqrt(om + q * q * mu * mu), etfac=np.sqrt(om) / (a * np.sqrt(h2)),
                    Nz=a * a * mu, NR=q * a * a * np.sqrt(om), dzw=np.full_like(mu, q * a),
                    dXabs=a * mu * (q * q - 1) / np.sqrt(om + q * q * mu * mu))
    def volume(self): return 4 * math.pi / 3 * self.q * self.a ** 3
    def scaled(self, f): return Spheroid(self.a * f, self.q)


class Star:
    """star-shaped wall r = rho(mu), mu = cos(polar angle), rho a Legendre series (coefficients cl, even terms for symmetry)."""
    kind = "star"
    def __init__(self, cl): self.cl = np.asarray(cl, float)
    def rho(self, mu): return legval(mu, self.cl)
    def drho(self, mu): return legval(mu, legder(self.cl)) if len(self.cl) > 1 else np.zeros_like(mu)
    def coef(self, mu):
        r, dr = self.rho(mu), self.drho(mu); om = 1 - mu * mu; g = np.sqrt(dr * dr * om + r * r)
        return dict(A=r + om * dr * dr / r, B=om * dr, C=om * r, RD=r ** 3, Rw=r * np.sqrt(om), zw=r * mu, Sarea=r * g, Xabs=r,
                    etfac=np.sqrt(om) / g, Nz=-(r * om * dr - r * r * mu), NR=r * np.sqrt(om) * (dr * mu + r), dzw=dr * mu + r,
                    dXabs=dr)
    def volume(self):
        x, w = leggauss(200); return 2 * math.pi / 3 * float(np.sum(w * self.rho(x) ** 3))
    def scaled(self, f): return Star(self.cl * f)


# ------------------------------------------------------------------ exterior maps
def _legP(M, mu):
    """P[l, j] = P_l(mu_j), dP[l, j] = P_l'(mu_j), l = 0..M."""
    P = legvander(mu, M).T
    dP = np.zeros_like(P)
    for l in range(1, M + 1):
        c = np.zeros(l + 1); c[l] = 1.0; dP[l] = legval(mu, legder(c))
    return P, dP


def conf_lambdas(q, M, m):
    """d ln F_l / d xi on the spheroid of axis ratio q for the decaying confocal harmonics; order m = 0 (l = 0..M-1) or
    m = 1 (l = 1..M). Also returns the far-field dipole factor D1: p = (wall coefficient of l = 1) * a^2 * D1."""
    extra = 400
    if abs(q - 1.0) < 1e-12:
        if m == 0: return -(np.arange(M) + 1.0), 1.0
        return -(np.arange(1, M + 1) + 1.0), 1.0
    if q < 1:                                                        # oblate: argument i x, x = sinh xi
        x = q / math.sqrt(1 - q * q); ch = math.sqrt(1 + x * x); f2 = 1 - q * q        # f^2 / a^2
        if m == 0:
            L = M - 1 + extra; r = np.zeros(L + 2); r[L + 1] = ch - x
            for l in range(L, 0, -1): r[l] = l / ((2 * l + 1) * x + (l + 1) * r[l + 1])
            q0 = math.atan(1 / x); q1 = 1 - x * math.atan(1 / x)
            assert abs(r[1] - q1 / q0) < 1e-10 * abs(q1 / q0), "oblate m=0 ratio check"
            lam = np.array([-1 / (ch * q0)] + [l * (x - 1 / r[l]) / ch for l in range(1, M)])
            return lam, f2 / (3 * q1)
        L = M + extra; s = np.zeros(L + 2); s[L + 1] = ch - x
        for l in range(L, 0, -1): s[l] = (l + 1) / ((2 * l + 1) * x + l * s[l + 1])
        g0 = 1 / ch; g1 = ch * (math.atan(1 / x) - x / (1 + x * x))
        assert abs(s[1] - g1 / g0) < 1e-10 * abs(g1 / g0), "oblate m=1 ratio check"
        lam = np.array([(l * x - (l + 1) / s[l]) / ch for l in range(1, M + 1)])
        return lam, 2 * f2 / (3 * g1)
    z = q / math.sqrt(q * q - 1); sh = math.sqrt(z * z - 1); f2 = q * q - 1               # prolate: argument z = cosh xi
    Q0 = 0.5 * math.log((z + 1) / (z - 1)); Q1 = z * Q0 - 1
    if m == 0:
        L = M - 1 + extra; r = np.zeros(L + 2); r[L + 1] = z - sh
        for l in range(L, 0, -1): r[l] = l / ((2 * l + 1) * z - (l + 1) * r[l + 1])
        assert abs(r[1] - Q1 / Q0) < 1e-10 * abs(Q1 / Q0), "prolate m=0 ratio check"
        lam = np.array([-1 / (sh * Q0)] + [l * (z - 1 / r[l]) / sh for l in range(1, M)])
        return lam, f2 / (3 * Q1)
    L = M + extra; s = np.zeros(L + 2); s[L + 1] = z - sh
    for l in range(L, 0, -1): s[l] = (l + 1) / ((2 * l + 1) * z - l * s[l + 1])
    g0 = -1 / sh; g1 = sh * (Q0 - z / (z * z - 1))
    assert abs(s[1] - g1 / g0) < 1e-10 * abs(g1 / g0), "prolate m=1 ratio check"
    lam = np.array([(l * z - (l + 1) / s[l]) / sh for l in range(1, M + 1)])
    return lam, -2 * f2 / (3 * g1)


class Exterior:
    """outer-surface operators for one geometry (already scaled to the outer surface) on the mu nodes.
    E0, E1: wall potential (m = 0 values; m = 1 amplitudes) -> outward flux per dmu per radian at the nodes.
    dip0, dip1: row vectors giving the far-field dipole p_z, p_x from the scattered wall potential."""
    def __init__(self, geom, mu, w, kind):
        M = len(mu); self.kind = kind
        P, dP = _legP(M, mu); om = 1 - mu * mu
        T0 = ((2 * np.arange(M) + 1) / 2.0)[:, None] * P[:M] * w[None, :]            # analysis, m = 0 (exact)
        self.T0 = T0; self.P0 = P[:M]; self.dP0 = dP[:M]
        B1 = (np.sqrt(om)[None, :] * dP[1:M + 1]).T                                  # B1[j, l-1] = sqrt(1-mu^2) P_l'(mu_j)
        A1 = np.linalg.inv(B1)                                                       # analysis, m = 1 (collocation)
        if kind == "conf":
            a, q = geom.a, geom.q
            lam0, D0 = conf_lambdas(q, M, 0); lam1, D1 = conf_lambdas(q, M, 1)
            self.E0 = a * (P[:M].T * lam0[None, :]) @ T0
            self.E1 = a * (B1 * lam1[None, :]) @ A1
            self.dip0 = a * a * D0 * T0[1]; self.dip1 = a * a * D1 * A1[0]
        elif kind == "ray":
            if geom.kind != "star": raise ValueError("ray exterior needs a star-shaped wall")
            c = geom.coef(mu); r = c["Xabs"]; dr = geom.drho(mu); sc = float(np.mean(r)); x = r / sc   # basis (r / sc)^-(l+1)
            l0 = np.arange(M); U0 = x[:, None] ** (-(l0[None, :] + 1.0)) * P[:M].T
            F0 = -(l0[None, :] + 1.0) * sc * x[:, None] ** (-l0[None, :] * 1.0) * P[:M].T \
                 - (dr * om)[:, None] * x[:, None] ** (-(l0[None, :] + 1.0)) * dP[:M].T
            U0i = np.linalg.inv(U0); self.E0 = F0 @ U0i; self.dip0 = sc * sc * U0i[1]
            l1 = np.arange(1, M + 1); Pt = B1
            dPt = (np.sqrt(om)[None, :] * (mu[None, :] * dP[1:M + 1] - (l1 * (l1 + 1.0))[:, None] * P[1:M + 1])).T   # (1-mu^2) dPt/dmu
            U1 = x[:, None] ** (-(l1[None, :] + 1.0)) * Pt
            F1 = -(l1[None, :] + 1.0) * sc * x[:, None] ** (-l1[None, :] * 1.0) * Pt - dr[:, None] * x[:, None] ** (-(l1[None, :] + 1.0)) * dPt
            U1i = np.linalg.inv(U1); self.E1 = F1 @ U1i; self.dip1 = sc * sc * U1i[0]
        else:
            self.E0 = self.E1 = None


# ------------------------------------------------------------------ the bubble
class Bubble:
    def __init__(self, geom, s, M=48, ext="conf", S_of_m=None, kmode="law", Kconst=None, point=True, mass=None,
                 flux_mutate=False, law_sign=+1.0, ref="law"):
        """geom: wall geometry at m = 1. s: radial nodes ln m (increasing; last node is the outer surface, at or beyond the wall).
        S_of_m: None for a sharp wall at the last node (S = 1 everywhere inside), else a function of m (smooth wall).
        point: unit point mass at the centre (flux through the inner surface); mass: (N+1, M) cell masses (full azimuth)."""
        self.geom, self.kmode, self.Kconst, self.flux_mutate, self.law_sign = geom, kmode, Kconst, flux_mutate, law_sign
        self.s = np.asarray(s, float); self.N = len(s) - 1; self.M = M
        self.m = np.exp(self.s); self.sf = 0.5 * (self.s[1:] + self.s[:-1]); self.mf = np.exp(self.sf); self.dsf = np.diff(self.s)
        dsc = np.zeros(self.N + 1); dsc[:-1] += 0.5 * self.dsf; dsc[1:] += 0.5 * self.dsf; self.dsc = dsc
        mu, w = leggauss(M); self.mu, self.w = mu, w
        self.muf = -1.0 + np.cumsum(w)[:-1]; self.dmu = np.diff(mu)
        c = geom.coef(mu); cf = geom.coef(self.muf); self.c = c
        self.A, self.B, self.C, self.RD = c["A"], c["B"], c["C"], c["RD"]
        self.Af, self.Bf, self.Cf, self.RDf = cf["A"], cf["B"], cf["C"], cf["RD"]
        # d/dmu at nodes (3-point non-uniform inside, 2-point at the ends)
        D = np.zeros((M, M))
        for j in range(M):
            if j == 0: D[0, 0] = -1 / self.dmu[0]; D[0, 1] = 1 / self.dmu[0]
            elif j == M - 1: D[j, j - 1] = -1 / self.dmu[-1]; D[j, j] = 1 / self.dmu[-1]
            else:
                h1, h2 = self.dmu[j - 1], self.dmu[j]
                D[j, j - 1] = -h2 / (h1 * (h1 + h2)); D[j, j] = (h2 - h1) / (h1 * h2); D[j, j + 1] = h1 / (h2 * (h1 + h2))
        self.Dmu = D
        h1, h2 = self.dsf[:-1], self.dsf[1:]
        self.cm, self.c0, self.cp = -h2 / (h1 * (h1 + h2)), (h2 - h1) / (h1 * h2), h1 / (h2 * (h1 + h2))
        if S_of_m is None:
            self.Sn = np.ones(self.N + 1); self.Sf = np.ones(self.N); self.smooth = False
        else:
            self.Sn = S_of_m(self.m); self.Sf = S_of_m(self.mf); self.smooth = True
        self.mout = float(self.m[-1])
        self.gout = geom.scaled(self.mout) if self.mout != 1.0 else geom
        self.cout = self.gout.coef(mu)
        self.extkind = ext
        self.ext = Exterior(self.gout, mu, w, ext) if ext in ("conf", "ray") else None
        mono = w * c["RD"] / c["Xabs"] ** 3; mono *= 2.0 / mono.sum()              # monopole flux of unit mass through any m-surface
        self.mono = mono
        self.Fin = mono.copy() if point else np.zeros(M)
        self.mass = np.zeros((self.N + 1, M)) if mass is None else np.asarray(mass, float)
        self.vol = (self.RD * w)[None, :] * (np.exp(3 * np.concatenate([self.sf, [self.s[-1]]]))
                                              - np.exp(3 * np.concatenate([[self.s[0]], self.sf])))[:, None] / 3.0   # per radian
        # reference: the law's spherical solution around a unit point mass, differentiated analytically; the unknown is
        # psi = Phi - Phi_ref. The reference's discrete residual is exactly zero inside (its field is radial), so the grid
        # only has to resolve what the wall and an extended source add.
        self.ref = ref
        def refd(m_, cc):
            r = m_[:, None] * cc["Xabs"][None, :]; g = u_in(1.0 / (r * r))
            return g * r, g * m_[:, None] * cc["dXabs"][None, :]
        if ref == "law":
            self.Rs_f, self.Rm_f = refd(self.mf, c); self.Rs_mf, self.Rm_mf = refd(self.m, cf); self.Rs_n, self.Rm_n = refd(self.m, c)
            self.Pref = phi_law(self.m[:, None] * c["Xabs"][None, :])
        else:
            z = np.zeros((self.N, M)); zf = np.zeros((self.N + 1, M - 1)); zn = np.zeros((self.N + 1, M))
            self.Rs_f, self.Rm_f, self.Rs_mf, self.Rm_mf, self.Rs_n, self.Rm_n, self.Pref = z, z, zf, zf, zn, zn, zn
        self.Phi = None

    def total(self, Phi=None): return (self.Phi if Phi is None else Phi) + self.Pref

    # -- discrete operators
    def _Ds(self, Phi):
        Ps = np.empty_like(Phi)
        Ps[1:-1] = self.cm[:, None] * Phi[:-2] + self.c0[:, None] * Phi[1:-1] + self.cp[:, None] * Phi[2:]
        Ps[0] = (Phi[1] - Phi[0]) / self.dsf[0]; Ps[-1] = (Phi[-1] - Phi[-2]) / self.dsf[-1]
        return Ps

    def _K(self, S, u):
        if self.kmode == "lin": return self.Kconst + 0 * u
        if self.kmode == "newton": return 1.0 + 0 * u
        return 1 - self.law_sign * S / (1 + u)

    def faces(self, Phi, newton=False):
        """fluxes through radial faces Fs (N, M) and mu faces Fm (N+1, M-1), per radian; with newton=True, K = 1 (grad Phi)."""
        dPs = (Phi[1:] - Phi[:-1]) / self.dsf[:, None] + self.Rs_f
        Pm = Phi @ self.Dmu.T
        dPm = 0.5 * (Pm[1:] + Pm[:-1]) + self.Rm_f; mf = self.mf[:, None]
        if newton: K = 1.0
        else:
            u = np.sqrt((self.A * dPs ** 2 - 2 * self.B * dPs * dPm + self.C * dPm ** 2) / (mf ** 2 * self.RD))
            K = self._K(self.Sf[:, None], u)
        Fs = mf * K * (self.A * dPs - self.B * dPm) * self.w
        dPmf = (Phi[:, 1:] - Phi[:, :-1]) / self.dmu + self.Rm_mf
        Ps = self._Ds(Phi); dPsf = 0.5 * (Ps[:, 1:] + Ps[:, :-1]) + self.Rs_mf; mn = self.m[:, None]
        if newton: Kf = 1.0
        else:
            uf = np.sqrt((self.Af * dPsf ** 2 - 2 * self.Bf * dPsf * dPmf + self.Cf * dPmf ** 2) / (mn ** 2 * self.RDf))
            Kf = self._K(self.Sn[:, None], uf)
        Fm = mn * Kf * (-self.Bf * dPsf + self.Cf * dPmf) * self.dsc[:, None]
        return Fs, Fm

    def node_u(self, Phi):
        Ps = self._Ds(Phi) + self.Rs_n; Pm = Phi @ self.Dmu.T + self.Rm_n
        return np.sqrt((self.A * Ps ** 2 - 2 * self.B * Ps * Pm + self.C * Pm ** 2) / (self.m[:, None] ** 2 * self.RD))

    def Fext(self, Phi):
        if self.ext is None: return self.mono * (self.mass.sum() + (1.0 if self.Fin.sum() > 0 else 0.0))
        F = self.w * (self.ext.E0 @ (Phi[-1] + self.Pref[-1]))
        if self.flux_mutate:                                           # M2: dPhi/dn continuous instead of K dPhi/dn
            F = F * self._K(self.Sn[-1], self.node_u(Phi)[-1])
        return F

    def resid_int(self, Phi):
        Fs, Fm = self.faces(Phi)
        R = np.zeros(Phi.shape, dtype=Phi.dtype)
        R[:-1] += Fs; R[1:] -= Fs; R[:, :-1] += Fm; R[:, 1:] -= Fm
        R[0] -= self.Fin; R -= 2 * self.mass
        if self.ext is None: R[-1, 0] += Phi[-1, 0]                      # prescribed outer flux: pin the free constant
        return R

    def resid(self, Phi):
        R = self.resid_int(Phi); R[-1] += self.Fext(Phi); return R

    def jac_int(self, Phi, extra=None):
        """complex-step Jacobian of resid_int (plus an optional extra local term), CSC."""
        N1, M = self.N + 1, self.M; h = 1e-30
        I, Jn = np.meshgrid(np.arange(N1), np.arange(M), indexing="ij")
        rows, cols, vals = [], [], []
        for ci in range(3):
            for cj in range(3):
                pert = np.zeros((N1, M)); pert[ci::3, cj::3] = 1.0
                Z = Phi.astype(complex) + 1j * h * pert
                dR = (self.resid_int(Z) if extra is None else extra(Z)).imag / h
                di = (ci - I + 1) % 3 - 1; dj = (cj - Jn + 1) % 3 - 1
                ic, jc = I + di, Jn + dj
                ok = (ic >= 0) & (ic < N1) & (jc >= 0) & (jc < M) & (dR != 0)
                rows.append((I * M + Jn)[ok]); cols.append((ic * M + jc)[ok]); vals.append(dR[ok])
        n = N1 * M
        return coo_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(n, n)).tocsc()

    def _ext_block(self, E, mutK=None):
        N1, M = self.N + 1, self.M; n = N1 * M; base = self.N * M
        j, k = np.meshgrid(np.arange(M), np.arange(M), indexing="ij")
        v = self.w[:, None] * E
        if mutK is not None: v = mutK[:, None] * v
        return coo_matrix((v.ravel(), ((base + j).ravel(), (base + k).ravel())), shape=(n, n)).tocsc()

    def jacobian(self, Phi):
        if self.ext is None: return self.jac_int(Phi)
        if self.flux_mutate:                                            # numerical: the mutated exterior term depends on Phi locally too
            return self.jac_int(Phi, extra=lambda Z: self.resid(Z) - self._lin_ext(Z)) + self._ext_block(
                self.ext.E0, self._K(self.Sn[-1], self.node_u(Phi)[-1]).real)
        return self.jac_int(Phi) + self._ext_block(self.ext.E0)

    def _lin_ext(self, Z):
        R = np.zeros(Z.shape, dtype=Z.dtype)
        R[-1] = self._K(self.Sn[-1], self.node_u(Z.real)[-1]) * self.w * (self.ext.E0 @ (Z[-1] + self.Pref[-1])); return R

    def solve(self, Phi0, tol=1e-11, itmax=80, verbose=False):
        Phi = np.array(Phi0, float); R = self.resid(Phi); r0 = np.max(np.abs(R)); ok = False
        for it in range(itmax):
            if r0 < tol: ok = True; break
            J = self.jacobian(Phi)
            d = splu(J).solve(-R.ravel()).reshape(Phi.shape)
            t = 1.0
            while True:
                Pn = Phi + t * d; Rn = self.resid(Pn); rn = np.max(np.abs(Rn))
                if np.isfinite(rn) and (rn < r0 * (1 - 1e-4 * t) or t < 1e-6): break
                t *= 0.5
            if verbose: print(f"    newton {it}: |R| {r0:.3e} -> {rn:.3e} (t {t:.3g})", flush=True)
            Phi, R, r0 = Pn, Rn, rn
        if r0 < tol: ok = True
        self.Phi, self.converged, self.res = Phi, ok, r0
        return Phi, ok

    # -- wall and field diagnostics
    def wall(self, mutate_W=False):
        """sharp-wall quantities on the mu nodes (requires a sharp wall at the outer node)."""
        Phi = self.Phi; c = self.cout; ex = self.ext; w = self.w
        Pw = Phi[-1] + self.Pref[-1]
        F = self.w * (ex.E0 @ Pw)                                         # exterior flux per cell, per radian (= normal flux of grad Phi outside)
        d = F / w / c["Sarea"]
        dPhidmu = (ex.dP0.T @ (ex.T0 @ Pw))
        et = c["etfac"] * dPhidmu
        if self.flux_mutate: dflux = d * self._K(1.0, self.node_u(Phi)[-1])
        else: dflux = d
        u, n = interior_un(np.abs(dflux), et)
        if self.law_sign < 0:
            p = np.array([wall_quad_pressure(abs(dj), abs(ej), sign=-1.0, nS=801) for dj, ej in zip(dflux, et)])
        else:
            p = Wsph(u) if mutate_W else Wg(u, n)
        gout = np.sqrt(d * d + et * et)
        Fn = 0.5 * float(np.sum(p * c["Sarea"] * w)); Dil = 0.5 * float(np.sum(p * c["RD"] * w))
        Gw = 0.5 * float(np.sum(gout * c["Sarea"] * w))
        return dict(d=d, et=et, u=u, n=n, p=p, gout=gout, Fn=Fn, Dil=Dil, Gamma_w=Gw, col_max=float(np.max(p / gout)),
                    M_ext=0.5 * float(F.sum()), u_node=self.node_u(Phi)[-1])

    def volume_force(self):
        """smooth wall: F_n and the dilation moment from the integral of J |grad S| (the force density on the carrier)."""
        Phi = self.Phi
        dPs = (Phi[1:] - Phi[:-1]) / self.dsf[:, None] + self.Rs_f; Pm = Phi @ self.Dmu.T; dPm = 0.5 * (Pm[1:] + Pm[:-1]) + self.Rm_f
        u = np.sqrt((self.A * dPs ** 2 - 2 * self.B * dPs * dPm + self.C * dPm ** 2) / (self.mf[:, None] ** 2 * self.RD))
        dS = (self.Sn[:-1] - self.Sn[1:])[:, None]
        Jv = self.law_sign * Jt(u) * dS
        Fn = 0.5 * float(np.sum(Jv * self.mf[:, None] ** 2 * self.c["Sarea"] * self.w))
        Dil = 0.5 * float(np.sum(Jv * self.mf[:, None] ** 3 * self.RD * self.w))
        return Fn, Dil

    def lagrangian(self):
        """L in units a0 M_b r_M, up to a wall-independent constant: interior field and S J terms by cell quadrature, the
        exterior field energy as a surface term, and the source term on the inner surface."""
        Phi = self.Phi; u = self.node_u(Phi)
        dens = -0.5 * u * u + self.law_sign * self.Sn[:, None] * Jt(u)
        Lin = 0.5 * float(np.sum(dens * self.vol))
        Fe = self.Fext(Phi); Pt = Phi + self.Pref
        return Lin + 0.25 * float(np.sum(Pt[-1] * Fe)) - 0.5 * float(np.sum(Pt[0] * self.Fin)) - float(np.sum(self.mass * Pt))

    def eff_mass(self, nsub=4):
        """effective mass (baryons + phantom + wall layer) as thin shells: returns (radii, masses, cos theta, central mass).
        Each cell's mass is spread over nsub sub-shells across its extent in s. For a sharp wall the wall half-cell's phantom
        mass and the compensating layer are kept apart: the layer sits on the wall itself."""
        Phi = self.Phi; Fs, Fm = self.faces(Phi, newton=True)
        G = np.zeros(Phi.shape); G[:-1] += Fs; G[1:] -= Fs; G[:, :-1] += Fm; G[:, 1:] -= Fm
        K0 = self._K(self.Sn[0], self.node_u(Phi)[0])
        G[0] -= self.Fin / K0
        Fe = self.Fext(Phi); layer = None
        if self.smooth or self.ext is None:
            Kn = self._K(self.Sn[-1], self.node_u(Phi)[-1]); G[-1] += Fe / Kn
        else:
            wq = self.wall(); ratio = wq["n"] / np.maximum(np.abs(wq["d"]), 1e-300)   # 1 / K just inside the wall
            G[-1] += Fe * ratio; layer = 0.5 * Fe * (1 - ratio)
        Meff = 0.5 * G
        lo = np.concatenate([[self.s[0]], self.sf]); hi = np.concatenate([self.sf, [self.s[-1]]])
        X = self.c["Xabs"][None, :]; cz = (self.c["zw"] / self.c["Xabs"])[None, :]
        rr, mm, cc = [], [], []
        for k in range(nsub):
            sk = lo + (k + 0.5) / nsub * (hi - lo)
            rr.append((np.exp(sk)[:, None] * X).ravel()); mm.append((Meff / nsub).ravel()); cc.append((cz + 0 * Meff).ravel())
        if layer is not None:
            rr.append((self.m[-1] * X).ravel()); mm.append(layer); cc.append(cz.ravel())
        m_centre = 0.5 * float(np.sum(self.Fin / K0))
        return np.concatenate(rr), np.concatenate(mm), np.concatenate(cc), m_centre

    def inplane(self):
        """radial field in the plane, g_R(R) = (dPhi/ds) / R at mu = 0, by even quadratic interpolation of the two node pairs
        nearest the plane. Returns R (physical) and g_R on the radial nodes."""
        M = self.M; ja, jb = M // 2, M // 2 + 1
        mua, mub = self.mu[ja], self.mu[jb]
        Phi0 = (mub ** 2 * self.Phi[:, ja] - mua ** 2 * self.Phi[:, jb]) / (mub ** 2 - mua ** 2)
        Ps = np.empty_like(Phi0)
        Ps[1:-1] = self.cm * Phi0[:-2] + self.c0 * Phi0[1:-1] + self.cp * Phi0[2:]
        Ps[0] = (Phi0[1] - Phi0[0]) / self.dsf[0]; Ps[-1] = (Phi0[-1] - Phi0[-2]) / self.dsf[-1]
        R = self.m * float(self.geom.coef(np.array([0.0]))["Rw"][0])
        if self.ref == "law": return R, Ps / R + u_in(1.0 / (R * R))
        return R, Ps / R

    # -- linear responses in a uniform external field (unit strength)
    def response(self, order):
        """tangent problem of the converged state for a unit external field along the axis (order 0) or across it (order 1).
        Returns the far-field dipole p (Phi_scat -> p cos(angle) / r^2) and the wall perturbation."""
        Phi = self.Phi; ex = self.ext; c = self.cout; w = self.w; N1, M = self.N + 1, self.M
        Jint = self.jac_int(Phi)
        if order == 0:
            E = ex.E0; inc_pot = -c["zw"]; inc_flux = -c["Nz"]; dip = ex.dip0
        else:
            E = ex.E1; inc_pot = -c["Rw"]; inc_flux = -c["NR"]; dip = ex.dip1
            if self.kmode == "lin": Kn = np.full((N1, M), float(self.Kconst))
            else: Kn = self._K(self.Sn[:, None], self.node_u(Phi))
            Gphi = (self.m * self.dsc)[:, None] * (w * self.RD / self.c["Rw"] ** 2)[None, :]
            Jint = Jint - csc_matrix((np.ravel(Kn * Gphi), (np.arange(N1 * M), np.arange(N1 * M))), shape=(N1 * M, N1 * M))
        Jm = Jint + self._ext_block(E)
        rhs = np.zeros((N1, M)); rhs[-1] = -w * (inc_flux - E @ inc_pot)
        psi = splu(Jm.tocsc()).solve(rhs.ravel()).reshape(N1, M)
        scat = psi[-1] - inc_pot
        return float(dip @ scat), psi


# ------------------------------------------------------------------ grids, sources, references
def s_grid(r0_over_a, ds):
    """uniform nodes in s = ln m from ln(r0 / a) to 0 (the sharp wall)."""
    N = max(8, int(math.ceil(-math.log(r0_over_a) / ds)))
    return np.linspace(math.log(r0_over_a), 0.0, N + 1)


def s_grid_smooth(r0_over_a, ds, wdt, nfine=10.0, mlim=12.0, ratio=1.15, lattice0=None):
    """nodes for a smooth wall of width wdt (in m): spacing wdt / nfine for |m - 1| <= mlim * wdt, grading geometrically (ratio)
    inward to the bulk spacing ds; bulk nodes on the lattice ln(r0 / a) + k ds when lattice0 is None, else lattice0 + k ds."""
    s_out = math.log(1 + mlim * wdt); s_in = math.log(1 - mlim * wdt); dsw = wdt / nfine
    fine = list(np.arange(s_out, s_in - 1e-12, -dsw))
    h = dsw; x = fine[-1]; grade = []
    while h * ratio < ds:
        h *= ratio; x -= h; grade.append(x)
    s0 = math.log(r0_over_a) if lattice0 is None else lattice0
    k = int(math.floor((x - 0.5 * ds - s0) / ds))
    bulk = [s0 + i * ds for i in range(0, k + 1)]
    while bulk and bulk[0] < math.log(r0_over_a) - 1e-9: bulk.pop(0)
    return np.array(bulk + grade[::-1] + fine[::-1])


def phi_law(r):
    """potential of the law around a unit point mass (law everywhere), up to a constant."""
    r = np.asarray(r, float); return -1 / (2 * r) - np.sqrt(1 + 4 * r * r) / (2 * r) + np.arcsinh(2 * r)


def initial_guess(b):
    if b.ref == "law": return np.zeros((b.N + 1, b.M))
    r = b.m[:, None] * b.c["Xabs"][None, :]
    return phi_law(r)


def _mu_of_z(geom, zeta):
    """mu on the wall curve with z_w(mu) = zeta (zeta within the curve's range)."""
    if geom.kind == "spheroid": return np.clip(zeta / (geom.q * geom.a), -1.0, 1.0)
    mu = np.clip(zeta / geom.rho(np.zeros_like(zeta)), -1.0, 1.0)
    for _ in range(60):
        r, dr = geom.rho(mu), geom.drho(mu)
        mu = np.clip(mu - (r * mu - zeta) / (dr * mu + r), -1.0, 1.0)
    return mu


def expdisc_mass(b, Rd, zd, rtrunc_m=1.0, nsub=8):
    """cell masses (full azimuth) of rho ~ exp(-R / Rd) sech^2(z / zd), truncated at m = rtrunc_m and renormalised to unit mass.
    The mu integral of each cell is taken in t = tanh(z / zd), in which the vertical profile is exact, so a disc thinner than a
    cell is deposited with the right radial distribution. Returns the masses and the fraction of the disc left outside."""
    N1, M = b.N + 1, b.M; g = b.geom
    se = np.concatenate([[b.s[0]], b.sf, [b.s[-1]]]); mue = np.concatenate([[-1.0], b.muf, [1.0]])
    xs, ws = leggauss(nsub)
    zwe = g.coef(mue)["zw"]
    mass = np.zeros((N1, M))
    for a in range(nsub):
        sm = 0.5 * (se[1:] + se[:-1]) + 0.5 * (se[1:] - se[:-1]) * xs[a]; wsm = 0.5 * (se[1:] - se[:-1]) * ws[a]
        m_ = np.exp(sm)[:, None]                                            # (N1, 1)
        tlo = np.tanh(m_ * zwe[None, :-1] / zd); thi = np.tanh(m_ * zwe[None, 1:] / zd)   # (N1, M)
        for bq in range(nsub):
            t = 0.5 * (thi + tlo) + 0.5 * (thi - tlo) * xs[bq]; wt = 0.5 * (thi - tlo) * ws[bq]
            z = zd * np.arctanh(np.clip(t, -1 + 1e-16, 1 - 1e-16))
            mu = _mu_of_z(g, (z / m_).ravel()).reshape(z.shape)
            c = g.coef(mu.ravel()); Rw = c["Rw"].reshape(z.shape); RDv = c["RD"].reshape(z.shape)
            dzw = c["dzw"].reshape(z.shape)
            f = RDv * m_ ** 2 * zd * np.exp(-m_ * Rw / Rd) / dzw
            mass += 2 * math.pi * (wsm[:, None] * (m_ <= rtrunc_m)) * wt * f
    tot_exact = 4 * math.pi * Rd * Rd * zd                                 # 2 pi Rd^2 * 2 zd
    inside = mass.sum()
    return mass / inside, 1.0 - inside / tot_exact


def kuzmin_mass(b, aK):
    """razor-thin Kuzmin disc of unit mass and scale aK, deposited in the two cell rows adjacent to the plane (spherical grid)."""
    N1, M = b.N + 1, b.M
    me = np.exp(np.concatenate([[b.s[0]], b.sf, [b.s[-1]]])) * float(b.geom.coef(np.array([0.0]))["Rw"][0])
    Mlt = 1 - aK / np.sqrt(me * me + aK * aK); Mlt[0] = 0.0
    ring = np.diff(Mlt)
    mass = np.zeros((N1, M)); mass[:, M // 2 - 1] = 0.5 * ring; mass[:, M // 2] = 0.5 * ring
    return mass, float(1 - Mlt[-1])


# ------------------------------------------------------------------ lensing of a spherically averaged effective mass
def mcyl(Rp, r_sh, m_sh, m_centre=0.0):
    """projected mass inside the cylinder of radius Rp for thin spherical shells (radii r_sh, masses m_sh) plus a central point."""
    Rp = np.atleast_1d(Rp); out = np.full(Rp.shape, float(m_centre))
    for k, R in enumerate(Rp):
        x = np.minimum(R / r_sh, 1.0)
        out[k] += float(np.sum(m_sh * (1 - np.sqrt(1 - x * x))))
    return out


def delta_sigma(edges, r_sh, m_sh, m_centre=0.0):
    """Delta Sigma in the annuli between consecutive edges: mean surface density inside the geometric mid radius minus the
    annulus mean (units M_b / r_M^2). Returns mid radii and the signal."""
    mid = np.sqrt(edges[1:] * edges[:-1])
    Me = mcyl(edges, r_sh, m_sh, m_centre); Mm = mcyl(mid, r_sh, m_sh, m_centre)
    sig = np.diff(Me) / (math.pi * (edges[1:] ** 2 - edges[:-1] ** 2))
    return mid, Mm / (math.pi * mid * mid) - sig


def law_shells(rmax, n_per_dex=400, rmin=1e-6):
    """thin shells of the law's effective mass around a unit point mass, nu(1 / r^2), from rmin to rmax."""
    e = 10 ** np.arange(math.log10(rmin), math.log10(rmax) + 1e-12, 1.0 / n_per_dex)
    Me = nu(1 / e ** 2)
    return np.sqrt(e[1:] * e[:-1]), np.diff(Me), float(Me[0])


def sphere_shells(Rs, n_per_dex=400, rmin=1e-6):
    """a spherical law-on region of radius Rs around a unit point mass: nu inside, the compensating layer at the wall."""
    e = 10 ** np.arange(math.log10(rmin), math.log10(Rs) + 1e-12, 1.0 / n_per_dex); e[-1] = Rs
    Me = nu(1 / e ** 2)
    r = np.concatenate([np.sqrt(e[1:] * e[:-1]), [Rs]]); m = np.concatenate([np.diff(Me), [1.0 - Me[-1]]])
    return r, m, float(Me[0])


def reach(mid, ratio, tol=0.10):
    """largest radius out to which |ratio - 1| <= tol holds at every smaller radius (log-linear interpolation of the crossing)."""
    bad = np.where(np.abs(ratio - 1) > tol)[0]
    if len(bad) == 0: return float(mid[-1])
    k = int(bad[0])
    if k == 0: return float(mid[0])
    e0, e1 = abs(ratio[k - 1] - 1), abs(ratio[k] - 1)
    t = (tol - e0) / (e1 - e0)
    return float(math.exp(math.log(mid[k - 1]) + t * (math.log(mid[k]) - math.log(mid[k - 1]))))


# ------------------------------------------------------------------ SWT1's polarizability of a sphere (transcribed from swt1.py)
def alpha_law_y(yw):
    """SWT1's alpha_law for a spherical law-on region around point baryons with y at the wall = yw (units r_M, a0)."""
    from scipy.integrate import solve_ivp
    R = 1 / math.sqrt(yw)
    def yy(s): return 1.0 / math.exp(2 * s)
    def uu(s):
        y = yy(s); return 0.5 * y + math.sqrt(0.25 * y * y + y)
    def mur(s):
        u = uu(s); return u * (2 + u) / (1 + u) ** 2
    def mut(s):
        u = uu(s); return u / (1 + u)
    def dlnmur(s):
        y = yy(s); u = uu(s)
        dudy = 0.5 + (0.5 * y + 1.0) / (2.0 * math.sqrt(0.25 * y * y + y))
        return (2.0 / (1 + u) ** 3) * dudy * (-2.0 * y) / mur(s)
    r0 = math.sqrt(1.0 / 1e8)
    if R <= r0: return 0.0
    def rhs(s, L): return [-L[0] ** 2 - (1.0 + dlnmur(s)) * L[0] + 2.0 * mut(s) / mur(s)]
    so = solve_ivp(rhs, (math.log(r0), math.log(R)), [1.0], rtol=1e-10, atol=1e-12, method="LSODA")
    Lam = mur(math.log(R)) * so.y[0, -1]
    return (Lam - 1.0) / (Lam + 2.0)
