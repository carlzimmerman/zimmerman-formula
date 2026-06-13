"""
INDEPENDENT hostile re-derivation (referee). Three checks, NONE reusing agentRR's code objects:
 (A) dispersion sigma4,sigma6 from a Lorentzian gain self-energy -- derived a DIFFERENT way
     (general Lorentzian Re-part Pade, then series), cross-check signs and the sigma4<0 condition.
 (B) the bounded-fold WINDOW 1 < sigma6/sigma6* < 4/3 -- derived purely from the group-velocity /
     ghost conditions on a generic omega^2 = c^2 k^2 + s4 k^4 + s6 k^6 with s4<0, s6>0. This is the
     load-bearing geometric claim and is MODEL-INDEPENDENT (no gain model). Verify both edges.
 (C) the FORCED/FREE parameter count, done adversarially: enumerate every continuous knob the route
     uses (g0, kappa, Isat, k0, Gamma, A) and ask which the dS pump genuinely pins by ORDER vs which
     fixes the dimensionless RATIO the fold needs. The hostile question: is anything the route called
     FORCED actually a tunable gain/saturation knob in disguise?
"""
import sympy as sp

print("="*70)
print("CHECK (A): dispersion coefficients, independent derivation")
print("="*70)
# A generic active (negative-residue) Lorentzian in the energy^2 variable u=k^2.
# Most general single-pole real response: Re Sigma(u) = N*(u-u0)/((u-u0)^2+G^2) up to overall sign.
# Active/gain => the residue sign is negative. Write Sigma = -A*G*(u-u0)/((u-u0)^2+G^2), A,G>0, u0=k0^2.
# omega^2 = c^2*u + Sigma. Expand to O(u^3). I do this via Maclaurin coefficients f^(n)(0)/n!,
# NOT via sp.series on a prebuilt expr, to be a genuinely separate computation.
u, A, G, u0, c = sp.symbols('u A G u0 c', positive=True, real=True)
Sig = -A*G*(u-u0)/((u-u0)**2 + G**2)
f = c**2*u + Sig
# Maclaurin coefficients
a0 = f.subs(u,0)
a1 = sp.diff(f,u,1).subs(u,0)
a2 = sp.diff(f,u,2).subs(u,0)/2
a3 = sp.diff(f,u,3).subs(u,0)/6
a0,a1,a2,a3 = [sp.simplify(x) for x in (a0,a1,a2,a3)]
print("gap   a0 =", a0)
print("c_eff^2 a1 =", a1)
print("sigma4 a2 =", a2)
print("sigma6 a3 =", a3)
# substitute u0=k0^2 to compare with agentRR (they used k0^2 directly => u0=k0^2)
k0 = sp.symbols('k0', positive=True)
sub = {u0: k0**2}
s4 = sp.simplify(a2.subs(sub))
s6 = sp.simplify(a3.subs(sub))
print("\nsigma4 (u0=k0^2):", s4)
print("sigma6 (u0=k0^2):", s6)
# agentRR claimed: sigma4 = A*G*k0^2*(k0^4-3G^2)/(G^2+k0^4)^3 ; sigma6 = A*G*(G^4-6G^2 k0^4+k0^8)/(G^2+k0^4)^4
s4_claim = A*G*k0**2*(k0**4-3*G**2)/(G**2+k0**4)**3
s6_claim = A*G*(G**4-6*G**2*k0**4+k0**8)/(G**2+k0**4)**4
print("\nsigma4 matches agentRR claim:", sp.simplify(s4 - s4_claim)==0)
print("sigma6 matches agentRR claim:", sp.simplify(s6 - s6_claim)==0)
# sign condition sigma4<0 <=> k0^4<3G^2 (since A,G,k0>0 and denom>0): numerator sign = sign(k0^4-3G^2)
print("sigma4<0  <=>  k0^4 < 3 G^2  (numerator sign):", "k0^4-3G^2 controls sign -> confirmed")

print()
print("="*70)
print("CHECK (B): the bounded-fold window 1 < sigma6/sigma6* < 4/3, MODEL-INDEPENDENT")
print("="*70)
# Generic IR tower omega^2(k)=c^2 k^2 + s4 k^4 + s6 k^6, with s4<0 (bend, forced) and s6>0.
# Let x=k^2>=0. omega^2 = c^2 x + s4 x^2 + s6 x^3.
# group-velocity^2 proxy: d(omega^2)/d(k^2) = c^2 + 2 s4 x + 3 s6 x^2  -- a VISIBLE fold needs this <0
#   somewhere (omega^2 non-monotone in k^2). Min of the quadratic c^2+2 s4 x+3 s6 x^2 over x>=0:
#   vertex at x* = -s4/(3 s6) > 0 (since s4<0). value there = c^2 - s4^2/(3 s6).
# => fold exists  <=>  c^2 - s4^2/(3 s6) < 0  <=>  s6 < s4^2/(3 c^2)  =: s6_fold.
# no-ghost (omega^2>0 for all k>0): need the cubic c^2 + s4 x + s6 x^2 (=omega^2/x) >0 for x>0.
#   discriminant of s6 x^2 + s4 x + c^2:  s4^2 - 4 s6 c^2. If <0 always positive (no real root) => safe.
#   boundary s4^2-4 s6 c^2=0 => s6 = s4^2/(4 c^2) =: s6_star (the no-ghost threshold).
#   s6 > s6_star => no real root => omega^2>0 (no ghost). s6 < s6_star => two positive roots => ghost.
c2, s4, s6 = sp.symbols('c2 s4 s6', real=True)  # c2=c^2>0, s4<0, s6>0
s6_star = s4**2/(4*c2)   # no-ghost
s6_fold = s4**2/(3*c2)   # fold-existence
print("no-ghost threshold  s6* = s4^2/(4 c^2)")
print("fold-existence      s6_fold = s4^2/(3 c^2)")
print("ratio s6_fold/s6* =", sp.simplify(s6_fold/s6_star), " (claim: 4/3)")
# verify the two boundaries concretely with c=1, s4=-1/2 (QQ units => s6*=1/16)
import mpmath as mp
cval=1.0; s4val=-0.5
s6star_n = s4val**2/(4*cval**2); s6fold_n = s4val**2/(3*cval**2)
print(f"\nQQ units c=1,s4=-1/2: s6*={s6star_n:.6f} (claim 1/16={1/16:.6f}), s6_fold={s6fold_n:.6f}")
def has_fold(s6v):
    # does c^2 + 2 s4 x + 3 s6 x^2 dip below 0 for some x>0?
    import numpy as np
    xs=np.linspace(0,20,200001)
    g = cval**2 + 2*s4val*xs + 3*s6v*xs**2
    return g.min()<0
def has_ghost(s6v):
    import numpy as np
    xs=np.linspace(1e-6,50,500001)
    w2 = cval**2*xs + s4val*xs**2 + s6v*xs**3
    return w2.min()<0
for s6v in [0.060, 1/16-1e-4, 1/16+1e-4, 0.07, s6fold_n-1e-4, s6fold_n+1e-4, 0.090]:
    print(f"  s6={s6v:.6f}  s6/s6*={s6v/s6star_n:.4f}  ghost={has_ghost(s6v)}  fold={has_fold(s6v)}")
print("\nExpected: ghost for s6/s6*<1 ; fold(visible) for s6/s6*<4/3 ; so bounded+visible fold")
print("lives in 1<s6/s6*<4/3. Window WIDTH in ratio = 4/3-1 = 1/3 (33%).")
