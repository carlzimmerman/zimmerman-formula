#!/usr/bin/env python3
"""EMV1 one-bubble solver (criteria f924165783). TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.

One law-on bubble (radius R_w = 1) around point baryons in a uniform external field e (fields in units of a0, lengths in R_w):
    inside  r < 1 : div[K(|grad Phi|) grad Phi] = 4 pi G M_b delta,   K(u) = u / (1 + u)   (the law)
    outside r > 1 : Laplace;   at r = 1: Phi continuous, K dPhi/dr (in) = dPhi/dr (out);   Phi -> -e z far away.
The problem depends only on y_w = G M_b / (R_w^2 a0) and e = g_ext / a0.

Phi = Phi_ref(r) + psi. Axisymmetric finite volume in s = ln r (vertex-centred, nodes on both boundaries) and mu = cos theta
(cells centred on Gauss-Legendre nodes, widths = the Gauss weights). Outer boundary: the exact exterior Dirichlet-to-Neumann map
in Legendre modes. Inner boundary r0 (y(r0) = 1e6 with a galaxy): regular modes d psi_l / d ln r = l psi_l for l >= 1 and the
l = 0 flux fixed by Gauss. Newton with a sparse central-difference Jacobian (column colouring), continuation in e.
alpha_tot = 1 + psi_1(1) / e;  alpha_inc = 1 + d psi_1(1) / d e from the tangent problem at the converged state.
"""
import math
import numpy as np
from numpy.polynomial.legendre import leggauss, legvander
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import splu


def u_in(y):
    """the law's field (a0 units) for Newtonian field y: K(u) u = y."""
    y = np.asarray(y, float)
    return 0.5 * y + np.sqrt(0.25 * y * y + y)


class Bubble:
    def __init__(self, yw, ds=0.06, Nmu=32, kmode="law", ref="law", r0=None, Kconst=None, coat=None,
                 flux_mutate=False, eta=1.0, y_inner=1e6, eps_fac=1e-6):
        self.yw = float(yw)
        self.kmode, self.ref, self.flux_mutate, self.eta = kmode, ref, flux_mutate, eta
        self.Kconst, self.coat = Kconst, coat
        if r0 is None:
            r0 = math.sqrt(self.yw / y_inner) if self.yw > 0 else 1e-3
        s0 = math.log(r0)
        if coat is not None:                                      # put the core/shell interface on a radial face
            a = coat[2]; k = max(1, int(round(-math.log(a) / ds + 0.5)))
            ds = -math.log(a) / (k - 0.5)
        N = int(math.ceil(-s0 / ds)); self.ds = -s0 / N if coat is None else ds
        if coat is not None:
            N = int(math.ceil(-s0 / self.ds))
        self.N, self.M = N, Nmu
        self.s = np.linspace(-N * self.ds, 0.0, N + 1); self.r = np.exp(self.s); self.r0 = self.r[0]
        self.sf = 0.5 * (self.s[1:] + self.s[:-1]); self.rf = np.exp(self.sf)
        ri = np.empty(N + 1); ri[0] = self.rf[0] - self.r[0]; ri[1:-1] = self.rf[1:] - self.rf[:-1]; ri[-1] = self.r[-1] - self.rf[-1]
        self.rint = ri
        mu, w = leggauss(Nmu); self.mu, self.w = mu, w
        self.muf = -1.0 + np.cumsum(w)[:-1]; self.dmuc = mu[1:] - mu[:-1]
        self.omu2, self.omuf2 = 1 - mu * mu, 1 - self.muf * self.muf
        V = legvander(mu, Nmu - 1)                                # V[j, l] = P_l(mu_j)
        self.P = V.T                                              # (L+1, M)
        lfac = (2 * np.arange(Nmu) + 1) / 2.0
        self.T = (lfac[:, None] * self.P) * w[None, :]            # psi_l = T @ psi_j  (exact for l < Nmu)
        l = np.arange(Nmu)
        self.Dout = self.P[1:].T @ np.diag(l[1:] + 1.0) @ self.T[1:]
        self.Din = self.P[1:].T @ np.diag(l[1:] * 1.0) @ self.T[1:]
        # central-difference d/dmu at nodes
        C = np.zeros((Nmu, Nmu))
        for j in range(Nmu):
            jl, jr = max(j - 1, 0), min(j + 1, Nmu - 1)
            C[j, jr] += 1.0 / (mu[jr] - mu[jl]); C[j, jl] -= 1.0 / (mu[jr] - mu[jl])
        self.Cmu = C
        self.gref_n = self.gref(self.r); self.gref_f = self.gref(self.rf); self.gref0 = float(self.gref(np.array([self.r0]))[0])
        self.gwall = float(u_in(self.yw)) if self.yw > 0 else 0.0
        self.eps_fac = eps_fac; self.eps2 = 0.0
        # coated sphere: K by radius, harmonic mean on the interface face
        if coat is not None:
            m1, m2, a = coat
            self.Kf_c = np.where(self.rf < a * (1 - 1e-9), m1, m2).astype(float)
            iface = np.argmin(np.abs(self.rf - a))
            if abs(self.rf[iface] / a - 1) < 1e-9: self.Kf_c[iface] = 2 * m1 * m2 / (m1 + m2)
            self.Kn_c = np.where(self.r < a, m1, m2).astype(float)
        self._colouring()

    # ---------------------------------------------------------------- reference field and K
    def gref(self, r):
        r = np.asarray(r, float)
        if self.ref == "law" and self.yw > 0: return u_in(self.yw / r ** 2)
        if self.ref == "newton" and self.yw > 0: return self.yw / r ** 2
        return np.zeros_like(r)

    def K(self, G, where):
        if self.kmode == "law": return G / (1.0 + G)
        if self.kmode == "mu1": return np.ones_like(G)
        if self.kmode == "const": return np.full_like(G, self.Kconst)
        if self.kmode == "coated":
            if where == "f": return np.broadcast_to(self.Kf_c[:, None], G.shape)
            if where == "n": return np.broadcast_to(self.Kn_c[:, None], G.shape)
            if where == "0": return np.full_like(G, self.Kn_c[0])
            if where == "N": return np.full_like(G, self.Kn_c[-1])
        raise ValueError(self.kmode)

    def set_eps(self, e):
        base = min(self.gwall, e) if self.gwall > 0 else e
        self.eps2 = (self.eps_fac * base) ** 2

    # ---------------------------------------------------------------- residual (net outward flux of every control volume)
    def F(self, x, e):
        N, M = self.N, self.M
        psi = x.reshape(N + 1, M)
        dps = (psi[1:] - psi[:-1]) / self.ds                                   # d psi / ds on radial faces
        grf = self.gref_f[:, None] + dps / self.rf[:, None]
        dmn = psi @ self.Cmu.T                                                 # d psi / dmu at nodes
        tq = 0.5 * (dmn[1:] + dmn[:-1])
        Gf = np.sqrt(grf ** 2 + self.omu2[None, :] * tq ** 2 / self.rf[:, None] ** 2 + self.eps2)
        Fr = self.K(Gf, "f") * grf * (self.rf ** 2)[:, None] * self.w[None, :]
        dsin = psi[0] @ self.Din.T                                            # regular modes at r0
        drn = np.empty_like(psi); drn[1:-1] = 0.5 * (dps[1:] + dps[:-1]); drn[0] = dsin; drn[-1] = dps[-1]
        grn = self.gref_n[:, None] + drn / self.r[:, None]
        dpm = (psi[:, 1:] - psi[:, :-1]) / self.dmuc[None, :]
        grm = 0.5 * (grn[:, 1:] + grn[:, :-1])
        Gm = np.sqrt(grm ** 2 + self.omuf2[None, :] * dpm ** 2 / self.r[:, None] ** 2 + self.eps2)
        Fm = self.K(Gm, "n") * self.omuf2[None, :] * dpm * self.rint[:, None]
        res = np.zeros_like(psi)
        res[:-1] += Fr; res[1:] -= Fr
        res[:, :-1] += Fm; res[:, 1:] -= Fm
        # inner face: nonlinear flux, with the l = 0 flux held at Gauss's value y_w
        gr0 = self.gref0 + dsin / self.r0
        G0 = np.sqrt(gr0 ** 2 + self.omu2 * dmn[0] ** 2 / self.r0 ** 2 + self.eps2)
        Gr = abs(self.gref0)
        Kr = self.K(np.array([Gr]), "0")[0] if self.yw > 0 else 0.0
        Fin = self.w * (self.r0 ** 2 * self.K(G0, "0") * gr0 - self.r0 ** 2 * Kr * self.gref0 + self.yw)
        res[0] -= Fin
        # outer face: exact exterior DtN; flux continuity (or, under M-FLUX, field continuity)
        psiN = psi[-1]
        gout = self.yw - 3.0 * e * self.mu - psiN @ self.Dout.T
        if self.flux_mutate:
            GN = np.sqrt(gout ** 2 + self.omu2 * dmn[-1] ** 2 + self.eps2)
            Fout = self.w * self.K(GN, "N") * gout
        else:
            Fout = self.w * gout
        Fout = Fout + self.eta * self.w * (self.T[0] @ psiN)
        res[-1] += Fout
        return res.ravel()

    def dFde(self, x, e):
        """partial derivative of the residual in e at fixed psi (eps held fixed). The law and every known-answer mode enter e
        only through the exterior DtN term, linearly, so the derivative is exact there; under M-FLUX that term is multiplied
        by K(|grad Phi|), so the derivative is taken by central difference (step 1e-6 of the field scale)."""
        if self.flux_mutate:
            h = 1e-6 * max(e, self.gwall, 1e-30)
            return (self.F(x, e + h) - self.F(x, e - h)) / (2 * h)
        d = np.zeros((self.N + 1, self.M))
        d[-1] = -3.0 * self.w * self.mu
        return d.ravel()

    # ---------------------------------------------------------------- sparse Jacobian by coloured central differences
    def _colouring(self):
        N, M = self.N, self.M
        idx = np.arange((N + 1) * M).reshape(N + 1, M)
        col = np.empty((N + 1, M), int)
        ii, jj = np.meshgrid(np.arange(N + 1), np.arange(M), indexing="ij")
        col[:] = (ii % 3) * 3 + (jj % 3)
        col[0] = 9 + np.arange(M); col[-1] = 9 + M + np.arange(M)
        self.ncol = 9 + 2 * M; self.col = col.ravel()
        rows, cols = [], []
        for di in (-1, 0, 1):
            for dj in (-1, 0, 1):
                i2, j2 = ii + di, jj + dj
                ok = (i2 >= 0) & (i2 <= N) & (j2 >= 0) & (j2 < M)
                rows.append(idx[ok]); cols.append(idx[i2[ok], j2[ok]])
        for b in (0, N):                                     # dense boundary blocks
            rr, cc = np.meshgrid(idx[b], idx[b], indexing="ij"); rows.append(rr.ravel()); cols.append(cc.ravel())
        rows = np.concatenate(rows); cols = np.concatenate(cols)
        key = np.unique(rows * idx.size + cols)
        self.pr, self.pc = key // idx.size, key % idx.size
        self.pg = self.col[self.pc]
        self.gsel = [np.nonzero(self.pg == g)[0] for g in range(self.ncol)]
        self.gcols = [np.nonzero(self.col == g)[0] for g in range(self.ncol)]

    def jac(self, x, e, h):
        n = x.size; data = np.empty(self.pr.size)
        for g in range(self.ncol):
            dx = np.zeros(n); dx[self.gcols[g]] = h
            df = (self.F(x + dx, e) - self.F(x - dx, e)) / (2 * h)
            sel = self.gsel[g]; data[sel] = df[self.pr[sel]]
        return coo_matrix((data, (self.pr, self.pc)), shape=(n, n)).tocsc()

    # ---------------------------------------------------------------- Newton
    def solve(self, e, x0=None, maxit=50, tol=1e-12):
        self.set_eps(e)
        n = (self.N + 1) * self.M
        x = np.zeros(n) if x0 is None else x0.copy()
        scale = max(e, self.gwall, 1e-30)
        h = 1e-7 * scale
        Fx = self.F(x, e); f0 = np.linalg.norm(Fx)
        fscale = max(self.yw, e, 1e-30) * float(np.max(self.w))
        it = 0; conv = False; step = 0.0; xs = scale
        for it in range(1, maxit + 1):
            J = self.jac(x, e, h); lu = splu(J)
            d = lu.solve(-Fx)
            lam = 1.0; nF = np.linalg.norm(Fx)
            while True:
                xn = x + lam * d; Fn = self.F(xn, e)
                if np.linalg.norm(Fn) <= (1 - 1e-4 * lam) * nF or lam < 1e-6: break
                lam *= 0.5
            x, Fx = xn, Fn
            step = np.max(np.abs(lam * d)); xs = max(np.max(np.abs(x)), scale)
            if (step <= tol * xs and lam == 1.0) or (np.max(np.abs(Fx)) <= 1e-11 * fscale and step <= 1e-9 * xs):
                conv = True; break
        J = self.jac(x, e, h); lu = splu(J)
        dx = lu.solve(-self.dFde(x, e))
        psiN = x.reshape(self.N + 1, self.M)[-1]; dN = dx.reshape(self.N + 1, self.M)[-1]
        p1 = float(self.T[1] @ psiN); dp1 = float(self.T[1] @ dN)
        info = dict(iters=it, converged=bool(conv), resid_max_over_scale=float(np.max(np.abs(Fx)) / fscale), resid0=float(f0),
                    last_step_rel=float(step / xs))
        return x, dx, ((1.0 + p1 / e) if e > 0 else float('nan')), (1.0 + dp1), info

    # ---------------------------------------------------------------- diagnostics
    def fields(self, x):
        psi = x.reshape(self.N + 1, self.M)
        dps = (psi[1:] - psi[:-1]) / self.ds
        grf = self.gref_f[:, None] + dps / self.rf[:, None]
        dmn = psi @ self.Cmu.T; tq = 0.5 * (dmn[1:] + dmn[:-1])
        Gf = np.sqrt(grf ** 2 + self.omu2[None, :] * tq ** 2 / self.rf[:, None] ** 2)
        return grf, Gf

    def legendre_wall(self, x):
        return self.T @ x.reshape(self.N + 1, self.M)[-1]


def path(b, es, x0=None, maxfac=2.0):
    """continuation over an increasing list of e; returns {e: (alpha_tot, alpha_inc, info)} at the requested nodes."""
    es = sorted(set(float(v) for v in es)); out = {}
    x = x0; dx = None; eprev = None
    full = []
    for e in es:
        if eprev is None: full.append(e)
        else:
            k = max(1, int(math.ceil(math.log(e / eprev) / math.log(maxfac))))
            full += list(eprev * (e / eprev) ** (np.arange(1, k + 1) / k))
        eprev = e
    want = set(es); eprev = None
    for e in full:
        guess = None
        if x is not None:
            guess = x + (dx * (e - eprev) if dx is not None and eprev is not None else 0.0)
        x, dx, at, ai, info = b.solve(e, guess)
        eprev = e
        for ew in want:
            if abs(e / ew - 1) < 1e-12: out[ew] = (at, ai, info)
    return out, x

# kappa = 1/2 FITTED; not theory closed. Adopts nothing.
