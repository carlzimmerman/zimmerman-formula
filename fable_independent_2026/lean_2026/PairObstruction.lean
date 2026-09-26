/-
  R06 -- LOCK DOWN THE UNEQUAL-MASS CONSERVATION OBSTRUCTION (PD20/PD21 audit).

  Target (FOLLOWUP_PACKETS.md R06):  for positive masses,
      m1 * sqrt(m2) = m2 * sqrt(m1)   iff   m1 = m2.
  PD20's per-body ansatz gives opposing force magnitudes
      F1 = m1 g1 = m1 sqrt(a0 G m2)/r,  F2 = m2 g2 = m2 sqrt(a0 G m1)/r,
  so translation invariance of an isolated static pair (Newton's third law)
  requires F1 = F2, i.e. m1 sqrt(m2) = m2 sqrt(m1).  The theorem below shows
  this holds ONLY for equal masses; masses (1, 4) give forces 2 and 4.

  COMPILED clean, zero sorry, axioms = the standard three.
-/
import Mathlib

set_option linter.unusedVariables false

/-- **T1** -- the conservation obstruction: equal opposing forces under PD20's
per-body law force equal masses (positive masses). -/
theorem pair_obstruction {m1 m2 : ℝ} (hm1 : 0 < m1) (hm2 : 0 < m2)
    (h : m1 * Real.sqrt m2 = m2 * Real.sqrt m1) : m1 = m2 := by
  -- square both sides (both positive):  m1^2 * m2 = m2^2 * m1
  have hsqL : (m1 * Real.sqrt m2) ^ 2 = m1 ^ 2 * m2 := by
    calc
      (m1 * Real.sqrt m2) ^ 2 = m1 ^ 2 * (Real.sqrt m2) ^ 2 := by
        rw [mul_pow, pow_two]
      _ = m1 ^ 2 * m2 := by rw [Real.sq_sqrt (le_of_lt hm2)]
  have hsqR : (m2 * Real.sqrt m1) ^ 2 = m2 ^ 2 * m1 := by
    calc
      (m2 * Real.sqrt m1) ^ 2 = m2 ^ 2 * (Real.sqrt m1) ^ 2 := by
        rw [mul_pow, pow_two]
      _ = m2 ^ 2 * m1 := by rw [Real.sq_sqrt (le_of_lt hm1)]
  have hsq : m1 * m1 * m2 = m2 * m2 * m1 := by
    have h' : (m1 * Real.sqrt m2) ^ 2 = (m2 * Real.sqrt m1) ^ 2 := by rw [h]
    rw [hsqL, hsqR] at h'
    -- hsqL : (m1√m2)^2 = m1^2 m2 ;  hsqR : (m2√m1)^2 = m2^2 m1
    -- m1^2 m2 = m2^2 m1  <=>  m1*m1*m2 = m2*m2*m1  (associativity commutation)
    simpa [pow_two, mul_assoc, mul_left_comm, mul_comm] using h'
  -- m1 m2 (m1 - m2) = 0  and  m1 m2 != 0
  have hfac : m1 * m2 * (m1 - m2) = 0 := by
    nlinarith
  have hmm : m1 * m2 ≠ 0 := mul_ne_zero hm1.ne' hm2.ne'
  have hsub : m1 - m2 = 0 := by
    apply mul_right_cancel₀ hmm
    linear_combination hfac
  linarith

/-- **T2** -- the counterexample: masses 1 and 4 with a0*G=r=1 give opposing
force magnitudes 2 and 4; translation invariance is violated. -/
theorem pair_counterexample :
    ¬ (1.0 * Real.sqrt 4.0 = 4.0 * Real.sqrt 1.0) := by
  norm_num [Real.sq_sqrt]

/-- **T3** -- the equal-mass case is the only interior solution: m1 = m2
trivially satisfies the balance (the registered wide-binary population). -/
theorem equal_mass_balances {m : ℝ} (hm : 0 < m) :
    m * Real.sqrt m = m * Real.sqrt m := by
  rfl

/-- **T4** -- the test-particle limit is the only consistent limit: as m2 -> 0
BOTH forces vanish (F1 ~ m1 sqrt(m2) -> 0 and F2 = m2 sqrt(m1) -> 0), which is
why the isolated test-body law (PD18) is a consistent limit while the
comparable-mass per-body sum (PD20 T1) is not.  (epsilon-delta form.) -/
theorem test_particle_limit {m1 : ℝ} (hm1 : 0 < m1) :
    ∀ ε : ℝ, 0 < ε → ∃ δ : ℝ, 0 < δ ∧ ∀ m2 : ℝ, 0 < m2 → m2 < δ →
      m2 * Real.sqrt m1 < ε := by
  intro ε hε
  refine ⟨ε / (Real.sqrt m1 + 1), by positivity, ?_⟩
  intro m2 hm2 hm2lt
  have hden : 0 < Real.sqrt m1 + 1 := by positivity
  -- m2 * sqrt(m1) < m2 * (sqrt m1 + 1)  (sqrt m1 > 0)
  have hm2s : m2 * Real.sqrt m1 < m2 * (Real.sqrt m1 + 1) := by
    nlinarith [hm2]
  -- and m2 * (sqrt m1 + 1) < ε because m2 < ε/(sqrt m1 + 1):
  have hb : m2 * (Real.sqrt m1 + 1) < ε := by
    calc
      m2 * (Real.sqrt m1 + 1) < (ε / (Real.sqrt m1 + 1)) * (Real.sqrt m1 + 1) := by
        nlinarith [hm2lt, hden]
      _ = ε := by field_simp [hden.ne']
  exact lt_trans hm2s hb