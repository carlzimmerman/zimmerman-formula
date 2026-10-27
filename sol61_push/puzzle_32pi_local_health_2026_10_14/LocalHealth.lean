import Mathlib

/-! Algebraic certificates for LOCAL32PI-001. Stationary equations and tensor
kinetic dictionary are stated premises, not formalized variational geometry.
No theorem derives the MOND coefficient or certifies nonlinear health. -/
namespace LocalHealth

/-- The same constant scalar cannot balance two distinct Euler curvatures
with a nonzero Euler-coupling derivative. -/
theorem constant_scalar_two_curvatures (v f e₁ e₂ : ℝ)
    (hne : e₁ ≠ e₂) (h₁ : v = f*e₁) (h₂ : v = f*e₂) : f = 0 := by
  have h : f*(e₁-e₂)=0 := by nlinarith
  rcases mul_eq_zero.mp h with hf | he
  · exact hf
  · exact False.elim (hne (sub_eq_zero.mp he))

/-- Scale-only P=M²a² F(R/a²): scalar and metric stationarity force F'=0.
Here y=F(x), d=F'(x), x=R/a² ≠ 0. -/
theorem scale_only_degeneracy (x y d : ℝ) (hx : x ≠ 0)
    (hs : y-x*d=0) (hg : x*d-2*y=0) : y=0 ∧ d=0 := by
  have hy : y=0 := by linarith
  constructor
  · exact hy
  · have hxd : x*d=0 := by linarith
    exact (mul_eq_zero.mp hxd).resolve_left hx

/-- Consequently this class has no stationary branch with positive F'. -/
theorem no_positive_tensor_branch (x y d : ℝ) (hx : x ≠ 0)
    (hs : y-x*d=0) (hg : x*d-2*y=0) (hd : 0<d) : False := by
  have h := (scale_only_degeneracy x y d hx hs hg).2
  linarith

/-- Explicit R²/6 replacement cancels the Einstein tensor kinetic coefficient. -/
theorem ricci_filter_zero (M C a : ℝ) (hC : C ≠ 0) (ha : a ≠ 0) :
    M^2 + (2/3:ℝ)*(-3*M^2/(16*C*a^2))*(8*C*a^2) = 0 := by
  field_simp
  ring

/-- De Sitter normalization is unchanged by the stabilizer. -/
theorem stabilizer_zero_value_slope (a μ : ℝ) :
    μ*(a-a)^2/2=0 ∧ μ*(a-a)=0 := by simp

/-- A positive stabilizer lifts the homogeneous neutral mode. -/
theorem restored_mass_positive (M a μ : ℝ) (ha : 0<a) (hμ : 0<μ) :
    0 < μ*a^2/(a^2+6*M^2) := by positivity

/-- Positive damping and restoring terms preclude a nonnegative real growth root. -/
theorem no_nonnegative_real_growth (H m r : ℝ) (hH : 0<H)
    (hm : 0 < m) (hr : 0 ≤ r) : r^2+3*H*r+m ≠ 0 := by
  have h : 0 < r^2+3*H*r+m := by positivity
  exact ne_of_gt h

/-- Stabilization alone does not protect the curvature-to-response ratio. -/
theorem ratio_drift (M C a b μ delta : ℝ) (hM : M ≠ 0) (ha : a ≠ 0) :
    (2*C*M^2*a^2 + μ*(a-b)^2/2+delta)/(M^2*a^2) =
      2*C + (μ*(a-b)^2/2+delta)/(M^2*a^2) := by
  field_simp
  ring

/-- A positive vacuum shift moves the ratio strictly upward, even with stabilization. -/
theorem positive_shift_changes_ratio (M C a b μ delta : ℝ)
    (hM : 0<M) (ha : 0<a) (hμ : 0≤μ) (hd : 0<delta) :
    2*C < (2*C*M^2*a^2 + μ*(a-b)^2/2+delta)/(M^2*a^2) := by
  rw [ratio_drift M C a b μ delta (ne_of_gt hM) (ne_of_gt ha)]
  have h : 0 < (μ*(a-b)^2/2+delta)/(M^2*a^2) := by positivity
  linarith


/-- Tensor gradient coefficient at an initial rest point; physical dictionary assumed. -/
noncomputable def tensorGradientAtRest (eps nu x : ℝ) : ℝ :=
  let U := 3*x^2+(eps+6)*nu*(x-1)^2/2
  let Ux := 6*x+(eps+6)*nu*(x-1)
  (eps*x^6+2*U^2-2*Ux*x^3)/(eps*x^6+(2/3:ℝ)*U^2)

/-- Exact counterexample in the small-kinetic-parameter limit. -/
theorem strong_stabilizer_limit :
    tensorGradientAtRest 0 10 (11/10) = -4419/17161 := by
  norm_num [tensorGradientAtRest]

/-- Negative tensor gradient persists for a strictly positive parameter. -/
theorem strong_stabilizer_finite :
    tensorGradientAtRest (1/1000000) 10 (11/10) < 0 := by
  norm_num [tensorGradientAtRest]

end LocalHealth
#print axioms LocalHealth.constant_scalar_two_curvatures
#print axioms LocalHealth.scale_only_degeneracy
#print axioms LocalHealth.no_positive_tensor_branch
#print axioms LocalHealth.ricci_filter_zero
#print axioms LocalHealth.stabilizer_zero_value_slope
#print axioms LocalHealth.restored_mass_positive
#print axioms LocalHealth.no_nonnegative_real_growth
#print axioms LocalHealth.ratio_drift
#print axioms LocalHealth.positive_shift_changes_ratio

#print axioms LocalHealth.strong_stabilizer_limit
#print axioms LocalHealth.strong_stabilizer_finite
