"""
LANE A -- higher-n, done EFFICIENTLY. At O(eps^2) in the quadratic action we only need u
to O(eps^1). Expand u_low, u_up in eps to linear order FIRST (kills the sqrt), then apply
Box_u (whose u^a coefficients we also expand). The quadratic form needs:
  B_n^(2) = [ u^(0).Box^(n)(u)^(2)  cross terms ]  collected at O(eps^2).
Simplest robust route: substitute a PLANE WAVE for phi from the start (phi = A e^{i(wt-kx)}),
expand in eps to O(eps^2), extract the |A|^2 (i.e. eps^2) coefficient = the dispersion symbol.
"""
import sympy as sp

t, x, eps, om, kk = sp.symbols('t x epsilon omega k', real=True)
coords2 = [t, x]
eta2inv = sp.diag(-1, 1)
# use complex conjugate pair to get a real quadratic form: phi = e^{i(wt-kx)} + c.c. is messy;
# instead use phi = cos(om*t - kk*x); then eps^2 coeff time-averaged gives symbol up to const.
phi = sp.cos(om*t - kk*x)
T = t + eps*phi
dT = sp.Matrix([sp.diff(T, c) for c in coords2])
norm2 = sum(eta2inv[i, i]*dT[i]**2 for i in range(2))
denom = sp.sqrt(-norm2)
u_low = sp.Matrix([sp.series(-dT[i]/denom, eps, 0, 2).removeO() for i in range(2)])
u_up = sp.Matrix([sp.expand(eta2inv[i, i]*u_low[i]) for i in range(2)])

def box_u(F):
    inner = sum(u_up[b]*sp.diff(F, coords2[b]) for b in range(2))
    inner = sp.series(sp.expand(inner), eps, 0, 2).removeO()
    outer = sum(u_up[a]*sp.diff(inner, coords2[a]) for a in range(2))
    return sp.series(sp.expand(outer), eps, 0, 2).removeO()

def eps2coeff(expr):
    e = sp.expand(expr)
    c = e.coeff(eps, 2)
    # time/space average of the oscillatory eps^2 term -> replace cos^2->1/2, sin^2->1/2, cross->0
    c = c.rewrite(sp.cos)
    c = sp.simplify(c)
    return c

for n in [1, 2, 3]:
    v = u_low
    for _ in range(n):
        v = sp.Matrix([box_u(v[i]) for i in range(2)])
    Bn = sum(u_up[i]*v[i] for i in range(2))
    c2 = eps2coeff(Bn)
    # substitute a point to read magnitude vs (om,kk): evaluate at t=0,x=0 after averaging is
    # not clean; instead just print the simplified symbol structure in om,kk.
    c2s = sp.simplify(sp.expand_trig(c2))
    print(f"n={n}: O(eps^2) coeff (symbol ~ in omega,k):")
    sp.pprint(sp.trigsimp(c2s))
    print()
