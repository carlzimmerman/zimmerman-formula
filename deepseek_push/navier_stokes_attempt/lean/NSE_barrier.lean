import Mathlib

/-!
# NSE barrier rungs (SPEC_A_LEAN.md, file 3): the invariant-set algebra

Certifies the algebraic rungs of the sup-barrier argument: the crossing-point
identity (`barrier_eq_at_crossing`), the pull-down slope above the barrier
(`barrier_pull_down`), and the stretch-vs-drag count
(`drag_beats_stretching_never`: a drag linear in the norm cannot dominate the
cubic stretching at every level — the canonical reason the two-constant drag
class cannot close 3D regularity, the N02 door).

Algebra only — physics scope as in N00_CAMPAIGN.md; zero `sorry`,
Mathlib 4.34.0-rc2.
-/

noncomputable section

open Real

/-!
### Blocker: `barrier_factor` is FALSE as stated (deleted, house rule)

SPEC_A's `barrier_factor (A c M m : ℝ) (hm2 : m ^ 2 = A / c) :
A - c * M ^ 2 = -c * (M - m) * (M + m)` cannot be certified: it is false as
stated.  Lean's real division is total (`(5 : ℝ) / 0 = 0`), so with
`A = 5, c = 0, m = 0` the hypothesis `0 ^ 2 = 5 / 0` holds while the conclusion
reads `5 - 0 = -0 * (M - 0) * (M + 0)`, i.e. `5 = 0`.  The intended identity
needs `c ≠ 0` (the SPEC's own recipe `rw [hm2]; field_simp` requires it), and
SPEC_A does not grant adding that hypothesis, so the theorem is deleted per
house rules and the disproof is certified below (`barrier_factor_false`).
The `c ≠ 0`-guarded version of the identity is carried inside
`barrier_pull_down` (which holds `hc : 0 < c`).
-/

/-- Disproof of the SPEC_A `barrier_factor` statement: the counterexample
`A = 5, c = 0, m = 0` satisfies `m^2 = A/c` but the conclusion would read
`5 = 0` (division by zero is total in Lean). -/
theorem barrier_factor_false :
    ¬ (∀ (A c M m : ℝ), m ^ 2 = A / c → A - c * M ^ 2 = -c * (M - m) * (M + m)) := by
  intro h
  have hc : (0 : ℝ) ^ 2 = (5 : ℝ) / 0 := by norm_num
  have hbad := h 5 0 0 0 hc
  norm_num at hbad

theorem barrier_eq_at_crossing (A c m : ℝ) (hc : c ≠ 0) (hm2 : m ^ 2 = A / c) :
    A - c * m ^ 2 = 0 := by
  rw [hm2]
  have hAc : c * (A / c) = A := mul_div_cancel₀ A hc
  rw [hAc]
  ring

theorem barrier_pull_down (A c M m : ℝ) (hc : 0 < c) (hm : 0 ≤ m) (hm2 : m ^ 2 = A / c)
    (hM : m ≤ M) :
    A - c * M ^ 2 ≤ -c * m * (M - m) := by
  have hA : A = c * m ^ 2 := by
    calc
      A = (A / c) * c := by rw [div_mul_cancel₀ _ (ne_of_gt hc)]
      _ = m ^ 2 * c := by rw [← hm2]
      _ = c * m ^ 2 := by ring
  rw [hA]
  have hMm : 0 ≤ M - m := by linarith
  have hneg : (-c) * (M - m) ≤ 0 := mul_nonpos_of_nonpos_of_nonneg (by linarith : -c ≤ 0) hMm
  have hM0 : 0 ≤ M := by linarith
  have htriple : (-c) * (M - m) * M ≤ 0 := mul_nonpos_of_nonpos_of_nonneg hneg hM0
  nlinarith [htriple]

theorem drag_beats_stretching_never (a C : ℝ) (ha : 0 < a) (hC : 0 < C) :
    ∃ ω : ℝ, Real.sqrt (a / C) < ω ∧ C * ω ^ 3 > a * ω := by
  refine ⟨1 + a / C, ?_, ?_⟩
  · have hpos : 0 < a / C := div_pos ha hC
    have hsq : (Real.sqrt (a / C)) ^ 2 < (1 + a / C) ^ 2 := by
      rw [Real.sq_sqrt (le_of_lt hpos)]
      nlinarith [sq_nonneg (a / C + (1 / 2 : ℝ))]
    have hs0 : 0 ≤ Real.sqrt (a / C) := Real.sqrt_nonneg _
    have hwpos : 0 < 1 + a / C := by linarith [hpos]
    have habs : |Real.sqrt (a / C)| < |1 + a / C| := sq_lt_sq.mp hsq
    simpa [abs_of_nonneg hs0, abs_of_nonneg hwpos.le] using habs
  · have hwpos : 0 < 1 + a / C := by positivity
    have hdiff : 0 < C * (1 + a / C) ^ 2 - a := by
      have hid : C * (1 + a / C) ^ 2 - a = (C ^ 3 + C ^ 2 * a + C * a ^ 2) / C ^ 2 := by
        field_simp [hC.ne']
        ring
      rw [hid]
      positivity
    have hprod : 0 < (C * (1 + a / C) ^ 2 - a) * (1 + a / C) := mul_pos hdiff hwpos
    nlinarith [hprod]

/-!
### Blocker: `barrier_decay` (not stated — SPEC_A option, extra cost guard)

Full ODE comparison (`E' ≤ -k·E ⇒ E(t) ≤ E(0)`, Gronwall class) is certified
in the N03 lane; algebraic rungs (1)-(4) are certified here.
-/

end

#print axioms barrier_factor_false
#print axioms barrier_eq_at_crossing
#print axioms barrier_pull_down
#print axioms drag_beats_stretching_never