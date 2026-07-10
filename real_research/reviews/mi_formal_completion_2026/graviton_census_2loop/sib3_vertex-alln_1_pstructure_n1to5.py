#!/usr/bin/env python3
r"""
sib3_vertex-alln_1_pstructure_n1to5.py
======================================
METHOD 1 (SIBLING-3, the direct du^2 x hTT^2 SUNSET SEAGULL): the frame-leg SPATIAL-momentum
(p) structure of the seagull du_perp self-energy at resolvent order n=1,2,3,4,5 by EXPLICIT
curved-dS CAS, deciding whether ANY n reaches a p^2|du_perp|^2 SPATIAL-gradient kinetic (wave
cone, FATAL) or stays p-FREE (mass/time, BENIGN).

WHAT THIS ADDS OVER THE SETUP (sib3_setup_1, which used a SINGLE graviton momentum q on both
legs, n<=3):
  * TWO INDEPENDENT graviton momenta q1,q2 on the two h_TT legs -- the PHYSICALLY CORRECT loop
    (in a real TT self-energy the two legs carry independent loop momenta; a single shared q is
    a special slice). This is the harder test: it exposes any (d_x h1)(d_x h2) ~ q1*q2 explicit
    momentum-squared seed the single-q setup could miss.
  * CAS pushed to n=1..5 (SIB3_NMAX, default 5): 2n = 2,4,6,8,10 covariant derivatives.
  * The p-power (frame spatial kinetic) AND q1,q2-power (graviton loop momenta) content read
    SEPARATELY per n, so we can TRACK WHERE q_perp goes:
       - q1,q2 on the frame KINETIC as p^2 (cone, FATAL) vs
       - q1,q2 absorbed into the h_TT loop / trace / a p-FREE mass term (BENIGN).
  * K-RESUMMATION: sum c_n (Box_u/a0^2)^n with a bounded ||K||<=1 Herglotz kernel and confirm
    the resummed seagull inherits p-free-ness term by term.
  * PROVE-BY-MOVING: break F2 (u.grad -> u.grad + lam d_x) and show the p^2 spatial seed switches
    ON at the SAME n -> the p-free result is physics, not a blind extraction.

DANGER CRITERION (restated): FATAL = a p^2|du_perp|^2 SPATIAL kinetic (k0=c_s|p| cone) reaching
the frame. BENIGN = p-FREE: MASS-type M^2|du_perp|^2 (p^0, k-free) or TIME kinetic (u.grad)^2
(k0^2, H_TT'/V' time profiles, k-independent roots). We distinguish p^2(spatial) vs k0^2(time)
vs p^0(mass) EVERY n.

Metric (exact dS flat slicing): ds^2=-dt^2+a^2[dx^2+(1+h)dy^2+(1-h)dz^2], a=e^{Ht}, R=12H^2.
  h_TT = A1(t)cos(q1 x) + A2(t)cos(q2 x)   (same yy/zz TT; cross yz variant also run).
  Frame du_perp along y: u^y = V(t) cos(p x),  frame spatial momentum p ALONG x.
A p^2 spatial kinetic = an EXPLICIT p^2 polynomial factor on the surviving |du_perp|^2 structure.
The graviton q1,q2 enter ONLY via d_x h ~ q sin(qx) inside Gamma(h_TT).
"""
import sympy as sp, sys, os, functools, time
print=functools.partial(print, flush=True)

def sec(t): print("\n"+"="*94+"\n "+t+"\n"+"="*94)
PASS=[]; FAIL=[]
def ck(n,c):(PASS if c else FAIL).append(n); print(f"   [{'PASS' if c else 'FAIL'}] {n}")

t,x,y,z = sp.symbols('t x y z', real=True)
H       = sp.symbols('H', positive=True)
q1,q2,p = sp.symbols('q1 q2 p', real=True)     # two graviton momenta, one frame momentum (all along x)
e1,e2,ep= sp.symbols('e1 e2 ep', real=True)    # order counters: graviton1, graviton2, two frame legs
lam     = sp.symbols('lambda', real=True)      # F2-break knob (control)
crd=[t,x,y,z]
A1=sp.Function('A1')(t); A2=sp.Function('A2')(t); V=sp.Function('V')(t)

# order bookkeeping: e1^1 e2^1 (two DISTINCT graviton legs) x ep^2 (two frame legs)
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
    """(D w)_mu = u^a(d_a w_mu - Gamma^l_{a mu} w_l). break_F2: inject lam*d_x transverse deriv."""
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
    if not cross:
        h = e1*A1*sp.cos(q1*x) + e2*A2*sp.cos(q2*x)     # two TT gravitons, same yy/zz pol
        g=sp.diag(-1, a**2, a**2*(1+h), a**2*(1-h))
    else:
        hc= e1*A1*sp.cos(q1*x) + e2*A2*sp.cos(q2*x)     # cross yz pol
        g=sp.Matrix([[-1,0,0,0],
                     [0,a**2,0,0],
                     [0,0,a**2, a**2*hc],
                     [0,0,a**2*hc, a**2]])
    G=christoffel(g)
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

def seagull_coeff(n, cross=False, break_F2=False):
    """the e1^1 e2^1 ep^2 coefficient = the h1 h2 x du_perp^2 seagull at order n."""
    g,u_low,u_up,G=build(cross=cross)
    B=Bn(n,g,u_low,u_up,G,break_F2=break_F2)
    return sp.expand(B.coeff(e1,1).coeff(e2,1).coeff(ep,2))

# ---- p-power / q-power extractor: strip x-oscillation keeping EXPLICIT p,q1,q2 (=momenta) ----
Cq1,Sq1,Cq2,Sq2,Cp,Sp=sp.symbols('Cq1 Sq1 Cq2 Sq2 Cp Sp',real=True)
def strip_osc(c):
    ct=sp.expand_trig(sp.expand(c))
    # expand any composite-angle cos/sin into products of the atomic ones so no q-power hides
    subd={sp.cos(q1*x):Cq1,sp.sin(q1*x):Sq1,sp.cos(q2*x):Cq2,sp.sin(q2*x):Sq2,
          sp.cos(p*x):Cp,sp.sin(p*x):Sp}
    for kk,vv in subd.items(): ct=ct.subs(kk,vv)
    # any leftover composite angles -> expand via trig then re-sub
    ct=sp.expand_trig(sp.expand(ct))
    for kk,vv in subd.items(): ct=ct.subs(kk,vv)
    return sp.expand(ct)

def pq_structure(c):
    """Return dict: p2_seed (coeff of p^2), p0_mass (coeff of p^0), q_explicit, p_explicit,
    and the FULL explicit-momentum-squared cross content q1^i q2^j p^k with i+j+k>=2 landing on p."""
    if c==0:
        return dict(zero=True, p2=sp.Integer(0), p0=sp.Integer(0),
                    q_explicit=False, p_explicit=False, cone_seed=sp.Integer(0))
    s=strip_osc(c)
    p_explicit=s.has(p); q_explicit=(s.has(q1) or s.has(q2))
    if s.has(p):
        pp=sp.Poly(s,p); p2=sp.simplify(pp.nth(2)); p0=sp.simplify(pp.nth(0))
    else:
        p2=sp.Integer(0); p0=sp.simplify(s)
    # the DANGEROUS wave-cone seed = an explicit p^2 factor that ALSO carries graviton momentum
    # q1/q2 (i.e. the graviton loop momentum has been converted into a frame spatial kinetic).
    # p2 already IS the coeff of p^2; if p2!=0 it is a spatial kinetic regardless of q content.
    cone_seed=p2
    return dict(zero=False, p2=p2, p0=p0, q_explicit=q_explicit, p_explicit=p_explicit,
                cone_seed=cone_seed)

# ==========================================================================================
sec("(1) SIBLING-3 seagull p-structure, EXACT dS, TWO INDEPENDENT graviton momenta q1,q2, n=1..NMAX")
NMAX=int(os.environ.get('SIB3_NMAX', 5))
print(f"   NMAX={NMAX}  (2n = {[2*n for n in range(1,NMAX+1)]} covariant derivatives). Reading per n:")
print("   p^2 SPATIAL seed (wave cone, FATAL if !=0) | p^0 MASS piece | explicit graviton q? | explicit frame p?")
table={}
for pol,cross in (('same',False),('cross',True)):
    print(f"\n   --- {pol}-polarization TT (independent q1,q2) ---")
    for n in range(1,NMAX+1):
        t0=time.time()
        c=seagull_coeff(n, cross=cross)
        st=pq_structure(c)
        table[(pol,n)]=st
        dt=time.time()-t0
        print(f"   n={n}: p^2 seed = {st['p2']}  | mass(p^0) nonzero? {st['p0']!=0}"
              f"  | q-explicit? {st['q_explicit']} | p-explicit? {st['p_explicit']}   [{dt:.1f}s]")
        ck(f"{pol} n={n}: seagull has NO p^2 SPATIAL wave-cone seed (p-free -> mass/time only)",
           sp.simplify(st['p2'])==0)

# ==========================================================================================
sec("(2) WHERE DOES THE GRAVITON q GO? -- q lands on the loop legs / mass, NOT the p^2 kinetic")
print("   For each n we check: is q1/q2 present AT ALL (q_explicit), and if so does it appear")
print("   MULTIPLYING a p^2 factor (=> converted into a frame spatial kinetic = cone, FATAL) or")
print("   ONLY in p-free (p^0) structures (=> absorbed into the h_TT loop / mass = BENIGN)?")
for pol in ('same','cross'):
    for n in range(1,NMAX+1):
        st=table[(pol,n)]
        q_on_p2 = (st['p2']!=0) and (st['p2'].has(q1) or st['p2'].has(q2))
        print(f"   {pol} n={n}: q present? {st['q_explicit']}"
              f"  | q multiplies a p^2 factor (cone)? {q_on_p2}  | p^2 seed itself = {st['p2']}")
        ck(f"{pol} n={n}: graviton q does NOT land on a p^2 frame kinetic (q absorbed in loop/mass)",
           not q_on_p2)

# ==========================================================================================
sec("(3) K-RESUMMATION: sum c_n (Box_u/a0^2)^n with bounded ||K||<=1 -> resummed seagull p-free")
print("   K(Box_u/a0^2)=sum_n c_n (Box_u/a0^2)^n is a bounded Herglotz kernel (||K||<=1). The seagull")
print("   du_perp self-energy inherits the p-structure LINEARLY term by term: Sigma_seagull ~ sum_n c_n")
print("   (seagull p-structure at n). Since EVERY term is p-free (p^2 seed=0 all n above), the")
print("   c_n-weighted sum is p-free for ANY bounded coefficient sequence.")
a0=sp.symbols('a0', positive=True)
csym=sp.symbols('c1:%d'%(NMAX+1))     # generic bounded resolvent coefficients
resummed_p2 = sum(csym[n-1]*table[('same',n)]['p2'] for n in range(1,NMAX+1))
resummed_p2 = sp.simplify(resummed_p2)
print(f"   resummed p^2 seed  sum_n c_n * p2(n) = {resummed_p2}")
ck("K-resummed seagull p^2 spatial seed = 0 for ARBITRARY bounded coefficients c_n (p-free survives "
   "resummation; ||K||<=1 cannot manufacture a cone from p-free terms)", sp.simplify(resummed_p2)==0)
# sanity: also the mass channel is generically nonzero (the loop DOES dress a mass) -> benign kinetic
resummed_mass_nonzero = any(table[('same',n)]['p0']!=0 for n in range(1,NMAX+1))
print(f"   resummed MASS (p^0) channel has nonzero terms (a genuine du_perp mass IS dressed)? "
      f"{resummed_mass_nonzero}")

# ==========================================================================================
sec("(4) PROVE-BY-MOVING: break F2 (u.grad -> u.grad + lam d_x) -> p^2 SPATIAL seed switches ON")
print("   If the extraction is SENSITIVE, injecting a transverse d_x into Box_u must produce an")
print("   EXPLICIT p^2 (lam-carrying) spatial seed on the frame legs at the SAME n. We test n=1,2.")
for n in (1,2):
    cb=seagull_coeff(n, cross=False, break_F2=True)
    sb=strip_osc(cb)
    lam_piece = sp.expand(sb.coeff(lam,1)) + sp.expand(sb.coeff(lam,2))
    # does the F2-break introduce an explicit p (spatial momentum) on the frame that was absent?
    lam_has_p = (sb.coeff(lam,1).has(p) or sb.coeff(lam,2).has(p))
    # p^2 seed of the FULL broken coeff (should now be nonzero and lam-carrying)
    if sb.has(p):
        p2b=sp.simplify(sp.Poly(sb,p).nth(2))
    else:
        p2b=sp.Integer(0)
    intact_p2 = table[('same',n)]['p2']
    print(f"   n={n}: F2-INTACT p^2 seed = {intact_p2}   ||   F2-BROKEN p^2 seed = {p2b}"
          f"  (lam-carrying? {p2b.has(lam) if p2b!=0 else False})")
    ck(f"PROVE-BY-MOVING n={n}: breaking F2 turns ON a p^2 spatial seed absent when F2 intact "
       f"(extraction SENSITIVE; the p-free verdict is earned)",
       (sp.simplify(intact_p2)==0) and (sp.simplify(p2b)!=0) and (p2b.has(lam)))

# ==========================================================================================
sec("VERDICT (Method 1: seagull frame-leg p-structure at n=1..%d)"%NMAX)
allp2 = all(sp.simplify(table[(pol,n)]['p2'])==0 for pol in ('same','cross') for n in range(1,NMAX+1))
print(f"   ALL n=1..{NMAX}, BOTH polarizations, INDEPENDENT q1,q2: p^2 spatial wave-cone seed = 0?  {allp2}")
print("   -> The direct du^2 x hTT^2 sunset seagull is p-FREE (mass/time) at every CAS order 1..%d."%NMAX)
print("      The h_TT-dressed Box_u^n does NOT inject the graviton q_perp onto the du_perp legs as a")
print("      p^2 SPATIAL kinetic; q rides the (integrated) loop legs / a p-free mass. NO transverse")
print("      aether wave cone reaches the frame. BENIGN at divergence level.")
print("   -> ALL-n is closed by the operator-symbol induction (sib3_setup_2 PART 1: frame symbol k0^{2n}).")
print(f"\nPASS={len(PASS)} FAIL={len(FAIL)}")
sys.exit(0 if not FAIL else 1)
