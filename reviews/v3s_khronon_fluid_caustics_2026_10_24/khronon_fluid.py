#!/usr/bin/env python3
"""v3s self-consistent khronon fluid, axisymmetric particle-mesh (FROZEN_CRITERIA.md, 1343f40b91).

Units kpc, Gyr, Msun.  Khronon elements (signed mass, rho_tau = D.P) move with
    Dv/Dt = grad Psi - grad phi - gamma_L grad (rho_tau)_+ ,
    div[ grad Psi / (1 + |grad Psi|/a0) ] = 4 pi G rho_tau        (Gauss law, P(A) of v3)
    lap phi = 4 pi G (rho_b + rho_tau).
Equilibrium Psi = phi is AQUAL with mu = x/(1+x).  Modes: sc (self-consistent), frozen (F = A - grad phi_tau held at
t_i: test particles in the difference field), mutate (masses frozen at r(t_i)).
Preemptible (compute_queue/JOB_CONTRACT.md): SIGTERM/SIGINT -> checkpoint at the next step -> exit 75; --resume.
"""
import argparse
import json
import math
import os
import resource
import signal
import sys
import time
from pathlib import Path

import numpy as np
import scipy.sparse as sps
from scipy.optimize import brentq
from scipy.sparse.linalg import splu

HERE = Path(__file__).resolve().parent
G = 4.498502151469554e-06
MS = (3.15576e16) ** 2 / 3.0856775814913673e19
A0 = {"canonical": 9.36e-11 * MS, "alt": 1.13e-10 * MS}
KMS = 1.0227121650537077
M1, M2, EPS = 6e10, 1e11, 20.0
R0, V0, T0 = 780.0, -110.0 * KMS, 13.8
GAMMA_L = 2 * math.pi * G * 0.024 ** 2
STOP = []
signal.signal(signal.SIGTERM, lambda s, f: STOP.append(s))
signal.signal(signal.SIGINT, lambda s, f: STOP.append(s))
YIELD_EXIT = int(os.environ.get("HEAVYQ_YIELD_EXIT", "75"))


# ---------------------------------------------------------------------------------------------- orbits (as the 10-23 lane)
def _f(e):
    return math.sin(e) * (e - math.sin(e)) / (1 - math.cos(e)) ** 2


ETA0 = brentq(lambda e: _f(e) - V0 * T0 / R0, math.pi + 1e-9, 2 * math.pi - 1e-6)
AK = R0 / (1 - math.cos(ETA0))
GMK = AK ** 3 * ((ETA0 - math.sin(ETA0)) / T0) ** 2
TK = math.sqrt(AK ** 3 / GMK)


def r_O1(t):
    e = brentq(lambda x: TK * (x - math.sin(x)) - t, 0.0, 2 * math.pi)
    return AK * (1 - math.cos(e))


def r_O2(t):
    return R0 + (-V0) * (T0 - t)


ORBITS = {"O1": r_O1, "O2": r_O2}


def t_at_r(orbit, rr):
    if orbit == "O1":
        return brentq(lambda t: r_O1(t) - rr, T0, TK * 2 * math.pi - 1e-6)
    return T0 + (R0 - rr) / (-V0)


def zpos(r):
    return -M2 / (M1 + M2) * r, M1 / (M1 + M2) * r          # MW, M31 on the z axis


# ---------------------------------------------------------------------------------------------- grid and operators
class Grid:
    def __init__(self, h, Rmax=2000.0, Z=2000.0):
        self.h, self.Z = h, Z
        self.nR, self.nz = int(round(Rmax / h)), int(round(2 * Z / h))
        self.Rc = (np.arange(self.nR) + 0.5) * h
        self.zc = -Z + (np.arange(self.nz) + 0.5) * h
        self.RR, self.ZZ = np.meshgrid(self.Rc, self.zc, indexing="ij")
        self.V = 2 * math.pi * self.RR * h * h
        Rf = np.arange(self.nR + 1) * h
        self.AR = 2 * math.pi * Rf[:, None] * h * np.ones((1, self.nz))
        self.Az = 2 * math.pi * self.Rc[:, None] * h * np.ones((1, self.nz + 1))
        self.Rmax = Rmax
        # boundary face centres
        self.bR = (np.full(self.nz, Rmax), self.zc)                    # outer R faces
        self.bzlo = (self.Rc, np.full(self.nR, -Z))
        self.bzhi = (self.Rc, np.full(self.nR, Z))
        self.N = self.nR * self.nz
        self._L = None

    def bc_values(self, fun):
        return fun(*self.bR), fun(*self.bzlo), fun(*self.bzhi)

    def cell_grad(self, P, bc):
        h = self.h
        bR, blo, bhi = bc
        gR = np.empty_like(P)
        gz = np.empty_like(P)
        gR[1:-1] = (P[2:] - P[:-2]) / (2 * h)
        gR[0] = (P[1] - P[0]) / (2 * h)                               # mirror at the axis
        gR[-1] = (bR - P[-2]) / (1.5 * h)
        gz[:, 1:-1] = (P[:, 2:] - P[:, :-2]) / (2 * h)
        gz[:, 0] = (P[:, 1] - blo) / (1.5 * h)
        gz[:, -1] = (bhi - P[:, -2]) / (1.5 * h)
        return gR, gz

    def face_gradmag(self, P, bc):
        h = self.h
        bR, blo, bhi = bc
        gR, gz = self.cell_grad(P, bc)
        mR = np.empty((self.nR + 1, self.nz))
        n = (P[1:] - P[:-1]) / h
        t = 0.5 * (gz[1:] + gz[:-1])
        mR[1:-1] = np.hypot(n, t)
        mR[0] = np.abs(gz[0])
        mR[-1] = np.hypot((bR - P[-1]) / (h / 2), gz[-1])
        mz = np.empty((self.nR, self.nz + 1))
        n = (P[:, 1:] - P[:, :-1]) / h
        t = 0.5 * (gR[:, 1:] + gR[:, :-1])
        mz[:, 1:-1] = np.hypot(n, t)
        mz[:, 0] = np.hypot((P[:, 0] - blo) / (h / 2), gR[:, 0])
        mz[:, -1] = np.hypot((bhi - P[:, -1]) / (h / 2), gR[:, -1])
        return mR, mz

    def apply(self, P, kR, kz, bc):
        """div(kappa grad P) per cell (flux form, Dirichlet bc on outer faces, axis face area 0)."""
        h = self.h
        bR, blo, bhi = bc
        F = np.zeros_like(P)
        fl = self.AR[1:-1] * kR[1:-1] * (P[1:] - P[:-1]) / h
        F[:-1] += fl
        F[1:] -= fl
        F[-1] += self.AR[-1] * kR[-1] * (bR - P[-1]) / (h / 2)
        fz = self.Az[:, 1:-1] * kz[:, 1:-1] * (P[:, 1:] - P[:, :-1]) / h
        F[:, :-1] += fz
        F[:, 1:] -= fz
        F[:, 0] += self.Az[:, 0] * kz[:, 0] * (blo - P[:, 0]) / (h / 2)
        F[:, -1] += self.Az[:, -1] * kz[:, -1] * (bhi - P[:, -1]) / (h / 2)
        return F / self.V

    def matrix(self, kR, kz):
        """Sparse M with apply(P) = M P + b (b from the boundary values)."""
        h, nR, nz = self.h, self.nR, self.nz
        idx = np.arange(self.N).reshape(nR, nz)
        rows, cols, vals = [], [], []
        diag = np.zeros((nR, nz))
        c = self.AR[1:-1] * kR[1:-1] / h                                # between (i-1, j) and (i, j)
        for a_, b_ in ((idx[:-1], idx[1:]), (idx[1:], idx[:-1])):
            rows.append(a_.ravel()); cols.append(b_.ravel()); vals.append(c.ravel())
        diag[:-1] -= c
        diag[1:] -= c
        diag[-1] -= self.AR[-1] * kR[-1] / (h / 2)
        cz = self.Az[:, 1:-1] * kz[:, 1:-1] / h
        for a_, b_ in ((idx[:, :-1], idx[:, 1:]), (idx[:, 1:], idx[:, :-1])):
            rows.append(a_.ravel()); cols.append(b_.ravel()); vals.append(cz.ravel())
        diag[:, :-1] -= cz
        diag[:, 1:] -= cz
        diag[:, 0] -= self.Az[:, 0] * kz[:, 0] / (h / 2)
        diag[:, -1] -= self.Az[:, -1] * kz[:, -1] / (h / 2)
        rows.append(idx.ravel()); cols.append(idx.ravel()); vals.append(diag.ravel())
        Vinv = 1.0 / self.V.ravel()
        r = np.concatenate(rows); cc = np.concatenate(cols); v = np.concatenate(vals) * Vinv[np.concatenate(rows)]
        return sps.csc_matrix((v, (r, cc)), shape=(self.N, self.N))

    def bvec(self, kR, kz, bc):
        z = np.zeros((self.nR, self.nz))
        return self.apply(z, kR, kz, bc)

    def laplace_lu(self):
        if self._L is None:
            kR = np.ones((self.nR + 1, self.nz))
            kz = np.ones((self.nR, self.nz + 1))
            self._ones = (kR, kz)
            self._L = splu(self.matrix(kR, kz))
        return self._L

    def poisson(self, src, bc):
        kR, kz = self._ones if self._L is not None else (None, None)
        L = self.laplace_lu()
        kR, kz = self._ones
        rhs = src - self.bvec(kR, kz, bc)
        return L.solve(rhs.ravel()).reshape(self.nR, self.nz)

    def gauss(self, src, bc, a0, P0=None, tol=1e-13, maxit=400):
        """Solve div[grad P/(1 + |grad P|/a0)] = src by defect correction against the Laplacian."""
        L = self.laplace_lu()
        P = self.poisson(src, bc) if P0 is None else P0.copy()
        scale = max(np.max(np.abs(src)), 1e-300)
        for it in range(maxit):
            mR, mz = self.face_gradmag(P, bc)
            res = self.apply(P, 1.0 / (1 + mR / a0), 1.0 / (1 + mz / a0), bc) - src
            r = np.max(np.abs(res)) / scale
            if r < tol:
                return P, it, r
            P = P - L.solve(res.ravel()).reshape(self.nR, self.nz)
        return P, maxit, r

    def aqual(self, src, bc, a0, guess, tol=1e-12, maxit=400, damp=0.7):
        """Picard for div[mu(|grad phi|/a0) grad phi] = src, mu = y/(1+y), floor 1e-6."""
        P = guess.copy()
        scale = max(np.max(np.abs(src)), 1e-300)
        hist = []
        for it in range(maxit):
            mR, mz = self.face_gradmag(P, bc)
            muR = np.maximum((mR / a0) / (1 + mR / a0), 1e-6)
            muz = np.maximum((mz / a0) / (1 + mz / a0), 1e-6)
            res = self.apply(P, muR, muz, bc) - src
            r = np.max(np.abs(res)) / scale
            hist.append(r)
            if r < tol:
                return P, it, r, hist
            M = self.matrix(muR, muz)
            Pn = splu(M).solve((src - self.bvec(muR, muz, bc)).ravel()).reshape(self.nR, self.nz)
            P = damp * Pn + (1 - damp) * P
        return P, maxit, r, hist


def plummer_rho(G_, R, z, zc, M):
    r2 = R ** 2 + (z - zc) ** 2
    return 3 * M / (4 * math.pi * EPS ** 3) * (1 + r2 / EPS ** 2) ** -2.5


def baryon_density(grid, r):
    out = np.zeros((grid.nR, grid.nz))
    for M, zc in zip((M1, M2), zpos(r)):
        d = plummer_rho(grid, grid.RR, grid.ZZ, zc, M)
        out += d * M / np.sum(d * grid.V)                          # renormalised to the mass
    return out


def plummer_gN(R, z, r):
    gR = np.zeros_like(R)
    gz = np.zeros_like(R)
    for M, zc in zip((M1, M2), zpos(r)):
        d2 = R ** 2 + (z - zc) ** 2 + EPS ** 2
        gR -= G * M * R / d2 ** 1.5
        gz -= G * M * (z - zc) / d2 ** 1.5
    return gR, gz


# ---------------------------------------------------------------------------------------------- particles
def cic_weights(grid, Rp, zp):
    fi = Rp / grid.h - 0.5
    fj = (zp + grid.Z) / grid.h - 0.5
    i0 = np.floor(fi).astype(int)
    j0 = np.floor(fj).astype(int)
    wi = fi - i0
    wj = fj - j0
    out = []
    for di, wI in ((0, 1 - wi), (1, wi)):
        for dj, wJ in ((0, 1 - wj), (1, wj)):
            ii = np.clip(i0 + di, 0, grid.nR - 1)                    # i = -1 folds onto the axis cell
            jj = np.clip(j0 + dj, 0, grid.nz - 1)
            out.append((ii, jj, wI * wJ))
    return out


def deposit(grid, Rp, zp, m):
    acc = np.zeros((grid.nR, grid.nz))
    for ii, jj, w in cic_weights(grid, Rp, zp):
        np.add.at(acc, (ii, jj), m * w)
    return acc / grid.V


def interp(grid, F, Rp, zp):
    out = np.zeros_like(Rp)
    for ii, jj, w in cic_weights(grid, Rp, zp):
        out += F[ii, jj] * w
    return out


# ---------------------------------------------------------------------------------------------- run
def atomic_save(path, **arrs):
    tmp = path.with_suffix(".tmp.npz")
    with open(tmp, "wb") as fh:
        np.savez(fh, **arrs)
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, path)


def atomic_json(path, obj):
    tmp = path.with_suffix(".tmp")
    with open(tmp, "w") as fh:
        json.dump(obj, fh, indent=1, default=float)
        fh.flush()
        os.fsync(fh.fileno())
    os.replace(tmp, path)


class Run:
    def __init__(self, a):
        self.a = a
        self.grid = Grid(a.h)
        self.a0 = A0[a.foot]
        self.rfun = ORBITS[a.orbit]
        self.ti = a.ti
        self.t_end = t_at_r(a.orbit, 300.0)
        self.t_ext = t_at_r(a.orbit, 150.0) if a.extend else self.t_end
        if a.tsteps:
            self.t_ext = self.ti + a.tsteps * a.dt
            self.t_end = min(self.t_end, self.t_ext)
        self.dt = a.dt

    def setup(self):
        g = self.grid
        ri = self.rfun(self.ti)
        Mb = M1 + M2
        a0 = self.a0
        phibc = lambda R, z: math.sqrt(G * Mb * a0) * np.log(np.sqrt(R ** 2 + z ** 2) / 1000.0)
        self.bc = g.bc_values(phibc)
        rho_b = baryon_density(g, ri)
        src = 4 * math.pi * G * rho_b
        # initial guess: QUMOND potential from analytic g_N is awkward; use the deep-MOND monopole plus Newtonian
        guess = g.poisson(src, self.bc)
        phi, nit, res, hist = g.aqual(src, self.bc, a0, guess)
        self.aqual_info = {"iterations": nit, "residual": res}
        kR, kz = g._ones
        mR, mz = g.face_gradmag(phi, self.bc)
        muR = np.maximum((mR / a0) / (1 + mR / a0), 1e-6)
        muz = np.maximum((mz / a0) / (1 + mz / a0), 1e-6)
        rho_tau = (g.apply(phi, kR, kz, self.bc) - g.apply(phi, muR, muz, self.bc)) / (4 * math.pi * G)
        self.rho_tau0 = rho_tau
        self.m = (rho_tau * g.V).ravel()
        self.Rq, self.zq = g.RR.ravel().copy(), g.ZZ.ravel().copy()
        self.Rp, self.zp = self.Rq.copy(), self.zq.copy()
        self.vR, self.vz = np.zeros_like(self.Rp), np.zeros_like(self.Rp)
        fr = np.zeros((g.nR, g.nz), bool)
        fr[-3:, :] = True
        fr[:, :3] = True
        fr[:, -3:] = True
        self.frozen = fr.ravel()
        self.Psi = phi.copy()
        self.phi_b0 = g.poisson(src, self.bc) if self.a.mode == "frozen" else None
        self.t, self.step = self.ti, 0
        self.diag = []
        self.first_cross = None
        self.acc = self.accel(self.t)
        self.eq_check = float(np.max(np.hypot(self.acc[0][~self.frozen], self.acc[1][~self.frozen])))
        gR, gz = g.cell_grad(phi, self.bc)
        self.eq_scale = float(np.max(np.hypot(gR, gz).ravel()[~self.frozen]))
        if self.a.mode != "frozen":
            nR_ = interp(g, self.noL[0], self.Rp, self.zp)
            nz_ = interp(g, self.noL[1], self.Rp, self.zp)
            self.eq_noL = float(np.max(np.hypot(nR_, nz_)[~self.frozen]))
        else:
            self.eq_noL = self.eq_check

    def accel(self, t):
        g = self.grid
        r = self.rfun(self.ti if self.a.mode == "mutate" else t)
        rho_b = baryon_density(g, r)
        if self.a.mode == "frozen":
            phi_b = g.poisson(4 * math.pi * G * rho_b, self.bc)
            g0R, g0z = g.cell_grad(self.phi_b0, self.bc)
            g1R, g1z = g.cell_grad(phi_b, self.bc)
            aR, az = g0R - g1R, g0z - g1z
            self.gauss_it = 0
        else:
            rho_tau = deposit(g, self.Rp, self.zp, self.m)
            phi = g.poisson(4 * math.pi * G * (rho_b + rho_tau), self.bc)
            self.Psi, self.gauss_it, self.gauss_res = g.gauss(4 * math.pi * G * rho_tau, self.bc, self.a0, self.Psi)
            pR, pz = g.cell_grad(self.Psi, self.bc)
            fR, fz = g.cell_grad(phi, self.bc)
            rp = np.maximum(rho_tau, 0.0)
            qR, qz = np.gradient(rp, g.h, edge_order=1)
            aR = pR - fR - GAMMA_L * qR
            az = pz - fz - GAMMA_L * qz
            self.noL = (pR - fR, pz - fz)
            self.gauss_worst = max(getattr(self, "gauss_worst", 0.0), self.gauss_res)
        AR = interp(g, aR, self.Rp, self.zp)
        Az = interp(g, az, self.Rp, self.zp)
        AR[self.frozen] = 0.0
        Az[self.frozen] = 0.0
        return AR, Az

    def jacobian(self):
        g = self.grid
        Rp = self.Rp.reshape(g.nR, g.nz)
        zp = self.zp.reshape(g.nR, g.nz)
        dRdi, dRdj = np.gradient(Rp, g.h)
        dzdi, dzdj = np.gradient(zp, g.h)
        J2 = dRdi * dzdj - dRdj * dzdi
        J = (Rp / self.Rq.reshape(g.nR, g.nz)) * J2
        return J

    def diagnostics(self):
        g = self.grid
        J = self.jacobian()
        inner = np.zeros((g.nR, g.nz), bool)
        inner[1:-4, 4:-4] = True
        soft = (self.rho_tau0 < 0) & inner
        stiff = (self.rho_tau0 >= 0) & inner
        r = self.rfun(self.ti if self.a.mode == "mutate" else self.t)
        z1, z2 = zpos(r)
        halo = []
        for zc in (z1, z2):
            d = np.hypot(self.Rp, self.zp - zc)
            sel = (d < 100.0) & (self.m > 0)
            mass = float(self.m[sel].sum())
            cz = float((self.m[sel] * self.zp[sel]).sum() / mass) if mass > 0 else float("nan")
            halo.append({"mass": mass, "centroid_offset": cz - zc})
        rec = {"t": self.t, "r": r, "softJmin": float(J[soft].min()), "stiffJmin": float(J[stiff].min()),
               "disp_max": float(np.max(np.hypot(self.Rp - self.Rq, self.zp - self.zq))), "halo": halo,
               "gauss_it": int(getattr(self, "gauss_it", 0))}
        if self.first_cross is None and rec["softJmin"] <= 0:
            k = np.argmin(np.where(soft, J, np.inf))
            i, j = np.unravel_index(k, J.shape)
            kk = i * g.nz + j
            dgal = float(min(np.hypot(self.Rp[kk], self.zp[kk] - z1), np.hypot(self.Rp[kk], self.zp[kk] - z2)))
            self.first_cross = {"t_sc": self.t, "t_sc_minus_t0": self.t - T0, "q": [float(self.Rq[kk]), float(self.zq[kk])],
                                "x": [float(self.Rp[kk]), float(self.zp[kk])], "dist_gal": dgal}
        self.diag.append(rec)
        return rec

    def kdk(self):
        dt = self.dt
        mov = ~self.frozen
        self.vR[mov] += 0.5 * dt * self.acc[0][mov]
        self.vz[mov] += 0.5 * dt * self.acc[1][mov]
        self.Rp[mov] += dt * self.vR[mov]
        self.zp[mov] += dt * self.vz[mov]
        neg = self.Rp < 0
        self.Rp[neg] *= -1
        self.vR[neg] *= -1
        self.t += dt
        self.acc = self.accel(self.t)
        self.vR[mov] += 0.5 * dt * self.acc[0][mov]
        self.vz[mov] += 0.5 * dt * self.acc[1][mov]
        self.step += 1

    def state(self):
        return dict(t=self.t, step=self.step, Rp=self.Rp, zp=self.zp, vR=self.vR, vz=self.vz, aR=self.acc[0], az=self.acc[1],
                    Psi=self.Psi, diag=np.array(json.dumps(self.diag)), fc=np.array(json.dumps(self.first_cross)))

    def load(self, ck):
        d = np.load(ck, allow_pickle=False)
        self.t, self.step = float(d["t"]), int(d["step"])
        self.Rp, self.zp, self.vR, self.vz = d["Rp"].copy(), d["zp"].copy(), d["vR"].copy(), d["vz"].copy()
        self.acc = (d["aR"].copy(), d["az"].copy())
        self.Psi = d["Psi"].copy()
        self.diag = json.loads(str(d["diag"]))
        self.first_cross = json.loads(str(d["fc"]))


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--foot", default="canonical")
    p.add_argument("--orbit", default="O1")
    p.add_argument("--ti", type=float, default=6.0)
    p.add_argument("--h", type=float, default=20.0)
    p.add_argument("--dt", type=float, default=None)
    p.add_argument("--mode", default="sc", choices=["sc", "frozen", "mutate"])
    p.add_argument("--extend", action="store_true")
    p.add_argument("--tsteps", type=int, default=0)
    p.add_argument("--kill-at-step", type=int, default=0)
    p.add_argument("--tag", default="")
    p.add_argument("--resume", action="store_true")
    a = p.parse_args()
    if a.dt is None:
        a.dt = 0.02 if a.h >= 20 else 0.01
    name = a.tag or f"{a.mode}_{a.foot}_{a.orbit}_ti{a.ti:g}_h{a.h:g}"
    outdir = HERE / "runs"
    outdir.mkdir(exist_ok=True)
    res_path, ck_path = outdir / f"{name}.json", outdir / f"{name}.ckpt.npz"
    if a.resume and res_path.exists():
        sys.exit(0)
    T = time.time()
    run = Run(a)
    run.setup()
    if a.resume and ck_path.exists():
        run.load(ck_path)
    else:
        run.diagnostics()
    every = 10
    while run.t < run.t_ext - 1e-9:
        if STOP or (a.kill_at_step and run.step == a.kill_at_step and not a.resume):
            atomic_save(ck_path, **run.state())
            sys.exit(YIELD_EXIT)
        run.kdk()
        if run.step % every == 0 or run.t >= run.t_ext - 1e-9:
            run.diagnostics()
        if run.step % 50 == 0:
            atomic_save(ck_path, **run.state())
    d_end = [x for x in run.diag if x["t"] <= run.t_end + 1e-9]
    out = {"args": vars(a), "t_i": run.ti, "t_end": run.t_end, "t_ext": run.t_ext, "aqual": run.aqual_info,
           "eq_max_acc": run.eq_check, "eq_scale": run.eq_scale, "eq_rel": run.eq_check / run.eq_scale,
           "eq_rel_without_gammaL": run.eq_noL / run.eq_scale, "gauss_worst_residual": float(getattr(run, "gauss_worst", 0.0)),
           "n_soft": int(((run.rho_tau0 < 0)).sum()), "softJmin_to_t_end": min(x["softJmin"] for x in d_end),
           "t_softJmin": min(d_end, key=lambda x: x["softJmin"])["t"], "stiffJmin_to_t_end": min(x["stiffJmin"] for x in d_end),
           "softJmin_to_ext": min(x["softJmin"] for x in run.diag), "first_cross": run.first_cross,
           "disp_max": max(x["disp_max"] for x in run.diag), "halo_t_i": run.diag[0]["halo"], "halo_t_end": d_end[-1]["halo"],
           "diag": run.diag, "final_Rp": run.Rp.tolist() if a.tsteps else None, "final_zp": run.zp.tolist() if a.tsteps else None,
           "wall_s": time.time() - T, "maxrss_GB": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 2 ** 30}
    atomic_json(res_path, out)
    if ck_path.exists():
        ck_path.unlink()                                             # own checkpoint, result written
    print(json.dumps({k: out[k] for k in ("t_i", "t_end", "eq_rel", "n_soft", "softJmin_to_t_end", "t_softJmin",
                                           "stiffJmin_to_t_end", "softJmin_to_ext", "first_cross", "disp_max", "wall_s",
                                           "maxrss_GB")}, default=float))
    sys.exit(0)


if __name__ == "__main__":
    main()
