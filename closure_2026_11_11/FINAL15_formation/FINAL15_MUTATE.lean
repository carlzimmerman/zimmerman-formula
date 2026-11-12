/-
FINAL-15 (FORMATION) MUTATE twin: FALSE versions of the statements in FINAL15.lean.

This file MUST FAIL to compile. The certified statements are first re-proved here (same proofs,
renamed namespace), then each false twin is stated with its true counterpart pulled in as a
hypothesis, so every failure below is a real contradiction rather than a typo.

  M1  Newton lies above the law                  (contradicts XL_pos)
  M2  the excess exceeds its deep-field value    (contradicts XL_le_sqrt)
  M3  the defining quadratic carries a factor 2  (contradicts XL_quad)
  M4  a settled closed system is not on the law  (contradicts ledger_anchor)
  M5  recycled material carries the full share   (contradicts ledger_recycled)
  M6  stripping RAISES a system                  (contradicts strip_below)
  M7  baryon loss LOWERS a system                (contradicts loss_above)
  M8  the ledger breaches the ceiling g_c <= a0  (contradicts ceiling)

TEST lane; adopts nothing. kappa = 1/2 FITTED; not theory closed.
-/
/-
FINAL-15 (FORMATION), criteria 639e7f3b12: Lean statements for the formation ledger.

They certify the ALGEBRA of the theory written in PREREGISTER.md sections 1-3, not the physics.
u = a0 / g_bar is the dimensionless inverse field. XL is the law's ratio; led is the ledger
X = X_L(g_bar / F_b) * F_C / F_b rewritten in u (since g_b,f = g_bar/F_b implies u_f = u F_b).

  XL_pos        Newton (X = 0) lies strictly below the law at every field
  XL_quad       X_L (X_L + 1) = u: the defining quadratic of the law's static branch
  XL_nonneg     X_L >= 0
  XL_le_sqrt    X_L <= sqrt(u): the excess never exceeds the deep-field value
  XL_le_ratio   X_L <= u  (the cold pull never exceeds a0 on the law's branch)
  XL_increasing the deeper the field, the larger the excess
  XL_cross      X_L(u2) u1 <= X_L(u1) u2 for u1 <= u2: the ratio X_L/u falls with u
  ledger_anchor   F_C = 1, F_b = 1  =>  X = X_f   : a settled closed system sits ON the law
  ledger_recycled F_C = 0           =>  X = 0     : recycled material sits AT the floor
  ledger_floor    X >= 0 for every admissible transport : nothing below Newton
  strip_below     F_C <= 1, F_b = 1 =>  X <= X_f  : stripping can only lower a system
  loss_above      F_C = 1, F_b <= 1 =>  X_f <= X  : baryon loss can only raise it
  ceiling        led u 1 Fb <= u                  : the ledger respects g_c <= a0
-/
import Mathlib

namespace FINAL15_MUTATE

open Real

/-- the law's cold-to-baryon ratio at dimensionless inverse field u = a0/g_bar -/
noncomputable def XL (u : ℝ) : ℝ := (Real.sqrt (1 + 4 * u) - 1) / 2

/-- the ledger: the ratio today, after transport (F_C charge retained, F_b baryons retained) -/
noncomputable def led (u FC Fb : ℝ) : ℝ := XL (u * Fb) * FC / Fb

theorem XL_pos (u : ℝ) (hu : 0 < u) : 0 < XL u := by
  unfold XL
  have hlt : (1 : ℝ) < 1 + 4 * u := by nlinarith
  have hs := Real.sqrt_lt_sqrt (by norm_num : (0 : ℝ) ≤ 1) hlt
  rw [Real.sqrt_one] at hs
  linarith

theorem XL_quad (u : ℝ) (hu : 0 ≤ u) : XL u * XL u + XL u = u := by
  unfold XL
  have hnon : 0 ≤ 1 + 4 * u := by nlinarith
  have hs2 : (Real.sqrt (1 + 4 * u)) ^ 2 = 1 + 4 * u := Real.sq_sqrt hnon
  nlinarith

theorem XL_nonneg (u : ℝ) (hu : 0 ≤ u) : 0 ≤ XL u := by
  unfold XL
  have h1 : (1 : ℝ) ≤ 1 + 4 * u := by nlinarith
  have hs : Real.sqrt (1 : ℝ) ≤ Real.sqrt (1 + 4 * u) := Real.sqrt_le_sqrt h1
  rw [Real.sqrt_one] at hs
  linarith

theorem XL_le_sqrt (u : ℝ) (hu : 0 ≤ u) : XL u ≤ Real.sqrt u := by
  have hp : 0 ≤ XL u := XL_nonneg u hu
  rw [Real.le_sqrt hp hu]
  have hq := XL_quad u hu
  nlinarith

theorem XL_le_ratio (u : ℝ) (hu : 0 ≤ u) : XL u ≤ u := by
  have hp : 0 ≤ XL u := XL_nonneg u hu
  have hq := XL_quad u hu
  nlinarith

theorem XL_increasing (u1 u2 : ℝ) (hu1 : 0 ≤ u1) (hle : u1 ≤ u2) : XL u1 ≤ XL u2 := by
  unfold XL
  have hle2 : 1 + 4 * u1 ≤ 1 + 4 * u2 := by linarith
  have hs := Real.sqrt_le_sqrt hle2
  nlinarith

theorem XL_cross (u1 u2 : ℝ) (hu1 : 0 < u1) (hle : u1 ≤ u2) : XL u2 * u1 ≤ XL u1 * u2 := by
  have hu2 : 0 < u2 := lt_of_lt_of_le hu1 hle
  have h1 : XL u1 * (XL u1 + 1) = u1 := by nlinarith [XL_quad u1 hu1.le]
  have h2 : XL u2 * (XL u2 + 1) = u2 := by nlinarith [XL_quad u2 hu2.le]
  have ha : 0 ≤ XL u1 := XL_nonneg u1 hu1.le
  have hb : 0 ≤ XL u2 := XL_nonneg u2 hu2.le
  have hm : XL u1 ≤ XL u2 := XL_increasing u1 u2 hu1.le hle
  have hab : 0 ≤ XL u1 * XL u2 := mul_nonneg ha hb
  have hba : XL u1 - XL u2 ≤ 0 := by linarith
  have hp : (XL u1 * XL u2) * (XL u1 - XL u2) ≤ 0 := mul_nonpos_of_nonneg_of_nonpos hab hba
  nlinarith

theorem ledger_anchor (u : ℝ) : led u 1 1 = XL u := by
  unfold led; ring_nf

theorem ledger_recycled (u Fb : ℝ) : led u 0 Fb = 0 := by
  unfold led; ring

theorem ledger_floor (u FC Fb : ℝ) (hu : 0 < u) (hFC : 0 ≤ FC) (hFb : 0 < Fb) :
    0 ≤ led u FC Fb := by
  unfold led
  have hp : 0 < XL (u * Fb) := XL_pos (u * Fb) (mul_pos hu hFb)
  positivity

theorem strip_below (u FC : ℝ) (hu : 0 < u) (_hFC0 : 0 ≤ FC) (hFC1 : FC ≤ 1) :
    led u FC 1 ≤ XL u := by
  unfold led
  have hp : 0 ≤ XL u := le_of_lt (XL_pos u hu)
  ring_nf
  nlinarith

theorem loss_above (u Fb : ℝ) (hu : 0 < u) (hFb0 : 0 < Fb) (hFb1 : Fb ≤ 1) :
    XL u ≤ led u 1 Fb := by
  unfold led
  have huF : 0 < u * Fb := mul_pos hu hFb0
  have hle : u * Fb ≤ u := by nlinarith [mul_le_mul_of_nonneg_left hFb1 (le_of_lt hu)]
  have hcross : XL u * (u * Fb) ≤ XL (u * Fb) * u := XL_cross (u * Fb) u huF hle
  rw [le_div_iff₀ hFb0]
  nlinarith

theorem ceiling (u Fb : ℝ) (hu : 0 < u) (hFb : 0 < Fb) :
    led u 1 Fb ≤ u := by
  unfold led
  have hxR : XL (u * Fb) ≤ u * Fb := XL_le_ratio (u * Fb) (mul_nonneg hu.le hFb.le)
  rw [div_le_iff₀ hFb]
  nlinarith


-- ===================== the mutation arm: false twins, each MUST fail =====================

-- M1  false: Newton would lie above the law
theorem M1_newton_above (u : ℝ) (hu : 0 < u) : XL u < 0 := by
  have h := XL_pos u hu
  nlinarith

-- M2  false: the excess exceeds its deep-field value
theorem M2_above_sqrt (u : ℝ) (hu : 0 < u) : Real.sqrt u < XL u := by
  have h := XL_le_sqrt u (le_of_lt hu)
  nlinarith

-- M3  false: the defining quadratic carries a factor 2
theorem M3_quad_wrong (u : ℝ) (hu : 0 < u) : XL u * XL u + XL u = 2 * u := by
  have h := XL_quad u (le_of_lt hu)
  nlinarith

-- M4  false: a settled closed system is not on the law
theorem M4_anchor_false (u : ℝ) : led u 1 1 = 2 * XL u := by
  have h := ledger_anchor u
  nlinarith

-- M5  false: recycled material carries the full share
theorem M5_recycled_false (u Fb : ℝ) : led u 0 Fb = 1 := by
  have h := ledger_recycled u Fb
  nlinarith

-- M6  false: stripping RAISES a system above where formation put it
theorem M6_strip_raises (u FC : ℝ) (hu : 0 < u) (hFC0 : 0 ≤ FC) (hFC1 : FC ≤ 1) :
    XL u < led u FC 1 := by
  have h := strip_below u FC hu hFC0 hFC1
  nlinarith

-- M7  false: baryon loss LOWERS a system below where formation put it
theorem M7_loss_lowers (u Fb : ℝ) (hu : 0 < u) (hFb0 : 0 < Fb) (hFb1 : Fb ≤ 1) :
    led u 1 Fb < XL u := by
  have h := loss_above u Fb hu hFb0 hFb1
  nlinarith

-- M8  false: the ledger breaches the ceiling g_c <= a0
theorem M8_above_ceiling (u Fb : ℝ) (hu : 0 < u) (hFb : 0 < Fb) :
    u < led u 1 Fb := by
  have h := ceiling u Fb hu hFb
  nlinarith

end FINAL15_MUTATE

-- kappa = 1/2 FITTED; not theory closed. Adopts nothing.
