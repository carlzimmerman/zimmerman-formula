#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
CFG119 -- Door 7: a fuzzy-dark-matter soliton plus baryons (Schrodinger-Poisson ground state) against the CFG44 target.

Frozen criteria: ../CFG119_FROZEN_CRITERIA.md (written before any script or number of this lane).
Shared gates G1-G5: ../closure_map/TEN_DOORS_GATES_2026-09-29.md.  The CFG44 target is imported READ-ONLY from
../CFG44_fluid_target/Bcommon.py; the report harness from ../CFG7_common.py.

THE QUESTION.  An ultralight scalar of boson mass m has the spherical Schrodinger-Poisson (SP) ground state (n = 0, l = 0)
    -(hbar^2/2m) lap psi + m (Phi_b + Phi_psi) psi = E psi,   lap Phi_psi = 4 pi G m |psi|^2,   int m |psi|^2 dV = M_sol.
Can it reproduce CFG44's target C(r) = rho_c r^3 g_tot = (a0/4 pi) M_b(<r), g_tot = G (M_b(<r) + M_sol(<r))/r^2, within 10%
(ratio in [0.9, 1.1]) over x = r/r_M in [0.1, 30], r_M = sqrt(G M_b/a0), for M_b = 1e9, 1e10, 1e11, 1e12 Msun, for a point mass
and CFG44's exponential spheres (h = 2, 3, 4, 5 kpc), with ONE boson mass at every M_b?

METHOD (the frozen file asks to state it):
  * t = ln r on a uniform grid of step 1e-3; phi = r^(1/2) psi turns the l = 0 radial equation into
        -(beta^2/2)(phi_tt - phi/4) + r^2 (V - eps) phi = 0,      beta = hbar/m,  eps = E/m,
    and second-order finite differences give a symmetric tridiagonal generalised eigenproblem A phi = eps B phi, B = r^2.
    Inner boundary: the regular solution's ghost-point ratio (psi -> const, with the Kato cusp psi'/psi = -G M_b/beta^2 for the
    point mass); outer boundary: phi = 0 at an edge where the state has decayed by > e^-100.
  * the lowest eigenpair: shifted inverse iteration from a rigorous lower bound (the larger of min V and the hydrogenic bound
    -(G M_tot)^2/2 beta^2), polished by Rayleigh-quotient iteration; "ground state" is certified by a nodeless eigenvector.
  * self-gravity: Phi_psi = -G M(<r)/r - 4 pi G int_r^inf rho r' dr' (trapezoid in t).  SELF-CONSISTENT ITERATION on Phi_psi
    with Anderson mixing (memory 6, mixing 0.5), started from the no-baryon soliton rescaled to M_sol; converged when eps
    changes by < 1e-11 (relative) between iterations and the potential residual is < 1e-10 (the frozen line is 1e-8 in E).
    The eigen-solve inside the iteration is finite-difference inverse iteration, NOT shooting (a disclosed departure);
    shooting is used as the independent check of the no-baryon soliton (C1x) and Newton-Raphson on the coupled system,
    with a differential Poisson equation, as the independent check of the runs with baryons (N2).
  * tails: ln psi beyond the peak of r psi comes from an exact piecewise-constant-potential log-derivative sweep inward from
    the outer edge (stable inward), so log ratios of -1e11 dex are computed, never floored by underflow.
  * the grid: the frozen file declares a log grid from 1e-3 r_M to 1e3 r_M.  For most (m, M_b) the ground state's own scale
    (the Bohr radius a_B = beta^2/G M_b, or the soliton core) lies far inside 1e-3 r_M, so the solver grid runs from
    min(1e-3 r_M, 1e-6 x the smallest physical scale) to max(1e3 r_M, 300 a_B).  The declared grid is contained in it
    (a disclosed departure; without it the ground state is not resolved).

DECLARED CHOICES (before the run):
  * m in {1e-23, 1e-22, 1e-21, 1e-20} eV (the frozen grid; m is reported, not tuned).
  * a0 on both footings: canonical 9.3603e-11 (Bcommon's A0, which the imported target uses) and alt 1.1312e-10 m/s^2
    (CFG4_common's FP0 value).  H1 is scored on each footing separately.
  * rule (i): Schive et al. 2014 (PRL 113, 261302; arXiv:1407.7762, read as HTML): M_c = (1/4) a^(-1/2) (zeta(z)/zeta(0))^(1/6)
    (M_h/M_min,0)^(1/3) M_min,0, M_min,0 ~ 4.4e7 m22^(-3/2) Msun, taken at z = 0 (a = 1).  Schive's M_c is the mass INSIDE
    r_c (the half-peak-density radius); it is converted to the SP normalisation by M_sol = M_c / f_c, with f_c = M(<r_c)/M_sol
    of the no-baryon ground state (computed in C1).  M_h = the target's own cold mass inside 30 r_M (frozen).  Because rule
    (ii) minimises over every M_sol, this conversion cannot change H1.
  * rule (ii): M_sol free per galaxy (and per footing): the minimiser of J = max |log10 ratio| over x in [0.1, 30], searched over
    log10(M_sol/M_b) in [-16, +4]: a 0.5-dex scan, then golden section to 1e-3 dex around the best scan point.
  * x grid: 601 log-spaced points in [0.1, 30].
  * G2: Hu, Barkana & Gruzinov 2000 (PRL 85, 1158; astro-ph/0003365, read as HTML): T_F = cos(x^3)/(1 + x^8),
    x = 1.61 m22^(1/18) k/k_Jeq, k_Jeq = 9 m22^(1/2)/Mpc, k_1/2 = 4.5 m22^(4/9)/Mpc (the POWER halves there).  "Growth within
    5%" is read on the amplitude, T_F >= 0.95 for every k <= 30/Mpc (CFG43's convention: delta(z=0) within 5% of LCDM).

MUTATE=1: G1 is evaluated on the target's own rho_c (CFG44 target_fields) in place of the SP ground state, through the same
evaluator and the same "one m at every mass" aggregation; H1 must then pass.  The SP scans are not run under MUTATE (they are
not used by its headline); the physics controls C1 and C2 run in both modes.

kappa = 1/2 and Omega_c h^2 stay fitted.  Nothing here says the data favour either model, or that the theory is closed.
"""
import os
import sys

sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_v] = "1"

import math
import time
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import scipy.sparse as sps
from scipy.linalg import solve_banded
from scipy.sparse.linalg import splu
from scipy.special import gammainc
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

HERE = os.path.dirname(os.path.abspath(__file__))
CFG_DIR = os.path.dirname(HERE)
sys.path.insert(0, CFG_DIR)
sys.path.insert(0, os.path.join(CFG_DIR, "CFG44_fluid_target"))
import CFG7_common as C                                                                  # noqa: E402  (Report, jclean)
from Bcommon import G, A0, KPC_M, exp_sphere, point_mass, target_fields                 # noqa: E402  (READ-ONLY)

MUTATE = os.environ.get("MUTATE", "0") == "1"
SLUG = "CFG119_fdm_soliton"

# ------------------------------------------------------------------------------------------------------------ constants
HBAR = 1.054571817e-34            # J s
EV_J = 1.602176634e-19            # J
C_SI = 299792458.0                # m/s
LN10 = math.log(10.0)
M_GRID = (1e-23, 1e-22, 1e-21, 1e-20)                  # eV, frozen
MB_GRID = (1e9, 1e10, 1e11, 1e12)                      # Msun, frozen
HEXP = {1e9: 2.0, 1e10: 3.0, 1e11: 4.0, 1e12: 5.0}     # kpc, CFG44 / CFG50 exponential spheres
GEOMS = ("point", "exp")
FOOTS = ("canonical", "alt")
A0_FOOT = {"canonical": A0, "alt": C.C4.A0["alt"] * KPC_M / 1e6}      # (km/s)^2/kpc
X_EVAL = np.geomspace(0.1, 30.0, 601)
BAND = (math.log10(0.9), math.log10(1.1))
H_STEP = 1e-3
LOGMS_LO, LOGMS_HI, LOGMS_STEP = -16.0, 4.0, 0.5
LOGMS_SCAN = np.arange(LOGMS_LO, LOGMS_HI + 1e-9, LOGMS_STEP)
GOLDEN_TOL = 1e-3
X_REPORT = (0.1, 0.2, 0.3, 0.5, 1.0, 2.0, 3.0, 5.0, 10.0, 20.0, 30.0)
SCHIVE_A = 0.091                   # Schive 2014 soliton shape coefficient
SCHIVE_AMP = 1.9                   # Msun/pc^3 at m = 1e-23 eV, r_c = 1 kpc
SCHIVE_MMIN0 = 4.4e7               # Msun at m22 = 1


def beta_of_m(m_eV):
    """hbar/m in kpc km/s."""
    return HBAR * C_SI ** 2 / (m_eV * EV_J) / (KPC_M * 1e3)


# ------------------------------------------------------------------------------------------------------------ grid, baryons
class Grid:
    def __init__(self, rmin, rmax, h):
        self.h = h
        self.n = int(math.ceil(math.log(rmax / rmin) / h)) + 1
        self.t = math.log(rmin) + h * np.arange(self.n)
        self.r = np.exp(self.t)


def baryon_phi_M(geom, Mb, r):
    """(Phi_b, M_b(<r)).  Point mass: -G M/r.  Exponential sphere rho_0 e^(-r/h), rho_0 = M/(8 pi h^3) (Bcommon.exp_sphere):
    M_b(<r) = M P(3, s), Phi_b = -G M_b(<r)/r - (G M/2h)(1 + s) e^(-s), s = r/h."""
    r = np.asarray(r, float)
    if geom == "none":
        return np.zeros_like(r), np.zeros_like(r)
    if geom == "point":
        return -G * Mb / r, np.full_like(r, Mb)
    hx = HEXP[Mb]
    s = r / hx
    Menc = Mb * gammainc(3.0, s)
    return -G * Menc / r - (G * Mb / (2.0 * hx)) * (1.0 + s) * np.exp(-s), Menc


def galaxy_grid(beta, Mb, geom, h=H_STEP):
    """one grid per (m, M_b, geometry), shared by every M_sol of the scan: inner edge 1e-6 x the smallest physical scale
    (the Coulomb scale of M_b + 1e4 M_b, the harmonic width of the sphere's core) or 1e-3 r_M if smaller; outer edge
    max(1e3 r_M, 300 a_B).  r_M on the canonical footing (the larger one)."""
    rM = math.sqrt(G * Mb / A0_FOOT["canonical"])
    scales = [beta ** 2 / (G * Mb * (1.0 + 10 ** LOGMS_HI))]
    if geom == "exp":
        hx = HEXP[Mb]
        om = math.sqrt(G * Mb / (6.0 * hx ** 3))
        scales.append(math.sqrt(beta / om))
    rmin = min(1e-3 * rM, 1e-6 * min(scales))
    rmax = max(1e3 * rM, 300.0 * beta ** 2 / (G * Mb))
    return Grid(rmin, rmax, h)


def cusp_lambda(g, c):
    """ghost-point ratio phi_{-1}/phi_0 of the regular solution: phi = r^(1/2) psi, psi ~ psi0 (1 - c r)."""
    r0 = g.r[0]
    rm1 = r0 * math.exp(-g.h)
    return math.exp(-0.5 * g.h) * (1.0 - c * rm1) / (1.0 - c * r0)


# ------------------------------------------------------------------------------------------------------------ linear eigen-solver
class Eig:
    """A phi = e B phi, everything divided by beta^2 (e = eps/beta^2):
       A = tridiag(-1/2h^2, 1/h^2 + 1/8 + r^2 V/beta^2, -1/2h^2) (inner ghost folded into A_00), B = diag(r^2)."""

    def __init__(self, g, lam):
        self.g, self.lam = g, lam
        self.r2 = g.r ** 2
        self.off = -0.5 / g.h ** 2
        self.ab = np.zeros((3, g.n))
        self.ab[0, 1:] = self.off
        self.ab[2, :-1] = self.off

    def set_V(self, V, beta):
        self.w = 0.125 + self.r2 * V / beta ** 2
        self.diag = 1.0 / self.g.h ** 2 + self.w
        self.diag[0] += self.off * self.lam

    def solve(self, s, rhs):
        self.ab[1] = self.diag - s * self.r2
        return solve_banded((1, 1), self.ab, rhs, check_finite=False)

    def rq(self, p):
        """Rayleigh quotient with the kinetic term in gradient form (no cancellation)."""
        d = np.diff(p)
        kin = 0.5 / self.g.h ** 2 * (np.dot(d, d) + (1.0 - self.lam) * p[0] ** 2 + p[-1] ** 2)
        return (kin + np.dot(self.w, p * p)) / np.dot(self.r2, p * p)

    def nrm(self, p):
        return p / math.sqrt(np.dot(self.r2, p * p))

    def _rqi(self, p, tol):
        sig = self.rq(p)
        k = 0
        for k in range(60):
            y = self.solve(sig, self.r2 * p)
            if not np.all(np.isfinite(y)):
                sig *= (1.0 + 1e-12)
                continue
            p = self.nrm(y)
            e = self.rq(p)
            done = abs(e - sig) <= tol * abs(e)
            sig = e
            if done:
                break
        if p[np.argmax(np.abs(p))] < 0:
            p = -p
        big = np.abs(p) > 1e-10 * np.max(np.abs(p))
        return sig, p, bool(np.all(p[big] > 0)), k

    def lowest(self, p=None, sig_lb=None, ell=None, tol=1e-14, maxit=5000):
        """lowest eigenpair.  With p: Rayleigh-quotient iteration from p, kept only if nodeless.  Otherwise: shifted inverse
        iteration from the lower bound sig_lb (converges to the ground state from any positive start), then RQI polish."""
        if p is not None:
            e, q, nl, k = self._rqi(self.nrm(p), tol)
            if nl:
                return e, q, nl, 0
        r = self.g.r
        q = self.nrm(np.sqrt(r) * np.exp(-r / ell))
        e_old = None
        it = 0
        for it in range(1, maxit + 1):
            q = self.nrm(self.solve(sig_lb, self.r2 * q))
            e = self.rq(q)
            if e_old is not None and abs(e - e_old) < 1e-9 * abs(e):
                break
            e_old = e
        e, q, nl, k = self._rqi(q, tol)
        return e, q, nl, it


def normalize(g, p):
    """4 pi [ trapezoid(p^2 r^2 dt) + r0^2 p0^2/3 ] = 1   (int |psi|^2 dV = 1, psi = p/r^(1/2), psi = const inside r0)."""
    f = p ** 2 * g.r ** 2
    I = g.h * (f.sum() - 0.5 * (f[0] + f[-1])) + g.r[0] ** 2 * p[0] ** 2 / 3.0
    return p / math.sqrt(4.0 * math.pi * I)


def self_pot(g, p, Msol):
    """Phi_psi and M(<r) for the normalised p: rho = M_sol p^2/r."""
    r, h = g.r, g.h
    f = p ** 2 * r ** 2
    cum = np.concatenate([[0.0], np.cumsum(0.5 * (f[1:] + f[:-1]) * h)])
    Menc = 4.0 * math.pi * Msol * (cum + r[0] ** 2 * p[0] ** 2 / 3.0)
    q = p ** 2 * r
    rc = np.concatenate([[0.0], np.cumsum(0.5 * (q[1:] + q[:-1]) * h)])
    return -G * Menc / r - 4.0 * math.pi * G * Msol * (rc[-1] - rc), Menc


def scf(g, Vb, beta, Msol, c_cusp, x0, Mt, mix=0.5, mem=6, tol_e=1e-11, tol_x=1e-10, maxit=400):
    """self-consistent iteration on Phi_psi (Anderson mixing).  Returns the converged state."""
    E = Eig(g, cusp_lambda(g, c_cusp))
    ell = beta ** 2 / (G * Mt)
    x = x0.copy()
    Xs, Fs = [], []
    e_prev, p, ncold, res, de = None, None, 0, 1.0, 1.0
    nl = False
    for k in range(maxit):
        V = Vb + x
        E.set_V(V, beta)
        lb = max(float(np.min(V)), -(G * Mt) ** 2 / (2.0 * beta ** 2) * 1.0001) / beta ** 2
        e, p, nl, i_inv = E.lowest(p=p, sig_lb=lb, ell=ell)
        ncold += int(i_inv > 0)
        pn = normalize(g, p)
        Pn, Menc = self_pot(g, pn, Msol)
        f = Pn - x
        res = float(np.max(np.abs(f)) / max(np.max(np.abs(Pn)), 1e-300))
        de = abs(e - e_prev) / abs(e) if e_prev is not None else 1.0
        if res < tol_x and de < tol_e:
            return dict(e=e, eps=e * beta ** 2, p=pn, Phi=Pn, Menc=Menc, V=Vb + Pn, it=k, res=res, de=de, nodeless=nl,
                        conv=True, ncold=ncold)
        e_prev = e
        Xs.append(x.copy())
        Fs.append(f.copy())
        if len(Xs) > mem + 1:
            Xs.pop(0)
            Fs.pop(0)
        if len(Xs) >= 2:
            dF = np.stack([Fs[i + 1] - Fs[i] for i in range(len(Fs) - 1)], axis=1)
            gam = np.linalg.lstsq(dF, f, rcond=None)[0]
            xn = x + mix * f
            for j in range(len(gam)):
                xn = xn - gam[j] * ((Xs[j + 1] - Xs[j]) + mix * (Fs[j + 1] - Fs[j]))
            x = xn
        else:
            x = x + mix * f
    Pn, Menc = self_pot(g, normalize(g, p), Msol)
    return dict(e=e, eps=e * beta ** 2, p=normalize(g, p), Phi=Pn, Menc=Menc, V=Vb + Pn, it=maxit, res=res, de=de,
                nodeless=nl, conv=False, ncold=ncold)


# ------------------------------------------------------------------------------------------------------------ tails in log space
def log_tail(r, qn, i0):
    """exact piecewise-constant-q sweep of chi'' = q chi (chi = r psi; q = 2(V - eps)/beta^2 at nodes, cell value = mean of
    its ends) inward from a Dirichlet ghost beyond the last node.  Returns (L, ok), L[i] = ln chi_i - ln chi_{n-1} for
    i >= i0 (nan below); ok = False if a node is met (never for a ground state)."""
    n = len(r)
    rl = r.tolist()
    ql = qn.tolist()
    L = [math.nan] * n
    D = rl[-1] * (rl[-1] / rl[-2]) - rl[-1]
    q = ql[-1]
    if q > 0:
        k = math.sqrt(q)
        a = k * D
        s = -k / math.tanh(a) if a < 30.0 else -k
    elif q < 0:
        k = math.sqrt(-q)
        s = -k / math.tan(k * D)
    else:
        s = -1.0 / D
    acc = 0.0
    L[n - 1] = 0.0
    sqrt, log, expm1, cos, sin = math.sqrt, math.log, math.expm1, math.cos, math.sin
    for i in range(n - 2, i0 - 1, -1):
        D = rl[i + 1] - rl[i]
        q = 0.5 * (ql[i] + ql[i + 1])
        if q > 0:
            k = sqrt(q)
            a = k * D
            u = s / k
            if a > 30.0:
                if u >= 1.0:
                    return np.array(L), False
                lr = a + log(0.5 * (1.0 - u))
                s = -k
            else:
                em = -expm1(-2.0 * a)
                ep = 2.0 - em
                den = ep - u * em
                if den <= 0.0:
                    return np.array(L), False
                lr = a - 0.6931471805599453 + log(den)
                s = k * (u * ep - em) / den
        elif q < 0:
            k = sqrt(-q)
            b = k * D
            cb, sb = cos(b), sin(b)
            rat = cb - (s / k) * sb
            if rat <= 0.0:
                return np.array(L), False
            lr = log(rat)
            s = (k * sb + cb * s) / rat
        else:
            rat = 1.0 - s * D
            if rat <= 0.0:
                return np.array(L), False
            lr = log(rat)
            s = s / rat
        acc += lr
        L[i] = acc
    return np.array(L), True


def lnpsi_of(g, p, V, e, beta):
    """ln psi on every node: the finite-difference eigenvector up to the peak of chi = r psi, the log-space tail beyond it."""
    chi = np.sqrt(g.r) * p
    ip = int(np.argmax(chi))
    q = 2.0 * (V / beta ** 2 - e)
    L, ok = log_tail(g.r, q, ip)
    ln = np.empty(g.n)
    with np.errstate(divide="ignore"):
        ln[:ip + 1] = np.log(np.abs(p[:ip + 1])) - 0.5 * g.t[:ip + 1]
    ln[ip:] = L[ip:] + (math.log(chi[ip]) - L[ip]) - g.t[ip:]
    return ln, ok


# ------------------------------------------------------------------------------------------------------------ the evaluator (G1)
def ratio_curve(t_nodes, lnrho_nodes, Mcold_nodes, Mb, geom, a0):
    """log10 [C_eval/C_target] on X_EVAL:  C_eval = rho r^3 G (M_b(<r) + M_cold(<r))/r^2, C_target = (a0/4 pi) M_b(<r)."""
    rM = math.sqrt(G * Mb / a0)
    r = X_EVAL * rM
    lr = np.log(r)
    lrho = np.interp(lr, t_nodes, lnrho_nodes)
    Mc = np.interp(lr, t_nodes, Mcold_nodes)
    _, Mbe = baryon_phi_M(geom, Mb, r)
    return (math.log(4.0 * math.pi * G) + lrho + lr + np.log(Mbe + Mc) - math.log(a0) - np.log(Mbe)) / LN10


def curve_stats(L):
    j = int(np.argmax(np.abs(L)))
    lo, hi = BAND
    bad = (L < lo) | (L > hi)
    inner, outer = X_EVAL <= 1.0, X_EVAL >= 1.0
    bi, bo = bool((bad & inner).any()), bool((bad & outer).any())
    fails = "none" if not bad.any() else ("both" if (bi and bo) else ("inner" if bi else "outer"))
    return dict(J=float(abs(L[j])), xJ=float(X_EVAL[j]), passed=bool(not bad.any()), fails=fails,
                L_at={f"{x:g}": float(np.interp(math.log(x), np.log(X_EVAL), L)) for x in X_REPORT},
                Lmin=float(L.min()), Lmax=float(L.max()))


def slope_at(t_nodes, y_nodes, x, Mb, a0):
    """d y/d ln r at x r_M (y = ln rho)."""
    rM = math.sqrt(G * Mb / a0)
    lr = math.log(x * rM)
    k = int(np.clip(np.searchsorted(t_nodes, lr), 1, len(t_nodes) - 2))
    return float((y_nodes[k + 1] - y_nodes[k - 1]) / (t_nodes[k + 1] - t_nodes[k - 1]))


# ------------------------------------------------------------------------------------------------------------ the soliton template
def template_potential(T, g, beta, Msol):
    """the no-baryon SP soliton's potential, rescaled to M_sol (SP scaling: r -> r/l_s, Phi -> (G M_sol/l_s) Phi_hat)."""
    ls = beta ** 2 / (G * Msol)
    lrh = g.t - math.log(ls)
    ph = np.interp(lrh, T["lr"], T["Phat"])
    far = lrh > T["lr"][-1]
    ph[far] = -np.exp(-lrh[far])
    return G * Msol / ls * ph


def msol_rule_i(Mh, m, fc):
    """Schive et al. 2014 at z = 0: M_c = (1/4) (M_h/M_min,0)^(1/3) M_min,0, M_min,0 = 4.4e7 m22^(-3/2); M_sol = M_c/f_c."""
    m22 = m / 1e-22
    mmin = SCHIVE_MMIN0 * m22 ** -1.5
    Mc = 0.25 * (Mh / mmin) ** (1.0 / 3.0) * mmin
    return Mc / fc, Mc


# ------------------------------------------------------------------------------------------------------------ Newton cross-check (N2)
def newton_sp(g, Vb, beta, Msol, c_cusp, phi0, Phi0, e0, tol=1e-12, maxit=60):
    """Newton-Raphson on the coupled finite-difference system (phi, Phi, e = eps/beta^2) with the DIFFERENTIAL Poisson
    equation Phi_tt + Phi_t = 4 pi G M_sol r phi^2 (inner ghost Phi_-1 = Phi_1, outer ghost Phi ~ 1/r) and the normalisation;
    the bordered Jacobian is factorised by sparse LU.  An independent discretisation of the same problem."""
    n, h, r = g.n, g.h, g.r
    r2 = r * r
    lam = cusp_lambda(g, c_cusp)
    b2 = beta * beta
    K4 = 4.0 * math.pi * G * Msol
    eh = math.exp(-h)
    w = np.full(n, h)
    w[0] = w[-1] = 0.5 * h
    wn = 4.0 * math.pi * (w * r2)
    wn[0] += 4.0 * math.pi * r2[0] / 3.0
    p, P, e = phi0.copy(), Phi0.copy(), e0
    kd, ko = 1.0 / h ** 2 + 0.125, -0.5 / h ** 2
    pd, pu, pl = -2.0 / h ** 2, 1.0 / h ** 2 + 0.5 / h, 1.0 / h ** 2 - 0.5 / h
    i = np.arange(n)
    upv = np.full(n - 1, pu)
    upv[0] += pl
    rows_st = np.concatenate([2 * i[1:], 2 * i[:-1], 2 * i[1:] + 1, 2 * i[:-1] + 1])
    cols_st = np.concatenate([2 * i[1:] - 2, 2 * i[:-1] + 2, 2 * i[1:] - 1, 2 * i[:-1] + 3])
    vals_st = np.concatenate([np.full(n - 1, ko), np.full(n - 1, ko), np.full(n - 1, pl), upv])
    de, fn = 1.0, 1.0
    for it in range(maxit):
        S = kd * p + r2 * (Vb + P) / b2 * p - e * r2 * p
        S[1:] += ko * p[:-1]
        S[:-1] += ko * p[1:]
        S[0] += ko * lam * p[0]
        Pm = np.empty(n)
        Pp = np.empty(n)
        Pm[1:] = P[:-1]
        Pm[0] = P[1]
        Pp[:-1] = P[1:]
        Pp[-1] = P[-1] * eh
        Q = pl * Pm + pd * P + pu * Pp - K4 * r * p * p
        Nres = float(np.dot(wn, p * p) - 1.0)
        fn = max(np.max(np.abs(S)) / np.max(np.abs(kd * p)), np.max(np.abs(Q)) / max(np.max(np.abs(pd * P)), 1e-300), abs(Nres))
        if fn < tol and it > 0:
            return dict(p=p, Phi=P, e=e, it=it, conv=True, fn=float(fn), de=de)
        dS = kd + r2 * (Vb + P) / b2 - e * r2
        dS[0] += ko * lam
        dQ = np.full(n, pd)
        dQ[-1] += pu * eh
        rows = np.concatenate([rows_st, 2 * i, 2 * i, 2 * i + 1, 2 * i + 1, 2 * i, np.full(n, 2 * n)])
        cols = np.concatenate([cols_st, 2 * i, 2 * i + 1, 2 * i + 1, 2 * i, np.full(n, 2 * n), 2 * i])
        vals = np.concatenate([vals_st, dS, r2 * p / b2, dQ, -2.0 * K4 * r * p, -r2 * p, 2.0 * wn * p])
        J = sps.csc_matrix((vals, (rows, cols)), shape=(2 * n + 1, 2 * n + 1))
        F = np.empty(2 * n + 1)
        F[0:2 * n:2] = S
        F[1:2 * n:2] = Q
        F[-1] = Nres
        du = splu(J, permc_spec="COLAMD").solve(-F)
        p = p + du[0:2 * n:2]
        P = P + du[1:2 * n:2]
        e_new = e + du[-1]
        de = abs(e_new - e) / abs(e_new)
        e = e_new
    return dict(p=p, Phi=P, e=e, it=maxit, conv=False, fn=float(fn), de=de)


# ------------------------------------------------------------------------------------------------------------ one galaxy (a worker)
def run_galaxy(args):
    """all SP states of one (m, M_b, geometry): rule (i) on both footings, the rule-(ii) scan and its golden refinement per
    footing, the Newton cross-check of the canonical rule-(i) state.  Returns summaries only."""
    m, Mb, geom, T, Mh, fc, tslope = args
    t0 = time.time()
    b = beta_of_m(m)
    g = galaxy_grid(b, Mb, geom)
    Vb, _ = baryon_phi_M(geom, Mb, g.r)
    c = G * Mb / b ** 2 if geom == "point" else 0.0
    cache = {}

    def state(lf, keep=False):
        key = round(float(lf), 9)
        if key in cache and (not keep or "lnrho" in cache[key]):
            return cache[key]
        Msol = Mb * 10.0 ** lf
        S = scf(g, Vb, b, Msol, c, template_potential(T, g, b, Msol), Mb + Msol)
        ln, ok = lnpsi_of(g, S["p"], S["V"], S["e"], b)
        lnrho = math.log(Msol) + 2.0 * ln
        curves = {f: ratio_curve(g.t, lnrho, S["Menc"], Mb, geom, A0_FOOT[f]) for f in FOOTS}
        rec = dict(lf=float(lf), Msol=Msol, eps=S["eps"], it=S["it"], de=S["de"], res=S["res"], conv=S["conv"],
                   nodeless=S["nodeless"], tail_ok=ok, ncold=S["ncold"],
                   J={f: float(np.max(np.abs(curves[f]))) for f in FOOTS})
        if keep:
            rec["stats"] = {f: curve_stats(curves[f]) for f in FOOTS}
            rec["slopes"] = {f: dict(sp01=slope_at(g.t, lnrho, 0.1, Mb, A0_FOOT[f]), sp30=slope_at(g.t, lnrho, 30.0, Mb, A0_FOOT[f]))
                             for f in FOOTS}
            rec["lnrho"] = True
            rec["_S"] = S
        cache[key] = rec
        return rec

    out = dict(m=m, Mb=Mb, geom=geom, n_grid=g.n, rmin_over_rM=float(g.r[0] / math.sqrt(G * Mb / A0_FOOT["canonical"])),
               rmax_over_rM=float(g.r[-1] / math.sqrt(G * Mb / A0_FOOT["canonical"])), aB_over_rM=float(b ** 2 / (G * Mb) / math.sqrt(G * Mb / A0_FOOT["canonical"])))
    # rule (i)
    rule_i = {}
    for f in FOOTS:
        Msol, Mc = msol_rule_i(Mh[f], m, fc)
        rec = state(math.log10(Msol / Mb), keep=True)
        st = rec["stats"][f]
        rule_i[f] = dict(Msol=Msol, Mc=Mc, Mh=Mh[f], Msol_over_Mb=Msol / Mb, eps=rec["eps"], **st, slopes=rec["slopes"][f],
                         target_slopes=tslope[f])
    # rule (ii): scan + golden, per footing
    scan = {f: [] for f in FOOTS}
    for lf in LOGMS_SCAN:
        rec = state(lf)
        for f in FOOTS:
            scan[f].append(rec["J"][f])
    rule_ii = {}
    gr = (math.sqrt(5.0) - 1.0) / 2.0
    for f in FOOTS:
        k = int(np.argmin(scan[f]))
        a, bb = max(LOGMS_LO, LOGMS_SCAN[k] - LOGMS_STEP), min(LOGMS_HI, LOGMS_SCAN[k] + LOGMS_STEP)
        cc, dd = bb - gr * (bb - a), a + gr * (bb - a)
        fcv, fdv = state(cc)["J"][f], state(dd)["J"][f]
        while bb - a > GOLDEN_TOL:
            if fcv < fdv:
                bb, dd, fdv = dd, cc, fcv
                cc = bb - gr * (bb - a)
                fcv = state(cc)["J"][f]
            else:
                a, cc, fcv = cc, dd, fdv
                dd = a + gr * (bb - a)
                fdv = state(dd)["J"][f]
        best_lf = min(cache, key=lambda kk: cache[kk]["J"][f])
        rec = state(best_lf, keep=True)
        st = rec["stats"][f]
        rule_ii[f] = dict(Msol=rec["Msol"], Msol_over_Mb=rec["Msol"] / Mb, lf=rec["lf"], eps=rec["eps"], **st,
                          slopes=rec["slopes"][f], target_slopes=tslope[f],
                          at_boundary=bool(abs(rec["lf"] - LOGMS_LO) < 1e-6 or abs(rec["lf"] - LOGMS_HI) < 1e-6),
                          scan_J=[float(v) for v in scan[f]])
    # SCF diagnostics over every state computed for this galaxy
    recs = list(cache.values())
    diag = dict(n_states=len(recs), all_conv=all(r_["conv"] for r_ in recs), all_nodeless=all(r_["nodeless"] for r_ in recs),
                all_tail_ok=all(r_["tail_ok"] for r_ in recs), max_de=max(r_["de"] for r_ in recs),
                max_res=max(r_["res"] for r_ in recs), max_it=max(r_["it"] for r_ in recs),
                n_cold_restarts=sum(max(r_["ncold"] - 1, 0) for r_ in recs))
    # N2: Newton on the coupled system for the canonical rule-(i) state, started from the rescaled soliton + the linear state
    Msol = rule_i["canonical"]["Msol"]
    P0 = template_potential(T, g, b, Msol)
    E = Eig(g, cusp_lambda(g, c))
    E.set_V(Vb + P0, b)
    lb = max(float(np.min(Vb + P0)), -(G * (Mb + Msol)) ** 2 / (2.0 * b ** 2) * 1.0001) / b ** 2
    e1, p1, _, _ = E.lowest(sig_lb=lb, ell=b ** 2 / (G * (Mb + Msol)))
    NR = newton_sp(g, Vb, b, Msol, c, normalize(g, p1), P0, e1)
    pn = NR["p"] * (1.0 if NR["p"][np.argmax(np.abs(NR["p"]))] > 0 else -1.0)
    big = np.abs(pn) > 1e-10 * np.max(np.abs(pn))
    lnN, okN = lnpsi_of(g, pn, Vb + NR["Phi"], NR["e"], b)
    f_ = pn ** 2 * g.r ** 2
    cumN = np.concatenate([[0.0], np.cumsum(0.5 * (f_[1:] + f_[:-1]) * g.h)])
    MencN = 4.0 * math.pi * Msol * (cumN + g.r[0] ** 2 * pn[0] ** 2 / 3.0)
    LN = ratio_curve(g.t, math.log(Msol) + 2.0 * lnN, MencN, Mb, geom, A0_FOOT["canonical"])
    JN = float(np.max(np.abs(LN)))
    recI = state(math.log10(Msol / Mb), keep=True)
    newton = dict(conv=NR["conv"], it=NR["it"], nodeless=bool(np.all(pn[big] > 0)), tail_ok=okN,
                  eps_newton=NR["e"] * b ** 2, eps_scf=recI["eps"], rel_eps=abs(NR["e"] * b ** 2 / recI["eps"] - 1.0),
                  J_newton=JN, J_scf=recI["J"]["canonical"], dJ=abs(JN - recI["J"]["canonical"]))
    out.update(rule_i=rule_i, rule_ii=rule_ii, diag=diag, newton=newton, seconds=time.time() - t0)
    return out


def recompute_state(m, Mb, geom, lf, T, h):
    """one SP state at a given grid step (for the grid-convergence check N3): eps and J on the canonical footing."""
    b = beta_of_m(m)
    g = galaxy_grid(b, Mb, geom, h=h)
    Vb, _ = baryon_phi_M(geom, Mb, g.r)
    c = G * Mb / b ** 2 if geom == "point" else 0.0
    Msol = Mb * 10.0 ** lf
    S = scf(g, Vb, b, Msol, c, template_potential(T, g, b, Msol), Mb + Msol)
    ln, ok = lnpsi_of(g, S["p"], S["V"], S["e"], b)
    L = ratio_curve(g.t, math.log(Msol) + 2.0 * ln, S["Menc"], Mb, geom, A0_FOOT["canonical"])
    return dict(eps=S["eps"], J=float(np.max(np.abs(L))), conv=S["conv"], nodeless=S["nodeless"], tail_ok=ok, n=g.n)


# ------------------------------------------------------------------------------------------------------------ C1 shooting cross-check
def shoot_soliton():
    """no-baryon SP ground state by shooting, units beta = G = 1, psi(0) = 1, Phi(0) = 0:
       psi'' + 2 psi'/r = 2 (Phi - e) psi,  Phi'' + 2 Phi'/r = 4 pi psi^2.  Bisection on e (sign of the divergence)."""
    def rhs(r, y, e):
        psi, dpsi, Phi, dPhi, M = y
        return [dpsi, 2.0 * (Phi - e) * psi - 2.0 * dpsi / r, dPhi, 4.0 * math.pi * psi ** 2 - 2.0 * dPhi / r,
                4.0 * math.pi * psi ** 2 * r * r]

    def shoot(e, R=20.0):
        r0 = 1e-6
        y0 = [1.0 - e * r0 ** 2 / 3.0, -2.0 * e * r0 / 3.0, (2.0 * math.pi / 3.0) * r0 ** 2, (4.0 * math.pi / 3.0) * r0,
              (4.0 * math.pi / 3.0) * r0 ** 3]

        def cross(r, y, e):
            return y[0]
        cross.terminal, cross.direction = True, -1

        def turn(r, y, e):
            return y[1]
        turn.terminal, turn.direction = True, 1
        s = solve_ivp(rhs, (r0, R), y0, args=(e,), rtol=1e-13, atol=1e-16, method="DOP853", events=(cross, turn),
                      dense_output=True)
        if s.t_events[0].size:
            return +1, s
        if s.t_events[1].size:
            return -1, s
        return 0, s

    lo, hi = 0.1, 3.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        sg, _s = shoot(mid)
        if sg > 0:
            hi = mid
        else:
            lo = mid
        if hi - lo < 1e-15 * mid:
            break
    e = 0.5 * (lo + hi)
    _, s = shoot(lo)
    psi, Phi, M = s.y[0], s.y[2], s.y[4]
    j = np.where(psi < 1e-6)[0]
    j = int(j[0]) if j.size else len(s.t) - 1
    Mt = M[j]
    Phi_inf = Phi[j] + Mt / s.t[j]
    inv_e = (e - Phi_inf) / Mt ** 2
    rc = brentq(lambda rr: s.sol(rr)[0] ** 2 - 0.5, 1e-3, s.t[j])
    prof = {k: float(s.sol(k * rc)[0] ** 2) for k in (0.5, 1.0, 1.5, 2.0, 2.5, 3.0)}
    fc = float(s.sol(rc)[4] / Mt)
    return dict(inv_e=float(inv_e), inv_rc=float(rc * Mt), fc=fc, prof=prof, e_center=e)


def pure_soliton(m, Msol, h=H_STEP):
    b = beta_of_m(m)
    ls = b ** 2 / (G * Msol)
    g = Grid(1e-7 * ls, 400.0 * ls, h)
    S = scf(g, np.zeros(g.n), b, Msol, 0.0, np.zeros(g.n), Msol)
    psi = S["p"] / np.sqrt(g.r)
    rho = Msol * psi ** 2
    rho0 = rho[0]
    with np.errstate(divide="ignore"):
        lr = np.log(rho / rho0)
    i = int(np.searchsorted(-lr, math.log(2.0)))
    tc = float(np.interp(math.log(2.0), -lr[:i + 2], g.t[:i + 2]))
    rc = math.exp(tc)
    sel = g.r <= 3.0 * rc
    fit = (1.0 + SCHIVE_A * (g.r[sel] / rc) ** 2) ** -8
    ratio = rho[sel] / rho0 / fit
    dev = ratio - 1.0
    kmax = int(np.argmax(np.abs(dev)))
    ok3 = np.abs(dev) <= 0.03
    r_ok = float(g.r[sel][np.argmax(~ok3)] / rc) if (~ok3).any() else 3.0
    dev_rho0 = float(np.max(np.abs(rho[sel] / rho0 - fit)))
    Mc = float(np.interp(tc, g.t, S["Menc"]))
    prof = {k: float(np.interp(math.log(k * rc), g.t, rho / rho0)) for k in (0.5, 1.0, 1.5, 2.0, 2.5, 3.0)}
    return dict(S=S, g=g, beta=b, ls=ls, rc=rc, rho0=rho0, fc=Mc / Msol, maxdev=float(np.abs(dev[kmax])),
                maxdev_signed=float(dev[kmax]), x_maxdev=float(g.r[sel][kmax] / rc), r_within3=r_ok, dev_rel_rho0=dev_rho0,
                inv_e=float(S["eps"] * b ** 2 / (G * Msol) ** 2), inv_rc=float(rc * G * Msol / b ** 2),
                amp=float(rho0 / 1e9 * rc ** 4 * (m / 1e-23) ** 2), prof=prof, it=S["it"], conv=S["conv"], de=S["de"])


# ------------------------------------------------------------------------------------------------------------ main
def factor(J):
    """10^J as text (J can be ~1e11 dex)."""
    return f"{10 ** J:.3g}" if J < 300 else f"10^{J:.4g}"


def main():
    R = C.Report(SLUG, MUTATE)
    t_start = time.time()
    R.banner("CFG119 -- Door 7: FDM soliton plus baryons (Schrodinger-Poisson ground state) against the CFG44 target"
             + ("   [MUTATE: G1 evaluated on the target's own rho_c]" if MUTATE else ""))
    R.P("  Frozen criteria: ../CFG119_FROZEN_CRITERIA.md.  Shared gates: ../closure_map/TEN_DOORS_GATES_2026-09-29.md.")
    R.P("  Target: CFG44 Bcommon (read-only): C(r) = rho_c r^3 g_tot = (a0/4 pi) M_b(<r).  Pass band for C_SP/C_target: [0.9, 1.1]")
    R.P("  over x = r/r_M in [0.1, 30] (601 log-spaced points), M_b = 1e9..1e12 Msun, point mass and exponential spheres")
    R.P("  (h = 2, 3, 4, 5 kpc), ONE m at every mass.  m grid (frozen, not tuned): 1e-23, 1e-22, 1e-21, 1e-20 eV.")
    R.P(f"  a0: canonical {A0_FOOT['canonical'] * 1e6 / KPC_M:.5e} m/s^2 (Bcommon), alt {A0_FOOT['alt'] * 1e6 / KPC_M:.5e} m/s^2 (FP0).")
    R.P("  Method: finite-difference (t = ln r, step 1e-3) inverse iteration for the lowest eigenpair inside a self-consistent")
    R.P("  (Anderson-mixed) iteration on Phi_psi, started from the rescaled no-baryon soliton; eps converged to < 1e-11 between")
    R.P("  iterations; tails in log space (no underflow).  Cross-checks: shooting (C1x), Newton on the coupled system (N2),")
    R.P("  half the grid step (N3).  Departures from the frozen file are listed in the README.")
    for m in M_GRID:
        R.P(f"    m = {m:.0e} eV: hbar/m = {beta_of_m(m):.6g} kpc km/s")
    R.num("A0_canonical_SI", A0_FOOT["canonical"] * 1e6 / KPC_M)
    R.num("A0_alt_SI", A0_FOOT["alt"] * 1e6 / KPC_M)

    # ---------------------------------------------------------------------------------------------------- N0: the target
    R.banner("N0  the imported target (CFG44 Bcommon.target_fields) and the rule-(i) halo mass M_h = M_cold(<30 r_M)")
    Mh, tslope, tfields = {}, {}, {}
    worst_C, worst_M = 0.0, 0.0
    for geom in GEOMS:
        for Mb in MB_GRID:
            prof = point_mass(Mb) if geom == "point" else exp_sphere(Mb, HEXP[Mb])
            for f in FOOTS:
                a0 = A0_FOOT[f]
                tf = target_fields(prof, a0=a0)
                rM = math.sqrt(G * Mb / a0)
                sel = (tf["r"] >= 0.1 * rM) & (tf["r"] <= 30.0 * rM)
                _, Mbe = baryon_phi_M(geom, Mb, tf["r"][sel])
                Ct = tf["rho"][sel] * tf["r"][sel] ** 3 * tf["g"][sel]
                worst_C = max(worst_C, float(np.max(np.abs(Ct / (a0 / (4 * math.pi) * Mbe) - 1.0))))
                worst_M = max(worst_M, float(np.max(np.abs(tf["uN"][sel] / (G * Mbe) - 1.0))))
                Mh[(geom, Mb, f)] = float(np.interp(math.log(30.0 * rM), np.log(tf["r"]), tf["w"])) / G
                tslope[(geom, Mb, f)] = dict(t01=float(np.interp(math.log(0.1 * rM), np.log(tf["r"]), tf["dln"])),
                                             t30=float(np.interp(math.log(30.0 * rM), np.log(tf["r"]), tf["dln"])))
                tfields[(geom, Mb, f)] = tf
    mh_pt = Mh[("point", 1e10, "canonical")] / 1e10
    R.P(f"  target identity rho_c r^3 g_tot = (a0/4 pi) M_b(<r) over x in [0.1, 30], 8 galaxies x 2 footings: worst {worst_C:.2e}")
    R.P(f"  analytic M_b(<r) used by the evaluator vs Bcommon's profile u_N/G: worst {worst_M:.2e}")
    R.P(f"  M_h/M_b (point mass) = {mh_pt:.7f}  (analytic sqrt(901) - 1 = {math.sqrt(901.0) - 1.0:.7f})")
    for geom in GEOMS:
        R.P(f"  M_h/M_b {geom:5s}: " + "  ".join(f"{Mb:.0e}: {Mh[(geom, Mb, 'canonical')] / Mb:.4f} (can) {Mh[(geom, Mb, 'alt')] / Mb:.4f} (alt)" for Mb in MB_GRID))
    okN0 = worst_C < 1e-6 and worst_M < 1e-6 and abs(mh_pt / (math.sqrt(901.0) - 1.0) - 1.0) < 1e-6
    R.check("N0 the imported target reproduces C = (a0/4 pi) M_b(<r) and M_h(point) = (sqrt(901) - 1) M_b to 1e-6",
            f"identity {worst_C:.2e}; M_b(<r) {worst_M:.2e}; M_h/M_b = {mh_pt:.7f}", okN0)
    R.num("N0", dict(worst_identity=worst_C, worst_Mb=worst_M, Mh_over_Mb={f"{g_}|{Mb:.0e}|{f}": Mh[(g_, Mb, f)] / Mb for (g_, Mb, f) in Mh}))

    # ---------------------------------------------------------------------------------------------------- C2
    R.banner("C2  CONTROL: self-gravity off, point mass: the ground state is hydrogen-like, psi ~ exp(-r/a_B), a_B = hbar^2/(G M_b m^2)")
    R.P("  on each galaxy's own solver grid; sup|psi - psi_H|/psi_H(0) (normalised), |eps/eps_H - 1| with eps_H = E_H/m = -(G M_b)^2/(2 beta^2), beta = hbar/m,")
    R.P("  and the log-space tail: max |ln psi/ln psi_H - 1| over x in [0.1, 30] where |ln psi_H| > 1")
    R.P(f"  {'m [eV]':>8s} {'M_b':>7s} {'a_B/r_M':>10s} {'n_grid':>7s} {'|de|':>9s} {'sup dpsi':>9s} {'tail rel':>9s} {'ln psi_H(30 r_M)':>17s}")
    c2 = []
    for m in M_GRID:
        b = beta_of_m(m)
        for Mb in MB_GRID:
            g = galaxy_grid(b, Mb, "point")
            Vb, _ = baryon_phi_M("point", Mb, g.r)
            aB = b ** 2 / (G * Mb)
            E = Eig(g, cusp_lambda(g, G * Mb / b ** 2))
            E.set_V(Vb, b)
            e, p, nl, _ = E.lowest(sig_lb=-(G * Mb) ** 2 / (2 * b ** 4) * 1.0001, ell=aB)
            p = normalize(g, p)
            psi = p / np.sqrt(g.r)
            psiH = np.exp(-g.r / aB) / math.sqrt(math.pi * aB ** 3)
            sup = float(np.max(np.abs(psi - psiH)) / psiH[0])
            de = abs(e * b ** 2 / (-(G * Mb) ** 2 / (2 * b ** 2)) - 1.0)
            ln, ok = lnpsi_of(g, p, Vb, e, b)
            rM = math.sqrt(G * Mb / A0_FOOT["canonical"])
            rr = X_EVAL * rM
            lp = np.interp(np.log(rr), g.t, ln)
            lex = -rr / aB - 0.5 * math.log(math.pi * aB ** 3)
            use = np.abs(lex) > 1.0
            tail = float(np.max(np.abs(lp[use] / lex[use] - 1.0))) if use.any() else 0.0
            c2.append(dict(m=m, Mb=Mb, aB_over_rM=aB / rM, n=g.n, de=de, sup=sup, tail=tail, nodeless=nl, tail_ok=ok,
                           lnpsiH_30=float(lex[-1])))
            R.P(f"  {m:8.0e} {Mb:7.0e} {aB / rM:10.3e} {g.n:7d} {de:9.2e} {sup:9.2e} {tail:9.2e} {lex[-1]:17.5g}")
    w_de, w_sup, w_tail = max(r_["de"] for r_ in c2), max(r_["sup"] for r_ in c2), max(r_["tail"] for r_ in c2)
    okC2 = w_de <= 1e-6 and w_sup <= 1e-6 and w_tail <= 1e-6 and all(r_["nodeless"] and r_["tail_ok"] for r_ in c2)
    R.check("C2 CONTROL: hydrogen-like ground state to 1e-6 (eigenvalue, wavefunction, and the log-space tail) for all 16 (m, M_b)",
            f"worst |eps/eps_H - 1| = {w_de:.2e}, sup|psi - psi_H|/psi_H(0) = {w_sup:.2e}, tail |ln psi/ln psi_H - 1| = {w_tail:.2e}; all nodeless",
            okC2)
    R.num("C2", c2)

    # ---------------------------------------------------------------------------------------------------- C1
    R.banner("C1  CONTROL: no baryons: the ground state vs Schive et al.'s empirical soliton rho ~ (1 + 0.091 (r/r_c)^2)^-8, within 3% to 3 r_c")
    R.P("  M_sol = 1e9 Msun at each m (the shape is universal by the SP scaling; the four runs check that).  r_c = half-peak-density radius.")
    c1 = {}
    for m in M_GRID:
        c1[m] = pure_soliton(m, 1e9)
        s_ = c1[m]
        R.P(f"  m = {m:.0e}: SCF it {s_['it']} (conv {s_['conv']}, dE/E {s_['de']:.1e}); E hbar^2/(G^2 M^2 m^3) = {s_['inv_e']:.10f}; "
            f"r_c G M m^2/hbar^2 = {s_['inv_rc']:.7f}; r_c = {s_['rc']:.5g} kpc; f_c = M(<r_c)/M_sol = {s_['fc']:.6f}")
        R.P(f"         max |rho/rho_fit - 1| over r <= 3 r_c = {s_['maxdev']:.4f} ({s_['maxdev_signed']:+.4f}) at r = {s_['x_maxdev']:.2f} r_c; "
            f"pointwise 3% holds to r = {s_['r_within3']:.2f} r_c; max |rho - rho_fit|/rho0 = {s_['dev_rel_rho0']:.4f}; "
            f"amplitude rho0 r_c^4 (m/1e-23 eV)^2 = {s_['amp']:.4f} Msun/pc^3 kpc^4 (Schive: 1.9)")
    s22 = c1[1e-22]
    R.P("  profile (m = 1e-22):   r/r_c    rho/rho0 (SP)    fit (1+0.091 x^2)^-8    SP/fit - 1")
    for k, v in s22["prof"].items():
        fitv = (1.0 + SCHIVE_A * k * k) ** -8
        R.P(f"                        {k:5.2f}    {v:12.6f}      {fitv:12.6f}          {v / fitv - 1.0:+.4f}")
    worst_c1 = max(c1[m]["maxdev"] for m in M_GRID)
    R.check("C1 CONTROL: no-baryon ground state within 3% (pointwise) of Schive's rho ~ (1 + 0.091 (r/r_c)^2)^-8 out to 3 r_c",
            f"worst max |rho/rho_fit - 1| over r <= 3 r_c = {worst_c1:.4f} (at r = {s22['x_maxdev']:.2f} r_c); the 3% line holds only to "
            f"r = {s22['r_within3']:.2f} r_c.  Relative to rho0 the difference is {s22['dev_rel_rho0']:.4f} (a reading NOT declared; not re-scored)",
            worst_c1 <= 0.03)
    sh = shoot_soliton()
    d_inv_e = abs(sh["inv_e"] / s22["inv_e"] - 1.0)
    d_inv_rc = abs(sh["inv_rc"] / s22["inv_rc"] - 1.0)
    d_fc = abs(sh["fc"] / s22["fc"] - 1.0)
    d_prof = max(abs(sh["prof"][k] - s22["prof"][k]) for k in sh["prof"])
    spread = max(max(abs(c1[m]["inv_e"] / s22["inv_e"] - 1.0), abs(c1[m]["inv_rc"] / s22["inv_rc"] - 1.0)) for m in M_GRID)
    R.P(f"  shooting (units beta = G = 1): eps/M^2 = {sh['inv_e']:.10f}, r_c M = {sh['inv_rc']:.7f}, f_c = {sh['fc']:.6f}; "
        f"profile at r/r_c = 0.5..3: " + ", ".join(f"{v:.6f}" for v in sh["prof"].values()))
    R.check("C1x the finite-difference self-consistent soliton agrees with an independent shooting integration (1e-5)",
            f"|d(eps/M^2)| = {d_inv_e:.1e}, |d(r_c M)| = {d_inv_rc:.1e}, |d f_c| = {d_fc:.1e}, max |d(rho/rho0)| at 0.5..3 r_c = {d_prof:.1e}; "
            f"spread over the four m = {spread:.1e}",
            max(d_inv_e, d_inv_rc, d_fc, d_prof, spread) <= 1e-5)
    R.check("C1a Schive's amplitude 1.9 Msun/pc^3 kpc^4 (m = 1e-23 eV, r_c = 1 kpc) and his two relations' M_c r_c, against the SP ground state",
            f"{s22['amp']:.4f} ({(s22['amp'] / SCHIVE_AMP - 1) * 100:+.1f}%); Schive's two relations imply M_c r_c = 1.6 x (1/4)(4.4e7)^(2/3) x 1e3 = "
            f"{1.6 * 0.25 * SCHIVE_MMIN0 ** (2 / 3) * 1e3:.4g} m22^-2 Msun kpc; the SP ground state gives f_c (r_c M) hbar^2/(G m^2) = "
            f"{s22['fc'] * s22['inv_rc'] * beta_of_m(1e-22) ** 2 / G:.4g} m22^-2 Msun kpc", True, load_bearing=False)
    FC = s22["fc"]
    R.num("C1", {f"{m:.0e}": {k: v for k, v in c1[m].items() if k not in ("S", "g")} for m in M_GRID})
    R.num("C1_shooting", sh)
    R.num("f_c", FC)
    # the template: the m = 1e-22 soliton in units of its own scale
    T = dict(lr=s22["g"].t - math.log(s22["ls"]), Phat=s22["S"]["Phi"] * s22["ls"] / (G * 1e9))

    # ---------------------------------------------------------------------------------------------------- rule (i) masses
    R.banner("RULE (i)  Schive et al. 2014 core-halo relation at z = 0: M_c = (1/4)(M_h/M_min,0)^(1/3) M_min,0, M_min,0 = 4.4e7 m22^-3/2 Msun;"
             f" M_sol = M_c/f_c, f_c = {FC:.6f}")
    for geom in GEOMS:
        for Mb in MB_GRID:
            row = []
            for m in M_GRID:
                Ms, Mc = msol_rule_i(Mh[(geom, Mb, "canonical")], m, FC)
                row.append(f"{m:.0e}: {Ms / Mb:.3e}")
            R.P(f"  {geom:5s} M_b = {Mb:.0e}: M_h = {Mh[(geom, Mb, 'canonical')]:.4e} (canonical);  M_sol/M_b by m:  " + "  ".join(row))

    # ---------------------------------------------------------------------------------------------------- the SP runs (or the MUTATE)
    cells = {}          # (foot, geom, Mb, m, rule) -> stats
    results = []
    if not MUTATE:
        R.banner("SP RUNS  32 galaxies (4 m x 4 M_b x 2 geometries): rule (i) on both footings, the rule-(ii) scan + golden search per footing")
        tasks = [(m, Mb, geom, T, {f: Mh[(geom, Mb, f)] for f in FOOTS}, FC, {f: tslope[(geom, Mb, f)] for f in FOOTS})
                 for geom in GEOMS for Mb in MB_GRID for m in M_GRID]
        nw = max(1, min(12, (os.cpu_count() or 2) - 2))
        R.P(f"  {len(tasks)} tasks on {nw} worker processes (results do not depend on the worker count)")
        t0 = time.time()
        with ProcessPoolExecutor(max_workers=nw, mp_context=mp.get_context("spawn")) as ex:
            results = list(ex.map(run_galaxy, tasks))
        R.P(f"  SP runs done in {time.time() - t0:.0f} s wall; per-galaxy CPU {min(r_['seconds'] for r_ in results):.1f}-{max(r_['seconds'] for r_ in results):.1f} s")
        for res in results:
            for f in FOOTS:
                cells[(f, res["geom"], res["Mb"], res["m"], "i")] = res["rule_i"][f]
                cells[(f, res["geom"], res["Mb"], res["m"], "ii")] = res["rule_ii"][f]
    else:
        R.banner("MUTATE  the target's own rho_c (CFG44 target_fields) replaces the SP ground state in the evaluator, for every (m, rule) cell")
        for geom in GEOMS:
            for Mb in MB_GRID:
                for f in FOOTS:
                    tf = tfields[(geom, Mb, f)]
                    L = ratio_curve(np.log(tf["r"]), np.log(tf["rho"]), tf["w"] / G, Mb, geom, A0_FOOT[f])
                    st = curve_stats(L)
                    for m in M_GRID:
                        for rule in ("i", "ii"):
                            cells[(f, geom, Mb, m, rule)] = dict(Msol=float("nan"), Msol_over_Mb=float("nan"), **st)

    # ---------------------------------------------------------------------------------------------------- R1
    R.banner("R1  per footing, geometry, M_b, m and rule: J = max |log10(C/C_target)| over x in [0.1, 30], where, and the failing region")
    R.P("  (the pass band is log10 ratio in [-0.0458, +0.0414]; 'fails' = inner (x <= 1), outer (x >= 1), both, or none)")
    for f in FOOTS:
        R.P(f"\n  footing: {f}")
        R.P(f"  {'geom':5s} {'M_b':>7s} {'m':>7s} {'rule':>4s} {'M_sol/M_b':>10s} {'J [dex]':>11s} {'at x':>6s} {'L(0.1)':>11s} {'L(1)':>11s} {'L(30)':>11s} {'fails':>5s}"
            + ("" if MUTATE else f" {'slope SP/target at x=0.1':>26s} {'at x=30':>22s}"))
        for geom in GEOMS:
            for Mb in MB_GRID:
                for m in M_GRID:
                    for rule in ("i", "ii"):
                        s_ = cells[(f, geom, Mb, m, rule)]
                        extra = ""
                        if not MUTATE:
                            sl, ts = s_["slopes"], s_["target_slopes"]
                            extra = f" {sl['sp01']:>12.4g} / {ts['t01']:<+7.3f}   {sl['sp30']:>11.4g} / {ts['t30']:<+7.3f}"
                        R.P(f"  {geom:5s} {Mb:7.0e} {m:7.0e} {rule:>4s} {s_['Msol_over_Mb']:10.3e} {s_['J']:11.4g} {s_['xJ']:6.3g} "
                            f"{s_['L_at']['0.1']:11.4g} {s_['L_at']['1']:11.4g} {s_['L_at']['30']:11.4g} {s_['fails']:>5s}" + extra)
    closest = min(cells.items(), key=lambda kv: kv[1]["J"])
    ck = closest[0]
    R.P(f"\n  closest cell anywhere: {ck[0]} footing, {ck[1]}, M_b = {ck[2]:.0e}, m = {ck[3]:.0e} eV, rule ({ck[4]}): J = {closest[1]['J']:.4g} dex "
        f"(a factor {factor(closest[1]['J'])}) at x = {closest[1]['xJ']:.3g}")
    if not MUTATE:
        nb = sum(1 for k_, v_ in cells.items() if k_[4] == "ii" and v_.get("at_boundary"))
        R.P(f"  rule-(ii) optima at the edge of the declared search range [1e-16, 1e4] M_b: {nb} of {sum(1 for k_ in cells if k_[4] == 'ii')}")
        fails = {}
        for k_, v_ in cells.items():
            fails[v_["fails"]] = fails.get(v_["fails"], 0) + 1
        R.P(f"  failing region over all {len(cells)} cells: " + ", ".join(f"{k_}: {v_}" for k_, v_ in sorted(fails.items())))
        rs_cells = []
        for m in M_GRID:
            for Mb in MB_GRID:
                aB = beta_of_m(m) ** 2 / (G * Mb)
                rs = 2.0 * G * Mb / (C_SI / 1e3) ** 2
                if aB < rs:
                    rs_cells.append(dict(m=m, Mb=Mb, aB_over_rs=aB / rs, J_rule_ii_canonical=cells[("canonical", "point", Mb, m, "ii")]["J"]))
        R.P(f"  validity: for the point mass the Bohr radius a_B = hbar^2/(G M_b m^2) lies inside the Schwarzschild radius 2 G M_b/c^2 for "
            f"{len(rs_cells)} of 16 (m, M_b): " + ", ".join(f"({z['m']:.0e} eV, {z['Mb']:.0e}: a_B/r_s = {z['aB_over_rs']:.2g}, J = {z['J_rule_ii_canonical']:.3g})" for z in rs_cells))
        R.P("  the Newtonian ground state is formal in those cells (the exponential spheres have no singular point and no such cells)")
        R.num("aB_inside_rs_point_mass", rs_cells)
    R.num("R1", [dict(foot=k_[0], geom=k_[1], Mb=k_[2], m=k_[3], rule=k_[4], **{kk: vv for kk, vv in v_.items() if kk != "scan_J"})
                 for k_, v_ in cells.items()])

    # ---------------------------------------------------------------------------------------------------- H1
    R.banner("H1  [HEADLINE; MUTATE must change it]  G1 holds: with ONE m at every mass, C/C_target in [0.9, 1.1] over x in [0.1, 30],"
             " for every mass and both geometries, under rule (i) or rule (ii)")
    h1 = {}
    for f in FOOTS:
        per_m = {}
        for m in M_GRID:
            wi = max(cells[(f, geom, Mb, m, "i")]["J"] for geom in GEOMS for Mb in MB_GRID)
            wii = max(cells[(f, geom, Mb, m, "ii")]["J"] for geom in GEOMS for Mb in MB_GRID)
            pi_ = all(cells[(f, geom, Mb, m, "i")]["passed"] for geom in GEOMS for Mb in MB_GRID)
            pii = all(cells[(f, geom, Mb, m, "ii")]["passed"] for geom in GEOMS for Mb in MB_GRID)
            per_m[m] = dict(worst_J_rule_i=wi, worst_J_rule_ii=wii, pass_rule_i=pi_, pass_rule_ii=pii)
            R.P(f"  [{f:9s}] m = {m:.0e}: rule (i) {'PASS' if pi_ else 'FAIL'} (worst galaxy J = {wi:.4g} dex);  "
                f"rule (ii) {'PASS' if pii else 'FAIL'} (worst galaxy J = {wii:.4g} dex)")
        ok = any(v_["pass_rule_i"] or v_["pass_rule_ii"] for v_ in per_m.values())
        best_m = min(M_GRID, key=lambda mm: per_m[mm]["worst_J_rule_ii"])
        h1[f] = dict(passed=ok, per_m={f"{mm:.0e}": v_ for mm, v_ in per_m.items()}, best_m=best_m,
                     best_worst_J=per_m[best_m]["worst_J_rule_ii"])
        R.check(f"H1 [{f}] G1 holds with one m at every mass (rule i or ii)",
                f"best single m = {best_m:.0e} eV under rule (ii): its worst galaxy misses by J = {per_m[best_m]['worst_J_rule_ii']:.4g} dex "
                f"(a factor {factor(per_m[best_m]['worst_J_rule_ii'])}); pass needs J <= 0.0414 on every galaxy", ok)
    R.num("H1", {f: dict(passed=v_["passed"], best_m=v_["best_m"], best_worst_J=v_["best_worst_J"], per_m=v_["per_m"]) for f, v_ in h1.items()})

    # ---------------------------------------------------------------------------------------------------- R2
    R.banner("R2  the best m per mass under rule (ii) (a single m could fit only if these agree)")
    r2 = {}
    if MUTATE:
        R.P("  MUTATE: the target does not depend on m; R2 is not defined here")
    else:
        for f in FOOTS:
            for geom in GEOMS:
                bests = []
                for Mb in MB_GRID:
                    mm = min(M_GRID, key=lambda m_: cells[(f, geom, Mb, m_, "ii")]["J"])
                    bests.append((Mb, mm, cells[(f, geom, Mb, mm, "ii")]["J"]))
                agree = len(set(b_[1] for b_ in bests)) == 1
                r2[f"{f}|{geom}"] = dict(best=[dict(Mb=b_[0], m=b_[1], J=b_[2]) for b_ in bests], agree=agree)
                R.P(f"  [{f:9s}] {geom:5s}: " + "; ".join(f"M_b {b_[0]:.0e} -> m {b_[1]:.0e} (J {b_[2]:.4g})" for b_ in bests)
                    + f"   agree: {agree}")
        R.num("R2", r2)

    # ---------------------------------------------------------------------------------------------------- numerics (main run only)
    if not MUTATE:
        R.banner("N1-N3  numerics of the SP runs")
        allc = all(r_["diag"]["all_conv"] for r_ in results)
        alln = all(r_["diag"]["all_nodeless"] for r_ in results)
        allt = all(r_["diag"]["all_tail_ok"] for r_ in results)
        mde = max(r_["diag"]["max_de"] for r_ in results)
        nst = sum(r_["diag"]["n_states"] for r_ in results)
        mit = max(r_["diag"]["max_it"] for r_ in results)
        ncr = sum(r_["diag"]["n_cold_restarts"] for r_ in results)
        R.check("N1 every SP state converged (|dE/E| < 1e-8 between the last two iterations), nodeless, with a node-free log tail",
                f"{nst} states: converged {allc}, nodeless {alln}, tails ok {allt}; worst final |dE/E| = {mde:.1e}; max iterations {mit}; "
                f"eigen-solver cold restarts after the first {ncr}", allc and alln and allt and mde < 1e-8)
        wN_e = max(r_["newton"]["rel_eps"] for r_ in results)
        wN_J = max(r_["newton"]["dJ"] / (1e-3 + 1e-5 * r_["newton"]["J_scf"]) for r_ in results)
        wN_dJ = max(r_["newton"]["dJ"] for r_ in results)
        nN = all(r_["newton"]["conv"] and r_["newton"]["nodeless"] and r_["newton"]["tail_ok"] for r_ in results)
        R.check("N2 Newton-Raphson on the coupled system (differential Poisson) reproduces the canonical rule-(i) state of all 32 galaxies",
                f"all converged + nodeless {nN}; worst |eps_N/eps_SCF - 1| = {wN_e:.1e} (line 1e-6); worst |dJ| = {wN_dJ:.2e} dex "
                f"(line 1e-3 + 1e-5 J; worst fraction of the line {wN_J:.2f})", nN and wN_e <= 1e-6 and wN_J <= 1.0)
        # N3: half the grid step, five final states
        picks = [(1e-23, 1e9, "point", "ii"), (1e-23, 1e9, "exp", "ii"), (1e-22, 1e11, "exp", "ii"), (1e-20, 1e12, "point", "ii"),
                 (1e-21, 1e10, "exp", "i")]
        n3 = []
        for (m, Mb, geom, rule) in picks:
            s_ = cells[("canonical", geom, Mb, m, rule)]
            lf = math.log10(s_["Msol_over_Mb"])
            a_ = recompute_state(m, Mb, geom, lf, T, H_STEP)
            b_ = recompute_state(m, Mb, geom, lf, T, H_STEP / 2)
            n3.append(dict(m=m, Mb=Mb, geom=geom, rule=rule, lf=lf, eps_h=a_["eps"], eps_h2=b_["eps"], J_h=a_["J"], J_h2=b_["J"],
                           rel_eps=abs(b_["eps"] / a_["eps"] - 1.0), dJ=abs(b_["J"] - a_["J"]), ok_states=a_["conv"] and b_["conv"]
                           and a_["nodeless"] and b_["nodeless"] and a_["tail_ok"] and b_["tail_ok"], n_h2=b_["n"]))
            R.P(f"  {geom:5s} M_b {Mb:.0e} m {m:.0e} rule ({rule}): eps {a_['eps']:.10e} -> {b_['eps']:.10e} (rel {n3[-1]['rel_eps']:.1e}); "
                f"J {a_['J']:.8g} -> {b_['J']:.8g} (|dJ| {n3[-1]['dJ']:.1e}); n = {b_['n']}")
        okN3 = all(z["ok_states"] and z["rel_eps"] <= 1e-6 and z["dJ"] <= 1e-3 + 1e-5 * z["J_h"] for z in n3)
        R.check("N3 halving the grid step changes eps by <= 1e-6 and J by <= 1e-3 dex + 1e-5 J on five final states",
                f"worst rel eps {max(z['rel_eps'] for z in n3):.1e}; worst |dJ| {max(z['dJ'] for z in n3):.1e} dex", okN3)
        R.num("N1", dict(n_states=nst, all_conv=allc, all_nodeless=alln, all_tail_ok=allt, max_de=mde, max_it=mit, cold_restarts=ncr))
        R.num("N2", [dict(m=r_["m"], Mb=r_["Mb"], geom=r_["geom"], **r_["newton"]) for r_ in results])
        R.num("N3", n3)
        R.num("grids", [dict(m=r_["m"], Mb=r_["Mb"], geom=r_["geom"], n=r_["n_grid"], rmin_over_rM=r_["rmin_over_rM"],
                             rmax_over_rM=r_["rmax_over_rM"], aB_over_rM=r_["aB_over_rM"], seconds=r_["seconds"]) for r_ in results])

    # ---------------------------------------------------------------------------------------------------- R3: G2..G5
    R.banner("R3  G2 (Hu, Barkana & Gruzinov 2000 scaling), G3, G4, G5 as statements")
    g2 = []
    for m in M_GRID:
        m22 = m / 1e-22
        kJ = 9.0 * m22 ** 0.5
        cx = 1.61 * m22 ** (1.0 / 18.0) / kJ
        k12 = 4.5 * m22 ** (4.0 / 9.0)
        kk = np.geomspace(1e-4, 30.0, 200001)
        TT = np.cos((cx * kk) ** 3) / (1.0 + (cx * kk) ** 8)
        x95 = brentq(lambda x: math.cos(x ** 3) / (1.0 + x ** 8) - 0.95, 0.1, 1.0)
        k95 = x95 / cx
        T30 = math.cos((cx * 30.0) ** 3) / (1.0 + (cx * 30.0) ** 8)
        ok = bool(TT.min() >= 0.95)
        g2.append(dict(m=m, k_Jeq=kJ, k_half=k12, k_95=k95, T_F_30=T30, min_T_F_to_30=float(TT.min()), within_5pct_to_30=ok))
        R.P(f"  m = {m:.0e}: k_Jeq = {kJ:.3f}/Mpc, k_1/2 (power halves) = {k12:.3f}/Mpc; T_F >= 0.95 only to k = {k95:.3f}/Mpc; "
            f"T_F(30/Mpc) = {T30:+.4f}: {'within' if ok else 'NOT within'} 5% to k = 30/Mpc")
    x95 = brentq(lambda x: math.cos(x ** 3) / (1.0 + x ** 8) - 0.95, 0.1, 1.0)
    m22_needed = (30.0 * 1.61 / (9.0 * x95)) ** (9.0 / 4.0)
    R.check("G2 (statement from HBG's fit) linear growth within 5% of LCDM to k = 30/Mpc for some m on the declared grid",
            f"no: the largest m (1e-20 eV) is suppressed {100 * (1 - g2[-1]['T_F_30']):.1f}% at 30/Mpc; the 5% line to 30/Mpc needs "
            f"m >= {m22_needed * 1e-22:.2e} eV (above the grid); cold at z >~ 10 above the Jeans scale, but the frozen 5% line fails",
            any(z["within_5pct_to_30"] for z in g2), load_bearing=False)
    R.check("G3 (statement) reciprocity and energy: the field gravitates only through ordinary Newtonian gravity",
            "action equals reaction exactly and no extra force acts on the baryons (reaction 0 <= 0.10 g_law); the ground state is the "
            "bound minimum-energy state at fixed M_sol, so no energy supply beyond ordinary gravitational collapse is needed. Not computed.",
            True, load_bearing=False)
    R.check("G4 (statement) constants: m is a new constant not tied to Lambda or kappa (none is declared); rule (ii) adds M_sol per galaxy",
            "FAIL: m (and, under rule (i), Schive's simulation-calibrated normalisation) are constants beyond kappa and Omega_c h^2",
            False, load_bearing=False)
    R.check("G5 (statement) well-posedness: a minimally coupled Klein-Gordon field with m^2 > 0",
            "no ghost (positive kinetic term), no gradient instability, hyperbolic with light-cone characteristics; Solar System safe "
            "(no fifth force, PPN as GR; the local density is negligible for Cassini). The Jeans instability is gravitational, not a pathology.",
            True, load_bearing=False)
    R.num("G2", g2)
    R.num("G2_m_needed_eV", m22_needed * 1e-22)

    # ---------------------------------------------------------------------------------------------------- summary
    R.banner("SUMMARY")
    for f in FOOTS:
        R.P(f"  H1 [{f}]: {'PASS' if h1[f]['passed'] else 'FAIL'}  (best single m {h1[f]['best_m']:.0e} eV; its worst galaxy J = "
            f"{h1[f]['best_worst_J']:.4g} dex under rule (ii))")
    R.P(f"  C1 {'PASS' if worst_c1 <= 0.03 else 'FAIL'} (Schive's fit vs the exact ground state: {worst_c1 * 100:.1f}% at {s22['x_maxdev']:.2f} r_c); "
        f"C2 {'PASS' if okC2 else 'FAIL'}")
    R.P(f"  closest single galaxy over every cell: J = {closest[1]['J']:.4g} dex ({ck[0]}, {ck[1]}, M_b = {ck[2]:.0e}, m = {ck[3]:.0e} eV, rule ({ck[4]}))")
    R.P("  G1 (H1) above; G2 FAIL for every m on the grid; G3 PASS (statement); G4 FAIL (m); G5 PASS (statement).")
    R.P("  kappa = 1/2 and Omega_c h^2 stay fitted.  Nothing here says the data favour either model, or that the theory is closed.")
    R.P(f"  wall time {time.time() - t_start:.0f} s")
    nf = R.write(here=HERE)
    return nf


if __name__ == "__main__":
    sys.exit(1 if main() else 0)
