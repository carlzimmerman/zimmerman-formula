import Mathlib

-- AS041 certificate: Q-branch closed forms underpinning the nonspherical-obstruction audit.
--   nu_Q(y) = sqrt(1 + 1/y)  (y > 0)
--   C_Q(y)  = -y * nu_Q'(y)  =  1 / (2*y*sqrt(1+1/y))
-- Theorems:
--   T1: derivative identity  nu_Q'(y) = -1 / (2*y^2*sqrt(1+1/y))   (y > 0)
--   T2: deep-universality closed form  2*sqrt(y)*C_Q(y) = 1/sqrt(1+y)   (y > 0)
--   T3: deep limit  lim_{y -> 0+} 2*sqrt(y)*C_Q(y) = 1
-- These are the exact algebraic content of checks CK1 (Q branch), CK2 (Q branch) and
-- CK6 (universal deep coefficient, Q branch: 2*sqrt(y)*C_Q(y) -> 1 as y -> 0).

noncomputable section

open Filter
open scoped Topology

def nu_Q (y : ℝ) : ℝ := Real.sqrt (1 + 1 / y)

def C_Q (y : ℝ) : ℝ := 1 / (2 * y * Real.sqrt (1 + 1 / y))

theorem nu_Q_deriv (y : ℝ) (hy : 0 < y) :
    HasDerivAt nu_Q (-1 / (2 * y ^ 2 * Real.sqrt (1 + 1 / y))) y := by
  have hyne : y ≠ 0 := ne_of_gt hy
  have hgoal_pos : 0 < 1 + 1 / y := by positivity
  have hgoal_ne : 1 + 1 / y ≠ 0 := ne_of_gt hgoal_pos
  have hsqrt_ne : Real.sqrt (1 + 1 / y) ≠ 0 := by
    exact ne_of_gt (Real.sqrt_pos.mpr hgoal_pos)
  have hconst : HasDerivAt (fun t : ℝ => (1 : ℝ)) (0 : ℝ) y := hasDerivAt_const (c := (1 : ℝ)) (x := y)
  have hinv0 : HasDerivAt (fun t : ℝ => t⁻¹) (-1 / y ^ 2) y := (hasDerivAt_id y).inv hyne
  have hinv : HasDerivAt (fun t : ℝ => 1 / t) (-1 / y ^ 2) y := by
    convert hinv0 using 1
    all_goals first | rfl | ring
  have hsum : HasDerivAt (fun t : ℝ => 1 + 1 / t) (-1 / y ^ 2) y := by
    convert hconst.add hinv using 1
    all_goals first | rfl | ring
  have hsqrt := hsum.sqrt hgoal_ne
  unfold nu_Q
  convert hsqrt using 1
  field_simp [hyne, hsqrt_ne]

theorem deep_universality_closed_form (y : ℝ) (hy : 0 < y) :
    2 * Real.sqrt y * C_Q y = 1 / Real.sqrt (1 + y) := by
  unfold C_Q
  have hyne : y ≠ 0 := ne_of_gt hy
  have hyge : 0 ≤ y := le_of_lt hy
  have hy1pos : 0 < 1 + 1 / y := by positivity
  have hsp : Real.sqrt (1 + 1 / y) ≠ 0 := by
    exact ne_of_gt (Real.sqrt_pos.mpr hy1pos)
  have hsy : Real.sqrt y ≠ 0 := by
    exact ne_of_gt (Real.sqrt_pos.mpr hy)
  have hprod : Real.sqrt y * Real.sqrt (1 + 1 / y) = Real.sqrt (1 + y) := by
    have hxy : 0 ≤ Real.sqrt y * Real.sqrt (1 + 1 / y) :=
      mul_nonneg (Real.sqrt_nonneg _) (Real.sqrt_nonneg _)
    have hsq : (Real.sqrt y * Real.sqrt (1 + 1 / y)) ^ 2 = 1 + y := by
      ring_nf
      have hyinv : 0 < y⁻¹ := inv_pos.mpr hy
      rw [Real.sq_sqrt hyge, Real.sq_sqrt (le_of_lt (by positivity : 0 < 1 + y⁻¹))]
      field_simp [hyne]
      ring
    exact ((Real.sqrt_eq_iff_mul_self_eq (by positivity : 0 ≤ 1 + y) hxy).2
      (by simpa [sq] using hsq.symm)).symm
  calc
    2 * Real.sqrt y * (1 / (2 * y * Real.sqrt (1 + 1 / y)))
        = Real.sqrt y / (y * Real.sqrt (1 + 1 / y)) := by
            field_simp [hyne, hsp, hsy]
    _ = 1 / (Real.sqrt y * Real.sqrt (1 + 1 / y)) := by
            -- rewrite ONLY the leading y (nth_rewrite): a blind rw would hit the y inside Real.sqrt y
            have hden : y * Real.sqrt (1 + 1 / y) =
                Real.sqrt y * (Real.sqrt y * Real.sqrt (1 + 1 / y)) := by
              nth_rewrite 1 [← Real.sq_sqrt hyge]
              ring
            rw [hden]
            field_simp [hsp, hsy]
    _ = 1 / Real.sqrt (1 + y) := by rw [hprod]

theorem deep_universality_limit :
    Tendsto (fun y : ℝ => 2 * Real.sqrt y * C_Q y) (𝓝[>] 0) (𝓝 1) := by
  have ht : Tendsto (fun y : ℝ => 1 / Real.sqrt (1 + y)) (𝓝[>] 0) (𝓝 1) := by
    have hcont : ContinuousAt (fun y : ℝ => 1 / Real.sqrt (1 + y)) 0 := by
      apply ContinuousAt.div
      · exact continuousAt_const
      · exact (Real.continuous_sqrt.comp (continuous_const.add continuous_id)).continuousAt
      · norm_num [Real.sqrt_one]
    simpa [Real.sqrt_one] using hcont.tendsto.mono_left nhdsWithin_le_nhds
  refine Filter.Tendsto.congr' ?_ ht
  have hgt : ∀ᶠ y : ℝ in 𝓝[>] (0 : ℝ), 0 < y := by
    exact eventually_iff.mpr (self_mem_nhdsWithin (s := Set.Ioi (0 : ℝ)) (a := (0 : ℝ)))
  exact hgt.mono (fun y hy => (deep_universality_closed_form y hy).symm)

end

#print axioms nu_Q_deriv
#print axioms deep_universality_closed_form
#print axioms deep_universality_limit
