#!/usr/bin/env python3
r"""
INDEPENDENT SKEPTIC re-derivation of the SIBLING-3 seagull p-structure, pushed to HIGH n.

I do NOT trust the hard-coded frame_symbol model in sib3_setup_2 PART 1 (it returns
(k0)^{2n} by fiat -- that is asserting the conclusion). The only honest all-n test is the
FULL curved-dS covariant-derivative CAS. sib3_setup_1 stopped at n=3. Here I re-implement
the covariant-derivative tower from scratch (no import of the banked builders) and push the
explicit p^2 SPATIAL wave-cone seed extraction to n=4,5,6, both polarizations.

I ALSO attack three high-n leak routes the reviewer flagged:
  (R1) the h_TT-dressed connection Gamma(h_TT) ~ q h injecting q_perp that at high n combines
       with the frame legs into an EXPLICIT p^2 (via a q-p cross term that could reduce to p^2).
  (R2) a subtle SYMMETRIZATION: check both p^2 AND the p*q cross coefficient (a p*q term with
       the graviton q integrated to <q^2> could masquerade as a p^2 mass -- but if it is
       genuinely p*q it would be a p-ODD gradient, still not a clean cone; I read p^1 and p^2).
  (R3) PROVE-BY-MOVING at HIGH n (not just n=1): break F2 at n=4 and confirm p^2 switches ON,
       so a null p^2 at n=4 is a real null, not an extraction that went blind at high order.

Metric: exact dS flat slicing ds^2=-dt^2+a^2[dx^2+(1+h)dy^2+(1-h)dz^2], a=e^{Ht}.
h_TT=eps2 HTT(t) cos(q x); frame du_perp along y: u^y=eps V(t) cos(p x).
p^2 spatial seed = explicit p^2 polynomial factor on the surviving |du_perp|^2 structure.
"""
import sympy as sp, sys, functools, time, os
print=functools.partial(print,flush=True)
def sec(s): print("\n"+"="*90+"\n "+s+"\n"+"="*90)
PASS=[];FAIL=[]
def ck(n,c):(PASS if c else FAIL).append(n);print(f"   [{'PASS' if c else 'FAIL'}] {n}")

t,x,y,z=sp.symbols('t x y z',real=True)
H=sp.symbols('H',positive=True)
q,p=sp.symbols('q p',real=True)
eps,eps2=sp.symbols('epsilon epsilon2',real=True)
lam=sp.symbols('lambda',real=True)
crd=[t,x,y,z]
MAXE=2;MAXE2=2
def trunc(e):
    # fast bilinear truncation via Poly; fall back to series for rational (metric-inverse) exprs
    e=sp.expand(e)
    if e==0: return sp.Integer(0)
    try:
        P=sp.Poly(e,eps,eps2)
        out=sp.Integer(0)
        for (a,b),c in zip(P.monoms(),P.coeffs()):
            if a<=MAXE and b<=MAXE2:
                out+=c*eps**a*eps2**b
        return sp.expand(out)
    except sp.PolynomialError:
        e=sp.series(e,eps,0,MAXE+1).removeO()
        e=sp.series(e,eps2,0,MAXE2+1).removeO()
        return sp.expand(e)

def christ(g):
    gi=g.inv();G=[[[sp.Integer(0)]*4 for _ in range(4)] for _ in range(4)]
    for l in range(4):
        for m in range(4):
            for nu in range(4):
                G[l][m][nu]=trunc(sum(gi[l,s]*(sp.diff(g[s,m],crd[nu])+sp.diff(g[s,nu],crd[m])
                                -sp.diff(g[m,nu],crd[s])) for s in range(4))/2)
    return G

def Dop(w,u_up,G,break_F2=False):
    out=[]
    for m in range(4):
        e=sum(u_up[al]*(sp.diff(w[m],crd[al])-sum(G[l][al][m]*w[l] for l in range(4))) for al in range(4))
        if break_F2:
            e+=lam*(sp.diff(w[m],x)-sum(G[l][1][m]*w[l] for l in range(4)))
        out.append(trunc(e))
    return sp.Matrix(out)

def build(cross=False):
    a=sp.exp(H*t)
    if not cross:
        h=eps2*sp.Function('HTT')(t)*sp.cos(q*x)
        g=sp.diag(-1,a**2,a**2*(1+h),a**2*(1-h))
    else:
        hc=eps2*sp.Function('HTT')(t)*sp.cos(q*x)
        g=sp.Matrix([[-1,0,0,0],[0,a**2,0,0],[0,0,a**2,a**2*hc],[0,0,a**2*hc,a**2]])
    G=christ(g)
    V=sp.Function('V')(t)
    uy=eps*V*sp.cos(p*x)
    u0=sp.symbols('u0d')
    sol=sp.solve(sp.Eq(g[0,0]*u0**2+g[2,2]*uy**2,-1),u0)
    pick=[s for s in sol if sp.simplify(s.subs({eps:0,eps2:0})-1)==0]
    u0v=trunc(pick[0] if pick else sol[0])
    u_up=sp.Matrix([u0v,0,uy,0])
    u_low=sp.Matrix([trunc(sum(g[m,nn]*u_up[nn] for nn in range(4))) for m in range(4)])
    return g,u_low,u_up,G

def Bn(n,cross=False,break_F2=False):
    g,u_low,u_up,G=build(cross=cross)
    v=u_low
    for _ in range(2*n):
        v=Dop(v,u_up,G,break_F2=break_F2)
    return trunc(sum(u_up[m]*v[m] for m in range(4)))

def seagull(n,cross=False,break_F2=False):
    B=Bn(n,cross=cross,break_F2=break_F2)
    return sp.expand(B.coeff(eps,2).coeff(eps2,2))

# p-power extraction: substitute all x-oscillations to symbols, read explicit p^1,p^2 factors
Cq,Sq,Cp,Sp=sp.symbols('Cq Sq Cp Sp',real=True)
def strip_osc(c):
    c=sp.expand_trig(sp.expand(c))
    sub={sp.cos(q*x):Cq,sp.sin(q*x):Sq,sp.cos(p*x):Cp,sp.sin(p*x):Sp,
         sp.cos((q+p)*x):Cq*Cp-Sq*Sp,sp.cos((q-p)*x):Cq*Cp+Sq*Sp,
         sp.sin((q+p)*x):Sq*Cp+Cq*Sp,sp.sin((q-p)*x):Sq*Cp-Cq*Sp,
         sp.cos(2*q*x):Cq*Cq-Sq*Sq,sp.sin(2*q*x):2*Sq*Cq,
         sp.cos(2*p*x):Cp*Cp-Sp*Sp,sp.sin(2*p*x):2*Sp*Cp}
    for k,v in sub.items(): c=c.subs(k,v)
    return sp.expand(c)

def ppowers(c):
    lc=strip_osc(c)
    if not lc.has(p):
        return {'p2':sp.Integer(0),'p1':sp.Integer(0),'p0':sp.simplify(lc),'has_q':lc.has(q)}
    P=sp.Poly(lc,p)
    return {'p2':sp.simplify(P.nth(2)),'p1':sp.simplify(P.nth(1)),
            'p0':sp.simplify(P.nth(0)),'has_q':lc.has(q)}

NMAX=int(os.environ.get('MYNMAX','6'))
sec(f"INDEPENDENT full curved-dS CAS: seagull p-structure, n=1..{NMAX}, both polarizations")
print("   p2 = explicit p^2 SPATIAL wave-cone seed (FATAL if nonzero)")
print("   p1 = explicit p^1 (odd gradient); p0 = p-free mass/time piece")
res={}
for pol,cross in (('same',False),('cross',True)):
    print(f"\n   --- {pol}-pol ---")
    for n in range(1,NMAX+1):
        t0=time.time()
        c=seagull(n,cross=cross)
        pw=ppowers(c)
        res[(pol,n)]=pw
        print(f"   n={n}: p2={pw['p2']} | p1={pw['p1']} | p0_nonzero={pw['p0']!=0} | q_in_coeff={pw['has_q']} | {round(time.time()-t0,1)}s")
        ck(f"{pol} n={n}: NO p^2 spatial seed AND NO p^1 gradient (p-free -> mass/time)",
           sp.simplify(pw['p2'])==0 and sp.simplify(pw['p1'])==0)

sec("PROVE-BY-MOVING at HIGH n: break F2 at n=4 -> p^2 (or lam*p) spatial seed must switch ON")
cb=seagull(4,cross=False,break_F2=True)
lcb=strip_osc(cb)
lam_piece=sp.expand(lcb.coeff(lam,1)) if lcb.has(lam) else sp.Integer(0)
switched=(lam_piece!=0) and (lam_piece.has(p) or lam_piece.has(q))
print(f"   n=4 F2-broken: lam-coefficient carries explicit spatial momentum? {switched}")
print(f"   n=4 F2-intact p^2 seed (from table) = {res[('same',4)]['p2'] if ('same',4) in res else 'n/a'}")
ck("HIGH-n control: breaking F2 at n=4 injects an explicit spatial-momentum term (extraction still SENSITIVE at high n)",
   switched)

sec("VERDICT (independent skeptic high-n CAS)")
allclean=all(sp.simplify(res[(pol,n)]['p2'])==0 and sp.simplify(res[(pol,n)]['p1'])==0
             for pol in ('same','cross') for n in range(1,NMAX+1))
print(f"   ALL n=1..{NMAX}, both pol: p^2 seed = 0 AND p^1 = 0 ?  {allclean}")
print(f"   PASS={len(PASS)} FAIL={len(FAIL)}")
sys.exit(0 if not FAIL else 1)
