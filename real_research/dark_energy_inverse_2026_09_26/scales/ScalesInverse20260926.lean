import Mathlib

/-! Conditional scale inverses and non-identifiability. No physical-origin,
likelihood, vacuum equation of state, or gravitational-action theorem. -/
namespace ScalesInverse20260926

theorem positive_scale_squared (k c G rho : ℝ) (hG : 0 ≤ G) (hr : 0 ≤ rho) :
    (k * c * Real.sqrt (G * rho)) ^ 2 = k ^ 2 * c ^ 2 * G * rho := by
  rw [mul_pow, mul_pow, Real.sq_sqrt (mul_nonneg hG hr)]
  ring

theorem density_inverse_iff (a k c G rho : ℝ)
    (hk : k ≠ 0) (hc : c ≠ 0) (hG : G ≠ 0) :
    a ^ 2 = k ^ 2 * c ^ 2 * G * rho ↔ rho = a ^ 2 / (k ^ 2 * c ^ 2 * G) := by
  have hn : k ^ 2 * c ^ 2 * G ≠ 0 := mul_ne_zero (mul_ne_zero (pow_ne_zero 2 hk) (pow_ne_zero 2 hc)) hG
  constructor
  · intro h
    apply (eq_div_iff hn).2
    nlinarith
  · intro h
    rw [h]
    field_simp

theorem nonnegative_branch_reconstruction (a k c G rho : ℝ)
    (ha : 0 ≤ a) (hk : 0 ≤ k) (hc : 0 ≤ c) (hG : 0 ≤ G) (hr : 0 ≤ rho)
    (hs : a ^ 2 = k ^ 2 * c ^ 2 * G * rho) :
    a = k * c * Real.sqrt (G * rho) := by
  have hh := positive_scale_squared k c G rho hG hr
  have hn : 0 ≤ k * c * Real.sqrt (G * rho) := by positivity
  nlinarith

theorem fixed_coefficient_density_unique (a k c G r₁ r₂ : ℝ)
    (hk : k ≠ 0) (hc : c ≠ 0) (hG : G ≠ 0)
    (h₁ : a ^ 2 = k ^ 2 * c ^ 2 * G * r₁)
    (h₂ : a ^ 2 = k ^ 2 * c ^ 2 * G * r₂) : r₁ = r₂ := by
  have x := (density_inverse_iff a k c G r₁ hk hc hG).1 h₁
  have y := (density_inverse_iff a k c G r₂ hk hc hG).1 h₂
  exact x.trans y.symm

theorem joint_scale_degeneracy (k rho g u : ℝ) (hu : u ≠ 0) :
    (u * k) ^ 2 * (rho / u ^ 2) = k ^ 2 * rho ∧
    (u ^ 2 * g) * (rho / u ^ 2) = g * rho := by
  constructor <;> field_simp

theorem log_null_direction (k r g t : ℝ) :
    ((k + t) + (r - 2 * t) / 2, ((r - 2 * t) + (g + 2 * t)) / 2) =
      (k + r / 2, (r + g) / 2) := by
  ext <;> ring

theorem Z_coupling_bridge (k c G rho g : ℝ)
    (hk : k ≠ 0) (hc : c ≠ 0) (hG : G ≠ 0) (hr : rho ≠ 0) :
    ((8 * Real.pi / 3) * g * G * rho * c ^ 2) /
        (k ^ 2 * c ^ 2 * G * rho) = (8 * Real.pi / 3) * g / k ^ 2 := by
  field_simp

theorem total_rate_exceeds_vacuum_rate (H Hv Om : ℝ)
    (hH : 0 < H) (hHv : 0 ≤ Hv) (hOm : Om < 1)
    (hs : Hv ^ 2 = Om * H ^ 2) : Hv < H := by
  have hh := mul_lt_mul_of_pos_right hOm (sq_pos_of_pos hH)
  nlinarith

theorem thermometric_equality_iff (a H c pref : ℝ)
    (hc : c ≠ 0) (hp : pref ≠ 0) : pref * a / c = pref * H ↔ a = c * H := by
  constructor
  · intro h
    have h1 := (div_eq_iff hc).1 h
    apply mul_left_cancel₀ hp
    calc
      pref * a = pref * H * c := h1
      _ = pref * (c * H) := by ring
  · intro h
    rw [h]
    field_simp

theorem calibrated_density_round_trip (a d Q rho : ℝ)
    (ha : a ≠ 0) (hd : d ≠ 0) (hQ : Q ≠ 0) (hs : d ^ 2 = Q * rho) :
    a ^ 2 / ((a / d) ^ 2 * Q) = rho := by
  calc
    a ^ 2 / ((a / d) ^ 2 * Q) = d ^ 2 / Q := by field_simp
    _ = rho := by rw [hs]; field_simp

theorem same_action_coupling_ratio (Gbare C D : ℝ)
    (hG : Gbare ≠ 0) (hC : C ≠ 0) (hD : D ≠ 0) :
    (Gbare / D) / (Gbare / C) = C / D := by field_simp

theorem horizon_acceleration_ratio (a c H : ℝ)
    (ha : a ≠ 0) (hc : c ≠ 0) (hH : H ≠ 0) :
    (c ^ 2 / a) / (c / H) = c * H / a := by field_simp

end ScalesInverse20260926

#print axioms ScalesInverse20260926.positive_scale_squared
#print axioms ScalesInverse20260926.density_inverse_iff
#print axioms ScalesInverse20260926.nonnegative_branch_reconstruction
#print axioms ScalesInverse20260926.fixed_coefficient_density_unique
#print axioms ScalesInverse20260926.joint_scale_degeneracy
#print axioms ScalesInverse20260926.log_null_direction
#print axioms ScalesInverse20260926.Z_coupling_bridge
#print axioms ScalesInverse20260926.total_rate_exceeds_vacuum_rate
#print axioms ScalesInverse20260926.thermometric_equality_iff
#print axioms ScalesInverse20260926.calibrated_density_round_trip
#print axioms ScalesInverse20260926.same_action_coupling_ratio
#print axioms ScalesInverse20260926.horizon_acceleration_ratio
