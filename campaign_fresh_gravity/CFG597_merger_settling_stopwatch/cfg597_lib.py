#!/usr/bin/env python3
"""CFG597 library: 3-D cluster-merger model with cold-energy settling (criteria: FROZEN_CRITERIA.md, ae49ff4d7).

Units kpc, Gyr, Msun.  Gas: adiabatic Euler (MUSCL-minmod, Rusanov, RK2).  Galaxies and cold energy: PM particles (CIC).
Gravity and the deficit potential psi: zero-padded FFT Poisson (isolated).  Cold-energy settling: CFG541 class-A drift
v_s = -alpha tau grad psi toward the round-rule phantom of the CURRENT baryons of each progenitor (no EFE), plus CFG544 FIX-2
OU velocity relaxation (rate alpha/tau, toward the local mean cold velocity, target = isotropic spherical Jeans dispersion).
kappa = 1/2 is fitted; the cold energy's mass is required (an input); no particle species is proposed.
"""
import os
os.environ.setdefault("OMP_NUM_THREADS", "1")
import math
import numpy as np
import scipy.fft as sfft

G = 4.49850215e-6                      # kpc^3 Gyr^-2 Msun^-1
KMS = 1.0227121650537077               # 1 km/s in kpc/Gyr
A0_SI = {"can": 9.3603e-11, "alt": 1.1312e-10}
SI_TO_KPCGYR2 = (3.15576e16 ** 2) / 3.0857e19
A0 = {k: v * SI_TO_KPCGYR2 for k, v in A0_SI.items()}
GAMMA = 5.0 / 3.0
H0, OM = 0.07, 0.3                     # km/s/kpc, the record's plate-scale convention (size convention only)
Z_BULLET = 0.296
RHO_CRIT0 = 3 * (H0 * KMS) ** 2 / (8 * math.pi * G)
RHO_CRIT_Z = RHO_CRIT0 * (OM * (1 + Z_BULLET) ** 3 + 1 - OM)


def nu_mono(y):
    y = np.maximum(y, 1e-300)
    return 1.0 / (-np.expm1(-np.sqrt(y)))


def r200_of(M200):
    return (3 * M200 / (4 * math.pi * 200 * RHO_CRIT_Z)) ** (1 / 3)


# ------------------------------------------------------------------------------------------------------------ grid
class Grid:
    def __init__(self, nx=128, ny=64, nz=64, dx=50.0):
        self.n = (nx, ny, nz); self.dx = dx
        self.L = np.array([nx, ny, nz]) * dx
        self.lo = -self.L / 2
        self.xc = [self.lo[i] + (np.arange(self.n[i]) + 0.5) * dx for i in range(3)]
        self.dV = dx ** 3
        # isolated Green's function on the doubled grid
        P = tuple(2 * m for m in self.n); self.P = P
        ax = [np.minimum(np.arange(P[i]), P[i] - np.arange(P[i])) * dx for i in range(3)]
        R = np.sqrt(ax[0][:, None, None] ** 2 + ax[1][None, :, None] ** 2 + ax[2][None, None, :] ** 2)
        R[0, 0, 0] = dx / 2.38           # cell self-potential: the mean of 1/r over a cube of side dx is 2.38/dx
        self.Gk = sfft.rfftn(-G / R)
        del R

    def poisson(self, rho):
        """potential of the mass density rho (Msun/kpc^3), isolated boundary."""
        nx, ny, nz = self.n
        pad = np.zeros(self.P)
        pad[:nx, :ny, :nz] = rho * self.dV
        phi = sfft.irfftn(sfft.rfftn(pad) * self.Gk, s=self.P)
        return phi[:nx, :ny, :nz]

    def grad(self, f):
        return [np.gradient(f, self.dx, axis=i, edge_order=1) for i in range(3)]

    # ---- CIC
    def _cic(self, pos):
        u = (pos - self.lo) / self.dx - 0.5
        i0 = np.floor(u).astype(np.int64); w1 = u - i0; w0 = 1 - w1
        return i0, w0, w1

    def deposit(self, pos, m):
        nx, ny, nz = self.n
        i0, w0, w1 = self._cic(pos)
        out = np.zeros(nx * ny * nz)
        mm = np.broadcast_to(m, (pos.shape[0],)) if np.ndim(m) == 0 else m
        for a in (0, 1):
            ia = i0[:, 0] + a; wa = w0[:, 0] if a == 0 else w1[:, 0]
            for b in (0, 1):
                ib = i0[:, 1] + b; wb = w0[:, 1] if b == 0 else w1[:, 1]
                for c in (0, 1):
                    ic = i0[:, 2] + c; wc = w0[:, 2] if c == 0 else w1[:, 2]
                    ok = (ia >= 0) & (ia < nx) & (ib >= 0) & (ib < ny) & (ic >= 0) & (ic < nz)
                    idx = (ia[ok] * ny + ib[ok]) * nz + ic[ok]
                    out += np.bincount(idx, weights=(mm * wa * wb * wc)[ok], minlength=out.size)
        return out.reshape(self.n) / self.dV

    def interp(self, pos, fields):
        nx, ny, nz = self.n
        i0, w0, w1 = self._cic(pos)
        res = [np.zeros(pos.shape[0]) for _ in fields]
        for a in (0, 1):
            ia = np.clip(i0[:, 0] + a, 0, nx - 1); wa = w0[:, 0] if a == 0 else w1[:, 0]
            for b in (0, 1):
                ib = np.clip(i0[:, 1] + b, 0, ny - 1); wb = w0[:, 1] if b == 0 else w1[:, 1]
                for c in (0, 1):
                    ic = np.clip(i0[:, 2] + c, 0, nz - 1); wc = w0[:, 2] if c == 0 else w1[:, 2]
                    w = wa * wb * wc
                    for k, f in enumerate(fields):
                        res[k] += w * f[ia, ib, ic]
        return res

    def radius_from(self, x0):
        X, Y, Z = self.xc
        return np.sqrt((X[:, None, None] - x0[0]) ** 2 + (Y[None, :, None] - x0[1]) ** 2 + (Z[None, None, :] - x0[2]) ** 2)


# ------------------------------------------------------------------------------------------------------------ hydro
def prim(U):
    rho = U[0]
    v = U[1:4] / rho
    e = U[4] - 0.5 * rho * (v ** 2).sum(0)
    P = np.maximum((GAMMA - 1) * e, 1e-12 * rho)
    return rho, v, P, U[5] / rho


def cons(rho, v, P, X):
    U = np.empty((6,) + rho.shape)
    U[0] = rho; U[1:4] = rho * v; U[4] = P / (GAMMA - 1) + 0.5 * rho * (v ** 2).sum(0); U[5] = rho * X
    return U


def _sl(A, ax, a, b):
    idx = [slice(None)] * A.ndim
    idx[ax] = slice(a, b)
    return A[tuple(idx)]


def _minmod(a, b):
    return np.where(a * b > 0, np.where(np.abs(a) < np.abs(b), a, b), 0.0)


def _flux(W, d):
    rho, vx, vy, vz, P, X = W
    v = (vx, vy, vz)
    vn = v[d]
    E = P / (GAMMA - 1) + 0.5 * rho * (vx * vx + vy * vy + vz * vz)
    F = np.empty((6,) + rho.shape)
    F[0] = rho * vn
    F[1] = rho * vx * vn; F[2] = rho * vy * vn; F[3] = rho * vz * vn
    F[1 + d] += P
    F[4] = (E + P) * vn
    F[5] = rho * X * vn
    return F, E


def hydro_rhs(U, dx, rho_floor):
    """-div F for the 6 conserved fields, MUSCL-minmod on primitives, Rusanov flux, zero-gradient boundaries."""
    rho, v, P, X = prim(U)
    W = np.stack([rho, v[0], v[1], v[2], P, X])
    rhs = np.zeros_like(U)
    for d in range(3):
        ax = d + 1
        Wp = np.concatenate([_sl(W, ax, 0, 1), W, _sl(W, ax, -1, None)], axis=ax)    # one ghost each side
        dl = np.diff(Wp, axis=ax)
        n = W.shape[ax]
        sl = _minmod(_sl(dl, ax, 0, n), _sl(dl, ax, 1, n + 1))
        WL_face = W + 0.5 * sl          # right face of each cell (left state of face i+1/2)
        WR_face = W - 0.5 * sl          # left face of each cell (right state of face i-1/2)
        # interior faces between cell i and i+1 : L = WL_face[i], R = WR_face[i+1]; boundary faces copy
        L = np.concatenate([_sl(WR_face, ax, 0, 1), WL_face], axis=ax)
        R = np.concatenate([WR_face, _sl(WL_face, ax, -1, None)], axis=ax)
        L[0] = np.maximum(L[0], rho_floor); R[0] = np.maximum(R[0], rho_floor)
        L[4] = np.maximum(L[4], 1e-12 * L[0]); R[4] = np.maximum(R[4], 1e-12 * R[0])
        FL, EL = _flux(L, d); FR, ER = _flux(R, d)
        UL = np.stack([L[0], L[0] * L[1], L[0] * L[2], L[0] * L[3], EL, L[0] * L[5]])
        UR = np.stack([R[0], R[0] * R[1], R[0] * R[2], R[0] * R[3], ER, R[0] * R[5]])
        cL = np.sqrt(GAMMA * L[4] / L[0]) + np.abs(L[1 + d]); cR = np.sqrt(GAMMA * R[4] / R[0]) + np.abs(R[1 + d])
        smax = np.maximum(cL, cR)
        F = 0.5 * (FL + FR) - 0.5 * smax * (UR - UL)
        rhs -= np.diff(F, axis=ax) / dx
    return rhs


def hydro_step(U, g, dt, dx, rho_floor):
    """Heun RK2 with gravity source (g fixed over the step)."""
    def full(Uin):
        r = hydro_rhs(Uin, dx, rho_floor)
        rho = Uin[0]; mom = Uin[1:4]
        r[1:4] += rho * np.stack(g)
        r[4] += (mom * np.stack(g)).sum(0)
        return r
    k1 = full(U)
    U1 = U + dt * k1
    _fix(U1, rho_floor)
    k2 = full(U1)
    Un = U + 0.5 * dt * (k1 + k2)
    _fix(Un, rho_floor)
    return Un


def _fix(U, rho_floor):
    bad = U[0] < rho_floor
    if bad.any():
        U[0] = np.where(bad, rho_floor, U[0])
    U[5] = np.clip(U[5], 0, U[0])
    rho, v, P, X = prim(U)
    Pmin = 1e-8 * rho * (1e3 * KMS) ** 2
    e_min = Pmin / (GAMMA - 1) + 0.5 * rho * (v ** 2).sum(0)
    U[4] = np.maximum(U[4], e_min)


def hydro_dt(U, dx, cfl=0.3):
    rho, v, P, X = prim(U)
    cs = np.sqrt(GAMMA * P / rho)
    s = (np.abs(v[0]) + cs).max(), (np.abs(v[1]) + cs).max(), (np.abs(v[2]) + cs).max()
    return cfl * dx / max(s)


# ------------------------------------------------------------------------------------------------------------ profiles
class Progenitor:
    """Spherical progenitor: gas beta-model (beta=2/3, r_c=0.1 r200, steep x^-8 fall-off beyond r_t), stars NFW c=4,
    cold energy = round phantom of its baryons (case L) [+ unsettled NFW c=4 (case U)], all truncated at r_t."""

    def __init__(self, M200, foot, case, swap=False, nr=4000, rmax=8000.0, rc_frac=0.1):
        self.M200 = M200; self.r200 = r200_of(M200); self.rt = min(self.r200, 1200.0)
        self.Mb = M200 / 6.73
        fg, fs = (0.13, 0.87) if swap else (0.87, 0.13)
        self.Mgas, self.Mst = fg * self.Mb, fs * self.Mb
        self.a0 = A0[foot]; self.case = case
        r = np.concatenate([[0.0], np.geomspace(0.5, rmax, nr)]); self.r = r
        rc = rc_frac * self.r200                 # 0.1 frozen; the supplementary S1 runs use a compact sub core
        sh = (1 + (r / rc) ** 2) ** -1.0 * np.where(r < self.rt, 1.0, (np.maximum(r, 1e-3) / self.rt) ** -8.0)
        self.gas_shape = sh
        Mg = cumtrapz_sph(r, sh)
        self.rho_g0 = self.Mgas / Mg[-1]
        self.rho_g = self.rho_g0 * sh
        self.Mg = self.rho_g0 * Mg
        rs = self.r200 / 4.0
        nfw = np.where(r < self.rt, 1.0 / (np.maximum(r, 1e-3) / rs * (1 + r / rs) ** 2), 0.0)
        Mn = cumtrapz_sph(r, nfw)
        self.nfw_shape = nfw / Mn[-1]; self.Mnfw_unit = Mn / Mn[-1]
        self.rho_s = self.Mst * self.nfw_shape; self.Ms = self.Mst * self.Mnfw_unit
        self.Mbar = self.Mg + self.Ms
        Mph = phantom_mass(r, self.Mbar, self.a0)
        Mph_t = np.interp(self.rt, r, Mph)
        self.Mph = np.where(r < self.rt, Mph, Mph_t)
        self.rho_ph = np.gradient(self.Mph, r) / (4 * math.pi * np.maximum(r, 1e-3) ** 2)
        self.rho_ph[r >= self.rt] = 0.0
        self.Mph_tot = Mph_t
        if case == "U":
            Mu = max(M200 - self.Mb - np.interp(self.r200, r, self.Mph), 0.0)
            # normalise the unsettled part so that the total cold mass inside r200 is M200 - M_b (truncated at r_t)
            self.Mu_tot = Mu * self.Mnfw_unit[-1] / np.interp(self.r200, r, self.Mnfw_unit)
            self.rho_u = self.Mu_tot * self.nfw_shape; self.Mu = self.Mu_tot * self.Mnfw_unit
        else:
            self.Mu_tot = 0.0; self.rho_u = 0 * r; self.Mu = 0 * r
        self.Mtot = self.Mbar + self.Mph + self.Mu
        # hydrostatic gas pressure, integrated inward from rmax
        gN = G * self.Mtot / np.maximum(r, 1e-3) ** 2
        integrand = self.rho_g * gN
        P = np.zeros_like(r)
        P[-1] = self.rho_g[-1] * 0.5 * G * self.Mtot[-1] / r[-1]
        for k in range(len(r) - 2, -1, -1):
            P[k] = P[k + 1] + 0.5 * (integrand[k] + integrand[k + 1]) * (r[k + 1] - r[k])
        self.P = P
        self.u_frac = self.Mu_tot / (self.Mu_tot + self.Mph_tot) if case == "U" else 0.0

    def jeans_sigma2(self, rho):
        """isotropic Jeans sigma^2(r) of a tracer rho(r) in this progenitor's total mass."""
        r = self.r
        gN = G * self.Mtot / np.maximum(r, 1e-3) ** 2
        f = rho * gN
        I = np.zeros_like(r)
        for k in range(len(r) - 2, -1, -1):
            I[k] = I[k + 1] + 0.5 * (f[k] + f[k + 1]) * (r[k + 1] - r[k])
        return np.where(rho > 0, I / np.maximum(rho, 1e-300), 0.0)


def cumtrapz_sph(r, rho):
    f = 4 * math.pi * r ** 2 * rho
    out = np.zeros_like(r)
    out[1:] = np.cumsum(0.5 * (f[1:] + f[:-1]) * np.diff(r))
    return out


def phantom_mass(r, Mb, a0):
    """round-rule phantom (CFG541 E7): M_ph(<r) = (nu(G M_b(<r)/(r^2 a0)) - 1) M_b(<r)."""
    rr = np.maximum(r, 1e-6)
    y = G * Mb / (rr ** 2 * a0)
    out = (nu_mono(y) - 1.0) * Mb
    out[Mb <= 0] = 0.0
    return out


def sample_radial(rng, r, Mcum, n):
    u = rng.random(n) * Mcum[-1]
    rr = np.interp(u, Mcum, r)
    cth = rng.uniform(-1, 1, n); ph = rng.uniform(0, 2 * math.pi, n); sth = np.sqrt(1 - cth ** 2)
    return np.stack([rr * sth * np.cos(ph), rr * sth * np.sin(ph), rr * cth], 1), rr


# ------------------------------------------------------------------------------------------------------------ helpers
def iter_centroid_2d(X, Y, S, start, R, it=60, tol=0.25):
    c = np.array(start, float)
    for _ in range(it):
        w = S * (((X - c[0]) ** 2 + (Y - c[1]) ** 2) <= R * R)
        sw = w.sum()
        if sw <= 0:
            return c
        cn = np.array([(w * X).sum() / sw, (w * Y).sum() / sw])
        if np.hypot(*(cn - c)) < tol:
            return cn
        c = cn
    return c


def phantom_profile_from_mass(rb, Mb_cum, a0, rt):
    """phantom density on radial edges rb from the cumulative baryon mass, truncated at rt."""
    Mph = phantom_mass(rb, Mb_cum, a0)
    Mph_t = np.interp(rt, rb, Mph)
    Mph = np.where(rb < rt, Mph, Mph_t)
    dM = np.diff(Mph)
    vol = 4 * math.pi / 3 * np.diff(rb ** 3)
    return dM / vol, Mph_t
