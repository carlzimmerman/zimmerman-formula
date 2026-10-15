#!/usr/bin/env python3
"""scratch diagnostic for AG1 C6 direction failure.
Three independent reads:
 (1) q(x) profile of the lambda=0 regular mode solution out to x=12 (does it cross zero past 6.45?)
 (2) M-turning point: M~(xi) = xi^2 psi'(xi) e^{-psi/2} at fixed (P_ext, c_s) — direction past 6.45
 (3) eigenvalue by DIRECT residual scan: R(lam) = q'(x_R) + psi'(x_R) q(x_R), lowest root in lam.
"""
import math
import numpy as np
from scipy.integrate import solve_ivp

X0 = 1e-6


def rhs_bg(x, y):
    psi, dpsi = y
    return [dpsi, math.exp(-psi) - 2.0 * dpsi / x]


bg = solve_ivp(rhs_bg, (X0, 14.0), [X0**2 / 6, X0 / 3], method="DOP853",
               rtol=1e-13, atol=1e-15, dense_output=True)


def shoot(lam, xmax):
    def rhs(x, y):
        psi, dpsi, q, dq = y
        return [dpsi, math.exp(-psi) - 2 * dpsi / x,
                dq, -(dpsi - 2 / x) * dq - (math.exp(-psi) + lam) * q]
    s = solve_ivp(rhs, (X0, xmax), [X0**2 / 6, X0 / 3, X0**3, 3 * X0**2],
                  method="DOP853", rtol=1e-13, atol=1e-16, dense_output=True)
    return s


print("(1) lambda=0 regular solution: q(x), F(x) = q' + psi' q")
s0 = shoot(0.0, 12.0)
for x in [5.0, 6.0, 6.4, 6.4508, 6.5, 6.6, 7.0, 7.5, 8.0, 9.0, 10.0, 11.0, 12.0]:
    psi, dpsi, q, dq = s0.sol(x)
    print(f"   x={x:7.4f}  q={q:+14.6e}  q'={dq:+14.6e}  F={dq + dpsi * q:+14.6e}")

print("\n(2) M~(xi) = xi^2 psi' e^{-psi/2} (fixed P_ext, c_s):")
prev = None
for x in np.arange(4.0, 10.01, 0.5):
    psi, dpsi = bg.sol(x)[:2]
    M = x**2 * dpsi * math.exp(-psi / 2)
    mark = "" if prev is None else ("up" if M > prev else "DOWN")
    print(f"   xi={x:5.2f}  M~={M:10.6f}  {mark}")
    prev = M

print("\n(3) direct residual scan R(lam) at fixed x_R; lowest roots:")
for xR in (5.5, 6.4508, 7.0, 8.0, 10.0):
    psiR, dpsiR = bg.sol(xR)[:2]
    lams = np.linspace(-1.0, 1.5, 501)
    Rs = []
    for lam in lams:
        s = shoot(lam, xR)
        q, dq = s.sol(xR)[2:]
        Rs.append(dq + dpsiR * q)
    Rs = np.array(Rs)
    sgn = np.sign(Rs)
    idx = np.where(np.diff(sgn) != 0)[0]
    roots = []
    from scipy.optimize import brentq

    def R(lam):
        s = shoot(lam, xR)
        q, dq = s.sol(xR)[2:]
        return dq + dpsiR * q

    for i in idx[:3]:
        try:
            roots.append(brentq(R, lams[i], lams[i + 1], xtol=1e-12))
        except Exception as e:
            roots.append(str(e))
    # zero count of the lambda=0 solution inside (0, xR)
    ts = np.linspace(1e-3, xR, 6001)
    qs = s0.sol(ts)[2] if xR <= 12 else None
    nzeros = int(np.sum(np.diff(np.sign(qs)) != 0))
    print(f"   x_R={xR:7.4f}: lowest R-roots lam = {roots}   interior zeros of q(lam=0) on (0,{xR}]: {nzeros}")
