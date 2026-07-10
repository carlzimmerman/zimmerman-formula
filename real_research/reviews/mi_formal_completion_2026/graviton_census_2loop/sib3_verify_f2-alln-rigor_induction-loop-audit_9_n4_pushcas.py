#!/usr/bin/env python3
r"""
Push the GENUINE dressed-CAS seagull p-structure to n=4 (2n=8 covariant derivatives),
same-pol TT, exact dS -- one order PAST the banked n=3. Independent skeptic code.
Also n=4 F2-break control (must show p turns ON) to confirm sensitivity at n=4.
"""
import sympy as sp, functools, sys, time
print=functools.partial(print, flush=True)
t,x,y,z=sp.symbols('t x y z',real=True)
H=sp.symbols('H',positive=True)
q,p,lam=sp.symbols('q p lambda',real=True)
e,e2=sp.symbols('e e2',real=True)
crd=[t,x,y,z]
HTT=sp.Function('H_TT')(t); V=sp.Function('V')(t)

def trunc(ex):
    ex=sp.series(ex,e,0,3).removeO()
    ex=sp.series(ex,e2,0,3).removeO()
    return sp.expand(ex)

a=sp.exp(H*t)
h=e2*HTT*sp.cos(q*x)
g=sp.diag(-1,a**2,a**2*(1+h),a**2*(1-h))
gi=g.inv()
n=4
G=[[[0]*n for _ in range(n)] for _ in range(n)]
for l in range(n):
    for m in range(n):
        for nu in range(n):
            G[l][m][nu]=trunc(sum(gi[l,s]*(sp.diff(g[s,m],crd[nu])+sp.diff(g[s,nu],crd[m])
                            -sp.diff(g[m,nu],crd[s])) for s in range(n))/2)
uy=e*V*sp.cos(p*x)
u0=sp.symbols('u0d')
sol=sp.solve(sp.Eq(g[0,0]*u0**2+g[2,2]*uy**2,-1),u0)
pick=[s for s in sol if sp.simplify(s.subs({e:0,e2:0})-1)==0]
u0v=trunc(pick[0])
u_up=sp.Matrix([u0v,0,uy,0])
u_low=sp.Matrix([trunc(sum(g[m,nn]*u_up[nn] for nn in range(4))) for m in range(4)])

def Dop(w,break_F2=False):
    out=[]
    for m in range(4):
        ex=0
        for al in range(4):
            ex+=u_up[al]*(sp.diff(w[m],crd[al])-sum(G[l][al][m]*w[l] for l in range(4)))
        if break_F2:
            ex+=lam*(sp.diff(w[m],x)-sum(G[l][1][m]*w[l] for l in range(4)))
        out.append(trunc(ex))
    return sp.Matrix(out)

def seagull(N,break_F2=False):
    v=u_low
    for _ in range(2*N):
        v=Dop(v,break_F2=break_F2)
    B=trunc(sp.expand(sum(u_up[m]*v[m] for m in range(4))))
    return sp.expand(B.coeff(e,2).coeff(e2,2))

Cq,Sq,Cp,Sp=sp.symbols('Cq Sq Cp Sp',real=True)
def strip(c):
    c=sp.expand_trig(sp.expand(c))
    rep={sp.cos(q*x):Cq,sp.sin(q*x):Sq,sp.cos(p*x):Cp,sp.sin(p*x):Sp,
         sp.cos((q+p)*x):Cq*Cp-Sq*Sp,sp.cos((q-p)*x):Cq*Cp+Sq*Sp,
         sp.sin((q+p)*x):Sq*Cp+Cq*Sp,sp.sin((q-p)*x):Sq*Cp-Cq*Sp,
         sp.cos(2*q*x):Cq**2-Sq**2,sp.sin(2*q*x):2*Sq*Cq,
         sp.cos(2*p*x):Cp**2-Sp**2,sp.sin(2*p*x):2*Sp*Cp,
         sp.cos(2*(q+p)*x):(Cq*Cp-Sq*Sp)**2-(Sq*Cp+Cq*Sp)**2,
         sp.cos(2*(q-p)*x):(Cq*Cp+Sq*Sp)**2-(Sq*Cp-Cq*Sp)**2}
    for k_,v_ in rep.items(): c=c.subs(k_,v_)
    return sp.expand(c)

def pinfo(c):
    s=strip(c)
    if not s.has(p): return sp.Integer(0),sp.Integer(0),0,False
    P=sp.Poly(s,p)
    p2=sp.simplify(P.nth(2)); p1=sp.simplify(P.nth(1))
    powers=[int(m[0]) for m in P.monoms()]
    anyp=any(k>=1 for k in powers)
    return p2,p1,max(powers),anyp

t0=time.time()
c4=seagull(4)
p2,p1,mx,anyp=pinfo(c4)
print(f"[same] n=4 (2n=8 cov derivs): p^2={p2} | p^1={p1} | max-p={mx if anyp else 0} | mass(p^0)!=0? {strip(c4).subs({p:0})!=0} | benign(p^2=0)? {sp.simplify(p2)==0} [{time.time()-t0:.1f}s]")

t1=time.time()
c4b=seagull(4,break_F2=True)
p2b,p1b,mxb,anypb=pinfo(c4b)
print(f"[same] n=4 F2-BROKEN control: p^2 nonzero? {sp.simplify(p2b)!=0} | any explicit p? {anypb} [{time.time()-t1:.1f}s]")
print("RESULT: n=4 p-free" if sp.simplify(p2)==0 else "RESULT: n=4 HAS p^2 CONE (FATAL)")
sys.exit(0)
