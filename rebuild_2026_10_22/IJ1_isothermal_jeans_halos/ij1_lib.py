"""IJ1 isothermal-Jeans halo solver (frozen criteria 46979ae8db, section 0). Units: kpc, Msun, km/s.

Inside r1 the cold dark energy is isothermal (dispersion sigma0) in its own plus the baryons' potential; outside r1 it is
an NFW halo; r1 is where rho_NFW(r1) s(v) v t = 1 with s v = svK sigma0^(1-n). Matching rho and M at r1 fixes (rho0, sigma0).
Branch rule: the lowest-rho0 root of the no-baryon (Lane-Emden) problem, continued in the baryon strength lambda 0 -> 1
(8 equal steps) by damped 2-D Newton in (ln sigma0, ln rho0). Everything is vectorised over lanes (one lane = one system).
"""
import math
import numpy as np
from scipy.integrate import solve_ivp

GK = 4.30091e-6          # kpc (km/s)^2 / Msun
FOURPI = 4 * math.pi
NU = 400                 # RK4 steps in u = ln(r/r1)
UMIN = math.log(1e-5)
LAM_STEPS = tuple((k + 1) / 8 for k in range(8))
SIG_GRID = np.linspace(math.log(0.3), math.log(1e4), 600)


def lane_emden(n=30000, lo=-4, hi=8):
    """(xi, psi, psi') for the isothermal sphere, IC1's ODE and settings."""
    xi = np.logspace(lo, hi, n)
    s = solve_ivp(lambda t, y: [y[1], math.exp(-y[0]) - 2 * y[1] / t], (xi[0], xi[-1]), [xi[0] ** 2 / 6, xi[0] / 3],
                  t_eval=xi, rtol=1e-11, atol=1e-14, method="LSODA")
    return xi, s.y[0], s.y[1]


XI, PSI, DPSI = lane_emden()
LXI = np.log(XI)
HX = np.exp(PSI) * DPSI / XI                   # M / (4 pi rho r^3) along the isothermal sphere
_j0 = int(np.searchsorted(XI, 1.0))
HMAXI = _j0 + int(np.argmax(np.diff(HX[_j0:]) < 0))   # first local maximum (xi > 1): end of the cored branch


def xi_of_h(hv):
    """first-branch inverse of HX; nan outside [1/3, max]."""
    return np.exp(np.interp(hv, HX[:HMAXI + 1], LXI[:HMAXI + 1], left=np.nan, right=np.nan))


def psi_of(xi):
    return np.interp(np.log(xi), LXI, PSI)


mN = lambda x: np.log1p(x) - x / (1 + x)


def r1_nfw(rho1, rs, rhos):
    """root of rhos / (x (1+x)^2) = rho1 (Newton in ln x)."""
    y = rhos / rho1
    lx = np.where(y > 1, np.log(np.maximum(y, 1e-300)) / 3, np.log(np.maximum(y, 1e-300)))
    for _ in range(60):
        x = np.exp(lx); lx = lx - (lx + 2 * np.log1p(x) - np.log(y)) / (1 + 2 * x / (1 + x))
    return np.exp(lx) * rs


class Lanes:
    """Per-lane NFW (rs, rhos, Rtr truncation radius), s-law (svK, n), age T, and baryon tables M_b = MBG + ups MBS on the
    uniform ln r grid LG (rows indexed by `row`)."""

    def __init__(self, rs, rhos, Rtr, svK, n, T, LG, MBG, MBS, row, ups):
        f = lambda a: np.atleast_1d(np.asarray(a, float))
        self.rs, self.rhos, self.Rtr, self.svK, self.n, self.T, self.ups = map(f, (rs, rhos, Rtr, svK, n, T, ups))
        self.row = np.atleast_1d(np.asarray(row, int)); self.LG, self.MBG, self.MBS = LG, MBG, MBS
        self.dLG = LG[1] - LG[0]; self.size = len(self.rs); self.nG = len(LG)
        self._g, self._s = MBG.ravel(), MBS.ravel(); self._base = self.row * self.nG
        m0 = MBG[self.row, 0] + self.ups * MBS[self.row, 0]; m1 = MBG[self.row, 1] + self.ups * MBS[self.row, 1]
        self._m0 = m0; self._p = np.where((m0 > 0) & (m1 > 0), np.log(np.maximum(m1, 1e-300) / np.maximum(m0, 1e-300)) / self.dLG, 3.0)

    def sub(self, idx):
        return Lanes(self.rs[idx], self.rhos[idx], self.Rtr[idx], self.svK[idx], self.n[idx], self.T[idx], self.LG, self.MBG,
                     self.MBS, self.row[idx], self.ups[idx])

    def mb(self, lr):
        t = (lr - self.LG[0]) / self.dLG; below = t < 0; t = np.clip(t, 0, self.nG - 1.000001); i = t.astype(int); fr = t - i
        k = self._base + i; g0, g1, s0, s1 = self._g[k], self._g[k + 1], self._s[k], self._s[k + 1]
        m = g0 + fr * (g1 - g0) + self.ups * (s0 + fr * (s1 - s0))
        if below.any():
            m = np.where(below, self._m0 * np.exp(self._p * np.minimum(lr - self.LG[0], 0)), m)   # first-step power law below the table
        return np.maximum(m, 0.0)

    def bc(self, lsig):
        sig = np.exp(lsig); rho1 = 1 / (self.svK * sig ** (1 - self.n) * self.T)
        r1 = r1_nfw(rho1, self.rs, self.rhos); M1 = FOURPI * self.rhos * self.rs ** 3 * mN(r1 / self.rs)
        return r1, rho1, M1

    def m_nfw(self, r):
        rr = np.minimum(r, self.Rtr[:, None] if np.ndim(r) == 2 else self.Rtr)
        rs = self.rs[:, None] if np.ndim(r) == 2 else self.rs; rh = self.rhos[:, None] if np.ndim(r) == 2 else self.rhos
        return FOURPI * rh * rs ** 3 * mN(rr / rs)


def integrate(L, lsig, lrho0, lam, keep=False):
    """outward RK4 in u = ln(r/r1) from r1 e^UMIN to r1. Returns ln rho(r1)/rho1, ln M(r1)/M1 (and M, ln rho on the u grid)."""
    r1, rho1, M1 = L.bc(lsig); s2 = np.exp(2 * lsig); lr1 = np.log(r1); du = -UMIN / NU
    u = UMIN; r0 = r1 * math.exp(u); x2 = FOURPI * GK * np.exp(lrho0) * r0 ** 2 / s2      # xi^2 at the start: isothermal series start
    lrho = lrho0 - x2 / 6; M = FOURPI / 3 * np.exp(lrho0) * r0 ** 3 * (1 - x2 / 10)

    def F(u, lrho, M):
        rr = r1 * math.exp(u); mb = lam * L.mb(lr1 + u) if lam else 0.0
        return -GK * (M + mb) / (s2 * rr), FOURPI * rr ** 3 * np.exp(np.minimum(lrho, 600))
    TM, TL = ([M.copy()], [lrho.copy()]) if keep else (None, None)
    for _ in range(NU):
        a1, b1 = F(u, lrho, M); a2, b2 = F(u + du / 2, lrho + du / 2 * a1, M + du / 2 * b1)
        a3, b3 = F(u + du / 2, lrho + du / 2 * a2, M + du / 2 * b2); a4, b4 = F(u + du, lrho + du * a3, M + du * b3)
        lrho = lrho + du / 6 * (a1 + 2 * a2 + 2 * a3 + a4); M = M + du / 6 * (b1 + 2 * b2 + 2 * b3 + b4); u += du
        if keep: TM.append(M.copy()); TL.append(lrho.copy())
    out = (lrho - np.log(rho1), np.log(np.maximum(M, 1e-300)) - np.log(M1))
    if keep: return out + (np.array(TM).T, np.array(TL).T)
    return out


def _res0(L, ls):
    """no-baryon residual ln sigma'(sigma) - ln sigma and ln rho0, for ls of shape (lanes,) or (lanes, k)."""
    ex = (lambda a: a[:, None]) if np.ndim(ls) == 2 else (lambda a: a)
    sig = np.exp(ls); rho1 = 1 / (ex(L.svK) * sig ** (1 - ex(L.n)) * ex(L.T))
    r1 = r1_nfw(rho1, ex(L.rs), ex(L.rhos)); M1 = FOURPI * ex(L.rhos) * ex(L.rs) ** 3 * mN(r1 / ex(L.rs))
    xi1 = xi_of_h(M1 / (FOURPI * rho1 * r1 ** 3)); good = np.isfinite(xi1)
    rho0 = rho1 * np.exp(psi_of(np.where(good, xi1, 1.0)))
    sigp = r1 / np.where(good, xi1, 1.0) * np.sqrt(FOURPI * GK * rho0)
    return np.where(good, np.log(sigp) - ls, np.nan), np.where(good, np.log(rho0), np.nan)


def init_nobaryon(L):
    """lowest-rho0 root per lane on SIG_GRID, bisected (vectorised). Returns ls, lrho0, number of roots."""
    nl = L.size; LS = np.broadcast_to(SIG_GRID, (nl, len(SIG_GRID)))
    R, LR0 = _res0(L, LS)
    sc = np.isfinite(R[:, :-1]) & np.isfinite(R[:, 1:]) & (np.sign(R[:, :-1]) != np.sign(R[:, 1:]))
    nroots = sc.sum(1)
    key = np.where(sc, LR0[:, :-1], np.inf); j = np.argmin(key, 1)
    a = SIG_GRID[j].copy(); b = SIG_GRID[np.minimum(j + 1, len(SIG_GRID) - 1)].copy(); fa = R[np.arange(nl), j]
    for _ in range(64):
        m = 0.5 * (a + b); fm, _ = _res0(L, m)
        same = np.sign(fm) == np.sign(fa); a = np.where(same, m, a); fa = np.where(same, fm, fa); b = np.where(same, b, m)
    ls = 0.5 * (a + b); _, lr0 = _res0(L, ls)
    ok = nroots > 0
    return np.where(ok, ls, np.nan), np.where(ok, lr0, np.nan), nroots


def solve(L, lam_final=1.0, tol=1e-9, itmax=40):
    """Returns x (lanes, 2) = (ln sigma0, ln rho0), converged mask, number of lambda = 0 roots."""
    ls, lr0, nroots = init_nobaryon(L)
    conv = np.isfinite(ls)
    x = np.c_[np.where(conv, ls, 4.0), np.where(conv, lr0, 15.0)]
    steps = (0.0,) + (tuple(lam_final * s for s in LAM_STEPS) if lam_final else ())
    for lam in steps:
        act = np.where(conv)[0]
        for _ in range(itmax):
            if not len(act): break
            Ls = L.sub(act); xs = x[act]
            ra, rb = integrate(Ls, xs[:, 0], xs[:, 1], lam); nrm = np.maximum(np.abs(ra), np.abs(rb))
            keep = ~(nrm < tol) & np.isfinite(nrm)
            bad = ~np.isfinite(nrm)
            if bad.any(): conv[act[bad]] = False
            act = act[keep]; xs = xs[keep]; ra = ra[keep]; rb = rb[keep]
            if not len(act): break
            Ls = L.sub(act); h = 1e-6
            a1, b1 = integrate(Ls, xs[:, 0] + h, xs[:, 1], lam); a2, b2 = integrate(Ls, xs[:, 0], xs[:, 1] + h, lam)
            J00, J01, J10, J11 = (a1 - ra) / h, (a2 - ra) / h, (b1 - rb) / h, (b2 - rb) / h
            det = J00 * J11 - J01 * J10
            d0 = -(J11 * ra - J01 * rb) / det; d1 = -(-J10 * ra + J00 * rb) / det
            sc = np.minimum(1.0, 0.5 / np.maximum(np.maximum(np.abs(d0), np.abs(d1)), 1e-300))
            d0 = np.where(np.isfinite(d0), d0 * sc, 0.0); d1 = np.where(np.isfinite(d1), d1 * sc, 0.0)
            x[act, 0] += d0; x[act, 1] += d1
        idx = np.where(conv)[0]
        if len(idx):
            ra, rb = integrate(L.sub(idx), x[idx, 0], x[idx, 1], lam)
            conv[idx] = np.isfinite(ra) & (np.maximum(np.abs(ra), np.abs(rb)) < 1e-7)
    return x, conv, nroots


def halo_mass(L, x, conv, r, lam=1.0):
    """M_h(r) in Msun, r (lanes, k) in kpc: isothermal inside r1, NFW (truncated at Rtr) outside; NFW for unconverged lanes."""
    r = np.asarray(r, float); Mn = L.m_nfw(r)
    idx = np.where(conv)[0]
    if not len(idx): return Mn, np.full(L.size, np.nan)
    Ls = L.sub(idx); _, _, TM, _ = integrate(Ls, x[idx, 0], x[idx, 1], lam, keep=True)
    r1, _, _ = Ls.bc(x[idx, 0]); u = np.log(r[idx] / r1[:, None]); du = -UMIN / NU
    t = (u - UMIN) / du; tc = np.clip(t, 0, NU - 1e-9); k = tc.astype(int); fr = tc - k
    lTM = np.log(np.maximum(TM, 1e-300)); rows = np.arange(len(idx))[:, None]
    lM = lTM[rows, k] * (1 - fr) + lTM[rows, k + 1] * fr
    Mi = np.where(t < 0, TM[:, :1] * np.exp(3 * np.minimum(u - UMIN, 0)), np.exp(lM))
    out = Mn.copy(); out[idx] = np.where(u < 0, Mi, Mn[idx])
    r1all = np.full(L.size, np.nan); r1all[idx] = r1
    return out, r1all


def check_lane(L, j, x, lam=1.0):
    """K1: independent LSODA outward solve from the centre at the solved (sigma0, rho0); returns rho(r1)/rho1-1, M(r1)/M1-1."""
    Lj = L.sub([j]); s = math.exp(x[0]); rho0 = math.exp(x[1]); r1, rho1, M1 = (float(v[0]) for v in Lj.bc(np.array([x[0]])))
    mb = lambda rr: lam * float(Lj.mb(np.array([math.log(rr)]))[0])
    f = lambda rr, y: [-GK * (y[1] + mb(rr)) / (s * s * rr * rr), FOURPI * rr * rr * math.exp(y[0])]
    r0 = r1 * 1e-6
    so = solve_ivp(f, (r0, r1), [math.log(rho0), FOURPI / 3 * rho0 * r0 ** 3], method="LSODA", rtol=1e-10, atol=[1e-12, 1e-12 * M1])
    return math.exp(so.y[0, -1]) / rho1 - 1, so.y[1, -1] / M1 - 1
