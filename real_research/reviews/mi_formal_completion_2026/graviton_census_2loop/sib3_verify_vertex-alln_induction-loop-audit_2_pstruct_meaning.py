#!/usr/bin/env python3
"""AUDIT 2: What does 'p^2 seed' actually measure here, and can the extractor SEE a spatial
kinetic given cos(px) parametrization? The frame leg u^y ~ V cos(px). A spatial kinetic
p^2|du|^2 in position space = (d_x du)^2 ~ (V p sin(px))^2 -> needs an EXPLICIT p from d_x.
The concern: strip_osc maps cos(px)^2 -> Cp^2 (p^0), losing the cos(2px) that a real d_x^2
would expose. Test: build a KNOWN p^2 spatial kinetic and see if pq_structure flags it."""
import sympy as sp, functools
print=functools.partial(print,flush=True)
t,x=sp.symbols('t x',real=True)
q1,q2,p,H=sp.symbols('q1 q2 p H',real=True)
Cq1,Sq1,Cq2,Sq2,Cp,Sp=sp.symbols('Cq1 Sq1 Cq2 Sq2 Cp Sp',real=True)
V=sp.Function('V')(t);A1=sp.Function('A1')(t);A2=sp.Function('A2')(t)
def strip_osc(c):
    ct=sp.expand_trig(sp.expand(c))
    subd={sp.cos(q1*x):Cq1,sp.sin(q1*x):Sq1,sp.cos(q2*x):Cq2,sp.sin(q2*x):Sq2,sp.cos(p*x):Cp,sp.sin(p*x):Sp}
    for kk,vv in subd.items(): ct=ct.subs(kk,vv)
    ct=sp.expand_trig(sp.expand(ct))
    for kk,vv in subd.items(): ct=ct.subs(kk,vv)
    return sp.expand(ct)
def pq_structure(c):
    s=strip_osc(c)
    if s.has(p):
        pp=sp.Poly(s,p);p2=sp.simplify(pp.nth(2));p0=sp.simplify(pp.nth(0))
    else: p2=sp.Integer(0);p0=sp.simplify(s)
    return dict(p2=p2,p0=p0,q=(s.has(q1) or s.has(q2)),pexp=s.has(p))

print("=== TEST A: a GENUINE spatial kinetic p^2 V^2 cos(px)^2 (the FATAL structure) ===")
# a real cone seed: (d_x du_perp)^2 with du_perp = V cos(px).  d_x -> -V p sin(px).
kinetic = (sp.diff(V*sp.cos(p*x),x))**2   # = V^2 p^2 sin(px)^2
print("genuine kinetic (d_x du)^2 =",sp.expand(kinetic))
print("pq_structure:",pq_structure(kinetic))
print("  -> does extractor flag p^2 seed?", pq_structure(kinetic)['p2']!=0)

print("\n=== TEST B: the ACTUAL n=1 seagull raw coeff ===")
sea1 = -2*V**2*sp.exp(2*H*t)*sp.cos(p*x)**2*sp.cos(q1*x)*sp.cos(q2*x)*sp.diff(A1,t)*sp.diff(A2,t)
print("pq_structure:",pq_structure(sea1))

print("\n=== TEST C: a MIXED graviton-gradient cone: V^2 cos(px)^2 * (d_x h1)(d_x h2) ===")
# if the graviton gradient reached the frame kinetic: q1 q2 sin(q1x) sin(q2x) with p^2 from frame
mixedcone = V**2 * (p*sp.sin(p*x))**2 * (q1*sp.sin(q1*x))*(q2*sp.sin(q2*x))*A1*A2
print("mixed cone (has p^2 AND q1 q2):",sp.expand(mixedcone))
print("pq_structure:",pq_structure(mixedcone))
print("  -> p^2 seed flagged?", pq_structure(mixedcone)['p2']!=0,
      " | q on p2?", (pq_structure(mixedcone)['p2'].has(q1) or pq_structure(mixedcone)['p2'].has(q2)) if pq_structure(mixedcone)['p2']!=0 else False)

print("\n=== TEST D: does cos(px)^2 hide a p^2? strip maps it to Cp^2 (p^0). Is that a HOLE? ===")
print("strip_osc(cos(px)^2) =",strip_osc(sp.cos(p*x)**2), " -> p-power:", sp.Poly(strip_osc(sp.cos(p*x)**2),p).degree() if strip_osc(sp.cos(p*x)**2).has(p) else 0)
print("NOTE: a physical p^2 kinetic ALWAYS carries an EXPLICIT p prefactor from d_x (p*sin(px)),")
print("NOT hidden inside cos(px)^2. The explicit-p extractor is the right probe IF every spatial")
print("derivative that acted produced an explicit p. Check: did any d_x act on the frame leg at n=1?")
