/-
SMF1 AMENDMENT A1 MUTATE twin: false versions, same tactics; each must fail. TEST lane; adopts nothing.
kappa = 1/2 FITTED; not theory closed.
-/
import Mathlib.Tactic

namespace SMF1_A1_MUTATE

-- MA1: density allowed to take negative values
theorem kinetic_starvation_false {n : ℕ} (f gam : Fin n → ℝ)
    (hs : (Finset.univ.sum fun i => f i) = 0) : (Finset.univ.sum fun i => gam i * f i) = 0 := by
  have h0 : ∀ i ∈ Finset.univ, f i = 0 :=
    (Finset.sum_eq_zero_iff_of_nonneg (fun i _ => le_refl (f i))).mp hs
  apply Finset.sum_eq_zero
  intro i hi
  rw [h0 i hi]; ring

-- stiffness with the stabilizing sign
theorem c1_collisionless_false (K n lam mu rho s : ℝ) (hmu : mu ≠ 0) (hnr : n + rho ≠ 0) :
    (K * n ^ 2 - lam * mu ^ 2 * n - lam * mu ^ 2 * rho + mu ^ 2 * rho * s ^ 2) / (mu ^ 2 * (n + rho))
      = s ^ 2 * rho / (n + rho) + lam + K * n ^ 2 / (mu ^ 2 * (n + rho)) := by
  field_simp; ring

-- inequality the wrong way round
theorem saturation_le_jeans_false (K n lam mu rho s : ℝ) (hs : 0 < s) :
    lam * (K * rho + mu ^ 2 * s ^ 2) / s ^ 2 ≤ K * (n + rho) ↔ K * (n + rho) * s ^ 2 ≤ lam * (K * rho + mu ^ 2 * s ^ 2) := by
  rw [div_le_iff₀ (by positivity)]

end SMF1_A1_MUTATE

-- Adopts nothing. kappa = 1/2 FITTED; not theory closed.
