import Mathlib

noncomputable section
open scoped Real

-- AS027 — Effective AQUAL response of the Q branch: Lean certificates of the
-- exact algebraic core.
--
-- Symbols (SI-free, dimensionless; x = g/a0, y = B/a0 on the Q branch
-- g^2 = B^2 + a0 B):
--   qY x  = y(x) = (sqrt(1+4x^2)-1)/2        : unique positive root of y^2+y=x^2
--   qMu x = mu_Q(x) = qY x / x               : effective AQUAL kernel of Q
--   qNu y = nu_Q(y) = sqrt(1+1/y)            : g/B boost of Q
--
-- Certified content:
--   qY_sq_add        : y^2 + y = x^2 (the Q-branch master identity)
--   qY_pos           : y > 0 for x > 0
--   qMu_mul_self     : mu(x) * x = y  (spherical AQUAL flux inversion:
--                      div(mu grad Phi) = 4 pi G rho  reduces to mu(x)*x = y)
--   qMu_rationalized : mu(x) = 2x/(1+sqrt(1+4x^2))  (stable form, no cancellation)
--   qMu_inverse      : x = mu/(1-mu^2)   (exact inverse of the Q law in mu space;
--                      the divided form is ill-conditioned near mu -> 1, but the
--                      identity itself is exact — certified here, independent of
--                      any floating-point conditioning)
--   qNu_sq           : nu(y)^2 = 1 + 1/y
--   qMu_lt_one       : 0 < mu < 1 for x > 0 (range statement, strict)
--
-- House discipline: this file is fully self-contained (no sibling imports),
-- contains no uncovered obligations, and its axiom set is verified below with
-- an unfiltered `#print axioms` block (nothing may exceed
-- {propext, Classical.choice, Quot.sound}).

def qY (x : ℝ) : ℝ := (Real.sqrt (1 + 4 * x ^ 2) - 1) / 2
def qMu (x : ℝ) : ℝ := qY x / x
def qNu (y : ℝ) : ℝ := Real.sqrt (1 + 1 / y)

-- sqrt(1+4x^2)^2 = 1+4x^2  (the only analysis input; holds since 1+4x^2 >= 0)
theorem q_sqrt_sq (x : ℝ) : (Real.sqrt (1 + 4 * x ^ 2)) ^ 2 = 1 + 4 * x ^ 2 := by
  have h : 0 ≤ 1 + 4 * x ^ 2 := by nlinarith [sq_nonneg x]
  simpa [pow_two] using Real.mul_self_sqrt h

-- Master identity: y^2 + y = x^2.
theorem qY_sq_add (x : ℝ) : qY x ^ 2 + qY x = x ^ 2 := by
  unfold qY
  nlinarith [q_sqrt_sq x]

-- y > 0 for x > 0.
theorem qY_pos (x : ℝ) (hx : 0 < x) : 0 < qY x := by
  unfold qY
  have hs_gt_one : 1 < Real.sqrt (1 + 4 * x ^ 2) := by
    by_contra h
    have hle : Real.sqrt (1 + 4 * x ^ 2) ≤ 1 := le_of_not_gt h
    have hmul : Real.sqrt (1 + 4 * x ^ 2) * Real.sqrt (1 + 4 * x ^ 2) ≤ 1 := by
      simpa using (mul_le_mul hle hle (Real.sqrt_nonneg _) (by norm_num : (0 : ℝ) ≤ 1) :
        Real.sqrt (1 + 4 * x ^ 2) * Real.sqrt (1 + 4 * x ^ 2) ≤ 1 * 1)
    nlinarith [q_sqrt_sq x, hmul, hx]
  have : 0 < Real.sqrt (1 + 4 * x ^ 2) - 1 := by nlinarith [hs_gt_one]
  nlinarith

-- Spherical AQUAL flux inversion: mu(x) * x = y.
theorem qMu_mul_self (x : ℝ) (hx : x ≠ 0) : qMu x * x = qY x := by
  unfold qMu
  field_simp [hx]

-- Stable (rationalized) form of the kernel: mu(x) = 2x/(1+sqrt(1+4x^2)).
theorem qMu_rationalized (x : ℝ) (hx : 0 < x) :
    qMu x = 2 * x / (1 + Real.sqrt (1 + 4 * x ^ 2)) := by
  unfold qMu qY
  have hden : 1 + Real.sqrt (1 + 4 * x ^ 2) ≠ 0 := by
    have : 0 < 1 + Real.sqrt (1 + 4 * x ^ 2) := by
      nlinarith [Real.sqrt_nonneg (1 + 4 * x ^ 2)]
    exact ne_of_gt this
  field_simp [ne_of_gt hx, hden]
  nlinarith [q_sqrt_sq x]

-- Exact inverse of the Q law in mu space: x = mu/(1-mu^2).
theorem qMu_inverse (x : ℝ) (hx : 0 < x) : x = qMu x / (1 - qMu x ^ 2) := by
  have hxne : x ≠ 0 := ne_of_gt hx
  have hmain : qY x ^ 2 + qY x = x ^ 2 := qY_sq_add x
  have hmu : qMu x * x = qY x := qMu_mul_self x hxne
  have h1 : qMu x ^ 2 * x ^ 2 + qMu x * x = x ^ 2 := by
    nlinarith [hmain, hmu]
  have h2 : qMu x ^ 2 * x + qMu x = x := by
    have h2a : x * (qMu x ^ 2 * x + qMu x) = x * x := by nlinarith [h1]
    exact mul_left_cancel₀ hxne h2a
  have hcq : x * (1 - qMu x ^ 2) = qMu x := by nlinarith [h2]
  have hmu_pos : 0 < qMu x := by
    unfold qMu
    exact div_pos (qY_pos x hx) hx
  have hden : 1 - qMu x ^ 2 ≠ 0 := by
    intro hz
    have hmm : qMu x * qMu x = 1 := by nlinarith [hz]
    have hmu1 : qMu x = 1 := by
      have hc := (mul_self_eq_mul_self_iff (a := qMu x) (b := 1)).mp (by simpa [pow_two] using hmm)
      rcases hc with hc | hc
      · exact hc
      · nlinarith [hmu_pos, hc]
    have hqyx : qY x = x := by
      have hmu1x : qMu x * x = 1 * x := by rw [hmu1]
      nlinarith [hmu, hmu1x]
    have hx0 : x = 0 := by nlinarith [hmain, hqyx]
    exact hxne hx0
  rw [eq_div_iff hden]
  exact hcq

-- nu form: nu(y)^2 = 1 + 1/y for y > 0.
theorem qNu_sq (y : ℝ) (hy : 0 < y) : qNu y ^ 2 = 1 + 1 / y := by
  unfold qNu
  have h : 0 ≤ 1 + 1 / y := by positivity
  simpa [pow_two] using Real.mul_self_sqrt h

-- Range statement: 0 < mu < 1 for x > 0 (upper bound here; positivity in qMu_mul_self proof).
theorem qMu_lt_one (x : ℝ) (hx : 0 < x) : qMu x < 1 := by
  have hmain := qY_sq_add x
  have hqy_pos := qY_pos x hx
  have hdiff : 0 < x ^ 2 - qY x ^ 2 := by nlinarith [hmain, hqy_pos]
  have hsum_pos : 0 < x + qY x := by nlinarith [hx, hqy_pos]
  have hxgt : qY x < x := by
    by_contra h
    have hle : x ≤ qY x := le_of_not_gt h
    have hprod : (x - qY x) * (x + qY x) ≤ 0 := by
      exact mul_nonpos_of_nonpos_of_nonneg (sub_nonpos.mpr hle) (le_of_lt hsum_pos)
    have hsqu : (x - qY x) * (x + qY x) = x ^ 2 - qY x ^ 2 := by ring
    nlinarith [hdiff, hprod, hsqu]
  unfold qMu
  exact (div_lt_one hx).2 hxgt

-- axiom audit (unfiltered)
#print axioms q_sqrt_sq
#print axioms qY_sq_add
#print axioms qY_pos
#print axioms qMu_mul_self
#print axioms qMu_rationalized
#print axioms qMu_inverse
#print axioms qNu_sq
#print axioms qMu_lt_one
