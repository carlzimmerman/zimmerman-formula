import Mathlib

noncomputable section

def f (X : ℝ) : ℝ := X - 2 * Real.log (1 + Real.sqrt X) - 2 / (1 + Real.sqrt X) + 1

def mu2 (u : ℝ) : ℝ := u * (2 + u) / (1 + u) ^ 2

example (X : ℝ) (hXne : X ≠ 0) (h1ne : 1 + Real.sqrt X ≠ 0) :
    HasDerivAt
      (fun Y : ℝ => Y - 2 * Real.log (1 + Real.sqrt Y) - 2 * (1 + Real.sqrt Y)⁻¹ + 1)
      (1 - 2 * ((1 / (2 * Real.sqrt X)) / (1 + Real.sqrt X))
         - 2 * (-((1 / (2 * Real.sqrt X)) / (1 + Real.sqrt X) ^ 2)))
      X := by
  have hsqrt : HasDerivAt (fun Y : ℝ => Real.sqrt Y) (1 / (2 * Real.sqrt X)) X :=
    Real.hasDerivAt_sqrt hXne
  have h1p : HasDerivAt (fun Y : ℝ => 1 + Real.sqrt Y) (1 / (2 * Real.sqrt X)) X :=
    hsqrt.const_add (1 : ℝ)
  have hlog : HasDerivAt (fun Y : ℝ => Real.log (1 + Real.sqrt Y))
      ((1 / (2 * Real.sqrt X)) / (1 + Real.sqrt X)) X := h1p.log h1ne
  have hlog2 : HasDerivAt (fun Y : ℝ => 2 * Real.log (1 + Real.sqrt Y))
      (2 * ((1 / (2 * Real.sqrt X)) / (1 + Real.sqrt X))) X := hlog.const_mul (2 : ℝ)
  have hinv : HasDerivAt (fun Y : ℝ => (1 + Real.sqrt Y)⁻¹)
      (-((1 / (2 * Real.sqrt X)) / (1 + Real.sqrt X) ^ 2)) X := by
    simpa only [Pi.inv_apply] using (h1p.inv h1ne)
  have hinv2 : HasDerivAt (fun Y : ℝ => 2 * (1 + Real.sqrt Y)⁻¹)
      (2 * (-((1 / (2 * Real.sqrt X)) / (1 + Real.sqrt X) ^ 2))) X :=
    hinv.const_mul (2 : ℝ)
  exact (((hasDerivAt_id X).sub hlog2).sub hinv2).add_const (1 : ℝ)

-- check the f-unfolding simp
example (X : ℝ) (hXne : X ≠ 0) (h1ne : 1 + Real.sqrt X ≠ 0)
    (hraw : HasDerivAt
      (fun Y : ℝ => Y - 2 * Real.log (1 + Real.sqrt Y) - 2 * (1 + Real.sqrt Y)⁻¹ + 1)
      (1 - 2 * ((1 / (2 * Real.sqrt X)) / (1 + Real.sqrt X))
         - 2 * (-((1 / (2 * Real.sqrt X)) / (1 + Real.sqrt X) ^ 2)))
      X) :
    HasDerivAt f
      (1 - 2 * ((1 / (2 * Real.sqrt X)) / (1 + Real.sqrt X))
         - 2 * (-((1 / (2 * Real.sqrt X)) / (1 + Real.sqrt X) ^ 2))) X := by
  simpa only [f, div_eq_mul_inv] using hraw

-- value identity
example (X : ℝ) (hspos : 0 < Real.sqrt X) (h1ne : 1 + Real.sqrt X ≠ 0) :
      1 - 2 * ((1 / (2 * Real.sqrt X)) / (1 + Real.sqrt X))
        - 2 * (-((1 / (2 * Real.sqrt X)) / (1 + Real.sqrt X) ^ 2))
      = mu2 (Real.sqrt X) := by
  have hsne : Real.sqrt X ≠ 0 := ne_of_gt hspos
  set u := Real.sqrt X with hu
  have hu_ne : u ≠ 0 := by rw [hu]; exact hsne
  have h1u : 1 + u ≠ 0 := by rw [hu]; exact h1ne
  unfold mu2
  field_simp [hu_ne, h1u]
  ring

end
