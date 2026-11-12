import Mathlib

/-!
# OUT-2 (KAPPA_RATELOCK) -- MUTATE: the false twin

Every theorem below is FALSE. The twin exists so the lane's certificate can be shown to bite:
if these compiled, the main file would be proving nothing. Expected: hard errors, exit != 0.

`kappa = 1/2 FITTED; not theory closed.`
-/

namespace Out2RateLockMutate

open Real

lemma pi_ne_zero_m : Real.pi ≠ 0 := ne_of_gt Real.pi_pos

/-- MU5: the circularity twin. Claims the lock DOES restate kappa = 1/2. -/
theorem lock_kappaSq_eq_quarter_FALSE : 2 / (3 * Real.pi) = (1 : ℝ) / 4 := by
  norm_num

/-- MU5b: claims the record identity is independent of kappa = 1/2. -/
theorem identity_is_independent_FALSE {a0 c G rho : ℝ} (hc : c ≠ 0) (hG : G ≠ 0) (hrho : rho ≠ 0) :
    a0 ^ 2 / (8 * Real.pi * G) = rho * c ^ 2 / (32 * Real.pi) ↔
    a0 ^ 2 / (c ^ 2 * G * rho) = 2 / (3 * Real.pi) := by
  constructor
  · intro h
    field_simp [hc, hG, hrho, pi_ne_zero_m] at h ⊢
    nlinarith
  · intro h
    field_simp [hc, hG, hrho, pi_ne_zero_m] at h ⊢
    nlinarith

/-- MU6: the vacuous twin. Claims the lock is NOT charged under G_lam (i.e. lam = 2 also works),
    which would put the lane back on the flat direction. -/
theorem lock_not_charged_FALSE {a0 c H : ℝ}
    (h1 : a0 ^ 2 = (c * H / (2 * Real.pi)) ^ 2) :
    ((2 : ℝ) * a0) ^ 2 = (c * H / (2 * Real.pi)) ^ 2 := by
  rw [← h1]
  ring

/-- MU6b: the same claim with a general lam. -/
theorem lock_scale_invariant_FALSE {a0 c H lam : ℝ}
    (h1 : a0 ^ 2 = (c * H / (2 * Real.pi)) ^ 2) :
    (lam * a0) ^ 2 = (c * H / (2 * Real.pi)) ^ 2 := by
  rw [← h1]
  ring

/-- MU8: claims kappa_lock > 1/2 (the opposite of the lane's T5). -/
theorem lock_kappa_gt_half_FALSE : (1 : ℝ) / 2 < Real.sqrt (2 / (3 * Real.pi)) := by
  have hsq : ((1 : ℝ) / 2) ^ 2 < 2 / (3 * Real.pi) := by
    rw [show ((1 : ℝ) / 2) ^ 2 = 1 / 4 by norm_num]
    field_simp [pi_ne_zero_m]
    nlinarith [Real.pi_gt_three]
  have h := Real.sqrt_lt_sqrt (show 0 ≤ ((1 : ℝ) / 2) ^ 2 by positivity) hsq
  rw [Real.sqrt_sq_eq_abs, abs_of_nonneg (by norm_num : (0 : ℝ) ≤ 1 / 2)] at h
  exact h

/-- MU9: claims the 1:1 and 2:1 windings are the same number. -/
theorem winding_two_equals_one_FALSE :
    (2 : ℝ) ^ 2 * (2 / (3 * Real.pi)) = 2 / (3 * Real.pi) := by
  ring_nf

end Out2RateLockMutate
