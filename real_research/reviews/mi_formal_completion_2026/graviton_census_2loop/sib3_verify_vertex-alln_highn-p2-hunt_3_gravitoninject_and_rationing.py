#!/usr/bin/env python3
r"""
SKEPTIC probe 3:
(A) DIRECT graviton-connection-injection test (the lens's exact worry): let the graviton
    depend on y (h ~ cos(qy y)) so u^y d_y differentiates it and Gamma(h_TT) can deposit q_y.
    Does the graviton momentum q_y land on the ep^2 frame KINETIC as a spatial p^2?  (In the
    real loop the graviton is integrated, so this is a fortiori test: even treating q as a live
    external spatial momentum on the frame, does it build a cone?)
(B) RATIONING quantifier: raise the ep truncation to ep^4 and find at WHICH ep order the spatial
    momentum kappa FIRST appears.  The claim: each spatial d_y costs one u^y=O(ep), so kappa^2
    (two d_y) needs ep^2 FROM THE DERIVATIVES on top of the two external frame legs -> first at
    ep^4, NOT the two-point ep^2.  This makes the "p-free at the two-point" a hard power-counting
    fact, n-independent.
"""
import sympy as sp, functools
print=functools.partial(print, flush=True)
def sec(t): print("\n"+"="*90+"\n "+t+"\n"+"="*90)

t,x,y,z=sp.symbols('t x y z',real=True)
H=sp.symbols('H',positive=True)
qy,kap=sp.symbols('q_y kappa',real=True)
ep,e2=sp.symbols('ep e2',real=True)
crd=[t,x,y,z]
A=sp.Function('A')(t); V=sp.Function('V')(t)

def mk(MAXep):
    def trunc(e):
        e=sp.series(e,ep,0,MAXep+1).removeO(); e=sp.series(e,e2,0,3).removeO()
        return sp.expand(e)
    return trunc

def christoffel(g,trunc):
    n=4; gi=g.inv(); G=[[[0]*n for _ in range(n)] for _ in range(n)]
    for l in range(n):
        for m in range(n):
            for nu in range(n):
                G[l][m][nu]=trunc(sum(gi[l,s]*(sp.diff(g[s,m],crd[nu])+sp.diff(g[s,nu],crd[m])
                                -sp.diff(g[m,nu],crd[s])) for s in range(n))/2)
    return G
def Dop(w_low,u_up,G,trunc):
    n=4; out=[]
    for m in range(n):
        e=0
        for al in range(n):
            e+=u_up[al]*(sp.diff(w_low[m],crd[al]) - sum(G[l][al][m]*w_low[l] for l in range(n)))
        out.append(trunc(e))
    return sp.Matrix(out)
def Bn(n,g,u_low,u_up,G,trunc):
    v=u_low
    for _ in range(2*n): v=Dop(v,u_up,G,trunc)
    return trunc(sp.expand(sum(u_up[m]*v[m] for m in range(4))))

# ---- (A) graviton with y-momentum: can Gamma(h) inject q_y onto the frame? ----
sec("(A) GRAVITON depends on y (h~cos(q_y y)) -> u^y d_y hits it; does q_y reach frame p^2?")
trunc=mk(2)
a=sp.exp(H*t)
h=e2*A*sp.cos(qy*y)                              # graviton now carries y-momentum
g=sp.diag(-1, a**2*(1+h), a**2, a**2*(1-h))      # polarization xx/zz (transverse to y-propagation)
G=christoffel(g,trunc)
uy=ep*V*sp.cos(kap*y)                             # frame also along y with momentum kappa
g00=g[0,0]; gyy=g[2,2]; u0=sp.symbols('u0d')
sol=sp.solve(sp.Eq(g00*u0**2+gyy*uy**2,-1),u0)
pick=[s for s in sol if sp.simplify(s.subs({ep:0,e2:0})-1)==0]
u0v=trunc(pick[0] if pick else sol[0])
u_up=sp.Matrix([u0v,0,uy,0]); u_low=sp.Matrix([trunc(sum(g[m,nn]*u_up[nn] for nn in range(4))) for m in range(4)])
Cy,Sy,Cqy,Sqy=sp.symbols('Cy Sy Cqy Sqy',real=True)
def strip(c):
    c=sp.expand_trig(sp.expand(c))
    sub={sp.cos(kap*y):Cy,sp.sin(kap*y):Sy,sp.cos(qy*y):Cqy,sp.sin(qy*y):Sqy,
         sp.cos(2*kap*y):Cy*Cy-Sy*Sy,sp.sin(2*kap*y):2*Sy*Cy,
         sp.cos(2*qy*y):Cqy*Cqy-Sqy*Sqy,sp.sin(2*qy*y):2*Sqy*Cqy,
         sp.cos((kap+qy)*y):Cy*Cqy-Sy*Sqy,sp.cos((kap-qy)*y):Cy*Cqy+Sy*Sqy,
         sp.sin((kap+qy)*y):Sy*Cqy+Cy*Sqy,sp.sin((kap-qy)*y):Sy*Cqy-Cy*Sqy}
    for k,v in sub.items(): c=c.subs(k,v)
    return sp.expand(c)
for n in (1,2,3):
    B=Bn(n,g,u_low,u_up,G,trunc)
    c=sp.expand(B.coeff(ep,2).coeff(e2,2))   # SEAGULL: two graviton legs, two frame legs
    s=strip(c)
    # any spatial p^2 seed on the frame: coeff of kappa^2, OR q_y landing as a squared spatial deriv
    kap2 = sp.simplify(sp.Poly(s,kap).nth(2)) if s.has(kap) else sp.Integer(0)
    # graviton-injected cross: kappa^1 * q_y^1 (a spatial-gradient cross kinetic) or q_y^2
    qy2  = sp.simplify(sp.Poly(s,qy).nth(2)) if s.has(qy) else sp.Integer(0)
    print(f"  n={n}: SEAGULL frame kappa^2 seed={kap2} | q_y^2 seed={qy2} | q_y explicit at all? {s.has(qy)}")

# ---- (B) rationing: at which ep order does kappa first appear? ----
sec("(B) RATIONING: raise truncation to ep^4; find the FIRST ep order carrying spatial kappa")
trunc4=mk(4)
a=sp.exp(H*t)
hx=e2*A*sp.cos(sp.Symbol('qx',real=True)*x)   # graviton back along x (irrelevant here; keep simple)
g4=sp.diag(-1, a**2, a**2*(1+hx), a**2*(1-hx))
G4=christoffel(g4,trunc4)
uy4=ep*V*sp.cos(kap*y)
u0=sp.symbols('u0e'); g00=g4[0,0]; gyy=g4[2,2]
sol=sp.solve(sp.Eq(g00*u0**2+gyy*uy4**2,-1),u0)
pick=[s for s in sol if sp.simplify(s.subs({ep:0,e2:0})-1)==0]
u0v=trunc4(pick[0] if pick else sol[0])
u_up4=sp.Matrix([u0v,0,uy4,0]); u_low4=sp.Matrix([trunc4(sum(g4[m,nn]*u_up4[nn] for nn in range(4))) for m in range(4)])
def strip_k(c):
    c=sp.expand_trig(sp.expand(c))
    sub={sp.cos(kap*y):Cy,sp.sin(kap*y):Sy,sp.cos(2*kap*y):Cy*Cy-Sy*Sy,sp.sin(2*kap*y):2*Sy*Cy,
         sp.cos(3*kap*y):Cy*(Cy*Cy-3*Sy*Sy),sp.cos(4*kap*y):(Cy*Cy-Sy*Sy)**2-(2*Sy*Cy)**2,
         sp.sin(3*kap*y):Sy*(3*Cy*Cy-Sy*Sy),sp.sin(4*kap*y):2*(2*Sy*Cy)*(Cy*Cy-Sy*Sy)}
    for k,v in sub.items(): c=c.subs(k,v)
    return sp.expand(c)
n=2
B=Bn(n,g4,u_low4,u_up4,G4,trunc4)
Bs=strip_k(sp.expand(B))
print(f"  n={n}, graviton set to 0 (e2->0) to isolate pure-frame rationing of kappa vs ep order:")
Bs0=sp.expand(Bs.subs(e2,0))
for ne in (2,3,4):
    ce=sp.expand(Bs0.coeff(ep,ne))
    k2=sp.simplify(sp.Poly(ce,kap).nth(2)) if ce.has(kap) else sp.Integer(0)
    print(f"    ep^{ne}: carries explicit kappa? {ce.has(kap)} | kappa^2 spatial seed nonzero? {k2!=0}")
print("  EXPECT: kappa (spatial) FIRST appears at ep^4 (two d_y each cost a u^y=O(ep)), NOT ep^2.")
print("  -> the two-point (ep^2) du_perp kinetic is p-free by hard power counting, for EVERY n.")
sec("DONE")
