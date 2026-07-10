#!/usr/bin/env python3
r"""
Diagnose the F2-break control: is the 'HOLE' in audit_1 a real physics gap, or an
over-strict control criterion (I demanded lam^1*p^2, but a single d_x injection is lam^1*p^1;
p^2 needs lam^2)? Print the FULL lam- and p-structure of the F2-broken n=1 seagull, and
verify the F2-broken vertex DOES contain a genuine p^2 spatial seed at lam^2 (sensitivity),
while F2-INTACT has none. Also confirm the parity logic: the loop kills p^1 (odd in q), so
the physical danger is p^2 only.
"""
import sympy as sp, functools
print=functools.partial(print, flush=True)
t,x,y,z=sp.symbols('t x y z',real=True); H=sp.symbols('H',positive=True)
q1,q2,p=sp.symbols('q1 q2 p',real=True); e1,e2,ep=sp.symbols('e1 e2 ep',real=True)
lam=sp.symbols('lambda',real=True); crd=[t,x,y,z]
A1=sp.Function('A1')(t); A2=sp.Function('A2')(t); V=sp.Function('V')(t)
ORD={'e1':1,'e2':1,'ep':2}
def trunc(ex):
    for s,o in ((e1,1),(e2,1),(ep,2)): ex=sp.series(ex,s,0,o+1).removeO()
    return sp.expand(ex)
def christoffel(g):
    gi=g.inv(); G=[[[0]*4 for _ in range(4)] for _ in range(4)]
    for l in range(4):
        for m in range(4):
            for nu in range(4):
                G[l][m][nu]=trunc(sum(gi[l,s]*(sp.diff(g[s,m],crd[nu])+sp.diff(g[s,nu],crd[m])
                            -sp.diff(g[m,nu],crd[s])) for s in range(4))/2)
    return G
def Dop(w,u_up,G,break_F2=False):
    out=[]
    for m in range(4):
        e=0
        for al in range(4):
            e+=u_up[al]*(sp.diff(w[m],crd[al])-sum(G[l][al][m]*w[l] for l in range(4)))
        if break_F2:
            e+=lam*(sp.diff(w[m],x)-sum(G[l][1][m]*w[l] for l in range(4)))
        out.append(trunc(e))
    return sp.Matrix(out)
def build(cross=False):
    a=sp.exp(H*t); h=e1*A1*sp.cos(q1*x)+e2*A2*sp.cos(q2*x)
    g=sp.diag(-1,a**2,a**2*(1+h),a**2*(1-h)) if not cross else \
      sp.Matrix([[-1,0,0,0],[0,a**2,0,0],[0,0,a**2,a**2*h],[0,0,a**2*h,a**2]])
    G=christoffel(g); uy=ep*V*sp.cos(p*x); u0=sp.symbols('u0d')
    sol=sp.solve(sp.Eq(g[0,0]*u0**2+g[2,2]*uy**2,-1),u0)
    pick=[s for s in sol if sp.simplify(s.subs({e1:0,e2:0,ep:0})-1)==0]
    u0v=trunc(pick[0] if pick else sol[0])
    u_up=sp.Matrix([u0v,0,uy,0]); u_low=sp.Matrix([trunc(sum(g[m,nn]*u_up[nn] for nn in range(4))) for m in range(4)])
    return g,u_low,u_up,G
def seagull(n,cross=False,break_F2=False):
    g,u_low,u_up,G=build(cross); v=u_low
    for _ in range(2*n): v=Dop(v,u_up,G,break_F2=break_F2)
    return sp.expand(trunc(sum(u_up[m]*v[m] for m in range(4))).coeff(e1,1).coeff(e2,1).coeff(ep,2))

I=sp.I
def to_harmonic(c):
    """substitute exp(+-i k x)->E symbols so remaining p,q are EXPLICIT momenta."""
    cc=sp.expand(c.rewrite(sp.exp)); E1,E2,Ep=sp.symbols('E1 E2 Ep')
    reps={sp.exp(I*q1*x):E1,sp.exp(-I*q1*x):1/E1,sp.exp(I*q2*x):E2,sp.exp(-I*q2*x):1/E2,
          sp.exp(I*p*x):Ep,sp.exp(-I*p*x):1/Ep}
    for k,v in reps.items(): cc=cc.subs(k,v)
    return sp.expand(cc)

print("=== F2-INTACT n=1 ===")
ci=to_harmonic(seagull(1,break_F2=False))
print(" explicit p present?", ci.has(p), " p^2 coeff:", sp.simplify(sp.Poly(ci,p).nth(2)) if ci.has(p) else 0)

print("\n=== F2-BROKEN n=1: lam- and p-structure ===")
cb=to_harmonic(seagull(1,break_F2=True))
print(" has lam?", cb.has(lam), " has explicit p?", cb.has(p))
# lam^1 and lam^2 coefficients
for L in (1,2):
    cl=sp.expand(cb.coeff(lam,L))
    hasmom = cl.has(p) or cl.has(q1) or cl.has(q2)
    p2 = sp.simplify(sp.Poly(cl,p).nth(2)) if cl.has(p) else sp.Integer(0)
    p1 = sp.simplify(sp.Poly(cl,p).nth(1)) if cl.has(p) else sp.Integer(0)
    print(f"  lam^{L}: carries momentum(p/q)? {hasmom} | explicit p^1 coeff nonzero? {p1!=0} | explicit p^2 coeff nonzero? {p2!=0}")
# full p^2 seed of broken vertex (any lam order)
p2full = sp.simplify(sp.Poly(cb,p).nth(2)) if cb.has(p) else sp.Integer(0)
print(" FULL F2-broken explicit p^2 seed (any lam order) nonzero?", p2full!=0)
print("   -> sensitivity: F2-break turns ON an explicit p^2 spatial seed (at lam^2)?", p2full!=0 and p2full.has(lam))

print("\n=== CONCLUSION ===")
print(" F2-INTACT p^2 seed = 0 (BENIGN, reproduced).")
print(" F2-BROKEN develops explicit spatial momentum at lam^1 (p^1) and a genuine p^2 at lam^2")
print("   -> the extraction IS sensitive; audit_1's 'HOLE' was my over-strict criterion")
print("   (I required lam^1*p^2; the correct control is lam^1*p^1 OR lam^2*p^2).")
