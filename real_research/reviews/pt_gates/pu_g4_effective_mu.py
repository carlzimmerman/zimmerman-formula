#!/usr/bin/env python3
"""G4: integrate out / adiabatically eliminate the fast PU mode -> what inertia law do slow orbits obey?

(1) EXACT circular-orbit identity (symbolic, general k):  a [1 - (Omega^2/w^2) k'(y)] = g_N
    => mu_eff = 1 - (Omega/w_eff)^2,  w_eff^2 = w^2/k'(y).  SIGN: k'>0 => softening (MOND-direction).
(2) Selector: 1-mu ~ Omega^2 k'(a^2/a0^2); monomial k'~y^(p-1): 1-mu ~ a^(2p-1)/R (Omega^2=a/R).
    p=1/2 (matches framework tail 1-mu=a0/2a in a) => 1-mu = beta*a0/(w^2 R): pure 1/R (Grumiller-
    Rindler form, PRL 105,211303) AND kappa_par = k'+2yk'' = 0 exactly (marginal longitudinal mode).
(3) Required k' to reproduce mu_fw is R-dependent => NOT a function: no local k works (G0 echo).
(4) NUMERICS both ways: (a) w_eff=5*Omega orbit -> mu_num matches 1-(Omega/w)^2 to <0.5%;
    (b) w_eff=1.8*Omega0 (past EP) -> exponential runaway at the predicted rate.
"""
import sympy as sp
import numpy as np
from scipy.integrate import solve_ivp

# ---- (1) exact identity, general k'
t, R, Om, w, m, a0s, gN = sp.symbols('t R Omega w m a0 g_N', positive=True)
kpf = sp.Function('kprime')
x1, x2 = R*sp.cos(Om*t), R*sp.sin(Om*t)
y_traj = sp.simplify((sp.diff(x1,t,2)**2 + sp.diff(x2,t,2)**2)/a0s**2)
assert sp.diff(y_traj, t) == 0                      # y const on circular orbit
Y = sp.symbols('Y', positive=True)
lhs1 = m*sp.diff(x1,t,2) + (m/w**2)*sp.diff(kpf(Y)*sp.diff(x1,t,2), t, 2)
targ = -m*Om**2*x1*(1 - (Om**2/w**2)*kpf(Y))
assert sp.simplify(lhs1 - targ) == 0
print("(1) EXACT (no adiabatic approx): a [1 - (Omega^2/w^2) k'(y)] = g_N on circular orbits.")
print("    mu_eff = 1-(Omega/w_eff)^2, w_eff^2=w^2/k'.  k'>0 => SIGN = softening (MOND-direction, not anti-MOND).")

# ---- (2) tail-match exponent and its degeneracy
yv = sp.symbols('y', positive=True)
k_tail = 2*sp.sqrt(yv)                               # k' = y^(-1/2): 1-mu = (Om^2/w^2)/sqrt(y) = a0*Om^2/(w^2 a) = a0/(w^2 R)
kappa_par = sp.simplify(sp.diff(k_tail, yv) + 2*yv*sp.diff(k_tail, yv, 2))
assert kappa_par == 0
print("(2) tail-match k=2*sqrt(y) (1-mu ~ a^-1, framework tail exponent): 1-mu = a0/(w^2 R) -> pure 1/R;")
print("    kappa_parallel = k'+2yk'' = 0 EXACTLY: longitudinal PU term degenerates (marginal/cuscuton edge).")

# ---- (3) required k' is not a function of y alone
mu_fw = lambda a: (np.sqrt(a0n**2 + 4*a**2) - a0n)/(2*a)
a0n = 9.36e-11
a_test = 0.5*a0n; wn = 3.08e-16
for Rn in [6.2e19, 6.2e20]:   # 2 kpc vs 20 kpc at the same a
    kreq = (wn**2*Rn/a_test)*(1 - mu_fw(a_test))
    print(f"    required k'(y={0.25:.2f}) at R={Rn/3.086e19:.0f} kpc: {kreq:.3e}")
print("    same y, required k' differs by 10x = R1/R2 => k' CANNOT be a function of y. No local k gives mu_fw.")

# ---- (4a) numeric orbit, k'=1, w = 5*Omega: verify mu_eff = 1-(Omega/w)^2 = 0.96
GM = 1.0; Rn = 1.0
from scipy.optimize import brentq
Omn = brentq(lambda O: O**2*Rn*(1-(1/5.0)**2) - GM/Rn**2, 0.5, 2.0)  # w=5*Om exactly
wn4 = 5.0*Omn
def rhs(t_, s):
    x = s[0:2]; v = s[2:4]; A = s[4:6]; J = s[6:8]
    r3 = (x[0]**2+x[1]**2)**1.5
    g = -GM*x/r3
    return np.concatenate([v, A, J, wn4**2*(g - A)])
s0 = np.array([Rn,0, 0,Omn*Rn, -Omn**2*Rn,0, 0,-Omn**3*Rn])
T = 2*np.pi/Omn
sol = solve_ivp(rhs, [0, 30*T], s0, rtol=1e-11, atol=1e-12, dense_output=True)
rr = np.hypot(sol.y[0], sol.y[1])
mu_num = GM/Rn**2/(Omn**2*Rn)   # by construction; verify orbit STAYS on it
drift = abs(rr.max()-rr.min())/Rn
phi_end = np.arctan2(sol.y[1,-1], sol.y[0,-1]) % (2*np.pi)
phi_pred = (Omn*30*T) % (2*np.pi)
dphi = abs(phi_end-phi_pred); dphi = min(dphi, 2*np.pi-dphi)
print(f"(4a) w_eff=5*Omega, 30 orbits: radius drift {drift:.2e}, phase err {dphi:.2e} rad -> mu_eff = 1-(Om/w)^2 = {1-(Omn/wn4)**2:.4f} CONFIRMED (softening, stable)")
assert drift < 1e-6 and dphi < 1e-4

# ---- (4b) past the exceptional point: w = 1.8*Omega0 in a well -> runaway at predicted rate
W0 = 1.0; wb = 1.8*W0
lam = np.roots([1, 0, wb**2, 0, wb**2*W0**2])
gr_pred = max(lam.real)
def rhs1d(t_, s):
    x, v, A, J = s
    return [v, A, J, -wb**2*(A + W0**2*x)]
solb = solve_ivp(rhs1d, [0, 40.0], [1.0, 0, -0.5, 0], rtol=1e-10, atol=1e-12, dense_output=True)
tt = np.linspace(25, 40, 400); xx = np.abs(solb.sol(tt)[0])
gr_num = np.polyfit(tt, np.log(np.maximum(xx, 1e-30)), 1)[0]
print(f"(4b) w=1.8*Omega0 (< 2*Omega0): predicted growth {gr_pred:.4f}, measured {gr_num:.4f} per unit time")
print(f"     e-fold per orbit = {gr_pred*2*np.pi/W0:.2f}: MOND-zone orbits disrupt in ~1 orbit at tree level.")
assert abs(gr_num-gr_pred)/gr_pred < 0.05

print("\nG4 VERDICT: DECOY CONFIRMED. Slow dynamics obeys mu_eff = 1-(Omega/w_eff(a))^2:")
print("  SIGN   = softening (correct MOND direction, for any k'>0);")
print("  SHAPE  = frequency-selected, not acceleration-selected: exponent a^(2p-1)/R, never a pure mu(a/a0);")
print("  best exponent (p=1/2, framework-tail match) collapses to a 1/R Rindler force with kappa_par=0;")
print("  O(1) softening (mu<3/4) requires w_eff<2*Omega = past the EP = runaway (4b). Not mu_fw, not anti-MOND: anti-UNIVERSAL.")
print("EXIT 0")
