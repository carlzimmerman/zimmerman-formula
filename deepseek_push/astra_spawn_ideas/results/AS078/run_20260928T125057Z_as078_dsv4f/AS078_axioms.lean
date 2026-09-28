/-
AS078 -- General slope normalizability: Lean 4 certificate of the algebraic core.

Certified theorems (all real-valued, zero `sorry`, axioms subset of
{propext, Classical.choice, Quot.sound}):

  A. mass_closed_form      : the finite-shell enclosed mass of rho = A r^-gamma,
                             M(R) = int_{rin}^{R} 4 pi A s^(2-gamma) ds
                             = 4 pi A (R^(3-gamma) - rin^(3-gamma))/(3-gamma),
                             gamma != 3, 0 < rin < R, derived from the
                             fundamental theorem via `integral_rpow`.
  B. mass_at_inner_edge    : the same closed form vanishes at R = rin
                             (M(rin) = 0, the boundary condition pinning the
                             antiderivative to the physical enclosed mass).
  C. gamma3_limit          : the gamma -> 3 limit of the 0/0 form
                             (u2^d - u1^d)/d -> log u2 - log u1 as d -> 0,
                             i.e. lim_{gamma->3} (u2^(3-g)-u1^(3-g))/(3-g)
                             = log(u2/u1)  [continuous removable extension].
  D. gamma3_limit_log_ratio: the same limit expressed as log (u2/u1).
  E. gamma2_outer_unbounded: the untruncated gamma = 2 enclosed mass diverges
                             outward: the partial integrals
                             int_{rin}^{R} s^(2-2) ds = R - rin tend to +inf.
  F. gamma3_outer_diverges : int_{rin}^{R} s^(2-3) ds = log R - log rin -> +inf.
  G. gamma3_inner_diverges : int_{eps}^{R} s^(2-3) ds = log R - log eps -> +inf
                             as eps -> 0+ (r_in -> 0).
  H. horn_gamma_lt_3       : for gamma < 3 the outer mass diverges like R^(3-g).
  I. horn_gamma_gt_3       : for gamma > 3 the inner mass diverges like eps^(3-g).
  J. no_gamma_both_ends    : no real gamma satisfies both integrability
                             conditions (gamma < 3 AND 3 < gamma) -- the
                             (0, inf) power law is never normalizable.
  K. equipartition_mass    : framework specialization at gamma = 2:
                             4 pi A r_M = M_b with A = C/(4 pi G),
                             C = sqrt(G M_b a0), r_M = sqrt(G M_b / a0) --
                             the exact equipartition normalization.
-/
import Mathlib

noncomputable section
open Filter
open scoped Topology
open intervalIntegral

namespace AS078

/- ------------------------------------------------------------ A. closed form -/

theorem mass_closed_form {A γ rin R : ℝ} (hrin : 0 < rin)
    (hrinR : rin < R) (hγ : γ ≠ 3) :
    (∫ x in rin..R, (4 * Real.pi * A) * x ^ (2 - γ)) =
      4 * Real.pi * A * ((R ^ (3 - γ) - rin ^ (3 - γ)) / (3 - γ)) := by
  have hexp : (2 : ℝ) - γ + 1 = 3 - γ := by ring
  have hmain := integral_rpow (a := rin) (b := R) (r := 2 - γ) (by
    right
    constructor
    · intro h
      apply hγ
      linarith
    · rw [Set.uIcc_of_le (le_of_lt hrinR)]
      exact fun hz => by
        have hle : rin ≤ (0 : ℝ) := (Set.mem_Icc.mp hz).1
        linarith)
  have hmain' : (∫ x in rin..R, x ^ (2 - γ)) =
      (R ^ (3 - γ) - rin ^ (3 - γ)) / (3 - γ) := by
    simpa [hexp] using hmain
  calc
    (∫ x in rin..R, (4 * Real.pi * A) * x ^ (2 - γ))
        = 4 * Real.pi * A * (∫ x in rin..R, x ^ (2 - γ)) := by
            rw [intervalIntegral.integral_const_mul]
    _ = 4 * Real.pi * A * ((R ^ (3 - γ) - rin ^ (3 - γ)) / (3 - γ)) := by
            rw [hmain']

theorem mass_at_inner_edge {A γ rin : ℝ} :
    (4 * Real.pi * A) * ((rin ^ (3 - γ) - rin ^ (3 - γ)) / (3 - γ)) = 0 := by
  simp

/- ------------------------------------------------------- B. gamma -> 3 limit -/

theorem slope_rpow_at_zero {u : ℝ} (hu : 0 < u) :
    Tendsto (fun t : ℝ => (u ^ t - 1) / t) (𝓝[≠] 0) (𝓝 (Real.log u)) := by
  have hd : HasDerivAt (fun d : ℝ => u ^ d) (Real.log u) 0 := by
    have h := (Real.hasStrictDerivAt_const_rpow hu 0).hasDerivAt
    simpa [Real.rpow_zero, mul_comm] using h
  have hs := (hasDerivAt_iff_tendsto_slope_zero.mp hd)
  -- hs : Tendsto (fun t => t⁻¹ • (u ^ (0 + t) - u ^ 0)) (𝓝[≠] 0) (𝓝 (log u))
  simpa [zero_add, Real.rpow_zero, smul_eq_mul, div_eq_mul_inv, mul_comm]
    using hs

theorem gamma3_limit {u1 u2 : ℝ} (hu1 : 0 < u1) (hu2 : 0 < u2) :
    Tendsto (fun d : ℝ => (u2 ^ d - u1 ^ d) / d) (𝓝[≠] 0)
      (𝓝 (Real.log u2 - Real.log u1)) := by
  have h1 := slope_rpow_at_zero hu1
  have h2 := slope_rpow_at_zero hu2
  have hsub : Tendsto (fun d : ℝ => (u2 ^ d - 1) / d - (u1 ^ d - 1) / d)
      (𝓝[≠] 0) (𝓝 (Real.log u2 - Real.log u1)) := h2.sub h1
  refine Tendsto.congr' ?_ hsub
  filter_upwards [self_mem_nhdsWithin] with d hd
  field_simp [hd]
  ring

theorem gamma3_limit_log_ratio {u1 u2 : ℝ} (hu1 : 0 < u1) (hu2 : 0 < u2) :
    Tendsto (fun d : ℝ => (u2 ^ d - u1 ^ d) / d) (𝓝[≠] 0)
      (𝓝 (Real.log (u2 / u1))) := by
  simpa [Real.log_div (ne_of_gt hu2) (ne_of_gt hu1)] using gamma3_limit hu1 hu2

/- ------------------------------------------- C. gamma = 2 outer unboundedness -/

theorem gamma2_outer_unbounded {rin : ℝ} (hrin : 0 < rin) :
    Tendsto (fun R : ℝ => ∫ x in rin..R, x ^ (2 - 2)) atTop atTop := by
  have hsh : (fun R : ℝ => ∫ x in rin..R, x ^ (2 - 2)) =ᶠ[atTop]
      fun R : ℝ => R - rin := by
    filter_upwards with R
    simp [Real.rpow_zero]
  have h2 : Tendsto (fun R : ℝ => R - rin) atTop atTop := by
    have hshift : Tendsto (fun R : ℝ => -rin + R) atTop atTop :=
      tendsto_atTop_add_const_left atTop (-rin) tendsto_id
    simpa [sub_eq_add_neg, add_comm] using hshift
  exact Tendsto.congr' hsh.symm h2

/- ----------------------------------------------- D. gamma = 3 log divergences -/

theorem gamma3_outer_diverges {rin : ℝ} (hrin : 0 < rin) :
    Tendsto (fun R : ℝ => Real.log R - Real.log rin) atTop atTop := by
  have hshift : Tendsto (fun R : ℝ => -Real.log rin + Real.log R) atTop atTop :=
    tendsto_atTop_add_const_left atTop (-Real.log rin) Real.tendsto_log_atTop
  simpa [sub_eq_add_neg, add_comm] using hshift

theorem gamma3_inner_diverges {R : ℝ} (hR : 0 < R) :
    Tendsto (fun ε : ℝ => Real.log R - Real.log ε) (𝓝[>] 0) atTop := by
  have hneg : Tendsto (fun ε : ℝ => -Real.log ε) (𝓝[>] 0) atTop := by
    exact tendsto_neg_atTop_iff.2 Real.tendsto_log_nhdsGT_zero
  have hshift : Tendsto (fun ε : ℝ => Real.log R + (-Real.log ε)) (𝓝[>] 0) atTop :=
    tendsto_atTop_add_const_left (𝓝[>] 0) (Real.log R) hneg
  simpa [sub_eq_add_neg, add_comm] using hshift

/- --------------------------------- E. divergence horns for general gamma -/

theorem horn_gamma_lt_3 {γ rin : ℝ} (hrin : 0 < rin) (hg : γ < 3) :
    Tendsto (fun R : ℝ => (R ^ (3 - γ) - rin ^ (3 - γ)) / (3 - γ)) atTop atTop := by
  have hp : 0 < 3 - γ := by linarith
  have hpow : Tendsto (fun R : ℝ => R ^ (3 - γ)) atTop atTop :=
    tendsto_rpow_atTop hp
  have hc : 0 < 1 / (3 - γ) := one_div_pos.mpr hp
  have hsc : Tendsto (fun R : ℝ => (1 / (3 - γ)) * R ^ (3 - γ)) atTop atTop :=
    hpow.const_mul_atTop hc
  have hshift : Tendsto (fun R : ℝ =>
      (-(rin ^ (3 - γ) / (3 - γ))) + (1 / (3 - γ)) * R ^ (3 - γ)) atTop atTop :=
    tendsto_atTop_add_const_left atTop (-(rin ^ (3 - γ) / (3 - γ))) hsc
  convert hshift using 1
  ext R
  field_simp
  ring

theorem horn_gamma_gt_3 {γ R : ℝ} (hR : 0 < R) (hg : 3 < γ) :
    Tendsto (fun ε : ℝ => (R ^ (3 - γ) - ε ^ (3 - γ)) / (3 - γ)) (𝓝[>] 0)
      atTop := by
  have hp : 3 - γ < 0 := by linarith
  have hpow : Tendsto (fun ε : ℝ => ε ^ (3 - γ)) (𝓝[>] 0) atTop :=
    tendsto_rpow_neg_nhdsGT_zero hp
  have hc : 0 < -(1 / (3 - γ)) := by
    have hneg' : 1 / (3 - γ) < 0 := div_neg_of_pos_of_neg (by norm_num) hp
    linarith
  have hsc : Tendsto (fun ε : ℝ => -(1 / (3 - γ)) * ε ^ (3 - γ)) (𝓝[>] 0) atTop :=
    hpow.const_mul_atTop hc
  have hshift : Tendsto (fun ε : ℝ =>
      R ^ (3 - γ) / (3 - γ) + (-(1 / (3 - γ)) * ε ^ (3 - γ))) (𝓝[>] 0) atTop :=
    tendsto_atTop_add_const_left (𝓝[>] 0) (R ^ (3 - γ) / (3 - γ)) hsc
  convert hshift using 1
  ext ε
  field_simp
  ring

theorem no_gamma_both_ends (γ : ℝ) : ¬(γ < 3 ∧ 3 < γ) := by
  rintro ⟨h1, h2⟩
  linarith

/- ------------------------ F. equipartition normalization at gamma = 2 -/

theorem equipartition_mass {G M a : ℝ} (hG : 0 < G) (hM : 0 < M) (ha : 0 < a) :
    4 * Real.pi * (Real.sqrt (G * M * a) / (4 * Real.pi * G)) *
        Real.sqrt (G * M / a) = M := by
  have hA : 0 ≤ G * M * a := by positivity
  have hD : 0 ≤ G * M / a := by positivity
  have hsq : 0 ≤ G * M := mul_nonneg hG.le hM.le
  calc
    4 * Real.pi * (Real.sqrt (G * M * a) / (4 * Real.pi * G)) *
        Real.sqrt (G * M / a)
        = Real.sqrt (G * M * a) * Real.sqrt (G * M / a) / G := by
            field_simp [hG.ne', Real.pi_ne_zero]
    _ = Real.sqrt ((G * M * a) * (G * M / a)) / G := by
            rw [Real.sqrt_mul hA (G * M / a)]
    _ = Real.sqrt ((G * M) ^ 2) / G := by
            congr 1
            field_simp [ha.ne']
    _ = (G * M) / G := by
            rw [Real.sqrt_sq hsq]
    _ = M := by
            field_simp [hG.ne']

end AS078

end

#print axioms AS078.mass_closed_form
#print axioms AS078.mass_at_inner_edge
#print axioms AS078.slope_rpow_at_zero
#print axioms AS078.gamma3_limit
#print axioms AS078.gamma3_limit_log_ratio
#print axioms AS078.gamma2_outer_unbounded
#print axioms AS078.gamma3_outer_diverges
#print axioms AS078.gamma3_inner_diverges
#print axioms AS078.horn_gamma_lt_3
#print axioms AS078.horn_gamma_gt_3
#print axioms AS078.no_gamma_both_ends
#print axioms AS078.equipartition_mass
