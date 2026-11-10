/-
SCS2_MUTATE (criteria 158c4cf770): deliberately false versions of SCS2.lean's statements with the true file's proof
attempts. Every one must fail; the file must not compile. TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.

  M_aniso_any_sign   : the anisotropic form claimed positive even with J_par < 0.
  M_Km_le_one_u0     : K m < 1 claimed at u = 0 (it equals 1 there).
  M_sign_flip        : omega^2 claimed to have the sign of -G (the M1 tilt flip).
  M_nu_monotone      : nu claimed monotone (increasing) on y > 0.
  M_far_field        : the far-field exponent claimed to be 1/(1+x)^2.
  M_stiffness_bounded: with the stiffness on and G < 0, omega^2 claimed never to fall below its k = 0 value.
  M_band_positive    : the far-field phantom claimed positive in the band (the sign of the band flipped).
(The last two were added with the true file's last four; compile_MUTATE.txt is the recompile of the whole file.)
-/
import Mathlib

namespace SCS2M

theorem M_aniso_any_sign (p q r a b c Jpar Jperp : ℝ) (hg : p ^ 2 + q ^ 2 + r ^ 2 = 1)
    (hperp : 0 < Jperp) (hv : a ^ 2 + b ^ 2 + c ^ 2 ≠ 0) :
    0 < Jperp * (a ^ 2 + b ^ 2 + c ^ 2) + (Jpar - Jperp) * (p * a + q * b + r * c) ^ 2 := by
  have hpos : 0 < a ^ 2 + b ^ 2 + c ^ 2 := by positivity
  nlinarith [sq_nonneg (p * b - q * a), sq_nonneg (p * c - r * a), sq_nonneg (q * c - r * b)]

theorem M_Km_le_one_u0 (c s : ℝ) (hcs : c ^ 2 + s ^ 2 = 1) :
    c ^ 2 / (1 + 0) ^ 2 + s ^ 2 / (1 + 0) < 1 := by
  norm_num
  linarith

theorem M_sign_flip (G Km m : ℝ) (hm : 0 < m) (hK0 : 0 < Km) (hK1 : Km < 1) (hG : 0 < G) :
    G * (1 - Km) / m < 0 := by
  have h1 : 0 < 1 - Km := by linarith
  exact div_neg_of_neg_of_pos (mul_neg_of_neg_of_pos hG h1) hm

noncomputable def nu (y : ℝ) : ℝ := 1 / 2 + Real.sqrt (1 / 4 + 1 / y)

theorem M_nu_monotone : MonotoneOn nu (Set.Ioi 0) := by
  intro y₁ h₁ y₂ h₂ h12
  have hy1 : (0 : ℝ) < y₁ := h₁
  unfold nu
  have : 1 / y₂ ≤ 1 / y₁ := one_div_le_one_div_of_le hy1 h12
  have : Real.sqrt (1 / 4 + 1 / y₂) ≤ Real.sqrt (1 / 4 + 1 / y₁) := Real.sqrt_le_sqrt (by linarith)
  linarith

theorem M_far_field (x : ℝ) (hx : 0 < x) :
    x * (1 / (1 + x) ^ 2) / (x / (1 + x)) = 1 / (1 + x) ^ 2 := by
  have h1 : (0 : ℝ) < 1 + x := by linarith
  field_simp

theorem M_stiffness_bounded (K G m g : ℝ) (hG : G < 0) (hm : 0 < m) (hg : 0 < g * m) (k2 : ℝ) (hk : 0 ≤ k2) :
    G * (1 - K * m) / m ≤ G * (1 + g * m * k2 - K * m) / m := by
  have hslope : G * g < 0 := by nlinarith
  rw [div_le_div_iff_of_pos_right hm]
  nlinarith

theorem M_band_positive (A L s5 rp2 z : ℝ) (hA : 0 < A) (hL : 0 < L) (hs : 0 < s5)
    (hband : 2 * z ^ 2 / (1 + L) < rp2) :
    0 < -L * A * (rp2 - 2 * z ^ 2 / (1 + L)) / ((1 + L) * s5) := by
  have h1 : 0 < rp2 - 2 * z ^ 2 / (1 + L) := by linarith
  have h2 : 0 < (1 + L) * s5 := by positivity
  exact div_pos (by positivity) h2

end SCS2M

-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
