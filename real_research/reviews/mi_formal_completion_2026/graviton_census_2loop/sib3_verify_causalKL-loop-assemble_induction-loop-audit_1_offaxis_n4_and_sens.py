#!/usr/bin/env python3
r"""
SKEPTIC audit: push the OFF-AXIS full-vector (connection ON) seagull CAS to n=4, and REPAIR the
n=1 F2-break sensitivity control so the p-free verdict is genuinely earned, not blind.

Two concerns from the banked off-axis hunt:
  (A) It only reached n=3. The all-n claim rests on a scalar recursion that DROPS the connection --
      the very object that could inject q. So the FULL-VECTOR (connection ON) check must go higher.
  (B) The F2-break prove-by-moving at n=1 off-axis showed p did NOT switch on. If the extraction is
      blind at n=1, the n=1 "p-free" is not a real datum. I test the F2-break more carefully: inject a
      transverse d ALONG THE FRAME PROPAGATION AXIS x so it MUST hit the frame phase e^{ipx}.

If p^2 stays 0 through n=4 off-axis with the connection ON AND the F2-break reliably turns p on,
the p-free-to-all-n claim is corroborated one order deeper by the genuine (connection-ON) operator.
"""
import sympy as sp, sys, functools, time, os
print=functools.partial(print, flush=True)
def sec(s): print("\n"+"="*96+"\n "+s+"\n"+"="*96)
PASS=[]; FAIL=[]
def ck(nm,c):(PASS if c else FAIL).append(nm); print(f"   [{'PASS' if c else 'FAIL'}] {nm}")

t,x,y,z=sp.symbols('t x y z', real=True)
H=sp.symbols('H', positive=True)
q,p=sp.symbols('q p', real=True)
eps,eps2=sp.symbols('epsilon epsilon2', real=True)
lam=sp.symbols('lambda', real=True)
I=sp.I
crd=[t,x,y,z]; a=sp.exp(H*t)
HTT=sp.Function('H_TT')(t); V=sp.Function('V')(t)

MAXE=2; MAXE2=2
def trunc(e):
    e=sp.series(e,eps,0,MAXE+1).removeO()
    e=sp.series(e,eps2,0,MAXE2+1).removeO()
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

def Dop(w_low,u_up,G,break_dir=None):
    """break_dir: None (F2 intact) or an axis index 1,2,3 to inject lam*d_(axis) (breaks F2)."""
    n=4; out=[]
    for m in range(n):
        e=0
        for al in range(n):
            e+=u_up[al]*(sp.diff(w_low[m],crd[al]) - sum(G[l][al][m]*w_low[l] for l in range(n)))
        if break_dir is not None:
            e+= lam*(sp.diff(w_low[m],crd[break_dir]) - sum(G[l][break_dir][m]*w_low[l] for l in range(n)))
        out.append(trunc(e))
    return sp.Matrix(out)

def build_geom():
    """Off-axis: graviton h_xy propagating along z (d_z~q); frame du_perp along y prop along x (d_x~p)."""
    h = eps2*HTT*sp.exp(I*q*z)
    g=sp.Matrix([[-1,0,0,0],
                 [0,a**2, a**2*h,0],
                 [0,a**2*h, a**2,0],
                 [0,0,0,a**2]])
    uy_up=eps*V*sp.exp(I*p*x)
    G=christoffel(g)
    g00=g[0,0]; gyy=g[2,2]
    u0=sp.symbols('u0d')
    sol=sp.solve(sp.Eq(g00*u0**2+gyy*uy_up**2,-1),u0)
    pick=[s for s in sol if sp.simplify(s.subs({eps:0,eps2:0})-1)==0]
    u0v=trunc(pick[0] if pick else sol[0])
    u_up=sp.Matrix([u0v,0,uy_up,0])
    u_low=sp.Matrix([trunc(sum(g[m,nn]*u_up[nn] for nn in range(4))) for m in range(4)])
    return g,u_low,u_up,G

def Bn(n,u_low,u_up,G,break_dir=None):
    v=u_low
    for _ in range(2*n):
        v=Dop(v,u_up,G,break_dir=break_dir)
    return trunc(sp.expand(sum(u_up[m]*v[m] for m in range(4))))

def seagull(n,break_dir=None):
    g,u_low,u_up,G=build_geom()
    B=Bn(n,u_low,u_up,G,break_dir=break_dir)
    return sp.expand(B.coeff(eps,2).coeff(eps2,2))

def strip_phase_ppow(c, order=2):
    c=sp.expand(c)
    ph=[a_ for a_ in c.atoms(sp.exp) if a_.has(x) or a_.has(z)]
    c2=c.subs({e:sp.Symbol(f'PH{i}') for i,e in enumerate(ph)})
    if not c2.has(p): return sp.Integer(0), False
    return sp.simplify(sp.Poly(c2,p).nth(order)), True

# ---- (A) push off-axis (connection ON) to n=4 ----
NMAX=int(os.environ.get('SIB3_AUDIT_NMAX',4))
sec(f"(A) OFF-AXIS full-vector (connection ON) seagull p^2 coeff, n=1..{NMAX} (past banked n=3)")
res={}
for n in range(1,NMAX+1):
    t0=time.time()
    c=seagull(n)
    p2,hasp=strip_phase_ppow(c,2)
    res[n]=(p2,hasp)
    print(f"   n={n}: p^2 coeff = {p2} | explicit p at all? {hasp} | [{time.time()-t0:.1f}s]")
    ck(f"n={n} off-axis connection-ON: p^2 spatial cone seed = 0 (p-free)", sp.simplify(p2)==0)

# ---- (B) repair the sensitivity control: break along x (frame prop axis) so it MUST hit e^{ipx} ----
sec("(B) SENSITIVITY (prove-by-moving): inject lam*d_x (along frame prop axis) -> p MUST turn ON")
for n in (1,2,3):
    c=seagull(n, break_dir=1)   # break_dir=1 is x-axis (frame propagation)
    lc=sp.expand(c).coeff(lam,1)
    _,hasp=strip_phase_ppow(lc+sp.Symbol('DUMMY')*0,1) if lc!=0 else (0,False)
    # simpler: does the lam-linear piece carry explicit p after phase strip?
    ph=[a_ for a_ in lc.atoms(sp.exp) if a_.has(x) or a_.has(z)]
    lc2=lc.subs({e:sp.Symbol(f'PH{i}') for i,e in enumerate(ph)})
    on = bool(lc2.has(p))
    print(f"   n={n}: F2-break along x, lam-piece carries explicit frame p? {on}")
    ck(f"n={n}: F2-break along x switches p ON -> extraction sensitive", on)

sec("SKEPTIC AUDIT VERDICT")
allsafe=all(sp.simplify(res[n][0])==0 for n in res)
print(f"   off-axis connection-ON p^2 = 0 through n={NMAX}? {allsafe}")
print(f"\nPASS={len(PASS)} FAIL={len(FAIL)}")
sys.exit(0 if not FAIL else 1)
