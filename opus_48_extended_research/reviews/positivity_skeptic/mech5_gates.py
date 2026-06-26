"""
MECHANISM 5 — THE TWO GATES, applied to the S^3 zeta-Casimir result.

Result established (mech5_zeta_casimir_s3.py + mech5_casimir_verify.py):
  conformal scalar  E_conf = (1/2) zeta(-3) / R = 1/(240 R)    [exact, scheme-indep]
  minimal scalar    has a zeta(1) pole -> scheme-dependent finite part ~ -0.0569/R
  Dirac (massless)  E_D = -29/30 / R   [exact]
  NONE equals 1/2.

GATE (a) — DOES IT EQUAL 1/2 (and is it even the right KIND of object)?
GATE (b) — DOUBLE-COUNT: a Casimir energy is a VACUUM ENERGY -> renormalizes rho_Lambda,
           which is ALREADY SPENT building cH_Lambda + the 8pi.

We also apply the framework's TWO GATES from the task:
  (G1 ANTI-CIRCULARITY): is the S^3, the field content, the coupling FORCED by the
     framework's own dS/MM/K(Q) structure, or inserted to yield 1/2?
  (G2 SCALE-FRACTION): is the 1/2 the SAME 1/2 as kappa (the coupling OUTSIDE
     sqrt(G rho_Lambda) that sets a0's normalization), or a vacuum energy that
     double-counts rho_Lambda?
"""
import sympy as sp
import mpmath as mp
mp.mp.dps = 40

print("="*80)
print("GATE (a): magnitude AND kind")
print("="*80)
vals = {
  "conformal scalar  E*R": sp.Rational(1,240),
  "Dirac massless    E*R": sp.Rational(-29,30),
}
for k,v in vals.items():
    print("  %s = %s = %.6f   == 1/2 ? %s" % (k, v, float(v), v==sp.Rational(1,2)))
print("  minimal scalar: zeta(1) POLE -> not even finite without a counterterm (scheme-dep).")
print()
print("  MAGNITUDE: NO mechanism gives 1/2. The clean (conformal) number is 1/240.")
print("  The analogy to the string -1/12 (=zeta(-1)) FAILS to land on 1/2: the S^3 energy")
print("  zeta is zeta(s-2) (from the (l+1)^2 degeneracy), so the special value is zeta(-3)=")
print("  1/120, and the (1/2) sum-omega prefactor gives 1/240. 1/2 is structurally absent.")
print()
print("  KIND: even the conformal 1/240 is a DIMENSIONLESS ENERGY COEFFICIENT (E has units")
print("  1/R = energy). kappa is a DIMENSIONLESS ACTION NORMALIZATION multiplying the WHOLE")
print("  Route-E action OUTSIDE sqrt(G rho_DE). A Casimir coefficient sits INSIDE a particular")
print("  field's vacuum energy; it is not the overall action multiplier. Different object.")

print("\n" + "="*80)
print("GATE (b): DOUBLE-COUNT — the Casimir energy IS rho_Lambda (the guard bites hard)")
print("="*80)
print("""
  A Casimir energy on S^3 of radius R is a VACUUM ENERGY:  E_cas = C/R  (C=1/240,...).
  As an energy DENSITY on the S^3 (volume 2 pi^2 R^3):
        rho_cas = E_cas / Vol = (C/R)/(2 pi^2 R^3) = C/(2 pi^2 R^4)  ~  1/R^4.
  This is EXACTLY a contribution to the vacuum energy density = a contribution to
  Lambda (rho_vac). In the framework, R is the de Sitter / Hubble radius (the horizon
  S^3), so rho_cas ~ 1/R_H^4 is a renormalization of rho_Lambda ITSELF.

  But rho_Lambda is the INPUT that is ALREADY SPENT:
     a0 = (c/2) sqrt(G rho_Lambda) = c^2 sqrt(Lambda/32pi),
  with the 8pi from rho_DE = Lambda c^2/(8 pi G) and the Friedmann-3 ALREADY inside Z.
  Using a Casimir vacuum energy to 'fix kappa' would feed a piece of rho_Lambda back in
  to set the coefficient that multiplies sqrt(rho_Lambda) -> the SAME geometric input
  (the horizon scale + the vacuum energy it carries) is counted TWICE. This is the
  identical double-count that produced the spurious 'alpha2 LIVE' reading in memory
  (c^2/(GM/R) reused) and that the TOPOLOGICAL_KAPPA verdict flagged for the GH
  temperature/entropy halves.
""")

# Quantify: the Casimir density vs rho_Lambda are the SAME order (both ~ 1/R_H^4 = Lambda^2),
# differing only by the dimensionless C and 8pi/3 factors -> they are the SAME quantity up to
# an O(1), confirming it is a renormalization of the same input, not an independent number.
print("  Quantitative: rho_Lambda = Lambda c^2/(8 pi G); with Lambda = 3/R_H^2 (c=1),")
print("    rho_Lambda = 3/(8 pi G R_H^2)  -> the vacuum-energy SCALE set by R_H.")
print("    rho_cas = C/(2 pi^2 R_H^4)      -> SAME R_H, also a vacuum-energy density.")
print("  These are the SAME physical input (horizon-scale vacuum energy) up to dimensionless")
print("  factors; one cannot be an INDEPENDENT determiner of the coefficient on the other's")
print("  square root. => DOUBLE-COUNT. Gate (b) FAILS even if (a) had given 1/2.")

print("\n" + "="*80)
print("FRAMEWORK GATE G1 (anti-circularity): is the construction FORCED?")
print("="*80)
print("""
  - The S^3 (round dS horizon) IS forced by the framework (the Euclidean dS saddle's
    horizon). GOOD so far -- same geometry the eta-route used.
  - BUT the FIELD CONTENT is NOT forced. To even HAVE a Casimir energy you must pick a
    field (conformal scalar? minimal scalar? the K(Q) mode? a Dirac fermion?). Each gives
    a DIFFERENT number (1/240, scheme-dep, -29/30, ...). The framework does not force WHICH
    field's vacuum energy to use, nor the coupling xi. Picking the one (if any) that gave
    1/2 would be inserting the answer -> CIRCULAR. (And none of the natural choices gives 1/2.)
  - The COUPLING xi (conformal vs minimal) is a genuine free choice that changes the number
    discontinuously (minimal even has a pole). No framework structure fixes xi.
""")

print("="*80)
print("FRAMEWORK GATE G2 (scale-fraction): is this 1/2 the SAME 1/2 as kappa?")
print("="*80)
print("""
  NO. kappa is the OUTSIDE action normalization multiplying sqrt(G rho_DE); the
  Casimir coefficient is a vacuum ENERGY living INSIDE rho_DE itself (it renormalizes
  Lambda). So even granting a hypothetical 1/2:
    - it would be a piece of rho_Lambda (INSIDE the root), not the outside multiplier;
    - and that piece is already spent (gate b).
  This is the SAME scale-fraction wall that closed unitarity, holography, and the
  eta-route: every probe sees INSIDE the operator / the dimensionless structure /
  the vacuum energy, never the bare OUTSIDE multiplier kappa.
""")

print("="*80)
print("VERDICT: Mechanism 5 HITS THE WALL on BOTH gates.")
print("  (a) magnitude: NO mechanism gives 1/2 (clean conformal = 1/240; the string -1/12")
print("      analogy lands on zeta(-3)=1/120 -> 1/240, not 1/2). And it is the wrong KIND")
print("      (an energy coefficient, not the action normalization).")
print("  (b) double-count: a Casimir is a vacuum energy ~1/R_H^4 = a renormalization of")
print("      rho_Lambda, ALREADY SPENT building cH_Lambda + the 8pi. Using it for kappa")
print("      double-counts. G2 (scale-fraction) confirms: it is INSIDE the root, not kappa.")
print("  G1: field content + xi are not framework-forced; selecting to hit 1/2 = circular.")
print("  => CLOSED, consistent with TOPOLOGICAL_KAPPA + KAPPA_FORCING_DOOR_CLOSED.")
