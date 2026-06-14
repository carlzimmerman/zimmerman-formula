# ----------------------------------------------------------------------
# VV2 part (a): dS observer algebra is HYPERFINITE II_1 -- the crossed
# product amenability-preservation logic, made explicit & sanity-checked.
#
# CLPW: N_obs = (M (x) B(L^2 R)) ^ {modular-flow-invariant} where M is the
# type III_1 QFT vacuum algebra, crossed by the modular automorphism group
# (boost) ~ R, then constrained by observer energy -> II_1 with trace.
#
# Connes permanence facts (cited, not numerically provable, but the LOGIC
# is a finite implication chain we lay out + the group-amenability inputs
# are checkable):
#   (i)   M (QFT local/vacuum algebra) is the hyperfinite III_1 factor.
#         [Buchholz-D'Antoni-Fredenhagen; split property/nuclearity]
#   (ii)  hyperfinite <=> injective <=> amenable (Connes 1976).
#   (iii) injectivity is preserved under crossed product by an amenable
#         locally compact group. R (the boost/modular group) is ABELIAN
#         => amenable. [Connes; the standard permanence theorem]
#   (iv)  injectivity passes to the type II_1 corner / centralizer
#         (compression by a projection, and to a vN subalgebra that is the
#         image of a normal conditional expectation -- the trace-preserving
#         expectation exists here).
#   => N_obs is injective II_1 => by Connes uniqueness = the UNIQUE
#      hyperfinite II_1 factor R.
# ----------------------------------------------------------------------

print("=== (a) dS-side amenability chain: every link is a THEOREM, inputs checkable ===")
links = [
 ("(i) QFT vacuum algebra M is hyperfinite III_1",
  "Buchholz-D'Antoni-Fredenhagen / split property (standard); cited"),
 ("(ii) hyperfinite <=> amenable <=> injective",
  "Connes 1976 Ann.Math.104 (THEOREM)"),
 ("(iii) modular/boost group is R, abelian => amenable",
  "abelian groups are amenable (THEOREM); checkable: R = (R,+)"),
 ("(iv) crossed product of injective by amenable lc group is injective",
  "Connes permanence (THEOREM)"),
 ("(v) injectivity passes to II_1 corner via normal cond. expectation",
  "trace-preserving E exists (CLPW have the trace); injective subalg (THEOREM)"),
 ("=> N_obs injective II_1 => = R by Connes uniqueness",
  "Connes 1976 uniqueness of hyperfinite II_1 (THEOREM)"),
]
for claim, basis in links:
    print(f"  {claim}\n      basis: {basis}")

# checkable input: amenability of R via Folner sequence (the only group-theory input)
print()
print("=== amenability of the modular group R: Folner condition (checkable) ===")
import numpy as np
# Folner: |g F_n triangle F_n| / |F_n| -> 0 ; for R use F_n=[-n,n], g=t
for t in [1.0, 10.0, 100.0]:
    for n in [10, 100, 1000, 10000]:
        # symmetric difference of [-n,n] and [-n+t,n+t] has measure 2|t| (for n>|t|)
        sym = 2*abs(t)
        ratio = sym/(2*n)
        if n == 10000:
            print(f"  shift t={t}: |tF_n △ F_n|/|F_n| at n={n} = {ratio:.2e}  (-> 0  => R amenable)")
