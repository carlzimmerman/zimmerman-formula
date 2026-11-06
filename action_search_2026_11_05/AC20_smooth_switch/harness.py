"""AC20 shared numerics: AC16's Lagrangian staggered scheme with a general stiffness force -d_x F'(Pi).

Pi carried by labels (cell charge m = Pi_0 da, Pi = m / width), switch state carried by the sign of m
(soft cells contribute F' = 0). gamma-type constants and a live inside the hprime callable.
Measures: Delta v_x at the interface label (one-sided least-squares slopes over 4 cells) at t_meas,
and t_inv, the first time a cell within |a| < 0.5 of the interface has width <= 0.
kappa = 1/2 FITTED; not theory closed.
"""
import numpy as np


def run(N, hprime, Pi0f=np.tanh, t_meas=0.05, t_max=2.0, ncell=4):
    an = np.linspace(-3.0, 3.0, N + 1)
    am = 0.5 * (an[1:] + an[:-1])
    da = an[1] - an[0]
    m = Pi0f(am) * da
    on = m > 0
    X = an.copy(); V = np.zeros(N + 1)

    def acc(X):
        w = np.diff(X)
        Pc = np.where(on, m / np.where(w > 0, w, np.inf), 0.0)
        h = np.where(on, hprime(np.maximum(Pc, 0.0)), 0.0)
        a_ = np.zeros_like(X)
        dxn = 0.5 * (X[2:] - X[:-2])
        a_[1:-1] = -(h[1:] - h[:-1]) / dxn
        return a_

    dt = 0.1 * da
    nmeas = int(round(t_meas / dt)); dt_m = t_meas / nmeas
    tcur, t_inv, Dvx, step = 0.0, None, None, 0
    i0 = N // 2
    near = np.abs(am) < 0.5
    while tcur < t_max - 1e-14:
        hs = dt_m if step < nmeas else dt
        k1x, k1v = V, acc(X)
        k2x, k2v = V + 0.5 * hs * k1v, acc(X + 0.5 * hs * k1x)
        k3x, k3v = V + 0.5 * hs * k2v, acc(X + 0.5 * hs * k2x)
        k4x, k4v = V + hs * k3v, acc(X + hs * k3x)
        X = X + hs / 6 * (k1x + 2 * k2x + 2 * k3x + k4x)
        V = V + hs / 6 * (k1v + 2 * k2v + 2 * k3v + k4v)
        tcur += hs; step += 1
        if step == nmeas:
            R = slice(i0, i0 + ncell + 1); L = slice(i0 - ncell, i0 + 1)
            sR = np.polyfit(X[R], V[R], 1)[0]; sL = np.polyfit(X[L], V[L], 1)[0]
            Dvx = float(sR - sL)
        if t_inv is None and np.any(np.diff(X)[near] <= 0):
            t_inv = tcur
        if t_inv is not None and Dvx is not None:
            break
    return dict(N=N, Dvx=Dvx, t_inv=t_inv)


def ladder(hprime, Ns=(400, 800, 1600, 3200), **kw):
    return [run(N, hprime, **kw) for N in Ns]
