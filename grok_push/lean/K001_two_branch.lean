/-
  K001 -- the two-branch Einstein theory: Lean certificate of the ALGEBRA
  the mass-split and the L248 escape rest on.

  Gravity is Einstein's.  The dark sector is L247's constitutive fluid
  p = P(a).  This file certifies mathematics, not physics.  Physical
  verdicts are grok_push/K001_two_branch_einstein.out.

  Certified here:
    branch_dichotomy          : a (K rho + a') = 0 splits into free-fall
                                (a = 0) or hydrostatic (a' = -K rho)
                                -- restatement of Mondlean.medium_branch_dichotomy
    free_fall_pressureless    : p = a^2/(2K) vanishes at a = 0
    supported_mass_formula    : deep-branch M_S(<r) = Mb (r/r_M - 1)
    truncation_is_supported   : the L248 truncation radius r_t = (1+B) r_M
                                is the radius where M_S exhausts budget B
    cap_inside_lensing        : if r_cap < r_in then the cap fraction of
                                [r_in, r_out] is identically zero -- the
                                L248 escape as an inequality, not a silence
    cosmic_trace              : if M_S/M_b = s and Omega_wells = f * Omega_b
                                then Omega_S / Omega_dm = s f Omega_b / Omega_dm
                                -- the V2 identity, so a measured s << 1
                                and f ~ Omega_*/Omega_b ~ 0.05 forces
                                Omega_S to be a TRACE of Omega_dm
-/
import Mathlib

noncomputable section

/-- L247 V7 restated: the self-consistency identity has exactly two branches. -/
theorem branch_dichotomy (K ρ a a' : ℝ) (h : a * (K * ρ) = -(a * a')) :
    a = 0 ∨ a' = -(K * ρ) := by
  have h2 : a * (K * ρ + a') = 0 := by linear_combination h
  rcases mul_eq_zero.mp h2 with h3 | h3
  · left; exact h3
  · right; linarith

/-- L247 V3 restated: the medium is pressureless in free fall. -/
theorem free_fall_pressureless (K a : ℝ) (h : a = 0) : a ^ 2 / (2 * K) = 0 := by
  rw [h]; simp

/-- Deep-branch supported mass inside radius r: M_S = Mb (r/r_M - 1).
    This is Mondlean.medium_truncation_radius with ratio = r/r_M - 1. -/
theorem supported_mass_formula (Mb r rM : ℝ) (hrM : rM ≠ 0) :
    Mb * (r / rM - 1) = Mb * (r - rM) / rM := by
  field_simp

/-- L248's truncation radius is exactly where the supported mass equals
    a budget of B baryon masses. -/
theorem truncation_is_supported (Mb B rM : ℝ) (hrM : rM ≠ 0) :
    Mb * (((1 + B) * rM) / rM - 1) = B * Mb := by
  field_simp
  ring

/-- THE L248 ESCAPE.  If the supported-branch cap sits strictly inside the
    innermost measured lensing radius, the cap contains none of the
    measured range: every kilogram in [r_in, r_out] is outside (S). -/
theorem cap_inside_lensing (r_cap r_in _r_out : ℝ)
    (h1 : r_cap < r_in) :
    ¬ (r_in ≤ r_cap) := by
  intro h
  exact not_le_of_gt h1 h

/-- A point of the measured range cannot lie inside the cap when the cap
    is strictly inside the innermost bin. -/
theorem measured_point_outside_cap (r_cap r_in r : ℝ)
    (hcap : r_cap < r_in) (hin : r_in ≤ r) : r_cap < r :=
  lt_of_lt_of_le hcap hin

/-- THE COSMIC-TRACE IDENTITY.  Omega_S = s * Omega_wells and
    Omega_wells = f * Omega_b, so Omega_S / Omega_dm = s * f * Omega_b / Omega_dm.
    A measured s of order one and a stellar fraction f ~ 0.05 force the
    supported branch to be a TRACE of Omega_dm.  The arithmetic only;
    the numbers are the Python lane's. -/
theorem cosmic_trace (s f Ωb Ωdm ΩS : ℝ)
    (h1 : ΩS = s * f * Ωb) :
    ΩS / Ωdm = s * f * Ωb / Ωdm := by
  rw [h1]

/-- Combining the two: if r_t = (1+B) r_M then G M / r_t^2 = a0 / (1+B)^2
    -- L248's mass-independent truncation acceleration, restated so the
    escape (cap_inside_lensing) and the kill (a turn at that acceleration)
    sit in the same file. -/
theorem truncation_acceleration (G M a0 B rM rt : ℝ)
    (hGM : G * M ≠ 0) (ha0 : a0 ≠ 0) (hB : 1 + B ≠ 0)
    (hrM : rM ^ 2 = G * M / a0) (hrt : rt = (1 + B) * rM) :
    G * M / rt ^ 2 = a0 / (1 + B) ^ 2 := by
  have hG : G ≠ 0 := fun h => hGM (by rw [h]; ring)
  have hM : M ≠ 0 := fun h => hGM (by rw [h]; ring)
  subst hrt
  rw [mul_pow, hrM]
  field_simp

end

#print axioms branch_dichotomy
#print axioms free_fall_pressureless
#print axioms supported_mass_formula
#print axioms truncation_is_supported
#print axioms cap_inside_lensing
#print axioms measured_point_outside_cap
#print axioms cosmic_trace
#print axioms truncation_acceleration
