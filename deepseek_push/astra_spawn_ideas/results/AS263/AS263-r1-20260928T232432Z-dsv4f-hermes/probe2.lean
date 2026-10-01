import Mathlib
open scoped BigOperators

noncomputable section
open Finset

-- fixed idiom: HasDerivAt.sum gives the sum-of-functions; convert to fun t => sum...
example {n : ℕ} (w : Fin n → ℝ → ℝ) (c zd : Fin n → ℝ) (z : Fin n → ℝ → ℝ) (τ : ℝ)
    (hw : ∀ i, HasDerivAt (w i) (c i * w i τ) τ)
    (hz : ∀ i, HasDerivAt (z i) (zd i) τ) :
    HasDerivAt (fun t : ℝ => (Finset.univ.sum (fun i : Fin n => w i t * z i t)))
      (Finset.univ.sum (fun i : Fin n => (c i * w i τ) * z i τ + w i τ * zd i)) τ := by
  have hprod : ∀ i : Fin n, HasDerivAt (fun t : ℝ => w i t * z i t)
      ((c i * w i τ) * z i τ + w i τ * zd i) τ := by
    intro i
    exact (hw i).mul (hz i)
  have hS := HasDerivAt.sum (u := Finset.univ) (fun i _hi => hprod i)
  convert hS using 1
  · ext t
    simp only [Finset.sum_apply]

example {n : ℕ} (w z : Fin n → ℝ → ℝ) (c zd : Fin n → ℝ) (τ : ℝ)
    (hw : ∀ i, HasDerivAt (w i) (c i * w i τ) τ)
    (hz : ∀ i, HasDerivAt (z i) (zd i) τ)
    (hW : (Finset.univ.sum (fun i : Fin n => w i τ)) ≠ 0) :
    HasDerivAt (fun t : ℝ => (Finset.univ.sum (fun i : Fin n => w i t * z i t))
                              / (Finset.univ.sum (fun i : Fin n => w i t)))
      (((Finset.univ.sum (fun i : Fin n => (c i * w i τ) * z i τ + w i τ * zd i))
           * (Finset.univ.sum (fun i : Fin n => w i τ))
           - (Finset.univ.sum (fun i : Fin n => w i τ * z i τ))
             * (Finset.univ.sum (fun i : Fin n => c i * w i τ)))
        / (Finset.univ.sum (fun i : Fin n => w i τ)) ^ 2) τ := by
  have hN : HasDerivAt (fun t : ℝ => Finset.univ.sum (fun i : Fin n => w i t * z i t))
      (Finset.univ.sum (fun i : Fin n => (c i * w i τ) * z i τ + w i τ * zd i)) τ := by
    have hprod : ∀ i : Fin n, HasDerivAt (fun t : ℝ => w i t * z i t)
        ((c i * w i τ) * z i τ + w i τ * zd i) τ := by
      intro i
      exact (hw i).mul (hz i)
    have hS := HasDerivAt.sum (u := Finset.univ) (fun i _hi => hprod i)
    convert hS using 1
    · ext t
      simp only [Finset.sum_apply]
    · rfl
  have hD : HasDerivAt (fun t : ℝ => Finset.univ.sum (fun i : Fin n => w i t))
      (Finset.univ.sum (fun i : Fin n => c i * w i τ)) τ := by
    have hS := HasDerivAt.sum (u := Finset.univ) (fun i _hi => hw i)
    convert hS using 1
    · ext t
      simp only [Finset.sum_apply]
    · rfl
  have hdiv := hN.div hD hW
  convert hdiv using 1
  · ext t
    simp only [Finset.sum_apply]
  · rfl