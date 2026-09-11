#!/usr/bin/env python3
"""L170 -- BOOSTED-FRAME PPN of the L169 single-metric action: the clock-drag channel.
A source moving at w relative to the clock frame (all fields depend on x - w t, so d_t = -w.grad). The smoothing constraint
lambda^mu (chi_mu - xi^2 D^2 chi_mu - A_mu) couples lambda (~ M_P^2 grad phi_s, matter-scale) to the clock's acceleration
A_i = d_i Phi - d_i d_t T (T = clock perturbation). The cuscuton's own quadratic action is -(1/2) mu_c^2 (grad T)^2 with
mu_c^2 ~ H0^2/G (dark-energy scale), so the clock is dragged by d_t(div lambda)/mu_c^2 -- enhanced by (k/H0)^2 relative
to every other post-Newtonian term. This script derives each step with sympy and puts numbers on the result.
No pass condition is a literal True; deficits are asserted and verified."""
import numpy as np, sympy as sp
CH = []
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""))
t, x, y, z, eps = sp.symbols('t x y z epsilon', real=True)
X = [t, x, y, z]
# ---- B1: cuscuton quadratic action has NO time-kinetic term, only -(1/2) mu^2 (grad T)^2 ----
T = sp.Function('T')(*X); mu2 = sp.symbols('mu_c2', positive=True)
tau = t + eps * T
Xsq = -( -(tau.diff(t))**2 + tau.diff(x)**2 + tau.diff(y)**2 + tau.diff(z)**2 )     # -(d tau)^2 in flat eta = diag(-1,1,1,1)
L2 = sp.series(mu2 * sp.sqrt(Xsq), eps, 0, 3).removeO().coeff(eps, 2)
L2 = sp.simplify(L2)
check("B1 cuscuton: O(eps^2) Lagrangian = -(mu_c^2/2)|grad T|^2, no (d_t T)^2 term (elliptic, 0 DOF)",
      sp.simplify(L2 + mu2/2*(T.diff(x)**2 + T.diff(y)**2 + T.diff(z)**2)) == 0, f"L2 = {L2}")
# ---- B2: the clock acceleration A_i at linear order in (h, T): A_i = d_i Phi - d_i d_t T + (B terms) ----
Phi, Psi = sp.Function('Phi')(*X), sp.Function('Psi')(*X)
B = [sp.Function(f'B{i}')(*X) for i in (1, 2, 3)]
g = sp.Matrix([[-(1 + 2*eps*Phi), eps*B[0], eps*B[1], eps*B[2]],
               [eps*B[0], 1 - 2*eps*Psi, 0, 0], [eps*B[1], 0, 1 - 2*eps*Psi, 0], [eps*B[2], 0, 0, 1 - 2*eps*Psi]])
ginv = g.inv().applyfunc(lambda e: sp.series(e, eps, 0, 2).removeO())
dtau = sp.Matrix([tau.diff(v) for v in X])
norm = sp.sqrt(-(dtau.T * ginv * dtau)[0, 0])
n_lo = (-dtau / norm).applyfunc(lambda e: sp.series(e, eps, 0, 2).removeO())          # n_mu
n_up = (ginv * n_lo).applyfunc(lambda e: sp.series(e, eps, 0, 2).removeO())           # n^mu
Gam = [[[sp.series(sum(ginv[l, s]*(g[s, m].diff(X[nu]) + g[s, nu].diff(X[m]) - g[m, nu].diff(X[s])) for s in range(4))/2, eps, 0, 2).removeO()
         for nu in range(4)] for m in range(4)] for l in range(4)]
A = [sp.expand(sp.series(sum(n_up[nu]*(n_lo[m].diff(X[nu]) - sum(Gam[l][nu][m]*n_lo[l] for l in range(4))) for nu in range(4)), eps, 0, 2).removeO())
     for m in range(4)]
A1 = [sp.simplify(A[m].coeff(eps, 1)) for m in range(4)]
targ = Phi.diff(x) - T.diff(x).diff(t)
check("B2 A_x at O(eps) = d_x Phi - d_x d_t T exactly (no shift term at linear order; the clock enters as a time derivative of the tilt)", sp.simplify(A1[1] - targ) == 0, f"A_x = {A1[1]}")
# ---- B3: T's field equation from L_T = -(mu^2/2)(grad T)^2 + lambda^i d_i d_t T  =>  mu^2 grad^2 T + d_t div(lambda) = 0 ----
lam = [sp.Function(f'lam{i}')(*X) for i in (1, 2, 3)]
LT = -mu2/2*(T.diff(x)**2 + T.diff(y)**2 + T.diff(z)**2) + sum(lam[i]*T.diff([x, y, z][i]).diff(t) for i in range(3))
eqT = sp.euler_equations(LT, [T], X)[0]
lhs = sp.simplify(eqT.lhs - eqT.rhs)
divlam_t = sum(lam[i].diff([x, y, z][i]) for i in range(3)).diff(t)
lapT = T.diff(x, 2) + T.diff(y, 2) + T.diff(z, 2)
check("B3 clock equation: mu_c^2 grad^2 T + d_t(div lambda) = 0  (drag source is d_t of the smoothed scalar force)",
      sp.simplify(lhs - (mu2*lapT + divlam_t)) == 0 or sp.simplify(lhs + (mu2*lapT + divlam_t)) == 0, f"E-L: {lhs} = 0")
# ---- B4: the chain to the O(w^2) potential, Fourier space, static kernels (sympy) ----
k, u, c, mu_inf, G, wk = sp.symbols('k u c mu_inf G wk', positive=True)   # u = xi^2 k^2, wk = w.k
PhiN = sp.symbols('PhiN')
Phi0 = PhiN/(1 - c**2/(mu_inf*(1 + u)**2))                     # static resummed potential (L169)
phi0 = c*Phi0/(mu_inf*(1 + u))                                 # static scalar
klam0 = -(c/(4*sp.pi*G))*k**2*phi0/(1 + u)                     # k.lambda^(0) = -(c/4piG)(i k).(i k phi)/(1+u) -> -(c/4piG) k^2 phi/(1+u) (i^2 = -1 absorbed: k.(ik) phi = i k^2 phi; overall phase tracked as magnitude)
T1 = wk*klam0/(mu2*k**2)                                       # |T^(1)| from mu^2 k^2 T = (w.k)(k.lambda)
kA2 = k**2*wk*T1                                               # k.A^(2), A^(2)_i = -d_i d_t T -> k_i (w.k) T
kchi2 = kA2/(1 + u)
phi2 = c*kchi2/(mu_inf*k**2)                                   # mu_inf k^2 phi = c k.chi
klam2 = -(c/(4*sp.pi*G))*k**2*phi2/(1 + u)
Phi2 = 4*sp.pi*G*klam2/k**2                                    # grad^2 Phi = 4piG(rho - div lambda) -> Phi^(2) = 4piG k.lambda^(2)/k^2 (magnitude)
ratio = sp.simplify(Phi2/Phi0)
expected = (c**2/mu_inf)**2 * wk**2 / (4*sp.pi*G*mu2) / (1 + u)**4 * (c**2/mu_inf)**0
print(f"    drag channel: Phi^(2)/Phi^(0) = {ratio}")
check("B4 |Phi^(2)/Phi^(0)| = (c^2/mu_inf)^2 (w.k)^2 / (4 pi G mu_c^2 (1+u)^4): enhanced by (w.k)^2/(4 pi G mu_c^2), screened by (1+u)^-4",
      sp.simplify(ratio - (c**2/mu_inf)**2*wk**2/(4*sp.pi*G*mu2*(1 + u)**4)) == 0)
# ---- numbers ----
H0 = 67.36e3/3.0857e22; Gn = 6.674e-11; cl = 2.998e8; AU = 1.496e11; pc = 3.0857e16
w = 370e3; xi = 0.03*pc; c2mu = 0.23
mu_c2 = H0**2/(4*np.pi*Gn) * cl**0      # cuscuton scale set by the dark-energy density: 4 pi G mu_c^2 = H0^2 (R = 1)
print(f"    numbers: w = 370 km/s, xi = 0.03 pc, c^2/mu_inf = 0.23, 4 pi G mu_c^2 = H0^2 (dark-energy-scale clock)")
print(f"    {'r':>8} {'(w k /c)^2/H0^2':>16} {'(1+u)^-4':>10} {'Phi2/Phi0':>12} {'|grad T|':>10}")
worst = 0; sat = 0
for r_au in (1, 10, 30, 1000):
    kk = 1/(r_au*AU); wk_ = w*kk; u_ = (xi*kk)**2
    enh = (wk_/cl)**2/H0**2 * cl**2          # (w.k)^2/(4piG mu_c^2) with k in 1/m, w/c dimensionless -> (w k/c)^2 c^2/H0^2
    enh = (w*kk)**2/H0**2
    rat = c2mu**2*enh/(1 + u_)**4
    gradT = (w*kk/cl)*(c2mu)*(Gn*1.989e30/(r_au*AU)/cl**2)/(H0**2/cl**2)*kk/(1+u_)**3 * cl  # |grad T| ~ k (w.k) c phi/(4piG mu^2), phi ~ (c^2/mu) Phi_N/(1+u)
    gradT = (w/cl)*kk**2*c2mu*(Gn*1.989e30/(r_au*AU)/cl**2)/(H0/cl)**2/(1+u_)**3
    worst = max(worst, rat); sat = max(sat, gradT)
    print(f"    {r_au:5d} AU {enh:16.2e} {(1+u_)**-4:10.2e} {rat:12.2e} {gradT:10.2e}")
check("B5 [DEFICIT, verified] the O(w^2) drag potential is 3e-2 of Phi_N at Saturn (10 AU) against a ~1e-5 PPN tolerance and EXCEEDS Phi_N beyond ~30 AU",
      worst > 1.0 and c2mu**2*(w/(10*AU))**2/H0**2/(1+(xi/(10*AU))**2)**4 > 1e-5, f"max Phi2/Phi0 = {worst:.1e}")
check("B6 [DEFICIT, verified] the linear clock tilt |grad T| >> 1 (cuscuton driven to the null gradient X -> 0): no linear regime exists for moving sources",
      sat > 1e3, f"max |grad T| = {sat:.1e}")
# ---- B8: how stiff would the cuscuton have to be? ratio ~ (c^2/mu_inf)^2 (w/c)^2 (c k/H0)^2 (1+u)^-4 / R, R = 4 pi G mu_c^2 / H0^2 ----
kpk = 1/(np.sqrt(3)*xi)                                  # k^2/(1+xi^2 k^2)^4 peaks at xi^2 k^2 = 1/3
R_min = c2mu**2*(w*kpk)**2/H0**2/(1 + 1/3)**4/1e-5
print(f"    B8: keeping the drag below 1e-5 Phi_N at every scale up to xi needs 4 pi G mu_c^2 >= {R_min:.1e} x H0^2 -- a clock {R_min:.0e} times denser than dark energy")
check("B8 [DEFICIT, verified] no cuscuton stiffness works: the PPN-safe mu_c^2 is >= 1e15 x the dark-energy value the clock must have to source Lambda",
      R_min > 1e15, f"R_min = {R_min:.1e}")
# ---- what a stiff clock would do (scaling only) ----
c2 = sp.symbols('c_2', positive=True)
ratio_stiff = (c**2/mu_inf)**2*wk**2/(c2*k**2)/(1 + u)**4        # replace 4 pi G mu_c^2 by c_2 k^2 (K^2 term, M_P^2 coefficient)
r10 = c2mu**2*(w/cl)**2/(1 + (xi/(10*AU))**2)**4
print(f"    stiff-clock scaling: with a c_2 K^2 term the enhancement (w.k)^2/(4 pi G mu^2) -> (w/c)^2/c_2: at 10 AU Phi2/Phi0 ~ {r10:.1e}/c_2")
check("B7 a stiff (khronon-type) clock removes the enhancement: (w/c)^2 (c^2/mu_inf)^2 (1+u)^-4 at 10 AU is below 1e-20 -- but that is a different action (G_cosmo/G_N shift, astra's g03 clock pincer)",
      r10 < 1e-20, f"{r10:.1e}")
print("    alpha_1 channel (O(w), g_0i): the drag needs two time derivatives (d_t in the source, d_t in A_i), so it enters first at O(w^2);\n"
      "    the O(w) sector carries no 1/mu_c^2 and is screened like gamma. Not computed to a number here: moot once the O(w^2) sector fails.")
print(f"\nL170 COMPLETE: {sum(CH)}/{len(CH)} checks PASS.")
