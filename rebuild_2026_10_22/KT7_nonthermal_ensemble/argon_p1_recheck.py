#!/usr/bin/env python3
"""p = 1 Cassini: nu - 1 is non-zero only where y < 2, a corner dblquad steps over. Integrate that corner explicitly. Control: smooth exponential on the same explicit grid."""
import math, numpy as np
from scipy.optimize import brentq
GM = 6.6743e-11 * 1.98892e30
a0 = 9.3619e-11; et = 2.32e-10 / a0; qp = 5.2e-27 / (1.5 * a0**1.5 / math.sqrt(GM))
def nu_p1(y):  # mu(x) = x - x^2/4 for x <= 2, else 1; x mu = y -> x^2 - x^3/4 = y
    y = np.asarray(y, float); out = np.ones_like(y)
    for i, yy in np.ndenumerate(y):
        if yy < 2:
            out[i] = brentq(lambda x: x * x - x**3 / 4 - yy, 0, 2) / yy
    return out
def nu_exp(y):
    y = np.asarray(y, float); out = np.ones_like(y)
    for i, yy in np.ndenumerate(y):
        if yy < 40:
            out[i] = brentq(lambda x: x * (-math.expm1(-x)) - yy, 1e-12, yy + 50) / yy
    return out
def Q(nu, eN, cut, nv=1200, nm=500, vmax=None):
    vs = np.linspace(1e-4, vmax or math.sqrt(eN + cut) * 1.0001, nv)
    tot = np.zeros(nv)
    x, w = np.polynomial.legendre.leggauss(nm)
    for i, v in enumerate(vs):
        muc = (cut**2 - eN**2 - v**4) / (2 * eN * v * v)
        hi = min(muc, 1.0)
        if hi <= -1: continue
        mu = -1 + (x + 1) * (hi + 1) / 2
        D = np.sqrt(np.maximum(eN**2 + v**4 + 2 * eN * v * v * mu, 1e-30))
        tot[i] = np.sum(w * (nu(D) - 1) * (eN * (3 * mu - 5 * mu**3) + v * v * (1 - 3 * mu * mu))) * (hi + 1) / 2
    return abs(1.5 * np.trapz(tot, vs))
eP = brentq(lambda x: x * float(nu_p1(np.array([x]))[0]) - et, 1e-6, 1e4)
qq = Q(nu_p1, eP, 2.0)
print(f"p=1: eN {eP:.4f}, q {qq:.5f} = {qq/qp:.3f} x ceiling {'PASS' if qq < qp else 'FAIL'}")
for nv, nm in ((600, 200), (2400, 800)):
    print(f"  resolution {nv},{nm}: {Q(nu_p1, eP, 2.0, nv, nm)/qp:.3f} x")
eE = brentq(lambda x: x * float(nu_exp(np.array([x]))[0]) - et, 1e-6, 1e4)
qe = Q(nu_exp, eE, 40.0, 800, 120, vmax=7.0)
print(f"control exponential on this grid, y < 40: {qe/qp:.2f} x ceiling; dblquad gave 3.76")
