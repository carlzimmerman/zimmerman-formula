"""
wf_hessian_constitutive.py
Verify the constitutive-sector Hessian eigenvalues of the exact MOND primitive
  W(y) = (1/2)y^2 + (1+y) e^{-y} - 1
  W'(y)  = y (1 - e^{-y})            [radial/parallel force law: mu(y)*y]
  mu(y)  = W'/y = 1 - e^{-y}         [transverse Hessian eigenvalue H_perp]
  W''(y) = 1 + (y-1) e^{-y}          [radial Hessian eigenvalue H_par]
across 1e-6 < y < 1e6 (and asymptotics), with sympy + numpy.

The "constitutive Hessian" is the Hessian of the scalar-field energy density
W(|a|/a0) w.r.t. the vector a (up to a0^2 factors). For a radial function W(|a|):
  d^2 W(|a|)/da_i da_j = W''(y) n_i n_j + (W'(y)/y)(delta_ij - n_i n_j)
so eigenvalue along the field = W''(y) = H_par, and transverse (2-fold) = W'/y = mu = H_perp.
This script confirms BOTH are strictly positive for all y>0 (constitutive sector
never ghostly), which is the premise handed to the perturbation analysis.
"""
import sympy as sp
import numpy as np

y = sp.symbols('y', positive=True)

W    = sp.Rational(1,2)*y**2 + (1+y)*sp.exp(-y) - 1
Wp   = sp.diff(W, y)
Wpp  = sp.diff(W, y, 2)
mu   = sp.simplify(Wp/y)

print("=== SYMBOLIC ===")
print("W       =", sp.simplify(W))
print("W'      =", sp.simplify(Wp))
print("W''     =", sp.simplify(Wpp))
print("mu=W'/y =", sp.simplify(mu))
print()

# Claimed closed forms
Wp_claim  = y*(1 - sp.exp(-y))
Wpp_claim = 1 + (y-1)*sp.exp(-y)
mu_claim  = 1 - sp.exp(-y)
print("W'  matches y(1-e^-y):        ", sp.simplify(Wp - Wp_claim) == 0)
print("W'' matches 1+(y-1)e^-y:      ", sp.simplify(Wpp - Wpp_claim) == 0)
print("mu  matches 1-e^-y:           ", sp.simplify(mu - mu_claim) == 0)
print()

# Asymptotics (series)
print("=== ASYMPTOTICS ===")
print("W  (y->0):", sp.series(W, y, 0, 5).removeO())
print("W' (y->0):", sp.series(Wp, y, 0, 5).removeO())
print("W''(y->0):", sp.series(Wpp, y, 0, 5).removeO())
print("mu (y->0):", sp.series(mu, y, 0, 5).removeO())
print("-> deep-MOND: W ~ y^3/3 ? leading term of W:", sp.series(W, y, 0, 4).removeO())
print("W'' (y->inf) -> 1 ; mu (y->inf) -> 1  (Newtonian/khronometric)")
print()

# Minimum of W'' : does H_par ever dip? W''' = (2-y)e^-y ; zero at y=2 -> minimum
Wppp = sp.diff(Wpp, y)
crit = sp.solve(sp.Eq(Wppp,0), y)
print("=== W'' EXTREMA (constitutive H_par) ===")
print("W''' =", sp.simplify(Wppp), " -> critical y =", crit)
for c in crit:
    print(f"  W''(y={c}) = {sp.simplify(Wpp.subs(y,c))} = {float(Wpp.subs(y,c)):.10f}")
print("  (W'' minimum value; must be > 0)")
print()

# Numeric sweep, log-spaced 1e-6 .. 1e6, plus dense linear near transition
print("=== NUMERIC SWEEP 1e-6 < y < 1e6 ===")
def f_mu(yy):  return 1 - np.exp(-yy)
def f_Wpp(yy): return 1 + (yy-1)*np.exp(-yy)
def f_W(yy):   return 0.5*yy**2 + (1+yy)*np.exp(-yy) - 1

ys = np.concatenate([
    np.logspace(-6, 6, 200001),
    np.linspace(0.01, 10, 200001)
])
mu_v  = f_mu(ys)
Wpp_v = f_Wpp(ys)
W_v   = f_W(ys)
print(f"min mu   over sweep = {mu_v.min():.6e}  at y={ys[np.argmin(mu_v)]:.6e}")
print(f"min W''  over sweep = {Wpp_v.min():.6e}  at y={ys[np.argmin(Wpp_v)]:.6e}")
print(f"min W    over sweep = {W_v.min():.6e}  at y={ys[np.argmin(W_v)]:.6e}")
print(f"all mu  > 0 : {np.all(mu_v  > 0)}")
print(f"all W'' > 0 : {np.all(Wpp_v > 0)}")
print(f"all W  >= 0 : {np.all(W_v  >= -1e-15)}")
print()
# spot values across transition
print(" y        mu=H_perp     W''=H_par")
for yy in [1e-4, 1e-2, 0.1, 0.5, 1.0, 2.0, 3.0, 5.0, 10.0, 100.0]:
    print(f"{yy:8.4g}  {f_mu(yy):.8f}   {f_Wpp(yy):.8f}")
