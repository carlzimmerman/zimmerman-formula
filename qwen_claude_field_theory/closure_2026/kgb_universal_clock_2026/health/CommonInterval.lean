import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

/-! Conditional real-algebra certificates for already-derived local pencils.
No claim that two backgrounds share an action, or that this counts modes. -/
namespace UniversalClockHealth

theorem margin_factor (K I R c beta t : ℝ) :
    K+beta*(K-I)-2*c*t+(R-beta*(K-I))*t^2 =
    (1+beta*(1-t^2))*K-(beta*I*(1-t^2)+2*c*t-R*t^2) := by ring

theorem strict_bound_implies_margin (K I R c beta t : ℝ)
    (h : beta*I*(1-t^2)+2*c*t-R*t^2 < (1+beta*(1-t^2))*K) :
    0 < K+beta*(K-I)-2*c*t+(R-beta*(K-I))*t^2 := by
  rw [margin_factor]
  linarith

theorem common_open_interval_iff (l1 u1 l2 u2 : ℝ) :
    (∃ j : ℝ, l1 < j ∧ j < u1 ∧ l2 < j ∧ j < u2) ↔
    max l1 l2 < min u1 u2 := by
  constructor
  · rintro ⟨j,h1,h2,h3,h4⟩
    exact lt_trans (max_lt h1 h3) (lt_min h2 h4)
  · intro h
    refine ⟨(max l1 l2+min u1 u2)/2, ?_, ?_, ?_, ?_⟩
    · linarith [le_max_left l1 l2]
    · linarith [min_le_left u1 u2]
    · linarith [le_max_right l1 l2]
    · linarith [min_le_right u1 u2]

#print axioms margin_factor
#print axioms strict_bound_implies_margin
#print axioms common_open_interval_iff
end UniversalClockHealth
