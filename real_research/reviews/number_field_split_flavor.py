#!/usr/bin/env python3
"""
Where the wall REALLY is: the framework splits into a TRANSCENDENTAL normalization and an ALGEBRAIC shape.

Carl's reframe (2026-06-27): maybe the number-field obstruction is being mis-read as a hard wall. Test it.
Claim to verify:
  (A) Z = sqrt(32pi/3) is transcendental (a period: Z = algebraic * sqrt(pi) = algebraic * Gamma(1/2)).
  (B) BUT the framework's SHAPE sector -- mu_fw(x), the constitutive law, theta(0), the fixed point mu_fw(1) --
      is ALGEBRAIC (lives in Q-bar), the SAME number field as the flavor data.
  (C) The clean flavor relations (Koide Q=2/3, sin^2 theta_W = 3/8, Koide amplitude r=sqrt2) are algebraic.
  => CONCLUSION: the number-field wall separates flavor from a0's VALUE (Z), NOT from the framework's shape.
     Flavor and the shape-sector are the SAME field. So the obstruction THERE is STRUCTURAL (wrong slot),
     not number-theoretic -- a softer, potentially-addressable wall. This is where "derive the math ourselves" aims.

Honest both-ways: this does NOT derive flavor. It LOCATES the real obstruction (same-field/wrong-slot) and shows
it is not the number-field wall. The previous chase already found the specific constants free/wrong-slot; this
script's job is only to prove the field-split claim cleanly, so the search is aimed at the right wall.
"""
import sympy as sp

print("="*80); print("(A) The NORMALIZATION Z is transcendental -- a period (Gamma(1/2))"); print("="*80)
Z = sp.sqrt(sp.Rational(32,1)*sp.pi/3)
Z_over_sqrtpi = sp.simplify(Z/sp.sqrt(sp.pi))
print(f"  Z = sqrt(32pi/3) = {sp.nsimplify(Z)} = {float(Z):.6f}")
print(f"  Z / sqrt(pi) = {Z_over_sqrtpi}   -> ALGEBRAIC (in Q-bar)")
print(f"  => Z = (algebraic) * sqrt(pi) = (algebraic) * Gamma(1/2)  ->  Z is a PERIOD (transcendental).")
print(f"     The sqrt(pi) is the geometric measure from rho_DE = Lambda c^2/8piG (sphere area / Einstein 8pi).")
# is sqrt(pi) algebraic? No (Lindemann: pi transcendental => sqrt(pi) transcendental)
print(f"     sqrt(pi) transcendental (Lindemann) -> Z NOT in Q-bar. CONFIRMED: normalization lives outside Q-bar.")

print("\n"+"="*80); print("(B) The SHAPE sector is ALGEBRAIC (in Q-bar) -- same field as flavor"); print("="*80)
x = sp.symbols('x', positive=True)
mu = (sp.sqrt(1+4*x**2)-1)/(2*x)                       # framework's own interpolation
constit = 2*x/(1+sp.sqrt(1+4*x**2))                    # constitutive law m_I = tanh(1/2 asinh(2x))
# the constitutive law, mu_fw, and 2x/(1+sqrt..) are ONE algebraic object. Prove all three identical:
#   rationalizing 2x/(1+sqrt(1+4x^2)) gives (sqrt(1+4x^2)-1)/(2x) = mu_fw ;
#   and tanh(asinh(2x)/2) = (w-1)/(w+1) with w=2x+sqrt(1+4x^2), which equals mu_fw (hand-proved).
ident_mu_constit = sp.simplify(mu - constit) == 0                       # symbolic: mu_fw == 2x/(1+sqrt..)
lhs = sp.tanh(sp.asinh(2*x)/2)
# robust numeric cross-check of the tanh-form == mu_fw at several rationals (sympy won't auto-simplify it)
num_ok = all(abs(complex(lhs.subs(x, sp.Rational(k,4)).evalf()) - float(mu.subs(x, sp.Rational(k,4)))) < 1e-12
             for k in (1,2,3,5,8))
print(f"  mu_fw(x) == 2x/(1+sqrt(1+4x^2))            ? symbolic = {ident_mu_constit}")
print(f"  tanh(1/2 asinh(2x)) == mu_fw(x)            ? numeric  = {num_ok}  (the constitutive law IS mu_fw)")
print(f"  => one algebraic object: mu_fw = (sqrt(1+4x^2)-1)/(2x) = 2x/(1+sqrt(1+4x^2)) = tanh(1/2 asinh 2x)")
mu1 = sp.simplify(mu.subs(x,1))
con1 = sp.simplify(constit.subs(x,1))
phi = (sp.sqrt(5)+1)/2
print(f"  mu_fw(1)        = {mu1} = {float(mu1):.6f}   (1/phi = {float(1/phi):.6f})  -> golden ratio, ALGEBRAIC")
print(f"  constit(1)      = {con1} = {float(con1):.6f}  (= mu_fw(1) = 1/phi at x=1)   -> ALGEBRAIC")
print(f"  theta(0) = sqrt(2) = {float(sp.sqrt(2)):.6f}                                 -> ALGEBRAIC")
# minimal polynomials prove Q-bar membership
print(f"  minimal polynomial of mu_fw(1)=1/phi : {sp.minimal_polynomial(mu1, sp.Symbol('t'))}")
print(f"  minimal polynomial of sqrt(2)        : {sp.minimal_polynomial(sp.sqrt(2), sp.Symbol('t'))}")
print(f"  => the WHOLE shape sector is in Q-bar (algebraic). The sqrt(pi) lives ONLY in the normalization.")

print("\n"+"="*80); print("(C) The clean flavor relations are ALGEBRAIC (Q-bar) -- not periods"); print("="*80)
me, mmu, mtau = 0.51099895, 105.6583755, 1776.86
s = [sp.sqrt(sp.Float(v)) for v in (me,mmu,mtau)]
Q = sum(sp.Float(v) for v in (me,mmu,mtau))/ (sum(s))**2
print(f"  Koide Q (measured)   = {float(Q):.8f}  -> matches the RATIONAL 2/3 = {2/3:.8f} (algebraic)")
print(f"  sin^2 theta_W |_GUT  = 3/8 = {3/8}                                  -> RATIONAL (algebraic)")
r_koide = sp.sqrt(2)
print(f"  Koide amplitude r    = sqrt(2) = {float(r_koide):.6f}                -> ALGEBRAIC")
print(f"  => the clean, parameter-free flavor numbers are ALGEBRAIC. Masses do NOT need pi -> they live in Q-bar.")

print("\n"+"="*80); print("THE REFRAME (computed): where the wall actually is"); print("="*80)
print(f"""  number field of a0's NORMALIZATION (Z) : Q-bar(sqrt(pi))   [transcendental, a period]
  number field of the framework's SHAPE     : Q-bar             [algebraic: mu_fw, 1/phi, sqrt2, constit]
  number field of the FLAVOR data           : Q-bar             [algebraic: 2/3, 3/8, r=sqrt2]

  => The number-field wall separates flavor from a0's VALUE (Z) ONLY. It does NOT separate flavor from the
     framework's SHAPE sector -- those share Q-bar. The famous coincidence stares back: theta(0)=sqrt2 (kernel)
     and r_Koide=sqrt2 (mass vector) are the SAME number in the SAME field; mu_fw(1)=1/phi is a clean algebraic
     constant the flavor sector could in principle use. The obstruction between SHAPE and flavor is therefore
     STRUCTURAL (which algebraic constant sits in which slot, and whether a dynamics FORCES it) -- NOT a number
     field separation. That is a strictly SOFTER wall, and it is exactly the place to 'derive the math ourselves':
     build the dynamics in which the framework's own algebraic shape-constants are FORCED into the flavor slots.

  HONEST CAVEAT (both-ways): this LOCATES the real obstruction; it does NOT cross it. The prior chase showed the
  specific constants are currently FREE/wrong-slot (r=sqrt2 not forced; the F4 sqrt2 had no equivariant map to the
  mass amplitude). 'Same field' makes a bridge NOT-FORBIDDEN; it does not make one EXIST. The open problem is now
  precisely posed: a structural (equivariance) problem inside Q-bar, not a transcendence problem. a0/Z stays out
  of reach by number field; the SHAPE sector is the only candidate bridge and it is structural, not numeric.""")
