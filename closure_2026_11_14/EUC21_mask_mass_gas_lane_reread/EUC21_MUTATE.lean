/-
EUC21_MUTATE: the mutation twin of EUC21.lean (pair EUC21 / EUC21R). Each theorem carries ONE false change (a sign,
a factor or an inequality direction) and the same proof script; every theorem here must fail to compile. They
certify the algebra, not the physics, and no number or label of the lane.

  lawS_monotone_mut              : inequality direction reversed.
  lawS_ratio_antitone_mut        : inequality direction reversed (g / y rising).
  pressure_integrand_bracket_mut : lower bound A in place of A^2 (exact proportion claimed as a bound).
  g2_newtonian_hydrostatic_mut   : dP/dr = +rho g in place of -rho g.
  excluded_iff_fT_mut            : f_T compared with 2 in place of 1.
  fT_rises_as_pred_falls_mut     : inequality direction reversed.
  nopower_excluded_overlap_mut   : conclusion measured < 0 in place of measured < sigma.
  paired_mean_difference_mut     : plus the controls' mean in place of minus.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
-/
import Mathlib

namespace EUC21

theorem lawS_monotone_mut (a0 y1 y2 : ℝ) (ha : 0 ≤ a0) (h1 : 0 ≤ y1) (h12 : y1 ≤ y2) :
    (y2 + Real.sqrt (y2 ^ 2 + 4 * a0 * y2)) / 2 ≤ (y1 + Real.sqrt (y1 ^ 2 + 4 * a0 * y1)) / 2 := by
  have hs : Real.sqrt (y1 ^ 2 + 4 * a0 * y1) ≤ Real.sqrt (y2 ^ 2 + 4 * a0 * y2) := by
    apply Real.sqrt_le_sqrt
    nlinarith
  linarith

theorem lawS_ratio_antitone_mut (a0 y1 y2 : ℝ) (ha : 0 ≤ a0) (h1 : 0 < y1) (h12 : y1 ≤ y2) :
    y2 * ((y1 + Real.sqrt (y1 ^ 2 + 4 * a0 * y1)) / 2) ≤ y1 * ((y2 + Real.sqrt (y2 ^ 2 + 4 * a0 * y2)) / 2) := by
  have h2 : 0 < y2 := by linarith
  have e1 : y1 * Real.sqrt (y2 ^ 2 + 4 * a0 * y2) = Real.sqrt (y1 ^ 2 * (y2 ^ 2 + 4 * a0 * y2)) := by
    rw [Real.sqrt_mul (sq_nonneg _), Real.sqrt_sq (le_of_lt h1)]
  have e2 : y2 * Real.sqrt (y1 ^ 2 + 4 * a0 * y1) = Real.sqrt (y2 ^ 2 * (y1 ^ 2 + 4 * a0 * y1)) := by
    rw [Real.sqrt_mul (sq_nonneg _), Real.sqrt_sq (le_of_lt h2)]
  have hs : Real.sqrt (y1 ^ 2 * (y2 ^ 2 + 4 * a0 * y2)) ≤ Real.sqrt (y2 ^ 2 * (y1 ^ 2 + 4 * a0 * y1)) := by
    apply Real.sqrt_le_sqrt
    have hm : 0 ≤ y1 * y2 * (y2 - y1) := by
      apply mul_nonneg (le_of_lt (mul_pos h1 h2))
      linarith
    nlinarith [mul_nonneg ha hm]
  nlinarith [e1, e2, hs]

theorem pressure_integrand_bracket_mut (a0 gs gh rho A : ℝ) (ha : 0 ≤ a0) (hs : 0 ≤ gs) (hh : 0 ≤ gh)
    (hpos : 0 < gs + A * gh) (hrho : 0 ≤ rho) (hA0 : 0 ≤ A) (hA1 : A ≤ 1) :
    A * (rho * ((gs + gh + Real.sqrt ((gs + gh) ^ 2 + 4 * a0 * (gs + gh))) / 2))
        ≤ A * (rho * ((gs + A * gh + Real.sqrt ((gs + A * gh) ^ 2 + 4 * a0 * (gs + A * gh))) / 2)) ∧
      A * (rho * ((gs + A * gh + Real.sqrt ((gs + A * gh) ^ 2 + 4 * a0 * (gs + A * gh))) / 2))
        ≤ A * (rho * ((gs + gh + Real.sqrt ((gs + gh) ^ 2 + 4 * a0 * (gs + gh))) / 2)) := by
  set y1 := gs + A * gh with hy1
  set y2 := gs + gh with hy2
  have h12 : y1 ≤ y2 := by nlinarith
  have hy1pos : 0 < y1 := hpos
  have hy2pos : 0 < y2 := by linarith
  set g1 := (y1 + Real.sqrt (y1 ^ 2 + 4 * a0 * y1)) / 2 with hg1
  set g2 := (y2 + Real.sqrt (y2 ^ 2 + 4 * a0 * y2)) / 2 with hg2
  -- monotone: g1 <= g2
  have hmono : g1 ≤ g2 := by
    have hs' : Real.sqrt (y1 ^ 2 + 4 * a0 * y1) ≤ Real.sqrt (y2 ^ 2 + 4 * a0 * y2) := by
      apply Real.sqrt_le_sqrt
      nlinarith
    rw [hg1, hg2]
    linarith
  -- ratio: y1 g2 <= y2 g1
  have hratio : y1 * g2 ≤ y2 * g1 := by
    have e1 : y1 * Real.sqrt (y2 ^ 2 + 4 * a0 * y2) = Real.sqrt (y1 ^ 2 * (y2 ^ 2 + 4 * a0 * y2)) := by
      rw [Real.sqrt_mul (sq_nonneg _), Real.sqrt_sq (le_of_lt hy1pos)]
    have e2 : y2 * Real.sqrt (y1 ^ 2 + 4 * a0 * y1) = Real.sqrt (y2 ^ 2 * (y1 ^ 2 + 4 * a0 * y1)) := by
      rw [Real.sqrt_mul (sq_nonneg _), Real.sqrt_sq (le_of_lt hy2pos)]
    have hs' : Real.sqrt (y1 ^ 2 * (y2 ^ 2 + 4 * a0 * y2)) ≤ Real.sqrt (y2 ^ 2 * (y1 ^ 2 + 4 * a0 * y1)) := by
      apply Real.sqrt_le_sqrt
      have hm : 0 ≤ y1 * y2 * (y2 - y1) := by
        apply mul_nonneg (le_of_lt (mul_pos hy1pos hy2pos))
        linarith
      nlinarith [mul_nonneg ha hm]
    rw [hg1, hg2]
    nlinarith [e1, e2, hs']
  have hg2nn : 0 ≤ g2 := by
    rw [hg2]
    have := Real.sqrt_nonneg (y2 ^ 2 + 4 * a0 * y2)
    linarith
  -- A g2 <= g1, from y1 >= A y2
  have hAy : A * y2 ≤ y1 := by nlinarith
  have hAg : A * g2 ≤ g1 := by
    have h3 : A * y2 * g2 ≤ y1 * g2 := mul_le_mul_of_nonneg_right hAy hg2nn
    have h4 : A * y2 * g2 ≤ y2 * g1 := le_trans h3 hratio
    have h5 : y2 * (A * g2) ≤ y2 * g1 := by linarith
    exact le_of_mul_le_mul_left h5 hy2pos
  constructor
  · have h6 : A * (A * g2) ≤ A * g1 := mul_le_mul_of_nonneg_left hAg hA0
    have h7 : rho * (A * (A * g2)) ≤ rho * (A * g1) := mul_le_mul_of_nonneg_left h6 hrho
    nlinarith [h7]
  · have h8 : rho * g1 ≤ rho * g2 := mul_le_mul_of_nonneg_left hmono hrho
    exact mul_le_mul_of_nonneg_left h8 hA0

theorem g2_newtonian_hydrostatic_mut (G M rt r : ℝ) (hr : r ≠ 0) (hrt : rt ≠ 0) :
    HasDerivAt (fun x => G * M ^ 2 / (8 * Real.pi * rt ^ 2) * ((x ^ 2)⁻¹ - (rt ^ 2)⁻¹))
      ((M / (4 * Real.pi * rt * r ^ 2)) * (G * (M * r / rt) / r ^ 2)) r := by
  have hpi : Real.pi ≠ 0 := Real.pi_ne_zero
  have h1 : HasDerivAt (fun x : ℝ => (x ^ 2)⁻¹) (-((2 : ℕ) * r ^ (2 - 1)) / (r ^ 2) ^ 2) r :=
    (hasDerivAt_pow 2 r).inv (pow_ne_zero 2 hr)
  have h2 := (h1.sub_const ((rt ^ 2)⁻¹)).const_mul (G * M ^ 2 / (8 * Real.pi * rt ^ 2))
  refine h2.congr_deriv ?_
  norm_num
  field_simp
  ring

theorem excluded_iff_fT_mut (m s p : ℝ) (hp : 0 < p) : m + 2 * s < p ↔ (m + 2 * s) / p < 2 := by
  rw [div_lt_one hp]

theorem fT_rises_as_pred_falls_mut (m s p1 p2 : ℝ) (hnum : 0 ≤ m + 2 * s) (hp1 : 0 < p1) (h12 : p1 ≤ p2) :
    (m + 2 * s) / p1 ≤ (m + 2 * s) / p2 := by
  exact div_le_div_of_nonneg_left hnum hp1 h12

theorem nopower_excluded_overlap_mut (m s p : ℝ) (hnp : p < 3 * s) (hex : m + 2 * s < p) : m < 0 := by
  linarith

theorem paired_mean_difference_mut {n : ℕ} (w c : Fin n → ℝ) :
    (∑ i, (w i - c i)) / n = (∑ i, w i) / n + (∑ i, c i) / n := by
  rw [Finset.sum_sub_distrib, sub_div]

end EUC21

-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
