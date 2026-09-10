import Mathlib.Data.Real.Basic
import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring

/-! First-principles algebra for the exact exponential spherical bridge. -/

namespace ExactExponentialBridge

theorem exact_spherical_bridge
    (a0 x s g gN : ℝ)
    (ha0 : a0 ≠ 0)
    (hg : g = a0 * x)
    (hgn : gN = a0 * s)
    (hs : s = x * (1 - Real.exp (-x))) :
    (1 - Real.exp (-g / a0)) * g = gN := by
  rw [hg, hgn]
  have hratio_neg : -(a0 * x) / a0 = -x := by
    field_simp [ha0]
  rw [hratio_neg, hs]
  ring

theorem exponential_slope_pos
    (x : ℝ) (hx : 0 < x) :
    0 < 1 + (x - 1) * Real.exp (-x) := by
  by_cases h : 1 ≤ x
  · have hx1 : 0 ≤ x - 1 := by linarith
    have he : 0 < Real.exp (-x) := Real.exp_pos _
    have hmul : 0 ≤ (x - 1) * Real.exp (-x) :=
      mul_nonneg hx1 (le_of_lt he)
    linarith
  · have hx1 : x < 1 := lt_of_not_ge h
    have hneg : -x < 0 := by linarith
    have hleft : 1 - x < 1 := by linarith
    have hleft_pos : 0 < 1 - x := by linarith
    have hright : Real.exp (-x) < 1 := Real.exp_lt_one_iff.mpr hneg
    have hmul : (1 - x) * Real.exp (-x) < (1 - x) * 1 :=
      mul_lt_mul_of_pos_left hright hleft_pos
    have hprod : (1 - x) * Real.exp (-x) < 1 := by
      have hrightprod : (1 - x) * 1 < 1 := by simpa using hleft
      exact lt_trans hmul hrightprod
    have hrewrite :
        1 + (x - 1) * Real.exp (-x) =
          1 - (1 - x) * Real.exp (-x) := by ring
    rw [hrewrite]
    linarith

theorem deep_mond_btfr
    (G M a0 r v g : ℝ)
    (hr : r ≠ 0)
    (hforce : g ^ 2 = a0 * G * M / r ^ 2)
    (hcircular : v ^ 2 = r * g) :
    v ^ 4 = G * M * a0 := by
  have hforce' := hforce
  field_simp [hr] at hforce'
  calc
    v ^ 4 = (v ^ 2) ^ 2 := by ring
    _ = (r * g) ^ 2 := by rw [hcircular]
    _ = r ^ 2 * g ^ 2 := by ring
    _ = G * M * a0 := by
      calc
        r ^ 2 * g ^ 2 = g ^ 2 * r ^ 2 := by ring
        _ = a0 * G * M := hforce'
        _ = G * M * a0 := by ring

end ExactExponentialBridge
