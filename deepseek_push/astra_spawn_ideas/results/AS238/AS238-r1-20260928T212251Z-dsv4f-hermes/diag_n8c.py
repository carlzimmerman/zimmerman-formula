#!/usr/bin/env python3
"""Pointwise check with the QUARTIC probe: numeric L2raw vs sympy R2 at multiple (t,z) cells."""
import numpy as np
import sympy as sp
import as238_numeric as A238

t = sp.Symbol('t')
C, S = sp.symbols('C S')
kz, a0v, q0v, Twin = sp.symbols('kz a0 q0 Twin')
qsym = q0v*((t + Twin/2)/Twin)**2*(1 - (t + Twin/2)/Twin)**2
qd = sp.diff(qsym, t); qdd = sp.diff(qsym, t, 2)
R2 = -(4*C**2*kz**2*qsym**2 + 4*C**2*a0v**2*qsym*qdd + 3*C**2*a0v**2*qd**2
       - 3*S**2*kz**2*qsym**2)/(2*a0v**2)
R2f = sp.lambdify((t, C, S, kz, a0v, q0v, Twin), R2, 'numpy')

Twin_ = 0.3
q0_ = 0.02
a0_ = 1.3
Ns = (24, 24, 24, 41)
Lx = 2*np.pi
qfun = lambda tt, q0: q0*((tt + Twin_/2)/Twin_)**2*(1 - (tt + Twin_/2)/Twin_)**2

Lp, sgm = A238.curvature_action(Ns, Lx, a0_, 0.0, q0=0.0, q1=0.0, P_d=-3*0.11**2,
                                q_fn=(lambda tt: qfun(tt, q0_)))
Lm, _ = A238.curvature_action(Ns, Lx, a0_, 0.0, q0=0.0, q1=0.0, P_d=-3*0.11**2,
                              q_fn=(lambda tt: qfun(tt, -q0_)))
L0, _ = A238.curvature_action(Ns, Lx, a0_, 0.0, q0=0.0, q1=0.0, P_d=-3*0.11**2,
                              q_fn=(lambda tt: 0.0*tt))
L2raw = 0.5*(Lp + Lm) - L0

dz = Lx/Ns[2]
ts = (np.arange(Ns[3]) - Ns[3]//2)*(Twin_/(Ns[3]-1))
zgrid = (np.arange(Ns[2]) - Ns[2]//2)*dz
zc0 = int(np.argmin(np.abs(zgrid)))            # C=1 cell (z=0)
zc1 = int(np.argmin(np.abs(zgrid - np.pi/2)))  # S=1 cell (z=pi/2)
print("cell  t        z      L2raw_num      (M/2)sg R2_sym    car         ratio")
for it in range(0, Ns[3], 4):
    tt = ts[it]
    qv = q0_*((tt + Twin_/2)/Twin_)**2*(1 - (tt + Twin_/2)/Twin_)**2
    for zc, (Cv, Sv) in [(zc0, (1.0, 0.0)), (zc1, (0.0, 1.0))]:
        R2v = float(R2f(tt, Cv, Sv, 1.0, a0_, q0_, Twin_))
        sgg = sgm[it, 12, 12, zc]
        car = -(-3*0.11**2)*a0_**3*0.5*qv**2*Cv**2
        pred = 0.5*sgg*R2v + car
        num = L2raw[it, 12, 12, zc]
        print("%.4f %.3f %12.8f %14.8f %12.8f %.5f" % (tt, zgrid[zc], num, 0.5*sgg*R2v, car,
              num/(pred + 1e-30)))