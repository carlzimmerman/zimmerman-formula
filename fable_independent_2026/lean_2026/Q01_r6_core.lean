import Mathlib

/-!
# Q01 — the first-flight ladder certified as exact R-core polynomial integrals

Companion to deepseek_push/Q01_r6_lean.py (P01's E[int r^6 ds] = 149/700, M05's
3/4 / 5/12 / 1/4).  For each first-flight moment I_m the lane derives, in exact
sympy rational arithmetic, an explicit even polynomial P~_m(R) on [0,1] with
I_m = ∫₀¹ P~_m dR (route: per-R exact mu->t change of variables t = chord, the
log/atanh terms integrated by parts with the V(1)=0 antiderivative so V/(1-R²)
is polynomial — the divisibility is CHECKED, not assumed).  Lean certifies the
four one-dimensional polynomial integrals below EXACTLY (FTC engine of
N03_small_spine.lean).

SCOPE (pre-registered K3): Lean certifies the 1D cores.  The 2D->1D reduction is
analytic (sympy exact rationals, recorded in Q01_r6_lean.py) and numerically
cross-checked at 40 dps by P01's two independent routes (agreement 2.87e-42,
P01_r6_moment.py/.json) — it is NOT a 2D Lean certification.
-/

namespace Q01

noncomputable section

open scoped intervalIntegral

/-- Antiderivative of a degree-8 polynomial (function-level sum). -/
def coreAnti (c0 c1 c2 c3 c4 c5 c6 c7 c8 : ℝ) : ℝ → ℝ :=
  (fun y : ℝ => c0 * y) +
    (fun y : ℝ => (c1 / 2) * y ^ 2) +
    (fun y : ℝ => (c2 / 3) * y ^ 3) +
    (fun y : ℝ => (c3 / 4) * y ^ 4) +
    (fun y : ℝ => (c4 / 5) * y ^ 5) +
    (fun y : ℝ => (c5 / 6) * y ^ 6) +
    (fun y : ℝ => (c6 / 7) * y ^ 7) +
    (fun y : ℝ => (c7 / 8) * y ^ 8) +
    (fun y : ℝ => (c8 / 9) * y ^ 9)

/-- The polynomial itself. -/
def corePoly (c0 c1 c2 c3 c4 c5 c6 c7 c8 : ℝ) : ℝ → ℝ :=
  fun x : ℝ => c0 + c1 * x ^ 1 + c2 * x ^ 2 + c3 * x ^ 3 + c4 * x ^ 4 + c5 * x ^ 5 + c6 * x ^ 6 + c7 * x ^ 7 + c8 * x ^ 8

/-- deriv (coreAnti) = corePoly, termwise. -/
lemma q01_deriv_coreAnti (c0 c1 c2 c3 c4 c5 c6 c7 c8 : ℝ) : deriv (coreAnti c0 c1 c2 c3 c4 c5 c6 c7 c8) = corePoly c0 c1 c2 c3 c4 c5 c6 c7 c8 := by
  funext x
  unfold coreAnti corePoly
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
  change deriv (fun y : ℝ => c0 * id y) x + deriv (fun y : ℝ => (c1 / 2) * y ^ 2) x + deriv (fun y : ℝ => (c2 / 3) * y ^ 3) x + deriv (fun y : ℝ => (c3 / 4) * y ^ 4) x + deriv (fun y : ℝ => (c4 / 5) * y ^ 5) x + deriv (fun y : ℝ => (c5 / 6) * y ^ 6) x + deriv (fun y : ℝ => (c6 / 7) * y ^ 7) x + deriv (fun y : ℝ => (c7 / 8) * y ^ 8) x + deriv (fun y : ℝ => (c8 / 9) * y ^ 9) x
      = c0 + c1 * x ^ 1 + c2 * x ^ 2 + c3 * x ^ 3 + c4 * x ^ 4 + c5 * x ^ 5 + c6 * x ^ 6 + c7 * x ^ 7 + c8 * x ^ 8
  simp_rw [deriv_const_mul_field, deriv_pow_field, deriv_id]
  simp
  ring_nf

/-- Differentiability of the antiderivative everywhere. -/
lemma q01_diff_coreAnti (c0 c1 c2 c3 c4 c5 c6 c7 c8 x : ℝ) : DifferentiableAt ℝ (coreAnti c0 c1 c2 c3 c4 c5 c6 c7 c8) x := by
  unfold coreAnti
  fun_prop

/-- Continuity of the polynomial on [0,1]. -/
lemma q01_cont_corePoly (c0 c1 c2 c3 c4 c5 c6 c7 c8 : ℝ) :
    ContinuousOn (corePoly c0 c1 c2 c3 c4 c5 c6 c7 c8) (Set.uIcc 0 1) := by
  unfold corePoly
  apply ContinuousOn.mono (by continuity :
    ContinuousOn (fun x : ℝ => c0 + c1 * x ^ 1 + c2 * x ^ 2 + c3 * x ^ 3 + c4 * x ^ 4 + c5 * x ^ 5 + c6 * x ^ 6 + c7 * x ^ 7 + c8 * x ^ 8) Set.univ)
  intro x hx
  simp

/-- Exact polynomial integral on [0,1]. -/
lemma q01_int_core_01 (c0 c1 c2 c3 c4 c5 c6 c7 c8 : ℝ) :
    (∫ x in (0 : ℝ)..1, corePoly c0 c1 c2 c3 c4 c5 c6 c7 c8 x) = c0 + c1 / 2 + c2 / 3 + c3 / 4 + c4 / 5 + c5 / 6 + c6 / 7 + c7 / 8 + c8 / 9 := by
  rw [intervalIntegral.integral_deriv_eq_sub' (coreAnti c0 c1 c2 c3 c4 c5 c6 c7 c8)]
  · dsimp [coreAnti]
    norm_num <;> ring_nf
  · exact q01_deriv_coreAnti c0 c1 c2 c3 c4 c5 c6 c7 c8
  · intro x hx
    exact q01_diff_coreAnti c0 c1 c2 c3 c4 c5 c6 c7 c8 x
  · exact q01_cont_corePoly c0 c1 c2 c3 c4 c5 c6 c7 c8

/-- I_1 = ∫₀¹ P~_{m} dR = 3/4 (sympy-exact core; see Q01_r6_lean.py). -/
theorem q01CoreChord : (∫ R in (0 : ℝ)..1, (3 : ℝ) / 8 * R ^ 0 + (0 : ℝ) * R ^ 1 + (9 : ℝ) / 8 * R ^ 2 + (0 : ℝ) * R ^ 3 + (0 : ℝ) * R ^ 4 + (0 : ℝ) * R ^ 5 + (0 : ℝ) * R ^ 6 + (0 : ℝ) * R ^ 7 + (0 : ℝ) * R ^ 8) = (3 : ℝ) / 4 := by
  have hp : (∫ R in (0 : ℝ)..1, (3 : ℝ) / 8 * R ^ 0 + (0 : ℝ) * R ^ 1 + (9 : ℝ) / 8 * R ^ 2 + (0 : ℝ) * R ^ 3 + (0 : ℝ) * R ^ 4 + (0 : ℝ) * R ^ 5 + (0 : ℝ) * R ^ 6 + (0 : ℝ) * R ^ 7 + (0 : ℝ) * R ^ 8)
      = (∫ R in (0 : ℝ)..1, corePoly ((3 : ℝ) / 8) ((0 : ℝ)) ((9 : ℝ) / 8) ((0 : ℝ)) ((0 : ℝ)) ((0 : ℝ)) ((0 : ℝ)) ((0 : ℝ)) ((0 : ℝ)) R) := by
    apply intervalIntegral.integral_congr
    intro w _
    simp only [corePoly]
    ring
  rw [hp]
  rw [q01_int_core_01 ((3 : ℝ) / 8) ((0 : ℝ)) ((9 : ℝ) / 8) ((0 : ℝ)) ((0 : ℝ)) ((0 : ℝ)) ((0 : ℝ)) ((0 : ℝ)) ((0 : ℝ))]
  norm_num

/-- I_2 = ∫₀¹ P~_{m} dR = 5/12 (sympy-exact core; see Q01_r6_lean.py). -/
theorem q01CoreR2 : (∫ R in (0 : ℝ)..1, (1 : ℝ) / 4 * R ^ 0 + (0 : ℝ) * R ^ 1 + (1 : ℝ) / 8 * R ^ 2 + (0 : ℝ) * R ^ 3 + (5 : ℝ) / 8 * R ^ 4 + (0 : ℝ) * R ^ 5 + (0 : ℝ) * R ^ 6 + (0 : ℝ) * R ^ 7 + (0 : ℝ) * R ^ 8) = (5 : ℝ) / 12 := by
  have hp : (∫ R in (0 : ℝ)..1, (1 : ℝ) / 4 * R ^ 0 + (0 : ℝ) * R ^ 1 + (1 : ℝ) / 8 * R ^ 2 + (0 : ℝ) * R ^ 3 + (5 : ℝ) / 8 * R ^ 4 + (0 : ℝ) * R ^ 5 + (0 : ℝ) * R ^ 6 + (0 : ℝ) * R ^ 7 + (0 : ℝ) * R ^ 8)
      = (∫ R in (0 : ℝ)..1, corePoly ((1 : ℝ) / 4) ((0 : ℝ)) ((1 : ℝ) / 8) ((0 : ℝ)) ((5 : ℝ) / 8) ((0 : ℝ)) ((0 : ℝ)) ((0 : ℝ)) ((0 : ℝ)) R) := by
    apply intervalIntegral.integral_congr
    intro w _
    simp only [corePoly]
    ring
  rw [hp]
  rw [q01_int_core_01 ((1 : ℝ) / 4) ((0 : ℝ)) ((1 : ℝ) / 8) ((0 : ℝ)) ((5 : ℝ) / 8) ((0 : ℝ)) ((0 : ℝ)) ((0 : ℝ)) ((0 : ℝ))]
  norm_num

/-- I_4 = ∫₀¹ P~_{m} dR = 1/4 (sympy-exact core; see Q01_r6_lean.py). -/
theorem q01CoreR4 : (∫ R in (0 : ℝ)..1, (5 : ℝ) / 32 * R ^ 0 + (0 : ℝ) * R ^ 1 + (61 : ℝ) / 160 * R ^ 2 + (0 : ℝ) * R ^ 3 + (-31 : ℝ) / 96 * R ^ 4 + (0 : ℝ) * R ^ 5 + (7 : ℝ) / 32 * R ^ 6 + (0 : ℝ) * R ^ 7 + (0 : ℝ) * R ^ 8) = (1 : ℝ) / 4 := by
  have hp : (∫ R in (0 : ℝ)..1, (5 : ℝ) / 32 * R ^ 0 + (0 : ℝ) * R ^ 1 + (61 : ℝ) / 160 * R ^ 2 + (0 : ℝ) * R ^ 3 + (-31 : ℝ) / 96 * R ^ 4 + (0 : ℝ) * R ^ 5 + (7 : ℝ) / 32 * R ^ 6 + (0 : ℝ) * R ^ 7 + (0 : ℝ) * R ^ 8)
      = (∫ R in (0 : ℝ)..1, corePoly ((5 : ℝ) / 32) ((0 : ℝ)) ((61 : ℝ) / 160) ((0 : ℝ)) ((-31 : ℝ) / 96) ((0 : ℝ)) ((7 : ℝ) / 32) ((0 : ℝ)) ((0 : ℝ)) R) := by
    apply intervalIntegral.integral_congr
    intro w _
    simp only [corePoly]
    ring
  rw [hp]
  rw [q01_int_core_01 ((5 : ℝ) / 32) ((0 : ℝ)) ((61 : ℝ) / 160) ((0 : ℝ)) ((-31 : ℝ) / 96) ((0 : ℝ)) ((7 : ℝ) / 32) ((0 : ℝ)) ((0 : ℝ))]
  norm_num

/-- I_6 = ∫₀¹ P~_{m} dR = 149/700 (sympy-exact core; see Q01_r6_lean.py). -/
theorem q01CoreR6 : (∫ R in (0 : ℝ)..1, (3 : ℝ) / 20 * R ^ 0 + (0 : ℝ) * R ^ 1 + (9 : ℝ) / 560 * R ^ 2 + (0 : ℝ) * R ^ 3 + (3 : ℝ) / 80 * R ^ 4 + (0 : ℝ) * R ^ 5 + (7 : ℝ) / 80 * R ^ 6 + (0 : ℝ) * R ^ 7 + (27 : ℝ) / 80 * R ^ 8) = (149 : ℝ) / 700 := by
  have hp : (∫ R in (0 : ℝ)..1, (3 : ℝ) / 20 * R ^ 0 + (0 : ℝ) * R ^ 1 + (9 : ℝ) / 560 * R ^ 2 + (0 : ℝ) * R ^ 3 + (3 : ℝ) / 80 * R ^ 4 + (0 : ℝ) * R ^ 5 + (7 : ℝ) / 80 * R ^ 6 + (0 : ℝ) * R ^ 7 + (27 : ℝ) / 80 * R ^ 8)
      = (∫ R in (0 : ℝ)..1, corePoly ((3 : ℝ) / 20) ((0 : ℝ)) ((9 : ℝ) / 560) ((0 : ℝ)) ((3 : ℝ) / 80) ((0 : ℝ)) ((7 : ℝ) / 80) ((0 : ℝ)) ((27 : ℝ) / 80) R) := by
    apply intervalIntegral.integral_congr
    intro w _
    simp only [corePoly]
    ring
  rw [hp]
  rw [q01_int_core_01 ((3 : ℝ) / 20) ((0 : ℝ)) ((9 : ℝ) / 560) ((0 : ℝ)) ((3 : ℝ) / 80) ((0 : ℝ)) ((7 : ℝ) / 80) ((0 : ℝ)) ((27 : ℝ) / 80)]
  norm_num

-- FIX-FORWARD 2026-09-24 (4th): no closing end — the anonymous noncomputable section
-- must be closed before `end Q01`; N03_small_spine.lean precedent is to let EOF auto-close.
#print axioms q01CoreChord
#print axioms q01CoreR2
#print axioms q01CoreR4
#print axioms q01CoreR6
