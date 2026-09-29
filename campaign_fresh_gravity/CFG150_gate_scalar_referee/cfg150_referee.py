#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG150 -- REFEREE OF CFG102's HEADLINE: the gate scalar's universal stiffness mu_uni and its costs at m2 = 1e-12 Pa under
two background boundary conditions (D: chi0 = t at 1 kpc and 2e4 kpc; N: chi0' = 0 at both ends).

Frozen criteria (checked FIRST, by sha256, before anything else runs): campaign_fresh_gravity/CFG150_FROZEN_CRITERIA.md.
Targets (read from CFG102's README, so not blind): mu_uni = 1.474e28 J/m under D and N; flagship potential -13.67 (D) and
-13.50 (N) v_f^2; Sun potential -9.29e5 (D) and +7.647e7 (N) v_f^2.

Method (my own code; nothing of CFG102 or CFG49 is imported or executed):
  * s = ln(r/kpc); fields piecewise linear in s (P1 finite elements).  The gradient term is integrated exactly on each
    element; the (chi - t)^2 and W(chi) terms by 3-point Gauss-Legendre, with t, B and a evaluated exactly at the
    quadrature radii (consistent, not lumped).
  * Background chi0: the unknown is chi itself.  Newton on the exact gradient and tridiagonal Hessian of the discrete
    energy, started from the B = 0 (linear) solution at the same mu; Armijo backtracking on an exactly-differenced energy as
    a safeguard; a declared diagonal shift (tau m2 x lumped mass) if the Hessian is not positive definite.  Converged when
    every nodal residual is <= 1e-13 of the summed absolute sizes of its terms.
  * Stability: every window gets its own P1 grid (4000 elements, uniform in s) between the exact radii where the baryons'
    t crosses the window limits; delta chi = 0 at both ends; lambda_min = smallest eigenvalue of the lumped-r^2-mass-scaled
    window operator (LAPACK tridiagonal eigensolver); Lambda(mu) = min over the five windows.
  * mu_min: Brent on Lambda(10^x), x = log10 mu in [20, 34], xtol 1e-7, then probes above the root (largest root kept).
  * Costs: Phi_chi = -4 pi G t_U m2 (chi0 - t)/(H^2 x_c,eff), with chi0 - t formed at the nodes and interpolated in s.
  * Layers: DE12's formulas re-typed here; L352's constants and tables come through DE12's own loader, executed read-only.

Modes: MUTATE unset (main: P-lines, R-rows and every control); MUTATE=bc swaps the boundary conditions; MUTATE=slaved puts
chi0 := t in the stability test.  The MUTATE runs compute only the P-lines and the R-rows.  Outputs next to this file:
cfg150_<main|MUTATE_bc|MUTATE_slaved>.out and cfg150_<...>_results.json.
Repository root: ZF_REPO, else a search up from this file.  One process; BLAS threads set to 1.
kappa = 1/2 and Omega_c h^2 stay fitted. Nothing here says the data favour either model, or that the theory is closed.
"""
import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import sys
import io
import json
import math
import time
import hashlib
import contextlib
import subprocess
import platform

T0 = time.time()
HERE = os.path.dirname(os.path.abspath(__file__))


def _find_repo():
    ok = lambda d: os.path.isdir(os.path.join(d, "campaign_fresh_gravity")) and os.path.isdir(os.path.join(d, "real_research"))
    env = os.environ.get("ZF_REPO", "").strip()
    if env and ok(env):
        return os.path.abspath(env)
    d = HERE
    while True:
        if ok(d):
            return d
        up = os.path.dirname(d)
        if up == d:
            sys.exit("CFG150: repository root not found (set ZF_REPO)")
        d = up


# ---------------------------------------------------------------------------------------------- the hash check comes first
REPO = _find_repo()
SPEC_REL = "campaign_fresh_gravity/CFG150_FROZEN_CRITERIA.md"
SPEC_SHA256 = "bb3aad1500bc10eaf9edec7a4fa5e4d7f80069d2fe1b87dc1a84c54498a1542b"
with open(os.path.join(REPO, SPEC_REL), "rb") as _fh:
    SPEC_SHA_SEEN = hashlib.sha256(_fh.read()).hexdigest()
if SPEC_SHA_SEEN != SPEC_SHA256:
    print(f"CFG150: frozen criteria sha256 {SPEC_SHA_SEEN} differs from the frozen {SPEC_SHA256}; stopping.", flush=True)
    sys.exit(2)

import numpy as np                                                          # noqa: E402
import scipy                                                                # noqa: E402
from scipy.linalg import solveh_banded, eigh_tridiagonal, LinAlgError       # noqa: E402
from scipy.optimize import brentq                                           # noqa: E402

_MUT = os.environ.get("MUTATE", "").strip()
MODE = "" if _MUT in ("", "0") else _MUT
if MODE not in ("", "bc", "slaved"):
    sys.exit(f"CFG150: unknown MUTATE={_MUT!r} (allowed: bc, slaved)")
TAG = "main" if MODE == "" else f"MUTATE_{MODE}"

# ---------------------------------------------------------------------------------------------- frozen numbers
M2 = 1e-12                       # Pa, the headline mass
MU_REF = 1.474e28                # J/m, CFG102's printed mu_uni; the costs are scored here
ROUND_HALF = 3.4e-4              # |ln(mu_true/1.474e28)| bound from CFG102's 4-digit rounding
TGT = dict(mu_uni=1.474e28, PhiF_D=-13.67, PhiF_N=-13.50, PhiS_D=-9.29e5, PhiS_N=7.647e7,
           forceF_D=-45.60, forceF_N=-44.02, mu_inf=3.860e28, ratio=0.382, ell_kpc=3.9, slaved_ratio=2.62)
P5_BAND = (-0.19, -0.15)
WINS = [(0.0, 0.5), (0.125, 0.625), (0.25, 0.75), (0.375, 0.875), (0.5, 1.0)]
T_LO, T_HI = 0.004, 0.996        # DE13's layer range
W_GATE = 0.25
T_U = 1.0 / (2.0 * W_GATE)
LAYERS = [(z, Mb, f) for z in (0.25, 1.0, 2.5, 4.0) for Mb in (1e10, 1e11, 1e12) for f in ("canonical", "alt")]
NBG_SEARCH, NW_SEARCH = 2 ** 16, 4000
NBG_COST = 2 ** 17
X_LO, X_HI, X_TOL = 20.0, 34.0, 1e-7
PROBES = (5e-4, 5e-3, 5e-2, 0.3, 1.0, 2.0, 4.0)
NEWTON_TOL, NEWTON_MAXIT = 1e-13, 60
RMAX_KPC = 2e4
LN_RMAX = math.log(RMAX_KPC)

# Gauss-Legendre, 3 points on each element; PH = right-node shape function at the points (also their fractional position)
GLX = np.array([-math.sqrt(0.6), 0.0, math.sqrt(0.6)])
GLW = np.array([5.0 / 9.0, 8.0 / 9.0, 5.0 / 9.0])
PH = 0.5 * (1.0 + GLX)
PL = 1.0 - PH

_LOG = None


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    if _LOG is not None:
        _LOG.write(s + "\n")
        _LOG.flush()


def banner(t):
    P("\n" + "=" * 118)
    P(t)
    P("=" * 118)


def el():
    return f"[{time.time() - T0:.0f}s]"


# ================================================================================================ DE12's definitions
def load_de12():
    """Execute DE12's definitions read-only (its head: L352's constants and tables, Wd; and host/transition).
    Nothing is edited on disk; the only in-memory change forces DE12's MUTATE flag to False."""
    p12 = os.path.join(REPO, "real_research", "dark_energy_2026", "DE12_mond_sector_gate_stiffness.py")
    src = open(p12).read()
    m_c1 = "# ============================================================================================ C1 the amplification"
    m_tr = "# ============================================================================================ the transitions"
    m_g1 = "# ============================================================================================ G1 G2 the budget"
    # DE12's own flag line (at a line start).  The same text also sits inside DE12's string literal that switches L352's
    # flag off; that occurrence is left untouched so DE12's own neutralisation of L352 still works.
    mline = '\nMUTATE = os.environ.get("MUTATE", "0") == "1"'
    for m in (m_c1, m_tr, m_g1, mline):
        assert src.count(m) == 1, f"DE12 marker not unique: {m[:60]}"
    head = src.split(m_c1)[0]
    trans = src.split(m_tr)[1].split(m_g1)[0].split('banner("C2')[0]
    ns = {"__name__": "de12_readonly", "__file__": p12}
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile((head + "\n" + trans).replace(mline, "\nMUTATE = False"), p12, "exec"), ns)
    shas = {}
    for rel in ("real_research/dark_energy_2026/DE12_mond_sector_gate_stiffness.py",
                "real_research/g03_audit_2026/L352_switch_gauss_compensation.py"):
        with open(os.path.join(REPO, rel), "rb") as fh:
            shas[rel] = hashlib.sha256(fh.read()).hexdigest()
    return ns, shas


class Const:
    """L352's constants and interpolation tables (through DE12's loader) and DE12's own constants; formulas re-typed."""

    def __init__(self, ns):
        self.G, self.H0, self.Om, self.OL, self.rho_crit0 = ns["G"], ns["H0"], ns["Om"], ns["OL"], ns["rho_crit0"]
        self.A0 = dict(ns["A0"])
        self.LYG, self.YG, self.HM, self.DH = ns["LYG"], ns["YG"], ns["HM"], ns["DH"]
        self.MS, self.KPC, self.KB, self.MP, self.FB, self.HUB = ns["MS"], ns["KPC"], ns["KB"], ns["MP"], ns["FB"], ns["h"]
        self.C_LIGHT = ns["L52"]["c"]
        self.QG = 2.0 * ((2.0 / 3.0) * self.YG[0] ** 1.5 +
                         np.concatenate([[0.0], np.cumsum(0.5 * (self.HM[1:] + self.HM[:-1]) * np.diff(self.YG))]))
        self.CS2 = self.KB * 1e6 / (0.6 * self.MP)                          # isothermal 1e6 K gas, (117 km/s)^2

    def E2(self, z):
        return 0.3138 * (1 + z) ** 3 + 0.6862

    def Hz(self, z):
        return self.H0 * math.sqrt(self.Om * (1 + z) ** 3 + self.OL)

    def h_of(self, y):
        return np.interp(np.log10(y), self.LYG, self.HM)

    def dh_of(self, y):
        return np.interp(np.log10(y), self.LYG, self.DH)

    def q_of(self, y):
        return np.interp(np.log10(y), self.LYG, self.QG)

    def nu(self, y):
        return 1.0 + self.h_of(y) / y


C = None
KPC = None


class Prof:
    """One DE12 transition (w = 0.25, amp on, no kappa cap): scalars and an evaluator at arbitrary radii (metres)."""

    def __init__(self, z, Mb, foot):
        self.z, self.Mb, self.foot = z, Mb, foot
        self.key = f"{z}/{Mb:.0e}/{foot}"
        c = C
        self.a0 = c.A0[foot]
        self.H = c.Hz(z)
        self.xce = 2.5 * c.E2(z)
        self.rho_bar = c.Om * c.rho_crit0 * (1 + z) ** 3
        M200 = Mb / (0.3 * c.FB) if Mb < 1e13 else Mb / c.FB
        rhoc = c.rho_crit0 * c.E2(z) * (c.Hz(z) / (c.H0 * math.sqrt(c.E2(z)))) ** 2
        conc = 10 ** (0.905 - 0.101 * math.log10(M200 / (1e12 / c.HUB))) * (1 + z) ** -0.5
        r200 = (3 * M200 * c.MS / (4 * math.pi * 200 * rhoc)) ** (1 / 3)
        self.rs = r200 / conc
        self.rho_s = M200 * c.MS / (4 * math.pi * self.rs ** 3 * (math.log(1 + conc) - conc / (1 + conc)))
        self.vf2 = math.sqrt(c.G * Mb * c.MS * self.a0)
        self.Cc = 1.0 / (self.H ** 2 * self.xce)
        self.hfac = T_U * 4 * math.pi * c.G / (self.H ** 2 * self.xce)      # h = hfac * nu(y)

    def ev(self, r):
        c = C
        r = np.asarray(r, float)
        y = c.G * self.Mb * c.MS / (r ** 2 * self.a0)
        hy = c.h_of(y)
        dhy = c.dh_of(y)
        rho_ph = self.Mb * c.MS * (hy - y * dhy) / (2 * math.pi * r ** 3 * y)
        x = r / self.rs
        rho_nfw = self.rho_s / (x * (1 + x) ** 2)
        rho_b = c.FB * (rho_nfw + self.rho_bar)
        xms = 4 * math.pi * c.G * (rho_b + rho_ph - c.FB * self.rho_bar) / self.H ** 2
        U = xms / self.xce
        t = (U - 1) / (2 * W_GATE) + 0.5
        B = self.a0 ** 2 * c.q_of(y) / (8 * math.pi * c.G)
        nu = 1.0 + hy / y
        hg = self.hfac * nu
        a = c.CS2 / (rho_b * hg ** 2)
        return dict(t=t, B=B, a=a, y=y, rho_b=rho_b, rho_ph=rho_ph, nu=nu)


class FakeProf:
    """A test profile given by functions t(r) and B(r) (used by the analytic controls)."""

    def __init__(self, tfun, Bfun):
        self.tfun, self.Bfun = tfun, Bfun

    def ev(self, r):
        r = np.asarray(r, float)
        return dict(t=self.tfun(r), B=self.Bfun(r), a=np.ones_like(r))


# ================================================================================================ the step W (re-typed)
def Wfun(x):
    """W = 1/(1 + exp(1/x - 1/(1-x))) on (0,1), 0 below, 1 above; W' = W(1-W) q; W'' = W(1-W)[(1-2W) q^2 + q'],
    q = 1/x^2 + 1/(1-x)^2 (my own derivation; the exponent is clipped at +-700 as in DE12)."""
    x = np.asarray(x, float)
    ins = (x > 0) & (x < 1)
    xx = np.where(ins, x, 0.5)
    with np.errstate(over="ignore", invalid="ignore"):
        g = np.clip(1.0 / xx - 1.0 / (1.0 - xx), -700.0, 700.0)
        W = 1.0 / (1.0 + np.exp(g))
        q = 1.0 / xx ** 2 + 1.0 / (1.0 - xx) ** 2
        qp = -2.0 / xx ** 3 + 2.0 / (1.0 - xx) ** 3
        WW = W * (1.0 - W)
        W1 = WW * q
        W2 = WW * ((1.0 - 2.0 * W) * q * q + qp)
    # only within ~1e-100 of 0 or 1 can the products overflow (inf - inf); W is flat there, so those points get 0
    W1 = np.nan_to_num(W1, nan=0.0, posinf=0.0, neginf=0.0)
    W2 = np.nan_to_num(W2, nan=0.0, posinf=0.0, neginf=0.0)
    W = np.where(x >= 1, 1.0, np.where(x <= 0, 0.0, W))
    return W, np.where(ins, W1, 0.0), np.where(ins, W2, 0.0)


# ================================================================================================ P1 finite elements in s
class Grid:
    """P1 elements uniform in s = ln(r/kpc) on [s0, s1]; profile values at the nodes and at 3 Gauss points per element."""

    def __init__(self, s0, s1, nel, prof=None):
        self.nel = nel
        self.s = np.linspace(s0, s1, nel + 1)
        self.ds = (s1 - s0) / nel
        self.r = KPC * np.exp(self.s)
        self.sg = self.s[:-1, None] + PH[None, :] * self.ds
        self.rg = KPC * np.exp(self.sg)
        self.q = (0.5 * self.ds * GLW)[None, :] * self.rg ** 3          # r^2 dr = r^3 ds, with the Gauss weight
        self.k = np.diff(self.r) / self.ds ** 2                         # int_e r ds / ds^2, exact
        lump = np.zeros(nel + 1)
        lump[:-1] += (self.q * PL).sum(1)
        lump[1:] += (self.q * PH).sum(1)
        self.lump = lump
        if prof is not None:
            eg = prof.ev(self.rg)
            en = prof.ev(self.r)
            self.tg, self.Bg, self.ag = eg["t"], eg["B"], eg["a"]
            self.tn = en["t"]


def _ev(chi):
    return chi[:-1, None] * PL + chi[1:, None] * PH


def grad_hess(g, chi, mu, m2, Bs):
    """Exact gradient and tridiagonal Hessian of the discrete energy, and the residual scale S (summed |terms|)."""
    d = np.diff(chi)
    c = _ev(chi)
    _, W1, W2 = Wfun(c)
    f = g.q * (m2 * (c - g.tg) - Bs * g.Bg * W1)
    hh = g.q * (m2 - Bs * g.Bg * W2)
    ks = mu * g.k
    fs = ks * d
    grad = np.zeros_like(chi)
    grad[:-1] += (f * PL).sum(1) - fs
    grad[1:] += (f * PH).sum(1) + fs
    dg = np.zeros_like(chi)
    dg[:-1] += ks + (hh * PL * PL).sum(1)
    dg[1:] += ks + (hh * PH * PH).sum(1)
    off = -ks + (hh * PL * PH).sum(1)
    sa = ks * (np.abs(chi[:-1]) + np.abs(chi[1:]))
    fa = g.q * (m2 * (np.abs(c) + np.abs(g.tg)) + Bs * g.Bg * np.abs(W1))
    S = np.zeros_like(chi)
    S[:-1] += sa + (fa * PL).sum(1)
    S[1:] += sa + (fa * PH).sum(1)
    return grad, dg, off, S


def energy(g, chi, mu, m2, Bs):
    d = np.diff(chi)
    c = _ev(chi)
    return float(0.5 * mu * (g.k * d * d).sum() + (g.q * (0.5 * m2 * (c - g.tg) ** 2 - Bs * g.Bg * Wfun(c)[0])).sum())


def energy_diff(g, chi, dchi, mu, m2, Bs):
    """E(chi + dchi) - E(chi), differenced element by element (no cancellation between large totals)."""
    d, dd = np.diff(chi), np.diff(dchi)
    c, dc = _ev(chi), _ev(dchi)
    x = c - g.tg
    e1 = 0.5 * mu * g.k * dd * (2 * d + dd)
    e2 = g.q * (0.5 * m2 * dc * (2 * x + dc) - Bs * g.Bg * (Wfun(c + dc)[0] - Wfun(c)[0]))
    return float(e1.sum() + e2.sum())


def spd_solve(d, e, b, shift):
    ab = np.zeros((2, d.size))
    ab[0, 1:] = e
    ab[1] = d
    try:
        return solveh_banded(ab, b, lower=False, check_finite=False), 0.0
    except LinAlgError:
        pass
    for tau in (1e-3, 1e-2, 1e-1, 1.0, 1e1, 1e2, 1e3, 1e4, 1e5, 1e6):
        ab[1] = d + tau * shift
        try:
            return solveh_banded(ab, b, lower=False, check_finite=False), tau
        except LinAlgError:
            continue
    raise RuntimeError("no positive-definite diagonal shift found")


class Stats:
    def __init__(self):
        self.n = 0
        self.maxit = 0
        self.maxres = 0.0
        self.nconv_fail = 0
        self.maxshift = 0.0
        self.ls = 0

    def add(self, info):
        self.n += 1
        self.maxit = max(self.maxit, info["it"])
        self.maxres = max(self.maxres, info["res"])
        self.nconv_fail += (not info["conv"])
        self.maxshift = max(self.maxshift, info["shift"])
        self.ls += info["ls"]

    def as_dict(self):
        return dict(solves=self.n, max_newton_iterations=self.maxit, max_final_residual=self.maxres,
                    unconverged=self.nconv_fail, max_shift_tau=self.maxshift, line_search_halvings=self.ls)


STATS = Stats()


def bc_tuple(g, kind, left=None, right=None):
    if kind == "N":
        return "N"
    return ("D", g.tn[0] if left is None else left, g.tn[-1] if right is None else right)


def solve_bg(g, mu, m2, bc, Bs=1.0, start=None, maxit=NEWTON_MAXIT, tol=NEWTON_TOL, stats=STATS):
    """Background chi0 on grid g.  bc = 'N' (free ends) or ('D', left, right).  Starts from the B = 0 solution."""
    D = bc != "N"
    n = g.nel + 1
    fr = slice(1, n - 1) if D else slice(0, n)
    shift = m2 * g.lump[fr]

    def bands(dg, off):
        return dg[fr], (off[1:-1] if D else off)

    if start is None:
        chi = g.tn.copy()
        if D:
            chi[0], chi[-1] = bc[1], bc[2]
        gr, dg, off, _ = grad_hess(g, chi, mu, m2, 0.0)                  # B = 0: the energy is quadratic
        dd, ee = bands(dg, off)
        p, _ = spd_solve(dd, ee, -gr[fr], shift)
        chi[fr] += p
    else:
        chi = start.copy()
        if D:
            chi[0], chi[-1] = bc[1], bc[2]
    info = dict(it=0, res=float("inf"), conv=False, shift=0.0, ls=0)
    for it in range(maxit + 1):
        gr, dg, off, S = grad_hess(g, chi, mu, m2, Bs)
        gf = gr[fr]
        res = float(np.max(np.abs(gf) / np.maximum(S[fr], 1e-300)))
        info["it"], info["res"] = it, res
        if res <= tol:
            info["conv"] = True
            break
        if it == maxit:
            break
        dd, ee = bands(dg, off)
        p, tau = spd_solve(dd, ee, -gf, shift)
        info["shift"] = max(info["shift"], tau)
        full = np.zeros(n)
        full[fr] = p
        if float(np.max(np.abs(p) / (1.0 + np.abs(chi[fr])))) >= 1e-8:
            slope = float(gf @ p)
            a = 1.0
            while a > 1e-12 and energy_diff(g, chi, a * full, mu, m2, Bs) > 1e-4 * a * slope:
                a *= 0.5
                info["ls"] += 1
            full *= a
        chi = chi + full
    if stats is not None:
        stats.add(info)
    return chi, info


def chi_only_pd(g, chi, mu, m2, D):
    """Is the chi-only Hessian (B on) positive definite at chi?  (plain Cholesky, no shift)"""
    _, dg, off, _ = grad_hess(g, chi, mu, m2, 1.0)
    n = g.nel + 1
    fr = slice(1, n - 1) if D else slice(0, n)
    ab = np.zeros((2, dg[fr].size))
    ab[0, 1:] = off[1:-1] if D else off
    ab[1] = dg[fr]
    try:
        solveh_banded(ab, np.ones(ab.shape[1]), lower=False, check_finite=False)
        return True
    except LinAlgError:
        return False


# ================================================================================================ the stability test
def win_lambda(w, mu, V):
    """Smallest eigenvalue (Pa) of the window operator mu K + M[V] (delta chi = 0 at both ends), scaled by the lumped mass."""
    Vq = w.q * V
    ks = mu * w.k
    dg = np.zeros(w.nel + 1)
    dg[:-1] += ks + (Vq * PL * PL).sum(1)
    dg[1:] += ks + (Vq * PH * PH).sum(1)
    off = -ks + (Vq * PL * PH).sum(1)
    sc = 1.0 / np.sqrt(w.lump[1:-1])
    lam = eigh_tridiagonal(dg[1:-1] * sc * sc, off[1:-1] * sc[:-1] * sc[1:], eigvals_only=True,
                           select="i", select_range=(0, 0), check_finite=False)
    return float(lam[0])


def find_mu_min(Lam, lo=X_LO, hi=X_HI, xtol=X_TOL):
    """mu_min = 10^x*, the largest root of Lambda in [lo, hi] (Brent, then probes above the root)."""
    ncall = [0]

    def f(x):
        ncall[0] += 1
        return Lam(x)

    flo, fhi = f(lo), f(hi)
    rec = dict(f_lo=flo, f_hi=fhi, nonmonotone=False, reroots=0)
    if fhi <= 0:
        rec.update(x=None, mu=None, status="not stabilised by mu = 1e34", evals=ncall[0], below_unstable=None, probes=[])
        return rec
    if flo > 0:
        rec.update(x=lo, mu=10 ** lo, status="stable at the floor mu = 1e20", evals=ncall[0], below_unstable=None, probes=[])
        return rec
    x = brentq(f, lo, hi, xtol=xtol, maxiter=300)
    probes = []
    for _ in range(8):
        pts = sorted(set(min(x + d, hi) for d in PROBES))
        vals = [f(p) for p in pts]
        probes = list(zip(pts, vals))
        bad = [i for i, v in enumerate(vals) if v <= 0]
        if not bad:
            break
        rec["nonmonotone"] = True
        rec["reroots"] += 1
        j = max(bad)
        a = pts[j]
        b = pts[j + 1] if j + 1 < len(pts) else hi
        x = brentq(f, a, b, xtol=xtol, maxiter=300)
    fb = f(x - 5e-4)
    rec.update(x=x, mu=10 ** x, status="ok", evals=ncall[0], below_unstable=bool(fb < 0), f_below=fb,
               probes=[(float(p), float(v)) for p, v in probes])
    return rec


def r_of_t(prof, target):
    """Radius where t = target (outermost crossing), by a scan and Brent; also returns the number of crossings."""
    s = np.linspace(0.0, LN_RMAX, 20001)
    r = KPC * np.exp(s)
    d = prof.ev(r)["t"] - target
    idx = np.nonzero(d[:-1] * d[1:] <= 0.0)[0]
    if idx.size == 0:
        raise RuntimeError(f"t never crosses {target}")
    i = int(idx[-1])
    fun = lambda rr: float(prof.ev(np.array([rr]))["t"][0] - target)
    if fun(r[i]) == 0.0:
        return float(r[i]), int(idx.size)
    return float(brentq(fun, r[i], r[i + 1], xtol=1e-13 * r[i], maxiter=300)), int(idx.size)


class Layer:
    def __init__(self, z, Mb, foot):
        self.prof = Prof(z, Mb, foot)
        self.key = self.prof.key
        self.crossings = {}
        rr = {}
        for tt in sorted({T_LO, T_HI, 0.5} | {max(lo, T_LO) for lo, _ in WINS} | {min(hi, T_HI) for _, hi in WINS}):
            rr[tt], self.crossings[tt] = r_of_t(self.prof, tt)
        self.rt = rr
        self.win_r = [(rr[min(hi, T_HI)], rr[max(lo, T_LO)]) for lo, hi in WINS]   # (inner, outer) radii
        self._bg, self._w = {}, {}

    def bg(self, nel):
        if nel not in self._bg:
            self._bg[nel] = Grid(0.0, LN_RMAX, nel, self.prof)
        return self._bg[nel]

    def wins(self, nel):
        if nel not in self._w:
            self._w[nel] = [Grid(math.log(ri / KPC), math.log(ro / KPC), nel, self.prof) for ri, ro in self.win_r]
        return self._w[nel]

    def drop(self):
        self._bg, self._w = {}, {}


def actual_bc(label):
    """The boundary condition actually used for a D- or N-labelled run (MUTATE=bc swaps them)."""
    if MODE == "bc":
        return {"D": "N", "N": "D"}[label]
    return label


def layer_mu_min(L, m2, label, nbg=NBG_SEARCH, nw=NW_SEARCH, slaved=False):
    wins = L.wins(nw)
    inf = math.isinf(m2)
    use_bg = (not inf) and (not slaved)
    g = L.bg(nbg) if use_bg else None
    bc = bc_tuple(g, actual_bc(label)) if use_bg else None
    geffs = [w.ag if inf else w.ag * m2 / (w.ag + m2) for w in wins]

    def Lam(x):
        mu = 10.0 ** x
        if use_bg:
            chi, _ = solve_bg(g, mu, m2, bc)
            chis = [np.interp(w.sg, g.s, chi) for w in wins]
        else:
            chis = [w.tg for w in wins]
        return min(win_lambda(w, mu, ge - w.Bg * Wfun(c)[2]) for w, ge, c in zip(wins, geffs, chis))

    return find_mu_min(Lam)


# ================================================================================================ the costs
class Case:
    def __init__(self, name, z, Mb, foot, r_eval_kpc=None):
        self.name = name
        self.prof = Prof(z, Mb, foot)
        a0 = self.prof.a0
        self.r_eval = math.sqrt(C.G * Mb * C.MS / (0.1 * a0)) if r_eval_kpc is None else r_eval_kpc * KPC
        self.gM = float(C.nu(np.array([0.1]))[0]) * 0.1 * a0
        self._g = {}

    def grid(self, nel):
        if nel not in self._g:
            self._g[nel] = Grid(0.0, LN_RMAX, nel, self.prof)
        return self._g[nel]


def cost(case, mu, m2, label, nel=NBG_COST, Bs=1.0):
    g = case.grid(nel)
    bc = bc_tuple(g, actual_bc(label))
    chi, info = solve_bg(g, mu, m2, bc, Bs=Bs)
    dn = chi - g.tn
    se = math.log(case.r_eval / KPC)
    dF = float(np.interp(se, g.s, dn))
    K = 4 * math.pi * C.G * T_U * m2 * case.prof.Cc
    hs = 5 * g.ds
    ddds = (float(np.interp(se + hs, g.s, dn)) - float(np.interp(se - hs, g.s, dn))) / (2 * hs)
    return dict(Phi=-K * dF / case.prof.vf2, force=K * (ddds / case.r_eval) / case.gM, delta=dF,
                t=float(case.prof.ev(np.array([case.r_eval]))["t"][0]), newton=info, chi=chi)


def dPhi_dlnmu(case, mu, m2, label, nel=NBG_COST):
    h = 1e-3
    up = cost(case, mu * (1 + h), m2, label, nel)["Phi"]
    dn = cost(case, mu * (1 - h), m2, label, nel)["Phi"]
    return (up - dn) / (math.log(1 + h) - math.log(1 - h))


# ================================================================================================ helpers
def read_committed_json(rel):
    try:
        out = subprocess.run(["git", "-C", REPO, "show", f"HEAD:{rel}"], capture_output=True, check=True, timeout=120).stdout
        return json.loads(out), "git HEAD"
    except Exception:
        with open(os.path.join(REPO, rel)) as fh:
            return json.load(fh), "working tree"


def clean(o):
    if isinstance(o, dict):
        return {str(k): clean(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [clean(v) for v in o]
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    if isinstance(o, np.ndarray):
        return None
    if isinstance(o, float) and (math.isinf(o) or math.isnan(o)):
        return str(o)
    return o


PLINES, CONTROLS = [], []


def line(store, name, ok, measured, reading=""):
    ok = bool(ok)
    store.append(dict(name=name, pass_=ok, measured=measured, reading=reading))
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}")
    P(f"         measured: {measured}")
    if reading:
        P(f"         reading:  {reading}")
    return ok


def setup():
    global C, KPC
    ns, shas = load_de12()
    C = Const(ns)
    KPC = C.KPC
    return ns, shas


# ================================================================================================ controls
def control_W(ns):
    xs = np.linspace(-0.5, 1.5, 200001)
    mine, theirs = Wfun(xs), ns["Wd"](xs)
    dev = max(float(np.max(np.abs(m - t) / (1.0 + np.abs(t)))) for m, t in zip(mine, theirs))
    xi = np.linspace(0.02, 0.98, 9601)
    h = 1e-6
    W1fd = (Wfun(xi + h)[0] - Wfun(xi - h)[0]) / (2 * h)
    W2fd = (Wfun(xi + h)[1] - Wfun(xi - h)[1]) / (2 * h)
    _, W1, W2 = Wfun(xi)
    e1 = float(np.max(np.abs(W1fd - W1)) / np.max(np.abs(W1)))
    e2 = float(np.max(np.abs(W2fd - W2)) / np.max(np.abs(W2)))
    return dev, e1, e2


def control_FD(mu, m2):
    """A5: gradient and Hessian against central finite differences of my own discrete energy (W terms active)."""
    xs = np.linspace(1e-6, 1 - 1e-6, 1_000_001)
    Bc = 0.5 * m2 / float(np.max(np.abs(Wfun(xs)[2])))
    chim = lambda r: 0.5 - 0.8 * np.log(r / (200 * KPC))
    tf = lambda r: chim(r) + (0.8 * mu / r ** 2 - Bc * Wfun(chim(r))[1]) / m2
    g = Grid(math.log(50.0), math.log(500.0), 60, FakeProf(tf, lambda r: np.full_like(r, Bc)))
    rng = np.random.default_rng(150)
    chi = chim(g.r) + 0.1 * rng.standard_normal(g.r.size)
    grad, dg, off, _ = grad_hess(g, chi, mu, m2, 1.0)
    n = chi.size
    h = 1e-6
    gfd = np.empty(n)
    Hfd = np.empty((n, n))
    for i in range(n):
        e = np.zeros(n)
        e[i] = h
        gfd[i] = (energy(g, chi + e, mu, m2, 1.0) - energy(g, chi - e, mu, m2, 1.0)) / (2 * h)
        Hfd[:, i] = (grad_hess(g, chi + e, mu, m2, 1.0)[0] - grad_hess(g, chi - e, mu, m2, 1.0)[0]) / (2 * h)
    H = np.diag(dg) + np.diag(off, 1) + np.diag(off, -1)
    eg = float(np.max(np.abs(grad - gfd)) / np.max(np.abs(grad)))
    eH = float(np.max(np.abs(H - Hfd)) / np.max(np.abs(H)))
    eS = float(np.max(np.abs(Hfd - Hfd.T)) / np.max(np.abs(H)))
    wterm = float(np.max(np.abs(Bc * Wfun(_ev(chi))[2])) / m2)
    return eg, eH, eS, wterm


def run_controls_analytic():
    banner("CONTROLS A1-A5: analytic checks of my solver")
    mu0, gpos = 1e28, 1e-15
    a1 = {}
    for ra, rb in ((100.0, 150.0), (50.0, 300.0)):
        w = Grid(math.log(ra), math.log(rb), NW_SEARCH)
        L = (rb - ra) * KPC
        exact = mu0 * (math.pi / L) ** 2 + gpos
        got = win_lambda(w, mu0, np.full(w.q.shape, gpos))
        a1[f"[{ra:g},{rb:g}] kpc"] = dict(exact=exact, mine=got, rel=abs(got / exact - 1))
    worst = max(v["rel"] for v in a1.values())
    line(CONTROLS, "A1 constant-coefficient window: lambda_min = mu (pi/L)^2 + g within 1e-4 (4000 elements)",
         worst <= 1e-4, {k: f"mine {v['mine']:.8e} exact {v['exact']:.8e} rel {v['rel']:.2e}" for k, v in a1.items()})
    a2 = {}
    for ra, rb in ((100.0, 150.0), (50.0, 300.0)):
        w = Grid(math.log(ra), math.log(rb), NW_SEARCH)
        L = (rb - ra) * KPC
        exact = gpos * L ** 2 / math.pi ** 2
        V = np.full(w.q.shape, -gpos)
        rec = find_mu_min(lambda x, w=w, V=V: win_lambda(w, 10.0 ** x, V))
        a2[f"[{ra:g},{rb:g}] kpc"] = dict(exact=exact, mine=rec["mu"], rel=abs(rec["mu"] / exact - 1),
                                          probes_ok=(not rec["nonmonotone"]) and rec["below_unstable"])
    worst = max(v["rel"] for v in a2.values())
    line(CONTROLS, "A2 the whole mu_min chain (eigenvalue, Brent, probes) on g < 0: root = -g L^2/pi^2 within 1e-4",
         worst <= 1e-4 and all(v["probes_ok"] for v in a2.values()),
         {k: f"mine {v['mine']:.8e} exact {v['exact']:.8e} rel {v['rel']:.2e} probes ok {v['probes_ok']}" for k, v in a2.items()})

    # A3: harmonic t = 1e5 (kpc/r), B = 0
    mu, m2 = MU_REF, M2
    ts = 1e5
    fp = FakeProf(lambda r: ts * KPC / r, lambda r: np.zeros_like(r))
    g = Grid(0.0, LN_RMAX, NBG_COST, fp)
    ell = math.sqrt(mu / m2)
    r0, r1 = float(g.r[0]), float(g.r[-1])
    tp = lambda r: -ts * KPC / r ** 2
    f1 = lambda r: np.exp((r - r1) / ell) / r
    f2 = lambda r: np.exp(-(r - r0) / ell) / r
    f1p = lambda r: np.exp((r - r1) / ell) * (1 / (ell * r) - 1 / r ** 2)
    f2p = lambda r: np.exp(-(r - r0) / ell) * (-1 / (ell * r) - 1 / r ** 2)
    Mx = np.array([[f1p(r0), f2p(r0)], [f1p(r1), f2p(r1)]])
    Acoef, Ccoef = np.linalg.solve(Mx, np.array([-tp(r0), -tp(r1)]))
    rF = math.sqrt(C.G * 1e11 * C.MS / (0.1 * C.A0["canonical"]))
    a3 = {}
    chiD, _ = solve_bg(g, mu, m2, bc_tuple(g, "D"), stats=None)
    chiN, _ = solve_bg(g, mu, m2, "N", stats=None)
    okD, okN = True, True
    for lab, rr in (("8 kpc", 8 * KPC), ("r_F 38.6 kpc", rF)):
        se = math.log(rr / KPC)
        tt = ts * KPC / rr
        dD = float(np.interp(se, g.s, chiD - g.tn))
        dN = float(np.interp(se, g.s, chiN - g.tn))
        ex = float(Acoef * f1(rr) + Ccoef * f2(rr))
        a3[lab] = dict(t=tt, D_delta=dD, D_rel_to_t=abs(dD) / tt, N_delta=dN, N_exact=ex, N_rel=abs(dN / ex - 1))
        okD &= abs(dD) <= 1e-6 * tt
        okN &= abs(dN / ex - 1) <= 1e-4
    line(CONTROLS, "A3 harmonic t = 1e5 kpc/r, B = 0: D gives chi = t (|chi - t| <= 1e-6 t); N matches the closed form within 1e-4",
         okD and okN, {k: (f"t {v['t']:.4e}; D: chi - t = {v['D_delta']:.3e} ({v['D_rel_to_t']:.1e} of t); "
                            f"N: {v['N_delta']:.8e} vs exact {v['N_exact']:.8e} (rel {v['N_rel']:.1e})") for k, v in a3.items()})

    # A4: manufactured nonlinear solution
    xs = np.linspace(1e-6, 1 - 1e-6, 1_000_001)
    W2max = float(np.max(np.abs(Wfun(xs)[2])))
    Bc = 0.5 * m2 / W2max
    chim = lambda r: 0.5 - 0.8 * np.log(r / (200 * KPC))
    tf = lambda r: chim(r) + (0.8 * mu / r ** 2 - Bc * Wfun(chim(r))[1]) / m2
    g4 = Grid(0.0, LN_RMAX, NBG_SEARCH, FakeProf(tf, lambda r: np.full_like(r, Bc)))
    cm = chim(g4.r)
    chi4, inf4 = solve_bg(g4, mu, m2, ("D", float(cm[0]), float(cm[-1])), stats=None)
    err4 = float(np.max(np.abs(chi4 - cm)))
    line(CONTROLS, "A4 manufactured nonlinear solution chi_m = 0.5 - 0.8 ln(r/200 kpc), max B_c|W''| = 0.5 m2, D ends: nodes within 1e-6",
         err4 <= 1e-6 and inf4["conv"], f"max |chi - chi_m| = {err4:.2e}; Newton iterations {inf4['it']}, residual {inf4['res']:.1e}; "
                                         f"B_c = {Bc:.3e} Pa (max|W''| = {W2max:.4f})")
    return dict(A1=a1, A2=a2, A3=a3, A4=dict(err=err4, newton=inf4, Bc=Bc))


# ================================================================================================ main
def main():
    global _LOG
    out_txt = os.path.join(HERE, f"cfg150_{TAG}.out")
    out_json = os.path.join(HERE, f"cfg150_{TAG}_results.json")
    _LOG = open(out_txt, "w")
    P(__doc__.strip())
    P(f"\n  frozen criteria {SPEC_REL}: sha256 {SPEC_SHA_SEEN} == frozen value: OK")
    P(f"  mode: {TAG}; python {platform.python_version()}, numpy {np.__version__}, scipy {scipy.__version__}; "
      f"threads OMP={os.environ.get('OMP_NUM_THREADS')} VECLIB={os.environ.get('VECLIB_MAXIMUM_THREADS')}")
    if MODE == "bc":
        P("  *** MUTATE=bc: the D-labelled runs use free (Neumann) ends and the N-labelled runs use chi0 = t ends. "
          "Expected: P1, P2, P3D, P3N pass; P4D, P4N and P5 fail; exit 1 ***")
    if MODE == "slaved":
        P("  *** MUTATE=slaved: chi0 := t in the stability test (CFG102's attack A2). Expected: mu_uni near 3.86e28, "
          "P1 fails, the cost lines (scored at mu_ref) pass; exit 1 ***")
    ns, shas = setup()
    RES = dict(lane="CFG150", mode=TAG, spec_sha256=SPEC_SHA_SEEN, provenance_sha256=shas,
               versions=dict(python=platform.python_version(), numpy=np.__version__, scipy=scipy.__version__))
    P(f"  DE12's definitions loaded read-only (L352 constants and tables through DE12's loader)   {el()}")
    P(f"  constants: G = {C.G}, H0 = {C.H0:.6e} 1/s, a0 canonical {C.A0['canonical']}, alt {C.A0['alt']}, "
      f"c_s = {math.sqrt(C.CS2) / 1e3:.2f} km/s, table LYG {C.LYG[0]}..{C.LYG[-1]} ({C.LYG.size} nodes)")
    main_mode = MODE == ""

    # ------------------------------------------------------------------------------------------ controls first (main only)
    if main_mode:
        banner("CONTROL A5 (code): my W, W', W'' against DE12's Wd and against finite differences; gradient/Hessian vs FD")
        dev, e1, e2 = control_W(ns)
        eg, eH, eS, wterm = control_FD(MU_REF, M2)
        line(CONTROLS, "A5 W, W', W'' equal DE12's within 1e-12; W', W'' match FD of my W within 1e-5; gradient and Hessian "
                       "equal FD of my discrete energy within 1e-6; FD Hessian symmetric within 1e-6",
             dev <= 1e-12 and e1 <= 1e-5 and e2 <= 1e-5 and eg <= 1e-6 and eH <= 1e-6 and eS <= 1e-6,
             f"W vs DE12 {dev:.1e}; W' FD {e1:.1e}; W'' FD {e2:.1e}; gradient {eg:.1e}; Hessian {eH:.1e}; "
             f"symmetry {eS:.1e} (W'' term reaches {wterm:.2f} of m2 in the test)")
        RES["A5"] = dict(W_vs_DE12=dev, W1_fd=e1, W2_fd=e2, grad_fd=eg, hess_fd=eH, hess_sym=eS)

        banner("CONTROL L1: my re-typed layers against DE12's transition() on DE12's own grid")
        worst = dict(t=0.0, B=0.0, rho_b=0.0, y=0.0, nu=0.0, a=0.0, scalars=0.0)
        for z, Mb, foot in LAYERS + [(0.0, 6e10, "canonical")]:
            tr = ns["transition"](z, Mb, foot, W_GATE)
            pr = Prof(z, Mb, foot)
            m = pr.ev(tr["r"])
            worst["t"] = max(worst["t"], float(np.max(np.abs(m["t"] - tr["t"]) / np.maximum(1.0, np.abs(tr["t"])))))
            for k in ("B", "rho_b", "y"):
                worst[k] = max(worst[k], float(np.max(np.abs(m[k] / tr[k] - 1.0))))
            nu12 = ns["nu_of"](tr["y"])
            worst["nu"] = max(worst["nu"], float(np.max(np.abs(m["nu"] / nu12 - 1.0))))
            a12 = ns["CS"]["1e6K"] ** 2 / (tr["rho_b"] * (T_U * 4 * math.pi * ns["G"] * nu12 / (tr["H"] ** 2 * tr["xce"])) ** 2)
            worst["a"] = max(worst["a"], float(np.max(np.abs(m["a"] / a12 - 1.0))))
            worst["scalars"] = max(worst["scalars"], abs(pr.H / tr["H"] - 1), abs(pr.xce / tr["xce"] - 1), abs(pr.vf2 / tr["vf2"] - 1))
        line(CONTROLS, "L1 re-typed t, B, rho_b, y, nu, a (and H, x_c,eff, v_f^2) equal DE12's transition() within 1e-12, "
                       "24 layers + the Sun case", max(worst.values()) <= 1e-12,
             {k: f"{v:.1e}" for k, v in worst.items()})
        RES["L1"] = worst

    # ------------------------------------------------------------------------------------------ layers
    banner("LAYERS: the t-crossing radii (kpc) of the 24 DE12 layers (w = 0.25)")
    LAY = {}
    for z, Mb, foot in LAYERS:
        Lr = Layer(z, Mb, foot)
        LAY[Lr.key] = Lr
        P(f"    {Lr.key:22s}: r(0.996) {Lr.rt[T_HI] / KPC:9.3f}  r(0.5) {Lr.rt[0.5] / KPC:9.3f}  r(0.004) {Lr.rt[T_LO] / KPC:9.3f}  "
          f"(ln-width {math.log(Lr.rt[T_LO] / Lr.rt[T_HI]):.4f}; crossings of 0.5: {Lr.crossings[0.5]})")
    RES["layers"] = {k: dict(r996_kpc=L.rt[T_HI] / KPC, r05_kpc=L.rt[0.5] / KPC, r004_kpc=L.rt[T_LO] / KPC,
                             crossings=L.crossings) for k, L in LAY.items()}
    if main_mode:
        de12, src12 = read_committed_json("real_research/dark_energy_2026/DE12_mond_sector_gate_stiffness_results.json")
        bud = de12["numbers"]["budget"]
        devs, mono = {}, {}
        for k, L in LAY.items():
            devs[k] = abs(L.rt[0.5] / KPC / bud[k]["r_edge_kpc"] - 1)
            ss = np.linspace(math.log(L.rt[T_HI] / KPC), math.log(L.rt[T_LO] / KPC), 20001)
            tt = L.prof.ev(KPC * np.exp(ss))["t"]
            mono[k] = bool(np.all(np.diff(tt) < 0))
        line(CONTROLS, f"L2 t = 1/2 radius matches DE12's committed r_edge_kpc within 1e-5 on all 24 layers, and t falls "
                       f"strictly across every layer (DE12 results read from {src12})",
             max(devs.values()) <= 1e-5 and all(mono.values()) and all(L.crossings[0.5] == 1 for L in LAY.values()),
             f"max rel dev {max(devs.values()):.1e} ({max(devs, key=devs.get)}); monotone {sum(mono.values())}/24; "
             f"single 0.5-crossing {sum(L.crossings[0.5] == 1 for L in LAY.values())}/24")
        RES["L2"] = dict(max_rel_dev=max(devs.values()), monotone=sum(mono.values()), source=src12)
        run_controls_analytic_out = run_controls_analytic()
        RES["A1_A4"] = run_controls_analytic_out

    # ------------------------------------------------------------------------------------------ m2 = infinity (chi0 = t, g_eff = a)
    banner("m2 = INFINITY: chi0 = t, g_eff = a (DE13's form (i) in t units); per-layer mu_min [J/m]")
    ROOTS = {}
    mu_inf = {}
    for k, L in LAY.items():
        t1 = time.time()
        rec = layer_mu_min(L, math.inf, "D")
        ROOTS[f"inf/{k}"] = rec
        mu_inf[k] = rec["mu"]
        P(f"    {k:22s}: mu_min = {rec['mu']:.6e}  ({rec['status']}; {rec['evals']} evaluations; "
          f"monotone probes {not rec['nonmonotone']}; below unstable {rec['below_unstable']})  {time.time() - t1:.1f}s")
    k_inf = max(mu_inf, key=lambda kk: mu_inf[kk] or 0.0)
    MUINF = mu_inf[k_inf]
    P(f"    mu_uni(inf) = {MUINF:.6e} J/m (set by {k_inf})   {el()}")
    RES["m2_inf"] = dict(per_layer=mu_inf, mu_uni=MUINF, argmax=k_inf)
    if main_mode:
        de13, src13 = read_committed_json("real_research/dark_energy_2026/DE13_gate_gradient_repair_results.json")
        rows = de13["numbers"]["F1"]["rows"]
        dev3 = {k: abs(mu_inf[k] / (rows[k]["mu_U"] / T_U ** 2) - 1) for k in LAY}
        de13max = max(rows[k]["mu_U"] for k in LAY) / T_U ** 2
        line(CONTROLS, f"L3 m2 = inf per-layer mu_min equals DE13's committed mu_U/t_U^2 within 0.5% on all 24 layers; the "
                       f"maximum within 0.5% of 3.860e28 (DE13 read from {src13})",
             max(dev3.values()) <= 5e-3 and abs(MUINF / TGT["mu_inf"] - 1) <= 5e-3,
             f"max per-layer dev {max(dev3.values()):.2e} ({max(dev3, key=dev3.get)}); median {float(np.median(list(dev3.values()))):.2e}; "
             f"my max {MUINF:.5e} vs 3.860e28 ({MUINF / TGT['mu_inf'] - 1:+.2e}); DE13's own max/4 = {de13max:.5e} "
             f"({MUINF / de13max - 1:+.2e})")
        RES["L3"] = dict(per_layer_dev=dev3, de13_max=de13max, source=src13)

    # ------------------------------------------------------------------------------------------ m2 = 1e-12, D and N labels
    slaved = MODE == "slaved"
    MU = {}
    ARG = {}
    for label in ("D", "N"):
        banner(f"m2 = 1e-12 Pa, label {label} (ends actually used: {actual_bc(label)}; stability background: "
               f"{'chi0 := t (MUTATE=slaved)' if slaved else 'chi0 re-solved at every trial mu'}); per-layer mu_min [J/m]")
        per = {}
        for k, L in LAY.items():
            t1 = time.time()
            rec = layer_mu_min(L, M2, label, slaved=slaved)
            ROOTS[f"{label}/{k}"] = rec
            per[k] = rec["mu"]
            P(f"    {k:22s}: mu_min = {rec['mu']:.6e}  ratio to m2=inf {rec['mu'] / mu_inf[k]:.4f}  ({rec['status']}; "
              f"{rec['evals']} evaluations; monotone probes {not rec['nonmonotone']}; below unstable {rec['below_unstable']})  "
              f"{time.time() - t1:.1f}s")
            L._bg.pop(NBG_SEARCH, None)
        ka = max(per, key=lambda kk: per[kk] or 0.0)
        MU[label], ARG[label] = per[ka], ka
        P(f"    mu_uni({label}) = {per[ka]:.6e} J/m (set by {ka}); ell = sqrt(mu_uni/m2) = "
          f"{math.sqrt(per[ka] / M2) / KPC:.4f} kpc; mu_uni/mu_uni(inf) = {per[ka] / MUINF:.4f}   {el()}")
        RES[f"m2_1e-12_{label}"] = dict(per_layer=per, mu_uni=per[ka], argmax=ka, ell_kpc=math.sqrt(per[ka] / M2) / KPC,
                                        ratio_to_inf=per[ka] / MUINF, stability_background="t" if slaved else "solved")

    # ------------------------------------------------------------------------------------------ costs
    banner("COSTS: flagship (z = 2.5, 1e11, canonical, r_F) and Sun (z = 0, 6e10, canonical, 8 kpc); 2^17 elements")
    FL = Case("flagship", 2.5, 1e11, "canonical")
    SU = Case("Sun", 0.0, 6e10, "canonical", 8.0)
    P(f"    r_F = {FL.r_eval / KPC:.4f} kpc; v_f^2 = {FL.prof.vf2:.6e} (flagship), {SU.prof.vf2:.6e} (Sun) m^2/s^2; "
      f"g_MOND = {FL.gM:.6e} m/s^2")
    CO = {}
    for label in ("D", "N"):
        cf = cost(FL, MU_REF, M2, label)
        cs = cost(SU, MU_REF, M2, label)
        sF = dPhi_dlnmu(FL, MU_REF, M2, label)
        sS = dPhi_dlnmu(SU, MU_REF, M2, label)
        cfu = cost(FL, MU[label], M2, label)
        csu = cost(SU, MU[label], M2, label)
        CO[label] = dict(PhiF=cf["Phi"], forceF=cf["force"], deltaF=cf["delta"], tF=cf["t"], dPhiF=sF,
                         PhiS=cs["Phi"], deltaS=cs["delta"], tS=cs["t"], dPhiS=sS,
                         PhiF_own=cfu["Phi"], forceF_own=cfu["force"], PhiS_own=csu["Phi"],
                         newtonF=cf["newton"], newtonS=cs["newton"])
        P(f"    [{label}] at mu_ref = 1.474e28: Phi(r_F) = {cf['Phi']:+.6f} v_f^2 (force {cf['force']:+.4f} g_MOND; "
          f"chi0 - t = {cf['delta']:+.6e}, t = {cf['t']:.5f}); Phi(Sun) = {cs['Phi']:+.6e} v_f^2 (chi0 - t = {cs['delta']:+.6e}, "
          f"t = {cs['t']:.6e})")
        P(f"         dPhi/dln mu: flagship {sF:+.4e}, Sun {sS:+.4e} v_f^2;  at my own mu_uni({label}) = {MU[label]:.6e}: "
          f"Phi(r_F) = {cfu['Phi']:+.6f}, force {cfu['force']:+.4f} g_MOND, Phi(Sun) = {csu['Phi']:+.6e}")
    RES["costs"] = {lab: {k: v for k, v in d.items()} for lab, d in CO.items()}

    # ------------------------------------------------------------------------------------------ P-lines
    banner("P-LINES (scored; a failure is kept)")
    p1 ={lab: MU[lab] / TGT["mu_uni"] - 1 for lab in ("D", "N")}
    line(PLINES, "P1 [headline] mu_uni(D) and mu_uni(N) each within 1% of 1.474e28 J/m",
         all(abs(v) <= 1e-2 for v in p1.values()),
         f"D {MU['D']:.6e} ({p1['D']:+.2e}); N {MU['N']:.6e} ({p1['N']:+.2e})")
    p2 = MU["D"] / MU["N"] - 1
    line(PLINES, "P2 [headline] |mu_uni(D)/mu_uni(N) - 1| <= 1e-3", abs(p2) <= 1e-3, f"{p2:+.3e}")

    def band_line(name, val, target, sens, sign):
        band = 0.02 * abs(target) + ROUND_HALF * abs(sens)
        ok = abs(val - target) <= band and (val < 0 if sign < 0 else val > 0)
        return line(PLINES, name, ok, f"{val:+.6e} vs {target:+.6e} (diff {val - target:+.3e}; band {band:.3e} = 2% "
                                      f"{0.02 * abs(target):.3e} + 3.4e-4 x |dPhi/dln mu| {ROUND_HALF * abs(sens):.3e}; "
                                      f"rel diff {val / target - 1:+.3e})")

    band_line("P3D flagship, D: negative and within the band of -13.67 v_f^2", CO["D"]["PhiF"], TGT["PhiF_D"], CO["D"]["dPhiF"], -1)
    band_line("P3N flagship, N: negative and within the band of -13.50 v_f^2", CO["N"]["PhiF"], TGT["PhiF_N"], CO["N"]["dPhiF"], -1)
    band_line("P4D Sun, D: negative and within the band of -9.29e5 v_f^2", CO["D"]["PhiS"], TGT["PhiS_D"], CO["D"]["dPhiS"], -1)
    band_line("P4N Sun, N: positive and within the band of +7.647e7 v_f^2", CO["N"]["PhiS"], TGT["PhiS_N"], CO["N"]["dPhiS"], +1)
    dFN = CO["D"]["PhiF"] - CO["N"]["PhiF"]
    line(PLINES, "P5 [my addition] Phi_F(D) - Phi_F(N) in [-0.19, -0.15] v_f^2", P5_BAND[0] <= dFN <= P5_BAND[1], f"{dFN:+.5f} v_f^2")

    # ------------------------------------------------------------------------------------------ R-rows
    banner("R-ROWS (reported, not scored)")
    P(f"  R1 mu_uni(1e-12): D {MU['D']:.6e} (set by {ARG['D']}), N {MU['N']:.6e} (set by {ARG['N']}); CFG102: z = 2.5, 1e12, alt")
    P(f"     mu_uni(inf) {MUINF:.6e} (set by {k_inf}); ratio mu_uni(1e-12)/mu_uni(inf): D {MU['D'] / MUINF:.4f}, "
      f"N {MU['N'] / MUINF:.4f} (CFG102: 0.382); ell: D {math.sqrt(MU['D'] / M2) / KPC:.4f} kpc (CFG49: 3.9)")
    ownF = CO["D"]["PhiF_own"] - CO["N"]["PhiF_own"]
    P(f"  R2 at my own mu_uni: Phi_F D {CO['D']['PhiF_own']:+.6f} ({CO['D']['PhiF_own'] / TGT['PhiF_D'] - 1:+.2e}), "
      f"N {CO['N']['PhiF_own']:+.6f} ({CO['N']['PhiF_own'] / TGT['PhiF_N'] - 1:+.2e}); D - N {ownF:+.5f}; "
      f"Phi_Sun D {CO['D']['PhiS_own']:+.6e} ({CO['D']['PhiS_own'] / TGT['PhiS_D'] - 1:+.2e}), "
      f"N {CO['N']['PhiS_own']:+.6e} ({CO['N']['PhiS_own'] / TGT['PhiS_N'] - 1:+.2e}); flagship force D "
      f"{CO['D']['forceF_own']:+.4f}, N {CO['N']['forceF_own']:+.4f} g_MOND")
    P(f"  R3 flagship force at mu_ref: D {CO['D']['forceF']:+.4f} (CFG102 -45.60), N {CO['N']['forceF']:+.4f} (CFG102 -44.02) g_MOND; "
      f"dPhi/dln mu: flagship D {CO['D']['dPhiF']:+.4e}, N {CO['N']['dPhiF']:+.4e}; Sun D {CO['D']['dPhiS']:+.4e}, "
      f"N {CO['N']['dPhiS']:+.4e} v_f^2")
    P(f"     t and chi0 - t at r_F: D t = {CO['D']['tF']:.5f}, delta {CO['D']['deltaF']:+.6e}; N delta {CO['N']['deltaF']:+.6e}; "
      f"at 8 kpc: t = {CO['D']['tS']:.6e}, delta D {CO['D']['deltaS']:+.6e}, N {CO['N']['deltaS']:+.6e}")
    RES["R"] = dict(mu_uni=MU, argmax=ARG, ratio={k: v / MUINF for k, v in MU.items()},
                    own_chain=dict(PhiF_D=CO["D"]["PhiF_own"], PhiF_N=CO["N"]["PhiF_own"], dF=ownF,
                                   PhiS_D=CO["D"]["PhiS_own"], PhiS_N=CO["N"]["PhiS_own"],
                                   forceF_D=CO["D"]["forceF_own"], forceF_N=CO["N"]["forceF_own"]))

    # ------------------------------------------------------------------------------------------ remaining controls (main only)
    if main_mode:
        banner("CONTROL L4: DE13's N1 costs at m2 = inf with mu = my mu_uni(inf): direct form and my solver at m2 = 1e-8 Pa")
        n1 = de13["numbers"]["form_i_cost"]
        refs = {"flagship": n1["flagship r_F, z = 2.5, 1e11"], "Sun": n1["the Sun, z = 0, 6e10 at 8 kpc"]}
        l4 = {}
        ok4 = True
        for case in (FL, SU):
            hs = 0.01
            se = math.log(case.r_eval / KPC)
            tt = [float(case.prof.ev(np.array([KPC * math.exp(se + j * hs)]))["t"][0]) for j in (-2, -1, 0, 1, 2)]
            t_s = (-tt[4] + 8 * tt[3] - 8 * tt[1] + tt[0]) / (12 * hs)
            t_ss = (-tt[4] + 16 * tt[3] - 30 * tt[2] + 16 * tt[1] - tt[0]) / (12 * hs ** 2)
            lap = (t_ss + t_s) / case.r_eval ** 2
            ev = case.prof.ev(np.array([case.r_eval]))
            W1 = float(Wfun(ev["t"])[1][0])
            Phid = -4 * math.pi * C.G * T_U * case.prof.Cc * (float(ev["B"][0]) * W1 + MUINF * lap) / case.prof.vf2
            Phis = cost(case, MUINF, 1e-8, "D")["Phi"]
            ref = refs[case.name]
            l4[case.name] = dict(direct=Phid, solver=Phis, DE13=ref, t=float(ev["t"][0]), W1=W1)
            ok4 &= abs(abs(Phid) / ref - 1) <= 1e-2 and abs(abs(Phis) / ref - 1) <= 1e-2 and abs(Phis / Phid - 1) <= 2e-3
        line(CONTROLS, "L4 DE13's N1 at m2 = inf (31.8 v_f^2 at r_F, 2.13e8 at the Sun) within 1%, both ways; the two ways within 2e-3",
             ok4, {k: (f"direct {v['direct']:+.6e}, solver {v['solver']:+.6e} (ways differ {v['solver'] / v['direct'] - 1:+.2e}); "
                       f"DE13 |Phi| {v['DE13']:.6e} (direct {abs(v['direct']) / v['DE13'] - 1:+.2e}, solver "
                       f"{abs(v['solver']) / v['DE13'] - 1:+.2e}); t there {v['t']:.4g}, W' {v['W1']:.1e}") for k, v in l4.items()})
        RES["L4"] = l4

        banner("CONTROL S1: mu_min of the layer that sets mu_uni (D) at (2^15, 2000) and (2^17, 8000) elements")
        La = LAY[ARG["D"]]
        s1 = {}
        for nbg, nw in ((2 ** 15, 2000), (2 ** 17, 8000)):
            t1 = time.time()
            rec = layer_mu_min(La, M2, "D", nbg=nbg, nw=nw)
            ROOTS[f"S1/{nbg}/{nw}"] = rec
            s1[f"{nbg}/{nw}"] = rec["mu"]
            P(f"    {ARG['D']} at ({nbg}, {nw}): mu_min = {rec['mu']:.6e} (rel to primary {rec['mu'] / MU['D'] - 1:+.2e})  "
              f"{time.time() - t1:.1f}s")
            La.drop()
        line(CONTROLS, "S1 mu_min of the argmax layer (D) at (2^15, 2000) and (2^17, 8000) within 1e-3 of the primary (2^16, 4000)",
             all(abs(v / MU["D"] - 1) <= 1e-3 for v in s1.values()),
             {k: f"{v:.6e} ({v / MU['D'] - 1:+.2e})" for k, v in s1.items()})
        RES["S1"] = s1

        banner("CONTROL S2: the four potentials at mu_ref on 2^15, 2^16, 2^17 (primary) and 2^18 elements")
        s2 = {}
        ok2 = True
        for label in ("D", "N"):
            for case, key in ((FL, "PhiF"), (SU, "PhiS")):
                vals = {}
                for nel in (2 ** 15, 2 ** 16, 2 ** 17, 2 ** 18):
                    vals[nel] = cost(case, MU_REF, M2, label, nel=nel)["Phi"]
                rel = vals[2 ** 18] / vals[2 ** 17] - 1
                s2[f"{key}_{label}"] = dict(values={str(k): v for k, v in vals.items()}, rel_2e18_vs_2e17=rel)
                ok2 &= abs(rel) <= 2e-3
                P(f"    {key} {label}: " + ", ".join(f"2^{int(math.log2(k))}: {v:+.7e}" for k, v in vals.items()) +
                  f"  (2^18 vs 2^17 {rel:+.2e})")
            for case in (FL, SU):
                case._g.pop(2 ** 18, None)
        line(CONTROLS, "S2 the 2^18 potentials within 0.2% of the primary 2^17 ones", ok2,
             {k: f"{v['rel_2e18_vs_2e17']:+.2e}" for k, v in s2.items()})
        RES["S2"] = s2

        banner("CONTROL S3 (branch): continuation in B gives the same chi0; the chi-only Hessian is positive definite")
        s3 = {}
        ok3 = True
        tests = [("flagship", FL.grid(NBG_COST)), ("Sun", SU.grid(NBG_COST)), (f"layer {ARG['D']}", LAY[ARG["D"]].bg(NBG_SEARCH))]
        for name, g in tests:
            for label in ("D", "N"):
                bc = bc_tuple(g, actual_bc(label))
                chi_dir, _ = solve_bg(g, MU_REF, M2, bc)
                chi_c, _ = solve_bg(g, MU_REF, M2, bc, Bs=0.0)
                for kb in range(1, 9):
                    chi_c, _ = solve_bg(g, MU_REF, M2, bc, Bs=kb / 8.0, start=chi_c)
                dev = float(np.max(np.abs(chi_c - chi_dir) / (1.0 + np.abs(chi_dir))))
                pd = chi_only_pd(g, chi_dir, MU_REF, M2, bc != "N")
                s3[f"{name}/{label}"] = dict(max_rel_dev=dev, chi_only_PD=pd)
                ok3 &= dev <= 1e-9 and pd
                P(f"    {name:32s} {label}: continuation vs direct max rel dev {dev:.1e}; chi-only Hessian PD {pd}")
        line(CONTROLS, "S3 continuation in B reproduces the direct chi0 within 1e-9; chi0 is a local minimum of the chi-only energy",
             ok3, {k: f"{v['max_rel_dev']:.1e}, PD {v['chi_only_PD']}" for k, v in s3.items()})
        RES["S3"] = s3

        banner("CONTROL S4: the probes above every root are stable, and just below it unstable")
        bad = [k for k, r in ROOTS.items() if r["status"] != "ok" or r["nonmonotone"] or not r["below_unstable"]]
        line(CONTROLS, "S4 every root: stable at all probes above (monotone), unstable 5e-4 decades below", not bad,
             f"{len(ROOTS)} roots; violations: {bad if bad else 'none'}")
        RES["S4"] = dict(n_roots=len(ROOTS), violations=bad)

    # ------------------------------------------------------------------------------------------ summary
    RES["roots"] = ROOTS
    RES["newton_stats"] = STATS.as_dict()
    banner("SUMMARY")
    P(f"  R4 Newton: {STATS.as_dict()}")
    npf = sum(not x["pass_"] for x in PLINES)
    ncf = sum(not x["pass_"] for x in CONTROLS)
    P(f"  P-lines: {len(PLINES) - npf}/{len(PLINES)} pass" + (f"; failed: {[x['name'].split()[0] for x in PLINES if not x['pass_']]}" if npf else ""))
    if main_mode:
        P(f"  controls: {len(CONTROLS) - ncf}/{len(CONTROLS)} pass" + (f"; failed: {[x['name'].split()[0] for x in CONTROLS if not x['pass_']]}" if ncf else ""))
        rc = 0 if (npf == 0 and ncf == 0) else 1
    else:
        rc = 1 if npf else 0
        P(f"  MUTATE={MODE}: {'the mutation changes the headline (some P-line fails): exit 1 as required' if npf else 'NO P-line fails: the mutation did not bite (a failure of the MUTATE requirement)'}")
    RES["plines"] = PLINES
    RES["controls"] = CONTROLS
    RES["exit_code"] = rc
    RES["elapsed_s"] = round(time.time() - T0, 1)
    with open(out_json, "w") as fh:
        json.dump(clean(RES), fh, indent=1)
    P(f"  wrote {os.path.basename(out_json)}; elapsed {time.time() - T0:.0f}s")
    P(f"  exit code {rc}")
    P("\n  kappa = 1/2 and Omega_c h^2 stay fitted. Nothing here says the data favour either model, or that the theory is closed.")
    _LOG.close()
    return rc


if __name__ == "__main__":
    sys.exit(main())
