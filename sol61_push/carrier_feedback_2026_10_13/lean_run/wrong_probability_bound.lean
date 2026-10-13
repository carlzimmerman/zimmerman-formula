import Mathlib

/-! Conditional cold-source collision and lifetime algebra. Scattering theory,
quantization, Markov admission, and source-state selection are not formalized. -/
noncomputable section
namespace CarrierFeedback

theorem energy_fraction (r z : ℝ) (hr : 1 + r ≠ 0) :
    (1 + r ^ 2 + 2 * r * z) / (1 + r) ^ 2 =
      1 - (4 * r / (1 + r) ^ 2) * (1 - z) / 2 := by
  field_simp
  ring

theorem near_threshold_mean_loss :
    (4 * (2 : ℝ) / (1 + 2) ^ 2) / 2 = 4 / 9 := by norm_num

theorem cold_collision_no_heating (a z : ℝ)
    (ha : 0 ≤ a) (hz : z ≤ 1) :
    1 - a * (1 - z) / 2 ≤ 1 := by
  have h := mul_nonneg ha (sub_nonneg.mpr hz)
  linarith

theorem source_rate_ratio (nb mu C v m eps delta pi : ℝ)
    (hm : m ≠ 0) (he : eps ≠ 0) (hd : delta ≠ 0)
    (hp : pi ≠ 0) (hC : C ≠ 0) :
    (nb * (16 * mu ^ 2 * C ^ 2 / (pi * delta ^ 2)) * v) /
      (C * m ^ 2 * eps / pi) =
        4 * (4 * C * nb / delta ^ 2) * (mu / m) ^ 2 * (v / eps) := by
  field_simp
  ring

theorem weak_density_bound (chi x y : ℝ) (hc : 0 ≤ chi)
    (hx : 0 ≤ x) (hx1 : x ≤ 1) (hy : 0 ≤ y) (hy1 : y ≤ 1) :
    4 * chi * x ^ 2 * y ≤ 4 * chi := by
  have hx2 : x ^ 2 ≤ 1 := by nlinarith
  have hxy : x ^ 2 * y ≤ 1 := by
    calc
      x ^ 2 * y ≤ 1 * y := mul_le_mul_of_nonneg_right hx2 hy
      _ ≤ 1 := by simpa using hy1
  calc
    4 * chi * x ^ 2 * y = (4 * chi) * (x ^ 2 * y) := by ring
    _ ≤ (4 * chi) * 1 := mul_le_mul_of_nonneg_left hxy (by positivity)
    _ = 4 * chi := by ring

theorem first_event_probability_bound (R : ℝ) :
    1 - Real.exp (-R) ≤ R - 1 := by
  have h := Real.add_one_le_exp (-R)
  linarith

theorem third_moment_generator_gap (a : ℝ) :
    (-3 * a / 2 + a ^ 2) -
      (-3 * a / 2 + a ^ 2 - a ^ 3 / 4) = a ^ 3 / 4 := by ring

end CarrierFeedback
#print axioms CarrierFeedback.energy_fraction
#print axioms CarrierFeedback.near_threshold_mean_loss
#print axioms CarrierFeedback.cold_collision_no_heating
#print axioms CarrierFeedback.source_rate_ratio
#print axioms CarrierFeedback.weak_density_bound
#print axioms CarrierFeedback.first_event_probability_bound
#print axioms CarrierFeedback.third_moment_generator_gap
