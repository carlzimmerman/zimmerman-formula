#!/usr/bin/env python3
r"""
SKEPTIC probe 2: (A) SENSITIVITY CONTROL for probe 1 -- prove my kappa-detector actually
catches a spatial gradient when one is really there, by injecting a BARE lam*d_y (a background
transverse derivative NOT rationed by u^y).  If kappa^2 switches ON, the detector is sensitive
and the kappa^2=0 of probe 1 is a real physics statement.
(B) Push frame-momentum-along-y to n=4 (2n=8 covariant derivatives).
(C) FULLY GENERAL frame momentum: u^y = ep V cos(a x + b y) with BOTH x- and y-components,
    so d_y AND (via connection) the x-structure are both live -- the most general external
    frame spatial momentum. Look for ANY spatial p^2 (a^2, b^2, or a*b) seed at ep^2.
"""
import sympy as sp, functools
print=functools.partial(print, flush=True)
def sec(t): print("\n"+"="*90+"\n "+t+"\n"+"="*90)

t,x,y,z=sp.symbols('t x y z',real=True)
H=sp.symbols('H',positive=True)
q,kap,lam=sp.symbols('q kappa lambda',real=True)
aa,bb=sp.symbols('a_x b_y',real=True)      # general frame momentum components
ep,e2=sp.symbols('ep e2',real=True)
crd=[t,x,y,z]
A=sp.Function('A')(t); V=sp.Function('V')(t)
MAXep=2; MAXe2=2
def trunc(e):
    e=sp.series(e,ep,0,MAXep+1).removeO(); e=sp.series(e,e2,0,MAXe2+1).removeO()
    return sp.expand(e)
def christoffel(g):
    n=4; gi=g.inv(); G=[[[0]*n for _ in range(n)] for _ in range(n)]
    for l in range(n):
        for m in range(n):
            for nu in range(n):
                G[l][m][nu]=trunc(sum(gi[l,s]*(sp.diff(g[s,m],crd[nu])+sp.diff(g[s,nu],crd[m])
                                -sp.diff(g[m,nu],crd[s])) for s in range(n))/2)
    return G
def Dop(w_low,u_up,G,break_dy=False):
    n=4; out=[]
    for m in range(n):
        e=0
        for al in range(n):
            e+=u_up[al]*(sp.diff(w_low[m],crd[al]) - sum(G[l][al][m]*w_low[l] for l in range(n)))
        if break_dy:                      # inject BARE lam*d_y (unrationed transverse derivative)
            e+= lam*(sp.diff(w_low[m],y) - sum(G[l][2][m]*w_low[l] for l in range(n)))
        out.append(trunc(e))
    return sp.Matrix(out)
def build(frame='y'):
    a=sp.exp(H*t)
    h=e2*A*sp.cos(q*x)
    g=sp.diag(-1, a**2, a**2*(1+h), a**2*(1-h))
    G=christoffel(g)
    if frame=='y':   uy=ep*V*sp.cos(kap*y)
    else:            uy=ep*V*sp.cos(aa*x+bb*y)     # general mixed-direction frame momentum
    g00=g[0,0]; gyy=g[2,2]; u0=sp.symbols('u0d')
    sol=sp.solve(sp.Eq(g00*u0**2+gyy*uy**2,-1),u0)
    pick=[s for s in sol if sp.simplify(s.subs({ep:0,e2:0})-1)==0]
    u0v=trunc(pick[0] if pick else sol[0])
    u_up=sp.Matrix([u0v,0,uy,0])
    u_low=sp.Matrix([trunc(sum(g[m,nn]*u_up[nn] for nn in range(4))) for m in range(4)])
    return g,u_low,u_up,G
def Bn(n,g,u_low,u_up,G,break_dy=False):
    v=u_low
    for _ in range(2*n): v=Dop(v,u_up,G,break_dy=break_dy)
    return trunc(sp.expand(sum(u_up[m]*v[m] for m in range(4))))

Cy,Sy,Cq,Sq=sp.symbols('Cy Sy Cq Sq',real=True)
def strip_y(c):
    c=sp.expand_trig(sp.expand(c))
    sub={sp.cos(kap*y):Cy,sp.sin(kap*y):Sy,sp.cos(q*x):Cq,sp.sin(q*x):Sq,
         sp.cos(2*kap*y):Cy*Cy-Sy*Sy,sp.sin(2*kap*y):2*Sy*Cy,
         sp.cos(2*q*x):Cq*Cq-Sq*Sq,sp.sin(2*q*x):2*Sq*Cq}
    for k,v in sub.items(): c=c.subs(k,v)
    return sp.expand(c)

# ---------------------------------------------------------------------------------------
sec("(A) SENSITIVITY CONTROL: inject BARE lam*d_y -> kappa^2 spatial seed MUST switch ON")
print("  If my extraction is sensitive, an unrationed transverse d_y makes kappa appear explicitly.")
for n in (1,2):
    g,u_low,u_up,G=build(frame='y')
    B=Bn(n,g,u_low,u_up,G,break_dy=True)
    c=sp.expand(B.coeff(ep,2)); s=strip_y(c)
    k2=sp.simplify(sp.Poly(s,kap).nth(2)) if s.has(kap) else sp.Integer(0)
    print(f"  n={n}: BROKEN (bare d_y) kappa^2 seed = {k2}   (lam-carrying? {k2.has(lam) if k2!=0 else False})")

# ---------------------------------------------------------------------------------------
sec("(B) FRAME MOMENTUM ALONG y, pushed to n=4 (2n=8 covariant derivatives)")
for n in (4,):
    g,u_low,u_up,G=build(frame='y')
    B=Bn(n,g,u_low,u_up,G)
    c=sp.expand(B.coeff(ep,2)); s=strip_y(c)
    kexp=s.has(kap)
    k2=sp.simplify(sp.Poly(s,kap).nth(2)) if s.has(kap) else sp.Integer(0)
    cs=sp.expand(c.coeff(e2,2)); ssg=strip_y(cs)
    k2s=sp.simplify(sp.Poly(ssg,kap).nth(2)) if ssg.has(kap) else sp.Integer(0)
    print(f"  n={n}: kappa explicit? {kexp} | FULL kappa^2 seed = {k2} | SEAGULL kappa^2 seed = {k2s}")

# ---------------------------------------------------------------------------------------
sec("(C) FULLY GENERAL frame momentum u^y=ep V cos(a_x x + b_y y): any spatial p^2 seed?")
print("  Frame leg now carries momentum in BOTH x and y. Extract ep^2 coeff; look for a_x^2,")
print("  b_y^2, a_x*b_y (any spatial-gradient kinetic). Uses generic-argument derivative counting.")
def strip_gen(c):
    # keep explicit a_x,b_y powers: replace cos/sin(a_x x+b_y y) and cos/sin(q x) by atoms after
    # expand_trig; the polynomial a_x,b_y powers come ONLY from d_x,d_y derivatives (real momenta).
    c=sp.expand_trig(sp.expand(c))
    Cg,Sg=sp.symbols('Cg Sg',real=True)
    arg=aa*x+bb*y
    sub={sp.cos(arg):Cg,sp.sin(arg):Sg,sp.cos(2*arg):Cg*Cg-Sg*Sg,sp.sin(2*arg):2*Sg*Cg,
         sp.cos(q*x):Cq,sp.sin(q*x):Sq,sp.cos(2*q*x):Cq*Cq-Sq*Sq,sp.sin(2*q*x):2*Sq*Cq}
    for k,v in sub.items(): c=c.subs(k,v)
    return sp.expand(c)
for n in (1,2,3):
    g,u_low,u_up,G=build(frame='gen')
    B=Bn(n,g,u_low,u_up,G)
    c=sp.expand(B.coeff(ep,2)); s=strip_gen(c)
    a2=sp.simplify(s.coeff(aa,2).coeff(bb,0)) if s.has(aa) else sp.Integer(0)
    b2=sp.simplify(s.coeff(bb,2).coeff(aa,0)) if s.has(bb) else sp.Integer(0)
    ab=sp.simplify(s.coeff(aa,1).coeff(bb,1)) if (s.has(aa) and s.has(bb)) else sp.Integer(0)
    anyspatial=(a2!=0) or (b2!=0) or (ab!=0)
    print(f"  n={n}: a_x^2 seed={a2} | b_y^2 seed={b2} | a_x*b_y seed={ab} | ANY spatial p^2? {anyspatial}")

sec("DONE")
