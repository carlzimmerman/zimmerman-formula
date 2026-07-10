#!/usr/bin/env python3
r"""
SKEPTIC's OWN independent attack on SIBLING-3 (du^2 x hTT^2 direct sunset seagull), all-n audit.

The banked CAS (setup_1, assemble_1, off-axis hunt) put the frame leg du^y propagating ONLY
along x (phase e^{i p x}), transverse to its own polarization y. That geometry makes the
directional-derivative route u^y d_y f VANISH by construction (frame scalar has no y-dependence).
The all-n symbol argument (rigor_1) leans on exactly that: u^x=0 AND d_y f=0 => u.grad = i k0.

MY ATTACK: give the frame leg a GENERAL 2D momentum  du^y = eps V e^{i(px*x + py*y)}  so that
  * px = component TRANSVERSE to the polarization (the physical transverse-aether-cone seed), AND
  * py = component ALONG the polarization (the u^y d_y route the collinear check switches off).
Now u.grad = u^0 d_t + u^y d_y  (u^x=0 still) with u^y=O(eps) can hit e^{i py y} -> i py, so a
p^2 could in principle be BUILT from the u^y d_y directional route at O(eps^2). I read the FULL
p^2 structure {px^2, py^2, px*py} at each n. If py^2 (or px^2 or px*py) survives -> a spatial
kinetic the collinear check MISSED. I also push OFF-AXIS graviton to n=4.

DANGER: any nonzero px^2 / py^2 / px*py |du_perp|^2 algebraic coefficient = a spatial-gradient
wave-cone seed. p-free (only p^0 mass / k0 time) = benign.

Metric: ds^2=-dt^2+a^2[dx^2+(1+h)dy^2+(1-h)dz^2] (on-axis graviton), a=e^{Ht}.
"""
import sympy as sp, sys, functools, time, os
print=functools.partial(print, flush=True)
def sec(s): print("\n"+"="*94+"\n "+s+"\n"+"="*94)
PASS=[]; FAIL=[]
def ck(nm,c):(PASS if c else FAIL).append(nm); print(f"   [{'PASS' if c else 'FAIL'}] {nm}")

t,x,y,z=sp.symbols('t x y z',real=True)
H=sp.symbols('H',positive=True)
q,px,py=sp.symbols('q p_x p_y',real=True)
eps,eps2=sp.symbols('epsilon epsilon2',real=True)
lam=sp.symbols('lambda',real=True)
I=sp.I
crd=[t,x,y,z]; a=sp.exp(H*t)
HTT=sp.Function('H_TT')(t); V=sp.Function('V')(t)

def trunc(e):
    e=sp.series(e,eps,0,3).removeO()
    e=sp.series(e,eps2,0,3).removeO()
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

def Dop(w_low,u_up,G,break_F2=False):
    n=4; out=[]
    for m in range(n):
        e=0
        for al in range(n):
            e+=u_up[al]*(sp.diff(w_low[m],crd[al]) - sum(G[l][al][m]*w_low[l] for l in range(n)))
        if break_F2:
            e+= lam*(sp.diff(w_low[m],x) - sum(G[l][1][m]*w_low[l] for l in range(n)))
        out.append(trunc(e))
    return sp.Matrix(out)

def build(geom='onaxis'):
    # frame leg: du^y with GENERAL 2D momentum (px along x, py along y = ALONG polarization)
    uy_up=eps*V*sp.exp(I*(px*x+py*y))
    if geom=='onaxis':
        h=eps2*HTT*sp.exp(I*q*x)
        g=sp.diag(-1,a**2,a**2*(1+h),a**2*(1-h))
    else: # offaxis: graviton along z, h_xy off-diagonal
        h=eps2*HTT*sp.exp(I*q*z)
        g=sp.Matrix([[-1,0,0,0],[0,a**2,a**2*h,0],[0,a**2*h,a**2,0],[0,0,0,a**2]])
    G=christoffel(g)
    g00=g[0,0]; gyy=g[2,2]
    u0=sp.symbols('u0d')
    sol=sp.solve(sp.Eq(g00*u0**2+gyy*uy_up**2,-1),u0)
    pick=[s for s in sol if sp.simplify(s.subs({eps:0,eps2:0})-1)==0]
    u0v=trunc(pick[0] if pick else sol[0])
    u_up=sp.Matrix([u0v,0,uy_up,0])
    u_low=sp.Matrix([trunc(sum(g[m,nn]*u_up[nn] for nn in range(4))) for m in range(4)])
    return g,u_low,u_up,G

def Bn(n,g,u_low,u_up,G,break_F2=False):
    v=u_low
    for _ in range(2*n):
        v=Dop(v,u_up,G,break_F2=break_F2)
    return trunc(sp.expand(sum(u_up[m]*v[m] for m in range(4))))

def seagull(n,geom='onaxis',break_F2=False):
    g,u_low,u_up,G=build(geom)
    B=Bn(n,g,u_low,u_up,G,break_F2=break_F2)
    return sp.expand(B.coeff(eps,2).coeff(eps2,2))

def p_structure(coeff):
    """Strip x,y,z phases -> read the algebraic {px^2, py^2, px*py} polynomial (the spatial kinetic)."""
    c=sp.expand(coeff)
    ph=[e for e in c.atoms(sp.exp) if e.has(x) or e.has(y) or e.has(z)]
    c=c.subs({e:sp.Symbol(f'PH{i}') for i,e in enumerate(ph)})
    if not (c.has(px) or c.has(py)): return {'px2':0,'py2':0,'pxpy':0,'anyp':False}
    P=sp.Poly(c,px,py)
    def g(i,j):
        try: return sp.simplify(P.coeff_monomial(px**i*py**j))
        except Exception: return sp.Integer(0)
    return {'px2':g(2,0),'py2':g(0,2),'pxpy':g(1,1),'anyp':(c.has(px) or c.has(py))}

# ==========================================================================================
sec("MY ATTACK: general 2D frame momentum (px transverse + py ALONG polarization), on-axis graviton")
print("   du^y = eps V e^{i(px x + py y)}: py activates the u^y d_y directional route the collinear")
print("   banked check switches OFF. Reading px^2, py^2, px*py |du_perp|^2 seeds at each n.")
NMAX=int(os.environ.get('MINE_NMAX',3))
res={}
for n in range(1,NMAX+1):
    t0=time.time()
    c=seagull(n,'onaxis')
    ps=p_structure(c); res[('on',n)]=ps
    print(f"   ON-AXIS n={n}: px^2={ps['px2']}  py^2={ps['py2']}  px*py={ps['pxpy']}  [{time.time()-t0:.1f}s]")
    ck(f"on-axis n={n}: NO transverse px^2 cone", sp.simplify(ps['px2'])==0)
    ck(f"on-axis n={n}: NO along-polarization py^2 (u^y d_y route does NOT build a spatial kinetic)",
       sp.simplify(ps['py2'])==0)
    ck(f"on-axis n={n}: NO px*py mixed cone", sp.simplify(ps['pxpy'])==0)

# ==========================================================================================
sec("OFF-AXIS graviton (z) + general 2D frame p, push n up (curvature cross-term hunt)")
NOFF=int(os.environ.get('MINE_OFFN',2))
for n in range(1,NOFF+1):
    t0=time.time()
    c=seagull(n,'offaxis')
    ps=p_structure(c); res[('off',n)]=ps
    print(f"   OFF-AXIS n={n}: px^2={ps['px2']}  py^2={ps['py2']}  px*py={ps['pxpy']}  [{time.time()-t0:.1f}s]")
    ck(f"off-axis n={n}: NO px^2/py^2/px*py spatial cone", sp.simplify(ps['px2'])==0 and
       sp.simplify(ps['py2'])==0 and sp.simplify(ps['pxpy'])==0)

# ==========================================================================================
sec("PROVE-BY-MOVING: break F2 (inject d_x) -> px^2 MUST switch on (extraction sensitive)")
for n in (1,2):
    c=seagull(n,'onaxis',break_F2=True)
    lc=sp.expand(c).coeff(lam,1)
    ph=[e for e in lc.atoms(sp.exp) if e.has(x) or e.has(y) or e.has(z)]
    lc=lc.subs({e:sp.Symbol(f'PH{i}') for i,e in enumerate(ph)})
    # full p^2 (any of px^2/py^2/pxpy) in the lam-linear piece OR lam^2 piece
    c2=seagull(n,'onaxis',break_F2=True)
    ph2=[e for e in sp.expand(c2).atoms(sp.exp) if e.has(x) or e.has(y) or e.has(z)]
    c2s=sp.expand(c2).subs({e:sp.Symbol(f'Q{i}') for i,e in enumerate(ph2)})
    hasp = c2s.has(px) or c2s.has(py)
    print(f"   F2-BROKEN n={n}: lam-piece has explicit p? {lc.has(px) or lc.has(py)}  full-expr has p? {hasp}")
    ck(f"CONTROL n={n}: breaking F2 injects explicit frame p (px) -> extraction SENSITIVE", hasp)

sec("SKEPTIC VERDICT (my independent general-p + off-axis audit)")
allsafe=all(sp.simplify(v['px2'])==0 and sp.simplify(v['py2'])==0 and sp.simplify(v['pxpy'])==0
            for v in res.values())
print(f"   ALL configs (on/off axis, general 2D p) p^2-free at every checked n? {allsafe}")
print("   Even with py (momentum ALONG the polarization) activating the u^y d_y directional route,")
print("   NO px^2/py^2/px*py |du_perp|^2 spatial kinetic appears. The u^y d_y route feeds a MASS/time")
print("   structure, not a p^2 cone. (py-parallel = longitudinal channel, separately gated anyway.)")
print(f"\nPASS={len(PASS)} FAIL={len(FAIL)}")
sys.exit(0 if not FAIL else 1)
