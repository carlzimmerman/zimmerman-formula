/-
FRM1_MUTATE: the false twin of FRM1.lean. One false statement per theorem of the real file; each must fail
to compile. TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.
-/
import Mathlib

namespace FRM1_MUTATE

open Real

noncomputable def XL (gb a : ℝ) : ℝ := (Real.sqrt (1 + 4 * a / gb) - 1) / 2

noncomputable def Yof (X : ℝ) : ℝ := Real.log (1 + X) / Real.log 10

-- false: the law's amount is not positive
theorem XL_nonpos (gb a : ℝ) (hgb : 0 < gb) (ha : 0 < a) : XL gb a ≤ 0 := by
  unfold XL
  have hpos : 0 < 4 * a / gb := by positivity
  have h1 : (1 : ℝ) < 1 + 4 * a / gb := by linarith
  have hs : Real.sqrt (1 : ℝ) < Real.sqrt (1 + 4 * a / gb) := Real.sqrt_lt_sqrt (by norm_num) h1
  norm_num at hs
  linarith

-- false: the amount is not bounded by sqrt(a0/g_bar), it exceeds it
theorem sqrt_le_XL (gb a : ℝ) (hgb : 0 < gb) (ha : 0 < a) : Real.sqrt (a / gb) ≤ XL gb a := by
  unfold XL
  have hn : 4 * a / gb = 4 * (a / gb) := by ring_nf
  rw [hn]
  set u := a / gb with hu
  set t := Real.sqrt u with ht
  set s := Real.sqrt (1 + 4 * u) with hs
  have hu0 : 0 ≤ u := by rw [hu]; positivity
  have ht0 : 0 ≤ t := by rw [ht]; exact Real.sqrt_nonneg u
  have ht2 : t ^ 2 = u := by rw [ht]; exact Real.sq_sqrt hu0
  have harg : 0 ≤ 1 + 4 * u := by nlinarith [hu0]
  have hs2 : s ^ 2 = 1 + 4 * u := by rw [hs]; exact Real.sq_sqrt harg
  change t ≤ (s - 1) / 2
  nlinarith [hs2, ht2, ht0]

-- false: the amount increases with the field
theorem XL_mono (gb gc a : ℝ) (hgb : 0 < gb) (hgc : 0 < gc) (ha : 0 < a) (h : gb ≤ gc) :
    XL gb a ≤ XL gc a := by
  unfold XL
  have _ : 0 < gc := hgc
  have hA : 4 * a / gc = 4 * (a / gc) := by ring_nf
  have hB : 4 * a / gb = 4 * (a / gb) := by ring_nf
  rw [hA, hB]
  have hdiv : a / gc ≤ a / gb := div_le_div_of_nonneg_left ha.le hgb h
  have h1 : 1 + 4 * (a / gc) ≤ 1 + 4 * (a / gb) := by linarith
  have hs : Real.sqrt (1 + 4 * (a / gc)) ≤ Real.sqrt (1 + 4 * (a / gb)) := Real.sqrt_le_sqrt h1
  linarith

-- false: the transferred charge can be negative
theorem charge_nonpos (Xf fC fb : ℝ) (hXf : 0 ≤ Xf) (hfC : 0 ≤ fC) (hfb : 0 < fb) :
    Xf * fC / fb ≤ 0 := by
  positivity

-- false: stripping raises X above what formation gave
theorem strip_raises (Xf fC fb : ℝ) (hXf : 0 ≤ Xf) (hfC1 : fC ≤ 1) (hfb : 0 < fb) :
    Xf / fb ≤ Xf * fC / fb := by
  have hm : Xf * fC ≤ Xf * 1 := mul_le_mul_of_nonneg_left hfC1 hXf
  have hinv : 0 ≤ fb⁻¹ := by positivity
  have h := mul_le_mul_of_nonneg_right hm hinv
  simpa [div_eq_mul_inv] using h

-- false: baryon loss puts X below the law's present demand
theorem baryon_loss_lowers (a gf fb : ℝ) (ha : 0 < a) (hgf : 0 < gf) (hfb0 : 0 < fb) (hfb1 : fb ≤ 1) :
    XL gf a ≤ fb * XL (fb * gf) a := by
  unfold XL
  have hsplit : 4 * a / (fb * gf) = 4 * ((a / gf) / fb) := by field_simp [hfb0.ne', hgf.ne']
  have hsplit2 : 4 * a / gf = 4 * (a / gf) := by ring_nf
  rw [hsplit, hsplit2]
  have hu0 : 0 ≤ a / gf := by positivity
  -- the true inequality, in the wrong direction
  set s := Real.sqrt (1 + 4 * ((a / gf) / fb)) with hs
  set r := Real.sqrt (1 + 4 * (a / gf)) with hr
  have h0s : 0 ≤ 1 + 4 * ((a / gf) / fb) := by positivity
  have h0r : 0 ≤ 1 + 4 * (a / gf) := by nlinarith [hu0]
  have hs2 : s ^ 2 = 1 + 4 * ((a / gf) / fb) := by rw [hs]; exact Real.sq_sqrt h0s
  have hr2 : r ^ 2 = 1 + 4 * (a / gf) := by rw [hr]; exact Real.sq_sqrt h0r
  nlinarith [hs2, hr2, hfb0, hfb1, hu0]

-- false: X >= 0 gives a negative Y
theorem Y_nonpos (X : ℝ) (hX : 0 ≤ X) : Yof X ≤ 0 := by
  unfold Yof
  have h1 : (1 : ℝ) ≤ 1 + X := by linarith
  have hl : 0 ≤ Real.log (1 + X) := Real.log_nonneg h1
  have hden : 0 < Real.log 10 := Real.log_pos (by norm_num)
  exact div_nonpos_of_nonneg_of_nonpos hl (by linarith : Real.log 10 ≤ 0)

end FRM1_MUTATE

-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
