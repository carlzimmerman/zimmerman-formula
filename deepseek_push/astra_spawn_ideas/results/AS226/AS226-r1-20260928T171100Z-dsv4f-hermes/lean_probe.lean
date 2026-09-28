import Mathlib

noncomputable section
open scoped Real

-- quick API probes for this mathlib build
example (x : ℝ) : HasDerivAt (fun t : ℝ => t / 2) (1 / 2) x := by
  simpa using (hasDerivAt_id x).div_const (2 : ℝ)

example (x : ℝ) (hx : 1 - x / 2 ≠ 0) :
    HasDerivAt (fun t : ℝ => 1 / (1 - t / 2)) (1 / (2 * (1 - x / 2) ^ 2)) x := by
  have hcst : HasDerivAt (fun _ : ℝ => (1 : ℝ)) 0 x := hasDerivAt_const x 1
  have hid : HasDerivAt (fun t : ℝ => t) 1 x := hasDerivAt_id x
  have ht2 : HasDerivAt (fun t : ℝ => t / 2) (1 / 2) x := by
    simpa using hid.div_const (2 : ℝ)
  have hsub := hcst.sub ht2
  have hv : (0 : ℝ) - (1 / 2 : ℝ) = -(1 / 2 : ℝ) := by norm_num
  have hden : HasDerivAt (fun t : ℝ => 1 - t / 2) (-(1 / 2) : ℝ) x := by
    rwa [hv] at hsub
  have hdiv := hcst.div hden hx
  have hnum : 0 * (1 - x / 2) - 1 * (-(1 / 2 : ℝ)) = (1 / 2 : ℝ) := by ring
  have hdiv' : HasDerivAt (fun t : ℝ => 1 / (1 - t / 2)) ((1 / 2 : ℝ) / (1 - x / 2) ^ 2) x := by
    rwa [hnum] at hdiv
  have hv2 : (1 / 2 : ℝ) / (1 - x / 2) ^ 2 = 1 / (2 * (1 - x / 2) ^ 2) := by
    field_simp [hx]
  rw [← hv2]
  exact hdiv'

example (α : ℝ) (h : α < 2) : (1 + (1 - α / 2)) ≠ 0 := by
  have hb : (0 : ℝ) < 2 := by norm_num
  have hlt : α / 2 < 1 := by
    rw [div_lt_one hb]
    exact h
  have hgt : 1 < 1 + (1 - α / 2) := by linarith [hlt]
  have hpos2 : 0 < 1 + (1 - α / 2) := by linarith [hgt]
  exact ne_of_gt hpos2

example (α : ℝ) (h0 : 0 < α) (h2 : α < 2) : 1 < 1 / (1 - α / 2) := by
  have hd0 : 1 - α / 2 ≠ 0 := by
    have hden : (2 : ℝ) ≠ 0 := by norm_num
    have h2a : 0 < 2 - α := by nlinarith [h2]
    have hpos : 0 < (2 - α) / 2 := div_pos h2a (by norm_num : (0 : ℝ) < 2)
    have hiden : (2 - α) / 2 = 1 - α / 2 := by ring
    rw [← hiden]
    exact ne_of_gt hpos
  rw [one_div]
  have hpos : 0 < 1 - α / 2 := by
    have hden : (2 : ℝ) ≠ 0 := by norm_num
    have h2a : 0 < 2 - α := by nlinarith [h2]
    have hp : 0 < (2 - α) / 2 := div_pos h2a (by norm_num : (0 : ℝ) < 2)
    have hiden : (2 - α) / 2 = 1 - α / 2 := by ring
    rwa [← hiden]
  have hl : 1 - α / 2 < 1 := by
    have hb : (0 : ℝ) < 2 := by norm_num
    have hlt : α / 2 < 1 := by
      rw [div_lt_one hb]
      exact h2
    linarith [hlt]
  exact (one_lt_inv₀ hpos).2 hl