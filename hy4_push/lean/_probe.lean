import Mathlib

noncomputable section

#check Pi.div_apply
#check Pi.inv_apply
#check Pi.pow_apply

example (X : ℝ) (h1p : HasDerivAt (fun Y : ℝ => 1 + Real.sqrt Y) (1 / (2 * Real.sqrt X)) X)
    (h1ne : 1 + Real.sqrt X ≠ 0) :
    ((fun Y : ℝ => (2 : ℝ) / (1 + Real.sqrt Y)) = ((fun _ : ℝ => (2 : ℝ)) / fun Y : ℝ => 1 + Real.sqrt Y)) := by
  rfl

example (X : ℝ) (h1p : HasDerivAt (fun Y : ℝ => 1 + Real.sqrt Y) (1 / (2 * Real.sqrt X)) X)
    (h1ne : 1 + Real.sqrt X ≠ 0) :
    HasDerivAt (fun Y : ℝ => (2 : ℝ) / (1 + Real.sqrt Y))
      (-(2 * (1 / (2 * Real.sqrt X))) / (1 + Real.sqrt X) ^ 2) X := by
  have h := (hasDerivAt_const (x := X) (c := (2 : ℝ))).div h1p h1ne
  change HasDerivAt (fun Y : ℝ => (2 : ℝ) / (1 + Real.sqrt Y))
      ((0 * (1 + Real.sqrt X) - 2 * (1 / (2 * Real.sqrt X))) / (1 + Real.sqrt X) ^ 2) X at h
  convert h using 1
  ring

end
