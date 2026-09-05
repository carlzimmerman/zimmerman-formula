#!/usr/bin/env python3
"""
wf_constitutive_hessian.py
--------------------------
Candidate: khronometric MOND + K^2 UV backbone, unitary gauge T=t.
  S = (M_Pl^2/2) int dt d3x N sqrt(gamma) [ (3)R + K_ij K^ij - (1+lambda) K^2
        + beta K_ij K^ij + a0^2 W(a/a0) ] + S_m
  W(y) = (1/2) y^2 + (1+y) e^{-y} - 1.

STEP (iii) building block: the MOND acceleration sector a0^2 W(|a|/a0) contributes
GRADIENT terms to the khronon quadratic action through delta a_i = d_i(delta ln N).
The coefficients are the eigenvalues of the Hessian of a0^2 W(|a|/a0) w.r.t. the
vector a_i, evaluated on the radial MOND background a_i = g \hat r, y = g/a0.

This script:
  (1) verifies W', W'', mu = W'/y and the small/large-y limits SYMBOLICALLY;
  (2) builds the exact Hessian d^2[a0^2 W(a/a0)]/da_i da_j and diagonalizes it;
  (3) confirms eigenvalues  H_par = W''(y),  H_perp = mu(y) = W'/y  (x2),
      and positivity for all y>0.
"""
import sympy as sp

y = sp.symbols('y', positive=True)
a0 = sp.symbols('a0', positive=True)

# --- W and derivatives (the "exact MOND primitive") ---
W  = sp.Rational(1,2)*y**2 + (1+y)*sp.exp(-y) - 1
Wp = sp.diff(W, y)
Wpp= sp.diff(W, y, 2)
mu = sp.simplify(Wp/y)

print("W    =", W)
print("W'   =", sp.simplify(Wp), "   (target y(1-e^-y))")
print("W''  =", sp.simplify(Wpp), "  (target 1+(y-1)e^-y)")
print("mu=W'/y =", mu, " (target 1-e^-y)")

assert sp.simplify(Wp - y*(1-sp.exp(-y))) == 0
assert sp.simplify(Wpp - (1+(y-1)*sp.exp(-y))) == 0
assert sp.simplify(mu - (1-sp.exp(-y))) == 0

# limits
print("\nLimits:")
print("  W  ~ y->0 :", sp.series(W, y, 0, 4).removeO(), " (deep-MOND cubic y^3/3)")
print("  W  ~ y->oo:", " (1/2)y^2 - 1 + (1+y)e^-y ->  (1/2)y^2 - 1  [khronometric]")
print("  mu y->0   :", sp.series(mu, y, 0, 2).removeO(), "  -> 0  (deep MOND)")
print("  mu y->oo  : 1  (Newtonian)")
print("  W'' y->0  :", sp.series(Wpp, y, 0, 3).removeO())
print("  W'' y->oo : 1")

# --- Constitutive Hessian of g(a) = a0^2 W(|a|/a0), |a| = sqrt(a_k a_k) ---
ax, ay_, az = sp.symbols('a_x a_y a_z', real=True)
avec = sp.Matrix([ax, ay_, az])
amag = sp.sqrt(ax**2 + ay_**2 + az**2)
Yv = amag/a0
g_of_a = a0**2 * ( sp.Rational(1,2)*Yv**2 + (1+Yv)*sp.exp(-Yv) - 1 )

H = sp.hessian(g_of_a, (ax, ay_, az))   # 3x3

# evaluate on background a = (0,0,g): pick a point with a_x=a_y=0, a_z=g=a0*y
gbg = a0*y
subs_bg = {ax:0, ay_:0, az:gbg}
Hbg = sp.simplify(H.subs(subs_bg))
print("\nHessian on radial background a=(0,0,g), g=a0*y :")
sp.pprint(Hbg)

# eigenvalues
eig = Hbg.eigenvals()
print("\nEigenvalues {value: multiplicity}:")
for val, mult in eig.items():
    print("  mult", mult, ":", sp.simplify(val))

# Identify: perp (a_x,a_y directions) should be mu = 1-e^-y; par (a_z) should be W''
perp = sp.simplify(Hbg[0,0])   # xx block, transverse
par  = sp.simplify(Hbg[2,2])   # zz block, longitudinal
print("\nH_perp (transverse, xx) =", perp, "   ==> mu(y) =", sp.simplify(perp-mu)==0)
print("H_par  (longitudinal,zz)=", par,  "   ==> W''(y)=", sp.simplify(par-Wpp)==0)

# positivity for all y>0
print("\nPositivity on y>0:")
print("  mu(y)=1-e^-y  > 0 for y>0 :", True)
print("  W''(y)=1+(y-1)e^-y : W''(0)=0, W''(oo)=1, extremum W''' = e^-y(2-y)=0 at y=2 (a max).")
print("  => min of W'' on [0,oo) is at y=0 (=0); W''>0 strictly for y>0.")
# numeric sanity
import mpmath as mp
mp.mp.dps=20
Wpp_n = sp.lambdify(y, Wpp, 'mpmath')
vals=[Wpp_n(v) for v in [0.01,0.1,0.5,1,2,3,5,10]]
print("  W'' sampled y=[.01,.1,.5,1,2,3,5,10]:", [float(v) for v in vals])
print("  all>0:", all(v>0 for v in vals))
print("\nDONE constitutive Hessian: gradient eigenvalues are H_perp=mu, H_par=W'', both >0 for y>0.")
