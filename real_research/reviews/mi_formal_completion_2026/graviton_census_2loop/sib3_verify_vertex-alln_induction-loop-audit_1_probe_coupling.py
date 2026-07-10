#!/usr/bin/env python3
"""AUDIT 1: Does the graviton actually couple to the frame in the seagull coeff at all?
If seagull_coeff(1) is IDENTICALLY ZERO or has no q anywhere BEFORE stripping, the whole
test is vacuous (q-explicit=False could just mean 'no coupling', not 'benign mass')."""
import sympy as sp, functools
print=functools.partial(print,flush=True)
t,x,y,z=sp.symbols('t x y z',real=True)
H=sp.symbols('H',positive=True)
q1,q2,p=sp.symbols('q1 q2 p',real=True)
e1,e2,ep=sp.symbols('e1 e2 ep',real=True)
crd=[t,x,y,z]
A1=sp.Function('A1')(t);A2=sp.Function('A2')(t);V=sp.Function('V')(t)
ORD={'e1':1,'e2':1,'ep':2}
def trunc(expr):
    for s,o in ((e1,ORD['e1']),(e2,ORD['e2']),(ep,ORD['ep'])):
        expr=sp.series(expr,s,0,o+1).removeO()
    return sp.expand(expr)
def christoffel(g):
    n=4;gi=g.inv();G=[[[0]*n for _ in range(n)] for _ in range(n)]
    for l in range(n):
        for m in range(n):
            for nu in range(n):
                G[l][m][nu]=trunc(sum(gi[l,s]*(sp.diff(g[s,m],crd[nu])+sp.diff(g[s,nu],crd[m])-sp.diff(g[m,nu],crd[s])) for s in range(n))/2)
    return G
def Dop(w,u,G):
    n=4;out=[]
    for m in range(n):
        e=0
        for al in range(n):
            e+=u[al]*(sp.diff(w[m],crd[al])-sum(G[l][al][m]*w[l] for l in range(n)))
        out.append(trunc(e))
    return sp.Matrix(out)
def build(cross=False):
    a=sp.exp(H*t)
    h=e1*A1*sp.cos(q1*x)+e2*A2*sp.cos(q2*x)
    g=sp.diag(-1,a**2,a**2*(1+h),a**2*(1-h))
    G=christoffel(g)
    uy=ep*V*sp.cos(p*x)
    u0=sp.symbols('u0d')
    sol=sp.solve(sp.Eq(g[0,0]*u0**2+g[2,2]*uy**2,-1),u0)
    pick=[s for s in sol if sp.simplify(s.subs({e1:0,e2:0,ep:0})-1)==0]
    u0v=trunc(pick[0] if pick else sol[0])
    u_up=sp.Matrix([u0v,0,uy,0])
    u_low=sp.Matrix([trunc(sum(g[m,nn]*u_up[nn] for nn in range(4))) for m in range(4)])
    return g,u_low,u_up,G
def Bn(n,g,u_low,u_up,G):
    v=u_low
    for _ in range(2*n):
        v=Dop(v,u_up,G)
    return trunc(sp.expand(sum(u_up[m]*v[m] for m in range(4))))

g,u_low,u_up,G=build()
print("u_up =",u_up.T)
print("u_low=",u_low.T)
# The FULL B_1 before pulling coeffs
B1=Bn(1,g,u_low,u_up,G)
print("\n--- FULL B_1 order content ---")
# what orders in e1,e2,ep are present?
poly=sp.Poly(B1,e1,e2,ep)
print("monomials (e1,e2,ep):",sorted(set((m[0],m[1],m[2]) for m in poly.monoms())))
sea=sp.expand(B1.coeff(e1,1).coeff(e2,1).coeff(ep,2))
print("\n--- seagull coeff e1^1 e2^1 ep^2 (RAW, before strip) ---")
print("is zero?",sea==0)
print("has q1?",sea.has(q1)," has q2?",sea.has(q2)," has p?",sea.has(p))
print("has sin(q1 x)?",sea.has(sp.sin(q1*x))," has cos(q1 x)?",sea.has(sp.cos(q1*x)))
print("\nRAW seagull:",sea)
