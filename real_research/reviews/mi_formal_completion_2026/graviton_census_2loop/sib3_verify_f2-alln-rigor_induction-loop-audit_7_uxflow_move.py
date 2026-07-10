#!/usr/bin/env python3
r"""PROVE-BY-MOVING at the PHYSICAL level on the FULL tensor: give the 4-velocity a genuine
x-flow u^x = beta (break F2/longitudinality physically, not via a bare lam d_x). If the p-free
result is EARNED by u^x=0, then u^x=beta!=0 must switch a p-polynomial ON in the full seagull.
n=1 suffices to demonstrate. Uses complex phases for a clean p detector."""
import sympy as sp, functools, importlib.util
print=functools.partial(print, flush=True)
spec=importlib.util.spec_from_file_location('s1','sib3_setup_1_seagull_vertex_generaln.py')
s1=importlib.util.module_from_spec(spec); spec.loader.exec_module(s1)
trunc=s1.trunc; eps=s1.eps; eps2=s1.eps2; p=s1.p; q=s1.q
t,x,y,z=s1.t,s1.x,s1.y,s1.z; crd=[t,x,y,z]; I=sp.I; H=s1.H
a=sp.exp(H*t)
h=eps2*sp.Function('H_TT')(t)*sp.exp(I*q*x)
g=sp.diag(-1,a**2,a**2*(1+h),a**2*(1-h))
G=s1.christoffel(g); V=sp.Function('V')(t)

def run(beta):
    """beta = background x-flow (u^x). beta=0 -> F2 intact; beta!=0 -> longitudinality broken."""
    uy_up=eps*V*sp.exp(I*p*x)
    ux_up=sp.Rational(beta) if beta!=0 else sp.Integer(0)
    g00=g[0,0]; gxx=g[1,1]; gyy=g[2,2]; u0=sp.symbols('u0d')
    sol=sp.solve(sp.Eq(g00*u0**2+gxx*ux_up**2+gyy*uy_up**2,-1),u0)
    pick=[s for s in sol if sp.simplify(s.subs({eps:0,eps2:0}))!=0 and sp.im(sp.simplify(s.subs({eps:0,eps2:0,H:1,t:0})))==0]
    u0v=trunc(pick[0]) if pick else trunc(sol[0])
    u_up=sp.Matrix([u0v,ux_up,uy_up,0])
    u_low=sp.Matrix([trunc(sum(g[m,nn]*u_up[nn] for nn in range(4))) for m in range(4)])
    def Dop(w):
        out=[]
        for m in range(4):
            e=sum(u_up[al]*(sp.diff(w[m],crd[al]) - sum(G[l][al][m]*w[l] for l in range(4))) for al in range(4))
            out.append(trunc(e))
        return sp.Matrix(out)
    v=u_low
    for _ in range(2):   # n=1
        v=Dop(v)
    B=trunc(sp.expand(sum(u_up[m]*v[m] for m in range(4))))
    c=sp.expand(B.coeff(eps,2).coeff(eps2,2))
    cne=sp.expand(c).replace(lambda e: e.func==sp.exp, lambda e: sp.Integer(1))
    return sp.expand(cne).has(p)

print("F2 INTACT   (u^x=0):    p-polynomial on frame kinetic?", run(0))
print("F2 BROKEN   (u^x=1/3):  p-polynomial on frame kinetic?", run(sp.Rational(1,3)))
