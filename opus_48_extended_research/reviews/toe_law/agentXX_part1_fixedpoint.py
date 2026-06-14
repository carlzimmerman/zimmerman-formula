"""
agentXX Route 2 — SYMMETRY / FIXED-POINT LOCK.
PART 1: sub-test (a) — the conformal / luminal fixed point.

Question: does the khronon (Einstein-aether / khronometric) sound speed c_chi
flow to (or get pinned at) a fixed value by ANY symmetry/RG/dS-conformal
structure of the dS+khronon system, in units of H?

We test the SCALAR (khronon/spin-0) sound speed. In Einstein-aether the spin-0
speed is a RATIO of Lagrangian couplings (c1,c2,c3,c4). In the khronometric
(T-reparam) limit it is set by (alpha, beta, lambda) ~ (a, k, l) couplings.
The literature pin (agentEE STEP 1): c_chi^2 = O(gamma/alpha), a ratio of
dimensionless couplings — i.e. a MARGINAL combination.

RUTHLESS framing: a fixed point at c_chi=1 (luminal) would DECOUPLE the sonic
edge (b->c_chi->1 = the horizon/light cone), HURTING the edge coincidence, not
helping. We must report which way any fixed point cuts.

Strategy of Part 1:
  (a1) Dimensional/engineering analysis: is c_chi a marginal (dimensionless)
       coupling or does it carry a scale? A scale-locked c_chi=f(H) requires
       c_chi to NOT be dimensionless OR to be tied to H by a beta-function with
       an H-dependent fixed point.
  (a2) The aether spin-0 speed as a function of couplings: symbolic form, and
       whether the one-loop running of the couplings drives the RATIO to a
       fixed number independent of the couplings (a true RG fixed point), and
       whether that number carries any H.
  (a3) The dS conformal weight of c_chi: under the dS dilatation (the only
       surviving boost-like generator on the foliation, agentEE/SS), what
       scaling weight does c_chi carry? Weight 0 => scale-invariant modulus
       (a dilation cannot pin it). This mirrors agentSS's weight-(-1) finding
       for the gain ratio but now for c_chi ITSELF.
"""
import sympy as sp

print("="*70)
print("PART 1 (a1): is c_chi a marginal (dimensionless) coupling?")
print("="*70)

# In natural units [c]=1 already; c_chi is a DIMENSIONLESS ratio of speeds
# (sound speed / light speed). Set up engineering dimensions explicitly.
# A coupling g_i in the aether action multiplies (del u)^2 terms; in 4D the
# aether couplings c1..c4 are DIMENSIONLESS (the action term
#   (1/16piG) c_i (del u)^2  has [G]=mass^-2, [(del u)^2]=mass^2*[u]^2,
#   u dimensionless (unit vector) => c_i dimensionless).
# Hence c_chi^2 = combination of dimensionless c_i is DIMENSIONLESS.
print("""
Engineering dimensions (4D, hbar=c=1):
  - aether field u^mu is a UNIT vector  => [u]=0 (dimensionless)
  - kinetic term (1/16 pi G) K^{ab}_{mn} del_a u^m del_b u^n
      [1/G]=mass^2, [del u]=mass => term ~ mass^4 (a density) OK
  - the K-tensor couplings c1,c2,c3,c4 are DIMENSIONLESS.
  - spin-0 speed^2 s0 = (c1+c2+c3)(2-c1-c3-... )/... = ratio of c_i
    => c_chi^2 is DIMENSIONLESS, carries NO mass scale, hence NO H.
""")
print("VERDICT (a1): c_chi is a MARGINAL dimensionless coupling.")
print("A dimensionless modulus cannot equal f(H) unless a beta-function")
print("introduces an H-dependent fixed point. Test that next.")

print()
print("="*70)
print("PART 1 (a2): the aether spin-0 (khronon) speed vs couplings, symbolic")
print("="*70)

# Standard Einstein-aether spin-0 squared speed (Jacobson-Mattingly / Jacobson
# 2008 review, eq for s_0^2). Use the canonical combination.
c1,c2,c3,c4 = sp.symbols('c1 c2 c3 c4', real=True)

# Jacobson (Einstein-aether review, 0801.1547) spin-0 speed^2:
#   s0^2 = ( (c1+c2+c3)(2 - c1 - 2 c2 - c3) ) / ( (2 - c1 - c3)(c1 + c2 + c3) * 3? )
# We use the widely-quoted form with c14 = c1+c4, c123 = c1+c2+c3, c13=c1+c3:
c13 = c1 + c3
c14 = c1 + c4
c123 = c1 + c2 + c3
# spin-0 speed squared (Jacobson 0801.1547 eq 86-ish):
s0sq = (c123*(2 - c14)) / (c14*(1 - c13)*(2 + c13 + 3*c2))
s0sq = sp.simplify(s0sq)
print("spin-0 speed^2 (couplings):")
sp.pprint(s0sq)

# Khronometric (T-reparam) limit: c1->0 with khronometric map
# alpha = c14, beta = c13, lambda = c2. Then
#   c_chi^2 = (alpha)(... )  -> Blas-Pujolas-Sibiryakov form:
alpha, beta, lam = sp.symbols('alpha beta lambda', positive=True)
# BPS khronometric scalar speed^2 (0905.2943):
#   c_s^2 = (alpha - 2)(beta + lambda) / [ alpha (beta - 1)(2 + beta + 3 lambda) ]
cchi_sq_khrono = (alpha - 2)*(beta + lam) / (alpha*(beta - 1)*(2 + beta + 3*lam))
cchi_sq_khrono = sp.simplify(cchi_sq_khrono)
print()
print("khronometric c_chi^2 (alpha,beta,lambda) [Blas-Pujolas-Sibiryakov]:")
sp.pprint(cchi_sq_khrono)
print()
print("Observation: c_chi^2 is a RATIONAL FUNCTION of dimensionless couplings.")
print("It contains NO H, NO scale. It is a free combination of Lagrangian")
print("parameters. There is no H anywhere on the RHS.")

print()
print("="*70)
print("PART 1 (a2'): does the RATIO have a COUPLING-INDEPENDENT fixed value?")
print("="*70)
# A genuine RG fixed point would make c_chi^2 approach a NUMBER independent
# of the couplings as the couplings flow. Test: is c_chi^2 -> const along any
# natural flow direction? Check the gradient: if d(c_chi^2)/dc_i are not all
# zero generically, c_chi^2 is NOT pinned — it tracks the couplings.
grads = [sp.simplify(sp.diff(cchi_sq_khrono, v)) for v in (alpha, beta, lam)]
print("d(c_chi^2)/d(alpha,beta,lambda):")
for v,g in zip((alpha,beta,lam), grads):
    print(f"  d/d{v}:")
    sp.pprint(g)
nonzero = [sp.simplify(g) != 0 for g in grads]
print()
print("All three gradients nonzero (generically)?", all(nonzero))
print("=> c_chi^2 SLIDES with the couplings: NO coupling-independent fixed")
print("   value. It is a free modulus, not pinned to any number (let alone H).")
