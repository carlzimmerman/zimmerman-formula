#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG321 engine: the reduced nonlinear zero-field system of the ungated C-H/K chassis on a periodic leaf (1-D or 2-D),
in the dimensionless variables derived in cfg321_zero_field_nonlinear.py (Part A):

    psi_tt = -Lap psi + (1 + eps) Lap u[psi]                                   (hyperbolic khronon, slow time)
    u[psi] = argmin_u  F[u; psi],   F = Int { eps |grad u|^2 - 2 grad psi . grad u + Q(|grad S u + G|^2) } + Vol (eps|G|^2 - 2 g.G)

(U solved per leaf; the lapse has been eliminated exactly through its elliptic equation; S = exp(Lap/2) is the heat
filter with xi = 1; Q'(s^2) = C_T(s) is the normalised kernel tangent, C_T(1) = 1 at y = y*; eps = 1/(Lambda - 1),
Lambda = 4/alpha_c^2; G is the leaf's mean MOND-field gradient, g the khronon's conserved mean gradient.)

Energy (conserved by the continuum flow):  E = Int { psi_t^2 - |grad psi|^2 } - (1 + eps) min_u F.
Discretisation: Fourier pseudo-spectral in space (odd N per dimension, so no Nyquist mode), kick-drift-kick leapfrog in
time, the leaf problem solved by a chord-Newton method on the strictly convex F (factorisation refreshed when the chord
iteration slows), with a backtracking line search and an indefinite-Hessian fallback that is COUNTED (the MUTATE kernel
is not convex).
"""
import math, time
import numpy as np
from scipy.linalg import cho_factor, cho_solve, LinAlgError


# ----------------------------------------------------------------------------------------------------- kernels
class NuMonoKernel:
    """nu_mono (= nu_RAR below the splice y_s = 2.3374), normalised so that C_T(yhat = 1) = 1: yhat = y / y*,
    y* defined exactly by C_T(y*) = C* = (2 - alpha)/alpha  ->  sqrt(y*) = log1p(1/C*)."""
    name = "nu_mono"

    def __init__(self, alpha):
        self.alpha = alpha
        self.Cstar = (2.0 - alpha) / alpha
        self.ystar = math.log1p(1.0 / self.Cstar) ** 2
        self.Y_S = 2.3374

    def _chk(self, y):
        if np.any(y > 1e-4):           # far below the splice in every run; the series below is exact to < 1e-12 there
            raise ValueError("field outside the series range of the kernel")

    def CT(self, yh):
        y = self.ystar * np.maximum(yh, 1e-300); self._chk(y)
        return 1.0 / (self.Cstar * np.expm1(np.sqrt(y)))

    def CL(self, yh):
        y = self.ystar * np.maximum(yh, 1e-300); self._chk(y)
        s = np.sqrt(y); e = np.expm1(s)
        return (1.0 / e) * (1.0 - 0.5 * s * (e + 1.0) / e) / self.Cstar

    def Q(self, yh):                    # Q(s^2) = 2 H(y* s)/(C* y*^2),  H(y) = 2 Int_0^sqrt(y) v^3/expm1(v) dv
        y = self.ystar * np.abs(yh); self._chk(y)
        s = np.sqrt(y)
        I = s ** 3 / 3 - s ** 4 / 8 + s ** 5 / 60 - s ** 7 / 5040 + s ** 9 / 272160
        return 2.0 * (2.0 * I) / (self.Cstar * self.ystar ** 2)


class MuExpKernel:
    """MUTATE: the record's turning kernel mu_exp(x) = 1 - e^{-x} in QUMOND form (x(y) from y = x(1 - e^{-x}); phantom
    h = x - y; C_T = 1/expm1(x), C_L = (1 - x)/(e^x + x - 1) < 0 for x > 1), with a0 -> y* a0 so that its deep-MOND end
    has the same normalisation C_T -> yhat^(-1/2) as nu_mono's; its turning point x = 1 sits at yhat = 1 - 1/e."""
    name = "mu_exp"

    def __init__(self, alpha):
        self.alpha = alpha

    @staticmethod
    def x_of(y):
        y = np.maximum(y, 1e-300)
        x = np.where(y < 1.0, np.sqrt(y) + y / 4.0, y + 0.5)
        for _ in range(40):
            em = -np.expm1(-x)
            f = x * em - y; fp = em + x * np.exp(-x)
            x = np.maximum(x - f / fp, 1e-300)
        return x

    def CT(self, yh):
        with np.errstate(over="ignore"):              # exp overflow at very large x gives the exact limit 0
            return 1.0 / np.expm1(self.x_of(yh))

    def CL(self, yh):
        x = self.x_of(yh)
        with np.errstate(over="ignore"):
            return (1.0 - x) / (np.exp(x) + x - 1.0)

    def Q(self, yh):
        y = np.abs(yh); x = self.x_of(y)
        # -x^2/2 + 1 - (1 + x) e^{-x}, by series at small x
        small = x < 1e-2
        r_big = -x ** 2 / 2 + (-np.expm1(-x) - x * np.exp(-x))
        r_sm = -x ** 3 / 3 + x ** 4 / 8 - x ** 5 / 30 + x ** 6 / 144
        r = np.where(small, r_sm, r_big)
        return 2.0 * (x * y - y ** 2 / 2 + r)


class ZeroKernel:
    """Control C-GR: the MOND sector switched off (Q = 0): GR + the healthy BPS khronon."""
    name = "off"

    def __init__(self, alpha=None):
        pass

    def CT(self, yh):
        return np.zeros_like(yh)

    def CL(self, yh):
        return np.zeros_like(yh)

    def Q(self, yh):
        return np.zeros_like(yh)


# ----------------------------------------------------------------------------------------------------- grid
class Grid:
    def __init__(self, dim, n, L):
        assert n % 2 == 1
        self.dim, self.n, self.L = dim, n, L
        self.dx = L / n
        self.N = n ** dim
        self.dV = self.dx ** dim
        self.Vol = L ** dim
        k1 = 2 * np.pi * np.fft.fftfreq(n, d=self.dx)
        self.k1 = k1
        if dim == 1:
            self.k = [k1]
        else:
            KX, KY = np.meshgrid(k1, k1, indexing="ij")
            self.k = [KX, KY]
        self.k2 = sum(kk ** 2 for kk in self.k)
        self.sig = np.exp(-self.k2 / 2.0)           # S = exp(Lap/2), xi = 1
        self.shape = (n,) * dim
        I1 = np.eye(n)
        D1 = np.fft.ifft(1j * k1[:, None] * np.fft.fft(I1, axis=0), axis=0).real
        S1 = np.fft.ifft(np.exp(-k1 ** 2 / 2)[:, None] * np.fft.fft(I1, axis=0), axis=0).real
        if dim == 1:
            self.Dm = [D1]; Sm = S1
        else:
            self.Dm = [np.kron(D1, I1), np.kron(I1, D1)]; Sm = np.kron(S1, S1)
        self.Bm = [D @ Sm for D in self.Dm]
        self.DtD = sum(D.T @ D for D in self.Dm)
        self.one = np.ones((self.N, self.N)) / self.N

    # spectral operators on flat arrays
    def fft(self, f):
        return np.fft.fftn(f.reshape(self.shape))

    def ifft(self, F):
        return np.fft.ifftn(F).real.ravel()

    def grad(self, f):
        F = self.fft(f); return [self.ifft(1j * kk * F) for kk in self.k]

    def Bop(self, f):                                # grad S f
        F = self.fft(f) * self.sig; return [self.ifft(1j * kk * F) for kk in self.k]

    def BTop(self, vs):                              # sum_a B_a^T v_a = -S div v
        acc = 0
        for kk, v in zip(self.k, vs):
            acc = acc + (-1j * kk) * self.fft(v)
        return self.ifft(acc * self.sig)

    def DTop(self, vs):                              # sum_a D_a^T v_a = -div v
        acc = 0
        for kk, v in zip(self.k, vs):
            acc = acc + (-1j * kk) * self.fft(v)
        return self.ifft(acc)

    def lap(self, f):
        return self.ifft(-self.k2 * self.fft(f))

    def coords(self):
        x1 = np.arange(self.n) * self.dx
        if self.dim == 1:
            return [x1]
        X, Y = np.meshgrid(x1, x1, indexing="ij")
        return [X.ravel(), Y.ravel()]


# ----------------------------------------------------------------------------------------------------- the leaf solver
class Leaf:
    """Solve min_u F[u; psi] for the periodic u (mean fixed to 0) and the mean field gradient G (d unknowns)."""

    def __init__(self, grid, kern, eps, g):
        self.gr, self.K, self.eps, self.g = grid, kern, eps, np.asarray(g, float)
        self.fac = None
        self.n_refac = 0
        self.n_indef = 0
        self.max_res = 0.0
        self.n_iter = 0

    def fields(self, u, G):
        w = self.gr.Bop(u)
        w = [wa + Ga for wa, Ga in zip(w, G)]
        yh = np.sqrt(sum(wa ** 2 for wa in w))
        return w, yh

    def F(self, u, G, psi):
        gr = self.gr
        du = gr.grad(u); dp = gr.grad(psi)
        w, yh = self.fields(u, G)
        dens = self.eps * sum(a ** 2 for a in du) - 2 * sum(a * b for a, b in zip(dp, du)) + self.K.Q(yh)
        return gr.dV * dens.sum() + gr.Vol * (self.eps * G @ G - 2 * self.g @ G)

    def dF(self, u, G, psi, du_, dG):               # F(u + du, G + dG) - F(u, G), cancellation-safe
        gr = self.gr
        Du = gr.grad(u); Ddu = gr.grad(du_); dp = gr.grad(psi)
        w0, y0 = self.fields(u, G)
        w1, y1 = self.fields(u + du_, G + dG)
        dens = (self.eps * sum(b * (2 * a + b) for a, b in zip(Du, Ddu)) - 2 * sum(p * b for p, b in zip(dp, Ddu))
                + (self.K.Q(y1) - self.K.Q(y0)))
        return gr.dV * dens.sum() + gr.Vol * (self.eps * (dG @ (2 * G + dG)) - 2 * self.g @ dG)

    def gradF(self, u, G, psi):
        gr = self.gr
        w, yh = self.fields(u, G)
        ct = self.K.CT(np.maximum(yh, 1e-300))
        flux = [ct * wa for wa in w]
        gu = 2 * self.eps * gr.DTop(gr.grad(u)) - 2 * gr.DTop(gr.grad(psi)) + 2 * gr.BTop(flux)
        gG = 2 * self.eps * G - 2 * self.g + 2 * np.array([fa.sum() for fa in flux]) * gr.dV / gr.Vol
        ref_u = np.linalg.norm(2 * gr.DTop(gr.grad(psi))) + 1e-300
        ref_G = 2 * (np.linalg.norm(self.g) + np.linalg.norm([np.abs(fa).mean() for fa in flux])) + 1e-300
        return gu, gG, ref_u, ref_G

    def hessian(self, u, G, floor=1e-14):
        gr, d = self.gr, self.gr.dim
        w, yh = self.fields(u, G)
        yf = np.maximum(yh, floor * max(yh.max(), 1e-300))
        ct, cl = self.K.CT(yf), self.K.CL(yf)
        nvec = [wa / np.maximum(yh, 1e-300) for wa in w]
        A = [[ct * (a == b) + (cl - ct) * nvec[a] * nvec[b] for b in range(d)] for a in range(d)]
        N = gr.N
        H = np.zeros((N + d, N + d))
        Huu = 2 * self.eps * gr.DtD + gr.one
        for a in range(d):
            for b in range(d):
                Huu += 2 * (gr.Bm[a].T * A[a][b]) @ gr.Bm[b]
        H[:N, :N] = Huu
        for b in range(d):
            col = sum(2 * gr.Bm[a].T @ A[a][b] for a in range(d))
            H[:N, N + b] = col; H[N + b, :N] = col
        for a in range(d):
            for b in range(d):
                H[N + a, N + b] = 2 * self.eps * gr.Vol / gr.dV * (a == b) + 2 * A[a][b].sum()
        return H

    def refactor(self, u, G, floor=1e-14):
        H = self.hessian(u, G, floor)
        self.n_refac += 1
        try:
            self.fac = cho_factor(H)
            self.indef = False
        except LinAlgError:
            self.n_indef += 1
            self.indef = True
            lam = np.linalg.eigvalsh(H)
            shift = -lam.min() * 1.1 + 1e-12 * abs(lam).max()
            self.fac = cho_factor(H + shift * np.eye(H.shape[0]))

    def solve(self, psi, u, G, tol=1e-10, tol_accept=1e-8, maxit=400):
        """Chord-Newton on the strictly convex F (residual-merit line search with over-relaxed trials).  The Hessian of Q is singular where the field crosses zero
        (C_L ~ yhat^(-1/2)); near such a point Newton approaches the minimiser geometrically before converging
        quadratically.  Step acceptance uses the residual (exact gradient) as merit; a stale factorisation that gives no
        decrease is refreshed with the exact Hessian; with a fresh one, Armijo on F is the fallback.  Convergence is
        judged on the EXACT gradient only."""
        gr, d, N = self.gr, self.gr.dim, self.gr.N
        if self.fac is None:
            self.refactor(u, G)
        it = 0; last = None; fresh = False

        def resid(uu, GG):
            a, b, ra, rb = self.gradF(uu, GG, psi)
            return max(np.linalg.norm(a) / ra, np.linalg.norm(b) / rb), a, b
        res, gu, gG = resid(u, G)
        while True:
            if res < tol:
                break
            if it >= maxit:
                if res < tol_accept:
                    break
                raise RuntimeError(f"leaf solve did not converge: residual {res:.3e}")
            if last is not None and res > 0.5 * last and not fresh:
                self.refactor(u, G); fresh = True
            rhs = np.concatenate([gu * gr.dV, gG * gr.Vol])
            step = -cho_solve(self.fac, rhs / gr.dV)
            du_, dG = step[:N], step[N:]
            du_ -= du_.mean()
            # residual-merit line search over s in {4, 2, 1, 1/2, ...}: the over-relaxed trials matter where the
            # minimiser has the field exactly at zero on a grid point (Newton then undershoots by a constant factor)
            acc = False; best = None
            r1_, g1u, g1G = resid(u + du_, G + dG)
            if r1_ < 0.5 * res:
                best = (r1_, 1.0, g1u, g1G)
            else:
                for s_try in (4.0, 2.0, 1.0, 0.5, 0.25, 0.125, 0.0625, 1 / 32, 1 / 64, 1 / 128, 1 / 512, 1 / 4096, 1 / 65536):
                    r_t, gtu, gtG = (r1_, g1u, g1G) if s_try == 1.0 else resid(u + s_try * du_, G + s_try * dG)
                    if r_t < res and (best is None or r_t < best[0]):
                        best = (r_t, s_try, gtu, gtG)
            if best is not None:
                r2, s, g2u, g2G = best; acc = True
            if not acc:
                if not fresh:
                    self.refactor(u, G); fresh = True; it += 1; continue
                slope = (gu * gr.dV) @ du_ + (gG * gr.Vol) @ dG
                s = 1.0
                while slope < 0 and self.dF(u, G, psi, s * du_, s * dG) > 1e-4 * s * slope and s > 1e-12:
                    s *= 0.5
                if slope >= 0 or s <= 1e-12:
                    if res < tol_accept:
                        break
                    raise RuntimeError(f"leaf solve stalled: residual {res:.3e}")
                r2, g2u, g2G = resid(u + s * du_, G + s * dG)
            u = u + s * du_; G = G + s * dG
            last = res; res, gu, gG = r2, g2u, g2G
            fresh = False; it += 1
        self.max_res = max(self.max_res, res)
        self.n_iter += it
        return u, G, res


# ----------------------------------------------------------------------------------------------------- data
def random_field(grid, seed, kmax=3.0):
    """Gaussian random field with fixed integer-mode content (grid independent): modes 0 < |k| <= kmax,
    amplitude ~ N(0,1) exp(-|k|^2/4), drawn in a fixed order."""
    rng = np.random.default_rng(seed)
    L, d = grid.L, grid.dim
    X = grid.coords()
    f = np.zeros(grid.N)
    m = int(kmax * L / (2 * np.pi)) + 1
    if d == 1:
        for n1 in range(1, m + 1):
            kk = 2 * np.pi * n1 / L
            a, b = rng.normal(size=2)
            if kk <= kmax + 1e-12:
                f += math.exp(-kk ** 2 / 4) * (a * np.cos(kk * X[0]) + b * np.sin(kk * X[0]))
    else:
        for n1 in range(0, m + 1):
            for n2 in range(-m, m + 1):
                if n1 == 0 and n2 <= 0:
                    continue
                kx, ky = 2 * np.pi * n1 / L, 2 * np.pi * n2 / L
                kk = math.hypot(kx, ky)
                a, b = rng.normal(size=2)
                if kk <= kmax + 1e-12:
                    ph = kx * X[0] + ky * X[1]
                    f += math.exp(-kk ** 2 / 4) * (a * np.cos(ph) + b * np.sin(ph))
    return f


def initial_data(grid, kern, eps, seed, yrms, delta=0.0, seed2=None, G_bg=None, g_bg=None):
    """Data class D: the initial MOND potential u0 is a random field with rms filtered field |grad S u0| = yrms
    (in units of y*), khronon velocity zero, zero mean khronon gradient g = 0 (exact zero background) unless a
    background is requested (linear-rate control).  psi0 follows from the leaf equation (no solve needed)."""
    u0 = random_field(grid, seed)
    w = grid.Bop(u0); s = math.sqrt(np.mean(sum(a ** 2 for a in w)))
    u0 *= yrms / s
    if delta:
        e2 = random_field(grid, seed2)
        w2 = grid.Bop(e2); s2 = math.sqrt(np.mean(sum(a ** 2 for a in w2)))
        u0 = u0 + delta * yrms * e2 / s2
    d = grid.dim
    if G_bg is None:
        # g = 0: solve eps G + <C_T(|w|) w> = 0 for G (d-dim Newton on a convex function)
        G = np.zeros(d)
        wb = grid.Bop(u0)
        for _ in range(200):
            w = [a + b for a, b in zip(wb, G)]
            yh = np.sqrt(sum(a ** 2 for a in w))
            ct = kern.CT(np.maximum(yh, 1e-300))
            r = eps * G + np.array([np.mean(ct * a) for a in w])
            if np.linalg.norm(r) < 1e-15 * (1e-300 + np.mean(np.abs(ct * yh))):
                break
            cl = kern.CL(np.maximum(yh, 1e-14 * yh.max()))
            nv = [a / np.maximum(yh, 1e-300) for a in w]
            J = np.array([[eps * (a == b) + np.mean(ct * (a == b) + (cl - ct) * nv[a] * nv[b]) for b in range(d)] for a in range(d)])
            G = G - np.linalg.solve(J, r)
        g = np.zeros(d)
    else:
        G = np.asarray(G_bg, float); g = np.asarray(g_bg, float)
    psi0 = psi_from_u(grid, kern, eps, u0, G)
    return psi0, u0, G, g


def psi_from_u(grid, kern, eps, u0, G):
    """The khronon field for which u0 (with mean field gradient G) solves the leaf equation exactly."""
    d = grid.dim
    w = [a + b for a, b in zip(grid.Bop(u0), G)]
    yh = np.sqrt(sum(a ** 2 for a in w))
    ct = kern.CT(np.maximum(yh, 1e-300))
    rhs = grid.BTop([ct * a for a in w])            # -S div(C_T w)
    R = grid.fft(rhs)
    k2 = grid.k2.copy(); k2[(0,) * d] = 1.0
    Pk = R / k2; Pk[(0,) * d] = 0.0
    return eps * u0 + grid.ifft(Pk)


# ----------------------------------------------------------------------------------------------------- the evolution
def evolve(grid, kern, eps, psi, u, G, g, T, dtout=0.25, cfl=0.5, snap_every=1, log=None, max_wall=None, probe_idx=()):
    leaf = Leaf(grid, kern, eps, g)
    u, G, r0 = leaf.solve(psi, u, G)
    p = np.zeros_like(psi)
    dt0 = cfl * math.sqrt(eps / (1 + eps)) * grid.dx / math.sqrt(grid.dim) / math.pi * 2.0   # omega_max dt <= cfl*2
    m = int(math.ceil(dtout / dt0)); dt = dtout / m
    nout = int(round(T / dtout))

    def force(psi, u):
        return grid.lap(-psi + (1 + eps) * u)

    def diag(psi, p, u, G):
        w, yh = leaf.fields(u, G)
        Fm = leaf.F(u, G, psi)
        dps = grid.grad(psi)
        Ekin = grid.dV * (p ** 2).sum()
        Egr = -grid.dV * sum(a ** 2 for a in dps).sum()
        E = Ekin + Egr - (1 + eps) * Fm
        Ps = np.abs(grid.fft(psi)) ** 2 * grid.k2
        kk = np.sqrt(grid.k2)
        top = Ps[kk > (2.0 / 3.0) * kk.max()].sum() / max(Ps.sum(), 1e-300)
        return yh, Ekin, E, top

    f = force(psi, u)
    rec = {"t": [], "yrms": [], "ymax": [], "ymed": [], "p10": [], "p90": [], "p99": [], "fpin": [], "Ekin": [],
           "E": [], "top": [], "G": []}
    snaps_w, snaps_t = [], []
    probes = []
    t0 = time.time()
    status = "ok"
    for io in range(nout + 1):
        try:
            yh, Ekin, E, top = diag(psi, p, u, G)
        except (ValueError, FloatingPointError):
            status = "blowup"; break
        if not np.all(np.isfinite(yh)) or yh.max() > 1e6:
            status = "blowup"; break
        rec["t"].append(io * dtout); rec["yrms"].append(float(np.sqrt(np.mean(yh ** 2)))); rec["ymax"].append(float(yh.max()))
        q = np.percentile(yh, [10, 50, 90, 99])
        rec["p10"].append(float(q[0])); rec["ymed"].append(float(q[1])); rec["p90"].append(float(q[2])); rec["p99"].append(float(q[3]))
        rec["fpin"].append(float(np.mean(kern.CT(np.maximum(yh, 1e-300)) > 1.0)))
        rec["Ekin"].append(float(Ekin)); rec["E"].append(float(E)); rec["top"].append(float(top)); rec["G"].append(G.tolist())
        if io in probe_idx:
            try:
                probes.append((io * dtout,) + leaf_two_start(grid, kern, eps, g, psi, u, G))
            except (RuntimeError, ValueError, LinAlgError) as e:
                probes.append((io * dtout, float("inf"), False))
        if io % snap_every == 0:
            w, _ = leaf.fields(u, G)
            snaps_w.append(np.array(w)); snaps_t.append(io * dtout)
        if log and io % int(round(5.0 / dtout)) == 0:
            log(f"      t = {io * dtout:6.2f}: yhat rms {rec['yrms'][-1]:.3e} max {rec['ymax'][-1]:.3e}; E {E:+.4e}, Ekin {Ekin:.3e}; "
                f"refac {leaf.n_refac}, indef {leaf.n_indef}; wall {time.time() - t0:.0f} s")
        if io == nout:
            break
        try:
            for _ in range(m):
                p += 0.5 * dt * f
                psi = psi + dt * p
                u, G, _ = leaf.solve(psi, u, G)
                f = force(psi, u)
                p += 0.5 * dt * f
        except (RuntimeError, ValueError, FloatingPointError) as e:
            status = f"leaf-fail: {e}"; break
        if max_wall and time.time() - t0 > max_wall:
            status = "wall"; break
    out = {"rec": rec, "status": status, "dt": dt, "m": m, "n_refac": leaf.n_refac, "n_indef": leaf.n_indef,
           "max_res": leaf.max_res, "wall": time.time() - t0, "snaps_t": np.array(snaps_t), "snaps_w": np.array(snaps_w),
           "psi": psi, "u": u, "G": G, "p": p, "probes": probes}
    return out


def leaf_two_start(grid, kern, eps, g, psi, u_warm, G_warm):
    """Uniqueness probe: solve the leaf from the warm start and from the healthy start u = psi/eps."""
    la = Leaf(grid, kern, eps, g); lb = Leaf(grid, kern, eps, g)
    ua, Ga, _ = la.solve(psi, u_warm.copy(), G_warm.copy())
    ub, Gb, _ = lb.solve(psi, psi / eps - (psi / eps).mean(), np.zeros(grid.dim))
    wa, _ = la.fields(ua, Ga); wb, _ = lb.fields(ub, Gb)
    num = math.sqrt(sum(((a - b) ** 2).sum() for a, b in zip(wa, wb)))
    den = math.sqrt(sum((a ** 2).sum() for a in wa)) + 1e-300
    Hs = la.hessian(ua, Ga)
    try:
        cho_factor(Hs); pd = True
    except LinAlgError:
        pd = False
    return num / den, pd
