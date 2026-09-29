import Mathlib

/-!
# AH8 -- Lean certificate of the arithmetic of the "closest formula" audit

The formula audited (real_research/reviews/alpha_12pi_identity_audit_2026.py):
    alpha^-1 + alpha - 12 pi alpha^2  =  4 Z^2 + 3,   Z^2 = 32 pi / 3,  i.e.  RHS = 128 pi/3 + 3,
with alpha^-1 = 137.035999177 (the CODATA-2022 central value, taken here as an exact decimal INPUT, not derived).

CERTIFIED (interval arithmetic with Mathlib's 20-digit bounds on pi; no numerics outside Lean):
* `bare_gap`: the BARE claim 128 pi/3 + 3 exceeds 137.035999177 by an amount in (0.0052, 0.0054): a relative miss of about 3.9e-5, i.e. about 4 significant digits, NOT 8.
* `residual_bounds`: the full identity's left minus right side lies in (2.4e-6, 2.5e-6) (relative ~1.8e-8): the identity does NOT hold exactly; it holds to ~1.8e-8.
* `exact_coefficient_bounds`: the coefficient C that would make 1/alpha + alpha - C alpha^2 = 128 pi/3 + 3 exactly lies in (37.74, 37.75).
* `twelve_pi_is_not_exact`: 12 pi < 37.70, so C exceeds 12 pi by more than 0.1%: the "12 pi" is not the exact coefficient.
* `amplification`: the whole term 12 pi alpha^2 is below 2.1e-3, less than 1.6e-5 of the total 137, so a 0.12% error in it shifts the sum by about 2e-8.
NOT CERTIFIED / NOT CLAIMED: that alpha equals any expression (it does not follow from anything); the physical meaning of the numbers; that alpha^-1 = 137.035999177 is the true value
(a recalled measured value taken as an exact decimal input). This certifies ARITHMETIC ABOUT A FORMULA, not a derivation of alpha. Zero sorry; axioms printed below.
-/

open Real

/-- alpha^-1 as an exact decimal input (CODATA 2022 central value). -/
noncomputable def ainv : ℝ := 137.035999177

theorem bare_gap : 0.0052 < 128 * π / 3 + 3 - ainv ∧ 128 * π / 3 + 3 - ainv < 0.0054 := by
  have h1 := Real.pi_gt_d20
  have h2 := Real.pi_lt_d20
  unfold ainv
  constructor <;> linarith

theorem residual_bounds :
    2.4e-6 < (ainv + 1 / ainv - 12 * π * (1 / ainv) ^ 2) - (128 * π / 3 + 3) ∧
    (ainv + 1 / ainv - 12 * π * (1 / ainv) ^ 2) - (128 * π / 3 + 3) < 2.5e-6 := by
  have h1 := Real.pi_gt_d20
  have h2 := Real.pi_lt_d20
  unfold ainv
  constructor <;> (norm_num; nlinarith [h1, h2])

theorem exact_coefficient_bounds :
    37.74 < (ainv + 1 / ainv - (128 * π / 3 + 3)) / (1 / ainv) ^ 2 ∧
    (ainv + 1 / ainv - (128 * π / 3 + 3)) / (1 / ainv) ^ 2 < 37.75 := by
  have h1 := Real.pi_gt_d20
  have h2 := Real.pi_lt_d20
  unfold ainv
  constructor <;> (norm_num; nlinarith [h1, h2])

theorem twelve_pi_is_not_exact : 12 * π < 37.70 ∧ 37.74 / (12 * π) > 1.001 := by
  have h1 := Real.pi_gt_d20
  have h2 := Real.pi_lt_d20
  constructor
  · linarith
  · rw [gt_iff_lt, lt_div_iff₀ (by positivity)]
    nlinarith

theorem amplification : 12 * π * (1 / ainv) ^ 2 < 2.1e-3 ∧ 12 * π * (1 / ainv) ^ 2 / ainv < 1.6e-5 := by
  have h1 := Real.pi_gt_d20
  have h2 := Real.pi_lt_d20
  unfold ainv
  constructor <;> (norm_num; nlinarith [h1, h2])

#print axioms bare_gap
#print axioms residual_bounds
#print axioms exact_coefficient_bounds
#print axioms twelve_pi_is_not_exact
#print axioms amplification
