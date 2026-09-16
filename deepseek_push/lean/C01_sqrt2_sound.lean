import Mathlib

/-!
# C01 -- THE sqrt-2 IDENTITY: t_sound/t_dyn = v_flat/c_s = sqrt(2) (Lean certificate)

Source B05 (project_atomos/B05_dark_gas.py, 11/11 PASS; WAVEBOARD WAVE-30 B5):
the dark sector is an isothermal gas with EOS P = sigma^2 rho, sound speed
c_s = sigma; the isothermal circular velocity obeys v_flat^2 = 2 sigma^2
(G127 C2's c_s t_ff/r = 1/sqrt(2) < 1 is the same identity inverted).  The
response lag t_sound = r_M/c_s vs the dynamical time t_dyn = r_M/v_flat:

    t_sound/t_dyn = v_flat/c_s = sqrt(2) = 1.41421356 EXACTLY.

THEOREMS IN THIS FILE (the G03G/G227 sqrt_pair technique: square both sides,
resolve the sign with positivity, no rpow):

  1. sound_flat_sq     : the field-level identity: from a^2 = b^2/2 (a, b > 0),
                         b^2 = 2 a^2.
  2. sqrt2_ratio       : THE ALGEBRA LEMMA: a^2 = b^2/2 with a > 0, b > 0
                         gives  b/a = Real.sqrt 2.
  3. response_lag_sqrt2: THE CROSSING-TIME COROLLARY: with t_sound := r_M/a,
                         t_dyn := r_M/b and a^2 = b^2/2 (b > 0, a > 0),
                         t_sound/t_dyn = sqrt(2); the radius r_M cancels.
  4. response_lag_defs : the same corollary with the physics definitions
                         in-line: v_flat := sqrt(2)*sigma,
                         t_sound := r_M/sigma, t_dyn := r_M/v_flat.
  5. cs2_over_flat     : the G127 C2 form inverted: c_s/v_flat = 1/sqrt(2).
  6. cs_tff_over_r     : the G127 C2 exact statement: c_s t_ff/r = 1/sqrt(2),
                         t_ff := r/v_flat.
  7. numeric_cross_check : 119.21/(119.21/sqrt(2)) = sqrt(2) EXACTLY (the
                         119.21 km/s anchor cancels; any nonzero radius works).
  8. sqrt2_decimal_interval : sqrt(2) in (1.41421356, 1.41421357), by squaring
                         (sq_lt_sq₀) -- no calculus.
  9. numeric_cross_check_interval : the literal numeric cross-check:
                         1.41421356 < 119.21/(119.21/sqrt(2)) < 1.41421357.
  S. c01_spine         : the two required statements together.

Zero sorry.  Axioms: {propext, Classical.choice, Quot.sound} only.
-/

-- ============================================================
-- 1. THE FIELD-LEVEL IDENTITY: b^2 = 2 a^2  from  a^2 = b^2/2
-- ============================================================
theorem sound_flat_sq (a b : ℝ) (h : a ^ 2 = b ^ 2 / 2) : b ^ 2 = 2 * a ^ 2 := by
  rw [h]
  field_simp [(by norm_num : (2 : ℝ) ≠ 0)]

-- ============================================================
-- 2. THE ALGEBRA LEMMA: a^2 = b^2/2, a > 0, b > 0  ==>  b/a = sqrt 2
-- ============================================================
theorem sqrt2_ratio (a b : ℝ) (ha : 0 < a) (hb : 0 < b) (h : a ^ 2 = b ^ 2 / 2) :
    b / a = Real.sqrt 2 := by
  have ha0 : a ≠ 0 := by positivity
  have ha2 : a ^ 2 ≠ 0 := by positivity
  have h2 : b ^ 2 = 2 * a ^ 2 := sound_flat_sq a b h
  -- square both sides:  (b/a)^2 = (sqrt 2)^2
  have hs : (b / a) ^ 2 = (Real.sqrt 2) ^ 2 := by
    rw [Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 2)]
    calc (b / a) ^ 2 = b ^ 2 / a ^ 2 := by rw [div_pow]
      _ = 2 := by
        rw [h2]
        field_simp [ha2]
  -- resolve the sign by positivity (b/a > 0, sqrt 2 > 0)
  have hnonneg : 0 ≤ b / a := by positivity
  have hor : b / a = Real.sqrt 2 ∨ b / a = -(Real.sqrt 2) :=
    eq_or_eq_neg_of_sq_eq_sq _ _ hs
  rcases hor with r | r
  · exact r
  · have hpos : 0 < b / a := by positivity
    have hn : -(Real.sqrt 2) < 0 := by
      have hs2 : 0 < Real.sqrt 2 := Real.sqrt_pos.2 (by norm_num : (0 : ℝ) < 2)
      linarith
    linarith

-- ============================================================
-- 3. THE CROSSING-TIME COROLLARY: t_sound/t_dyn = sqrt 2, r_M cancels
-- ============================================================
theorem response_lag_sqrt2 (rM a b : ℝ) (hrM : rM ≠ 0) (ha : 0 < a) (hb : 0 < b)
    (h : a ^ 2 = b ^ 2 / 2) :
    (rM / a) / (rM / b) = Real.sqrt 2 := by
  calc (rM / a) / (rM / b) = b / a := by field_simp [hrM, ha.ne', hb.ne']
    _ = Real.sqrt 2 := sqrt2_ratio a b ha hb h

-- ============================================================
-- 4. THE SAME COROLLARY WITH THE PHYSICS DEFINITIONS IN-LINE
--    v_flat := sqrt(2) sigma, t_sound := r_M/sigma, t_dyn := r_M/v_flat
-- ============================================================
theorem response_lag_defs (rM sigma : ℝ) (hrM : rM ≠ 0) (hsig : 0 < sigma) :
    let v_flat := Real.sqrt 2 * sigma
    let t_sound := rM / sigma
    let t_dyn := rM / v_flat
    t_sound / t_dyn = Real.sqrt 2 := by
  intro v_flat t_sound t_dyn
  dsimp [t_dyn, t_sound, v_flat]
  have hs2 : Real.sqrt 2 ≠ 0 := by positivity
  field_simp [hrM, hsig.ne', hs2]

-- ============================================================
-- 5. THE G127 C2 FORM INVERTED: c_s/v_flat = 1/sqrt(2)
-- ============================================================
theorem cs2_over_flat (a : ℝ) (ha : 0 < a) :
    a / (Real.sqrt 2 * a) = 1 / Real.sqrt 2 := by
  have hs2 : Real.sqrt 2 ≠ 0 := by positivity
  field_simp [ha.ne', hs2]

-- ============================================================
-- 6. THE G127 C2 EXACT STATEMENT: c_s t_ff/r = 1/sqrt(2), t_ff := r/v_flat
-- ============================================================
theorem cs_tff_over_r (a r : ℝ) (ha : 0 < a) (hr : r ≠ 0) :
    a * (r / (Real.sqrt 2 * a)) / r = 1 / Real.sqrt 2 := by
  have hs2 : Real.sqrt 2 ≠ 0 := by positivity
  field_simp [hr, ha.ne', hs2]

-- ============================================================
-- 7. THE NUMERIC CROSS-CHECK, EXACT FORM: 119.21/(119.21/sqrt 2) = sqrt 2
--    (the anchor 119.21 km/s cancels -- it is any nonzero radius)
-- ============================================================
theorem numeric_cross_check :
    (119.21 : ℝ) / ((119.21 : ℝ) / Real.sqrt 2) = Real.sqrt 2 := by
  have hA : (119.21 : ℝ) ≠ 0 := by norm_num
  have hs2 : Real.sqrt 2 ≠ 0 := by positivity
  field_simp [hA, hs2]

-- ============================================================
-- 8. THE DECIMAL PIN: sqrt(2) in (1.41421356, 1.41421357), by squaring
-- ============================================================
theorem sqrt2_decimal_interval :
    (1.41421356 : ℝ) < Real.sqrt 2 ∧ Real.sqrt 2 < (1.41421357 : ℝ) := by
  have hlo : (1.41421356 : ℝ) < Real.sqrt 2 := by
    exact (sq_lt_sq₀ (by norm_num : (0 : ℝ) ≤ (1.41421356 : ℝ))
        (by positivity : (0 : ℝ) ≤ Real.sqrt 2)).1
      (by
        rw [Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 2)]
        norm_num)
  have hhi : Real.sqrt 2 < (1.41421357 : ℝ) := by
    exact (sq_lt_sq₀ (by positivity : (0 : ℝ) ≤ Real.sqrt 2)
        (by norm_num : (0 : ℝ) ≤ (1.41421357 : ℝ))).1
      (by
        rw [Real.sq_sqrt (by norm_num : (0 : ℝ) ≤ 2)]
        norm_num)
  exact ⟨hlo, hhi⟩

-- ============================================================
-- 9. THE LITERAL NUMERIC CROSS-CHECK:
--    1.41421356 < 119.21/(119.21/sqrt 2) < 1.41421357
-- ============================================================
theorem numeric_cross_check_interval :
    (1.41421356 : ℝ) < (119.21 : ℝ) / ((119.21 : ℝ) / Real.sqrt 2) ∧
    (119.21 : ℝ) / ((119.21 : ℝ) / Real.sqrt 2) < (1.41421357 : ℝ) := by
  rw [numeric_cross_check]
  exact sqrt2_decimal_interval

-- ============================================================
-- S. THE SPINE: the two required statements, closed form
-- ============================================================
theorem c01_spine :
    (∀ a b : ℝ, 0 < a → 0 < b → a ^ 2 = b ^ 2 / 2 → b / a = Real.sqrt 2) ∧
    (∀ rM a b : ℝ, rM ≠ 0 → 0 < a → 0 < b → a ^ 2 = b ^ 2 / 2 →
      (rM / a) / (rM / b) = Real.sqrt 2) := by
  constructor
  · intro a b ha hb h
    exact sqrt2_ratio a b ha hb h
  · intro rM a b hrM ha hb h
    exact response_lag_sqrt2 rM a b hrM ha hb h

#print axioms sound_flat_sq
#print axioms sqrt2_ratio
#print axioms response_lag_sqrt2
#print axioms response_lag_defs
#print axioms cs2_over_flat
#print axioms cs_tff_over_r
#print axioms numeric_cross_check
#print axioms sqrt2_decimal_interval
#print axioms numeric_cross_check_interval
#print axioms c01_spine