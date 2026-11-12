/-
CRACK-1 MUTATE (criteria 16bc0102de): the false twin of CRACK-1.lean. Every statement below is the NEGATION of
one of the lane's algebraic claims, and every one must fail to compile - one error per false statement. If any of
them compiles, the corresponding theorem in CRACK-1.lean is vacuous. TEST lane; adopts nothing.
kappa = 1/2 FITTED; not theory closed.
-/
import Mathlib

namespace CRACK1_MUTATE

open Real

noncomputable def XL (gb a : ℝ) : ℝ := (Real.sqrt (1 + 4 * a / gb) - 1) / 2

noncomputable def Yof (X : ℝ) : ℝ := Real.log (1 + X) / Real.log 10

noncomputable def dof (Xf Xl : ℝ) : ℝ := Yof Xf - Yof Xl

noncomputable def kappa (zf alpha : ℝ) : ℝ := Real.exp (-3 * alpha * Real.log (1 + zf))

-- FALSE: X_L is not positive
theorem XL_pos_FALSE (gb a : ℝ) (hgb : 0 < gb) (ha : 0 < a) : XL gb a ≤ 0 := by
  unfold XL
  have hpos : 0 < 4 * a / gb := by positivity
  have h1 : (1 : ℝ) < 1 + 4 * a / gb := by linarith

-- FALSE: X_L increases with the field
theorem XL_anti_FALSE (gb gc a : ℝ) (hgb : 0 < gb) (_hgc : 0 < gc) (ha : 0 < a) (h : gb ≤ gc) :
    XL gb a ≤ XL gc a := by
  unfold XL
  have hA : 4 * a / gc = 4 * (a / gc) := by ring_nf
  have hB : 4 * a / gb = 4 * (a / gb) := by ring_nf
  rw [hA, hB]
  have hdiv : a / gc ≤ a / gb := div_le_div_of_nonneg_left ha.le hgb h

-- FALSE: a weaker formation field lowers a system
theorem d_weaker_field_raises_FALSE (gf gb a : ℝ) (hgf : 0 < gf) (hgb : 0 < gb) (ha : 0 < a) (h : gf ≤ gb) :
    dof (XL gf a) (XL gb a) ≤ 0 := by
  unfold dof Yof
  have hpos : 0 < 1 + XL gb a := by
    unfold XL
    have hpos' : 0 < 4 * a / gb := by positivity
    linarith [Real.sqrt_lt_sqrt (by norm_num : (0 : ℝ) < 1) (by linarith : (1 : ℝ) < 1 + 4 * a / gb)]
  have h1 : 1 + XL gb a ≤ 1 + XL gf a := by
    have hA : 4 * a / gf = 4 * (a / gf) := by ring_nf
    have hB : 4 * a / gb = 4 * (a / gb) := by ring_nf
    rw [hA, hB] at hpos ⊢
    have hdiv : a / gb ≤ a / gf := div_le_div_of_nonneg_left ha.le hgf h
    linarith [Real.sqrt_le_sqrt (by linarith : 1 + 4 * (a / gb) ≤ 1 + 4 * (a / gf))]

-- FALSE: infall into a host's field raises a system
theorem d_stronger_field_lowers_FALSE (gf gb a : ℝ) (hgf : 0 < gf) (hgb : 0 < gb) (ha : 0 < a) (h : gb ≤ gf) :
    0 ≤ dof (XL gf a) (XL gb a) := by
  unfold dof Yof
  have hpos : 0 < 1 + XL gf a := by
    unfold XL
    have hpos' : 0 < 4 * a / gf := by positivity
    linarith [Real.sqrt_lt_sqrt (by norm_num : (0 : ℝ) < 1) (by linarith : (1 : ℝ) < 1 + 4 * a / gf)]

-- FALSE: kappa can exceed one
theorem kappa_pos_le_one_FALSE (zf alpha : ℝ) (hzf : 0 ≤ zf) (ha : 0 ≤ alpha) :
    1 < kappa zf alpha := by
  unfold kappa
  apply (Real.exp_le_one_iff).2
  have hl : 0 ≤ Real.log (1 + zf) := Real.log_nonneg (by linarith)

-- FALSE: kappa increases with the formation redshift
theorem kappa_antitone_z_FALSE (zf zg alpha : ℝ) (hzf : 0 ≤ zf) (_hzg : 0 ≤ zg) (ha : 0 < alpha) (h : zf ≤ zg) :
    kappa zf alpha ≤ kappa zg alpha := by
  unfold kappa
  apply Real.exp_le_exp.mpr
  have hpos : 0 < 1 + zf := by linarith
  have hl : Real.log (1 + zf) ≤ Real.log (1 + zg) := Real.log_le_log hpos (by linarith)

-- FALSE: the epoch factor can raise a system
theorem d_of_kappa_le_one_nonpos_FALSE (Xl k : ℝ) (hXl : 0 ≤ Xl) (hk0 : 0 ≤ k) (hk1 : k ≤ 1) :
    0 ≤ dof (k * Xl) Xl := by
  unfold dof Yof
  have hm : k * Xl ≤ 1 * Xl := mul_le_mul_of_nonneg_right hk1 hXl
  have h1 : 1 + k * Xl ≤ 1 + Xl := by linarith

-- FALSE: stripping can raise a system
theorem strip_lowers_FALSE (Xl fC : ℝ) (hXl : 0 ≤ Xl) (hfC0 : 0 ≤ fC) (hfC1 : fC ≤ 1) :
    0 ≤ dof (Xl * fC) Xl := by
  unfold dof Yof
  have hm : Xl * fC ≤ Xl * 1 := mul_le_mul_of_nonneg_left hfC1 hXl
  have h1 : 1 + Xl * fC ≤ 1 + Xl := by linarith

-- FALSE: a positive offset can be a transfer
theorem pair_needs_source_FALSE (Xf Xl : ℝ) (hXf : 0 ≤ Xf) (hXl : 0 ≤ Xl) (hd : 0 < dof Xf Xl) : Xf ≤ Xl := by
  unfold dof Yof at hd
  have hden : 0 < Real.log 10 := Real.log_pos (by norm_num)
  have hlog : Real.log (1 + Xl) < Real.log (1 + Xf) := by
    have h := mul_lt_mul_of_pos_right hd hden
    field_simp [hden.ne'] at h
    linarith
  have hposl : 0 < 1 + Xl := by linarith
  have hposf : 0 < 1 + Xf := by linarith
  have hlt := (Real.log_lt_log_iff hposl hposf).mp hlog

-- FALSE: a valley can be monotone
theorem monotone_cannot_be_valley_FALSE (a b c : ℝ) (hab : a < b) (hbc : b < c) (F : ℝ → ℝ)
    (hlo : F b < F a) (hhi : F b < F c) : Monotone F ∨ Antitone F := by
  left
  intro x y hxy
  have h1 : F a ≤ F b := by linarith

end CRACK1_MUTATE

-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
