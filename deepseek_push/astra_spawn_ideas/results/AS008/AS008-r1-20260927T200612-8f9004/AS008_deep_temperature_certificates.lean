import Mathlib
import Mathlib.Tactic

/-!
AS008 -- Deep temperature as a velocity scale: Lean 4 certificates.

Framework cell (CORE scale identities, group A01), inputs per
FRAMEWORK_CONTRACT.md: a0 = kappa*c*sqrt(G*rho_Lambda), kappa = 1/2 ADOPTED;
C = sqrt(G*M_b*a0); v_flat^4 = G*M_b*a0; and the CONDITIONAL deep-equilibrium
targets/inputs sigma^2 = C/2, rho_ph = C/(4*pi*G*r^2), P = sigma^2*rho_ph
(checked for mutual consistency here, not derived from an action).

Certified algebraic content:
  T0.  k_B*T = m*sigma^2, sigma^2 = C/2  ==>  T = m*C/(2*k_B)   (temperature scale)
  T1.  sigma^2 = k_B*T/m  ==>  k_B*(lambda*T)/(lambda*m) = sigma^2
       (mass degeneracy: (m,T) -> (lambda*m, lambda*T) leaves sigma invariant;
        a measured sigma alone cannot select m)
  T1'. T'/m' = T/m  <=>  the pair (m,T) is only fixed up to a common scale.
  T2.  hydrostatic balance identity: with P = sigma^2*rho_ph, sigma^2 = C/2,
       rho_ph(r) = C/(4*pi*G*r^2), g(r) = C/r:
       dP/dr = -rho_ph(r)*g(r)  exactly for every r != 0.
  T2'. the same identity in cleared (algebraic) form.
  T3.  general solution of the hydrostatic ODE d sigma^2/dr = (2 sigma^2 - C)/r:
       sigma^2(r) = (C + K*r^2)/2 solves it for every constant K (the bounded
       solution K = 0 is selected by boundedness at r -> inf, a classical
       real-analysis argument, not certified here).
  T4.  SIS pairing: sigma^2 = C/2 and v_flat^2 = C give v_flat^2 = 2*sigma^2.
  T5.  negative control (can fail): with the WRONG normalization sigma^2 = C,
       hydrostatic balance fails identically, so the identity checks genuinely
       discriminate the factor 1/2.
-/

noncomputable section
open Real

/-- T0: k_B*T = m*sigma^2 and sigma^2 = C/2 imply T = m*C/(2*k_B). -/
theorem temperature_from_velocity_scale {kB T m C sigma : ℝ} (hkB : kB ≠ 0)
    (h1 : kB * T = m * sigma ^ 2) (h2 : sigma ^ 2 = C / 2) :
    T = m * C / (2 * kB) := by
  have h : kB * T = m * (C / 2) := by rw [h1, h2]
  have hb : kB * T = kB * (m * C / (2 * kB)) := by
    rw [h]
    field_simp [hkB]
  exact mul_left_cancel₀ hkB hb

/-- T1: the pair (m,T) -> (lambda*m, lambda*T) leaves sigma^2 = k_B*T/m invariant;
    hence a measured sigma determines only the ratio T/m, never m. -/
theorem mass_degeneracy_scaled {kB T sigma m lambda : ℝ} (hm : m ≠ 0) (hl : lambda ≠ 0)
    (h : sigma ^ 2 = kB * T / m) :
    kB * (lambda * T) / (lambda * m) = sigma ^ 2 := by
  rw [h]
  field_simp [hm, hl]

/-- T1': the mass-temperature pair is fixed only up to a common scale
    (field-algebra version: (lambda*T)/(lambda*m) = T/m). -/
theorem temperature_scales_with_mass {T m lambda : ℝ} (hm : m ≠ 0) (hl : lambda ≠ 0) :
    (lambda * T) / (lambda * m) = T / m := by
  field_simp [hm, hl]

/-- T2': the hydrostatic residual identity in cleared algebraic form
    (what the derivative computation reduces to):
    (C/2)*(C/(4 pi G))*(-2)/r^3  =  -(C/(4 pi G r^2))*(C/r). -/
theorem hydrostatic_residual_algebra {C G r : ℝ} (hr : r ≠ 0) :
    (C / 2) * (C / (4 * Real.pi * G)) * (-2) * (r ^ 3)⁻¹
      = -((C / (4 * Real.pi * G)) * (r ^ 2)⁻¹) * (C / r) := by
  field_simp [hr]

/-- helper: derivative of x -> (x^2)⁻¹ at r is -2/r^3 for r != 0. -/
lemma deriv_inv_sq {r : ℝ} (hr : r ≠ 0) :
    deriv (fun x : ℝ => (x ^ 2)⁻¹) r = -2 * (r ^ 3)⁻¹ := by
  have hsq : HasDerivAt (fun x : ℝ => x ^ 2) (2 * r) r := by
    have h0 := hasDerivAt_pow (n := 2) (x := r)
    simpa [show (2 - 1 : ℕ) = 1 by norm_num, pow_one] using h0
  have hsq0 : r ^ 2 ≠ 0 := pow_ne_zero 2 hr
  have hinv : HasDerivAt (fun x : ℝ => (x ^ 2)⁻¹) (-(2 * r) / (r ^ 2) ^ 2) r := hsq.inv hsq0
  rw [hinv.deriv]
  field_simp [hr]

/-- T2: hydrostatic balance identity for the deep isothermal equilibrium.
    P(r) = (C/2)*rho_ph(r), rho_ph(r) = C/(4 pi G r^2), g(r) = C/r.
    dP/dr = -rho_ph(r)*g(r) for every r != 0. -/
theorem hydrostatic_balance_identity {C G r : ℝ} (hr : r ≠ 0) (hG : G ≠ 0) :
    deriv (fun x : ℝ => (C / 2) * (C / (4 * Real.pi * G)) * (x ^ 2)⁻¹) r
      = -((C / (4 * Real.pi * G)) * (r ^ 2)⁻¹) * (C / r) := by
  have hsq : HasDerivAt (fun x : ℝ => x ^ 2) (2 * r) r := by
    have h0 := hasDerivAt_pow (n := 2) (x := r)
    simpa [show (2 - 1 : ℕ) = 1 by norm_num, pow_one] using h0
  have hsq0 : r ^ 2 ≠ 0 := pow_ne_zero 2 hr
  have hinv : HasDerivAt (fun x : ℝ => (x ^ 2)⁻¹) (-(2 * r) / (r ^ 2) ^ 2) r := hsq.inv hsq0
  have hc : HasDerivAt
      (fun x : ℝ => (C / 2) * (C / (4 * Real.pi * G)) * (x ^ 2)⁻¹)
      ((C / 2) * (C / (4 * Real.pi * G)) * (-(2 * r) / (r ^ 2) ^ 2)) r :=
    hinv.const_mul ((C / 2) * (C / (4 * Real.pi * G)))
  rw [hc.deriv]
  field_simp [hr, hG]

/-- T3: the general solution family sigma^2(r) = (C + K*r^2)/2 solves the
    hydrostatic ODE  d sigma^2/dr = (2*sigma^2 - C)/r  for every constant K. -/
theorem ode_general_solution {C K r : ℝ} (hr : r ≠ 0) :
    deriv (fun x : ℝ => (C + K * x ^ 2) / 2) r = (2 * ((C + K * r ^ 2) / 2) - C) / r := by
  simp [div_eq_mul_inv]
  field_simp [hr]
  ring

/-- T4: SIS pairing: sigma^2 = C/2 together with v_flat^2 = C gives
    v_flat^2 = 2*sigma^2. -/
theorem sis_relation {C sigma v : ℝ} (h1 : sigma ^ 2 = C / 2) (h2 : v ^ 2 = C) :
    v ^ 2 = 2 * sigma ^ 2 := by
  rw [h2, h1]
  ring

/-- T5: negative control (capable of failing): the WRONG normalization
    sigma^2 = C (instead of C/2) breaks hydrostatic balance identically —
    the cleared-algebra residual (C*(C/4πG)*(-2)/r^3 vs -(C/4πG)(1/r^2)(C/r))
    is nonzero, and the derivative-facing form of the same statement is
    carried by the Python lane (house pattern). -/
theorem wrong_normalization_fails {C G r : ℝ} (hr : r ≠ 0) (hG : G ≠ 0) (hC : C ≠ 0) :
    C * (C / (4 * Real.pi * G)) * (-2) * (r ^ 3)⁻¹
      ≠ -((C / (4 * Real.pi * G)) * (r ^ 2)⁻¹) * (C / r) := by
  intro h
  field_simp [hr, hG] at h
  ring_nf at h
  have hA : C / (4 * Real.pi * G) ≠ 0 := by
    exact div_ne_zero hC (mul_ne_zero (mul_ne_zero (by norm_num) Real.pi_ne_zero) hG)
  have hCC : C * (C / (4 * Real.pi * G)) ≠ 0 := mul_ne_zero hC hA
  have hz : C * (C / (4 * Real.pi * G)) = 0 := by nlinarith
  exact hCC hz

-- axiom audit (house style): expected at most propext, Classical.choice, Quot.sound
#print axioms temperature_from_velocity_scale
#print axioms mass_degeneracy_scaled
#print axioms temperature_scales_with_mass
#print axioms hydrostatic_residual_algebra
#print axioms deriv_inv_sq
#print axioms hydrostatic_balance_identity
#print axioms ode_general_solution
#print axioms sis_relation
#print axioms wrong_normalization_fails