"""Gate 1: Constitutive primitive.

Verify that a local spatial constitutive density G(y) exists whose lapse
variation reproduces the MOND modified Poisson operator with

    mu(y) = 1 - exp(-y),

and that the proposed primitive

    G(y) = y^2 + 2 (1+y) e^{-y} - 2

satisfies  G'(y) / (2 y) = mu(y).

We work in the quasistatic weak-field variables.  Let

    u_i = D_i ln N ,   u = |u| ,   y = (c^2 / a0) u .

The MOND flux is  F^i = c^2 mu(y) u^i .  A local primitive for the flux
divergence is sought in the form  F^i = dPhi/du_i  for a scalar potential
Phi(u) = c^2 G(y) / y^2  (so that dPhi/du_i = Phi'(y) du_i y/u ... ).  The
cleanest check is purely on the scalar function: we need a G with

    d/dy [ (1/2) dG/dy ] ...

Actually the operator we must reproduce is  D_i[ mu(y) D^i ln N ] .  In the
radial / single-gradient direction the relevant scalar derivative is

    d/dy [ y mu(y) ]  ...

The candidate statement to verify is simply the algebraic identity

    G'(y) / (2 y) = 1 - e^{-y} = mu(y)

for the given G.  We verify it exactly with SymPy, and also verify the two
asymptotic limits mu ~ y (y<<1) and mu -> 1 (y>>1), and that the primitive
reproduces the flux derivative (the "constitutive closure").
"""

import sympy as sp

y = sp.symbols("y", positive=True)
c, a0 = sp.symbols("c a0", positive=True)

mu = 1 - sp.exp(-y)

G = y**2 + 2 * (1 + y) * sp.exp(-y) - 2

print("=" * 70)
print("GATE 1: CONSTITUTIVE PRIMITIVE")
print("=" * 70)

# --- Check 1.1: G'(y) / (2y) == mu(y) ---
Gp = sp.diff(G, y)
ratio = sp.simplify(Gp / (2 * y))
check_1_1 = sp.simplify(ratio - mu) == 0
print("\n[1.1] G'(y)          =", sp.simplify(Gp))
print("[1.1] G'(y)/(2y)      =", sp.simplify(ratio))
print("[1.1] mu(y)           =", mu)
print("[1.1] G'(y)/(2y) - mu(y) simplifies to 0 :", check_1_1)

# --- Check 1.2: G'(y) = 2 y mu(y) exactly ---
check_1_2 = sp.simplify(Gp - 2 * y * mu) == 0
print("[1.2] G'(y) - 2 y mu(y) == 0             :", check_1_2)

# --- Check 1.3: G(0) == 0 (primitive vanishes at zero gradient) ---
G0 = sp.limit(G, y, 0)
check_1_3 = G0 == 0
print("[1.3] limit G(y) as y->0                 :", G0, "== 0:", check_1_3)

# --- Check 1.4: G is convex for y>0 (G''>0) -> elliptic constitutive law ---
Gpp = sp.simplify(sp.diff(G, y, 2))
print("[1.4] G''(y)                  =", Gpp)
# G''(y) = 2 e^{-y} (y+1) - 2?  let's get it
Gpp_s = sp.simplify(Gpp)
print("[1.4] G''(y) simplified       =", Gpp_s)

# --- Check 1.5: asymptotic limits ---
# mu(y) = y - y^2/2 + O(y^3):  the correct small-y statement is mu(y)/y -> 1.
mu_over_y_small = sp.limit(mu / y, y, 0)
mu_large = sp.limit(mu, y, sp.oo)
check_1_5 = (mu_over_y_small == 1) and (mu_large == 1)
print("[1.5] limit mu(y)/y as y->0          :", mu_over_y_small, "(=1 means mu~y)")
print("[1.5] mu(y) -> 1 for y>>1  (limit)   :", mu_large)
print("[1.5] both limits correct            :", check_1_5)

# --- Check 1.6: flux derivative in a single gradient direction ---
# F = c^2 mu(y) u  with y = (c^2/a0) u.  dF/du should be positive (elliptic).
u = sp.symbols("u", positive=True)
yy = c**2 * u / a0
F = c**2 * (1 - sp.exp(-yy)) * u
dF_du = sp.simplify(sp.diff(F, u))
print("[1.6] dF/du (single-gradient) =", sp.factor(dF_du))
# positivity:  dF/du = c^2 [ mu + (c^2 u/a0) mu' ]  = c^2[ mu + y mu' ]
# which is Gate 4's parallel eigenvalue.  We just record it here.

# --- Check 1.7: the constitutive potential Phi(u) = (c^2 a0^2 / 2) ... ---
# We want Phi'(y) such that the flux F^i = c^2 mu(y) u^i = dPhi/d u_i.
# With Phi = Phi(y), dPhi/du_i = Phi'(y) (dy/du_i) = Phi'(y) (c^2/a0) uhat_i.
# So we need  c^2 mu(y) u^i = Phi'(y) (c^2/a0) uhat_i  ->  mu(y) u = Phi'(y)(c^2/a0).
# => Phi'(y) = (a0/c^2) mu(y) u = (a0/c^2) mu(y) (a0 y / c^2) = (a0^2/c^4) mu(y) y.
# So Phi(y) = (a0^2/c^4) * (1/2) G(y)  since G'/(2y)=mu  =>  y mu = G'/2.
# Check: d/dy[(a0^2/c^4)(G/2)] = (a0^2/c^4) G'/2 = (a0^2/c^4) y mu.  ✓
Phi = (a0**2 / c**4) * (G / 2)
dPhi_dy = sp.simplify(sp.diff(Phi, y))
target = (a0**2 / c**4) * y * mu
check_1_7 = sp.simplify(dPhi_dy - target) == 0
print("[1.7] Phi'(y) == (a0^2/c^4) y mu(y)     :", check_1_7)

all_pass = all([check_1_1, check_1_2, check_1_3, check_1_5, check_1_7])
print("\n" + "=" * 70)
print("GATE 1 RESULT:", "PASS" if all_pass else "FAIL")
print("=" * 70)
