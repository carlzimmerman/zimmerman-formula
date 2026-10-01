import Mathlib

/-!
AS285 (Tier-0b): action-consistent growth response of CA5-GNC-R in the
restricted quasistatic band, inactive branch. Certified algebra over R:

Linearized Fourier constraint system (Newtonian gauge, comoving k2 = k):
  E2 (Z auxiliary, FINAL_ACTION (6) with f = 0):  -4k2 Z + ell S k2 Phi = 0
  E3 (Z/U projection constraint, (7), vacuum carrier origin):
        2 M_P^2 c_N (-k2)(Z - Phi + U) + rho_R0 Phi = 0
  E4 (independent spatial trace equation, Einstein + projector stress (9)):
        2 M_P^2 (-k2)(Phi - Psi) + 3 rho_R0 Z = 0
with the elimination
  Z  = ell S Phi/4
  U  = Phi - ell S Phi/4 + rho_R0 Phi/(2 M_P^2 c_N k2)
  Psi = Phi - 3 ell S rho_R0 Phi/(8 M_P^2 k2)
and the response functions
  mu_g = -4 c_N / A_total,   A_total = A0 + 2 ell S rho_R0/(M_P^2 k2),
  A0 = -4 + 2 alpha + ell S (1 + c_N - alpha/2) - c_N (ell S)^2/4,
  eta_g = Psi/Phi = 1 - 3 ell S rho_R0/(8 M_P^2 k2).
Certified statements: (i) substitution-back residuals of the eliminated
equations vanish exactly; (ii) the negative control (imposing Psi = Phi by
hand) gives the exact nonzero residual 3 rho_R0 (ell S/4) Phi; (iii) the
pure-host limit reproduces the pinned static factor Q = 1 - ell S/4 with
mu_g = 1/Q^2; (iv) the Einstein limit gives mu_g = eta_g = 1; (v) both the
high-k (S -> 0) and no-gate (ell -> 0) in-band recoveries give mu_g = 1.
-/

namespace AS285

/-- Compensator factor of the pinned static matrix, FINAL_ACTION (16). -/
noncomputable def Q (e s : ℝ) : ℝ := 1 - e * s / 4

/-- Reduced lapse coefficient A0 of the host (alpha = a, cN = c_N). -/
noncomputable def A0 (a cN e s : ℝ) : ℝ :=
  -4 + 2 * a + e * s * (1 + cN - a / 2) - cN * (e * s) ^ 2 / 4

/-- Z-elimination residual: Z = e*s*Phi/4 satisfies E2 exactly. -/
theorem z_solution (k e s Ph : ℝ) : -4 * k * (e * s * Ph / 4) + e * s * k * Ph = 0 := by
  ring

/-- U-elimination residual: E3 is satisfied exactly by (Z, U) above. -/
theorem u_solution (m k cn e s r0 Ph : ℝ) (hm : m ≠ 0) (hk : k ≠ 0) (hcn : cn ≠ 0) :
    2 * m * cn * (-k) * (e * s * Ph / 4 - Ph
        + (Ph - e * s * Ph / 4 + r0 * Ph / (2 * m * cn * k))) + r0 * Ph = 0 := by
  field_simp [hm, hk, hcn]
  ring

/-- Psi-elimination residual: the spatial trace equation E4 holds exactly. -/
theorem psi_solution (m k e s r0 Ph : ℝ) (hm : m ≠ 0) (hk : k ≠ 0) :
    2 * m * (-k) * (Ph - (Ph - 3 * e * s * r0 * Ph / (8 * m * k)))
        + 3 * r0 * (e * s * Ph / 4) = 0 := by
  field_simp [hm, hk]
  ring

/-- Negative control, exact residual: imposing Psi = Phi by hand leaves
    the independent spatial equation unsatisfied by 3 rho_R0 (ell S/4) Phi. -/
theorem negative_control_residual (m k e s r0 Ph Z : ℝ) (hZ : Z = e * s * Ph / 4) :
    2 * m * (-k) * (Ph - Ph) + 3 * r0 * Z = 3 * r0 * e * s * Ph / 4 := by
  rw [hZ]
  ring

/-- Negative control fires: the residual is nonzero for rho_R0, ell, S, Phi
    all nonzero. -/
theorem negative_control_fires (e s r0 Ph : ℝ) (he : e ≠ 0) (hs : s ≠ 0)
    (hr : r0 ≠ 0) (hp : Ph ≠ 0) : 3 * r0 * e * s * Ph / 4 ≠ 0 := by
  -- product of nonzero factors, divided by the numeral 4
  have hprod : r0 * e * s * Ph ≠ 0 := by
    exact mul_ne_zero (mul_ne_zero (mul_ne_zero hr he) hs) hp
  intro hz
  have hz4 : 4 * (3 * r0 * e * s * Ph / 4) = 0 := by rw [hz]; ring
  have hz5 : 3 * r0 * e * s * Ph = 0 := by
    -- 4 * (3 * x / 4) = 3 * x for the numeral 4
    calc
      3 * r0 * e * s * Ph = 4 * (3 * r0 * e * s * Ph / 4) := by ring
      _ = 0 := hz4
  rcases lt_or_gt_of_ne hprod with hpos | hneg
  · nlinarith [hz5, hpos]
  · nlinarith [hz5, hneg]

/-- Pure-host limit: A0(alpha=0, c_N=1) = -4 Q^2, the pinned static factor
    of FINAL_ACTION (16). -/
theorem a0_pure_host_identity (e s : ℝ) : A0 0 1 e s = -4 * (Q e s) ^ 2 := by
  simp [A0, Q]
  ring

/-- Pure-host response: mu_g = 1/Q^2 in the pinned static limit. -/
theorem mu_pure_host (e s : ℝ) (hq : Q e s ≠ 0) : -4 / A0 0 1 e s = 1 / (Q e s) ^ 2 := by
  rw [a0_pure_host_identity]
  field_simp [hq]

/-- Einstein recovery: ell = 0, alpha = 0, c_N = 1, rho_R0 = 0 gives
    mu_g = 1. -/
theorem mu_einstein_limit (s : ℝ) : -4 / A0 0 1 0 s = 1 := by
  simp [A0]

/-- Einstein recovery of the slip: with rho_R0 = 0, eta_g = 1. -/
theorem eta_einstein_limit (m k e s Ph : ℝ) (hm : m ≠ 0) (hk : k ≠ 0) :
    8 * m * k * (Ph - 3 * e * s * 0 * Ph / (8 * m * k)) = 8 * m * k * Ph - 3 * e * s * 0 * Ph := by
  field_simp [hm, hk]

/-- Slip formula in multiplication form: 8 M_P^2 k2 (Phi - Psi) =
    3 ell S rho_R0 Phi, i.e. eta_g = 1 - 3 ell S rho_R0/(8 M_P^2 k2). -/
theorem slip_multiplication (m k e s r0 Ph : ℝ) (hm : m ≠ 0) (hk : k ≠ 0) :
    8 * m * k * (Ph - 3 * e * s * r0 * Ph / (8 * m * k)) = 8 * m * k * Ph - 3 * e * s * r0 * Ph := by
  field_simp [hm, hk]

-- High-k in-band recovery, close of Eq. (F) in multiplication form (division
-- form follows for -4 + 2a /= 0, i.e. alpha /= 2): heat suppression S -> 0
-- and projection -> 0 give mu_g = 1 at fixed alpha, c_N = 1 - alpha/2.
theorem mu_highk_mul (a cN s : ℝ) (hcn : cN = 1 - a / 2) : -4 * cN = A0 a cN 0 s := by
  rw [hcn]
  simp [A0]
  ring

end AS285

#print axioms AS285.z_solution
#print axioms AS285.u_solution
#print axioms AS285.psi_solution
#print axioms AS285.negative_control_residual
#print axioms AS285.negative_control_fires
#print axioms AS285.a0_pure_host_identity
#print axioms AS285.mu_pure_host
#print axioms AS285.mu_einstein_limit
#print axioms AS285.eta_einstein_limit
#print axioms AS285.slip_multiplication
#print axioms AS285.mu_highk_mul
