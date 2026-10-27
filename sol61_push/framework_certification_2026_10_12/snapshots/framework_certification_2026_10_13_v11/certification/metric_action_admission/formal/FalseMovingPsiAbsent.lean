import Mathlib

/-! Explicit optical and worldline responses of an admitted isotropic weak metric.
No metric gravity action, field equation, slip relation, or Lovelock theorem is imported.
Diagnostic same-Phi/different-Psi family is not an adopted covariant model. -/
noncomputable section
open MeasureTheory
namespace FrameworkMetricResponse

def temporal (Φ e : ℝ) : ℝ := 2 * Φ * e + 1
def spatial (Ψ e : ℝ) : ℝ := (-2 * Ψ) * e + 1
def opticalIndex (Φ Ψ e : ℝ) : ℝ := Real.sqrt (spatial Ψ e / temporal Φ e)
def fermatDensity (Φ Ψ slope e : ℝ) : ℝ := opticalIndex Φ Ψ e * Real.sqrt (1 + slope ^ 2)
def worldlineDensity (m Φ Ψ speed e : ℝ) : ℝ :=
  -m * Real.sqrt (temporal Φ e - spatial Ψ e * speed ^ 2)

theorem null_optical_dictionary (Φ Ψ e dt dl : ℝ)
    (ht : 0 < temporal Φ e) (hs : 0 ≤ spatial Ψ e)
    (hnull : temporal Φ e * dt ^ 2 = spatial Ψ e * dl ^ 2) :
    dt ^ 2 = (opticalIndex Φ Ψ e * dl) ^ 2 := by
  have hn : 0 ≤ spatial Ψ e / temporal Φ e := div_nonneg hs ht.le
  unfold opticalIndex
  rw [mul_pow, Real.sq_sqrt hn]
  field_simp
  nlinarith [hnull]

theorem actual_optical_derivative (Φ Ψ : ℝ) :
    HasDerivAt (opticalIndex Φ Ψ) (-Φ - Ψ) 0 := by
  have ht : HasDerivAt (temporal Φ) (2 * Φ) 0 := by
    exact (((hasDerivAt_id (0 : ℝ)).const_mul (2 * Φ)).add_const 1).congr_deriv (by ring)
  have hs : HasDerivAt (spatial Ψ) (-2 * Ψ) 0 := by
    exact (((hasDerivAt_id (0 : ℝ)).const_mul (-2 * Ψ)).add_const 1).congr_deriv (by ring)
  have h := (hs.div ht (by norm_num [temporal])).sqrt (by norm_num [temporal, spatial])
  apply h.congr_deriv
  norm_num [temporal, spatial]
  ring

theorem actual_fermat_derivative (Φ Ψ slope : ℝ) :
    HasDerivAt (fermatDensity Φ Ψ slope) ((-Φ - Ψ) * Real.sqrt (1 + slope ^ 2)) 0 := by
  exact (actual_optical_derivative Φ Ψ).mul_const _

/-- Exact action derivative at a timelike flat speed; Psi enters at speed squared. -/
theorem actual_worldline_derivative (m Φ Ψ speed : ℝ) (hv : speed ^ 2 < 1) :
    HasDerivAt (worldlineDensity m Φ Ψ speed)
      (-m * (Φ + Ψ * speed ^ 2) / Real.sqrt (1 - speed ^ 2)) 0 := by
  have ht : HasDerivAt (temporal Φ) (2 * Φ) 0 := by
    exact (((hasDerivAt_id (0 : ℝ)).const_mul (2 * Φ)).add_const 1).congr_deriv (by ring)
  have hs : HasDerivAt (spatial Ψ) (-2 * Ψ) 0 := by
    exact (((hasDerivAt_id (0 : ℝ)).const_mul (-2 * Ψ)).add_const 1).congr_deriv (by ring)
  have hn : temporal Φ 0 - spatial Ψ 0 * speed ^ 2 ≠ 0 := by
    norm_num [temporal, spatial]
    linarith
  have h := ((ht.sub (hs.mul_const (speed ^ 2))).sqrt hn).const_mul (-m)
  apply h.congr_deriv
  norm_num [temporal, spatial]
  ring

theorem actual_rest_worldline_derivative (m Φ Ψ : ℝ) :
    HasDerivAt (worldlineDensity m Φ Ψ 0) (-m * Φ) 0 := by
  simpa using actual_worldline_derivative m Φ Ψ 0 (by norm_num)

/-- Differentiate the actual optical first-response profile transversely. -/
theorem optical_profile_gradient (Φ Ψ : ℝ → ℝ) (x dΦ dΨ : ℝ)
    (hΦ : HasDerivAt Φ dΦ x) (hΨ : HasDerivAt Ψ dΨ x) :
    HasDerivAt (fun y => deriv (opticalIndex (Φ y) (Ψ y)) 0) (-dΦ - dΨ) x := by
  have he : (fun y => deriv (opticalIndex (Φ y) (Ψ y)) 0) = fun y => -Φ y - Ψ y := by
    funext y
    exact (actual_optical_derivative (Φ y) (Ψ y)).deriv
  rw [he]
  exact hΦ.neg.sub hΨ

/-- Leading rest-worldline potential profile has derivative -m Phi', independent of Psi. -/
theorem rest_worldline_profile_gradient (m : ℝ) (Φ Ψ : ℝ → ℝ) (x dΦ : ℝ)
    (hΦ : HasDerivAt Φ dΦ x) :
    HasDerivAt (fun y => deriv (worldlineDensity m (Φ y) (Ψ y) 0) 0) (-m * dΦ) x := by
  have he : (fun y => deriv (worldlineDensity m (Φ y) (Ψ y) 0) 0) = fun y => -m * Φ y := by
    funext y
    exact (actual_rest_worldline_derivative m (Φ y) (Ψ y)).deriv
  rw [he]
  exact hΦ.const_mul (-m)

/-- Actual integrated local optical first-response for Psi=s Phi.
It is NOT interchange of derivative and integral of the full nonlinear index. -/
theorem integrated_optical_response {Ω : Type*} [MeasurableSpace Ω] (μ : Measure Ω)
    (Φ : Ω → ℝ) (s : ℝ) (hΦ : Integrable Φ μ) :
    (∫ x, deriv (opticalIndex (Φ x) (s * Φ x)) 0 ∂μ) = -(1 + s) * (∫ x, Φ x ∂μ) := by
  have he : (fun x => deriv (opticalIndex (Φ x) (s * Φ x)) 0) = fun x => -(1 + s) * Φ x := by
    funext x
    rw [(actual_optical_derivative (Φ x) (s * Φ x)).deriv]
    ring
  rw [he]
  simpa only [smul_eq_mul] using hΦ.integral_smul (-(1 + s))

/-- Exact diagnostic nonuniqueness: same Phi gives same rest response,
while the optical gradient changes between Psi=0 and Psi=Phi when Phi'!=0. -/
theorem same_cold_different_optics (m : ℝ) (Φ : ℝ → ℝ) (x dΦ : ℝ)
    (hΦ : HasDerivAt Φ dΦ x) (hd : dΦ ≠ 0) :
    deriv (fun y => deriv (worldlineDensity m (Φ y) 0 0) 0) x =
      deriv (fun y => deriv (worldlineDensity m (Φ y) (Φ y) 0) 0) x ∧
    deriv (fun y => deriv (opticalIndex (Φ y) 0) 0) x ≠
      deriv (fun y => deriv (opticalIndex (Φ y) (Φ y)) 0) x := by
  constructor
  · rw [(rest_worldline_profile_gradient m Φ (fun _ => 0) x dΦ hΦ).deriv,
      (rest_worldline_profile_gradient m Φ Φ x dΦ hΦ).deriv]
  · rw [(optical_profile_gradient Φ (fun _ => 0) x dΦ 0 hΦ (hasDerivAt_const x 0)).deriv,
      (optical_profile_gradient Φ Φ x dΦ dΦ hΦ hΦ).deriv]
    intro he
    apply hd
    linarith

end FrameworkMetricResponse

open FrameworkMetricResponse
-- Absence of Psi holds only at leading rest order, not arbitrary timelike speed.
example : deriv (worldlineDensity 1 0 1 (1/2)) 0 = 0 := by
  rw [(actual_worldline_derivative 1 0 1 (1/2) (by norm_num)).deriv]
  norm_num [div_eq_zero_iff, Real.sqrt_eq_zero]
