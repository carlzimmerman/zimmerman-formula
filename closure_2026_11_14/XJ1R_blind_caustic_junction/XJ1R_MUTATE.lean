/-
XJ1R MUTATE twin: the statements of XJ1R.lean, each with one false change (a term, a sign or an inequality direction)
and the same proof script. Every theorem is false and must fail (expected: exit 1, an error in every theorem).
TEST lane; adopts nothing.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
-/
import Mathlib

namespace XJ1R_MUTATE

theorem control_reaches_reference_mut (CB CR : ℝ) (h : CB ≠ 0) :
    CR / CB * CB = CB ∧ CB - CR / CB * CB = CB - CR := by
  constructor
  · field_simp
  · field_simp

theorem exact_minus_control_outside_mut (CBi CRi CR Ctot t : ℝ) (ht : t * (Ctot - CRi) = Ctot - CBi) :
    (CBi + t * (CR - CRi)) - CR = (1 + t) * (Ctot - CR) := by
  linear_combination ht

theorem exact_factor_le_one_iff_mut (CBi CRi Ctot : ℝ) (hlt : CRi < Ctot) :
    (Ctot - CBi) / (Ctot - CRi) ≤ 1 ↔ CBi ≤ CRi := by
  rw [div_le_one (by linarith)]
  constructor <;> intro h <;> linarith

theorem cap_monotone_mut (R3 R2 rta : ℝ) (h : R3 ≤ R2) :
    min R2 rta ≤ min R3 rta ∧ min R2 rta ≤ rta :=
  ⟨min_le_min_right rta h, min_le_right _ _⟩

theorem labels_exclusive_mut (D N12 : ℝ) (hN : 0 ≤ N12) :
    ¬ (D + 2 * (2 * Real.sqrt (D * N12) + N12) < 4 ∧ D - 2 * (2 * Real.sqrt (D * N12) + N12) < 4) := by
  rintro ⟨h1, h2⟩
  have := Real.sqrt_nonneg (D * N12)
  linarith

theorem fragile_under_holds_mut (D N12 b p : ℝ) (hN : 0 ≤ N12) (hp : 0 < p)
    (hH : D + 2 * (2 * Real.sqrt (D * N12) + N12) < 4) :
    ((4 < D * b / p) ↔ ¬ (4 < D)) ↔ D * b < 4 * p := by
  have hD : ¬ (4 < D) := by
    have := Real.sqrt_nonneg (D * N12)
    intro h
    linarith
  rw [lt_div_iff₀ hp]
  tauto

theorem lane_words_exclusive_mut (D N12 : ℝ) (n : ℕ) (hN : 0 ≤ N12) :
    ¬ ((D + 2 * (2 * Real.sqrt (D * N12) + N12) < 4 ∧ n = 0) ∧ D - 2 * (2 * Real.sqrt (D * N12) + N12) > 4) ∧
    ¬ ((D + 2 * (2 * Real.sqrt (D * N12) + N12) < 4 ∧ n = 0) ∧ n = 0) := by
  constructor
  · rintro ⟨⟨h1, _⟩, h2⟩
    have := Real.sqrt_nonneg (D * N12)
    linarith
  · rintro ⟨⟨_, h0⟩, hpos⟩
    omega

end XJ1R_MUTATE

-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
