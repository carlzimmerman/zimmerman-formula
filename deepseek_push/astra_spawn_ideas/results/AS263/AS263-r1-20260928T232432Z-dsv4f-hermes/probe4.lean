import Mathlib
open scoped BigOperators
noncomputable section
open Finset

example {n : ℕ} (w z : Fin n → ℝ → ℝ) (A : ℝ) :
    HasDerivAt (fun t : ℝ => (Finset.univ.sum (fun i : Fin n => w i t * z i t))) A 0 →
    HasDerivAt (Finset.univ.sum (fun i : Fin n => fun t : ℝ => w i t * z i t)) A 0 := by
  intro h
  convert h using 1
  · ext t
    simp only [Finset.sum_apply]
  · rfl

example {n : ℕ} (w z : Fin n → ℝ → ℝ) (A : ℝ) :
    HasDerivAt (fun t : ℝ => (Finset.univ.sum (fun i : Fin n => w i t * z i t))) A 0 →
    HasDerivAt (Finset.univ.sum (fun i : Fin n => fun t : ℝ => w i t * z i t)) A 0 := by
  intro h
  convert h using 1
  · exact funext (fun t => by simp only [Finset.sum_apply])
  · rfl