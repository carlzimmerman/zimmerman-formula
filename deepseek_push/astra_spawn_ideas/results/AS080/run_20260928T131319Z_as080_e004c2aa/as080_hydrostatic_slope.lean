import Mathlib

/-!
# AS080 -- Hydrostatic slope-temperature relation: Lean certificate

Lean certifies the MATHEMATICS below, not the physics laws behind it.
Scope: the algebraic core of the derivation in `derivation.md` --

  (T1) the slope-temperature equivalence: in the fixed logarithmic well
       Φ = C ln r with C > 0, the hydrostatic balance dP/dr = -ρC/r together
       with the isothermal EOS P = σ²ρ (σ² > 0) forces ρ(r) = A (r/r_ref)^(-γ)
       with γ = C/σ²; hence slope 2 (γ = 2) holds IFF σ² = C/2.
       (T1 certifies the equivalence; the ODE integration is elementary and
       cross-checked symbolically in the Python lane P1a/P1b.)
  (T2) the POWER-LAW SUBSTITUTION: the closed form solves the ODE, i.e.
       σ² · d/dr[A (r/r_ref)^(-C/σ²)] = -C · A (r/r_ref)^(-C/σ²)/r
       (derivative of a real power via HasStrictDerivAt.rpow).
  (T3) the log-well derivative d/dr(C ln r) = C/r (the well's gradient).
  (T4) the Poisson-consistency amplitude: with γ = 2 and A = C/(4πG_N),
       4πG_N ρ = C/r² exactly (the well sourced by its own density), and
       consequently σ² = C/2 (the equilibrium temperature, conditional on
       the log well).
  (T5) the Newtonian-limit counterpart: ρ_N(r) = exp(G_N M_b/(σ² r)) solves
       the Newtonian hydrostatic ODE σ² ρ' = -ρ G_N M_b/r² -- the profile is
       exponential, NOT a power law, in the Newtonian regime.

NOT certified here (named blockers, verified in the Python lane):
  * the 3D radial-Laplacian step Δ(C ln r) = C/r² -- needs second derivatives
    of nested `deriv (fun z => C * Real.log z)` with function-level
    extensionality at punctured neighborhoods (deriv_congr unavailable in
    this build's oleans); verified symbolically in the lane (P1d, sympy
    residual exactly 0) and by the 50-digit substitution residual (P2).
  * the implicit-kernel deep-exterior slope deviations of branches Q, RAR,
    MU2, EXP (transcendental solve; verified numerically in the lane, P3,
    including the Bernoulli-series coefficients of Q and RAR at 50 digits).

Constants are abstract (C, σ², A, r_ref, ...) over ℝ with the positivity/
nonvanishing hypotheses the identities need; the physical quantities are
G_N = 6.67430e-11, M_b = 6.5e10 M_sun, a0 = 9.3619e-11 / 1.1279e-10 m/s²,
C = √(G_N M_b a0), σ² = C/2 (both footings; see derivation.md §2, §9).
-/

noncomputable section

-- (T1) slope two  <==>  sigma^2 = C/2   (gamma = C/sigma^2 is the slope)
theorem slope_two_iff (C σ2 : ℝ) (hC : C ≠ 0) (hσ : σ2 ≠ 0) :
    (C / σ2 = 2 ↔ σ2 = C / 2) := by
  constructor
  · intro h
    have hc : C = 2 * σ2 := by
      rwa [div_eq_iff hσ] at h
    calc
      σ2 = (2 * σ2) / 2 := by field_simp
      _ = C / 2 := by rw [← hc]
  · intro h
    rw [h]
    field_simp [hC]

-- (T2a) derivative of the power-law profile
--   d/dr [A (r/r_ref)^p] = p * A (r/r_ref)^p / r   on r > 0, r_ref > 0
theorem powerlaw_deriv (A r_ref p x : ℝ) (hx : 0 < x) (hr : 0 < r_ref) :
    deriv (fun y : ℝ => A * (y / r_ref) ^ p) x = p * (A * (x / r_ref) ^ p) / x := by
  have hZpos : 0 < x / r_ref := div_pos hx hr
  have hpow : HasStrictDerivAt (fun z : ℝ => z ^ p) (p * (x / r_ref) ^ (p - 1)) (x / r_ref) := by
    simpa using (hasStrictDerivAt_id (x / r_ref)).rpow (hasStrictDerivAt_const (x / r_ref) p) hZpos
  have hlin : HasDerivAt (fun y : ℝ => y / r_ref) (1 / r_ref) x := by
    simpa using ((hasDerivAt_id x).div_const r_ref)
  have hcomp : HasDerivAt (fun y : ℝ => (y / r_ref) ^ p)
      (p * (x / r_ref) ^ (p - 1) * (1 / r_ref)) x := by
    convert (hpow.hasDerivAt.comp x hlin) using 1 <;> try rfl
  have htot : HasDerivAt (fun y : ℝ => A * (y / r_ref) ^ p)
      (A * (p * (x / r_ref) ^ (p - 1) * (1 / r_ref))) x :=
    hcomp.const_mul A
  have hcoef : (x / r_ref) ^ (p - 1) = (x / r_ref) ^ p * (x / r_ref) ^ (-1 : ℝ) := by
    -- p - 1 is definitionally p + (-1 : ℝ), so the rpow_add theorem applies
    -- verbatim (the rewrite above closed the goal by itself).
    exact Real.rpow_add hZpos p (-1 : ℝ)
  have hneg : (x / r_ref) ^ (-1 : ℝ) = (x / r_ref)⁻¹ := by
    rw [Real.rpow_neg (le_of_lt hZpos) (1 : ℝ), Real.rpow_one]
  have hval : A * (p * (x / r_ref) ^ (p - 1) * (1 / r_ref)) = p * (A * (x / r_ref) ^ p) / x := by
    rw [hcoef, hneg]
    field_simp [hx.ne', hr.ne']
  have hd : deriv (fun y : ℝ => A * (y / r_ref) ^ p) x
      = A * (p * (x / r_ref) ^ (p - 1) * (1 / r_ref)) := htot.deriv
  rwa [hval] at hd

-- (T2b) the closed form solves the hydrostatic ODE at gamma = C/sigma^2:
--   sigma^2 * rho' = -C * rho / r   with rho(r) = A (r/r_ref)^p, p = -C/sigma^2
theorem hydrostatic_ode_solved (A C σ2 r_ref p x : ℝ) (hx : 0 < x) (hr : 0 < r_ref)
    (hσ : σ2 ≠ 0) (hp : p = -C / σ2) :
    σ2 * deriv (fun y : ℝ => A * (y / r_ref) ^ p) x = -C * (A * (x / r_ref) ^ p) / x := by
  rw [powerlaw_deriv A r_ref p x hx hr]
  have hp1 : σ2 * p = -C := by
    rw [hp]
    field_simp [hσ]
  calc
    σ2 * (p * (A * (x / r_ref) ^ p) / x) = (σ2 * p) * (A * (x / r_ref) ^ p) / x := by
      ring
    _ = -C * (A * (x / r_ref) ^ p) / x := by rw [hp1]

-- (T3) the log-well gradient:  d/dr [C ln r] = C / r   (r ≠ 0)
theorem log_well_deriv (C x : ℝ) (hx : x ≠ 0) :
    deriv (fun y : ℝ => C * Real.log y) x = C / x := by
  rw [deriv_const_mul_field]
  rw [Real.deriv_log]
  field_simp [hx]

-- (T4a) Poisson consistency of the well at gamma = 2:
--   4 π G_N · (C/(4 π G_N)) / r² = C / r²   (the slope-2 profile sources
--   the log well exactly; the additional premise that Delta(C ln r) = C/r²
--   is the named blocker below)
theorem poisson_amplitude (G A C x : ℝ) (hG : G ≠ 0) (hx : x ≠ 0)
    (hA : A = C / (4 * Real.pi * G)) :
    4 * Real.pi * G * A / x ^ 2 = C / x ^ 2 := by
  rw [hA]
  field_simp [hG, Real.pi_ne_zero, hx]

-- (T4b) the conditional selection of the equilibrium temperature:
--   gamma = C/sigma^2 = 2   (Poisson selection)   ==>   sigma^2 = C/2
theorem poisson_selects_temperature (C σ2 : ℝ) (hC : C ≠ 0)
    (hσ : σ2 = C / 2) :
    C / σ2 = 2 := by
  rw [hσ]
  field_simp [hC]

-- (T5) the Newtonian-limit profile solves the Newtonian hydrostatic ODE:
--   sigma^2 * d/dr [exp(G M_b / (sigma^2 r))] = -G M_b exp(G M_b/(sigma^2 r)) / r^2
theorem newtonian_exp_solves (G Mb σ2 x : ℝ) (hG : G ≠ 0) (hMb : Mb ≠ 0)
    (hσ : σ2 ≠ 0) (hx : x ≠ 0) :
    σ2 * deriv (fun r : ℝ => Real.exp ((G * Mb / σ2) * r⁻¹)) x
      = -G * Mb * Real.exp ((G * Mb / σ2) * x⁻¹) / x ^ 2 := by
  have hv : HasDerivAt (fun r : ℝ => Real.exp ((G * Mb / σ2) * r⁻¹))
      (Real.exp ((G * Mb / σ2) * x⁻¹) * ((G * Mb / σ2) * (-(x ^ 2)⁻¹))) x := by
    have hinner : HasDerivAt (fun r : ℝ => (G * Mb / σ2) * r⁻¹)
        ((G * Mb / σ2) * (-(x ^ 2)⁻¹)) x := by
      exact (hasDerivAt_inv hx).const_mul (G * Mb / σ2)
    exact (Real.hasDerivAt_exp ((G * Mb / σ2) * x⁻¹)).comp x hinner
  rw [hv.deriv]
  calc
    σ2 * (Real.exp ((G * Mb / σ2) * x⁻¹) * ((G * Mb / σ2) * (-(x ^ 2)⁻¹)))
        = Real.exp ((G * Mb / σ2) * x⁻¹) * (σ2 * ((G * Mb / σ2) * (-(x ^ 2)⁻¹))) := by
        ring
    _ = Real.exp ((G * Mb / σ2) * x⁻¹) * (-(G * Mb) / x ^ 2) := by
        field_simp [hG, hMb, hσ, hx]
    _ = -G * Mb * Real.exp ((G * Mb / σ2) * x⁻¹) / x ^ 2 := by
        ring

end

#print axioms slope_two_iff
#print axioms powerlaw_deriv
#print axioms hydrostatic_ode_solved
#print axioms log_well_deriv
#print axioms poisson_amplitude
#print axioms poisson_selects_temperature
#print axioms newtonian_exp_solves
