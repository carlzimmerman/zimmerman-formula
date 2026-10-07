import Mathlib

/-! # Cert 374 cube-sharpness closed forms

Certifies the arithmetic of the sharpness example in family 374
("Sharp One-Third Stability of Brenier Maps", Prop 2.2, eqs 2.3/2.5):
for b = a/2, W2(mu,nu)^2 = a b^2 and ||T_mu - T_nu||_{L2(rho)}^2 = b/2 + a b^2,
hence the closed forms a^3/4 and a(1+a^2)/4, the a = 2/5 specialisations
2/125 = 0.016 and 29/250 = 0.116 (lane T1's LP and Monte-Carlo checks), and
the sharpness amplification factor ||dT||^2/W2^2 = (1+a^2)/a^2 -> +infinity
as a -> 0 (the mechanism that makes every exponent > 1/3 fail).

This file certifies the ALGEBRA only (house practice, cf. CFG375_budget):
the mapping from these expressions to W2 and to the L2 map norm is done by
the lane scripts t1_fam374/t1_fam374_brenier_stability.py (Monte Carlo,
C1) and the paper's own derivation. No physics is certified here.
-/

noncomputable section

/-- W2(mu,nu)^2 for the cube example, b = a/2: a * b^2. -/
def w2sq (a : ℝ) : ℝ := a * (a / 2) ^ 2

/-- ||T_mu - T_nu||_{L2(rho)}^2: b/2 + a b^2 with b = a/2. -/
def mapsq (a : ℝ) : ℝ := (a / 2) / 2 + a * (a / 2) ^ 2

theorem w2sq_closed (a : ℝ) : w2sq a = a ^ 3 / 4 := by
  unfold w2sq
  ring

theorem mapsq_closed (a : ℝ) : mapsq a = a * (1 + a ^ 2) / 4 := by
  unfold mapsq
  ring

-- The paper's numbers at a = 2/5 (its own figure): W2^2 = 0.016, map^2 = 0.116.
theorem w2sq_a25 : w2sq (2 / 5 : ℝ) = (2 : ℝ) / 125 := by
  rw [w2sq_closed]
  norm_num

theorem mapsq_a25 : mapsq (2 / 5 : ℝ) = (29 : ℝ) / 250 := by
  rw [mapsq_closed]
  norm_num

-- sqrt forms, as used by the lane (W2 and the map norm).
theorem w2_a25 : Real.sqrt (w2sq (2 / 5 : ℝ)) = Real.sqrt (2 / 125 : ℝ) := by
  rw [w2sq_a25]

theorem mapnorm_a25 : Real.sqrt (mapsq (2 / 5 : ℝ)) = Real.sqrt (29 / 250 : ℝ) := by
  rw [mapsq_a25]

-- Sharpness mechanism: ||dT||^2 / W2^2 = (1 + a^2)/a^2 -> +infinity as a -> 0.
theorem sharp_ratio (a : ℝ) (ha : a ≠ 0) : mapsq a / w2sq a = (1 + a ^ 2) / a ^ 2 := by
  rw [mapsq_closed, w2sq_closed]
  field_simp [ha] <;> ring

-- Amplification in norm form: ||dT|| >= (1/a) W2 (so W2^(1/3) control is
-- impossible at fixed constants: the map change grows like 1/a while W2 ~ a^(3/2)).
theorem amplification (a : ℝ) (ha : 0 < a) :
    (1 / a) * Real.sqrt (w2sq a) ≤ Real.sqrt (mapsq a) := by
  have hsq : (1 / a) ^ 2 * w2sq a ≤ mapsq a := by
    rw [mapsq_closed, w2sq_closed]
    field_simp [ne_of_gt ha] <;> nlinarith [sq_nonneg a]
  have hw : 0 ≤ w2sq a := by
    rw [w2sq_closed]
    positivity
  have hm : 0 ≤ mapsq a := by
    rw [mapsq_closed]
    positivity
  have h1 : 0 ≤ (1 / a) * Real.sqrt (w2sq a) := by
    exact mul_nonneg (by positivity) (Real.sqrt_nonneg _)
  have hw2 : (Real.sqrt (w2sq a)) ^ 2 = w2sq a := by
    rw [pow_two, Real.mul_self_sqrt hw]
  have hm2 : (Real.sqrt (mapsq a)) ^ 2 = mapsq a := by
    rw [pow_two, Real.mul_self_sqrt hm]
  have hsq2 : ((1 / a) * Real.sqrt (w2sq a)) ^ 2 ≤ (Real.sqrt (mapsq a)) ^ 2 := by
    rw [mul_pow, hw2, hm2]
    exact hsq
  calc
    (1 / a) * Real.sqrt (w2sq a) = Real.sqrt (((1 / a) * Real.sqrt (w2sq a)) ^ 2) := by
      rw [Real.sqrt_sq h1]
    _ ≤ Real.sqrt ((Real.sqrt (mapsq a)) ^ 2) := Real.sqrt_le_sqrt hsq2
    _ = Real.sqrt (mapsq a) := by rw [Real.sqrt_sq (Real.sqrt_nonneg _)]

end