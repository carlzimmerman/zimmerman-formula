"""Static cubic-galileon solver used by FA1 / I6 (criteria 062648e489).
Equation, scaled (phi = lambda pi, S_n = rho / rho_max, eps = 1/sqrt(k 8 pi G rho_max), k = r_c^2/(3 c^2)):
    eps lap(phi) + [(lap phi)^2 - phi_ij phi_ij] = S_n
Spherical: eps r^2 phi' + 2 r phi'^2 = Q(r) = int_0^r <S_n>_shell r'^2 dr'.
Axisymmetric (R, z >= 0), mirror symmetry in R and z, stretched grid R = L sinh(alpha u)/sinh(alpha), Newton with a
coloured finite-difference Jacobian and a sparse direct solve. Selector s = 3 sqrt(3) det H / |H|^3.
kappa = 1/2 FITTED; not theory closed."""
import math
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spl
from scipy.interpolate import RegularGridInterpolator
S3 = 3.0 * math.sqrt(3.0)

def s_from_n(n):
    """spherical: eigenvalues y (n, 1, 1)"""
    n = np.asarray(n, float); return S3 * n / (n * n + 2.0) ** 1.5

def s_from_eigs(a, b, c):
    det = a * b * c; nrm = np.sqrt(a * a + b * b + c * c); return np.where(nrm > 0, S3 * det / np.maximum(nrm, 1e-300) ** 3, 0.0)

def dphi_sph(r, Q, eps):
    """phi' from eps r^2 phi' + 2 r phi'^2 = Q"""
    r = np.asarray(r, float); Q = np.asarray(Q, float)
    return (-eps * r * r + np.sqrt(eps * eps * r ** 4 + 8.0 * r * Q)) / (4.0 * r)

def shell_Q(rho_fn, r, nmu=400):
    """Q(r) = int_0^r r'^2 <S>_shell dr' for an axisymmetric rho_fn(R, z) (already normalised), r a sorted array starting > 0"""
    mu = (np.arange(nmu) + 0.5) / nmu
    rr = np.concatenate([[0.0], r]); sh = np.array([np.mean(rho_fn(x * np.sqrt(1 - mu * mu), x * mu)) for x in r])
    f = np.concatenate([[0.0], sh * r * r]); return np.cumsum(0.5 * (f[1:] + f[:-1]) * np.diff(rr))

class Grid:
    def __init__(self, N, L, alpha):
        self.N, self.L, self.alpha = N, L, alpha; self.du = 1.0 / N
        u = np.arange(N + 1) / N; self.u = u; sa = math.sinh(alpha)
        self.x = L * np.sinh(alpha * u) / sa; self.f1 = L * alpha * np.cosh(alpha * u) / sa; self.f2 = L * alpha ** 2 * np.sinh(alpha * u) / sa
    def u_of(self, x): return np.arcsinh(np.asarray(x) * math.sinh(self.alpha) / self.L) / self.alpha

def derivs(g, phi):
    """Hessian pieces at unknown nodes (0..N-1)^2 from the full (N+1)^2 phi with mirror ghosts"""
    N, du = g.N, g.du
    P = np.empty((N + 2, N + 2)); P[1:, 1:] = phi; P[0, 1:] = phi[1, :]; P[1:, 0] = phi[:, 1]; P[0, 0] = phi[1, 1]
    c = P[1:N + 1, 1:N + 1]; e = P[2:N + 2, 1:N + 1]; w = P[0:N, 1:N + 1]; n = P[1:N + 1, 2:N + 2]; s = P[1:N + 1, 0:N]
    ne = P[2:N + 2, 2:N + 2]; nw = P[0:N, 2:N + 2]; se = P[2:N + 2, 0:N]; sw = P[0:N, 0:N]
    pu = (e - w) / (2 * du); puu = (e - 2 * c + w) / du ** 2; pv = (n - s) / (2 * du); pvv = (n - 2 * c + s) / du ** 2; puv = (ne - se - nw + sw) / (4 * du * du)
    F1 = g.f1[:N, None]; F2 = g.f2[:N, None]; G1 = g.f1[None, :N]; G2 = g.f2[None, :N]
    pR = pu / F1; pRR = (puu - F2 / F1 * pu) / F1 ** 2; pzz = (pvv - G2 / G1 * pv) / G1 ** 2; pRz = puv / (F1 * G1)
    R = g.x[:N, None] + 0 * pR; lam = np.where(R > 0, pR / np.where(R > 0, R, 1.0), pRR)
    return pRR, pzz, pRz, lam

def residual(g, phi, S, eps):
    pRR, pzz, pRz, lam = derivs(g, phi); lap = pRR + lam + pzz; H2 = pRR ** 2 + pzz ** 2 + 2 * pRz ** 2 + lam ** 2
    return eps * lap + (lap * lap - H2) - S

def selector(g, phi):
    pRR, pzz, pRz, lam = derivs(g, phi)
    tr2 = pRR + pzz; dt2 = pRR * pzz - pRz ** 2; disc = np.sqrt(np.maximum(tr2 ** 2 / 4 - dt2, 0))
    return s_from_eigs(tr2 / 2 + disc, tr2 / 2 - disc, lam)

def _col(I, a, N):
    """for rows I, the unknown index in {I-1, I, I+1} (mirror -1 -> 1) with index % 3 == a; -1 if none (or boundary)"""
    out = np.full(I.shape, -1)
    for d in (-1, 0, 1):
        c = I + d; c = np.where(c < 0, -c, c); ok = (c % 3 == a) & (c < N) & (out < 0); out = np.where(ok, c, out)
    return out

def solve(g, S, eps, phi0, tol=1e-10, maxit=60, log=None):
    N = g.N; phi = phi0.copy(); I, J = np.meshgrid(np.arange(N), np.arange(N), indexing="ij"); rows = (I * N + J).ravel()
    r0 = residual(g, phi, S, eps); hist = [float(np.max(np.abs(r0)))]
    for it in range(maxit):
        if hist[-1] < tol: break
        h = 1e-3 * (1.0 + np.abs(phi[:N, :N])); data, ri, ci = [], [], []
        for a in range(3):
            for b in range(3):
                m = (I % 3 == a) & (J % 3 == b); pp = phi.copy(); pp[:N, :N] += np.where(m, h, 0.0); pm = phi.copy(); pm[:N, :N] -= np.where(m, h, 0.0)
                dr = 0.5 * (residual(g, pp, S, eps) - residual(g, pm, S, eps))   # exact: the residual is quadratic, one perturbed node per stencil
                ic, jc = _col(I, a, N), _col(J, b, N); ok = (ic >= 0) & (jc >= 0)
                data.append((dr[ok] / h[ic[ok], jc[ok]])); ri.append((I[ok] * N + J[ok])); ci.append(ic[ok] * N + jc[ok])
        Jm = sp.csc_matrix((np.concatenate(data), (np.concatenate(ri), np.concatenate(ci))), shape=(N * N, N * N))
        dphi = spl.spsolve(Jm, -r0.ravel()).reshape(N, N); step = 1.0
        while True:
            pt = phi.copy(); pt[:N, :N] += step * dphi; rt = residual(g, pt, S, eps); m = float(np.max(np.abs(rt)))
            if np.isfinite(m) and (m < hist[-1] or step < 1e-3): break
            step *= 0.5
        phi, r0 = pt, rt; hist.append(m)
        if log: log(f"      newton {it + 1}: max|res| {m:.2e} step {step:.3g}")
    return phi, hist

def spherical_guess(g, rho_fn, eps):
    """phi from the shell-averaged spherical solution, on all nodes (boundary included)"""
    rmax = math.hypot(g.L, g.L) * 1.001; rq = np.geomspace(g.x[1] * 1e-2, rmax, 4000)
    Q = shell_Q(rho_fn, rq); dp = dphi_sph(rq, Q, eps)
    ph = np.concatenate([[0.0], np.cumsum(0.5 * (dp[1:] + dp[:-1]) * np.diff(rq))]) + dp[0] * rq[0]
    Rn, Zn = np.meshgrid(g.x, g.x, indexing="ij"); return np.interp(np.hypot(Rn, Zn), rq, ph), (rq, Q)

def interp_s(g, sgrid):
    N = g.N; it = RegularGridInterpolator((g.u[:N], g.u[:N]), sgrid, bounds_error=False, fill_value=np.nan)
    return lambda R, z: it(np.stack([g.u_of(R), g.u_of(z)], axis=-1))

def shell_W(si, r, s_c, nmu=48, sign=1.0):
    mu = (np.arange(nmu) + 0.5) / nmu; v = sign * si(r * np.sqrt(1 - mu * mu), r * mu); return float(np.mean(v >= s_c))

def W_enc(si, R, s_c, nr=48, sign=1.0):
    rs = R * (np.arange(nr) + 0.5) / nr; return float(np.mean([shell_W(si, x, s_c, sign=sign) for x in rs]))
