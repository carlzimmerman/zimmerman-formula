/-
AS049 -- Scale derivatives of a constitutive force (Lean 4 certificate).

Registered seed: deepseek_push/astra_spawn_ideas/AS049_scale_derivatives_of_a_constitutive_force.md
(task_sha256 ed91aefffb5a8b8615d09ebf7f90fe82d5ecf10a767948175f61c909b9b2a479).

Certified here (exact real-arithmetic statements):

  A  Q-branch chain rule:  d/da0 sqrt(B^2 + a0 B) = B / (2 sqrt(B^2 + a0 B))
       -- the principal-test identity dg/da0 = -(B^2/a0^2) nu'(y) evaluated on Q
          (nu_Q(y) = sqrt(1 + 1/y)), both sides of the chain rule.
  B  Q-branch elasticity:  eps_Q(y) = -y nu_Q'(y)/nu_Q(y) = 1/(2(y+1))
       with the exact nu_Q'(y) = -1/(2 y^2 sqrt(1+1/y));
       deep limit: eps_Q(y) -> 1/2 as y -> 0+  (Tendsto statement).
  C  C = a0 * r_M (positive-root identity from C^2 = G M_b a0 = (a0 r_M)^2)
       and the slab-ceiling crossing radius:  C/(4GR) = a0/(4 pi G)  =>  R = pi * r_M.
  D  Projected surface density of the log phantom (r = sqrt(R^2 + z^2),
       rho_ph = C/(4 pi G r^2)):
       d/dz [(1/R) arctan(z/R)] = 1/(R^2 + z^2),
       integral_0^T 1/(R^2+z^2) dz = (1/R) arctan(T/R),
       tendsto_T->oo integral = pi/(2 R)   -- the exact Abel half-column, and
       2 * (C/(4 pi G)) * (pi/(2 R)) = C/(4 G R)  (coefficient bookkeeping,
       face-on == edge-on column of the spherical monopole).
  E  Central column through the disk plane:
       d/dz [-(1/z)] = 1/z^2,
       integral_{r_in}^T 1/z^2 dz = 1/r_in - 1/T,
       tendsto_T->oo integral = 1/r_in, and
       2 * (C/(4 pi G)) * (1/r_in) = C/(2 pi G r_in)
       -- the inner-cutoff floor (capped central column).

The capped Abel form Sigma_cap(Rp;R) = (C/(2 pi G Rp)) arccos(Rp/R) (AS090),
the RAR/MONO elasticity closed forms, the MU2/EXP implicit derivatives, and all
finite grids are verified numerically in the companion Python runs (residuals
recorded in checks_*.json); y_p, y_star and pi enter only as exact symbols here.

Axiom discipline: zero `sorry`; printed axioms must be a subset of
{propext, Classical.choice, Quot.sound}.
-/
import Mathlib
import Mathlib.Tactic

noncomputable section

open Real Filter
open scoped Topology

namespace AS049

-- ==========================================================================
-- A. Q-branch chain rule:  d/da0 sqrt(B^2 + a0 B) = B / (2 sqrt(B^2 + a0 B))
-- ==========================================================================

theorem q_chain_rule (B a0 : ℝ) (hB : 0 < B) (ha : 0 < a0) :
    deriv (fun a : ℝ => Real.sqrt (B * B + a * B)) a0 =
      B / (2 * Real.sqrt (B * B + a0 * B)) := by
  have hpos : 0 < B * B + a0 * B := by
    nlinarith [sq_pos_of_ne_zero (ne_of_gt hB), mul_pos ha hB]
  have hlin : HasDerivAt (fun a : ℝ => B * B + a * B) B a0 := by
    have hA : HasDerivAt (fun a : ℝ => a * B) B a0 := by
      simpa using (hasDerivAt_id a0).mul_const B
    simpa [add_comm] using hA.add_const (B * B)
  have hsqrt : HasDerivAt Real.sqrt (1 / (2 * Real.sqrt (B * B + a0 * B)))
      (B * B + a0 * B) := by
    exact Real.hasDerivAt_sqrt (ne_of_gt hpos)
  have hmain : HasDerivAt (fun a : ℝ => Real.sqrt (B * B + a * B))
      (1 / (2 * Real.sqrt (B * B + a0 * B)) * B) a0 := by
    simpa [Function.comp_def, mul_comm, mul_left_comm, mul_assoc]
      using hsqrt.comp a0 hlin
  rw [hmain.deriv]
  field_simp [ne_of_gt hpos]

-- ==========================================================================
-- B. Q-branch nu'(y) and elasticity  eps_Q(y) = 1/(2(y+1))
-- ==========================================================================

theorem q_nu_deriv (y0 : ℝ) (hy : 0 < y0) :
    deriv (fun y : ℝ => Real.sqrt (1 + 1 / y)) y0 =
      -1 / (2 * y0 ^ 2 * Real.sqrt (1 + 1 / y0)) := by
  have harg : HasDerivAt (fun y : ℝ => 1 + 1 / y) (-(y0 ^ 2)⁻¹) y0 := by
    have hinv : HasDerivAt (fun y : ℝ => y⁻¹) (-(y0 ^ 2)⁻¹) y0 :=
      hasDerivAt_inv (ne_of_gt hy)
    simpa [one_div] using hinv.const_add 1
  have hsq : HasDerivAt Real.sqrt (1 / (2 * Real.sqrt (1 + 1 / y0))) (1 + 1 / y0) := by
    exact Real.hasDerivAt_sqrt (by positivity : 1 + 1 / y0 ≠ 0)
  have hmain : HasDerivAt (fun y : ℝ => Real.sqrt (1 + 1 / y))
      (1 / (2 * Real.sqrt (1 + 1 / y0)) * (-(y0 ^ 2)⁻¹)) y0 := by
    simpa [Function.comp_def] using hsq.comp y0 harg
  rw [hmain.deriv]
  field_simp [ne_of_gt hy]

theorem q_elasticity_closed (y0 : ℝ) (hy : 0 < y0) :
    -(y0 * deriv (fun y : ℝ => Real.sqrt (1 + 1 / y)) y0 /
        Real.sqrt (1 + 1 / y0)) = 1 / (2 * (y0 + 1)) := by
  rw [q_nu_deriv y0 hy]
  have hs : (Real.sqrt ((y0 + 1) / y0)) ^ 2 = (y0 + 1) / y0 := by
    exact Real.sq_sqrt (by positivity : 0 ≤ (y0 + 1) / y0)
  field_simp [ne_of_gt hy, ne_of_gt (by positivity : 0 < y0 + 1)]
  rw [hs]
  field_simp [ne_of_gt hy]

theorem q_epsilon_deep_limit :
    Tendsto (fun y : ℝ => 1 / (2 * (y + 1))) (𝓝[>] 0) (𝓝 (1 / 2)) := by
  have hc : ContinuousAt (fun y : ℝ => 1 / (2 * (y + 1))) 0 := by
    exact (continuousAt_const.div₀ (by fun_prop : ContinuousAt (fun y : ℝ => 2 * (y + 1)) 0)
      (by norm_num : (2 : ℝ) * (0 + 1) ≠ 0))
  have hv : (fun y : ℝ => 1 / (2 * (y + 1))) 0 = 1 / 2 := by norm_num
  simpa [hv] using hc.tendsto.mono_left nhdsWithin_le_nhds

-- ==========================================================================
-- C.  C = a0 * r_M  and the slab-ceiling crossing radius  R_crit = pi * r_M
-- ==========================================================================

theorem amu_rM_identity (G M a0 : ℝ) (hG : 0 < G) (hM : 0 < M) (ha : 0 < a0) :
    a0 * Real.sqrt (G * M / a0) = Real.sqrt (G * M * a0) := by
  have hs : (a0 * Real.sqrt (G * M / a0)) ^ 2 = (Real.sqrt (G * M * a0)) ^ 2 := by
    rw [mul_pow]
    rw [Real.sq_sqrt (le_of_lt (div_pos (mul_pos hG hM) ha))]
    rw [Real.sq_sqrt (le_of_lt (mul_pos (mul_pos hG hM) ha))]
    field_simp [ne_of_gt ha] <;> ring
  have hpos1 : 0 ≤ a0 * Real.sqrt (G * M / a0) :=
    mul_nonneg (le_of_lt ha) (Real.sqrt_nonneg _)
  have hpos2 : 0 ≤ Real.sqrt (G * M * a0) := Real.sqrt_nonneg _
  have habs := (sq_eq_sq_iff_abs_eq_abs _ _).mp hs
  simpa [abs_of_nonneg hpos1, abs_of_nonneg hpos2] using habs

theorem crossing_radius (a0 G R rM C : ℝ) (hR : 0 < R) (hG : 0 < G)
    (ha : 0 < a0) (hC : C = a0 * rM)
    (hCe : C / (4 * G * R) = a0 / (4 * Real.pi * G)) : R = Real.pi * rM := by
  have h1 : C * Real.pi = a0 * R := by
    field_simp [ne_of_gt hR, ne_of_gt hG, ne_of_gt Real.pi_pos] at hCe ⊢
    exact hCe
  rw [hC] at h1
  field_simp [ne_of_gt ha, ne_of_gt Real.pi_pos] at h1
  simpa [mul_comm] using h1.symm

-- ==========================================================================
-- D. Face-on == edge-on Abel column of the log phantom:  -> C/(4 G R)
-- ==========================================================================

theorem abel_hasDerivAt (R z : ℝ) (hR : 0 < R) :
    HasDerivAt (fun u : ℝ => (1 / R) * Real.arctan (u / R)) (1 / (R ^ 2 + z ^ 2)) z := by
  have hid : HasDerivAt (fun u : ℝ => u / R) (1 / R) z :=
    (hasDerivAt_id z).div_const R
  have hat : HasDerivAt Real.arctan (1 / (1 + (z / R) ^ 2)) (z / R) :=
    Real.hasDerivAt_arctan (z / R)
  have hc : HasDerivAt (Real.arctan ∘ fun u : ℝ => u / R)
      (1 / (1 + (z / R) ^ 2) * (1 / R)) z :=
    hat.comp z hid
  have hF : HasDerivAt (fun u : ℝ => (1 / R) * Real.arctan (u / R))
      ((1 / R) * (1 / (1 + (z / R) ^ 2) * (1 / R))) z := by
    simpa [Function.comp_def] using hc.const_mul (1 / R)
  convert hF using 1
  field_simp [ne_of_gt hR]

theorem abel_antiderivative (R z : ℝ) (hR : 0 < R) :
    deriv (fun u : ℝ => (1 / R) * Real.arctan (u / R)) z = 1 / (R ^ 2 + z ^ 2) := by
  exact (abel_hasDerivAt R z hR).deriv

theorem abel_integral_finite (R T : ℝ) (hR : 0 < R) (hT : 0 ≤ T) :
    ∫ u in 0..T, 1 / (R ^ 2 + u ^ 2) = (1 / R) * Real.arctan (T / R) := by
  have hpoly : ContinuousOn (fun u : ℝ => R ^ 2 + u ^ 2) (Set.uIcc 0 T) := by fun_prop
  have hne : ∀ x ∈ Set.uIcc 0 T, R ^ 2 + x ^ 2 ≠ 0 := by
    intro x hx
    nlinarith [sq_pos_of_ne_zero (ne_of_gt hR)]
  have hint : IntervalIntegrable (fun u : ℝ => 1 / (R ^ 2 + u ^ 2))
      MeasureTheory.volume 0 T := by
    apply ContinuousOn.intervalIntegrable
    exact ContinuousOn.div₀
      (by fun_prop : ContinuousOn (fun u : ℝ => (1 : ℝ)) (Set.uIcc 0 T)) hpoly hne
  have h1 := intervalIntegral.integral_eq_sub_of_hasDerivAt_of_le hT
    (by fun_prop : ContinuousOn (fun u : ℝ => (1 / R) * Real.arctan (u / R))
      (Set.Icc 0 T))
    (by
      intro x hx
      exact abel_hasDerivAt R x hR)
    hint
  rw [h1]
  simp [Real.arctan_zero]

theorem abel_integral_atTop (R : ℝ) (hR : 0 < R) :
    Tendsto (fun T : ℝ => ∫ u in 0..T, 1 / (R ^ 2 + u ^ 2)) atTop
      (𝓝 (Real.pi / (2 * R))) := by
  have heq : (fun T : ℝ => ∫ u in 0..T, 1 / (R ^ 2 + u ^ 2)) =ᶠ[atTop]
      (fun T : ℝ => (1 / R) * Real.arctan (T / R)) := by
    rw [EventuallyEq]
    refine eventually_atTop.2 ⟨0, ?_⟩
    intro T hT
    exact abel_integral_finite R T hR hT
  have htr : Tendsto (fun T : ℝ => T / R) atTop atTop := by
    simpa [div_eq_mul_inv, mul_comm] using
      (tendsto_id.atTop_mul_const (by positivity : 0 < 1 / R))
  have hat : Tendsto Real.arctan atTop (𝓝 (Real.pi / 2)) :=
    Real.tendsto_arctan_atTop.mono_right nhdsWithin_le_nhds
  have hat2 : Tendsto (fun T : ℝ => Real.arctan (T / R)) atTop (𝓝 (Real.pi / 2)) := by
    simpa [Function.comp_def] using hat.comp htr
  have hlim : Tendsto (fun T : ℝ => (1 / R) * Real.arctan (T / R)) atTop
      (𝓝 ((1 / R) * (Real.pi / 2))) :=
    hat2.const_mul (1 / R)
  have hc : Tendsto (fun T : ℝ => ∫ u in 0..T, 1 / (R ^ 2 + u ^ 2)) atTop
      (𝓝 ((1 / R) * (Real.pi / 2))) :=
    Tendsto.congr' heq.symm hlim
  simpa [div_eq_mul_inv, mul_comm, mul_left_comm, mul_assoc] using hc

theorem sigma_abel_coeff (C G R : ℝ) (hG : G ≠ 0) (hR : R ≠ 0) :
    2 * (C / (4 * Real.pi * G)) * (Real.pi / (2 * R)) = C / (4 * G * R) := by
  field_simp [hG, hR, ne_of_gt Real.pi_pos]

-- ==========================================================================
-- E. Central column through the disk plane:  floor = C/(2 pi G r_in)
-- ==========================================================================

theorem central_column_hasDerivAt (z0 : ℝ) (hz : z0 ≠ 0) :
    HasDerivAt (fun z : ℝ => -z⁻¹) ((z0 ^ 2)⁻¹) z0 := by
  have hinv : HasDerivAt (fun y : ℝ => y⁻¹) (-(z0 ^ 2)⁻¹) z0 :=
    hasDerivAt_inv hz
  have hmul : HasDerivAt (fun y : ℝ => (-1 : ℝ) * y⁻¹)
      ((-1 : ℝ) * (-(z0 ^ 2)⁻¹)) z0 :=
    hinv.const_mul (-1)
  simpa [mul_neg, neg_mul, neg_neg] using hmul

theorem central_column_antiderivative (z0 : ℝ) (hz : z0 ≠ 0) :
    deriv (fun z : ℝ => -z⁻¹) z0 = (z0 ^ 2)⁻¹ := by
  exact (central_column_hasDerivAt z0 hz).deriv

theorem central_column_finite (r_in T : ℝ) (hr : 0 < r_in) (hT : r_in ≤ T) :
    ∫ u in r_in..T, 1 / u ^ 2 = 1 / r_in - 1 / T := by
  have hneF : ∀ x ∈ Set.Icc r_in T, x ≠ 0 := by
    intro x hx
    exact ne_of_gt (lt_of_lt_of_le hr hx.1)
  have hcF : ContinuousOn (fun u : ℝ => -(1 / u)) (Set.Icc r_in T) := by
    have hci : ContinuousOn (fun u : ℝ => 1 / u) (Set.Icc r_in T) :=
      ContinuousOn.div₀
        (by fun_prop : ContinuousOn (fun u : ℝ => (1 : ℝ)) (Set.Icc r_in T))
        (by fun_prop : ContinuousOn (fun u : ℝ => u) (Set.Icc r_in T)) hneF
    exact hci.neg
  have hpoly : ContinuousOn (fun u : ℝ => u ^ 2) (Set.uIcc r_in T) := by fun_prop
  have hne2 : ∀ x ∈ Set.uIcc r_in T, x ^ 2 ≠ 0 := by
    intro x hx
    have hxr : r_in ≤ x := by simpa [Set.uIcc, min_eq_left hT] using hx.1
    exact pow_ne_zero 2 (ne_of_gt (lt_of_lt_of_le hr hxr))
  have hint : IntervalIntegrable (fun u : ℝ => 1 / u ^ 2) MeasureTheory.volume r_in T := by
    apply ContinuousOn.intervalIntegrable
    exact ContinuousOn.div₀
      (by fun_prop : ContinuousOn (fun u : ℝ => (1 : ℝ)) (Set.uIcc r_in T)) hpoly hne2
  have h1 := intervalIntegral.integral_eq_sub_of_hasDerivAt_of_le hT hcF
    (by
      intro x hx
      have hx0 : x ≠ 0 := ne_of_gt (lt_trans hr hx.1)
      simpa [one_div] using central_column_hasDerivAt x hx0)
    hint
  rw [h1]
  field_simp [ne_of_gt hr, ne_of_gt (lt_of_lt_of_le hr hT)] <;> ring

theorem central_column_atTop (r_in : ℝ) (hr : 0 < r_in) :
    Tendsto (fun T : ℝ => ∫ u in r_in..T, 1 / u ^ 2) atTop (𝓝 (1 / r_in)) := by
  have heq : (fun T : ℝ => 1 / r_in - 1 / T) =ᶠ[atTop]
      (fun T : ℝ => ∫ u in r_in..T, 1 / u ^ 2) := by
    rw [EventuallyEq]
    refine eventually_atTop.2 ⟨r_in, ?_⟩
    intro T hT
    exact (central_column_finite r_in T hr hT).symm
  have hlim : Tendsto (fun T : ℝ => 1 / r_in - 1 / T) atTop (𝓝 (1 / r_in)) := by
    simpa using (Tendsto.const_sub (1 / r_in)) tendsto_inv_atTop_zero
  exact Tendsto.congr' heq hlim

theorem central_column_coeff (C G r_in : ℝ) (hG : G ≠ 0) (hr : r_in ≠ 0) :
    2 * (C / (4 * Real.pi * G)) * (1 / r_in) = C / (2 * Real.pi * G * r_in) := by
  field_simp [hG, hr, ne_of_gt Real.pi_pos] <;> ring

end AS049

#check AS049.q_chain_rule
#check AS049.q_nu_deriv
#check AS049.q_elasticity_closed
#check AS049.q_epsilon_deep_limit
#check AS049.amu_rM_identity
#check AS049.crossing_radius
#check AS049.abel_hasDerivAt
#check AS049.abel_antiderivative
#check AS049.abel_integral_finite
#check AS049.abel_integral_atTop
#check AS049.sigma_abel_coeff
#check AS049.central_column_hasDerivAt
#check AS049.central_column_antiderivative
#check AS049.central_column_finite
#check AS049.central_column_atTop
#check AS049.central_column_coeff

-- axiom audit (zero sorry required)
#print axioms AS049.q_chain_rule
#print axioms AS049.q_elasticity_closed
#print axioms AS049.abel_integral_atTop
#print axioms AS049.central_column_atTop
#print axioms AS049.crossing_radius
#print axioms AS049.sigma_abel_coeff