#!/usr/bin/env python3
"""Z-sum sanity: grid-sum of sympy R2(C(z),S(z)) vs the numeric L2raw array mean."""
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
print("numeric mean(L2raw)          =", L2raw.mean())

# grid-sum of the sympy formula on the same cells (with spatial stencil-exact C,S):
dz = Lx/Ns[2]
dtv_ = Twin_/(Ns[3]-1)
ts = (np.arange(Ns[3]) - Ns[3]//2)*dtv_
zgrid = (np.arange(Ns[2]) - Ns[2]//2)*dz
Cg = np.cos(zgrid); Sg = np.sin(zgrid)
tot = 0.0
for it in range(Ns[3]):
    for iz in range(Ns[2]):
        R2v = float(R2f(ts[it], Cg[iz], Sg[iz], 1.0, a0_, q0_, Twin_))
        tot += 0.5*sgm[it, 12, 12, iz]*R2v
print("sympy-grid sum 0.5 sg R2    =", tot/(Ns[3]*Ns[2]))
# carrier:
qq = q0_*((ts + Twin_/2)/Twin_)**2*(1 - (ts + Twin_/2)/Twin_)**2
car = -(-3*0.11**2)*a0_**3*0.5*np.mean(qq**2)*np.mean(Cg**2)
print("carrier mean                =", car)
print("expect total (sympy grid + car) =", tot/(Ns[3]*Ns[2]) + car)
print("mean C^2 over grid          =", float(np.mean(Cg**2)), " mean S^2 =", float(np.mean(Sg**2)))