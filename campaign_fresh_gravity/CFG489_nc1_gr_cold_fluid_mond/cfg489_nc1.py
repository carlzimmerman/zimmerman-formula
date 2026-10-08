#!/usr/bin/env python3
"""CFG489: NC1's decisive tests (GR + Lambda chassis, MOND only in the cold fluid). Criteria: FROZEN_CRITERIA.md (6cce7b447).

Steps: (1) G1 well-posedness (linear dispersion, Petrovskii line); (2) H3 attractor (1-D spherical Lagrangian hydro from
cosmic-share infall, C core cfg489_core.c compiled at run time into a temporary directory); (3) H3 energy (static budget +
reservoir work); (4) G14 capture by the embedded Sun (Liouville cap + relaxation-limited build-up).

Run:   python3 cfg489_nc1.py               (main)
       CFG489_MUTATE=1 python3 cfg489_nc1.py   (MA anti-relaxation, MA-1D, MB target a0 -> 2 a0)
kappa = 1/2 FITTED; both footings; no dark-matter particle (the cold fluid's mass is still required); not "theory closed".
"""
import os
import sys
import json
import math
import time
import ctypes
import tempfile
import subprocess
from ctypes import c_int, c_long, c_double, POINTER
from concurrent.futures import ThreadPoolExecutor

sys.dont_write_bytecode = True
import numpy as np
from scipy.optimize import brentq
from scipy.special import gammainc
import sympy as sp

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))


def repo_root():
    env = os.environ.get("ZF_REPO")
    if env and os.path.isdir(os.path.join(env, "campaign_fresh_gravity")):
        return os.path.abspath(env)
    d = HERE
    for _ in range(8):
        if os.path.isdir(os.path.join(d, "campaign_fresh_gravity")):
            return d
        d = os.path.dirname(d)
    raise SystemExit("repo root not found; set ZF_REPO")


ROOT = repo_root()
CFG = os.path.join(ROOT, "campaign_fresh_gravity")
sys.path.insert(0, os.path.join(CFG, "CFG44_fluid_target"))
import Bcommon as BC  # noqa: E402  (read-only: nu_mono, nu_p2)

MUT = os.environ.get("CFG489_MUTATE", "0") == "1"
TAG = "_MUTATE" if MUT else ""
NTHREADS = int(os.environ.get("CFG489_THREADS", "4"))   # shared machine: <= 4 workers
LINES = []
CHECKS = []


def P(s=""):
    print(s, flush=True)
    LINES.append(str(s))


def check(name, ok, detail="", load_bearing=True):
    ok = bool(ok)
    CHECKS.append(dict(name=name, ok=ok, detail=detail, load_bearing=load_bearing))
    P(f"  [{'PASS' if ok else 'FAIL'}]{'' if load_bearing else ' (reported)'} {name}" + (f"  -- {detail}" if detail else ""))
    return ok


# ------------------------------------------------------------------------------------------------ constants (SI)
G = 6.67430e-11
MSUN = 1.98892e30
GM_SUN = 1.32712440018e20
AU = 1.495978707e11
PC = 3.0856775814913673e16
KPC = 1e3 * PC
YR = 3.15576e7
GYR = 1e9 * YR
A0 = {"canonical": 9.3603e-11, "alt": 1.1312e-10}
FOOTS = ["canonical", "alt"]
SHARE = 5.364
FB = 1.0 / (1.0 + SHARE)
H0 = 67.4e3 / (1e3 * KPC)
OM = 0.315
RHO_CRIT0 = 3 * H0 ** 2 / (8 * math.pi * G)
ZC = 1.0
GAMMA = 5.0 / 3.0
R_MARS, R_SAT = 1.523679 * AU, 9.5826 * AU
EPH = {"Mars": 1.4e-15, "Saturn": 7.0e-15}
V_REL = 230e3
NU = {"nu_mono": BC.nu_mono, "P2": BC.nu_p2}

OUT = dict(lane="CFG489", mutate=MUT, frozen_criteria="FROZEN_CRITERIA.md (6cce7b447, committed alone before any script; correction 1 32b3f9a35)",
           kappa="1/2 FITTED", inputs=dict(a0=A0, share=SHARE, z_c=ZC, gamma=GAMMA, eph=EPH, v_rel=V_REL))


# ------------------------------------------------------------------------------------------------ kernel tables
def kernel_table():
    """z = y nu(y) (g/a0 as a function of g_N/a0) on a fine grid, inverted onto a uniform ln z grid: ln y(z), dy/dz."""
    ly = np.linspace(math.log(1e-13), math.log(1e13), 520001)
    y = np.exp(ly)
    z = y * BC.nu_mono(y)
    lz = np.log(z)
    assert np.all(np.diff(lz) > 0)
    dlz_dly = np.gradient(lz, ly)                   # d ln z / d ln y
    dzdy = dlz_dly * z / y
    nz = 400001
    lzg = np.linspace(lz[0], lz[-1], nz)
    lyg = np.interp(lzg, lz, ly)
    dydz = 1.0 / np.interp(lzg, lz, dzdy)
    return dict(lnz0=float(lzg[0]), dlnz=float(lzg[1] - lzg[0]), nz=nz, LY=np.ascontiguousarray(lyg),
                DY=np.ascontiguousarray(dydz))


KT = kernel_table()


def gN_of_g(g, kernel):
    """g_N/a0 and dg_N/dg as functions of z = g/a0 (a0 = 1)."""
    z = np.asarray(g, float)
    if kernel == "P2":
        sq = np.sqrt(1 + 4 * z * z)
        return 0.5 * (-1 + sq), 2 * z / sq
    lz = np.log(z)
    lzg = KT["lnz0"] + KT["dlnz"] * np.arange(KT["nz"])
    y = np.exp(np.interp(lz, lzg, KT["LY"]))
    dy = np.interp(lz, lzg, KT["DY"])
    deep = lz < lzg[0]
    y = np.where(deep, z * z, y)
    dy = np.where(deep, 2 * z, dy)
    return y, dy


# ================================================================================================ controls K1, K2, K3
def K1_four_acceleration():
    t, x, y, z = sp.symbols("t x y z")
    eps, dl = sp.symbols("epsilon delta")
    X = [t, x, y, z]
    Phi = sp.Function("Phi")(*X)
    vs = [sp.Function(n)(*X) for n in ("v_x", "v_y", "v_z")]
    gm = sp.diag(-(1 + 2 * eps * Phi), 1 - 2 * eps * Phi, 1 - 2 * eps * Phi, 1 - 2 * eps * Phi)
    gi = sp.diag(*[1 / gm[i, i] for i in range(4)])
    Gam = [[[sp.Rational(1, 2) * gi[a, a] * (sp.diff(gm[a, b], X[c]) + sp.diff(gm[a, c], X[b]) - sp.diff(gm[b, c], X[a]))
             for c in range(4)] for b in range(4)] for a in range(4)]
    v2 = sum(v * v for v in vs)
    u0 = 1 / sp.sqrt((1 + 2 * eps * Phi) - (1 - 2 * eps * Phi) * dl ** 2 * v2)
    u = [u0] + [u0 * dl * v for v in vs]
    a1 = sum(u[n] * sp.diff(u[1], X[n]) for n in range(4)) + sum(Gam[1][b][c] * u[b] * u[c] for b in range(4) for c in range(4))
    at0 = {eps: 0, dl: 0}
    c00 = sp.simplify(a1.subs(at0))
    c01 = sp.simplify(sp.diff(a1, dl).subs(at0))
    c02 = sp.simplify(sp.diff(a1, dl, 2).subs(at0) / 2)
    c10 = sp.simplify(sp.diff(a1, eps).subs(at0))
    want01 = sp.diff(vs[0], t)
    want02 = sum(vs[j] * sp.diff(vs[0], X[j + 1]) for j in range(3))
    want10 = sp.diff(Phi, x)
    ok = (c00 == 0 and sp.simplify(c01 - want01) == 0 and sp.simplify(c02 - want02) == 0 and sp.simplify(c10 - want10) == 0)
    c11 = sp.simplify(sp.diff(a1, eps, dl).subs(at0))
    return ok, dict(c00=str(c00), c01=str(c01), c02=str(c02), c10=str(c10), c11_second_order=str(c11))


def K2_dispersion_symbolic():
    w, k, n, s, sig2, cs2, wJ, tau, rho0 = sp.symbols("omega k n s sigma2 cs2 omega_J tau rho0", positive=True)
    w = sp.Symbol("omega")
    I = sp.I
    # unknowns: drho, u, dps ; dPhi from Poisson; dP = cs2 drho
    drho, u, dps = sp.symbols("drho u dps")
    dPhi = -wJ ** 2 * drho / (rho0 * k ** 2)
    eq_cont = -I * w * drho + I * k * rho0 * u
    eq_mom = -I * w * rho0 * u + rho0 * I * k * dPhi + I * k * (cs2 * drho + dps)
    dA_kin = -I * w * u + I * k * dPhi                          # Dv/Dt + grad Phi (the TRUE 4-acceleration), linearised
    drho_t = (rho0 / wJ ** 2) * (1 - n) * (I * k) * dA_kin       # div[(I - N) dA]/4 pi G, longitudinal
    eq_rel = (1 - I * w * tau) * dps - s * sig2 * (drho - drho_t)
    Mx = sp.Matrix([[sp.diff(e_, v_) for v_ in (drho, u, dps)] for e_ in (eq_cont, eq_mom, eq_rel)])
    det = sp.expand(Mx.det())
    B = s * sig2 * (1 - n) * k ** 2 / wJ ** 2
    C = s * sig2 * (1 - (1 - n) * cs2 * k ** 2 / wJ ** 2)
    cubic = sp.expand((w ** 2 + wJ ** 2 - cs2 * k ** 2) * (1 + B - I * w * tau) - k ** 2 * C)
    ratio = sp.simplify(det / cubic)
    ok_cubic = ratio.free_symbols <= {rho0, k} and sp.simplify(sp.diff(ratio, w)) == 0
    # tau = 0 closed form
    w2 = sp.Symbol("W2")
    cub0 = sp.expand(cubic.subs(tau, 0)).subs(w ** 2, w2)
    sol = sp.solve(sp.Eq(cub0, 0), w2)
    closed = wJ ** 2 * ((cs2 + s * sig2 * n) * k ** 2 - wJ ** 2) / (wJ ** 2 + s * sig2 * (1 - n) * k ** 2)
    ok_tau0 = len(sol) == 1 and sp.simplify(sol[0] - closed) == 0
    jeans = sp.expand((w ** 2 + wJ ** 2 - cs2 * k ** 2) * (1 - I * w * tau))
    ok_s0 = sp.simplify(cubic.subs(s, 0) - jeans) == 0
    # A-kin equals -grad(P + p_s)/rho through the momentum equation
    u_sol = sp.solve(eq_mom, u)[0]
    ok_akin = sp.simplify(dA_kin.subs(u, u_sol) - (-I * k * (cs2 * drho + dps) / rho0)) == 0
    return ok_cubic and ok_tau0 and ok_s0 and ok_akin, dict(det_over_cubic=str(ratio), tau0=str(sol), ok_cubic=ok_cubic,
                                                            ok_tau0=ok_tau0, ok_jeans_s0=ok_s0, akin_identity=ok_akin)


# ================================================================================================ step (1) numerics
KGRID = np.logspace(-4, 8, 2401)       # k sigma / w_J


def cubic_roots(coef):
    """roots of a3 w^3 + a2 w^2 + a1 w + a0 (rows of coef), stable at large k: the largest root is taken from the companion
    eigenvalues and Newton-polished, then removed by BACKWARD deflation (the reversed polynomial, where it is the smallest
    root), and the remaining quadratic is solved with the cancellation-free formula; all roots get two Newton polishes."""
    a3, a2, a1, a0 = [coef[:, i] for i in range(4)]
    comp = np.zeros((len(a3), 3, 3), complex)
    comp[:, 0, :] = -coef[:, 1:] / coef[:, :1]
    comp[:, 1, 0] = 1
    comp[:, 2, 1] = 1
    ev = np.linalg.eigvals(comp)
    wL = ev[np.arange(len(a3)), np.argmax(np.abs(ev), axis=1)]
    Pf = lambda w: ((a3 * w + a2) * w + a1) * w + a0            # noqa: E731
    dP = lambda w: (3 * a3 * w + 2 * a2) * w + a1               # noqa: E731
    for _ in range(6):
        wL = wL - Pf(wL) / dP(wL)
    c2 = a0
    c1 = a1 + c2 / wL
    c0 = a2 + c1 / wL
    disc = np.sqrt(c1 * c1 - 4 * c0 * c2 + 0j)
    sgn = np.where(np.real(np.conj(c1) * disc) >= 0, 1.0, -1.0)
    q = -0.5 * (c1 + sgn * disc)
    q = np.where(q == 0, 1e-300, q)
    r1 = q / c0
    r2 = c2 / q
    R = np.stack([wL, r1, r2], axis=1)
    for _ in range(2):
        d = dP(R.T).T
        R = np.where(d != 0, R - Pf(R.T).T / np.where(d == 0, 1, d), R)
    return R


def growth(member, k, n, s, sig2, cs2, wJ, tau, ahyd=False):
    """max Im w over the roots, for each k (vectorised), plus the leading coefficient of the highest time derivative."""
    k = np.asarray(k, float)
    X = wJ ** 2 - cs2 * k ** 2
    C = s * sig2 * (1 - (1 - n) * cs2 * k ** 2 / wJ ** 2)
    B = s * sig2 * (1 - n) * k ** 2 / wJ ** 2
    if member == "M1":
        Y0 = np.ones_like(k) if ahyd else 1 + B
        c3 = -1j * tau * np.ones_like(k)
        # constant term X Y0 - k^2 C, written cancellation-free for A-kin: w_J^2 - (c_s^2 + s sigma^2 n) k^2
        a0c = (X - k ** 2 * C) if ahyd else (wJ ** 2 - (cs2 + s * sig2 * n) * k ** 2)
        coef = np.stack([c3, Y0 + 0j, -1j * tau * X, a0c + 0j], axis=1)
        lead = c3
        roots = cubic_roots(coef)
        G_ = np.max(roots.imag, axis=1)
        return G_, lead
    if member == "M2":
        Y0 = np.ones_like(k) if ahyd else 1 + B
        rhs = (k ** 2 * C - X) if ahyd else ((cs2 + s * sig2 * n) * k ** 2 - wJ ** 2) / np.where(Y0 == 0, np.nan, Y0)
        lead = Y0
    elif member == "M3":
        a = (1 + s * (1 - n)) * np.ones_like(k)
        rhs = (cs2 * k ** 2 - wJ ** 2 * (1 - s * n)) / np.where(a == 0, np.nan, a)
        lead = a
    root = np.sqrt(rhs + 0j)
    return np.abs(root.imag), lead


def growth_offtarget(k, n, s, sig2, cs2, wJ, tau, R):
    """post-freeze: M1 linearised about an OFF-target state, R = rho_t0/rho0 (p_eq = s P (1 - rho_t/rho)):
    (w^2 + X)(1 + B - i w tau) - k^2 C' = 0, C' = s[(1-R) cs2 + R sig2] - s sig2 (1-n) cs2 k^2/wJ^2; constant term written
    cancellation-free as wJ^2 - K_eff k^2, K_eff = cs2 (1 + s(1-R)) + s sig2 (R - 1 + n)."""
    k = np.asarray(k, float)
    X = wJ ** 2 - cs2 * k ** 2
    B = s * sig2 * (1 - n) * k ** 2 / wJ ** 2
    Keff = cs2 * (1 + s * (1 - R)) + s * sig2 * (R - 1 + n)
    coef = np.stack([-1j * tau * np.ones_like(k), 1 + B + 0j, -1j * tau * X, wJ ** 2 - Keff * k ** 2 + 0j], axis=1)
    return np.max(cubic_roots(coef).imag, axis=1), Keff


def petrovskii(member, n, s, sig2, cs2, wJ, tau, kmin_scored=None, ahyd=False):
    k = KGRID * wJ / math.sqrt(sig2)
    Gk, lead = growth(member, k, n, s, sig2, cs2, wJ, tau, ahyd)
    sc = np.ones_like(k, bool) if kmin_scored is None else (KGRID >= kmin_scored)
    lead_r = np.real(lead) if member != "M1" else np.abs(lead)
    pa = bool(np.all(lead_r[sc] > 0) or np.all(lead_r[sc] < 0)) and not np.any(np.isnan(np.asarray(Gk)[sc]))
    wref = max(wJ, 1.0 / tau) if (member == "M1" and tau > 0) else wJ
    Gs = np.where(np.isnan(Gk), np.inf, Gk)[sc]
    sup = float(np.max(Gs))
    pb = sup <= 2 * wref
    pc = bool(Gk[-1] <= Gk[-1 - 400] + 1e-9 * wref)      # 200 grid points per decade: k_max/100 is 400 points back
    # high-k character
    slope = float(np.log(max(Gs[-1], 1e-300) / max(Gs[-401], 1e-300)) / np.log(100.0)) if Gs[-1] > 0 and Gs[-401] > 0 else 0.0
    return dict(pass_=bool(pa and pb and pc), Pa=pa, Pb=pb, Pc=pc, sup_over_wref=sup / wref, slope_top=slope)


def step1(s_sign):
    res = {}
    allpass_M1 = True
    members = [("M1", False), ("M2", False), ("M3", False), ("M1", True), ("M2", True)]
    # (a) homogeneous
    for cs_lab, csr in [("adiabatic", GAMMA), ("isothermal", 1.0)]:
        for mem, hyd in members:
            r_ = petrovskii(mem, 0.0, s_sign, 1.0, csr, 1.0, 1.0, ahyd=hyd)
            key = f"homog|{cs_lab}|{mem}{'-hyd' if hyd else ''}"
            res[key] = r_
            if mem == "M1" and not hyd:
                allpass_M1 &= r_["pass_"]
    # (b) deep SIS
    for kern in ["nu_mono", "P2"]:
        for x in [3.0, 5.85, 10.0, 30.0, 100.0]:
            g0 = 1.0 / x
            gn, dgn = gN_of_g(np.array([g0]), kern)
            gn, dgn = float(gn[0]), float(dgn[0])
            for th in [0.0, math.pi / 4, math.pi / 2]:
                n = dgn * math.cos(th) ** 2 + (gn / g0) * math.sin(th) ** 2
                for cs_lab, csr in [("adiabatic", GAMMA), ("isothermal", 1.0)]:
                    for mem, hyd in members:
                        wJ, sig2, tau = 1.0 / x, 0.5, x
                        r_ = petrovskii(mem, n, s_sign, sig2, csr * sig2, wJ, tau, kmin_scored=3.0 / math.sqrt(2.0),
                                        ahyd=hyd)
                        r_["n"] = n
                        key = f"SIS|{kern}|x={x:g}|th={th:.3f}|{cs_lab}|{mem}{'-hyd' if hyd else ''}"
                        res[key] = r_
                        if mem == "M1" and not hyd:
                            allpass_M1 &= r_["pass_"]
    # (c) sweep (reported)
    sweep = {}
    for mem, hyd in members:
        okall = True
        worst = 0.0
        for n in [0.0, 0.01, 0.1, 0.5, 0.9, 0.99]:
            for wt in [0.1, 1.0, 10.0]:
                for csr in [1.0, GAMMA]:
                    r_ = petrovskii(mem, n, s_sign, 1.0, csr, 1.0, wt, ahyd=hyd)
                    okall &= r_["pass_"]
                    worst = max(worst, r_["sup_over_wref"])
        sweep[f"{mem}{'-hyd' if hyd else ''}"] = dict(all_pass=okall, worst_sup_over_wref=worst)
    return allpass_M1, res, sweep


# ================================================================================================ C core
class Params(ctypes.Structure):
    _fields_ = [("N", c_int), ("mode", c_int), ("ec", c_int), ("kernel", c_int), ("s", c_double), ("a0eff", c_double),
                ("gamma", c_double), ("C2", c_double), ("C1", c_double), ("cfl", c_double), ("rw", c_double),
                ("t_end", c_double), ("t_samp0", c_double), ("dt_samp", c_double), ("n_samp", c_int),
                ("max_steps", c_long), ("e_floor", c_double), ("nh", c_int), ("lnr0", c_double), ("dlnr", c_double),
                ("nz", c_int), ("lnz0", c_double), ("dlnz", c_double), ("wall_mode", c_int), ("point_host", c_int),
                ("Mcore", c_double)]


class Stats(ctypes.Structure):
    _fields_ = [("steps", c_long), ("crashed", c_int), ("t_final", c_double), ("n_floor", c_long), ("n_samp_done", c_int)]


_LIB = None


def lib():
    global _LIB
    if _LIB is None:
        tmp = tempfile.mkdtemp(prefix="cfg489_")
        so = os.path.join(tmp, "libcfg489.so")
        subprocess.run(["cc", "-O3", "-shared", "-fPIC", "-o", so, os.path.join(HERE, "cfg489_core.c"), "-lm"], check=True,
                       capture_output=True)
        _LIB = ctypes.CDLL(so)
        dp = POINTER(c_double)
        _LIB.run_nc1.argtypes = [POINTER(Params)] + [dp] * 5 + [dp] * 5 + [dp] * 4 + [POINTER(Stats)]
        _LIB.run_nc1.restype = c_int
        _LIB.target_mass.argtypes = [POINTER(Params), dp, dp, c_int, dp, dp, dp]
        _LIB.target_mass.restype = None
    return _LIB


def _p(a):
    return a.ctypes.data_as(POINTER(c_double))


# ------------------------------------------------------------------------------------------------ hosts (units G = M_b = a0 = 1)
RW = 0.05          # corrected numerics (FROZEN_CRITERIA correction 1; the frozen text had 0.02, see run 2)
DM1 = 2e-4         # mass of the innermost dynamic shell at N = 240 (smooth geometric shell masses; scaled as 240/N)
MAXSTEPS = 200_000_000   # resource cap (frozen text 4e7; correction 1)
NH = 40001
LNR0, LNR1 = math.log(1e-3), math.log(1e4)


def r_M_kpc(mb_msun, f):
    return math.sqrt(G * mb_msun * MSUN / A0[f]) / KPC


def host_tables(kind, f, mb_msun=1e10, a=None):
    lr = np.linspace(LNR0, LNR1, NH)
    r = np.exp(lr)
    if kind == "point":
        M = np.ones_like(r)
        rho = np.zeros_like(r)
    elif kind == "hernquist":
        M = r ** 2 / (r + a) ** 2
        rho = a / (2 * math.pi * r * (r + a) ** 3)
    elif kind in ("expsphere", "expshell"):
        rm = r_M_kpc(mb_msun, f)
        h = 2.0 / rm
        M = gammainc(3.0, r / h)
        rho = np.exp(-r / h) / (8 * math.pi * h ** 3)
        if kind == "expshell":
            Rs, w = 40.0 / rm, 0.5 / rm
            M = M + 10.0 * 0.5 * (1 + np.tanh((r - Rs) / w))
            rho = rho + 10.0 * 0.5 / np.cosh(np.clip((r - Rs) / w, -300, 300)) ** 2 / w / (4 * math.pi * r ** 2)
    else:
        raise ValueError(kind)
    # potential: Phi(r) = -M(rmax)/rmax - int_r^rmax M/r'^2 dr'
    integrand = M / r  # dr'/r'^2 * M = M/r' dln r'
    cum = np.concatenate([[0.0], np.cumsum(0.5 * (integrand[1:] + integrand[:-1]) * np.diff(lr))])
    Phi = -M[-1] / r[-1] - (cum[-1] - cum)
    return dict(M=np.ascontiguousarray(M), rho=np.ascontiguousarray(rho), Phi=np.ascontiguousarray(Phi), lr=lr, r=r,
                point=(kind == "point"), kind=kind)


def law(Mb_r, r, kernel="nu_mono", a0=1.0):
    gN = Mb_r / r ** 2
    nu = NU[kernel](gN / a0)
    return nu * gN, (nu - 1.0) * Mb_r


def host_M(H, r):
    """gravitating host mass (baryons + the inert core inside the wall)."""
    return np.interp(np.log(r), H["lr"], H["M"])


def host_Mb(H, r):
    """baryons only (what the law reads)."""
    return np.interp(np.log(r), H["lr"], H.get("Mbar", H["M"]))


def attach_core(H, kernel="nu_mono", a0=1.0):
    """correction 1: an inert core inside the wall holds the law's target phantom there, M_core = M_ph(<r_w); it is
    counted in gravity and in V_c, and equals the wall's own target r_w^2 F(g_wall)."""
    core = float(law(host_Mb(H, np.array([RW])), np.array([RW]), kernel, a0)[1][0])
    H2 = dict(H)
    H2["Mbar"] = H["M"].copy()
    H2["M"] = np.ascontiguousarray(H["M"] + core)
    H2["Phi"] = np.ascontiguousarray(H["Phi"] - core / H["r"])
    H2["core"] = core
    return H2


def supply_edge(H, kernel="nu_mono", a0=1.0):
    f = lambda x: float(law(host_Mb(H, np.array([x])), np.array([x]), kernel, a0)[1][0]) - SHARE  # noqa: E731
    return brentq(f, 0.5, 200.0, xtol=1e-12)


def R_ta_SI(mtot_kg, zc=ZC):
    rho_ta = (9 * math.pi ** 2 / 16) * OM * RHO_CRIT0 * (2 ** (2 / 3) * (1 + zc)) ** 3
    return (3 * mtot_kg / (4 * math.pi * rho_ta)) ** (1 / 3)


def Rta_over_rM(mb_msun, f):
    rM = math.sqrt(G * mb_msun * MSUN / A0[f])
    return R_ta_SI(mb_msun * MSUN / FB) / rM


# ------------------------------------------------------------------------------------------------ one run
NSH = 240


def mass_grid(N, total=SHARE, dm1=None):
    """correction 1: smooth geometric shell masses (constant neighbour ratio e^alpha), first shell dm1, sum = total."""
    dm1 = DM1 * 240.0 / N if dm1 is None else dm1
    al = brentq(lambda a: total * math.expm1(a) * math.exp(-a * N) / (-math.expm1(-a * N)) - dm1, 1e-8, 1.0)
    m = total * np.expm1(al * np.arange(1, N + 1)) / math.expm1(al * N)   # enclosed dynamic fluid mass at nodes 1..N
    dm = np.empty(N + 1)
    dm[0] = 0.0
    dm[1] = m[0]
    dm[2:] = np.diff(m)
    return m, dm


def target_state(H, N, kernel="nu_mono", a0=1.0):
    """discrete target: radii with M_ph(<r_i) - M_ph(<r_w) = m_i, hydrostatic P with P(surface) = 0, v = 0."""
    m, dm = mass_grid(N, SHARE - H.get("core", 0.0))
    rr = np.geomspace(RW, 300.0, 200001)
    Mph = law(host_Mb(H, rr), rr, kernel, a0)[1]
    Mph = np.maximum.accumulate(Mph)
    target = m + float(np.interp(RW, rr, Mph))
    r = np.empty(N + 1)
    r[0] = RW
    r[1:] = np.interp(target, Mph, rr)
    mb = np.empty(N + 1)
    mb[1:N] = 0.5 * (dm[1:N] + dm[2:N + 1])
    mb[N] = 0.5 * dm[N]
    mb[0] = 0.5 * dm[1]
    Menc = np.empty(N + 1)
    cum = mb[0]
    for i in range(1, N + 1):
        Menc[i] = cum + 0.5 * mb[i]
        cum += mb[i]
    gi = (host_M(H, r[1:]) + Menc[1:]) / r[1:] ** 2
    Pn = np.zeros(N + 2)
    for i in range(N, 0, -1):
        Pn[i] = Pn[i + 1] + gi[i - 1] * mb[i] / (4 * math.pi * r[i] ** 2)
    V = (4 * math.pi / 3) * (r[1:] ** 3 - r[:-1] ** 3)
    rho = dm[1:] / V
    e = np.zeros(N + 1)
    e[1:] = Pn[1:N + 1] / ((GAMMA - 1) * rho)
    return m, dm, r, np.zeros(N + 1), e


def infall_state(N, Rta, total=SHARE):
    m, dm = mass_grid(N, total)
    r = np.empty(N + 1)
    r[0] = RW
    r[1:] = Rta * (m / total) ** (1 / 3)
    e = np.full(N + 1, 1e-4)
    e[0] = 0.0
    return m, dm, r, np.zeros(N + 1), e


def run(H, state, t_end, te, mode=0, s=1.0, ec=0, kernel="nu_mono", a0eff=1.0, wall_mode=1, dt_samp=None, max_steps=MAXSTEPS,
        ps0=None, cfl=0.25):
    m, dm, r, v, e = [np.array(a, float) for a in state]
    N = len(dm) - 1
    ps = np.zeros(N + 1) if ps0 is None else np.array(ps0, float)
    dts = dt_samp if dt_samp is not None else 0.1 * te
    ns = int(t_end / dts) + 2
    prm = Params(N=N, mode=mode, ec=ec, kernel=(1 if kernel == "P2" else 0), s=s, a0eff=a0eff, gamma=GAMMA, C2=2.0, C1=0.3,
                 cfl=cfl, rw=float(r[0]), t_end=t_end, t_samp0=0.0, dt_samp=dts, n_samp=ns, max_steps=max_steps, e_floor=1e-12,
                 nh=NH, lnr0=LNR0, dlnr=(LNR1 - LNR0) / (NH - 1), nz=KT["nz"], lnz0=KT["lnz0"], dlnz=KT["dlnz"],
                 wall_mode=wall_mode, point_host=int(H.get("point", False)), Mcore=float(H.get("core", 0.0)))
    sr = np.zeros(ns * (N + 1))
    se = np.zeros(ns * (N + 1))
    sv = np.zeros(ns * (N + 1))
    sE = np.zeros(ns * 8)
    st = Stats()
    lib().run_nc1(ctypes.byref(prm), _p(H["M"]), _p(H["rho"]), _p(H["Phi"]), _p(KT["LY"]), _p(KT["DY"]), _p(dm), _p(r),
                  _p(v), _p(e), _p(ps), _p(sr), _p(se), _p(sv), _p(sE), ctypes.byref(st))
    k = st.n_samp_done
    return dict(m=m, dm=dm, sr=sr[:k * (N + 1)].reshape(k, N + 1), se=se[:k * (N + 1)].reshape(k, N + 1),
                sv=sv[:k * (N + 1)].reshape(k, N + 1), sE=sE[:k * 8].reshape(k, 8), steps=st.steps, crashed=st.crashed,
                t_final=st.t_final, n_floor=st.n_floor, ps=ps, r=r, e=e, v=v)


XG = None


def vc_profile(H, out, k, xg):
    r = out["sr"][k]
    mn = np.concatenate([[0.0], out["m"]])
    Mc = np.interp(xg, r, mn, left=0.0, right=mn[-1])
    return np.sqrt((host_M(H, xg) + Mc) / xg)


def score(H, out, te, t_s, xe, kernel="nu_mono", a0=1.0, frac=1.0):
    """time-average V_c over [t_s - 5 te, t_s]; D = max |log10(Vbar/V_law)| on x in [0.1, frac*xe]."""
    t = out["sE"][:, 0]
    sel = np.where((t >= t_s - 5 * te - 1e-9) & (t <= t_s + 1e-9))[0]
    if len(sel) == 0:
        return None, None
    xg = np.geomspace(0.1, frac * xe, 60)
    Vb = np.mean([vc_profile(H, out, k, xg) for k in sel], axis=0)
    gl = law(host_Mb(H, xg), xg, kernel, a0)[0]
    Vl = np.sqrt(xg * gl)
    dev = np.log10(Vb / Vl)
    return float(np.max(np.abs(dev))), dict(x=xg.tolist(), dev=dev.tolist(), Vbar=Vb.tolist())


def energy(out, k):
    row = out["sE"][k]
    return float(row[1] + row[2] + row[3]), row


# ================================================================================================ step (4) helpers
def mw_host(f):
    """CFG484 N1d's Milky Way host: P2 point-mass law, M_b = 6e10 Msun, R0 = 8.2 kpc."""
    a0 = A0[f]
    Mb = 6e10 * MSUN
    R0 = 8.2 * KPC
    rM = math.sqrt(G * Mb / a0)
    xx = R0 / rM
    rho = Mb * xx / (4 * math.pi * R0 ** 2 * rM * math.sqrt(1 + xx ** 2))
    gN = G * Mb / R0 ** 2
    gt = math.sqrt(gN ** 2 + a0 * gN)
    Vc = math.sqrt(R0 * gt)
    return dict(rho=rho, sigma=Vc / math.sqrt(2), Vc=Vc, g_host=gt, R0=R0)


def sun_R2(r, f, kernel="nu_mono"):
    gN = GM_SUN / r ** 2
    return (float(NU[kernel](np.array(gN / A0[f]))) - 1.0) * gN


def liouville_R1(f):
    h = mw_host(f)
    fmax = h["rho"] / ((2 * math.pi) ** 1.5 * h["sigma"] ** 3)
    out = {}
    for pl, rr in [("Mars", R_MARS), ("Saturn", R_SAT)]:
        Mcap = 4 * math.pi * fmax * (4 * math.pi / 3) * (2 * GM_SUN) ** 1.5 * (2.0 / 3.0) * rr ** 1.5
        dg = G * Mcap / rr ** 2
        out[pl] = dict(dg=dg, ratio=dg / EPH[pl])
    return out


def transit_bound(r, f, tau, v=V_REL):
    h = mw_host(f)
    Rfar = math.sqrt(GM_SUN / h["g_host"])
    return 3.0 * (2 * r / (v * tau)) * (1 + (4.0 / 3.0) * (h["sigma"] ** 2 / v ** 2) * (1 + math.log(Rfar / r))), Rfar


def step4():
    res = {}
    ok4a = ok4b = ok4c = True
    for f in FOOTS:
        h = mw_host(f)
        row = dict(host=dict(rho_kg_m3=h["rho"], rho_Msun_pc3=h["rho"] * PC ** 3 / MSUN, sigma_kms=h["sigma"] / 1e3,
                             g_host=h["g_host"]))
        R1 = liouville_R1(f)
        row["4a_liouville"] = R1
        ok4a &= all(R1[p]["ratio"] <= 0.1 for p in R1)
        tau_loc = 1.0 / math.sqrt(4 * math.pi * G * h["rho"])
        row["tau_local_Myr"] = tau_loc / (1e6 * YR)
        for pl, rr in [("Mars", R_MARS), ("Saturn", R_SAT)]:
            fb, Rfar = transit_bound(rr, f, tau_loc)
            for kern in ["nu_mono", "P2"]:
                R2 = sun_R2(rr, f, kern)
                an = fb * R2
                row[f"4b_{pl}_{kern}"] = dict(t_res_over_tau=2 * rr / (V_REL * tau_loc), f_bound=fb, R2=R2,
                                              R2_ratio=R2 / EPH[pl], anomaly=an, ratio=an / EPH[pl])
                if kern == "nu_mono":
                    ok4b &= an <= 0.1 * EPH[pl]
            rho_orb = (GM_SUN / rr) / (4 * math.pi * G * rr ** 2)
            tau_orb = 1.0 / math.sqrt(4 * math.pi * G * rho_orb)
            fo = min(1.0, transit_bound(rr, f, tau_orb)[0])
            R2 = sun_R2(rr, f)
            row[f"4c_{pl}"] = dict(tau_orb_days=tau_orb / 86400, t_res_over_tau=2 * rr / (V_REL * tau_orb), f=fo,
                                   anomaly=fo * R2, ratio=fo * R2 / EPH[pl])
            ok4c &= fo * R2 <= 0.1 * EPH[pl]
            row["R_far_AU"] = Rfar / AU
        cs2 = GAMMA * h["sigma"] ** 2
        for lab, c2 in [("sigma2", h["sigma"] ** 2), ("adiabatic_cs2", cs2)]:
            rB = 2 * GM_SUN / (V_REL ** 2 + c2)
            Mdot = 4 * math.pi * GM_SUN ** 2 * h["rho"] / (V_REL ** 2 + c2) ** 1.5
            row[f"4d_BHL_{lab}"] = dict(r_BH_AU=rB / AU, Mdot_kg_s=Mdot, M_accreted_Msun_4p6Gyr=Mdot * 4.6 * GYR / MSUN)
        res[f] = row
    verdict = "PASS" if (ok4a and ok4b and ok4c) else ("COND" if (ok4a and ok4b) else "FAIL")
    return verdict, dict(ok4a=ok4a, ok4b=ok4b, ok4c=ok4c), res


# ================================================================================================ main
XC = np.geomspace(0.1, 8.0, 90)        # common grid for stored profiles (MB comparison)


def cell_specs():
    specs = []
    for f in FOOTS:
        for lm in [9, 10, 11, 12]:
            specs.append(dict(name=f"point|1e{lm}|{f}", kind="point", f=f, mb=10.0 ** lm))
    for f in FOOTS:
        for a in [0.1, 0.3, 1.0, 3.0]:
            specs.append(dict(name=f"hernquist|a={a:g}|{f}", kind="hernquist", f=f, mb=1e10, a=a))
    for f in FOOTS:
        specs.append(dict(name=f"farshell_A|{f}", kind="expsphere", f=f, mb=1e10))
        specs.append(dict(name=f"farshell_B|{f}", kind="expshell", f=f, mb=1e10))
    return specs


def host_of(sp_, kernel="nu_mono"):
    return attach_core(host_tables(sp_["kind"], sp_["f"], sp_["mb"], sp_.get("a")), kernel)


def do_infall(sp_, mode=0, s=1.0, ec=0, kernel="nu_mono", a0eff=1.0, N=None, max_steps=MAXSTEPS, cfl=0.25):
    t0 = time.time()
    H = host_of(sp_, kernel)
    xe = supply_edge(H, kernel)
    te = xe
    Rta = Rta_over_rM(sp_["mb"], sp_["f"])
    tcoll = (math.pi / 2) * math.sqrt(Rta ** 3 / (2 * (1 + SHARE)))
    t_end = tcoll + 40 * te
    out = run(H, infall_state(N or NSH, Rta, SHARE - H["core"]), t_end, te, mode=mode, s=s, ec=ec, kernel=kernel,
              a0eff=a0eff, max_steps=max_steps, cfl=cfl)
    res = dict(name=sp_["name"], mode=mode, s=s, ec=ec, kernel=kernel, a0eff=a0eff, N=N or NSH, x_e=xe, Rta_rM=Rta,
               t_coll=tcoll, t_e=te, t_end=t_end, crashed=int(out["crashed"]), steps=int(out["steps"]),
               t_final=float(out["t_final"]), n_floor=int(out["n_floor"]))
    done = out["crashed"] == 0 and out["t_final"] >= t_end - 1e-9
    res["D40_0.9xe"] = None
    res["Vbar_common"] = None
    for q in (10, 20, 40):
        D, prof = score(H, out, te, tcoll + q * te, xe, kernel) if out["t_final"] >= tcoll + q * te - 1e-9 else (None, None)
        res[f"D{q}"] = D
        if q == 40 and prof is not None:
            res["prof40"] = dict(x=prof["x"][::6], dev=prof["dev"][::6])
            D9, _ = score(H, out, te, tcoll + q * te, xe, kernel, frac=0.9)
            res["D40_0.9xe"] = D9
            t = out["sE"][:, 0]
            sel = np.where((t >= tcoll + 35 * te - 1e-9) & (t <= tcoll + 40 * te + 1e-9))[0]
            res["Vbar_common"] = np.mean([vc_profile(H, out, k, XC) for k in sel], axis=0).tolist()
    res["completed"] = bool(done)
    res["settled"] = (done and res["D40"] is not None and res["D20"] is not None and abs(res["D40"] - res["D20"]) <= 0.02)
    res["pass"] = bool(res["settled"] and res["D40"] <= 0.05)
    if len(out["sE"]):
        E0, _ = energy(out, 0)
        E1, row = energy(out, len(out["sE"]) - 1)
        res.update(E_i=E0, E_end=E1, W_res=float(row[4]), S_ps=float(row[5]), S_q=float(row[6]))
        # fraction of fluid inside the edge at the end, and the outer radius
        res["r_surface_end"] = float(out["sr"][-1][-1])
        res["mass_inside_xe_end"] = float(np.interp(xe, out["sr"][-1], np.concatenate([[0.0], out["m"]]), right=SHARE))
    res["sec"] = time.time() - t0
    return res


def do_posthoc(sp_, kind):
    """post-freeze diagnostics (reported, not verdict inputs) on one cell:
    'late': pure hydro (s = 0) to t_coll + 5 t_e (virialised), then M1 switched on for 40 t_e;
    'frozen': the M1 infall on the FROZEN numerics (wall 0.02 r_M, M_t,0 = 0, no core, enclosed-mass grid geometric from
              2e-4 M_b), to show in the same run what run 2 found (the early crash)."""
    t0 = time.time()
    H = host_of(sp_)
    xe = supply_edge(H)
    te = xe
    Rta = Rta_over_rM(sp_["mb"], sp_["f"])
    tcoll = (math.pi / 2) * math.sqrt(Rta ** 3 / (2 * (1 + SHARE)))
    res = dict(name=sp_["name"], kind=kind, x_e=xe, t_e=te, t_coll=tcoll)
    if kind == "late":
        t1 = tcoll + 5 * te
        o1 = run(H, infall_state(NSH, Rta, SHARE - H["core"]), t1, te, mode=0, s=0.0)
        st = (o1["m"], o1["dm"], o1["r"], o1["v"], o1["e"])
        out = run(H, st, 40 * te, te, mode=0, s=1.0)
        res.update(phase1_crashed=int(o1["crashed"]), t_switch=t1)
        tq = lambda q: q * te  # noqa: E731
    else:
        H0 = host_tables(sp_["kind"], sp_["f"], sp_["mb"], sp_.get("a"))
        out = run(H0, frozen_infall_state(NSH, Rta), tcoll + 40 * te, te, mode=0, s=1.0, wall_mode=0, max_steps=40_000_000)
        tq = lambda q: tcoll + q * te  # noqa: E731
    res.update(crashed=int(out["crashed"]), steps=int(out["steps"]), t_final=float(out["t_final"]),
               t_end=float(tq(40)))
    for q in (10, 20, 40):
        res[f"D{q}"] = score(H, out, te, tq(q), xe)[0] if out["t_final"] >= tq(q) - 1e-9 else None
    if len(out["sE"]):
        k = len(out["sE"]) - 1
        res["mass_inside_xe_end"] = float(np.interp(xe, out["sr"][k], np.concatenate([[0.0], out["m"]]), right=out["m"][-1]))
    res["sec"] = time.time() - t0
    return res


def frozen_infall_state(N, Rta):
    """the frozen text's numerics: enclosed-mass grid geometric from 2e-4 M_b, wall 0.02 r_M (no core)."""
    m = np.geomspace(2e-4, SHARE, N)
    dm = np.concatenate([[0.0, m[0]], np.diff(m)])
    r = np.concatenate([[0.02], Rta * (m / SHARE) ** (1 / 3)])
    e = np.full(N + 1, 1e-4)
    e[0] = 0.0
    return m, dm, r, np.zeros(N + 1), e


def frozen_target_state(H0, N):
    """the frozen numerics' discrete target (wall 0.02, M_t,0 = 0, no core) for the C-static re-check."""
    m = np.geomspace(2e-4, SHARE, N)
    dm = np.concatenate([[0.0, m[0]], np.diff(m)])
    rr = np.geomspace(0.02, 300.0, 200001)
    Mph = np.maximum.accumulate(law(host_Mb(H0, rr), rr)[1])
    r = np.concatenate([[0.02], np.interp(m + float(np.interp(0.02, rr, Mph)), Mph, rr)])
    mb = np.empty(N + 1)
    mb[1:N] = 0.5 * (dm[1:N] + dm[2:N + 1])
    mb[N] = 0.5 * dm[N]
    mb[0] = 0.5 * dm[1]
    Menc = np.empty(N + 1)
    cum = mb[0]
    for i in range(1, N + 1):
        Menc[i] = cum + 0.5 * mb[i]
        cum += mb[i]
    gi = (host_M(H0, r[1:]) + Menc[1:]) / r[1:] ** 2
    Pn = np.zeros(N + 2)
    for i in range(N, 0, -1):
        Pn[i] = Pn[i + 1] + gi[i - 1] * mb[i] / (4 * math.pi * r[i] ** 2)
    rho = dm[1:] / ((4 * math.pi / 3) * (r[1:] ** 3 - r[:-1] ** 3))
    e = np.concatenate([[0.0], Pn[1:N + 1] / ((GAMMA - 1) * rho)])
    return m, dm, r, np.zeros(N + 1), e


def do_static_frozen(sp_, t_len_te=20.0):
    H0 = host_tables(sp_["kind"], sp_["f"], sp_["mb"], sp_.get("a"))
    xe = supply_edge(H0)
    out = run(H0, frozen_target_state(H0, NSH), t_len_te * xe, xe, mode=0, s=1.0, wall_mode=0, max_steps=40_000_000)
    k = len(out["sE"]) - 1
    return dict(name=sp_["name"], crashed=int(out["crashed"]), steps=int(out["steps"]), t_final=float(out["t_final"]),
                t_end=t_len_te * xe, D_end=score(H0, out, xe, out["sE"][k, 0], xe)[0])


def do_static(sp_, t_len_te=20.0, escale=1.0, wall_mode=1, kernel="nu_mono", mode=0, s=1.0, mscale_out=None):
    H = host_of(sp_, kernel)
    xe = supply_edge(H, kernel)
    te = xe
    m, dm, r, v, e = target_state(H, NSH, kernel)
    e = e * escale
    if mscale_out is not None:                     # post-freeze diagnostic: dilute the fluid beyond x = 1 by a factor
        xcut, fac = mscale_out
        rc = 0.5 * (r[1:] + r[:-1])
        dm = dm.copy()
        dm[1:] = np.where(rc > xcut, dm[1:] * fac, dm[1:])
        m = np.cumsum(dm[1:])
    out = run(H, (m, dm, r, v, e), t_len_te * te, te, mode=mode, s=s, kernel=kernel, wall_mode=wall_mode)
    res = dict(name=sp_["name"], escale=escale, wall_mode=wall_mode, crashed=int(out["crashed"]), steps=int(out["steps"]),
               t_final=float(out["t_final"]), t_end=t_len_te * te)
    k = len(out["sE"]) - 1
    if k >= 0:
        D, prof = score(H, out, te, out["sE"][k, 0], xe, kernel)
        res.update(D_end=D, max_v=float(np.max(np.abs(out["sv"][k]))), E_t=energy(out, 0)[0],
                   r1_end=float(out["sr"][k][1]), r1_init=float(r[1]), prof=dict(x=prof["x"][::6], dev=prof["dev"][::6]))
    return res


def energy_target(sp_, kernel="nu_mono"):
    H = host_of(sp_, kernel)
    xe = supply_edge(H, kernel)
    out = run(H, target_state(H, NSH, kernel), 0.0, xe, mode=0, s=1.0, kernel=kernel)
    E, row = energy(out, 0)
    return dict(E_t=E, U_t=float(row[2]), W_t=float(row[3]))


def main():
    P("=" * 110)
    P("CFG489: NC1's decisive tests (GR + Lambda chassis, MOND only in the cold fluid)" + ("   [MUTATE]" if MUT else ""))
    P("kappa = 1/2 FITTED; both footings; no dark-matter particle (cold mass still required); not 'theory closed'")
    P("criteria: FROZEN_CRITERIA.md (6cce7b447) + appended correction 1 (32b3f9a35: numerics only; run 2 kept as _run2)")
    P("=" * 110)

    # ---------------------------------------------------------------------------------------------- controls K1-K3
    P("\n[K1] sympy: Newtonian-limit 4-acceleration of a moving fluid element")
    ok, d = K1_four_acceleration()
    check("K1 a^i = dv/dt + (v.grad)v + grad Phi to first order (residual terms are Phi*v, v*dPhi/dt, ...)", ok,
          f"eps*delta coefficient: {d['c11_second_order']}")
    OUT["K1"] = d
    P("\n[K2] sympy: the M1 cubic from the linear system (A read kinematically)")
    ok, d = K2_dispersion_symbolic()
    check("K2 det(linear system) = const x cubic; tau = 0 closed form; s = 0 gives Jeans; A-kin = -grad(P+p_s)/rho", ok,
          f"det/cubic = {d['det_over_cubic']}")
    OUT["K2"] = d
    P("\n[K3] kernel facts: g_N'(g) and g_N(g)/g in (0, 1) on g in [1e-8, 1e8] a0")
    # cancellation-free forms (run 1 computed 1 - g_N' as a difference and P2's g_N' rounds to 1.0 at g = 1e8 a0):
    #   P2:  g_N' = 2z/sqrt(1+4z^2),  1 - g_N' = 1/(sqrt(1+4z^2)(sqrt(1+4z^2) + 2z)),
    #        g_N/g = y/z,  1 - g_N/g = 2/(2z + 1 + sqrt(1+4z^2));
    #   nu_mono (z = y + H(y)):  g_N' = 1/(1 + H'),  1 - g_N' = H'/(1 + H'),  g_N/g = y/(y + H),  1 - g_N/g = H/(y + H).
    gg = np.geomspace(1e-8, 1e8, 20001)
    k3 = {}
    sq = np.sqrt(1 + 4 * gg * gg)
    yP = 0.5 * (-1 + sq)
    k3["P2"] = dict(min_dgN=float(np.min(2 * gg / sq)), min_1m_dgN=float(np.min(1 / (sq * (sq + 2 * gg)))),
                    min_ratio=float(np.min(yP / gg)), min_1m_ratio=float(np.min(2 / (2 * gg + 1 + sq))))
    yy = np.geomspace(1e-14, 1e9, 400001)          # the record's table range (Bcommon: y >= 1e-14)
    HH = np.interp(np.log10(yy), BC._LYG, BC._HM)
    Hp = np.gradient(HH, yy)
    zz = yy + HH
    sel = (zz >= 1e-8) & (zz <= 1e8)
    zd = np.geomspace(1e-8, zz[0], 200)              # below the table: the deep form y = z^2 (as the C core uses)
    k3["nu_mono"] = dict(min_dgN=float(min(np.min(1 / (1 + Hp[sel])), np.min(2 * zd))),
                         min_1m_dgN=float(min(np.min(Hp[sel] / (1 + Hp[sel])), np.min(1 - 2 * zd))),
                         min_ratio=float(min(np.min(yy[sel] / zz[sel]), np.min(zd))),
                         min_1m_ratio=float(min(np.min(HH[sel] / zz[sel]), np.min(1 - zd))),
                         z_table=[float(zz[sel][0]), float(zz[sel][-1])])
    ok3 = all(k3[k]["min_dgN"] > 0 and k3[k]["min_1m_dgN"] > 0 and k3[k]["min_ratio"] > 0 and k3[k]["min_1m_ratio"] > 0
              for k in k3)
    check("K3 n in (0, 1) for every background (both kernels; g_N', 1 - g_N', g_N/g, 1 - g_N/g all > 0, cancellation-free)",
          ok3, json.dumps({k: {q: (f'{v:.3g}' if not isinstance(v, list) else v) for q, v in k3[k].items()} for k in k3}))
    OUT["K3"] = k3

    # ---------------------------------------------------------------------------------------------- step (1)
    s1 = -1.0 if MUT else 1.0
    P(f"\n[STEP 1] G1 well-posedness: dispersion of the linearised relaxation system, s = {s1:+g}"
      + ("  [MUTATE MA: anti-relaxation]" if MUT else ""))
    pass1, res1, sweep1 = step1(s1)
    for key in ["homog|adiabatic|M1", "homog|isothermal|M1", "homog|adiabatic|M2", "homog|adiabatic|M3",
                "homog|adiabatic|M1-hyd", "homog|adiabatic|M2-hyd"]:
        r_ = res1[key]
        P(f"  {key:28s} Pa {r_['Pa']!s:5s} Pb {r_['Pb']!s:5s} Pc {r_['Pc']!s:5s}  sup G/w_ref {r_['sup_over_wref']:.3e}  "
          f"top-decade growth slope {r_['slope_top']:+.3f}  -> {'PASS' if r_['pass_'] else 'FAIL'}")
    for mem in ["M1", "M2", "M3", "M1-hyd", "M2-hyd"]:
        cells = {k: v for k, v in res1.items() if k.startswith("SIS|") and k.endswith("|" + mem)}
        npass = sum(v["pass_"] for v in cells.values())
        worst = max(v["sup_over_wref"] for v in cells.values())
        P(f"  SIS ({len(cells)} cells: x 3-100, 3 angles, 2 kernels, adiabatic/isothermal) {mem:7s}: {npass}/{len(cells)} pass; "
          f"worst sup G/w_ref {worst:.3e}; sweep (all frozen coefficients): {'all pass' if sweep1[mem]['all_pass'] else 'FAILS'} "
          f"(worst {sweep1[mem]['worst_sup_over_wref']:.3e})")
    # high-k damping character of M1 (parabolic ~ k^2)
    kk = np.array([1e4, 1e6]) * 1.0
    co_damp = []
    for kv in kk:
        X = 1 - GAMMA * kv ** 2
        B = s1 * (kv ** 2)
        coef = np.array([[-1j, 1 + B, -1j * X, 1 - (GAMMA + 0) * kv ** 2 + 0j]])
        co_damp.append(float(np.min(cubic_roots(coef).imag)))
    damp_slope = math.log(abs(co_damp[1]) / abs(co_damp[0])) / math.log(100.0)
    P(f"  M1 high-k character (homogeneous): fastest root Im w = {co_damp[0]:.3e} at k = 1e4, {co_damp[1]:.3e} at k = 1e6 "
      f"-> |Im w| ~ k^{damp_slope:.2f} ({'parabolic damping' if s1 > 0 else 'parabolic GROWTH'}); relativistic causality: COND "
      f"(needs a second-order regulator; not PASS here)")
    # post-freeze: the same line applied OFF the target (R = rho_t0/rho0), the regime a settling fluid passes through
    off = {}
    P("  post-freeze (reported, not a verdict input): M1 linearised about an OFF-target state, R = rho_t/rho; homogeneous "
      "frozen coefficients (n = 0, w_J tau = 1); K_eff = c_s^2 (1 + s(1-R)) + s sigma^2 (R - 1 + n)")
    for glab, gcs in [("gamma 5/3", GAMMA), ("isothermal", 1.0)]:
        row = []
        for R in [1.0, 2.0, 3.5, 4.0, 10.0, 30.0, 100.0, 1e4]:
            Gk, Ke = growth_offtarget(KGRID, 0.0, s1, 1.0, gcs, 1.0, 1.0, R)
            row.append(dict(R=R, K_eff=Ke, sup_G=float(np.max(Gk)), G_kmax=float(Gk[-1]),
                            frozen_line_pass=bool(np.max(Gk) <= 2.0 and Gk[-1] <= Gk[-401] + 1e-9)))
        off[glab] = row
        P(f"    {glab:10s}: " + "; ".join(f"R {r_['R']:g}: K_eff {r_['K_eff']:+.2f}, G(k_max) {r_['G_kmax']:+.2f}, sup {r_['sup_G']:.2f}"
                                       f"{'' if r_['frozen_line_pass'] else ' FAILS line'}" for r_ in row))
    Rstar = (GAMMA + s1 * (GAMMA - 1)) / (s1 * (GAMMA - 1)) if s1 > 0 else float("nan")
    if s1 > 0:
        P(f"    -> with gamma = 5/3 and s = +1, K_eff < 0 for R > {Rstar:.2f} (+1.5 n): growth at EVERY large k (rate ~ "
          f"w_J sqrt((gamma-1)(R - R*)), bounded in k but not in R); the frozen line fails for R >~ 30. Isothermal: K_eff = "
          f"sigma^2 (1 + s n) > 0 for every R (no off-target instability)")
    else:
        P("    -> s = -1 (MUTATE): every R and both closures fail the line (growth ~ k^2 from the anti-relaxation itself)")
    OUT["step1_offtarget_posthoc"] = dict(rows=off, R_star=Rstar)
    check(f"STEP 1 PASS for the scored member M1 (s = {s1:+g})", pass1,
          "homogeneous + every SIS cell, both kernels, adiabatic and isothermal", load_bearing=not MUT)
    OUT["step1"] = dict(s=s1, M1_pass=pass1, cells=res1, sweep=sweep1, M1_damp_slope=damp_slope, causality="COND")
    verdict1 = "PASS" if pass1 else "FAIL"

    # ---------------------------------------------------------------------------------------------- controls K4-K6
    P("\n[K4] C target routine at static A = g_law reproduces the P2 point-mass cold mass; nu_mono supply edge")
    xs = np.geomspace(0.1, 10, 200)
    gl = np.sqrt((1 / xs ** 2) ** 2 + 1 / xs ** 2)
    prm = Params(kernel=1, a0eff=1.0, nz=KT["nz"], lnz0=KT["lnz0"], dlnz=KT["dlnz"])
    Mt = np.zeros_like(xs)
    lib().target_mass(ctypes.byref(prm), _p(KT["LY"]), _p(KT["DY"]), len(xs), _p(np.ascontiguousarray(xs)),
                      _p(np.ascontiguousarray(gl)), _p(Mt))
    k4a = float(np.max(np.abs(Mt / (np.sqrt(1 + xs ** 2) - 1) - 1)))
    prm.kernel = 0
    gl2 = law(np.ones_like(xs), xs)[0]
    Mt2 = np.zeros_like(xs)
    lib().target_mass(ctypes.byref(prm), _p(KT["LY"]), _p(KT["DY"]), len(xs), _p(np.ascontiguousarray(xs)),
                      _p(np.ascontiguousarray(gl2)), _p(Mt2))
    k4c = float(np.max(np.abs(Mt2 / law(np.ones_like(xs), xs)[1] - 1)))
    xe_pt = supply_edge(host_tables("point", "canonical"))
    check("K4 P2 point-mass target M(sqrt(1+x^2)-1) <= 1e-6 rel; nu_mono edge 5.8498 +- 0.001", k4a <= 1e-6 and
          abs(xe_pt - 5.8498) <= 1e-3, f"P2 max rel {k4a:.1e}; nu_mono table round trip {k4c:.1e}; x_e = {xe_pt:.5f}")
    OUT["K4"] = dict(P2_maxrel=k4a, numono_roundtrip=k4c, x_e=xe_pt)
    P("\n[K5] CFG461 contraction factors (z_c = 1, canonical)")
    k5 = []
    for lm, want in [(9.0, 3.50), (10.5, 1.97), (11.5, 1.34)]:
        mb = 10 ** lm
        rM = math.sqrt(G * mb * MSUN / A0["canonical"])
        re = rM / math.log(1 / (1 - FB))
        val = (5 / 12) * R_ta_SI(mb * MSUN / FB) / re
        k5.append((lm, val, want))
    check("K5 R_vir/r_e = 3.50 / 1.97 / 1.34 to 1%", all(abs(v / w - 1) <= 0.01 for _, v, w in k5),
          ", ".join(f"{v:.3f}" for _, v, _ in k5))
    OUT["K5"] = k5
    P("\n[K6] CFG484 N1d reproduces from its committed JSON")
    j484 = json.load(open(os.path.join(CFG, "CFG484_alternative_chassis_search", "cfg484_results.json")))
    k6 = {}
    ok6 = True
    for f in FOOTS:
        n1d = j484["NC1"]["N1d"][f]
        R1 = liouville_R1(f)
        for pl, rr in [("Mars", R_MARS), ("Saturn", R_SAT)]:
            a = R1[pl]["ratio"] / n1d["R1_boost1"]["planets"][pl]["ratio_to_bound"]
            b = (sun_R2(rr, f) / EPH[pl]) / n1d[f"R2_nu_mono_{pl}"]["ratio"]
            k6[f"{f}|{pl}"] = (a, b)
            ok6 &= abs(a - 1) <= 0.01 and abs(b - 1) <= 0.01
    check("K6 R1 Liouville ratios and R2 nu_mono ratios match CFG484 to 1%", ok6,
          ", ".join(f"{k}: {a:.4f}/{b:.4f}" for k, (a, b) in k6.items()))
    OUT["K6"] = {k: list(v) for k, v in k6.items()}

    # ---------------------------------------------------------------------------------------------- step (4) (cheap)
    P("\n[STEP 4] G14 capture by the embedded Sun (v_rel 230 km/s)")
    verdict4, ok4, res4 = step4()
    for f in FOOTS:
        r_ = res4[f]
        P(f"  {f:9s} host rho {r_['host']['rho_Msun_pc3']:.4f} Msun/pc^3, sigma {r_['host']['sigma_kms']:.0f} km/s, "
          f"tau_local {r_['tau_local_Myr']:.1f} Myr, R_far {r_['R_far_AU']:.0f} AU")
        for pl in ["Mars", "Saturn"]:
            a = r_["4a_liouville"][pl]
            b = r_[f"4b_{pl}_nu_mono"]
            bp = r_[f"4b_{pl}_P2"]
            c = r_[f"4c_{pl}"]
            P(f"    {pl:6s} (4a) Liouville {a['ratio']:.2e} x bound | (4b) t_res/tau {b['t_res_over_tau']:.2e}, f <= "
              f"{b['f_bound']:.2e}, x R2 ({b['R2_ratio']:.0f}x bound) = {b['ratio']:.2e} x bound (P2 {bp['ratio']:.2e}) | "
              f"(4c) orbital tau {c['tau_orb_days']:.1f} d, t_res/tau {c['t_res_over_tau']:.2f}, f {c['f']:.2f} -> "
              f"{c['ratio']:.0f} x bound")
        P(f"    (4d) BHL radius {r_['4d_BHL_sigma2']['r_BH_AU']:.3f} AU (adiabatic c_s: {r_['4d_BHL_adiabatic_cs2']['r_BH_AU']:.3f}); "
          f"accreted in 4.6 Gyr {r_['4d_BHL_sigma2']['M_accreted_Msun_4p6Gyr']:.1e} Msun (into the Sun)")
    P(f"  -> STEP 4 = {verdict4} (4a {ok4['ok4a']}, 4b {ok4['ok4b']}, 4c {ok4['ok4c']})")
    OUT["step4"] = dict(verdict=verdict4, ok=ok4, rows=res4)

    # ---------------------------------------------------------------------------------------------- step (2) runs
    specs = cell_specs()
    jobs = []
    if not MUT:
        for sp_ in specs:
            jobs.append(("M1", sp_, dict(mode=0, s=1.0, ec=0)))
            jobs.append(("M1-EC", sp_, dict(mode=0, s=1.0, ec=1)))
        for sp_ in specs[:8]:
            jobs.append(("P2", sp_, dict(mode=0, s=1.0, ec=0, kernel="P2")))
            jobs.append(("M2", sp_, dict(mode=1, s=1.0, ec=0)))
            jobs.append(("M3", sp_, dict(mode=2, s=1.0, ec=0)))
        base = [sp_ for sp_ in specs if sp_["name"] == "point|1e10|canonical"][0]
        jobs.append(("hydro", base, dict(mode=0, s=0.0, ec=0)))
        for sp_ in specs[:8]:          # post-freeze robustness: the scored point cells at a smaller time step
            jobs.append(("PH-cfl0.1", sp_, dict(mode=0, s=1.0, ec=0, cfl=0.1)))
        jobs.append(("N480", base, dict(mode=0, s=1.0, ec=0, N=480)))
    else:
        for sp_ in specs[:8]:
            jobs.append(("MB", sp_, dict(mode=0, s=1.0, ec=0, a0eff=2.0)))
        base = [sp_ for sp_ in specs if sp_["name"] == "point|1e10|canonical"][0]
        jobs.append(("MA-1D", base, dict(mode=0, s=-1.0, ec=0)))
    static_jobs = []
    if not MUT:
        pt = [sp_ for sp_ in specs if sp_["name"] == "point|1e10|canonical"][0]
        h1 = [sp_ for sp_ in specs if sp_["name"] == "hernquist|a=1|canonical"][0]
        static_jobs = [("C-static", pt, dict()), ("C-static", h1, dict()),
                       ("C-heat", pt, dict(escale=1.2)), ("C-cool", pt, dict(escale=0.8)),
                       ("PH-dilute-R2", pt, dict(t_len_te=5.0, mscale_out=(1.0, 0.5))),
                       ("PH-dilute-R10", pt, dict(t_len_te=5.0, mscale_out=(1.0, 0.1))),
                       ("PH-dilute-R10-hydro", pt, dict(t_len_te=5.0, mscale_out=(1.0, 0.1), s=0.0))]
    ph_jobs = []
    if not MUT:
        pt = [sp_ for sp_ in specs if sp_["name"] == "point|1e10|canonical"][0]
        ph_jobs = [("PH-late", pt, "late"), ("PH-frozen", pt, "frozen")]
    P(f"\n[STEP 2] 1-D runs: {len(jobs)} infall runs + {len(static_jobs)} static-start runs on {NTHREADS} threads "
      f"(N = {NSH}, wall r_w = {RW} r_M with the inert target core, smooth shell masses from {DM1} M_b; correction 1)")

    def runner(job):
        lab, sp_, kw = job
        return lab, sp_["name"], do_infall(sp_, **kw)

    def srunner(job):
        lab, sp_, kw = job
        return lab, sp_["name"], do_static(sp_, **kw)

    results = {}
    with ThreadPoolExecutor(NTHREADS) as ex:
        futs = ([ex.submit(runner, j) for j in jobs] + [ex.submit(srunner, j) for j in static_jobs]
                + [ex.submit(lambda j: (j[0], j[1]["name"], do_posthoc(j[1], j[2])), j) for j in ph_jobs]
                + ([ex.submit(lambda sp_: ("C-static-frozen", sp_["name"], do_static_frozen(sp_)), h1)] if not MUT else []))
        for fu in futs:
            lab, nm, r_ = fu.result()
            results.setdefault(lab, {})[nm] = r_
            P(f"  done {lab:22s} {nm:26s} crashed {r_.get('crashed')} steps {r_.get('steps'):>10d} "
              f"D10/20/40 {r_.get('D10', r_.get('D_end'))!s:.6s}/{r_.get('D20')!s:.6s}/{r_.get('D40')!s:.6s} "
              f"({r_.get('sec', 0):.0f} s)")
    OUT["runs"] = results

    if not MUT:
        # -------------------------------------------------------------------------------- controls C-static, C-energy
        P("\n[controls] C-static (start at the exact target), C-energy (EC run conserves energy)")
        cs = results["C-static"]
        okcs = all(r_["crashed"] == 0 and r_["D_end"] <= 0.01 and r_["max_v"] <= 0.01 for r_ in cs.values())
        check("C-static: after 20 t_e, D <= 0.01 and max|v| <= 0.01 V_f (point 1e10 canonical; Hernquist a = 1)", okcs,
              "; ".join(f"{k}: D {v['D_end']:.2e}, max|v| {v['max_v']:.2e}" for k, v in cs.items()))
        fw = list(results["C-static-frozen"].values())[0]
        P(f"  reported: the same C-static on the FROZEN numerics (Hernquist a = 1; run 2's load-bearing failure): crashed "
          f"{fw['crashed']} at t {fw['t_final']:.2f} of {fw['t_end']:.1f}")
        ec = results["M1-EC"]["point|1e10|canonical"]
        Et = energy_target([s_ for s_ in specs if s_["name"] == "point|1e10|canonical"][0])["E_t"]
        cerr = abs(ec["E_end"] - ec["E_i"]) / abs(Et)
        check("C-energy: EC run (point 1e10 canonical) conserves energy, |E_end - E_i| <= 2e-3 |E_t| (a run that crashed "
              "cannot certify it)", ec["completed"] and cerr <= 2e-3,
              f"crashed {ec['crashed']} at t {ec['t_final']:.2f} of {ec['t_end']:.1f}; up to its last sample {cerr:.2e} "
              f"(E_i {ec['E_i']:.4f}, E_t {Et:.4f})")
        hy = results["hydro"]["point|1e10|canonical"]
        herr = abs(hy["E_end"] - hy["E_i"]) / abs(Et)
        P(f"  reported (post-freeze integrator check): pure-hydro run (s = 0, all forces conservative, shock heat internal) "
          f"over the full {hy['t_end']:.0f} time units: |E_end - E_i|/|E_t| = {herr:.2e} (crashed {hy['crashed']})")
        OUT["integrator_check_hydro"] = herr
        for lab in ["C-heat", "C-cool"]:
            r_ = list(results[lab].values())[0]
            P(f"  reported {lab}: exact target with e x {r_['escale']}, 20 t_e of M1 -> D {r_['D_end']:.3f} dex "
              f"(the target's grip against a wrong temperature)")

        # -------------------------------------------------------------------------------- step (2) verdict
        P("\n[STEP 2] verdict table (M1, nu_mono, reservoir form; D in dex, scored D40 on x in [0.1, x_e])")
        m1 = results["M1"]
        okall = True
        for sp_ in specs:
            r_ = m1[sp_["name"]]
            okall &= r_["pass"]
            P(f"  {sp_['name']:26s} R_ta {r_['Rta_rM']:5.1f} r_M  x_e {r_['x_e']:.3f}  D10 {r_['D10']!s:.5s} D20 {r_['D20']!s:.5s} "
              f"D40 {r_['D40']!s:.5s} (0.9x_e {r_['D40_0.9xe']!s:.5s})  settled {r_['settled']!s:5s}  "
              f"mass inside x_e {r_.get('mass_inside_xe_end', float('nan')):.3f}/{SHARE}  r_surf {r_.get('r_surface_end', float('nan')):.2f}"
              f"  -> {'PASS' if r_['pass'] else 'FAIL'}")
        far = {}
        okfar = True
        for f in FOOTS:
            Rp = 40.0 / r_M_kpc(1e10, f)
            xmax = min(m1[f"farshell_A|{f}"]["x_e"], 0.9 * Rp)
            sel = XC <= xmax
            if m1[f"farshell_A|{f}"]["Vbar_common"] is None or m1[f"farshell_B|{f}"]["Vbar_common"] is None:
                dd = float("inf")              # not computed (a run crashed): cannot pass
            else:
                A_ = np.array(m1[f"farshell_A|{f}"]["Vbar_common"])
                B_ = np.array(m1[f"farshell_B|{f}"]["Vbar_common"])
                dd = float(np.max(np.abs(np.log10(A_[sel] / B_[sel]))))
            far[f] = dict(maxdev=dd, Rp_rM=Rp)
            okfar &= dd <= 0.05
            P(f"  far-shell pair {f}: max |log V_c,A/V_c,B| = {dd:.4f} dex over x <= {xmax:.2f} (R' = {Rp:.2f} r_M)")
        rN = results["N480"]["point|1e10|canonical"]
        r2 = m1["point|1e10|canonical"]
        if rN["D40"] is not None and r2["D40"] is not None:
            dres = abs(rN["D40"] - r2["D40"])
            converged = dres <= 0.02
        else:
            dres = float("nan")
            converged = (rN["crashed"] != 0 and r2["crashed"] != 0)     # both crash: the outcome is resolution-robust
        P(f"  resolution: N = 480 D40 {rN['D40']!s:.6s} (crashed {rN['crashed']}, t {rN['t_final']:.2f}) vs N = 240 "
          f"{r2['D40']!s:.6s} (crashed {r2['crashed']}, t {r2['t_final']:.2f}) -> "
          f"{'consistent' if converged else 'NOT CONVERGED'}")
        pass2 = okall and okfar and converged
        verdict2 = "PASS" if pass2 else ("FAIL (NOT CONVERGED)" if not converged else "FAIL")
        P(f"  reported members on the point-mass cells (D40): " + "; ".join(
            f"{lab}: " + ", ".join(f"{results[lab][s_['name']]['D40']!s:.5s}" for s_ in specs[:8]) for lab in ["P2", "M2", "M3"]))
        P("  post-freeze PH-cfl0.1 (the 8 scored point cells, M1, CFL 0.1 instead of 0.25): " + "; ".join(
            f"{s_['name']}: {'crash ' + str(results['PH-cfl0.1'][s_['name']]['crashed']) + ' at t ' + format(results['PH-cfl0.1'][s_['name']]['t_final'], '.1f') if results['PH-cfl0.1'][s_['name']]['crashed'] else 'D40 ' + format(results['PH-cfl0.1'][s_['name']]['D40'], '.3f')}"
            for s_ in specs[:8]))
        hyd = results['hydro']['point|1e10|canonical']
        P(f"  reported pure hydro (s = 0), point 1e10 canonical: D40 {hyd['D40']!s:.6s}, fluid inside x_e at the end "
          f"{hyd.get('mass_inside_xe_end', float('nan')):.3f} of {SHARE}, surface at {hyd.get('r_surface_end', float('nan')):.0f} r_M")
        for lab in ["PH-late", "PH-frozen"]:
            r_ = list(results[lab].values())[0]
            P(f"  post-freeze {lab} ({'hydro to t_coll + 5 t_e, then M1 on for 40 t_e' if lab == 'PH-late' else 'the scored cell on the frozen numerics'}): "
              f"crashed {r_['crashed']} at t {r_['t_final']:.2f} of {r_['t_end']:.1f}; D40 {r_['D40']!s:.6s}")
        for lab in ["PH-dilute-R2", "PH-dilute-R10", "PH-dilute-R10-hydro"]:
            r_ = list(results[lab].values())[0]
            P(f"  post-freeze {lab} (exact target, fluid beyond x = 1 diluted to R = rho_t/rho = {lab.split('-R')[1].split('-')[0]}"
              f"{', s = 0' if 'hydro' in lab else ', M1'}; 5 t_e): crashed {r_['crashed']}, t {r_['t_final']:.2f} of {r_['t_end']:.2f}, "
              f"steps {r_['steps']}")
        P(f"  -> STEP 2 = {verdict2}")
        OUT["step2"] = dict(verdict=verdict2, all_cells_pass=okall, farshell=far, farshell_ok=okfar, resolution_diff=dres,
                            converged=converged)

        # -------------------------------------------------------------------------------- step (3)
        P("\n[STEP 3] energy: (3a) static budget E_t vs E_i; (3b) reservoir work |W_res|; (3c) EC runs (reported)")
        ok3a = ok3b = True
        rows3 = {}
        n3b_untested = 0
        for sp_ in specs:
            et = energy_target(sp_)
            r_ = m1[sp_["name"]]
            e_ = results["M1-EC"][sp_["name"]]
            da = (et["E_t"] - r_["E_i"]) / abs(et["E_t"])
            wb = r_["W_res"] / abs(et["E_t"])
            ok3a &= abs(da) <= 0.1
            if not r_["completed"]:
                n3b_untested += 1          # crashed run: W_res not defined at t_end -> untested, not passed
                ok3b = False
            else:
                ok3b &= abs(wb) <= 0.1
            rows3[sp_["name"]] = dict(E_t=et["E_t"], U_t=et["U_t"], W_t=et["W_t"], E_i=r_["E_i"], dE_over_Et=da,
                                      Wres_over_Et=wb, EC_D40=e_["D40"], EC_floor_hits=e_["n_floor"],
                                      EC_energy_err=abs(e_["E_end"] - e_["E_i"]) / abs(et["E_t"]), EC_S_ps=e_["S_ps"],
                                      EC_S_q=e_["S_q"], EC_crashed=e_["crashed"])
            P(f"  {sp_['name']:26s} E_t {et['E_t']:+8.3f}  E_i {r_['E_i']:+8.3f}  (E_t-E_i)/|E_t| {da:+.3f}  W_res/|E_t| "
              f"{(f'{wb:+.3f}' if r_['completed'] else 'n/a (crashed)')}"
              f"  | EC: D40 {e_['D40']!s:.5s}, floor hits {e_['n_floor']}, S_ps {e_['S_ps']:+.3e} (S_q {e_['S_q']:+.3e})")
        k5m = {}
        for f in FOOTS:
            for lm in [9, 10, 11, 12]:
                mb = 10.0 ** lm
                rM = math.sqrt(G * mb * MSUN / A0[f])
                re = rM / math.log(1 / (1 - FB))
                k5m[f"1e{lm}|{f}"] = (5 / 12) * R_ta_SI(mb * MSUN / FB) / re
        P("  CFG461-convention contraction factors R_vir/r_e (z_c = 1): " + ", ".join(f"{k} {v:.2f}" for k, v in k5m.items()))
        verdict3 = "PASS" if (ok3a and ok3b) else "FAIL"
        P(f"  -> STEP 3 = {verdict3} ((3a) {'pass' if ok3a else 'FAIL'}, (3b) {'pass' if ok3b else 'FAIL'})")
        OUT["step3"] = dict(verdict=verdict3, ok3a=ok3a, ok3b=ok3b, rows=rows3, contraction=k5m)

        # -------------------------------------------------------------------------------- verdict
        if verdict1 == "FAIL" or verdict2 != "PASS":
            nc1 = "DEAD"
        elif verdict3 == "PASS" and verdict4 == "PASS":
            nc1 = "FULL PASS"
        else:
            nc1 = "ALIVE" + (", G14 COND" if verdict4 == "COND" else "")
        P("\n" + "=" * 110)
        P(f"VERDICT: step (1) {verdict1} | step (2) {verdict2} | step (3) {verdict3} | step (4) {verdict4}  ->  NC1 {nc1}")
        if nc1 == "DEAD":
            P("  by the frozen rule the chassis question returns to CFG484's R04 (C-H/K + Horava UV sector M_*); its decisive "
              "test is CFG319's moving-black-hole count with the z = 3 Horava terms at the universal horizon")
        P("  constants: chassis 0; fluid sector lambda = 1 (zero-constant), s = +1 and gamma = 5/3 structural; kappa fitted; "
          "amount 5.364 input")
        P("=" * 110)
        OUT["verdict"] = dict(step1=verdict1, step2=verdict2, step3=verdict3, step4=verdict4, NC1=nc1)
    else:
        # -------------------------------------------------------------------------------- MUTATE MB / MA-1D
        P("\n[MUTATE MB] target a0 -> 2 a0 inside F; scored against the true law and the 2 a0 law")
        mainj = json.load(open(os.path.join(HERE, "cfg489_results.json")))
        mb_rows = {}
        n_meas = 0
        moves = True
        for sp_ in specs[:8]:
            r_ = results["MB"][sp_["name"]]
            H = host_of(sp_)
            xe2 = supply_edge(H, "nu_mono", 2.0)
            mainr = mainj["runs"]["M1"][sp_["name"]]
            if mainr.get("Vbar_common") in (None, "None") or r_.get("Vbar_common") is None:
                mb_rows[sp_["name"]] = dict(measurable=False, main_crashed=mainr.get("crashed"), MB_crashed=r_["crashed"],
                                            MB_t_final=r_["t_final"], x_e2=xe2)
                P(f"  {sp_['name']:26s} not measurable: main crashed {mainr.get('crashed')}, MB crashed {r_['crashed']} "
                  f"(t {r_['t_final']:.1f} of {r_['t_end']:.1f})")
                continue
            n_meas += 1
            mainV = np.array(mainr["Vbar_common"], float)
            V = np.array(r_["Vbar_common"], float)
            xmax = min(r_["x_e"], xe2)
            sel = (XC >= 1.0) & (XC <= xmax)
            dlt = np.log10(V[sel] / mainV[sel])
            gl1 = law(host_Mb(H, XC[sel]), XC[sel])[0]
            gl2 = law(host_Mb(H, XC[sel]), XC[sel], a0=2.0)[0]
            dlaw = 0.5 * np.log10(gl2 / gl1)
            rms = float(np.sqrt(np.mean((dlt - dlaw) ** 2)))
            ok_m = bool(rms <= 0.02 and np.sign(np.mean(dlt)) == np.sign(np.mean(dlaw))
                        and abs(np.mean(dlt)) >= 0.5 * abs(np.mean(dlaw)))
            moves &= ok_m
            sel2 = (XC >= 0.1) & (XC <= xe2)
            D2 = float(np.max(np.abs(np.log10(V[sel2] / np.sqrt(XC[sel2] * law(host_Mb(H, XC[sel2]), XC[sel2], a0=2.0)[0])))))
            mb_rows[sp_["name"]] = dict(measurable=True, D_true=r_["D40"], D_2a0=D2, mean_shift=float(np.mean(dlt)),
                                        pred_shift=float(np.mean(dlaw)), rms=rms, moves=ok_m, x_e2=xe2)
            P(f"  {sp_['name']:26s} D vs true law {r_['D40']!s:.5s}  D vs 2a0 law {D2:.4f}  shift {np.mean(dlt):+.4f} "
              f"(predicted {np.mean(dlaw):+.4f}, rms {rms:.4f}) -> {'moves as predicted' if ok_m else 'does NOT move as predicted'}")
        moves = moves and n_meas > 0
        P(f"  MB summary: {n_meas} measurable cells; attractor moves as predicted: {moves if n_meas else 'not measurable'}")
        OUT["MB"] = dict(rows=mb_rows, moves_as_predicted=moves)
        ma = results["MA-1D"]["point|1e10|canonical"]
        P(f"\n[MUTATE MA-1D] s = -1, point 1e10 canonical: crashed {ma['crashed']} (1 inversion, 2 NaN, 3 dt), "
          f"t reached {ma['t_final']:.2f} of {ma['t_end']:.1f}")
        OUT["MA_1D"] = dict(crashed=ma["crashed"], t_final=ma["t_final"], t_end=ma["t_end"])

    # ---------------------------------------------------------------------------------------------- outputs
    OUT["checks"] = CHECKS
    lb_fail = [c["name"] for c in CHECKS if c["load_bearing"] and not c["ok"]]
    OUT["load_bearing_failures"] = lb_fail
    OUT["runtime_s"] = time.time() - T0
    P(f"\nchecks: {sum(c['ok'] for c in CHECKS)}/{len(CHECKS)} pass; load-bearing failures: {lb_fail if lb_fail else 'none'}"
      f"; runtime {OUT['runtime_s']:.0f} s")

    def _clean(o):
        if isinstance(o, dict):
            return {str(k): _clean(v) for k, v in o.items()}
        if isinstance(o, (list, tuple)):
            return [_clean(v) for v in o]
        if isinstance(o, (np.floating, float)):
            v = float(o)
            return v if math.isfinite(v) else str(v)
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, np.bool_):
            return bool(o)
        return o

    with open(os.path.join(HERE, f"cfg489_results{TAG}.json"), "w") as fh:
        json.dump(_clean(OUT), fh, indent=1)
    with open(os.path.join(HERE, f"cfg489_nc1{TAG}.out"), "w") as fh:
        fh.write("\n".join(LINES) + "\n")
    rc = 0 if not lb_fail else 1
    if MUT:
        rc = 1 if not pass1 else 0      # MA must fail step (1); the check above is printed and fails
    sys.exit(rc)


if __name__ == "__main__":
    main()
