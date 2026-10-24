#!/usr/bin/env python3
"""X8_soft_side_caustics core: an axisymmetric (R, z) self-consistent khronon-fluid solver for v3s.

FROZEN_CRITERIA.md §1, §3 as amended by AMENDMENT A1 (PRE-RESULT): the discretisation is variational. Q1 (bilinear)
finite elements on the (R, z) tensor grid with the axisymmetric volume element 2 pi R dR dz and 2x2 Gauss quadrature; the
CIC weights are exactly the Q1 basis functions; the particle acceleration is the gradient of the bilinear interpolant of the
nodal potential (energy-conserving particle-in-cell). The discrete particle system then derives from a discrete potential
energy U(x_p) (envelope theorem), and the hold operator is bounded by the Laplacian at every Gauss point.

Units: kpc, Gyr, Msun.  Weak-field PN system with mu_K -> 0, no dust (weak forms, N_n the Q1 basis,
R_c(u)_n = int c grad u . grad N_n dV):
    hold law   R_{1-mu}(Xi) = -K m          (Xi here is Xi~ = Xi + gamma_L rho_+ ; m = deposited khronon masses)
    Poisson    R_1(phi_tau) = -K m
    khronon    a_p = grad zeta_h(x_p) - gamma_L grad (rho_+)_h(x_p),   zeta = chi - phi_b,  chi = Xi - phi_tau
"""
import math
import time

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
from scipy.optimize import brentq

G = 4.498502151469554e-06                      # kpc^3 / (Msun Gyr^2)  (the review's value)
K = 4.0 * math.pi * G
MS2_TO_KPCGYR2 = (3.15576e16) ** 2 / 3.0856775814913673e19
A0 = {"canonical": 9.3603e-11 * MS2_TO_KPCGYR2, "alt": 1.1312e-10 * MS2_TO_KPCGYR2}
LSTAR = {"canonical": 21.682e-3, "alt": 22.849e-3}  # kpc, v3s floors (X3 D4)
KMS = 1.0227121650537077                      # kpc/Gyr per km/s
M1, M2 = 6e10, 1e11                           # MW, M31 baryons (review / H4 S1)
EPS = 20.0                                    # Plummer softening, kpc (review)
R0_ORB, V0_ORB, T0 = 780.0, -110.0 * KMS, 13.8


# ================================================================ orbits (the review's formulas)
def _f_eta(eta):
    return math.sin(eta) * (eta - math.sin(eta)) / (1 - math.cos(eta)) ** 2


ETA0 = brentq(lambda e: _f_eta(e) - V0_ORB * T0 / R0_ORB, math.pi + 1e-9, 2 * math.pi - 1e-6)
A_K = R0_ORB / (1 - math.cos(ETA0))
GMK = A_K ** 3 * ((ETA0 - math.sin(ETA0)) / T0) ** 2
TK = math.sqrt(A_K ** 3 / GMK)


def r_O1(t):
    eta = brentq(lambda e: TK * (e - math.sin(e)) - t, 0.0, 2 * math.pi)
    return A_K * (1 - math.cos(eta))


def rdot_O1(t):
    eta = brentq(lambda e: TK * (e - math.sin(e)) - t, 0.0, 2 * math.pi)
    return math.sqrt(GMK / A_K) * math.sin(eta) / (1 - math.cos(eta))


def r_O2(t):
    return R0_ORB + (-V0_ORB) * (T0 - t)


def rdot_O2(t):
    return V0_ORB


ORBITS = {"O1": (r_O1, rdot_O1), "O2": (r_O2, rdot_O2)}
T_END = {"O1": brentq(lambda t: r_O1(t) - 300.0, T0, TK * 2 * math.pi - 1e-6), "O2": T0 + (R0_ORB - 300.0) / (-V0_ORB)}


def pair_positions(r):
    return -M2 / (M1 + M2) * r, M1 / (M1 + M2) * r


# ================================================================ grid axes
def build_axis_R(R_f, h, B_out, q):
    n = int(round(R_f / h))
    xs = list(np.arange(n + 1) * h)
    d = h
    while xs[-1] < B_out:
        d *= q
        xs.append(xs[-1] + d)
    return np.array(xs, dtype=float)


def build_axis_z(z_lo, z_hi, h, B_out, q):
    n = int(round((z_hi - z_lo) / h))
    core = list(z_lo + np.arange(n + 1) * h)
    up, d = [core[-1]], h
    while up[-1] < B_out:
        d *= q
        up.append(up[-1] + d)
    dn, d = [core[0]], h
    while dn[-1] > -B_out:
        d *= q
        dn.append(dn[-1] - d)
    return np.array(dn[:0:-1] + core + up[1:], dtype=float)


_GP = (0.5 - 0.5 / math.sqrt(3.0), 0.5 + 0.5 / math.sqrt(3.0))
GAUSS = [(xi, eta) for eta in _GP for xi in _GP]           # xi along R, eta along z (cell-local, in [0, 1])
LOCAL = [(0, 0), (1, 0), (0, 1), (1, 1)]                   # (sR, sz): node offsets of the 4 cell corners


class Grid:
    """Q1 FEM on the (R, z) tensor grid. Nodes (NZ, NR); interior unknowns rows 1..NZ-2, columns 0..NR-2 (Dirichlet on
    R = R_out and z = z_min, z_max; natural condition on the axis)."""

    def __init__(self, R, z, fine=None):
        self.R, self.z = R, z
        self.NR, self.NZ = len(R), len(z)
        NR, NZ = self.NR, self.NZ
        self.fine = fine
        self.dR = np.diff(R)
        self.dz = np.diff(z)
        cdR, cdz = self.dR[None, :], self.dz[:, None]
        self.hmin = min(self.dR.min(), self.dz.min())
        self.nint = (NZ - 2) * (NR - 1)
        # Gauss weights and basis gradients, per Gauss point: arrays (NZ-1, NR-1)
        self.w, self.dN = [], []
        ones = np.ones((NZ - 1, NR - 1))
        for xi, eta in GAUSS:
            Rg = R[:-1][None, :] + xi * cdR
            self.w.append(0.25 * cdR * cdz * 2.0 * math.pi * Rg * ones)
            dn = []
            for sR, sz in LOCAL:
                fR = (eta if sz else 1 - eta) * (1.0 if sR else -1.0) / cdR * ones
                fz = (xi if sR else 1 - xi) * (1.0 if sz else -1.0) / cdz * ones
                dn.append((fR, fz))
            self.dN.append(dn)
        # lumped nodal volumes V_n = int N_n dV
        Vn = np.zeros((NZ, NR))
        for g, (xi, eta) in enumerate(GAUSS):
            for a, (sR, sz) in enumerate(LOCAL):
                Na = (xi if sR else 1 - xi) * (eta if sz else 1 - eta)
                self._acc(Vn, a, self.w[g] * Na)
        self.Vn = Vn
        self.V = Vn[1:-1, :-1]
        # interior index of each cell corner
        idx = -np.ones((NZ, NR), dtype=np.int64)
        idx[1:-1, :-1] = np.arange(self.nint).reshape(NZ - 2, NR - 1)
        self._cidx = [idx[:-1, :-1], idx[:-1, 1:], idx[1:, :-1], idx[1:, 1:]]
        self._lu = None
        # separable 1-D factors for the buffered kernel (no per-call temporaries)
        self.inv_dR = (1.0 / self.dR)[None, :]
        self.inv_dz = (1.0 / self.dz)[:, None]
        self.wR1 = [(0.5 * self.dR * 2.0 * math.pi * (R[:-1] + xi * self.dR))[None, :] for xi, eta in GAUSS]
        self.wZ1 = (0.5 * self.dz)[:, None]
        self.fR1 = [[((eta if sz else 1 - eta) * (1.0 if sR else -1.0) / self.dR)[None, :] for sR, sz in LOCAL]
                    for xi, eta in GAUSS]
        self.fz1 = [[((xi if sR else 1 - xi) * (1.0 if sz else -1.0) / self.dz)[:, None] for sR, sz in LOCAL]
                    for xi, eta in GAUSS]
        self._B = None

    def kernel(self, u, kind="one", a0=None, C=None, want_xmax=False):
        """Buffered weak-form residual int c grad u_h . grad N_n dV (all nodes, new (NZ, NR) array).
        kind: 'one' (c = 1), 'mu' (mu(x)), '1-mu' (1 - mu(x)), 'nu' (nu(|grad u|/a0)), 'tensor' (C = (cRR, cRz, czz))."""
        if self._B is None:
            sh = (self.NZ - 1, self.NR - 1)
            self._B = {k: np.empty(sh) for k in ("dRa", "dRb", "dza", "dzb", "gR", "gz", "t1", "t2", "c",
                                                 "a0", "a1", "a2", "a3")}
        B = self._B
        np.subtract(u[:-1, 1:], u[:-1, :-1], out=B["dRa"])
        B["dRa"] *= self.inv_dR
        np.subtract(u[1:, 1:], u[1:, :-1], out=B["dRb"])
        B["dRb"] *= self.inv_dR
        np.subtract(u[1:, :-1], u[:-1, :-1], out=B["dza"])
        B["dza"] *= self.inv_dz
        np.subtract(u[1:, 1:], u[:-1, 1:], out=B["dzb"])
        B["dzb"] *= self.inv_dz
        acc = [B["a0"], B["a1"], B["a2"], B["a3"]]
        for A_ in acc:
            A_.fill(0.0)
        gR, gz, t1, t2, c = B["gR"], B["gz"], B["t1"], B["t2"], B["c"]
        xmax = 0.0
        for g, (xi, eta) in enumerate(GAUSS):
            np.multiply(B["dRa"], 1 - eta, out=gR)
            np.multiply(B["dRb"], eta, out=t1)
            gR += t1
            np.multiply(B["dza"], 1 - xi, out=gz)
            np.multiply(B["dzb"], xi, out=t1)
            gz += t1
            if kind in ("mu", "1-mu", "nu"):
                np.hypot(gR, gz, out=c)
                c *= 1.0 / a0
                if want_xmax:
                    xmax = max(xmax, float(c.max()))
                if kind == "mu":
                    np.add(c, 1.0, out=t1)
                    np.divide(c, t1, out=c)
                elif kind == "1-mu":
                    np.add(c, 1.0, out=t1)
                    np.reciprocal(t1, out=c)
                else:
                    np.maximum(c, 1e-300, out=c)
                    np.divide(4.0, c, out=c)
                    c += 1.0
                    np.sqrt(c, out=c)
                    c += 1.0
                    c *= 0.5
                gR *= c
                gz *= c
            elif kind == "tensor":
                cRR, cRz, czz = C[0][g], C[1][g], C[2][g]
                np.multiply(cRR, gR, out=t1)
                np.multiply(cRz, gz, out=t2)
                t1 += t2
                np.multiply(cRz, gR, out=t2)
                np.multiply(czz, gz, out=c)
                c += t2
                gR[...] = t1
                gz[...] = c
            gR *= self.wR1[g]
            gR *= self.wZ1
            gz *= self.wR1[g]
            gz *= self.wZ1
            for a in range(4):
                np.multiply(gR, self.fR1[g][a], out=t1)
                acc[a] += t1
                np.multiply(gz, self.fz1[g][a], out=t1)
                acc[a] += t1
        out = np.zeros((self.NZ, self.NR))
        for a in range(4):
            self._acc(out, a, acc[a])
        return (out, xmax) if want_xmax else out

    @staticmethod
    def _acc(out, a, val):
        if a == 0:
            out[:-1, :-1] += val
        elif a == 1:
            out[:-1, 1:] += val
        elif a == 2:
            out[1:, :-1] += val
        else:
            out[1:, 1:] += val

    # ---------------------------------------------------------------- operators
    def grad_gauss(self, u):
        u00, u10, u01, u11 = u[:-1, :-1], u[:-1, 1:], u[1:, :-1], u[1:, 1:]
        cdR, cdz = self.dR[None, :], self.dz[:, None]
        dRa, dRb = (u10 - u00) / cdR, (u11 - u01) / cdR
        dza, dzb = (u01 - u00) / cdz, (u11 - u10) / cdz
        return [((1 - eta) * dRa + eta * dRb, (1 - xi) * dza + xi * dzb) for xi, eta in GAUSS]

    def residual(self, u, coef=None, grads=None):
        """R_c(u)_n = int c grad u_h . grad N_n dV on all nodes (NZ, NR); coef: None (=1) or list of 4 Gauss arrays."""
        if grads is None:
            grads = self.grad_gauss(u)
        acc = [np.zeros((self.NZ - 1, self.NR - 1)) for _ in range(4)]
        for g in range(4):
            gR, gz = grads[g]
            c = self.w[g] if coef is None else coef[g] * self.w[g]
            qR, qz = c * gR, c * gz
            for a in range(4):
                fR, fz = self.dN[g][a]
                acc[a] += qR * fR + qz * fz
        out = np.zeros((self.NZ, self.NR))
        for a in range(4):
            self._acc(out, a, acc[a])
        return out

    def matrix(self, cRR=None, cRz=None, czz=None):
        """Interior stiffness matrix of int grad N_a . C grad N_b dV, C per Gauss point (None -> identity). SPD."""
        rows, cols, vals = [], [], []
        for a in range(4):
            ia = self._cidx[a]
            for b in range(4):
                ib = self._cidx[b]
                mask = (ia >= 0) & (ib >= 0)
                v = np.zeros_like(self.w[0])
                for g in range(4):
                    faR, faz = self.dN[g][a]
                    fbR, fbz = self.dN[g][b]
                    if cRR is None:
                        v += self.w[g] * (faR * fbR + faz * fbz)
                    else:
                        v += self.w[g] * (faR * (cRR[g] * fbR + cRz[g] * fbz) + faz * (cRz[g] * fbR + czz[g] * fbz))
                rows.append(ia[mask])
                cols.append(ib[mask])
                vals.append(v[mask])
        return sp.csc_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))),
                             shape=(self.nint, self.nint))

    def _fd_setup(self):
        """Fast diagonalisation of the interior Laplacian stiffness matrix, which is exactly separable under 2x2 Gauss:
        A = M_z (x) K_R + K_z (x) M_R. Generalised eigenproblem in z (dense), batched Thomas solves in R."""
        from scipy.linalg import eigh
        R, z = self.R, self.z
        NR, NZ = self.NR, self.NZ
        KR, MR = np.zeros((NR, NR)), np.zeros((NR, NR))
        for e in range(NR - 1):
            d = self.dR[e]
            kloc, mloc = 0.0, np.zeros((2, 2))
            for xi in _GP:
                wg = 0.5 * d * 2.0 * math.pi * (R[e] + xi * d)
                kloc += wg / d ** 2
                ph = (1 - xi, xi)
                for a in range(2):
                    for b in range(2):
                        mloc[a, b] += wg * ph[a] * ph[b]
            KR[e:e + 2, e:e + 2] += kloc * np.array([[1.0, -1.0], [-1.0, 1.0]])
            MR[e:e + 2, e:e + 2] += mloc
        KZ, MZ = np.zeros((NZ, NZ)), np.zeros((NZ, NZ))
        for e in range(NZ - 1):
            d = self.dz[e]
            KZ[e:e + 2, e:e + 2] += np.array([[1.0, -1.0], [-1.0, 1.0]]) / d
            MZ[e:e + 2, e:e + 2] += np.array([[2.0, 1.0], [1.0, 2.0]]) * d / 6.0
        KR, MR = KR[:-1, :-1], MR[:-1, :-1]
        KZ, MZ = KZ[1:-1, 1:-1], MZ[1:-1, 1:-1]
        lam, V = eigh(KZ, MZ)
        self._fd_V, self._fd_lam = V, lam
        d = np.diag(KR)[None, :] + lam[:, None] * np.diag(MR)[None, :]
        e = np.diag(KR, 1)[None, :] + lam[:, None] * np.diag(MR, 1)[None, :]
        nr = KR.shape[0]
        cp = np.zeros_like(d)
        den = np.zeros_like(d)
        den[:, 0] = d[:, 0]
        cp[:, 0] = e[:, 0] / den[:, 0]
        for i in range(1, nr):
            den[:, i] = d[:, i] - e[:, i - 1] * cp[:, i - 1]
            if i < nr - 1:
                cp[:, i] = e[:, i] / den[:, i]
        self._fd_e, self._fd_cp, self._fd_den = e, cp, den
        self._fd_ready = True

    def solve_int(self, rhs_int):
        """Solve A u_int = rhs exactly (A the interior Laplacian stiffness matrix), by fast diagonalisation."""
        if not getattr(self, "_fd_ready", False):
            self._fd_setup()
        nz, nr = self.NZ - 2, self.NR - 1
        F = np.ascontiguousarray(rhs_int).reshape(nz, nr)
        if getattr(self, "_fd_buf", None) is None:
            self._fd_buf = (np.empty((nz, nr)), np.empty(nz))
            self._fd_VT = np.ascontiguousarray(self._fd_V.T)
        y, tmp = self._fd_buf
        with np.errstate(all="ignore"):                    # spurious FP flags from the BLAS matmul on this platform
            np.matmul(self._fd_VT, F, out=y)
        e, cp, den = self._fd_e, self._fd_cp, self._fd_den
        y[:, 0] /= den[:, 0]
        for i in range(1, nr):
            np.multiply(e[:, i - 1], y[:, i - 1], out=tmp)
            y[:, i] -= tmp
            y[:, i] /= den[:, i]
        for i in range(nr - 2, -1, -1):
            np.multiply(cp[:, i], y[:, i + 1], out=tmp)
            y[:, i] -= tmp
        out = np.empty((nz, nr))
        with np.errstate(all="ignore"):
            np.matmul(self._fd_V, y, out=out)
        return out.ravel()

    def residual_tensor(self, u, C, grads=None):
        """int grad N_n . C grad u_h dV, C = (cRR, cRz, czz) lists over the 4 Gauss points."""
        if grads is None:
            grads = self.grad_gauss(u)
        cRR, cRz, czz = C
        acc = [np.zeros((self.NZ - 1, self.NR - 1)) for _ in range(4)]
        for g in range(4):
            gR, gz = grads[g]
            qR = self.w[g] * (cRR[g] * gR + cRz[g] * gz)
            qz = self.w[g] * (cRz[g] * gR + czz[g] * gz)
            for a in range(4):
                fR, fz = self.dN[g][a]
                acc[a] += qR * fR + qz * fz
        out = np.zeros((self.NZ, self.NR))
        for a in range(4):
            self._acc(out, a, acc[a])
        return out

    def lumped_nodal(self, cg):
        """(1/V_n) int N_n c dV for a Gauss-point field c (list of 4 arrays)."""
        out = np.zeros((self.NZ, self.NR))
        for g, (xi, eta) in enumerate(GAUSS):
            for a, (sR, sz) in enumerate(LOCAL):
                Na = (xi if sR else 1 - xi) * (eta if sz else 1 - eta)
                self._acc(out, a, self.w[g] * Na * cg[g])
        return out / self.Vn

    def interior(self, full):
        return full[1:-1, :-1]

    def bdy_only(self, full):
        b = full.copy()
        b[1:-1, :-1] = 0.0
        return b

    def full(self, interior, bdy_full):
        u = bdy_full.copy()
        u[1:-1, :-1] = np.asarray(interior).reshape(self.NZ - 2, self.NR - 1)
        return u

    def proj_grad(self, u):
        """Lumped L2 projection of the FEM gradient onto the nodes: G_n = (1/V_n) int N_n grad u_h dV (axis: G_R = 0)."""
        gq = self.grad_gauss(u)
        GR = np.zeros((self.NZ, self.NR))
        GZ = np.zeros((self.NZ, self.NR))
        for g, (xi, eta) in enumerate(GAUSS):
            gR, gz = gq[g]
            for a, (sR, sz) in enumerate(LOCAL):
                Na = (xi if sR else 1 - xi) * (eta if sz else 1 - eta) * self.w[g]
                self._acc(GR, a, Na * gR)
                self._acc(GZ, a, Na * gz)
        GR /= self.Vn
        GZ /= self.Vn
        GR[:, 0] = 0.0
        return GR, GZ

    def node_grad(self, u):
        """Approximate nodal gradient (diagnostics only, e.g. x at nodes for the time-step estimate)."""
        dz = np.gradient(u, self.z, axis=0, edge_order=1)
        dR = np.gradient(u, self.R, axis=1, edge_order=1)
        dR[:, 0] = 0.0
        return dR, dz

    # ---------------------------------------------------------------- particles
    def cic(self, Rp, zp):
        R, z = self.R, self.z
        i = np.clip(np.searchsorted(R, Rp, side="right") - 1, 0, self.NR - 2)
        j = np.clip(np.searchsorted(z, zp, side="right") - 1, 0, self.NZ - 2)
        wr = np.clip((Rp - R[i]) / (R[i + 1] - R[i]), 0.0, 1.0)
        wz = np.clip((zp - z[j]) / (z[j + 1] - z[j]), 0.0, 1.0)
        return i, j, wr, wz

    def deposit(self, w, m):
        i, j, wr, wz = w
        NR = self.NR
        k = j * NR + i
        n = self.NZ * NR
        out = np.bincount(k, m * (1 - wr) * (1 - wz), minlength=n)
        out += np.bincount(k + 1, m * wr * (1 - wz), minlength=n)
        out += np.bincount(k + NR, m * (1 - wr) * wz, minlength=n)
        out += np.bincount(k + NR + 1, m * wr * wz, minlength=n)
        return out.reshape(self.NZ, NR)

    def interp(self, w, f):
        i, j, wr, wz = w
        return ((1 - wr) * (1 - wz) * f[j, i] + wr * (1 - wz) * f[j, i + 1] + (1 - wr) * wz * f[j + 1, i]
                + wr * wz * f[j + 1, i + 1])

    def interp_grad(self, w, f):
        """Gradient of the bilinear interpolant of nodal f at the particles (energy-conserving force)."""
        i, j, wr, wz = w
        f00, f10, f01, f11 = f[j, i], f[j, i + 1], f[j + 1, i], f[j + 1, i + 1]
        gR = ((1 - wz) * (f10 - f00) + wz * (f11 - f01)) / self.dR[i]
        gz = ((1 - wr) * (f01 - f00) + wr * (f11 - f10)) / self.dz[j]
        return gR, gz

    # ---------------------------------------------------------------- quadratic B-spline (TSC) shapes in index space
    def b2(self, Rp, zp):
        """Quadratic B-spline weights in index space: for each particle the 3 R-nodes and 3 z-nodes, their weights and
        d/dR, d/dz of the weights. Node -1 (beyond the axis) is folded onto node 1 (mirror symmetry)."""
        R, z = self.R, self.z
        i = np.clip(np.searchsorted(R, Rp, side="right") - 1, 0, self.NR - 2)
        j = np.clip(np.searchsorted(z, zp, side="right") - 1, 0, self.NZ - 2)
        sR = i + np.clip((Rp - R[i]) / self.dR[i], 0.0, 1.0)
        sz = j + np.clip((zp - z[j]) / self.dz[j], 0.0, 1.0)
        out = []
        for s, cell, dcell, nmax in ((sR, i, self.dR, self.NR - 1), (sz, j, self.dz, self.NZ - 1)):
            n0 = np.floor(s + 0.5).astype(np.int64)
            u = s - n0
            W = [0.5 * (0.5 - u) ** 2, 0.75 - u * u, 0.5 * (0.5 + u) ** 2]
            D = [-(0.5 - u), -2.0 * u, (0.5 + u)]
            D = [d / dcell[cell] for d in D]
            N = [n0 - 1, n0, n0 + 1]
            out.append((N, W, D, nmax))
        (NRn, WR, DR, _), (NZn, WZ, DZ, _) = out
        NRn = [np.abs(n) for n in NRn]                     # fold node -1 onto node 1
        NRn = [np.minimum(n, self.NR - 1) for n in NRn]
        NZn = [np.clip(n, 0, self.NZ - 1) for n in NZn]
        return NRn, WR, DR, NZn, WZ, DZ

    def deposit_b2(self, sh, m):
        NRn, WR, _, NZn, WZ, _ = sh
        n = self.NZ * self.NR
        out = np.zeros(n)
        for a in range(3):
            for b in range(3):
                out += np.bincount(NZn[b] * self.NR + NRn[a], m * WR[a] * WZ[b], minlength=n)
        return out.reshape(self.NZ, self.NR)

    def interp_grad_b2(self, sh, f):
        """Gradient of sum_n f_n S_n(x) at the particles (energy-conserving force with the C1 quadratic B-spline)."""
        NRn, WR, DR, NZn, WZ, DZ = sh
        gR = np.zeros_like(WR[0])
        gz = np.zeros_like(WR[0])
        for a in range(3):
            for b in range(3):
                fv = f[NZn[b], NRn[a]]
                gR += fv * DR[a] * WZ[b]
                gz += fv * WR[a] * DZ[b]
        return gR, gz

    def b2_deconvolve(self, m_int):
        """Particle masses M (one per interior node) whose B2 deposit equals the nodal masses m on the interior nodes."""
        from scipy.linalg import solve_banded
        nz, nr = self.NZ - 2, self.NR - 1
        abz = np.zeros((3, nz))
        abz[0, 1:] = 0.125
        abz[1, :] = 0.75
        abz[2, :-1] = 0.125
        X = solve_banded((1, 1), abz, np.asarray(m_int).reshape(nz, nr))
        # R direction: node n gets from particle p: S_R[n, p]; axis particle 0 gives 3/4 to node 0 and 1/8 + 1/8 to node 1
        abr = np.zeros((3, nr))
        abr[0, 1:] = 0.125                                  # S_R[n, n+1]
        abr[1, :] = 0.75
        abr[2, :-1] = 0.125                                 # S_R[n+1, n]
        abr[2, 0] = 0.25                                    # S_R[1, 0] (fold)
        M = solve_banded((1, 1), abr, X.T).T
        return M

    def jacobian(self, Xr, Xz):
        """J = (R/R_q) det d(R,z)/d(R_q,z_q) on the label lattice (NZ-2, NR-1).
        AMENDMENT A1: the axis column (R_q = 0) carries almost no mass in the B2 ring representation, so its particles are
        passive tracers; the derivatives at R_q = h use the symmetry-extrapolated axis values (R odd: 0; z even:
        (4 z(h) - z(2h))/3) instead of the tracer positions. The axis column's own J is the R_q -> 0 limit and is excluded
        from every statistic by the callers."""
        Rq, zq = self.R[:-1], self.z[1:-1]
        Xr = Xr.copy()
        Xz = Xz.copy()
        Xr[:, 0] = 0.0
        Xz[:, 0] = (4.0 * Xz[:, 1] - Xz[:, 2]) / 3.0
        dRR = np.gradient(Xr, Rq, axis=1, edge_order=1)
        dRz = np.gradient(Xr, zq, axis=0, edge_order=1)
        dzR = np.gradient(Xz, Rq, axis=1, edge_order=1)
        dzz = np.gradient(Xz, zq, axis=0, edge_order=1)
        J = np.empty_like(Xr)
        J[:, 1:] = Xr[:, 1:] / Rq[1:] * (dRR[:, 1:] * dzz[:, 1:] - dRz[:, 1:] * dzR[:, 1:])
        J[:, 0] = (Xr[:, 1] / Rq[1]) ** 2 * dzz[:, 0]
        return J


def make_pair_grid(r_max, h, B_out=20000.0, q=1.08):
    R_f = 20.0 * math.ceil(max(500.0, 0.6 * r_max) / 20.0)
    z_lo = -20.0 * math.ceil((0.625 * r_max + 200.0) / 20.0)
    z_hi = 20.0 * math.ceil((0.375 * r_max + 200.0) / 20.0)
    return Grid(build_axis_R(R_f, h, B_out, q), build_axis_z(z_lo, z_hi, h, B_out, q), fine=(R_f, z_lo, z_hi, h))


def make_box_grid(R_f, z_lo, z_hi, h, B_out, q=1.08):
    return Grid(build_axis_R(R_f, h, B_out, q), build_axis_z(z_lo, z_hi, h, B_out, q), fine=(R_f, z_lo, z_hi, h))


# ================================================================ physics helpers
def mu_of(x):
    return x / (1.0 + x)


def muL_of(x):
    return (2 * x + x * x) / (1.0 + x) ** 2


def nu_of(y):
    return 0.5 * (1.0 + np.sqrt(1.0 + 4.0 / np.maximum(y, 1e-300)))


def plummer_phi(Rn, zn, masses):
    """masses: list of (M, z_pos). Returns full (NZ, NR) potential."""
    RR, ZZ = np.meshgrid(Rn, zn)
    phi = np.zeros_like(RR)
    for M, zc in masses:
        phi -= G * M / np.sqrt(RR ** 2 + (ZZ - zc) ** 2 + EPS ** 2)
    return phi


class MonoAQUAL:
    """Spherical AQUAL potential of a point mass M (g = [gN + sqrt(gN^2 + 4 gN a0)]/2), tabulated for r >= 500 kpc."""

    def __init__(self, M, a0, rmin=500.0, rmax=1.0e5, n=40001):
        lr = np.linspace(math.log(rmin), math.log(rmax), n)
        r = np.exp(lr)
        gN = G * M / r ** 2
        g = 0.5 * (gN + np.sqrt(gN ** 2 + 4 * gN * a0))
        integrand = g * r
        pot = np.concatenate([[0.0], np.cumsum(0.5 * (integrand[1:] + integrand[:-1]) * np.diff(lr))])
        self.lr, self.pot = lr, pot

    def __call__(self, r):
        return np.interp(np.log(np.maximum(r, 1e-300)), self.lr, self.pot)


# ================================================================ solvers
def solve_aqual(grid, phib_full, Xi_bdy_full, a0, tol=1e-12, maxit=60, log=None, Xi_start=None):
    """Discrete AQUAL (weak form): R_mu(Xi) = R_1(phi_b) on interior nodes, Dirichlet Xi_bdy. Newton with the exact
    tensor Jacobian C = mu I + (mu_L - mu) g^g^ at the Gauss points; start from the QUMOND-like solve (or Xi_start)."""
    f_b = grid.interior(grid.kernel(phib_full)).copy()
    scale = np.abs(f_b).max()
    if Xi_start is None:
        rhs = grid.interior(grid.kernel(phib_full, "nu", a0)) - grid.interior(grid.kernel(grid.bdy_only(Xi_bdy_full)))
        Xi = grid.full(grid.solve_int(rhs), Xi_bdy_full)
    else:
        Xi = Xi_start.copy()

    def F(X):
        return grid.interior(grid.kernel(X, "mu", a0)) - f_b, None

    res, gq = F(Xi)
    hist, best, cg_total = [], None, []
    for it in range(maxit):
        rel = np.abs(res).max() / scale
        hist.append(rel)
        if log:
            log(f"      AQUAL it {it:3d}  max|res|/max|f| = {rel:.3e}")
        if best is None or rel < best[0]:
            best = (rel, Xi.copy())
        if rel <= tol or (it >= 8 and rel >= 0.5 * min(hist[-4:-1])):
            break
        cRR, cRz, czz = [], [], []
        for gR, gz in grid.grad_gauss(Xi):
            gm = np.maximum(np.hypot(gR, gz), 1e-300)
            x = gm / a0
            mu, muL = mu_of(x), muL_of(x)
            nR, nz = gR / gm, gz / gm
            cRR.append(np.maximum(mu, 1e-14) + (muL - mu) * nR * nR)
            cRz.append((muL - mu) * nR * nz)
            czz.append(np.maximum(mu, 1e-14) + (muL - mu) * nz * nz)
        C = (cRR, cRz, czz)
        Dn = grid.interior(grid.lumped_nodal([0.5 * (cRR[g] + czz[g]) for g in range(4)])).ravel()
        sD = 1.0 / np.sqrt(Dn)
        zero_bdy = np.zeros((grid.NZ, grid.NR))

        def matvec(v):
            return grid.interior(grid.kernel(grid.full(v, zero_bdy), "tensor", C=C)).ravel()

        def prec(r):
            return sD * grid.solve_int(sD * r)

        eta_k = min(0.1, math.sqrt(rel)) * 0.1
        delta, cg_it = pcg(matvec, -np.ascontiguousarray(res).ravel(), prec, eta_k)
        cg_total.append(cg_it)
        step = 1.0
        for _ in range(6):
            trial = grid.full(grid.interior(Xi).ravel() + step * delta, Xi_bdy_full)
            res2, gq2 = F(trial)
            if np.abs(res2).max() / scale < rel or step < 0.05:
                break
            step *= 0.5
        Xi, res, gq = trial, res2, gq2
    return best[1], {"iterations": len(hist), "rel_residual": best[0], "history_tail": hist[-5:], "cg_iterations": cg_total}


def pcg(matvec, b, prec, rtol, maxit=3000):
    """Preconditioned conjugate gradients from x0 = 0 to ||r|| <= rtol ||b||."""
    with np.errstate(all="ignore"):                        # spurious FP flags from BLAS dot on this platform
        return _pcg(matvec, b, prec, rtol, maxit)


def _pcg(matvec, b, prec, rtol, maxit):
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


class HoldSolver:
    """Anderson-accelerated fixed point Xi_int <- A^-1 [-K m + R_mu(Xi) - R_1(bdy)], warm-started (linear extrapolation)."""

    def __init__(self, grid, a0, tol=1e-7, depth=5, maxit=300):
        self.g, self.a0, self.tol, self.depth, self.maxit = grid, a0, tol, depth, maxit
        self.Xi_int = None
        self.Xi_prev = None
        self.last_iters = 0
        self.last_xmax = 0.0
        self.converged = True

    def solve(self, Km_int, Xi_bdy_full, Xi_start=None):
        g, a0 = self.g, self.a0
        bterm = g.interior(g.kernel(g.bdy_only(Xi_bdy_full))).ravel()
        Kmv = np.asarray(Km_int).ravel()
        thr = self.tol * a0 * g.hmin

        def T(xint):
            Xi = g.full(xint, Xi_bdy_full)
            res, xmax = g.kernel(Xi, "mu", a0, want_xmax=True)
            rhs = -Kmv + g.interior(res).ravel() - bterm
            return g.solve_int(rhs), xmax

        n, mdep = g.nint, self.depth
        if getattr(self, "_aa", None) is None or self._aa[0].shape[1] != n:
            self._aa = (np.empty((mdep + 1, n)), np.empty((mdep + 1, n)))   # ring buffers of x_k and g_k
        Xb, Gb = self._aa
        if Xi_start is not None:
            x = Xi_start.copy()
        elif self.Xi_int is None:
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
                order = [(cnt - k + j) % (mdep + 1) for j in range(k)]       # oldest -> newest
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


# ================================================================ the simulation
class Sim:
    """Self-consistent khronon fluid in prescribed baryon potentials.

    baryons(t) -> list of (M, z) ; bc(t, phib_full) -> (Xi_bdy_full, phit_bdy_full) ; phi_ext: static extra potential.
    Axis particles (label R_q = 0) stay on the axis (symmetry): their radial acceleration is zero.
    """

    def __init__(self, grid, a0, gamma_L, baryons, bc, Xi_eq_full, masses_int, t_start, frozen=False, tol=1e-7,
                 phi_ext=None, v0=None, force_mode="b2", node_masses=True):
        self.g, self.a0, self.gL = grid, a0, gamma_L
        self.baryons, self.bc = baryons, bc
        self.frozen = frozen
        self.phi_ext = phi_ext
        g = grid
        RR, ZZ = np.meshgrid(g.R[:-1], g.z[1:-1])
        self.q_R, self.q_z = RR.ravel().copy(), ZZ.ravel().copy()
        self.on_axis = self.q_R == 0.0
        self.XR, self.XZ = self.q_R.copy(), self.q_z.copy()
        self.VR = np.zeros_like(self.XR)
        self.VZ = np.zeros_like(self.XZ)
        if v0 is not None:
            self.VR += v0[0]
            self.VZ += v0[1]
            self.VR[self.on_axis] = 0.0
        self.force_mode = force_mode
        # masses_int are nodal masses; with the B2 shape the particle masses are their deconvolution
        if force_mode == "b2" and node_masses:
            self.m = g.b2_deconvolve(masses_int).ravel().copy()
        else:
            self.m = np.asarray(masses_int).ravel().copy()
        self.t = t_start
        self.hold = HoldSolver(g, a0, tol=tol)
        self.hold.Xi_int = Xi_eq_full[1:-1, :-1].ravel().copy()
        self.flags = {"F1": None, "F2": None, "F3": None}
        self.ncalls = 0
        self.iters_total = 0
        self.xmax_seen = 0.0
        self.lost_mass = 0.0
        self.acc_frozen = None
        self._rho = None
        self._sh = None
        if frozen:                             # frozen F: chi_0 - gamma_L rho_+0 on the grid (full), never updated
            chi0 = self._chi_nodes(self.t)
            self.acc_frozen = chi0 - gamma_L * np.maximum(self._rho, 0.0)

    def phib(self, t):
        ph = plummer_phi(self.g.R, self.g.z, self.baryons(t))
        if self.phi_ext is not None:
            ph = ph + self.phi_ext
        return ph

    def _chi_nodes(self, t, w=None):
        g = self.g
        if self.force_mode == "b2":
            self._sh = g.b2(self.XR, self.XZ)
            mdep = g.deposit_b2(self._sh, self.m)
        else:
            if w is None:
                w = g.cic(self.XR, self.XZ)
            mdep = g.deposit(w, self.m)
        self.lost_mass = float(np.abs(mdep).sum() - np.abs(mdep[1:-1, :-1]).sum())
        Km = K * mdep[1:-1, :-1]
        phib = self.phib(t)
        Xi_bdy, phit_bdy = self.bc(t, phib)
        Xi_int = self.hold.solve(Km, Xi_bdy)
        self.ncalls += 1
        self.iters_total += self.hold.last_iters
        self.xmax_seen = max(self.xmax_seen, self.hold.last_xmax)
        if not self.hold.converged and self.flags["F1"] is None:
            self.flags["F1"] = self.t
        if self.hold.last_xmax > 50 and self.flags["F2"] is None:
            self.flags["F2"] = self.t
        phit_int = g.solve_int(-Km.ravel() - g.interior(g.kernel(g.bdy_only(phit_bdy))).ravel())
        chi = g.full(Xi_int, Xi_bdy) - g.full(phit_int, phit_bdy)
        rho = np.zeros((g.NZ, g.NR))
        rho[1:-1, :-1] = mdep[1:-1, :-1] / g.V
        self._rho = rho
        return chi

    def accel(self, t):
        g = self.g
        w = None if self.force_mode == "b2" else g.cic(self.XR, self.XZ)
        if self.frozen and self.force_mode == "b2":
            self._sh = g.b2(self.XR, self.XZ)
        if self.frozen:
            zeta = self.acc_frozen - self.phib(t)
            rho_p = None
        else:
            chi = self._chi_nodes(t, w)
            zeta = chi - self.phib(t)
            rho_p = np.maximum(self._rho, 0.0)
        if self.force_mode == "b2":
            sh = self._sh
            tot = zeta if rho_p is None or self.gL == 0 else zeta - self.gL * rho_p
            aR, az = g.interp_grad_b2(sh, tot)
        elif self.force_mode == "ec":
            aR, az = g.interp_grad(w, zeta)
            if rho_p is not None and self.gL > 0:
                pR, pz = g.interp_grad(w, rho_p)
                aR = aR - self.gL * pR
                az = az - self.gL * pz
        else:
            GR, GZ = g.proj_grad(zeta)
            if rho_p is not None and self.gL > 0:
                pR, pz = g.proj_grad(rho_p)
                GR = GR - self.gL * pR
                GZ = GZ - self.gL * pz
            aR, az = g.interp(w, GR), g.interp(w, GZ)
        aR = np.where(self.on_axis, 0.0, aR)
        return aR, az

    def step(self, dt, acc):
        aR, az = acc
        self.VR += 0.5 * dt * aR
        self.VZ += 0.5 * dt * az
        self.XR += dt * self.VR
        self.XZ += dt * self.VZ
        neg = self.XR < 0
        if neg.any():
            self.XR[neg] = -self.XR[neg]
            self.VR[neg] = -self.VR[neg]
        out = (self.XR > self.g.R[-1]) | (self.XZ < self.g.z[0]) | (self.XZ > self.g.z[-1])
        if out.any():
            if self.flags["F3"] is None:
                self.flags["F3"] = self.t + dt
            self.XR = np.minimum(self.XR, self.g.R[-1])
            self.XZ = np.clip(self.XZ, self.g.z[0], self.g.z[-1])
        self.t += dt
        aR, az = self.accel(self.t)
        self.VR += 0.5 * dt * aR
        self.VZ += 0.5 * dt * az
        return aR, az

    def omega_max(self):
        """max over nodes of [K |rho| ((1+x)^2 - 1)]^1/2 for the last deposited state (x from the hold solution)."""
        g = self.g
        if self._rho is None or self.hold.Xi_int is None:
            return 0.0
        Xi = np.zeros((g.NZ, g.NR))
        Xi[1:-1, :-1] = self.hold.Xi_int.reshape(g.NZ - 2, g.NR - 1)
        dR, dz = g.node_grad(Xi)
        x = np.hypot(dR, dz)[1:-1, :-1] / self.a0
        om2 = K * np.abs(self._rho[1:-1, :-1]) * ((1 + x) ** 2 - 1)
        return float(np.sqrt(om2.max()))

    def J(self):
        g = self.g
        sh = (g.NZ - 2, g.NR - 1)
        return g.jacobian(self.XR.reshape(sh), self.XZ.reshape(sh)).ravel()

    def kinetic(self):
        """sum |m| v^2 / 2 (diagnostic)."""
        return float(0.5 * np.sum(np.abs(self.m) * (self.VR ** 2 + self.VZ ** 2)))


def masses_of(grid, Xi, a0):
    return -grid.interior(grid.kernel(Xi, "1-mu", a0)) / K


def initial_state(grid, a0, phib_full, Xi_bdy_full, gamma_L=0.0, log=None, max_outer=12):
    """Discrete v3s (switched) static equilibrium and the khronon particle masses m = -R_{1-mu}(Xi)/K (interior).

    AMENDMENT A1: the static khronon obeys grad(chi - phi_b - gamma_L rho_+) = 0, i.e. AQUAL with phi_b replaced by
    phi_b + gamma_L rho_+(Xi), rho_+ the lumped nodal density of the khronon masses; solved by fixed point (gamma_L = 0
    gives plain AQUAL)."""
    Xi, info = solve_aqual(grid, phib_full, Xi_bdy_full, a0, log=log)
    outer = []
    if gamma_L > 0:
        for k in range(max_outer):
            m = masses_of(grid, Xi, a0)
            rho_p = np.zeros_like(phib_full)
            rho_p[1:-1, :-1] = np.maximum(m / grid.V, 0.0)
            Xi_new, info = solve_aqual(grid, phib_full + gamma_L * rho_p, Xi_bdy_full, a0, Xi_start=Xi)
            dx = float(np.abs(Xi_new - Xi).max())
            outer.append(dx)
            Xi = Xi_new
            if dx <= 1e-9 * a0 * grid.hmin:
                break
    info["stiffness_outer"] = outer
    m = masses_of(grid, Xi, a0)
    dR, dz = grid.node_grad(Xi)
    x = np.hypot(dR, dz)[1:-1, :-1] / a0
    rho = m / grid.V
    om2 = K * np.abs(rho) * ((1 + x) ** 2 - 1)
    info["omega_max"] = float(np.sqrt(om2.max()))
    return Xi, m, rho, x, info


def wall():
    return time.time()
