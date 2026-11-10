/-
KDE1 (criteria 592b8291d1): Lean statements for the closed forms the lane uses. They certify the algebra, not the physics.
TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.

  balance_iff_lawS   : (KA2b) with mu(x) = x/(1+x), mu(g/a0) g = g_N iff g^2 = g_N (g + a0)  (QX1's theorem, restated).
  freq_capped        : AC2's FRW clock frequency at Lstar = 0, omega^2 = E x^2/(E + x^2) (E = eps H^2 = K phidot^2,
                       x^2 = k^2 in the same units), is below E at every k: the clock never rings faster than
                       sqrt(K phidot^2), however short the wavelength.
  phase_speed_small  : its phase speed squared E/(E + x^2) is below any eta > 0 once x^2 > E/eta (it goes to zero).
  Ks2_native         : 4 pi G (1+w) rho = 4 pi (1+w) a0^2/kappa^2 when a0^2 = kappa^2 G rho (c = 1): the clock's rate
                       squared in framework-native form.
  largest_case       : the largest D1 case (alt a0 1.1312e-10 m/s^2, 1+w = 2, COL1's later fold time 0.154 Gyr):
                       Omega^2 tau_f^2 = 8 pi (a0 tau_f/(kappa c))^2 < (1/50)^2, i.e. Omega tau_f < 1/50.
-/
import Mathlib

namespace KDE1

noncomputable def mu (x : ℝ) : ℝ := x / (1 + x)

theorem balance_iff_lawS (g gN a0 : ℝ) (hg : 0 ≤ g) (ha : 0 < a0) :
    mu (g / a0) * g = gN ↔ g ^ 2 = gN * (g + a0) := by
  have h1 : 0 < 1 + g / a0 := by positivity
  have h2 : 0 < g + a0 := by linarith
  have key : mu (g / a0) * g = g ^ 2 / (g + a0) := by
    unfold mu; field_simp; ring
  rw [key, div_eq_iff h2.ne']

theorem freq_capped (E x : ℝ) (hE : 0 < E) (hx : 0 < x) :
    E * x ^ 2 / (E + x ^ 2) < E := by
  have hd : 0 < E + x ^ 2 := by positivity
  rw [div_lt_iff₀ hd]
  nlinarith [mul_pos hE hE]

theorem phase_speed_small (E x η : ℝ) (hE : 0 < E) (hη : 0 < η) (hx : E / η < x ^ 2) :
    E / (E + x ^ 2) < η := by
  have hd : 0 < E + x ^ 2 := by positivity
  rw [div_lt_iff₀ hd]
  have h2 : E < η * x ^ 2 := by
    rw [div_lt_iff₀ hη] at hx; linarith
  nlinarith [mul_pos hη hE]

theorem Ks2_native (G w rho a0 κ : ℝ) (hκ : κ ≠ 0) (ha : a0 ^ 2 = κ ^ 2 * G * rho) :
    4 * Real.pi * G * ((1 + w) * rho) = 4 * Real.pi * (1 + w) * a0 ^ 2 / κ ^ 2 := by
  rw [ha]; field_simp

theorem largest_case :
    8 * Real.pi * ((1.1312e-10 : ℝ) * (0.154 * 3.15576e16) / ((1 / 2) * 299792458)) ^ 2 < (1 / 50) ^ 2 := by
  have h := Real.pi_lt_d2
  have hp := Real.pi_pos
  norm_num
  nlinarith

end KDE1
