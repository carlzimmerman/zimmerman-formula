"""EW2 shared library: v4 (AeST + capped F + gamma_L) static spherical solver (iter_1 equations, H2's exact form) and
the web projection of SV5 with AeST's dust-branch switch. Criteria: FROZEN_CRITERIA.md + iter_*/FROZEN_CRITERIA.md
(local 869b3d72ad, origin 041be83e4a). kappa = 1/2 FITTED; not theory closed. Footings never pooled. 1 thread."""
import os, sys, math, io, contextlib, json
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"): os.environ[v] = "1"
import numpy as np
np.seterr(all="ignore")
HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
CL6 = os.path.join(REPO, "closure_2026_11_06")
G = 6.674e-11; MSUN = 1.989e30; MPC = 3.0857e22; KPC = MPC / 1e3
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}       # kappa = 1/2 FITTED
DECLARED = [0.0156, 0.1, 0.3, 0.5, 0.7, 1.0, 1.58, 2.0, 3.0, 10.0, 56.6, 2.04e4, 1.24e8]   # Mpc^-1 (iter_1)
MAP = list(np.logspace(-3, 9, 61))                       # 0.2 dex map (iter_2)


def g_aqual(gN, a0):
    x = np.abs(gN); return np.sign(gN) * (0.5 * x + np.sqrt(0.25 * x ** 2 + x * a0))


def lam_max(mu, rM): return (2 / 3) * (1 - np.log(3 * np.sqrt(2) / (mu * rM)))   # VSZ eq_chioutmax (SI lengths)


def grid(r0, r1, mu, hmax=0.004, phase=0.08):
    """mu in 1/m; ln r nodes (r0, r1 in Mpc, SI out) with step min(hmax, phase/(mu r)): RK4 resolves the mass term's oscillation."""
    s, s1 = math.log(r0 * MPC), math.log(r1 * MPC); out = [s]
    while s < s1:
        r = math.exp(s); h = min(hmax, phase / (mu * r)) if mu > 0 else hmax; s = min(s + h, s1); out.append(s)
    return np.exp(np.array(out))


def phi_c(Mfun, Mtot, a0, mu, Delta, r0=1e-5, Rref=3.0):
    """central Phi giving VSZ's lambda = lambda_max + Delta at Rref on the mu = 0 solution (H2's phi_c_for). Delta: array."""
    rr = np.geomspace(r0 * MPC, Rref * MPC, 20001); gl = g_aqual(G * Mfun(rr) / rr ** 2, a0)
    Phi_mu0 = float(np.sum(0.5 * (gl[1:] + gl[:-1]) * np.diff(rr)))
    s = math.sqrt(G * Mtot * a0); rM = math.sqrt(G * Mtot / a0); R = Rref * MPC
    lam = lam_max(mu / MPC, rM) + np.asarray(Delta, float)        # mu given in Mpc^-1
    return -(G * Mtot / R) + s * (lam + math.log(R / rM)) - Phi_mu0


def solve(Mfun, a0, mu_Mpc, Phi0, r1, r0=1e-5, hmax=0.004, phase=0.08, retphi=False):
    """y = (Phi, D) in s = ln r: Phi' = r g_AQUAL(G (Mb + D)/r^2), D' = -mu^2 r^3 Phi/G (D = M_eff - M_b).
    Phi0: array over systems (zero points). Returns nodes r (SI), g (n, nsys), D (n, nsys)."""
    mu = mu_Mpc / MPC; mu2 = mu * mu; r = grid(r0, r1, mu, hmax, phase)
    rm = np.sqrt(r[1:] * r[:-1]); Mn = Mfun(r); Mm = Mfun(rm)
    ph = np.array(Phi0, float).copy(); dd = np.zeros_like(ph); n = len(r)
    g = np.empty((n, ph.size)); Dst = np.empty((n, ph.size)); Pst = np.empty((n, ph.size))
    def f(rr, Mb, p, d):
        a = g_aqual(G * (Mb + d) / rr ** 2, a0); return rr * a, -mu2 * rr ** 3 * p / G, a
    for k in range(n - 1):
        h = math.log(r[k + 1] / r[k])
        k1p, k1d, gk = f(r[k], Mn[k], ph, dd); g[k] = gk; Dst[k] = dd; Pst[k] = ph
        k2p, k2d, _ = f(rm[k], Mm[k], ph + 0.5 * h * k1p, dd + 0.5 * h * k1d)
        k3p, k3d, _ = f(rm[k], Mm[k], ph + 0.5 * h * k2p, dd + 0.5 * h * k2d)
        k4p, k4d, _ = f(r[k + 1], Mn[k + 1], ph + h * k3p, dd + h * k3d)
        ph = ph + h / 6 * (k1p + 2 * k2p + 2 * k3p + k4p); dd = dd + h / 6 * (k1d + 2 * k2d + 2 * k3d + k4d)
    _, _, g[-1] = f(r[-1], Mn[-1], ph, dd); Dst[-1] = dd; Pst[-1] = ph
    return (r, g, Dst, Pst) if retphi else (r, g, Dst)


def at(r, y, x):
    """interpolate node values y (n, nsys) at radii x (SI) in ln r."""
    return np.array([np.interp(np.log(x), np.log(r), y[:, j]) for j in range(y.shape[1])]).T


def hernquist(Mb, ah_kpc=3.0):
    a = ah_kpc * KPC; return lambda r: Mb * r ** 2 / (r + a) ** 2


def tabulated(r_si, M_kg):
    """M_b(r) from tabulated points: (r/r_1)^3 inside the first point, linear in r between, flat beyond the last."""
    r_si = np.asarray(r_si, float); M_kg = np.maximum.accumulate(np.maximum(np.asarray(M_kg, float), 0.0))
    def f(x):
        x = np.asarray(x, float); y = np.interp(x, r_si, M_kg)
        return np.where(x < r_si[0], M_kg[0] * (x / r_si[0]) ** 3, y)
    return f


# ---------------------------------------------------------------- loaders (read-only reuse)
def load_qx10():
    sys.path.insert(0, os.path.join(CL6, "SV5_growth_mechanism"))
    import sv5_common as C
    return C.load_qx10()


def load_web():
    sys.path.insert(0, os.path.join(CL6, "SV5_growth_mechanism"))
    import sv5_common as C
    N3 = C.load_growth(); sigA, AX0 = C.sigma_A_rel(N3)
    S1 = json.load(open(os.path.join(CL6, "SV5_growth_mechanism", "iter_1_law_on_web", "sv5_iter1.json")))
    return N3, sigA, AX0, S1


class Web:
    """SV5 iter_1 projection with AeST's switch: Rr = 1 for comoving k < mu/(1+z), sqrt(B) above."""
    ZG = [0.25, 0.5, 1.0, 2.0, 3.0, 5.0, 8.0, 12.0, 20.0, 50.0]

    def __init__(s, N3, sigA, S1):
        s.N3, s.I2, s.M, s.sigA = N3, N3["I2"], N3["M"], sigA
        NG, LBOX = 128, 2000.0; kf = 2 * np.pi / LBOX; edges = np.geomspace(kf, np.pi * NG / LBOX, 17)
        s.kc = np.sqrt(edges[1:] * edges[:-1]); s.kg, s.zg = np.array(N3["kgrid"]), np.array(N3["zgrid"])
        s.c0, s.A0x = s.I2.best_amp_chi2(N3["X0"]); s.S1 = S1
        s.base = {}
        for f in A0:
            rows = S1["foot"][f]["rows"]; assert [r_["z"] for r_ in rows] == s.ZG
            for mode in ("W", "floor"):
                Bz = [np.array(r_["B_by_shell"]) if mode == "W" else np.full(16, r_["nu_min"] ** 2) for r_ in rows]
                s.base[(f, mode)] = s._grid(Bz)

    def _grid(s, Bz):
        lz = np.log1p(np.array(s.ZG)); Rr = np.empty((len(s.kg), len(s.zg)))
        lB = np.array([np.interp(np.log(s.kg), np.log(s.kc), np.sqrt(b)) for b in Bz])
        for j, z in enumerate(s.zg):
            x = np.clip(math.log1p(z), lz[0], lz[-1])
            for i in range(len(s.kg)): Rr[i, j] = np.interp(x, lz, lB[:, i])
        return Rr

    def grade(s, mu, foot, mode="W"):
        Rr = s.base[(foot, mode)].copy()
        if mu is not None:
            ksw = mu / (1.0 + s.zg)[None, :]; Rr = np.where(s.kg[:, None] < ksw, 1.0, Rr)
        S = s.I2.limber_ratio(s.M, s.N3["H0"], s.kg, s.zg, Rr); c, A = s.I2.best_amp_chi2(s.N3["X0"] * S)
        r = float(s.A0x / A); d = float(c - s.c0)
        return dict(r=r, dchi2=d, W1=bool(abs(r - 1) <= 3 * s.sigA), W2=bool(d <= s.I2.DCHI2_LINE))
