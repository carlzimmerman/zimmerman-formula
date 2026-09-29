import Mathlib
import ChainCert.Chain

/-!
# ChainCert.Fluid -- the algebra of CFG43's fluid cap and its tie to Lambda

CFG43 writes the a0-Lambda tie into a conserved fluid's stress cap.  With c = 1 and M_P^2 = 1/(8 pi G):

    rho(n) = m n + P_cap x arctan x,   x = m n / s,      P = n rho'(n) - rho(n)

Certified here (premises => conclusion; the cap's entry FORM is a hypothesis of the action, not derived):
* the pressure of that equation of state is P_cap x^2/(1+x^2), which lies in [0, P_cap);
* the cap defines an acceleration a0 = sqrt(8 pi G P_cap) whose square is kappa^2 Lambda/(8 pi) when P_cap = (kappa^2/8 pi) M_P^2 Lambda,
  i.e. the fluid's cap reads the same Lambda-function as the kernel's alpha(Lambda) c^2 = kappa sqrt(Lambda/8 pi).
NOT certified: that the cap must take this form (POSTULATED), the field equations of the action (run by CFG43's sympy scripts), or the
scoped obstruction (numerical, CFG43 A3).
-/

open Filter Topology

noncomputable def rhoFluid (m Pc s : ℝ) (n : ℝ) : ℝ := m * n + Pc * (m * n / s) * Real.arctan (m * n / s)

theorem rhoFluid_hasDeriv (m Pc s n : ℝ) (hs : s ≠ 0) :
    HasDerivAt (rhoFluid m Pc s)
      (m + Pc * (m / s) * (Real.arctan (m * n / s) + (m * n / s) / (1 + (m * n / s) ^ 2))) n := by
  have hx : HasDerivAt (fun n : ℝ => m * n / s) (m / s) n := by
    simpa [div_eq_mul_inv, mul_comm, mul_left_comm, mul_assoc] using ((hasDerivAt_id n).const_mul m).mul_const s⁻¹
  have hatan : HasDerivAt (fun n : ℝ => Real.arctan (m * n / s)) (1 / (1 + (m * n / s) ^ 2) * (m / s)) n := by
    simpa using hx.arctan
  have hprod : HasDerivAt (fun n : ℝ => (m * n / s) * Real.arctan (m * n / s))
      ((m / s) * Real.arctan (m * n / s) + (m * n / s) * (1 / (1 + (m * n / s) ^ 2) * (m / s))) n := hx.mul hatan
  have hlin : HasDerivAt (fun n : ℝ => m * n) m n := by simpa using (hasDerivAt_id n).const_mul m
  have hfull := hlin.add (hprod.const_mul Pc)
  have hfun : rhoFluid m Pc s = (fun n : ℝ => m * n) + fun y : ℝ => Pc * (m * y / s * Real.arctan (m * y / s)) := by
    funext y
    simp only [rhoFluid, Pi.add_apply]
    ring
  rw [hfun]
  refine hfull.congr_deriv ?_
  field_simp

/-- the pressure of the saturating cap: P = n rho' - rho = P_cap x^2 / (1 + x^2) -/
theorem fluid_pressure (m Pc s n : ℝ) (hs : s ≠ 0) :
    n * deriv (rhoFluid m Pc s) n - rhoFluid m Pc s n = Pc * ((m * n / s) ^ 2 / (1 + (m * n / s) ^ 2)) := by
  rw [(rhoFluid_hasDeriv m Pc s n hs).deriv]
  unfold rhoFluid
  field_simp
  ring

/-- the pressure never exceeds the cap and is non-negative (P_cap >= 0) -/
theorem fluid_pressure_bounds (m Pc s n : ℝ) (hs : s ≠ 0) (hPc : 0 ≤ Pc) :
    0 ≤ n * deriv (rhoFluid m Pc s) n - rhoFluid m Pc s n ∧
      n * deriv (rhoFluid m Pc s) n - rhoFluid m Pc s n < Pc ∨ Pc = 0 := by
  rcases hPc.eq_or_lt with h | h
  · exact Or.inr h.symm
  · left
    rw [fluid_pressure m Pc s n hs]
    have hx : 0 ≤ (m * n / s) ^ 2 := sq_nonneg _
    have hd : 0 < 1 + (m * n / s) ^ 2 := by positivity
    refine ⟨mul_nonneg hPc (div_nonneg hx hd.le), ?_⟩
    have : (m * n / s) ^ 2 / (1 + (m * n / s) ^ 2) < 1 := by
      rw [div_lt_one hd]; linarith
    nlinarith

/-- the tie: with P_cap = (kappa^2/(8 pi)) M_P^2 Lambda and M_P^2 = 1/(8 pi G), the acceleration a0^2 = 8 pi G P_cap equals
    kappa^2 Lambda/(8 pi): the fluid's cap reads the same Lambda-function as the kernel (a0 = kappa sqrt(Lambda/(8 pi))) -/
theorem cap_a0_tie {G κ Λ : ℝ} (hG : 0 < G) :
    8 * Real.pi * G * ((κ ^ 2 / (8 * Real.pi)) * (1 / (8 * Real.pi * G)) * Λ) = κ ^ 2 * Λ / (8 * Real.pi) := by
  have hπ : (Real.pi) ≠ 0 := Real.pi_ne_zero
  field_simp

theorem cap_a0_eq {G κ Λ : ℝ} (hG : 0 < G) (hκ : 0 < κ) (hΛ : 0 ≤ Λ) :
    Real.sqrt (8 * Real.pi * G * ((κ ^ 2 / (8 * Real.pi)) * (1 / (8 * Real.pi * G)) * Λ)) = κ * Real.sqrt (Λ / (8 * Real.pi)) := by
  rw [cap_a0_tie hG]
  have h : κ ^ 2 * Λ / (8 * Real.pi) = κ ^ 2 * (Λ / (8 * Real.pi)) := by ring
  rw [h, Real.sqrt_mul (sq_nonneg κ), Real.sqrt_sq hκ.le]
