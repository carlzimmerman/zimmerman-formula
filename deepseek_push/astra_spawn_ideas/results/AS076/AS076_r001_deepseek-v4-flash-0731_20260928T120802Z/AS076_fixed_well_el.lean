/-
AS076 -- Fixed-well Euler-Lagrange density: Lean 4 certificate of the
algebraic core of the audit.

Theorems certified (all over the reals):

  A. el_identity        -- the Euler-Lagrange stationary profile of
     S = -int rho ln(rho/rho_ref) dV  at fixed well Phi = C ln r and fixed
     sigma, under M and E constraints, solves the EL equation identically:
     for  rho(r) = exp(K - beta*C*log r) with  K = -1-alpha-3*beta*sigma^2/2,
         log rho(r) + 1 + alpha + beta*(3*sigma^2/2 + C*log r) = 0.
     (The variation of S - alpha*M - beta*E gives -log rho - 1 - alpha
      - beta*(3 sigma^2/2 + Phi) = 0.)

  B. exponent_two        -- with the EXTRA thermal input beta = 1/sigma^2 and
     the virial input sigma^2 = C/2 (G091), the exponent is gamma = beta*C = 2
     exactly.  (beta = 1/sigma^2 is not obtained from the variation; the seed
     declares sigma fixed.)

  C. mass_relation       -- source normalization on the finite shell:
     int_{r_in}^R 4*pi*x^2*(A/x^2) dx = 4*pi*A*(R - r_in)   (0 < r_in <= R),
     i.e. rho = A/r^2 with A = M_b/(4 pi (R - r_in)) carries mass M_b.

  D. self_potential_closed -- NEGATIVE CONTROL: the missing term.
     For rho = A/r'^2 on [r_in, R], the shell-theorem self-potential is
         Phi_self(r) = -G*(4*pi*A*(r - r_in)/r  + 4*pi*A*log(R/r))
     with the inner-shell integral int_{r_in}^r 4 pi A dr' and the outer
     integral int_r^R 4 pi A/r' dr' both evaluated in closed form.

  E. missing_term_spread -- the self-consistent EL residual of the fixed-well
     solution (gamma = 2 profile) against the self-gravitating energy differs
     between the shell ends by
         res(R) - res(r_in) = +4*pi*G*beta*A*(log(R/r_in) - (1 - r_in/R)).
     The missing term beta*Phi_self(r) is r-dependent (not absorbed by alpha).

  F. missing_term_nonzero-- concrete instance: shell r_in = 1, R = 4
     (R/r_in = 4): the residual difference is nonzero
     (4*pi*G*beta*A*(log 4 - 3/4) != 0 with G, beta, A != 0), so the r^-2
     profile is NOT a stationary point of the self-gravitating energy on that
     shell.

Compiled host-side only; no mathlib files are modified.
-/
import Mathlib

noncomputable section
open Real
open scoped Real

namespace AS076

-- ============================================================ A. EL identity
theorem el_identity {K β C α σ2 : ℝ} (r : ℝ)
    (hK : K = -1 - α - 3 * β * σ2 / 2) :
    Real.log (Real.exp (K - β * C * Real.log r)) + 1 + α
      + β * (3 * σ2 / 2 + C * Real.log r) = 0 := by
  rw [hK]
  rw [Real.log_exp]
  ring

-- ============================================================ B. gamma = 2
theorem exponent_two {C σ2 β : ℝ} (hC : C ≠ 0) (hσ2 : σ2 = C / 2)
    (hβ : β = 1 / σ2) :
    β * C = 2 := by
  rw [hβ, hσ2]
  field_simp [hC]

-- ============================================================ C. normalization
lemma integrand_simp {A : ℝ} (x : ℝ) (hx : x ≠ 0) :
    x ^ 2 * (A / x ^ 2) = A := by
  field_simp [hx]

theorem mass_relation {A r_in R : ℝ} (hrin : 0 < r_in) (hle : r_in ≤ R) :
    ∫ x in r_in..R, 4 * Real.pi * x ^ 2 * (A / x ^ 2) =
      4 * Real.pi * A * (R - r_in) := by
  calc
    ∫ x in r_in..R, 4 * Real.pi * x ^ 2 * (A / x ^ 2)
        = ∫ x in r_in..R, 4 * Real.pi * A := by
          apply intervalIntegral.integral_congr
          intro x hx
          have hx0 : x ≠ 0 := by
            have hxi : x ∈ Set.Icc r_in R := by
              simpa [Set.uIcc_of_le hle] using hx
            exact ne_of_gt (lt_of_lt_of_le hrin hxi.1)
          dsimp
          have hs : 4 * Real.pi * x ^ 2 * (A / x ^ 2) = 4 * Real.pi * A := by
            calc
              4 * Real.pi * x ^ 2 * (A / x ^ 2)
                  = 4 * Real.pi * (x ^ 2 * (A / x ^ 2)) := by ring
              _ = 4 * Real.pi * A := by rw [integrand_simp x hx0]
          exact hs
    _ = 4 * Real.pi * A * (R - r_in) := by
          rw [intervalIntegral.integral_const, smul_eq_mul]
          ring

-- ============================================================ D. self-potential
/-- Inner-shell integral:  int_{r_in}^r 4 pi A dx = 4 pi A (r - r_in). -/
lemma inner_shell_integral {A r_in r : ℝ} :
    ∫ _x in r_in..r, 4 * Real.pi * A = 4 * Real.pi * A * (r - r_in) := by
  rw [intervalIntegral.integral_const, smul_eq_mul]
  ring

/-- Outer-shell integral:  int_r^R (4 pi A / x) dx = 4 pi A log (R / r),
    for 0 < r <= R (so 0 is outside the interval). -/
lemma outer_shell_integral {A r R : ℝ} (hr : 0 < r) (hrR : r ≤ R) :
    ∫ x in r..R, 4 * Real.pi * A / x = 4 * Real.pi * A * Real.log (R / r) := by
  -- re-express as (4 pi A) * x^-1 ; pull the constant out (explicit args so
  -- the rewrite matcher does not need to synthesize a function metavariable)
  rw [show (∫ x in r..R, 4 * Real.pi * A / x)
        = ∫ x in r..R, (4 * Real.pi * A) * x⁻¹ by
        apply intervalIntegral.integral_congr
        intro x hx
        ring]
  rw [intervalIntegral.integral_const_mul (r := (4 * Real.pi * A))
    (f := fun x : ℝ => x⁻¹)]
  -- FTC:  int_r^R x^-1 dx = log R - log r
  have hderiv : ∀ x ∈ Set.uIcc r R, HasDerivAt Real.log x⁻¹ x := by
    intro x hx
    have hxpos : 0 < x := by
      have hxi : x ∈ Set.Icc r R := by simpa [Set.uIcc_of_le hrR] using hx
      exact lt_of_lt_of_le hr hxi.1
    exact Real.hasDerivAt_log (ne_of_gt hxpos)
  have hint : IntervalIntegrable (fun x : ℝ => x⁻¹) MeasureTheory.volume r R := by
    exact intervalIntegral.intervalIntegrable_inv (f := fun x : ℝ => x)
      (by
        intro x hx
        have hxpos : 0 < x := by
          have hxi : x ∈ Set.Icc r R := by simpa [Set.uIcc_of_le hrR] using hx
          exact lt_of_lt_of_le hr hxi.1
        exact ne_of_gt hxpos)
      (by exact continuous_id.continuousOn)
  have hftc : ∫ x in r..R, x⁻¹ = Real.log R - Real.log r := by
    simpa using (intervalIntegral.integral_eq_sub_of_hasDerivAt
      (f := Real.log) (f' := fun x : ℝ => x⁻¹) hderiv hint)
  rw [hftc]
  rw [← Real.log_div (ne_of_gt (lt_of_lt_of_le hr hrR)) hr.ne']

/-- The shell-theorem self-potential of rho = A/r'^2 on [r_in, R], closed form.
    Phi_self(r) = -G * [ int_{r_in}^r 4 pi A dx / r  +  int_r^R 4 pi A/x dx ]. -/
theorem self_potential_closed {G A r_in R r : ℝ} (hrin : 0 < r_in)
    (hrinr : r_in ≤ r) (hrR : r ≤ R) :
    (∫ x in r_in..r, 4 * Real.pi * A) / r + ∫ x in r..R, 4 * Real.pi * A / x
      = 4 * Real.pi * A * (1 - r_in / r + Real.log (R / r)) := by
  rw [inner_shell_integral]
  rw [outer_shell_integral (lt_of_lt_of_le hrin hrinr) hrR]
  field_simp [hrin.ne', (ne_of_gt (lt_of_lt_of_le hrin hrinr))]

-- ============================================================ E. residual spread
/-- The self-consistent EL residual of the gamma-2 fixed-well solution against
    the self-gravitating energy differs between the shell ends by
    +4 pi G beta A (log (R/r_in) - (1 - r_in/R))  -- the missing term
    beta*Phi_self(r) is r-dependent (beta*Phi_self is not a constant that alpha
    can absorb). -/
theorem missing_term_spread {res : ℝ → ℝ} {G β A r_in R : ℝ} (hrin : 0 < r_in)
    (hr : r_in < R)
    (hres : ∀ r, 0 < r → res r =
      β * (-4 * Real.pi * G * A * (1 - r_in / r + Real.log (R / r)))) :
    res R - res r_in =
      4 * Real.pi * G * β * A * (Real.log (R / r_in) - (1 - r_in / R)) := by
  rw [hres R (lt_trans hrin hr), hres r_in hrin]
  have hR : R ≠ 0 := ne_of_gt (lt_trans hrin hr)
  have hlogRR : Real.log (R / R) = 0 := by
    rw [Real.log_div hR hR]
    ring
  rw [hlogRR]
  field_simp [hrin.ne']
  ring

-- ============================================================ F. nonzero instance
/-- log 4 > 3/4, hence log 4 - 3/4 != 0 (via the strict tangent bound
    log x < x - 1 at x = 1/4). -/
lemma log_four_gt_three_quarters : (3 / 4 : ℝ) < Real.log 4 := by
  have h : Real.log (1 / 4 : ℝ) < (1 / 4 : ℝ) - 1 :=
    Real.log_lt_sub_one_of_pos (by norm_num) (by norm_num)
  have hiv : Real.log ((4 : ℝ)⁻¹) = -Real.log 4 := Real.log_inv (4 : ℝ)
  have h2 : -(Real.log (4 : ℝ)) < (1 / 4 : ℝ) - 1 := by
    simpa [one_div, hiv] using h
  linarith

lemma log_four_ne_three_quarters : Real.log (4 : ℝ) ≠ 3 / 4 := by
  intro h
  have : (3 / 4 : ℝ) < 3 / 4 := by simpa [h] using log_four_gt_three_quarters
  exact (lt_irrefl (3 / 4 : ℝ)) this

/-- Concrete shell r_in = 1, R = 4 (R/r_in = 4): the missing-term residual
    difference of theorem missing_term_spread is nonzero for G, beta, A all
    nonzero. -/
theorem missing_term_nonzero {G β A : ℝ} (hG : G ≠ 0) (hβ : β ≠ 0)
    (hA : A ≠ 0) :
    4 * Real.pi * G * β * A * (Real.log (4 : ℝ) - 3 / 4) ≠ 0 := by
  intro hz
  have hprod : (Real.log (4 : ℝ) - 3 / 4) = 0 := by
    -- product of nonzero factors is zero => last factor is zero
    have hne1 : (4 * Real.pi * G * β * A) ≠ 0 := by
      exact mul_ne_zero (mul_ne_zero (mul_ne_zero (mul_ne_zero (by norm_num)
        Real.pi_ne_zero) hG) hβ) hA
    exact (mul_eq_zero.mp hz).resolve_left hne1
  have hlog : Real.log (4 : ℝ) = 3 / 4 := by linarith
  exact log_four_ne_three_quarters hlog

end AS076

end
