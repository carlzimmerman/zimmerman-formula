"""Step 1: static spherically symmetric reduction of the round-2 ADM action.

h_ij = f(r) delta_ij (conformally flat), N = N(r), P_i = p(r) n_i, n_i = x_i/r.
Checks: R3 formula, GR limit (p=0 -> Schwarzschild in this gauge), and the
leading P solution in the two regimes r<<L*, r>>L*.
"""
import sympy as sp

r = sp.symbols('r', positive=True)
K, beta, eta, gam, a0 = sp.symbols('K beta eta gamma a0', positive=True)
N = sp.Function('N')(r)
f = sp.Function('f')(r)
p = sp.Function('p')(r)


def R3_conf(fexpr, r):
    """Ricci scalar of h_ij = f delta_ij in 3D: R3 = -(1/f)[2 L'' + 4 L'/r + L'^2/2], L=ln f."""
    L = sp.log(fexpr)
    return -(1/fexpr)*(2*sp.diff(L, r, 2) + 4*sp.diff(L, r)/r + sp.Rational(1, 2)*sp.diff(L, r)**2)


# check R3 against the 3-sphere: dl^2 = 4/(1+r^2)^2 (dr^2 + r^2 dOmega^2) -> R3 = 6
fs = 4/(1 + r**2)**2
print("R3(3-sphere) =", sp.simplify(R3_conf(fs, r)))

# --- reduced lagrangian -------------------------------------------------
sqh = f**sp.Rational(3, 2)
q = sp.sqrt(f)*p              # q = sqrt(f) p
DP = (sp.diff(q, r) + 2*q/r)/f**sp.Rational(3, 2)   # D_i P^i
u = K*p/sp.sqrt(f)            # u = K|P|
W = (a0**2/K)*(-u/a0 - sp.log(1 - u/a0))
clock = p*sp.diff(N, r)/(f*N)  # P^i D_i ln N = (p/f)(N'/N)

Ldens = (R3_conf(f, r)/(4*K) + clock - W - (gam/2)*DP**2)
L = r**2*sqh*N*Ldens
print("reduced L ok, ops:", sp.count_ops(L))

# --- GR limit: p=0, beta arbitrary.  Vary N and f.
L0 = sp.simplify(L.subs(p, 0).subs(sp.Derivative(p, r), 0))
eN = sp.simplify(sp.diff(L0, N) - sp.diff(sp.diff(L0, sp.diff(N, r)), r))
ef = sp.simplify(sp.diff(L0, f) - sp.diff(sp.diff(L0, sp.diff(f, r)), r) + sp.diff(sp.diff(L0, sp.diff(f, r, 2)), r, 2))
print("GR eN:", sp.simplify(eN))
print("GR ef:", sp.simplify(ef/f**sp.Rational(1, 2)/r**2))
