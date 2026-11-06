import Mathlib.Tactic

/-!
# QX19 (2026-11-06): algebraic carries of the one-action scorecard (AC2q + Pi^6 blend)

Lane closure_2026_11_06/QX19_one_action_scorecard (criteria d65980ffcd). Numbers come from qx19.py; certified here
are the algebraic steps the carries rest on.

1. `hi_branch`: above the layer (Σ ≥ b > 0) the blended stiffness b²·f(Σ/b), with f(q) = q²/2, equals Σ²/2.
2. `hi_indep`: there it is the same for any two scales b₁, b₂ ≤ Σ (independent of b).
3. `frw_point`: on FRW, Σ = 2X with b = X > 0, so q = Σ/b = 2 ≥ 1.
4. `frw_pert`: a perturbation d of the charge with d ≥ -X keeps q = (2X + d)/X ≥ 1 (the exact region).
5. `power_ok`: the blend's near-zero power m = 6 satisfies m > d + 2 for d = 3.
6. `cassini_margin`: the C6P margin 4.8e7 times (1 - 2e-5) stays above 1.
-/

namespace QX19

theorem hi_branch {S b : ℝ} (hb : 0 < b) : b ^ 2 * ((S / b) ^ 2 / 2) = S ^ 2 / 2 := by
  field_simp

theorem hi_indep {S b1 b2 : ℝ} (h1 : 0 < b1) (h2 : 0 < b2) :
    b1 ^ 2 * ((S / b1) ^ 2 / 2) = b2 ^ 2 * ((S / b2) ^ 2 / 2) := by
  rw [hi_branch h1, hi_branch h2]

theorem frw_point {X : ℝ} (hX : 0 < X) : (2 * X) / X = 2 ∧ (1 : ℝ) ≤ (2 * X) / X := by
  have h : (2 * X) / X = 2 := by field_simp
  exact ⟨h, by rw [h]; norm_num⟩

theorem frw_pert {X d : ℝ} (hX : 0 < X) (hd : -X ≤ d) : (1 : ℝ) ≤ (2 * X + d) / X := by
  rw [le_div_iff₀ hX]; linarith

theorem power_ok : (3 : ℕ) + 2 < 6 := by norm_num

theorem cassini_margin : (1 : ℝ) < 4.8e7 * (1 - 2e-5) := by norm_num

end QX19

#print axioms QX19.hi_branch
#print axioms QX19.hi_indep
#print axioms QX19.frw_point
#print axioms QX19.frw_pert
#print axioms QX19.power_ok
#print axioms QX19.cassini_margin
