import Mathlib

noncomputable section

open Real

theorem transport_law (a : ℝ → ℝ) (A0 a0 : ℝ)
    (hne : ∀ η : ℝ, a η ≠ 0)
    (hd : ∀ η : ℝ, HasDerivAt a (deriv a η) η) :
    ∀ η : ℝ, deriv (fun t : ℝ => A0 * a0 / a t) η + (deriv a η / a η) * (A0 * a0 / a η) = 0 := by
  intro η
  have hinv : HasDerivAt (fun t : ℝ => (a t)⁻¹) (-(deriv a η) / (a η) ^ 2) η :=
    (hd η).inv (hne η)
  have hmul : HasDerivAt (fun t : ℝ => A0 * a0 * (a t)⁻¹)
      (A0 * a0 * (-(deriv a η) / (a η) ^ 2)) η := hinv.const_mul (A0 * a0)
  have hder : deriv (fun t : ℝ => A0 * a0 / a t) η = A0 * a0 * (-(deriv a η) / (a η) ^ 2) := by
    simpa [div_eq_mul_inv, mul_assoc] using hmul.deriv
  rw [hder]
  field_simp [hne η] <;> ring

theorem flux_scaling (ω0 A0 a0 a : ℝ) (ha : a ≠ 0) :
    ((ω0 * a0 / a) ^ 2) * ((A0 * a0 / a) ^ 2) * a ^ 4 = ω0 ^ 2 * A0 ^ 2 * a0 ^ 4 := by
  field_simp [ha] <;> ring

#print axioms transport_law
#print axioms flux_scaling

end