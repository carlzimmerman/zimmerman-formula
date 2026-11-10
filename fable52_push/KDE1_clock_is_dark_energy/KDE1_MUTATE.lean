/-
KDE1 MUTATE twin (criteria 592b8291d1): each statement of KDE1.lean stated falsely, with the same proof scripts.
Every one must fail to compile. TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.

  balance_iff_lawS   : sign of a0 flipped in law S.
  freq_capped        : the frequency claimed above E.
  phase_speed_small  : the phase speed claimed to stay above eta.
  Ks2_native         : kappa^2 moved from the denominator to the numerator.
  largest_case       : Omega tau_f claimed above 1 (the clock would hold against the fold).
-/
import Mathlib

namespace KDE1_MUTATE

noncomputable def mu (x : ℝ) : ℝ := x / (1 + x)

theorem balance_iff_lawS (g gN a0 : ℝ) (hg : 0 ≤ g) (ha : 0 < a0) :
    mu (g / a0) * g = gN ↔ g ^ 2 = gN * (g - a0) := by
  have h1 : 0 < 1 + g / a0 := by positivity
  have h2 : 0 < g + a0 := by linarith
  have key : mu (g / a0) * g = g ^ 2 / (g + a0) := by
    unfold mu; field_simp; ring
  rw [key, div_eq_iff h2.ne']

theorem freq_capped (E x : ℝ) (hE : 0 < E) (hx : 0 < x) :
    E < E * x ^ 2 / (E + x ^ 2) := by
  have hd : 0 < E + x ^ 2 := by positivity
  rw [lt_div_iff₀ hd]
  nlinarith [mul_pos hE hE]

theorem phase_speed_small (E x η : ℝ) (hE : 0 < E) (hη : 0 < η) (hx : E / η < x ^ 2) :
    η < E / (E + x ^ 2) := by
  have hd : 0 < E + x ^ 2 := by positivity
  rw [lt_div_iff₀ hd]
  have h2 : E < η * x ^ 2 := by
    rw [div_lt_iff₀ hη] at hx; linarith
  nlinarith [mul_pos hη hE]

theorem Ks2_native (G w rho a0 κ : ℝ) (hκ : κ ≠ 0) (ha : a0 ^ 2 = κ ^ 2 * G * rho) :
    4 * Real.pi * G * ((1 + w) * rho) = 4 * Real.pi * (1 + w) * a0 ^ 2 * κ ^ 2 := by
  rw [ha]; field_simp

theorem largest_case :
    1 < 8 * Real.pi * ((1.1312e-10 : ℝ) * (0.154 * 3.15576e16) / ((1 / 2) * 299792458)) ^ 2 := by
  have h := Real.pi_lt_d2
  have hp := Real.pi_pos
  norm_num
  nlinarith

end KDE1_MUTATE
