/-
SMF1 AMENDMENT A1 (cfa91d3feb): Lean cores of the collisionless checks. They certify the algebra, not the physics.
TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.

  kinetic_starvation : C2, a non-negative phase-space density with zero total (zero local density) gives zero loss
                       Sum gamma_i f_i into the frame, for any rates gamma_i.
  c1_collisionless   : C3, the growing root's k^2 coefficient
                       (K n^2 - lam mu^2 n - lam mu^2 rho + mu^2 rho s^2)/(mu^2 (n + rho))
                       = s^2 rho/(n + rho) - lam + K n^2/(mu^2 (n + rho)).
  saturation_le_jeans: C3, for s > 0: lam (K rho + mu^2 s^2)/s^2 <= K (n + rho) iff lam (K rho + mu^2 s^2) <= K (n + rho) s^2.
-/
import Mathlib.Tactic

namespace SMF1_A1

theorem kinetic_starvation {n : ℕ} (f gam : Fin n → ℝ) (hf : ∀ i, 0 ≤ f i)
    (hs : (Finset.univ.sum fun i => f i) = 0) : (Finset.univ.sum fun i => gam i * f i) = 0 := by
  have h0 : ∀ i ∈ Finset.univ, f i = 0 :=
    (Finset.sum_eq_zero_iff_of_nonneg (fun i _ => hf i)).mp hs
  apply Finset.sum_eq_zero
  intro i hi
  rw [h0 i hi]; ring

theorem c1_collisionless (K n lam mu rho s : ℝ) (hmu : mu ≠ 0) (hnr : n + rho ≠ 0) :
    (K * n ^ 2 - lam * mu ^ 2 * n - lam * mu ^ 2 * rho + mu ^ 2 * rho * s ^ 2) / (mu ^ 2 * (n + rho))
      = s ^ 2 * rho / (n + rho) - lam + K * n ^ 2 / (mu ^ 2 * (n + rho)) := by
  field_simp; ring

theorem saturation_le_jeans (K n lam mu rho s : ℝ) (hs : 0 < s) :
    lam * (K * rho + mu ^ 2 * s ^ 2) / s ^ 2 ≤ K * (n + rho) ↔ lam * (K * rho + mu ^ 2 * s ^ 2) ≤ K * (n + rho) * s ^ 2 := by
  rw [div_le_iff₀ (by positivity)]

end SMF1_A1

#print axioms SMF1_A1.kinetic_starvation
#print axioms SMF1_A1.c1_collisionless
#print axioms SMF1_A1.saturation_le_jeans

-- Adopts nothing. kappa = 1/2 FITTED; not theory closed.
