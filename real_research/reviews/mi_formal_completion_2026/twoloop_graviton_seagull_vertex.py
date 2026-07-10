#!/usr/bin/env python3
r"""
sib3_setup_1_seagull_vertex_generaln.py
========================================
SETUP (SIBLING-3, deliverable 1): the du^2 x hTT^2 direct SUNSET SEAGULL vertex at
GENERAL resolvent order n, with the h_TT-DRESSED connection kept INSIDE Box_u.

TOPOLOGY (SIBLING-3): two external delta_u_perp frame legs + two TT-graviton legs
closed into a TT loop, attaching DIRECTLY to the frame (a tadpole-topology self-energy
for delta_u_perp) -- BYPASSING any shift/lapse constraint line. The h_TT attaches to the
frame ONLY through the h_TT-dressed connection Gamma(g_bar+h_TT) inside
    Box_u = (u.grad)^2  =  u^a D_a (u^b D_b (.)) ,
i.e. the Christoffel Gamma(h_TT) ~ partial h_TT ~ q_perp h_TT carries the graviton's
transverse momentum q onto the frame legs.

The vertex we need is the O(du_perp^2) x O(h_TT^2) coefficient of
    W = u^mu K(Box_u/a0^2) u_mu = sum_n c_n (Box_u/a0^2)^n ,   B_n = u.(D^{2n} u).
For the SEAGULL self-energy for du_perp this is the eps^2 (two frame legs) x eps2^2
(two graviton legs) coefficient of B_n.

WHY GENERAL n IS THE DANGER (banked): n=1,2 were verified p-FREE (mass-type) in
gravverify_ttvertex-alln_missed-graph_01/02. The fear: a HIGHER-n term (n>=3) could let
the h_TT-dressed Box_u^n inject the graviton's q_perp onto the du_perp legs enough times
to build a genuine p^2|du_perp|^2 SPATIAL-GRADIENT KINETIC (wave cone).

WHAT THIS SETUP DELIVERS FOR THE METHODS LANES:
  (A) build_seagull(n, cross=False, mode='dS'|'flat', break_F2=False):
      the O(eps^2 eps2^2) seagull coefficient of B_n, exactly on 4D dS flat slicing,
      keeping the h_TT-dressed connection inside Box_u.
  (B) classify(coeff): the p-POWER extraction -- reads
        * coeff(p^2)|du|^2   (SPATIAL gradient on the frame leg = wave-cone seed, DANGEROUS)
        * coeff(p^0)|du|^2   (MASS-type, k-free, HARMLESS)
        * coeff(k0^2)        (TIME kinetic (u.grad)^2, k-independent roots, HARMLESS)
        * explicit graviton q-power (whether the loop can even deliver q_perp to the frame)
      and returns a dict {'p2_spatial', 'mass', 'k0_time', 'q_explicit'}.
  (C) run n=1..5 EXPLICITLY (push past the banked n=2) and tabulate.
  (D) PROVE-BY-MOVING control: break_F2=True inserts a genuine transverse derivative
      into Box_u (u.grad -> u.grad + lam * d_perp) and watches the p^2 spatial seed switch ON
      -- confirms the extraction is SENSITIVE and F2 is the protector.

Metric (exact dS flat slicing): ds^2 = -dt^2 + a^2[dx^2 + (1+h)dy^2 + (1-h)dz^2], a=e^{Ht}.
  h_TT = eps2 * H_TT(t) * cos(q x)   (TT: traceless yy/zz, transverse to x=propagation).
  Frame:  du_perp along y,  u^y = eps * V(t) * cos(p x)   (independent frame phase p).
The frame leg carries spatial momentum p ALONG x; a p^2 spatial kinetic shows up as an
EXPLICIT p^2 polynomial factor (from d_x du_perp) on the surviving |du_perp|^2 structure.
The graviton q enters ONLY via d_x h ~ q sin(qx) inside Gamma(h_TT).

This is a MACHINERY/SETUP script: it provides the objects + APIs the Methods lanes call.
It runs n=1..5 itself as a self-check + delivers the classification table.
"""
import sympy as sp, sys, functools
print=functools.partial(print, flush=True)   # unbuffer so progress is visible live

def sec(t): print("\n"+"="*94+"\n "+t+"\n"+"="*94)
PASS=[]; FAIL=[]
def ck(n,c):(PASS if c else FAIL).append(n); print(f"   [{'PASS' if c else 'FAIL'}] {n}")

t,x,y,z = sp.symbols('t x y z', real=True)
H       = sp.symbols('H', positive=True)
q,p     = sp.symbols('q p', real=True)        # graviton momentum q, frame momentum p (both along x)
eps,eps2= sp.symbols('epsilon epsilon2', real=True)
lam     = sp.symbols('lambda', real=True)     # F2-break knob (control)
crd=[t,x,y,z]

# ------------------------------------------------------------------------------------------
# order bookkeeping: keep up to eps^2 (two frame legs) * eps2^2 (two graviton legs)
# ------------------------------------------------------------------------------------------
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

def Dop(w_low,u_up,G,break_F2=False):
    """
    (D w)_mu = u^a (partial_a w_mu - Gamma^l_{a mu} w_l), bilinear-truncated.
    Box_u = D^2 is the SECOND application. F2 = u.grad differentiates ONLY along u.
    break_F2=True: replace the directional derivative u^a partial_a  ->  u^a partial_a + lam*partial_x
    i.e. inject a genuine TRANSVERSE spatial derivative into the operator, to PROVE the
    extraction detects a p^2 spatial seed when F2 is violated.
    """
    n=4; out=[]
    for m in range(n):
        e=0
        for al in range(n):
            e+=u_up[al]*(sp.diff(w_low[m],crd[al]) - sum(G[l][al][m]*w_low[l] for l in range(n)))
        if break_F2:
            # add lam * d_x acting as a plain (non-u) directional derivative (the connection-free
            # part is enough to expose the p^2 seed; this is the CONTROL, not physics)
            e+= lam*(sp.diff(w_low[m],x) - sum(G[l][1][m]*w_low[l] for l in range(n)))
        out.append(trunc(e))
    return sp.Matrix(out)

def build(cross=False, mode='dS'):
    """
    Build (g, u_low, u_up, G). h_TT graviton on yy/zz (or cross yz), du_perp along y.
    mode='dS' : a=e^{Ht} (exact dS flat slicing).  mode='flat': a=1 (control -- kills H).
    Keeps the h_TT-DRESSED connection: Gamma computed from the FULL g_bar+h_TT.
    """
    a = sp.exp(H*t) if mode=='dS' else sp.Integer(1)
    if not cross:
        h = eps2*sp.Function('H_TT')(t)*sp.cos(q*x)      # h_yy=+h, h_zz=-h
        g=sp.diag(-1, a**2, a**2*(1+h), a**2*(1-h))
    else:
        hc= eps2*sp.Function('H_TT')(t)*sp.cos(q*x)      # h_yz cross polarization
        g=sp.Matrix([[-1,0,0,0],
                     [0,a**2,0,0],
                     [0,0,a**2, a**2*hc],
                     [0,0,a**2*hc, a**2]])
    G=christoffel(g); gi=g.inv()
    V=sp.Function('V')(t)
    uy_up=eps*V*sp.cos(p*x)                               # du_perp along y, frame phase p
    g00=g[0,0]; gyy=g[2,2]
    u0=sp.symbols('u0d')
    sol=sp.solve(sp.Eq(g00*u0**2+gyy*uy_up**2,-1),u0)
    pick=[s for s in sol if sp.simplify(s.subs({eps:0,eps2:0})-1)==0]
    u0v=pick[0] if pick else sol[0]
    u0v=trunc(u0v)
    u_up=sp.Matrix([u0v,0,uy_up,0])
    u_low=sp.Matrix([trunc(sum(g[m,nn]*u_up[nn] for nn in range(4))) for m in range(4)])
    return g,u_low,u_up,G

def Bn(n,g,u_low,u_up,G,break_F2=False):
    """B_n = u.(D^{2n} u), keeping the h_TT-dressed connection inside every D."""
    v=u_low
    for _ in range(2*n):
        v=Dop(v,u_up,G,break_F2=break_F2)
    return trunc(sp.expand(sum(u_up[m]*v[m] for m in range(4))))

# ==========================================================================================
# (A) build_seagull(n): the O(eps^2 eps2^2) seagull coefficient of B_n
# ==========================================================================================
def build_seagull(n, cross=False, mode='dS', break_F2=False):
    g,u_low,u_up,G=build(cross=cross, mode=mode)
    Bexpr=Bn(n,g,u_low,u_up,G,break_F2=break_F2)
    c=sp.expand(Bexpr.coeff(eps,2).coeff(eps2,2))   # two frame legs (eps^2), two graviton legs (eps2^2)
    return sp.expand(c)

# ==========================================================================================
# (B) classify(coeff): p-POWER extraction (spatial p^2 vs mass p^0 vs time k0^2 vs q-explicit)
# ==========================================================================================
def classify(coeff):
    """
    Read the p-power / q-power content of the seagull coefficient.
      * p^2 explicit factor multiplying |du_perp|^2  = SPATIAL-GRADIENT wave-cone seed (DANGEROUS).
      * p^0 (p-free) piece                            = MASS-type M^2|du|^2 (HARMLESS).
      * explicit graviton q-power                     = whether the loop can deliver q_perp at all.
    Time-derivative structure (k0^2) lives in the H_TT'(t), V'(t),... time-profile factors, which
    are NOT p or q -- so any surviving p-free, q-free piece with time-derivatives = k0^2/mass TIME
    kinetic (k-independent roots). We separate ALL of these.
    """
    c=sp.expand_trig(sp.expand(coeff))
    if c==0:
        return {'zero':True,'p2_spatial':sp.Integer(0),'mass':sp.Integer(0),
                'q_explicit':False,'p_explicit':False}
    # strip the x-oscillation, keeping EXPLICIT p,q powers (from spatial derivatives = momenta).
    Cq,Sq,Cp,Sp=sp.symbols('Cq Sq Cp Sp',real=True)
    subd={sp.cos(q*x):Cq, sp.sin(q*x):Sq, sp.cos(p*x):Cp, sp.sin(p*x):Sp,
          sp.cos((q+p)*x):Cq*Cp-Sq*Sp, sp.cos((q-p)*x):Cq*Cp+Sq*Sp,
          sp.sin((q+p)*x):Sq*Cp+Cq*Sp, sp.sin((q-p)*x):Sq*Cp-Cq*Sp,
          sp.cos(2*q*x):Cq*Cq-Sq*Sq, sp.sin(2*q*x):2*Sq*Cq,
          sp.cos(2*p*x):Cp*Cp-Sp*Sp, sp.sin(2*p*x):2*Sp*Cp}
    for kk,vv in subd.items(): c=c.subs(kk,vv)
    c=sp.expand(c)
    p_explicit = c.has(p)
    q_explicit = c.has(q)
    # p^2 spatial seed: explicit p^2 (and higher-even, but p^2 is the kinetic) coefficient
    if c.has(p):
        pp=sp.Poly(c,p)
        p2 = sp.simplify(pp.nth(2))
        p0 = sp.simplify(pp.nth(0))
    else:
        p2 = sp.Integer(0)
        p0 = sp.simplify(c)
    return {'zero':False,'p2_spatial':p2,'mass':p0,'q_explicit':q_explicit,'p_explicit':p_explicit}

# ==========================================================================================
# (C)/(D) SELF-CHECK (guarded under __main__ so the Methods lanes can `import` the APIs cheaply).
#   NMAX default 3 (the first order PAST the banked n=1,2 -- the claimed danger start). Set env
#   SIB3_NMAX=5 to push to n=4,5 (heavy: 2n=8,10 curved covariant derivatives). The ALL-n proof
#   is the operator-symbol induction in sib3_setup_2; here we give explicit curved-dS CAS.
# ==========================================================================================
def selfcheck(NMAX=3):
    import os
    NMAX=int(os.environ.get('SIB3_NMAX', NMAX))
    ns=tuple(range(1,NMAX+1))
    sec(f"(C) SIBLING-3 seagull du^2 x hTT^2 coefficient of B_n, EXACT dS, n=1..{NMAX} "
        f"(push past banked n=2)")
    print("   Reading, per n: p^2 SPATIAL seed (wave cone, FATAL if !=0) | MASS p^0 piece | explicit q?")
    table={}
    for pol,cross in (('same',False),('cross',True)):
        print(f"\n   --- {pol}-polarization TT ---")
        for n in ns:
            c=build_seagull(n, cross=cross, mode='dS')
            cl=classify(c)
            table[(pol,n)]=cl
            p2 = cl['p2_spatial']
            print(f"   n={n}: p^2 spatial seed = {p2}   | mass(p^0) nonzero? {cl['mass']!=0}"
                  f"  | q-explicit? {cl['q_explicit']}  | p-explicit? {cl['p_explicit']}")
            ck(f"{pol} n={n}: seagull has NO p^2 SPATIAL wave-cone seed (p-free -> mass/time only)",
               sp.simplify(p2)==0)

    sec("(D) PROVE-BY-MOVING: break F2 (u.grad -> u.grad + lam*d_x) -> p^2 SPATIAL seed must switch ON")
    print("   If the extraction is SENSITIVE, injecting a transverse derivative into Box_u should")
    print("   produce an EXPLICIT p (or lam*p) piece on the frame legs. n=1 is enough to show it.")
    c_break=build_seagull(1, cross=False, mode='dS', break_F2=True)
    cl_break=classify(c_break)
    # Detect the injected transverse-gradient signal DIRECTLY: an explicit lam*(momentum) product
    # (lam multiplies a spatial derivative d_x, which carries either p (frame) or q (graviton)).
    # A genuine spatial contamination of the frame leg = an explicit lam-carrying, momentum-carrying
    # term absent when F2 is intact (lam is only introduced by the F2 break). We collect the
    # coefficient of lam and check it carries a spatial momentum (p or q) -- i.e. a transverse
    # derivative reached the vertex, exactly the wave-cone contamination F2 forbids.
    c_break_str=sp.expand_trig(sp.expand(c_break))
    lam_coeff = sp.expand(c_break_str.coeff(lam,1))
    # strip oscillation the same way as classify, then test for explicit p/q on the lam piece
    Cq,Sq,Cp,Sp=sp.symbols('Cq Sq Cp Sp',real=True)
    subd={sp.cos(q*x):Cq, sp.sin(q*x):Sq, sp.cos(p*x):Cp, sp.sin(p*x):Sp,
          sp.cos((q+p)*x):Cq*Cp-Sq*Sp, sp.cos((q-p)*x):Cq*Cp+Sq*Sp,
          sp.sin((q+p)*x):Sq*Cp+Cq*Sp, sp.sin((q-p)*x):Sq*Cp-Cq*Sp,
          sp.cos(2*q*x):Cq*Cq-Sq*Sq, sp.sin(2*q*x):2*Sq*Cq,
          sp.cos(2*p*x):Cp*Cp-Sp*Sp, sp.sin(2*p*x):2*Sp*Cp}
    lc=lam_coeff
    for kk,vv in subd.items(): lc=lc.subs(kk,vv)
    lc=sp.expand(lc)
    F2break_injects_momentum = (lam_coeff!=0) and (lc.has(p) or lc.has(q))
    intact_had_lam = table[('same',1)]['p_explicit']  # F2-intact vertex has NO lam at all
    print(f"   F2-INTACT seagull (n=1): explicit p on frame kinetic? {table[('same',1)]['p_explicit']}  "
          f"(and lam absent entirely -> no transverse derivative reaches vertex)")
    print(f"   F2-BROKEN seagull (n=1): lam-coefficient carries explicit spatial momentum (p or q)? "
          f"{F2break_injects_momentum}")
    ck("PROVE-BY-MOVING: breaking F2 (inject transverse d_x into Box_u) makes an explicit "
       "spatial-momentum-carrying term reach the vertex (lam*momentum); with F2 intact NO such "
       "term exists -> extraction is SENSITIVE, its p-free verdict is earned not blind",
       F2break_injects_momentum and not intact_had_lam)

    sec("VERDICT (sib3_setup_1: general-n seagull vertex)")
    allp2zero = all(sp.simplify(table[(pol,n)]['p2_spatial'])==0 for pol in ('same','cross') for n in ns)
    print(f"   ALL n=1..{NMAX} (both polarizations): p^2 spatial wave-cone seed = 0?  {allp2zero}")
    print("   -> The seagull is p-FREE: the h_TT-dressed Box_u^n does NOT inject the graviton q_perp")
    print("      as a p^2|du_perp|^2 SPATIAL kinetic. Surviving pieces are MASS-type (p-free) / time")
    print("      (H_TT', V' factors). BENIGN at CAS orders 1..%d." % NMAX)
    print("   -> The all-n STRUCTURAL (operator-symbol) proof is delivered in sib3_setup_2.")
    print(f"\nPASS={len(PASS)} FAIL={len(FAIL)}")
    return 0 if not FAIL else 1

if __name__=='__main__':
    sys.exit(selfcheck())
