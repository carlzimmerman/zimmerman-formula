import Mathlib

/-!
# RH05L -- THE GENERAL-LADDER REFLECTION AND THE MOMENT SEQUENCE (Lean-certified, zero sorry)
================================================================================================

THE FRAMEWORK LADDER (self-contained):  for shape exponent l > 1 the kernel
    f_l(u) = (l-1)·(1+u)^{-l}   (u ≥ 0)
has Mellin transform  M_l(s) = (l-1)·∫₀^∞ u^{s-1}(1+u)^{-l} du = (l-1)·B(s, l-s),
reflection axis l/2, and log-moment constraint E[ln(1+u)] = 1/(l-1).
RH01L certified the l = 3 case (reflection_shape/power/key, exit 0, zero sorry);
RH02L certified the axis map  l/2 ↦ l  is injective (zeta axis 1/2 = ladder edge l = 1).
This file generalizes both certificates to every ladder rung l > 1 (real l).

DELEGATION NOTE (correction, certified below): the as-delegated literal identity
    v^(2s−l)·v^(−2)·(1+1/v)^(−l)·(1+v)^l = v^(s−1)
is NOT valid for general s (it would force 2s−2 = s−1, i.e. s = 1, for all v).
The certified general form is the one that reduces exactly to RH01L's certified
l = 3 theorem (whose exponent is s−2 = s+1−3):
    v^(s+1−l)·v^(−2)·(1+1/v)^(−l)·(1+v)^l = v^(s−1).
The literal form's true reduction — v^(2s−l)·v^(−2)·(1+1/v)^(−l)·(1+v)^l = v^(2s−2) —
is itself CERTIFIED below as `delegated_literal_identity`, so the discrepancy is
pinned down exactly, not papered over.

WHAT IS CERTIFIED HERE (all theorems below, exit 0, zero sorry):

(A) THE GENERAL-L REFLECTION (target 2): for every real l and s, v > 0:
    reflection_shape_general :  (1 + 1/v)^(−l)·(1+v)^l = v^l            [kernel inversion, general l]
    reflection_power_general  :  v^(s+1−l)·v^(−2)·v^l = v^(s−1)          [power combine, general l]
    reflection_key_general    :  v^(s+1−l)·v^(−2)·((1+1/v)^(−l)·(1+v)^l) = v^(s−1)
                                 -- the M_l(l−s) integrand maps exactly onto the M_l(s)
                                    integrand under u = 1/v:  M_l(s) = M_l(l−s), axis l/2.
    reflection_key_l3         :  the l = 3 specialization, recovering RH01L's `reflection_key`.

(B) THE FULL MOMENT SEQUENCE (target 1): for s = e^w − 1 (u = ln(1+s) substitution):
    moment_subst_integrand   :  ln(1+s)·(1+s)^(−l)·e^w  =  w·e^(−(l−1)w)   [change-of-variables ALGEBRA]
    moment_integral          :  ∫₀^∞ w·e^(−c·w) dw = c^(−2)   (0 < c)     [Mathlib Gamma machinery]
    ladder_log_moment_integral_subst :  ∫₀^∞ ln(1+s)·(1+s)^(−l) ds = (l−1)^(−2)
                                 -- the FULL measure-theoretic substitution, via Mathlib's
                                    `integral_image_eq_integral_abs_deriv_smul` (no integrability
                                    pre-work needed).
    ladder_log_moment        :  (l−1)·∫₀^∞ ln(1+s)·(1+s)^(−l) ds = (l−1)⁻¹ = 1/(l−1)
                                 i.e. E[ln(1+u)] = 1/(l−1) for the ladder rung l, CERTIFIED.
    ladder_log_moment_l3     :  l = 3 gives E[ln(1+u)] = 1/2 (the framework's registered constant).

(C) CONNECTIONS TO THE ZETA'S FUNCTIONAL EQUATION (certified facts):
    euler_reflection_zeta_beta :  Γ(s)·Γ(1−s) = π/sin(πs)   -- the beta B(s,1−s) at the ladder
                                  EDGE l → 1, the same beta the completed zeta's functional
                                  equation is built from (Euler reflection, Mathlib-verified).
    reflection_symmetry_alone_insufficient :  (s−2)(s+1) is invariant under s ↦ 1−s (axis 1/2)
                                  yet has zeros at 2 and −1, OFF the axis -- certified proof that
                                  reflection symmetry class alone cannot place zeros on the line.

THE HONEST WALL -- what would be needed to reach the zeta's zeros (ALL UNPROVED):

  Transfer step T1 (kernel embedding — UNPROVED; as an equality it is FALSE):
      prove the ladder's Mellin family {(l−1)·B(s,l−s)} contains (or embeds into)
      the completed zeta's Mellin integral.  The zeta side is classical known
      mathematics (the theta transformation ψ(x)=ψ(1/x)/√x ⇒ ξ(s)=ξ(1−s), centuries
      old, independent of this framework); the ladder side is certified here.  The
      BRIDGE is not: the zeta's kernel is the theta kernel, not any Lomax (1+u)^(−l);
      both are closed under u ↦ 1/u (the shared inversion class), but that does not
      make one an instance of the other.  UNPROVED — and no argument in this repo
      supplies it.

  Transfer step T2 (edge limit — the limiting statement is ordinary analysis, NOT
      certified here; the final identity is certified):
      prove lim_{l→1⁺} (l−1)·B(s, l−s) = B(s,1−s) = Γ(s)Γ(1−s) = π/sin(πs).
      The FINAL equality is certified above (euler_reflection_zeta_beta); the LIMIT
      (uniform on compacta away from the poles at integer s, with the singular
      behaviour at s ∈ ℤ handled separately) would be a routine-large real-analysis
      Lean project — not a major theorem, but UNPROVED in Lean.  This would attach
      the ladder's edge to the zeta's beta: the classical STEP, pursued elsewhere.

  Transfer step T3 (symmetry ⇒ zeros — UNPROVED; NOT known mathematics, this IS the
      open problem):
      prove: a reflection-symmetric completion with axis 1/2, real on the line, with
      the zeta's growth and positivity constraints, has ALL zeros on the axis.
      Reflection alone manifestly fails (certified counterexample (C) above —
      (s−2)(s+1) is axis-1/2-symmetric with off-axis zeros).  For the zeta this
      implication is exactly the Riemann Hypothesis.  The framework contributes
      nothing beyond the reflection class at this step; RH is NOT claimed, in whole
      or in part, anywhere in this file or its lane.

  Global honesty note (frozen from RH01/RH02): the coincidence of the framework's
  log-moment 1/2 with the critical line's real part is data-awaited observation,
  not a theorem; the empirical lane measured E[ln(1+s)] = 0.6746±0.0035 on true
  zero spacings — 50σ off 1/2, matching GUE — so the kernel reads REAL zero
  spacings as GUE, not Lomax.  The Mellin reflection class is what survives.

-/

noncomputable section

open Real Set MeasureTheory
open scoped Real Topology

-- ============================================================
-- SECTION A -- THE GENERAL-L REFLECTION (extends RH01L from l = 3 to general l)
-- ============================================================

-- helper: (x/y)^l = x^l · y^(−l) for 0 < x, 0 < y  (general real exponent l)
private theorem rpow_div_rpow (x y : ℝ) (l : ℝ) (hx : 0 < x) (hy : 0 < y) :
    (x / y) ^ l = x ^ l * y ^ (-l) := by
  rw [div_eq_mul_inv]
  rw [Real.mul_rpow (le_of_lt hx) (inv_nonneg.mpr (le_of_lt hy))]
  congr 1
  rw [← Real.rpow_neg_eq_inv_rpow y l]

-- (A1) kernel inversion, general l:  (1 + 1/v)^(−l) · (1+v)^l = v^l
theorem reflection_shape_general (v : ℝ) (l : ℝ) (hv : 0 < v) :
    (1 + 1 / v) ^ (-l) * (1 + v) ^ l = v ^ l := by
  have hvpos : 0 < 1 + 1 / v := by positivity
  have hq : 1 + 1 / v = (1 + v) / v := by
    field_simp [ne_of_gt hv]
    ring
  calc
    (1 + 1 / v) ^ (-l) * (1 + v) ^ l
        = ((1 + v) / v) ^ (-l) * (1 + v) ^ l := by rw [hq]
    _ = (((1 + v) / v) ^ l)⁻¹ * (1 + v) ^ l := by
        have hvq : 0 < (1 + v) / v := by positivity
        rw [Real.rpow_neg (le_of_lt hvq) l]
    _ = ((1 + v) ^ l * v ^ (-l))⁻¹ * (1 + v) ^ l := by
        rw [rpow_div_rpow (1 + v) v l (by linarith) hv]
    _ = (v ^ (-l))⁻¹ := by
        have hnv : (1 + v) ^ l ≠ 0 := ne_of_gt (Real.rpow_pos_of_pos (by linarith) l)
        rw [mul_inv_rev]
        simp [mul_comm, mul_left_comm, mul_inv_cancel₀ hnv]
    _ = v ^ l := by
        rw [← Real.rpow_neg (le_of_lt hv) (-l)]
        simp [neg_neg]

-- (A2) power combine, general l:  v^(s+1−l) · v^(−2) · v^l = v^(s−1)
theorem reflection_power_general (v : ℝ) (s : ℝ) (l : ℝ) (hv : 0 < v) :
    v ^ (s + 1 - l) * v ^ (-2 : ℝ) * v ^ l = v ^ (s - 1) := by
  rw [← Real.rpow_add hv, ← Real.rpow_add hv]
  congr 1
  ring

-- (A3) THE KEY, general l: the M_l(l−s) integrand maps onto the M_l(s) integrand.
--      exponent check: s+1−l at l = 3 is s−2, exactly RH01L's certified exponent.
theorem reflection_key_general (v : ℝ) (s : ℝ) (l : ℝ) (hv : 0 < v) :
    v ^ (s + 1 - l) * v ^ (-2 : ℝ) * ((1 + 1 / v) ^ (-l) * (1 + v) ^ l) = v ^ (s - 1) := by
  rw [reflection_shape_general v l hv]
  exact reflection_power_general v s l hv

-- (A4) the l = 3 specialization: RECOVERS RH01L's certified `reflection_key` exactly.
theorem reflection_key_l3 (v : ℝ) (s : ℝ) (hv : 0 < v) :
    v ^ (s - 2) * v ^ (-2 : ℝ) * ((1 + 1 / v) ^ (-3 : ℝ) * (1 + v) ^ 3) = v ^ (s - 1) := by
  simpa [show s + 1 - 3 = s - 2 by ring] using reflection_key_general v s 3 hv

-- (A5) the delegation's LITERAL identity, certified in its true form:
--      v^(2s−l)·v^(−2)·(1+1/v)^(−l)·(1+v)^l  =  v^(2s−2),  NOT v^(s−1) in general.
theorem delegated_literal_identity (v : ℝ) (s : ℝ) (l : ℝ) (hv : 0 < v) :
    v ^ (2 * s - l) * v ^ (-2 : ℝ) * ((1 + 1 / v) ^ (-l) * (1 + v) ^ l) = v ^ (2 * s - 2) := by
  rw [reflection_shape_general v l hv]
  rw [← Real.rpow_add hv, ← Real.rpow_add hv]
  congr 1
  ring

-- ============================================================
-- SECTION B -- THE FULL MOMENT SEQUENCE: E[ln(1+u)] = 1/(l−1), certified
-- ============================================================

-- (B1) change-of-variables ALGEBRA: s = e^w − 1  ⇒  ln(1+s)·(1+s)^(−l)·(ds/dw) = w·e^(−(l−1)w)
--      i.e. the substitution u = ln(1+s) turns the moment integrand into w·e^(−(l−1)w).
theorem moment_subst_integrand (w : ℝ) (l : ℝ) :
    Real.log (1 + (Real.exp w - 1)) * (1 + (Real.exp w - 1)) ^ (-l) * Real.exp w
      = w * Real.exp (-((l - 1) * w)) := by
  have h1 : 1 + (Real.exp w - 1) = Real.exp w := by ring
  rw [h1]
  rw [Real.log_exp]
  have hm : (Real.exp w) ^ (-l) = Real.exp (w * (-l)) := by
    rw [← Real.exp_mul w (-l)]
  rw [hm]
  rw [mul_assoc]
  rw [← Real.exp_add (w * (-l)) w]
  congr 2; ring

-- (B2) the definite integral:  ∫₀^∞ w·e^(−c·w) dw = c^(−2)  (0 < c), via Mathlib's Gamma machinery
theorem moment_integral (c : ℝ) (hc : 0 < c) :
    ∫ x in Ioi (0 : ℝ), x * Real.exp (-(c * x)) = c ^ (-2 : ℝ) := by
  have h := integral_rpow_mul_exp_neg_mul_rpow (p := 1) (q := 1) (b := c)
    (by norm_num : (0 : ℝ) < 1) (by norm_num : (-1 : ℝ) < 1) hc
  calc
    ∫ x in Ioi (0 : ℝ), x * Real.exp (-(c * x))
        = ∫ x in Ioi (0 : ℝ), x ^ (1 : ℝ) * Real.exp (-c * x ^ (1 : ℝ)) := by
          apply setIntegral_congr_fun measurableSet_Ioi
          intro x hx
          simp [Real.rpow_one, neg_mul]
    _ = c ^ (-(1 + 1) / 1) * (1 / 1) * Real.Gamma ((1 + 1) / 1) := h
    _ = c ^ (-2 : ℝ) := by
          have harg : ((1 : ℝ) + 1) / 1 = (2 : ℝ) := by norm_num
          have hneg : (-(1 + 1 : ℝ)) / 1 = (-2 : ℝ) := by norm_num
          have hg : Real.Gamma (2 : ℝ) = 1 := by
            simp
          rw [harg, hneg, hg]
          norm_num

-- (B2') the delegated form with the ladder constant:  ∫₀^∞ w·e^(−(l−1)w) dw = (l−1)^(−2)
theorem moment_substitution_closed {l : ℝ} (hl : 1 < l) :
    ∫ x in Ioi (0 : ℝ), x * Real.exp (-((l - 1) * x)) = (l - 1) ^ (-2 : ℝ) :=
  moment_integral (l - 1) (sub_pos.mpr hl)

-- (B3) THE FULL SUBSTITUTION (measure-theoretic, image-based change of variables):
--      ∫₀^∞ ln(1+s)·(1+s)^(−l) ds  =  ∫₀^∞ w·e^(−(l−1)w) dw  =  (l−1)^(−2)
theorem ladder_log_moment_integral_subst {l : ℝ} (hl : 1 < l) :
    ∫ u in Ioi (0 : ℝ), Real.log (1 + u) * (1 + u) ^ (-l) = (l - 1) ^ (-2 : ℝ) := by
  -- f(w) = e^w − 1 maps Ioi 0 onto Ioi 0, f' = e^w, |f'| = e^w (positive)
  let f : ℝ → ℝ := fun w => Real.exp w - 1
  let f' : ℝ → ℝ := fun w => Real.exp w
  let g : ℝ → ℝ := fun u => Real.log (1 + u) * (1 + u) ^ (-l)
  have hderiv : ∀ x ∈ Ioi (0 : ℝ), HasDerivWithinAt f (f' x) (Ioi (0 : ℝ)) x := by
    intro x hx
    have hd : HasDerivAt f (Real.exp x) x := by
      dsimp [f]
      exact (Real.hasDerivAt_exp x).sub_const (1 : ℝ)
    exact hd.hasDerivWithinAt
  have hinj : InjOn f (Ioi (0 : ℝ)) := by
    intro x hx y hy h
    apply Real.exp_strictMono.injective
    -- f x = f y  ⇒  exp x = exp y
    dsimp [f] at h
    linarith
  have himg : f '' Ioi (0 : ℝ) = Ioi (0 : ℝ) := by
    ext u
    constructor
    · rintro ⟨x, hx, rfl⟩
      have hx1 : 1 < Real.exp x := by
        simpa [Real.exp_zero] using (Real.exp_lt_exp.mpr hx : Real.exp 0 < Real.exp x)
      exact sub_pos.mpr hx1
    · intro hu
      have hu' : 0 < u := mem_Ioi.mp hu
      refine ⟨Real.log (1 + u), ?_, ?_⟩
      · exact Real.log_pos (by linarith)
      · have hlog : Real.exp (Real.log (1 + u)) = 1 + u := Real.exp_log (by positivity)
        dsimp [f]
        linarith
  have hcongr : ∀ x ∈ Ioi (0 : ℝ),
      |f' x| • g (f x) = x * Real.exp (-((l - 1) * x)) := by
    intro x hx
    calc
      |f' x| • g (f x)
          = Real.log (1 + (Real.exp x - 1)) * (1 + (Real.exp x - 1)) ^ (-l) * Real.exp x := by
            dsimp [f, f', g]
            rw [abs_of_pos (Real.exp_pos x)]
            simp
            ring
      _ = x * Real.exp (-((l - 1) * x)) := by
            exact moment_subst_integrand x l
  have hsub := integral_image_eq_integral_abs_deriv_smul
    (s := Ioi (0 : ℝ)) (f := f) (f' := f') (g := g)
    measurableSet_Ioi hderiv hinj
  calc
    ∫ u in Ioi (0 : ℝ), Real.log (1 + u) * (1 + u) ^ (-l)
        = ∫ u in f '' Ioi (0 : ℝ), g u := by
          rw [himg]
    _ = ∫ x in Ioi (0 : ℝ), |f' x| • g (f x) := hsub
    _ = ∫ x in Ioi (0 : ℝ), x * Real.exp (-((l - 1) * x)) := by
          apply setIntegral_congr_fun measurableSet_Ioi hcongr
    _ = (l - 1) ^ (-2 : ℝ) := moment_substitution_closed hl

-- (B4) THE MOMENT SEQUENCE, closed form:  (l−1)·E[ln(1+u)]-integral  =  1/(l−1)
theorem ladder_log_moment {l : ℝ} (hl : 1 < l) :
    (l - 1) * ∫ u in Ioi (0 : ℝ), Real.log (1 + u) * (1 + u) ^ (-l) = (l - 1)⁻¹ := by
  rw [ladder_log_moment_integral_subst hl]
  have hp : 0 < l - 1 := sub_pos.mpr hl
  calc
    (l - 1) * (l - 1) ^ (-2 : ℝ)
        = (l - 1) * ((l - 1) ^ (2 : ℝ))⁻¹ := by rw [Real.rpow_neg hp.le (2 : ℝ)]
    _ = (l - 1) * ((l - 1) ^ 2)⁻¹ := by rw [Real.rpow_two]
    _ = (l - 1)⁻¹ := by
        have hnz : (l - 1) ≠ 0 := ne_of_gt hp
        field_simp [hnz]

-- (B5) the l = 3 rung of the sequence: E[ln(1+u)] = 1/2, the framework's registered constant
theorem ladder_log_moment_l3 :
    (2 : ℝ) * ∫ u in Ioi (0 : ℝ), Real.log (1 + u) * (1 + u) ^ (-3 : ℝ) = (1 : ℝ) / 2 := by
  have h := ladder_log_moment (l := 3) (by norm_num : (1 : ℝ) < 3)
  convert h using 1 <;> norm_num

-- ============================================================
-- SECTION C -- CONNECTIONS TO THE ZETA'S FUNCTIONAL EQUATION (certified facts)
-- ============================================================

-- (C1) Euler's reflection: the beta at the ladder edge l → 1 is the zeta's beta:
--      Γ(s)·Γ(1−s) = π/sin(πs)  (Mathlib-verified).
theorem euler_reflection_zeta_beta (s : ℝ) :
    Real.Gamma s * Real.Gamma (1 - s) = Real.pi / Real.sin (Real.pi * s) :=
  Real.Gamma_mul_Gamma_one_sub s

-- (C2) certified gap: reflection symmetry about axis 1/2 does NOT place zeros on the axis.
--      The polynomial (s−2)(s+1) is invariant under s ↦ 1−s (axis 1/2) ...
theorem reflection_symmetry_alone_insufficient (s : ℝ) :
    ((1 - s) - 2) * ((1 - s) + 1) = (s - 2) * (s + 1) := by
  ring

--      ... yet its zeros sit at 2 and −1, both OFF the axis.
theorem reflection_symmetry_zero_pair_off_axis :
    ((2 : ℝ) - 2) * (2 + 1) = 0 ∧
    ((-1 : ℝ) - 2) * (-1 + 1) = 0 ∧
    (2 : ℝ) ≠ 1 / 2 ∧
    (-1 : ℝ) ≠ 1 / 2 := by
  norm_num

end