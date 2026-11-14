/-
XJ1: Lean statements for the algebra of the exact junction. They certify the algebra, not the physics, and no number
or label of the lane. TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.

  junction_factor     : the outside factor t = (T - C_B)/(T - C_R) satisfies t (T - C_R) = T - C_B.
  junction_total      : with that factor the layout reaches the turnaround charge: C_B + t (T - C_R) = T.
  junction_factor_nonneg : t >= 0 when the law's enclosed charge does not exceed the total (KA-E iv).
  junction_outside_monotone : outside R_set the layout C_B + t (C_R(r) - C_R(R_set)) does not decrease when C_R does not.
  rescaled_is_law_iff : FZS1's rescaled inside, s C_B, equals the law's C_B exactly when s = 1 (C_B nonzero).
  rescale_gap         : the charge FZS1's junction leaves out of the law's halo inside R_set is (1 - s) C_B.
-/
import Mathlib

namespace XJ1

theorem junction_factor (T CB CR : ℝ) (h : T - CR ≠ 0) : (T - CB) / (T - CR) * (T - CR) = T - CB := by
  field_simp

theorem junction_total (T CB CR t : ℝ) (ht : t * (T - CR) = T - CB) : CB + t * (T - CR) = T := by
  linarith

theorem junction_factor_nonneg (T CB CR : ℝ) (h1 : CB ≤ T) (h2 : CR < T) : 0 ≤ (T - CB) / (T - CR) := by
  apply div_nonneg <;> linarith

theorem junction_outside_monotone (CB CRs CR1 CR2 t : ℝ) (ht : 0 ≤ t) (h12 : CR1 ≤ CR2) :
    CB + t * (CR1 - CRs) ≤ CB + t * (CR2 - CRs) := by
  have h : t * (CR1 - CRs) ≤ t * (CR2 - CRs) := mul_le_mul_of_nonneg_left (by linarith) ht
  linarith

theorem rescaled_is_law_iff (CB s : ℝ) (h : CB ≠ 0) : s * CB = CB ↔ s = 1 := by
  constructor
  · intro h1
    have h2 : (s - 1) * CB = 0 := by linarith
    rcases mul_eq_zero.mp h2 with h3 | h3
    · linarith
    · exact absurd h3 h
  · intro h1
    rw [h1]
    ring

theorem rescale_gap (CB s : ℝ) : CB - s * CB = (1 - s) * CB := by
  ring

end XJ1

-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
