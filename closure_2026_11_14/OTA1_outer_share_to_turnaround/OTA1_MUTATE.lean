/-
OTA1 MUTATE twin: the statements of OTA1.lean with one sign, term or direction changed. Every theorem is false and
must fail (expected: exit 1, an error in every theorem). TEST lane; adopts nothing.
kappa = 1/2 FITTED; not theory closed.
-/
import Mathlib

namespace OTA1_MUTATE

theorem rescale_total_mut (MR2 MT Mf S : ℝ) (hinc : MT - MR2 ≠ 0) :
    MR2 + (MR2 + S * (Mf - MR2) - MR2) / (MT - MR2) * (MT - MR2) = MR2 + S * (Mf - MR2) ∧
    (S = 1 → MR2 + (MR2 + S * (Mf - MR2) - MR2) / (MT - MR2) * (MT - MR2) = Mf + MR2) := by
  constructor
  · field_simp
    ring
  · intro hS
    subst hS
    field_simp
    ring

theorem lambda_gt_one_iff_mut (MR2 MT Mf : ℝ) (hinc : MR2 < MT) :
    (1 < (Mf - MR2) / (MT - MR2) ↔ Mf < MT) ∧ ((Mf - MR2) / (MT - MR2) = 1 ↔ MT = Mf) := by
  have hpos : 0 < MT - MR2 := by linarith
  constructor
  · rw [one_lt_div hpos]
    constructor <;> intro h <;> linarith
  · rw [div_eq_one_iff_eq hpos.ne']
    constructor <;> intro h <;> linarith

theorem tw0_lambda_one_mut (MR2 MT fr : ℝ) (hinc : MT - MR2 ≠ 0) :
    (MT - MR2) / (MT - MR2) = 1 ∧ MR2 + (MT - MR2) / (MT - MR2) * (fr - MR2) = fr + MR2 := by
  have h1 : (MT - MR2) / (MT - MR2) = 1 := div_self hinc
  refine ⟨h1, ?_⟩
  rw [h1]
  ring

theorem continuous_at_R2_mut (MR2 lam : ℝ) : MR2 + lam * (MR2 - MR2) = MR2 + lam := by
  ring

theorem uniform_fallback_ends_mut (MR2 T R2 rta : ℝ) (h : rta ^ 3 - R2 ^ 3 ≠ 0) :
    MR2 + (T - MR2) * (R2 ^ 3 - R2 ^ 3) / (rta ^ 3 - R2 ^ 3) = MR2 ∧
    MR2 + (T - MR2) * (rta ^ 3 - R2 ^ 3) / (rta ^ 3 - R2 ^ 3) = T + MR2 := by
  constructor
  · simp
  · field_simp
    ring

theorem bracket_at_rule_slope_mut (M5 Mbt I Mf : ℝ) (hI : I ≠ 0) (hM : Mbt ≠ 0) :
    M5 + (Mbt - M5) * I / I = Mbt + M5 ∧ Mf * (M5 + (Mbt - M5) * I / I) / Mbt = Mf := by
  have h1 : M5 + (Mbt - M5) * I / I = Mbt := by
    field_simp
    ring
  refine ⟨h1, ?_⟩
  rw [h1]
  field_simp

theorem gate_reach_mut (Z Zb : ℝ) :
    (Z < -2 → ¬ |Z| ≤ 2) ∧
    (2 < Zb → 2 < Z → Z ≤ Zb → 1 ≤ (Zb - Z) / (Zb - 2) ∧ (Zb - Z) / (Zb - 2) < 1) := by
  constructor
  · intro h habs
    have := (abs_le.mp habs).1
    linarith
  · intro hb hz hzb
    have hp : 0 < Zb - 2 := by linarith
    constructor
    · apply div_nonneg <;> linarith
    · rw [div_lt_one hp]
      linarith

end OTA1_MUTATE

-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
