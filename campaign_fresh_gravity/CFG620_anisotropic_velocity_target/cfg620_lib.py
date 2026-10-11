#!/usr/bin/env python3
"""CFG620 library: the maximum-entropy exact stationary F(E, L) of a given spherical density in a given spherical field
(route ME, FROZEN_CRITERIA.md 93abcbeb6), LP isotropy / mirror tests, and the target sampler used by the bench operator FIX-A.

Orbit library in (r_peri, r_apo) on a log grid; phase volume 8 pi^2 L T_r dE dL; time fractions by theta-quadrature.
kappa = 1/2 FITTED; cold energy mass required; not "theory closed".
"""
import math
import numpy as np
from scipy.interpolate import CubicSpline

NTH = 48                        # theta-quadrature points per orbit (midpoint rule in theta)


class Field:
    """Spherical field from an enclosed-mass function on a fine log grid (G = 1). g(r) = gfun(r) supplied directly."""
    def __init__(self, gfun, rlo, rhi, n=6001):
        lr = np.linspace(math.log(rlo) - 0.05, math.log(rhi) + 0.05, n)
        r = np.exp(lr); g = gfun(r)
        # Phi(r) = -int_r^rhi g dr' (zero at the top of the grid; only differences matter)
        integ = g * r                                          # d Phi / d ln r
        seg = 0.5 * (integ[1:] + integ[:-1]) * np.diff(lr)
        phi = np.concatenate([-np.cumsum(seg[::-1])[::-1], [0.0]])
        self.lr, self.r = lr, r
        self._phi = CubicSpline(lr, phi); self._g = CubicSpline(lr, g)

    def phi(self, r):
        return self._phi(np.log(r))

    def g(self, r):
        return self._g(np.log(r))


def EL_from_peri_apo(F, rp, ra):
    """E, L^2 of the orbit with turning points rp <= ra (circular limit handled)."""
    rp = np.asarray(rp, float); ra = np.asarray(ra, float)
    circ = (ra - rp) <= 1e-9 * ra
    pp, pa = F.phi(rp), F.phi(ra)
    with np.errstate(divide="ignore", invalid="ignore"):
        L2 = 2 * (pa - pp) / (1 / rp ** 2 - 1 / ra ** 2)
    rc = 0.5 * (rp + ra)
    L2 = np.where(circ, rc ** 3 * F.g(rc), L2)
    E = np.where(circ, F.phi(rc) + 0.5 * rc * F.g(rc), pa + L2 / (2 * ra ** 2))
    return E, np.maximum(L2, 0.0)


class Library:
    """Orbit cells (i <= j) on orbit nodes u (log r); constraint bins = every 2nd node (nb bins)."""
    def __init__(self, F, rlo, rhi, nb=120, sub=2):
        """the library has an inner boundary at rlo (no orbit passes inside it; the bench's reflecting RMIN)."""
        self.F = F; self.sub = sub; self.nb = nb
        self.ub = np.linspace(math.log(rlo), math.log(rhi), nb + 1)            # constraint-bin faces
        self.uo = np.linspace(math.log(rlo), math.log(rhi), nb * sub + 1)      # orbit-node faces
        no = nb * sub
        I, J = np.triu_indices(no)
        self.I, self.J = I, J
        uo = self.uo
        # cell centres (diagonal: triangle centroid in (u_p, u_a))
        up = np.where(I == J, (2 * uo[I] + uo[I + 1]) / 3, 0.5 * (uo[I] + uo[I + 1]))
        ua = np.where(I == J, (uo[J] + 2 * uo[J + 1]) / 3, 0.5 * (uo[J] + uo[J + 1]))
        self.rp, self.ra = np.exp(up), np.exp(ua)
        # (E, L) images of the corners -> cell area (shoelace)
        def EL(a, b):
            E, L2 = EL_from_peri_apo(F, np.exp(a), np.exp(b)); return E, np.sqrt(L2)
        c00 = EL(uo[I], uo[J]); c01 = EL(uo[I], uo[J + 1]); c11 = EL(uo[I + 1], uo[J + 1]); c10 = EL(uo[I + 1], uo[J])
        quad = [c00, c01, c11, c10]
        area_q = 0.5 * np.abs(sum(quad[k][0] * quad[(k + 1) % 4][1] - quad[(k + 1) % 4][0] * quad[k][1] for k in range(4)))
        tri = [c00, c01, c11]                                   # diagonal cell: rp in [u_i, u_i+1], ra in [rp, u_i+1]
        area_t = 0.5 * np.abs(sum(tri[k][0] * tri[(k + 1) % 3][1] - tri[(k + 1) % 3][0] * tri[k][1] for k in range(3)))
        self.area = np.where(I == J, area_t, area_q)
        self.E, L2 = EL_from_peri_apo(F, self.rp, self.ra); self.L = np.sqrt(L2)
        self._orbits()
        self.w = 8 * math.pi ** 2 * self.L * self.Tr * self.area                # phase volume of each cell

    def _orbits(self):
        """time fractions P[c, k] (half period), and time-weighted v_r^2, v_t^2 per bin."""
        F = self.F; nc = self.rp.size; nb = self.nb
        th = (np.arange(NTH) + 0.5) * math.pi / NTH
        rbar = 0.5 * (self.rp + self.ra); dl = 0.5 * (self.ra - self.rp)
        self.P = np.zeros((nc, nb)); self.Vr = np.zeros((nc, nb)); self.Vt = np.zeros((nc, nb))
        self.Tr = np.zeros(nc)
        step = 4000
        for s in range(0, nc, step):
            sl = slice(s, min(s + step, nc))
            rb, d, E, L = rbar[sl, None], dl[sl, None], self.E[sl, None], self.L[sl, None]
            r = rb - d * np.cos(th)[None, :]
            # v_r^2 = 2 (E - Phi) - L^2/r^2, evaluated stably as 2[Phi_eff(ra) - Phi_eff(r)]
            ra = self.ra[sl, None]
            vr2 = 2 * (F.phi(ra) + L ** 2 / (2 * ra ** 2) - F.phi(r) - L ** 2 / (2 * r ** 2))
            # near-circular / turning-point safety: epicyclic form vr2 ~ kappa^2 d^2 sin^2
            vr2 = np.maximum(vr2, 1e-300)
            dt = d * np.sin(th)[None, :] * (math.pi / NTH) / np.sqrt(vr2)
            T2 = dt.sum(1)                                     # half radial period
            self.Tr[sl] = 2 * T2
            k = np.clip(np.searchsorted(self.ub, np.log(r)) - 1, 0, nb - 1)
            rows = np.repeat(np.arange(sl.start, sl.stop), NTH)
            kk = k.ravel()
            np.add.at(self.P, (rows, kk), (dt / T2[:, None]).ravel())
            np.add.at(self.Vr, (rows, kk), (dt * vr2 / T2[:, None]).ravel())
            np.add.at(self.Vt, (rows, kk), (dt * (L ** 2 / r ** 2) / T2[:, None]).ravel())
        self.Vr[self.Vr < 0] = 0.0


def maxent(lib, M, tol=1e-7, itmax=400, verbose=False, gis=3000):
    """Maximise -sum w F ln F s.t. sum_c w_c F_c P_ck = M_k. Dual: min_l sum w exp(-1 - P l) + l.M (damped Newton).
    Returns dict with y = w F (cell masses), lambda, max relative bin error, iterations."""
    P, w = lib.P, lib.w
    lw = np.log(np.maximum(w, 1e-300))
    lam = np.zeros(M.size)
    # generalized iterative scaling first (rows of P sum to 1, so GIS is a valid monotone scheme for any dynamic range)
    for _ in range(gis):
        y = np.exp(np.minimum(lw - 1 - P @ lam, 700))
        Mm = P.T @ y
        lam += np.log(np.maximum(Mm, 1e-300) / M)
    def dual(l):
        a = lw - 1 - P @ l
        am = a.max()
        return math.exp(am) * np.sum(np.exp(a - am)) + l @ M if am < 700 else np.inf
    D = dual(lam); it = 0; err = np.inf
    for it in range(1, itmax + 1):
        y = np.exp(lw - 1 - P @ lam)
        Mm = P.T @ y
        gr = M - Mm
        err = float(np.max(np.abs(gr) / M))
        if err < tol: break
        H = (P * y[:, None]).T @ P
        H += 1e-14 * np.trace(H) / M.size * np.eye(M.size)
        try:
            dl = -np.linalg.solve(H, gr)
        except np.linalg.LinAlgError:
            dl = -np.linalg.lstsq(H, gr, rcond=None)[0]
        t = 1.0
        while t > 1e-10:
            ln = lam + t * dl; Dn = dual(ln)
            if Dn <= D + 1e-4 * t * (gr @ dl): break
            t *= 0.5
        lam, D = ln, Dn
        if verbose and it % 10 == 0: print(it, err, t)
    y = np.exp(lw - 1 - P @ lam)
    Mm = P.T @ y
    err = float(np.max(np.abs(M - Mm) / M))
    return dict(y=y, lam=lam, err=err, it=it, F=y / lib.w)


def moments(lib, y, M):
    Pr = lib.Vr.T @ y; Pt = lib.Vt.T @ y
    s2r = Pr / M; s2t = Pt / M
    with np.errstate(divide="ignore", invalid="ignore"):
        beta = 1 - s2t / (2 * s2r)
    return s2r, s2t, beta, Pr, Pt


def bin_masses(lib, Menc):
    """target bin masses from an enclosed-mass function."""
    rb = np.exp(lib.ub)
    return np.diff(Menc(rb))


def lp_minimax(lib, M, kset, ratio, iters=14, tmax=1.0, yscale=None, time_limit=120.0):
    """min over cell masses y >= 0 (bin masses exact) of max_{k in kset} |Pi_t - ratio_k Pi_r| / (Pi_t + ratio_k Pi_r).
    Bisection on t with HiGHS feasibility LPs. Returns (t_min, status_of_last_feasible)."""
    from scipy.optimize import linprog
    nc = lib.P.shape[0]
    cs = np.ones(nc) if yscale is None else np.maximum(yscale, 1e-300)   # column scaling y = cs * z (z ~ O(1))
    Aeq = (lib.P * cs[:, None] / M[None, :]).T                               # rows scaled to 1
    beq = np.ones(M.size)
    A_t = (lib.Vt[:, kset] * cs[:, None]).T; A_r = (lib.Vr[:, kset] * cs[:, None]).T
    sc = 1.0 / np.maximum(M[kset], 1e-300)
    rk = np.asarray(ratio)[:, None]
    def feasible(t):
        # Pi_t - r Pi_r <= t (Pi_t + r Pi_r)  and  -(Pi_t - r Pi_r) <= t (Pi_t + r Pi_r)
        A1 = ((1 - t) * A_t - (1 + t) * rk * A_r) * sc[:, None]
        A2 = (-(1 + t) * A_t + (1 - t) * rk * A_r) * sc[:, None]
        Aub = np.vstack([A1, A2]); bub = np.zeros(Aub.shape[0])
        res = linprog(np.zeros(nc), A_ub=Aub, b_ub=bub, A_eq=Aeq, b_eq=beq, bounds=(0, None), method="highs",
                      options=dict(primal_feasibility_tolerance=1e-9, dual_feasibility_tolerance=1e-9, time_limit=time_limit))
        if res.status not in (0, 2):
            stat["undetermined"] += 1
        return res.status == 0
    stat = dict(undetermined=0)
    lo, hi = 0.0, tmax
    if not feasible(hi):
        return float("nan"), stat
    if feasible(0.0):
        return 0.0, stat
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        if feasible(mid): hi = mid
        else: lo = mid
    return hi, stat


class Sampler:
    """Target conditional sampler: for a particle in constraint bin k, draw an orbit cell with weight y_c P_ck, jitter
    (r_peri, r_apo) inside the cell, clamp to bracket r, and return (v_r, v_t) from the turning-point relations in a field."""
    def __init__(self, lib, y):
        self.lib = lib
        W = lib.P * y[:, None]                                  # target mass of cell c in bin k
        self.cdf = []; self.idx = []
        for k in range(lib.nb):
            nz = np.where(W[:, k] > 0)[0]
            cw = np.cumsum(W[nz, k]); cw /= cw[-1]
            self.idx.append(nz); self.cdf.append(cw)
        self.ub = lib.ub; self.uo = lib.uo

    def draw(self, r, phi, g, rng):
        """r: positions (all inside the library range); phi, g: callables of the CURRENT field. Returns v_r, v_t."""
        lib = self.lib
        k = np.clip(np.searchsorted(self.ub, np.log(r)) - 1, 0, lib.nb - 1)
        cell = np.empty(r.size, int)
        u = rng.random(r.size)
        for kk in np.unique(k):
            m = k == kk
            cell[m] = self.idx[kk][np.minimum(np.searchsorted(self.cdf[kk], u[m]), self.idx[kk].size - 1)]
        I, J = lib.I[cell], lib.J[cell]
        a, b = rng.random((2, r.size))
        diag = I == J
        lo_, hi_ = np.minimum(a, b), np.maximum(a, b)
        up = np.where(diag, self.uo[I] + lo_ * (self.uo[I + 1] - self.uo[I]), self.uo[I] + a * (self.uo[I + 1] - self.uo[I]))
        ua = np.where(diag, self.uo[I] + hi_ * (self.uo[I + 1] - self.uo[I]), self.uo[J] + b * (self.uo[J + 1] - self.uo[J]))
        rp = np.minimum(np.exp(up), r); ra = np.maximum(np.exp(ua), r)
        pp, pa, pr = phi(rp), phi(ra), phi(r)
        circ = (ra - rp) <= 1e-9 * ra
        with np.errstate(divide="ignore", invalid="ignore"):
            L2 = 2 * (pa - pp) / (1 / rp ** 2 - 1 / ra ** 2)
        L2 = np.where(circ | ~np.isfinite(L2), r ** 3 * g(r), np.maximum(L2, 0.0))
        vr2 = 2 * (pa + L2 / (2 * ra ** 2) - pr - L2 / (2 * r ** 2))
        vr = np.sqrt(np.maximum(vr2, 0.0)) * np.where(rng.random(r.size) < 0.5, -1.0, 1.0)
        vt = np.sqrt(L2) / r
        return vr, vt
