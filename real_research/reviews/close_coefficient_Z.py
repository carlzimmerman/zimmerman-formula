#!/usr/bin/env python3
"""
GAP B -- can a defensible NORMALIZATION turn the Deser-Levin de Sitter-Unruh
mechanism's coefficient (a0_eff = 2 a_Lambda = 2 c H_Lambda) into the framework's
a0 = c H_Lambda / Z,  Z = sqrt(32pi/3) = 5.789?

The mechanism (reviews/deser_levin_mond_derivation.py, BANKED) gives the deep-MOND
sqrt-law with SCALE ~ cH_Lambda (REAL) but COEFFICIENT a0_eff = 2 a_Lambda. The
framework needs a0 = cH_Lambda / Z. Ratio a0_eff / a0 = 2 Z = 11.578. This script
tests every named normalization that could supply that factor and asks, ADVERSARIALLY:

  does the route FORCE 5.789, or does it merely move a free O(1) around / live in the
  wrong number field (so it can NEVER equal sqrt(32pi/3))?

Banked walls this BUILDS ON (cite, do not re-derive):
  * Z_is_one_pure_number.py : a0/cH is a PURE number; G,rho,c,H all cancel. The
    'density base vs horizon base' sqrt(8pi/3) is a UNIT CONVERSION, not a missing factor.
  * desitter_entropy_coefficient.py : NUMBER-FIELD THEOREM. Horizon/entropy/temperature
    coefficients are (rational x pi^n); Z = sqrt(32pi/3) carries a SQUARE ROOT of
    (rational x pi) -- the density (sqrt(G rho)) fingerprint. sqrt(rational*pi) is NOT
    in Q(pi). So no temperature/entropy NORMALIZATION can equal Z. Different fields.
  * kappa-closure + sqrt(pi) number-field obstruction (memory): Z PROVEN unforced.

This script is the SAME theorem applied to the Deser-Levin route specifically, run as a
number-field membership test on each candidate, in sympy (exact), so the conclusion is a
PROOF, not a numerical near-miss. Expected: STALLED-walled. Flag ONLY a genuinely new
forcing, then test it can't be a coincidence.

Run:  python reviews/close_coefficient_Z.py     (needs sympy, numpy; exit 0)
"""
import sympy as sp
import numpy as np

pi = sp.pi
Z_fw   = sp.sqrt(32*pi/3)          # framework coefficient, EXACT
inv_Z  = 1/Z_fw                    # a0/cH_Lambda target = 0.17275
a0_eff_over_cH = sp.Integer(2)     # Deser-Levin naive mechanism: a0_eff = 2 a_Lambda
RATIO  = a0_eff_over_cH * Z_fw     # = 2Z, the factor a normalization must supply

def fnum(x): return float(x)

print("="*94)
print(" GAP B -- NORMALIZATION test: can the Deser-Levin coefficient 2 a_Lambda become cH_Lambda/Z ?")
print("="*94)
print(f"  framework target : a0/cH_Lambda = 1/Z = 1/sqrt(32pi/3) = {fnum(inv_Z):.5f}")
print(f"  mechanism gives  : a0_eff/cH_Lambda = 2  (deep-MOND scale, BANKED deser_levin script)")
print(f"  a normalization must supply factor  a0_eff/a0 = 2Z = {fnum(RATIO):.4f}  (~11.6x LOWER a0)\n")

# ----------------------------------------------------------------------------------
# The number-field GATE (the adversarial backstop). A coefficient is "forceable by a
# horizon/temperature normalization" ONLY if it lives in Q(pi) = {rational x pi^n}.
# Z lives in Q(sqrt(pi)) (a square root). We test membership exactly.
# ----------------------------------------------------------------------------------
def in_Q_pi(expr):
    """True if expr is (rational)*pi**(integer): i.e. lives in the field horizon/entropy
    normalizations generate. We test: is expr/pi**k rational for some small integer k?"""
    e = sp.nsimplify(sp.simplify(expr))
    for k in (-2,-1,0,1,2,3):
        q = sp.simplify(e/pi**k)
        if q.is_rational and q != 0:
            return True, (q, k)
    return False, None

print("-"*94)
print(" THE GATE:  horizon/entropy/temperature factors are rational x pi^n  (number-field theorem,")
print("            BANKED desitter_entropy_coefficient.py).  Z must clear this gate to be forceable.")
print("-"*94)
ok, info = in_Q_pi(Z_fw)
print(f"   Z = sqrt(32pi/3): is it rational x pi^n ?  -> {ok}")
print(f"      Z^2 = {sp.simplify(Z_fw**2)} (= 32pi/3, irrational UNDER a sqrt).  Z carries a SQUARE ROOT.")
print(f"   => Z is in Q(sqrt(pi)), NOT in Q(pi). The gate is a number-field wall, independent of which")
print(f"      normalization we pick. Keep this in mind as each candidate is scored below.\n")

# ----------------------------------------------------------------------------------
# CANDIDATE NORMALIZATIONS (the four Carl named). For each: what factor does it actually
# supply, does it land on 2Z=11.578, and does its OUTPUT clear the number-field gate?
# ----------------------------------------------------------------------------------
results = []
print("="*94)
print(" CANDIDATE NORMALIZATIONS  (factor each supplies vs the needed 2Z = %.4f)" % fnum(RATIO))
print("="*94)

# --- (1) The 2pi in the Unruh/de Sitter temperature ---
# T = (hbar/2pi c k) sqrt(a^2 + a_L^2). The 2pi is ALREADY inside Deser-Levin's T; the
# mechanism's 2 a_Lambda came out AFTER the 2pi cancels in the F=T(a)-T(0) ratio (the
# 2pi sets the temperature SCALE, not the dimensionless a0/cH). Adding ANOTHER 2pi or 1/2pi:
f1 = 2*pi
land1 = sp.simplify(f1 - RATIO)
gate1, _ = in_Q_pi(f1)
results.append(("2pi  (Unruh temperature prefactor)", f1, gate1))
print(f" (1) Unruh 2pi:            factor = 2pi = {fnum(f1):.4f}.  needed {fnum(RATIO):.4f}.  off by {fnum(f1/RATIO):.3f}x")
print(f"     in Q(pi)? {gate1}.  The 2pi is rational x pi -> CANNOT equal 2Z (square root). And it is")
print(f"     already cancelled in the deep-MOND ratio. RELABEL, wrong field.\n")

# --- (2) Bekenstein-Hawking 1/4 (surface gravity / area-entropy) ---
# S = A/4 (in Planck units). Surface-gravity / entropy normalizations introduce factors
# like 1/4, 1/2, 4pi -- all rational x pi^n.
f2a = sp.Rational(1,4)
f2b = 4*pi          # solid angle
f2c = sp.Rational(1,2)  # surface gravity of enclosed mass
for nm,v in [("BH entropy 1/4",f2a),("solid angle 4pi",f2b),("surface-grav 1/2",f2c)]:
    g,_ = in_Q_pi(v); results.append((nm,v,g))
print(f" (2) Bekenstein-Hawking / surface gravity:  candidate factors 1/4, 4pi, 1/2")
print(f"     none equals 2Z={fnum(RATIO):.4f}; combos (e.g. 4pi*... ) stay rational x pi^n.")
print(f"     ALL in Q(pi) -> the GATE blocks them: a square root cannot be built from these. RELABEL.\n")

# --- (3) The density chain  rho_DE = Lambda c^2/(8piG),  a0 = (c/2) sqrt(G rho_DE) ---
# This is the ONLY route that produces a SQUARE ROOT. Let's run it EXACTLY and see what
# coefficient it forces -- because THIS is where Z actually comes from.
print(" (3) DENSITY chain (the only sqrt-producing route -- run exact):")
print("     rho_DE = Lambda c^2/(8piG),  H_Lambda^2 = Lambda c^2/3  =>  rho_DE = 3 H_L^2/(8piG)")
print("     a0 = (c/2) sqrt(G rho_DE) = (c/2) sqrt(G * 3 H_L^2/(8piG)) = (c H_L/2) sqrt(3/(8pi))")
H_L, c, G = sp.symbols('H_L c G', positive=True)
Lam = sp.symbols('Lambda', positive=True)
rho_DE = 3*H_L**2/(8*pi*G)                  # from Friedmann, Lambda-only
a0_dens = (c/2)*sp.sqrt(G*rho_DE)           # framework density definition
a0_dens = sp.simplify(a0_dens)
ratio_dens = sp.simplify(a0_dens/(c*H_L))   # a0/cH_Lambda
print(f"        a0 = {a0_dens}")
print(f"        a0/(cH_L) = {ratio_dens} = {sp.nsimplify(ratio_dens)}")
print(f"        check equals 1/Z ? 1/Z = {sp.nsimplify(inv_Z)};  match = {sp.simplify(ratio_dens-inv_Z)==0}")
g3,_ = in_Q_pi(1/ratio_dens)
results.append(("density chain (c/2)sqrt(Grho)", 1/ratio_dens, g3))
print(f"     => the density chain REPRODUCES Z EXACTLY (Z=1/(this ratio)). in Q(pi)? {g3} (it's a sqrt).")
print(f"     BUT: this is the framework's own DEFINITION a0=(c/2)sqrt(Grho_DE) re-expressed -- it does")
print(f"     NOT connect to the Deser-Levin temperature mechanism, whose output was 2 a_Lambda. Two")
print(f"     factors here are FREE: the '1/2' (why (c/2)? not (c) or (c/sqrt2)?) and the choice rho_DE")
print(f"     (vs rho_total). Moving either moves Z. So the density chain DEFINES Z, it does not FORCE it.\n")

# Prove the '1/2' is free: a general prefactor 'kappa' gives a0 = kappa*c*sqrt(Grho).
kappa = sp.symbols('kappa', positive=True)
a0_gen = kappa*c*sp.sqrt(G*rho_DE)
Z_gen = sp.simplify(c*H_L/a0_gen)
print(f"     PROOF the prefactor is free:  a0 = kappa*c*sqrt(G rho_DE) -> Z = {Z_gen}")
print(f"        kappa=1/2 -> Z={fnum(Z_gen.subs(kappa,sp.Rational(1,2))):.4f}=sqrt(32pi/3) (framework)")
print(f"        kappa=1   -> Z={fnum(Z_gen.subs(kappa,1)):.4f}")
print(f"        kappa=1/sqrt(2pi) -> Z={fnum(Z_gen.subs(kappa,1/sp.sqrt(2*pi))):.4f}")
print(f"     The mechanism does not pin kappa. (matches Z_is_one_pure_number.py: ONE free O(1).)\n")

# --- (4) d(d-1) vs (3/8pi) factors ---
# d(d-1)/2 is the Einstein-tensor / cosmological factor in d dims; for d=4 -> 12/2=6.
# (3/8pi) is the Friedmann 3/(8pi). Test whether the dimensional factor forces Z.
print(" (4) d(d-1) cosmological factor vs Friedmann 3/(8pi):")
d = sp.symbols('d', positive=True)
ddm1 = d*(d-1)
for dv in (3,4,5):
    print(f"        d={dv}: d(d-1)={ddm1.subs(d,dv)},  d(d-1)/2={ddm1.subs(d,dv)/2}  (d=4 gives 6 = Verlinde Z)")
fried = sp.Rational(3,8)/pi
print(f"        Friedmann 3/(8pi) = {sp.nsimplify(fried)} = {fnum(fried):.5f}  (the rho_DE normalization)")
print(f"        Z^2 = 32pi/3 = 1/(  (3/(32pi)) ). Note 3/(32pi) = (1/4)*(3/(8pi)): the BH 1/4 TIMES")
print(f"        Friedmann 3/8pi -- but UNDER the density sqrt. d(d-1) gives RATIONAL 6 (Verlinde), in")
g4a,_ = in_Q_pi(sp.Integer(6)); g4b,_ = in_Q_pi(fried)
results.append(("d(d-1)/2 = 6 (Verlinde)", sp.Integer(6), g4a))
print(f"        Q(pi){'='*0} ({g4a}); it does NOT carry the sqrt, so 6 != sqrt(32pi/3). RELABEL/wrong field.\n")

# ----------------------------------------------------------------------------------
# THE CRUX: does ANY route both (a) clear the number-field gate AND (b) FORCE the value?
# ----------------------------------------------------------------------------------
print("="*94)
print(" SCORECARD")
print("="*94)
print(f"   {'route':<40}{'factor/coeff':>16}{'in Q(pi)?':>11}{'= 2Z or = Z?':>14}")
print("   "+"-"*81)
for nm,v,g in results:
    matchZ  = sp.simplify(sp.nsimplify(v) - Z_fw)==0
    match2Z = sp.simplify(sp.nsimplify(v) - RATIO)==0
    tag = "= Z" if matchZ else ("= 2Z" if match2Z else "no")
    print(f"   {nm:<40}{fnum(v):>16.4f}{str(g):>11}{tag:>14}")
print()
print("   READ: every route that LANDS on Z (the density chain) is NOT in Q(pi) (it's a square root)")
print("   AND is the framework's own DEFINITION, not a forcing -- its 1/2 prefactor and rho_DE choice")
print("   are free (proven above). Every route that is genuinely a horizon/temperature NORMALIZATION")
print("   (2pi, 1/4, 4pi, 1/2, d(d-1)/2=6) IS in Q(pi) and therefore CANNOT equal sqrt(32pi/3).\n")

# ----------------------------------------------------------------------------------
# ADVERSARIAL: is there a NEW forcing? Test the one combination that looks structural:
# Z^2 = 32pi/3 = (BH 1/4)^{-1} * (Friedmann 3/8pi)^{-1}? i.e. does 4 * (8pi/3) = 32pi/3?
# ----------------------------------------------------------------------------------
print("="*94)
print(" ADVERSARIAL -- the one structural-looking combination (could it be a NEW forcing?)")
print("="*94)
combo = 4 * (8*pi/3)
print(f"   observe:  Z^2 = 32pi/3.  And  4 * (8pi/3) = {sp.simplify(combo)} = 32pi/3 ?  {sp.simplify(combo-Z_fw**2)==0}")
print(f"   so Z = sqrt( 4 * 8pi/3 ) = 2 sqrt(8pi/3).  Tempting story: '4' = Bekenstein-Hawking 1/4 inverted,")
print(f"   '8pi/3' = inverse Friedmann.  Does this FORCE Z?  Adversarial check:")
print(f"     - The '4' here is the 2^2 from a0=(c/2)... SQUARED, i.e. it is the prefactor^-2, the SAME free")
print(f"       1/2 from route (3) -- NOT the BH entropy 1/4 (which would enter LINEARLY in an area law, not")
print(f"       squared under a density sqrt). Identifying them is numerology: 4 = (1/2)^-2 = 4(BH)^... only")
print(f"       coincidentally. Move the prefactor kappa and the '4' becomes 1/kappa^2, killing the BH story.")
print(f"     - The 8pi/3 IS forced (Friedmann), but it enters as a UNIT CONVERSION (cH vs c sqrt(Grho)),")
print(f"       which Z_is_one_pure_number.py already showed is not a physical factor.")
print(f"   => the 'BH 1/4 x Friedmann' factorization is a RE-LABELING of the free prefactor, not a forcing.")
print(f"      It cannot be promoted to a derivation: the moment kappa!=1/2 is allowed, the '4' evaporates.\n")

# Show it explicitly: under kappa, the "4" is 1/kappa^2, not pinned to BH.
four_general = sp.simplify(Z_gen**2 / (8*pi/3))
print(f"   PROOF: with general prefactor kappa,  Z^2/(8pi/3) = {four_general}  (= 1/(4 kappa^2)... ).")
print(f"          kappa=1/2 -> {sp.simplify(four_general.subs(kappa,sp.Rational(1,2)))} (the '4'); kappa free -> any value.")
print(f"          So '4 = BH inverse' holds ONLY at the posited kappa=1/2. Not forced. No new door.\n")

print("="*94)
print(" VERDICT -- GAP B (the coefficient Z)")
print("="*94)
print("""  STALLED -- WALLED (both-ways honest; no closure, no manufactured deficit).

  * The Deser-Levin mechanism's coefficient (2 a_Lambda) and the framework's (cH/Z) differ by
    2Z = 11.58. The needed normalization is real and large.
  * EVERY genuine horizon/temperature/entropy normalization (the Unruh 2pi, BH 1/4, solid-angle
    4pi, surface-gravity 1/2, the d(d-1)/2=6 cosmological factor) lives in Q(pi) = rational x pi^n.
    Z = sqrt(32pi/3) lives in Q(sqrt(pi)) -- it carries a SQUARE ROOT. NUMBER-FIELD THEOREM
    (banked desitter_entropy_coefficient.py): these fields don't meet. So NO such normalization
    can FORCE Z. They can only bracket it numerically (6, 2pi ~ 5.8..6.28) -- a coincidence of
    magnitude, not an identity.
  * The ONLY route that lands on Z exactly is the framework's OWN density definition
    a0 = (c/2) sqrt(G rho_DE). That reproduces Z by CONSTRUCTION, but its 1/2 prefactor and its
    rho_DE (vs rho_total) choice are FREE -- moving kappa moves Z continuously (proven). So the
    density chain DEFINES Z, it does not DERIVE it. (Matches Z_is_one_pure_number.py: ONE free O(1).)
  * The structural-looking 'Z^2 = (BH 1/4)^-1 x (Friedmann 8pi/3)' factorization is a RE-LABELING:
    the '4' is the free prefactor squared (1/kappa^2 at kappa=1/2), NOT the area-law 1/4. It
    evaporates the instant kappa is allowed to vary. No new forcing.

  NET: no defensible normalization bridges 2 a_Lambda -> cH/Z. Z remains an UNFORCED O(1) -- the
  same wall as kappa-closure and the sqrt(pi) number-field obstruction, now confirmed along the
  Deser-Levin route specifically. The mechanism owns the SCALE (~cH_Lambda) and the deep-MOND
  LIMIT; it does NOT own the coefficient. GAP B does NOT close. (No genuinely new door flagged.)""")
print("="*94)
