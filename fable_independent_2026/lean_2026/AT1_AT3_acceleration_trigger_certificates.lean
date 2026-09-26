import Mathlib

/-!
# AT1–AT3 — the acceleration-triggered carrier: algebraic certificates

SCOPE. Lean certifies the algebra behind `real_research/acceleration_trigger_2026/AT1_acceleration_trigger_highz.py`
(the trigger and the trigger-independent removal bound) and `AT3_acceleration_trigger_full_gates.py` (the vacuum-gated
threshold).  The flagship, forest, S_8, X-COP, galaxy, KiDS and Harvey numbers are computed in those lanes, not here.

* `greedy_prefix_max`: for antitone weights w (the carrier orbits' time fractions inside the flagship radius, sorted
  decreasingly), any set of orbits S carries at most the weight of the first |S| orbits.
* `greedy_removal_bound`: hence if the first m orbits in that order do not reach a cut C of the inner mass, no removal
  of m or fewer orbits does -- AT1's minimum removal (ordering by time fraction inside) is the optimum for ANY trigger.
* `loss_cone_contains_interior`: an orbit currently inside r_v has its pericentre inside r_v, so the steady-state loss
  cone contains the snapshot's triggered mass (L357's in-place rule is a lower bound on the trigger's reach).
* `gate_hits_edge`: the vacuum-gated threshold y_v,eff = y_v0 E^q with q = log(0.1/y_v0)/log E(2.5)^2 equals 0.1 at
  z = 2.5 exactly (AT3's flagship edge), for any y_v0 > 0.
* `gate_monotone`: for q >= 0 the gated threshold rises with E(z)^2, i.e. into the matter era.
-/

theorem greedy_prefix_max (w : ℕ → ℝ) (hw : Antitone w) (S : Finset ℕ) :
    ∑ i ∈ S, w i ≤ ∑ i ∈ Finset.range S.card, w i := by
  induction S using Finset.induction_on_max with
  | empty => simp
  | insert a T hlt ih =>
    have haT : a ∉ T := fun h => lt_irrefl a (hlt a h)
    have hsub : T ⊆ Finset.range a := fun x hx => Finset.mem_range.mpr (hlt x hx)
    have hcard : T.card ≤ a := by simpa using Finset.card_le_card hsub
    have hwa : w a ≤ w T.card := hw hcard
    rw [Finset.sum_insert haT, Finset.card_insert_of_notMem haT, Finset.sum_range_succ]
    linarith

theorem greedy_removal_bound (w : ℕ → ℝ) (hw : Antitone w) (hw0 : ∀ i, 0 ≤ w i) (S : Finset ℕ) (C : ℝ)
    (hS : C ≤ ∑ i ∈ S, w i) (m : ℕ) (hm : ∑ i ∈ Finset.range m, w i < C) : m < S.card := by
  by_contra h
  have h' : S.card ≤ m := not_lt.mp h
  have h1 := greedy_prefix_max w hw S
  have h2 : ∑ i ∈ Finset.range S.card, w i ≤ ∑ i ∈ Finset.range m, w i :=
    Finset.sum_le_sum_of_subset_of_nonneg (Finset.range_mono h') (fun i _ _ => hw0 i)
  linarith

theorem loss_cone_contains_interior (r rp rv : ℝ) (hperi : rp ≤ r) (hin : r < rv) : rp < rv :=
  lt_of_le_of_lt hperi hin

theorem gate_hits_edge (y0 E : ℝ) (hy : 0 < y0) (hE : 1 < E) :
    y0 * E ^ (Real.log (0.1 / y0) / Real.log E) = 0.1 := by
  have hE0 : 0 < E := by linarith
  have hlogE : Real.log E ≠ 0 := ne_of_gt (Real.log_pos hE)
  rw [Real.rpow_def_of_pos hE0]
  rw [show Real.log E * (Real.log (0.1 / y0) / Real.log E) = Real.log (0.1 / y0) by field_simp]
  rw [Real.exp_log (by positivity)]
  field_simp

theorem gate_monotone (y0 q E1 E2 : ℝ) (hy : 0 ≤ y0) (hq : 0 ≤ q) (h1 : 1 ≤ E1) (h12 : E1 ≤ E2) :
    y0 * E1 ^ q ≤ y0 * E2 ^ q :=
  mul_le_mul_of_nonneg_left (Real.rpow_le_rpow (by linarith) h12 hq) hy
