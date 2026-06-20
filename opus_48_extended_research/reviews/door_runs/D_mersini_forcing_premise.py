#!/usr/bin/env python3
"""
DOOR D -- premise audit (adversarial both-ways tail to D_mersini_forcing.py).

Two loose ends from the main run, checked head-on so the verdict is robust:

 (A) c_s^2 = dQ/(3dQ+2) is NEGATIVE only on -2/3 < dQ < 0 (i.e. 1/3 < Q < 1).
     For dQ < -2/3 (Q < 1/3) BOTH numerator and denominator are negative -> c_s^2 > 0.
     So there is a deep Q<1/3 corner with g'<0 AND c_s^2>0. Does that corner give MH's
     forced phantom class {g'<0, g''>0, c_s^2>0, rho>=0, w<=-1}?  Check w and rho there.

 (B) MH's actual PREMISE is *stable PHANTOM* dark energy: w <= -1.  The forcing only
     bites on a component that is genuinely phantom.  Where is w<=-1 on the framework's
     shape?  w = (X-1)/(3X+1).  Find the region w<=-1 and check whether ANY point has
     {g'<0, g''>0, c_s^2>0, rho>=0, w<=-1} simultaneously.  If NONE -> MH's premise is
     never met on the framework's shape -> the forcing is vacuous for this K(Q) and the
     framework's DE face (w=-1 exactly) is the BOUNDARY, not the interior MH forces.

Both-ways: if a stable-phantom corner DID exist on the framework's shape, that would be
a partial-FORCING (the shape is forced *there*); we test honestly.
"""
import sympy as sp
import numpy as np

mu, X = sp.symbols('mu X', positive=True)
g  = mu**2*(X-1)**2
g1 = sp.diff(g, X); g2 = sp.diff(g, X, 2)
p   = g
rho = 2*X*g1 - g
w   = sp.simplify(p/rho)               # (X-1)/(3X+1)
cs2 = sp.simplify(g1/(g1+2*X*g2))      # (X-1)/(3X-1)

print("="*86)
print("(A) THE DEEP Q<1/3 CORNER: is there g'<0 AND c_s^2>0 there, and is it phantom & rho>=0?")
print("="*86)
print("c_s^2 = (X-1)/(3X-1):  sign-flip at X=1/3 (denominator zero).")
print(f"{'Q':>7} {'dQ':>7} | {'g1':>8} {'cs2':>10} {'rho':>9} {'w':>10} | flags")
for Qv in [0.05, 0.1, 0.2, 0.30, 0.34, 0.4, 0.6, 0.9]:
    sub = {mu:1.0, X:Qv}
    g1v=float(g1.subs(sub)); cs2v=float(cs2.subs(sub)); rhov=float(rho.subs(sub)); wv=float(w.subs(sub))
    flags=[]
    flags.append("g'<0" if g1v<0 else "g'>=0")
    flags.append("cs2>0" if cs2v>0 else "cs2<0")
    flags.append("rho>=0" if rhov>=0 else "rho<0")
    flags.append("w<=-1" if wv<=-1 else "w>-1")
    print(f"{Qv:>7.3g} {Qv-1:>7.3g} | {g1v:>8.3g} {cs2v:>10.4g} {rhov:>9.4g} {wv:>10.4g} | {', '.join(flags)}")

print("\nNOTE: on the WHOLE Q<1 range, rho = mu^2(3X^2-2X-1) = mu^2(3X+1)(X-1) < 0 for 0<X<1")
print("   (factor (X-1)<0, (3X+1)>0) -> rho<0 EVERYWHERE on Q<1, so MH4 (rho>=0) FAILS on the")
print("   ENTIRE phantom side, INCLUDING the deep Q<1/3 c_s^2>0 corner. The corner is unphysical.")
# verify factorization
print("   sympy check rho =", sp.factor(rho), " -> zero at X=1 and X=-1/3; <0 on (−1/3,1).")

print("\n" + "="*86)
print("(B) WHERE IS THE FRAMEWORK PHANTOM (w<=-1)?  w=(X-1)/(3X+1)")
print("="*86)
sol = sp.solve(sp.Eq(w, -1), X)
print("w=-1  =>  X =", sol, "  (i.e. Q=1/2)")
# w<=-1 region:
wm1 = sp.simplify(w + 1)   # = (X-1)/(3X+1) + 1 = (4X)/(3X+1)
print("w+1 = (X-1)/(3X+1)+1 =", sp.simplify(wm1), " = 4X/(3X+1) > 0 for X>0")
print("   => w+1 > 0 for ALL X>0  =>  w > -1 EVERYWHERE on X>0.")
print("   The framework's shape has NO w<=-1 (phantom) region for physical X=Q>0 at all")
print("   EXCEPT the single boundary the additive -2Lambda supplies (the I0=0 cosmological")
print("   constant point, w=-1 exactly, NOT w<-1).")
# numeric confirm
xs=np.linspace(1e-4,5,50000); wnum=(xs-1)/(3*xs+1)
print(f"   numeric: min w over X in (0,5] = {wnum.min():.4f} at X={xs[np.argmin(wnum)]:.4f}"
      f"  (>-1: { -1 < wnum.min() })")
print(f"            max w = {wnum.max():.4f};  w in (-1, 1/3).  No w<=-1 anywhere.")

print("\n" + "="*86)
print("PREMISE VERDICT")
print("="*86)
print("MH's theorem forces {g'<0,g''>0,c_s^2>0,rho>=0} ONLY for a component that is a")
print("STABLE PHANTOM (w<=-1). On the framework's K(Q)=mu^2(Q-1)^2:")
print("  * w > -1 strictly for every physical Q>0 (w in (-1,1/3)) -> the framework's scalar")
print("    is NEVER phantom as a dynamical component; its DE face is w=-1 EXACTLY (I0=0),")
print("    the BOUNDARY of MH's domain, not its phantom interior.")
print("  * rho < 0 on the ENTIRE g'<0 (Q<1) side -> MH4 fails there; the deep c_s^2>0 corner")
print("    (Q<1/3) is rho<0 (unphysical), so no {g'<0,g''>0,c_s^2>0,rho>=0} point exists.")
print("  => MH's PREMISE (stable phantom) is NOT met on the framework's shape. The forcing")
print("     theorem is VACUOUS for this K(Q): it cannot force a shape for a component that")
print("     is not phantom. CONFIRMS the main-run verdict: PARTIAL/NOT-FORCED.")
print("     The framework's K(Q) is a ghost condensate by CONSTRUCTION (g''>0 minimum), but")
print("     the MH origin-theorem does NOT transmit a forcing to it (no phantom premise).")
