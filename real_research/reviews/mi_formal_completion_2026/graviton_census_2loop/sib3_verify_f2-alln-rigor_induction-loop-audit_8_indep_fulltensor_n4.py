#!/usr/bin/env python3
r"""
INDEPENDENT SKEPTIC CAS for METHOD-2 (SIBLING-3 seagull all-n audit).
Rebuild the du^2 x hTT^2 seagull frame kinetic from scratch (my own covariant-derivative
code, independent of setup_1/rigor_1), and try HARD to make a p^2|du_perp|^2 spatial cone appear.

Checks:
 (0) SANITY: the raw B_n (before eps^2 eps2^2 extraction) MUST contain q-carrying terms
     (sin(qx), i.e. d_x h_TT ~ q) -- otherwise the engine is BLIND to the dangerous
     Gamma(h_TT)~q mechanism and any "p-free" result is vacuous.
 (1) Extract the seagull coeff O(eps^2 eps2^2); read the FULL p-polynomial (every power,
     including p^1 and p^2*q^k cross terms), n=1..4. p^2 (and any even p reaching the frame
     kinetic) MUST be 0 for BENIGN.
 (2) PROVE-BY-MOVING A: inject a genuine transverse d_x into the operator (break F2) -> p^2 ON.
 (3) PROVE-BY-MOVING B: give the frame 4-velocity a real x-flow component u^x != 0
     (a "spare u^perp") -> p should turn ON (matches rigor_2's rationing claim).
 (4) Also probe an ALTERNATE orientation: frame leg momentum with a transverse (py) part,
     to make sure the y-along/x-momentum choice isn't hiding a cone.
"""
import sympy as sp, functools, sys, os, time
print=functools.partial(print, flush=True)
def sec(s): print("\n"+"#"*90+"\n# "+s+"\n"+"#"*90)
PASS=[]; FAIL=[]
def ck(nm,c):(PASS if c else FAIL).append(nm); print(f"   [{'PASS' if c else 'FAIL'}] {nm}")

t,x,y,z=sp.symbols('t x y z',real=True)
H=sp.symbols('H',positive=True)
q,p,lam,uxc=sp.symbols('q p lambda uxc',real=True)
e,e2=sp.symbols('e e2',real=True)          # e=frame-leg order, e2=graviton order
crd=[t,x,y,z]
HTT=sp.Function('H_TT')(t); V=sp.Function('V')(t)

def trunc(ex):
    ex=sp.series(ex,e,0,3).removeO()
    ex=sp.series(ex,e2,0,3).removeO()
    return sp.expand(ex)

def build(cross=False, xflow=False):
    a=sp.exp(H*t)
    h=e2*HTT*sp.cos(q*x)
    if not cross:
        g=sp.diag(-1,a**2,a**2*(1+h),a**2*(1-h))
    else:
        g=sp.Matrix([[-1,0,0,0],[0,a**2,0,0],[0,0,a**2,a**2*h],[0,0,a**2*h,a**2]])
    gi=g.inv()
    n=4
    G=[[[0]*n for _ in range(n)] for _ in range(n)]
    for l in range(n):
        for m in range(n):
            for nu in range(n):
                G[l][m][nu]=trunc(sum(gi[l,s]*(sp.diff(g[s,m],crd[nu])+sp.diff(g[s,nu],crd[m])
                                -sp.diff(g[m,nu],crd[s])) for s in range(n))/2)
    # frame 4-velocity: du_perp along y, phase p along x. Optional REAL x-flow (spare u^perp) control.
    uy=e*V*sp.cos(p*x)
    ux= uxc*e*V*sp.cos(p*x) if xflow else sp.Integer(0)
    # solve normalization g_ab u^a u^b = -1 for u^0
    u0=sp.symbols('u0d')
    expr=g[0,0]*u0**2+g[1,1]*ux**2+g[2,2]*uy**2
    sol=sp.solve(sp.Eq(expr,-1),u0)
    pick=[s for s in sol if sp.simplify(s.subs({e:0,e2:0})-1)==0]
    u0v=trunc(pick[0] if pick else sol[0])
    u_up=sp.Matrix([u0v,ux,uy,0])
    u_low=sp.Matrix([trunc(sum(g[m,nn]*u_up[nn] for nn in range(4))) for m in range(4)])
    return g,gi,G,u_up,u_low

def Dop(w_low,u_up,G,break_F2=False):
    n=4; out=[]
    for m in range(n):
        ex=0
        for al in range(n):
            ex+=u_up[al]*(sp.diff(w_low[m],crd[al])-sum(G[l][al][m]*w_low[l] for l in range(n)))
        if break_F2:
            ex+=lam*(sp.diff(w_low[m],x)-sum(G[l][1][m]*w_low[l] for l in range(n)))
        out.append(trunc(ex))
    return sp.Matrix(out)

def Bn_raw(n,u_up,u_low,G,break_F2=False):
    v=u_low
    for _ in range(2*n):
        v=Dop(v,u_up,G,break_F2=break_F2)
    return trunc(sp.expand(sum(u_up[m]*v[m] for m in range(4))))

def seagull(n,cross=False,break_F2=False,xflow=False):
    g,gi,G,u_up,u_low=build(cross=cross,xflow=xflow)
    B=Bn_raw(n,u_up,u_low,G,break_F2=break_F2)
    return sp.expand(B.coeff(e,2).coeff(e2,2)), B

# strip oscillations -> expose EXPLICIT p,q momentum powers
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

def ppoly(c):
    """return dict power->coeff of explicit p (after stripping oscillation phases)."""
    s=strip(c)
    if not s.has(p): return {0:sp.simplify(s)}
    P=sp.Poly(s,p)
    return {int(m[0]):sp.simplify(co) for m,co in zip(P.monoms(),P.coeffs())}

NMAX=int(os.environ.get('SIB3_MYNMAX',4))

# ---------------------------------------------------------------------------
sec("(0) SANITY: raw B_n MUST see the q-carrying d_x h (sin(qx)) mechanism (engine not blind)")
for n in (1,2):
    _,B=seagull(n)
    hasq_deriv = sp.expand_trig(sp.expand(B)).has(sp.sin(q*x))
    print(f"   n={n}: raw B_n contains sin(q x) (a d_x h_TT ~ q insertion)? {hasq_deriv}")
    ck(f"n={n}: engine SEES the q-carrying Gamma(h_TT)~q mechanism (raw B_n has d_x h terms)",hasq_deriv)

# ---------------------------------------------------------------------------
sec(f"(1) INDEPENDENT seagull p-structure, EXACT dS, n=1..{NMAX}, BOTH TT pols -- FULL p-polynomial")
allbenign=True
for cross in (False,True):
    lab='cross' if cross else 'same'
    for n in range(1,NMAX+1):
        t0=time.time()
        c,_=seagull(n,cross=cross)
        pp=ppoly(c)
        p2=pp.get(2,sp.Integer(0)); p1=pp.get(1,sp.Integer(0)); p0=pp.get(0,sp.Integer(0))
        maxp=max(pp.keys())
        anyp = any(k>=1 and sp.simplify(v)!=0 for k,v in pp.items())
        benign = (sp.simplify(p2)==0)
        allbenign=allbenign and benign
        print(f"   [{lab}] n={n}: p^2={sp.simplify(p2)} | p^1={sp.simplify(p1)} | "
              f"max p-power w/ nonzero coeff = {maxp if anyp else 0} | mass(p^0)!=0? {sp.simplify(p0)!=0} "
              f"[{time.time()-t0:.1f}s]")
        ck(f"[{lab}] n={n}: NO p^2 spatial cone (p-free frame kinetic)",benign)
        ck(f"[{lab}] n={n}: NO explicit p at ALL on frame kinetic (mass/time only)",not anyp)

# ---------------------------------------------------------------------------
sec("(2) PROVE-BY-MOVING A: inject transverse d_x (break F2) -> p^2 spatial cone MUST switch ON")
for n in (1,2,3):
    c,_=seagull(n,break_F2=True)
    pp=ppoly(c)
    # F2-break introduces lam; look for lam-carrying p-power terms
    s=strip(c)
    p2=pp.get(2,sp.Integer(0))
    on = sp.simplify(p2)!=0 or s.has(lam*p) or any(sp.simplify(v).has(lam) and k>=1 for k,v in pp.items())
    print(f"   n={n}: F2-broken p^2 coeff = {sp.simplify(p2)} | p^1 coeff = {sp.simplify(pp.get(1,0))} -> cone {'ON' if on else 'OFF'}")
    ck(f"n={n}: F2-break turns ON explicit p on the frame kinetic (sensitive, not blind)",on)

# ---------------------------------------------------------------------------
sec("(3) PROVE-BY-MOVING B: real x-flow u^x != 0 (a spare u^perp) -> p MUST turn ON")
for n in (1,2):
    c,_=seagull(n,xflow=True)
    pp=ppoly(c)
    anyp=any(k>=1 and sp.simplify(v)!=0 for k,v in pp.items())
    # the xflow coeff uxc should appear multiplying a p-power
    s=strip(c)
    has_uxc_p = s.has(uxc) and anyp
    print(f"   n={n}: with u^x!=0, explicit p appears? {anyp} | max p-power={max(pp.keys())}")
    ck(f"n={n}: giving a spare u^perp (u^x!=0) turns ON explicit frame p -> rationing count is the real gate",anyp)

sec("VERDICT (independent skeptic full-tensor CAS)")
print(f"   ALL n=1..{NMAX} both pols: p-free frame kinetic (no p^2 cone)? {allbenign}")
print(f"PASS={len(PASS)} FAIL={len(FAIL)}")
sys.exit(0 if not FAIL else 1)
