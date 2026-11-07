#!/usr/bin/env python3
"""FS1 numpy reference implementation of scheme S (CRITERIA.md f716e2f98f), for K0 only (core = reference).
Same algorithm as fs1_core.c, written independently in numpy. kappa = 1/2 FITTED; not theory closed.
"""
import math
import numpy as np
from scipy.special import erf


def _herm(s, J0, d0, J1, d1, dt):
    return (2 * s**3 - 3 * s**2 + 1) * J0 + (s**3 - 2 * s**2 + s) * dt * d0 + (-2 * s**3 + 3 * s**2) * J1 + (s**3 - s**2) * dt * d1


def _hroot(J0, d0, J1, d1, dt, thr):
    if J0 - thr <= 0:
        return 0.0
    sp = 0.0
    for k in range(1, 65):
        s = k / 64.0
        if _herm(s, J0, d0, J1, d1, dt) - thr <= 0:
            lo, hi = sp, s
            for _ in range(60):
                m = 0.5 * (lo + hi)
                if _herm(m, J0, d0, J1, d1, dt) - thr <= 0:
                    hi = m
                else:
                    lo = m
            return hi
        sp = s
    return -1.0


def run(N, M1, Pi0, s2, gam, sheet=1.0, cq=1.0, cl=0.5, cfl=0.4, fsheet=0.05, tmax=6.0, jthr=1e-3, edge_b=0,
        WB=1e-3, X0=(-3.0, -0.05), EDGE=0.05):
    q = np.linspace(X0[0], X0[1], N + 1); dq = q[1] - q[0]
    i0, i1 = int(EDGE * N), int((1 - EDGE) * N)
    qc = 0.5 * (q[1:] + q[:-1]); e = EDGE * (q[-1] - q[0])
    T = 0.5 * (np.tanh((qc - q[0] - 0.5 * e) / (0.1 * e)) - np.tanh((qc - q[-1] + 0.5 * e) / (0.1 * e)))
    Pic = s2 + (Pi0 - s2) * T
    mnode = np.zeros(N + 1); mnode[:-1] += Pic * dq / 2; mnode[1:] += Pic * dq / 2
    K = gam * np.maximum(Pic, 0.0)
    if edge_b:
        K[:i0] = 0.0; K[i1:] = 0.0
    press = gam > 0 and K.max() > 0
    pg = gam * max(s2, 0.0) / 2
    minv = np.full(N + 1, 1.0 / dq); minv[0] = minv[-1] = 2.0 / dq
    Mtot = float(np.cumsum(mnode)[-1])
    s2q = math.sqrt(2) * WB

    def acc(x, v):
        order = np.argsort(x, kind="stable")
        cs = np.cumsum(mnode[order]) - mnode[order] / 2
        left = np.empty(N + 1); left[order] = cs
        xmin, xmax = x[order[0]], x[order[-1]]
        a = M1 * (left - s2 * (x - xmin) - (Mtot - s2 * (xmax - xmin)) / 2) - 0.5 * sheet * erf(x / s2q)
        if not press:
            return a, 0.0, None
        J = np.diff(x) / dq; dv = np.diff(v)
        pos = (J > 0) & (K > 0); Jp = np.where(pos, J, 1.0)
        p = np.where(pos, K / (2 * Jp * Jp), 0.0); C = np.where(pos, np.sqrt(K / Jp**3), 0.0)
        dvl = np.concatenate([[dv[0]], dv[:-1]]); dvr = np.concatenate([dv[1:], [dv[-1]]])
        with np.errstate(divide="ignore", invalid="ignore"):
            rl = np.where(dv != 0, dvl / dv, 1.0); rr = np.where(dv != 0, dvr / dv, 1.0)
        psi = np.clip(np.minimum(np.minimum(0.5 * (rl + rr), 2 * rl), 2 * rr), 0.0, 1.0)
        Q = np.where(pos & (dv < 0), (1 - psi) * (cq * dv * dv / Jp + cl * C * np.abs(dv)), 0.0)
        Pn = np.concatenate([[pg], p + Q, [pg]])
        a = a - (Pn[1:] - Pn[:-1]) * minv
        sig = np.where(pos, C + 2 * cq * (1 - psi) * np.abs(np.minimum(dv, 0)) / Jp, 0.0)
        return a, float(sig.max()), Q

    x = q.copy(); v = np.ones(N + 1); t = 0.0; jmin = 1.0; tf = None; tfa = None; ns = 0
    a, smax, _ = acc(x, v)
    while t < tmax:
        vm = np.abs(v).max(); dt = fsheet * WB / vm
        if smax > 0 and cfl * dq / smax < dt:
            dt = cfl * dq / smax
        if tmax - t < dt:
            dt = tmax - t
        x1 = x + dt * v; v1 = v + dt * a
        a1, _, _ = acc(x1, v1)
        x2 = 0.75 * x + 0.25 * (x1 + dt * v1); v2 = 0.75 * v + 0.25 * (v1 + dt * a1)
        a2, _, _ = acc(x2, v2)
        xn = x / 3 + 2.0 / 3 * (x2 + dt * v2); vn = v / 3 + 2.0 / 3 * (v2 + dt * a2)
        J0 = np.diff(x) / dq; J1 = np.diff(xn) / dq; d0 = np.diff(v) / dq; d1 = np.diff(vn) / dq
        lo = np.minimum(J0, J1) - dt * np.maximum(np.abs(d0), np.abs(d1))
        best, besta, bcell = 2.0, 2.0, None
        for i in np.nonzero((lo <= jthr) & (J0 > jthr))[0]:
            s = _hroot(J0[i], d0[i], J1[i], d1[i], dt, jthr)
            if s < 0:
                continue
            if i0 <= i < i1 and s < best:
                best, bcell = s, int(i)
            besta = min(besta, s)
        if tfa is None and besta < 2.0:
            tfa = t + besta * dt
        if bcell is not None:
            tf = t + best * dt; jmin = jthr; ns += 1
            break
        jmin = min(jmin, float(J1[i0:i1].min()))
        x, v = xn, vn; t += dt; ns += 1
        a, smax, _ = acc(x, v)
    return dict(t_fold=tf, t_fold_all=tfa, J_min=jmin, nstep=ns, t_end=t if tf is None else tf)
