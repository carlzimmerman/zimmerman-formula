#!/usr/bin/env python3
"""AUDIT 5: THE REAL INDUCTION. The graviton gradient sin(qx) enters via u^y Gamma^l_{y m}.
Track, component by component, whether sin(qx) MIGRATES out of the x-component of D^k u into
the t/y/z components as k grows. If it stays trapped in the x-component, u^mu(...)_mu kills it
(u^x=0) -> no q-gradient reaches the scalar -> p-free. If it migrates to t/y at some k, it
COULD survive -> potential cone. This is the genuine all-n question the setup's ansatz skipped.

Track which components of D^k u carry sin(qx), for k=1..6 (i.e. n up to 3), AND whether the
final scalar B_n = u.(D^{2n}u) picks up any sin(qx)*sin(px) (a p AND q gradient = cone seed)."""
import sympy as sp, functools, time
print=functools.partial(print,flush=True)
t,x,y,z=sp.symbols('t x y z',real=True)
H=sp.symbols('H',positive=True)
q1,q2,p=sp.symbols('q1 q2 p',real=True)
e1,e2,ep=sp.symbols('e1 e2 ep',real=True)
crd=[t,x,y,z]; nm=['t','x','y','z']
A1=sp.Function('A1')(t);A2=sp.Function('A2')(t);V=sp.Function('V')(t)
def trunc(expr):
    for s in (e1,e2,ep):
        expr=sp.series(expr,s,0,2).removeO() if s in (e1,e2) else sp.series(expr,s,0,3).removeO()
    return sp.expand(expr)
a=sp.exp(H*t)
h=e1*A1*sp.cos(q1*x)+e2*A2*sp.cos(q2*x)
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
pick=[s for s in sol if sp.simplify(s.subs({e1:0,e2:0,ep:0})-1)==0]
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
Cq1,Sq1,Cq2,Sq2,Cp,Sp=sp.symbols('Cq1 Sq1 Cq2 Sq2 Cp Sp',real=True)
def strip(c):
    ct=sp.expand_trig(sp.expand(c))
    subd={sp.cos(q1*x):Cq1,sp.sin(q1*x):Sq1,sp.cos(q2*x):Cq2,sp.sin(q2*x):Sq2,sp.cos(p*x):Cp,sp.sin(p*x):Sp}
    for kk,vv in subd.items(): ct=ct.subs(kk,vv)
    ct=sp.expand_trig(sp.expand(ct));  [ct:=ct.subs(kk,vv) for kk,vv in subd.items()]
    return sp.expand(ct)

v=u_low
KMAX=6
for k in range(1,KMAX+1):
    t0=time.time()
    v=Dop(v)
    comps_with_sinq=[nm[m] for m in range(4) if (v[m].has(sp.sin(q1*x)) or v[m].has(sp.sin(q2*x)))]
    # cross gradient in a component: does any component carry sin(qx)*sin(px) (q AND p gradient)?
    cross_grad=[nm[m] for m in range(4) if ((v[m].has(sp.sin(q1*x)) or v[m].has(sp.sin(q2*x))) and v[m].has(sp.sin(p*x)))]
    print(f"D^{k} u: components carrying sin(qx) = {comps_with_sinq} | carrying sin(qx)&sin(px) = {cross_grad}  [{time.time()-t0:.1f}s]")
    if k%2==0:
        nn=k//2
        B=trunc(sum(u_up[m]*v[m] for m in range(4)))
        s=strip(sp.expand(B).coeff(e1,1).coeff(e2,1).coeff(ep,2))
        p2=sp.simplify(sp.Poly(s,p).nth(2)) if s.has(p) else sp.Integer(0)
        print(f"   -> B_{nn}=u.D^{k}u : seagull p^2 seed = {p2} | explicit-q in seagull? {s.has(q1) or s.has(q2)}")
