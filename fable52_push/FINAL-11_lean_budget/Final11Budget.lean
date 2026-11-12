/-
  FINAL-11 (LEAN-BUDGET) -- amount-budget ARITHMETIC.

  SCOPE NOTE.
  This file machine-checks ARITHMETIC ONLY: exact-rational algebra and
  real-sqrt inequalities for the amount-budget bookkeeping. It is PURE
  MATHEMATICS -- no physical law is asserted, derived or claimed here.
  The physical input (which Lagrangian, which regime, which identification
  of the symbols with a cold-dark-energy budget) is an ASSUMPTION imported
  from outside this file, not a theorem proved in it. What Lean certifies is
  that the arithmetic consequences below follow from the stated definitions;
  it does not certify that any of it is a law of nature.

  Contents (see the docstring of each theorem):
    (1) X x > 0 for x > 0, and the functional equation X x * (1 + X x) = x^2.
    (2) X x = R_b iff x = sqrt (R_b * (1 + R_b)), for x >= 0, plus the
        numeric bracket x_break in (5.8887, 5.8889).
    (3) demand/budget ratios X x / R_b at x = 21.45, 41.98, 60.00, 98.32.
    (4) X_s / B in (10.99, 11.01).
    (5) X_s / D_low in (65.31, 65.32) and X_s / D_high = 85/2 = 42.5.
    (6) self-consistency x_b^2 = R_b * (1 + R_b) with x_b = sqrt (R_b (1+R_b)).

  HONESTY NOTE on theorem (2): the equivalence is stated with the hypothesis
  (hx : 0 <= x) because X is an EVEN function (theorem X_even below), so at
  x = -sqrt (R_b (1 + R_b)) the left side holds while the right side fails.
  The hypothesis is not a weakening of the intended claim; it records the
  domain (r / r_M >= 0) on which the claim is true. The unrestricted,
  exactly-true statement is X x = R_b iff x = sqrt (R_b (1+R_b)) OR
  x = -sqrt (R_b (1+R_b)); it is not needed downstream and is not asserted.

  Everything is closed; there are no sorry'd, weakened or trimmed statements.
-/

import Mathlib
import Aesop
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Ring
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic
open Real

namespace Final11Budget

/-- The shared-demand function X(x) = (sqrt (1 + 4 x^2) - 1) / 2. -/
noncomputable def X (x : ℝ) : ℝ := (Real.sqrt (1 + 4 * x^2) - 1) / 2

/-- Cosmic cold-to-baryon ratio, used both as the budget and as the share cap. -/
noncomputable abbrev R_b : ℝ := 541 / 100

/-- Budget B = Omega_c / Omega_b. -/
noncomputable abbrev B : ℝ := 541 / 100

/-- Low end of the delivered amount. -/
noncomputable abbrev D_low : ℝ := 911 / 1000

/-- High end of the delivered amount (140/100 = 7/5). -/
noncomputable abbrev D_high : ℝ := 7 / 5

/-- Requested share (119/2 = 59.5). -/
noncomputable abbrev X_s : ℝ := 119 / 2

/-! ------------------------------------------------------------------
  (1) Positivity and the functional equation.
  ------------------------------------------------------------------ -/

/-- X x is strictly positive for x > 0.

    Proof: 1 + 4x^2 > 1 when x ≠ 0, and sqrt is strictly monotone, so
    sqrt (1 + 4x^2) > sqrt 1 = 1, whence (sqrt (1 + 4x^2) - 1)/2 > 0. -/
theorem X_pos_of_pos (x : ℝ) (hx : 0 < x) : 0 < X x := by
  unfold X
  have hrad : (1 : ℝ) < 1 + 4 * x^2 := by nlinarith [sq_pos_of_pos hx]
  have hs : Real.sqrt (1 : ℝ) < Real.sqrt (1 + 4 * x^2) :=
    Real.sqrt_lt_sqrt (by norm_num : (0 : ℝ) ≤ 1) hrad
  rw [Real.sqrt_one] at hs
  nlinarith

/-- X x is nonnegative for every real x (the radicand is at least 1). -/
theorem X_nonneg (x : ℝ) : 0 ≤ X x := by
  unfold X
  have hrad : (1 : ℝ) ≤ 1 + 4 * x^2 := by nlinarith [sq_nonneg x]
  have hs : Real.sqrt (1 : ℝ) ≤ Real.sqrt (1 + 4 * x^2) := Real.sqrt_le_sqrt hrad
  rw [Real.sqrt_one] at hs
  nlinarith

/-- X is even. This is why theorem X_eq_R_b_iff carries the hypothesis 0 <= x. -/
theorem X_even (x : ℝ) : X (-x) = X x := by
  unfold X
  ring_nf

/-- Functional equation: X x * (1 + X x) = x^2.

    With s = sqrt (1 + 4x^2) the left side is ((s-1)/2)((s+1)/2) =
    (s^2 - 1)/4, and Real.sq_sqrt turns s^2 into the radicand (nonnegative
    because 1 + 4x^2 >= 0), giving (4x^2)/4 = x^2. -/
theorem X_mul_one_add_X (x : ℝ) : X x * (1 + X x) = x^2 := by
  unfold X
  have hnonneg : 0 ≤ 1 + 4 * x^2 := by nlinarith [sq_nonneg x]
  have hsq : Real.sqrt (1 + 4 * x^2) ^ 2 = 1 + 4 * x^2 := Real.sq_sqrt hnonneg
  nlinarith

/-! ------------------------------------------------------------------
  (2) Where X reaches the budget R_b.
  ------------------------------------------------------------------ -/

/-- X x = R_b exactly when x = sqrt (R_b * (1 + R_b)), on the domain x >= 0.

    Forward: the functional equation turns X x = R_b into x^2 = R_b(1+R_b),
    and x >= 0 identifies x with the nonnegative square root.
    Backward: with x = sqrt (R_b(1+R_b)) the functional equation gives
    (X x - R_b)(X x + (1 + R_b)) = 0; the second factor is strictly positive
    because X x >= 0 and 1 + R_b > 0, so X x = R_b. -/
theorem X_eq_R_b_iff (x : ℝ) (hx : 0 ≤ x) :
    X x = R_b ↔ x = Real.sqrt (R_b * (1 + R_b)) := by
  constructor
  · intro h
    have hx2 : x^2 = R_b * (1 + R_b) := by
      calc
        x^2 = X x * (1 + X x) := by rw [X_mul_one_add_X x]
        _ = R_b * (1 + R_b) := by rw [h]
    calc
      x = Real.sqrt (x^2) := by rw [Real.sqrt_sq_eq_abs, abs_of_nonneg hx]
      _ = Real.sqrt (R_b * (1 + R_b)) := by rw [hx2]
  · intro hxeq
    have hx2' : x^2 = R_b * (1 + R_b) := by
      rw [hxeq]
      exact Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ R_b * (1 + R_b))
    have hfe := X_mul_one_add_X x
    have hfac : (X x - R_b) * (X x + (1 + R_b)) = 0 := by
      nlinarith
    have hsec : X x + (1 + R_b) ≠ 0 := by
      have hxnn := X_nonneg x
      norm_num [R_b]
      nlinarith
    have hz : X x - R_b = 0 := by
      by_contra hne
      have : X x + (1 + R_b) = 0 := (mul_eq_zero.mp hfac).resolve_left hne
      exact hsec this
    nlinarith

/-- Numeric bracket for the break-even abscissa
    x_break = sqrt (R_b (1 + R_b)) = sqrt (346781/10000).

    Both bounds are certified by squaring:
      (58887/10000)^2 = 3467678769/100000000 < 346781/10000
      (58889/10000)^2 = 3467914321/100000000 > 346781/10000 -/
theorem x_break_bracket :
    (58887/10000 : ℝ) < Real.sqrt (R_b * (1 + R_b)) ∧
    Real.sqrt (R_b * (1 + R_b)) < (58889/10000 : ℝ) := by
  have hnorm : R_b * (1 + R_b) = (346781/10000 : ℝ) := by norm_num [R_b]
  constructor
  · rw [hnorm]
    rw [Real.lt_sqrt (by norm_num : (0 : ℝ) ≤ 58887/10000)]
    norm_num
  · rw [hnorm]
    rw [Real.sqrt_lt' (by norm_num : (0 : ℝ) < 58889/10000)]
    norm_num

/-! ------------------------------------------------------------------
  (3) Demand/budget ratio X x / R_b at the four sampled abscissae.

  Method, identical at each point. Put q = 1 + 4x^2 (an exact rational) and
  s = sqrt q. Since X x / R_b = (s - 1) * (50/541), a rational bracket
  (lo, hi) for the ratio is equivalent to a rational bracket
  (1 + 541*lo/50, 1 + 541*hi/50) for s, and each of those is certified by
  squaring the rational endpoint against q via Real.lt_sqrt / Real.sqrt_lt'.
  ------------------------------------------------------------------ -/

/-- At x = 21.45 the demand/budget ratio lies in (3.873, 3.874).
    Radicand q = 184141/100; sqrt q is bracketed by
    2145293/50000 and 1072917/25000. -/
theorem ratio_at_21_45 :
    (3873/1000 : ℝ) < X (2145/100 : ℝ) / R_b ∧
    X (2145/100 : ℝ) / R_b < (3874/1000 : ℝ) := by
  have hnorm : 1 + 4 * (2145/100 : ℝ)^2 = (184141/100 : ℝ) := by norm_num
  have hlow : (2145293/50000 : ℝ) < Real.sqrt (184141/100 : ℝ) := by
    rw [Real.lt_sqrt (by norm_num : (0 : ℝ) ≤ 2145293/50000)]
    norm_num
  have hhigh : Real.sqrt (184141/100 : ℝ) < (1072917/25000 : ℝ) := by
    rw [Real.sqrt_lt' (by norm_num : (0 : ℝ) < 1072917/25000)]
    norm_num
  have hX : X (2145/100 : ℝ) / R_b =
      (Real.sqrt (184141/100 : ℝ) - 1) * (50/541 : ℝ) := by
    unfold X R_b
    rw [hnorm]
    ring_nf
  constructor
  · rw [hX]; nlinarith
  · rw [hX]; nlinarith

/-- At x = 41.98 the demand/budget ratio lies in (7.667, 7.668).
    Radicand q = 4406426/625; sqrt q is bracketed by
    4197847/50000 and 1049597/12500. -/
theorem ratio_at_41_98 :
    (7667/1000 : ℝ) < X (4198/100 : ℝ) / R_b ∧
    X (4198/100 : ℝ) / R_b < (7668/1000 : ℝ) := by
  have hnorm : 1 + 4 * (4198/100 : ℝ)^2 = (4406426/625 : ℝ) := by norm_num
  have hlow : (4197847/50000 : ℝ) < Real.sqrt (4406426/625 : ℝ) := by
    rw [Real.lt_sqrt (by norm_num : (0 : ℝ) ≤ 4197847/50000)]
    norm_num
  have hhigh : Real.sqrt (4406426/625 : ℝ) < (1049597/12500 : ℝ) := by
    rw [Real.sqrt_lt' (by norm_num : (0 : ℝ) < 1049597/12500)]
    norm_num
  have hX : X (4198/100 : ℝ) / R_b =
      (Real.sqrt (4406426/625 : ℝ) - 1) * (50/541 : ℝ) := by
    unfold X R_b
    rw [hnorm]
    ring_nf
  constructor
  · rw [hX]; nlinarith
  · rw [hX]; nlinarith

/-- At x = 60.00 the demand/budget ratio lies in (10.998, 10.999).
    Radicand q = 14401; sqrt q is bracketed by 2999959/25000 and
    6000459/50000. -/
theorem ratio_at_60_00 :
    (10998/1000 : ℝ) < X (60 : ℝ) / R_b ∧
    X (60 : ℝ) / R_b < (10999/1000 : ℝ) := by
  have hnorm : 1 + 4 * (60 : ℝ)^2 = (14401 : ℝ) := by norm_num
  have hlow : (2999959/25000 : ℝ) < Real.sqrt (14401 : ℝ) := by
    rw [Real.lt_sqrt (by norm_num : (0 : ℝ) ≤ 2999959/25000)]
    norm_num
  have hhigh : Real.sqrt (14401 : ℝ) < (6000459/50000 : ℝ) := by
    rw [Real.sqrt_lt' (by norm_num : (0 : ℝ) < 6000459/50000)]
    norm_num
  have hX : X (60 : ℝ) / R_b =
      (Real.sqrt (14401 : ℝ) - 1) * (50/541 : ℝ) := by
    unfold X R_b
    rw [hnorm]
    ring_nf
  constructor
  · rw [hX]; nlinarith
  · rw [hX]; nlinarith

/-- At x = 98.32 the demand/budget ratio lies in (18.081, 18.082).
    Radicand q = 24167681/625; sqrt q is bracketed by 9831821/50000 and
    4916181/25000. -/
theorem ratio_at_98_32 :
    (18081/1000 : ℝ) < X (9832/100 : ℝ) / R_b ∧
    X (9832/100 : ℝ) / R_b < (18082/1000 : ℝ) := by
  have hnorm : 1 + 4 * (9832/100 : ℝ)^2 = (24167681/625 : ℝ) := by norm_num
  have hlow : (9831821/50000 : ℝ) < Real.sqrt (24167681/625 : ℝ) := by
    rw [Real.lt_sqrt (by norm_num : (0 : ℝ) ≤ 9831821/50000)]
    norm_num
  have hhigh : Real.sqrt (24167681/625 : ℝ) < (4916181/25000 : ℝ) := by
    rw [Real.sqrt_lt' (by norm_num : (0 : ℝ) < 4916181/25000)]
    norm_num
  have hX : X (9832/100 : ℝ) / R_b =
      (Real.sqrt (24167681/625 : ℝ) - 1) * (50/541 : ℝ) := by
    unfold X R_b
    rw [hnorm]
    ring_nf
  constructor
  · rw [hX]; nlinarith
  · rw [hX]; nlinarith

/-! ------------------------------------------------------------------
  (4) Requested share against the budget.
  ------------------------------------------------------------------ -/

/-- X_s / B = (119/2)/(541/100) = 5950/541, which lies in (10.99, 11.01).
    Exact rational arithmetic; no sqrt involved. -/
theorem share_over_budget :
    (1099/100 : ℝ) < X_s / B ∧ X_s / B < (1101/100 : ℝ) := by
  norm_num [X_s, B]

/-! ------------------------------------------------------------------
  (5) Requested share against the delivered amounts.
  ------------------------------------------------------------------ -/

/-- X_s / D_low = (119/2)/(911/1000) = 59500/911, which lies in
    (65.31, 65.32). Exact rational arithmetic. -/
theorem share_over_D_low :
    (6531/100 : ℝ) < X_s / D_low ∧ X_s / D_low < (6532/100 : ℝ) := by
  norm_num [X_s, D_low]

/-- X_s / D_high = (119/2)/(7/5) = 85/2 exactly, i.e. 42.5. -/
theorem share_over_D_high_exact : X_s / D_high = (85/2 : ℝ) := by
  norm_num [X_s, D_high]

/-- Bracket form of the same statement: X_s / D_high lies in (42.45, 42.55). -/
theorem share_over_D_high :
    (849/20 : ℝ) < X_s / D_high ∧ X_s / D_high < (851/20 : ℝ) := by
  norm_num [X_s, D_high]

/-! ------------------------------------------------------------------
  (6) Self-consistency of the break-even abscissa.
  ------------------------------------------------------------------ -/

/-- For any R with 0 < R, the abscissa x_b = sqrt (R (1 + R)) satisfies
    x_b^2 = R (1 + R): the radicand R(1+R) is positive, hence nonnegative,
    so Real.sq_sqrt applies. -/
theorem break_sq_of_pos (R : ℝ) (hR : 0 < R) :
    (Real.sqrt (R * (1 + R)))^2 = R * (1 + R) := by
  have h1 : 0 < 1 + R := by nlinarith
  exact Real.sq_sqrt (le_of_lt (mul_pos hR h1))

/-- The budget value R_b = 541/100 is positive, so its break-even abscissa
    satisfies x_b^2 = R_b (1 + R_b). This is the self-consistency identity. -/
theorem break_sq_R_b :
    (Real.sqrt (R_b * (1 + R_b)))^2 = R_b * (1 + R_b) := by
  exact break_sq_of_pos R_b (by norm_num [R_b])

/-- Consistency check: X actually attains the budget at the abscissa produced
    by theorem X_eq_R_b_iff. -/
theorem X_at_break : X (Real.sqrt (R_b * (1 + R_b))) = R_b := by
  exact (X_eq_R_b_iff (Real.sqrt (R_b * (1 + R_b))) (Real.sqrt_nonneg _)).mpr rfl

end Final11Budget

#print axioms Final11Budget.X_pos_of_pos
#print axioms Final11Budget.X_nonneg
#print axioms Final11Budget.X_even
#print axioms Final11Budget.X_mul_one_add_X
#print axioms Final11Budget.X_eq_R_b_iff
#print axioms Final11Budget.x_break_bracket
#print axioms Final11Budget.ratio_at_21_45
#print axioms Final11Budget.ratio_at_41_98
#print axioms Final11Budget.ratio_at_60_00
#print axioms Final11Budget.ratio_at_98_32
#print axioms Final11Budget.share_over_budget
#print axioms Final11Budget.share_over_D_low
#print axioms Final11Budget.share_over_D_high_exact
#print axioms Final11Budget.share_over_D_high
#print axioms Final11Budget.break_sq_of_pos
#print axioms Final11Budget.break_sq_R_b
#print axioms Final11Budget.X_at_break
