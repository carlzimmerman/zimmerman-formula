import Mathlib
import Mathlib.Tactic

noncomputable section
open scoped Topology
open Filter
open Real

def Kfun (C0 eps alpha : ℝ) (X : ℝ) : ℝ :=
  C0 + eps * X + alpha * (X * Real.sqrt X)

lemma wA {x : ℝ} (hx : 0 < x) :
    HasDerivAt (fun X : ℝ => X * Real.sqrt X) ((3 / 2 : ℝ) * Real.sqrt x) x := by
  have hsq : Real.sqrt x * Real.sqrt x = x := Real.mul_self_sqrt (le_of_lt hx)
  have hsq2 : Real.sqrt x ^ 2 = x := by simpa [pow_two] using hsq
  have hden : (2 * Real.sqrt x) ≠ 0 := by positivity
  have hderiv : 1 * Real.sqrt x + id x * (1 / (2 * Real.sqrt x)) = (3 / 2 : ℝ) * Real.sqrt x := by
    simp [one_mul, id]
    field_simp [hden]
    rw [hsq2]
    ring_nf
  have hd_raw := (hasDerivAt_id x).mul (hasDerivAt_sqrt hx.ne')
  rw [hderiv] at hd_raw
  convert hd_raw using 3
  all_goals first
    | simp [Kfun, Pi.add_apply, Pi.mul_apply, id]
    | rfl
    | ring_nf

lemma wB {C0 eps alpha x : ℝ} (hx : 0 < x) :
    HasDerivAt (fun X : ℝ => Kfun C0 eps alpha X) (eps + (3 / 2 : ℝ) * alpha * Real.sqrt x) x := by
  have h_id : HasDerivAt (fun X : ℝ => eps * X) eps x := by
    simpa using (hasDerivAt_id x).const_mul eps
  have hlin : HasDerivAt (fun X : ℝ => C0 + eps * X) eps x := by
    simpa using h_id.const_add C0
  have hsqrt : HasDerivAt (fun X : ℝ => X * Real.sqrt X) ((3 / 2 : ℝ) * Real.sqrt x) x := by
    have hsq : Real.sqrt x * Real.sqrt x = x := Real.mul_self_sqrt (le_of_lt hx)
    have hsq2 : Real.sqrt x ^ 2 = x := by simpa [pow_two] using hsq
    have hden : (2 * Real.sqrt x) ≠ 0 := by positivity
    have hderiv : 1 * Real.sqrt x + id x * (1 / (2 * Real.sqrt x)) = (3 / 2 : ℝ) * Real.sqrt x := by
      simp [one_mul, id]
      field_simp [hden]
      rw [hsq2]
      ring_nf
    have hd_raw := (hasDerivAt_id x).mul (hasDerivAt_sqrt hx.ne')
    rw [hderiv] at hd_raw
    convert hd_raw using 3
    all_goals first
      | simp [Pi.mul_apply, id]
      | rfl
      | ring_nf
  have hquad : HasDerivAt (fun X : ℝ => alpha * (X * Real.sqrt X))
      (alpha * ((3 / 2 : ℝ) * Real.sqrt x)) x := hsqrt.const_mul alpha
  have hderiv2 : eps + alpha * ((3 / 2 : ℝ) * Real.sqrt x) =
      eps + (3 / 2 : ℝ) * alpha * Real.sqrt x := by
    ring_nf
  have hadd := hlin.add hquad
  rw [hderiv2] at hadd
  convert hadd using 3
  all_goals first
    | simp [Kfun, Pi.add_apply]
    | rfl
    | ring_nf

lemma x_mul_sqrt_hasDerivAt_zero : HasDerivAt (fun X : ℝ => X * Real.sqrt X) 0 0 := by
  rw [hasDerivAt_iff_tendsto]
  have hEq : (fun y : ℝ =>
        ‖y - 0‖⁻¹ * ‖y * Real.sqrt y - 0 * Real.sqrt 0 - (y - 0) • (0 : ℝ)‖) =ᶠ[𝓝 (0 : ℝ)]
      (fun y : ℝ => ‖Real.sqrt y‖) := by
    apply Filter.Eventually.of_forall
    intro y
    by_cases hy : y = 0
    · simp [hy]
    · simp [hy]
  have hsqrt_tendsto : Tendsto (fun y : ℝ => ‖Real.sqrt y‖) (𝓝 (0 : ℝ)) (𝓝 0) := by
    have hc : ContinuousAt (fun y : ℝ => ‖Real.sqrt y‖) (0 : ℝ) :=
      Real.continuous_sqrt.continuousAt.norm
    simpa [Real.sqrt_zero] using hc.tendsto
  exact Tendsto.congr' hEq.symm hsqrt_tendsto

lemma wC {C0 eps alpha : ℝ} :
    HasDerivAt (fun X : ℝ => Kfun C0 eps alpha X) eps 0 := by
  have h_id : HasDerivAt (fun X : ℝ => eps * X) eps 0 := by
    simpa using (hasDerivAt_id 0).const_mul eps
  have hlin : HasDerivAt (fun X : ℝ => C0 + eps * X) eps 0 := by
    simpa using h_id.const_add C0
  have hquad : HasDerivAt (fun X : ℝ => alpha * (X * Real.sqrt X)) 0 0 := by
    simpa using x_mul_sqrt_hasDerivAt_zero.const_mul alpha
  have hadd := hlin.add hquad
  convert hadd using 3
  all_goals first
    | simp [Kfun, Pi.add_apply]
    | rfl
    | ring_nf

lemma wD {C0 eps alpha Y : ℝ} (hY : 0 < Y) :
    HasDerivAt (fun X : ℝ => Kfun C0 eps alpha X) (eps + (3 / 2 : ℝ) * alpha * Y) (Y ^ 2) := by
  have hpos : 0 < Y ^ 2 := pow_pos hY 2
  convert wB (C0 := C0) (eps := eps) (alpha := alpha) (x := Y ^ 2) hpos using 3
  all_goals first
    | rw [Real.sqrt_sq (le_of_lt hY)]
    | rfl
    | ring_nf

end