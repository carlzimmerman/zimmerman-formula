import Mathlib
import Mathlib.Tactic

/-
  AS066 -- Horizon coefficient comparison without a theorem leap (Lean 4 certificate).

  Coefficients (framework CORE cell, a0 = kappa c sqrt(G rho_Lambda)):
    kappa_h = sqrt(8 pi/3)/(2 pi)   the horizon-thermodynamic form a0 = c H/(2 pi)
                                    with H^2 = 8 pi G rho_Lambda/3 (same-G reading);
    kappa_Z = 1/2                   the adopted framework coefficient.

  Formalized content:
    A  kappa_h^2 = 2/(3 pi)                              (exact square identity)
    B  0 < kappa_h                                       (positivity)
    C  (1/kappa_h)^2 = 3 pi/2                            (reciprocal square)
    D  (kappa_Z/kappa_h)^2 = 3 pi/8                      (exact squared ratio)
    E  kappa_Z/kappa_h = sqrt(3 pi/8)                    (exact ratio)
    F  kappa_h != 1/2                                    (the coefficients differ; equality
                                                          would force pi = 8/3 rational)
    G  NOT exists q : Q, (q : R) = 1/kappa_h             (reciprocal not rational:
                                                          3 pi/2 is not a rational square)
    H  NOT exists n : N, (n : R) = 1/kappa_h             (channel integrality exclusion:
                                                          kappa_h is not 1/n for integer n)
    I  OR-composed two-channel response, per-channel engagement p(Y) = lambda*Y:
       1 - (1 - lambda*Y)^2 = 2*lambda*Y - lambda^2*Y^2  (exact polynomial identity)
    J  (1-(1-lambda*Y)^2)/Y = 2*lambda - lambda^2*Y  for Y != 0
       (the deep ratio; Y -> 0 limit is the deep slope 2*lambda, i.e.
        kappa(lambda) = 1/(2 lambda) in the deep matching)
    K  kappa_h = 1/(2 * (1/(2*kappa_h)))                 (matching-lambda identity of the
       negative control: lambda* = 1/(2 kappa_h) reproduces the horizon coefficient)
-/

noncomputable section
open Real

/-- Horizon coefficient: kappa_h = sqrt(8 pi/3)/(2 pi). -/
def kappa_h : ℝ := Real.sqrt (8 * Real.pi / 3) / (2 * Real.pi)

/-- Adopted framework coefficient: kappa_Z = 1/2. -/
def kappa_Z : ℝ := 1 / 2

/- A: exact square identity. -/
theorem kappa_h_sq : kappa_h ^ 2 = 2 / (3 * Real.pi) := by
  unfold kappa_h
  rw [div_pow]
  rw [Real.sq_sqrt (by positivity : (0 : ℝ) ≤ 8 * Real.pi / 3)]
  field_simp [Real.pi_pos.ne']; norm_num

/- B: positivity. -/
theorem kappa_h_pos : 0 < kappa_h := by
  unfold kappa_h
  exact div_pos ((Real.sqrt_pos).2 (by positivity : (0 : ℝ) < 8 * Real.pi / 3))
    (mul_pos (by norm_num) Real.pi_pos)

theorem kappa_h_ne_zero : kappa_h ≠ 0 := ne_of_gt kappa_h_pos

/- C: reciprocal square. -/
theorem inv_kappa_h_sq : (1 / kappa_h) ^ 2 = 3 * Real.pi / 2 := by
  rw [div_pow, one_pow]
  rw [kappa_h_sq]
  field_simp [Real.pi_pos.ne']

/- D: squared ratio. -/
theorem kappa_ratio_sq : (kappa_Z / kappa_h) ^ 2 = 3 * Real.pi / 8 := by
  unfold kappa_Z
  rw [div_pow]
  have h1 : (1 / 2 : ℝ) ^ 2 = 1 / 4 := by norm_num
  rw [h1, kappa_h_sq]
  field_simp [Real.pi_pos.ne']; norm_num

/- E: exact ratio (both sides nonnegative, sqrt by positivity). -/
theorem kappa_ratio : kappa_Z / kappa_h = Real.sqrt (3 * Real.pi / 8) := by
  have hsq : (kappa_Z / kappa_h) ^ 2 = (Real.sqrt (3 * Real.pi / 8)) ^ 2 := by
    rw [kappa_ratio_sq]
    rw [Real.sq_sqrt (show (0 : ℝ) ≤ 3 * Real.pi / 8 by positivity)]
  have hpos : 0 ≤ kappa_Z / kappa_h := by
    unfold kappa_Z
    exact div_nonneg (by norm_num) (le_of_lt kappa_h_pos)
  have hposes : 0 ≤ Real.sqrt (3 * Real.pi / 8) := Real.sqrt_nonneg _
  exact (sq_eq_sq_iff_eq_or_eq_neg.mp hsq).elim (fun h => h) (fun h => by linarith)

/- F: the coefficients differ (pi irrationality, i.e. pi is not 8/3). -/
theorem kappa_h_ne_half : kappa_h ≠ 1 / 2 := by
  intro hh
  have hsq : (1 / 2 : ℝ) ^ 2 = 2 / (3 * Real.pi) := by
    rw [← hh]
    exact kappa_h_sq
  have h8 : 3 * Real.pi = 8 := by
    field_simp [Real.pi_pos.ne'] at hsq
    linarith [hsq]
  have hpi : Real.pi = 8 / 3 := by
    rw [eq_div_iff (by norm_num : (3 : ℝ) ≠ 0)]
    simpa [mul_comm] using h8
  exact irrational_pi ⟨(8 / 3 : ℚ), by norm_num; exact hpi.symm⟩

/- G: the reciprocal is not rational. -/
theorem inv_kappa_h_not_rational : ¬ ∃ q : ℚ, (q : ℝ) = 1 / kappa_h := by
  rintro ⟨q, hq⟩
  have hq2 : (q : ℝ) ^ 2 = 3 * Real.pi / 2 := by
    rw [hq]
    exact inv_kappa_h_sq
  have hpi : Real.pi = (2 * (q : ℝ) ^ 2) / 3 := by
    rw [eq_div_iff (by norm_num : (3 : ℝ) ≠ 0)]
    nlinarith [hq2]
  exact irrational_pi ⟨q ^ 2 * 2 / 3, by
    norm_num
    linarith [hpi]⟩

/- H: the reciprocal is not a natural number (channel integrality exclusion). -/
theorem inv_kappa_h_not_nat : ¬ ∃ n : ℕ, (n : ℝ) = 1 / kappa_h := by
  rintro ⟨n, hn⟩
  exact inv_kappa_h_not_rational ⟨(n : ℚ), by exact_mod_cast hn⟩

/- I: OR-composed two-channel response with per-channel linear coefficient lambda:
     exact polynomial identity (the deep slope is 2*lambda). -/
theorem or2_expansion (lambda Y : ℝ) :
    1 - (1 - lambda * Y) ^ 2 = 2 * lambda * Y - lambda ^ 2 * Y ^ 2 := by
  ring

/- J: the deep coefficient of the OR-composed two-channel response.
     With per-channel engagement p(Y) = lambda*Y the deep ratio is
     mu(Y)/Y = 2*lambda - lambda^2*Y, whose Y -> 0 limit is the deep slope 2*lambda
     (the polynomial identity I plus this ratio are the premise-level objects of the
     negative control: kappa(lambda) = 1/(2 lambda)). -/
theorem or2_deep_ratio (lambda Y : ℝ) (hY : Y ≠ 0) :
    (1 - (1 - lambda * Y) ^ 2) / Y = 2 * lambda - lambda ^ 2 * Y := by
  rw [or2_expansion]
  field_simp [hY]

/- K: matching-lambda identity of the negative control. -/
theorem matching_lambda_coefficient : kappa_h = 1 / (2 * (1 / (2 * kappa_h))) := by
  field_simp [kappa_h_ne_zero]

end
