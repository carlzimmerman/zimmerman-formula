import Mathlib

/-!
# ChainCert.Footing -- the kappa convention identity and the one-parameter footing family

Source: sonnet55_push/equations/eq01_kappa_convention.py and eq03_footing_lambda.py.  All statements are pure algebra.

Certified here (premises => conclusions):
* `Z = sqrt(32 pi/3) = 2 sqrt(8 pi/3)`: the 2 is 1/kappa, the sqrt(8 pi/3) is the Friedmann factor (`footing_Z_factor`);
* Milgrom's `a0 = c H/(2 pi)`, written as `kappa c sqrt(G rho)` with `rho = 3H^2/(8 pi G)`, is `kappa = sqrt(2/(3 pi))`, and that is the
  only positive kappa that does it (`footing_kappaM_iff`); `(kappa_F/kappa_M)^2 = 3 pi/8` for kappa_F = 1/2 (`footing_ratio_sq`);
* the footing family `R^2(lam) = (a + lam b u)/(a + lam b)` (a = Omega_Lambda, b = Omega_m, u = (1+z)^3): equals 1 at lam = 0
  (`foot_lam0`), equals a + b u at lam = 1 when a + b = 1 (`foot_lam1`), obeys `1 <= R^2 <= u` (`foot_bounds`), is strictly increasing in
  lam for u > 1 (`foot_strictMono`), and is independent of kappa (`foot_kappa_cancels`);
* the rise inverts in closed form: `R^2 = rho` iff `lam = a (rho - 1)/(b (u - rho))` (`foot_lambda_of_rise`, `foot_rise_of_lambda`);
* the z = 0 amplitude fixes `Omega_eff = a + lam b` and hence lam (`foot_lambda_of_Omeff`).
NOT certified: that a0 sees any matter density (lam is a parametrisation, not physics); any committed number (Omega_Lambda, H0, the SPARC
a0); kappa = 1/2 stays FITTED.
-/

open Real

theorem footing_Z_factor : Real.sqrt (32 * π / 3) = 2 * Real.sqrt (8 * π / 3) := by
  have h : (32 * π / 3) = 2 ^ 2 * (8 * π / 3) := by ring
  rw [h, Real.sqrt_mul (by positivity), Real.sqrt_sq (by norm_num)]

theorem footing_kappaM_iff {κ : ℝ} :
    κ * Real.sqrt (3 / (8 * π)) = 1 / (2 * π) ↔ κ = Real.sqrt (2 / (3 * π)) := by
  have hpi : 0 < π := Real.pi_pos
  have hs : 0 < Real.sqrt (3 / (8 * π)) := Real.sqrt_pos.mpr (by positivity)
  have key : Real.sqrt (2 / (3 * π)) * Real.sqrt (3 / (8 * π)) = 1 / (2 * π) := by
    rw [← Real.sqrt_mul (by positivity)]
    have : 2 / (3 * π) * (3 / (8 * π)) = (1 / (2 * π)) ^ 2 := by field_simp; ring
    rw [this, Real.sqrt_sq (by positivity)]
  constructor
  · intro h
    have : κ * Real.sqrt (3 / (8 * π)) = Real.sqrt (2 / (3 * π)) * Real.sqrt (3 / (8 * π)) := by rw [h, key]
    exact mul_right_cancel₀ hs.ne' this
  · intro h; rw [h, key]

theorem footing_ratio_sq : (1 / 2 : ℝ) ^ 2 / (Real.sqrt (2 / (3 * π))) ^ 2 = 3 * π / 8 := by
  have hpi : 0 < π := Real.pi_pos
  rw [Real.sq_sqrt (by positivity)]
  field_simp
  ring

noncomputable def footR2 (a b lam u : ℝ) : ℝ := (a + lam * b * u) / (a + lam * b)

theorem foot_lam0 {a b u : ℝ} (ha : 0 < a) : footR2 a b 0 u = 1 := by
  unfold footR2
  simp only [zero_mul, add_zero]
  exact div_self ha.ne'

theorem foot_lam1 {a b u : ℝ} (hab : a + b = 1) : footR2 a b 1 u = a + b * u := by
  unfold footR2
  simp only [one_mul]
  rw [hab, div_one]

theorem foot_bounds {a b lam u : ℝ} (ha : 0 < a) (hb : 0 < b) (hl : 0 ≤ lam) (hu : 1 ≤ u) :
    1 ≤ footR2 a b lam u ∧ footR2 a b lam u ≤ u := by
  have hd : 0 < a + lam * b := by positivity
  unfold footR2
  constructor
  · rw [le_div_iff₀ hd]; nlinarith [mul_nonneg hl hb.le]
  · rw [div_le_iff₀ hd]; nlinarith [mul_nonneg hl hb.le, mul_pos ha (sub_pos.mpr (lt_of_lt_of_le one_pos hu))]

theorem foot_strictMono {a b l₁ l₂ u : ℝ} (ha : 0 < a) (hb : 0 < b) (h1 : 0 ≤ l₁) (h12 : l₁ < l₂) (hu : 1 < u) :
    footR2 a b l₁ u < footR2 a b l₂ u := by
  have h2 : 0 ≤ l₂ := le_trans h1 h12.le
  have d1 : 0 < a + l₁ * b := by positivity
  have d2 : 0 < a + l₂ * b := by positivity
  unfold footR2
  rw [div_lt_div_iff₀ d1 d2]
  nlinarith [mul_pos ha hb, mul_pos (mul_pos ha hb) (sub_pos.mpr h12), sub_pos.mpr hu,
    mul_pos (mul_pos (mul_pos ha hb) (sub_pos.mpr h12)) (sub_pos.mpr hu)]

theorem foot_kappa_cancels {κ c s a b lam u : ℝ} (hk : κ ≠ 0) (hc : c ≠ 0) (hs : s ≠ 0)
    (hd : 0 < a + lam * b) (hn : 0 ≤ a + lam * b * u) :
    (κ * c * s * Real.sqrt (a + lam * b * u)) / (κ * c * s * Real.sqrt (a + lam * b)) =
      Real.sqrt (footR2 a b lam u) := by
  have hkcs : κ * c * s ≠ 0 := mul_ne_zero (mul_ne_zero hk hc) hs
  have hsd : Real.sqrt (a + lam * b) ≠ 0 := (Real.sqrt_pos.mpr hd).ne'
  rw [mul_div_mul_left _ _ hkcs, footR2, Real.sqrt_div hn]

theorem foot_lambda_of_rise {a b lam u ρ : ℝ} (ha : 0 < a) (hb : 0 < b) (hl : 0 ≤ lam) (hρu : ρ ≠ u)
    (h : footR2 a b lam u = ρ) : lam = a * (ρ - 1) / (b * (u - ρ)) := by
  have hd : 0 < a + lam * b := by positivity
  unfold footR2 at h
  rw [div_eq_iff hd.ne'] at h
  have hu : u - ρ ≠ 0 := sub_ne_zero.mpr (Ne.symm hρu)
  rw [eq_div_iff (mul_ne_zero hb.ne' hu)]
  nlinarith [h]

theorem foot_rise_of_lambda {a b u ρ : ℝ} (ha : 0 < a) (hb : 0 < b) (hρu : ρ ≠ u) (hpos : 0 ≤ a * (ρ - 1) / (b * (u - ρ))) :
    footR2 a b (a * (ρ - 1) / (b * (u - ρ))) u = ρ := by
  set lam := a * (ρ - 1) / (b * (u - ρ)) with hlam
  have hu : u - ρ ≠ 0 := sub_ne_zero.mpr (Ne.symm hρu)
  have hd : 0 < a + lam * b := by positivity
  unfold footR2
  rw [div_eq_iff hd.ne']
  have : lam * (b * (u - ρ)) = a * (ρ - 1) := by rw [hlam]; field_simp
  nlinarith [this]

theorem foot_lambda_of_Omeff {a b lam Ωe : ℝ} (hb : 0 < b) : Ωe = a + lam * b ↔ lam = (Ωe - a) / b := by
  constructor
  · intro h; rw [h]; field_simp; ring
  · intro h; rw [h]; field_simp; ring
