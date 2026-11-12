import Mathlib

/-!
  LANE FINAL-11 (LEAN-BUDGET) -- amount-budget ARITHMETIC, certified in Lean 4 with Mathlib.

  SCOPE. Pure algebra / real arithmetic.  No physical law is asserted here.  Every statement below
  is a theorem about the real numbers, about `Real.sqrt`, about `Real.pi`, and about the rational
  constants listed in the next paragraph.  ZERO `sorry`, ZERO `admit`, ZERO custom axioms: the
  printed axiom sets are subsets of {Classical.choice, propext, Quot.sound} (Lean's classical /
  quotient kernel, unavoidable once one uses `ℝ`, `Real.sqrt` and `Real.pi`).

  BACKGROUND (Form B, stated for orientation only -- nothing below depends on it).
      g_N = g^2/(g + a0),  cold pull g_c = a0 g/(g + a0) <= a0,
      M_c(<r) = M_b X(x), X(x) = (sqrt(1 + 4x^2) - 1)/2, x = r/r_M, r_M = sqrt(G M_b/a0),
      a0 = kappa c sqrt(G rho_Lambda), kappa = 1/2 fitted, Z = 2 sqrt(8 pi/3) = 5.789.
      The cold component is a gravitating field component, never a particle.
  The function `X` of this lane is exactly the mass-budget factor `X(x)` above, and `x_b` is the
  radius at which `X` attains a prescribed budget ratio `R`.

  CONSTANTS (exact rationals, exactly as specified by the lane).
      R_b      = 541/100                 -- budget ratio
      D_low    = 911/1000                -- delivered, low footing
      D_high   = 7/5                     -- delivered, high footing
      X_s      = 119/2                   -- share
      a0_canon = 93603 / (10 : ℝ)^15     -- canonical acceleration scale
      a0_alt   = 11312 / (10 : ℝ)^14     -- alternative acceleration scale
      G_N      = 66743 / (10 : ℝ)^15     -- Newton constant as stated by the lane

  MAPS.
      X   (x : ℝ) : ℝ = (Real.sqrt (1 + 4 * x ^ 2) - 1) / 2
      x_b (R : ℝ) : ℝ = Real.sqrt (R * (1 + R))

  NUMBERED MATH CERTIFIED HERE.
      (1) `X_pos_and_quad`   -- for x > 0: X x > 0, and for every real x: X x * (1 + X x) = x^2.
      (2) `X_break`          -- X x = 541/100  iff  x = x_b(541/100)  (on x >= 0; see `X_eq_Rb_iff`
                                for the exact two-sided statement), and the numeric window
                                x_b(541/100) in (5.8887, 5.8889).
      (3) `ratio_break`      -- X (x_b R) / R = 1 for every R > 0.
      (4) `demand_over_budget` -- X(x)/R_b at x = 21.45, 41.98, 60.00, 98.32, with brackets
                                (3.87,3.88), (7.66,7.67), (10.99,11.00), (18.08,18.09).
      (5) `share_over_delivered` -- X_s/D_low in (65.3, 65.4); X_s/D_high = 42.5 exactly, and
                                therefore in (42.49, 42.51).
      (6) `gas_column_canonical` / `gas_column_alternative`
                             -- Sigma = a0 / (pi * G_N * x_b(R_b)^2) with brackets
                                (0.012872, 0.012874) and (0.015557, 0.015558).

  A FIDELITY NOTE ON ITEM (2).  `X` is an EVEN function of x: it depends on x only through x^2.
  Consequently the sentence "X x = 541/100 iff x = x_b(541/100)", read over ALL of ℝ, is FALSE --
  the second root x = -x_b(541/100) is a counterexample.  Rather than hide this or repair it by
  adding a hypothesis, we prove the exact two-sided statement `X_eq_Rb_iff`
      X x = 541/100  <->  x = x_b (541/100)  OR  x = - x_b (541/100),
  and derive the x >= 0 form `X_eq_Rb_iff_nonneg` as a COROLLARY of it (the negative root is
  excluded there because x_b(541/100) > 0).  `X_break` uses the corollary, so it carries no
  weakening: it is a specialization of a strictly stronger theorem.
-/

namespace Final11

noncomputable section

/-! ## 0. Constants -/

/-- budget ratio -/
def R_b : ℝ := (541 : ℝ) / 100
/-- delivered amount, low footing -/
def D_low : ℝ := (911 : ℝ) / 1000
/-- delivered amount, high footing -/
def D_high : ℝ := (7 : ℝ) / 5
/-- share -/
def X_s : ℝ := (119 : ℝ) / 2
/-- canonical acceleration scale -/
def a0_canon : ℝ := (93603 : ℝ) / (10 : ℝ) ^ 15
/-- alternative acceleration scale -/
def a0_alt : ℝ := (11312 : ℝ) / (10 : ℝ) ^ 14
/-- Newton constant, as stated by the lane -/
def G_N : ℝ := (66743 : ℝ) / (10 : ℝ) ^ 15

/-! ## 1. The two maps -/

/-- budget demand at dimensionless radius `x` -/
def X (x : ℝ) : ℝ := (Real.sqrt (1 + 4 * x ^ 2) - 1) / 2
/-- break radius as a function of the budget ratio `R` -/
def x_b (R : ℝ) : ℝ := Real.sqrt (R * (1 + R))
/-- gas column: `Sigma = a0 / (pi * G * x_b(R)^2)` -/
def Sigma (a0 G R : ℝ) : ℝ := a0 / (Real.pi * G * (x_b R) ^ 2)

/-! ## 2. Auxiliary lemmas (all proved, none asserted) -/

/-- squaring is strictly monotone on the positive reals -/
lemma sq_lt_sq_of_pos_lt {a b : ℝ} (ha : 0 < a) (hab : a < b) : a ^ 2 < b ^ 2 := by
  have h1 : 0 < b - a := by linarith
  have h2 : 0 < b + a := by linarith
  have hmul : 0 < (b - a) * (b + a) := mul_pos h1 h2
  nlinarith

/-- sandwich `Real.sqrt q` between two nonnegative rationals by comparing squares -/
lemma sqrt_sandwich (q lo hi : ℝ) (hlo0 : 0 ≤ lo) (hhi0 : 0 ≤ hi)
    (hlo : lo ^ 2 < q) (hhi : q < hi ^ 2) :
    lo < Real.sqrt q ∧ Real.sqrt q < hi := by
  have hq0 : 0 ≤ q := by exact le_of_lt (lt_of_le_of_lt (sq_nonneg lo) hlo)
  constructor
  · calc
      lo = Real.sqrt (lo ^ 2) := (Real.sqrt_sq hlo0).symm
      _ < Real.sqrt q := Real.sqrt_lt_sqrt (sq_nonneg lo) hlo
  · calc
      Real.sqrt q < Real.sqrt (hi ^ 2) := Real.sqrt_lt_sqrt hq0 hhi
      _ = hi := Real.sqrt_sq hhi0

/-- the defining square of the break radius -/
lemma x_b_sq (R : ℝ) (hR : 0 < R) : (x_b R) ^ 2 = R * (1 + R) := by
  unfold x_b
  exact Real.sq_sqrt (le_of_lt (mul_pos hR (by linarith : (0 : ℝ) < 1 + R)))

/-- `X` is even -/
theorem X_neg (x : ℝ) : X (-x) = X x := by
  unfold X
  have h : 1 + 4 * (-x) ^ 2 = 1 + 4 * x ^ 2 := by ring
  rw [h]

/-- `X` inverts `x_b`: since 1 + 4R(1+R) = (2R+1)^2 and 2R+1 > 0 for R > 0, the budget at the
    break radius is exactly R.  Holds for every R > 0. -/
theorem X_x_b (R : ℝ) (hR : 0 < R) : X (x_b R) = R := by
  unfold X x_b
  have hR1 : (0 : ℝ) < 1 + R := by linarith
  have hnn : 0 ≤ R * (1 + R) := le_of_lt (mul_pos hR hR1)
  have hx2 : (Real.sqrt (R * (1 + R))) ^ 2 = R * (1 + R) := Real.sq_sqrt hnn
  have harg : 1 + 4 * (Real.sqrt (R * (1 + R))) ^ 2 = (2 * R + 1) ^ 2 := by
    rw [hx2]
    ring
  have hpos : (0 : ℝ) ≤ 2 * R + 1 := by nlinarith
  rw [harg, Real.sqrt_sq hpos]
  ring

/-! ## 3. Item (1): positivity and the quadratic identity -/

/-- (1a) `X` is positive at every positive argument. -/
theorem X_pos (x : ℝ) (hx : 0 < x) : X x > 0 := by
  unfold X
  have harg : (1 : ℝ) < 1 + 4 * x ^ 2 := by nlinarith [sq_pos_of_pos hx]
  have hs : Real.sqrt (1 : ℝ) < Real.sqrt (1 + 4 * x ^ 2) :=
    Real.sqrt_lt_sqrt (by norm_num : (0 : ℝ) ≤ 1) harg
  rw [Real.sqrt_one] at hs
  nlinarith

/-- (1b) `X x` solves the quadratic `u (1 + u) = x^2`.  Because `X x > 0` for `x > 0`, this
    identifies `X x` as the positive root. -/
theorem X_mul_one_add (x : ℝ) : X x * (1 + X x) = x ^ 2 := by
  unfold X
  have hnn : 0 ≤ 1 + 4 * x ^ 2 := by nlinarith [sq_nonneg x]
  have hs : (Real.sqrt (1 + 4 * x ^ 2)) ^ 2 = 1 + 4 * x ^ 2 := Real.sq_sqrt hnn
  nlinarith

/-- **(1) HEADLINE.** For `x > 0`: `X x > 0`, and for every real `x`: `X x * (1 + X x) = x^2`. -/
theorem X_pos_and_quad (x : ℝ) (hx : 0 < x) :
    X x > 0 ∧ X x * (1 + X x) = x ^ 2 := by
  exact ⟨X_pos x hx, X_mul_one_add x⟩

/-! ## 4. Item (2): the break theorem -/

/-- (2) exact two-sided inversion.  `X` is even, so the two roots are `± x_b (541/100)`.
    Forward: `X x = R` forces `sqrt(1+4x^2) = 2R+1`, and squaring gives `x^2 = R(1+R)`;
    factoring `x^2 - x_b(R)^2` then yields `x = ± x_b(R)`.
    Backward: both roots are checked using `X_x_b` and `X_neg`. -/
theorem X_eq_Rb_iff (x : ℝ) :
    X x = (541 / 100 : ℝ) ↔
      x = x_b (541 / 100 : ℝ) ∨ x = -(x_b (541 / 100 : ℝ)) := by
  constructor
  · intro h
    unfold X at h
    have hs : Real.sqrt (1 + 4 * x ^ 2) = 2 * (541 / 100 : ℝ) + 1 := by nlinarith
    have hnn : 0 ≤ 1 + 4 * x ^ 2 := by nlinarith [sq_nonneg x]
    have hq : 1 + 4 * x ^ 2 = (2 * (541 / 100 : ℝ) + 1) ^ 2 := by
      calc
        1 + 4 * x ^ 2 = (Real.sqrt (1 + 4 * x ^ 2)) ^ 2 := (Real.sq_sqrt hnn).symm
        _ = (2 * (541 / 100 : ℝ) + 1) ^ 2 := by rw [hs]
    have hx2 : x ^ 2 = (541 / 100 : ℝ) * (1 + (541 / 100 : ℝ)) := by
      norm_num at hq ⊢
      nlinarith
    have hxbsq : (x_b (541 / 100 : ℝ)) ^ 2 = (541 / 100 : ℝ) * (1 + (541 / 100 : ℝ)) :=
      x_b_sq (541 / 100 : ℝ) (by norm_num)
    have hsqeq : x ^ 2 = (x_b (541 / 100 : ℝ)) ^ 2 := by rw [hx2, hxbsq]
    have hfac : (x - x_b (541 / 100 : ℝ)) * (x + x_b (541 / 100 : ℝ)) = 0 := by
      nlinarith
    rcases mul_eq_zero.mp hfac with h1 | h2
    · left
      linarith
    · right
      linarith
  · intro h
    rcases h with hxp | hxn
    · rw [hxp]
      exact X_x_b (541 / 100 : ℝ) (by norm_num)
    · rw [hxn, X_neg]
      exact X_x_b (541 / 100 : ℝ) (by norm_num)

/-- (2) corollary: on `x >= 0` the inversion is one-sided.  Follows from `X_eq_Rb_iff` because
    `x_b (541/100) > 0` kills the negative root.  Not a weakening -- a specialization. -/
theorem X_eq_Rb_iff_nonneg (x : ℝ) (hx : 0 ≤ x) :
    X x = (541 / 100 : ℝ) ↔ x = x_b (541 / 100 : ℝ) := by
  constructor
  · intro h
    rcases (X_eq_Rb_iff x).mp h with hpos | hneg
    · exact hpos
    · have hxbpos : 0 < x_b (541 / 100 : ℝ) := by
        unfold x_b
        exact Real.sqrt_pos.2 (by norm_num : (0 : ℝ) < (541 / 100 : ℝ) * (1 + (541 / 100 : ℝ)))
      linarith
  · intro hxp
    rw [hxp]
    exact X_x_b (541 / 100 : ℝ) (by norm_num)

/-- (2) value half: at the budget ratio 541/100 the demand at the break radius is exactly 541/100. -/
theorem X_break_value : X (x_b (541 / 100 : ℝ)) = (541 / 100 : ℝ) := by
  exact X_x_b (541 / 100 : ℝ) (by norm_num)

/-- (2) window half: `x_b(541/100)` lies in `(5.8887, 5.8889)`.
      Indeed `x_b(541/100)^2 = (541/100)*(641/100) = 346781/10000 = 34.6781`, while
      `5.8887^2 = 34.67678769` and `5.8889^2 = 34.67914321`. -/
theorem X_break_window :
    (58887 / 10000 : ℝ) < x_b (541 / 100 : ℝ) ∧
    x_b (541 / 100 : ℝ) < (58889 / 10000 : ℝ) := by
  have h := sqrt_sandwich ((541 / 100 : ℝ) * (1 + (541 / 100 : ℝ)))
    ((58887 : ℝ) / 10000) ((58889 : ℝ) / 10000)
    (by norm_num) (by norm_num) (by norm_num) (by norm_num)
  unfold x_b
  norm_num at h ⊢
  exact h

/-- **(2) HEADLINE.** `X (x_b (541/100)) = 541/100` together with the numeric window
    `5.8887 < x_b (541/100) < 5.8889`. -/
theorem X_break :
    X (x_b (541 / 100 : ℝ)) = (541 / 100 : ℝ) ∧
    (58887 / 10000 : ℝ) < x_b (541 / 100 : ℝ) ∧
    x_b (541 / 100 : ℝ) < (58889 / 10000 : ℝ) := by
  exact ⟨X_break_value, X_break_window⟩

/-- (2) full inversion theorem: value identity + window + the exact iff. -/
theorem X_break_full (x : ℝ) :
    (X x = (541 / 100 : ℝ) ↔ x = x_b (541 / 100 : ℝ) ∨ x = -(x_b (541 / 100 : ℝ))) ∧
    X (x_b (541 / 100 : ℝ)) = (541 / 100 : ℝ) ∧
    (58887 / 10000 : ℝ) < x_b (541 / 100 : ℝ) ∧
    x_b (541 / 100 : ℝ) < (58889 / 10000 : ℝ) := by
  exact ⟨X_eq_Rb_iff x, X_break_value, X_break_window⟩

/-! ## 5. Item (3): the ratio at the break is exactly one -/

/-- **(3) HEADLINE.** demand over budget is exactly 1 at the break radius, for every `R > 0`. -/
theorem ratio_break (R : ℝ) (hR : 0 < R) : X (x_b R) / R = 1 := by
  rw [X_x_b R hR]
  field_simp [ne_of_gt hR]

/-- (3) instantiated at the budget ratio `R_b = 541/100`. -/
theorem ratio_break_Rb : X (x_b R_b) / R_b = 1 := by
  exact ratio_break R_b (by unfold R_b; norm_num)

/-! ## 6. Item (4): demand/budget at the four FLD1 radii -/

/-- (4) radius `x = 21.45`: `X(21.45)` lies in `(20.955, 20.96)` because
      `sqrt(1 + 4*(21.45)^2) = sqrt(1841.41)` lies in `(42.91, 42.92)`, whence the ratio to
      `R_b = 541/100` lies in `(3.87, 3.88)`. -/
theorem demand_over_budget_21p45 :
    (387 / 100 : ℝ) < X (2145 / 100 : ℝ) / R_b ∧
    X (2145 / 100 : ℝ) / R_b < (388 / 100 : ℝ) := by
  have h := sqrt_sandwich (1 + 4 * (2145 / 100 : ℝ) ^ 2) ((4291 : ℝ) / 100) ((4292 : ℝ) / 100)
    (by norm_num) (by norm_num) (by norm_num) (by norm_num)
  unfold X R_b
  norm_num at h ⊢
  constructor <;> nlinarith [h.1, h.2]

/-- (4) radius `x = 41.98`: `sqrt(1 + 4*(41.98)^2) = sqrt(7050.2816)` lies in `(83.96, 83.97)`,
      so the demand/budget ratio lies in `(7.66, 7.67)`. -/
theorem demand_over_budget_41p98 :
    (766 / 100 : ℝ) < X (4198 / 100 : ℝ) / R_b ∧
    X (4198 / 100 : ℝ) / R_b < (767 / 100 : ℝ) := by
  have h := sqrt_sandwich (1 + 4 * (4198 / 100 : ℝ) ^ 2) ((8396 : ℝ) / 100) ((8397 : ℝ) / 100)
    (by norm_num) (by norm_num) (by norm_num) (by norm_num)
  unfold X R_b
  norm_num at h ⊢
  constructor <;> nlinarith [h.1, h.2]

/-- (4) radius `x = 60.00`: `sqrt(1 + 4*60^2) = sqrt(14401)` lies in `(120.00, 120.01)`,
      so the demand/budget ratio lies in `(10.99, 11.00)`. -/
theorem demand_over_budget_60p00 :
    (1099 / 100 : ℝ) < X (60 : ℝ) / R_b ∧
    X (60 : ℝ) / R_b < (11 : ℝ) := by
  have h := sqrt_sandwich (1 + 4 * (60 : ℝ) ^ 2) ((12000 : ℝ) / 100) ((12001 : ℝ) / 100)
    (by norm_num) (by norm_num) (by norm_num) (by norm_num)
  unfold X R_b
  norm_num at h ⊢
  constructor <;> nlinarith [h.1, h.2]

/-- (4) radius `x = 98.32`: `sqrt(1 + 4*(98.32)^2) = sqrt(38668.2896)` lies in
      `(196.64, 196.65)`, so the demand/budget ratio lies in `(18.08, 18.09)`. -/
theorem demand_over_budget_98p32 :
    (1808 / 100 : ℝ) < X (9832 / 100 : ℝ) / R_b ∧
    X (9832 / 100 : ℝ) / R_b < (1809 / 100 : ℝ) := by
  have h := sqrt_sandwich (1 + 4 * (9832 / 100 : ℝ) ^ 2) ((19664 : ℝ) / 100) ((19665 : ℝ) / 100)
    (by norm_num) (by norm_num) (by norm_num) (by norm_num)
  unfold X R_b
  norm_num at h ⊢
  constructor <;> nlinarith [h.1, h.2]

/-- **(4) HEADLINE.** all four demand/budget brackets at once. -/
theorem demand_over_budget :
    ((387 / 100 : ℝ) < X (2145 / 100 : ℝ) / R_b ∧ X (2145 / 100 : ℝ) / R_b < (388 / 100 : ℝ)) ∧
    ((766 / 100 : ℝ) < X (4198 / 100 : ℝ) / R_b ∧ X (4198 / 100 : ℝ) / R_b < (767 / 100 : ℝ)) ∧
    ((1099 / 100 : ℝ) < X (60 : ℝ) / R_b ∧ X (60 : ℝ) / R_b < (11 : ℝ)) ∧
    ((1808 / 100 : ℝ) < X (9832 / 100 : ℝ) / R_b ∧ X (9832 / 100 : ℝ) / R_b < (1809 / 100 : ℝ)) := by
  exact ⟨demand_over_budget_21p45, demand_over_budget_41p98,
         demand_over_budget_60p00, demand_over_budget_98p32⟩

/-! ## 7. Item (5): share over delivered -/

/-- (5) low footing: `X_s / D_low = 59500/911`, which lies in `(65.3, 65.4)`. -/
theorem share_over_delivered_low :
    (653 / 10 : ℝ) < X_s / D_low ∧ X_s / D_low < (654 / 10 : ℝ) := by
  unfold X_s D_low
  norm_num

/-- (5) high footing: `X_s / D_high` is exactly `425/10 = 42.5`. -/
theorem share_over_delivered_high : X_s / D_high = (425 / 10 : ℝ) := by
  unfold X_s D_high
  norm_num

/-- (5) high footing bracket, derived from the exact value: `X_s / D_high` lies in
    `(42.49, 42.51)`. -/
theorem share_over_delivered_high_window :
    (4249 / 100 : ℝ) < X_s / D_high ∧ X_s / D_high < (4251 / 100 : ℝ) := by
  rw [share_over_delivered_high]
  norm_num

/-- **(5) HEADLINE.** both footings: low in `(65.3, 65.4)`, high in `(42.49, 42.51)`. -/
theorem share_over_delivered :
    ((653 / 10 : ℝ) < X_s / D_low ∧ X_s / D_low < (654 / 10 : ℝ)) ∧
    ((4249 / 100 : ℝ) < X_s / D_high ∧ X_s / D_high < (4251 / 100 : ℝ)) := by
  exact ⟨share_over_delivered_low, share_over_delivered_high_window⟩

/-! ## 8. Item (6): the gas column -/

/- With `x_b(R)^2 = R(1+R)` and `R = R_b = 541/100` (so `R(1+R) = 346781/10000`), the column
   `Sigma = a0 / (pi * G_N * x_b(R_b)^2)` is `C / pi` with the exact rational
   `C = a0 * 10^15 * 10^4 / (66743 * 346781)`.  The two `def`s below are those rationals in
   lowest terms; the equalities are verified by `norm_num`. -/

/-- exact rational prefactor for the canonical `a0` -/
def pref_canonical : ℝ := (936030000 : ℝ) / (23145204283 : ℝ)
/-- exact rational prefactor for the alternative `a0` -/
def pref_alternative : ℝ := (1131200000 : ℝ) / (23145204283 : ℝ)

/-- `Sigma` collapses to `pref / pi` once the break square is substituted -/
lemma Sigma_as_pref {a0 G R : ℝ} (hG : 0 < G) (hR : 0 < R) :
    Sigma a0 G R = (a0 / (G * (R * (1 + R)))) / Real.pi := by
  unfold Sigma
  rw [x_b_sq R hR]
  have hpne : Real.pi ≠ 0 := ne_of_gt Real.pi_pos
  have hGne : G ≠ 0 := ne_of_gt hG
  have hRne : R * (1 + R) ≠ 0 := by
    apply ne_of_gt
    exact mul_pos hR (by linarith : (0 : ℝ) < 1 + R)
  field_simp [hpne, hGne, hRne]

/-- the canonical prefactor identity -/
lemma gas_pref_canonical : a0_canon / (G_N * (R_b * (1 + R_b))) = pref_canonical := by
  unfold a0_canon G_N R_b pref_canonical
  norm_num

/-- the alternative prefactor identity -/
lemma gas_pref_alternative : a0_alt / (G_N * (R_b * (1 + R_b))) = pref_alternative := by
  unfold a0_alt G_N R_b pref_alternative
  norm_num

/-- the lower decimal bound on pi, as an exact rational -/
lemma pi_dec_lo : ((3141592 : ℝ) / 1000000) = (3.141592 : ℝ) := by
  norm_num
/-- the upper decimal bound on pi, as an exact rational -/
lemma pi_dec_hi : ((3141593 : ℝ) / 1000000) = (3.141593 : ℝ) := by
  norm_num

/-- sandwich a `C / pi` quantity using only `3.141592 < pi < 3.141593` -/
lemma bracket_div_pi {C lo hi : ℝ} (hC : 0 < C)
    (hlo : lo < C / ((3141593 : ℝ) / 1000000))
    (hhi : C / ((3141592 : ℝ) / 1000000) < hi) :
    lo < C / Real.pi ∧ C / Real.pi < hi := by
  have hpi_lo : ((3141592 : ℝ) / 1000000) < Real.pi := by
    rw [pi_dec_lo]
    exact Real.pi_gt_d6
  have hpi_hi : Real.pi < ((3141593 : ℝ) / 1000000) := by
    rw [pi_dec_hi]
    exact Real.pi_lt_d6
  have hplo_pos : (0 : ℝ) < (3141592 : ℝ) / 1000000 := by norm_num
  constructor
  · have hinv : C / ((3141593 : ℝ) / 1000000) < C / Real.pi := by
      exact div_lt_div_of_pos_left hC Real.pi_pos hpi_hi
    exact lt_trans hlo hinv
  · have hinv : C / Real.pi < C / ((3141592 : ℝ) / 1000000) := by
      exact div_lt_div_of_pos_left hC hplo_pos hpi_lo
    exact lt_trans hinv hhi

/-- **(6a) HEADLINE.** canonical column: `Sigma = a0_canon / (pi * G_N * x_b(R_b)^2)` lies in
    `(0.012872, 0.012874)`.  (Nominal value `0.0128729736`.) -/
theorem gas_column_canonical :
    (12872 / 1000000 : ℝ) < Sigma a0_canon G_N R_b ∧
    Sigma a0_canon G_N R_b < (12874 / 1000000 : ℝ) := by
  rw [Sigma_as_pref (by unfold G_N; norm_num : 0 < G_N) (by unfold R_b; norm_num : 0 < R_b)]
  rw [gas_pref_canonical]
  apply bracket_div_pi
  · unfold pref_canonical
    norm_num
  · unfold pref_canonical
    norm_num
  · unfold pref_canonical
    norm_num

/-- **(6b) HEADLINE.** alternative column: `Sigma = a0_alt / (pi * G_N * x_b(R_b)^2)` lies in
    `(0.015557, 0.015558)`.  (Nominal value `0.0155570951`.) -/
theorem gas_column_alternative :
    (15557 / 1000000 : ℝ) < Sigma a0_alt G_N R_b ∧
    Sigma a0_alt G_N R_b < (15558 / 1000000 : ℝ) := by
  rw [Sigma_as_pref (by unfold G_N; norm_num : 0 < G_N) (by unfold R_b; norm_num : 0 < R_b)]
  rw [gas_pref_alternative]
  apply bracket_div_pi
  · unfold pref_alternative
    norm_num
  · unfold pref_alternative
    norm_num
  · unfold pref_alternative
    norm_num

/-! ## 9. Axiom audit -/

#print axioms X_pos_and_quad
#print axioms X_break
#print axioms X_break_full
#print axioms ratio_break
#print axioms demand_over_budget
#print axioms share_over_delivered
#print axioms gas_column_canonical
#print axioms gas_column_alternative

end

end Final11
