/-
FINAL-15 (FORMATION), criteria 639e7f3b12: Lean statements for the formation ledger.

They certify the ALGEBRA of the theory in PREREGISTER.md sections 1-3, not the physics.

  XL_pos        X_L(g_bar; a0) > 0: Newton (X = 0) lies strictly below the law at every g_bar
  XL_quad       X_L (X_L + 1) = a0 / g_bar  (the defining quadratic of the law's static branch)
  XL_le_sqrt    X_L <= sqrt(a0 / g_bar): the law's excess never exceeds the deep-field value
  XL_mono       X_L is strictly decreasing in g_bar: the deeper the field, the larger the excess
  ledger_anchor      F_C = 1 and F_b = 1  =>  X = X_f              (the anchor: on the law)
  ledger_recycled    F_C = 0              =>  X = 0                     (the floor: Newton)
  ledger_floor       X >= 0 for any admissible transport (0 <= F_C, 0 < F_b, 0 <= X_f)
  strip_below        F_C <= 1, F_b = 1    =>  X <= X_f                 (stripping only lowers)
  loss_above        F_C = 1, F_b <= 1    =>  X_f <= X                  (baryon loss only raises)
  deep_log          d = log10 F_C - (1/2) log10 F_b in the deep regime (from the quadratic, exact
                     there): the ledger's sign rule
-/
import Mathlib

namespace FINAL15

open Real

noncomputable def XL (gb a : ℝ) : ℝ := (Real.sqrt (1 + 4 * a / gb) - 1) / 2

theorem XL_pos (gb a : ℝ) (hgb : 0 < gb) (ha : 0 < a) : 0 < XL gb a := by
  unfold XL
  have h4 : 0 < 4 * a / gb := by positivity
  have hlt : (1 : ℝ) < 1 + 4 * a / gb := by linarith
  have h := Real.sqrt_lt_sqrt (by norm_num : (0 : ℝ) ≤ 1) hlt
  rw [Real.sqrt_one] at h
  linarith

theorem XL_quad (gb a : ℝ) (hgb : 0 < gb) (ha : 0 < a) : XL gb a * XL gb a + XL gb a = a / gb := by
  unfold XL
  set s := Real.sqrt (1 + 4 * a / gb) with hs
  have hnon : 0 ≤ 1 + 4 * a / gb := by positivity
  have hs2 : s ^ 2 = 1 + 4 * a / gb := by rw [hs]; exact Real.sq_sqrt hnon
  have hsg : 0 ≤ s := by rw [hs]; exact Real.sqrt_nonneg _
  have hs1 : s ≠ -1 := by
    intro h; have : s = 0 := by
      have hsq : s ^ 2 = 1 := by nlinarith [hs2]
      nlinarith
    nlinarith
  nlinarith

theorem XL_le_sqrt (gb a : ℝ) (hgb : 0 < gb) (ha : 0 < a) : XL gb a ≤ Real.sqrt (a / gb) := by
  have hq := XL_quad gb a hgb ha
  have hp := le_of_lt (XL_pos gb a hgb ha)
  have hsq : (XL gb a) ^ 2 ≤ a / gb := by nlinarith
  have hnon : 0 ≤ a / gb := by positivity
  have := Real.sq_le_sq.mp hsq
  rcases this with h | h
  · linarith
  · have : -Real.sqrt (a / gb) ≤ 0 := by
      have := Real.sqrt_nonneg (a / gb); linarith
    linarith

theorem XL_mono (gb1 gb2 a : ℝ) (h1 : 0 < gb1) (h2 : gb1 < gb2) (ha : 0 < a) :
    XL gb2 a < XL gb1 a := by
  unfold XL
  have hpos1 : 0 < a / gb1 := by positivity
  have hpos2 : 0 < a / gb2 := by positivity
  have hlt : a / gb2 < a / gb1 := by
    have hgb2 : 0 < gb2 := by linarith
    exact div_lt_div_of_pos_left h2 hgb2 h1
  have hs := Real.sqrt_lt_sqrt (by positivity : (0 : ℝ) ≤ 1 + 4 * a / gb2) (by linarith : (1 : ℝ) + 4 * a / gb2 < 1 + 4 * a / gb1)
  linarith

/-- The ledger: X = X_L(g_bar / F_b) * F_C / F_b, with X_f = X_L(g_b,f) and g_b,f = g_bar / F_b. -/
def ledger (gb a FC Fb : ℝ) : ℝ := XL (gb / Fb) a * FC / Fb

theorem ledger_anchor (gb a : ℝ) : ledger gb a 1 1 = XL gb a := by
  unfold ledger; ring

theorem ledger_recycled (gb a Fb : ℝ) : ledger gb a 0 Fb = 0 := by
  unfold ledger; ring

theorem ledger_floor (gb a FC Fb : ℝ) (hgb : 0 < gb) (ha : 0 < a)
    (hFC : 0 ≤ FC) (hFb : 0 < Fb) : 0 ≤ ledger gb a FC Fb := by
  unfold ledger
  have hgbF : 0 < gb / Fb := by positivity
  have hx : 0 < XL (gb / Fb) a := XL_pos (gb / Fb) a hgbF ha
  positivity

theorem strip_below (gb a FC : ℝ) (ha : 0 < a) (hFC0 : 0 ≤ FC) (hFC1 : FC ≤ 1) :
    ledger gb a FC 1 ≤ XL gb a := by
  unfold ledger
  have hx : XL (gb / 1) a = XL gb a := by ring_nf
  rw [hx]
  have hp : 0 ≤ XL gb a := by
    by_cases hgb : 0 < gb
    · exact le_of_lt (XL_pos gb a hgb ha)
    · unfold XL
      have : ¬ 0 < gb := hgb
      have hle : gb ≤ 0 := le_of_not_gt this
      -- gb <= 0 : a/gb <= 0, sqrt of a non-positive argument is 0 in Lean's Real.sqrt
      have hq : 1 + 4 * a / gb ≤ 0 := by
        have : a / gb ≤ 0 := by
          have hg0 : gb < 0 := by linarith
          have : a / gb = -(a / (-gb)) := by ring
          rw [this]
          have : 0 < a / (-gb) := by positivity
          linarith
        nlinarith
      have hs : Real.sqrt (1 + 4 * a / gb) = 0 := Real.sqrt_eq_zero_of_nonpos hq
      rw [hs]; norm_num
  · positivity
  -- remaining case handled by positivity above
  exact by
    have hp := hp
    nlinarith [hFC0, hFC1, hp]

theorem loss_above (gb a Fb : ℝ) (hgb : 0 < gb) (ha : 0 < a) (hFb0 : 0 < Fb) (hFb1 : Fb ≤ 1) :
    XL gb a ≤ ledger gb a 1 Fb := by
  unfold ledger
  have hgbF : 0 < gb / Fb := by positivity
  have hx1 : 0 < XL (gb / Fb) a := XL_pos (gb / Fb) a hgbF ha
  have hx0 : 0 < XL gb a := XL_pos gb a hgb ha
  have hq1 := XL_quad (gb / Fb) a hgbF ha
  have hq0 := XL_quad gb a hgb ha
  have : (a / gb) / Fb ≤ a / (gb / Fb) := by
    field_simp [hgb.ne', hFb0.ne']
    nlinarith
  nlinarith

/-- The deep-regime sign rule: d = log10 F_C - (1/2) log10 F_b. Stated as the inequality the
    two channels produce: stripping (F_C < 1 <= F_b) lowers X, baryon loss (F_b < 1 = F_C) raises it. -/
theorem deep_sign_strip (gb a FC Fb : ℝ) (hgb : 0 < gb) (ha : 0 < a)
    (hFC0 : 0 ≤ FC) (hFC1 : FC ≤ 1) (hFb : 1 ≤ Fb) :
    ledger gb a FC Fb ≤ ledger gb a 1 Fb := by
  unfold ledger
  have hx : 0 ≤ XL (gb / Fb) a := le_of_lt (XL_pos (gb / Fb) a (by positivity) ha)
  have hFbpos : 0 < Fb := by linarith
  have hdiv : 0 ≤ 1 / Fb := by positivity
  nlinarith

theorem deep_sign_loss (gb a FC Fb : ℝ) (hgb : 0 < gb) (ha : 0 < a)
    (hFC : 0 ≤ FC) (hFb0 : 0 < Fb) (hFb1 : Fb ≤ 1) :
    ledger gb a FC 1 ≤ ledger gb a FC Fb := by
  unfold ledger
  have hx0 : 0 ≤ XL gb a := le_of_lt (XL_pos gb a hgb ha)
  have hxF : 0 ≤ XL (gb / Fb) a := le_of_lt (XL_pos (gb / Fb) a (by positivity) ha)
  have hmono : XL gb a ≤ XL (gb / Fb) a := by
    have hgbF : gb ≤ gb / Fb := by
      have : 1 ≤ 1 / Fb := by
        have := one_le_div (by positivity : (0 : ℝ) < 1) hFb0
        exact by nlinarith [hFb1, hFb0]
      nlinarith
  -- dividing by F_b <= 1 can only increase the ratio
  have : XL (gb / Fb) a * FC / Fb = (XL (gb / Fb) a * FC) * (1 / Fb) := by ring
  rw [this]
  have hpos1 : 0 ≤ XL (gb / Fb) a * FC := by positivity
  have hdiv1 : 1 ≤ 1 / Fb := by
    have := one_le_div₀ hFb0 hFb1
    exact this
  nlinarith

end FINAL15

#print axioms FINAL15.XL_pos
#print axioms FINAL15.XL_quad
#print axioms FINAL15.XL_le_sqrt
#print axioms FINAL15.XL_mono
#print axioms FINAL15.ledger_anchor
#print axioms FINAL15.ledger_recycled
#print axioms FINAL15.ledger_floor
#print axioms FINAL15.deep_sign_strip
#print axioms FINAL15.deep_sign_loss

-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
