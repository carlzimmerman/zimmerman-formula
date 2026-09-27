import Mathlib
open Real

/- G2a -/
theorem step1_gen (r : ℝ) (hr : r ≠ 0) (F : ℝ → ℝ) :
    ∫ mu in (-1:ℝ)..1, F (r * mu) = (1/r) * ∫ v in (-r:ℝ)..r, F v := by
  rw [intervalIntegral.integral_comp_mul_left F hr, smul_eq_mul, inv_eq_one_div, mul_neg_one, mul_one]

theorem step1 (r : ℝ) (hr : 0 < r) (H : ℝ → ℝ → ℝ) :
    ∫ mu in (-1:ℝ)..1, H (r * Real.sqrt (1 - mu ^ 2)) (r * mu)
      = (1/r) * ∫ v in (-r:ℝ)..r, H (Real.sqrt (r ^ 2 - v ^ 2)) v := by
  have hsqrt : ∀ mu : ℝ, Real.sqrt (r ^ 2 - (r * mu) ^ 2) = r * Real.sqrt (1 - mu ^ 2) := by
    intro mu
    rw [show r ^ 2 - (r * mu) ^ 2 = r ^ 2 * (1 - mu ^ 2) from by ring,
        Real.sqrt_mul (sq_nonneg r) (1 - mu ^ 2), Real.sqrt_sq_eq_abs,
        abs_eq_self.mpr hr.le]
  have key := step1_gen r (ne_of_gt hr) (fun v => H (Real.sqrt (r ^ 2 - v ^ 2)) v)
  simp only [show ∀ mu : ℝ, H (r * Real.sqrt (1 - mu ^ 2)) (r * mu)
      = H (Real.sqrt (r ^ 2 - (r * mu) ^ 2)) (r * mu) from by
      intro mu; rw [hsqrt mu]]
  exact key

/- LR3: G1 -- first-flight moment values, polynomial 1D certificates.
  Mechanical sympy derivation (LR3_m05_moments_lean.py R0) cross-checks the four
  rationals: chord 3/4, E[int r^2 ds] = 5/12, E[int r^4 ds] = 17/60 (M05's table
  entry 1/4 is a polynomial-coefficient bug, audited by M05B),
  E[int r^6 ds] = 149/700 (M05's uncertified candidate, now CERTIFIED). -/
theorem val_chord : ∫ u in (0:ℝ)..1, ((3:ℝ) * u ^ 1 + (-3:ℝ) * u ^ 3) = ((3:ℚ)/4 : ℝ) := by
  rw [intervalIntegral.integral_add (f := fun u => (3:ℝ)*u^1) (g := fun u => (-3:ℝ)*u^3)
      (Continuous.intervalIntegrable (by fun_prop) _ _)
      (Continuous.intervalIntegrable (by fun_prop) _ _),
      intervalIntegral.integral_const_mul, intervalIntegral.integral_const_mul,
      integral_pow, integral_pow]
  norm_num

theorem val_I1 : ∫ u in (0:ℝ)..1, ((1:ℝ) * u ^ 1 + (1:ℝ) * u ^ 3 + (-2:ℝ) * u ^ 5) = ((5:ℚ)/12 : ℝ) := by
  rw [intervalIntegral.integral_add (f := fun u => (1:ℝ)*u^1 + (1:ℝ)*u^3) (g := fun u => (-2:ℝ)*u^5)
      (Continuous.intervalIntegrable (by fun_prop) _ _)
      (Continuous.intervalIntegrable (by fun_prop) _ _)]
  rw [intervalIntegral.integral_add (f := fun u => (1:ℝ)*u^1) (g := fun u => (1:ℝ)*u^3)
      (Continuous.intervalIntegrable (by fun_prop) _ _)
      (Continuous.intervalIntegrable (by fun_prop) _ _),
      intervalIntegral.integral_const_mul, intervalIntegral.integral_const_mul,
      intervalIntegral.integral_const_mul, integral_pow, integral_pow, integral_pow]
  norm_num

theorem val_I2 : ∫ u in (0:ℝ)..1, ((3/5:ℝ) * u ^ 1 + (1/5:ℝ) * u ^ 3 + (4/5:ℝ) * u ^ 5 + (-8/5:ℝ) * u ^ 7)
    = ((17:ℚ)/60 : ℝ) := by
  rw [intervalIntegral.integral_add (f := fun u => (3/5:ℝ)*u^1 + (1/5:ℝ)*u^3 + (4/5:ℝ)*u^5)
      (g := fun u => (-8/5:ℝ)*u^7)
      (Continuous.intervalIntegrable (by fun_prop) _ _)
      (Continuous.intervalIntegrable (by fun_prop) _ _)]
  rw [intervalIntegral.integral_add (f := fun u => (3/5:ℝ)*u^1 + (1/5:ℝ)*u^3)
      (g := fun u => (4/5:ℝ)*u^5)
      (Continuous.intervalIntegrable (by fun_prop) _ _)
      (Continuous.intervalIntegrable (by fun_prop) _ _)]
  rw [intervalIntegral.integral_add (f := fun u => (3/5:ℝ)*u^1) (g := fun u => (1/5:ℝ)*u^3)
      (Continuous.intervalIntegrable (by fun_prop) _ _)
      (Continuous.intervalIntegrable (by fun_prop) _ _),
      intervalIntegral.integral_const_mul, intervalIntegral.integral_const_mul,
      intervalIntegral.integral_const_mul, intervalIntegral.integral_const_mul,
      integral_pow, integral_pow, integral_pow, integral_pow]
  norm_num

theorem val_I3 : ∫ u in (0:ℝ)..1, ((3/7:ℝ) * u ^ 1 + (3/35:ℝ) * u ^ 3 + (6/35:ℝ) * u ^ 5 + (24/35:ℝ) * u ^ 7 + (-48/35:ℝ) * u ^ 9)
    = ((149:ℚ)/700 : ℝ) := by
  rw [intervalIntegral.integral_add (f := fun u => (3/7:ℝ)*u^1 + (3/35:ℝ)*u^3 + (6/35:ℝ)*u^5 + (24/35:ℝ)*u^7)
      (g := fun u => (-48/35:ℝ)*u^9)
      (Continuous.intervalIntegrable (by fun_prop) _ _)
      (Continuous.intervalIntegrable (by fun_prop) _ _)]
  rw [intervalIntegral.integral_add (f := fun u => (3/7:ℝ)*u^1 + (3/35:ℝ)*u^3 + (6/35:ℝ)*u^5)
      (g := fun u => (24/35:ℝ)*u^7)
      (Continuous.intervalIntegrable (by fun_prop) _ _)
      (Continuous.intervalIntegrable (by fun_prop) _ _)]
  rw [intervalIntegral.integral_add (f := fun u => (3/7:ℝ)*u^1 + (3/35:ℝ)*u^3)
      (g := fun u => (6/35:ℝ)*u^5)
      (Continuous.intervalIntegrable (by fun_prop) _ _)
      (Continuous.intervalIntegrable (by fun_prop) _ _)]
  rw [intervalIntegral.integral_add (f := fun u => (3/7:ℝ)*u^1) (g := fun u => (3/35:ℝ)*u^3)
      (Continuous.intervalIntegrable (by fun_prop) _ _)
      (Continuous.intervalIntegrable (by fun_prop) _ _),
      intervalIntegral.integral_const_mul, intervalIntegral.integral_const_mul,
      intervalIntegral.integral_const_mul, intervalIntegral.integral_const_mul,
      intervalIntegral.integral_const_mul, integral_pow, integral_pow, integral_pow,
      integral_pow, integral_pow]
  norm_num


#print axioms val_chord
#print axioms val_I1
#print axioms val_I2
#print axioms val_I3
