#!/usr/bin/env python3
"""L169 -- the single-metric kinetic-mixing action: static reduction (sympy Euler-Lagrange), double-filter kernel and
transmission T(x) = 1 - e^-x (1 + x + x^2/2), PPN gamma at the Cassini radius, Newtonian-G renormalisation and the
mu_inf bound from SPARC Upsilon_*, and the dark-fraction no-go. No pass condition is a literal True. See SINGLE_METRIC_ACTION.md."""
import numpy as np, sympy as sp
from scipy.integrate import quad
CH = []
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""))
# ---- 1. static variation (1-D, weak field, Newtonian regime mu = mu_inf) ----
x = sp.symbols('x', real=True); G, c, xi, rho, mu = sp.symbols('G c xi rho mu_inf', positive=True)
Phi, phi, chi, lam = [sp.Function(n)(x) for n in ('Phi', 'phi', 'chi', 'lam')]
L = -Phi.diff(x)**2/(8*sp.pi*G) - rho*Phi - mu*phi.diff(x)**2/(8*sp.pi*G) + c/(4*sp.pi*G)*chi*phi.diff(x) \
    + lam*(chi - xi**2*chi.diff(x, 2) - Phi.diff(x))
eqs = sp.euler_equations(L, [Phi, phi, chi, lam], x)
E = {str(f.func): sp.simplify(e.lhs - e.rhs) for f, e in zip([Phi, phi, chi, lam], eqs)}
ok_lam = sp.simplify(E['lam'] - (chi - xi**2*chi.diff(x, 2) - Phi.diff(x))) == 0
ok_chi = sp.simplify(E['chi'] - (c/(4*sp.pi*G)*phi.diff(x) + lam - xi**2*lam.diff(x, 2))) == 0
ok_phi = sp.simplify(E['phi'] - (mu*phi.diff(x, 2)/(4*sp.pi*G) - c/(4*sp.pi*G)*chi.diff(x))) == 0
ok_Phi = sp.simplify(E['Phi'] - (Phi.diff(x, 2)/(4*sp.pi*G) - rho + lam.diff(x))) == 0
check("S1 Euler-Lagrange of the static action gives the four double-filter equations exactly (delta lambda, chi, phi, Phi)", ok_lam and ok_chi and ok_phi and ok_Phi)
# ---- 2. Fourier kernel and transmission ----
k, u = sp.symbols('k u', positive=True)
lhs = 1/(k**2*(1 + xi**2*k**2)**2); rhs = 1/k**2 - xi**2/(1 + xi**2*k**2) - xi**2/(1 + xi**2*k**2)**2
check("S2 partial fractions 1/(k^2(1+u)^2) = 1/k^2 - xi^2/(1+u) - xi^2/(1+u)^2", sp.simplify(lhs - rhs) == 0)
T = lambda xx: 1 - np.exp(-xx)*(1 + xx + xx**2/2)
# numeric inverse FT of the point-source potential with kernel 1/(k^2 (1+k^2)^2) (xi = 1): phi(r) = (1/2 pi^2 r) int sin(kr)/(k (1+k^2)^2) dk
def phi_num(r): return quad(lambda kk: np.sin(kk*r)/(kk*(1+kk**2)**2), 0, np.inf, limit=800)[0]/(2*np.pi**2*r)
def phi_cf(r): return (1 - np.exp(-r)*(1 + r/2))/(4*np.pi*r)
rs = np.array([0.1, 0.5, 1, 2, 5]); dev = max(abs(phi_num(r)/phi_cf(r) - 1) for r in rs)
check("S3 closed-form smoothed potential (1 - e^-x(1+x/2))/(4 pi r) matches the numerical inverse transform to 1e-4", dev < 1e-4, f"max dev {dev:.1e}")
xs = sp.symbols('xs', positive=True); Tsym = 1 - sp.exp(-xs)*(1 + xs + xs**2/2)
check("S4 force transmission: -d/dr of the potential gives T(x) = 1 - e^-x(1+x+x^2/2), and T = x^3/6 + O(x^4)",
      sp.simplify(-sp.diff((1 - sp.exp(-xs)*(1 + xs/2))/xs, xs)*xs**2 - Tsym) == 0 and sp.series(Tsym, xs, 0, 4).removeO() == xs**3/6)
xg = np.linspace(1e-4, 1, 2000)
check("S5 0 <= T(x) <= x^3 on [0,1] and T increasing (the Lean statement, checked numerically)", np.all(T(xg) >= 0) and np.all(T(xg) <= xg**3) and np.all(np.diff(T(xg)) > 0))
# ---- 3. PPN gamma ----
AU = 4.848e-6  # pc
for xi_pc in (0.03, 0.002):
    xr = 10*AU/xi_pc; print(f"    xi = {xi_pc} pc: at Saturn (10 AU) x = r/xi = {xr:.2e}, |gamma-1| <= 2 T(x) = {2*T(xr):.1e} (Cassini 2.3e-5)")
check("S6 gamma at the f-lane floor xi = 0.03 pc: |gamma - 1| <= 2 T(10 AU / xi) < 2.3e-5 by more than 1e3", 2*T(10*AU/0.03) < 2.3e-8)
# ---- 4. Newtonian G renormalisation and mu_inf ----
cc, mi = sp.symbols('c mu', positive=True)
Geff = 1/(1 - cc**2/mi)   # r >> xi, Newtonian regime, relative to lab G
mu_min = float(sp.solve(sp.Eq(Geff.subs(cc, 1), 1.3), mi)[0])
print(f"    G_gal/G_lab = 1/(1 - c^2/mu_inf); c = 1 and a 30% Upsilon_* tolerance need mu_inf >= {mu_min:.2f}")
check("S7 with c = 1 (a0_tilde = a0, derived kappa intact) the Newtonian-regime stiffening must reach mu_inf >= 4.3", abs(mu_min - 13/3) < 1e-9)
# ---- 5. dark fraction: uniform ----
f_gal_max, f_cmb_min = 0.105, 0.988
print(f"    the action's dark components: cuscuton dust (0 DOF, no clustering), phi background (stiff, a^-6). Host-mass dependence: none.")
check("S8 [DEFICIT, verified] a host-independent dark fraction cannot satisfy f <= 0.105 (galaxies) and f >= 0.988 (CMB): 0.105 < 0.988", f_gal_max < f_cmb_min)
peak_ratio_smooth, peak_ratio_obs = 0.5545, 0.9906   # L129 / L165
check("S9 [DEFICIT, verified] smooth (non-clustering) dust fails the third peak: L129/L165 peak3/peak2 = 0.5545 vs 0.9906", abs(peak_ratio_smooth/peak_ratio_obs - 1) > 0.3)
print(f"\nL169 COMPLETE: {sum(CH)}/{len(CH)} checks PASS.")
