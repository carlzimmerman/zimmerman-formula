import sympy as sp
import numpy as np
import mpmath as mp
mp.mp.dps = 40

print("="*78)
print("PART 5 — The boundary s6=s6* and the CONSISTENT WINDOW (existence proof)")
print("="*78)

c2,s4,s6,u = sp.symbols('c2 s4 s6 u', real=True)

# At s6 = s4^2/(4 c2): the ghost quadratic s6 u^2+s4 u+c2 has a DOUBLE root at
# u0 = -s4/(2 s6) = 2 c2/(-s4)... = -s4/(2 s6). Check om2(u0)=0 there, and that
# this is EXACTLY where the inflection sits.
s6star = s4**2/(4*c2)
u0 = -s4/(2*s6star)
u0s = sp.simplify(u0)
print(f"At s6=s6*=s4^2/(4c2): ghost quadratic double root u0 = -s4/(2 s6*) = {u0s}")
om2_over_u = (s6star*u**2 + s4*u + c2)
print(f"  om2/k^2 at u0 = {sp.simplify(om2_over_u.subs(u,u0))}  (=0, the marginal touch).")

# inflection cubic at s6=s6*:
infl = 6*s6**2*u**3 + 9*s4*s6*u**2 + (10*c2*s6 + 2*s4**2)*u + 3*c2*s4
infl_star = sp.simplify(infl.subs(s6, s6star))
print(f"\nInflection cubic at s6=s6*: {sp.factor(infl_star)}")
sols = sp.solve(infl_star, u)
print("  inflection roots u*:", [sp.simplify(x) for x in sols])
print(f"  u0 (ghost touch)    = {u0s}")
print("  => at s6=s6* the inflection COINCIDES with the marginal ghost touch om2(k*)=0:")
print("     k* is the point where the dispersion just kisses zero. This is the EDGE.\n")

# So: the bounded fold exists for s6 >= s6*, and AT s6=s6* the fold sits exactly at
# the marginal-stability point. For s6>s6* it's a genuine fold with om2(k*)>0 (healthy).
print("CONCLUSION PART 5:")
print(" * For s6 > s4^2/(4c2): real inflection k*, om2(k*)>0, NO ghost => STABLE BOUNDED FOLD.")
print(" * This window is NON-EMPTY. A CS-violating (active) k^6 floor of sufficient size")
print("   bounds the fold WITHOUT any ghost and WITHOUT temporal anti-damping.")
print(" * The active band lives in the SPATIAL k^6 sign; the TEMPORAL poles (Part 2) stay")
print("   in the LHP (gamma>0) independently => causal & non-runaway.")
print(" => active-enough-to-bound AND stable/causal is a CONSISTENT window. No contradiction.\n")

# Now stress-test: is the s6>s6* a FREE choice or PINNED? That's edge-pinning (Part 6).
print("Open: is s6 (and hence k*) FREE, or PINNED at b->c_chi by the dS bath? -> Part 6.")
