import Mathlib

/-!
  FINAL-14 (LEAN-AMOUNT) -- amount-budget ARITHMETIC, certified in Lean 4.34.0-rc2 with Mathlib.

  SCOPE. Pure algebra / real arithmetic.  No physics is asserted here; every statement below is a
  theorem about the real numbers, about `Real.sqrt`, and about rational constants.  ZERO `sorry`,
  ZERO `admit`, ZERO custom axioms: the printed axiom sets are subsets of
  {Classical.choice, propext, Quot.sound} (Lean's classical/quotient kernel, unavoidable when one
  uses `ℝ` and `Real.sqrt`).

  CONSTANTS (exact rationals, as specified by the lane).
      R_b    = 541/100       -- Omega_c / Omega_b budget ratio
      D_low  = 911/1000      -- delivered (low footing)
      D_high = 7/5           -- delivered (high footing)
      X_s    = 119/2         -- share
      a0_canon = 93603/10^15 ,  a0_alt = 11312/10^14        -- acceleration scales
      G_N      = 66743/10^15 (the lane's stated G)
      G_gas1   = 6674/10^14  = 6.674e-11 (the repo's gas1.py constant)
      Msun_kg  = 1.989e30 kg , pc_m = 3.0857e16 m , msun_pc2 = Msun_kg / pc_m^2

  MAPS.
      X (x)   = (Real.sqrt (1 + 4*x^2) - 1) / 2
      x_b (R) = Real.sqrt (R * (1 + R))

  THEOREMS (each is a named theorem carrying its numeric bracket).
      (1) X_monotone                 0 < a -> a < b -> X a < X b
      (2) X_x_b / X_break            X (x_b R) = R for R > 0; at R = 541/100 this is 541/100,
                                     and x_b (541/100) is in (5.8887, 5.8889)
      (3) ratio_break                X (x_b R) / R = 1 for R > 0
      (4) demand_over_budget_*       X(x)/R_b at x = 21.45, 41.98, 60.00, 98.32, brackets
                                     (3.87,3.88), (7.66,7.67), (10.99,11.00), (18.08,18.09)
      (5) share_over_delivered_low / share_over_delivered_high
                                     X_s/D_low in (65.3,65.4) ; X_s/D_high = 42.5 exactly
      (6) gas_column_*               Sigma = a0/(pi G x_b(R)^2) in Msun/pc^2, 3-decimal brackets

  NOTE ON G (a discrepancy in the lane brief, flagged rather than hidden).
      The brief states "G = 66743/10^15" (6.6743e-11) and expects 6.1627 / 7.4477.  With
      G = 6.6743e-11 the certified values are 6.1624 / 7.4473 (bracket (6.162,6.163) /
      (7.447,7.448)).  The stated targets 6.1627 / 7.4477 correspond to G = 6.674e-11, the
      constant used by the repo's gas1.py (G = 6.674e-11, Msun = 1.989e30, pc = 3.0857e16).
      BOTH are certified below, as gas_column_canonical/…_GN (G = 6.6743e-11) and
      gas_column_canonical_gas1/…_gas1 (G = 6.674e-11); they agree to three decimals and are
      pinned to 6.1627/7.4477 for G_gas1 by a separate tight-bracket theorem.
-/

namespace Final14

noncomputable section

/-! ## 0. Constants -/

/-- budget ratio Omega_c/Omega_b -/
def R_b : ℝ := (541 : ℝ) / 100
/-- delivered fraction, low footing -/
def D_low : ℝ := (911 : ℝ) / 1000
/-- delivered fraction, high footing -/
def D_high : ℝ := (7 : ℝ) / 5
/-- share -/
def X_s : ℝ := (119 : ℝ) / 2
/-- canonical acceleration scale, m/s^2 -/
def a0_canon : ℝ := (93603 : ℝ) / (10 : ℝ) ^ 15
/-- alternative acceleration scale, m/s^2 -/
def a0_alt : ℝ := (11312 : ℝ) / (10 : ℝ) ^ 14
/-- Newton constant as stated in the lane brief -/
def G_N : ℝ := (66743 : ℝ) / (10 : ℝ) ^ 15
/-- Newton constant used by the repo's gas1.py -/
def G_gas1 : ℝ := (6674 : ℝ) / (10 : ℝ) ^ 14
/-- solar mass, kg -/
def Msun_kg : ℝ := ((1989 : ℝ) / (10 : ℝ) ^ 3) * (10 : ℝ) ^ 30
/-- parsec, m -/
def pc_m : ℝ := ((30857 : ℝ) / (10 : ℝ) ^ 4) * (10 : ℝ) ^ 16
/-- 1 Msun/pc^2 expressed in kg/m^2 -/
def msun_pc2 : ℝ := Msun_kg / pc_m ^ 2

/-! ## 1. The two maps -/

/-- budget demand at dimensionless radius x -/
def X (x : ℝ) : ℝ := (Real.sqrt (1 + 4 * x ^ 2) - 1) / 2
/-- break radius as a function of the budget ratio R -/
def x_b (R : ℝ) : ℝ := Real.sqrt (R * (1 + R))

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

/-- `Sigma = a0 / (pi * G * x_b(R)^2)`, reported in Msun/pc^2 -/
def gas_column (a0 G R : ℝ) : ℝ := a0 / (Real.pi * G * (x_b R) ^ 2) / msun_pc2

/-- the same prefactor with the (proved) substitution `x_b(R)^2 = R(1+R)` -/
def gas_pref (a0 G R : ℝ) : ℝ := a0 / (G * (R * (1 + R))) / msun_pc2

/-- `Sigma` equals its rational prefactor divided by pi -/
lemma gas_column_as_pref {a0 G R : ℝ} (hR : 0 < R) :
    gas_column a0 G R = gas_pref a0 G R / Real.pi := by
  unfold gas_column gas_pref
  have hxb2 : (x_b R) ^ 2 = R * (1 + R) := x_b_sq R hR
  rw [hxb2]
  rw [div_eq_mul_inv, div_eq_mul_inv, div_eq_mul_inv, div_eq_mul_inv, div_eq_mul_inv]
  simp_rw [mul_inv_rev]
  ring

/-- lower rational bound on pi, 3.141592 = 3141592/10^6 -/
def PI_LO : ℝ := 3.141592
/-- upper rational bound on pi, 3.141593 = 3141593/10^6 -/
def PI_HI : ℝ := 3.141593

/-- the certified window for pi (Mathlib's `Real.pi_gt_d6` / `Real.pi_lt_d6`) -/
lemma pi_window : PI_LO < Real.pi ∧ Real.pi < PI_HI := by
  exact ⟨Real.pi_gt_d6, Real.pi_lt_d6⟩

lemma PI_LO_pos : 0 < PI_LO := by
  norm_num [PI_LO]

/-- sandwich a `C / pi` quantity using only `PI_LO < pi < PI_HI`.
      Monotonicity of `a / b` in the (positive) denominator is all that is used. -/
lemma one_over_pi_bracket {C lo hi : ℝ} (hC : 0 < C)
    (hlo : lo < C / PI_HI) (hhi : C / PI_LO < hi) :
    lo < C / Real.pi ∧ C / Real.pi < hi := by
  have hpi_lo : PI_LO < Real.pi := pi_window.1
  have hpi_hi : Real.pi < PI_HI := pi_window.2
  constructor
  · have hinv : C / PI_HI < C / Real.pi := by
      exact div_lt_div_of_pos_left hC Real.pi_pos hpi_hi
    exact lt_trans hlo hinv
  · have hinv : C / Real.pi < C / PI_LO := by
      exact div_lt_div_of_pos_left hC PI_LO_pos hpi_lo
    exact lt_trans hinv hhi

/-! ## 3. (1) Monotonicity of X -/

/-- (1) `X` is strictly increasing on the positive reals. -/
theorem X_monotone {a b : ℝ} (ha : 0 < a) (hab : a < b) : X a < X b := by
  unfold X
  have hsq : a ^ 2 < b ^ 2 := sq_lt_sq_of_pos_lt ha hab
  have harg : 1 + 4 * a ^ 2 < 1 + 4 * b ^ 2 := by nlinarith
  have hnn : 0 ≤ 1 + 4 * a ^ 2 := by nlinarith [sq_nonneg a]
  have hs : Real.sqrt (1 + 4 * a ^ 2) < Real.sqrt (1 + 4 * b ^ 2) := Real.sqrt_lt_sqrt hnn harg
  nlinarith

/-! ## 4. (2)-(3) The break identity X(x_b R) = R -/

/-- `X` inverts `x_b`: because 1 + 4R(1+R) = (2R+1)^2, the budget at the break radius
    is exactly the budget ratio R.  Holds for every R > 0. -/
theorem X_x_b (R : ℝ) (hR : 0 < R) : X (x_b R) = R := by
  unfold X x_b
  have hR1 : 0 < 1 + R := by linarith
  have hnn : 0 ≤ R * (1 + R) := le_of_lt (mul_pos hR hR1)
  have hx2 : (Real.sqrt (R * (1 + R))) ^ 2 = R * (1 + R) := Real.sq_sqrt hnn
  have harg : 1 + 4 * (Real.sqrt (R * (1 + R))) ^ 2 = (2 * R + 1) ^ 2 := by
    rw [hx2]
    ring
  have hs : Real.sqrt (1 + 4 * (Real.sqrt (R * (1 + R))) ^ 2) = 2 * R + 1 := by
    rw [harg]
    exact Real.sqrt_sq (by nlinarith : (0 : ℝ) ≤ 2 * R + 1)
  rw [hs]
  ring

/-- (2) value half: at the measured budget ratio, X at the break radius equals 541/100. -/
theorem X_break_value : X (x_b (541 / 100 : ℝ)) = (541 / 100 : ℝ) := by
  exact X_x_b (541 / 100 : ℝ) (by norm_num)

/-- (2) window half: the break radius sits in (5.8887, 5.8889).
      x_b(541/100)^2 = (541/100)*(641/100) = 346781/10000, and
      5.8887^2 = 34.67678769 < 34.6781 < 34.67914321 = 5.8889^2. -/
theorem X_break_window :
    (58887 / 10000 : ℝ) < x_b (541 / 100 : ℝ) ∧
    x_b (541 / 100 : ℝ) < (58889 / 10000 : ℝ) := by
  have h := sqrt_sandwich (((541 : ℝ) / 100) * (1 + (541 : ℝ) / 100))
    ((58887 : ℝ) / 10000) ((58889 : ℝ) / 10000)
    (by norm_num) (by norm_num) (by norm_num) (by norm_num)
  unfold x_b
  exact h

/-- (2) the break theorem: value identity AND the radius window. -/
theorem X_break :
    X (x_b (541 / 100 : ℝ)) = (541 / 100 : ℝ) ∧
    (58887 / 10000 : ℝ) < x_b (541 / 100 : ℝ) ∧
    x_b (541 / 100 : ℝ) < (58889 / 10000 : ℝ) := by
  exact ⟨X_break_value, X_break_window⟩

/-- (3) demand/budget is exactly 1 at the break radius, for every R > 0. -/
theorem ratio_break {R : ℝ} (hR : 0 < R) : X (x_b R) / R = 1 := by
  rw [X_x_b R hR]
  field_simp [ne_of_gt hR]

/-- (3) instantiated at the measured budget ratio. -/
theorem ratio_break_Rb : X (x_b R_b) / R_b = 1 := by
  exact ratio_break (by unfold R_b; norm_num)

/-! ## 5. (4) demand/budget at the four FLD1 radii -/

/-- FLD1 radius 1: x = 21.45, demand/budget in (3.87, 3.88). -/
theorem demand_over_budget_21p45 :
    (387 / 100 : ℝ) < X (2145 / 100 : ℝ) / R_b ∧
    X (2145 / 100 : ℝ) / R_b < (388 / 100 : ℝ) := by
  have h := sqrt_sandwich (1 + 4 * (2145 / 100 : ℝ) ^ 2) (4291 / 100 : ℝ) (4292 / 100 : ℝ)
    (by norm_num) (by norm_num) (by norm_num) (by norm_num)
  unfold X R_b
  constructor <;> nlinarith [h.1, h.2]

/-- FLD1 radius 2: x = 41.98, demand/budget in (7.66, 7.67). -/
theorem demand_over_budget_41p98 :
    (766 / 100 : ℝ) < X (4198 / 100 : ℝ) / R_b ∧
    X (4198 / 100 : ℝ) / R_b < (767 / 100 : ℝ) := by
  have h := sqrt_sandwich (1 + 4 * (4198 / 100 : ℝ) ^ 2) (8396 / 100 : ℝ) (8397 / 100 : ℝ)
    (by norm_num) (by norm_num) (by norm_num) (by norm_num)
  unfold X R_b
  constructor <;> nlinarith [h.1, h.2]

/-- FLD1 radius 3: x = 60.00, demand/budget in (10.99, 11.00). -/
theorem demand_over_budget_60p00 :
    (1099 / 100 : ℝ) < X (60 : ℝ) / R_b ∧
    X (60 : ℝ) / R_b < (11 : ℝ) := by
  have h := sqrt_sandwich (1 + 4 * (60 : ℝ) ^ 2) (12000 / 100 : ℝ) (12001 / 100 : ℝ)
    (by norm_num) (by norm_num) (by norm_num) (by norm_num)
  unfold X R_b
  constructor <;> nlinarith [h.1, h.2]

/-- FLD1 radius 4: x = 98.32, demand/budget in (18.08, 18.09). -/
theorem demand_over_budget_98p32 :
    (1808 / 100 : ℝ) < X (9832 / 100 : ℝ) / R_b ∧
    X (9832 / 100 : ℝ) / R_b < (1809 / 100 : ℝ) := by
  have h := sqrt_sandwich (1 + 4 * (9832 / 100 : ℝ) ^ 2) (19664 / 100 : ℝ) (19665 / 100 : ℝ)
    (by norm_num) (by norm_num) (by norm_num) (by norm_num)
  unfold X R_b
  constructor <;> nlinarith [h.1, h.2]

/-- (4) all four radii at once. -/
theorem demand_over_budget :
    ((387 / 100 : ℝ) < X (2145 / 100 : ℝ) / R_b ∧ X (2145 / 100 : ℝ) / R_b < (388 / 100 : ℝ)) ∧
    ((766 / 100 : ℝ) < X (4198 / 100 : ℝ) / R_b ∧ X (4198 / 100 : ℝ) / R_b < (767 / 100 : ℝ)) ∧
    ((1099 / 100 : ℝ) < X (60 : ℝ) / R_b ∧ X (60 : ℝ) / R_b < (11 : ℝ)) ∧
    ((1808 / 100 : ℝ) < X (9832 / 100 : ℝ) / R_b ∧ X (9832 / 100 : ℝ) / R_b < (1809 / 100 : ℝ)) := by
  exact ⟨demand_over_budget_21p45, demand_over_budget_41p98,
         demand_over_budget_60p00, demand_over_budget_98p32⟩

/-! ## 6. (5) share over delivered -/

/-- (5) low footing: X_s / D_low = 59500/911 lies in (65.3, 65.4). -/
theorem share_over_delivered_low :
    (653 / 10 : ℝ) < X_s / D_low ∧ X_s / D_low < (654 / 10 : ℝ) := by
  unfold X_s D_low
  norm_num

/-- (5) high footing: X_s / D_high is exactly 42.5. -/
theorem share_over_delivered_high : X_s / D_high = (425 / 10 : ℝ) := by
  unfold X_s D_high
  norm_num

/-! ## 7. (6) the gas column -/

/- The prefactor, as an exact rational:  Sigma = pref / pi, with
     pref = a0 * pc_m^2 / (G * R(1+R) * Msun_kg)
   For a0 = A/10^p and G = B/10^g this is  A * 10^(g+4-p) * 30857^2 / (B * 346781 * 1989) * 10^-3...
   the concrete rationals below are just `norm_num`-reduced forms of the defining expression. -/

/-- prefactor, canonical a0 with the lane's G = 6.6743e-11 -/
def pref_canon_GN : ℝ := ((93603 : ℝ) * 10 * (30857 : ℝ) ^ 2) / (66743 * 346781 * 1989)
/-- prefactor, alternative a0 with the lane's G = 6.6743e-11 -/
def pref_alt_GN : ℝ := ((11312 : ℝ) * 100 * (30857 : ℝ) ^ 2) / (66743 * 346781 * 1989)
/-- prefactor, canonical a0 with the repo's G = 6.674e-11 -/
def pref_canon_gas1 : ℝ := ((93603 : ℝ) * (30857 : ℝ) ^ 2) / (6674 * 346781 * 1989)
/-- prefactor, alternative a0 with the repo's G = 6.674e-11 -/
def pref_alt_gas1 : ℝ := ((11312 : ℝ) * 10 * (30857 : ℝ) ^ 2) / (6674 * 346781 * 1989)

lemma gas_pref_canon_GN : gas_pref a0_canon G_N R_b = pref_canon_GN := by
  unfold gas_pref a0_canon G_N R_b pref_canon_GN msun_pc2 Msun_kg pc_m
  norm_num

lemma gas_pref_alt_GN : gas_pref a0_alt G_N R_b = pref_alt_GN := by
  unfold gas_pref a0_alt G_N R_b pref_alt_GN msun_pc2 Msun_kg pc_m
  norm_num

lemma gas_pref_canon_gas1 : gas_pref a0_canon G_gas1 R_b = pref_canon_gas1 := by
  unfold gas_pref a0_canon G_gas1 R_b pref_canon_gas1 msun_pc2 Msun_kg pc_m
  norm_num

lemma gas_pref_alt_gas1 : gas_pref a0_alt G_gas1 R_b = pref_alt_gas1 := by
  unfold gas_pref a0_alt G_gas1 R_b pref_alt_gas1 msun_pc2 Msun_kg pc_m
  norm_num

lemma msun_pc2_pos : 0 < msun_pc2 := by
  unfold msun_pc2 Msun_kg pc_m
  norm_num

/-- (6) canonical a0, lane G = 6.6743e-11: Sigma in (6.162, 6.163) Msun/pc^2. -/
theorem gas_column_canonical :
    (6162 / 1000 : ℝ) < gas_column a0_canon G_N R_b ∧
    gas_column a0_canon G_N R_b < (6163 / 1000 : ℝ) := by
  rw [gas_column_as_pref (by unfold R_b; norm_num : 0 < R_b)]
  rw [gas_pref_canon_GN]
  apply one_over_pi_bracket
  · norm_num [pref_canon_GN, PI_HI, PI_LO]
  · norm_num [pref_canon_GN, PI_HI, PI_LO]
  · norm_num [pref_canon_GN, PI_HI, PI_LO]

/-- (6) alternative a0, lane G = 6.6743e-11: Sigma in (7.447, 7.448) Msun/pc^2. -/
theorem gas_column_alternative :
    (7447 / 1000 : ℝ) < gas_column a0_alt G_N R_b ∧
    gas_column a0_alt G_N R_b < (7448 / 1000 : ℝ) := by
  rw [gas_column_as_pref (by unfold R_b; norm_num : 0 < R_b)]
  rw [gas_pref_alt_GN]
  apply one_over_pi_bracket
  · norm_num [pref_alt_GN, PI_HI, PI_LO]
  · norm_num [pref_alt_GN, PI_HI, PI_LO]
  · norm_num [pref_alt_GN, PI_HI, PI_LO]

/-- (6) canonical a0, repo G = 6.674e-11: Sigma in (6.162, 6.163) Msun/pc^2. -/
theorem gas_column_canonical_gas1 :
    (6162 / 1000 : ℝ) < gas_column a0_canon G_gas1 R_b ∧
    gas_column a0_canon G_gas1 R_b < (6163 / 1000 : ℝ) := by
  rw [gas_column_as_pref (by unfold R_b; norm_num : 0 < R_b)]
  rw [gas_pref_canon_gas1]
  apply one_over_pi_bracket
  · norm_num [pref_canon_gas1, PI_HI, PI_LO]
  · norm_num [pref_canon_gas1, PI_HI, PI_LO]
  · norm_num [pref_canon_gas1, PI_HI, PI_LO]

/-- (6) alternative a0, repo G = 6.674e-11: Sigma in (7.447, 7.448) Msun/pc^2. -/
theorem gas_column_alternative_gas1 :
    (7447 / 1000 : ℝ) < gas_column a0_alt G_gas1 R_b ∧
    gas_column a0_alt G_gas1 R_b < (7448 / 1000 : ℝ) := by
  rw [gas_column_as_pref (by unfold R_b; norm_num : 0 < R_b)]
  rw [gas_pref_alt_gas1]
  apply one_over_pi_bracket
  · norm_num [pref_alt_gas1, PI_HI, PI_LO]
  · norm_num [pref_alt_gas1, PI_HI, PI_LO]
  · norm_num [pref_alt_gas1, PI_HI, PI_LO]

/-! ## 7b. (6) tight 4-decimal brackets: these SEPARATE the two G choices -/

/-- (6t) canonical a0, lane G = 6.6743e-11: Sigma in (6.1624, 6.1625) Msun/pc^2. -/
theorem gas_column_canonical_tight :
    (61624 / 10000 : ℝ) < gas_column a0_canon G_N R_b ∧
    gas_column a0_canon G_N R_b < (61625 / 10000 : ℝ) := by
  rw [gas_column_as_pref (by unfold R_b; norm_num : 0 < R_b)]
  rw [gas_pref_canon_GN]
  apply one_over_pi_bracket
  · norm_num [pref_canon_GN, PI_LO]
  · norm_num [pref_canon_GN, PI_HI]
  · norm_num [pref_canon_GN, PI_LO]

/-- (6t) alternative a0, lane G = 6.6743e-11: Sigma in (7.4473, 7.4474) Msun/pc^2. -/
theorem gas_column_alternative_tight :
    (74473 / 10000 : ℝ) < gas_column a0_alt G_N R_b ∧
    gas_column a0_alt G_N R_b < (74474 / 10000 : ℝ) := by
  rw [gas_column_as_pref (by unfold R_b; norm_num : 0 < R_b)]
  rw [gas_pref_alt_GN]
  apply one_over_pi_bracket
  · norm_num [pref_alt_GN, PI_LO]
  · norm_num [pref_alt_GN, PI_HI]
  · norm_num [pref_alt_GN, PI_LO]

/-- (6t) canonical a0, repo G = 6.674e-11: Sigma in (6.1626, 6.1628), i.e. 6.1627 +- 1e-4. -/
theorem gas_column_canonical_gas1_tight :
    (61626 / 10000 : ℝ) < gas_column a0_canon G_gas1 R_b ∧
    gas_column a0_canon G_gas1 R_b < (61628 / 10000 : ℝ) := by
  rw [gas_column_as_pref (by unfold R_b; norm_num : 0 < R_b)]
  rw [gas_pref_canon_gas1]
  apply one_over_pi_bracket
  · norm_num [pref_canon_gas1, PI_LO]
  · norm_num [pref_canon_gas1, PI_HI]
  · norm_num [pref_canon_gas1, PI_LO]

/-- (6t) alternative a0, repo G = 6.674e-11: Sigma in (7.4476, 7.4478), i.e. 7.4477 +- 1e-4. -/
theorem gas_column_alternative_gas1_tight :
    (74476 / 10000 : ℝ) < gas_column a0_alt G_gas1 R_b ∧
    gas_column a0_alt G_gas1 R_b < (74478 / 10000 : ℝ) := by
  rw [gas_column_as_pref (by unfold R_b; norm_num : 0 < R_b)]
  rw [gas_pref_alt_gas1]
  apply one_over_pi_bracket
  · norm_num [pref_alt_gas1, PI_LO]
  · norm_num [pref_alt_gas1, PI_HI]
  · norm_num [pref_alt_gas1, PI_LO]


/-! ## 8. Axiom audit -/

#print axioms sq_lt_sq_of_pos_lt
#print axioms sqrt_sandwich
#print axioms x_b_sq
#print axioms gas_column_as_pref
#print axioms one_over_pi_bracket
#print axioms X_monotone
#print axioms X_x_b
#print axioms X_break_value
#print axioms X_break_window
#print axioms X_break
#print axioms ratio_break
#print axioms ratio_break_Rb
#print axioms demand_over_budget_21p45
#print axioms demand_over_budget_41p98
#print axioms demand_over_budget_60p00
#print axioms demand_over_budget_98p32
#print axioms demand_over_budget
#print axioms share_over_delivered_low
#print axioms share_over_delivered_high
#print axioms gas_pref_canon_GN
#print axioms gas_pref_alt_GN
#print axioms gas_pref_canon_gas1
#print axioms gas_pref_alt_gas1
#print axioms gas_column_canonical
#print axioms pi_window
#print axioms PI_LO_pos
#print axioms gas_column_canonical_tight
#print axioms gas_column_alternative_tight
#print axioms gas_column_canonical_gas1_tight
#print axioms gas_column_alternative_gas1_tight
#print axioms gas_column_alternative
#print axioms gas_column_canonical_gas1
#print axioms gas_column_alternative_gas1

end

end Final14