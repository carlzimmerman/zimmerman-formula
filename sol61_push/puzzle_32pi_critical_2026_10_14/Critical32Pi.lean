import Mathlib

/-! Algebraic audit of a specified leading-large-N effective potential.
No theorem identifies this composite with gravitational polarization. -/
namespace Critical32Pi

theorem critical_flat (m : ℝ) :
    m^3/(24*Real.pi)*(1-(16*Real.pi^2)/(16*Real.pi^2))=0 := by
  have hp : (16:ℝ)*Real.pi^2 ≠ 0 := by positivity
  rw [div_self hp]
  ring

theorem selected_coupling (g m : ℝ) (hm : m ≠ 0)
    (hgap : m^2*(1-g/(16*Real.pi^2))=0) : g=16*Real.pi^2 := by
  have hm2 : m^2 ≠ 0 := pow_ne_zero _ hm
  have h := (mul_eq_zero.mp hgap).resolve_left hm2
  have hp : (16:ℝ)*Real.pi^2 ≠ 0 := by positivity
  have hg : g/(16*Real.pi^2)=1 := by linarith
  exact (div_eq_one_iff_eq hp).mp hg

theorem condensation_ratio (d m : ℝ) (hd : d ≠ 0) (hm : m ≠ 0) :
    (d*m^3/(12*Real.pi))*(d/(4*Real.pi))^2 /
      (d*m/(4*Real.pi))^3 = (1/3:ℝ) := by
  have hp := ne_of_gt Real.pi_pos
  field_simp
  <;> ring

theorem scaling_cancels (B D f0 f2 f3 : ℝ) (hB : B ≠ 0)
    (hD : D ≠ 0) (h2 : f2 ≠ 0) :
    (B*f0)*(B*f3/D^3)^2/(B*f2/D^2)^3=f0*f3^2/f2^3 := by
  field_simp
  <;> ring

#print axioms critical_flat
#print axioms selected_coupling
#print axioms condensation_ratio
#print axioms scaling_cancels
end Critical32Pi
