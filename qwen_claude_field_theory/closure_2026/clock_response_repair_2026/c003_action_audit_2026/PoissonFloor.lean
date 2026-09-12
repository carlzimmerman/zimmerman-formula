import Mathlib.Analysis.Complex.Exponential
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring

set_option autoImplicit false

/-!
Measure-to-algebra boundary: independently marked no-event trajectories in a
prescribed common potential contribute p0 times the control mass. The physical
flow, Poisson probability law, and independence are NOT formalized here.
Given that decomposition, these are exact real-algebra/exp theorems, not a
claim of an action-derived theory or a new law of nature.
-/
namespace PoissonFloor

def retention (p0 hit : ℝ) : ℝ := p0 + (1-p0)*hit

theorem no_event_lower_bound (p0 hit : ℝ) (hp : p0 ≤ 1) (hh : 0 ≤ hit) :
    p0 ≤ retention p0 hit := by
  unfold retention
  have h := mul_nonneg (sub_nonneg.mpr hp) hh
  linarith

theorem saturation_iff_no_hit_contribution (p0 hit : ℝ) (hp : p0 < 1) :
    retention p0 hit = p0 ↔ hit = 0 := by
  unfold retention
  constructor
  · intro h
    have hm : (1-p0)*hit = 0 := by linarith
    exact (mul_eq_zero.mp hm).resolve_left (ne_of_gt (sub_pos.mpr hp))
  · intro h
    simp [h]

theorem host_difference (p0 hitA hitB : ℝ) :
    retention p0 hitA-retention p0 hitB = (1-p0)*(hitA-hitB) := by
  unfold retention
  ring

theorem exact_mean_two_floor_exceeds_spiral_ceiling :
    (21:ℝ)/200 < Real.exp (-2) := by
  have hE : Real.exp (2:ℝ) = Real.exp 1 * Real.exp 1 := by
    rw [show (2:ℝ) = 1+1 by norm_num, Real.exp_add]
  have h9 : Real.exp (2:ℝ) ≤ 9 := by
    rw [hE]
    have ha := Real.abs_exp_sub_one_sub_id_le (x := (1:ℝ)) (by norm_num)
    have hu := (abs_le.mp ha).2
    have hp := Real.exp_pos (1:ℝ)
    nlinarith
  have hm : Real.exp (-2:ℝ) * Real.exp 2 = 1 := by
    rw [← Real.exp_add]
    norm_num
  have hp := Real.exp_pos (-2:ℝ)
  have hi := mul_le_mul_of_nonneg_left h9 (le_of_lt hp)
  nlinarith

theorem mean_two_cannot_meet_original_spiral_ceiling (hit : ℝ) (hh : 0 ≤ hit) :
    ¬ retention (Real.exp (-2)) hit ≤ (21:ℝ)/200 := by
  have hp : Real.exp (-2:ℝ) ≤ 1 := by
    rw [← Real.exp_zero]
    exact Real.exp_le_exp.mpr (by norm_num)
  have hf := no_event_lower_bound (Real.exp (-2)) hit hp hh
  have hg := exact_mean_two_floor_exceeds_spiral_ceiling
  linarith

#print axioms no_event_lower_bound
#print axioms saturation_iff_no_hit_contribution
#print axioms host_difference
#print axioms exact_mean_two_floor_exceeds_spiral_ceiling
#print axioms mean_two_cannot_meet_original_spiral_ceiling
end PoissonFloor
