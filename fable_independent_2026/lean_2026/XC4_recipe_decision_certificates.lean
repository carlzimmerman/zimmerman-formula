import Mathlib

/-!
# XC4 — the 2026-09-26 recipe decisions: certificates for their mathematics

SCOPE. The user decided (2026-09-26): the kernel is ν_mono, causality is criterion B, and Z is corrected in the recipe
(`qwen_claude_field_theory/closure_2026/CRISPY_FRIED_CHICKEN_RECIPE.md`, user-decision block; the spec's requirements
1, 7, 12 amended). Lean certifies the mathematics those decisions rest on; the numbers y_p = 2.5396, h_p = 0.6476 and
the ≤ 0.01 dex agreement of ν_mono with ν_RAR are computed in L340, not here.

* `z_is_kappa`: with Z = √(8π/3)/κ (Z ≡ κ), κ = ½ ⟺ Z² = 32π/3 for κ > 0 — Z is κ restated, not a second number.
* `z_value_bounds`: 5.788 < √(32π/3) < 5.789 — the recipe's corrected value (never ≈ 21).
* `mono_phantom_increasing`: ν_mono's phantom slope max(h′_RAR, δ h_p/(y + y_p)) is strictly positive for y ≥ 0 —
  the monotone-phantom condition (C_L > 0) that L340's khronon health requires holds by construction.
* `mu_exp_phantom_turns`: for the retired AQUAL kernel μ(x) = 1 − e^{−x}, the phantom slope
  C_L = (1 − x)/(eˣ + x − 1) is negative for every x > 1 — the reason it cannot be the kernel of a healthy
  momentum-carrying completion.
* `nu_rar_phantom_turns`: ν_RAR's phantom h(y) = y/(e^{√y} − 1) is smaller at y = 9 than at y = 4:
  9/(e³ − 1) < 4/(e² − 1) — it turns over, which is why ν_mono continues it monotonically above the peak.
-/

theorem z_is_kappa (κ : ℝ) (hκ : 0 < κ) :
    κ = 1 / 2 ↔ (Real.sqrt (8 * Real.pi / 3) / κ) ^ 2 = 32 * Real.pi / 3 := by
  have hpi : 0 < Real.pi := Real.pi_pos
  have hs : Real.sqrt (8 * Real.pi / 3) ^ 2 = 8 * Real.pi / 3 := Real.sq_sqrt (by positivity)
  rw [div_pow, hs]
  constructor
  · intro h; rw [h]; ring
  · intro h
    have hκ2 : κ ^ 2 = 1 / 4 := by
      field_simp at h
      nlinarith [hpi]
    have : (κ - 1 / 2) * (κ + 1 / 2) = 0 := by nlinarith
    rcases mul_eq_zero.mp this with h1 | h1
    · linarith
    · linarith

theorem z_value_bounds : 5.788 < Real.sqrt (32 * Real.pi / 3) ∧ Real.sqrt (32 * Real.pi / 3) < 5.789 := by
  have h1 := Real.pi_gt_d6
  have h2 := Real.pi_lt_d6
  constructor
  · rw [Real.lt_sqrt (by norm_num)]
    nlinarith
  · rw [Real.sqrt_lt' (by norm_num)]
    nlinarith

theorem mono_phantom_increasing (dRAR δ hp yp y : ℝ) (hδ : 0 < δ) (hhp : 0 < hp) (hyp : 0 < yp) (hy : 0 ≤ y) :
    0 < max dRAR (δ * hp / (y + yp)) := by
  have : 0 < δ * hp / (y + yp) := by
    have : 0 < y + yp := by linarith
    positivity
  exact lt_of_lt_of_le this (le_max_right _ _)

theorem mu_exp_phantom_turns (x : ℝ) (hx : 1 < x) : (1 - x) / (Real.exp x + x - 1) < 0 := by
  have hexp : x + 1 ≤ Real.exp x := Real.add_one_le_exp x
  have hden : 0 < Real.exp x + x - 1 := by linarith
  apply div_neg_of_neg_of_pos (by linarith) hden

theorem nu_rar_phantom_turns : 9 / (Real.exp 3 - 1) < 4 / (Real.exp 2 - 1) := by
  have h1 := Real.exp_one_gt_d9
  have h2 := Real.exp_one_lt_d9
  set t := Real.exp 1 with ht
  have e2 : Real.exp 2 = t ^ 2 := by
    rw [show (2 : ℝ) = 1 + 1 by norm_num, Real.exp_add]; ring
  have e3 : Real.exp 3 = t ^ 3 := by
    rw [show (3 : ℝ) = 1 + 1 + 1 by norm_num, Real.exp_add, Real.exp_add]; ring
  rw [e2, e3]
  have htpos : 2.7 < t := by linarith
  have hd2 : 0 < t ^ 2 - 1 := by nlinarith
  have hd3 : 0 < t ^ 3 - 1 := by nlinarith
  rw [div_lt_div_iff₀ hd3 hd2]
  have h4 : 0 < 4 * t - 9 := by linarith
  have ht2 : 0 < t ^ 2 := by positivity
  nlinarith [mul_pos ht2 h4]

#print axioms z_is_kappa
#print axioms z_value_bounds
#print axioms mono_phantom_increasing
#print axioms mu_exp_phantom_turns
#print axioms nu_rar_phantom_turns
