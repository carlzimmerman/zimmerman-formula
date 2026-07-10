#!/usr/bin/env python3
"""AUDIT 3: My OWN independent CAS to n=3, tracking whether the graviton SPATIAL gradient
(sin(qx), carrying q) OR a frame spatial gradient (sin(px), carrying p) ever reaches the
seagull vertex. The danger is NOT just 'p^2 seed !=0' -- it's whether d_x EVER acts, since
if only cos(qx),cos(px) survive the coupling is genuinely gradient-free (mass-type).
I also check n=3 raw for any sin(qx) or sin(px) or explicit p/q."""
import sympy as sp, functools, time
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
    if not cross:
        h=e1*A1*sp.cos(q1*x)+e2*A2*sp.cos(q2*x)
        g=sp.diag(-1,a**2,a**2*(1+h),a**2*(1-h))
    else:
        hc=e1*A1*sp.cos(q1*x)+e2*A2*sp.cos(q2*x)
        g=sp.Matrix([[-1,0,0,0],[0,a**2,0,0],[0,0,a**2,a**2*hc],[0,0,a**2*hc,a**2]])
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
        v=Dop(v,u,G) if False else Dop(v,u_up,G)
    return trunc(sp.expand(sum(u_up[m]*v[m] for m in range(4))))
def seagull(n,cross=False):
    g,u_low,u_up,G=build(cross=cross)
    return sp.expand(Bn(n,g,u_low,u_up,G).coeff(e1,1).coeff(e2,1).coeff(ep,2))

Cq1,Sq1,Cq2,Sq2,Cp,Sp=sp.symbols('Cq1 Sq1 Cq2 Sq2 Cp Sp',real=True)
def strip(c):
    ct=sp.expand_trig(sp.expand(c))
    subd={sp.cos(q1*x):Cq1,sp.sin(q1*x):Sq1,sp.cos(q2*x):Cq2,sp.sin(q2*x):Sq2,sp.cos(p*x):Cp,sp.sin(p*x):Sp}
    for kk,vv in subd.items(): ct=ct.subs(kk,vv)
    ct=sp.expand_trig(sp.expand(ct))
    for kk,vv in subd.items(): ct=ct.subs(kk,vv)
    return sp.expand(ct)

for cross in (False,True):
    lab='cross' if cross else 'same'
    for n in (1,2,3):
        t0=time.time()
        c=seagull(n,cross=cross)
        raw_has_sinq = c.has(sp.sin(q1*x)) or c.has(sp.sin(q2*x))
        raw_has_sinp = c.has(sp.sin(p*x))
        s=strip(c)
        p2 = sp.simplify(sp.Poly(s,p).nth(2)) if s.has(p) else sp.Integer(0)
        # explicit q power (a bare q1 or q2 as polynomial factor, meaning d_x hit the graviton)
        q_poly = s.has(q1) or s.has(q2)
        print(f"{lab} n={n}: RAW has sin(qx)? {raw_has_sinq} | RAW has sin(px)? {raw_has_sinp} "
              f"| stripped explicit-q? {q_poly} | p^2 seed = {p2}  [{time.time()-t0:.1f}s]")
