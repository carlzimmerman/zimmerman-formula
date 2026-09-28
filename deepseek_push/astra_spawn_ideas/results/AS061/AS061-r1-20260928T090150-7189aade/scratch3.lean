import Mathlib
import Mathlib.Tactic

noncomputable section
open Filter
open Real

def Kfun (C0 eps alpha : ℝ) (X : ℝ) : ℝ :=
  C0 + eps * X + alpha * (X * Real.sqrt X)

lemma vA2 {x : ℝ} (hx : 0 < x) :
    HasDerivAt (fun X : ℝ => X * Real.sqrt X) ((3 / 2 : ℝ) * Real.sqrt x) x := by
  have hd_raw := (hasDerivAt_id x).mul (hasDerivAt_sqrt hx.ne')
  convert hd_raw using 2
  · ext X
    rfl
  · rfl
  · have hsq : Real.sqrt x * Real.sqrt x = x := Real.mul_self_sqrt (le_of_lt hx)
    have hsq2 : Real.sqrt x ^ 2 = x := by simpa [pow_two] using hsq
    have hden : (2 * Real.sqrt x) ≠ 0 := by positivity
    trace_state
    simp [one_mul, id]
    trace_state
    field_simp [hden]
    rw [hsq2]
    ring_nf

lemma vB2 {C0 eps alpha x : ℝ} (hx : 0 < x) :
    HasDerivAt (fun X : ℝ => Kfun C0 eps alpha X) (eps + (3 / 2 : ℝ) * alpha * Real.sqrt x) x := by
  have h_id : HasDerivAt (fun X : ℝ => eps * X) eps x := by
    simpa using (hasDerivAt_id x).const_mul eps
  have hlin : HasDerivAt (fun X : ℝ => C0 + eps * X) eps x := by
    simpa using h_id.const_add C0
  have hsqrt : HasDerivAt (fun X : ℝ => X * Real.sqrt X) ((3 / 2 : ℝ) * Real.sqrt x) x := by
    have hd_raw := (hasDerivAt_id x).mul (hasDerivAt_sqrt hx.ne')
    convert hd_raw using 2
    · ext X
      rfl
    · rfl
    · have hsq : Real.sqrt x * Real.sqrt x = x := Real.mul_self_sqrt (le_of_lt hx)
      have hsq2 : Real.sqrt x ^ 2 = x := by simpa [pow_two] using hsq
      have hden : (2 * Real.sqrt x) ≠ 0 := by positivity
      simp [one_mul, id]
      field_simp [hden]
      rw [hsq2]
      ring_nf
  have hquad : HasDerivAt (fun X : ℝ => alpha * (X * Real.sqrt X))
      (alpha * ((3 / 2 : ℝ) * Real.sqrt x)) x := hsqrt.const_mul alpha
  convert (hlin.add hquad) using 2
  · ext X
    rfl
  · rfl
  · ring_nf

lemma vC2 {C0 eps alpha : ℝ} :
    HasDerivAt (fun X : ℝ => Kfun C0 eps alpha X) eps 0 := by
  have h_id : HasDerivAt (fun X : ℝ => eps * X) eps 0 := by
    simpa using (hasDerivAt_id 0).const_mul eps
  have hlin : HasDerivAt (fun X : ℝ => C0 + eps * X) eps 0 := by
    simpa using h_id.const_add C0
  have hquad : HasDerivAt (fun X : ℝ => alpha * (X * Real.sqrt X)) 0 0 := by
    simpa using x_mul_sqrt_hasDerivAt_zero.const_mul alpha
  have hadd := hlin.add hquad
  convert hadd using 2
  · ext X
    rfl
  · rfl
  · ring_nf

end