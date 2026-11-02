#!/usr/bin/env python3
"""AN2: triaxial peak of the one-field action's dust in 3D, slow branch, up to the first fold. Criteria: FROZEN_CRITERIA.md.
Mesh, CIC and hold solver copied from ../L1_khronon_pm/khronon_pm.py (read-only there). Background and amplitude copied from
../AN1_aest_nonlinear_dust/an1.py. kappa = 1/2 FITTED. Gravitating field, no particle. No completion, nothing past a fold.
Run: python3 an2.py row KEY MU FOOT SHAPE N ETA LFAC [--mutate]    (SHAPE: 0, A, B)"""
import os, sys, json, time, signal, resource
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_v] = "1"
import numpy as np
import numexpr as ne
from scipy import fft as sfft
from scipy.integrate import solve_ivp, quad, dblquad
from scipy.optimize import brentq
from scipy.special import erf

G = 4.30091e-6; TU = 0.97779; MS2 = 3.24078e-14
AF = {"canonical": 9.3603e-11 / MS2, "alt": 1.1312e-10 / MS2}
H_ = 0.672; RX0, RB0 = 33.2, 33.2 / 5.35
MUTATE = "--mutate" in sys.argv
TAG = "_MUTATE" if MUTATE else ""
HERE = os.path.dirname(os.path.abspath(__file__))
CPU_CAP = 67.5 * 60
STOP = {"flag": False}
signal.signal(signal.SIGTERM, lambda *a: STOP.__setitem__("flag", True))
SETUP = {"1e12": dict(M=1e12, Rt=36.0), "1e15": dict(M=1e15, Rt=1350.0)}


class Bg:  # AN1
    def __init__(s, rm0=RX0 + RB0, h=H_):
        s.H0 = 0.1 * h; rc = 3 * s.H0**2 / (8 * np.pi * G); s.rm0 = rm0; s.Om = rm0 / rc; s.OL = 1 - s.Om
    def a(s, t):
        return (s.Om / s.OL) ** (1 / 3) * np.sinh(1.5 * np.sqrt(s.OL) * s.H0 * t) ** (2 / 3)
    def t(s, a):
        return np.arcsinh(np.sqrt(s.OL / s.Om) * a**1.5) / (1.5 * np.sqrt(s.OL) * s.H0)
    def H(s, a):
        return s.H0 * np.sqrt(s.Om / a**3 + s.OL)
    def D(s, a):  # growing mode
        return s.H(a) / s.H0 * quad(lambda x: 1 / (x * s.H(x) / s.H0) ** 3, 0, a, epsabs=0, epsrel=1e-11)[0]


def gbar(x):  # AN1
    x = float(x)
    return 3 / x**3 * (np.sqrt(np.pi / 2) * erf(x / np.sqrt(2)) - x * np.exp(-x**2 / 2))


def edge_amp(bg, Mtot, zi=20.0):  # AN1
    ai = 1 / (1 + zi); q = (3 * Mtot / (4 * np.pi * bg.rm0)) ** (1 / 3)
    ti, Hi, t0 = bg.t(ai), bg.H(ai), bg.t(1.0); L = bg.OL * bg.H0**2
    def coll(d):
        r = ai * q * (1 - d / 3); v = Hi * ai * q * (1 - 2 * d / 3)
        ev = lambda t, y: y[0] - 1e-5 * r
        ev.terminal = True
        s = solve_ivp(lambda t, y: [y[1], -G * Mtot / y[0]**2 + L * y[0]], (ti, 3 * t0), [r, v], events=ev, rtol=1e-10, atol=1e-12 * r, method="DOP853")
        return s.t_events[0][0] if len(s.t_events[0]) else np.inf
    return brentq(lambda d: coll(d) - t0, 1e-3, 0.5, xtol=1e-8), q


def peak_amp(key):
    bg = Bg(); M = SETUP[key]["M"]; de, qt = edge_amp(bg, M)
    RG = (M / ((2 * np.pi) ** 1.5 * bg.rm0)) ** (1 / 3)
    return dict(d0=de / gbar(qt / RG), de=de, qt=qt, RG=RG)


# ---------- peak statistics (BBKS 1986, from memory, PROVISIONAL; KN guards it)
def bbks_f(x):
    a = np.sqrt(5 / 2) * x
    return (x**3 - 3 * x) / 2 * (erf(a) + erf(a / 2)) + np.sqrt(2 / (5 * np.pi)) * ((31 * x**2 / 4 + 8 / 5) * np.exp(-5 * x**2 / 8) + (x**2 / 2 - 8 / 5) * np.exp(-5 * x**2 / 2))
def bbks_W(e, p):
    return e * (e**2 - p**2) * (1 - 2 * p) * ((1 + p) ** 2 - 9 * e**2)
def bbks_P(e, p, x):
    return 9 * 5**2.5 / np.sqrt(2 * np.pi) * x**8 / bbks_f(x) * np.exp(-2.5 * x**2 * (3 * e**2 + p**2)) * bbks_W(e, p)
def bbks_grid(x, n=1601):
    e = np.linspace(0, 0.5, n); p = np.linspace(-0.25, 0.5, int(n * 1.5))
    E, P = np.meshgrid(e, p, indexing="ij")
    dom = (P <= E) & (P >= -E) & (E <= 0.5) & (((E <= 0.25) & (P >= -E)) | ((E > 0.25) & (P >= 3 * E - 1)))
    return e, p, np.where(dom, bbks_P(E, P, x), 0.0)
def KN():
    out = {}
    for x in (1.0, 2.0, 3.0, 5.0):
        e, p, Z = bbks_grid(x); out[str(x)] = float(np.trapz(np.trapz(Z, p, axis=1), e))
    return dict(norm=out, ok=all(abs(v - 1) <= 1e-3 for v in out.values()))


def spectral_moments(R_kpc):
    d = np.load(os.path.join(HERE, "..", "L1_khronon_pm", "work", "class_modelB_pk.npz"))
    k, P = d["KS"], d["Pk"]; R = R_kpc / 1000 * 0.6856426703851345
    W2 = np.exp(-(k * R) ** 2); lk = np.log(k)
    mom = lambda j: np.sqrt(np.trapz(k**3 * P * W2 * k ** (2 * j) / (2 * np.pi**2), lk))
    return mom(0), mom(1), mom(2)


def shapes(key):
    A = peak_amp(key); bg = Bg()
    s0, s1, s2 = spectral_moments(A["RG"]); gam = s1**2 / (s0 * s2)
    nu = A["d0"] * bg.D(1.0) / bg.D(1 / 21) / s0
    xs = np.linspace(0.02, 12 + nu, 6000); w = np.maximum(bbks_f(xs), 0) * np.exp(-(xs - gam * nu) ** 2 / (2 * (1 - gam**2)))
    xbar = float(np.trapz(xs * w, xs) / np.trapz(w, xs))
    e, p, Z = bbks_grid(xbar)
    i, j = np.unravel_index(np.argmax(Z), Z.shape); eA, pA = float(e[i]), float(p[j])
    Pe = np.trapz(Z, p, axis=1); C = np.concatenate([[0], np.cumsum(0.5 * (Pe[1:] + Pe[:-1]) * np.diff(e))]); C /= C[-1]
    eB = float(np.interp(0.9, C, e)); iB = int(np.argmin(np.abs(e - eB))); pB = float(p[np.argmax(Z[iB])])
    out = dict(sigma0=float(s0), gamma=float(gam), nu=float(nu), xbar=xbar, A=dict(e=eA, p=pA), B=dict(e=eB, p=pB), d0=A["d0"], RG=A["RG"], qt=A["qt"])
    for nm in "AB":
        ee, pp = out[nm]["e"], out[nm]["p"]; l = np.array([1 + 3 * ee + pp, 1 - 2 * pp, 1 - 3 * ee + pp])
        R = 1 / np.sqrt(l); R *= A["RG"] / np.prod(R) ** (1 / 3); out[nm]["R"] = R.tolist(); out[nm]["axis_ratio"] = float(R[2] / R[0])
    return out


# ---------- copied from L1_khronon_pm/khronon_pm.py
class Mesh:
    def __init__(self, N, L):
        self.N, self.L, self.dx = N, L, L / N
        k1 = 2 * np.pi * sfft.fftfreq(N, d=self.dx); kz = 2 * np.pi * sfft.rfftfreq(N, d=self.dx)
        nyq = np.pi / self.dx
        g1 = np.where(np.abs(np.abs(k1) - nyq) < 1e-9 * nyq, 0.0, k1); gz = np.where(np.abs(kz - nyq) < 1e-9 * nyq, 0.0, kz)
        self.gk = (g1[:, None, None], g1[None, :, None], gz[None, None, :])
        self.k2 = k1[:, None, None] ** 2 + k1[None, :, None] ** 2 + kz[None, None, :] ** 2
        self.ik2 = np.zeros_like(self.k2); self.ik2[self.k2 > 0] = 1.0 / self.k2[self.k2 > 0]
    def fft(self, x): return sfft.rfftn(x, workers=1)
    def ifft(self, xk): return sfft.irfftn(xk, s=(self.N,) * 3, workers=1)
    def grad_c(self, xk, c): return self.ifft(1j * self.gk[c] * xk)
    def div_k(self, F):
        out = None
        for c in range(3):
            t = 1j * self.gk[c] * self.fft(F[c]); out = t if out is None else out + t
        return out


def solve_hold(m, Sk, m2, g0, xi0=None, tol=1e-6, maxit=400, depth=5, coef="hold"):
    N = m.N; den = m.k2 + m2
    den_inv = np.zeros_like(den); den_inv[den > 0] = -1.0 / den[den > 0]
    def T(xi):
        xk = m.fft(xi); g = [m.grad_c(xk, c) for c in range(3)]; del xk
        gx, gy, gz = g; gm = ne.evaluate("sqrt(gx*gx + gy*gy + gz*gz)"); g0_ = float(g0)
        mu = ne.evaluate("gm / (g0_ + gm)") if coef == "hold" else ne.evaluate("1.0 - gm / (g0_ + gm)")
        del gm
        r = Sk.copy()
        for c in range(3):
            gc = g[c]; r += 1j * m.gk[c] * m.fft(ne.evaluate("mu * gc"))
        del g, mu
        r *= den_inv
        return m.ifft(r)
    x = np.zeros((N, N, N)) if xi0 is None else xi0.copy()
    hist_dx, hist_df = [], []; x_prev = f_prev = None; info = dict(iters=0, res=float("inf"), converged=False)
    for it in range(1, maxit + 1):
        Tx = T(x); nTx = float(np.sqrt(np.vdot(Tx.ravel(), Tx.ravel()).real))
        f = ne.evaluate("Tx - x"); nf = float(np.sqrt(np.vdot(f.ravel(), f.ravel()).real))
        res = nf / nTx if nTx > 0 else 0.0; info.update(iters=it, res=res)
        if res <= tol:
            info["converged"] = True; x = Tx; break
        if it == maxit:
            x = Tx; break
        del Tx
        if x_prev is not None:
            hist_dx.append(ne.evaluate("x - x_prev")); hist_df.append(ne.evaluate("f - f_prev"))
            if len(hist_dx) > depth: hist_dx.pop(0); hist_df.pop(0)
        x_prev, f_prev = x, f
        if hist_df:
            k_ = len(hist_df); A = np.empty((k_, k_)); b = np.empty(k_)
            for i in range(k_):
                b[i] = np.vdot(hist_df[i].ravel(), f.ravel()).real
                for j in range(i, k_):
                    A[i, j] = A[j, i] = np.vdot(hist_df[i].ravel(), hist_df[j].ravel()).real
            A += 1e-12 * np.trace(A) * np.eye(k_)
            gam = np.linalg.solve(A, b); xn = x + f
            for i in range(k_):
                gi = float(gam[i]); dxi, dfi = hist_dx[i], hist_df[i]
                xn = ne.evaluate("xn - gi * (dxi + dfi)")
            x = xn
        else:
            x = x + f
    return x, info


def solve_aqual_projection(m, Sb_k, a0c, tol=1e-9, maxit=300):
    phiN = -Sb_k * m.ik2
    GN = [m.grad_c(phiN, c) for c in range(3)]; GNk = [m.fft(GN[c]) for c in range(3)]
    def nu_apply(U):
        um = np.sqrt(U[0]**2 + U[1]**2 + U[2]**2); y = np.maximum(um, 1e-300) / a0c; nu = 0.5 * (1 + np.sqrt(1 + 4 / y))
        return [U[c] * nu for c in range(3)]
    def mu_apply(Gv):
        gm = np.sqrt(Gv[0]**2 + Gv[1]**2 + Gv[2]**2); x = gm / a0c; mu = x / (1 + x)
        return [Gv[c] * mu for c in range(3)]
    def longit(Fk):
        kd = sum(m.gk[c] * Fk[c] for c in range(3))
        return [m.gk[c] * kd * m.ik2 for c in range(3)]
    Gv = [m.ifft(t) for t in longit([m.fft(t) for t in nu_apply(GN)])]; info = dict(iters=0, res=None)
    for it in range(1, maxit + 1):
        U = mu_apply(Gv); Uk = [m.fft(U[c]) for c in range(3)]; Lk = longit(Uk)
        Up = [m.ifft(GNk[c] + Uk[c] - Lk[c]) for c in range(3)]
        Gn = [m.ifft(t) for t in longit([m.fft(t) for t in nu_apply(Up)])]
        num = sum(float(np.sum((Gn[c] - Gv[c]) ** 2)) for c in range(3)); den = sum(float(np.sum(Gn[c] ** 2)) for c in range(3))
        Gv = Gn; info.update(iters=it, res=np.sqrt(num / den))
        if info["res"] <= tol: break
    return Gv, GN, info


def deposit(m, x):
    """x: (3, n) positions; CIC -> delta (L1, in chunks of n, float64)."""
    N = m.N; rho = np.zeros(N**3, np.float64); n = x.shape[1]; CH = 1 << 21
    for s in range(0, n, CH):
        u = np.mod(x[:, s:s + CH], m.L) / m.dx; i0 = np.floor(u).astype(np.int64); w = u - i0; i1 = (i0 + 1) % N; i0 = i0 % N
        for cx in (0, 1):
            ix = i1[0] if cx else i0[0]; wx = w[0] if cx else 1 - w[0]
            for cy in (0, 1):
                iy = i1[1] if cy else i0[1]; wy = w[1] if cy else 1 - w[1]
                for cz in (0, 1):
                    iz = i1[2] if cz else i0[2]; wz = w[2] if cz else 1 - w[2]
                    rho += np.bincount((ix * N + iy) * N + iz, weights=wx * wy * wz, minlength=N**3)
    rho *= N**3 / n; rho -= 1.0
    return rho.reshape(N, N, N)


def interp_acc(m, x, f3):
    """CIC force interpolation, (3, n)."""
    N = m.N; flats = [f.reshape(-1) for f in f3]; out = np.zeros(x.shape); CH = 1 << 21
    for s in range(0, x.shape[1], CH):
        u = np.mod(x[:, s:s + CH], m.L) / m.dx; i0 = np.floor(u).astype(np.int64); w = u - i0; i1 = (i0 + 1) % N; i0 = i0 % N
        for cx in (0, 1):
            ix = i1[0] if cx else i0[0]; wx = w[0] if cx else 1 - w[0]
            for cy in (0, 1):
                iy = i1[1] if cy else i0[1]; wy = w[1] if cy else 1 - w[1]
                for cz in (0, 1):
                    iz = i1[2] if cz else i0[2]; wz = w[2] if cz else 1 - w[2]
                    idx = (ix * N + iy) * N + iz; ww = wx * wy * wz
                    for c in range(3): out[c, s:s + CH] += ww * flats[c][idx]
    return out


# ---------- fold tracker
PERMS = [(0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)]
PSIGN = [1, -1, -1, 1, 1, -1]


def tet_dets(disp, dq):
    """disp (3,N,N,N) unwrapped, lattice dq. Returns the 6 Kuhn tet dets of each lattice cube."""
    return list(iter_dets(disp, dq))


def iter_dets(disp, dq):
    D = {}
    for j in range(3):
        for c in range(3):
            d = np.roll(disp[c], -1, axis=j) - disp[c]
            d /= dq
            if c == j: d += 1.0
            D[(c, j)] = d
    for perm, sg in zip(PERMS, PSIGN):
        col = []
        for k, axis in enumerate(perm):
            sh = [0, 0, 0]
            for pa in perm[:k]: sh[pa] = -1
            col.append([np.roll(D[(c, axis)], sh, axis=(0, 1, 2)) if any(sh) else D[(c, axis)] for c in range(3)])
        a, b, cc = col[0]; d, e, f = col[1]; g, h, i = col[2]
        yield sg * ne.evaluate("a*(e*i-f*h)-d*(b*i-c_*h)+g*(b*f-c_*e)", local_dict=dict(a=a, b=b, c_=cc, d=d, e=e, f=f, g=g, h=h, i=i))
        del col, a, b, cc, d, e, f, g, h, i


class Tracker:
    def __init__(s, N, dq, qmask, mutate=False):
        s.N, s.dq, s.qmask, s.mutate = N, dq, qmask, mutate
        s.prev = {"any": None, "q": None}
        s.cand = {"any": None, "q": None}
        s.fold = {"any": None, "q": None}
        s.transient = 0
    def scan(s, disp):
        m_all = None
        for d in iter_dets(disp, s.dq):
            if s.mutate: d = np.abs(d)
            m_all = d if m_all is None else np.minimum(m_all, d)
        ia = int(np.argmin(m_all)); da = float(m_all.flat[ia]); ninv_a = int(np.sum(m_all <= 0))
        mq = np.where(s.qmask, m_all, np.inf); iq = int(np.argmin(mq)); dq_ = float(mq.flat[iq]); ninv_q = int(np.sum(mq <= 0))
        return dict(any=(da, ia, ninv_a), q=(dq_, iq, ninv_q))
    def update(s, t_prev, t_now, sc):
        """returns list of regions newly confirmed"""
        new = []
        for rg in ("any", "q"):
            d, i, ninv = sc[rg]
            if s.fold[rg] is None:
                c = s.cand[rg]
                if c is not None:
                    if d <= 0:
                        s.fold[rg] = c; new.append(rg)
                    else:
                        s.transient += 1; s.cand[rg] = None
                elif d <= 0 and s.prev[rg] is not None and s.prev[rg] > 0:
                    dp = s.prev[rg]
                    s.cand[rg] = dict(t=t_prev + (t_now - t_prev) * dp / (dp - d), idx=i, det_prev=dp, det_now=d, t_prev=t_prev, t_now=t_now)
            s.prev[rg] = d
        return new


def fold_shape(disp_prev, idx, N, dq):
    i = np.unravel_index(idx, (N, N, N)); J = np.eye(3)
    for c in range(3):
        for j in range(3):
            ip = list(i); im = list(i); ip[j] = (ip[j] + 1) % N; im[j] = (im[j] - 1) % N
            J[c, j] += (disp_prev[c][tuple(ip)] - disp_prev[c][tuple(im)]) / (2 * dq)
    ev = np.sort(np.linalg.eigvalsh(0.5 * (J + J.T)))
    nm = "sheet" if ev[1] > 0.25 else ("filament" if ev[2] > 0.25 else "point")
    return nm, ev.tolist()


# ---------- baryon stop targets, AN1
def stop_radii(key, cum):
    rf = np.full_like(cum, np.inf)
    if key == "1e12":
        Md, Rd = 6.72e10, 3.565
        x = np.logspace(-4, 2, 4000); M = Md * (1 - (1 + x) * np.exp(-x)); s = cum <= Md * 0.9999
        rf[s] = Rd * np.interp(cum[s], M, x)
    else:
        R5, rcg, Mg = 1350.0, 0.15 * 1350.0, 1.19e14
        x = np.logspace(-3, np.log10(R5), 4000); P = lambda r: r - rcg * np.arctan(r / rcg); M = Mg * P(x) / P(R5); s = cum <= Mg
        rf[s] = np.interp(cum[s], M, x)
    return rf


def glaw(gN, a0):
    return 0.5 * (gN + np.sqrt(gN**2 + 4 * gN * a0))


# ---------- engine
class Sim:
    def __init__(s, N, L, a0, mu_kpc, eta, t0, bg, disp, mom, key=None, Rt=None, rf=None, dust=False, c=None, qt=None, qmask_fn=None, mutate=None):
        s.N, s.L, s.a0, s.mu, s.eta, s.t, s.bg = N, L, a0, mu_kpc, eta, t0, bg
        s.m = Mesh(N, L); s.dq = L / N; s.dust = dust
        s.mutate = MUTATE if mutate is None else mutate
        i = (np.arange(N) + 0.5) * s.dq
        Q = np.meshgrid(i, i, i, indexing="ij"); s.q = np.stack(Q).astype(np.float64)
        s.c = L / 2 if c is None else c
        s.dd, s.pd = disp.copy(), mom.copy()
        s.db, s.pb = disp.copy(), mom.copy()
        s.pin = np.zeros((N, N, N), bool)
        s.rpin = None
        s.rf = rf
        s.Rt = Rt
        s.mpd = RX0 * s.dq**3; s.mpb = RB0 * s.dq**3
        # cube centroid = lattice base + dq/2 on each axis
        s.rc2 = ((s.q + 0.5 * s.dq - s.c) ** 2).sum(0)
        qmask = (s.rc2 <= (qt if qt else 1e99) ** 2) if qmask_fn is None else qmask_fn(s.q + 0.5 * s.dq - s.c)
        s.tr = Tracker(N, s.dq, qmask, mutate=s.mutate)
        s.xi = None; s.nstep = 0; s.warn = 0; s.iters = 0; s.max_y = 0.0; s.reach = None
        s.status = None; s.reads = None; s.disp_prev = None; s.read_prev = None; s.max_iters = 0
        s.cpu0 = 0.0

    def posd(s): return (s.q + s.dd).reshape(3, -1)
    def posb(s): return (s.q + s.db).reshape(3, -1)

    def solve(s):
        a = float(s.bg.a(s.t)); m = s.m
        dd = deposit(m, s.posd()); db = deposit(m, s.posb())
        Sd = 4 * np.pi * G / a * RX0 * dd; Sm = Sd + 4 * np.pi * G / a * RB0 * db
        Smk = m.fft(Sm); phi = -Smk * m.ik2
        s.fb = [-m.grad_c(phi, c) for c in range(3)]
        if s.dust:
            s.fd = s.fb; s.gx = None; s.ygrid = None; s.rhoD = dd
            return dict(res=0.0)
        xi, info = solve_hold(m, m.fft(Sd), (a * s.mu) ** 2, a * s.a0, xi0=s.xi)
        s.xi = xi; xk = m.fft(xi); gx = [m.grad_c(xk, c) for c in range(3)]
        sg = 1.0 if not s.mutate else -1.0
        s.fd = [s.fb[c] + sg * gx[c] for c in range(3)]
        gm = np.sqrt(gx[0]**2 + gx[1]**2 + gx[2]**2)
        s.ygrid = gm / (a * s.a0); s.rhoD = dd
        s.nstep_iters = info["iters"]; s.iters += info["iters"]; s.max_iters = max(s.max_iters, info["iters"])
        s.max_y = max(s.max_y, float(s.ygrid.max()))
        return info

    def dt(s):
        a = float(s.bg.a(s.t)); H = s.bg.H(a); fly = ~s.pin
        vm = max(float(np.sqrt((s.pd**2).sum(0).max())), float(np.sqrt((s.pb[:, fly]**2).sum(0).max())) if fly.any() else 0) / a**2
        Fm = max(float(np.sqrt(s.fd[0]**2 + s.fd[1]**2 + s.fd[2]**2).max()), float(np.sqrt(s.fb[0]**2 + s.fb[1]**2 + s.fb[2]**2).max())) / a**2
        ts = [s.eta * s.dq / (vm + 1e-30), s.eta * np.sqrt(s.dq / (Fm + 1e-30)), 0.2 * s.eta / H]
        if not s.dust:
            kp = np.pi / (s.dq * a); mu2 = s.mu**2; y = s.ygrid; rho = np.maximum(RX0 / a**3 * (1 + s.rhoD), 0)
            r = ne.evaluate("kp*kp/(kp*kp/(1+y)**2+mu2)")
            om2 = 4 * np.pi * G * rho * np.maximum(r, np.abs(r - 1))
            ts.append(10 * s.eta / np.sqrt(om2.max() + 1e-300))
        s.dtv = ts
        return min(ts)

    def stop_baryons(s, a):
        if s.rf is None: return
        H = s.bg.H(a); fly = ~s.pin
        x = (s.q + s.db - s.c)[:, fly]; r = a * np.sqrt((x**2).sum(0)); rs = np.maximum(r, 1e-30)
        v = (a * (x) * H + s.pb[:, fly] / a)
        vr = (a * x * v).sum(0) / rs
        rf = s.rf[fly]; fin = np.isfinite(rf)
        hit = (vr <= 0) & ((fin & (r <= rf)) | ~fin)
        if not hit.any(): return
        # stopped: fixed physical vector r_pin; rf finite -> at rf along own direction, else at own r
        rtarget = np.where(fin, rf, r)
        if s.rpin is None: s.rpin = np.zeros_like(s.db)
        rv = a * x * (rtarget / rs)
        idx = np.where(fly)
        for c in range(3):
            s.rpin[c][idx[0][hit], idx[1][hit], idx[2][hit]] = rv[c][hit]
        s.pin[idx[0][hit], idx[1][hit], idx[2][hit]] = True

    def read(s, a):
        X = s.Rt
        rd = a * np.sqrt(((s.q + s.dd - s.c) ** 2).sum(0)); rb = a * np.sqrt(((s.q + s.db - s.c) ** 2).sum(0))
        nd = int((rd <= X).sum()); nb = int((rb <= X).sum()); Md, Mb = nd * s.mpd, nb * s.mpb
        gN = G * Mb / X**2; Mph = (glaw(gN, s.a0) - gN) * X**2 / G
        return dict(a=a, t=s.t, nd=nd, nb=nb, Md=Md, Mb=Mb, Mph=float(Mph))

    def step(s):
        tp = s.t; dt = s.dt(); a0_ = float(s.bg.a(tp)); a1_ = float(s.bg.a(tp + dt))
        fly = ~s.pin
        ad = interp_acc(s.m, s.posd(), s.fd); s.pd += 0.5 * dt * ad.reshape(s.pd.shape)
        ab = interp_acc(s.m, s.posb(), s.fb).reshape(s.pb.shape)
        for c in range(3): s.pb[c][fly] += 0.5 * dt * ab[c][fly]
        del ad, ab
        Dd = quad(lambda t: s.bg.a(t) ** -2, tp, tp + dt, epsabs=0, epsrel=1e-10)[0]
        s.disp_prev = s.dd.copy()
        s.dd += Dd * s.pd
        for c in range(3): s.db[c][fly] += Dd * s.pb[c][fly]
        s.t = tp + dt
        s.stop_baryons(a1_)
        if s.pin.any():
            xp = s.rpin / a1_
            for c in range(3):
                s.db[c][s.pin] = xp[c][s.pin] + s.c - s.q[c][s.pin]
                s.pb[c][s.pin] = 0.0
        info = s.solve()
        fly = ~s.pin
        ad = interp_acc(s.m, s.posd(), s.fd); s.pd += 0.5 * dt * ad.reshape(s.pd.shape)
        ab = interp_acc(s.m, s.posb(), s.fb).reshape(s.pb.shape)
        for c in range(3): s.pb[c][fly] += 0.5 * dt * ab[c][fly]
        del ad, ab
        s.nstep += 1
        return tp, info

    def save(s, fn):
        d = dict(dd=s.dd, pd=s.pd, db=s.db, pb=s.pb, pin=s.pin, t=s.t, nstep=s.nstep, warn=s.warn, iters=s.iters, max_y=s.max_y,
                 xi=s.xi if s.xi is not None else np.zeros(1), rpin=s.rpin if s.rpin is not None else np.zeros(1),
                 extra=json.dumps(dict(prev=s.tr.prev, cand=s.tr.cand, fold=s.tr.fold, transient=s.tr.transient, reach=s.reach, read_prev=s.read_prev, cpu=s.cpu0 + time.process_time(), max_iters=s.max_iters)),
                 disp_prev=s.disp_prev if s.disp_prev is not None else np.zeros(1),
                 fd=np.stack(s.fd), fb=np.stack(s.fb), rhoD=s.rhoD, ygrid=s.ygrid if s.ygrid is not None else np.zeros(1))
        tmp = fn + ".tmp"
        with open(tmp, "wb") as f:
            np.savez(f, **d); f.flush(); os.fsync(f.fileno())
        os.replace(tmp, fn)

    def load(s, fn):
        d = np.load(fn)
        s.dd, s.pd, s.db, s.pb, s.pin = d["dd"], d["pd"], d["db"], d["pb"], d["pin"]
        s.t, s.nstep, s.warn, s.iters, s.max_y = float(d["t"]), int(d["nstep"]), int(d["warn"]), int(d["iters"]), float(d["max_y"])
        s.xi = d["xi"] if d["xi"].size > 1 else None; s.rpin = d["rpin"] if d["rpin"].size > 1 else None
        s.disp_prev = d["disp_prev"] if d["disp_prev"].size > 1 else None
        s.fd, s.fb, s.rhoD = list(d["fd"]), list(d["fb"]), d["rhoD"]; s.ygrid = d["ygrid"] if d["ygrid"].size > 1 else None
        s.resumed = True
        e = json.loads(str(d["extra"]))
        s.tr.prev, s.tr.cand, s.tr.fold, s.tr.transient, s.reach, s.read_prev, s.cpu0, s.max_iters = e["prev"], e["cand"], e["fold"], e["transient"], e["reach"], e["read_prev"], e["cpu"], e["max_iters"]

    def run(s, tmax, ckpt=None, maxsteps=20000, cap=CPU_CAP, kill_at=None, log=None, stop_on="q"):
        if ckpt and os.path.exists(ckpt):
            s.load(ckpt)
        if not getattr(s, "resumed", False): s.solve()
        if s.tr.prev["any"] is None:
            sc = s.tr.scan(s.dd); s.tr.prev["any"], s.tr.prev["q"] = sc["any"][0], sc["q"][0]
        out = None
        while True:
            if s.t >= tmax:
                out = dict(status="NO FOLD"); break
            if kill_at is not None and s.nstep == kill_at: STOP["flag"] = True
            if STOP["flag"]:
                if ckpt: s.save(ckpt)
                return dict(status="PREEMPTED", nstep=s.nstep, t=s.t)
            if s.cpu0 + time.process_time() > cap:
                if ckpt: s.save(ckpt)
                return dict(status="CPU_CAP", nstep=s.nstep, t=s.t, cpu_s=s.cpu0 + time.process_time())
            if s.nstep >= maxsteps:
                out = dict(status="UNRESOLVED", reason="steps"); break
            a_before = float(s.bg.a(s.t))
            cur_read = s.read(a_before) if s.Rt else None
            tp, info = s.step()
            res = info.get("res", 0.0)
            if res > 1e-5:
                out = dict(status="UNRESOLVED", reason="hold residual %.2e" % res); break
            if res > 1e-6: s.warn += 1
            sc = s.tr.scan(s.dd)
            if s.Rt:
                if s.tr.fold["q"] is None and s.tr.cand["q"] is None:
                    s.read_prev = cur_read
                    if cur_read["Md"] >= cur_read["Mph"] and cur_read["nd"] >= 8 and s.reach is None:
                        s.reach = cur_read
            prior_prevdisp = s.disp_prev
            new = s.tr.update(tp, s.t, sc)
            for rg in ("any", "q"):
                c = s.tr.cand[rg]
                if c is not None and "shape" not in c:
                    c["shape"], c["eig"] = fold_shape(prior_prevdisp, c["idx"], s.N, s.dq)
            if log and s.nstep % log == 0:
                print(f"  step {s.nstep} z {1 / s.bg.a(s.t) - 1:.3f} det {sc['any'][0]:.3e} q {sc['q'][0]:.3e} it {getattr(s, 'nstep_iters', 0)} ymax {0 if s.ygrid is None else s.ygrid.max():.2f} pin {int(s.pin.sum())} cpu {s.cpu0 + time.process_time():.0f}", flush=True)
            if s.tr.fold[stop_on] is not None:
                out = dict(status="FOLD"); break
        out.update(nstep=s.nstep, t_end=s.t, warn=s.warn, transient=s.tr.transient, iters=s.iters, max_iters=s.max_iters, max_y=s.max_y, cpu_s=s.cpu0 + time.process_time(),
                   rss_gb=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2**30)
        for rg in ("any", "q"):
            f = s.tr.fold[rg]
            if f:
                i = np.unravel_index(f["idx"], (s.N,) * 3); r = (s.q[:, i[0], i[1], i[2]] + 0.5 * s.dq - s.c)
                out[f"fold_{rg}"] = dict(t_Gyr=f["t"] * TU, z=float(1 / s.bg.a(f["t"]) - 1), shape=f.get("shape"), eig=f.get("eig"), q_kpc=r.tolist(), q_over_qt=None, idx=[int(v) for v in i],
                                         r_phys_kpc=float(s.bg.a(f["t"]) * np.sqrt(((s.q + s.disp_prev - s.c)[:, i[0], i[1], i[2]] ** 2).sum())))
        out["read"] = s.read_prev; out["reach"] = s.reach
        return out


def build_row(key, mu, foot, shape, N, eta, Lfac, dust=False):
    P = peak_amp(key); bg = Bg(); qt, RG, d0 = P["qt"], P["RG"], P["d0"]; L = Lfac * qt
    if shape == "0":
        R = [RG] * 3; sh = dict(e=0.0, p=0.0, R=R)
    else:
        sh = json.load(open(os.path.join(HERE, "an2_shapes.json")))[key][shape]; R = sh["R"]
    ai = 1 / 21.0; dq = L / N; i = (np.arange(N) + 0.5) * dq - L / 2
    X, Y, Z = np.meshgrid(i, i, i, indexing="ij")
    dl = d0 * np.exp(-0.5 * (X**2 / R[0]**2 + Y**2 / R[1]**2 + Z**2 / R[2]**2))
    m = Mesh(N, L); dk = m.fft(dl - dl.mean())
    disp = np.stack([m.ifft(1j * m.gk[c] * dk * m.ik2) for c in range(3)])
    mom = ai**2 * bg.H(ai) * disp
    # baryon rank, ellipsoidal Lagrangian radius
    me = (X**2 / R[0]**2 + Y**2 / R[1]**2 + Z**2 / R[2]**2).ravel()
    o = np.argsort(me, kind="stable"); mpb = RB0 * dq**3
    cum = np.empty(N**3); cum[o] = (np.arange(N**3) + 1) * mpb
    rf = stop_radii(key, cum).reshape(N, N, N)
    del dl, dk, me, o, cum, X, Y, Z
    S = Sim(N, L, AF[foot], mu * 1e-3, eta, bg.t(ai), bg, disp, mom, Rt=SETUP[key]["Rt"], rf=rf, dust=dust, qt=qt)
    S.qt = qt; S.t0 = bg.t(1.0); S.meta = dict(d0=d0, RG=RG, qt=qt, L=L, R=R, e=sh["e"], p=sh["p"])
    return S


def run_row(key, mu, foot, shape, N, eta, Lfac, kill_at=None, log=None, cap=CPU_CAP):
    tag = f"{key}_{mu}_{foot}_{shape}_N{N}_e{eta}_L{Lfac}{TAG}"
    ck = os.path.join(HERE, f"ckpt_{tag}.npz"); fn = os.path.join(HERE, f"an2_rows{TAG}.jsonl")
    S = build_row(key, mu, foot, shape, N, eta, Lfac)
    o = S.run(S.t0, ckpt=ck, kill_at=kill_at, log=log, cap=cap)
    o.update(id=tag, key=key, mu=mu, foot=foot, shape=shape, N=N, eta=eta, Lfac=Lfac, **S.meta)
    if o["status"] in ("PREEMPTED", "CPU_CAP"):
        print(json.dumps(o), flush=True)
        return o
    if os.path.exists(ck): os.remove(ck)
    with open(fn, "a") as f:
        f.write(json.dumps(o) + "\n")
    print(json.dumps({k: v for k, v in o.items() if k in ("id", "status", "fold_any", "fold_q", "read", "reach", "nstep", "cpu_s", "rss_gb", "max_y", "max_iters", "warn", "transient", "reason")}), flush=True)
    return o


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if a[0] == "row":
        log = 25 if "--log" in sys.argv else None
        o = run_row(a[1], float(a[2]), a[3], a[4], int(a[5]), float(a[6]), int(a[7]), log=log)
        sys.exit(75 if o["status"] == "PREEMPTED" else (76 if o["status"] == "CPU_CAP" else 0))
    elif a[0] == "shapes":
        s = {k: shapes(k) for k in SETUP}
        json.dump(s, open(os.path.join(HERE, "an2_shapes.json"), "w"), indent=1); print(json.dumps(s, indent=1))
