/-
  PD20 -- THE TWO-BODY FACTOR: the wide-binary amplitude DERIVED from
  the corpus's own per-body law.  This resolves PD19's R3 (the flagged
  two-body normalization subtlety) -- by derivation, not convention.

  THE STRUCTURE.  In the deep regime, EACH body obeys the a0-line on
  the OTHER body's pull (the corpus's own law, per body):
    body 1: g1 = sqrt(a0 G M2) / r
    body 2: g2 = sqrt(a0 G M1) / r
  The relative acceleration (the accelerations point at each other):
    g_rel = g1 + g2 = (sqrt M2 + sqrt M1) sqrt(a0 G) / r.        (T1)

  THE EQUAL-MASS CASE (the registered wide-binary population):
    M1 = M2 = M/2  =>  g_rel = sqrt(2 a0 G M) / r.              (T2)
  THE FACTOR: sqrt 2 = the TWO BODIES, each driving the other's MOND
  response.  The test-particle convention (PD18) gives sqrt(a0 G M)/r:
  the two-body amplitude is sqrt 2 TIMES it -- DERIVED here from the
  per-body law, not imported.

  THE VELOCITY (the wide-binary BTFR):
    v_rel^4 = 2 a0 G M                                          (T3)
  -- the corpus's BTFR (v^4 = a0 G M_b) with the two-body factor 2 in
  the fourth power: the velocity boost 2^{1/4} = 1.19.

  T4 two_body_btfr -- the velocity chain, machine-checked.
  T5 the amplitude's positivity root-exclusion (the validated pattern).

  THE FALSIFIER (registered): equal-mass wide binaries at r > r_M have
  v_rel = (2 a0 G M)^{1/4} = 0.398 km/s for M = 1 Msun -- vs the
  Newtonian decline and vs the test-particle normalization 0.335 km/s:
  the amplitude discriminates the per-body law from BOTH.  Gaia-class
  samples measure v_rel and r directly.
-/

import Mathlib

set_option linter.unusedVariables false

/-- **T1** -- the per-body deep forces summed: the relative acceleration
is the sum of each body's a0-line response to the other's pull. -/
theorem two_body_relative {g1 g2 g_rel a0 G M1 M2 r : ℝ}
    (hG : 0 < G) (hM1 : 0 < M1) (hM2 : 0 < M2) (ha0 : 0 < a0) (hr : 0 < r)
    (hg1 : g1 = Real.sqrt (a0 * G * M2) / r)
    (hg2 : g2 = Real.sqrt (a0 * G * M1) / r)
    (hrel : g_rel = g1 + g2) :
    g_rel = (Real.sqrt M2 + Real.sqrt M1) * Real.sqrt (a0 * G) / r := by
  rw [hrel, hg1, hg2, Real.sqrt_mul (mul_pos ha0 hG).le M2,
    Real.sqrt_mul (mul_pos ha0 hG).le M1]
  ring

/-- **T2** -- the equal-mass case: the relative acceleration is
sqrt(2 a0 G M)/r with M the total -- the sqrt-2 two-body factor,
DERIVED. -/
theorem equal_mass_two_body {g_rel a0 G M r : ℝ}
    (hG : 0 < G) (hM : 0 < M) (ha0 : 0 < a0) (hr : 0 < r)
    (hrel : g_rel = (Real.sqrt (M / 2) + Real.sqrt (M / 2))
      * Real.sqrt (a0 * G) / r) :
    g_rel = Real.sqrt (2 * a0 * G * M) / r := by
  have hP : 0 < g_rel := by
    rw [hrel]
    positivity
  have hsum : (Real.sqrt (M / 2) + Real.sqrt (M / 2)) ^ 2 = 2 * M := by
    rw [← two_mul (Real.sqrt (M / 2)), mul_pow, pow_two, pow_two,
      Real.mul_self_sqrt (le_of_lt (div_pos hM (by norm_num : (0:ℝ) < 2)))]
    ring
  have hsq : g_rel ^ 2 = 2 * a0 * G * M / r ^ 2 := by
    rw [hrel, div_pow, mul_pow, hsum, pow_two, Real.mul_self_sqrt
      (le_of_lt (mul_pos ha0 hG))]
    ring
  have hsq2 : (Real.sqrt (2 * a0 * G * M) / r) ^ 2 = 2 * a0 * G * M / r ^ 2 := by
    rw [div_pow, pow_two, Real.mul_self_sqrt
      (le_of_lt (mul_pos (mul_pos (mul_pos (by norm_num : (0:ℝ) < 2) ha0) hG) hM))]
  have hEq : g_rel * g_rel
      = (Real.sqrt (2 * a0 * G * M) / r) * (Real.sqrt (2 * a0 * G * M) / r) := by
    rw [← pow_two, hsq, ← pow_two, hsq2]
  rcases mul_self_eq_mul_self_iff.mp hEq with h | h
  · exact h
  · have hneg : 0 < -(Real.sqrt (2 * a0 * G * M) / r) := by
      rw [← h]
      exact hP
    have hnonneg : 0 ≤ Real.sqrt (2 * a0 * G * M) := Real.sqrt_nonneg _
    have hdenom : 0 < Real.sqrt (2 * a0 * G * M) / r := by positivity
    linarith [hneg, hdenom]

/-- **T3/T4** -- the wide-binary BTFR: the relative velocity's fourth
power is 2 a0 G M -- the corpus's law with the two-body factor. -/
theorem two_body_btfr {v_rel g_rel a0 G M r : ℝ}
    (hr : 0 < r) (hM : 0 < M) (ha0 : 0 < a0) (hG : 0 < G)
    (hgr : g_rel ^ 2 = 2 * a0 * G * M / r ^ 2)
    (hv : v_rel ^ 2 = g_rel * r) :
    v_rel ^ 4 = 2 * a0 * G * M := by
  have h5 : v_rel ^ 4 = (v_rel ^ 2) ^ 2 := by ring
  rw [h5, hv, mul_pow, hgr]
  field_simp [hr.ne]
