/-
OTA1: Lean statements for the algebra of counting the cold dark energy share once on the baryons out to turnaround,
with the cold mass beyond the fair-share R200c rescaled. They certify the algebra, not the physics, and no number or
label of the lane. TEST lane; adopts nothing.

  rescale_total        : with lambda = (T - M_c(R2)) / (M_c(r_ta) - M_c(R2)) and T = M_c(R2) + S (Mfair - M_c(R2)),
                         the rescaled mass at r_ta is T; at the rule's S = 1 it is exactly Mfair = X M_b(< r_ta).
  lambda_gt_one_iff    : at S = 1, with a positive record increment beyond R2, lambda > 1 exactly when the record
                         holds less than Mfair inside r_ta, and lambda = 1 exactly when it holds Mfair.
  tw0_lambda_one       : the zero-extra-share twin (T = M_c(r_ta)) gives lambda = 1, and then the rescaled mass equals
                         the record's at every radius beyond R2.
  continuous_at_R2     : the outer formula M_c(R2) + lambda (M_c(r) - M_c(R2)) equals the untouched inside mass at
                         r = R2, for any lambda.
  uniform_fallback_ends : the uniform-density fallback M_c(R2) + (T - M_c(R2)) (r^3 - R2^3)/(r_ta^3 - R2^3) is M_c(R2)
                         at R2 and T at r_ta.
  bracket_at_rule_slope : bracket B's M_b' = M_b(R500) + (M_b(r_ta) - M_b(R500)) I(s')/I(s) returns the record's
                         M_b(r_ta) at s' = s (I nonzero), so Mfair' = Mfair there.
  gate_reach           : a cell's label: OVER (Z < -2) is never a pass (|Z| <= 2); and with the base above the line
                         (Z_base > 2), a rule Z with 2 < Z <= Z_base has reach (Z_base - Z)/(Z_base - 2) in [0, 1).

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
-/
import Mathlib

namespace OTA1

theorem rescale_total (MR2 MT Mf S : ℝ) (hinc : MT - MR2 ≠ 0) :
    MR2 + (MR2 + S * (Mf - MR2) - MR2) / (MT - MR2) * (MT - MR2) = MR2 + S * (Mf - MR2) ∧
    (S = 1 → MR2 + (MR2 + S * (Mf - MR2) - MR2) / (MT - MR2) * (MT - MR2) = Mf) := by
  constructor
  · field_simp
    ring
  · intro hS
    subst hS
    field_simp
    ring

theorem lambda_gt_one_iff (MR2 MT Mf : ℝ) (hinc : MR2 < MT) :
    (1 < (Mf - MR2) / (MT - MR2) ↔ MT < Mf) ∧ ((Mf - MR2) / (MT - MR2) = 1 ↔ MT = Mf) := by
  have hpos : 0 < MT - MR2 := by linarith
  constructor
  · rw [one_lt_div hpos]
    constructor <;> intro h <;> linarith
  · rw [div_eq_one_iff_eq hpos.ne']
    constructor <;> intro h <;> linarith

theorem tw0_lambda_one (MR2 MT fr : ℝ) (hinc : MT - MR2 ≠ 0) :
    (MT - MR2) / (MT - MR2) = 1 ∧ MR2 + (MT - MR2) / (MT - MR2) * (fr - MR2) = fr := by
  have h1 : (MT - MR2) / (MT - MR2) = 1 := div_self hinc
  refine ⟨h1, ?_⟩
  rw [h1]
  ring

theorem continuous_at_R2 (MR2 lam : ℝ) : MR2 + lam * (MR2 - MR2) = MR2 := by
  ring

theorem uniform_fallback_ends (MR2 T R2 rta : ℝ) (h : rta ^ 3 - R2 ^ 3 ≠ 0) :
    MR2 + (T - MR2) * (R2 ^ 3 - R2 ^ 3) / (rta ^ 3 - R2 ^ 3) = MR2 ∧
    MR2 + (T - MR2) * (rta ^ 3 - R2 ^ 3) / (rta ^ 3 - R2 ^ 3) = T := by
  constructor
  · simp
  · field_simp
    ring

theorem bracket_at_rule_slope (M5 Mbt I Mf : ℝ) (hI : I ≠ 0) (hM : Mbt ≠ 0) :
    M5 + (Mbt - M5) * I / I = Mbt ∧ Mf * (M5 + (Mbt - M5) * I / I) / Mbt = Mf := by
  have h1 : M5 + (Mbt - M5) * I / I = Mbt := by
    field_simp
    ring
  refine ⟨h1, ?_⟩
  rw [h1]
  field_simp

theorem gate_reach (Z Zb : ℝ) :
    (Z < -2 → ¬ |Z| ≤ 2) ∧
    (2 < Zb → 2 < Z → Z ≤ Zb → 0 ≤ (Zb - Z) / (Zb - 2) ∧ (Zb - Z) / (Zb - 2) < 1) := by
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

end OTA1

-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
