import Mathlib
import Mathlib.Tactic

noncomputable section
open Filter
open scoped Topology

-- A: simpa with Pi.inv_apply
example (u : ℝ) (hu : 1 + u ≠ 0) : HasDerivAt (fun x : ℝ => (1 + x)⁻¹) (-1 / (1 + u)^2) u := by
  have hlin : HasDerivAt (fun x : ℝ => 1 + x) 1 u := by simpa using (hasDerivAt_id u).const_add 1
  simpa [Pi.inv_apply] using hlin.inv hu

-- B: convert + ext
example (u : ℝ) (hu : 1 + u ≠ 0) : HasDerivAt (fun x : ℝ => (1 + x)⁻¹) (-1 / (1 + u)^2) u := by
  have hlin : HasDerivAt (fun x : ℝ => 1 + x) 1 u := by simpa using (hasDerivAt_id u).const_add 1
  convert hlin.inv hu using 1
  ext x
  simp

-- C: pow of id
example (u : ℝ) : HasDerivAt (fun x : ℝ => x^2) (2 * u) u := by
  simpa [Pi.pow_apply] using (hasDerivAt_id u).pow 2

-- D: mul of id
example (u : ℝ) : HasDerivAt (fun x : ℝ => x^2) (2 * u) u := by
  have h := (hasDerivAt_id u).mul (hasDerivAt_id u)
  convert h using 1
  · ext x
    simp [pow_two]
  · ring

-- E: deriv via simp
example (u : ℝ) (hu : 1 + u ≠ 0) : deriv (fun x : ℝ => (1 + x)⁻¹) u = -1 / (1 + u)^2 := by
  simp [deriv_inv, hu]

-- F: log comp
example (u : ℝ) (hu : 0 < 1 + u) : HasDerivAt (fun x : ℝ => Real.log (1 + x)) ((1 + u)⁻¹) u := by
  have hlin : HasDerivAt (fun x : ℝ => 1 + x) 1 u := by simpa using (hasDerivAt_id u).const_add 1
  have hlog0 : HasDerivAt Real.log ((1 + u)⁻¹) (1 + u) := Real.hasDerivAt_log (ne_of_gt hu)
  simpa [Function.comp_def] using hlog0.comp u hlin

-- G: full pow of inverse
example (u : ℝ) (hu : 1 + u ≠ 0) :
    HasDerivAt (fun x : ℝ => (1 + x)⁻¹ * (1 + x)⁻¹)
      (2 * (1 + u)⁻¹ * (-1 / (1 + u)^2)) u := by
  have hlin : HasDerivAt (fun x : ℝ => 1 + x) 1 u := by simpa using (hasDerivAt_id u).const_add 1
  have hinv : HasDerivAt (fun x : ℝ => (1 + x)⁻¹) (-1 / (1 + u)^2) u := by
    simpa [Pi.inv_apply] using hlin.inv hu
  simpa [Pi.mul_apply] using hinv.mul hinv

-- H: csSq_as_one_minus
def csSq (u : ℝ) : ℝ := (u^2 + 3 * u + 2) / (u^2 + 3 * u + 4)
theorem denom_pos (u : ℝ) : 0 < u^2 + 3 * u + 4 := by nlinarith [sq_nonneg (u + (3 / 2 : ℝ))]
example (u : ℝ) : csSq u = 1 - 2 / (u^2 + 3 * u + 4) := by
  unfold csSq
  have hd : u^2 + 3 * u + 4 ≠ 0 := ne_of_gt (denom_pos u)
  field_simp [hd]
  ring_nf

-- I: div_lt_one route
example (u : ℝ) : csSq u < 1 := by
  unfold csSq
  have hd : 0 < u^2 + 3 * u + 4 := denom_pos u
  rw [div_lt_one hd]
  norm_num
