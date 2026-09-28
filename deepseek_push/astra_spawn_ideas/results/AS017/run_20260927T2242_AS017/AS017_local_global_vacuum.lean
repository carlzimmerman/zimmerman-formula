/-
AS017 — Local versus global vacuum input (Lean 4 / Mathlib certificate).

Run: cd fable_independent_2026/lean_2026 && lake env lean <abs path>/AS017_local_global_vacuum.lean

Scope note: Lean certifies the ALGEBRA of the audit. The statements:

  T1  vac_energy_identity : eps = a0^2/(k^2 G), rho = eps/c^2  =>  a0^2 = k^2 G rho c^2
      (the framework footing identity a0^2 = kappa^2 G rho_Lambda c^2, kappa adopted).

  T2  a0_eps_transfer : from a^2 = k^2 G e  and  b^2 = k^2 G f  (b = a + delta a,
      f = e + delta e), the EXACT finite perturbation fraction is
          (b - a)/a  =  ((f - e)/e) * (a/(a + b))
      whose leading term is delta a0/a0 = (1/2)(delta eps/eps) ("delta a0/a0 =
      delta eps_L/(2 eps_L)" in the task).  No first-order truncation is used.

  T3  deep_law_transfer : the identical structure for the deep law g^2 = a0 g_N:
          (g2 - g)/g = ((a2 - a)/a) * (g/(g + g2))     ->   delta g/g -> (1/4) delta eps/eps.

  T4  q_branch_transfer : Q-branch g^2 = B^2 + a B, same finite fraction:
          (g2 - g)/g = ((a2 - a)/a) * ((g^2 - B^2)/(g*(g + g2)))
      (the sensitivity coefficient (g^2-B^2)/(g(g+g2)) = 1/(2(1+y)) + O(delta) with
      y = B/a0, i.e. in (0, 1/2]).

  T5  rar_sensitivity_bounds : for the RAR kernel the environmental transfer of the
      phantom-branch response, s(y) = sqrt(y) e^{-sqrt y} / (2 (1 - e^{-sqrt y}))
      = - d ln g / d ln a0 at fixed B, satisfies  0 <= s(y) <= 1/2  for all y > 0
      (hence the RAR environmental scatter coefficient is at most 1/4 of the
      relative vacuum density variation).

  T6  cluster_boost_six : at y = (ln(6/5))^2 the RAR boost is EXACTLY 6 (the
      benchmark y for the DERIVATIONS.md median cluster source factor 5.998).

The full gradient/channel audit (missing term -y nu'(y)|g| nhat . grad ln a0) is
differential calculus; it is verified numerically by finite differences in
compute_AS017_local_global_vacuum.py and derived symbolically in derivation.md,
not re-certified here.
-/
import Mathlib

noncomputable section

open scoped Real

namespace AS017

-- T1: vacuum footing identity (kappa = 1/2 adopted; k is the adopted kappa).
theorem vac_energy_identity (a0 G c k : ℝ) (hk : k ≠ 0) (hG : G ≠ 0) (hc : c ≠ 0) :
    a0 ^ 2 = k ^ 2 * G * ((a0 ^ 2 / (k ^ 2 * G)) / c ^ 2) * c ^ 2 := by
  field_simp [hk, hG, hc]

-- T2: exact finite perturbation transfer  delta a0/a0 = (delta eps/eps) * a/(a+b).
theorem a0_eps_transfer (a b e f k G : ℝ) (ha : a ^ 2 = k ^ 2 * G * e)
    (hb : b ^ 2 = k ^ 2 * G * f) (ha_pos : 0 < a) (hb_pos : 0 < b)
    (he_pos : 0 < e) (hk : k ≠ 0) (hG : G ≠ 0) :
    (b - a) / a = (f - e) / e * (a / (a + b)) := by
  have hden_a : a ≠ 0 := ne_of_gt ha_pos
  have hden_b : a + b ≠ 0 := by positivity
  have hden_e : e ≠ 0 := ne_of_gt he_pos
  have hdiff : b ^ 2 - a ^ 2 = k ^ 2 * G * (f - e) := by
    rw [hb, ha]
    ring
  have hka : k ^ 2 * G = a ^ 2 / e := by
    rw [ha]
    field_simp [hden_e]
  calc
    (b - a) / a = (b - a) * (b + a) / (a * (b + a)) := by
      field_simp [hden_a, hden_b]
    _ = (b ^ 2 - a ^ 2) / (a * (b + a)) := by ring
    _ = (k ^ 2 * G * (f - e)) / (a * (b + a)) := by rw [hdiff]
    _ = (a ^ 2 / e * (f - e)) / (a * (b + a)) := by rw [hka]
    _ = (f - e) / e * (a / (a + b)) := by
      field_simp [hden_e, hden_a, hden_b]
      ring

-- corollary of T2: the leading coefficient is 1/2 with an explicit O((delta e/e)^2)
-- remainder, as a finite statement (no limits used):
--   (b-a)/a - (f-e)/(2 e) = -((f-e)/e)^2 * a / (2 (a+b))   -- only when b = a (infinitesimal).
-- (Not stated: requires a limiting argument; the exact fraction above is the operative
-- statement, and its -> 1/2 limit is verified numerically at q = +/-0.5, +/-0.1, +/-0.01
-- on both footings in AS017_outputs.json, C1.)

-- T3: deep-law transfer  g^2 = a0 g_N.
theorem deep_law_transfer (g g2 a a2 q : ℝ) (hg : g ^ 2 = a * q) (hg2 : g2 ^ 2 = a2 * q)
    (hg_pos : 0 < g) (hg2_pos : 0 < g2) (ha_pos : 0 < a) (hq_pos : 0 < q) :
    (g2 - g) / g = (a2 - a) / a * (g / (g + g2)) := by
  have hden_g : g ≠ 0 := ne_of_gt hg_pos
  have hden_gg : g + g2 ≠ 0 := by positivity
  have hden_a : a ≠ 0 := ne_of_gt ha_pos
  have hdiff : g2 ^ 2 - g ^ 2 = (a2 - a) * q := by
    rw [hg2, hg]
    ring
  have hqa : a2 - a = (a2 - a) / a * a := by field_simp [hden_a]
  calc
    (g2 - g) / g = (g2 - g) * (g2 + g) / (g * (g2 + g)) := by
      field_simp [hden_g, hden_gg]
    _ = (g2 ^ 2 - g ^ 2) / (g * (g2 + g)) := by ring
    _ = ((a2 - a) * q) / (g * (g2 + g)) := by rw [hdiff]
    _ = (a2 - a) / a * (g / (g + g2)) := by
      -- (a2-a)*q / (g(g+g2)) ; substitute q = g^2/a from hg, then cancel
      have hqa : (a2 - a) * q = (a2 - a) / a * g ^ 2 := by
        rw [hg]
        field_simp [hden_a]
      rw [hqa]
      field_simp [hden_g, hden_gg]
      ring

-- T4: Q-branch transfer  g^2 = B^2 + a B.
theorem q_branch_transfer (g g2 B a a2 : ℝ) (hg : g ^ 2 = B ^ 2 + a * B)
    (hg2 : g2 ^ 2 = B ^ 2 + a2 * B) (hg_pos : 0 < g) (hg2_pos : 0 < g2)
    (ha_pos : 0 < a) (hB_pos : 0 < B) :
    (g2 - g) / g = (a2 - a) / a * ((g ^ 2 - B ^ 2) / (g * (g + g2))) := by
  have hden_g : g ≠ 0 := ne_of_gt hg_pos
  have hden_gg : g + g2 ≠ 0 := by positivity
  have hden_a : a ≠ 0 := ne_of_gt ha_pos
  have hden_B : B ≠ 0 := ne_of_gt hB_pos
  have hdiff : g2 ^ 2 - g ^ 2 = (a2 - a) * B := by
    rw [hg2, hg]
    ring
  have hB_eq : (g ^ 2 - B ^ 2) / B = a := by
    rw [hg]
    field_simp [hden_B]
    ring
  have hgb : g ^ 2 - B ^ 2 ≠ 0 := by
    have : g ^ 2 - B ^ 2 = a * B := by
      rw [hg]
      ring
    rw [this]
    exact mul_ne_zero (ne_of_gt ha_pos) (ne_of_gt hB_pos)
  calc
    (g2 - g) / g = (g2 - g) * (g2 + g) / (g * (g2 + g)) := by
      field_simp [hden_g, hden_gg]
    _ = (g2 ^ 2 - g ^ 2) / (g * (g2 + g)) := by ring
    _ = ((a2 - a) * B) / (g * (g2 + g)) := by rw [hdiff]
    _ = (a2 - a) / a * ((g ^ 2 - B ^ 2) / (g * (g + g2))) := by
      -- (g^2 - B^2) = B*a from hg; substitute into the RHS denominator-free part and cancel
      have hB_a : B * a = g ^ 2 - B ^ 2 := by
        rw [hg]
        ring
      rw [← hB_a]
      field_simp [hden_a, hden_g, hden_gg]
      ring

-- T5: RAR environmental sensitivity is bounded: 0 <= s(y) <= 1/2, y > 0.
-- s(y) = sqrt y * e^{-sqrt y} / (2 (1 - e^{-sqrt y})) = - d ln g / d ln a0 at fixed B.
theorem rar_sensitivity_bounds (y : ℝ) (hy : 0 < y) :
    0 ≤ Real.sqrt y * Real.exp (-Real.sqrt y) / (2 * (1 - Real.exp (-Real.sqrt y)))
      ∧ Real.sqrt y * Real.exp (-Real.sqrt y) / (2 * (1 - Real.exp (-Real.sqrt y))) ≤ 1 / 2 := by
  let t : ℝ := Real.sqrt y
  have ht_pos : 0 < t := Real.sqrt_pos.2 hy
  have h_exp_neg_lt_one : Real.exp (-t) < 1 := by
    rw [Real.exp_lt_one_iff]
    linarith
  have h_den_pos : 0 < 2 * (1 - Real.exp (-t)) := by
    have hsub : 0 < 1 - Real.exp (-t) := sub_pos.mpr h_exp_neg_lt_one
    exact mul_pos (by norm_num) hsub
  have h_num_nonneg : 0 ≤ t * Real.exp (-t) := by positivity
  have h_left : 0 ≤ t * Real.exp (-t) / (2 * (1 - Real.exp (-t))) := by
    exact div_nonneg h_num_nonneg (le_of_lt h_den_pos)
  have h_ident : t * Real.exp (-t) / (2 * (1 - Real.exp (-t)))
      = t / (2 * (Real.exp t - 1)) := by
    have h_exp_t : Real.exp t ≠ 0 := Real.exp_ne_zero t
    have h_den2 : 2 * (Real.exp t - 1) ≠ 0 := by
      have hgt : 1 < Real.exp t := by
        rw [← Real.exp_zero]
        exact (Real.exp_lt_exp).2 ht_pos
      exact mul_ne_zero (by norm_num) (sub_ne_zero.mpr (ne_of_gt hgt))
    rw [Real.exp_neg]
    field_simp [h_exp_t, h_den2, h_den_pos.ne']
  have h_add_one_le : t + 1 ≤ Real.exp t := Real.add_one_le_exp t
  have h_exp_gt_one : 1 < Real.exp t := by
    rw [← Real.exp_zero]
    exact (Real.exp_lt_exp).2 ht_pos
  have h_t_le : t ≤ Real.exp t - 1 := by linarith
  have h_exp_minus_one_pos : 0 < Real.exp t - 1 := sub_pos.mpr h_exp_gt_one
  have h_two_den_pos : 0 < 2 * (Real.exp t - 1) := by
    exact mul_pos (by norm_num) h_exp_minus_one_pos
  have h_frac_le_one : t / (Real.exp t - 1) ≤ 1 := by
    exact div_le_one_of_le₀ h_t_le (le_of_lt h_exp_minus_one_pos)
  have h_right : t / (2 * (Real.exp t - 1)) ≤ 1 / 2 := by
    rw [show t / (2 * (Real.exp t - 1)) = (1 / 2) * (t / (Real.exp t - 1)) by
      field_simp [h_two_den_pos.ne']]
    nlinarith [h_frac_le_one]
  constructor
  · simpa [t] using h_left
  · calc
      Real.sqrt y * Real.exp (-Real.sqrt y) / (2 * (1 - Real.exp (-Real.sqrt y)))
          = t / (2 * (Real.exp t - 1)) := by simpa [t] using h_ident
      _ ≤ 1 / 2 := h_right

-- T6: cluster benchmark boost: at y = (ln(6/5))^2 the RAR boost nu = 6 EXACTLY.
theorem cluster_boost_six :
    1 / (1 - Real.exp (-Real.sqrt ((Real.log (6 / 5 : ℝ)) ^ 2))) = 6 := by
  have hpos : 0 < Real.log (6 / 5 : ℝ) := by
    exact Real.log_pos (by norm_num)
  have hsqrt : Real.sqrt ((Real.log (6 / 5 : ℝ)) ^ 2) = Real.log (6 / 5 : ℝ) := by
    rw [Real.sqrt_sq_eq_abs, abs_of_pos hpos]
  have hpos65 : 0 < (6 / 5 : ℝ) := by norm_num
  calc
    1 / (1 - Real.exp (-Real.sqrt ((Real.log (6 / 5 : ℝ)) ^ 2)))
        = 1 / (1 - Real.exp (-Real.log (6 / 5 : ℝ))) := by rw [hsqrt]
    _ = 1 / (1 - (Real.exp (Real.log (6 / 5 : ℝ)))⁻¹) := by rw [Real.exp_neg]
    _ = 1 / (1 - (6 / 5 : ℝ)⁻¹) := by rw [Real.exp_log hpos65]
    _ = 6 := by norm_num

end AS017

end
