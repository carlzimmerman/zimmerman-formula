#!/usr/bin/env python3
"""KT5 guard: routeA at eta = 2, the anchor's own eta, with the same integral settings as kt5.py."""
import math, numpy as np
from scipy import integrate
from scipy.optimize import brentq
def nu(y):
    y = np.asarray(y, float); s = np.sqrt(y)
    out = np.where(s < 1e-8, 1.0 / np.maximum(s, 1e-300), 1.0 / (1.0 - np.exp(-np.minimum(s, 700.0))))
    return np.where(s > 40.0, 1.0 + np.exp(-np.minimum(s, 700.0)), out)
def q(et, vmax=400.0):
    eN = brentq(lambda x: x * float(nu(x)) - et, 1e-12, 1e10, xtol=1e-15, rtol=8.9e-16)
    def ig(mu, v):
        D = eN * eN + v**4 + 2.0 * eN * v * v * mu
        if D <= 0: return 0.0
        return (float(nu(math.sqrt(D))) - 1.0) * (eN * (3 * mu - 5 * mu**3) + v * v * (1 - 3 * mu * mu))
    return abs(1.5 * integrate.dblquad(ig, 0.0, vmax, lambda v: -1.0, lambda v: 1.0, epsabs=1e-7, epsrel=1e-5)[0])
print(f"routeA q(eta=2) = {q(2.0):.4f}, anchor 0.221")
