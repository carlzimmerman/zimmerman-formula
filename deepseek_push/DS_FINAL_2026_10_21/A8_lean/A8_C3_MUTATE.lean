/-
A8 / C3 — MUTATION FILE.  THIS FILE IS SUPPOSED TO FAIL TO COMPILE.

Two deliberate mutations of the C3 certificates:

  M1. `gCanon_le_gQuad_MUTANT`  — the ordering direction reversed:
      claims `g_c <= g_q` for all gN, a0 > 0.  FALSE.

  M2. `gCanon_eq_gQuad_MUTANT`  — the two laws identified:
      claims `g_c = g_q` for all gN, a0 > 0.  FALSE.

The supporting lemmas are the real, proven ones (copied from
`A8_C3_law_ordering.lean`); only the mutant statements are false.  The point is
that the C3 proof has teeth: if the ordering were reversed, the same proof
script that proves `gQuad_lt_gCanon` cannot close the goal, and Lean rejects the
file.  See MUTATE.md for the captured errors and a numerical counterexample.

Numerical witness (python, not a proof): gN = 1, a0 = 1 gives
  g_c = 1.6180339887...,  g_q = 1.4142135623...,  so g_c <= g_q is false and
  g_c = g_q is false.
-/
import Mathlib

namespace A8

noncomputable def gCanon (gN a0 : ℝ) : ℝ :=
  gN / 2 * (1 + Real.sqrt (1 + 4 * a0 / gN))

noncomputable def gQuad (gN a0 : ℝ) : ℝ := Real.sqrt (gN ^ 2 + a0 * gN)

theorem gCanon_form {gN a0 : ℝ} (hgN : 0 < gN) :
    gCanon gN a0 = gN / 2 + Real.sqrt (gN ^ 2 / 4 + a0 * gN) := by
  unfold gCanon
  have harg : gN ^ 2 / 4 + a0 * gN = (gN / 2) ^ 2 * (1 + 4 * a0 / gN) := by
    field_simp
    ring
  rw [harg, Real.sqrt_mul (by positivity : (0 : ℝ) ≤ (gN / 2) ^ 2),
    Real.sqrt_sq (by positivity : (0 : ℝ) ≤ gN / 2)]
  ring

theorem gCanon_gt_gN {gN a0 : ℝ} (hgN : 0 < gN) (ha0 : 0 < a0) :
    gN < gCanon gN a0 := by
  rw [gCanon_form hgN]
  have h1 : gN / 2 < Real.sqrt (gN ^ 2 / 4 + a0 * gN) := by
    rw [Real.lt_sqrt (by positivity)]
    nlinarith
  linarith

theorem gCanon_root {gN a0 : ℝ} (hgN : 0 < gN) (ha0 : 0 < a0) :
    gCanon gN a0 ^ 2 = gN * (gCanon gN a0 + a0) := by
  rw [gCanon_form hgN]
  have hs : Real.sqrt (gN ^ 2 / 4 + a0 * gN) ^ 2 = gN ^ 2 / 4 + a0 * gN :=
    Real.sq_sqrt (by positivity)
  nlinarith [hs]

theorem gQuad_root {gN a0 : ℝ} (hgN : 0 < gN) (ha0 : 0 < a0) :
    gQuad gN a0 ^ 2 = gN ^ 2 + a0 * gN := by
  unfold gQuad
  exact Real.sq_sqrt (by positivity)

theorem gCanon_sq_sub_gQuad_sq {gN a0 : ℝ} (hgN : 0 < gN) (ha0 : 0 < a0) :
    gCanon gN a0 ^ 2 - gQuad gN a0 ^ 2 = gN * (gCanon gN a0 - gN) := by
  rw [gCanon_root hgN ha0, gQuad_root hgN ha0]
  ring

/-! ## M1: the reversed ordering — FALSE -/

theorem gCanon_le_gQuad_MUTANT {gN a0 : ℝ} (hgN : 0 < gN) (ha0 : 0 < a0) :
    gCanon gN a0 ≤ gQuad gN a0 := by
  have hcgt : gN < gCanon gN a0 := gCanon_gt_gN hgN ha0
  have hsq : gCanon gN a0 ^ 2 ≤ gQuad gN a0 ^ 2 := by
    have h := gCanon_sq_sub_gQuad_sq hgN ha0
    nlinarith [h, hcgt, hgN]
  have h1 : 0 ≤ gQuad gN a0 := by unfold gQuad; positivity
  have h2 : 0 ≤ gCanon gN a0 := le_of_lt (lt_trans hgN hcgt)
  have habs := sq_le_sq.mp hsq
  rw [abs_of_nonneg h1, abs_of_nonneg h2] at habs
  exact habs

/-! ## M2: the two laws identified — FALSE -/

theorem gCanon_eq_gQuad_MUTANT {gN a0 : ℝ} (hgN : 0 < gN) (ha0 : 0 < a0) :
    gCanon gN a0 = gQuad gN a0 := by
  have hcgt : gN < gCanon gN a0 := gCanon_gt_gN hgN ha0
  have h := gCanon_sq_sub_gQuad_sq hgN ha0
  have hsq : gCanon gN a0 ^ 2 = gQuad gN a0 ^ 2 := by
    nlinarith [h, hcgt, hgN]
  have h1 : 0 ≤ gQuad gN a0 := by unfold gQuad; positivity
  have h2 : 0 ≤ gCanon gN a0 := le_of_lt (lt_trans hgN hcgt)
  have habs := sq_eq_sq_iff_eq_or_eq_neg.mp hsq
  rcases habs with h3 | h3
  · exact h3
  · linarith

end A8
