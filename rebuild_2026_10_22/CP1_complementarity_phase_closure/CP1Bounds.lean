/-! CP1: algebra about STIPULATED bounds on the mix. It proves nothing about galaxies:
the hypotheses are assumed, not derived, and no physics enters. Core Lean only, no Mathlib.
The mix is written over `Int` with scaled weights: wp * a + wh * b, where wp + wh = W.
kappa = 1/2 FITTED; not theory closed. -/

/-- If the weights are nonnegative and sum to W, and a ≤ b, the mix lies between W*a and W*b. -/
theorem mix_between (wp wh W a b : Int) (hw : wp + wh = W) (h0 : 0 ≤ wp) (h1 : 0 ≤ wh) (hab : a ≤ b) :
    W * a ≤ wp * a + wh * b ∧ wp * a + wh * b ≤ W * b := by
  subst hw
  have d : 0 ≤ b - a := by omega
  have e1 : 0 ≤ wh * (b - a) := Int.mul_nonneg h1 d
  have e2 : 0 ≤ wp * (b - a) := Int.mul_nonneg h0 d
  rw [Int.mul_sub] at e1 e2
  rw [Int.add_mul, Int.add_mul]
  constructor <;> omega

/-- The stipulated complement: `chi_clust = 1 - chi_pol`, scaled, sums to W. -/
theorem weights_sum (wp W : Int) : wp + (W - wp) = W := by omega

/-- With zero weight on the halo the cold term drops out. Where that mass goes isn't stated. -/
theorem halo_weight_zero (wp a b : Int) : wp * a + 0 * b = wp * a := by simp
