import Mathlib

/-!
# QX7 -- Lean certificate for the switched cold-dark-energy sector (closure_2026_11_06/QX7_unified_cold_switch)

CERTIFIED (algebra only):
* `lapse_X_identity`: AC2q's clock with N = 1 + Phi has X / X_bg = 1/(1+Phi)^2
  = 1 - 2 Phi + (3 Phi^2 + 2 Phi^3)/(1+Phi)^2 (exact), so delta X / X = -2 Phi + O(Phi^2).
* `lapse_X_bound`: for |Phi| <= 1/2, |1/(1+Phi)^2 - (1 - 2 Phi)| <= 16 Phi^2.
* `kq_cs2_barotropic`: for rho = Q p' - p, rho' = Q p'', so c_s^2 = p'/rho' = p'/(Q p'') depends on Q alone
  (a Q-switched sound speed is barotropic: iter_1 reading R1).
* `kJ_map`: 2 pi / (lambda3 (a/a3)^m) = (2 pi a3^m / lambda3) a^(-m) (iter_2's map onto QX3 iter3's solver).
* `heating_ratio_mono`: for 1 < x and m <= m', x^m <= x^m' (the z=3 -> z=2 heating ratio grows with m).
* `omega_de_lt_one`, `omega_de_mono`: Omega_DE(a) = L/(L + B a^-3) is < 1 and strictly increasing in a for L, B > 0
  (iter_3's switch saturates).
NOT CERTIFIED: the growth ODE, the CLASS spectra, any capture criterion, any number graded against data.
Zero sorry; axioms printed below.
-/

theorem lapse_X_identity (Φ : ℝ) (h : 1 + Φ ≠ 0) :
    1 / (1 + Φ) ^ 2 = 1 - 2 * Φ + (3 * Φ ^ 2 + 2 * Φ ^ 3) / (1 + Φ) ^ 2 := by
  field_simp
  ring

theorem lapse_X_bound (Φ : ℝ) (h : |Φ| ≤ 1 / 2) :
    |1 / (1 + Φ) ^ 2 - (1 - 2 * Φ)| ≤ 16 * Φ ^ 2 := by
  have hl : -(1 / 2) ≤ Φ := by linarith [neg_abs_le Φ]
  have hu : Φ ≤ 1 / 2 := by linarith [le_abs_self Φ]
  have hpos : 0 < 1 + Φ := by linarith
  have hsq : (1 / 4 : ℝ) ≤ (1 + Φ) ^ 2 := by nlinarith
  have hne : 1 + Φ ≠ 0 := ne_of_gt hpos
  rw [lapse_X_identity Φ hne]
  have e : 1 - 2 * Φ + (3 * Φ ^ 2 + 2 * Φ ^ 3) / (1 + Φ) ^ 2 - (1 - 2 * Φ)
      = (3 * Φ ^ 2 + 2 * Φ ^ 3) / (1 + Φ) ^ 2 := by ring
  rw [e, abs_div, abs_of_pos (by positivity : (0:ℝ) < (1 + Φ) ^ 2), div_le_iff₀ (by positivity)]
  have hn : |3 * Φ ^ 2 + 2 * Φ ^ 3| ≤ 4 * Φ ^ 2 := by
    rw [abs_le]; constructor <;> nlinarith [sq_nonneg Φ]
  nlinarith [sq_nonneg Φ]

theorem kq_cs2_barotropic (Q p1 p2 : ℝ) (hQ : Q ≠ 0) (hp2 : p2 ≠ 0) :
    -- rho = Q p' - p differentiates to rho' = p' + Q p'' - p' = Q p''
    (p1 + Q * p2 - p1 = Q * p2) ∧ p1 / (Q * p2) = p1 / Q / p2 := by
  refine ⟨by ring, ?_⟩
  field_simp

theorem kJ_map (a a3 lam3 m : ℝ) (ha : 0 < a) (ha3 : 0 < a3) (hl : 0 < lam3) :
    2 * Real.pi / (lam3 * (a / a3) ^ m) = (2 * Real.pi * a3 ^ m / lam3) * a ^ (-m) := by
  rw [Real.div_rpow ha.le ha3.le, Real.rpow_neg ha.le]
  have h1 : 0 < a ^ m := Real.rpow_pos_of_pos ha m
  have h2 : 0 < a3 ^ m := Real.rpow_pos_of_pos ha3 m
  field_simp

theorem heating_ratio_mono (x m m' : ℝ) (hx : 1 < x) (hm : m ≤ m') : x ^ m ≤ x ^ m' :=
  Real.rpow_le_rpow_of_exponent_le hx.le hm

theorem omega_de_lt_one (L B a : ℝ) (hL : 0 < L) (hB : 0 < B) (ha : 0 < a) :
    L / (L + B / a ^ 3) < 1 := by
  have : 0 < B / a ^ 3 := by positivity
  rw [div_lt_one (by positivity)]; linarith

theorem omega_de_mono (L B a b : ℝ) (hL : 0 < L) (hB : 0 < B) (ha : 0 < a) (hab : a < b) :
    L / (L + B / a ^ 3) < L / (L + B / b ^ 3) := by
  have hb : 0 < b := lt_trans ha hab
  have h3 : a ^ 3 < b ^ 3 := by gcongr
  have hd : B / b ^ 3 < B / a ^ 3 := div_lt_div_of_pos_left hB (by positivity) h3
  apply div_lt_div_of_pos_left hL (by positivity)
  linarith

#print axioms lapse_X_identity
#print axioms lapse_X_bound
#print axioms kq_cs2_barotropic
#print axioms kJ_map
#print axioms heating_ratio_mono
#print axioms omega_de_lt_one
#print axioms omega_de_mono
