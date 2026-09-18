import Mathlib

/-!
# L279 -- the algebra downstream of the candidate's derived quasi-static system

L279 (real_research/clock_2026/L279_quasistatic_slip_from_action.py) derives, from the action the PPN
pipeline uses, the leading-order static spherically symmetric equations.  Pointwise, with the Laplacians
written as reals (LΨ, LΦ, LP) and D := div(J_Y ∇P):
  (H)  4 LΦ - 2 c14 LΨ = 16 π G ρ + 2 (2 - K_B) LP      the Hamiltonian constraint with the AeST coupling
  (T)  LΨ = LΦ                                          the traceless equation carries no scalar term
  (S)  D = LΨ                                           the scalar law (the pipeline's static law)
This file certifies the algebra that follows -- nothing about ODE solutions:
  1. lensing = dynamics: the lensing Laplacian (LΨ + LΦ)/2 equals the dynamical one LΨ;
  2. the measured Newton constant: (4 - 2 c14) LΨ = 16 π G ρ + 2 (2 - K_B) LP, i.e. G_N = G/(1 - c14/2);
  3. the effective MOND equation: (2 - c14) D - (2 - K_B) LP = 8 π G ρ;
  4. the deep-MOND force bookkeeping: β √(ã₀ G M)/r = √(β² ã₀ G M)/r, i.e. a₀ = β² ã₀.
Zero sorry.  Axioms: {propext, Classical.choice, Quot.sound} only.
-/

theorem lensing_equals_dynamics (LΨ LΦ : ℝ) (hT : LΨ = LΦ) : (LΨ + LΦ) / 2 = LΨ := by
  rw [hT]; ring

theorem measured_newton_constant (LΨ LΦ LP ρ G KB c14 : ℝ)
    (hH : 4 * LΦ - 2 * c14 * LΨ = 16 * Real.pi * G * ρ + 2 * (2 - KB) * LP) (hT : LΨ = LΦ) :
    (4 - 2 * c14) * LΨ = 16 * Real.pi * G * ρ + 2 * (2 - KB) * LP := by
  rw [hT] at hH ⊢
  linear_combination hH

theorem effective_mond_equation (LΨ LΦ LP D ρ G KB c14 : ℝ)
    (hH : 4 * LΦ - 2 * c14 * LΨ = 16 * Real.pi * G * ρ + 2 * (2 - KB) * LP) (hT : LΨ = LΦ) (hS : D = LΨ) :
    (2 - c14) * D - (2 - KB) * LP = 8 * Real.pi * G * ρ := by
  subst hS
  rw [hT] at hH ⊢
  linear_combination (1 / 2 : ℝ) * hH

theorem deep_mond_force_bookkeeping (a0t G M β r : ℝ) (hβ : 0 ≤ β) :
    β * Real.sqrt (a0t * G * M) / r = Real.sqrt (β ^ 2 * (a0t * G * M)) / r := by
  rw [Real.sqrt_mul (sq_nonneg β), Real.sqrt_sq hβ]

#print axioms lensing_equals_dynamics
#print axioms measured_newton_constant
#print axioms effective_mond_equation
#print axioms deep_mond_force_bookkeeping
