"""
ADVERSARIAL: build the STRONGEST possible pro-door case, then test it honestly.

The prompt's hope: 'eta-invariants naturally give 1/2 (the APS eta/2 term)'.
Strongest versions:
  (A) The eta/2 PREFACTOR is literally a 1/2 -- but it multiplies eta, not a bare 1.
  (B) The 5D embedding: SO(4,1) lives in R^{4,1}; S^4 is the boundary of the 5-ball
      / the dS hyperboloid is codim-1 in R^{4,1}. Is there a 5D->4D eta=1/2?
  (C) The signature operator on S^3 / the Hirzebruch defect.
  (D) The gravitational Chern-Simons of the MM connection -> a half-level?
  (E) The 'half' in the de Sitter free energy / the conical-deficit eta.
Each tested for: does it give EXACTLY 1/2, NON-circularly, and reach kappa?
"""
import sympy as sp
from sympy import Rational, pi, S, sqrt, simplify, nsimplify, gamma, zeta, Symbol

print("="*70)
print("ADVERSARIAL PRO-DOOR STRESS TEST")
print("="*70)

# (A) the eta/2 prefactor
print("""
(A) 'The eta/2 term IS a 1/2.'  -- The 1/2 in (eta+h)/2 is a UNIVERSAL prefactor
    multiplying the spectral data; it is NOT a free-standing number the geometry
    OUTPUTS. The OUTPUT of the boundary term is (eta+h)/2, and for the dS S^3 that
    output is (0+0)/2 = 0. The bare prefactor 1/2 is the same 1/2 in EVERY APS
    formula on every manifold -- it carries no dS information, so identifying
    kappa with it ('a0 has a 1/2 because APS has a 1/2') is pure coincidence-
    matching, exactly the circular move the gate forbids.
""")
print("   (eta+h)/2 on dS S^3 = (0+0)/2 = 0.  The prefactor-1/2 is geometry-blind.")

# (B) 5D embedding eta
print("""
(B) 5D embedding SO(4,1) in R^{4,1}: is there an odd-(5)-dim eta giving 1/2?
    The APS eta-invariant is defined for the boundary operator, which is
    ODD-dimensional = the (4-1)=3-dim S^3 (for a 4D bulk index) OR the 4-dim S^4
    (if one does a 5D bulk index). For a 5D BULK (the SO(4,1) embedding space) with
    boundary S^4: the boundary Dirac eta on the round S^4 (EVEN dim) -- but eta is
    only defined for SELF-ADJOINT operators on ODD-dim boundaries; S^4 is even, so
    the relevant boundary eta would need a 5D manifold with S^4 boundary. The round
    S^4 Dirac operator (even dim) has a CHIRAL grading and its 'eta' is replaced by
    the INDEX, which is A-hat[disk_5]=0 for the round geometry. No 1/2.
""")
# round S^4 Dirac index = 0 (A-hat[S^4]=0); 5-ball A-hat = 0 (flat-ish). No 1/2.
print("   5D bulk, S^4 boundary: A-hat=0, index=0; no eta-1/2 (S^4 even-dim).")
print("   The relevant odd boundary is S^3, already shown eta=0.")

# (C) signature operator
print("""
(C) Signature operator on S^3 (the Atiyah-Hirzebruch / Hirzebruch signature
    defect). For the round S^3 bounding the round S^4: signature(S^4)=0, the
    eta of the ODD signature operator on round S^3 = 0 (again +/- symmetric).
    Lens-space signature defects are non-zero Dedekind sums but q=1 -> 0.
""")
print("   signature eta on round S^3 = 0 (sigma(S^4)=0). No 1/2.")

# (D) gravitational Chern-Simons half-level
print("""
(D) Gravitational CS of the MM connection.  The MM action S ~ INT eps F^F is, on
    a manifold WITH boundary, EH+Lambda+ a boundary gravitational Chern-Simons
    term. Its 'level' is set by 1/G (the Newton constant / Lambda), NOT a pure
    integer or half-integer topological number -- it is a DIMENSIONFUL coupling.
    So the CS 'level' here is 1/(16 pi G) x (geometry), continuous, NOT a Z/2
    half-level. No topological 1/2.
""")
G = Symbol('G', positive=True)
print("   MM boundary CS level ~ 1/(16 pi G) = DIMENSIONFUL/continuous, not 1/2.")

# (E) conical deficit / de Sitter free-energy 'half'
print("""
(E) The de Sitter free energy / horizon entropy carries an S_dS = A/4G = pi/(G H^2)
    with a famous '1/4' and the Gibbons-Hawking T_dS = H/2pi with a '1/2pi'. These
    ARE the gravitational halves -- but the framework ALREADY SPENT them: the KAPPA
    paper sec 3.3 states every gravitational 1/2 (surface-gravity kappa_sg=c^2/2R,
    Komar, equipartition) is consumed building cH_Lambda and the 8pi. Re-using the
    horizon 1/2 to ALSO supply kappa would DOUBLE-COUNT the same factor -- exactly
    the alpha2 double-count error flagged in memory (c^2/(GM/R) reused twice).
""")
print("   Horizon 1/2's are ALREADY spent (surface gravity c^2/2R, GH temp).")
print("   Re-using one for kappa = DOUBLE-COUNT (cf. the alpha2 self-energy error).")

print()
print("="*70)
print("ADVERSARIAL VERDICT: no construction yields a NON-CIRCULAR 1/2 that REACHES kappa.")
print("="*70)
print("The strongest pro-door cases all fail at one of three gates:")
print("  1. OUTPUT is 0, not 1/2 (round S^3/S^4 is +/- symmetric, h=0, sigma=0).")
print("  2. A non-zero number needs structure dS LACKS (Z_q quotient) = CIRCULAR.")
print("  3. A real 1/2 (prefactor, horizon) is geometry-blind or ALREADY-SPENT,")
print("     and a spectral-asymmetry/level cannot reach the action-normalization kappa")
print("     (the same scale-fraction wall that closed unitarity & holography).")
