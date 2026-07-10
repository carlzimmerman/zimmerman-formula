#!/usr/bin/env python3
"""AUDIT 11: push the DIRECT seagull p^2-seed CAS deeper (single graviton is enough to test the
frame p-structure of Box_u^n; the frame kinetic p^2 needs d_x on the FRAME leg, independent of
graviton count). Run n=1..7 single-graviton, reading the p^2 seed AND whether B_n has sin(px)
(a frame gradient) or sin(qx) (graviton gradient) in the scalar."""
import sympy as sp, functools, time
print=functools.partial(print,flush=True)
t,x,y,z=sp.symbols('t x y z',real=True)
H=sp.symbols('H',positive=True)
q1,p=sp.symbols('q1 p',real=True)
e1,ep=sp.symbols('e1 ep',real=True)
crd=[t,x,y,z]
A1=sp.Function('A1')(t);V=sp.Function('V')(t)
def trunc(expr):
    expr=sp.series(expr,e1,0,2).removeO();expr=sp.series(expr,ep,0,3).removeO()
    return sp.expand(expr)
a=sp.exp(H*t)
h=e1*A1*sp.cos(q1*x)
g=sp.diag(-1,a**2,a**2*(1+h),a**2*(1-h))
gi=g.inv();n=4
G=[[[sp.Integer(0)]*n for _ in range(n)] for _ in range(n)]
for l in range(n):
    for m in range(n):
        for nu in range(n):
            G[l][m][nu]=trunc(sum(gi[l,s]*(sp.diff(g[s,m],crd[nu])+sp.diff(g[s,nu],crd[m])-sp.diff(g[m,nu],crd[s])) for s in range(n))/2)
uy=ep*V*sp.cos(p*x)
u0=sp.symbols('u0d')
sol=sp.solve(sp.Eq(g[0,0]*u0**2+g[2,2]*uy**2,-1),u0)
pick=[s for s in sol if sp.simplify(s.subs({e1:0,ep:0})-1)==0]
u0v=trunc(pick[0])
u_up=sp.Matrix([u0v,0,uy,0])
u_low=sp.Matrix([trunc(sum(g[m,nn]*u_up[nn] for nn in range(4))) for m in range(4)])
def Dop(w):
    out=[]
    for m in range(n):
        e=0
        for al in range(n):
            e+=u_up[al]*(sp.diff(w[m],crd[al])-sum(G[l][al][m]*w[l] for l in range(n)))
        out.append(trunc(e))
    return sp.Matrix(out)
Cq1,Sq1,Cp,Sp=sp.symbols('Cq1 Sq1 Cp Sp',real=True)
def strip(c):
    ct=sp.expand_trig(sp.expand(c))
    for kk,vv in {sp.cos(q1*x):Cq1,sp.sin(q1*x):Sq1,sp.cos(p*x):Cp,sp.sin(p*x):Sp}.items(): ct=ct.subs(kk,vv)
    ct=sp.expand_trig(sp.expand(ct))
    for kk,vv in {sp.cos(q1*x):Cq1,sp.sin(q1*x):Sq1,sp.cos(p*x):Cp,sp.sin(p*x):Sp}.items(): ct=ct.subs(kk,vv)
    return sp.expand(ct)
v=u_low
for k in range(1,15):
    v=Dop(v)
    if k%2==0:
        nn=k//2
        B=trunc(sum(u_up[m]*v[m] for m in range(4)))
        seag=sp.expand(B).coeff(e1,1).coeff(ep,2)
        s=strip(seag)
        p2=sp.simplify(sp.Poly(s,p).nth(2)) if s.has(p) else sp.Integer(0)
        print(f"n={nn} (single grav): p^2 seed={p2} | B_n has sin(px)?={seag.has(sp.sin(p*x))} sin(qx)?={seag.has(sp.sin(q1*x))} | explicit q?={s.has(q1)}")
