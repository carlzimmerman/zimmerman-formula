import Mathlib
noncomputable section
namespace CurvatureTracking

theorem locked_ratio (lam xi z L : ℝ) (hx : 0 < xi) (hz : 0 < z)
    (h : 4*xi*L = lam*z) : L/z = lam/(4*xi) := by
  apply (div_eq_div_iff (ne_of_gt hz) (by positivity : 4*xi ≠ 0)).2
  nlinarith [h]

theorem mass_term_changes_ratio (lam xi z L h : ℝ)
    (hx : 0 < xi) (hz : 0 < z) (hh : h ≠ 0)
    (he : 4*xi*L = h+lam*z) : L/z ≠ lam/(4*xi) := by
  intro eq
  have hc := (div_eq_div_iff (ne_of_gt hz) (by positivity : 4*xi ≠ 0)).1 eq
  apply hh
  nlinarith [hc]

theorem scalar_mass_positive (M z F xi D : ℝ)
    (hm : 0 < M) (hz : 0 < z) (hf : 0 < F) (hd : 0 < D) :
    0 < 2*M^2*z*D/(F*(F+6*xi^2*z)) := by positivity

theorem target_requires_coupling (lam xi : ℝ) (hx : 0 < xi) :
    lam/(4*xi) = 32*Real.pi ↔ lam = 128*Real.pi*xi := by
  rw [div_eq_iff (by positivity : 4*xi ≠ 0)]
  constructor <;> intro h <;> nlinarith [h]

#print axioms locked_ratio
#print axioms mass_term_changes_ratio
#print axioms scalar_mass_positive
#print axioms target_requires_coupling
end CurvatureTracking
