import Mathlib
open scoped BigOperators

-- AS263 API probe (fixed): calculus + finset-sum interaction in this build
noncomputable section
open Finset

example {n : ℕ} (w z : Fin n → ℝ → ℝ) (c zd : Fin n → ℝ) (τ : ℝ)
    (hw : ∀ i, HasDerivAt (w i) (c i * w i τ) τ)
    (hz : ∀ i, HasDerivAt (z i) (zd i) τ) :
    HasDerivAt (fun t : ℝ => ∑ i, w i t * z i t)
      (∑ i : Fin n, (c i * w i τ) * z i τ + w i τ * zd i) τ := by
  have hprod : ∀ i : Fin n, HasDerivAt (fun t : ℝ => w i t * z i t)
      ((c i * w i τ) * z i τ + w i τ * zd i) τ := by
    intro i
    exact (hw i).mul (hz i)
  simpa using (HasDerivAt.sum (s := Finset.univ) (fun i _hi => hprod i))

example {n : ℕ} (w z : Fin n → ℝ → ℝ) (c zd : Fin n → ℝ) (τ : ℝ)
    (hw : ∀ i, HasDerivAt (w i) (c i * w i τ) τ)
    (hz : ∀ i, HasDerivAt (z i) (zd i) τ)
    (hW : (∑ i, w i τ) ≠ 0) :
    HasDerivAt (fun t : ℝ => (∑ i, w i t * z i t) / (∑ i, w i t))
      (((∑ i : Fin n, (c i * w i τ) * z i τ + w i τ * zd i) * (∑ i, w i τ)
           - (∑ i, w i τ * z i τ) * (∑ i, c i * w i τ)) / (∑ i, w i τ) ^ 2) τ := by
  have hN : HasDerivAt (fun t : ℝ => ∑ i, w i t * z i t)
      (∑ i : Fin n, (c i * w i τ) * z i τ + w i τ * zd i) τ := by
    have hprod : ∀ i : Fin n, HasDerivAt (fun t : ℝ => w i t * z i t)
        ((c i * w i τ) * z i τ + w i τ * zd i) τ := by
      intro i
      exact (hw i).mul (hz i)
    simpa using (HasDerivAt.sum (s := Finset.univ) (fun i _hi => hprod i))
  have hD : HasDerivAt (fun t : ℝ => ∑ i, w i t) (∑ i : Fin n, c i * w i τ) τ := by
    simpa using (HasDerivAt.sum (s := Finset.univ) (fun i _hi => hw i))
  simpa using hN.div hD hW