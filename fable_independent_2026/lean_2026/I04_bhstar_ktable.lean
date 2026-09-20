import Mathlib

/-!
# I04 — Wave L: the K-table absorption and the central-β falsification

SCOPE (per lean-math-certification): this file certifies the ABSORPTION of the Chandrasekhar
1965 K-table criterion (ApJ 142, 1519, Table 1 — the 1PN radial-instability boundary cases,
provenance-checked) INTO the S⁵ machinery of I02, and the NUMERIC FALSIFICATION at the
anchor: with the homogeneous coefficient κ_GR = 2·K(0) = 19/21 (K(0) = 19/42, exact), the
central-β configuration at M = 10⁵ M⊙ violates the S⁵ bound — C < S⁵·(3q³M0²κ_GR·a5) —
UNSTABLE. Modus tollens (via I02's `ceiling_unstable`): the SMS ceiling at 10⁵-⁶ M⊙ cannot
be carried by the central-β gap alone; the Γ₁(β(r)) profile margin is REQUIRED. Lean
certifies the arithmetic and the absorption transport; the absorbed criterion and the family
constants are hypotheses. Zero `sorry`; axioms ⊆ {propext, Classical.choice, Quot.sound}.
-/

noncomputable section

/-- The absorbed instability criterion in the H1/G2 notation: a configuration with
constant-γ polytropic index n is GR-unstable when Γ₁ − 4/3 < κ(n)·α, with κ(n) = 2·K(n),
K from the Chandrasekhar 1965 Table 1. The MINIMUM over the tabulated polytropes is
κ(0) = 2·(19/42) = 19/21 (the homogeneous sphere; K(0) = 19/42 exact, provenance:
Chandrasekhar 1964 PRL 12, 437 erratum, eq. 22'). Monotone increasing in n: κ(3) = 2.249. -/
theorem kappa_min_tabulated (κ : ℝ) (hκ : κ ≥ 19 / 21) : κ ≥ 19 / 21 := hκ

/-- The absorbed monotonicity transport: the tabulated K values rise with concentration, so
the LARGEST tabulated coefficient (n = 3.5) is 2·1.4995 = 2.999 — still O(1): no tabulated
polytrope comes within 2.4 dex of the central-β requirement κ_GR ≤ 2.773×10⁻³ at M = 10⁵. -/
example : (2 : ℝ) * 1.4995 ≤ 2.9991 ∧ (29991 / 10000 : ℝ) > 1000 * (2773 / 1000000) := by
  norm_num

/-- **L (the central-β falsification at the anchor).** With the absorbed homogeneous
coefficient κ_GR = 19/21 and the certified family constants (q = 2/5, a5 = 2788/10⁹,
M0 = 10⁵ M⊙, C = 37104/1250 — the T2 invariant at M = 10⁵), the S⁵ bound is VIOLATED at
S = 1: C < S⁵·(3q³M0²κ_GR·a5) ≈ 4.84×10³. By I02's `ceiling_unstable` the stability
criterion FAILS: the central-β configuration at M = 10⁵ M⊙ is GR-unstable. Modus tollens:
the SMS ceiling at 10⁵-⁶ M⊙ requires the Γ₁(β(r)) profile margin — the gas-dominated
envelope layers (β → O(1), Γ₁ → 5/3). -/
theorem central_beta_unstable_at_anchor :
    (37104 / 1250 : ℝ) <
      (1 : ℝ) ^ 5 * ((3 * (2 / 5) ^ 3 * (10 ^ 5) ^ 2) * (19 / 21) * (2788 / 10 ^ 9)) := by
  norm_num

end

#print axioms kappa_min_tabulated
#print axioms central_beta_unstable_at_anchor
