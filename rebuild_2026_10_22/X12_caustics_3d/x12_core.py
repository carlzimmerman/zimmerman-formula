#!/usr/bin/env python3
"""X12_caustics_3d core: a 3D self-consistent khronon-fluid solver for v3s (FROZEN_CRITERIA §3).

X8 AMENDMENT A1's design carried to 3D: the field operators are gradients of discrete energies (variational finite
differences with the cell-averaged squared edge gradient; the linear part is exactly the 7-point Laplacian), the particles
are energy-conserving quadratic B-spline (TSC) shapes in index space, the start is the exact discrete v3s switched static
equilibrium, the hold law is X8's Anderson fixed point, the 7-point operator is solved by fast diagonalisation, and the
integrator is KDK leapfrog with X8's adaptive step. Physical constants, orbits and the AQUAL boundary data are X8's
(x8_core.py, imported read-only). Units: kpc, Gyr, Msun.

Mirror planes (FROZEN §0, §3): an axis flagged as mirrored starts at coordinate 0 with an unknown node and the natural
condition; particles keep their true (unreflected) positions and deposit / interpolate at |coordinate|.
"""
import ctypes
import math
import os
import subprocess
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
X8DIR = HERE.parent / "X8_soft_side_caustics"
sys.path.insert(0, str(X8DIR))
from x8_core import (A0, EPS, G, K, KMS, LSTAR, M1, M2, MonoAQUAL, T0, T_END, r_O2, V0_ORB)  # noqa: E402,F401

# ------------------------------------------------------------------ compiled kernels
_SRC = HERE / "x12_kern.c"
_LIB = HERE / "work" / "libx12kern.so"


def _load():
    _LIB.parent.mkdir(exist_ok=True)
    if (not _LIB.exists()) or _LIB.stat().st_mtime < _SRC.stat().st_mtime:
        tmp = _LIB.with_suffix(f".{os.getpid()}.so")
        subprocess.check_call(["cc", "-O3", "-ffp-contract=off", "-shared", "-fPIC", "-o", str(tmp), str(_SRC), "-lm"])
        os.replace(tmp, _LIB)
    lib = ctypes.CDLL(str(_LIB))
    P = ctypes.POINTER(ctypes.c_double)
    I, L, D = ctypes.c_int, ctypes.c_long, ctypes.c_double
    lib.residual.argtypes = [P, I, I, I, P, P, P, I, D, P, P]
    lib.hessvec.argtypes = [P, P, I, I, I, P, P, P, D, P, P, P]
    lib.tridiag.argtypes = [P, L, I, P, P, P, P]
    lib.tsc_deposit.argtypes = [L, P, P, P, P, P, P, P, I, I, I, I, I, I, P]
    lib.tsc_grad.argtypes = [L, P, P, P, P, P, P, I, I, I, I, I, I, P, P, P, P]
    lib.jacobian.argtypes = [P, P, P, I, I, I, P, P, P, I, I, I, I, I, I, I, I, I, P, P]
    lib.omega2_max.argtypes = [P, P, I, I, I, P, P, P, I, I, I, D, D]
    lib.omega2_max.restype = D
    return lib


LIB = _load()
NULL = ctypes.POINTER(ctypes.c_double)()


def ptr(a):
    assert a.dtype == np.float64 and a.flags["C_CONTIGUOUS"]
    return a.ctypes.data_as(ctypes.POINTER(ctypes.c_double))


# ------------------------------------------------------------------ axes
def build_axis(lo, hi, h, B_out, q, mirror):
    """Fine nodes lo..hi step h; beyond, spacings h q, h q^2, ... until |coordinate| >= B_out. A mirrored axis has lo = 0
    and no extension below."""
    n = int(round((hi - lo) / h))
    core = list(lo + np.arange(n + 1) * h)
    up, d = [core[-1]], h
    while up[-1] < B_out:
        d *= q
        up.append(up[-1] + d)
    if mirror:
        assert lo == 0.0
        return np.array(core + up[1:], dtype=float)
    dn, d = [core[0]], h
    while dn[-1] > -B_out:
        d *= q
        dn.append(dn[-1] - d)
    return np.array(dn[:0:-1] + core + up[1:], dtype=float)


class Grid3:
    """Tensor-product node grid. Unknown nodes: all but the Dirichlet outer faces (a mirrored axis keeps index 0)."""

    def __init__(self, X, Y, Z, mir, fine):
        self.X, self.Y, self.Z = (np.ascontiguousarray(a, dtype=float) for a in (X, Y, Z))
        self.mir = tuple(int(m) for m in mir)
        self.NX, self.NY, self.NZ = len(X), len(Y), len(Z)
        self.shape = (self.NX, self.NY, self.NZ)
        self.dx, self.dy, self.dz = (np.ascontiguousarray(np.diff(a)) for a in (self.X, self.Y, self.Z))
        self.fine = fine                                     # dict: lo/hi per axis, h
        self.h = fine["h"]
        self.hmin = min(self.dx.min(), self.dy.min(), self.dz.min())
        self.lo = [0 if m else 1 for m in self.mir]
        self.sl = tuple(slice(self.lo[a], n - 1) for a, n in enumerate(self.shape))
        self.ishape = tuple(n - 1 - self.lo[a] for a, n in enumerate(self.shape))
        self.nint = int(np.prod(self.ishape))
        # dual lengths (lumped 1-D masses) on all nodes; mirror node 0 gets half its cell
        self.dual = []
        for ax, d in enumerate((self.dx, self.dy, self.dz)):
            m = np.zeros(len(d) + 1)
            m[:-1] += 0.5 * d
            m[1:] += 0.5 * d
            self.dual.append(m)
        self.Vn = (self.dual[0][:, None, None] * self.dual[1][None, :, None] * self.dual[2][None, None, :])
        self._fd_setup()
        self._R = np.empty(self.shape)
        self._xm = ctypes.c_double(0.0)

    # ---------------- kernels
    def residual(self, u, kind, a0=0.0, out=None, want_xmax=False):
        """R(u) = dE/du on all nodes. kind: 0 Poisson (c = 1), 1 mu, 2 1 - mu, 3 nu."""
        u = np.ascontiguousarray(u)
        out = np.empty(self.shape) if out is None else out
        LIB.residual(ptr(u), self.NX, self.NY, self.NZ, ptr(self.dx), ptr(self.dy), ptr(self.dz), kind, float(a0),
                     ptr(out), ctypes.byref(self._xm))
        return (out, self._xm.value) if want_xmax else out

    def interior(self, full):
        return full[self.sl]

    def full(self, interior, bdy_full):
        u = bdy_full.copy()
        u[self.sl] = np.asarray(interior).reshape(self.ishape)
        return u

    def bdy_only(self, full):
        b = full.copy()
        b[self.sl] = 0.0
        return b

    # ---------------- fast diagonalisation of the separable 7-point operator
    def _fd_setup(self):
        from scipy.linalg import eigh_tridiagonal
        self._fd = []
        for ax, d in enumerate((self.dx, self.dy, self.dz)):
            n = len(d) + 1
            Ld = np.zeros(n)
            Le = np.zeros(n - 1)
            Ld[:-1] += 1.0 / d
            Ld[1:] += 1.0 / d
            Le[:] = -1.0 / d
            Md = self.dual[ax].copy()
            s = slice(self.lo[ax], n - 1)
            Ld, Md = Ld[s], Md[s]
            Le = Le[self.lo[ax]:n - 2]
            self._fd.append((Ld, Le, Md))
        # x and y: symmetric scaled eigenproblems (Md diagonal)
        self._S, self._lam = [], []
        for ax in (0, 1):
            Ld, Le, Md = self._fd[ax]
            sc = 1.0 / np.sqrt(Md)
            w, V = eigh_tridiagonal(Ld * sc * sc, Le * sc[:-1] * sc[1:])
            S = sc[:, None] * V
            self._S.append((np.ascontiguousarray(S), np.ascontiguousarray(S.T)))
            self._lam.append(w)
        self._lamxy = np.ascontiguousarray((self._lam[0][:, None] + self._lam[1][None, :]).ravel())
        Ld, Le, Md = self._fd[2]
        self._zLd, self._zLe, self._zMd = (np.ascontiguousarray(a) for a in (Ld, Le, Md))
        # the 1-D factors give A = Lx(x)My(x)Mz + Mx(x)Ly(x)Mz + Mx(x)My(x)Lz; Mx, My scale the transformed problem
        Sx, SxT = self._S[0]
        Sy, SyT = self._S[1]
        self._SxT, self._Sx, self._SyT, self._Sy = SxT, Sx, SyT, Sy

    def solve_int(self, rhs_int):
        """Solve A u = rhs exactly on the unknowns (A = the interior block of R_1 with Dirichlet outer faces)."""
        nx, ny, nz = self.ishape
        F = np.ascontiguousarray(rhs_int, dtype=float).reshape(nx, ny * nz)
        with np.errstate(all="ignore"):                     # spurious FP flags from the BLAS matmul on this platform
            t = self._SxT @ F
            t = np.matmul(self._SyT, t.reshape(nx, ny, nz))
        t = np.ascontiguousarray(t)
        LIB.tridiag(ptr(t), nx * ny, nz, ptr(self._lamxy), ptr(self._zLd), ptr(self._zLe), ptr(self._zMd))
        with np.errstate(all="ignore"):
            t = np.matmul(self._Sy, t)
            u = self._Sx @ t.reshape(nx, ny * nz)
        return u.ravel()

    # ---------------- particles
    def deposit(self, px, py, pz, m, out=None):
        out = np.empty(self.shape) if out is None else out
        LIB.tsc_deposit(px.size, ptr(px), ptr(py), ptr(pz), ptr(m), ptr(self.X), ptr(self.Y), ptr(self.Z),
                        self.NX, self.NY, self.NZ, *self.mir, ptr(out))
        return out

    def grad_at(self, px, py, pz, f, gx, gy, gz):
        f = np.ascontiguousarray(f)
        LIB.tsc_grad(px.size, ptr(px), ptr(py), ptr(pz), ptr(self.X), ptr(self.Y), ptr(self.Z), self.NX, self.NY,
                     self.NZ, *self.mir, ptr(f), ptr(gx), ptr(gy), ptr(gz))

    def deconvolve(self, m_int):
        """Particle masses (one per unknown node) whose TSC deposit equals the nodal masses on the unknown nodes."""
        from scipy.linalg import solve_banded
        X = np.asarray(m_int, dtype=float).reshape(self.ishape).copy()
        for ax in range(3):
            n = self.ishape[ax]
            ab = np.zeros((3, n))
            ab[0, 1:] = 0.125
            ab[1, :] = 0.75
            ab[2, :-1] = 0.125
            if self.mir[ax]:
                ab[2, 0] = 0.25                           # node 1 receives 1/8 + 1/8 (folded) from the plane particle
            Xm = np.moveaxis(X, ax, 0)
            sh = Xm.shape
            sol = solve_banded((1, 1), ab, Xm.reshape(n, -1))
            X = np.moveaxis(sol.reshape(sh), 0, ax)
        return np.ascontiguousarray(X).ravel()

    def omega_max(self, Xi_full, rho_abs, a0):
        return math.sqrt(LIB.omega2_max(ptr(np.ascontiguousarray(Xi_full)), ptr(np.ascontiguousarray(rho_abs)), self.NX,
                                        self.NY, self.NZ, ptr(self.X), ptr(self.Y), ptr(self.Z), *self.mir, float(a0),
                                        float(K)))

    def hessvec(self, u, v, a0, diag=False):
        out = np.empty(self.shape)
        if diag:
            dn, dd = np.empty(self.shape), np.empty(self.shape)
            LIB.hessvec(ptr(u), NULL, self.NX, self.NY, self.NZ, ptr(self.dx), ptr(self.dy), ptr(self.dz), float(a0),
                        ptr(out), ptr(dn), ptr(dd))
            return dn / np.maximum(dd, 1e-300)
        LIB.hessvec(ptr(u), ptr(v), self.NX, self.NY, self.NZ, ptr(self.dx), ptr(self.dy), ptr(self.dz), float(a0),
                    ptr(out), NULL, NULL)
        return out


# ------------------------------------------------------------------ solvers
def pcg(matvec, b, prec, rtol, maxit=3000):
    with np.errstate(all="ignore"):
        x = np.zeros_like(b)
        r = b.copy()
        zv = prec(r)
        p = zv.copy()
        rz = float(r @ zv)
        nb = float(np.linalg.norm(b))
        for it in range(1, maxit + 1):
            Ap = matvec(p)
            alpha = rz / float(p @ Ap)
            x += alpha * p
            r -= alpha * Ap
            if np.linalg.norm(r) <= rtol * nb:
                return x, it
            zv = prec(r)
            rz_new = float(r @ zv)
            p = zv + (rz_new / rz) * p
            rz = rz_new
    return x, maxit


def solve_aqual(g, phib_full, Xi_bdy_full, a0, tol=1e-12, maxit=60, log=None, Xi_start=None):
    """Discrete AQUAL R_mu(Xi) = R_1(phi_b) on the unknowns, Dirichlet Xi_bdy (X8's Newton-PCG in 3D)."""
    f_b = g.interior(g.residual(phib_full, 0)).copy()
    scale = np.abs(f_b).max()
    if Xi_start is None:
        rhs = g.interior(g.residual(phib_full, 3, a0)) - g.interior(g.residual(g.bdy_only(Xi_bdy_full), 0))
        Xi = g.full(g.solve_int(rhs), Xi_bdy_full)
    else:
        Xi = Xi_start.copy()
    res = g.interior(g.residual(Xi, 1, a0)) - f_b
    hist, best, cgs = [], None, []
    zero = np.zeros(g.shape)
    for it in range(maxit):
        rel = float(np.abs(res).max() / scale)
        hist.append(rel)
        if log:
            log(f"      AQUAL it {it:3d}  max|res|/max|f| = {rel:.3e}")
        if best is None or rel < best[0]:
            best = (rel, Xi.copy())
        if rel <= tol or (it >= 8 and rel >= 0.5 * min(hist[-4:-1])):
            break
        Dn = g.interior(g.hessvec(Xi, None, a0, diag=True)).ravel()
        sD = 1.0 / np.sqrt(np.maximum(Dn, 1e-14))

        def matvec(v):
            return g.interior(g.hessvec(Xi, g.full(v, zero), a0)).ravel()

        def prec(r):
            return sD * g.solve_int(sD * r)

        eta = min(0.1, math.sqrt(rel)) * 0.1
        delta, ncg = pcg(matvec, -np.ascontiguousarray(res).ravel(), prec, eta)
        cgs.append(ncg)
        step = 1.0
        for _ in range(6):
            trial = g.full(g.interior(Xi).ravel() + step * delta, Xi_bdy_full)
            res2 = g.interior(g.residual(trial, 1, a0)) - f_b
            if np.abs(res2).max() / scale < rel or step < 0.05:
                break
            step *= 0.5
        Xi, res = trial, res2
    return best[1], {"iterations": len(hist), "rel_residual": best[0], "history_tail": hist[-5:], "cg_iterations": cgs}


def initial_state(g, a0, phib_full, Xi_bdy_full, gamma_L, log=None, max_outer=12):
    """Discrete v3s switched static equilibrium (X8 A1(e)) and the nodal khronon masses m = -R_{1-mu}(Xi)/K."""
    Xi, info = solve_aqual(g, phib_full, Xi_bdy_full, a0, log=log)
    outer = []
    if gamma_L > 0:
        for _ in range(max_outer):
            m = -g.interior(g.residual(Xi, 2, a0)) / K
            rho_p = np.zeros(g.shape)
            rho_p[g.sl] = np.maximum(m / g.Vn[g.sl], 0.0)
            Xi_new, info = solve_aqual(g, phib_full + gamma_L * rho_p, Xi_bdy_full, a0, Xi_start=Xi)
            dxi = float(np.abs(Xi_new - Xi).max())
            outer.append(dxi)
            Xi = Xi_new
            if dxi <= 1e-9 * a0 * g.hmin:
                break
    info["stiffness_outer"] = outer
    m = -g.interior(g.residual(Xi, 2, a0)) / K
    rho_abs = np.zeros(g.shape)
    rho_abs[g.sl] = np.abs(m) / g.Vn[g.sl]
    info["omega_max"] = g.omega_max(Xi, rho_abs, a0)
    return Xi, np.ascontiguousarray(m), info


class HoldSolver:
    """X8's Anderson-accelerated fixed point Xi_int <- A^-1 [-K m + R_mu(Xi) - R_1(bdy)], warm-started."""

    def __init__(self, g, a0, tol=1e-7, depth=5, maxit=300):
        self.g, self.a0, self.tol, self.depth, self.maxit = g, a0, tol, depth, maxit
        self.Xi_int = None
        self.Xi_prev = None
        self.last_iters = 0
        self.last_xmax = 0.0
        self.converged = True
        self._aa = None
        self._full = None

    def solve(self, Km_int, Xi_bdy_full, bterm):
        g, a0 = self.g, self.a0
        Kmv = np.asarray(Km_int).ravel()
        thr = self.tol * a0 * g.hmin
        if self._full is None:
            self._full = Xi_bdy_full.copy()
            self._res = np.empty(g.shape)
        full = self._full
        full[...] = Xi_bdy_full

        def T(xint):
            full[g.sl] = xint.reshape(g.ishape)
            res, xmax = g.residual(full, 1, a0, out=self._res, want_xmax=True)
            rhs = g.interior(res).ravel() - Kmv - bterm
            return g.solve_int(rhs), xmax

        n, mdep = g.nint, self.depth
        if self._aa is None:
            self._aa = (np.empty((mdep + 1, n)), np.empty((mdep + 1, n)))
        Xb, Gb = self._aa
        if self.Xi_int is None:
            x = T(np.zeros(n))[0]
        elif self.Xi_prev is None:
            x = self.Xi_int.copy()
        else:
            x = 2.0 * self.Xi_int - self.Xi_prev
        cnt = 0
        for it in range(1, self.maxit + 1):
            Tx, xmax = T(x)
            gres = Tx - x
            if np.abs(gres).max() <= thr:
                self.Xi_prev = self.Xi_int
                self.Xi_int, self.last_iters, self.last_xmax, self.converged = Tx, it, xmax, True
                return Tx
            slot = cnt % (mdep + 1)
            Xb[slot] = x
            Gb[slot] = gres
            cnt += 1
            k = min(cnt, mdep + 1)
            xnew = Tx
            if k >= 2:
                order = [(cnt - k + j) % (mdep + 1) for j in range(k)]
                with np.errstate(all="ignore"):
                    dG = [Gb[order[j + 1]] - Gb[order[j]] for j in range(k - 1)]
                    Mm = np.array([[float(dG[a_] @ dG[b_]) for b_ in range(k - 1)] for a_ in range(k - 1)])
                    rv = np.array([float(dG[a_] @ gres) for a_ in range(k - 1)])
                    sc = np.sqrt(np.maximum(np.diag(Mm), 1e-300))
                    gam, *_ = np.linalg.lstsq(Mm / np.outer(sc, sc), rv / sc, rcond=1e-12)
                    gam = gam / sc
                    if np.all(np.isfinite(gam)):
                        xnew = x + gres
                        for j in range(k - 1):
                            xnew -= gam[j] * (Xb[order[j + 1]] - Xb[order[j]] + dG[j])
                        if not np.all(np.isfinite(xnew)):
                            xnew, cnt = Tx, 0
                    else:
                        cnt = 0
                del dG
            x = xnew
        self.Xi_prev = self.Xi_int
        self.Xi_int, self.last_iters, self.last_xmax, self.converged = Tx, self.maxit, xmax, False
        return Tx


# ------------------------------------------------------------------ the simulation
class Sim3:
    """Self-consistent khronon fluid in prescribed baryon potentials (3D). baryons(t) -> list of (M, (x, y, z));
    bc(t, phib_full) -> (Xi_bdy_full, phit_bdy_full)."""

    def __init__(self, g, a0, gamma_L, baryons, bc, Xi_eq_full, m_nodes_int, t_start, tol=1e-7, masses=None):
        self.g, self.a0, self.gL = g, a0, gamma_L
        self.baryons, self.bc = baryons, bc
        qx, qy, qz = (a[s] for a, s in zip((g.X, g.Y, g.Z), g.sl))
        self.qx, self.qy, self.qz = (np.ascontiguousarray(a) for a in (qx, qy, qz))
        QX, QY, QZ = np.meshgrid(self.qx, self.qy, self.qz, indexing="ij")
        self.q = [np.ascontiguousarray(a.ravel()) for a in (QX, QY, QZ)]
        del QX, QY, QZ
        self.X = [a.copy() for a in self.q]
        self.V = [np.zeros_like(a) for a in self.q]
        self.A = [np.zeros_like(a) for a in self.q]
        self.m = g.deconvolve(m_nodes_int) if masses is None else np.ascontiguousarray(masses)
        self.t = t_start
        self.hold = HoldSolver(g, a0, tol=tol)
        self.hold.Xi_int = np.ascontiguousarray(Xi_eq_full[g.sl]).ravel().copy()
        self.flags = {"F1": None, "F2": None, "F3": None}
        self.ncalls = 0
        self.iters_total = 0
        self.xmax_seen = 0.0
        self.lost_mass = 0.0
        self._mdep = np.empty(g.shape)
        self._tot = np.empty(g.shape)
        self._rho_abs = np.zeros(g.shape)
        self.Xi_full = Xi_eq_full.copy()
        self._bcache = (None, None)

    def phib(self, t):
        """Plummer potentials of the baryons on all nodes."""
        g = self.g
        out = np.zeros(g.shape)
        for M, (xc, yc, zc) in self.baryons(t):
            dx2 = ((g.X - xc) ** 2)[:, None, None]
            dy2 = ((g.Y - yc) ** 2)[None, :, None]
            dz2 = ((g.Z - zc) ** 2)[None, None, :]
            out -= G * M / np.sqrt(dx2 + dy2 + dz2 + EPS ** 2)
        return out

    def accel(self, t):
        g = self.g
        mdep = g.deposit(self.X[0], self.X[1], self.X[2], self.m, out=self._mdep)
        tot_abs = float(np.abs(mdep).sum())
        self.lost_mass = tot_abs - float(np.abs(mdep[g.sl]).sum())
        Km = K * np.ascontiguousarray(mdep[g.sl]).ravel()
        phib = self.phib(t)
        Xi_bdy, phit_bdy = self.bc(t, phib)
        if self._bcache[0] is not Xi_bdy:                       # fixed Dirichlet data: computed once
            self._bcache = (Xi_bdy, g.interior(g.residual(g.bdy_only(Xi_bdy), 0)).ravel().copy())
        bterm = self._bcache[1]
        Xi_int = self.hold.solve(Km, Xi_bdy, bterm)
        self.ncalls += 1
        self.iters_total += self.hold.last_iters
        self.xmax_seen = max(self.xmax_seen, self.hold.last_xmax)
        if not self.hold.converged and self.flags["F1"] is None:
            self.flags["F1"] = self.t
        if self.hold.last_xmax > 50 and self.flags["F2"] is None:
            self.flags["F2"] = self.t
        pb = g.bdy_only(phit_bdy)
        phit_int = g.solve_int(-Km - g.interior(g.residual(pb, 0)).ravel())
        tot = self._tot
        tot[...] = Xi_bdy - phit_bdy
        tot[g.sl] = (Xi_int - phit_int).reshape(g.ishape)        # chi = Xi - phi_tau
        tot -= phib                                              # zeta = chi - phi_b
        self.Xi_full = g.full(Xi_int, Xi_bdy)
        rho = mdep[g.sl] / g.Vn[g.sl]
        self._rho_abs[g.sl] = np.abs(rho)
        if self.gL > 0:
            tot[g.sl] -= self.gL * np.maximum(rho, 0.0)
        g.grad_at(self.X[0], self.X[1], self.X[2], tot, *self.A)
        return self.A

    def step(self, dt):
        for a in range(3):
            self.V[a] += 0.5 * dt * self.A[a]
            self.X[a] += dt * self.V[a]
        g = self.g
        out = np.zeros(self.X[0].size, bool)
        for a, ax in enumerate((g.X, g.Y, g.Z)):
            lo = -ax[-1] if g.mir[a] else ax[0]
            out |= (self.X[a] < lo) | (self.X[a] > ax[-1])
        if out.any():
            if self.flags["F3"] is None:
                self.flags["F3"] = self.t + dt
            for a, ax in enumerate((g.X, g.Y, g.Z)):
                lo = -ax[-1] if g.mir[a] else ax[0]
                np.clip(self.X[a], lo, ax[-1], out=self.X[a])
        self.t += dt
        self.accel(self.t)
        for a in range(3):
            self.V[a] += 0.5 * dt * self.A[a]

    def omega_max(self):
        return self.g.omega_max(self.Xi_full, self._rho_abs, self.a0)

    def jacobian(self, block, want_F=False):
        """J on a block ((i0, i1), (j0, j1), (k0, k1)) of the label lattice."""
        g = self.g
        (i0, i1), (j0, j1), (k0, k1) = block
        n = (i1 - i0) * (j1 - j0) * (k1 - k0)
        J = np.empty(n)
        F = np.empty(9 * n) if want_F else None
        LX, LY, LZ = g.ishape
        LIB.jacobian(ptr(self.X[0]), ptr(self.X[1]), ptr(self.X[2]), LX, LY, LZ, ptr(self.qx), ptr(self.qy), ptr(self.qz),
                     *g.mir, i0, i1, j0, j1, k0, k1, ptr(J), ptr(F) if want_F else NULL)
        return (J, F.reshape(n, 3, 3)) if want_F else J

    def defgrad(self, li, lj, lk):
        """Deformation gradient of one label (lattice indices)."""
        _, F = self.jacobian(((li, li + 1), (lj, lj + 1), (lk, lk + 1)), want_F=True)
        return F[0]


def plummer_phi3(g, masses):
    out = np.zeros(g.shape)
    for M, (xc, yc, zc) in masses:
        dx2 = ((g.X - xc) ** 2)[:, None, None]
        dy2 = ((g.Y - yc) ** 2)[None, :, None]
        dz2 = ((g.Z - zc) ** 2)[None, None, :]
        out -= G * M / np.sqrt(dx2 + dy2 + dz2 + EPS ** 2)
    return out


def mono_bdy(g, M, a0, centre, mono=None):
    """Spherical AQUAL potential of mass M about centre on the Dirichlet nodes (zero elsewhere)."""
    mono = MonoAQUAL(M, a0) if mono is None else mono
    out = np.zeros(g.shape)
    bm = np.ones(g.shape, bool)
    bm[g.sl] = False
    xc, yc, zc = centre
    r = np.sqrt(((g.X - xc) ** 2)[:, None, None] + ((g.Y - yc) ** 2)[None, :, None] + ((g.Z - zc) ** 2)[None, None, :])
    out[bm] = mono(r[bm])
    return out


def wall():
    import time
    return time.time()
