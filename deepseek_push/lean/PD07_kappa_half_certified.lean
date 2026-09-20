/-
  PD07 -- kappa = 1/2, and within the framework it CANNOT be anything else.
  The certificate.

  WHAT THIS FILE CERTIFIES (mathematics, machine-checked, axioms = the
  standard three):
    * T1/T2: given the framework's axioms, kappa = 1/2, and ANY value
      satisfying the axioms is 1/2 -- the uniqueness form of "cannot be
      anything else".
    * T3: a one-channel (scalar-carried) framework is not instantiable --
      its count contradicts the metric's two-channel axiom.
    * T4: NO natural number n satisfies n = sqrt(3 pi/2): the 2 pi horizon
      coefficient (kappa = 0.461) requires a channel count of sqrt(3 pi/2),
      which does not exist.  Certified UNCONDITIONALLY, from pi's
      irrationality alone.
    * T5: the horizon form kappa = sqrt(8 pi/3)/(2 pi) cannot coexist with
      the framework: it would force pi = 8/3, contradicting pi's
      irrationality.  THE one principle-shaped competitor (k03's "not
      excluded") is now MACHINE-EXCLUDED.

  THE AXIOMS (each with its backing, stated in the structure):
    A1: kappa = 1/(channel count) -- the corpus's L230 principle (PD01 A4,
      the deep-MOND slope identity, sympy-exact).
    A4: the count is 2 -- the metric's two static Poisson channels (PD01
      B1/B2 computed to 2e-14; PD02: dimension-invariant, every d >= 2).
  Lean certifies the MATHEMATICS: the axioms' physical truth is the
  registered instruments' job (the corpus's zero points sit at 0.46 and
  1.19 sigma from 1/2; the sky measurement to 1.2% is the final word).
  Within the axioms: one value, no other.
-/

import Mathlib

/-- **The framework's axioms**, as one structure.  `count` is the number of
equal independent channels the response's carrier presents to a static
source; A1 is the corpus's L230 principle; A4 is the computed two-channel
content of the metric (PD01/PD02). -/
structure Framework (kappa : ℝ) where
  /-- the channel count of the carrier -/
  count : ℕ
  /-- a count is nonzero -/
  hnz : count ≠ 0
  /-- **A1** -- the L230 principle: kappa is the reciprocal of the count -/
  hprinciple : kappa = 1 / (count : ℝ)
  /-- **A4** -- the metric presents exactly two static channels (PD01/PD02) -/
  hcount : count = 2

/-- **T1** -- the landing: the framework forces kappa = 1/2. -/
theorem kappa_half {kappa : ℝ} (F : Framework kappa) : kappa = 1 / 2 := by
  have h := F.hprinciple
  rw [F.hcount] at h
  simpa using h

/-- **T2** -- UNIQUENESS: every framework-consistent value is 1/2.  There is
no other value the axioms permit: "cannot be anything else", positive form. -/
theorem only_half (κ' : ℝ) (F' : Framework κ') : κ' = 1 / 2 := kappa_half F'

/-- **T3** -- a scalar-carried framework (one channel) cannot exist: the
carrier's count contradicts the metric's two-channel axiom. -/
theorem no_scalar_framework {kappa : ℝ} (F : Framework kappa) :
    F.count ≠ 1 := by
  rw [F.hcount]
  norm_num

/-- **T4** -- NO natural number equals sqrt(3 pi / 2): the 2 pi horizon
coefficient would need exactly that channel count, and it does not exist.
UNCONDITIONAL -- certified from pi's irrationality alone. -/
theorem two_pi_not_a_count : ∀ n : ℕ, (n : ℝ) ≠ Real.sqrt (3 * Real.pi / 2) := by
  intro n hn
  have hsq : (n : ℝ)^2 = 3 * Real.pi / 2 := by
    rw [hn, pow_two, Real.mul_self_sqrt (by positivity)]
  have hpi : Real.pi = 2 * (n : ℝ)^2 / 3 := by
    field_simp
    linarith [hsq, Real.pi_pos]
  exact irrational_pi ⟨((2 * (n : ℚ)^2) / 3), by
    rw [Rat.cast_div, Rat.cast_mul, Rat.cast_pow, Rat.cast_ofNat, Rat.cast_natCast]
    linarith [hpi, Real.pi_pos]⟩

/-- **T5** -- THE HORIZON FORM IS EXCLUDED.  The one principle-shaped
competitor (k03's "not excluded", kappa = sqrt(8 pi/3)/(2 pi) = 0.461)
cannot coexist with the framework: the two values would force pi = 8/3,
contradicting pi's irrationality.  Machine-excluded, UNCONDITIONALLY. -/
theorem horizon_form_excluded :
    ¬ ∃ (κ : ℝ) (F : Framework κ), κ = Real.sqrt (8 * Real.pi / 3) / (2 * Real.pi) := by
  rintro ⟨κ, F, hκ⟩
  have h2 : κ = 1 / 2 := kappa_half F
  have hcomb : (1 : ℝ) / 2 = Real.sqrt (8 * Real.pi / 3) / (2 * Real.pi) := by
    rw [← h2, ← hκ]
  have hsqrt : Real.pi = Real.sqrt (8 * Real.pi / 3) := by
    have h4 := (eq_div_iff (by linarith [Real.pi_pos])).mp hcomb
    simpa using h4
  have hsq : Real.pi ^ 2 = 8 * Real.pi / 3 := by
    nth_rw 1 [hsqrt]
    rw [pow_two, Real.mul_self_sqrt (by positivity)]
  have hmul : Real.pi * (Real.pi - 8 / 3) = 0 := by nlinarith [hsq]
  rcases mul_eq_zero.mp hmul with h0 | h8
  · exact absurd h0 Real.pi_ne_zero
  · exact irrational_pi ⟨(8 : ℚ) / 3, by
      rw [Rat.cast_div, Rat.cast_ofNat]
      linarith [h8]⟩

/-- **THE LOCKED STATEMENT**: within the framework, kappa = 1/2; the value
is unique; the one-channel variant is uninstantiable; the 2 pi form is not
a count; and the horizon form cannot coexist with the axioms. -/
theorem kappa_locked {kappa : ℝ} (F : Framework kappa) :
    kappa = 1 / 2
    ∧ (∀ κ' : ℝ, Framework κ' → κ' = 1 / 2)
    ∧ (∀ n : ℕ, (n : ℝ) ≠ Real.sqrt (3 * Real.pi / 2))
    ∧ (¬ ∃ (κ : ℝ) (_F' : Framework κ), κ = Real.sqrt (8 * Real.pi / 3) / (2 * Real.pi)) :=
  ⟨kappa_half F, only_half, two_pi_not_a_count, horizon_form_excluded⟩
