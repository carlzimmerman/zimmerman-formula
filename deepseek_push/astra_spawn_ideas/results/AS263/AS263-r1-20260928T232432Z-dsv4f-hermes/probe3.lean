import Mathlib
open scoped BigOperators
noncomputable section
open Finset

example {n : ℕ} (w : Fin n → ℝ → ℝ) (z : Fin n → ℝ → ℝ) :
    (fun t : ℝ => (Finset.univ.sum (fun i : Fin n => w i t * z i t)))
      = (Finset.univ.sum (fun i : Fin n => fun t : ℝ => w i t * z i t)) := by
  ext t
  simp only [Finset.sum_apply]

example {n : ℕ} (w : Fin n → ℝ → ℝ) (z : Fin n → ℝ → ℝ) (t : ℝ) :
    (Finset.univ.sum (fun i : Fin n => w i t * z i t))
      = (Finset.univ.sum (fun i : Fin n => fun t : ℝ => w i t * z i t)) t := by
  simp only [Finset.sum_apply]