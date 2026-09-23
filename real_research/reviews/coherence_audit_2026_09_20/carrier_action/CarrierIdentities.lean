import Mathlib

/-! Exact algebraic obligations for the carrier audit. This file does not
formalize metric variation, PDE stability, or the power-function derivative.
The U variable in the completion is (X/X0)^m in the accompanying derivation. -/
namespace CarrierAudit
noncomputable section

def pressure (X X0 p1 g : ℝ) : ℝ :=
  p1 * (X - X0) + g / 2 * (X - X0)^2

def density (X X0 p1 g : ℝ) : ℝ :=
  2 * X * (p1 + g * (X - X0)) - pressure X X0 p1 g

theorem pressure_at_reference (X0 p1 g : ℝ) :
    pressure X0 X0 p1 g = 0 := by simp [pressure]

theorem density_at_reference (X0 p1 g : ℝ) :
    density X0 X0 p1 g = 2 * X0 * p1 := by simp [density, pressure]

/-- Positive sound speed does not imply the proposed equilibrium EOS. -/
theorem pressure_is_not_rho_times_cs :
    pressure 1 1 1 1 ≠ density 1 1 1 1 * ((1 : ℝ) / 3) := by
  norm_num [pressure, density]

/-- This composition lemma applies to every positive-X member of the
smooth constitutive family. The hypothesis makes explicit the remaining
elementary differentiability obligation for the power function. -/
theorem quadratic_in_Y_protects_all_X (P : ℝ → ℝ → ℝ) (d : ℝ → ℝ)
    (h : ∀ X, HasDerivAt (P X) (d X) 0) :
    ∀ X, HasDerivAt (fun (Y : ℝ) => P X (Y ^ (2 : ℕ))) 0 0 := by
  intro X
  have hsq : HasDerivAt (fun Y : ℝ => Y ^ (2 : ℕ)) 0 0 := by
    simpa using hasDerivAt_pow 2 (0 : ℝ)
  have hh : HasDerivAt (P X) (d X) ((fun Y : ℝ => Y ^ (2 : ℕ)) 0) := by
    simpa using h X
  simpa using! HasDerivAt.comp (h := fun Y : ℝ => Y ^ (2 : ℕ))
    (h₂ := P X) (h' := (0 : ℝ)) (h₂' := d X) (0 : ℝ) hh hsq

/-- For the completed positive-X family K=(2m-1)p_X. This proves
the isolated carrier's time kinetic coefficient is positive. -/
theorem completed_kinetic_positive (m pX : ℝ) (hm : 1 / 2 < m)
    (hpX : 0 < pX) : 0 < (2*m-1)*pX := by
  exact mul_pos (by linarith) hpX

/-- At fixed nonzero background current, charge conservation fixes the
scale factor rather than permitting expansion. -/
theorem fixed_current_conservation_forces_fixed_scale
    (a q : ℝ) (hq : q ≠ 0) (hc : a^3 * q = q) : a = 1 := by
  have hcube : a^3 = 1 := by
    apply (mul_right_cancel₀ hq)
    simpa using hc
  have hf : (a - 1) * (a^2 + a + 1) = 0 := by nlinarith [hcube]
  have hp : 0 < a^2 + a + 1 := by nlinarith [sq_nonneg (a + 1 / 2)]
  rcases mul_eq_zero.mp hf with h | h
  · linarith
  · linarith

def completedPressure (rho0 m U : ℝ) := rho0 * (U - 1) / (2*m)
def completedDensity (rho0 m U : ℝ) := rho0 * ((2*m-1)*U+1) / (2*m)

/-- The integrated constant-sound-speed constitutive family is affine
in density, with a nonzero reference density offset. -/
theorem completed_affine_eos (rho0 m U : ℝ)
    (hm : m ≠ 0) (hd : 2*m-1 ≠ 0) :
    completedPressure rho0 m U =
      (completedDensity rho0 m U-rho0)/(2*m-1) := by
  unfold completedPressure completedDensity
  field_simp
  ring

theorem completion_reference_density (rho0 m : ℝ) (hm : m ≠ 0) :
    completedDensity rho0 m 1 = rho0 := by
  unfold completedDensity
  field_simp
  ring

/-- Continuity reduces to this identity once U' / U = -3(1+1/A)/a. -/
theorem completion_FRW_continuity_identity (rho0 A U : ℝ)
    (hA : A ≠ 0) (hAp : A+1 ≠ 0) :
    rho0*A/(A+1)*(-3*(1+1/A)*U) +
      3*(rho0*(A*U+1)/(A+1)+rho0*(U-1)/(A+1)) = 0 := by
  field_simp
  ring

end
end CarrierAudit
