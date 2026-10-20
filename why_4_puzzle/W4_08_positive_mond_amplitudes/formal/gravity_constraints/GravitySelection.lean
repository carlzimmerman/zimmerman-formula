module

public import Mathlib.Algebra.Order.Field.Basic
meta import Mathlib.Tactic.FieldSimp
meta import Mathlib.Tactic.Ring.Basic
meta import Mathlib.Tactic.Linarith.Frontend
meta import Mathlib.Tactic.NormNum

@[expose] public section

/-!
Conditional de Sitter lapse/shift and static-normalization algebra.

The ADM component action, its PDE constraints and retained physical modes,
the time-dependent integration by parts (including its temporal boundary),
the static source/force dictionary, and the gravitating vacuum stress are
analytic inputs, not theorems of this file.  The redshift expression below
represents Wdot = 3 H W and Xdot = -2 H X, with d representing zdot.
The finite polynomial increment certifies the displayed lapse-linear term;
no general differentiation or variational formalism is imported.

P is a generic nonzero field element, not a formalized value of actual pi.
The tensor-plus-scalar identity assumes its displayed physical calibration;
it does not derive that calibration from a coupled gravitational theory.
No theorem here supplies microscopic health or a selection of xi = 1/4.
-/

namespace Why4.GravitySelection

variable {K : Type*} [Field K] [LinearOrder K] [IsStrictOrderedRing K]

def rawQuadratic (d H n B X z eta mu : K) : K :=
  -6 * (d - H * n) ^ 2 + 4 * (d - H * n) * B +
    X * (2 * z ^ 2 + 4 * n * z + eta * n ^ 2) + 2 * mu ^ 2 * n ^ 2

def lapseEquation (d H n B X z eta mu : K) : K :=
  12 * H * (d - H * n) - 4 * H * B + 4 * X * z +
    2 * (eta * X + 2 * mu ^ 2) * n

def reducedKinetic (W X eta mu H : K) : K :=
  W * (eta * X + 2 * mu ^ 2) / H ^ 2

omit [LinearOrder K] [IsStrictOrderedRing K] in
theorem shift_substitution
    (d H B X z eta mu : K) (hH : H ≠ 0) :
    rawQuadratic d H (d / H) B X z eta mu =
      2 * X * z ^ 2 + 4 * X * z * d / H +
        (eta * X + 2 * mu ^ 2) * d ^ 2 / H ^ 2 := by
  unfold rawQuadratic
  field_simp [hH]
  ring1

omit [LinearOrder K] [IsStrictOrderedRing K] in
theorem redshift_boundary_cancellation
    (W X z d H eta mu : K) (hH : H ≠ 0) :
    W * (2 * X * z ^ 2 + 4 * X * z * d / H +
        (eta * X + 2 * mu ^ 2) * d ^ 2 / H ^ 2) -
      (2 / H) * (3 * H * W * X * z ^ 2 -
        2 * H * W * X * z ^ 2 + 2 * W * X * z * d) =
      W * (eta * X + 2 * mu ^ 2) * d ^ 2 / H ^ 2 := by
  field_simp [hH]
  ring1

theorem reduced_kinetic_positive
    (W X eta mu H : K) (hW : 0 < W) (hX : 0 < X)
    (heta : 0 < eta) (hH : H ≠ 0) :
    0 < reducedKinetic W X eta mu H := by
  have hsum : 0 < eta * X + 2 * mu ^ 2 := by
    nlinarith [mul_pos heta hX, sq_nonneg mu]
  unfold reducedKinetic
  exact div_pos (mul_pos hW hsum) (sq_pos_of_ne_zero hH)

omit [LinearOrder K] [IsStrictOrderedRing K] in
theorem lapse_polynomial_increment
    (d H n B X z eta mu v : K) :
    rawQuadratic d H (n + v) B X z eta mu -
      rawQuadratic d H n B X z eta mu =
      lapseEquation d H n B X z eta mu * v +
        (-6 * H ^ 2 + eta * X + 2 * mu ^ 2) * v ^ 2 := by
  unfold rawQuadratic lapseEquation
  ring1

theorem lapse_substitution_zero
    (d H X z eta mu : K) (hH : H ≠ 0) :
    lapseEquation d H (d / H)
      (X * z / H + (eta * X + 2 * mu ^ 2) * d / (2 * H ^ 2))
      X z eta mu = 0 := by
  unfold lapseEquation
  field_simp [hH]
  ring1

theorem metric_static_amplitude_ratio
    (P G f0 a0 : K) (hP : P ≠ 0) (hG : G ≠ 0) (ha0 : a0 ≠ 0) :
    (f0 / (8 * P * G)) * (1 / (12 * P * G * a0)) ^ 2 /
      (1 / (8 * P * G)) ^ 3 = 4 * f0 / (9 * a0 ^ 2) := by
  field_simp [hP, hG, ha0]
  ring1

theorem cubic_ratio_scaling (epsilon C2 C3 delta : K) :
    epsilon * ((1 + delta) * C3) ^ 2 / C2 ^ 3 =
      (1 + delta) ^ 2 * (epsilon * C3 ^ 2 / C2 ^ 3) := by
  ring1

omit [LinearOrder K] [IsStrictOrderedRing K] in
theorem tensor_scalar_xi_cube
    (Gs Gt a0s epsilon : K) (hGs : Gs ≠ 0)
    (hGtotal : Gt + Gs ≠ 0) (hepsilon : epsilon ≠ 0) :
    ((Gs / (Gt + Gs)) * a0s) ^ 2 / ((Gt + Gs) * epsilon) =
      (Gs / (Gt + Gs)) ^ 3 * (a0s ^ 2 / (Gs * epsilon)) := by
  field_simp [hGs, hGtotal, hepsilon]

theorem reduced_kinetic_rational_control :
    reducedKinetic (2 : K) 3 2 1 2 = 4 := by
  norm_num [reducedKinetic]

/- The target equation is a downstream counterfactual, never an input
used to select a coupling.  The bound 0 < P < 4 is an explicit hypothesis;
identifying P with actual pi remains an analytic bridge. -/
theorem target_scalar_fraction_bound
    (P r f : K) (hP : 0 < P) (hP4 : P < 4)
    (hr : 0 ≤ r) (hrhalf : r < 1 / 2) (hf : 0 ≤ f) (hf1 : f < 1)
    (htarget : 125 * P * (1 + r) * f ^ 3 = 32 * (1 - r) * (1 - f)) :
    1 / 4 < f := by
  by_contra h
  have hfq : f ≤ 1 / 4 := le_of_not_gt h
  have hquad : 0 ≤ f ^ 2 + f / 4 + 1 / 16 := by
    nlinarith [sq_nonneg f]
  have hcube : f ^ 3 ≤ 1 / 64 := by
    nlinarith [mul_nonneg (sub_nonneg.mpr hfq) hquad]
  have hfactor : 0 < 1 + r := by linarith
  have hcoeff : 0 < 125 * P * (1 + r) := by
    nlinarith [mul_pos hP hfactor]
  have hproduct : P * (1 + r) < 6 := by
    nlinarith [mul_pos (sub_pos.mpr hP4) hfactor]
  have hleft : 125 * P * (1 + r) * f ^ 3 < 375 / 32 := by
    have hbound := mul_le_mul_of_nonneg_left hcube (le_of_lt hcoeff)
    nlinarith
  have hright : 12 < 32 * (1 - r) * (1 - f) := by
    have hpositive : 0 < 1 - f := by linarith
    have hbound := mul_pos (show 0 < 1 / 2 - r by linarith) hpositive
    nlinarith
  linarith

theorem inferred_target_gamma_bound
    (P r f : K) (hP : 0 < P) (hP4 : P < 4)
    (hr : 0 ≤ r) (hrhalf : r < 1 / 2) (hf : 0 ≤ f) (hf1 : f < 1)
    (htarget : 125 * P * (1 + r) * f ^ 3 = 32 * (1 - r) * (1 - f)) :
    1 - 2 * f < 1 / 2 := by
  have h := target_scalar_fraction_bound P r f hP hP4
    hr hrhalf hf hf1 htarget
  linarith

/- This polynomial is the normalized frozen-background determinant at
k = m_b / 2.  Root existence and its physical, constrained-mode
interpretation are analytic claims, not supplied by these identities. -/
def bandPolynomial (c s : K) : K :=
  (s - c / 4) * (s + 3 / 4) - (5 / 49) * s

theorem band_test_identity (c : K) :
    bandPolynomial c (-11 / 49) = -913 / 9604 - 103 * c / 784 := by
  unfold bandPolynomial
  ring1

theorem band_test_negative (c : K) (hc : 0 ≤ c) :
    bandPolynomial c (-11 / 49) < 0 := by
  rw [band_test_identity]
  nlinarith

theorem band_zero_negative (c : K) (hc : 0 < c) :
    bandPolynomial c 0 < 0 := by
  unfold bandPolynomial
  nlinarith

#check @shift_substitution
#check @redshift_boundary_cancellation
#check @reduced_kinetic_positive
#check @lapse_polynomial_increment
#check @lapse_substitution_zero
#check @metric_static_amplitude_ratio
#check @cubic_ratio_scaling
#check @tensor_scalar_xi_cube
#check @reduced_kinetic_rational_control
#check @target_scalar_fraction_bound
#check @inferred_target_gamma_bound
#check @band_test_identity
#check @band_test_negative
#check @band_zero_negative
#print axioms shift_substitution
#print axioms redshift_boundary_cancellation
#print axioms reduced_kinetic_positive
#print axioms lapse_polynomial_increment
#print axioms lapse_substitution_zero
#print axioms metric_static_amplitude_ratio
#print axioms cubic_ratio_scaling
#print axioms tensor_scalar_xi_cube
#print axioms reduced_kinetic_rational_control
#print axioms target_scalar_fraction_bound
#print axioms inferred_target_gamma_bound
#print axioms band_test_identity
#print axioms band_test_negative
#print axioms band_zero_negative

end Why4.GravitySelection
