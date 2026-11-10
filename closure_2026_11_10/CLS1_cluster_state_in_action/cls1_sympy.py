#!/usr/bin/env python3
"""CLS1 symbolic checks (sympy): KA3 (the clock dust as a fluid), S2a (no anisotropic / dispersion stress in the
clock sector), S2b (the multiplier and the radial khronon current of a stationary tilted clock).

Usage: python3 -I cls1_sympy.py OUT.json
Adopts nothing. kappa = 1/2 FITTED; not theory closed.
"""
import json
import sys

import sympy as sp

out = {}
Q, K, mu, r = sp.symbols('Q K mu r', positive=True)
x = Q - 1
LK = mu**2*x**2/(2*K)
n = sp.diff(LK, Q)                                   # charge
e = mu**2*(Q**2 - 1)/(2*K)                           # QX17 K5 energy density of the dust term
p = LK
out['KA3_charge_minus_mu2x_over_K'] = str(sp.simplify(n - mu**2*x/K))
out['KA3_e_minus_n(1+x/2)'] = str(sp.simplify(e - n*(1 + x/2)))
out['KA3_e_minus_(Q*LQ-L)'] = str(sp.simplify(e - (Q*n - LK)))
out['KA3_p_minus_n*x/2'] = str(sp.simplify(p - n*x/2))
out['KA3_enthalpy_per_charge_minus_Q'] = str(sp.simplify((e + p)/n - Q))
out['KA3_active_e+3p_minus_n(1+2x)'] = str(sp.simplify(e + 3*p - n*(1 + 2*x)))
# static Euler: dp/dr + (e+p) dlnN/dr = 0  with Q = Q(r), N = N(r)  <=>  d(N Q)/dr = 0
Qf, Nf = sp.Function('Q')(r), sp.Function('N')(r)
sub = {Q: Qf}
euler = sp.diff(p.subs(sub), r) + (e + p).subs(sub)*sp.diff(Nf, r)/Nf
tolman = n.subs(sub)*sp.diff(Nf*Qf, r)/Nf
out['KA3_euler_minus_n*d(NQ)/dr/N'] = str(sp.simplify(euler - tolman))

# S2a: T^Q_mn = g_mn L_K + (mu^2/K) Q x n_m n_n for a boosted unit timelike n in Minkowski (mostly plus)
vx, vy, vz = sp.symbols('v_x v_y v_z', real=True)
v2 = vx**2 + vy**2 + vz**2
gam = 1/sp.sqrt(1 - v2)
g = sp.diag(-1, 1, 1, 1)
nu = sp.Matrix([gam, gam*vx, gam*vy, gam*vz])        # n^m
nl = g*nu                                            # n_m
out['S2a_n_unit_minus_(-1)'] = str(sp.simplify((nu.T*g*nu)[0] + 1))
T = g*LK + (mu**2/K)*Q*x*(nl*nl.T)
h = g + nl*nl.T                                      # h_mn
hmix = sp.eye(4) + nu*nl.T                           # h^m_n
proj = hmix.T*T*hmix                                 # h_m^a T_ab h^b_n
res = sp.simplify(proj - LK*h)
out['S2a_projected_stress_minus_LK_h (max abs entry)'] = str(max([sp.simplify(c) for c in res], key=lambda c: 0 if c == 0 else 1))
out['S2a_nnT_minus_e'] = str(sp.simplify((nu.T*T*nu)[0] - e))
out['S2a_momentum_density_hnT'] = str(sp.simplify(hmix.T*T*nu))

# S2b: (E2) contracted with n gives the multiplier; in a stationary state n^m d_m = n^r d_r
lam, gL, Pi, KWp = sp.symbols('lambda gamma_L Pi KWp', real=True)
dl = sp.Matrix(sp.symbols('dl0:4', real=True))        # d_m l, l = ln Q (lower index)
dPi = sp.Matrix(sp.symbols('dPi0:4', real=True))
P = sp.Matrix(sp.symbols('P0:4', real=True))          # P_m (lower); constraint n^m P_m = 0 imposed below
ginv = g.inv()
E2 = -ginv*dl - KWp*(ginv*P) + gL*(ginv*dPi - Pi*ginv*dl) + lam*nu    # upper-index (E2), Phat absorbed in KWp P
contr = sp.expand((nl.T*E2)[0])                       # n_m E2^m
P0sol = sp.solve(sp.Eq((nu.T*P)[0], 0), P[0])[0]      # n^m P_m = 0
contr = sp.simplify(contr.subs(P[0], P0sol))
lam_sol = sp.solve(sp.Eq(contr, 0), lam)[0]
ndl = (nu.T*dl)[0]; ndPi = (nu.T*dPi)[0]
out['S2b_lambda_minus_[-(1+gL Pi) n.dl + gL n.dPi]'] = str(sp.simplify(lam_sol - (-(1 + gL*Pi)*ndl + gL*ndPi)))
# stationary tilted clock: only radial gradients (take r along x); then n.d = n^x d_x and lambda is proportional to n^x
dlr, dPir, rhoQ, Pr = sp.symbols('dl_r dPi_r rho_Q P_r', real=True)
lam_st = lam_sol.subs({dl[0]: 0, dl[2]: 0, dl[3]: 0, dPi[0]: 0, dPi[2]: 0, dPi[3]: 0, dl[1]: dlr, dPi[1]: dPir})
Jr = nu[1]*rhoQ - lam_st*Pr/Q
fac = sp.simplify(Jr/nu[1])
out['S2b_Jr_over_n^r'] = str(fac)
out['S2b_Jr_over_n^r_minus_[rhoQ + ((1+gL Pi) dl_r - gL dPi_r) P_r/Q]'] = str(
    sp.simplify(fac - (rhoQ + ((1 + gL*Pi)*dlr - gL*dPir)*Pr/Q)))

checks = [v for k, v in out.items() if 'minus' in k]
out['all_residuals_zero'] = all(v == '0' for v in checks)
out['note'] = 'Adopts nothing. kappa = 1/2 FITTED; not theory closed.'
json.dump(out, open(sys.argv[1], 'w'), indent=1)
for k, v in out.items():
    print(k, ':', v)

# Adopts nothing. kappa = 1/2 FITTED; not theory closed.
