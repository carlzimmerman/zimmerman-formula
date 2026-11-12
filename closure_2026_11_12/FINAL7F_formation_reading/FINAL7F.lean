/-
FINAL-7F (FORMATION READING): the algebra the lane's statistic rests on. It certifies the closed forms,
not the physics. TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.

  surf_dyn        the enclosed DYNAMICAL surface density M_dyn(<r)/(pi r^2) IS g_obs/(pi G):
                  correlating with log g_obs is correlating with a present-day surface density
  surf_bar        the same for the BARYONIC surface density: M_b(<r)/(pi r^2) = g_bar/(pi G)
  XL_anti_gb      X_L falls strictly as g_bar rises at fixed a0: the law's baseline is footing- and
                  field-dependent, so the residual is measured against a moving reference
  law_curve       g_bar (g + a0) = g^2 for g = g_bar (1 + X_L): the law the residual is taken against
  g_law_closed    the closed form the script uses, g = (g_bar + sqrt(g_bar^2 + 4 a0 g_bar))/2
  resid_zero_on_law  the force reading's truth (residual 0 at every point) is exactly "on the law":
                  g_obs/g_bar - 1 = X_L  <=>  g_obs = g_law(g_bar; a0)
-/
import Mathlib

namespace FINAL7F

open Real

noncomputable def XL (gb a : ℝ) : ℝ := (Real.sqrt (1 + 4 * a / gb) - 1) / 2
noncomputable def glaw (gb a : ℝ) : ℝ := gb * (1 + XL gb a)

theorem surf_dyn (gobs r G : ℝ) (hr : r ≠ 0) (hG : G ≠ 0) :
    (gobs * r ^ 2 / G) / (Real.pi * r ^ 2) = gobs / (Real.pi * G) := by
  have hr2 : r ^ 2 ≠ 0 := pow_ne_zero 2 hr
  have hpi : Real.pi ≠ 0 := ne_of_gt Real.pi_pos
  field_simp [hr2, hG, hpi]

theorem surf_bar (gb r G : ℝ) (hr : r ≠ 0) (hG : G ≠ 0) :
    (gb * r ^ 2 / G) / (Real.pi * r ^ 2) = gb / (Real.pi * G) := by
  have hr2 : r ^ 2 ≠ 0 := pow_ne_zero 2 hr
  have hpi : Real.pi ≠ 0 := ne_of_gt Real.pi_pos
  field_simp [hr2, hG, hpi]

theorem law_curve (gb a : ℝ) (hgb : 0 < gb) (ha : 0 < a) :
    gb * (glaw gb a + a) = (glaw gb a) ^ 2 := by
  unfold glaw XL
  set s := Real.sqrt (1 + 4 * a / gb) with hs
  have h0 : 0 ≤ 1 + 4 * a / gb := by positivity
  have hsq : s ^ 2 = 1 + 4 * a / gb := by rw [hs]; exact Real.sq_sqrt h0
  have key : gb * s ^ 2 = gb + 4 * a := by rw [hsq]; field_simp
  nlinarith [key]

theorem XL_anti_gb (gb1 gb2 a : ℝ) (h1 : 0 < gb1) (h2 : 0 < gb2) (ha : 0 < a)
    (h : gb1 < gb2) : XL gb2 a < XL gb1 a := by
  unfold XL
  have hinv : gb2⁻¹ < gb1⁻¹ := (inv_lt_inv₀ h2 h1).mpr h
  have h4a : 0 < 4 * a := by positivity
  have hm : (4 * a) * gb2⁻¹ < (4 * a) * gb1⁻¹ := mul_lt_mul_of_pos_left hinv h4a
  have hlt : 4 * a / gb2 < 4 * a / gb1 := by simpa [div_eq_mul_inv] using hm
  have h2' : 1 + 4 * a / gb2 < 1 + 4 * a / gb1 := by linarith
  have h0 : 0 ≤ 1 + 4 * a / gb2 := by positivity
  have hs := Real.sqrt_lt_sqrt h0 h2'
  linarith

theorem g_law_closed (gb a : ℝ) (hgb : 0 < gb) (ha : 0 < a) :
    glaw gb a = (gb + Real.sqrt (gb ^ 2 + 4 * a * gb)) / 2 := by
  unfold glaw XL
  set s := Real.sqrt (1 + 4 * a / gb) with hs
  have h0 : 0 ≤ 1 + 4 * a / gb := by positivity
  have hsq : s ^ 2 = 1 + 4 * a / gb := by rw [hs]; exact Real.sq_sqrt h0
  have harg_pos : 0 < gb ^ 2 + 4 * a * gb := by nlinarith [sq_pos_of_pos hgb, mul_pos ha hgb]
  have harg_nonneg : 0 ≤ gb ^ 2 + 4 * a * gb := le_of_lt harg_pos
  have hsq2 : (gb * s) ^ 2 = gb ^ 2 + 4 * a * gb := by
    calc
      (gb * s) ^ 2 = gb ^ 2 * s ^ 2 := by ring
      _ = gb ^ 2 * (1 + 4 * a / gb) := by rw [hsq]
      _ = gb ^ 2 + 4 * a * gb := by field_simp [ne_of_gt hgb]
  have hgs : Real.sqrt (gb ^ 2 + 4 * a * gb) = gb * s := by
    have hA : (Real.sqrt (gb ^ 2 + 4 * a * gb)) ^ 2 = (gb * s) ^ 2 := by
      rw [Real.sq_sqrt harg_nonneg, hsq2]
    rcases sq_eq_sq_iff_eq_or_eq_neg.mp hA with heq | hneg
    · exact heq
    · have hs_nonneg : 0 ≤ Real.sqrt (gb ^ 2 + 4 * a * gb) := Real.sqrt_nonneg _
      have hgs_nonneg : 0 ≤ gb * s := by
        have hs0 : 0 ≤ s := by rw [hs]; exact Real.sqrt_nonneg _
        positivity
      have hzero : Real.sqrt (gb ^ 2 + 4 * a * gb) = 0 := by nlinarith
      have hsq0 : (Real.sqrt (gb ^ 2 + 4 * a * gb)) ^ 2 = gb ^ 2 + 4 * a * gb := Real.sq_sqrt harg_nonneg
      nlinarith
  rw [hgs]
  ring

theorem resid_zero_on_law (gobs gb a : ℝ) (hgb : 0 < gb) (_ha : 0 < a) :
    (gobs / gb - 1 = XL gb a) ↔ gobs = glaw gb a := by
  unfold glaw
  constructor
  · intro h
    have : gobs / gb = 1 + XL gb a := by linarith
    have : gobs = gb * (1 + XL gb a) := by
      rw [← this]
      field_simp [ne_of_gt hgb]
    exact this
  · intro h
    rw [h]
    field_simp [ne_of_gt hgb]
    ring

end FINAL7F

#print axioms FINAL7F.surf_dyn
#print axioms FINAL7F.surf_bar
#print axioms FINAL7F.XL_anti_gb
#print axioms FINAL7F.law_curve
#print axioms FINAL7F.g_law_closed
#print axioms FINAL7F.resid_zero_on_law

-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
