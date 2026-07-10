#!/usr/bin/env python3
r"""
SKEPTIC AUDIT of SIBLING-3 (du^2 x hTT^2 seagull) all-n p-structure claim.

Independent re-derivation. Attack points:
  (A1) Is the RAW seagull coefficient (BEFORE any strip_osc) genuinely free of the frame
       momentum p AND graviton momenta q1,q2? (Claim: q_explicit=p_explicit=False.)
       If TRUE, the vertex is manifestly a MASS/time term -- no spatial derivative survives,
       and the whole "(p.q)^2 builds a cone at high n" worry is moot. Verify the RAW object,
       not the stripped one (strip_osc could in principle hide/misread momenta).
  (A2) strip_osc COMPLETENESS: after stripping, are there ANY residual sp.cos/sp.sin that
       still contain p,q1,q2? If yes, Poly(s,p).nth(2) is UNRELIABLE (p hidden in a transcendental).
  (A3) PARITY route to a hidden cone: even if the vertex has no explicit p^2, a term linear in p
       times a graviton momentum (p.q) could be promoted to p^2 by the loop integral
       int d^3q q_i q_j <hh> ~ delta_ij. For the SEAGULL TADPOLE (both gravitons on one vertex,
       q2=-q1) a p^1 q^1 term is ODD in q and integrates to ZERO -- so ONLY an explicit p^2
       (i.e. (p.q)^2 or a bare p^2) can seed a cone. TEST: does the raw vertex carry ANY term
       linear in p times linear in q? (If present, must check it's parity-odd; if a (p.q)^2
       appears, it is an explicit p^2 and would be caught.)
  (A4) PROVE-BY-MOVING: break F2 -> the p^2 seed and the q content must switch ON.

Everything recomputed from scratch (own Christoffels, own Dop), NOT importing their build.
"""
import sympy as sp, functools
print=functools.partial(print, flush=True)
def sec(t): print("\n"+"#"*90+"\n# "+t+"\n"+"#"*90)

t,x,y,z=sp.symbols('t x y z',real=True)
H=sp.symbols('H',positive=True)
q1,q2,p=sp.symbols('q1 q2 p',real=True)
e1,e2,ep=sp.symbols('e1 e2 ep',real=True)
lam=sp.symbols('lambda',real=True)
crd=[t,x,y,z]
A1=sp.Function('A1')(t); A2=sp.Function('A2')(t); V=sp.Function('V')(t)
ORD={'e1':1,'e2':1,'ep':2}
def trunc(ex):
    ex=sp.series(ex,e1,0,ORD['e1']+1).removeO()
    ex=sp.series(ex,e2,0,ORD['e2']+1).removeO()
    ex=sp.series(ex,ep,0,ORD['ep']+1).removeO()
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
    a=sp.exp(H*t)
    h=e1*A1*sp.cos(q1*x)+e2*A2*sp.cos(q2*x)
    if not cross:
        g=sp.diag(-1,a**2,a**2*(1+h),a**2*(1-h))
    else:
        g=sp.Matrix([[-1,0,0,0],[0,a**2,0,0],[0,0,a**2,a**2*h],[0,0,a**2*h,a**2]])
    G=christoffel(g)
    uy=ep*V*sp.cos(p*x)
    u0=sp.symbols('u0d')
    sol=sp.solve(sp.Eq(g[0,0]*u0**2+g[2,2]*uy**2,-1),u0)
    pick=[s for s in sol if sp.simplify(s.subs({e1:0,e2:0,ep:0})-1)==0]
    u0v=trunc(pick[0] if pick else sol[0])
    u_up=sp.Matrix([u0v,0,uy,0])
    u_low=sp.Matrix([trunc(sum(g[m,nn]*u_up[nn] for nn in range(4))) for m in range(4)])
    return g,u_low,u_up,G
def Bn(n,cross=False,break_F2=False):
    g,u_low,u_up,G=build(cross=cross)
    v=u_low
    for _ in range(2*n):
        v=Dop(v,u_up,G,break_F2=break_F2)
    return trunc(sp.expand(sum(u_up[m]*v[m] for m in range(4))))
def seagull(n,cross=False,break_F2=False):
    return sp.expand(Bn(n,cross,break_F2).coeff(e1,1).coeff(e2,1).coeff(ep,2))

def residual_trig_has_momentum(expr):
    """Return True if any cos/sin atom in expr contains p,q1,q2 in its argument."""
    for f in expr.atoms(sp.cos, sp.sin):
        arg=f.args[0]
        if arg.has(p) or arg.has(q1) or arg.has(q2):
            return True
    return False

# ------ own robust momentum extractor: convert the coefficient to momentum space by
# reading the coefficient of e^{i k x} components. Simplest robust route: substitute the
# oscillations by rewriting cos/sin in exponential form, expand, and inspect which pure
# exponentials e^{i m p x + i a q1 x + i b q2 x} carry which explicit polynomial p,q powers.
def raw_momentum_report(c):
    cc=sp.expand(c)
    return dict(has_p=cc.has(p), has_q1=cc.has(q1), has_q2=cc.has(q2))

def exp_p2_seed(c):
    """
    ROBUST p^2 spatial-kinetic extractor independent of their strip dict.
    Rewrite all trig in complex exponentials, expand, then the x-dependence is a sum of
    e^{i K x} with K a linear combo of p,q1,q2. Collect terms, drop the e^{iKx} (set x's
    oscillation aside by grouping on the exponent), and read the polynomial coefficient of p^2
    in the amplitude of EACH harmonic. A genuine spatial kinetic = a nonzero explicit p^2
    amplitude on SOME harmonic. Also report any p^1*q^1 (parity-route) amplitude.
    """
    cc=sp.expand(sp.rewrite(c, sp.exp)) if hasattr(sp,'rewrite') else sp.expand(c.rewrite(sp.exp))
    cc=sp.expand(cc)
    I=sp.I
    # group by the x-harmonic: coefficient extraction via collecting exp(I*K*x)
    # Build a dict harmonic-exponent-tuple -> amplitude by matching exp(I*(...)*x).
    # Practical approach: substitute x-> a formal, take the Fourier-like decomposition by
    # differentiating out. Simpler & robust: treat E1=exp(I*q1*x),E2=exp(I*q2*x),Ep=exp(I*p*x)
    E1,E2,Ep=sp.symbols('E1 E2 Ep')
    reps={sp.exp(I*q1*x):E1, sp.exp(-I*q1*x):1/E1,
          sp.exp(I*q2*x):E2, sp.exp(-I*q2*x):1/E2,
          sp.exp(I*p*x):Ep, sp.exp(-I*p*x):1/Ep}
    cc2=cc
    for k,v in reps.items(): cc2=cc2.subs(k,v)
    cc2=sp.expand(cc2)
    # anything with residual exp(...) that still contains x*momentum -> incomplete
    incomplete = any((a.args[0]).has(x) for a in cc2.atoms(sp.exp))
    # amplitudes: for each monomial in E1,E2,Ep (the harmonics), read p-poly
    cc2=sp.expand(cc2)
    poly_p_amplitudes=[]
    # collect coefficient of each harmonic monomial E1^a E2^b Ep^c
    cc2=sp.together(cc2)
    cc2=sp.expand(cc2)
    # get p^2 and p^1 content overall (harmonic-agnostic but momentum p is explicit poly here)
    has_p=cc2.has(p); has_q1=cc2.has(q1); has_q2=cc2.has(q2)
    if has_p:
        # note: p also sits inside Ep? we substituted exp(I p x)->Ep, so remaining p is EXPLICIT
        pp=sp.Poly(cc2,p)
        p2=sp.simplify(pp.nth(2)); p1=sp.simplify(pp.nth(1)); p0=sp.simplify(pp.nth(0))
    else:
        p2=sp.Integer(0); p1=sp.Integer(0); p0=sp.simplify(cc2)
    return dict(incomplete=incomplete, has_p=has_p, has_q1=has_q1, has_q2=has_q2,
                p2=p2, p1=p1, p0_massish=(p0!=0))

sec("A1/A2/A3: RAW momenta + robust exponential extractor, n=1,2,3 (same + cross)")
allpass=True
for pol,cross in (('same',False),('cross',True)):
    for n in (1,2,3):
        c=seagull(n,cross=cross)
        raw=raw_momentum_report(c)
        rep=exp_p2_seed(c)
        # p^1*q term (parity route): explicit p^1 amplitude carrying q1 or q2
        p1_has_q = (rep['p1']!=0) and (rep['p1'].has(q1) or rep['p1'].has(q2))
        print(f"\n[{pol} n={n}] RAW has_p={raw['has_p']} has_q1={raw['has_q1']} has_q2={raw['has_q2']}")
        print(f"        EXP-extractor: incomplete_strip={rep['incomplete']}  p2_seed={rep['p2']}  "
              f"p1_seed={rep['p1']}  mass_p0_nonzero={rep['p0_massish']}")
        print(f"        parity-route p^1*q term present? {p1_has_q}")
        ok = (rep['incomplete']==False) and (sp.simplify(rep['p2'])==0) and (not p1_has_q)
        # also: if RAW truly has no p and no q, that's the strongest benign statement
        manifest_mass = (not raw['has_p']) and (not raw['has_q1']) and (not raw['has_q2'])
        print(f"        => p2==0 & strip complete & no parity route? {ok} | RAW manifest-mass (no p,no q at all)? {manifest_mass}")
        allpass = allpass and ok

sec("A4: PROVE-BY-MOVING -- break F2, p^2 seed and q content must switch ON (n=1)")
cb=seagull(1,cross=False,break_F2=True)
rawb=raw_momentum_report(cb); repb=exp_p2_seed(cb)
print(f" F2-BROKEN n=1: RAW has_p={rawb['has_p']} has_q1={rawb['has_q1']} has_q2={rawb['has_q2']}")
print(f"                EXP-extractor p2_seed={repb['p2']}  (lam-carrying? {repb['p2'].has(lam) if repb['p2']!=0 else False})")
control_on = (repb['p2']!=0) and repb['p2'].has(lam)
print(f"                p^2 spatial seed switched ON by F2-break, lam-carrying? {control_on}")

sec("SKEPTIC VERDICT")
print(f" All n=1,2,3 (both pol): p2==0, strip complete, no parity route survived? {allpass}")
print(f" F2-break control turns p^2 ON (extraction sensitive)? {control_on}")
print(f" NET: {'p-FREE / BENIGN reproduced independently' if (allpass and control_on) else 'HOLE FOUND'}")
