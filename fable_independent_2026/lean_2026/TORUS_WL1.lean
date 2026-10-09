import Mathlib

/-!
# TORUS_WL1 -- one-parameter continuous Wilson lines (criteria TORUS_WL1_CRITERIA.md, bcbc4ea9a): KILL

Numeric (TORUS_WL1.py / .out): 108 solutions fit m_μ/m_e = 206.768 (families F1, F3, both τ); EVERY one has
m_τ = m_μ (heavy pair degenerate), Q = 0.468090.  F2 and F4 never reach m_μ/m_e.  The printed "chance
expectation" line is meaningless (all Q identical, spread → 0); the verdict rests on zero Koide-band hits.

CERTIFIED: `light_single_heavy_pair_never_koide`: a spectrum with one light state and a degenerate HEAVY pair,
√-masses (x, y, y) with 0 < x < y, can never satisfy Koide (Koide needs x² - 8xy - 2y² = 0, impossible for
x < y).  With TORUS_YUKAWA `koide_with_pair`, a degenerate pair is compatible with Koide only as a LIGHT pair
with the single state heavier by 4 + 3√2.  The torus families here produce the forbidden pattern.
-/

theorem light_single_heavy_pair_never_koide (x y : ℝ) (hx : 0 < x) (hxy : x < y) :
    (x ^ 2 + 2 * y ^ 2) / (x + 2 * y) ^ 2 ≠ 2 / 3 := by
  have hpos : (x + 2 * y) ^ 2 ≠ 0 := by nlinarith
  rw [Ne, div_eq_iff hpos]
  intro h
  nlinarith [mul_pos hx hx, mul_pos hx (lt_trans hx hxy)]

#print axioms light_single_heavy_pair_never_koide
