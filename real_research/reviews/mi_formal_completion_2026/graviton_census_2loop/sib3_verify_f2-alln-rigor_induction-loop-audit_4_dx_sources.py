#!/usr/bin/env python3
r"""AUDIT the induction's CORE claim: with F2 intact, the frame leg cos(p x) is NEVER
differentiated by d_x, so no p-polynomial (hence no p^2 cone) can ever appear on the frame
kinetic -- at ANY n. I make this a HARD structural check, not a hand-wave.

Dop = u^a(d_a w_m - Gamma^l_{a m} w_l). The ONLY spatial derivative d_x acts through:
   (i)  u^a d_a with a=x -> needs u^x != 0. But u^x IDENTICALLY 0 (F2). So no d_x from the
        directional part.
   (ii) Gamma^l_{a m} contains d_x g ~ d_x h(x) = -q sin(qx): this differentiates the GRAVITON
        phase, giving q, NOT p. It never touches cos(p x).
So the frame phase cos(p x) is only ever MULTIPLIED (as a spectator), never differentiated ->
p appears solely as the cos(p x)^2 PHASE, never as a p-polynomial momentum. A p^2 spatial cone
needs a p^2 POLYNOMIAL (from d_x^2 on cos p x) -> impossible with u^x=0.

I VERIFY this by tracking, symbolically, whether d_x EVER hits the frame phase across the whole
Dop string, using a TAGGED frame phase F(x) (an opaque function) and a TAGGED graviton phase.
If d/dx F(x) ever appears, the induction claim is FALSE. Then I BREAK F2 and confirm it appears.
"""
import sympy as sp, functools, importlib.util
print=functools.partial(print, flush=True)
spec=importlib.util.spec_from_file_location('s1','sib3_setup_1_seagull_vertex_generaln.py')
s1=importlib.util.module_from_spec(spec); spec.loader.exec_module(s1)
build=s1.build; trunc=s1.trunc; eps=s1.eps; eps2=s1.eps2; p=s1.p; q=s1.q
t,x,y,z=s1.t,s1.x,s1.y,s1.z; crd=[t,x,y,z]

g,u_low,u_up,G=build(cross=False, mode='dS')
print("u^x (must be 0 for the induction):", sp.simplify(u_up[1]))

# Replace the frame phase cos(p x) in u_low by an OPAQUE function F(x) so we can DETECT if any
# d_x hits it. We rebuild u with F(x) marking the frame leg.
F=sp.Function('F')  # opaque frame phase; d/dx F(x) = F'(x) is detectable
V=sp.Function('V')(t)
uy_up = eps*V*F(x)                 # frame leg with opaque phase
g00=g[0,0]; gyy=g[2,2]
u0=sp.symbols('u0d')
sol=sp.solve(sp.Eq(g00*u0**2+gyy*uy_up**2,-1),u0)
pick=[s for s in sol if sp.simplify(s.subs({eps:0,eps2:0})-1)==0]
u0v=trunc(pick[0])
u_up2=sp.Matrix([u0v,0,uy_up,0])
u_low2=sp.Matrix([trunc(sum(g[m,nn]*u_up2[nn] for nn in range(4))) for m in range(4)])

def Dop_tagged(w_low, break_F2=False):
    out=[]
    for m in range(4):
        e=0
        for al in range(4):
            e+=u_up2[al]*(sp.diff(w_low[m],crd[al]) - sum(G[l][al][m]*w_low[l] for l in range(4)))
        if break_F2:
            e+=sp.Symbol('lam')*(sp.diff(w_low[m],x) - sum(G[l][1][m]*w_low[l] for l in range(4)))
        out.append(trunc(e))
    return sp.Matrix(out)

def frame_phase_differentiated(n, break_F2=False):
    """Return True if F'(x) (d_x hitting the frame phase) EVER appears in B_n at eps^2 eps2^2."""
    v=u_low2
    for _ in range(2*n):
        v=Dop_tagged(v, break_F2=break_F2)
    B=trunc(sp.expand(sum(u_up2[m]*v[m] for m in range(4))))
    c=sp.expand(B.coeff(eps,2).coeff(eps2,2))
    # does the derivative of the opaque frame phase appear?
    hit = c.has(sp.Derivative(F(x),x)) or c.has(F(x).diff(x))
    return hit, c

print("\n=== F2 INTACT: does d_x EVER hit the frame phase F(x)? (must be False at all n) ===")
allclean=True
for n in (1,2,3):
    hit,c = frame_phase_differentiated(n, break_F2=False)
    allclean = allclean and (not hit)
    print(f"  n={n}: frame phase differentiated (F'(x) present)? {hit}   -> {'CLEAN (no p-momentum)' if not hit else 'CONTAMINATED'}")
print(f"  ALL n=1,2,3 clean (frame phase never differentiated under F2)? {allclean}")

print("\n=== F2 BROKEN (inject lam d_x): d_x MUST now hit the frame phase (sensitivity) ===")
for n in (1,2):
    hit,c = frame_phase_differentiated(n, break_F2=True)
    print(f"  n={n}: frame phase differentiated? {hit}  -> {'DETECTED (F2-break exposes p)' if hit else 'MISS'}")
