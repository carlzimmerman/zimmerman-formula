import Mathlib

/-!
# I28 — why the own-dense-set clearing statistic overstates what is left (L379)

SCOPE (per lean-math-certification): Lean certifies the MATHEMATICS. Physics inputs are hypotheses: each cell i of a
finite set carries ΛCDM's carrier c_l i > 0 and the model's carrier c_m i ≥ 0; the fixed-cell clearing is the aggregate
ratio Σ c_m / Σ c_l over all of ΛCDM's dense cells; a statistic computed only over cells SELECTED for having kept carrier
(idealised: the cells whose own retained fraction c_m i / c_l i is at least τ) is the aggregate over that subset.
Companion lane: `real_research/dark_sector_2026/L379_clearing_by_environment.py`.

* `selected_ratio_ge_tau` — over the selected cells, Σ c_m ≥ τ Σ c_l.
* `unselected_ratio_le_tau` — over the rest, Σ c_m ≤ τ Σ c_l.
* `selection_inflates_retention` — (Σ_S c_m)(Σ_all c_l) ≥ (Σ_all c_m)(Σ_S c_l): the aggregate retained fraction over the
  selected cells is at least the fixed-cell (all-cells) value, whatever τ ≥ 0 is.  Selecting cells on having kept carrier
  can only inflate the measured retention; it can never reveal clearing that the fixed cells do not show.
* `l379_instance` — L379's pooled protocluster numbers are consistent with this: an own-set value 0.552 above the
  fixed-cell 0.104.

Zero `sorry`; axioms ⊆ {propext, Classical.choice, Quot.sound}.
-/

noncomputable section

open Finset

variable {ι : Type*}

theorem selected_ratio_ge_tau (s : Finset ι) (cl cm : ι → ℝ) (τ : ℝ) :
    τ * ∑ i ∈ s.filter (fun i => τ * cl i ≤ cm i), cl i ≤ ∑ i ∈ s.filter (fun i => τ * cl i ≤ cm i), cm i := by
  rw [mul_sum]
  exact sum_le_sum (fun i hi => (mem_filter.mp hi).2)

theorem unselected_ratio_le_tau (s : Finset ι) (cl cm : ι → ℝ) (τ : ℝ) :
    ∑ i ∈ s.filter (fun i => ¬ (τ * cl i ≤ cm i)), cm i ≤ τ * ∑ i ∈ s.filter (fun i => ¬ (τ * cl i ≤ cm i)), cl i := by
  rw [mul_sum]
  exact sum_le_sum (fun i hi => le_of_lt (not_le.mp (mem_filter.mp hi).2))

theorem selection_inflates_retention (s : Finset ι) (cl cm : ι → ℝ) (τ : ℝ) (hcl : ∀ i ∈ s, 0 ≤ cl i) :
    (∑ i ∈ s, cm i) * (∑ i ∈ s.filter (fun i => τ * cl i ≤ cm i), cl i) ≤
      (∑ i ∈ s.filter (fun i => τ * cl i ≤ cm i), cm i) * (∑ i ∈ s, cl i) := by
  set p : ι → Prop := fun i => τ * cl i ≤ cm i
  have hA := selected_ratio_ge_tau s cl cm τ
  have hC := unselected_ratio_le_tau s cl cm τ
  have sm := (sum_filter_add_sum_filter_not s p cm).symm
  have sl := (sum_filter_add_sum_filter_not s p cl).symm
  have hB : 0 ≤ ∑ i ∈ s.filter p, cl i := sum_nonneg (fun i hi => hcl i (mem_filter.mp hi).1)
  have hD : 0 ≤ ∑ i ∈ s.filter (fun i => ¬ p i), cl i := sum_nonneg (fun i hi => hcl i (mem_filter.mp hi).1)
  rw [sm, sl]
  set A := ∑ i ∈ s.filter p, cm i
  set B := ∑ i ∈ s.filter p, cl i
  set C := ∑ i ∈ s.filter (fun i => ¬ p i), cm i
  set D := ∑ i ∈ s.filter (fun i => ¬ p i), cl i
  have h1 : τ * B * D ≤ A * D := mul_le_mul_of_nonneg_right hA hD
  have h2 : C * B ≤ τ * D * B := mul_le_mul_of_nonneg_right hC hB
  nlinarith [h1, h2]

theorem l379_instance : (0.104 : ℝ) < 0.552 ∧ (0.552 : ℝ) > 0.30 ∧ (0.104 : ℝ) ≤ 0.30 := by norm_num

end
