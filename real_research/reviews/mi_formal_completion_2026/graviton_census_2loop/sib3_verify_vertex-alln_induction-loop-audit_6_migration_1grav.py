#!/usr/bin/env python3
"""AUDIT 6: migration test with a SINGLE graviton (e1) + frame (ep), tracking sin(qx) location
in D^k u through k=1..8 (n up to 4). Enough to see if the graviton gradient escapes the
x-component into t/y (survival) or stays trapped (killed by u^x=0)."""
import sympy as sp, functools, time
print=functools.partial(print,flush=True)
t,x=sp.symbols('t x',real=True)
y,z=sp.symbols('y z',real=True)
H=sp.symbols('H',positive=True)
q1,p=sp.symbols('q1 p',real=True)
e1,ep=sp.symbols('e1 ep',real=True)
crd=[t,x,y,z]; nm=['t','x','y','z']
A1=sp.Function('A1')(t);V=sp.Function('V')(t)
def trunc(expr):
    expr=sp.series(expr,e1,0,2).removeO()
    expr=sp.series(expr,ep,0,3).removeO()
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
v=u_low
for k in range(1,9):
    t0=time.time()
    v=Dop(v)
    comps=[nm[m] for m in range(4) if v[m].has(sp.sin(q1*x))]
    # does the x-comp still hold sinq, and do t/y/z comps EVER get it?
    escaped = [nm[m] for m in (0,2,3) if v[m].has(sp.sin(q1*x))]  # t,y,z (non-x)
    cross=[nm[m] for m in range(4) if v[m].has(sp.sin(q1*x)) and v[m].has(sp.sin(p*x))]
    print(f"D^{k} u: sinq in comps={comps} | ESCAPED to non-x (t/y/z)?={escaped} | sinq&sinp cross={cross}  [{time.time()-t0:.1f}s]")
    if k%2==0:
        B=trunc(sum(u_up[m]*v[m] for m in range(4)))
        seag=sp.expand(B).coeff(e1,1).coeff(ep,2)
        has_sinq = seag.has(sp.sin(q1*x)); has_sinp=seag.has(sp.sin(p*x))
        print(f"   B_{k//2}=u.D^{k}u seagull(e1 ep^2): has sin(qx)?={has_sinq} has sin(px)?={has_sinp}")
