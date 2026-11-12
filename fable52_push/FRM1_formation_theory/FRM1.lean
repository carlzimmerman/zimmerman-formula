/-
FRM1 (criteria 462eaa806d+fed1bc94a4): the formation reading as a theory. Lean statements for the algebra the
lane uses. They certify the algebra, not the physics. TEST lane; adopts nothing.
kappa = 1/2 FITTED; not theory closed.

  XL_pos              the law's amount is positive at every field: no system is asked for negative mass
  XL_le_sqrt          X_L <= sqrt(a0/g_bar): the amount the law grants at a field is bounded by that field
  XL_anti             X_L decreases with the field: a deeper formation field grants less
  charge_nonneg       the transferred charge is non-negative: X = X_f f_C/f_b >= 0
  strip_lowers        f_C <= 1 lowers X below what formation gave (stripping only removes)
  baryon_loss_raises  f_b <= 1 with g_bar = f_b g_b,f puts X above the law's present demand
                      (the only channel that raises a system, and it is this way round)
  Y_nonneg            X >= 0 gives Y >= 0, so the floor under d is -Y_L
-/
import Mathlib

namespace FRM1

open Real

noncomputable def XL (gb a : ℝ) : ℝ := (Real.sqrt (1 + 4 * a / gb) - 1) / 2

noncomputable def Yof (X : ℝ) : ℝ := Real.log (1 + X) / Real.log 10

theorem XL_pos (gb a : ℝ) (hgb : 0 < gb) (ha : 0 < a) : 0 < XL gb a := by
  unfold XL
  have hpos : 0 < 4 * a / gb := by positivity
  have h1 : (1 : ℝ) < 1 + 4 * a / gb := by linarith
  have hs : Real.sqrt (1 : ℝ) < Real.sqrt (1 + 4 * a / gb) := Real.sqrt_lt_sqrt (by norm_num) h1
  norm_num at hs
  linarith

theorem XL_le_sqrt (gb a : ℝ) (hgb : 0 < gb) (ha : 0 < a) : XL gb a ≤ Real.sqrt (a / gb) := by
  unfold XL
  have hn : 4 * a / gb = 4 * (a / gb) := by ring_nf
  rw [hn]
  set u := a / gb with hu
  set t := Real.sqrt u with ht
  set s := Real.sqrt (1 + 4 * u) with hs
  have hu0 : 0 ≤ u := by rw [hu]; positivity
  have ht0 : 0 ≤ t := by rw [ht]; exact Real.sqrt_nonneg u
  have hs0 : 0 ≤ s := by rw [hs]; exact Real.sqrt_nonneg _
  have ht2 : t ^ 2 = u := by rw [ht]; exact Real.sq_sqrt hu0
  have harg : 0 ≤ 1 + 4 * u := by nlinarith [hu0]
  have hs2 : s ^ 2 = 1 + 4 * u := by rw [hs]; exact Real.sq_sqrt harg
  have hsq : s ^ 2 ≤ (1 + 2 * t) ^ 2 := by nlinarith [hs2, ht2, ht0]
  have habs : |s| ≤ |1 + 2 * t| := sq_le_sq.mp hsq
  have hb : 0 ≤ 1 + 2 * t := by nlinarith [ht0]
  have hle : s ≤ 1 + 2 * t := by rwa [abs_of_nonneg hs0, abs_of_nonneg hb] at habs
  change (s - 1) / 2 ≤ t
  nlinarith

theorem XL_anti (gb gc a : ℝ) (hgb : 0 < gb) (hgc : 0 < gc) (ha : 0 < a) (h : gb ≤ gc) :
    XL gc a ≤ XL gb a := by
  unfold XL
  have _ : 0 < gc := hgc
  have hA : 4 * a / gc = 4 * (a / gc) := by ring_nf
  have hB : 4 * a / gb = 4 * (a / gb) := by ring_nf
  rw [hA, hB]
  have hdiv : a / gc ≤ a / gb := div_le_div_of_nonneg_left ha.le hgb h
  have h1 : 1 + 4 * (a / gc) ≤ 1 + 4 * (a / gb) := by linarith
  have hs : Real.sqrt (1 + 4 * (a / gc)) ≤ Real.sqrt (1 + 4 * (a / gb)) := Real.sqrt_le_sqrt h1
  linarith

theorem charge_nonneg (Xf fC fb : ℝ) (hXf : 0 ≤ Xf) (hfC : 0 ≤ fC) (hfb : 0 < fb) :
    0 ≤ Xf * fC / fb := by
  positivity

theorem strip_lowers (Xf fC fb : ℝ) (hXf : 0 ≤ Xf) (hfC1 : fC ≤ 1) (hfb : 0 < fb) :
    Xf * fC / fb ≤ Xf / fb := by
  have hm : Xf * fC ≤ Xf * 1 := mul_le_mul_of_nonneg_left hfC1 hXf
  have hinv : 0 ≤ fb⁻¹ := by positivity
  have h := mul_le_mul_of_nonneg_right hm hinv
  simpa [div_eq_mul_inv] using h

theorem baryon_loss_raises_u (u fb : ℝ) (hu : 0 ≤ u) (hfb0 : 0 < fb) (hfb1 : fb ≤ 1) :
    fb * ((Real.sqrt (1 + 4 * (u / fb)) - 1) / 2) ≤ (Real.sqrt (1 + 4 * u) - 1) / 2 := by
  set s := Real.sqrt (1 + 4 * (u / fb)) with hs
  set r := Real.sqrt (1 + 4 * u) with hr
  have h0s : 0 ≤ 1 + 4 * (u / fb) := by positivity
  have h0r : 0 ≤ 1 + 4 * u := by nlinarith [hu]
  have hs2 : s ^ 2 = 1 + 4 * (u / fb) := by rw [hs]; exact Real.sq_sqrt h0s
  have hr2 : r ^ 2 = 1 + 4 * u := by rw [hr]; exact Real.sq_sqrt h0r
  have hs0 : 0 ≤ s := by rw [hs]; exact Real.sqrt_nonneg _
  have hr0 : 0 ≤ r := by rw [hr]; exact Real.sqrt_nonneg _
  have hr_ge1 : 1 ≤ r := by
    have h1 : (1 : ℝ) ≤ 1 + 4 * u := by nlinarith [hu]
    have h2 : Real.sqrt (1 : ℝ) ≤ Real.sqrt (1 + 4 * u) := Real.sqrt_le_sqrt h1
    have h3 : (1 : ℝ) ≤ Real.sqrt (1 + 4 * u) := by simpa [Real.sqrt_one] using h2
    simpa [hr] using h3
  have hkey : r ≤ 1 + 2 * u := by
    have hb : 0 ≤ 1 + 2 * u := by nlinarith [hu]
    have hsq : r ^ 2 ≤ (1 + 2 * u) ^ 2 := by rw [hr2]; nlinarith [sq_nonneg u]
    have habs : |r| ≤ |1 + 2 * u| := sq_le_sq.mp hsq
    rwa [abs_of_nonneg hr0, abs_of_nonneg hb] at habs
  have hL0 : 0 ≤ fb * s := by positivity
  have hR0 : 0 ≤ r + fb - 1 := by nlinarith [hr_ge1, hfb0]
  have hsq2 : (fb * s) ^ 2 ≤ (r + fb - 1) ^ 2 := by
    have hmul : fb ^ 2 * (u / fb) = u * fb := by field_simp [hfb0.ne']
    have hd : 0 ≤ 1 - fb := by linarith
    have hkd : 0 ≤ (1 - fb) * (1 + 2 * u - r) := mul_nonneg hd (by nlinarith [hkey])
    nlinarith [hs2, hr2, hmul, hkd]
  have habs2 : |fb * s| ≤ |r + fb - 1| := sq_le_sq.mp hsq2
  have hle : fb * s ≤ r + fb - 1 := by rwa [abs_of_nonneg hL0, abs_of_nonneg hR0] at habs2
  nlinarith

theorem baryon_loss_raises (a gf fb : ℝ) (ha : 0 < a) (hgf : 0 < gf) (hfb0 : 0 < fb) (hfb1 : fb ≤ 1) :
    fb * XL (fb * gf) a ≤ XL gf a := by
  unfold XL
  have hsplit : 4 * a / (fb * gf) = 4 * ((a / gf) / fb) := by field_simp [hfb0.ne', hgf.ne']
  have hsplit2 : 4 * a / gf = 4 * (a / gf) := by ring_nf
  rw [hsplit, hsplit2]
  exact baryon_loss_raises_u (a / gf) fb (by positivity) hfb0 hfb1

theorem Y_nonneg (X : ℝ) (hX : 0 ≤ X) : 0 ≤ Yof X := by
  unfold Yof
  have h1 : (1 : ℝ) ≤ 1 + X := by linarith
  have hl : 0 ≤ Real.log (1 + X) := Real.log_nonneg h1
  have hden : 0 < Real.log 10 := Real.log_pos (by norm_num)
  exact div_nonneg hl hden.le

end FRM1

#print axioms FRM1.XL_pos
#print axioms FRM1.XL_le_sqrt
#print axioms FRM1.XL_anti
#print axioms FRM1.charge_nonneg
#print axioms FRM1.strip_lowers
#print axioms FRM1.baryon_loss_raises_u
#print axioms FRM1.baryon_loss_raises
#print axioms FRM1.Y_nonneg

-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
