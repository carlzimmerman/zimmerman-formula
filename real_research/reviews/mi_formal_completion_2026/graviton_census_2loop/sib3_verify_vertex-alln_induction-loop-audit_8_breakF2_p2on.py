#!/usr/bin/env python3
"""AUDIT 8: does the F2-break (u.grad -> u.grad + lam d_x) switch a p^2 SPATIAL seed ON in the
seagull (Method 1's prove-by-moving)? If yes at n=1,2 with lam-carrying p^2, the extractor is
proven sensitive to a genuine spatial cone. Reproduce independently."""
import sympy as sp, functools, time
print=functools.partial(print,flush=True)
t,x,y,z=sp.symbols('t x y z',real=True)
H=sp.symbols('H',positive=True)
q1,q2,p,lam=sp.symbols('q1 q2 p lambda',real=True)
e1,e2,ep=sp.symbols('e1 e2 ep',real=True)
crd=[t,x,y,z]
A1=sp.Function('A1')(t);A2=sp.Function('A2')(t);V=sp.Function('V')(t)
def trunc(expr):
    expr=sp.series(expr,e1,0,2).removeO();expr=sp.series(expr,e2,0,2).removeO();expr=sp.series(expr,ep,0,3).removeO()
    return sp.expand(expr)
def christoffel(g):
    n=4;gi=g.inv();G=[[[0]*n for _ in range(n)] for _ in range(n)]
    for l in range(n):
        for m in range(n):
            for nu in range(n):
                G[l][m][nu]=trunc(sum(gi[l,s]*(sp.diff(g[s,m],crd[nu])+sp.diff(g[s,nu],crd[m])-sp.diff(g[m,nu],crd[s])) for s in range(n))/2)
    return G
def Dop(w,u,G,break_F2):
    n=4;out=[]
    for m in range(n):
        e=0
        for al in range(n):
            e+=u[al]*(sp.diff(w[m],crd[al])-sum(G[l][al][m]*w[l] for l in range(n)))
        if break_F2:
            e+=lam*(sp.diff(w[m],x)-sum(G[l][1][m]*w[l] for l in range(n)))
        out.append(trunc(e))
    return sp.Matrix(out)
def build():
    a=sp.exp(H*t)
    h=e1*A1*sp.cos(q1*x)+e2*A2*sp.cos(q2*x)
    g=sp.diag(-1,a**2,a**2*(1+h),a**2*(1-h))
    G=christoffel(g)
    uy=ep*V*sp.cos(p*x)
    u0=sp.symbols('u0d')
    sol=sp.solve(sp.Eq(g[0,0]*u0**2+g[2,2]*uy**2,-1),u0)
    pick=[s for s in sol if sp.simplify(s.subs({e1:0,e2:0,ep:0})-1)==0]
    u0v=trunc(pick[0])
    u_up=sp.Matrix([u0v,0,uy,0])
    u_low=sp.Matrix([trunc(sum(g[m,nn]*u_up[nn] for nn in range(4))) for m in range(4)])
    return g,u_low,u_up,G
def seagull(n,break_F2):
    g,u_low,u_up,G=build()
    v=u_low
    for _ in range(2*n):
        v=Dop(v,u_up,G,break_F2)
    B=trunc(sp.expand(sum(u_up[m]*v[m] for m in range(4))))
    return sp.expand(B.coeff(e1,1).coeff(e2,1).coeff(ep,2))
Cq1,Sq1,Cq2,Sq2,Cp,Sp=sp.symbols('Cq1 Sq1 Cq2 Sq2 Cp Sp',real=True)
def strip(c):
    ct=sp.expand_trig(sp.expand(c))
    subd={sp.cos(q1*x):Cq1,sp.sin(q1*x):Sq1,sp.cos(q2*x):Cq2,sp.sin(q2*x):Sq2,sp.cos(p*x):Cp,sp.sin(p*x):Sp}
    for kk,vv in subd.items(): ct=ct.subs(kk,vv)
    ct=sp.expand_trig(sp.expand(ct))
    for kk,vv in subd.items(): ct=ct.subs(kk,vv)
    return sp.expand(ct)
for n in (1,2):
    ci=seagull(n,False); si=strip(ci); p2i=sp.simplify(sp.Poly(si,p).nth(2)) if si.has(p) else sp.Integer(0)
    cb=seagull(n,True);  sb=strip(cb); p2b=sp.simplify(sp.Poly(sb,p).nth(2)) if sb.has(p) else sp.Integer(0)
    print(f"n={n}: F2-INTACT p^2 seed = {p2i}  ||  F2-BROKEN p^2 seed = {p2b}  (lam-carrying? {p2b.has(lam) if p2b!=0 else False})")
