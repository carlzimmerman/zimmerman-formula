/-
EUC21: Lean statements for the algebra of the gas-lane re-read at the in-mask mass (ESZ1's code run on the corrected
masses), covering the pair EUC21 (lead) and EUC21R (blind re-grade, closure_2026_11_14/EUC21R_blind_gas_lane_regrade).
Both builds apply ESZ1's family, lane and Part C rules unchanged. They certify the algebra, not the physics, and no
number or label of the lane. TEST lane; adopts nothing.

  lawS_monotone          : law S in closed form, g = (y + sqrt(y^2 + 4 a0 y)) / 2 with y = g_N >= 0, does not fall
                           when y rises.
  lawS_ratio_antitone    : g / y does not rise with y: y2 g(y1) >= y1 g(y2) for 0 < y1 <= y2.
  pressure_integrand_bracket : with the gas amplitude scaled by 0 <= A <= 1 (stars fixed, g_N = g_star + A g_gas), the
                           hydrostatic integrand rho g of the needed gas lies between A^2 and A times its value at
                           A = 1: a smaller missing mass needs less pressure, by a factor between linear and quadratic
                           in the amplitude (not exactly in proportion).
  g2_newtonian_hydrostatic : check K4's closed form: for the r^-2 cusp cut at r_t (rho = M / (4 pi r_t r^2),
                           M(<r) = M r / r_t), P(r) = G M^2 / (8 pi r_t^2) (r^-2 - r_t^-2) has dP/dr = -rho g.
  excluded_iff_fT        : with pred_min > 0, EXCLUDED (measured + 2 sigma < pred_min) holds exactly when the hiding
                           factor f_T = (measured + 2 sigma) / pred_min is below 1.
  fT_rises_as_pred_falls : f_T does not fall when pred_min falls (measured + 2 sigma >= 0): the hiding room grows.
  nopower_excluded_overlap : NO POWER (pred_min < 3 sigma) and EXCLUDED can both hold only if measured < sigma, so for
                           measured >= sigma the order of the family rule does not decide the word.
  paired_mean_difference : the Part C statistic, the mean over pairs of (wide - control), is the wide lenses' mean
                           minus the controls' mean: with the wide stack fixed, the change is the controls' alone.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
-/
import Mathlib

namespace EUC21

theorem lawS_monotone (a0 y1 y2 : ℝ) (ha : 0 ≤ a0) (h1 : 0 ≤ y1) (h12 : y1 ≤ y2) :
    (y1 + Real.sqrt (y1 ^ 2 + 4 * a0 * y1)) / 2 ≤ (y2 + Real.sqrt (y2 ^ 2 + 4 * a0 * y2)) / 2 := by
  have hs : Real.sqrt (y1 ^ 2 + 4 * a0 * y1) ≤ Real.sqrt (y2 ^ 2 + 4 * a0 * y2) := by
    apply Real.sqrt_le_sqrt
    nlinarith
  linarith

theorem lawS_ratio_antitone (a0 y1 y2 : ℝ) (ha : 0 ≤ a0) (h1 : 0 < y1) (h12 : y1 ≤ y2) :
    y1 * ((y2 + Real.sqrt (y2 ^ 2 + 4 * a0 * y2)) / 2) ≤ y2 * ((y1 + Real.sqrt (y1 ^ 2 + 4 * a0 * y1)) / 2) := by
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

theorem pressure_integrand_bracket (a0 gs gh rho A : ℝ) (ha : 0 ≤ a0) (hs : 0 ≤ gs) (hh : 0 ≤ gh)
    (hpos : 0 < gs + A * gh) (hrho : 0 ≤ rho) (hA0 : 0 ≤ A) (hA1 : A ≤ 1) :
    A ^ 2 * (rho * ((gs + gh + Real.sqrt ((gs + gh) ^ 2 + 4 * a0 * (gs + gh))) / 2))
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

theorem g2_newtonian_hydrostatic (G M rt r : ℝ) (hr : r ≠ 0) (hrt : rt ≠ 0) :
    HasDerivAt (fun x => G * M ^ 2 / (8 * Real.pi * rt ^ 2) * ((x ^ 2)⁻¹ - (rt ^ 2)⁻¹))
      (-(M / (4 * Real.pi * rt * r ^ 2)) * (G * (M * r / rt) / r ^ 2)) r := by
  have hpi : Real.pi ≠ 0 := Real.pi_ne_zero
  have h1 : HasDerivAt (fun x : ℝ => (x ^ 2)⁻¹) (-((2 : ℕ) * r ^ (2 - 1)) / (r ^ 2) ^ 2) r :=
    (hasDerivAt_pow 2 r).inv (pow_ne_zero 2 hr)
  have h2 := (h1.sub_const ((rt ^ 2)⁻¹)).const_mul (G * M ^ 2 / (8 * Real.pi * rt ^ 2))
  refine h2.congr_deriv ?_
  norm_num
  field_simp
  ring

theorem excluded_iff_fT (m s p : ℝ) (hp : 0 < p) : m + 2 * s < p ↔ (m + 2 * s) / p < 1 := by
  rw [div_lt_one hp]

theorem fT_rises_as_pred_falls (m s p1 p2 : ℝ) (hnum : 0 ≤ m + 2 * s) (hp1 : 0 < p1) (h12 : p1 ≤ p2) :
    (m + 2 * s) / p2 ≤ (m + 2 * s) / p1 := by
  exact div_le_div_of_nonneg_left hnum hp1 h12

theorem nopower_excluded_overlap (m s p : ℝ) (hnp : p < 3 * s) (hex : m + 2 * s < p) : m < s := by
  linarith

theorem paired_mean_difference {n : ℕ} (w c : Fin n → ℝ) :
    (∑ i, (w i - c i)) / n = (∑ i, w i) / n - (∑ i, c i) / n := by
  rw [Finset.sum_sub_distrib, sub_div]

end EUC21

-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
