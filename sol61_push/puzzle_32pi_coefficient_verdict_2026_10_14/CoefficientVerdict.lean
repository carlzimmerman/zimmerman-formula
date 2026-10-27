import Mathlib

/-! Exact countermodels for the reduced premises, not full cosmological solutions.
The mapping from physical vacuum stress to lambda is an explicit premise. -/
namespace CoefficientVerdict

noncomputable def potential (C a K u : ℝ) : ℝ :=
  a^2/K*(C-u/a-Real.log (1-u/a))

theorem potential_shift (C d a K u : ℝ) :
    potential (C+d) a K u = potential C a K u + d*a^2/K := by
  unfold potential
  ring

theorem same_derivative (C d a K u slope : ℝ)
    (h : HasDerivAt (potential C a K) slope u) :
    HasDerivAt (potential (C+d) a K) slope u := by
  have he : potential (C+d) a K = fun v => potential C a K v+d*a^2/K := by
    funext v
    exact potential_shift C d a K v
  rw [he]
  exact h.add_const _

noncomputable def areaProduct (C a : ℝ) : ℝ := (Real.pi/a^2)*(2*C*a^2)

theorem area_formula (C a : ℝ) (ha : a ≠ 0) :
    areaProduct C a = 2*Real.pi*C := by
  unfold areaProduct
  field_simp

/-- Every positive product is allowed by this reduced vacuum normalization. -/
theorem arbitrary_positive_product (a target : ℝ) (ha : 0<a) (ht : 0<target) :
    ∃ C : ℝ, 0<C ∧ areaProduct C a=target := by
  refine ⟨target/(2*Real.pi), by positivity, ?_⟩
  rw [area_formula _ _ (ne_of_gt ha)]
  field_simp

/-- A positive offset with the same derivative law violates the target. -/
theorem explicit_counterexample (a : ℝ) (ha : 0<a) :
    0 < 8*Real.pi ∧ areaProduct (8*Real.pi) a ≠ 32*Real.pi^2 := by
  constructor
  · positivity
  rw [area_formula _ _ (ne_of_gt ha)]
  have hp : 0<Real.pi^2 := sq_pos_of_pos Real.pi_pos
  nlinarith

theorem target_iff_chosen_constant (C a : ℝ) (ha : a ≠ 0) :
    areaProduct C a=32*Real.pi^2 ↔ C=16*Real.pi := by
  rw [area_formula _ _ ha]
  constructor
  · intro h
    have hp := Real.pi_pos
    nlinarith
  · intro h
    rw [h]
    ring

/-- Euler integral on round S4, independent of positive lambda. -/
theorem euler_independent (L : ℝ) (hL : L ≠ 0) :
    ((8/3:ℝ)*L^2)*(24*Real.pi^2/L^2)=64*Real.pi^2 := by
  field_simp
  ring

theorem dust_and_vacuum (rho : ℝ) :
    rho+(-rho)/2=rho/2 ∧ rho+(-4*rho)/2= -rho := by
  constructor <;> ring

/-- The familiar half is already part of Newtonian normalization. -/
theorem newton_normalization (G rho pressure : ℝ) :
    8*Real.pi*G*((rho+3*pressure)/2)=4*Real.pi*G*(rho+3*pressure) := by
  ring

theorem averaged_coefficient_not_target :
    (24:ℝ)*Real.pi ≠ 32*Real.pi := by
  have hp := Real.pi_pos
  linarith

#print axioms potential_shift
#print axioms same_derivative
#print axioms area_formula
#print axioms arbitrary_positive_product
#print axioms explicit_counterexample
#print axioms target_iff_chosen_constant
#print axioms euler_independent
#print axioms dust_and_vacuum
#print axioms newton_normalization
#print axioms averaged_coefficient_not_target
end CoefficientVerdict
