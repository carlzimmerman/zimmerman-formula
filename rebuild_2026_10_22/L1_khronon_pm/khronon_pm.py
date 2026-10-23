#!/usr/bin/env python3
"""khronon_pm.py: the L1 Khronon-native particle-mesh engine (FROZEN_CRITERIA.md §1, AMENDMENT A1).

Equations (BS24's post-Newtonian system as transcribed in real_research/bs_khronon_2026/BSK1_moving_source_gate.py,
comoving, mean-subtracted, code units: x in Mpc/h, time 1/H0, velocity 100 km/s, potentials in (100 km/s)^2):
    lap Phi                                  = (3/2)(Om/a) delta_m          (metric potential, all mass)
    div[(1 - mu(x)) grad Xi] - a^2 muK^2 Xi  = (3/2)(Otau/a) delta_tau      (hold equation, J = J_x, mu = x/(1+x))
    x = |grad Xi| / (a a0_code)                                              (khronon congruence acceleration / a0)
    baryon particles: dp/dt = -grad Phi;   khronon particles: dp/dt = -grad(Phi - Xi)
Modes: KX (full J_x, nonlinear solve), LIN (J_Y = -1), GRJ (J = GR, finite muK: Xi = -S/(a muK)^2), S0 (Xi = 0, dust ICs).
No settling, no relocation, no QUMOND phantom, no nu_mono.  kappa = 1/2 FITTED; footings never pooled; no dark-matter particle.

Usage (production, AMENDMENT A1):
    python3 khronon_pm.py run --mode KX --foot canonical --muK 14.8 --N 512 --L 100 --zi 49 --nseed 512 --threads 8 [--resume]
    python3 khronon_pm.py estimate --N 512
SIGTERM: finish the current step, checkpoint, exit 0.  --resume: continue from the latest checkpoint (bit-identical).
"""
import os, sys, json, math, time, signal, hashlib, threading, subprocess, io, argparse
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np
import numexpr as ne
from scipy import fft as sfft
from scipy.integrate import quad, solve_ivp

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
WORK = os.environ.get("L1_WORK", os.path.join(HERE, "work"))
MPC = 3.0856775814913673e22
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}           # m/s^2 (doors BRIEF footings)
G_CODE = 4.30091e-13                                        # (Mpc/h)(100 km/s)^2/(Msun/h)
THREADS = [1]
POOL = [None]

def set_threads(t):
    THREADS[0] = int(t); ne.set_num_threads(int(t))
    if int(t) > 1:
        from concurrent.futures import ThreadPoolExecutor
        POOL[0] = ThreadPoolExecutor(int(t))

# ================================================================ background
class Background:
    def __init__(self, name, Om, Ob, h, Or):
        self.name, self.Om, self.Ob, self.h, self.Or = name, Om, Ob, h, Or
        self.Otau = Om - Ob; self.OL = 1.0 - Om - Or
        self.fb = Ob / Om; self.ftau = 1.0 - self.fb
        self.acc_unit = 1e10 * h / MPC                    # (100 km/s)^2 / (Mpc/h) in m/s^2
    def E(self, a):
        return math.sqrt(self.Om / a ** 3 + self.Or / a ** 4 + self.OL)
    def a0c(self, foot):
        return A0[foot] / self.acc_unit
    def kick(self, a1, a2):
        return quad(lambda x: 1.0 / (x * x * self.E(x)), a1, a2, epsabs=0, epsrel=1e-12)[0]
    def drift(self, a1, a2):
        return quad(lambda x: 1.0 / (x ** 3 * self.E(x)), a1, a2, epsabs=0, epsrel=1e-12)[0]
    def desc(self):
        return dict(name=self.name, Om=self.Om, Ob=self.Ob, Otau=self.Otau, h=self.h, Or=self.Or, OL=self.OL)

H_B = 0.6856426703851345; OM_B = 0.2976015949416498; WB_C2B = 0.02230806312032179     # CFG886 / C2 c2b (F3 model B)
LNAS_C2B, NS_C2B, TAU_C2B = 3.0493480900154184, 0.9618333380441444, 0.056275828999093405
MODEL_B = Background("B_cfg886", OM_B, WB_C2B / H_B ** 2, H_B, 4.18e-5 / H_B ** 2)
CFG596_BG = Background("CFG596_planck18", (0.02237 + 0.12) / 0.6736 ** 2, 0.02237 / 0.6736 ** 2, 0.6736, 0.0)

# ================================================================ linear theory (F3 f3_growth_audit.py growth_ratio, extended)
def kernel_s(kind, kk, a, mu):
    if mu is None or kind == "dust":
        return np.ones_like(kk)
    x2 = (kk / (a * mu)) ** 2
    return (1.0 - x2) if kind == "jeans" else 1.0 / (1.0 + x2)

def two_fluid(kk, mu, Om, Ob, h, kind="bsk2", a_start=1e-3, a_out=(1.0,), rad=True):
    """F3's sub-horizon two-fluid system (baryons feel all mass at every k; khronon own-gravity kernel s).
    Returns arrays (len(a_out), n) of delta_b, delta_tau, d delta_b/dlna, d delta_tau/dlna; start delta = a_start (both)."""
    Or = (4.18e-5 / h ** 2) if rad else 0.0; OL = 1.0 - Om - Or; OK = Om - Ob
    Ek = lambda a: math.sqrt(Om * a ** -3 + Or * a ** -4 + OL)
    kk = np.asarray(kk, float); n = len(kk)
    def rhs(x, st):
        a = math.exp(x); E = Ek(a); eps = 1e-6
        dlnE = (math.log(Ek(a * math.exp(eps))) - math.log(Ek(a * math.exp(-eps)))) / (2 * eps)
        dens = 1.5 * a ** -3 / E ** 2
        db, gb, dk, gk = st[:n], st[n:2 * n], st[2 * n:3 * n], st[3 * n:]
        s = kernel_s(kind, kk, a, mu)
        src_b = dens * (Ob * db + OK * dk); src_k = dens * (Ob * db + OK * dk * s)
        return np.concatenate([gb, -(2 + dlnE) * gb + src_b, gk, -(2 + dlnE) * gk + src_k])
    st0 = np.full(4 * n, a_start)
    xs = sorted(set([math.log(a) for a in a_out]))
    sol = solve_ivp(rhs, [math.log(a_start), xs[-1]], st0, method="DOP853", rtol=1e-7, atol=1e-12, t_eval=xs)
    out = {}
    for j, x in enumerate(sol.t):
        y = sol.y[:, j]
        out[round(math.exp(x), 12)] = (y[:n], y[2 * n:3 * n], y[n:2 * n], y[3 * n:])
    return [out[round(a, 12)] if round(a, 12) in out else out[min(out, key=lambda q: abs(q - a))] for a in a_out]

def linear_transfer(kk, mode, muK, bg, a_list, a_start=1e-3):
    """per-species transfer relative to the dust-limit total delta_m(a = 1): R_b, R_tau, f_b, f_tau at each a in a_list,
    plus T_m(a) = delta_m(a)/delta_m,dust(1)."""
    kind = {"KX": "bsk2", "LIN": "bsk2", "GRJ": "jeans", "S0": "dust"}[mode]
    mu = None if kind == "dust" else muK
    dust = two_fluid(np.array([0.1]), None, bg.Om, bg.Ob, bg.h, "dust", a_start, (1.0,))[0]
    norm = (bg.Ob * dust[0][0] + bg.Otau * dust[1][0]) / bg.Om
    sols = two_fluid(kk, mu, bg.Om, bg.Ob, bg.h, kind, a_start, tuple(a_list))
    res = []
    for db, dt, gb, gt in sols:
        res.append(dict(Rb=db / norm, Rt=dt / norm, fb=gb / db, ft=gt / dt, Tm=(bg.Ob * db + bg.Otau * dt) / bg.Om / norm))
    return res

# ---- CLASS dust-limit spectrum (vanilla CLASS = the dust limit; F3 K2)
KS = np.geomspace(1e-4, 50.0, 1500)
def class_pk(wb, wc, h, lnA, ns, tau):
    from classy import Class
    c = Class(); c.set({"omega_b": wb, "omega_cdm": wc, "h": h, "ln10^{10}A_s": lnA, "n_s": ns, "tau_reio": tau, "N_ur": 3.044,
                        "T_cmb": 2.7255, "output": "mPk", "P_k_max_h/Mpc": 60.0, "z_max_pk": 4.0})
    c.compute(); Pk = np.array([c.pk_lin(k * h, 0.0) for k in KS]) * h ** 3; s8 = c.sigma8()
    c.struct_cleanup(); c.empty()
    return Pk, s8

_PKB = {}
def pk_model_B():
    if "Pk" not in _PKB:
        fn = os.path.join(WORK, "class_modelB_pk.npz")
        if os.path.exists(fn):
            d = np.load(fn); _PKB["Pk"], _PKB["s8"] = d["Pk"], float(d["s8"])
        else:
            Pk, s8 = class_pk(WB_C2B, OM_B * H_B ** 2 - WB_C2B, H_B, LNAS_C2B, NS_C2B, TAU_C2B)
            os.makedirs(WORK, exist_ok=True); atomic_npz(fn, Pk=Pk, s8=np.array(s8), KS=KS); _PKB["Pk"], _PKB["s8"] = Pk, s8
    return _PKB["Pk"], _PKB["s8"]

W8 = lambda x: 3 * (np.sin(x) - x * np.cos(x)) / x ** 3

# ================================================================ atomic I/O
def atomic_json(fn, obj):
    tmp = fn + ".tmp"
    with open(tmp, "w") as f:
        json.dump(clean(obj), f, indent=1); f.flush(); os.fsync(f.fileno())
    os.replace(tmp, fn)
def atomic_npz(fn, **arrs):
    tmp = fn + ".tmp"
    with open(tmp, "wb") as f:
        np.savez(f, **arrs); f.flush(); os.fsync(f.fileno())
    os.replace(tmp, fn)
def atomic_npy(fn, arr):
    tmp = fn + ".tmp"
    with open(tmp, "wb") as f:
        np.save(f, arr); f.flush(); os.fsync(f.fileno())
    os.replace(tmp, fn)
def atomic_text(fn, text):
    tmp = fn + ".tmp"
    with open(tmp, "w") as f:
        f.write(text); f.flush(); os.fsync(f.fileno())
    os.replace(tmp, fn)
def clean(x):
    if isinstance(x, dict): return {str(k): clean(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)): return [clean(v) for v in x]
    if isinstance(x, np.ndarray): return clean(x.tolist())
    if isinstance(x, (np.floating, np.integer)): return x.item()
    if isinstance(x, np.bool_): return bool(x)
    if isinstance(x, float) and not math.isfinite(x): return str(x)
    return x

# ================================================================ mesh
class Mesh:
    def __init__(self, N, L):
        self.N, self.L, self.dx = N, L, L / N
        k1 = 2 * np.pi * sfft.fftfreq(N, d=self.dx); kz = 2 * np.pi * sfft.rfftfreq(N, d=self.dx)
        self.kx, self.ky, self.kz = k1[:, None, None], k1[None, :, None], kz[None, None, :]
        nyq = np.pi / self.dx
        g1 = np.where(np.abs(np.abs(k1) - nyq) < 1e-9 * nyq, 0.0, k1); gz = np.where(np.abs(kz - nyq) < 1e-9 * nyq, 0.0, kz)
        self.gk = (g1[:, None, None], g1[None, :, None], gz[None, None, :])     # gradient wavevectors, Nyquist zeroed
        self.k2 = self.kx ** 2 + self.ky ** 2 + self.kz ** 2
        self.kmag = np.sqrt(self.k2)
        self.ik2 = np.zeros_like(self.k2); self.ik2[self.k2 > 0] = 1.0 / self.k2[self.k2 > 0]
        self.kf = 2 * np.pi / L; self.knyq = nyq
    def fft(self, x): return sfft.rfftn(x, workers=THREADS[0])
    def ifft(self, xk): return sfft.irfftn(xk, s=(self.N,) * 3, workers=THREADS[0])
    def grad_c(self, xk, c): return self.ifft(1j * self.gk[c] * xk)
    def div_k(self, F):
        out = None
        for c in range(3):
            t = 1j * self.gk[c] * self.fft(F[c])
            out = t if out is None else out + t
        return out

def nyq_zero(m, dk):
    N = m.N
    dk[N // 2, :, :] = 0; dk[:, N // 2, :] = 0; dk[:, :, -1] = 0; dk[0, 0, 0] = 0
    return dk

# ================================================================ particles (float32 displacement from the cell-centre lattice + float32 momentum)
class Species:
    def __init__(self, name, npg, L):
        self.name, self.npg, self.L, self.N = name, npg, L, npg ** 3
        self.disp = np.zeros((3, self.N), np.float32); self.mom = np.zeros((3, self.N), np.float32)
        CH = int(os.environ.get("L1_CHUNK", str(1 << 21)))
        self.chunks = [(i, min(i + CH, self.N)) for i in range(0, self.N, CH)]
    def q(self, c, i0, i1):
        idx = np.arange(i0, i1, dtype=np.int64); n = self.npg
        ic = idx // (n * n) if c == 0 else ((idx // n) % n if c == 1 else idx % n)
        return (ic + 0.5) * (self.L / n)
    def pos(self, i0, i1):
        return np.stack([(self.q(c, i0, i1) + self.disp[c, i0:i1]) % self.L for c in range(3)], 1)

def _cic(pos, N, dx):
    u = pos / dx; i0 = np.floor(u).astype(np.int64); w = u - i0
    return i0 % N, (i0 + 1) % N, w

def deposit(m, S):
    """CIC mass assignment -> delta = rho/rhobar - 1 (float64 mesh)."""
    N = m.N; rho = np.zeros(N ** 3, np.float64)
    for i0_, i1_ in S.chunks:
        i0, i1, w = _cic(S.pos(i0_, i1_), N, m.dx)
        for cx in (0, 1):
            ix = i1[:, 0] if cx else i0[:, 0]; wx = w[:, 0] if cx else 1 - w[:, 0]
            for cy in (0, 1):
                iy = i1[:, 1] if cy else i0[:, 1]; wy = w[:, 1] if cy else 1 - w[:, 1]
                for cz in (0, 1):
                    iz = i1[:, 2] if cz else i0[:, 2]; wz = w[:, 2] if cz else 1 - w[:, 2]
                    rho += np.bincount((ix * N + iy) * N + iz, weights=wx * wy * wz, minlength=N ** 3)
    rho *= (N ** 3 / S.N); rho -= 1.0
    return rho.reshape(N, N, N)

def kick_species(m, S, fields, cc):
    """fields: 3 float32 meshes of acceleration (code units, already x a); cc: kick factor."""
    N = m.N; flats = [f.reshape(-1) for f in fields]
    def task(ch):
        i0_, i1_ = ch
        i0, i1, w = _cic(S.pos(i0_, i1_), N, m.dx)
        acc = np.zeros((3, i1_ - i0_), np.float64)
        for cx in (0, 1):
            ix = i1[:, 0] if cx else i0[:, 0]; wx = w[:, 0] if cx else 1 - w[:, 0]
            for cy in (0, 1):
                iy = i1[:, 1] if cy else i0[:, 1]; wy = w[:, 1] if cy else 1 - w[:, 1]
                for cz in (0, 1):
                    iz = i1[:, 2] if cz else i0[:, 2]; wz = w[:, 2] if cz else 1 - w[:, 2]
                    idx = (ix * N + iy) * N + iz; ww = wx * wy * wz
                    for c in range(3): acc[c] += ww * flats[c][idx]
        for c in range(3):
            S.mom[c, i0_:i1_] += (cc * acc[c]).astype(np.float32)
    if POOL[0] is not None: list(POOL[0].map(task, S.chunks))
    else:
        for ch in S.chunks: task(ch)

def drift_species(S, d):
    for c in range(3):
        S.disp[c] += np.float32(d) * S.mom[c]

# ================================================================ field solvers
def solve_hold(m, Sk, m2, g0, xi0=None, tol=1e-6, maxit=400, depth=5, coef="hold", maxit_cap=None):
    """Hold equation div[(1 - mu(x)) grad Xi] - m2 Xi = S (Sk = rfftn(S)), J = J_x (mu = x/(1+x)).
    Fixed point (lap - m2) Xi = S + div[mu grad Xi], Anderson(depth).  coef = 'swap' (MUTATE): (1 - mu) -> mu.
    Returns Xi (real), info."""
    N = m.N
    den = m.k2 + m2
    den_inv = np.zeros_like(den); den_inv[den > 0] = -1.0 / den[den > 0]
    def T(xi):
        xk = m.fft(xi)
        g = [m.grad_c(xk, c) for c in range(3)]; del xk
        gx, gy, gz = g
        gm = ne.evaluate("sqrt(gx*gx + gy*gy + gz*gz)")
        g0_ = float(g0)
        mu = (ne.evaluate("gm / (g0_ + gm)", local_dict={"gm": gm, "g0_": g0_}) if coef == "hold"
              else ne.evaluate("1.0 - gm / (g0_ + gm)", local_dict={"gm": gm, "g0_": g0_}))
        del gm
        r = Sk.copy()
        for c in range(3):
            gc = g[c]
            r += 1j * m.gk[c] * m.fft(ne.evaluate("mu * gc"))
        del g, mu
        r *= den_inv
        return m.ifft(r)
    x = np.zeros((N, N, N)) if xi0 is None else xi0.copy()
    hist_dx, hist_df = [], []
    x_prev = f_prev = None; info = dict(iters=0, res=float("inf"), converged=False)
    cap = maxit if maxit_cap is None else maxit_cap
    for it in range(1, cap + 1):
        Tx = T(x)
        nTx = float(np.sqrt(np.vdot(Tx.ravel(), Tx.ravel()).real))
        f = ne.evaluate("Tx - x")
        nf = float(np.sqrt(np.vdot(f.ravel(), f.ravel()).real))
        res = nf / nTx if nTx > 0 else 0.0
        info.update(iters=it, res=res)
        if res <= tol:
            info["converged"] = True; x = Tx; break
        if it == cap:
            x = Tx; break
        del Tx
        if x_prev is not None:
            hist_dx.append(ne.evaluate("x - x_prev")); hist_df.append(ne.evaluate("f - f_prev"))
            if len(hist_dx) > depth: hist_dx.pop(0); hist_df.pop(0)
        x_prev, f_prev = x, f
        if hist_df:
            k_ = len(hist_df)
            A = np.empty((k_, k_)); b = np.empty(k_)
            for i in range(k_):
                b[i] = np.vdot(hist_df[i].ravel(), f.ravel()).real
                for j in range(i, k_):
                    A[i, j] = A[j, i] = np.vdot(hist_df[i].ravel(), hist_df[j].ravel()).real
            A += 1e-12 * np.trace(A) * np.eye(k_)
            gam = np.linalg.solve(A, b)
            xn = x + f
            for i in range(k_):
                gi = float(gam[i]); dxi, dfi = hist_dx[i], hist_df[i]
                xn = ne.evaluate("xn - gi * (dxi + dfi)")
            x = xn
        else:
            x = x + f
    gk = m.fft(x); g = [m.grad_c(gk, c) for c in range(3)]
    gm = np.sqrt(g[0] ** 2 + g[1] ** 2 + g[2] ** 2) / g0
    info.update(x_rms=float(np.sqrt(np.mean(gm ** 2))), x_max=float(gm.max()))
    return x, info

def field_solve(m, Sb_k, St_k, a, mode, muK, a0c, xi0=None, mut=None, maxit_cap=None):
    """Sb_k, St_k: rfftn of the baryon and khronon sources ((3/2)(O_s/a) delta_s, or 4 pi G rho_s in static tests).
    Returns phi_k, xi_k (or None), info."""
    info = {}
    Stot = Sb_k if (mut == "noKhronon") else Sb_k + St_k
    phi_k = -Stot * m.ik2
    if mode == "S0" or (mut == "noHold"):
        return phi_k, None, info
    if mode == "GRJ":
        if not math.isfinite(muK): return phi_k, None, info
        return phi_k, -St_k / (a * muK) ** 2, info
    m2 = (a * muK) ** 2 if math.isfinite(muK) else None
    if mode == "LIN":
        den = m.k2 + m2; inv = np.zeros_like(den); inv[den > 0] = -1.0 / den[den > 0]
        return phi_k, St_k * inv, info
    if mode == "KX":
        xi, info = solve_hold(m, St_k, m2, a * a0c, xi0=xi0, coef=("swap" if mut == "swap" else "hold"), maxit_cap=maxit_cap)
        info["xi"] = xi
        return phi_k, m.fft(xi), info
    raise ValueError(mode)

def solve_aqual_projection(m, Sb_k, a0c, mu_kind="simple", tol=1e-9, maxit=300):
    """AQUAL div[mu(|g|/a0) g] = S by alternating projection (iterative FFT): U = mu g = g_N + curl part; g curl-free.
    Returns gradient field G = grad Phi (3 real meshes), Newtonian G_N, info."""
    phiN = -Sb_k * m.ik2
    GN = [m.grad_c(phiN, c) for c in range(3)]; GNk = [m.fft(GN[c]) for c in range(3)]
    def nu_apply(U):
        um = np.sqrt(U[0] ** 2 + U[1] ** 2 + U[2] ** 2); y = np.maximum(um, 1e-300) / a0c
        if mu_kind == "simple": nu = 0.5 * (1 + np.sqrt(1 + 4 / y))
        else: nu = np.sqrt(0.5 * (1 + np.sqrt(1 + 4 / y ** 2)))
        return [U[c] * nu for c in range(3)]
    def mu_apply(G):
        gm = np.sqrt(G[0] ** 2 + G[1] ** 2 + G[2] ** 2); x = gm / a0c
        mu = x / (1 + x) if mu_kind == "simple" else x / np.sqrt(1 + x ** 2)
        return [G[c] * mu for c in range(3)]
    def longit(Fk):
        kd = sum(m.gk[c] * Fk[c] for c in range(3))
        return [m.gk[c] * kd * m.ik2 for c in range(3)]
    G = [m.ifft(t) for t in longit([m.fft(t) for t in nu_apply(GN)])]
    info = dict(iters=0, res=None)
    for it in range(1, maxit + 1):
        U = mu_apply(G); Uk = [m.fft(U[c]) for c in range(3)]; Lk = longit(Uk)
        Up = [m.ifft(GNk[c] + Uk[c] - Lk[c]) for c in range(3)]
        Gn = [m.ifft(t) for t in longit([m.fft(t) for t in nu_apply(Up)])]
        num = sum(float(np.sum((Gn[c] - G[c]) ** 2)) for c in range(3)); den = sum(float(np.sum(Gn[c] ** 2)) for c in range(3))
        G = Gn; info.update(iters=it, res=math.sqrt(num / den))
        if info["res"] <= tol: break
    # AQUAL residual: div(mu G) - S relative
    divk = m.div_k(mu_apply(G)); r = divk - Sb_k; r[0, 0, 0] = 0
    info["aqual_residual_rel"] = float(np.sqrt(np.sum(np.abs(r) ** 2) / np.sum(np.abs(Sb_k) ** 2)))
    return G, GN, info

# ================================================================ measurement (cfg596 measure_pk convention)
def pk_bins(m, dk):
    N, L = m.N, m.L
    W = (np.sinc(m.kx * m.dx / (2 * np.pi)) * np.sinc(m.ky * m.dx / (2 * np.pi)) * np.sinc(m.kz * m.dx / (2 * np.pi))) ** 2
    pk3 = (np.abs(dk) ** 2) * L ** 3 / N ** 6 / W ** 2
    edges = np.arange(0.5, N // 2 + 1, 1.0) * m.kf
    wt = np.full(dk.shape, 2.0); wt[..., 0] = 1.0
    if N % 2 == 0: wt[..., -1] = 1.0
    wt[0, 0, 0] = 0.0
    ib = np.digitize(m.kmag.ravel(), edges); wv = wt.ravel()
    nb = np.bincount(ib, weights=wv, minlength=len(edges) + 1)
    sk = np.bincount(ib, weights=wv * m.kmag.ravel(), minlength=len(edges) + 1)
    sp = np.bincount(ib, weights=wv * pk3.ravel(), minlength=len(edges) + 1)
    x = m.kmag * 8.0; x = np.where(x > 0, x, 1e-3)
    s8 = math.sqrt(float(np.sum(wt * pk3 * W8(x) ** 2)) / L ** 3)
    ok = nb[1:len(edges)] > 0
    kb = (sk[1:len(edges)] / np.maximum(nb[1:len(edges)], 1))[ok]; pb = (sp[1:len(edges)] / np.maximum(nb[1:len(edges)], 1))[ok]
    return kb, pb, s8, dict(ib=ib, wv=wv, edges=edges, ok=ok)

def cross_growth(m, dk, dk0):
    """per bin: sum Re(dk dk0*) / sum |dk0|^2 (cfg596 bins)."""
    edges = np.arange(0.5, m.N // 2 + 1, 1.0) * m.kf
    wt = np.full(dk.shape, 2.0); wt[..., 0] = 1.0
    if m.N % 2 == 0: wt[..., -1] = 1.0
    wt[0, 0, 0] = 0.0
    ib = np.digitize(m.kmag.ravel(), edges); wv = wt.ravel()
    num = np.bincount(ib, weights=wv * (dk * np.conj(dk0)).real.ravel(), minlength=len(edges) + 1)
    den = np.bincount(ib, weights=wv * (np.abs(dk0) ** 2).ravel(), minlength=len(edges) + 1)
    sk = np.bincount(ib, weights=wv * m.kmag.ravel(), minlength=len(edges) + 1)
    nb = np.bincount(ib, weights=wv, minlength=len(edges) + 1)
    ok = (nb[1:len(edges)] > 0) & (den[1:len(edges)] > 0)
    return (sk[1:len(edges)] / np.maximum(nb[1:len(edges)], 1))[ok], (num[1:len(edges)] / np.maximum(den[1:len(edges)], 1e-300))[ok]

# ================================================================ initial conditions
def white_noise_k(npg, nseed, seed, cache=True):
    """cfg596 recipe (initial_conditions_exact / lean): seed-359 Gaussian white noise; NSEED > N selects the low modes.
    For NSEED > N the selected modes are computed once in a child process and cached (bit-identical), so a run's own RSS does
    not carry the NSEED^3 transform."""
    if cache and nseed != npg:
        fn = os.path.join(WORK, f"whitenoise_N{npg}_ns{nseed}_s{seed}.npy")
        if not os.path.exists(fn):
            os.makedirs(WORK, exist_ok=True)
            subprocess.run([sys.executable, "-c", f"import sys; sys.path.insert(0, {HERE!r}); import khronon_pm as K, numpy as np; "
                            f"K.atomic_npy({fn!r}, K.white_noise_k({npg}, {nseed}, {seed}, cache=False))"], check=True)
        return np.load(fn)
    rng = np.random.default_rng(seed)
    wk = sfft.rfftn(rng.standard_normal((nseed,) * 3), workers=THREADS[0]) / nseed ** 1.5
    if nseed != npg:
        ix = np.concatenate([np.arange(0, npg // 2), np.arange(nseed - npg // 2, nseed)])
        wk = wk[ix][:, ix][:, :, :npg // 2 + 1].copy()
    return wk

def ics_native(m, sp_b, sp_t, cfg, bg):
    """per-species Zel'dovich ICs: delta_s(k, a_i) = R_s(k) delta_lin,dust(k, z = 0); p_s = a^2 E f_s(k) psi_s."""
    npg = m.N; L = m.L; a_i = cfg["a_i"]
    Pk, s8_class = pk_model_B()
    wk = white_noise_k(npg, cfg["nseed"], cfg["seed"])
    dk = wk * np.sqrt(np.interp(np.log(np.maximum(m.kmag, 1e-5)), np.log(KS), Pk, left=0, right=0) / (L / npg) ** 3) * npg ** 1.5 * cfg["eps"]
    del wk
    dk = nyq_zero(m, dk)
    kg = np.geomspace(max(m.kf * 0.5, 1e-4), m.kmag.max() * 1.05, 160)
    tr = linear_transfer(kg, cfg["mode"], cfg["muK"], bg, [a_i, 1.0])
    ti, t1 = tr[0], tr[1]
    lk = np.log(np.maximum(m.kmag, kg[0]))
    info = dict(kgrid=kg, Tm_z0=t1["Tm"], Rb_ai=ti["Rb"], Rt_ai=ti["Rt"], fb_ai=ti["fb"], ft_ai=ti["ft"])
    cm = a_i ** 2 * bg.E(a_i)
    for S, R, f in ((sp_b, ti["Rb"], ti["fb"]), (sp_t, ti["Rt"], ti["ft"])):
        Rk = np.interp(lk, np.log(kg), R); Vk = np.interp(lk, np.log(kg), R * f)     # interpolate d delta/dlna, not f (f has poles where delta = 0)
        for c in range(3):
            kc = (m.kx, m.ky, m.kz)[c]
            S.disp[c] = m.ifft(1j * kc * dk * Rk * m.ik2).reshape(-1).astype(np.float32)
            S.mom[c] = (cm * m.ifft(1j * kc * dk * Vk * m.ik2)).reshape(-1).astype(np.float32)
        del Rk, Vk
    # linear predictions for this realisation (sigma8 over the same mesh modes)
    Tm1 = np.interp(lk, np.log(kg), t1["Tm"])
    dm_lin0 = dk * Tm1
    x8 = np.where(m.kmag > 0, m.kmag * 8.0, 1e-3)
    wt = np.full(dk.shape, 2.0); wt[..., 0] = 1.0; wt[..., -1] = 1.0; wt[0, 0, 0] = 0.0
    info["sigma8_lin_box"] = math.sqrt(float(np.sum(wt * np.abs(dm_lin0) ** 2 * W8(x8) ** 2)) / npg ** 6)
    info["sigma8_lin_box_dust"] = math.sqrt(float(np.sum(wt * np.abs(dk) ** 2 * W8(x8) ** 2)) / npg ** 6)
    info["sigma8_class_dust"] = s8_class * cfg["eps"]
    return info

def ics_cfg596(m, sp_b, sp_t, cfg):
    """gate KA: both species get the copied CFG596 engine's exact-mode ICs."""
    R = ref596()
    pos, mom = R.initial_conditions_exact(m.N, 1.0)
    for S in (sp_b, sp_t):
        for c in range(3):
            q = S.q(c, 0, S.N)
            S.disp[c] = (((pos[:, c] - q + 0.5 * m.L) % m.L) - 0.5 * m.L).astype(np.float32)
            S.mom[c] = mom[:, c].astype(np.float32)
    return dict(source="ref_cfg596_pm.initial_conditions_exact")

_REF = {}
def ref596():
    if "R" not in _REF:
        sys.path.insert(0, HERE)
        import importlib
        _REF["R"] = importlib.import_module("ref_cfg596_pm")
    return _REF["R"]


# ================================================================ halo profiles (AMENDMENT A3 item 5; reported only, no verdict weight)
RHOC = 2.775e11                                             # critical density, (Msun/h)/(Mpc/h)^3
def halo_profiles(m, db, dt, bg, a=1.0, max_cand=10000, max_halo=3000):
    from scipy import ndimage
    np.seterr(invalid="ignore")
    N, dx, h = m.N, m.dx, bg.h
    rb = bg.Ob * (1.0 + db); rt = bg.Otau * (1.0 + dt)        # rho_crit units (comoving)
    tot = rb + rt
    tk = m.fft(tot); sm = m.ifft(tk * np.exp(-0.5 * m.k2 * dx ** 2)); del tk
    mx = ndimage.maximum_filter(sm, size=3, mode="wrap")
    cand = np.argwhere((sm >= mx) & (sm > 20.0 * bg.Om)); del mx
    vals = sm[tuple(cand.T)]; cand = cand[np.argsort(-vals)][:max_cand]; del sm, vals
    Rphys = lambda r: r * h / a                                  # physical Mpc -> comoving Mpc/h
    nr = int(math.ceil(Rphys(3.0) / dx)) + 1; off = np.arange(-nr, nr + 1)
    OX, OY, OZ = np.meshgrid(off, off, off, indexing="ij"); rr = np.sqrt(OX ** 2 + OY ** 2 + OZ ** 2) * dx; del OX, OY, OZ
    in1 = rr <= Rphys(1.0)
    edges_phys = np.array([0.1, 0.2, 0.3, 0.5, 0.7, 1.0, 1.5, 2.0, 3.0]); sh = np.digitize(rr, Rphys(edges_phys))
    ann1 = (rr >= Rphys(0.3)) & (rr < Rphys(1.0)); ann2 = (rr >= Rphys(1.0)) & (rr < Rphys(3.0))
    cellM = RHOC * dx ** 3 / h                                    # Msun per unit (rho/rho_crit) per cell
    def cube(f, c):
        return f[np.ix_((c[0] + off) % N, (c[1] + off) % N, (c[2] + off) % N)]
    M1 = np.array([cube(tot, c)[in1].sum() * cellM for c in cand])
    order = np.argsort(-M1); acc = []; accM = []
    rex = Rphys(1.0) / dx
    for i in order:
        c = cand[i]
        if acc:
            d = np.abs(np.array(acc) - c); d = np.minimum(d, N - d)
            if np.min(np.sqrt((d ** 2).sum(1))) <= rex: continue
        acc.append(c); accM.append(M1[i])
        if len(acc) >= max_halo: break
    acc = np.array(acc); accM = np.array(accM)
    prof = []
    for c in acc:
        B = cube(rb, c); T = cube(rt, c)
        pb = np.array([B[sh == j].mean() for j in range(1, len(edges_phys))]); pt = np.array([T[sh == j].mean() for j in range(1, len(edges_phys))])
        prof.append((pb, pt, T[ann1].sum() / B[ann1].sum(), T[ann2].sum() / B[ann2].sum(), T[ann1].sum(), B[ann1].sum(), T[ann2].sum(), B[ann2].sum()))
    classes = {"cluster": accM >= 1e14, "group": (accM >= 1e13) & (accM < 1e14), "galaxy": (accM >= 1e12) & (accM < 1e13)}
    if classes["cluster"].sum() < 10:
        t50 = np.zeros(len(accM), bool); t50[:min(50, len(accM))] = True; classes["top50"] = t50
    out = dict(a=a, n_candidates=int(len(cand)), n_halos=int(len(acc)), edges_Mpc_phys=edges_phys, cosmic_tau_over_b=bg.Otau / bg.Ob,
               cell_Mpc_phys=dx / h * a, classes={})
    for nm, sel in classes.items():
        idx = np.where(sel)[0]
        if len(idx) == 0:
            out["classes"][nm] = dict(n=0); continue
        PB = np.array([prof[i][0] for i in idx]); PT = np.array([prof[i][1] for i in idx])
        r1 = np.array([prof[i][2] for i in idx]); r2 = np.array([prof[i][3] for i in idx])
        st1 = sum(prof[i][4] for i in idx) / sum(prof[i][5] for i in idx); st2 = sum(prof[i][6] for i in idx) / sum(prof[i][7] for i in idx)
        out["classes"][nm] = dict(n=int(len(idx)), M1_Msun_min=float(accM[idx].min()), M1_Msun_median=float(np.median(accM[idx])),
                                  M1_Msun_max=float(accM[idx].max()), rho_b_over_mean_b=PB.mean(0) / bg.Ob, rho_tau_over_mean_tau=PT.mean(0) / bg.Otau,
                                  tau_over_b_shell=PT.mean(0) / PB.mean(0), ratio_0p3_1_stacked=st1, ratio_1_3_stacked=st2,
                                  ratio_0p3_1_median=float(np.median(r1)), ratio_1_3_median=float(np.median(r2)))
    out["catalog_top200"] = dict(pos_Mpch=(acc[:200] * dx).tolist(), M1_Msun=accM[:200].tolist(),
                                 ratio_0p3_1=[prof[i][2] for i in range(min(200, len(prof)))], ratio_1_3=[prof[i][3] for i in range(min(200, len(prof)))])
    return out

# ================================================================ time grid
def step_grid(zi):
    a_i = 1.0 / (1 + 49.0)
    seg = [(a_i, 0.5, 123), (0.5, 2 / 3, 11), (2 / 3, 1.0, 16)]
    a = [a_i]
    for lo, hi, n in seg:
        a += list(np.exp(np.linspace(math.log(lo), math.log(hi), n + 1))[1:])
    a[-1] = 1.0
    if zi == 199:
        pre = list(np.exp(np.linspace(math.log(1 / 200.0), math.log(a_i), 61)))[:-1]
        a = pre + a
    elif zi != 49:
        raise ValueError("zi must be 49 or 199 (frozen)")
    return np.array(a)

# ================================================================ memory guard, signals
STOP = {"flag": False, "t": None}
def _on_term(signum, frame):
    STOP["flag"] = True; STOP["t"] = time.time()
    print(f"[khronon_pm] SIGTERM received: checkpoint at the next safe point", flush=True)

def swap_used_mb():
    try:
        s = subprocess.run(["sysctl", "-n", "vm.swapusage"], capture_output=True, text=True, timeout=10).stdout
        return float(s.split("used =")[1].split("M")[0])
    except Exception:
        return None

import ctypes
class _RU(ctypes.Structure):          # rusage_info_v2 (flavor 2), as compute_queue/heavyq.py
    _fields_ = [("uuid", ctypes.c_uint8 * 16)] + [(n, ctypes.c_uint64) for n in (
        "user_time", "system_time", "pkg_idle_wkups", "interrupt_wkups", "pageins", "wired", "resident", "footprint",
        "start_abstime", "exit_abstime")] + [("pad", ctypes.c_uint64 * 40)]
def footprint_gb(pid=None):
    try:
        lp = ctypes.CDLL("/usr/lib/libproc.dylib"); ru = _RU()
        if lp.proc_pid_rusage(int(pid or os.getpid()), 2, ctypes.byref(ru)) != 0: return None
        return ru.footprint / 1e9
    except Exception:
        return None

def start_guard(rss_cap_gb=52.0, swap_grow_gb=4.0):
    import psutil
    pr = psutil.Process(); s0 = swap_used_mb()
    PEAK = {"rss": 0.0, "footprint": 0.0, "swap0_mb": s0, "swap_max_mb": s0}
    def loop():
        while True:
            time.sleep(2.0)
            r = pr.memory_info().rss / 1e9; PEAK["rss"] = max(PEAK["rss"], r)
            fp = footprint_gb()
            if fp is not None:
                PEAK["footprint"] = max(PEAK["footprint"], fp); r = max(r, fp)
            s = swap_used_mb()
            if s is not None and s0 is not None:
                PEAK["swap_max_mb"] = max(PEAK["swap_max_mb"], s)
                if s - s0 > swap_grow_gb * 1024:
                    print(f"[khronon_pm] GUARD: swap grew {(s - s0) / 1024:.2f} GB > {swap_grow_gb} GB: hard abort", flush=True); os._exit(3)
            if r > rss_cap_gb:
                print(f"[khronon_pm] GUARD: RSS {r:.2f} GB > {rss_cap_gb} GB: hard abort", flush=True); os._exit(3)
    threading.Thread(target=loop, daemon=True).start()
    return PEAK

def peak_rss_gb():
    import resource
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9

def estimate_gb(N, depth=5):
    """declared peak memory (GB) for N^3 mesh and N^3 particles per species: particles 2 x 24 B; hold solver
    (2 depth history + 4 iterate + 6 inside T + 2 sources/potentials) float64 meshes; kick phase 6 float32 meshes is smaller.
    Calibrated against measured peaks in README (factor CAL)."""
    cells = N ** 3
    b = 2 * 24 * cells + (2 * depth + 4 + 6 + 2) * 8 * cells + 0.35e9
    return 1.0 * b / 1e9

# ================================================================ the simulation
def run_sim(cfg):
    """cfg keys: mode, foot, muK, N, L, zi, nseed, seed, eps, bg ('B'|'CFG596'), ic ('native'|'cfg596'), mut, tag,
    snaps (list of a), xgrowth (bool), resume (bool), ckpt_every, maxit_cap, guard (bool), log (bool)."""
    T0 = time.time()
    bg = MODEL_B if cfg.get("bg", "B") == "B" else CFG596_BG
    N, L = cfg["N"], cfg["L"]; mode = cfg["mode"]; muK = float(cfg.get("muK", float("inf")))
    a0c = bg.a0c(cfg.get("foot", "canonical")); mut = cfg.get("mut")
    tag = cfg["tag"]; wdir = os.path.join(WORK, tag); os.makedirs(wdir, exist_ok=True)
    ckpt_fn = os.path.join(wdir, "ckpt.npz"); res_fn = os.path.join(wdir, "result.json")
    aa = step_grid(cfg.get("zi", 49)); nsteps = len(aa) - 1; cfg["a_i"] = float(aa[0])
    snap_a = cfg.get("snaps", [0.5, 2 / 3, 1.0])
    snap_idx = {}
    for sa in snap_a:
        j = int(np.argmin(np.abs(aa - sa))); snap_idx[j] = sa
    log = cfg.get("log", True)
    def P(msg):
        if log: print(f"  [{tag}] {msg} t={time.time() - T0:.0f}s rss_peak={peak_rss_gb():.2f}GB", flush=True)
    if cfg.get("resume") and os.path.exists(os.path.join(wdir, "DONE")):
        P("already complete (DONE present): exit 0"); return json.load(open(res_fn))
    guard = start_guard() if cfg.get("guard", True) else None
    signal.signal(signal.SIGTERM, _on_term); signal.signal(signal.SIGINT, _on_term)
    m = Mesh(N, L); sb = Species("b", N, L); st = Species("tau", N, L)
    res = dict(lane="L1_khronon_pm", engine="khronon_pm.py", cfg={k: v for k, v in cfg.items()}, background=bg.desc(),
               a0_code=a0c, nsteps=nsteps, a_grid=aa, snap={}, diag=[], status="running",
               declared_peak_gb=estimate_gb(N), threads=THREADS[0])
    xi_prev = None; n_start = 0; dk0 = None
    if cfg.get("resume") and os.path.exists(ckpt_fn):
        d = np.load(ckpt_fn, allow_pickle=False)
        sb.disp[...] = d["b_disp"]; sb.mom[...] = d["b_mom"]; st.disp[...] = d["t_disp"]; st.mom[...] = d["t_mom"]
        xi_prev = d["xi"] if d["xi"].size > 1 else None
        dk0 = d["dk0"] if d["dk0"].size > 1 else None
        n_start = int(d["n_next"]); res = json.loads(bytes(d["res"]).decode()); res["status"] = "running"
        res.setdefault("resumes", []).append(dict(n_next=n_start, t=time.time()))
        del d
        P(f"resumed at loop step {n_start}/{nsteps}")
    else:
        if cfg.get("ic", "native") == "native":
            res["ic"] = ics_native(m, sb, st, cfg, bg)
        else:
            res["ic"] = ics_cfg596(m, sb, st, cfg)
    res["declared_peak_gb"] = estimate_gb(N)
    atomic_json(res_fn, res)

    def deposit_all():
        db = deposit(m, sb); dt = deposit(m, st)
        return db, dt
    def sources(db, dt, a):
        Sb = m.fft((1.5 * bg.Ob / a) * db); St = m.fft((1.5 * bg.Otau / a) * dt)
        return Sb, St
    def forces_and_kick(a, kicks, n_call):
        nonlocal xi_prev
        tf = time.time()
        db, dt = deposit_all(); Sb, St = sources(db, dt, a); del db, dt
        phi_k, xi_k, info = field_solve(m, Sb, St, a, mode, muK, a0c, xi0=xi_prev, mut=mut, maxit_cap=cfg.get("maxit_cap"))
        del Sb, St
        if "xi" in info: xi_prev = info.pop("xi")
        d = dict(n=n_call, a=a, **{k: v for k, v in info.items()})
        # baryons: -a grad Phi; khronon: -a grad(Phi - Xi)
        fb_ = [(-a * m.grad_c(phi_k, c)).astype(np.float32) for c in range(3)]
        for cc in kicks: kick_species(m, sb, fb_, cc)
        del fb_
        pt_k = phi_k if xi_k is None else phi_k - xi_k
        del phi_k, xi_k
        ft_ = [(-a * m.grad_c(pt_k, c)).astype(np.float32) for c in range(3)]
        del pt_k
        for cc in kicks: kick_species(m, st, ft_, cc)
        del ft_
        d["t"] = time.time() - tf
        res["diag"].append(d)
    def snapshot(name, a):
        nonlocal dk0
        db, dt = deposit_all()
        dm = bg.fb * db + bg.ftau * dt
        dmk = m.fft(dm)
        kb, pb, s8, _ = pk_bins(m, dmk)
        _, pbb, s8b, _ = pk_bins(m, m.fft(db)); _, pbt, s8t, _ = pk_bins(m, m.fft(dt))
        out = dict(a=a, z=1 / a - 1, k=kb, P=pb, sigma8=s8, P_b=pbb, P_tau=pbt, sigma8_b=s8b, sigma8_tau=s8t,
                   delta_rms=float(np.std(dm)), t=time.time() - T0)
        if cfg.get("xgrowth"):
            if dk0 is None: dk0 = dmk.copy()
            kg_, G_ = cross_growth(m, dmk, dk0); out["G_cross"] = G_; out["k_cross"] = kg_
        if cfg.get("halos") and abs(a - 1.0) < 1e-9:
            th = time.time(); out["halos"] = halo_profiles(m, db, dt, bg, a); out["halos"]["t_s"] = time.time() - th
        res["snap"][name] = out
        P(f"snapshot {name} a={a:.4f} sigma8={s8:.4f} (b {s8b:.4f}, tau {s8t:.4f})")
    def save_ckpt(n_next, status):
        res["status"] = status; res["peak_rss_gb"] = peak_rss_gb()
        if guard: res["guard"] = dict(guard)
        atomic_npz(ckpt_fn, b_disp=sb.disp, b_mom=sb.mom, t_disp=st.disp, t_mom=st.mom,
                   xi=(xi_prev if xi_prev is not None else np.zeros(1)), dk0=(dk0 if dk0 is not None else np.zeros(1, complex)),
                   n_next=np.array(n_next), res=np.frombuffer(json.dumps(clean(res)).encode(), dtype=np.uint8))
        atomic_json(res_fn, res)

    if n_start == 0 and not res.get("started_loop"):
        snapshot("zi", float(aa[0]))
        a0_, a1_ = aa[0], aa[1]; am = math.sqrt(a0_ * a1_)
        forces_and_kick(float(a0_), [bg.kick(a0_, am)], 0)
        d = bg.drift(a0_, a1_); drift_species(sb, d); drift_species(st, d)
        res["started_loop"] = True
    for n in range(n_start, nsteps):
        a0_, a1_ = aa[n], aa[n + 1]; am = math.sqrt(a0_ * a1_)
        last = n == nsteps - 1
        kicks = [bg.kick(am, a1_)]
        if not last:
            b0, b1 = aa[n + 1], aa[n + 2]; bm = math.sqrt(b0 * b1); kicks.append(bg.kick(b0, bm))
        forces_and_kick(float(a1_), kicks, n + 1)
        if (n + 1) in snap_idx:
            nm = {0.5: "z1", 2 / 3: "z0.5", 1.0: "z0"}.get(snap_idx[n + 1], f"a{snap_idx[n + 1]:.4f}")
            snapshot(nm, float(a1_))
        if not last:
            d = bg.drift(b0, b1); drift_species(sb, d); drift_species(st, d)
        if (n + 1) % 10 == 0 or n < 2: P(f"step {n + 1}/{nsteps} a={a1_:.4f} last-call {res['diag'][-1].get('iters', '-')} it")
        if STOP["flag"] and not last:
            save_ckpt(n + 1, "preempted")
            code = int(os.environ.get("HEAVYQ_YIELD_EXIT", "0"))
            P(f"preempted: checkpoint at loop step {n + 1}; exit {code} ({time.time() - STOP['t']:.1f} s after SIGTERM)")
            sys.exit(code)
        if cfg.get("maxsteps") and (n + 1 - n_start) >= cfg["maxsteps"]:
            res["status"] = "calibration_stop"; res["peak_rss_gb"] = peak_rss_gb()
            if guard: res["guard"] = dict(guard)
            res["sec_per_step"] = [d["t"] for d in res["diag"]]
            atomic_json(res_fn, res); P(f"calibration stop after {cfg['maxsteps']} loop steps"); return res
        if cfg.get("ckpt_every", 10) and (n + 1) % cfg.get("ckpt_every", 10) == 0 and not last:
            save_ckpt(n + 1, "running")
    h = hashlib.sha256()
    for arr in (sb.disp, sb.mom, st.disp, st.mom): h.update(np.ascontiguousarray(arr).tobytes())
    res["final_state_sha256"] = h.hexdigest()
    res["nonconverged_calls"] = sum(1 for d in res["diag"] if "converged" in d and not d["converged"])
    res["max_iters"] = max([d.get("iters", 0) for d in res["diag"]] or [0])
    res["max_res"] = max([d.get("res", 0.0) for d in res["diag"] if "res" in d] or [0.0])
    res["status"] = "done"; res["runtime_s"] = res.get("runtime_s", 0.0) + (time.time() - T0); res["peak_rss_gb"] = peak_rss_gb()
    if guard: res["guard"] = dict(guard)
    atomic_json(res_fn, res)
    atomic_text(os.path.join(wdir, "DONE"), res["final_state_sha256"] + "\n")
    if os.path.exists(ckpt_fn) and not cfg.get("keep_ckpt"):
        os.replace(ckpt_fn, ckpt_fn + ".done")          # kept (renamed) until the lane decides; not deleted here
    P("done")
    return res

# ================================================================ CLI
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["run", "estimate"])
    ap.add_argument("--mode", default="KX", choices=["KX", "LIN", "GRJ", "S0"])
    ap.add_argument("--foot", default="canonical", choices=["canonical", "alt"])
    ap.add_argument("--muK", type=float, default=14.8)
    ap.add_argument("--N", type=int, default=128); ap.add_argument("--L", type=float, default=100.0)
    ap.add_argument("--zi", type=int, default=49); ap.add_argument("--nseed", type=int, default=256)
    ap.add_argument("--seed", type=int, default=359); ap.add_argument("--eps", type=float, default=1.0)
    ap.add_argument("--threads", type=int, default=int(os.environ.get("HEAVYQ_THREADS", "1"))); ap.add_argument("--tag", default=None)
    ap.add_argument("--resume", action="store_true"); ap.add_argument("--ckpt_every", type=int, default=10)
    ap.add_argument("--xgrowth", action="store_true"); ap.add_argument("--snaps", default="0.5,0.6666666666666666,1.0")
    ap.add_argument("--no_guard", action="store_true"); ap.add_argument("--halos", action="store_true")
    ap.add_argument("--maxsteps", type=int, default=0)
    a = ap.parse_args()
    if a.cmd == "estimate":
        print(json.dumps({"N": a.N, "declared_peak_gb": estimate_gb(a.N)})); return
    set_threads(a.threads)
    try: os.nice(0)
    except OSError: pass
    mu = a.muK if a.mode != "S0" else float("inf")
    tag = a.tag or f"{a.mode}_{a.foot}_mu{a.muK:g}_N{a.N}_L{a.L:g}_zi{a.zi}_ns{a.nseed}" + (f"_eps{a.eps:g}" if a.eps != 1 else "")
    cfg = dict(mode=a.mode, foot=a.foot, muK=mu, N=a.N, L=a.L, zi=a.zi, nseed=a.nseed, seed=a.seed, eps=a.eps, bg="B",
               ic="native", tag=tag, resume=a.resume, ckpt_every=a.ckpt_every, xgrowth=a.xgrowth,
               snaps=[float(s) for s in a.snaps.split(",")], guard=not a.no_guard, halos=a.halos, maxsteps=a.maxsteps)
    run_sim(cfg)

if __name__ == "__main__":
    main()
