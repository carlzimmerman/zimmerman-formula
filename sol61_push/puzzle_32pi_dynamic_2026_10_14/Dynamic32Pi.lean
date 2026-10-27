import Mathlib

/-!
Certificates for DYNAMIC32PI-001/002, c = hbar = 1.
The FRW constraint and scalar equation are MODEL INPUTS, not derived here
from differential geometry or a covariant variational calculus.
No theorem selects beta or identifies the scalar with measured MOND a0.
-/
namespace Dynamic32Pi

noncomputable def hsq (C a : ℝ) := 2 * C * a^2 / 3
noncomputable def vp (C M a : ℝ) := 4 * C * M^2 * a
noncomputable def fp (beta M a : ℝ) := -2 * beta * M^2 / a^3
noncomputable def residual (C beta M a : ℝ) :=
  vp C M a - 24 * fp beta M a * (hsq C a)^2
noncomputable def selectedBeta (C : ℝ) := -3 / (16 * C)

/-- Eliminate the assumed Einstein vacuum equation in the scalar residual. -/
theorem residual_factor (C beta M a : ℝ) (ha : a ≠ 0) :
    residual C beta M a = 4*C*M^2*a*(1 + (16/3:ℝ)*beta*C) := by
  unfold residual vp fp hsq
  field_simp
  <;> ring

/-- On the positive branch, stationarity is equivalent to one coupling relation. -/
theorem stationary_iff (C beta M a : ℝ)
    (hC : 0 < C) (hM : 0 < M) (ha : 0 < a) :
    residual C beta M a = 0 ↔ 1 + (16/3:ℝ)*beta*C = 0 := by
  rw [residual_factor C beta M a (ne_of_gt ha)]
  have hp : 4*C*M^2*a ≠ 0 := ne_of_gt (by positivity)
  exact mul_eq_zero.trans (by simp [hp])

/-- Every positive C admits a stationary branch after a coupling choice. -/
theorem calibrated_stationary (C M a : ℝ) (hC : C ≠ 0) (ha : a ≠ 0) :
    residual C (selectedBeta C) M a = 0 := by
  rw [residual_factor C (selectedBeta C) M a ha]
  unfold selectedBeta
  field_simp
  <;> ring

/-- Lambda=3H^2 gives the ratio, conditional on the stationary relation. -/
theorem curvature_ratio (C beta a : ℝ) (hb : beta ≠ 0) (ha : a ≠ 0)
    (h : 1 + (16/3:ℝ)*beta*C = 0) :
    3 * hsq C a / a^2 = -3 / (8*beta) := by
  unfold hsq
  field_simp
  nlinarith [sq_nonneg a]

/-- The desired number is equivalent to choosing this beta, not implied without it. -/
theorem target_iff (beta : ℝ) (hb : beta ≠ 0) :
    -3 / (8*beta) = 32*Real.pi ↔ beta = -3/(256*Real.pi) := by
  have hp : Real.pi ≠ 0 := ne_of_gt Real.pi_pos
  constructor
  · intro h
    apply (eq_div_iff (by positivity : (256:ℝ)*Real.pi ≠ 0)).2
    have hh := (div_eq_iff (by exact mul_ne_zero (by norm_num) hb)).1 h
    nlinarith
  · intro h
    rw [h]
    field_simp
    <;> ring

/-- A positive stationary branch with a different curvature coefficient. -/
theorem alternative_branch :
    residual 1 (selectedBeta 1) 1 1 = 0 ∧
    3 * hsq 1 1 / (1:ℝ)^2 ≠ 32*Real.pi := by
  constructor
  · exact calibrated_stationary 1 1 1 (by norm_num) (by norm_num)
  · norm_num [hsq]
    nlinarith [Real.pi_gt_three]

noncomputable def kinetic (M a : ℝ) := 1 + 6*M^2/a^2
noncomputable def branchFp (C M a : ℝ) := 3*M^2/(8*C*a^3)
noncomputable def branchFpp (C M a : ℝ) := -9*M^2/(8*C*a^4)

/-- Algebraic elimination of the linearized lapse constraint, acceleration term. -/
theorem reduced_kinetic (C M a : ℝ) (hC : C ≠ 0) (hM : M ≠ 0) (ha : a ≠ 0) :
    1 + 96*(branchFp C M a)^2*(hsq C a)^2/M^2 = kinetic M a := by
  unfold branchFp hsq kinetic
  field_simp
  <;> ring

theorem kinetic_positive (M a : ℝ) : 0 < kinetic M a := by
  unfold kinetic
  positivity

/-- Friction divided by H is three times the reduced acceleration coefficient. -/
theorem reduced_friction (C M a : ℝ) (hC : C ≠ 0) (hM : M ≠ 0) (ha : a ≠ 0) :
    3 + 384*(branchFp C M a)^2*(hsq C a)^2/M^2 -
      4*branchFp C M a*vp C M a/M^2 = 3*kinetic M a := by
  unfold branchFp hsq vp kinetic
  field_simp
  <;> ring

/-- The coupled homogeneous restoring coefficient vanishes exactly. -/
theorem reduced_mass_zero (C M a : ℝ) (hC : C ≠ 0) (hM : M ≠ 0) (ha : a ≠ 0) :
    4*C*M^2 - 24*branchFpp C M a*(hsq C a)^2 -
      16*branchFp C M a*hsq C a*vp C M a/M^2 = 0 := by
  unfold branchFp branchFpp hsq vp
  field_simp
  <;> ring

/-- Every constant perturbation solves the supplied reduced ODE: a neutral mode. -/
theorem neutral_constant_mode (q H M a t : ℝ) :
    kinetic M a * deriv (deriv (fun _ : ℝ => q)) t +
      3*H*kinetic M a * deriv (fun _ : ℝ => q) t = 0 := by
  simp

noncomputable def shiftedResidual (C M a delta : ℝ) :=
  vp C M a - (8/3:ℝ)*branchFp C M a*(2*C*M^2*a^2+delta)^2/M^4

/-- Exact constant-vacuum-shift residual after eliminating the metric constraint. -/
theorem shift_factor (C M a delta : ℝ)
    (hC : C ≠ 0) (hM : M ≠ 0) (ha : a ≠ 0) :
    shiftedResidual C M a delta =
      -delta*(4*C*M^2*a^2+delta)/(C*M^2*a^3) := by
  unfold shiftedResidual vp branchFp
  field_simp
  <;> ring

/-- Any strictly positive added vacuum energy destroys this finite positive branch. -/
theorem positive_shift_obstruction (C M a delta : ℝ)
    (hC : 0 < C) (hM : 0 < M) (ha : 0 < a) (hd : 0 < delta) :
    shiftedResidual C M a delta < 0 := by
  rw [shift_factor C M a delta (ne_of_gt hC) (ne_of_gt hM) (ne_of_gt ha)]
  apply div_neg_of_neg_of_pos
  · exact mul_neg_of_neg_of_pos (neg_neg_of_pos hd) (by positivity)
  · positivity

end Dynamic32Pi

#print axioms Dynamic32Pi.residual_factor
#print axioms Dynamic32Pi.stationary_iff
#print axioms Dynamic32Pi.calibrated_stationary
#print axioms Dynamic32Pi.curvature_ratio
#print axioms Dynamic32Pi.target_iff
#print axioms Dynamic32Pi.alternative_branch
#print axioms Dynamic32Pi.reduced_kinetic
#print axioms Dynamic32Pi.kinetic_positive
#print axioms Dynamic32Pi.reduced_friction
#print axioms Dynamic32Pi.reduced_mass_zero
#print axioms Dynamic32Pi.neutral_constant_mode
#print axioms Dynamic32Pi.shift_factor
#print axioms Dynamic32Pi.positive_shift_obstruction
