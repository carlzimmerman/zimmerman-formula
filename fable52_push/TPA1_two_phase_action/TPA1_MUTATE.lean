/-
TPA1_MUTATE (criteria b81c28d00c): deliberately false versions of TPA1.lean's statements, with the true file's proof
attempts. Every one must fail; the file must not compile. TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.

  M_pa_only_same      : S on P.A alone claimed to keep the S-free Legendre map (false for S /= 1).
  M_stress_jump_flip  : the momentum-flux jump claimed equal to -W_wall (the M1 sign) for u >= 0.
  M_leaf_stress_drop  : the leaf stress with the 2 P d l component dropped, claimed equal to -S W (the M3 type).
  M_static_antitone   : the static-clock switch claimed antitone in N (the cleared-disc direction).
  M_dPi_flip          : the force density along fixed displacement claimed to be -J.
-/
import Mathlib

namespace TPA1M

noncomputable def Wd (x : ℝ) : ℝ := -x - Real.log (1 - x)
noncomputable def J (u : ℝ) : ℝ := u - Real.log (1 + u)
noncomputable def Wwall (u : ℝ) : ℝ := u - Real.log (1 + u) - u ^ 2 / (2 * (1 + u) ^ 2)

theorem M_pa_only_same (S u x : ℝ) (hx : x < 1) (hu : 0 ≤ u) :
    S * u - x / (1 - x) = 0 ↔ x = u / (1 + u) := by
  have hp : (1 - x) ≠ 0 := by linarith
  have hq : (1 + u) ≠ 0 := by linarith
  constructor
  · intro h
    have h3 : u = x / (1 - x) := by linarith
    rw [h3]; field_simp; ring
  · intro h
    rw [h]; field_simp; ring

theorem M_stress_jump_flip (u : ℝ) (hu : 0 ≤ u) :
    (u ^ 2 / 2 - 1 * Wd (u / (1 + u))) - ((u ^ 2 / (1 + u)) ^ 2 / 2 - 0 * Wd 0) = -Wwall u := by
  unfold Wd Wwall
  have hq : (0 : ℝ) < 1 + u := by linarith
  have h1 : 1 - u / (1 + u) = (1 + u)⁻¹ := by field_simp; ring
  rw [h1, Real.log_inv]
  field_simp
  ring

theorem M_leaf_stress_drop (S p E Wv : ℝ) :
    S * ((p * E - Wv) + E * p) = -(S * Wv) := by ring

theorem M_static_antitone (S : ℝ → ℝ) (hS : Antitone S) (c Qi : ℝ) (hc : 0 < c) (hQ : 0 < Qi) :
    AntitoneOn (fun N : ℝ => S (c * (Qi / N - 1))) (Set.Ioi 0) := by
  intro N₁ h₁ N₂ h₂ h12
  have h1 : (0 : ℝ) < N₁ := h₁
  apply hS
  have : Qi / N₂ ≤ Qi / N₁ := div_le_div_of_nonneg_left hQ.le h1 h12
  have h3 : Qi / N₂ - 1 ≤ Qi / N₁ - 1 := by linarith
  exact mul_le_mul_of_nonneg_left h3 hc.le

theorem M_dPi_flip (S E : ℝ) (hE : 0 ≤ E) (hden : 1 - S / (1 + E) ^ 2 ≠ 0) :
    -Wd (E / (1 + E)) - (E * (1 - S / (1 + E) ^ 2)) * (-(E / (1 + E))) / (1 - S / (1 + E) ^ 2) = -J E := by
  rw [mul_div_right_comm, mul_div_cancel_right₀ _ hden]
  unfold Wd J
  have hq : (0 : ℝ) < 1 + E := by linarith
  have h1 : 1 - E / (1 + E) = (1 + E)⁻¹ := by field_simp; ring
  rw [h1, Real.log_inv]
  field_simp
  ring

end TPA1M

-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
