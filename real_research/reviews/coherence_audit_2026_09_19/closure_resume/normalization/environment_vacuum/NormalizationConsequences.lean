import Mathlib

/-!
Exact normalization consequences, independently formalized 2026-09-19.

Scope: the analytic integral lower bound is an EXPLICIT HYPOTHESIS below.
This file does not formalize integration of alpha, the action variation,
the physical meaning of kappa, or full gravitational health. It certifies
the algebraic consequence and a primitive-constant ambiguity separately.
No sorry, custom axioms, or numerical oracle.
-/

noncomputable section
namespace NormalizationConsequences

/-- Measured-G coefficient squared, under the action normalization derived
    in the accompanying report. This definition is not an action derivation. -/
def environmentKappaSq (a a0 I : ℝ) : ℝ :=
  8 * Real.pi * (2 - a) * a0 ^ 2 / I

/-- Conditional consequence of the analytically derived area bound.
    `harea` is the unformalized integral theorem supplied as a hypothesis. -/
theorem coefficient_bound_from_area
    (a A g0 a0 I : ℝ) (ha : 0 < a) (ha2 : a < 2)
    (hA : a < A) (hg0 : 0 < g0)
    (harea : g0 ^ 2 * A * (A - a) / a ≤ I) :
    environmentKappaSq a a0 I ≤
      8 * Real.pi * (2 - a) * a / (A * (A - a)) * (a0 / g0) ^ 2 := by
  have hApos : 0 < A := lt_trans ha hA
  have hdiff : 0 < A - a := sub_pos.mpr hA
  have hB : 0 < g0 ^ 2 * A * (A - a) / a := by positivity
  have hnum : 0 ≤ 8 * Real.pi * (2 - a) * a0 ^ 2 := by positivity
  unfold environmentKappaSq
  calc
    8 * Real.pi * (2 - a) * a0 ^ 2 / I ≤
        8 * Real.pi * (2 - a) * a0 ^ 2 /
          (g0 ^ 2 * A * (A - a) / a) :=
      div_le_div_of_nonneg_left hnum hB harea
    _ = 8 * Real.pi * (2 - a) * a / (A * (A - a)) * (a0 / g0) ^ 2 := by
      field_simp [ne_of_gt ha, ne_of_gt hApos, ne_of_gt hdiff, ne_of_gt hg0]

/-- At alpha_lo=10^-7, A=1/2, and g0=a0, the supplied area bound excludes
    kappa^2=1/4 by a large margin. This uses only pi<4, not decimal evaluation. -/
theorem same_scale_excludes_half
    (a0 I : ℝ) (ha0 : 0 < a0)
    (harea : (4999999 / 2 : ℝ) * a0 ^ 2 ≤ I) :
    environmentKappaSq (1 / 10000000) a0 I < (1 / 4 : ℝ) := by
  have hs : 0 < a0 ^ 2 := sq_pos_of_pos ha0
  have hI : 0 < I := by nlinarith
  have hp : Real.pi < 4 := Real.pi_lt_four
  have hc : 8 * Real.pi * (2 - (1 / 10000000 : ℝ)) < 64 := by
    nlinarith [Real.pi_pos]
  have hn := mul_lt_mul_of_pos_right hc hs
  unfold environmentKappaSq
  apply (div_lt_iff₀ hI).2
  nlinarith

/-- The rational input in the preceding theorem is exactly the sharp area
    bound's coefficient at alpha_lo=10^-7 and A=1/2. -/
theorem proposed_area_coefficient :
    (1 / 2 : ℝ) * ((1 / 2 : ℝ) - 1 / 10000000) / (1 / 10000000) =
      (4999999 / 2 : ℝ) := by norm_num

def aqualKappaSq (n F0 : ℝ) : ℝ := 8 * Real.pi / (n ^ 2 * F0)

/-- Adding a primitive constant preserves the derivative at every point
    where the original derivative is known. -/
theorem primitive_shift_preserves_flux
    (f : ℝ → ℝ) (mu z c : ℝ) (hf : HasDerivAt f mu z) :
    HasDerivAt (fun x => f x + c) mu z := by
  exact hf.add_const c

/-- The same n=2 derivative law permits distinct coefficients under the
    declared AQUAL vacuum normalization, depending on the primitive value. -/
theorem two_normalizations :
    aqualKappaSq 2 (8 * Real.pi) = (1 / 4 : ℝ) ∧
    aqualKappaSq 2 (2 * Real.pi) = 1 ∧
    (8 * Real.pi ≠ 2 * Real.pi) := by
  constructor
  · unfold aqualKappaSq
    field_simp [Real.pi_ne_zero]
    ring
  constructor
  · unfold aqualKappaSq
    field_simp [Real.pi_ne_zero]
    ring
  · nlinarith [Real.pi_pos]

/-- Positivity of the finite-profile analytic lower bound. The actual
    profile-to-bound inequality remains in the report, not in this theorem. -/
theorem finite_profile_health_margin_positive (a : ℝ) (ha : 0 < a) :
    0 < a * (1 - 3 * Real.sqrt 3 / 8) := by
  have hs : (Real.sqrt 3) ^ 2 = (3 : ℝ) := Real.sq_sqrt (by norm_num)
  have hn : 0 ≤ Real.sqrt (3 : ℝ) := Real.sqrt_nonneg 3
  have hm : 0 < 1 - 3 * Real.sqrt (3 : ℝ) / 8 := by nlinarith
  exact mul_pos ha hm

end NormalizationConsequences

#print axioms NormalizationConsequences.coefficient_bound_from_area
#print axioms NormalizationConsequences.same_scale_excludes_half
#print axioms NormalizationConsequences.proposed_area_coefficient
#print axioms NormalizationConsequences.primitive_shift_preserves_flux
#print axioms NormalizationConsequences.two_normalizations
#print axioms NormalizationConsequences.finite_profile_health_margin_positive
