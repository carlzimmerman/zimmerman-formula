/-
COL1 MUTATE twin: the statements of COL1.lean with a sign or factor flipped. Every theorem below is false and must fail to
compile (expected: exit 1, one error per theorem). TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.
-/
import Mathlib

namespace COL1_MUTATE

theorem jeans_polytrope_flip (K n mu : ℝ) (hmu : mu ≠ 0) : (K * n / mu ^ 2) * mu ^ 2 = -K * n := by
  field_simp

theorem lawon_cancel_flip (K N k : ℝ) (hk : k ≠ 0) :
    -K * N / k ^ 2 - K * N / ((0 : ℝ) ^ 2 + k ^ 2) = 0 := by
  have : (0 : ℝ) ^ 2 + k ^ 2 = k ^ 2 := by ring
  rw [this]
  ring

theorem law_point_flip (a0 u : ℝ) (hu : 1 + u ≠ 0) :
    (a0 * u / (1 + u)) ^ 2 = (a0 * u ^ 2 / (1 + u)) * (a0 + a0 * u / (1 + u)) := by
  field_simp
  ring

theorem shell_frequency_flip (a0 u r : ℝ) (hu : 1 + u ≠ 0) (hr : r ≠ 0) :
    2 * a0 * (u / (1 + u)) ^ 2 / (r * (1 - u / (1 + u)) ^ 2) = 2 * a0 * u / r := by
  have h1 : 1 - u / (1 + u) = 1 / (1 + u) := by
    field_simp
    ring
  rw [h1]
  field_simp

theorem wkb_reduced_flip (K N0 k m mu : ℝ) (hK : K ≠ 0) (hk : k ≠ 0) (hd : mu ^ 2 + K * m * k ^ 2 ≠ 0) :
    N0 * k ^ 2 * (1 - K * m - mu ^ 2 / k ^ 2) / (mu ^ 2 / K + m * k ^ 2)
      = K * N0 * ((1 + K * m) * k ^ 2 - mu ^ 2) / (mu ^ 2 + K * m * k ^ 2) := by
  have h2 : mu ^ 2 / K + m * k ^ 2 = (mu ^ 2 + K * m * k ^ 2) / K := by
    field_simp
  rw [h2]
  field_simp
  ring

theorem flux_cap_flip (a0 A : ℝ) (ha : 0 < a0) (hA : 0 ≤ A) : a0 < a0 * A / (a0 + A) := by
  have h : 0 < a0 + A := by linarith
  rw [lt_div_iff₀ h]
  nlinarith

theorem pericentre_flip (G m a0 M : ℝ) (ha : a0 ≠ 0) (hM : M ≠ 0) :
    G * m ^ 2 / (a0 * M) = 2 * (G * m ^ 2 / (3 * a0 * M)) := by
  field_simp

end COL1_MUTATE

-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
