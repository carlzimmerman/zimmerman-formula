import Mathlib.Topology.Order.IntermediateValue
import Mathlib.Topology.Algebra.Polynomial
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity

namespace ClockCharacteristic

/- The source bridge checks these coefficients against the actual action
Hessian at the rational profile event, not an assumed wave-speed formula. -/
noncomputable def p (v : ℝ) : ℝ :=
  1618128500398262*v^3 + 9256916134592200*v^2 + 5857568581738*v - 131701478915325

theorem characteristic_root_outside_metric_cone : ∃ v : ℝ, p v=0 ∧ v < -1 := by
  have hc : Continuous p := by unfold p; fun_prop
  have hlo : p (-6)<0 := by norm_num [p]
  have hhi : 0<p (-5) := by norm_num [p]
  have hz : (0:ℝ) ∈ Set.Icc (p (-6)) (p (-5)) := ⟨le_of_lt hlo,le_of_lt hhi⟩
  obtain ⟨v,hv,hroot⟩ := intermediate_value_Icc (by norm_num : (-6:ℝ)≤ -5) hc.continuousOn hz
  exact ⟨v,hroot,by have := hv.2; linarith⟩

theorem nonzero_clock_transport (A Q U : ℝ) (hA : 0<A) (hQ : 0<Q) (hU : 0<U) :
    -A*U/(A*Q+U)<0 := by
  have hn : -A*U<0 := mul_neg_of_neg_of_pos (neg_neg_of_pos hA) hU
  have hd : 0<A*Q+U := by positivity
  exact div_neg_of_neg_of_pos hn hd

#print axioms characteristic_root_outside_metric_cone
#print axioms nonzero_clock_transport
end ClockCharacteristic
