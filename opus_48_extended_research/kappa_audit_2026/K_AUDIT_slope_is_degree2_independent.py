#!/usr/bin/env python3
"""
K_AUDIT (result) -- kappa = 1/2 does NOT depend on the degree-2 joint.

The degree-2 deep dive (K_AUDIT_degree2_circularity.py) showed P4 is circular. This script shows
that circularity is HARMLESS to kappa: the deep-MOND slope mu'(0) -- the only quantity kappa needs
-- is independent of P3 (saturation) and P4 (degree-2), and of the completion shape. So kappa=1/2
does not rest on the circular premise; the degree-2 joint bears only on the full mu-SHAPE, which
the framework already treats as empirical (PD10).

Result: kappa = a0/s = 1/(2 cp), and the "2" is fixed by TWO premises only --
  (1) the source excites TWO channels (the metric's two static sectors; premise 1), and
  (2) one-channel exactness + symmetry (a single driven channel returns its own engagement),
with cp the measured zero mode (k01; cp = 1 to 0.33%). P3 and P4 never enter.

Run: python3 opus_48_extended_research/kappa_audit_2026/K_AUDIT_slope_is_degree2_independent.py  (sympy)
"""
import sympy as sp

Y, cp, c2, c3, k, a, b = sp.symbols('Y cp c2 c3 k a b', real=True)
print("="*90)
print("kappa = 1/(2 cp): the '2' is the channel count, robust to P3/P4 and to the completion")
print("="*90)

# a GENERAL per-channel completion (any shape), linear coefficient cp:
p = cp*Y + c2*Y**2 + c3*Y**3

def slope(Cfun, label):
    mu = Cfun(p, p)
    s = sp.simplify(sp.diff(mu, Y).subs(Y, 0))
    print(f"    {label:52s} mu'(0) = {s}")
    return s

print("\nCompositions tested (each symmetric + one-channel-exact C(p,0)=p; varying P3/P4 compliance):")
s1 = slope(lambda a, b: a + b - a*b,                      "OR (P4 ok):  p+q-pq")
s2 = slope(lambda a, b: a + b - a*b + k*a*b*(1-a)*(1-b),  "tower (P4 broken, any k): +k pq(1-p)(1-q)")
s3 = slope(lambda a, b: a + b - a*b*sp.cos(a-b),          "exotic (non-polynomial): p+q-pq cos(p-q)")
s4 = slope(lambda a, b: a + b - a*b + a*b*(a+b)/2,        "cubic (P4 broken): +pq(p+q)/2")

allsame = all(sp.simplify(si - 2*cp) == 0 for si in (s1, s2, s3, s4))
print(f"\n    every composition gives mu'(0) = 2 cp : {allsame}")
print("    ANALYTIC: C(p,0)=p => dC/dp(0,0)=1 ; symmetry => dC/dq(0,0)=1 ;")
print("              mu'(0) = [dC/dp+dC/dq](0,0)*cp = 2 cp.  P3 and P4 are nowhere in this.")

# the matching: g^2 = (s/2cp) g_N  ->  a0 = s/(2cp)  ->  kappa = a0/s = 1/(2cp)
s_, gN, g = sp.symbols('s g_N g', positive=True)
a0 = sp.simplify(s_/(2*cp))
kappa = sp.simplify(a0/s_)
print(f"\n    spherical deep-MOND matching with slope 2cp:  a0 = {a0} ;  kappa = a0/s = {kappa}")
print(f"    at the MEASURED cp=1 (k01 zero mode, SPARC slope to 0.33%): kappa = {sp.simplify(kappa.subs(cp,1))}")

print("\n" + "="*90)
print("VERDICT: kappa = 1/2 does NOT depend on the degree-2 premise (P4) or saturation (P3).")
print("The circular degree-2 joint bears ONLY on the full mu-completion, which is empirical anyway.")
print("kappa's dependency chain reduces to:  (1) TWO channels [premise 1, the real structural leg]")
print("+ (2) symmetry + one-channel exactness  + (3) cp=1 MEASURED (k01 underivable).")
print("So the honest open problem is no longer degree-2 -- it is whether the TWO-CHANNEL count is")
print("unconditional for a MOND-regime (pressureless) source, given GR degenerates Phi=Psi for dust.")
assert allsame, "slope was not 2cp for some composition -- investigate"
