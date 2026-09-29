#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cfg72_stability -- Q3 helper: the linearised operator of a spherical Lagrangian ideal-gas cold fluid (gamma = 5/3) with self-gravity, a fixed central point
mass, a heat-bath exchange toward the CFG44/CFG48 target, about the STATIC TARGET state.  Everything is a discrete Lagrangian (shell) scheme whose
ideal part is conservative, so the ideal spectrum is imaginary (a control).  The Jacobian is built by COMPLEX-STEP differentiation of the nonlinear
vector field (no finite-difference noise).  Declared model: see the docstring of cfg72_lightcone_exchange.py, section Q3.

nodes r_0 < ... < r_N (node 0 pinned = inner wall), cells i = 0..N-1 between nodes i and i+1 with Lagrangian mass mu_i and internal energy U_i,
P_i = (2/3) U_i / V_i, V_i = (4 pi/3)(r_{i+1}^3 - r_i^3); node j (1..N) has mass m_j = (mu_{j-1} + mu_j)/2 (m_N = mu_{N-1}/2), shell gravity
g_j = G M_in,j / r_j^2, M_in,j = M_0 + sum_{1<=k<j} m_k (conservative: W = -G sum_{k<j} m_k m_j / r_j),  outer pressure P_ext held.
   dv_j/dt = kin [ 4 pi r_j^2 (P_{j-1} - P_j)/m_j - G M_in,j / r_j^2 ]                 (kin = +1; MUTATE c: kin = -1, a negative kinetic term)
   dU_i/dt = - P_i dV_i/dt + Q_i,   Q_i = (U^T_i(position) - U_i)/tau                 (tau = inf: ideal)
reading P (pressure bath, Eulerian target): U^T_i = U_eq,i (rc0/rc)^2  with rc = (r_i + r_{i+1})/2 the cell's CURRENT centre (target pressure a0 M/(8 pi r^2) evaluated at the
        cell's position, times the CURRENT volume ratio absorbed: U^T = (3/2) V_i P^T(rc)),
reading S (temperature bath, per-mass target): U^T_i = U_eq,i * s(rc)/s(rc0), s(r) = sqrt(1 + (r/r_M)^2)/r (= 2 sigma^2_T / (G M)), fixed shell mass mu_i (G4's sigma-slaved).
"""
import math
import numpy as np
from cfg72_common import *   # noqa


class ShellGas:
    def __init__(self, Mb, N=60, rin_x=0.05, rout=None, reading="P", tau=np.inf, kin=1.0, recip=False, r_led=0.0, eps_c=1.0):
        self.Mb, self.N, self.reading, self.tau, self.kin = Mb, N, reading, tau, kin
        self.recip, self.r_led, self.eps_c = recip, r_led, eps_c
        self.rM = r_M_kpc(Mb)
        self.rin = rin_x * self.rM
        self.rout = r_ta48_kpc(Mb) * 0.4 if rout is None else rout
        self.r0 = np.geomspace(self.rin, self.rout, N + 1)
        Mc = lambda r: Mb * (np.sqrt(1.0 + (r / self.rM) ** 2) - 1.0)          # target cold-fluid mass (CFG44: M_c = M (sqrt(1+x^2) - 1))
        self.mu = np.diff(Mc(self.r0))                                          # cell masses
        m = np.zeros(N + 1)
        m[0] = 0.5 * self.mu[0]
        m[1:N] = 0.5 * (self.mu[:-1] + self.mu[1:])
        m[N] = 0.5 * self.mu[N - 1]
        self.m = m                                                              # node masses (index 0 = pinned)
        self.M0 = Mb + Mc(self.r0[0]) + m[0]
        self.Min = np.zeros(N + 1)
        acc = self.M0
        for j in range(1, N + 1):
            self.Min[j] = acc
            acc += m[j]
        rc0 = 0.5 * (self.r0[:-1] + self.r0[1:])
        self.rc0 = rc0
        V0 = 4 * math.pi / 3 * (self.r0[1:] ** 3 - self.r0[:-1] ** 3)
        # target edge pressure P_ext = a0 M/(8 pi r_out^2) (CFG44: P = a0 M_b/(8 pi r^2))
        self.Pext = A0 * Mb / (8 * math.pi * self.rout ** 2)
        P = np.zeros(N)
        P_out = self.Pext
        for j in range(N, 0, -1):
            P_in = P_out + G * self.m[j] * self.Min[j] / (4 * math.pi * self.r0[j] ** 4)     # discrete node balance
            P[j - 1] = P_in
            P_out = P_in
        self.Peq = P
        self.Ueq = 1.5 * P * V0
        self.V0 = V0
        Ptarget = A0 * Mb / (8 * math.pi * rc0 ** 2)
        self.disc_err = float(np.max(np.abs(P / Ptarget - 1.0)))                # discretisation error of the hydrostatic target
        self.sfun = lambda rc: np.sqrt(1.0 + (rc / self.rM) ** 2) / rc
        self.imbalance = None
        self.dP_eq = 0.0
        if recip:
            self._solve_reciprocal_equilibrium()

    # ------------------------------------------------------------------------------------------- reciprocal completion (disclosed addition, T5)
    def _kappa(self):
        """F_i = (kappa_i/2)(U_i - U^T_i)^2 with kappa_i = c_f/dr_i, c_f = eps_c/(vartheta M_b): the exchange free energy of CFG70 written on the cells."""
        cf = self.eps_c / (0.75 * A0 * self.Mb)
        return cf / np.diff(self.r0)

    def UT_grad(self, r_nodes, amp):
        """target cell energy U^T_i(position) and its derivatives w.r.t. the lower / upper node radius; amp = target amplitude per cell."""
        r = r_nodes
        rc = 0.5 * (r[:-1] + r[1:])
        if self.reading == "P":
            V = 4 * math.pi / 3 * (r[1:] ** 3 - r[:-1] ** 3)
            PT = amp * (self.rc0 / rc) ** 2
            dPT = -2.0 * PT / rc
            UT = 1.5 * V * PT
            dlo = 1.5 * (-4 * math.pi * r[:-1] ** 2 * PT + V * dPT * 0.5)
            dhi = 1.5 * (4 * math.pi * r[1:] ** 2 * PT + V * dPT * 0.5)
        else:
            s0 = self.sfun(self.rc0)
            sr = self.sfun(rc)
            x2 = (rc / self.rM) ** 2
            UT = amp * sr / s0
            dU = amp * (-sr / (rc * (1.0 + x2))) / s0
            dlo = 0.5 * dU
            dhi = 0.5 * dU
        return UT, dlo, dhi

    def _node_force_static(self, amp):
        kap = self._kappa()
        UT, dlo, dhi = self.UT_grad(self.r0.astype(float), amp)
        eps = -self.r_led / kap                                       # static misfit U - U^T
        f0 = np.zeros(self.N + 1)
        for j in range(1, self.N + 1):
            f0[j] = kap[j - 1] * eps[j - 1] * dhi[j - 1] + (kap[j] * eps[j] * dlo[j] if j < self.N else 0.0)
        return f0

    def _solve_reciprocal_equilibrium(self):
        N = self.N
        kap = self._kappa()
        amp0 = self.Peq.copy() if self.reading == "P" else self.Ueq.copy()
        amp = amp0.copy()
        for it in range(200):
            f0 = self._node_force_static(amp)
            if it == 0:
                pres = 4 * math.pi * self.r0[1:] ** 2 * np.concatenate([self.Peq[:-1] - self.Peq[1:], [self.Peq[-1] - self.Pext]])
                self.imbalance = float(np.max(np.abs(f0[1:])) / np.max(np.abs(pres)))
            P = np.zeros(N)
            P_out = self.Pext
            for j in range(N, 0, -1):
                P_in = P_out + (G * self.m[j] * self.Min[j] / self.r0[j] ** 2 - f0[j]) / (4 * math.pi * self.r0[j] ** 2)
                P[j - 1] = P_in
                P_out = P_in
            U = 1.5 * P * self.V0
            Utarget = U + self.r_led / kap
            amp_new = (Utarget / (1.5 * self.V0)) if self.reading == "P" else Utarget
            if np.max(np.abs(amp_new / amp - 1)) < 1e-13:
                amp = amp_new
                break
            amp = amp_new
        self.amp = amp
        self.P_eq_r = P
        self.Peq_shift = P
        self.Ueq = U
        self.dP_eq = float(np.max(np.abs(P / self.Peq - 1.0)))

    def y0(self):
        return np.concatenate([self.r0[1:], np.zeros(self.N), self.Ueq]).astype(complex)

    def f(self, y):
        N = self.N
        r = np.concatenate([[self.r0[0]], y[:N]])
        v = np.concatenate([[0.0], y[N:2 * N]])
        U = y[2 * N:]
        V = 4 * math.pi / 3 * (r[1:] ** 3 - r[:-1] ** 3)
        P = (2.0 / 3.0) * U / V
        Pfull = np.concatenate([P, [self.Pext]])
        acc = 4 * math.pi * r[1:] ** 2 * (Pfull[:-1] - Pfull[1:]) / self.m[1:] - G * self.Min[1:] / r[1:] ** 2
        Vdot = 4 * math.pi * (r[1:] ** 2 * v[1:] - r[:-1] ** 2 * v[:-1])
        dU = -P * Vdot
        if np.isfinite(self.tau):
            rc = 0.5 * (r[:-1] + r[1:])
            if self.recip:
                UT, dlo, dhi = self.UT_grad(r, self.amp)
                kap = self._kappa()
                dU = dU + (UT - U) / self.tau - self.r_led / (self.tau * kap)
                eps = U - UT
                fnode = np.zeros(self.N + 1, dtype=complex)
                fnode[:self.N] += kap * eps * dlo                     # lower node of each cell (nodes 0..N-1)
                fnode[1:] += kap * eps * dhi                          # upper node of each cell (nodes 1..N)
                acc = acc + fnode[1:] / self.m[1:]
            else:
                if self.reading == "P":
                    UT = 1.5 * V * (self.Peq * (self.rc0 / rc) ** 2)
                elif self.reading == "L":                              # label-slaved bath: every shell relaxes to its OWN constant energy (no position dependence)
                    UT = self.Ueq
                else:
                    UT = self.Ueq * self.sfun(rc) / self.sfun(self.rc0)
                dU = dU + (UT - U) / self.tau
        return np.concatenate([v[1:], self.kin * acc, dU])

    def jac(self):
        y0 = self.y0()
        n = len(y0)
        J = np.zeros((n, n))
        for k in range(n):
            h = 1e-20 * max(abs(y0[k]), 1e-30)
            yp = y0.copy()
            yp[k] += 1j * h
            J[:, k] = np.imag(self.f(yp)) / h
        return J

    def residual(self):
        return self.f(self.y0())

    def spectrum(self):
        J = self.jac()
        ev = np.linalg.eigvals(J)
        return ev, J
