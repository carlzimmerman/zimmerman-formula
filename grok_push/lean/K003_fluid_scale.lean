/-
  K003 -- GR fluid action algebra at the Zimmerman scale a0 = s/2.

  Lean certifies mathematics, not physics.  Verdicts:
  grok_push/K003_gr_fluid_action.out.

  Certified here:
    mond_scale_pressure : P = a^2/(8 pi G) and s^2 = c^2 G rho_L
                          imply P = rho_L c^2 (a/s)^2 / (8 pi)
    pressure_at_a0      : a = s/2 => P / (rho_L c^2) = 1/(32 pi)
    free_fall_p         : a = 0 => P = 0  (branch F)
-/
import Mathlib

noncomputable section

/-- The Zimmerman scale identity: deep-MOND pressure in dark-energy units. -/
theorem mond_scale_pressure (a s G c rhoL P : ℝ)
    (hG : G ≠ 0) (hs : s ≠ 0) (hc : c ≠ 0)
    (hρ : rhoL ≠ 0)
    (hP : P = a ^ 2 / (8 * Real.pi * G))
    (hs2 : s ^ 2 = c ^ 2 * G * rhoL) :
    P = rhoL * c ^ 2 * (a / s) ^ 2 / (8 * Real.pi) := by
  have hc2 : c ^ 2 ≠ 0 := pow_ne_zero 2 hc
  have hs2ne : s ^ 2 ≠ 0 := pow_ne_zero 2 hs
  subst hP
  calc
    a ^ 2 / (8 * Real.pi * G)
        = rhoL * c ^ 2 * (a ^ 2 / s ^ 2) / (8 * Real.pi) := by
          have : 8 * Real.pi * G ≠ 0 := by
            have : (8 : ℝ) ≠ 0 := by norm_num
            exact mul_ne_zero (mul_ne_zero this Real.pi_ne_zero) hG
          field_simp
          have hden : c ^ 2 * G * rhoL ≠ 0 :=
            mul_ne_zero (mul_ne_zero hc2 hG) hρ
          rw [hs2]
          field_simp [hden]
    _ = rhoL * c ^ 2 * (a / s) ^ 2 / (8 * Real.pi) := by
          rw [div_pow]

/-- At the characteristic acceleration a = s/2 the pressure is 1/(32 pi)
    of the dark-energy density. -/
theorem pressure_at_a0 (s G c rhoL P : ℝ)
    (hG : G ≠ 0) (hs : s ≠ 0) (hc : c ≠ 0) (hρ : rhoL ≠ 0)
    (hP : P = (s / 2) ^ 2 / (8 * Real.pi * G))
    (hs2 : s ^ 2 = c ^ 2 * G * rhoL) :
    P = rhoL * c ^ 2 / (32 * Real.pi) := by
  have h := mond_scale_pressure (s / 2) s G c rhoL P hG hs hc hρ hP hs2
  rw [h]
  field_simp
  ring

/-- Branch (F): vanishing acceleration => vanishing pressure. -/
theorem free_fall_p (G a : ℝ) (h : a = 0) :
    a ^ 2 / (8 * Real.pi * G) = 0 := by
  rw [h]; simp

end

#print axioms mond_scale_pressure
#print axioms pressure_at_a0
#print axioms free_fall_p
