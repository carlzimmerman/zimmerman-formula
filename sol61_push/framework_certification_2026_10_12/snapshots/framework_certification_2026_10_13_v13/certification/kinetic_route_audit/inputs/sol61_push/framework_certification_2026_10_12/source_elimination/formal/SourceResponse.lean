import Mathlib

/-! Exact prescribed constant forcing response of the supplied NR source,
i b_t=delta*b+c3*F at P=0. Here c names c3, NOT speed of light.
No damping, backreacted combined conservation, bath, or halo selection inferred.
-/
noncomputable section
namespace FrameworkSourceResponse

def realPart (δ c F t : ℝ) : ℝ := c * F / δ * (Real.cos (δ * t) - 1)
def imagPart (δ c F t : ℝ) : ℝ := -(c * F / δ) * Real.sin (δ * t)
def storage (δ c F t : ℝ) : ℝ := realPart δ c F t ^ 2 + imagPart δ c F t ^ 2

theorem real_derivative (δ c F t : ℝ) (hδ : δ ≠ 0) :
    HasDerivAt (realPart δ c F) (-c * F * Real.sin (δ * t)) t := by
  have ha : HasDerivAt (fun s : ℝ => δ * s) δ t := by
    simpa using (hasDerivAt_id t).const_mul δ
  have h := ((ha.cos).sub_const 1).const_mul (c * F / δ)
  apply h.congr_deriv
  field_simp

theorem imag_derivative (δ c F t : ℝ) (hδ : δ ≠ 0) :
    HasDerivAt (imagPart δ c F) (-c * F * Real.cos (δ * t)) t := by
  have ha : HasDerivAt (fun s : ℝ => δ * s) δ t := by
    simpa using (hasDerivAt_id t).const_mul δ
  have h := (ha.sin).const_mul (-(c * F / δ))
  apply h.congr_deriv
  field_simp

/-- Both actual real/imaginary source ODEs, with exact source reaction sign. -/
theorem driven_source_ode (δ c F t : ℝ) (hδ : δ ≠ 0) :
    -deriv (imagPart δ c F) t = δ * realPart δ c F t + c * F ∧
      deriv (realPart δ c F) t = δ * imagPart δ c F t := by
  rw [(real_derivative δ c F t hδ).deriv, (imag_derivative δ c F t hδ).deriv]
  unfold realPart imagPart
  constructor
  · field_simp
    ring
  · field_simp

theorem zero_initial_source (δ c F : ℝ) : realPart δ c F 0 = 0 ∧ imagPart δ c F 0 = 0 := by
  simp [realPart, imagPart]

theorem storage_exact (δ c F t : ℝ) :
    storage δ c F t = 2 * c ^ 2 * F ^ 2 / δ ^ 2 * (1 - Real.cos (δ * t)) := by
  unfold storage realPart imagPart
  calc
    (c * F / δ * (Real.cos (δ * t) - 1)) ^ 2 +
        (-(c * F / δ) * Real.sin (δ * t)) ^ 2 =
      (c * F / δ) ^ 2 * ((Real.cos (δ * t) - 1) ^ 2 + Real.sin (δ * t) ^ 2) := by ring
    _ = (c * F / δ) ^ 2 * (2 * (1 - Real.cos (δ * t))) := by
      congr 1
      nlinarith [Real.sin_sq_add_cos_sq (δ * t)]
    _ = 2 * c ^ 2 * F ^ 2 / δ ^ 2 * (1 - Real.cos (δ * t)) := by ring

theorem storage_nonnegative (δ c F t : ℝ) : 0 ≤ storage δ c F t := by unfold storage; positivity

theorem storage_derivative (δ c F t : ℝ) (hδ : δ ≠ 0) :
    HasDerivAt (storage δ c F) (2 * c ^ 2 * F ^ 2 / δ * Real.sin (δ * t)) t := by
  have hf : storage δ c F = fun s => 2 * c ^ 2 * F ^ 2 / δ ^ 2 * (1 - Real.cos (δ * s)) :=
    funext (storage_exact δ c F)
  rw [hf]
  have ha : HasDerivAt (fun s : ℝ => δ * s) δ t := by
    simpa using (hasDerivAt_id t).const_mul δ
  have h := ((ha.cos).const_sub 1).const_mul (2 * c ^ 2 * F ^ 2 / δ ^ 2)
  apply h.congr_deriv
  field_simp

/-- Source storage increases and decreases within the same driven cycle. -/
theorem opposite_storage_power (δ c F : ℝ) (hδ : 0 < δ) (hcf : c * F ≠ 0) :
    0 < deriv (storage δ c F) (Real.pi / (2 * δ)) ∧
      deriv (storage δ c F) (3 * Real.pi / (2 * δ)) < 0 := by
  rw [(storage_derivative δ c F (Real.pi / (2 * δ)) hδ.ne').deriv,
    (storage_derivative δ c F (3 * Real.pi / (2 * δ)) hδ.ne').deriv]
  have h1 : δ * (Real.pi / (2 * δ)) = Real.pi / 2 := by field_simp
  have h3 : δ * (3 * Real.pi / (2 * δ)) = Real.pi + Real.pi / 2 := by field_simp; ring
  rw [h1, h3, Real.sin_pi_div_two, Real.sin_add]
  simp only [Real.sin_pi, Real.cos_pi, Real.cos_pi_div_two, Real.sin_pi_div_two]
  have hc : c ≠ 0 := (mul_ne_zero_iff.mp hcf).1
  have hF : F ≠ 0 := (mul_ne_zero_iff.mp hcf).2
  have hpower : 0 < 2 * c ^ 2 * F ^ 2 / δ := by positivity
  constructor <;> nlinarith [hpower]

/-- Intermediate nonzero source storage returns exactly to zero after a full cycle. -/
theorem storage_and_return (δ c F : ℝ) (hδ : 0 < δ) (hcf : c * F ≠ 0) :
    0 < storage δ c F (Real.pi / δ) ∧ storage δ c F (2 * Real.pi / δ) = 0 := by
  rw [storage_exact, storage_exact]
  have hhalf : δ * (Real.pi / δ) = Real.pi := by field_simp
  have hfull : δ * (2 * Real.pi / δ) = 2 * Real.pi := by field_simp
  rw [hhalf, hfull, Real.cos_pi, Real.cos_two_pi]
  have hc : c ≠ 0 := (mul_ne_zero_iff.mp hcf).1
  have hF : F ≠ 0 := (mul_ne_zero_iff.mp hcf).2
  constructor
  · positivity
  · ring

end FrameworkSourceResponse
#print axioms FrameworkSourceResponse.real_derivative
#print axioms FrameworkSourceResponse.imag_derivative
#print axioms FrameworkSourceResponse.driven_source_ode
#print axioms FrameworkSourceResponse.zero_initial_source
#print axioms FrameworkSourceResponse.storage_exact
#print axioms FrameworkSourceResponse.storage_nonnegative
#print axioms FrameworkSourceResponse.storage_derivative
#print axioms FrameworkSourceResponse.opposite_storage_power
#print axioms FrameworkSourceResponse.storage_and_return
