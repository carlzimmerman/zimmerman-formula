import Mathlib

/-!
AS226 Lean 4 certificate — measured Newton G in the reciprocal high-k limit.
Seed: AS226_derive_measured_newton_g_in_the_reciprocal_high_k_limit.md
      (sha256 51e2412c78b88902d617f2369913abccbbd69a918b37268d3f75d06b809dd398)
Framework: c_N = 1 - alpha/2 (0 < alpha < 2); M_P^2 = (8 pi G_bare)^-1;
4 pi G_N = 1/(2 M_P^2 c_N); G_N/G_bare = 1/c_N; negative-control residual
(1+c_N)(rho_b+rho_d) = (2 - alpha/2)(rho_b+rho_d) != 0.

Theorems certified (all real arithmetic):
 1. c_N lies strictly between 0 and 1 for 0 < alpha < 2  (positive, < 1)
 2. G_N/G_bare = 1/c_N          (given G_bare = c_N G_N, c_N,G_N != 0)
 3. 1 < G_N/G_bare on (0,2)     (measured constant exceeds the bare one)
 4. alpha -> 0 recovers G_N/G_bare -> 1 (the GR limit c_N -> 1)
 5. d/dalpha G_N/G_bare = 1/(2(1-alpha/2)^2) > 0 on (0,2)  (monotone rise)
 6. negative control residual algebra: substituting the G_bare-calibrated
    potential u'_bare = 4 pi G_bare rho/k^2 into the sourced equation
    (2 M_P^2 c_N k^2 coefficient) leaves -(1+c_N) rho  (fires, != 0)
-/

noncomputable section

open scoped Real

lemma cn_range (α : ℝ) (h0 : 0 < α) (h2 : α < 2) : 0 < 1 - α / 2 ∧ 1 - α / 2 < 1 := by
  have h2a : 0 < 2 - α := by nlinarith [h2]
  have hpos : 0 < (2 - α) / 2 := div_pos h2a (by norm_num : (0 : ℝ) < 2)
  have hiden : (2 - α) / 2 = 1 - α / 2 := by ring
  constructor
  · rwa [← hiden]
  · have hb : (0 : ℝ) < 2 := by norm_num
    have hlt : α / 2 < 1 := by
      rw [div_lt_one hb]
      exact h2
    linarith [hlt]

lemma gn_over_gbare (G_N G_bare c_N : ℝ) (hG : G_bare = c_N * G_N)
    (hc : c_N ≠ 0) (hN : G_N ≠ 0) : G_N / G_bare = 1 / c_N := by
  rw [hG]
  field_simp [hc, hN]

lemma ratio_gt_one (α : ℝ) (h0 : 0 < α) (h2 : α < 2) : 1 < 1 / (1 - α / 2) := by
  have ⟨hpos, hl⟩ := cn_range α h0 h2
  rw [one_div]
  exact (one_lt_inv₀ hpos).2 hl

lemma gr_limit (α : ℝ) (h : α = 0) : 1 / (1 - α / 2) = 1 := by
  rw [h]
  norm_num

lemma cN_plus_one_ne_zero (α : ℝ) (h2 : α < 2) : (1 + (1 - α / 2)) ≠ 0 := by
  have hb : (0 : ℝ) < 2 := by norm_num
  have hlt : α / 2 < 1 := by
    rw [div_lt_one hb]
    exact h2
  have hgt : 1 < 1 + (1 - α / 2) := by linarith [hlt]
  have hpos2 : 0 < 1 + (1 - α / 2) := by linarith [hgt]
  exact ne_of_gt hpos2

lemma negative_control_residual (_α : ℝ) (c_N ρ k2 G_bare : ℝ)
    (hπ : π ≠ 0) (hk : k2 ≠ 0) (hGb : G_bare ≠ 0) :
    -2 * (1 / (8 * π * G_bare)) * c_N * k2 * (4 * π * G_bare * ρ / k2) - ρ
      = -(1 + c_N) * ρ := by
  field_simp [hπ, hk, hGb]
  ring

lemma negative_control_fires (α ρ : ℝ) (hρ : ρ ≠ 0) (h2 : α < 2) :
    -((1 + (1 - α / 2)) * ρ) ≠ 0 := by
  have h1 : (1 + (1 - α / 2)) ≠ 0 := cN_plus_one_ne_zero α h2
  exact neg_ne_zero.mpr (mul_ne_zero h1 hρ)

lemma deriv_formula (x : ℝ) (hx : 1 - x / 2 ≠ 0) :
    HasDerivAt (fun t : ℝ => 1 / (1 - t / 2)) (1 / (2 * (1 - x / 2) ^ 2)) x := by
  have hcst : HasDerivAt (fun _ : ℝ => (1 : ℝ)) 0 x := hasDerivAt_const x 1
  have hid : HasDerivAt (fun t : ℝ => t) 1 x := hasDerivAt_id x
  have ht2 : HasDerivAt (fun t : ℝ => t / 2) (1 / 2) x := by
    simpa using hid.div_const (2 : ℝ)
  have hsub := hcst.sub ht2
  have hv : (0 : ℝ) - (1 / 2 : ℝ) = -(1 / 2 : ℝ) := by norm_num
  have hden : HasDerivAt (fun t : ℝ => 1 - t / 2) (-(1 / 2) : ℝ) x := by
    rwa [hv] at hsub
  have hdiv := hcst.div hden hx
  have hnum : 0 * (1 - x / 2) - 1 * (-(1 / 2 : ℝ)) = (1 / 2 : ℝ) := by ring
  have hdiv' : HasDerivAt (fun t : ℝ => 1 / (1 - t / 2)) ((1 / 2 : ℝ) / (1 - x / 2) ^ 2) x := by
    rwa [hnum] at hdiv
  have hv2 : (1 / 2 : ℝ) / (1 - x / 2) ^ 2 = 1 / (2 * (1 - x / 2) ^ 2) := by
    field_simp [hx]
  rw [← hv2]
  exact hdiv'

lemma deriv_pos (α : ℝ) (_h0 : 0 < α) (h2 : α < 2) :
    0 < deriv (fun t : ℝ => 1 / (1 - t / 2)) α := by
  have h2a : 0 < 2 - α := by nlinarith [h2]
  have hpos : 0 < (2 - α) / 2 := div_pos h2a (by norm_num : (0 : ℝ) < 2)
  have hiden : (2 - α) / 2 = 1 - α / 2 := by ring
  have hd0 : 1 - α / 2 ≠ 0 := by
    rw [← hiden]
    exact ne_of_gt hpos
  have hd : HasDerivAt (fun t : ℝ => 1 / (1 - t / 2)) (1 / (2 * (1 - α / 2) ^ 2)) α :=
    deriv_formula α hd0
  rw [hd.deriv]
  have h2p : (0 : ℝ) < 2 := by norm_num
  have hself : 0 < (1 - α / 2) * (1 - α / 2) := mul_self_pos.mpr hd0
  have hmul : 0 < 2 * ((1 - α / 2) * (1 - α / 2)) := mul_pos h2p hself
  have hiden2 : (1 - α / 2) ^ 2 = (1 - α / 2) * (1 - α / 2) := by rw [pow_two]
  rw [hiden2]
  exact one_div_pos.mpr hmul

-- Combined statement of the Tier-0b observable claim on (0,2):
theorem measured_constant_majorizes_bare (α G_N G_bare c_N : ℝ)
    (hG : G_bare = c_N * G_N) (hcN : c_N = 1 - α / 2)
    (hc : c_N ≠ 0) (hN : G_N ≠ 0) (h0 : 0 < α) (h2 : α < 2) :
    G_N / G_bare = 1 / c_N ∧ 1 < G_N / G_bare ∧
    0 < deriv (fun t : ℝ => 1 / (1 - t / 2)) α := by
  constructor
  · exact gn_over_gbare G_N G_bare c_N hG hc hN
  · constructor
    · rw [hG]
      calc
        1 < (c_N)⁻¹ := by
          rw [hcN]
          rw [← one_div]
          exact ratio_gt_one α h0 h2
        _ = G_N / (c_N * G_N) := by field_simp [hc, hN]
    · exact deriv_pos α h0 h2

#print axioms measured_constant_majorizes_bare
#print axioms negative_control_fires
#print axioms deriv_pos
#print axioms negative_control_residual