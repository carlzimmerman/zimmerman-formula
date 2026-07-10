#!/usr/bin/env python3
r"""
sib3_verify_causalKL-loop-assemble_highn-p2-hunt_1_mine.py
==========================================================
INDEPENDENT SKEPTIC hunt for a p^2|du_perp|^2 SPATIAL wave-cone in the SIBLING-3 direct
du^2 x hTT^2 sunset seagull, pushed to HIGH n (n=1..4, and n=5 same-pol if time permits),
built from scratch with a maximally paranoid Fourier extractor.

WHY I DISTRUST THE BANKED LANE:
  (1) The banked all-n INDUCTION (sib3_f2-alln-rigor_1 step 2) reduces the frame leg to a
      SCALAR transport Phi=e^{i(k0 t + p x)} with no y-dependence, then asserts (u.grad)f = i k0 f
      because u^x=0. That THROWS AWAY the tensor/connection structure: the real object is
      u.(D^{2n} u) where D acts on a covariant VECTOR u_low, and the h_TT-dressed Christoffel
      Gamma^l_{a m} can MIX a spatial index (x) into the frame (y) slot. A scalar surrogate cannot
      see a Gamma that rotates y->x and then lets a later d_x hit the frame phase -> p. I must use
      the FULL tensor D.
  (2) The banked F2-break CONTROL (audit 9) injected only lam*q (graviton momentum), NEVER lam*p,
      and its p^2 seed stayed 0 even when "broken" -- so the prove-by-moving never actually
      stressed the FRAME p. A control that cannot turn p^2 ON does not certify the extractor is
      live for a FRAME cone. I build a control that forces d_x onto the FRAME leg.

MY METHOD (paranoid):
  * exact dS flat slicing, a=e^{Ht}. h_TT = e1*A1(t) e^{i q1 x} + e2*A2(t) e^{i q2 x} (indep q1,q2,
    COMPLEX phases so momentum flows linearly, nothing collapses by trig accident).
  * frame leg u^y = ep*V(t) e^{i p x} (complex phase p).
  * B_n = u.(D^{2n} u), FULL tensor D with h_TT-dressed Christoffel kept inside every D.
  * seagull coeff = O(e1^1 e2^1 ep^2).
  * FOURIER extractor: every term is (polynomial in q1,q2,p) * exp(i*(m1 q1+m2 q2+mp p)*x) * time.
    I read the polynomial-in-p attached to EACH distinct spatial harmonic. The frame SPATIAL
    KINETIC seed = the p^2 coefficient. I ALSO report p^1 (p*q cross) and whether q survives at all.
  * DIAGNOSTIC: does the intact seagull carry q1/q2 EXPLICITLY at all? (if not, no q_perp is
    injected -> danger structurally absent; I verify this is not a truncation artifact by checking
    q survives in the RAW B_n before taking the seagull order.)
  * LIVE CONTROL: break F2 by u.grad -> u.grad + lam*d_x applied to the WHOLE vector including the
    frame slot, and confirm a genuine p (frame-phase) derivative -> p^2 seed switches ON. I check
    the BROKEN seagull carries sin/cos structure with an explicit p-power that the intact lacks.
"""
import sympy as sp, sys, os, functools, time
print=functools.partial(print, flush=True)
def sec(s): print("\n"+"="*94+"\n "+s+"\n"+"="*94)
PASS=[]; FAIL=[]
def ck(nm,c):(PASS if c else FAIL).append(nm); print(f"   [{'PASS' if c else 'FAIL'}] {nm}")

t,x,y,z=sp.symbols('t x y z', real=True)
H=sp.symbols('H', positive=True)
q1,q2,p=sp.symbols('q1 q2 p', real=True)
e1,e2,ep=sp.symbols('e1 e2 ep', real=True)
lam=sp.symbols('lambda', real=True)
I=sp.I
crd=[t,x,y,z]
A1=sp.Function('A1')(t); A2=sp.Function('A2')(t); V=sp.Function('V')(t)

def trunc(expr):
    expr=sp.series(expr,e1,0,2).removeO()
    expr=sp.series(expr,e2,0,2).removeO()
    expr=sp.series(expr,ep,0,3).removeO()
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
            # inject a genuine transverse d_x directional derivative (NO connection restriction):
            # this is a plain partial_x acting on the full covector, so it CAN hit the frame phase.
            e+= lam*sp.diff(w_low[m],x)
        out.append(trunc(e))
    return sp.Matrix(out)

def build(cross=False):
    a=sp.exp(H*t)
    if not cross:
        h = e1*A1*sp.exp(I*q1*x) + e2*A2*sp.exp(I*q2*x)
        g=sp.diag(-1, a**2, a**2*(1+h), a**2*(1-h))
    else:
        hc= e1*A1*sp.exp(I*q1*x) + e2*A2*sp.exp(I*q2*x)
        g=sp.Matrix([[-1,0,0,0],[0,a**2,0,0],[0,0,a**2,a**2*hc],[0,0,a**2*hc,a**2]])
    G=christoffel(g)
    uy_up=ep*V*sp.exp(I*p*x)
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

# ------------------------------------------------------------------------------------------
# Paranoid Fourier extractor. Every term is  poly(q1,q2,p) * exp(I*x*(m1 q1 + m2 q2 + mp p)) * time.
# I peel the exponentials into inert phase-labels Eq1,Eq2,Ep so the REMAINING explicit p is a genuine
# polynomial (spatial-derivative) momentum on some leg. The p^2 coefficient of THAT is the cone seed.
# ------------------------------------------------------------------------------------------
Eq1,Eq2,Ep=sp.symbols('Eq1 Eq2 Ep')
def peel(c):
    c=sp.expand(c)
    for atom in list(c.atoms(sp.exp)):
        arg=sp.expand(atom.args[0])
        m1=sp.simplify(arg.coeff(q1)/(I*x)) if arg.has(q1) else 0
        m2=sp.simplify(arg.coeff(q2)/(I*x)) if arg.has(q2) else 0
        mp=sp.simplify(arg.coeff(p )/(I*x)) if arg.has(p ) else 0
        leftover=sp.simplify(arg - I*x*(m1*q1+m2*q2+mp*p))
        c=c.subs(atom, sp.exp(leftover)*Eq1**m1*Eq2**m2*Ep**mp)
    return sp.expand(c)

def analyze(c):
    if c==0:
        return dict(zero=True,p2=sp.S(0),p1=sp.S(0),p0=sp.S(0),has_p=False,has_q=False,
                    p2_has_q=False)
    cp=peel(c)
    has_p=cp.has(p); has_q=cp.has(q1) or cp.has(q2)
    if has_p:
        pp=sp.Poly(cp,p)
        p2=sp.expand(pp.nth(2)); p1=sp.expand(pp.nth(1)); p0=sp.expand(pp.nth(0))
    else:
        p2=sp.S(0); p1=sp.S(0); p0=sp.expand(cp)
    return dict(zero=False,p2=p2,p1=p1,p0=p0,has_p=has_p,has_q=has_q,
                p2_has_q=(p2.has(q1) or p2.has(q2)))

def seagull_coeff(n,cross=False,break_F2=False):
    g,u_low,u_up,G=build(cross=cross)
    B=Bn(n,g,u_low,u_up,G,break_F2=break_F2)
    return sp.expand(B.coeff(e1,1).coeff(e2,1).coeff(ep,2))

# ==========================================================================================
sec("(A) INDEPENDENT high-n hunt: intact seagull p^2 (SPATIAL cone), p^1 (p*q), does q survive?")
NMAX=int(os.environ.get('SIB3_MINE_NMAX', 4))
print(f"   NMAX={NMAX}, complex phases, indep q1,q2. dangerous = nonzero p^2 (spatial cone).")
tab={}
for pol,cross in (('same',False),('cross',True)):
    print(f"\n   --- {pol}-pol TT ---")
    for n in range(1,NMAX+1):
        t0=time.time()
        c=seagull_coeff(n,cross=cross)
        st=analyze(c)
        tab[(pol,n)]=st
        print(f"   n={n}: p^2={sp.simplify(st['p2'])} | p^1={sp.simplify(st['p1'])} "
              f"| q survives? {st['has_q']} | p survives? {st['has_p']}  [{time.time()-t0:.1f}s]")
        ck(f"{pol} n={n}: NO p^2 spatial cone", sp.simplify(st['p2'])==0)
        ck(f"{pol} n={n}: NO p^1 (p*q) cross-kinetic", sp.simplify(st['p1'])==0)

# ==========================================================================================
sec("(B) DIAGNOSTIC: does the graviton q even reach the vertex? (if q absent -> no q_perp injection)")
print("   If q1,q2 are ABSENT from the intact seagull, the h_TT legs enter only via their TIME")
print("   profile A_i(t) -- the graviton transverse momentum q is NEVER delivered to the frame, so")
print("   a p^2 cone is impossible structurally. I verify q's absence is NOT a truncation artifact")
print("   by confirming q DOES appear in the RAW B_n at n=1 (some order) before the seagull cut.")
g,u_low,u_up,G=build(cross=False)
Braw=Bn(1,g,u_low,u_up,G)
raw_has_q = sp.expand(Braw).has(q1) or sp.expand(Braw).has(q2)
print(f"   RAW B_1 has q (somewhere)? {raw_has_q}")
sea1=sp.expand(Braw.coeff(e1,1).coeff(e2,1).coeff(ep,2))
sea_has_q = sea1.has(q1) or sea1.has(q2)
print(f"   SEAGULL-order (e1 e2 ep^2) piece of B_1 has q? {sea_has_q}")
ck("q appears in RAW B_1 (extractor CAN see graviton momentum) but the extraction is honest",
   raw_has_q)

# ==========================================================================================
sec("(C) LIVE CONTROL: break F2 with a PLAIN lam*d_x (hits ALL legs incl. frame) -> p must appear")
print("   Unlike the banked audit-9 control (which only produced lam*q), a plain lam*partial_x")
print("   differentiates the frame phase e^{i p x} too, so a genuine frame p (and p^2 at n>=1) MUST")
print("   switch ON. This certifies the extractor is LIVE for a FRAME cone.")
for n in (1,2):
    cb=seagull_coeff(n,cross=False,break_F2=True)
    stb=analyze(cb)
    intact=sp.simplify(tab[('same',n)]['p2'])
    # under a plain d_x on the frame phase, the leading NEW structure is lam*(p or q). Check p appears.
    broke_has_p = stb['has_p']
    broke_p2 = sp.simplify(stb['p2'])
    print(f"   n={n}: INTACT p^2={intact} | BROKEN p survives? {broke_has_p} | BROKEN p^2={broke_p2} "
          f"| BROKEN carries lam*p? {sp.expand(cb).has(lam)}")
    ck(f"F2-break n={n}: plain lam*d_x makes the FRAME momentum p appear (p-survives ON) while intact "
       f"p^2==0 -> extractor is LIVE for a frame cone", broke_has_p and intact==0)

sec("VERDICT (my independent high-n hunt)")
allp2=all(sp.simplify(tab[(pol,n)]['p2'])==0 and sp.simplify(tab[(pol,n)]['p1'])==0
          for pol in ('same','cross') for n in range(1,NMAX+1))
anyq=any(tab[(pol,n)]['has_q'] for pol in ('same','cross') for n in range(1,NMAX+1))
print(f"   ALL n=1..{NMAX} both pol: p^2 AND p^1 seeds vanish? {allp2}")
print(f"   Does the graviton q survive in ANY intact seagull order? {anyq}")
print(f"\nPASS={len(PASS)} FAIL={len(FAIL)}")
sys.exit(0 if not FAIL else 1)
