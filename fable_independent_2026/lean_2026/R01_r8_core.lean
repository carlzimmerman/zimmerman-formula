import Mathlib

/-!
# R01 — the m=8 rung of the first-flight ladder certified as an exact R-core polynomial integral
Companion to deepseek_push/R01_r8_moment.py.  1D scope ONLY (K3): the 2D->1D reduction is
sympy-exact, cross-checked by P01-style original-variable 40-dps quadrature and 1e7 MC
(R01_results.json); the artanh divisibility V/(1-R^2) is CHECKED there, not assumed.
-/

namespace R01

noncomputable section

open scoped intervalIntegral

/-- Antiderivative of a degree-10 polynomial (function-level sum). -/
def coreAnti (c0 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 : ℝ) : ℝ → ℝ :=
  (fun y : ℝ => c0 * y) +
    (fun y : ℝ => (c1 / 2) * y ^ 2) +
    (fun y : ℝ => (c2 / 3) * y ^ 3) +
    (fun y : ℝ => (c3 / 4) * y ^ 4) +
    (fun y : ℝ => (c4 / 5) * y ^ 5) +
    (fun y : ℝ => (c5 / 6) * y ^ 6) +
    (fun y : ℝ => (c6 / 7) * y ^ 7) +
    (fun y : ℝ => (c7 / 8) * y ^ 8) +
    (fun y : ℝ => (c8 / 9) * y ^ 9) +
    (fun y : ℝ => (c9 / 10) * y ^ 10) +
    (fun y : ℝ => (c10 / 11) * y ^ 11)

/-- The polynomial itself. -/
def corePoly (c0 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 : ℝ) : ℝ → ℝ :=
  fun x : ℝ => c0 + c1 * x ^ 1 + c2 * x ^ 2 + c3 * x ^ 3 + c4 * x ^ 4 + c5 * x ^ 5 + c6 * x ^ 6 + c7 * x ^ 7 + c8 * x ^ 8 + c9 * x ^ 9 + c10 * x ^ 10

/-- deriv (coreAnti) = corePoly, termwise. -/
lemma r01_deriv_coreAnti (c0 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 : ℝ) : deriv (coreAnti c0 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10) = corePoly c0 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 := by
  funext x
  unfold coreAnti corePoly
  rw [deriv_add (by fun_prop : DifferentiableAt ℝ ((fun y : ℝ => c0 * y) + (fun y : ℝ => (c1 / 2) * y ^ 2) + (fun y : ℝ => (c2 / 3) * y ^ 3) + (fun y : ℝ => (c3 / 4) * y ^ 4) + (fun y : ℝ => (c4 / 5) * y ^ 5) + (fun y : ℝ => (c5 / 6) * y ^ 6) + (fun y : ℝ => (c6 / 7) * y ^ 7) + (fun y : ℝ => (c7 / 8) * y ^ 8) + (fun y : ℝ => (c8 / 9) * y ^ 9) + (fun y : ℝ => (c9 / 10) * y ^ 10)) x)
                (by fun_prop : DifferentiableAt ℝ (fun y : ℝ => (c10 / 11) * y ^ 11) x)]
  rw [deriv_add (by fun_prop : DifferentiableAt ℝ ((fun y : ℝ => c0 * y) + (fun y : ℝ => (c1 / 2) * y ^ 2) + (fun y : ℝ => (c2 / 3) * y ^ 3) + (fun y : ℝ => (c3 / 4) * y ^ 4) + (fun y : ℝ => (c4 / 5) * y ^ 5) + (fun y : ℝ => (c5 / 6) * y ^ 6) + (fun y : ℝ => (c6 / 7) * y ^ 7) + (fun y : ℝ => (c7 / 8) * y ^ 8) + (fun y : ℝ => (c8 / 9) * y ^ 9)) x)
                (by fun_prop : DifferentiableAt ℝ (fun y : ℝ => (c9 / 10) * y ^ 10) x)]
  rw [deriv_add (by fun_prop : DifferentiableAt ℝ ((fun y : ℝ => c0 * y) + (fun y : ℝ => (c1 / 2) * y ^ 2) + (fun y : ℝ => (c2 / 3) * y ^ 3) + (fun y : ℝ => (c3 / 4) * y ^ 4) + (fun y : ℝ => (c4 / 5) * y ^ 5) + (fun y : ℝ => (c5 / 6) * y ^ 6) + (fun y : ℝ => (c6 / 7) * y ^ 7) + (fun y : ℝ => (c7 / 8) * y ^ 8)) x)
                (by fun_prop : DifferentiableAt ℝ (fun y : ℝ => (c8 / 9) * y ^ 9) x)]
  rw [deriv_add (by fun_prop : DifferentiableAt ℝ ((fun y : ℝ => c0 * y) + (fun y : ℝ => (c1 / 2) * y ^ 2) + (fun y : ℝ => (c2 / 3) * y ^ 3) + (fun y : ℝ => (c3 / 4) * y ^ 4) + (fun y : ℝ => (c4 / 5) * y ^ 5) + (fun y : ℝ => (c5 / 6) * y ^ 6) + (fun y : ℝ => (c6 / 7) * y ^ 7)) x)
                (by fun_prop : DifferentiableAt ℝ (fun y : ℝ => (c7 / 8) * y ^ 8) x)]
  rw [deriv_add (by fun_prop : DifferentiableAt ℝ ((fun y : ℝ => c0 * y) + (fun y : ℝ => (c1 / 2) * y ^ 2) + (fun y : ℝ => (c2 / 3) * y ^ 3) + (fun y : ℝ => (c3 / 4) * y ^ 4) + (fun y : ℝ => (c4 / 5) * y ^ 5) + (fun y : ℝ => (c5 / 6) * y ^ 6)) x)
                (by fun_prop : DifferentiableAt ℝ (fun y : ℝ => (c6 / 7) * y ^ 7) x)]
  rw [deriv_add (by fun_prop : DifferentiableAt ℝ ((fun y : ℝ => c0 * y) + (fun y : ℝ => (c1 / 2) * y ^ 2) + (fun y : ℝ => (c2 / 3) * y ^ 3) + (fun y : ℝ => (c3 / 4) * y ^ 4) + (fun y : ℝ => (c4 / 5) * y ^ 5)) x)
                (by fun_prop : DifferentiableAt ℝ (fun y : ℝ => (c5 / 6) * y ^ 6) x)]
  rw [deriv_add (by fun_prop : DifferentiableAt ℝ ((fun y : ℝ => c0 * y) + (fun y : ℝ => (c1 / 2) * y ^ 2) + (fun y : ℝ => (c2 / 3) * y ^ 3) + (fun y : ℝ => (c3 / 4) * y ^ 4)) x)
                (by fun_prop : DifferentiableAt ℝ (fun y : ℝ => (c4 / 5) * y ^ 5) x)]
  rw [deriv_add (by fun_prop : DifferentiableAt ℝ ((fun y : ℝ => c0 * y) + (fun y : ℝ => (c1 / 2) * y ^ 2) + (fun y : ℝ => (c2 / 3) * y ^ 3)) x)
                (by fun_prop : DifferentiableAt ℝ (fun y : ℝ => (c3 / 4) * y ^ 4) x)]
  rw [deriv_add (by fun_prop : DifferentiableAt ℝ ((fun y : ℝ => c0 * y) + (fun y : ℝ => (c1 / 2) * y ^ 2)) x)
                (by fun_prop : DifferentiableAt ℝ (fun y : ℝ => (c2 / 3) * y ^ 3) x)]
  rw [deriv_add (by fun_prop : DifferentiableAt ℝ (fun y : ℝ => c0 * y) x)
                (by fun_prop : DifferentiableAt ℝ (fun y : ℝ => (c1 / 2) * y ^ 2) x)]
  change deriv (fun y : ℝ => c0 * id y) x + deriv (fun y : ℝ => (c1 / 2) * y ^ 2) x + deriv (fun y : ℝ => (c2 / 3) * y ^ 3) x + deriv (fun y : ℝ => (c3 / 4) * y ^ 4) x + deriv (fun y : ℝ => (c4 / 5) * y ^ 5) x + deriv (fun y : ℝ => (c5 / 6) * y ^ 6) x + deriv (fun y : ℝ => (c6 / 7) * y ^ 7) x + deriv (fun y : ℝ => (c7 / 8) * y ^ 8) x + deriv (fun y : ℝ => (c8 / 9) * y ^ 9) x + deriv (fun y : ℝ => (c9 / 10) * y ^ 10) x + deriv (fun y : ℝ => (c10 / 11) * y ^ 11) x
      = c0 + c1 * x ^ 1 + c2 * x ^ 2 + c3 * x ^ 3 + c4 * x ^ 4 + c5 * x ^ 5 + c6 * x ^ 6 + c7 * x ^ 7 + c8 * x ^ 8 + c9 * x ^ 9 + c10 * x ^ 10
  simp_rw [deriv_const_mul_field, deriv_pow_field, deriv_id]
  simp
  ring_nf

/-- Differentiability of the antiderivative everywhere. -/
lemma r01_diff_coreAnti (c0 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 x : ℝ) : DifferentiableAt ℝ (coreAnti c0 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10) x := by
  unfold coreAnti
  fun_prop

/-- Continuity of the polynomial on [0,1]. -/
lemma r01_cont_corePoly (c0 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 : ℝ) :
    ContinuousOn (corePoly c0 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10) (Set.uIcc 0 1) := by
  unfold corePoly
  apply ContinuousOn.mono (by continuity :
    ContinuousOn (fun x : ℝ => c0 + c1 * x ^ 1 + c2 * x ^ 2 + c3 * x ^ 3 + c4 * x ^ 4 + c5 * x ^ 5 + c6 * x ^ 6 + c7 * x ^ 7 + c8 * x ^ 8 + c9 * x ^ 9 + c10 * x ^ 10) Set.univ)
  intro x hx
  simp

/-- Exact polynomial integral on [0,1]. -/
lemma r01_int_core_01 (c0 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 : ℝ) :
    (∫ x in (0 : ℝ)..1, corePoly c0 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 x) = c0 + c1 / 2 + c2 / 3 + c3 / 4 + c4 / 5 + c5 / 6 + c6 / 7 + c7 / 8 + c8 / 9 + c9 / 10 + c10 / 11 := by
  rw [intervalIntegral.integral_deriv_eq_sub' (coreAnti c0 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10)]
  · dsimp [coreAnti]
    norm_num <;> ring_nf
  · exact r01_deriv_coreAnti c0 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10
  · intro x hx
    exact r01_diff_coreAnti c0 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10 x
  · exact r01_cont_corePoly c0 c1 c2 c3 c4 c5 c6 c7 c8 c9 c10

theorem r01CoreR8 : (∫ R in (0 : ℝ)..1, (1 : ℝ) / 8 * R ^ 0 + (0 : ℝ) * R ^ 1 + (1 : ℝ) / 120 * R ^ 2 + (0 : ℝ) * R ^ 3 + (1 : ℝ) / 56 * R ^ 4 + (0 : ℝ) * R ^ 5 + (7 : ℝ) / 200 * R ^ 6 + (0 : ℝ) * R ^ 7 + (3 : ℝ) / 40 * R ^ 8 + (0 : ℝ) * R ^ 9 + (11 : ℝ) / 40 * R ^ 10) = (1069 : ℝ) / 6300 := by
  have hp : (∫ R in (0 : ℝ)..1, (1 : ℝ) / 8 * R ^ 0 + (0 : ℝ) * R ^ 1 + (1 : ℝ) / 120 * R ^ 2 + (0 : ℝ) * R ^ 3 + (1 : ℝ) / 56 * R ^ 4 + (0 : ℝ) * R ^ 5 + (7 : ℝ) / 200 * R ^ 6 + (0 : ℝ) * R ^ 7 + (3 : ℝ) / 40 * R ^ 8 + (0 : ℝ) * R ^ 9 + (11 : ℝ) / 40 * R ^ 10)
      = (∫ R in (0 : ℝ)..1, corePoly ((1 : ℝ) / 8) ((0 : ℝ)) ((1 : ℝ) / 120) ((0 : ℝ)) ((1 : ℝ) / 56) ((0 : ℝ)) ((7 : ℝ) / 200) ((0 : ℝ)) ((3 : ℝ) / 40) ((0 : ℝ)) ((11 : ℝ) / 40) R) := by
    apply intervalIntegral.integral_congr
    intro w _
    simp only [corePoly]
    ring
  rw [hp]
  rw [r01_int_core_01 ((1 : ℝ) / 8) ((0 : ℝ)) ((1 : ℝ) / 120) ((0 : ℝ)) ((1 : ℝ) / 56) ((0 : ℝ)) ((7 : ℝ) / 200) ((0 : ℝ)) ((3 : ℝ) / 40) ((0 : ℝ)) ((11 : ℝ) / 40)]
  norm_num

-- no closing end: anonymous noncomputable section auto-closes at EOF (N03/Q01 precedent)

#print axioms r01CoreR8
