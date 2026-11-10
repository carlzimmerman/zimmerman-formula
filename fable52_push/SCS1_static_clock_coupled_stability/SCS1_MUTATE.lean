/-
SCS1_MUTATE (criteria 5d2870617c): deliberately false versions of SCS1.lean's statements, with the true file's proof
attempts. Every one must fail; the file must not compile. TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.

  M_decoupled_rate    : the coupled dispersion claimed equal to the decoupled K G k2 / X (mixing dropped).
  M_mixing_mu         : TPA1's factor 1/(1 - K m) claimed exact at mu /= 0.
  M_unstable_mu0      : G > 0 at mu = 0 claimed to give omega^2 < 0.
  M_planar_div        : the spherical divergence claimed equal to p' alone (TPA1's planar model).
  M_decomp_sign       : the bounded decomposition with the wrong sign of the mu^2 term.
-/
import Mathlib

namespace SCS1M

theorem M_decoupled_rate (K G m mu k2 : ℝ) (hK : K ≠ 0) (hk : k2 ≠ 0) (hX : mu ^ 2 + K * m * k2 ≠ 0)
    (hd : k2 - (mu ^ 2 + K * m * k2) ≠ 0) :
    G * k2 / ((mu ^ 2 + K * m * k2) * k2 / (K * (k2 - (mu ^ 2 + K * m * k2))))
      = K * G * k2 / (mu ^ 2 + K * m * k2) := by
  field_simp
  ring

theorem M_mixing_mu (K m mu k2 : ℝ) (hK : K ≠ 0) (hk : k2 ≠ 0) (hX : mu ^ 2 + K * m * k2 ≠ 0)
    (hd : k2 - (mu ^ 2 + K * m * k2) ≠ 0) (h1 : 1 - K * m ≠ 0) :
    ((mu ^ 2 + K * m * k2) * k2 / (K * (k2 - (mu ^ 2 + K * m * k2)))) / ((mu ^ 2 + K * m * k2) / K)
      = 1 / (1 - K * m) := by
  field_simp
  ring

theorem M_unstable_mu0 (K G m k2 : ℝ) (hG : 0 < G) (hm : 0 < m) (hKm : 0 < K * m) (hKm1 : K * m < 1) (hk : 0 < k2) :
    K * G * ((1 - K * m) * k2 - 0 ^ 2) / (0 ^ 2 + K * m * k2) < 0 := by
  have h1 : 0 < (1 - K * m) * k2 := mul_pos (by linarith) hk
  have h2 : 0 < K * m * k2 := mul_pos hKm hk
  apply div_neg_of_neg_of_pos
  · nlinarith
  · simpa using h2

theorem M_planar_div (r p dp : ℝ) (hr : r ≠ 0) :
    (2 * r * p + r ^ 2 * dp) / r ^ 2 = dp := by
  field_simp
  ring

theorem M_decomp_sign (K G m mu k2 : ℝ) (hm : m ≠ 0) (hX : mu ^ 2 + K * m * k2 ≠ 0) :
    K * G * ((1 - K * m) * k2 - mu ^ 2) / (mu ^ 2 + K * m * k2)
      = G * (1 - K * m) / m + G * mu ^ 2 / (m * (mu ^ 2 + K * m * k2)) := by
  field_simp
  ring

end SCS1M

-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
