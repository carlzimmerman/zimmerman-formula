#!/usr/bin/env python3
r"""
SKEPTIC probe 1: the banked SIBLING-3 scripts put the FRAME spatial momentum p ALONG x,
while du_perp points along y with u^x=0.  Because u.grad = u^0 d_t + u^y d_y has NO d_x,
the frame leg's cos(p x) is never differentiated -> p_explicit=False is nearly AUTOMATIC
in that ansatz, independent of any real F2 protection.  That could HIDE a p^2 cone that
only shows up when the frame carries momentum ALONG its own polarization (y), where
u^y d_y CAN act on it.

THIS SCRIPT: frame perturbation carries momentum kappa ALONG y (u^y = ep V(t) cos(kappa y)),
graviton along x (h = A(t) cos(q x)).  Now u^y d_y is genuinely nonzero and can pull down
kappa = p_y.  We extract the ep^2 (two-frame-leg) seagull coefficient of B_n = u.(D^{2n}u)
at n=1,2,3 and ask: does an EXPLICIT kappa^2 (=p_y^2) SPATIAL-gradient factor appear on the
|du_perp|^2 structure?  If yes -> a wave cone the banked p-along-x ansatz MISSED -> FATAL.
If it stays zero -> the p-free result is physics (transverse-gradient rationing), not artifact.

Also probes the du^2 x hTT^2 seagull piece (coeff of A, the graviton) inside this kappa!=0 setup.
"""
import sympy as sp, functools
print=functools.partial(print, flush=True)
def sec(t): print("\n"+"="*90+"\n "+t+"\n"+"="*90)

t,x,y,z=sp.symbols('t x y z',real=True)
H=sp.symbols('H',positive=True)
q,kap=sp.symbols('q kappa',real=True)      # graviton mom q (along x), frame mom kappa (along y)
ep,e2=sp.symbols('ep e2',real=True)        # ep = frame-leg counter, e2 = graviton counter
crd=[t,x,y,z]
A=sp.Function('A')(t); V=sp.Function('V')(t)

MAXep=2; MAXe2=2
def trunc(e):
    e=sp.series(e,ep,0,MAXep+1).removeO()
    e=sp.series(e,e2,0,MAXe2+1).removeO()
    return sp.expand(e)

def christoffel(g):
    n=4; gi=g.inv()
    G=[[[0]*n for _ in range(n)] for _ in range(n)]
    for l in range(n):
        for m in range(n):
            for nu in range(n):
                G[l][m][nu]=trunc(sum(gi[l,s]*(sp.diff(g[s,m],crd[nu])+sp.diff(g[s,nu],crd[m])
                                -sp.diff(g[m,nu],crd[s])) for s in range(n))/2)
    return G

def Dop(w_low,u_up,G):
    n=4; out=[]
    for m in range(n):
        e=0
        for al in range(n):
            e+=u_up[al]*(sp.diff(w_low[m],crd[al]) - sum(G[l][al][m]*w_low[l] for l in range(n)))
        out.append(trunc(e))
    return sp.Matrix(out)

def build():
    a=sp.exp(H*t)
    h=e2*A*sp.cos(q*x)                       # graviton yy/zz, propagates along x
    g=sp.diag(-1, a**2, a**2*(1+h), a**2*(1-h))
    G=christoffel(g)
    uy=ep*V*sp.cos(kap*y)                     # FRAME MOMENTUM ALONG y (the missed direction!)
    g00=g[0,0]; gyy=g[2,2]
    u0=sp.symbols('u0d')
    sol=sp.solve(sp.Eq(g00*u0**2+gyy*uy**2,-1),u0)
    pick=[s for s in sol if sp.simplify(s.subs({ep:0,e2:0})-1)==0]
    u0v=trunc(pick[0] if pick else sol[0])
    u_up=sp.Matrix([u0v,0,uy,0])
    u_low=sp.Matrix([trunc(sum(g[m,nn]*u_up[nn] for nn in range(4))) for m in range(4)])
    return g,u_low,u_up,G

def Bn(n,g,u_low,u_up,G):
    v=u_low
    for _ in range(2*n): v=Dop(v,u_up,G)
    return trunc(sp.expand(sum(u_up[m]*v[m] for m in range(4))))

Cy,Sy,Cq,Sq=sp.symbols('Cy Sy Cq Sq',real=True)
def strip(c):
    c=sp.expand_trig(sp.expand(c))
    sub={sp.cos(kap*y):Cy,sp.sin(kap*y):Sy,sp.cos(q*x):Cq,sp.sin(q*x):Sq,
         sp.cos(2*kap*y):Cy*Cy-Sy*Sy,sp.sin(2*kap*y):2*Sy*Cy,
         sp.cos(2*q*x):Cq*Cq-Sq*Sq,sp.sin(2*q*x):2*Sq*Cq}
    for k,v in sub.items(): c=c.subs(k,v)
    return sp.expand(c)

sec("FRAME MOMENTUM ALONG y (kappa) -- the direction the banked p-along-x ansatz could NOT probe")
print("  u^y = ep V(t) cos(kappa y);  graviton h = e2 A(t) cos(q x).  u.grad = u^0 d_t + u^y d_y")
print("  Now u^y d_y CAN differentiate the frame leg -> kappa (=p_y) can appear explicitly if a")
print("  spatial kinetic exists. Reading ep^2 coeff of B_n; looking for kappa^2 SPATIAL seed.\n")

for n in (1,2,3):
    g,u_low,u_up,G=build()
    B=Bn(n,g,u_low,u_up,G)
    # FULL ep^2 coeff (du_perp two-point), BOTH graviton orders (mass term e2^0 AND seagull e2^2)
    c_full=sp.expand(B.coeff(ep,2))
    s=strip(c_full)
    kap_expl=s.has(kap)
    if s.has(kap):
        pol=sp.Poly(s,kap); k2=sp.simplify(pol.nth(2)); k0=sp.simplify(pol.nth(0))
    else:
        k2=sp.Integer(0); k0=sp.simplify(s)
    # isolate the SEAGULL piece: e2^2 (two graviton legs)
    c_seag=sp.expand(c_full.coeff(e2,2))
    ss=strip(c_seag)
    if ss.has(kap): k2_seag=sp.simplify(sp.Poly(ss,kap).nth(2))
    else: k2_seag=sp.Integer(0)
    print(f"  n={n}: FULL ep^2 coeff -> kappa explicit? {kap_expl} | kappa^2 SPATIAL seed = {k2}")
    print(f"        SEAGULL (e2^2) piece    -> kappa^2 spatial seed = {k2_seag}")
    print(f"        (mass/time p^0 piece nonzero? {k0!=0})")

sec("INTERPRETATION")
print("  If kappa^2 seed = 0 even with frame momentum ALONG y (u^y d_y active), the p-free result")
print("  is NOT an artifact of the p-perp-x ansatz -- it is the transverse-gradient RATIONING:")
print("  each spatial d_y costs a u^y = O(ep) frame leg, so two d_y (needed for kappa^2) exhaust")
print("  ep beyond the two-point ep^2 order. If kappa^2 != 0 -> a genuine cone the banked missed.")
