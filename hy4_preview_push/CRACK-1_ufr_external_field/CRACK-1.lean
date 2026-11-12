/-
CRACK-1 (criteria 16bc0102de): three readings of the ultra-faint / X-COP pair. Lean statements for the algebra
the lane grades. They certify the algebra, not the physics. TEST lane; adopts nothing.
kappa = 1/2 FITTED; not theory closed.

The one sentence the three readings are graded against:
  d = log10[(1 + X_f)/(1 + X_L(g_bar))].  A formation field WEAKER than the system's own RAISES a system above
  today's law; a formation field STRONGER LOWERS it.

  XL_pos                   0 < X_L: no system is asked for a negative amount
  XL_anti                  X_L decreases with the field: a deeper formation field grants less
  d_weaker_field_raises    g_f <= g_bar gives d >= 0   (the only way a formation amount lifts a system)
  d_stronger_field_lowers  g_bar <= g_f gives d <= 0   (infall into a host's field can only lower)
  kappa_pos_le_one         0 < kappa <= 1 for z_f >= 0, alpha >= 0
  kappa_antitone_z         kappa decreases in z_f for alpha > 0  (the epoch factor is monotone)
  d_of_kappa_le_one_nonpos kappa <= 1 at g_amb,f = g_bar gives d <= 0  (the epoch factor can only lower)
  strip_lowers             f_C <= 1 with the baryons kept gives d <= 0  (stripping can only lower)
  pair_needs_source        d > 0 implies X_f > X_L(g_bar): a positive offset is a source, not a transfer
  monotone_cannot_be_valley  a < b < c with F b below both F a and F c: F is neither monotone nor antitone
-/
import Mathlib

namespace CRACK1

open Real

noncomputable def XL (gb a : ℝ) : ℝ := (Real.sqrt (1 + 4 * a / gb) - 1) / 2

noncomputable def Yof (X : ℝ) : ℝ := Real.log (1 + X) / Real.log 10

noncomputable def dof (Xf Xl : ℝ) : ℝ := Yof Xf - Yof Xl

noncomputable def kappa (zf alpha : ℝ) : ℝ := Real.exp (-3 * alpha * Real.log (1 + zf))

theorem XL_pos (gb a : ℝ) (hgb : 0 < gb) (ha : 0 < a) : 0 < XL gb a := by
  unfold XL
  have hpos : 0 < 4 * a / gb := by positivity
  have h1 : (1 : ℝ) < 1 + 4 * a / gb := by linarith
  have hs : Real.sqrt (1 : ℝ) < Real.sqrt (1 + 4 * a / gb) := Real.sqrt_lt_sqrt (by norm_num) h1
  norm_num at hs
  linarith

theorem XL_anti (gb gc a : ℝ) (hgb : 0 < gb) (_hgc : 0 < gc) (ha : 0 < a) (h : gb ≤ gc) :
    XL gc a ≤ XL gb a := by
  unfold XL
  have hA : 4 * a / gc = 4 * (a / gc) := by ring_nf
  have hB : 4 * a / gb = 4 * (a / gb) := by ring_nf
  rw [hA, hB]
  have hdiv : a / gc ≤ a / gb := div_le_div_of_nonneg_left ha.le hgb h
  have h1 : 1 + 4 * (a / gc) ≤ 1 + 4 * (a / gb) := by linarith
  have hs : Real.sqrt (1 + 4 * (a / gc)) ≤ Real.sqrt (1 + 4 * (a / gb)) := Real.sqrt_le_sqrt h1
  linarith

/-- A formation field weaker than the system's own grants at least as much, so d >= 0. -/
theorem d_weaker_field_raises (gf gb a : ℝ) (hgf : 0 < gf) (hgb : 0 < gb) (ha : 0 < a) (h : gf ≤ gb) :
    0 ≤ dof (XL gf a) (XL gb a) := by
  unfold dof Yof
  have hxl : XL gb a ≤ XL gf a := XL_anti gf gb a hgf hgb ha h
  have hpos : 0 < 1 + XL gb a := by have := XL_pos gb a hgb ha; linarith
  have h1 : 1 + XL gb a ≤ 1 + XL gf a := by linarith
  have hl : Real.log (1 + XL gb a) ≤ Real.log (1 + XL gf a) := Real.log_le_log hpos h1
  have hden : 0 < Real.log 10 := Real.log_pos (by norm_num)
  exact sub_nonneg.mpr (div_le_div_of_nonneg_right hl hden.le)

/-- A formation field stronger than the system's own (infall into a host) grants no more, so d <= 0. -/
theorem d_stronger_field_lowers (gf gb a : ℝ) (hgf : 0 < gf) (hgb : 0 < gb) (ha : 0 < a) (h : gb ≤ gf) :
    dof (XL gf a) (XL gb a) ≤ 0 := by
  unfold dof Yof
  have hxl : XL gf a ≤ XL gb a := XL_anti gb gf a hgb hgf ha h
  have hpos : 0 < 1 + XL gf a := by have := XL_pos gf a hgf ha; linarith
  have h1 : 1 + XL gf a ≤ 1 + XL gb a := by linarith
  have hl : Real.log (1 + XL gf a) ≤ Real.log (1 + XL gb a) := Real.log_le_log hpos h1
  have hden : 0 < Real.log 10 := Real.log_pos (by norm_num)
  exact sub_nonpos.mpr (div_le_div_of_nonneg_right hl hden.le)

theorem kappa_pos_le_one (zf alpha : ℝ) (hzf : 0 ≤ zf) (ha : 0 ≤ alpha) :
    0 < kappa zf alpha ∧ kappa zf alpha ≤ 1 := by
  unfold kappa
  constructor
  · exact Real.exp_pos _
  · apply (Real.exp_le_one_iff).2
    have hl : 0 ≤ Real.log (1 + zf) := Real.log_nonneg (by linarith)
    nlinarith

theorem kappa_antitone_z (zf zg alpha : ℝ) (hzf : 0 ≤ zf) (_hzg : 0 ≤ zg) (ha : 0 < alpha) (h : zf ≤ zg) :
    kappa zg alpha ≤ kappa zf alpha := by
  unfold kappa
  apply Real.exp_le_exp.mpr
  have hpos : 0 < 1 + zf := by linarith
  have hl : Real.log (1 + zf) ≤ Real.log (1 + zg) := Real.log_le_log hpos (by linarith)
  nlinarith

/-- The epoch factor can only lower: kappa <= 1 at the system's own field gives d <= 0. -/
theorem d_of_kappa_le_one_nonpos (Xl k : ℝ) (hXl : 0 ≤ Xl) (hk0 : 0 ≤ k) (hk1 : k ≤ 1) :
    dof (k * Xl) Xl ≤ 0 := by
  unfold dof Yof
  have hm : k * Xl ≤ 1 * Xl := mul_le_mul_of_nonneg_right hk1 hXl
  have h1 : 1 + k * Xl ≤ 1 + Xl := by linarith
  have hpos : 0 < 1 + k * Xl := by nlinarith [mul_nonneg hk0 hXl]
  have hl : Real.log (1 + k * Xl) ≤ Real.log (1 + Xl) := Real.log_le_log hpos h1
  have hden : 0 < Real.log 10 := Real.log_pos (by norm_num)
  exact sub_nonpos.mpr (div_le_div_of_nonneg_right hl hden.le)

/-- Stripping can only lower: f_C <= 1 with the baryons kept. -/
theorem strip_lowers (Xl fC : ℝ) (hXl : 0 ≤ Xl) (hfC0 : 0 ≤ fC) (hfC1 : fC ≤ 1) :
    dof (Xl * fC) Xl ≤ 0 := by
  unfold dof Yof
  have hm : Xl * fC ≤ Xl * 1 := mul_le_mul_of_nonneg_left hfC1 hXl
  have h1 : 1 + Xl * fC ≤ 1 + Xl := by linarith
  have hpos : 0 < 1 + Xl * fC := by nlinarith [mul_nonneg hXl hfC0]
  have hl : Real.log (1 + Xl * fC) ≤ Real.log (1 + Xl) := Real.log_le_log hpos h1
  have hden : 0 < Real.log 10 := Real.log_pos (by norm_num)
  exact sub_nonpos.mpr (div_le_div_of_nonneg_right hl hden.le)

/-- A positive offset is a source, not a transfer: the amount exceeds what today's law grants. -/
theorem pair_needs_source (Xf Xl : ℝ) (hXf : 0 ≤ Xf) (hXl : 0 ≤ Xl) (hd : 0 < dof Xf Xl) : Xl < Xf := by
  unfold dof Yof at hd
  have hden : 0 < Real.log 10 := Real.log_pos (by norm_num)
  have hlog : Real.log (1 + Xl) < Real.log (1 + Xf) := by
    have h := mul_lt_mul_of_pos_right hd hden
    field_simp [hden.ne'] at h
    linarith
  have hposl : 0 < 1 + Xl := by linarith
  have hposf : 0 < 1 + Xf := by linarith
  have hlt := (Real.log_lt_log_iff hposl hposf).mp hlog
  linarith

/-- A valley cannot be monotone: the U-shape the pair measures excludes every monotone formation map. -/
theorem monotone_cannot_be_valley (a b c : ℝ) (hab : a < b) (hbc : b < c) (F : ℝ → ℝ)
    (hlo : F b < F a) (hhi : F b < F c) :
    ¬ Monotone F ∧ ¬ Antitone F := by
  constructor
  · intro hm
    have h1 : F a ≤ F b := hm hab.le
    linarith
  · intro hm
    have h1 : F c ≤ F b := hm hbc.le
    linarith

end CRACK1

#print axioms CRACK1.XL_pos
#print axioms CRACK1.XL_anti
#print axioms CRACK1.d_weaker_field_raises
#print axioms CRACK1.d_stronger_field_lowers
#print axioms CRACK1.kappa_pos_le_one
#print axioms CRACK1.kappa_antitone_z
#print axioms CRACK1.d_of_kappa_le_one_nonpos
#print axioms CRACK1.strip_lowers
#print axioms CRACK1.pair_needs_source
#print axioms CRACK1.monotone_cannot_be_valley

-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
