import Mathlib

-- API probe: exact signatures of the square-root / pi lemmas used by FINAL-14.
#check Real.sqrt
#check Real.sqrt_nonneg
#check Real.sq_sqrt
#check Real.sqrt_sq
#check Real.sqrt_sq_eq_abs
#check Real.sqrt_lt_sqrt
#check Real.sqrt_lt_sqrt_iff
#check Real.lt_sqrt
#check Real.sqrt_lt
#check Real.sqrt_lt'
#check Real.le_sqrt
#check Real.sqrt_le_left
#check Real.sqrt_le_sqrt
#check Real.pi_pos
#check Real.pi_gt_three
#check Real.pi_lt_four
#check Real.pi_gt_3141592
#check Real.pi_lt_3141593
#check Real.pi_gt_d2
#check sq_lt_sq
#check sq_lt_sq'
#check div_lt_div_of_pos_left
#check div_lt_div_of_pos_right
#check div_le_div_of_nonneg_left
#check abs_of_nonneg

-- small end to end smoke test of the X-inverse identity at R = 541/100
noncomputable def Xprobe (x : ℝ) : ℝ := (Real.sqrt (1 + 4 * x ^ 2) - 1) / 2
noncomputable def xbprobe (R : ℝ) : ℝ := Real.sqrt (R * (1 + R))

example : Xprobe (xbprobe (541 / 100 : ℝ)) = (541 / 100 : ℝ) := by
  have hR : (0 : ℝ) < 541 / 100 := by norm_num
  have hnonneg : (0 : ℝ) ≤ (541 / 100 : ℝ) * (1 + (541 / 100 : ℝ)) := by positivity
  have hx2 : (xbprobe (541 / 100 : ℝ)) ^ 2 = (541 / 100 : ℝ) * (1 + (541 / 100 : ℝ)) := by
    unfold xbprobe
    exact Real.sq_sqrt hnonneg
  have harg : 1 + 4 * (xbprobe (541 / 100 : ℝ)) ^ 2 = (2 * (541 / 100 : ℝ) + 1) ^ 2 := by
    rw [hx2]
    ring
  have hs : Real.sqrt (1 + 4 * (xbprobe (541 / 100 : ℝ)) ^ 2) = 2 * (541 / 100 : ℝ) + 1 := by
    rw [harg]
    exact Real.sqrt_sq (by nlinarith : (0 : ℝ) ≤ 2 * (541 / 100 : ℝ) + 1)
  unfold Xprobe
  rw [hs]
  ring
