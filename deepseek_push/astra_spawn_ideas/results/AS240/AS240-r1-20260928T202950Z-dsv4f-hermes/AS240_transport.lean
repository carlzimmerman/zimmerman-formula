import Mathlib

noncomputable section

open Real

-- AS240-r1  Lean certificate (seed AS240, gravitational-wave amplitude transport)
-- --------------------------------------------------------------------------------
-- T1 transport_law:  the WKB amplitude law A(eta) = A0 * a0 / a(eta) satisfies the
--   amplitude-order (transport) equation of the tensor wave operator on the
--   homogeneous FRW branch,  A' + (a'/a) A = 0, identically in eta
--   (substitution back into the original equation; as240_derive D3).
-- T2 flux_scaling:   with conformal frequency omega = omega0*a0/a and amplitude
--   A = A0*a0/a the GW flux density F ~ omega^2 A^2 dilutes as a^-4:
--   F(eta)*a(eta)^4 = F(eta0)*a0^4  (the luminosity-distance bookkeeping that
--   yields D_L^GW = D_L^EM for constant M_P; as240_derive D4).

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

end