/-
SV2 (closure_2026_11_06/SV2_causality, criteria 7d31bb0ac2), iter_2 / iter_3 algebra.
Leaf-mode dispersion on AC18's charged anisotropic background with the standard khronometric terms
(sympy, sv2_iter2.py): omega^2 = (Pi + l2 k^2)/(1/Z + alpha/(2K)), Z = K f + gamma k^2, f in [1+x, (1+x)^2],
l2 = (beta+lambda) c^2/(2K). Its k -> 0 limit is omega0^2(f) = Pi K f/(1 + alpha f/2), free of beta, lambda.
R1: omega0^2 strictly increasing in f on the no-ghost region, so it differs along e and perp whenever x > 0:
    the anisotropy is exactly 2x/(alpha(1+x)^2 + 2), never 0 for x > 0. No alpha, beta, lambda removes it.
R2: c_k^2 = (beta+lambda) c^2/alpha > 0 for alpha, beta+lambda > 0; c_k <= c iff beta+lambda <= alpha.
R3: alpha >= 0 => kinetic coefficient > 0 for all k; beta+lambda >= 0 => gradient coefficient > 0.
iter_3: alpha < 0 => a ghost wavenumber exists; beta+lambda < 0 => a gradient-unstable wavenumber exists.
Lean certifies only the algebra. kappa = 1/2 FITTED; not theory closed.
-/
import Mathlib

namespace SV2R

theorem omega0_strict_mono {P K α f1 f2 : ℝ} (hP : 0 < P) (hK : 0 < K) (h12 : f1 < f2)
    (hg1 : 0 < 1 + α * f1 / 2) (hg2 : 0 < 1 + α * f2 / 2) :
    P * K * f1 / (1 + α * f1 / 2) < P * K * f2 / (1 + α * f2 / 2) := by
  rw [div_lt_div_iff₀ hg1 hg2]
  nlinarith [mul_pos (mul_pos hP hK) (sub_pos.mpr h12)]

theorem transverse_lt_longitudinal {x : ℝ} (hx : 0 < x) : 1 + x < (1 + x) ^ 2 := by
  nlinarith

theorem anisotropy_exact {P K α x : ℝ} (hP : 0 < P) (hK : 0 < K) (hx : 0 < x)
    (hgT : 0 < 1 + α * (1 + x) / 2) (hgL : 0 < 1 + α * (1 + x) ^ 2 / 2) :
    (P * K * (1 + x) ^ 2 / (1 + α * (1 + x) ^ 2 / 2)) / (P * K * (1 + x) / (1 + α * (1 + x) / 2)) - 1
      = 2 * x / (α * (1 + x) ^ 2 + 2) := by
  have h1 : (1 + x) ≠ 0 := by linarith
  have h2 : α * (1 + x) ^ 2 + 2 ≠ 0 := by nlinarith
  have hPK : P * K ≠ 0 := (mul_pos hP hK).ne'
  have hden : (1 + α * (1 + x) ^ 2 / 2) * (P * K * (1 + x)) ≠ 0 :=
    mul_ne_zero hgL.ne' (mul_ne_zero hPK h1)
  rw [sub_eq_iff_eq_add, div_add_one h2, div_div_div_eq, div_eq_div_iff hden h2]
  ring

theorem anisotropy_ne_zero {α x : ℝ} (hx : 0 < x) (hgL : 0 < 1 + α * (1 + x) ^ 2 / 2) :
    0 < 2 * x / (α * (1 + x) ^ 2 + 2) := by
  apply div_pos (by linarith); nlinarith

theorem no_repair_in_class {P K α x : ℝ} (hP : 0 < P) (hK : 0 < K) (hx : 0 < x)
    (hgT : 0 < 1 + α * (1 + x) / 2) (hgL : 0 < 1 + α * (1 + x) ^ 2 / 2) :
    P * K * (1 + x) / (1 + α * (1 + x) / 2) ≠ P * K * (1 + x) ^ 2 / (1 + α * (1 + x) ^ 2 / 2) :=
  ne_of_lt (omega0_strict_mono hP hK (transverse_lt_longitudinal hx) hgT hgL)

theorem ck_sq_pos {bl c α : ℝ} (hbl : 0 < bl) (hc : 0 < c) (hα : 0 < α) : 0 < bl * c ^ 2 / α := by
  positivity

theorem ck_le_c_iff {bl c α : ℝ} (hc : 0 < c) (hα : 0 < α) : bl * c ^ 2 / α ≤ c ^ 2 ↔ bl ≤ α := by
  rw [div_le_iff₀ hα]
  constructor
  · intro h; nlinarith [pow_pos hc 2]
  · intro h; nlinarith [pow_pos hc 2]

theorem kinetic_pos {K α Z : ℝ} (hK : 0 < K) (hα : 0 ≤ α) (hZ : 0 < Z) : 0 < 1 / Z + α / (2 * K) := by
  have : 0 ≤ α / (2 * K) := by positivity
  have : 0 < 1 / Z := by positivity
  linarith

theorem gradient_pos {P l2 k2 : ℝ} (hP : 0 < P) (hl : 0 ≤ l2) (hk : 0 ≤ k2) : 0 < P + l2 * k2 := by
  nlinarith [mul_nonneg hl hk]

theorem ghost_if_alpha_neg {K α γ f : ℝ} (hK : 0 < K) (hα : α < 0) (hγ : 0 < γ) (hf : 0 < f) :
    ∃ k2 : ℝ, 0 ≤ k2 ∧ 1 / (K * f + γ * k2) + α / (2 * K) < 0 := by
  have hna : 0 < -α := neg_pos.mpr hα
  have hα0 : α ≠ 0 := hα.ne
  refine ⟨4 * K / (-α * γ), (div_pos (by positivity) (mul_pos hna hγ)).le, ?_⟩
  have hD : K * f + γ * (4 * K / (-α * γ)) = K * f + 4 * K / (-α) := by
    field_simp
  rw [hD]
  have hDp : 0 < K * f + 4 * K / (-α) := add_pos (mul_pos hK hf) (div_pos (by positivity) hna)
  have key : 2 * K < -α * (K * f + 4 * K / (-α)) := by
    have e : -α * (K * f + 4 * K / (-α)) = -α * K * f + 4 * K := by
      field_simp
      ring
    rw [e]; nlinarith [mul_pos hna (mul_pos hK hf)]
  have h1 : 1 / (K * f + 4 * K / (-α)) < -α / (2 * K) := by
    rw [div_lt_div_iff₀ hDp (by positivity)]; linarith
  have e2 : α / (2 * K) = -(-α / (2 * K)) := by ring
  rw [e2]; linarith

theorem gradient_unstable_if_neg {P l2 : ℝ} (hP : 0 < P) (hl : l2 < 0) :
    ∃ k2 : ℝ, 0 ≤ k2 ∧ P + l2 * k2 < 0 := by
  have hnl : 0 < -l2 := neg_pos.mpr hl
  have hl0 : l2 ≠ 0 := hl.ne
  refine ⟨2 * P / (-l2), (div_pos (by positivity) hnl).le, ?_⟩
  have e : l2 * (2 * P / (-l2)) = -2 * P := by
    field_simp
  rw [e]; linarith

end SV2R

#print axioms SV2R.omega0_strict_mono
#print axioms SV2R.transverse_lt_longitudinal
#print axioms SV2R.anisotropy_exact
#print axioms SV2R.anisotropy_ne_zero
#print axioms SV2R.no_repair_in_class
#print axioms SV2R.ck_sq_pos
#print axioms SV2R.ck_le_c_iff
#print axioms SV2R.kinetic_pos
#print axioms SV2R.gradient_pos
#print axioms SV2R.ghost_if_alpha_neg
#print axioms SV2R.gradient_unstable_if_neg
