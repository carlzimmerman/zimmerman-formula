import Mathlib

/-!
# a09_lean_nonvacuity -- adversarial audit of fable_independent_2026/lean_2026/PUZZLE_32pi_reductions.lean

Question (i): are the hypotheses of the author's theorems satisfiable (non-vacuous), and are the `iff`s non-degenerate?
This file does NOT import the author's file; it restates the two hypothesis-carrying theorems' premises and produces explicit witnesses,
plus counter-examples showing the equivalences separate true from false cases.  Compile with (from fable_independent_2026/lean_2026):
    lake env lean /path/to/a09_lean_nonvacuity.lean
-/

open Real

/-- premises of `Zsq_from_curvature_match` are satisfiable (a0 = 1, Λ = 32π, L = sqrt (3/(32π))) -/
example : ∃ a0 Λ L : ℝ, 0 < a0 ∧ L ^ 2 = 3 / Λ ∧ 1 / (1 / (2 * a0)) ^ 2 = Λ / (8 * π) := by
  have hp := Real.pi_pos
  refine ⟨1, 32 * π, Real.sqrt (3 / (32 * π)), one_pos, ?_, ?_⟩
  · rw [Real.sq_sqrt (by positivity)]
  · field_simp; ring

/-- premises of `Zsq_from_kappa_match` are satisfiable (a0 = 1, Λ = 8π, L = sqrt(3/(8π))) -/
example : ∃ a0 Λ L : ℝ, 0 < a0 ∧ 0 < Λ ∧ L ^ 2 = 3 / Λ ∧ a0 ^ 2 = Λ / (8 * π) := by
  have hp := Real.pi_pos
  refine ⟨1, 8 * π, Real.sqrt (3 / (8 * π)), one_pos, by positivity, ?_, ?_⟩
  · rw [Real.sq_sqrt (by positivity)]
  · field_simp

/-- the first equivalence separates: a WRONG coefficient (16π instead of 32π) makes the left side false -/
example : ¬ ((π / (1 : ℝ) ^ 2) * (16 * π) = 32 * π ^ 2) := by
  have hp := Real.pi_pos
  intro h
  nlinarith [h, sq_pos_of_pos hp]

/-- the density equivalence separates: Λ = 16π a0^2 does NOT satisfy rho r_s^2 = 1 -/
example : ¬ (((16 * π) / (8 * π)) * (1 / (2 * (1 : ℝ))) ^ 2 = 1) := by
  have hp := Real.pi_pos
  intro h
  field_simp at h
  norm_num at h

/-- mutation of the near-miss theorem: kappa^2 = rho_Lambda does NOT give 32π/3 (it gives 8π/3 ≠ 32π/3) -/
example : (8 * π / 3 : ℝ) ≠ 32 * π / 3 := by
  have hp := Real.pi_pos
  intro h
  linarith

/-- What the file does NOT certify (kept as a reminder): `charge_Schwarzschild` takes E4 = 48 M^2/r^6 as an INPUT constant; the Riemann computation is sympy (p01). -/
example : True := trivial
