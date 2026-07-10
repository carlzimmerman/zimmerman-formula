#!/usr/bin/env python3
r"""
sib3_verify_vertex-alln_highn-p2-hunt_1_independent_CAS.py
=========================================================
SKEPTIC / INDEPENDENT re-derivation. HUNT for a p^2|du_perp|^2 SPATIAL cone at high n in the
direct du^2 x hTT^2 sunset seagull (SIBLING-3). I do NOT trust the banked lane's scalar-surrogate
induction; I recompute the seagull vertex from scratch with a DIFFERENT, more paranoid extractor
that keeps the frame momentum p AND both graviton momenta q1,q2 as EXPLICIT plane-wave phases so
that any d_x hitting a frame leg (via the h_TT-dressed Christoffel Gamma(h_TT)) surfaces as an
explicit p (or p*q) power.

KEY DIFFERENCE from the banked script: I use COMPLEX exponential phases e^{i p x}, e^{i q1 x},
e^{i q2 x} (not cos), so momentum flows are linear and NOTHING cancels by trig identity accidentally.
The seagull coefficient is O(e1^1 e2^1 ep^2). After building B_n = u.(D^{2n} u), I extract that order
and read, from the surviving x-phase e^{i(m1 q1 + m2 q2 + mp p) x}, whether the ATTACHED polynomial
prefactor carries p^2 (or the full symbol carries a genuine spatial-gradient p^2 on the frame legs).

DANGER: p^2 factor = spatial wave-cone kinetic on the frame -> FATAL.
BENIGN: only p^0 (mass) or k0/time -> no cone.

I push CAS to n=1..4 (2n up to 8 covariant derivatives) with the FULL tensor B_n, and add an
F2-break control. If p-free survives n=4 independently, I corroborate the banked induction.
"""
import sympy as sp, sys, os, functools, time
print=functools.partial(print, flush=True)
def sec(s): print("\n"+"="*94+"\n "+s+"\n"+"="*94)
PASS=[]; FAIL=[]
def ck(nm,c):(PASS if c else FAIL).append(nm); print(f"   [{'PASS' if c else 'FAIL'}] {nm}")

t,x,y,z=sp.symbols('t x y z', real=True)
H=sp.symbols('H', positive=True)
q1,q2,p=sp.symbols('q1 q2 p', real=True)
e1,e2,ep=sp.symbols('e1 e2 ep', real=True)   # order counters
lam=sp.symbols('lambda', real=True)          # F2-break
I=sp.I
crd=[t,x,y,z]
A1=sp.Function('A1')(t); A2=sp.Function('A2')(t); V=sp.Function('V')(t)

ORD={'e1':1,'e2':1,'ep':2}
def trunc(expr):
    expr=sp.series(expr,e1,0,ORD['e1']+1).removeO()
    expr=sp.series(expr,e2,0,ORD['e2']+1).removeO()
    expr=sp.series(expr,ep,0,ORD['ep']+1).removeO()
    return sp.expand(expr)

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

def build(cross=False):
    a=sp.exp(H*t)
    # COMPLEX phases: expose momentum flow linearly. h_TT = A1 e^{i q1 x} + A2 e^{i q2 x}
    if not cross:
        h = e1*A1*sp.exp(I*q1*x) + e2*A2*sp.exp(I*q2*x)
        g=sp.diag(-1, a**2, a**2*(1+h), a**2*(1-h))
    else:
        hc= e1*A1*sp.exp(I*q1*x) + e2*A2*sp.exp(I*q2*x)
        g=sp.Matrix([[-1,0,0,0],[0,a**2,0,0],[0,0,a**2,a**2*hc],[0,0,a**2*hc,a**2]])
    G=christoffel(g)
    uy_up=ep*V*sp.exp(I*p*x)      # frame leg along y, complex phase p
    g00=g[0,0]; gyy=g[2,2]
    u0=sp.symbols('u0d')
    sol=sp.solve(sp.Eq(g00*u0**2+gyy*uy_up**2,-1),u0)
    pick=[s for s in sol if sp.simplify(s.subs({e1:0,e2:0,ep:0})-1)==0]
    u0v=trunc(pick[0] if pick else sol[0])
    u_up=sp.Matrix([u0v,0,uy_up,0])
    u_low=sp.Matrix([trunc(sum(g[m,nn]*u_up[nn] for nn in range(4))) for m in range(4)])
    return g,u_low,u_up,G

def Bn(n,g,u_low,u_up,G,break_F2=False):
    v=u_low
    for _ in range(2*n):
        v=Dop(v,u_up,G,break_F2=break_F2)
    return trunc(sp.expand(sum(u_up[m]*v[m] for m in range(4))))

def seagull_coeff(n,cross=False,break_F2=False):
    g,u_low,u_up,G=build(cross=cross)
    B=Bn(n,g,u_low,u_up,G,break_F2=break_F2)
    return sp.expand(B.coeff(e1,1).coeff(e2,1).coeff(ep,2))

# --- paranoid extractor: the FULL x-phase is e^{i(m1 q1 + m2 q2 + mp p)x}. The frame KINETIC seed is
# any term whose polynomial prefactor (after collecting the phase) carries an EXPLICIT p^2. With complex
# phases, spatial derivatives d_x become i*(momentum), so p^2 appears as a real polynomial coeff. ---
Eq1,Eq2,Ep=sp.symbols('Eq1 Eq2 Ep', positive=True)  # placeholders for the x-phase exponentials
def strip_phases(c):
    """Replace e^{i q1 x}, e^{i q2 x}, e^{i p x} (and conjugates/powers) with inert symbols Eq1,Eq2,Ep.
    Any REMAINING explicit p (outside the phase) is a genuine spatial-momentum polynomial factor from a
    d_x that pulled down i*p onto the FRAME leg -- that is the p^2 cone we hunt. rewrite exp so that
    exp(I*(a*q1+b*q2+c*p)*x) factorizes into Eq1**a * Eq2**b * Ep**c."""
    c=sp.expand(c)
    # force all exponentials to the canonical exp(I*(...)*x) and split the sum in the exponent
    def repl(e):
        e=sp.expand(e)
        # collect all exp(...) atoms
        for atom in list(e.atoms(sp.exp)):
            arg=sp.expand(atom.args[0])
            # arg = I*x*(coeff of q1)*q1 + ... ; read integer multiplicities
            m1=sp.simplify(arg.coeff(q1)/(I*x)) if arg.has(q1) else 0
            m2=sp.simplify(arg.coeff(q2)/(I*x)) if arg.has(q2) else 0
            mp=sp.simplify(arg.coeff(p )/(I*x)) if arg.has(p ) else 0
            leftover=sp.simplify(arg - I*x*(m1*q1+m2*q2+mp*p))
            rep=sp.exp(leftover)*Eq1**m1*Eq2**m2*Ep**mp
            e=e.subs(atom,rep)
        return sp.expand(e)
    return repl(c)

def p_power_content(c):
    """Return: (has_p, coeff of p^2 as full symbol, coeff of p^1, coeff of p^0, does p^2 carry q?).
    p is now the EXPLICIT polynomial p (spatial-derivative momentum on the FRAME leg); the phase p is
    hidden in Ep so it does not pollute the Poly."""
    if c==0:
        return dict(zero=True,p2=sp.S(0),p1=sp.S(0),p0=sp.S(0),has_p=False,p2_has_q=False)
    c=strip_phases(c)
    has_p=c.has(p)
    if has_p:
        pp=sp.Poly(c,p)
        p2=sp.expand(pp.nth(2)); p1=sp.expand(pp.nth(1)); p0=sp.expand(pp.nth(0))
    else:
        p2=sp.S(0); p1=sp.S(0); p0=sp.expand(c)
    p2_has_q=(p2.has(q1) or p2.has(q2))
    return dict(zero=False,p2=p2,p1=p1,p0=p0,has_p=has_p,p2_has_q=p2_has_q)

sec("(A) INDEPENDENT seagull p-power hunt, COMPLEX phases, exact dS, indep q1,q2, n=1..NMAX")
NMAX=int(os.environ.get('SIB3_HUNT_NMAX', 4))
print(f"   NMAX={NMAX} (2n = {[2*n for n in range(1,NMAX+1)]} covariant derivatives)")
print("   Reading per n: full p^2 seed (SPATIAL cone if !=0), p^1 (p*q cross), p^0 (mass), does p^2 carry q?")
tab={}
for pol,cross in (('same',False),('cross',True)):
    print(f"\n   --- {pol}-pol TT ---")
    for n in range(1,NMAX+1):
        t0=time.time()
        c=seagull_coeff(n,cross=cross)
        st=p_power_content(c)
        tab[(pol,n)]=st
        dt=time.time()-t0
        print(f"   n={n}: p^2 seed={sp.simplify(st['p2'])} | p^1 (p*q cross)={sp.simplify(st['p1'])} "
              f"| has_p?{st['has_p']} | p^2 carries q?{st['p2_has_q']}  [{dt:.1f}s]")
        ck(f"{pol} n={n}: NO p^2 spatial cone (p2 seed==0)", sp.simplify(st['p2'])==0)
        ck(f"{pol} n={n}: NO p^1 (p*q) cross-kinetic either", sp.simplify(st['p1'])==0)

sec("(B) F2-BREAK CONTROL: inject lam*d_x -> p^2 (or p*q) must switch ON (prove extractor is live)")
for n in (1,2,3):
    cb=seagull_coeff(n,cross=False,break_F2=True)
    stb=p_power_content(cb)
    intact=sp.simplify(tab[('same',n)]['p2'])
    broke=sp.simplify(stb['p2'])
    print(f"   n={n}: INTACT p^2={intact}  ||  BROKEN p^2={broke}  (lam-carrying? {broke.has(lam) if broke!=0 else False})")
    ck(f"F2-break n={n}: p^2 switches ON and carries lam (extractor sensitive)",
       intact==0 and broke!=0 and broke.has(lam))

sec("VERDICT (independent hunt)")
allp2=all(sp.simplify(tab[(pol,n)]['p2'])==0 and sp.simplify(tab[(pol,n)]['p1'])==0
          for pol in ('same','cross') for n in range(1,NMAX+1))
print(f"   ALL n=1..{NMAX}, both pol, complex-phase indep q1,q2: p^2 AND p^1 seeds = 0?  {allp2}")
print(f"\nPASS={len(PASS)} FAIL={len(FAIL)}")
sys.exit(0 if not FAIL else 1)
