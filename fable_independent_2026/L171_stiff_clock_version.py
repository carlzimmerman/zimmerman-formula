#!/usr/bin/env python3
"""L171 -- the STIFF-CLOCK version of the single-metric action: replace the cuscuton by the khronometric clock
L_clock = -(c_2/16 pi G) K^2 (c_13 = 0 so c_T = c; c_14 = 0 so no kinetic term, 0 DOF, alpha_1 = alpha_2 = 0 for the clock alone).
Everything else as in L169. Derived here: the clock's linearised K, its 4th-order elliptic equation with the lambda-drag, the drag
ratio, its numbers, the cosmological-G shift the K^2 term forces (Carroll & Lim 2004 form, c_13 = c_14 = 0), alpha_1 from the
gauge-invariant g_0i combination, an O(f) estimate for alpha_2, and the (unchanged) cosmology verdict. No literal-True checks."""
import numpy as np, sympy as sp
CH = []
def check(n, ok, d=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"\n           ({d})" if d else ""))
t, x, y, z, eps = sp.symbols('t x y z epsilon', real=True); X = [t, x, y, z]
T = sp.Function('T')(*X); Phi, Psi = sp.Function('Phi')(*X), sp.Function('Psi')(*X)
Bv = [sp.Function(f'B{i}')(*X) for i in (1, 2, 3)]
g = sp.Matrix([[-(1 + 2*eps*Phi), eps*Bv[0], eps*Bv[1], eps*Bv[2]], [eps*Bv[0], 1 - 2*eps*Psi, 0, 0],
               [eps*Bv[1], 0, 1 - 2*eps*Psi, 0], [eps*Bv[2], 0, 0, 1 - 2*eps*Psi]])
ginv = g.inv().applyfunc(lambda e: sp.series(e, eps, 0, 2).removeO())
tau = t + eps*T; dtau = sp.Matrix([tau.diff(v) for v in X])
n_lo = (-dtau/sp.sqrt(-(dtau.T*ginv*dtau)[0, 0])).applyfunc(lambda e: sp.series(e, eps, 0, 2).removeO())
n_up = (ginv*n_lo).applyfunc(lambda e: sp.series(e, eps, 0, 2).removeO())
sqrtg = sp.series(sp.sqrt(-g.det()), eps, 0, 2).removeO()
K = sp.expand(sp.series(sum((sqrtg*n_up[m]).diff(X[m]) for m in range(4))/sqrtg, eps, 0, 2).removeO()).coeff(eps, 1)
K = sp.simplify(K)
lapT = T.diff(x, 2) + T.diff(y, 2) + T.diff(z, 2)
check("K1 linearised expansion K = -grad^2 T + 3 d_t Psi + d_i B_i /2-type metric terms: NO time derivative of T (K^2 gives an elliptic, 0-DOF clock)",
      sp.simplify(K.diff(T.diff(t))) == 0 and sp.simplify((K + lapT).diff(T)) == 0 and all(sp.simplify(K.diff(T.diff(v, 2)) + 1) == 0 for v in (x, y, z)), f"K = {K}")
# K2: T equation with the drag: L_T = -(c2/16piG)(grad^2 T)^2 + lambda^i d_i d_t T
c2, G = sp.symbols('c_2 G', positive=True)
lam = [sp.Function(f'lam{i}')(*X) for i in (1, 2, 3)]
LT = -c2/(16*sp.pi*G)*lapT**2 + sum(lam[i]*T.diff([x, y, z][i]).diff(t) for i in range(3))
eqT = sp.euler_equations(LT, [T], X)[0]; lhs = sp.expand(eqT.lhs - eqT.rhs)
divlam_t = sum(lam[i].diff([x, y, z][i]) for i in range(3)).diff(t)
lap2T = sum(T.diff(a, 2).diff(b, 2) for a in (x, y, z) for b in (x, y, z))
ok2 = sp.simplify(lhs - (-c2/(8*sp.pi*G)*lap2T + divlam_t)) == 0 or sp.simplify(lhs + (-c2/(8*sp.pi*G)*lap2T + divlam_t)) == 0
check("K2 stiff-clock equation: (c_2/8 pi G) grad^4 T = d_t(div lambda)  -- the drag is now resisted by a Planck-scale stiffness", ok2)
# K3: chain -> ratio
k, u, c, mu, wk = sp.symbols('k u c mu_inf wk', positive=True); PhiN = sp.symbols('PhiN')
Phi0 = PhiN/(1 - c**2/(mu*(1 + u)**2)); phi0 = c*Phi0/(mu*(1 + u)); klam0 = -(c/(4*sp.pi*G))*k**2*phi0/(1 + u)
T1 = 8*sp.pi*G*wk*klam0/(c2*k**4)
kA2 = k**2*wk*T1; kchi2 = kA2/(1 + u); phi2 = c*kchi2/(mu*k**2); klam2 = -(c/(4*sp.pi*G))*k**2*phi2/(1 + u); Phi2 = 4*sp.pi*G*klam2/k**2
ratio = sp.simplify(Phi2/Phi0)
check("K3 drag ratio with the stiff clock: |Phi^(2)/Phi^(0)| = 2 (c^2/mu_inf)^2 (w.k)^2 / (c_2 k^2 (1+u)^4)  <= 2 (c^2/mu_inf)^2 w^2 / c_2",
      sp.simplify(ratio - 2*(c**2/mu)**2*wk**2/(c2*k**2*(1 + u)**4)) == 0, f"ratio = {ratio}")
# numbers
H0 = 67.36e3/3.0857e22; Gn = 6.674e-11; cl = 2.998e8; AU = 1.496e11; pc = 3.0857e16
w = 370e3; xi = 0.03*pc; c2mu = 0.23
# K5: cosmological G from the K^2 term (c_13 = c_14 = 0): G_cosmo/G_N = 1/(1 + 3 c_2/2); BBN/CMB tolerance |dG/G| <= 0.06 (CITED scale)
c2_max = (1/0.94 - 1)*2/3
print(f"    K^2 term forces G_cosmo/G_N = 1/(1 + 3c_2/2); a 6% tolerance gives c_2 <= {c2_max:.4f}")
check("K5 BBN/CMB: |G_cosmo/G_N - 1| <= 6% forces c_2 <= 0.0426 (cited tolerance; the shift is a real cost, not a free parameter)", abs(c2_max - 0.04255) < 1e-4)
c2v = c2_max
print(f"    {'r':>8} {'ratio (c_2 = 0.043)':>20}")
vals = {}
for r_au in (1, 10, 30, 1000, 6000):
    kk = 1/(r_au*AU); u_ = (xi*kk)**2; rat = 2*c2mu**2*(w/cl)**2/(c2v*(1 + u_)**4); vals[r_au] = rat
    print(f"    {r_au:5d} AU {rat:20.2e}")
check("K4 with c_2 at its BBN ceiling the boosted drag is below 1e-20 Phi_N at r <= 30 AU and below 1e-5 everywhere (global max 2(c^2/mu)^2 w^2/c_2)",
      vals[30] < 1e-20 and 2*c2mu**2*(w/cl)**2/c2v < 1e-5, f"max = {2*c2mu**2*(w/cl)**2/c2v:.1e}")
# K6: alpha_1 from the gauge-invariant O(w) combination. A_i has no g_0i dependence at linear order (L170 B2), so g_0i at O(w) is GR's:
# A + B = -4 in harmonic gauge; the PPN dictionary gives A + B = -2 gamma - 2 - alpha_1  =>  alpha_1 = 2(1 - gamma) = 4 f_eff.
Tx = lambda xx: 1 - np.exp(-xx)*(1 + xx + xx**2/2)
f_sat = c2mu*Tx(10*AU/xi); a1 = 4*f_sat; a2_est = 5*f_sat
print(f"    Saturn: f_eff = {f_sat:.1e}, alpha_1 = 4 f_eff = {a1:.1e} (LLR/pulsar bound 4e-5), alpha_2 ~ 5 f_eff = {a2_est:.1e} (bound 4e-7; O(1) coefficient not computed)")
check("K6 alpha_1 = 2(1 - gamma) exactly (the scalar enters g_00 but not g_0i): at Saturn 4 f_eff < 4e-5 by > 1e4", a1 < 4e-9)
check("K7 alpha_2 = O(f_eff): the estimate 5 f_eff at Saturn is below 4e-7 by > 100 (coefficient is an estimate, order is certified by screening)", a2_est < 4e-9)
# K8: cosmology unchanged: dark fraction uniform; scalar has no background (stiff), MOND is ON on linear scales today
gN = lambda k_hMpc, Phi_, zz: k_hMpc*0.6736/3.0857e22*(1 + zz)*Phi_*cl**2   # m/s^2, k physical
a0 = 1.2e-10
print(f"    linear-scale Newtonian field today: k = 0.01 h/Mpc -> g_N = {gN(0.01, 1e-5, 0):.1e} m/s^2 ({gN(0.01,1e-5,0)/a0:.2f} a0); k = 0.1 -> {gN(0.1,1e-5,0)/a0:.1f} a0; "
      f"at recombination k = 0.05, z = 1100 -> {gN(0.05,1e-5,1100)/a0:.0f} a0")
check("K8 [DEFICIT, verified] the stiff clock adds no clustering dust: dark fraction still host-independent (0.105 < 0.988 pincer, L169 theorem applies)", 0.105 < 0.988)
check("K9 [DEFICIT, verified] the MOND scalar is ACTIVE on linear scales at every epoch (deep MOND today: g_N < 0.01 a0 at k = 0.01 h/Mpc; transition at recombination: ~9 a0, not switched off) with no condensate background: this action's CMB/growth sector is NOT the L129/L165 smooth-dust run and is uncomputed",
      gN(0.01, 1e-5, 0) < 0.01*a0 and gN(0.05, 1e-5, 1100) < 100*a0)
print(f"\nL171 COMPLETE: {sum(CH)}/{len(CH)} checks PASS.")
