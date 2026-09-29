import Mathlib

/-!
# M3E -- the turnaround-keyed conversion gate: FRW expansion, Zel'dovich axis rates, opening points,
#        the shock stand-off thresholds

Source: `real_research/derivation_chain_2026/FP25_constructive_dark_sector.py`, `partA()`
(lines 219-284: checks A1, A2, A3, A4).  No Zel'dovich / turnaround / opening-point statement is in the
Lean corpus (git grep for Zel, turnaround, opening, caustic-of-theta finds nothing relevant).

Model hypotheses (declared, not certified): the comoving flow on FRW has scale factor a with a' = H a;
the Zel'dovich map gives axis lengths l_i = a (1 - D lam_i) with growth D' = f H D (f = dlnD/dlna);
"n axes already collapsed" contribute 0 to theta and the remaining 2 - n axes expand at rate H each;
in an EdS collapse the gas axis obeys l/l_ta = 4 x (1 - x) after turnaround.

CERTIFIED:
  * `theta_FRW`       : (a^3)'/a^3 = 3H  (so theta = 3H > 0 for H > 0 and the gate Theta(-theta) is closed on FRW).
  * `axis_rate`       : l' / l = H (1 - f x/(1 - x)), x = D lam != 1, a != 0.
  * `axis_rate_expand`: 1 - f x/(1-x) = 1 - f x - f x^2/(1-x)  (linear limit 3 - f delta_L, exact remainder).
  * `opening_iff`     : for f > 0, n < 3, 0 <= x < 1:  1 - f x/(1-x) + (2-n) <= 0  <->  x >= (3-n)/(3-n+f),
                        with equality exactly at x*_n = (3-n)/(3-n+f) in (0,1)  (`opening_point_zero`, `opening_point_lt_one`).
  * `rate_strictAnti` : the rate is strictly decreasing on [0,1) for f > 0.
  * `rate_to_minus_infty` : for every bound B there is delta > 0 with rate < B on (1-delta, 1)  (caustic: -infinity).
  * `standoff_numbers`: with f = 1 and x*_n = (3-n)/(4-n):  4 x*_n (1 - x*_n) = 3/4, 8/9, 1 for n = 0, 1, 2.
  * `standoff_gate`   : for 1/2 <= x* < 1 and 0 < s <= 1, the collapsing-branch solution x_s = (1+sqrt(1-s))/2 of
                        4 x (1-x) = s satisfies x_s >= x* iff s <= 4 x* (1-x*)  (the gate opens before the gas axis
                        freezes iff s <= l/l_ta(x*); at equality theta = 0 counts as open).

NOT CERTIFIED: the Zel'dovich approximation itself, the EdS l/l_ta = 4x(1-x) law, the value 0.347 of the
self-similar stand-off, the Monte-Carlo web fractions, any consequence for the dark sector, S_8, the forest,
X-COP or Harvey (all data-facing gates in FP25 are outside this file).  No physical claim is an axiom.
-/

noncomputable section
namespace M3E

open Real Filter

/-! ### FRW -/

theorem theta_FRW (a : ℝ → ℝ) (H t : ℝ) (ha : HasDerivAt a (H * a t) t) (hne : a t ≠ 0) :
    HasDerivAt (fun s => a s ^ 3) (3 * H * a t ^ 3) t ∧ (3 * H * a t ^ 3) / a t ^ 3 = 3 * H := by
  constructor
  · have := ha.pow 3
    refine this.congr_deriv ?_
    simp; ring
  · field_simp

/-! ### axis rates -/

theorem axis_rate (a D : ℝ → ℝ) (H f lam t : ℝ)
    (ha : HasDerivAt a (H * a t) t) (hD : HasDerivAt D (f * H * D t) t)
    (hane : a t ≠ 0) (hx : D t * lam ≠ 1) :
    HasDerivAt (fun s => a s * (1 - D s * lam)) (H * a t * (1 - D t * lam) - a t * (f * H * (D t * lam))) t ∧
    (H * a t * (1 - D t * lam) - a t * (f * H * (D t * lam))) / (a t * (1 - D t * lam))
      = H * (1 - f * (D t * lam) / (1 - D t * lam)) := by
  have h1 : 1 - D t * lam ≠ 0 := fun h => hx (by linarith)
  constructor
  · have h2 := ha.mul ((hD.mul_const lam).const_sub 1)
    refine h2.congr_deriv ?_
    ring
  · field_simp

theorem axis_rate_expand (f x : ℝ) (hx : x ≠ 1) :
    1 - f * x / (1 - x) = 1 - f * x - f * x ^ 2 / (1 - x) := by
  have : 1 - x ≠ 0 := fun h => hx (by linarith)
  field_simp
  ring

/-- theta/H for three axes, split into the linear part and the exact remainder. -/
theorem theta_three_axes (f x1 x2 x3 : ℝ) (h1 : x1 ≠ 1) (h2 : x2 ≠ 1) (h3 : x3 ≠ 1) :
    (1 - f * x1 / (1 - x1)) + (1 - f * x2 / (1 - x2)) + (1 - f * x3 / (1 - x3))
      = 3 - f * (x1 + x2 + x3)
        - f * (x1 ^ 2 / (1 - x1) + x2 ^ 2 / (1 - x2) + x3 ^ 2 / (1 - x3)) := by
  have e1 := axis_rate_expand f x1 h1
  have e2 := axis_rate_expand f x2 h2
  have e3 := axis_rate_expand f x3 h3
  rw [e1, e2, e3]
  ring

/-! ### opening points -/

/-- theta/H when n axes are already collapsed (contribute 0), the collapsing axis has x, and the
rest (2 - n) expand at H. -/
def thetaRate (f n x : ℝ) : ℝ := 1 - f * x / (1 - x) + (2 - n)

theorem opening_iff (f n x : ℝ) (hf : 0 < f) (hn : n < 3) (_hx0 : 0 ≤ x) (hx1 : x < 1) :
    thetaRate f n x ≤ 0 ↔ (3 - n) / (3 - n + f) ≤ x := by
  have h1 : 0 < 1 - x := by linarith
  have h2 : 0 < 3 - n + f := by linarith
  unfold thetaRate
  rw [div_le_iff₀ h2]
  have : 1 - f * x / (1 - x) + (2 - n) = ((3 - n) * (1 - x) - f * x) / (1 - x) := by
    field_simp; ring
  rw [this, div_nonpos_iff]
  constructor
  · intro h
    rcases h with ⟨h, _⟩ | ⟨h, h'⟩
    · linarith
    · linarith
  · intro h
    right
    exact ⟨by nlinarith, h1.le⟩

theorem opening_point_zero (f n : ℝ) (hf : 0 < f) (hn : n < 3) :
    thetaRate f n ((3 - n) / (3 - n + f)) = 0 := by
  have h2 : 0 < 3 - n + f := by linarith
  have h3 : 1 - (3 - n) / (3 - n + f) = f / (3 - n + f) := by field_simp; ring
  unfold thetaRate
  rw [h3]
  field_simp
  ring

theorem opening_point_lt_one (f n : ℝ) (hf : 0 < f) (hn : n < 3) :
    0 < (3 - n) / (3 - n + f) ∧ (3 - n) / (3 - n + f) < 1 := by
  have h2 : 0 < 3 - n + f := by linarith
  have h3 : 0 < 3 - n := by linarith
  constructor
  · positivity
  · rw [div_lt_one h2]; linarith

theorem rate_strictAnti (f : ℝ) (hf : 0 < f) {x y : ℝ} (_hx : 0 ≤ x) (hxy : x < y) (hy : y < 1) :
    1 - f * y / (1 - y) < 1 - f * x / (1 - x) := by
  have h1 : 0 < 1 - x := by linarith
  have h2 : 0 < 1 - y := by linarith
  have : f * x / (1 - x) < f * y / (1 - y) := by
    rw [div_lt_div_iff₀ h1 h2]
    nlinarith [mul_pos hf (show 0 < y - x by linarith)]
  linarith

theorem rate_to_minus_infty (f B : ℝ) (hf : 0 < f) :
    ∃ δ : ℝ, 0 < δ ∧ ∀ x : ℝ, 1 - δ < x → x < 1 → 1 - f * x / (1 - x) < B := by
  refine ⟨min (1 / 2) (f / (2 * (|1 - B| + 1))), by positivity, ?_⟩
  intro x hx1 hx2
  have hδ1 : min (1 / 2 : ℝ) (f / (2 * (|1 - B| + 1))) ≤ 1 / 2 := min_le_left _ _
  have hδ2 : min (1 / 2 : ℝ) (f / (2 * (|1 - B| + 1))) ≤ f / (2 * (|1 - B| + 1)) := min_le_right _ _
  have hxh : 1 / 2 < x := by linarith
  have h1 : 0 < 1 - x := by linarith
  have hab : 0 < |1 - B| + 1 := by positivity
  have hlt : 1 - x < f / (2 * (|1 - B| + 1)) := by linarith
  have hlt' : (1 - x) * (2 * (|1 - B| + 1)) < f := by
    rwa [lt_div_iff₀ (by positivity)] at hlt
  -- f x / (1-x) > 1 - B
  have hfx : (1 - B) < f * x / (1 - x) := by
    rw [lt_div_iff₀ h1]
    have hB : 1 - B ≤ |1 - B| := le_abs_self _
    have : f * x > f / 2 := by nlinarith
    nlinarith [mul_pos h1 hab]
  linarith

/-! ### stand-off thresholds (EdS l/l_ta = 4x(1-x), f = 1) -/

theorem standoff_numbers :
    4 * ((3 - (0 : ℝ)) / (3 - 0 + 1)) * (1 - (3 - (0 : ℝ)) / (3 - 0 + 1)) = 3 / 4 ∧
    4 * ((3 - (1 : ℝ)) / (3 - 1 + 1)) * (1 - (3 - (1 : ℝ)) / (3 - 1 + 1)) = 8 / 9 ∧
    4 * ((3 - (2 : ℝ)) / (3 - 2 + 1)) * (1 - (3 - (2 : ℝ)) / (3 - 2 + 1)) = 1 := by
  refine ⟨?_, ?_, ?_⟩ <;> norm_num

theorem standoff_gate (xs s : ℝ) (hxs : 1 / 2 ≤ xs) (_hxs1 : xs < 1) (_hs0 : 0 < s) (hs1 : s ≤ 1) :
    xs ≤ (1 + Real.sqrt (1 - s)) / 2 ↔ s ≤ 4 * xs * (1 - xs) := by
  have hsq : 0 ≤ 1 - s := by linarith
  have hr := Real.sq_sqrt hsq
  have hr0 := Real.sqrt_nonneg (1 - s)
  constructor
  · intro h
    have h2 : 2 * xs - 1 ≤ Real.sqrt (1 - s) := by linarith
    have h3 : 0 ≤ 2 * xs - 1 := by linarith
    have h4 : (2 * xs - 1) ^ 2 ≤ (Real.sqrt (1 - s)) ^ 2 := by
      exact pow_le_pow_left₀ h3 h2 2
    nlinarith
  · intro h
    by_contra hc
    push Not at hc
    have h2 : Real.sqrt (1 - s) < 2 * xs - 1 := by linarith
    have h4 : (Real.sqrt (1 - s)) ^ 2 < (2 * xs - 1) ^ 2 := by
      exact pow_lt_pow_left₀ h2 hr0 (by norm_num)
    nlinarith

end M3E

#print axioms M3E.theta_FRW
#print axioms M3E.axis_rate
#print axioms M3E.axis_rate_expand
#print axioms M3E.theta_three_axes
#print axioms M3E.opening_iff
#print axioms M3E.opening_point_zero
#print axioms M3E.opening_point_lt_one
#print axioms M3E.rate_strictAnti
#print axioms M3E.rate_to_minus_infty
#print axioms M3E.standoff_numbers
#print axioms M3E.standoff_gate
