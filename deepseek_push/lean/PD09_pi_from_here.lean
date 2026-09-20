/-
  PD09 -- PI FROM HERE?  The honest answer, certified.

  QUESTION: can the framework figure out the irrationality of pi?

  ANSWER: no -- and the work shows something better.  pi's arithmetic is
  UPSTREAM of any physical framework: the count structure constrains kappa,
  not pi's number theory, and nothing in the action reaches pi's deeper
  arithmetic.  But the framework never NEEDED pi's irrationality, and in
  its canonical form the framework is pi-FREE:

      a0 = (c/2) sqrt(G rho_Lambda)      -- no pi anywhere;

  pi enters only through the density CONVENTIONS of the rivals (the 2 pi
  horizon form, the sqrt(pi) Jeans form, the sqrt(8 pi/3) half-Z form).
  And every one of those rivals dies by a DECADE argument -- its required
  channel count n = sqrt(k pi) is O(1) and lands strictly between
  consecutive integers, using pi-bounds coarser than Archimedes:

      3.14 < pi < 3.15   kills all three:
        2 pi form:   n = sqrt(3 pi/2) = 2.170  in (2, 3)   -- no integer
        Jeans form:  n = sqrt(pi)      = 1.772  in (1, 2)   -- no integer
        half-Z form: n = sqrt(8 pi/3)  = 2.894  in (2, 3)   -- no integer

  CERTIFIED HERE, from the bounds ALONE (irrational_pi NOT used):
    T1: no natural count for the 2 pi form        (3 < pi < 4 kills it)
    T2: no natural count for the Jeans form       (3 < pi < 4 kills it)
    T3: no natural count for the half-Z form      (pi < 3.15 kills it)
    T4: the inversion, certified: a natural count for the horizon form
        would FORCE pi = 2 n^2 / 3 -- rational.  The framework's falsifier
        is also a probe of pi's arithmetic character: a confirmed off-1/2
        count would rationalize pi, which is exactly why the horizon form
        is dead.  (Corollary re-derives T1 WITH irrational_pi: the two
        routes connect.)

  So: the framework cannot prove pi irrational -- but it proves that any
  rival needing pi to be something special is dead, and it proves it with
  arithmetic coarser than Archimedes.  That is the useful direction.
-/

import Mathlib

open Real

/-- **T1** -- the 2 pi horizon form's channel count `n = sqrt(3 pi/2)` is
not a natural number.  From `3 < pi < 4` alone: `n^2 = 3 pi/2` lies in
(4.5, 6), strictly between 2^2 and 3^2. -/
theorem two_pi_count_decade : ∀ n : ℕ, (n : ℝ) ≠ Real.sqrt (3 * Real.pi / 2) := by
  intro n hn
  have hsq : (n : ℝ)^2 = 3 * Real.pi / 2 := by
    rw [hn, pow_two, Real.mul_self_sqrt (by positivity)]
  rcases Nat.lt_or_ge n 3 with h3 | h3
  · have hn2n : (n : ℕ) ≤ 2 := by omega
    have hn2 : (n : ℝ) ≤ 2 := Nat.cast_le.mpr hn2n
    have h4 : (n : ℝ)^2 ≤ (2 : ℝ)^2 := pow_le_pow_left₀ (Nat.cast_nonneg n) hn2 2
    linarith [h4, hsq, Real.pi_gt_three]
  · have hge3n : (3 : ℕ) ≤ n := by omega
    have hge3 : (3 : ℝ) ≤ n := Nat.cast_le.mpr hge3n
    have h9 : (3 : ℝ)^2 ≤ (n : ℝ)^2 := pow_le_pow_left₀ (by norm_num : (0:ℝ) ≤ 3) hge3 2
    linarith [h9, hsq, Real.pi_lt_four]

/-- **T2** -- the Jeans form's channel count `n = sqrt(pi)` is not a natural
number: `n^2 = pi` lies in (3, 4), strictly between 1^2 and 2^2. -/
theorem jeans_count_decade : ∀ n : ℕ, (n : ℝ) ≠ Real.sqrt Real.pi := by
  intro n hn
  have hsq : (n : ℝ)^2 = Real.pi := by
    rw [hn, pow_two, Real.mul_self_sqrt (by positivity)]
  rcases Nat.lt_or_ge n 2 with h2 | h2
  · have hn1n : (n : ℕ) ≤ 1 := by omega
    have hn1 : (n : ℝ) ≤ 1 := le_trans (Nat.cast_le.mpr hn1n) (by norm_num)
    have h1 : (n : ℝ)^2 ≤ (1 : ℝ)^2 := pow_le_pow_left₀ (Nat.cast_nonneg n) hn1 2
    linarith [h1, hsq, Real.pi_gt_three]
  · have hge2n : (2 : ℕ) ≤ n := by omega
    have hge2 : (2 : ℝ) ≤ n := Nat.cast_le.mpr hge2n
    have h4 : (2 : ℝ)^2 ≤ (n : ℝ)^2 := pow_le_pow_left₀ (by norm_num : (0:ℝ) ≤ 2) hge2 2
    linarith [h4, hsq, Real.pi_lt_four]

/-- **T3** -- the half-Z form's channel count `n = sqrt(8 pi/3)` is not a
natural number: `n^2 = 8 pi/3` lies in (8, 8.4), strictly between 2^2 and
3^2 (using `pi < 3.15`). -/
theorem z_half_count_decade : ∀ n : ℕ, (n : ℝ) ≠ Real.sqrt (8 * Real.pi / 3) := by
  intro n hn
  have hsq : (n : ℝ)^2 = 8 * Real.pi / 3 := by
    rw [hn, pow_two, Real.mul_self_sqrt (by positivity)]
  rcases Nat.lt_or_ge n 3 with h3 | h3
  · have hn2n : (n : ℕ) ≤ 2 := by omega
    have hn2 : (n : ℝ) ≤ 2 := Nat.cast_le.mpr hn2n
    have h4 : (n : ℝ)^2 ≤ (2 : ℝ)^2 := pow_le_pow_left₀ (Nat.cast_nonneg n) hn2 2
    linarith [h4, hsq, Real.pi_gt_three]
  · have hge3n : (3 : ℕ) ≤ n := by omega
    have hge3 : (3 : ℝ) ≤ n := Nat.cast_le.mpr hge3n
    have h9 : (3 : ℝ)^2 ≤ (n : ℝ)^2 := pow_le_pow_left₀ (by norm_num : (0:ℝ) ≤ 3) hge3 2
    linarith [h9, hsq, Real.pi_lt_d2]

/-- **T4** -- THE INVERSION: if the horizon form's channel count were a
natural number, pi would be FORCED into the quadratic `pi = 2 n^2/3` --
rational.  The framework's falsifier is therefore also a probe of pi's
arithmetic character: a confirmed off-1/2 count would rationalize pi.
Corollary (with `irrational_pi`): no such count exists. -/
theorem horizon_count_would_rationalize_pi (n : ℕ)
    (h : (n : ℝ)^2 = 3 * Real.pi / 2) : ∃ q : ℚ, Real.pi = q :=
  ⟨(2 * (n : ℚ)^2) / 3, by
    rw [Rat.cast_div, Rat.cast_mul, Rat.cast_pow, Rat.cast_natCast]
    linarith [h, Real.pi_pos]⟩

/-- **T4'** -- the corollary that connects the routes: with pi's
irrationality, the inversion closes back on the horizon form. -/
theorem horizon_count_impossible (n : ℕ)
    (h : (n : ℝ)^2 = 3 * Real.pi / 2) : False :=
  irrational_pi (Set.mem_range.mpr ⟨(2 * (n : ℚ)^2) / 3, by
      rw [Rat.cast_div, Rat.cast_mul, Rat.cast_pow, Rat.cast_natCast]
      linarith [h, Real.pi_pos]⟩)

/-- **THE STATEMENT**: the three pi-bearing rival counts are not natural
numbers -- certified from rational bounds on pi coarser than Archimedes
(`3.14 < pi < 3.15` suffices for all three), with `irrational_pi` needed
nowhere. -/
theorem pi_bearing_rivals_not_counts :
    (∀ n : ℕ, (n : ℝ) ≠ Real.sqrt (3 * Real.pi / 2))
    ∧ (∀ n : ℕ, (n : ℝ) ≠ Real.sqrt Real.pi)
    ∧ (∀ n : ℕ, (n : ℝ) ≠ Real.sqrt (8 * Real.pi / 3)) :=
  ⟨two_pi_count_decade, jeans_count_decade, z_half_count_decade⟩
