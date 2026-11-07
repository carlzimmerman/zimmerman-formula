/-
SV2_repair MUTATE twin: four planted false claims, each must fail.
M1: the k -> 0 leaf frequency is isotropic at x > 0 (the anisotropy 2x/(alpha(1+x)^2+2) vanishes).
M2: omega0^2 DEcreases with f.
M3: alpha < 0 is ghost-free at every k.
M4: beta + lambda < 0 is gradient-stable at every k.
kappa = 1/2 FITTED; not theory closed.
-/
import Mathlib

namespace SV2RM

theorem isotropic_at_x_pos {α x : ℝ} (hx : 0 < x) (hgL : 0 < 1 + α * (1 + x) ^ 2 / 2) :
    2 * x / (α * (1 + x) ^ 2 + 2) = 0 := by
  field_simp
  nlinarith

theorem omega0_decreasing {P K α f1 f2 : ℝ} (hP : 0 < P) (hK : 0 < K) (h12 : f1 < f2)
    (hg1 : 0 < 1 + α * f1 / 2) (hg2 : 0 < 1 + α * f2 / 2) :
    P * K * f2 / (1 + α * f2 / 2) < P * K * f1 / (1 + α * f1 / 2) := by
  rw [div_lt_div_iff₀ hg2 hg1]
  nlinarith [mul_pos (mul_pos hP hK) (sub_pos.mpr h12)]

theorem ghost_free_alpha_neg {K α γ f : ℝ} (hK : 0 < K) (hα : α < 0) (hγ : 0 < γ) (hf : 0 < f) :
    ∀ k2 : ℝ, 0 ≤ k2 → 0 < 1 / (K * f + γ * k2) + α / (2 * K) := by
  intro k2 hk2
  have : 0 < 1 / (K * f + γ * k2) := by positivity
  nlinarith

theorem gradient_stable_neg {P l2 : ℝ} (hP : 0 < P) (hl : l2 < 0) :
    ∀ k2 : ℝ, 0 ≤ k2 → 0 < P + l2 * k2 := by
  intro k2 hk2
  nlinarith

end SV2RM

#print axioms SV2RM.isotropic_at_x_pos
#print axioms SV2RM.omega0_decreasing
#print axioms SV2RM.ghost_free_alpha_neg
#print axioms SV2RM.gradient_stable_neg
