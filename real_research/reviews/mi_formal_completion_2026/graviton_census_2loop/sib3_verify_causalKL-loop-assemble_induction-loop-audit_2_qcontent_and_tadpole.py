#!/usr/bin/env python3
r"""
SKEPTIC audit #2: the DEEPER question behind the tadpole claim.

The banked verdict says: seagull vertex is p-free -> in a TADPOLE the external p flows only through
the (p-free) vertex -> Sigma p-free. The hidden assumption is the SEAGULL IS A TADPOLE (both graviton
legs close on the SAME vertex with loop momenta k,-k). But the danger the workflow flags is a p^2 built
by the h_TT-dressed connection injecting the graviton q_perp onto the frame legs. Even in a tadpole, if
the vertex carried a term ~ (q_perp . p) or ~ q_perp^2 that after the loop integral (which sets an
INTERNAL scale, not p) leaves a residual p^2, that would be a cone. STEP-1 already checked q1*q2/q1^2/q2^2
= 0. Here I attack the SUBTLER channel:

  Does the seagull vertex carry an EXPLICIT graviton-momentum q on the du_perp KINETIC in a form that
  could survive as p? Concretely, I extract the FULL q-polynomial of the du_perp^2 hTT^2 vertex (real
  full-vector CAS, connection ON) and check:
    (i)  is there any term ~ q * p  (a q-p CROSS term -- the seed that, if the loop set q~p, becomes p^2)?
    (ii) is there any term ~ q^2    (which in a NON-tadpole (sunset) routing k->p-k would give (p-k)^2 -> p^2)?
    (iii) is the vertex EVEN in q (q -> -q symmetric)? An even, q^2-free, qp-free vertex cannot build p^2
          under ANY loop routing (tadpole or sunset), because the only p-carrying structure is absent.

This is stronger than "tadpole => p-free": it checks the vertex has NO q-structure that ANY routing could
convert to p^2. If the vertex q-polynomial has no q*p and no q^2 on the du_perp kinetic, the cone is
excluded independent of the tadpole assumption.

Metric: off-axis, graviton h_xy ~ e^{i q z}, frame du_perp along y prop along x (e^{i p x}).
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

def Dop(w_low,u_up,G):
    n=4; out=[]
    for m in range(n):
        e=0
        for al in range(n):
            e+=u_up[al]*(sp.diff(w_low[m],crd[al]) - sum(G[l][al][m]*w_low[l] for l in range(n)))
        out.append(trunc(e))
    return sp.Matrix(out)

def build_geom():
    h = eps2*HTT*sp.exp(I*q*z)
    g=sp.Matrix([[-1,0,0,0],[0,a**2, a**2*h,0],[0,a**2*h, a**2,0],[0,0,0,a**2]])
    uy_up=eps*V*sp.exp(I*p*x)
    G=christoffel(g)
    u0=sp.symbols('u0d')
    sol=sp.solve(sp.Eq(g[0,0]*u0**2+g[2,2]*uy_up**2,-1),u0)
    pick=[s for s in sol if sp.simplify(s.subs({eps:0,eps2:0})-1)==0]
    u0v=trunc(pick[0] if pick else sol[0])
    u_up=sp.Matrix([u0v,0,uy_up,0])
    u_low=sp.Matrix([trunc(sum(g[m,nn]*u_up[nn] for nn in range(4))) for m in range(4)])
    return u_low,u_up,G

def seagull(n):
    u_low,u_up,G=build_geom()
    v=u_low
    for _ in range(2*n):
        v=Dop(v,u_up,G)
    B=trunc(sp.expand(sum(u_up[m]*v[m] for m in range(4))))
    return sp.expand(B.coeff(eps,2).coeff(eps2,2))

def qp_content(c):
    """Strip phases, then read the joint (q,p) polynomial content of the du_perp^2 hTT^2 vertex."""
    c=sp.expand(c)
    ph=[a_ for a_ in c.atoms(sp.exp) if a_.has(x) or a_.has(z)]
    c2=sp.expand(c.subs({e:sp.Symbol(f'PH{i}') for i,e in enumerate(ph)}))
    # collect on q and p
    poly=sp.Poly(c2, q, p) if c2.has(q) or c2.has(p) else None
    terms={}
    if poly is not None:
        for (iq,ip),co in poly.terms():
            terms[(iq,ip)]=sp.simplify(co)
    return c2, terms

sec("SEAGULL VERTEX q,p-CONTENT (off-axis, connection ON): hunt q*p cross and q^2 seeds, n=1,2,3")
print("  (i) q*p cross term?  (ii) q^2 term?  (iii) any p?  -- ANY of these on the du_perp kinetic is a")
print("  cone seed under some loop routing. A vertex with NONE cannot build p^2 by ANY routing.")
NMAX=int(os.environ.get('SIB3_QP_NMAX',3))
for n in range(1,NMAX+1):
    t0=time.time()
    c=seagull(n)
    c2,terms=qp_content(c)
    # classify
    has_qp = any(iq>=1 and ip>=1 for (iq,ip) in terms)
    has_q2 = any(iq>=2 for (iq,ip) in terms)
    has_p  = any(ip>=1 for (iq,ip) in terms)
    has_q  = any(iq>=1 for (iq,ip) in terms)
    print(f"   n={n}: (q,p)-monomials present: {sorted(terms.keys())}  [{time.time()-t0:.1f}s]")
    print(f"        q*p cross? {has_qp} | q^2? {has_q2} | any p? {has_p} | any q? {has_q}")
    ck(f"n={n}: NO q*p cross term (no seed convertible to p^2 by a loop q~p)", not has_qp)
    ck(f"n={n}: NO q^2 term (no seed -> (p-k)^2 -> p^2 under sunset routing)", not has_q2)
    ck(f"n={n}: NO explicit p on the vertex (p-free, tadpole-independent)", not has_p)

sec("AUDIT #2 VERDICT")
print("  If the vertex has NO q*p cross AND NO q^2 AND NO p, then NEITHER a tadpole NOR a sunset routing")
print("  can build a p^2 spatial cone on the du_perp legs -- the p-free result is routing-independent,")
print("  stronger than the tadpole argument alone. (An all-q-EVEN, q^2-free, qp-free vertex is p-safe.)")
print(f"\nPASS={len(PASS)} FAIL={len(FAIL)}")
sys.exit(0 if not FAIL else 1)
