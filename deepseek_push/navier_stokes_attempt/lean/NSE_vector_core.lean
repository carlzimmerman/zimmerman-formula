import Mathlib

/-!
# NSE vector core (SPEC_A_LEAN.md, file 2): the sup-argument algebra

Certifies the pointwise algebraic core of the convective-term bookkeeping
behind the sup estimate:
- the sum-swap identity behind `u·((u·∇)u) = ½(u·∇)|u|²` (the chain-rule half
  is calculus — cited, not certified here);
- `(ω×u) ⊥ u` — the nondissipative part of the convective term, the reason the
  drag-only mechanism can be capped pointwise;
- the superset-bookkeeping bilinearity `⟪u+v, u+v⟫ = ⟪u,u⟫ + 2⟪u,v⟫ + ⟪v,v⟫`.

Algebra only — physics scope as in N00_CAMPAIGN.md; zero `sorry`,
Mathlib 4.34.0-rc2.
-/

open scoped RealInnerProductSpace
open scoped EuclideanSpace
open scoped Matrix
open WithLp

noncomputable section

/-!
### Blocker (named: SPEC_A file-2 statements are not elaboratable on this toolchain)

The theorem statements as printed in SPEC_A_LEAN.md cannot be written down in
Mathlib 4.34.0-rc2:

1. `adv_energy_swap (u du : Fin 3 → Fin 3 → ℝ)` makes `u i : Fin 3 → ℝ`, so the
   term `u i * (∑ j, u j * du j i)` fails with
   `failed to synthesize instance of HMul (Fin 3 → ℝ) ℝ`.  For `u i` to be a
   scalar the velocity field must be typed `u : Fin 3 → ℝ`.
2. `EuclideanSpace ℝ 3` fails with `failed to synthesize instance of OfNat
   (Type) 3` (numerals are not types in this Mathlib — Mathlib itself spells
   the space `EuclideanSpace ℝ (Fin 3)`).
3. There is no EuclideanSpace-level cross-product notation `×` and no
   `Real.inner_cross_self`: `×` elaborates as the type-theoretic `Prod`, and the
   only cross-product notation is `scoped[Matrix] ⨯₃` on `Fin 3 → ℝ`
   (`Mathlib/LinearAlgebra/CrossProduct.lean`).  On EuclideanSpace the cross
   product must be built through the `WithLp` bridge (`ofLp`/`toLp`), as below.

The same mathematics with the minimal well-typed statements (SPEC contents
unchanged except the typing fix; names carry a `_fix` suffix to mark them):
-/

/-- Pointwise algebraic core of `u·((u·∇)u) = ½(u·∇)|u|²` (chain-rule half is
calculus — cited, not certified here).  SPEC_A statement with the required
typing fix `u : Fin 3 → ℝ` (see blocker note above). -/
theorem adv_energy_swap_fix (u : Fin 3 → ℝ) (du : Fin 3 → Fin 3 → ℝ) :
    (∑ i, u i * (∑ j, u j * du j i)) = (∑ j, u j * (∑ i, u i * du j i)) := by
  simp_rw [Finset.mul_sum]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro j _
  apply Finset.sum_congr rfl
  intro i _
  ring

/-- `(ω×u) ⊥ u` on `EuclideanSpace ℝ (Fin 3)`, the nondissipative part of the
convective term.  SPEC_A statement, with the `(Fin 3)` spelling and the
`ofLp`/`toLp` cross-product bridge (see blocker note above); the underlying
Mathlib lemma is `dot_self_cross`. -/
theorem inner_cross_zero_fix (u v : EuclideanSpace ℝ (Fin 3)) :
    ⟪u, toLp 2 ((u.ofLp) ⨯₃ (v.ofLp))⟫ = 0 := by
  rw [EuclideanSpace.inner_eq_star_dotProduct]
  rw [ofLp_toLp]
  rw [star_trivial]
  rw [dotProduct_comm]
  exact dot_self_cross u.ofLp v.ofLp

/-- Superset-bookkeeping bilinearity for the sup estimate.  SPEC_A statement,
with the `(Fin 3)` spelling (see blocker note above). -/
theorem norm_sq_add_cross_fix (u v : EuclideanSpace ℝ (Fin 3)) :
    ⟪u + v, u + v⟫ = ⟪u,u⟫ + 2*⟪u,v⟫ + ⟪v,v⟫ := by
  rw [inner_add_left, inner_add_right, inner_add_right]
  rw [real_inner_comm u v]
  ring

end

#print axioms adv_energy_swap_fix
#print axioms inner_cross_zero_fix
#print axioms norm_sq_add_cross_fix