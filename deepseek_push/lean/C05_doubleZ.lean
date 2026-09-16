import Mathlib

/-!
# C05-DOUBLEZ -- THE DOUBLE-Z EXPONENT IN THE MASS LADDER (A08 certified)

A08 (`project_atomos/A08_double_Z.py` + `A08_results.json`) establishes the
double appearance of the pure coefficient Z = 2 sqrt(8 pi/3) = 5.7888:

    a0      = c^2 / (Z R_dS)                       -- the horizon form (Z11)
    sigma^2 = (1/2) sqrt(G M_b a0)                 -- the ladder's velocity square
    m       = k_B T_0 (1+z*) / sigma^2             -- the mass ladder

and the closed form (T := T_0(1+z*), the committed temperature rung):

    m = (2 k_B T / c) * Z^(+1/2) * R_dS^(+1/2) * G^(-1/2) * M_b^(-1/2)

i.e. m carries the Z-dependence Z^(+1/2) EXACTLY -- sigma^2 carries Z^(-1/2)
through a0, and m = k_B T / sigma^2 inverts the sign.  This file certifies
that field-level exponent flip and its scaling corollary:

  1. exponent_flip     1/(k x^(-1/2)) = x^(+1/2)/k  for x > 0 (the
                       reciprocal-square-root algebra; x^(-1/2) is rendered
                       as 1/sqrt(x), x^(+1/2) as sqrt(x) -- no rpow).
  2. sqrt_recip        sqrt(1/y) = 1/sqrt(y) for y > 0 (the same flip on
                       the square root itself).
  3. sqrt_mul_pos      sqrt(A*B) = sqrt(A)*sqrt(B) for 0 < A, 0 < B (the
                       two-factor product, by squaring both sides).
  4. ladder_sqrt_pair  sqrt(G M_b c^2/(Z R_dS)) * sqrt(Z R_dS/(G M_b)) = c
                       -- the single sqrt product that carries the whole flip.
  5. ladder_closed_form  m = k_B T/sigma^2 equals the closed form
                       (2 k_B T/c) sqrt(Z R_dS/(G M_b)) for
                       sigma^2 = (1/2) sqrt(G M_b c^2/(Z R_dS)).
  6. z_exponent        sqrt(Z R_dS/(G M_b)) = sqrt(Z) * sqrt(R_dS/(G M_b))
                       -- the Z^(+1/2) factor separates exactly.
  7. z_dependence_of_m m itself, re-expressed with the Z^(+1/2) explicit:
                       m = (2 k_B T/c) * sqrt(Z) * sqrt(R_dS/(G M_b)).
  8. double_z_scaling  the corollary m(2Z)/m(Z) = sqrt(2) EXACTLY, with m(2Z)
                       the same ladder at the doubled horizon coefficient
                       (a0 -> c^2/((2Z) R_dS)).  Numeric anchor from A08:
                       1.4142135624 vs sqrt(2) to 1e-9.
  9. z_squared_exact   Z^2 = 32 pi/3 exactly for Z := 2 sqrt(8 pi/3).
 10. sqrt_z_sqrt_form  sqrt(Z) = sqrt(sqrt(32 pi/3)) exactly -- the
                       (32 pi/3)^(1/4) content in sqrt-of-sqrt form (A08's
                       "sqrt(Z) = (32 pi/3)^(1/4)").

SCOPE (what this certificate does and does not claim): Lean certifies the
ALGEBRA above -- that the ladder formula, granted the premises sigma^2 =
(1/2) sqrt(G M_b a0) and a0 = c^2/(Z R_dS), is exactly the closed form and
scales as Z^(+1/2).  It does NOT certify the physics-law reading: that the
ladder is the framework's mass germ, that Z = 2 sqrt(8 pi/3) is the
framework's coefficient, or the decimal numerics (5.09 keV band, 30.6-sigma
sensitivity, 1.7e-16 machine agreement) -- those live in the A08 Python lane
(`project_atomos/A08_double_Z.py`, 8/8 PASS).  All variables are abstract
positive reals at battlefield strength: no units, no constants' values.

Zero sorry.  Axioms expected: {propext, Classical.choice, Quot.sound}.
-/

noncomputable section

-- ============================================================
-- 1. THE EXPONENT FLIP: 1/(k x^(-1/2)) = x^(+1/2)/k for x > 0
--    (x^(-1/2) := 1/sqrt(x); x^(+1/2) := sqrt(x))
-- ============================================================
theorem exponent_flip (x k : ℝ) (hx : 0 < x) (hk : k ≠ 0) :
    1 / (k * (1 / Real.sqrt x)) = Real.sqrt x / k := by
  have hsq : Real.sqrt x ≠ 0 := by
    exact (Real.sqrt_pos.mpr hx).ne'
  field_simp [hsq, hk]

-- ============================================================
-- 2. THE SQUARE-ROOT RECIPROCAL: sqrt(1/y) = 1/sqrt(y) for y > 0
--    (the exponent flip at the sqrt level: (y^(-1))^(+1/2) = y^(-1/2))
-- ============================================================
theorem sqrt_recip (y : ℝ) (hy : 0 < y) :
    Real.sqrt (1 / y) = 1 / Real.sqrt y := by
  have hyy : 0 ≤ y := le_of_lt hy
  have h1y : 0 ≤ 1 / y := by positivity
  have hsq : (Real.sqrt (1 / y)) ^ 2 = (1 / Real.sqrt y) ^ 2 := by
    rw [Real.sq_sqrt h1y]
    rw [div_pow]
    rw [Real.sq_sqrt hyy]
    norm_num
  have hnonneg1 : 0 ≤ Real.sqrt (1 / y) := by positivity
  have hnonneg2 : 0 ≤ 1 / Real.sqrt y := by positivity
  have hr0 : (1 / Real.sqrt y : ℝ) ≠ 0 := by
    exact div_ne_zero (by norm_num : (1 : ℝ) ≠ 0) (Real.sqrt_pos.mpr hy).ne'
  have hor : Real.sqrt (1 / y) = 1 / Real.sqrt y
      ∨ Real.sqrt (1 / y) = -(1 / Real.sqrt y) :=
    eq_or_eq_neg_of_sq_eq_sq _ _ hsq
  rcases hor with h | h
  · exact h
  · nlinarith

-- ============================================================
-- 3. THE TWO-FACTOR PRODUCT: sqrt(A*B) = sqrt(A) sqrt(B), 0 < A, 0 < B
--    (square both sides, resolve the sign with nonnegativity -- no rpow)
-- ============================================================
theorem sqrt_mul_pos (A B : ℝ) (hA : 0 < A) (hB : 0 < B) :
    Real.sqrt (A * B) = Real.sqrt A * Real.sqrt B := by
  have hAnn : 0 ≤ A := le_of_lt hA
  have hBnn : 0 ≤ B := le_of_lt hB
  have hABnn : 0 ≤ A * B := by positivity
  have hsq : (Real.sqrt (A * B)) ^ 2 = (Real.sqrt A * Real.sqrt B) ^ 2 := by
    rw [Real.sq_sqrt hABnn]
    rw [mul_pow]
    rw [Real.sq_sqrt hAnn]
    rw [Real.sq_sqrt hBnn]
  have hnonneg1 : 0 ≤ Real.sqrt (A * B) := by positivity
  have hnonneg2 : 0 ≤ Real.sqrt A * Real.sqrt B := by positivity
  have hsqrtA : 0 < Real.sqrt A := Real.sqrt_pos.mpr hA
  have hsqrtB : 0 < Real.sqrt B := Real.sqrt_pos.mpr hB
  have hor : Real.sqrt (A * B) = Real.sqrt A * Real.sqrt B
      ∨ Real.sqrt (A * B) = -(Real.sqrt A * Real.sqrt B) :=
    eq_or_eq_neg_of_sq_eq_sq _ _ hsq
  rcases hor with h | h
  · exact h
  · nlinarith

-- ============================================================
-- 4. THE LADDER SQRT-PAIR: sqrt(G M_b c^2/(Z R_dS)) * sqrt(Z R_dS/(G M_b)) = c
--    (sigma^2 = (1/2) sqrt(G M_b a0) with a0 = c^2/(Z R_dS): the two-factor
--     product of the ladder's inverse scales to c -- the whole flip in one line)
-- ============================================================
theorem ladder_sqrt_pair (G Mb c Z RdS : ℝ) (hG : 0 < G) (hMb : 0 < Mb) (hc : 0 < c)
    (hZ : 0 < Z) (hRdS : 0 < RdS) :
    Real.sqrt (G * Mb * c ^ 2 / (Z * RdS)) * Real.sqrt (Z * RdS / (G * Mb)) = c := by
  have hXnn : 0 ≤ G * Mb * c ^ 2 / (Z * RdS) := by positivity
  have hYnn : 0 ≤ Z * RdS / (G * Mb) := by positivity
  have hsq : (Real.sqrt (G * Mb * c ^ 2 / (Z * RdS)) * Real.sqrt (Z * RdS / (G * Mb))) ^ 2 = c ^ 2 := by
    rw [mul_pow]
    rw [Real.sq_sqrt hXnn]
    rw [Real.sq_sqrt hYnn]
    field_simp [hG.ne', hMb.ne', hZ.ne', hRdS.ne', hc.ne']
  have hnonneg : 0 ≤ Real.sqrt (G * Mb * c ^ 2 / (Z * RdS)) * Real.sqrt (Z * RdS / (G * Mb)) := by positivity
  have hcpos : 0 ≤ c := le_of_lt hc
  have hor : Real.sqrt (G * Mb * c ^ 2 / (Z * RdS)) * Real.sqrt (Z * RdS / (G * Mb)) = c
      ∨ Real.sqrt (G * Mb * c ^ 2 / (Z * RdS)) * Real.sqrt (Z * RdS / (G * Mb)) = -c :=
    eq_or_eq_neg_of_sq_eq_sq _ _ hsq
  rcases hor with h | h
  · exact h
  · nlinarith

-- ============================================================
-- 5. THE LADDER CLOSED FORM: m = k_B T / sigma^2  with
--    sigma^2 = (1/2) sqrt(G M_b c^2/(Z R_dS))  equals
--    m = (2 k_B T / c) sqrt(Z R_dS / (G M_b))   (A08's closed form, exact)
-- ============================================================
theorem ladder_closed_form (kB T G Mb c Z RdS : ℝ) (hkB : 0 < kB) (hT : 0 < T)
    (hG : 0 < G) (hMb : 0 < Mb) (hc : 0 < c) (hZ : 0 < Z) (hRdS : 0 < RdS) :
    kB * T / ((1 / 2 : ℝ) * Real.sqrt (G * Mb * c ^ 2 / (Z * RdS))) =
      (2 * kB * T / c) * Real.sqrt (Z * RdS / (G * Mb)) := by
  have hXpos : 0 < G * Mb * c ^ 2 / (Z * RdS) := by positivity
  have hXsq : Real.sqrt (G * Mb * c ^ 2 / (Z * RdS)) ≠ 0 := by
    exact (Real.sqrt_pos.mpr hXpos).ne'
  have hp := ladder_sqrt_pair G Mb c Z RdS hG hMb hc hZ hRdS
  field_simp [hXsq, hc.ne', hkB.ne', hT.ne']
  nlinarith [hp]

-- ============================================================
-- 6. THE Z-EXPONENT SEPARATION: sqrt(Z R_dS/(G M_b)) = sqrt(Z) sqrt(R_dS/(G M_b))
--    (the Z^(+1/2) factor of m, extracted exactly)
-- ============================================================
theorem z_exponent (Z G Mb RdS : ℝ) (hZ : 0 < Z) (hG : 0 < G) (hMb : 0 < Mb)
    (hRdS : 0 < RdS) :
    Real.sqrt (Z * RdS / (G * Mb)) = Real.sqrt Z * Real.sqrt (RdS / (G * Mb)) := by
  have hBpos : 0 < RdS / (G * Mb) := by positivity
  have hm := sqrt_mul_pos Z (RdS / (G * Mb)) hZ hBpos
  rw [← hm]
  congr; ring

-- ============================================================
-- 7. THE Z-DEPENDENCE OF m, EXPLICIT: m = (2 k_B T/c) sqrt(Z) sqrt(R_dS/(G M_b))
--    (m carries Z^(+1/2) exactly -- A08's "m = [Z-independent prefactor] Z^(+1/2)")
-- ============================================================
theorem z_dependence_of_m (kB T G Mb c Z RdS : ℝ) (hkB : 0 < kB) (hT : 0 < T)
    (hG : 0 < G) (hMb : 0 < Mb) (hc : 0 < c) (hZ : 0 < Z) (hRdS : 0 < RdS) :
    kB * T / ((1 / 2 : ℝ) * Real.sqrt (G * Mb * c ^ 2 / (Z * RdS))) =
      (2 * kB * T / c) * Real.sqrt Z * Real.sqrt (RdS / (G * Mb)) := by
  have hm : kB * T / ((1 / 2 : ℝ) * Real.sqrt (G * Mb * c ^ 2 / (Z * RdS))) =
      (2 * kB * T / c) * Real.sqrt (Z * RdS / (G * Mb)) :=
    ladder_closed_form kB T G Mb c Z RdS hkB hT hG hMb hc hZ hRdS
  calc
    kB * T / ((1 / 2 : ℝ) * Real.sqrt (G * Mb * c ^ 2 / (Z * RdS)))
        = (2 * kB * T / c) * Real.sqrt (Z * RdS / (G * Mb)) := hm
    _ = (2 * kB * T / c) * (Real.sqrt Z * Real.sqrt (RdS / (G * Mb))) := by
        rw [z_exponent Z G Mb RdS hZ hG hMb hRdS]
    _ = (2 * kB * T / c) * Real.sqrt Z * Real.sqrt (RdS / (G * Mb)) := by ring

-- ============================================================
-- 8. THE SCALING COROLLARY: m(2Z)/m(Z) = sqrt(2) EXACTLY
--    (m(2Z) = the same ladder at the doubled horizon coefficient,
--     a0 := c^2/((2Z) R_dS); numeric anchor A08: 1.4142135624)
-- ============================================================
theorem double_z_scaling (kB T G Mb c Z RdS : ℝ) (hkB : 0 < kB) (hT : 0 < T)
    (hG : 0 < G) (hMb : 0 < Mb) (hc : 0 < c) (hZ : 0 < Z) (hRdS : 0 < RdS) :
    let mZ := kB * T / ((1 / 2 : ℝ) * Real.sqrt (G * Mb * c ^ 2 / (Z * RdS)))
    let m2Z := kB * T / ((1 / 2 : ℝ) * Real.sqrt (G * Mb * c ^ 2 / ((2 * Z) * RdS)))
    m2Z / mZ = Real.sqrt 2 := by
  intro mZ m2Z
  dsimp [mZ, m2Z]
  have hmZ : kB * T / ((1 / 2 : ℝ) * Real.sqrt (G * Mb * c ^ 2 / (Z * RdS))) =
      (2 * kB * T / c) * Real.sqrt (Z * RdS / (G * Mb)) :=
    ladder_closed_form kB T G Mb c Z RdS hkB hT hG hMb hc hZ hRdS
  have hm2Z : kB * T / ((1 / 2 : ℝ) * Real.sqrt (G * Mb * c ^ 2 / ((2 * Z) * RdS))) =
      (2 * kB * T / c) * Real.sqrt ((2 * Z) * RdS / (G * Mb)) :=
    ladder_closed_form kB T G Mb c (2 * Z) RdS hkB hT hG hMb hc (by positivity : 0 < (2 : ℝ) * Z) hRdS
  rw [hm2Z, hmZ]
  have hBpos : 0 < Z * RdS / (G * Mb) := by positivity
  have h2pos : 0 < (2 : ℝ) := by norm_num
  have hfold : Real.sqrt ((2 * Z) * RdS / (G * Mb)) = Real.sqrt ((2 : ℝ) * (Z * RdS / (G * Mb))) := by
    congr; ring
  have hprod : Real.sqrt ((2 : ℝ) * (Z * RdS / (G * Mb))) = Real.sqrt (2 : ℝ) * Real.sqrt (Z * RdS / (G * Mb)) :=
    sqrt_mul_pos (2 : ℝ) (Z * RdS / (G * Mb)) h2pos hBpos
  have hB' : Real.sqrt ((2 * Z) * RdS / (G * Mb)) = Real.sqrt (2 : ℝ) * Real.sqrt (Z * RdS / (G * Mb)) := by
    rw [hfold, hprod]
  rw [hB']
  have hfs : (2 * kB * T / c : ℝ) ≠ 0 := by positivity
  have hBsq : Real.sqrt (Z * RdS / (G * Mb)) ≠ 0 := (Real.sqrt_pos.mpr hBpos).ne'
  field_simp [hfs, hBsq, hc.ne']

-- ============================================================
-- 9. Z-SQUARED: (2 sqrt(8 pi/3))^2 = 32 pi/3 EXACTLY
--    (the A08 re-expression Z = sqrt(32 pi/3), Z > 0, at the squared level)
-- ============================================================
theorem z_squared_exact :
    (2 * Real.sqrt (8 * Real.pi / 3)) ^ 2 = 32 * Real.pi / 3 := by
  rw [mul_pow]
  rw [Real.sq_sqrt (by positivity : 0 ≤ 8 * Real.pi / 3)]
  norm_num
  ring

-- ============================================================
-- 10. sqrt(Z) = sqrt(sqrt(32 pi/3)) EXACTLY -- A08's "sqrt(Z) = (32 pi/3)^(1/4)"
--     in sqrt-of-sqrt form (the 1/4 power rendered without rpow)
-- ============================================================
theorem sqrt_z_sqrt_form :
    Real.sqrt (2 * Real.sqrt (8 * Real.pi / 3)) = Real.sqrt (Real.sqrt (32 * Real.pi / 3)) := by
  have hZsq : (2 * Real.sqrt (8 * Real.pi / 3)) ^ 2 = (Real.sqrt (32 * Real.pi / 3)) ^ 2 := by
    rw [mul_pow]
    rw [Real.sq_sqrt (by positivity : 0 ≤ 8 * Real.pi / 3)]
    rw [Real.sq_sqrt (by positivity : 0 ≤ 32 * Real.pi / 3)]
    norm_num
    ring
  have hZpos : 0 ≤ 2 * Real.sqrt (8 * Real.pi / 3) := by positivity
  have hSpos : 0 < Real.sqrt (32 * Real.pi / 3) := Real.sqrt_pos.mpr (by positivity : 0 < 32 * Real.pi / 3)
  have hZ : 2 * Real.sqrt (8 * Real.pi / 3) = Real.sqrt (32 * Real.pi / 3) := by
    have hor : 2 * Real.sqrt (8 * Real.pi / 3) = Real.sqrt (32 * Real.pi / 3)
        ∨ 2 * Real.sqrt (8 * Real.pi / 3) = -Real.sqrt (32 * Real.pi / 3) :=
      eq_or_eq_neg_of_sq_eq_sq _ _ hZsq
    rcases hor with h | h
    · exact h
    · nlinarith
  rw [hZ]

end

#print axioms exponent_flip
#print axioms sqrt_recip
#print axioms sqrt_mul_pos
#print axioms ladder_sqrt_pair
#print axioms ladder_closed_form
#print axioms z_exponent
#print axioms z_dependence_of_m
#print axioms double_z_scaling
#print axioms z_squared_exact
#print axioms sqrt_z_sqrt_form