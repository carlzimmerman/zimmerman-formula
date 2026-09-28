import Mathlib

/-!
# AS003 — omega_L identity, its null direction, and the closure ratio

SCOPE. `deepseek_push/astra_spawn_ideas/AS003_critical_density_closure_as_a_dependency_problem.md`
(seed AS003, run AS003-20260927-r01). The framework input is
`rho_Lambda = 4*a0^2/(G_N*c^2)` (the adopted kappa = 1/2 restatement of a0 = kappa*c*sqrt(G_N*rho_Lambda),
kappa = 1/2 is ADOPTED, never derived here; FRAMEWORK_CONTRACT) and the critical-density
definition `rho_crit = 3*H0^2/(8*pi*G_cosmo)`. Three certified objects:

* `omegaL_identity`:  Omega_L := rho_Lambda/rho_crit = (32*pi/3)*(G_cosmo/G_N)*(a0/(H0*c))^2,
  exact on the positive domain — the two declared claims of the task (same-G reduction and the
  G_cosmo/G_N factor) are one field identity.
* `omegaL_scale_invariant`: the map (a0,H0) -> Omega_L depends only on the ratio a0/H0
  (the Jacobian null direction (1,1) in log coordinates), i.e. assigning two of {a0,H0,Omega_L}
  fixes the third by re-expression, never prediction.
* `closure_ratio_positive`: the critical-density-closure hypothesis Omega_L = 1 (on the common
  coupling) forces a0/(H0*c) = sqrt(3/(32*pi)) — the closure as a condition, not a derivation.

No `sorry`; axioms are verified by `#print axioms` below. -/

noncomputable section

/-- The exact critical-density identity with separate couplings G_N (scale) and
G_cosmo (critical density): rho_Lambda/rho_crit = (32 pi/3)(G_cosmo/G_N)(a0/(H0 c))^2. -/
theorem omegaL_identity (a0 H0 GN Gc c : ℝ)
    (hH0 : H0 ≠ 0) (hGN : GN ≠ 0) (hGc : Gc ≠ 0) (hc : c ≠ 0) :
    (4 * a0 ^ 2 / (GN * c ^ 2)) / (3 * H0 ^ 2 / (8 * Real.pi * Gc))
      = (32 * Real.pi / 3) * (Gc / GN) * (a0 / (H0 * c)) ^ 2 := by
  field_simp [Real.pi_ne_zero]
  ring

/-- Null direction of the (a0,H0) -> Omega_L map: simultaneous rescaling (a0,H0) -> (t*a0,t*H0)
leaves Omega_L unchanged, so the level sets are rays a0/H0 = constant. -/
theorem omegaL_scale_invariant (a0 H0 GN Gc c t : ℝ)
    (ht : t ≠ 0) (hH0 : H0 ≠ 0) (hGN : GN ≠ 0) (hc : c ≠ 0) :
    (32 * Real.pi / 3) * (Gc / GN) * ((t * a0) / ((t * H0) * c)) ^ 2
      = (32 * Real.pi / 3) * (Gc / GN) * (a0 / (H0 * c)) ^ 2 := by
  field_simp [Real.pi_ne_zero, ht, hH0, hc]

/-- Closure hypothesis Omega_L = 1 (common coupling): on the positive domain the ratio
a0/(H0 c) is forced to sqrt(3/(32 pi)) — a condition, not a derivation of kappa. -/
theorem closure_ratio_positive (a0 H0 c : ℝ)
    (ha : 0 < a0) (hH : 0 < H0) (hc : 0 < c)
    (hclosure : (32 * Real.pi / 3) * (a0 / (H0 * c)) ^ 2 = 1) :
    a0 / (H0 * c) = Real.sqrt (3 / (32 * Real.pi)) := by
  have hpi : Real.pi ≠ 0 := Real.pi_ne_zero
  have h32 : (32 : ℝ) ≠ 0 := by norm_num
  have h3 : (3 : ℝ) ≠ 0 := by norm_num
  have hcoef : (32 * Real.pi / 3) ≠ 0 := by
    exact div_ne_zero (mul_ne_zero h32 hpi) h3
  have hcl : (32 * Real.pi / 3) * (a0 / (H0 * c)) ^ 2 = 1 := hclosure
  have hsq : (a0 / (H0 * c)) ^ 2 = 3 / (32 * Real.pi) := by
    calc
      (a0 / (H0 * c)) ^ 2
          = ((32 * Real.pi / 3) * (a0 / (H0 * c)) ^ 2) / (32 * Real.pi / 3) := by
            field_simp [hcoef]
      _ = 1 / (32 * Real.pi / 3) := by
            rw [hcl]
      _ = 3 / (32 * Real.pi) := by
            field_simp [hpi]
  have hpos : 0 < a0 / (H0 * c) := by
    exact div_pos ha (mul_pos hH hc)
  have hsq2 : Real.sqrt ((a0 / (H0 * c)) ^ 2) = a0 / (H0 * c) := by
    rw [Real.sqrt_sq_eq_abs]
    rw [abs_of_nonneg (le_of_lt hpos)]
  have hfinal : Real.sqrt ((a0 / (H0 * c)) ^ 2) = Real.sqrt (3 / (32 * Real.pi)) := by
    rw [hsq]
  rw [← hfinal]
  rw [hsq2]

#print axioms omegaL_identity
#print axioms omegaL_scale_invariant
#print axioms closure_ratio_positive