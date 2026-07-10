#!/usr/bin/env python3
"""AUDIT 9: reconcile the F2-break control. Compute the n=1 BROKEN seagull raw, inspect whether
it carries an EXPLICIT p at all (a p^2 spatial seed), and check what Method 1's assertion sees.
The claim under audit: does breaking F2 switch a p^2 SPATIAL seed ON, or only a lam*q (graviton
momentum, not frame p) term? If only lam*q, the control does NOT demonstrate p^2-frame-cone
sensitivity -- a weaker prove-by-moving than advertised."""
import sympy as sp, functools
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
v=u_low
for _ in range(2):
    v=Dop(v,u_up,G,True)
B=trunc(sp.expand(sum(u_up[m]*v[m] for m in range(4))))
sea=sp.expand(B.coeff(e1,1).coeff(e2,1).coeff(ep,2))
print("BROKEN n=1 seagull raw:")
print(" ",sea)
print("\nhas explicit p?",sea.has(p))
print("has explicit q1 or q2?",sea.has(q1) or sea.has(q2))
print("has sin(px)?",sea.has(sp.sin(p*x)),"  has sin(qx)?",sea.has(sp.sin(q1*x)) or sea.has(sp.sin(q2*x)))
print("has lam?",sea.has(lam))
# strip and read p^2
Cq1,Sq1,Cq2,Sq2,Cp,Sp=sp.symbols('Cq1 Sq1 Cq2 Sq2 Cp Sp',real=True)
ct=sp.expand_trig(sp.expand(sea))
for kk,vv in {sp.cos(q1*x):Cq1,sp.sin(q1*x):Sq1,sp.cos(q2*x):Cq2,sp.sin(q2*x):Sq2,sp.cos(p*x):Cp,sp.sin(p*x):Sp}.items(): ct=ct.subs(kk,vv)
ct=sp.expand(ct)
p2 = sp.simplify(sp.Poly(ct,p).nth(2)) if ct.has(p) else sp.Integer(0)
print("\nstripped p^2 seed of BROKEN n=1 =",p2)
# where does lam*momentum sit? coeff of lam
lc=sp.expand(ct.coeff(lam,1))
print("lam^1 coeff (stripped): has p?",lc.has(p)," has q?",lc.has(q1) or lc.has(q2))
print("  lam^1 coeff =",lc)
