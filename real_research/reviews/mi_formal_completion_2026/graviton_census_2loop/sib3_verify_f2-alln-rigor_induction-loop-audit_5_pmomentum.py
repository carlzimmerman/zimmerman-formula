#!/usr/bin/env python3
r"""Lighter version: use exp(I p x) frame phase and exp(I q x) graviton phase. Under F2 intact
the frame phase is a pure spectator -> p appears ONLY as the overall exp(2 I p x) phase, with NO
p-POLYNOMIAL coefficient. A p^2 spatial cone REQUIRES a p^2 polynomial (from d_x^2 cos px). So:
detect whether the eps^2 eps2^2 vertex, AFTER dividing out its overall x-phase, still contains
an explicit p. If yes -> p-polynomial -> potential cone. If no -> pure phase -> p-free.
Then break F2 and confirm p-polynomial appears (sensitivity)."""
import sympy as sp, functools, importlib.util
print=functools.partial(print, flush=True)
spec=importlib.util.spec_from_file_location('s1','sib3_setup_1_seagull_vertex_generaln.py')
s1=importlib.util.module_from_spec(spec); spec.loader.exec_module(s1)
build=s1.build; trunc=s1.trunc; eps=s1.eps; eps2=s1.eps2; p=s1.p; q=s1.q
t,x,y,z=s1.t,s1.x,s1.y,s1.z; crd=[t,x,y,z]; I=sp.I
lam=sp.Symbol('lam',real=True)

# rebuild g with graviton phase exp(I q x) (complex, so d_x brings down I*q explicitly)
H=s1.H; a=sp.exp(H*t)
h=eps2*sp.Function('H_TT')(t)*sp.exp(I*q*x)
g=sp.diag(-1,a**2,a**2*(1+h),a**2*(1-h))
G=s1.christoffel(g)
V=sp.Function('V')(t)
uy_up=eps*V*sp.exp(I*p*x)     # frame leg, complex phase -> d_x -> I p explicitly
g00=g[0,0]; gyy=g[2,2]; u0=sp.symbols('u0d')
sol=sp.solve(sp.Eq(g00*u0**2+gyy*uy_up**2,-1),u0)
pick=[s for s in sol if sp.simplify(s.subs({eps:0,eps2:0})-1)==0]
u0v=trunc(pick[0])
u_up=sp.Matrix([u0v,0,uy_up,0])
u_low=sp.Matrix([trunc(sum(g[m,nn]*u_up[nn] for nn in range(4))) for m in range(4)])
print("u^x =", sp.simplify(u_up[1]), " (must be 0)")

def Dop(w_low, break_F2=False):
    out=[]
    for m in range(4):
        e=0
        for al in range(4):
            e+=u_up[al]*(sp.diff(w_low[m],crd[al]) - sum(G[l][al][m]*w_low[l] for l in range(4)))
        if break_F2:
            e+=lam*(sp.diff(w_low[m],x) - sum(G[l][1][m]*w_low[l] for l in range(4)))
        out.append(trunc(e))
    return sp.Matrix(out)

def vertex(n, break_F2=False):
    v=u_low
    for _ in range(2*n):
        v=Dop(v, break_F2=break_F2)
    B=trunc(sp.expand(sum(u_up[m]*v[m] for m in range(4))))
    return sp.expand(B.coeff(eps,2).coeff(eps2,2))

def p_polynomial_present(c):
    """After stripping the overall x-phase exp(i*Phase*x), is there a residual explicit p?
    We divide by exp over the total x-phase. Simplest robust test: collect exp(I*k*x) factors.
    A pure spectator gives c = (poly in q, time) * exp(I*(2p+ mq) x). A p-poly on the frame
    kinetic gives an EXTRA p multiplying. We test: does d/dp of (c / c|_{overall phase}) keep p?
    Robust proxy: rewrite exps, then check if p survives OUTSIDE an exponential argument."""
    c=sp.expand(c)
    # replace every exp(I*(...)*x) by a symbol E**(coeff) is messy; instead: substitute p-> p, and
    # test whether c has p in a NON-exponential position by taking c, replacing all exp(...) -> 1,
    # and seeing if p remains.
    c_noexp = c.replace(lambda e: e.func==sp.exp, lambda e: sp.Integer(1))
    return sp.expand(c_noexp).has(p), c_noexp

print("\n=== F2 INTACT: is there a p-POLYNOMIAL (momentum) on the frame kinetic? (must be NO) ===")
for n in (1,2,3):
    c=vertex(n, break_F2=False)
    has_ppoly, cne = p_polynomial_present(c)
    print(f"  n={n}: p-polynomial present (after stripping phases)? {has_ppoly}   [{'p-FREE, spectator phase only' if not has_ppoly else 'P-CONE POSSIBLE'}]")

print("\n=== F2 BROKEN: p-polynomial MUST appear (sensitivity of the test) ===")
for n in (1,2):
    c=vertex(n, break_F2=True)
    has_ppoly, cne = p_polynomial_present(c)
    print(f"  n={n}: p-polynomial present? {has_ppoly}  [{'DETECTED cone seed' if has_ppoly else 'MISS'}]")
