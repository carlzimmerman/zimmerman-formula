import Mathlib

/-!
FRAMEWORK-CERT-2026-10-12: conditional offset and coefficient audit.
Base Git: 8cef73ea7d01e20f1d08f435ad621b739f8eb3cc.
No physical theory is imported. `responsePotential` is a DECLARED scalar
polynomial test model, not a derived microscopic action. `scale` is the
framework's DECLARED scale relation after W0 = rho_DE*c^2 and c > 0.
The formal statements test sufficiency of these premises only. They do not
formalize Einstein equations, metric variation, dynamics, or empirical data.
An offset can gravitate in a metric theory; only this scalar derivative is
shown unchanged. No conclusion about the full gravitational action follows.
-/
noncomputable section
namespace FrameworkVacuumLink

def responsePotential (W0 A B x : ℝ) : ℝ := W0 + A / 2 * x ^ 2 + B / 3 * x ^ 3
def response (A B x : ℝ) : ℝ := A * x + B * x ^ 2
def ratio (G W0 a : ℝ) : ℝ := G * W0 / a ^ 2
def scale (κ G W0 : ℝ) : ℝ := κ * Real.sqrt (G * W0)

/-- For every real offset, the declared polynomial has the same response derivative. -/
theorem response_derivative (W0 A B x : ℝ) :
    HasDerivAt (responsePotential W0 A B) (response A B x) x := by
  have h2 := (hasDerivAt_id x).pow 2
  have h3 := (hasDerivAt_id x).pow 3
  have h := ((h2.const_mul (A / 2)).add (h3.const_mul (B / 3))).const_add W0
  have hf : (fun y : ℝ => W0 + (A / 2 * y ^ 2 + B / 3 * y ^ 3)) =
      responsePotential W0 A B := by
    funext y
    dsimp [responsePotential]
    ring
  dsimp at h
  rw [hf] at h
  exact h.congr_deriv (by dsimp [response]; ring)

/-- Pointwise derivative invariance requires no assumption on the offset. -/
theorem offset_invisible_to_response (W0 δ A B x : ℝ) :
    deriv (responsePotential (W0 + δ) A B) x =
      deriv (responsePotential W0 A B) x := by
  rw [(response_derivative (W0 + δ) A B x).deriv,
    (response_derivative W0 A B x).deriv]

/-- At fixed force scale, the ratio changes when the independent offset changes. -/
theorem offset_ratio_change (G W0 a δ : ℝ) :
    ratio G (W0 + δ) a - ratio G W0 a = G * δ / a ^ 2 := by
  unfold ratio
  ring

/-- Fixing the factor four is precisely an additional offset constraint. -/
theorem factor_four_iff_offset (G W0 a : ℝ) (hG : G ≠ 0) (ha : a ≠ 0) :
    ratio G W0 a = 4 ↔ W0 = 4 * a ^ 2 / G := by
  unfold ratio
  constructor
  · intro h
    apply (eq_div_iff hG).mpr
    have := (div_eq_iff (pow_ne_zero 2 ha)).mp h
    nlinarith
  · intro h
    rw [h]
    field_simp

/-- Positive coefficients in the scale equation yield factor four exactly at κ=1/2.
No dimensional premise, derivative premise, or conservation premise fixes κ. -/
theorem factor_four_iff_half (κ G W0 : ℝ) (hκ : 0 < κ) (hGW : 0 < G * W0) :
    ratio G W0 (scale κ G W0) = 4 ↔ κ = 1 / 2 := by
  have hs : 0 < Real.sqrt (G * W0) := Real.sqrt_pos.mpr hGW
  have ha : scale κ G W0 ≠ 0 := (mul_pos hκ hs).ne'
  have hsq : scale κ G W0 ^ 2 = κ ^ 2 * (G * W0) := by
    unfold scale
    rw [mul_pow, Real.sq_sqrt hGW.le]
  unfold ratio
  rw [div_eq_iff (pow_ne_zero 2 ha), hsq]
  constructor
  · intro h
    have hzero : (G * W0) * (1 - 4 * κ ^ 2) = 0 := by nlinarith
    have hk := (mul_eq_zero.mp hzero).resolve_left hGW.ne'
    nlinarith
  · intro h
    rw [h]
    ring

/-- Concrete normalized countermodel: both positive coefficients obey the scale
relation; the force coefficients and the required ratio differ. -/
theorem coefficient_not_selected :
    0 < (1 : ℝ) ∧ 0 < (1 / 2 : ℝ) ∧
    scale 1 1 1 = 1 ∧ scale (1 / 2) 1 1 = 1 / 2 ∧
    ratio 1 1 (scale 1 1 1) = 1 ∧
    ratio 1 1 (scale (1 / 2) 1 1) = 4 := by
  norm_num [scale, ratio]

/-- At fixed a=1, the same declared response derivative admits positive offsets
1 and 4, whose vacuum ratios are respectively 1 and 4. -/
theorem fixed_response_different_vacuum_ratio (A B x : ℝ) :
    deriv (responsePotential 1 A B) x = deriv (responsePotential 4 A B) x ∧
    ratio 1 1 1 = 1 ∧ ratio 1 4 1 = 4 := by
  constructor
  · rw [(response_derivative 1 A B x).deriv, (response_derivative 4 A B x).deriv]
  · norm_num [ratio]

end FrameworkVacuumLink
#print axioms FrameworkVacuumLink.response_derivative
#print axioms FrameworkVacuumLink.offset_invisible_to_response
#print axioms FrameworkVacuumLink.offset_ratio_change
#print axioms FrameworkVacuumLink.factor_four_iff_offset
#print axioms FrameworkVacuumLink.factor_four_iff_half
#print axioms FrameworkVacuumLink.coefficient_not_selected
#print axioms FrameworkVacuumLink.fixed_response_different_vacuum_ratio
