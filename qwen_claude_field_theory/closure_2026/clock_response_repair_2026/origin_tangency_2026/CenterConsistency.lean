import Mathlib.Data.Real.Basic
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring

/- Algebraic certificate for the center consistency diagnostic, not a gravity
   closure certificate. SymPy separately links this expression to the varied
   action; that symbolic implementation is not formalized here. -/
namespace ClockCenterConsistency
noncomputable section

def clockRate (a q wy w wt h b u : ℝ) : ℝ :=
  (b + 6*q*wy*u/a^2)/(3*w) - h*wt/w

theorem gradient_error_transport (a q wy w wt h b ud ue : ℝ)
    (ha : a ≠ 0) (hw : w ≠ 0) :
    clockRate a q wy w wt h b ud - clockRate a q wy w wt h b ue =
      (2*q*wy/(a^2*w))*(ud-ue) := by
  unfold clockRate
  field_simp [ha, hw]
  ring

/- A linear origin-jet functional L applied to a correction direction e.
   l = L(raw), weight = L(e), target is the independently derived mixed jet. -/
theorem one_sample_jet_correction (l target weight : ℝ) (hw : weight ≠ 0) :
    l + weight*((target-l)/weight) = target := by
  field_simp [hw]
  ring

#print axioms gradient_error_transport
#print axioms one_sample_jet_correction
end
end ClockCenterConsistency
