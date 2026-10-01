#!/usr/bin/env python3
"""Resolve: numerically evaluate each term of <R2> on the grid and compare with the
analytic A0/C0/B0 decomposition vs the L2raw array mean."""
import numpy as np
import as238_numeric as A238

Twin_ = 0.3
q0_ = 0.02
a0_ = 1.3
Ns = (24, 24, 24, 41)
Lx = 2*np.pi
dtv_ = Twin_/(Ns[3]-1)
ts = (np.arange(Ns[3]) - Ns[3]//2)*dtv_

# discrete q, qd (4th-order stencil), qdd on the time axis:
u = (ts + Twin_/2)/Twin_
q = q0_*u**2*(1-u)**2
def d4t(f):
    o = np.zeros_like(f)
    o[2:-2] = (f[4:] - 8*f[3:-1] + 8*f[1:-3] - f[:-4])/(12*dtv_)
    o[0] = (-25*f[0] + 48*f[1] - 36*f[2] + 16*f[3] - 3*f[4])/(12*dtv_)
    o[1] = (-3*f[0] - 10*f[1] + 18*f[2] - 6*f[3] + f[4])/(12*dtv_)
    o[-1] = (25*f[-1] - 48*f[-2] + 36*f[-3] - 16*f[-4] + 3*f[-5])/(12*dtv_)
    o[-2] = (3*f[-1] + 10*f[-2] - 18*f[-3] + 6*f[-4] - f[-5])/(12*dtv_)
    return o
qd = d4t(q); qdd = d4t(qd)
dz = Lx/Ns[2]
zgrid = (np.arange(Ns[2]) - Ns[2]//2)*dz
Cg2 = np.cos(zgrid)**2; Sg2 = np.sin(zgrid)**2
n = Ns[3]*Ns[2]
m_qd2 = np.mean(qd**2)
m_q2 = np.mean(q**2)
m_qddq = np.mean(qdd*q)
# <R2> = sum_z [-2 C^2 k^2 q^2/a^2 - 2 C^2 q qdd - 1.5 C^2 qd^2 + 1.5 S^2 k^2 q^2/a^2]
mR2 = (-2*np.mean(Cg2)*1.0**2*np.mean(q**2)/a0_**2
       - 2*np.mean(Cg2)*m_qddq
       - 1.5*np.mean(Cg2)*m_qd2
       + 1.5*np.mean(Sg2)*1.0**2*np.mean(q**2)/a0_**2)
print("grid means: <qd^2>=%.6f  <q^2>=%.6f  <qddq>=%.6f" % (m_qd2, m_q2, m_qddq))
print("analytic  : A0 0.7054673721  B0 0.0052910053  C0 -0.7054673721")
print("<R2> grid-computed   =", mR2)
brack = -0.75*m_qd2 - m_qddq - 0.25*m_q2/a0_**2
print("<R2> as [-.75 qd2 - qddq - .25 q2/a^2] =", brack)
print("ratio:", mR2/brack)
print("L2raw mean (should be (M/2) a^3 <R2> + car):", 0.5*a0_**3*mR2)
print("measured L2raw mean:", 2.23351918510049e-05)