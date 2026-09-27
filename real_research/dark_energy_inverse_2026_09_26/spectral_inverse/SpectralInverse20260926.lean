import Mathlib

/-! Algebraic inverse/identifiability statements for the supplied spectral
lapse sector. No continuum eigenvalue, full-action, measured-G or cosmological
observational theorem is assumed or certified. -/
namespace SpectralInverse20260926

theorem inverse_lapse_equation (A b y d : ℝ) (hy : y ≠ 0)
    (hA : A = -4 * b * d / y) : A * y + 4 * b * d = 0 := by
  rw [hA]
  field_simp
  ring

theorem inverse_global_scale (b c y d : ℝ) (hc : c ≠ 0) (hy : y ≠ 0) :
    -4 * b * (c * d) / (c * y) = -4 * b * d / y := by
  field_simp

theorem vacuum_density_shift (ell q L rho shift : ℝ) :
    -ell * q ^ 2 + (L + shift) + (rho - shift) =
      -ell * q ^ 2 + L + rho := by ring

theorem same_proper_expansion (ell H : ℝ) (he : ell ≠ 0) :
    -ell * (-H / ell) = H := by field_simp

theorem same_observations_family (ell H rho0 b J : ℝ) (he : ell ≠ 0) :
    -ell * (-H / ell) ^ 2 + (H ^ 2 / ell - rho0) +
      (rho0 + b * J) = b * J := by
  field_simp
  ring

theorem distinct_couplings_distinct_vacuum (ell1 ell2 H rho0 : ℝ)
    (h1 : 0 < ell1) (h12 : ell1 < ell2) (hH : 0 < H) :
    H ^ 2 / ell2 - rho0 < H ^ 2 / ell1 - rho0 := by
  have h2 : 0 < ell2 := lt_trans h1 h12
  have hh : 0 < H ^ 2 := sq_pos_of_pos hH
  have hdiv : H ^ 2 / ell2 < H ^ 2 / ell1 := by
    apply (div_lt_div_iff₀ h2 h1).2
    exact mul_lt_mul_of_pos_left h12 hh
  linarith

theorem constant_slice_slope (b J1 J2 rho1 rho2 offset : ℝ)
    (hJ : J1 - J2 ≠ 0)
    (h1 : rho1 = b * J1 + offset) (h2 : rho2 = b * J2 + offset) :
    b = (rho1 - rho2) / (J1 - J2) := by
  apply (eq_div_iff hJ).2
  rw [h1,h2]
  ring

theorem full_inverse_balance (ell q rho t sigma2 v R b J : ℝ) :
    t * sigma2 - ell * q ^ 2 +
      (ell * q ^ 2 - rho - t * sigma2 + v * R + b * J) - v * R + rho = b * J := by
  ring

theorem expansion_sign (ell q : ℝ) (he : 0 < ell) :
    0 < -ell * q ↔ q < 0 := by
  constructor
  · intro h
    by_contra hn
    have hq : 0 ≤ q := le_of_not_gt hn
    have hm : -ell * q ≤ 0 := mul_nonpos_of_nonpos_of_nonneg (by linarith) hq
    linarith
  · intro hq
    exact mul_pos_of_neg_of_neg (by linarith) hq

end SpectralInverse20260926

#print axioms SpectralInverse20260926.inverse_lapse_equation
#print axioms SpectralInverse20260926.inverse_global_scale
#print axioms SpectralInverse20260926.vacuum_density_shift
#print axioms SpectralInverse20260926.same_proper_expansion
#print axioms SpectralInverse20260926.same_observations_family
#print axioms SpectralInverse20260926.distinct_couplings_distinct_vacuum
#print axioms SpectralInverse20260926.constant_slice_slope
#print axioms SpectralInverse20260926.full_inverse_balance
#print axioms SpectralInverse20260926.expansion_sign
