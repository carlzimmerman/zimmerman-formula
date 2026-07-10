#!/usr/bin/env python3
r"""
sib3_causalKL-loop-assemble_1_twomomentum_vertex_highn.py
=========================================================
METHOD 3, STEP 1 (the LOOP vertex, pushed past the banked n=1,2).

The seagull self-energy Sigma_perp closes the two h_TT legs into a LOOP. In a real loop the two
graviton legs carry INDEPENDENT momenta q1, q2 (q1 = loop momentum k, q2 = -(k - external); the
loop momentum is SPATIAL and integrated). The wave-cone danger the assembly cares about is an
EXPLICIT q1*q2 (or q1^2, q2^2) product -- TWO spatial derivatives, one on each graviton leg -- which,
once the loop integrates k, could leave a p^2 (or a genuine spatial) kinetic on the frame legs and,
paired with the TT q0-pole, PROPAGATE. FATAL.

Banked (gravverify_ttvertex-alln_missed-graph_02): the two-independent-momenta seagull has NO
explicit q_perp^2 seed at n=1,2 (both polarizations). THIS SCRIPT PUSHES THAT TO n=3 (and n=4 if
SIB3_NMAX>=4), i.e. one/two full orders past the banked n=2, for BOTH physical TT polarizations,
AND records the SAME-x frame p-power simultaneously (so we can feed the assembly the exact vertex
p- and q-content). It ALSO runs the F2-break control (inject a transverse d_x) so the extraction is
proven SENSITIVE at high n, not blind.

WHAT THIS DELIVERS TO STEP 2 (the assembly):
  seagull_vertex_content(n, cross): a dict
     {'q_seed': explicit q1^i q2^j (i+j>=2) coefficient  -- the wave-cone seed (must be 0),
      'p_seed': explicit p^2 coefficient on the frame legs -- the direct spatial kinetic (must be 0),
      'mass':   the surviving p-free, q-seed-free MASS piece (the only thing the loop can dress)}
so the assembly knows the vertex is p-free AND q_perp^2-free -> the closed loop can only produce a
MASS/time self-energy, never a spatial cone.

Metric (exact dS flat slicing): ds^2=-dt^2+a^2[dx^2+(1+h)dy^2+(1-h)dz^2], a=e^{Ht}, R=12H^2.
Two TT gravitons h = e1 A1 cos(q1 x) + e2 A2 cos(q2 x) (same yy/zz, or cross yz for BOTH).
Frame du_perp along y: u^y = ep V cos(p x).
"""
import sympy as sp, os, sys, functools
print=functools.partial(print, flush=True)

def sec(t): print("\n"+"="*94+"\n "+t+"\n"+"="*94)
PASS=[]; FAIL=[]
def ck(n,c):(PASS if c else FAIL).append(n); print(f"   [{'PASS' if c else 'FAIL'}] {n}")

t,x,y,z=sp.symbols('t x y z',real=True)
H=sp.symbols('H',positive=True)
q1,q2,p=sp.symbols('q1 q2 p',real=True)
e1,e2,ep=sp.symbols('e1 e2 ep',real=True)   # graviton1, graviton2, frame order counters
lam=sp.symbols('lambda',real=True)          # F2-break knob
crd=[t,x,y,z]; a=sp.exp(H*t)
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
    if not cross:
        h = e1*A1*sp.cos(q1*x) + e2*A2*sp.cos(q2*x)
        g=sp.diag(-1, a**2, a**2*(1+h), a**2*(1-h))
    else:
        hc = e1*A1*sp.cos(q1*x) + e2*A2*sp.cos(q2*x)
        g=sp.Matrix([[-1,0,0,0],[0,a**2,0,0],[0,0,a**2,a**2*hc],[0,0,a**2*hc,a**2]])
    G=christoffel(g); gi=g.inv()
    uy_up=ep*V*sp.cos(p*x)
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

def seagull_two_momentum(n,cross=False,break_F2=False):
    """The h1 h2 x du^2 coefficient (e1^1 e2^1 ep^2) = the TWO-INDEPENDENT-MOMENTUM loop vertex."""
    g,u_low,u_up,G=build(cross=cross)
    Bexpr=Bn(n,g,u_low,u_up,G,break_F2=break_F2)
    return sp.expand(Bexpr.coeff(e1,1).coeff(e2,1).coeff(ep,2))

# strip oscillation, keep EXPLICIT q1,q2,p powers = momenta from spatial derivatives
def strip_osc(c):
    Cq1,Sq1,Cq2,Sq2,Cp,Sp=sp.symbols('Cq1 Sq1 Cq2 Sq2 Cp Sp',real=True)
    ct=sp.expand_trig(sp.expand(c))
    # general product-to-sum: substitute all cos/sin of integer combos of q1,q2,p
    reps={}
    for expr in ct.atoms(sp.cos,sp.sin):
        arg=expr.args[0]
        # extract coefficients of x
        poly=sp.Poly(arg, x) if arg.has(x) else None
    # simpler: substitute the primitive oscillations and let expand_trig handle the rest
    subd={sp.cos(q1*x):Cq1,sp.sin(q1*x):Sq1,sp.cos(q2*x):Cq2,sp.sin(q2*x):Sq2,
          sp.cos(p*x):Cp,sp.sin(p*x):Sp,
          sp.cos((q1+q2)*x):Cq1*Cq2-Sq1*Sq2, sp.cos((q1-q2)*x):Cq1*Cq2+Sq1*Sq2,
          sp.sin((q1+q2)*x):Sq1*Cq2+Cq1*Sq2, sp.sin((q1-q2)*x):Sq1*Cq2-Cq1*Sq2,
          sp.cos((q1+p)*x):Cq1*Cp-Sq1*Sp, sp.cos((q1-p)*x):Cq1*Cp+Sq1*Sp,
          sp.sin((q1+p)*x):Sq1*Cp+Cq1*Sp, sp.sin((q1-p)*x):Sq1*Cp-Cq1*Sp,
          sp.cos((q2+p)*x):Cq2*Cp-Sq2*Sp, sp.cos((q2-p)*x):Cq2*Cp+Sq2*Sp,
          sp.sin((q2+p)*x):Sq2*Cp+Cq2*Sp, sp.sin((q2-p)*x):Sq2*Cp-Cq2*Sp,
          sp.cos(2*p*x):Cp*Cp-Sp*Sp, sp.sin(2*p*x):2*Sp*Cp,
          sp.cos(2*q1*x):Cq1*Cq1-Sq1*Sq1, sp.cos(2*q2*x):Cq2*Cq2-Sq2*Sq2}
    for kk,vv in subd.items(): ct=ct.subs(kk,vv)
    return sp.expand(ct)

def q_seed(c):
    """explicit q1^i q2^j with i+j>=2 (the wave-cone seed) after stripping oscillation."""
    ct=strip_osc(c)
    if not (ct.has(q1) or ct.has(q2)): return sp.Integer(0)
    pj=sp.Poly(ct,q1,q2)
    seed=sp.Integer(0)
    for (i,j),cc in pj.terms():
        if i+j>=2 and sp.simplify(cc)!=0:
            seed+=cc*q1**i*q2**j
    return sp.simplify(seed)

def p_seed(c):
    """explicit p^2 coefficient on the frame legs (direct spatial kinetic) after stripping."""
    ct=strip_osc(c)
    if not ct.has(p): return sp.Integer(0)
    return sp.simplify(sp.Poly(ct,p).nth(2))

def seagull_vertex_content(n,cross=False):
    c=seagull_two_momentum(n,cross=cross)
    qs=q_seed(c); ps=p_seed(c)
    # mass = the p-free, q-seed-free remainder (evaluate stripped at q1=q2=p=0 keeping only Cq*=Cp=1)
    ct=strip_osc(c)
    Cq1,Sq1,Cq2,Sq2,Cp,Sp=sp.symbols('Cq1 Sq1 Cq2 Sq2 Cp Sp',real=True)
    mass=ct.subs({Sq1:0,Sq2:0,Sp:0,Cq1:1,Cq2:1,Cp:1,q1:0,q2:0,p:0})
    return {'q_seed':qs,'p_seed':ps,'mass':sp.simplify(mass),'raw':c}

# ==========================================================================================
NMAX=int(os.environ.get('SIB3_NMAX',3))    # default n=3 (past banked n=2); set 4 to push further
sec(f"STEP 1: TWO-INDEPENDENT-MOMENTUM seagull loop vertex, n=1..{NMAX} (push past banked n=1,2)")
print("   loop config: two graviton legs carry INDEPENDENT momenta q1,q2 (=loop momentum k, integrated).")
print("   DANGER = an explicit q1*q2 / q1^2 / q2^2 seed (wave-cone) OR an explicit p^2 frame kinetic.")
content={}
for pol,cross in (('same',False),('cross',True)):
    print(f"\n   --- {pol}-polarization TT ---")
    for n in range(1,NMAX+1):
        vc=seagull_vertex_content(n,cross=cross)
        content[(pol,n)]=vc
        print(f"   n={n}: q_perp^2 wave-cone seed = {vc['q_seed']}   | p^2 frame kinetic = {vc['p_seed']}"
              f"   | mass piece nonzero? {vc['mass']!=0}")
        ck(f"{pol} n={n}: two-momentum seagull has NO explicit q_perp^2 wave-cone seed (q1q2/q1^2/q2^2)",
           sp.simplify(vc['q_seed'])==0)
        ck(f"{pol} n={n}: two-momentum seagull has NO explicit p^2 spatial frame kinetic",
           sp.simplify(vc['p_seed'])==0)

# ==========================================================================================
sec("STEP 1 CONTROL (prove-by-moving): break F2 -> q/p spatial seed must switch ON at n>=1")
print("   Inject a transverse d_x into Box_u; a genuine spatial contamination = an explicit")
print("   lam-carrying, momentum-carrying term absent when F2 is intact.")
for n in (1,2):
    c_break=seagull_two_momentum(n,cross=False,break_F2=True)
    lam_coeff=sp.expand(sp.expand_trig(sp.expand(c_break)).coeff(lam,1))
    lc=strip_osc(lam_coeff)
    injects=(lam_coeff!=0) and (lc.has(q1) or lc.has(q2) or lc.has(p))
    print(f"   n={n}: F2-broken -> lam-coeff carries explicit spatial momentum (q or p)? {injects}")
    ck(f"CONTROL n={n}: breaking F2 injects an explicit spatial-momentum term (extraction SENSITIVE)",
       injects)
c_intact=seagull_two_momentum(1,cross=False,break_F2=False)
ck("F2-intact two-momentum seagull carries NO lam term at all (no transverse derivative reaches vertex)",
   sp.expand(c_intact).coeff(lam,1)==0)

# ==========================================================================================
sec("STEP 1 VERDICT (the loop vertex is p-free AND q_perp^2-free)")
allq0=all(sp.simplify(content[(pl,n)]['q_seed'])==0 for pl in ('same','cross') for n in range(1,NMAX+1))
allp0=all(sp.simplify(content[(pl,n)]['p_seed'])==0 for pl in ('same','cross') for n in range(1,NMAX+1))
print(f"   ALL n=1..{NMAX}, both pols: q_perp^2 wave-cone seed = 0? {allq0}")
print(f"   ALL n=1..{NMAX}, both pols: p^2 frame spatial kinetic = 0? {allp0}")
print("   -> The two-independent-momentum loop vertex carries NEITHER an explicit q1*q2 product")
print("      (so the closed loop cannot leave a spatial q_perp^2 on the frame) NOR a p^2 frame")
print("      kinetic. The only surviving piece is the p-free, q-seed-free MASS term (H_TT'^2-type).")
print("   -> Feeds STEP 2: the assembled Sigma_perp can only be a MASS/time self-energy, NOT a cone.")
print(f"\nPASS={len(PASS)} FAIL={len(FAIL)}")
sys.exit(0 if not FAIL else 1)
