#!/usr/bin/env python3
"""Pointwise diagnosis of N8: exact numeric L2raw at cells vs sympy R^(2) formula."""
import numpy as np
import sympy as sp
import importlib.util

spec = importlib.util.spec_from_file_location('A238', 'as238_numeric.py')
# careful: importing runs the whole file; instead copy the kernel pieces:
import as238_numeric as A238  # will run the full script; acceptable for diagnosis

# reuse kernel: rebuild curvature_action via import (file runs; get globals)
out = A238.out

# sympy pointwise R^(2) for e=diag(1,-1,0), k=(0,0,kz), static a:
t = sp.Symbol('t')
C, S = sp.symbols('C S')
kz, a0v, q0v, Twin = sp.symbols('kz a0 q0 Twin')
qsym = q0v*sp.sin(sp.pi*(t + Twin/2)/Twin)**2
qd = sp.diff(qsym, t); qdd = sp.diff(qsym, t, 2)
R2 = -(4*C**2*kz**2*qsym**2 + 4*C**2*a0v**2*qsym*qdd + 3*C**2*a0v**2*qd**2
       - 3*S**2*kz**2*qsym**2)/(2*a0v**2)
R2f = sp.lambdify((t, C, S, kz, a0v, q0v, Twin), R2, 'numpy')

Twin_ = 0.3
q0_ = 0.02
a0_ = 1.3
Ns = (24, 24, 24, 41)
Lx = 2*np.pi
Lp, sgm = A238.curvature_action(Ns, Lx, a0_, 0.0, q0=0.0, q1=0.0, P_d=-3*0.11**2,
                                q_fn=(lambda tt: q0_*np.sin(np.pi*(tt + Twin_/2)/Twin_)**2))
Lm, _ = A238.curvature_action(Ns, Lx, a0_, 0.0, q0=0.0, q1=0.0, P_d=-3*0.11**2,
                              q_fn=(lambda tt: -q0_*np.sin(np.pi*(tt + Twin_/2)/Twin_)**2))
L0, _ = A238.curvature_action(Ns, Lx, a0_, 0.0, q0=0.0, q1=0.0, P_d=-3*0.11**2,
                              q_fn=(lambda tt: 0.0*tt))
L2raw = 0.5*(Lp + Lm) - L0      # = (M/2) (sqrt-g)^(2) R + R^(2) sqrt-g ... quadratic in q0
dtv = Twin_/(Ns[3]-1)
dz = Lx/Ns[2]
ts = (np.arange(Ns[3]) - Ns[3]//2)*dtv
zgrid = (np.arange(Ns[2]) - Ns[2]//2)*dz
zmid = Ns[2]//2
print("cell-level check: L2raw at z=0 vs (M/2) R^(2) sympy (times sqrt-g ~ a^3)")
for i in [0, 5, 10, 15, 20, 25, 30, 35, 40]:
    tt = ts[i]
    Cv = np.cos(2*np.pi*zgrid[zmid]/Lx)   # k=1, z at mid cell = -12*dz+.. zgrid[zmid]=-0.0
    Cv = 1.0 if abs(zgrid[zmid]) < 1e-12 else np.cos(zgrid[zmid])
    Sv = 0.0 if abs(zgrid[zmid]) < 1e-12 else np.sin(zgrid[zmid])
    R2v = R2f(tt, Cv, Sv, 1.0, a0_, q0_, Twin_)
    sgg = sgm[i, 12, 12, zmid]
    pred = (1.0/2)*sgg*R2v
    # carrier second variation: P_d * (delta^2 sqrt-g): -(P_d/4) a^3 e2 q^2 C^2 = -P_d a^3/2 q^2 C^2
    qq = float((q0_*np.sin(np.pi*(tt + Twin_/2)/Twin_)**2)**2)
    car = -(-3*0.11**2)*a0_**3*0.5*qq*Cv**2
    print("t=%.3f  L2raw=%.8f  (M/2)R2*sqrtg=%.8f  car=%.8f  sum=%.8f  ratio=%.4f"
          % (tt, L2raw[i, 12, 12, zmid], (1./2)*sgg*R2v, car,
             (1./2)*sgg*R2v + car, L2raw[i, 12, 12, zmid]/((1./2)*sgg*R2v + car + 1e-30)))