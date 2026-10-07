import Mathlib
open Real Filter Topology intervalIntegral MeasureTheory

/-- LR10B -- Lean certificate of the LR10X-corrected rational closed forms (Z18 door).
   LR10X (deepseek_push/LR10X_results.json, exit 0) adjudicated EXACTLY:
     E2(q) = 37/60 + (701/1050) q + (3491/18375) q^2   (channel a/b/c sums)
   hence the thin-window law c1(q) = E2(q) - S(q) = 17/60 + (117/350) q + (627/6125) q^2
   with S(q) = 1/3 + q/3 + 46 q^2/525 (LR9-certified).
   Certified HERE unconditionally, with no unfinished tactic proofs: 10 single-log
   core integrals int_0^1 u^p log(1+-u) du (odd p in {1,3,5,7,9}), 4 polynomial
   cores, the 30 per-term integral certificates, the three channel assemblies, and
   the c1 coefficient law -- via the normalized antiderivative
     F = P + ((u^(p+1)-1)/(p+1)) log(1+-u),  P' = -s/(p+1) Q,  Q = (u^(p+1)-1)/(1+-u),
   and mathlib's integral_eq_sub_of_hasDerivAt_of_tendsto (the technique of
   mathlib's own integral_log lemmas). The geometric reduction chain upstream of
   these integrals remains numerically audited (E2F1 G1/G2b, LR10X G-T1) and is
   NOT probability-space-certified -- K01 consistency-family labeling carries over.
   Gates: G-L0/G-L2 in LR10B_gen.py (loaded-not-transcribed from LR10X data),
   G-L1 = this file compiles rc 0 with zero unfinished proofs and channel-law axiom
   footprints inside {propext, Classical.choice, Quot.sound}. -/

theorem logm_int : IntervalIntegrable (fun x : ℝ => Real.log (1 - x)) volume 0 1 := by
  simpa using (intervalIntegrable_log' (a := (0: ℝ)) (b := (1: ℝ))).comp_sub_left 1 |>.symm

theorem logp_int : IntervalIntegrable (fun x : ℝ => Real.log (x + 1)) volume 0 1 := by
  have h := (intervalIntegrable_log' (a := (1: ℝ)) (b := (2: ℝ))).comp_sub_right (-1)
  simp only [sub_neg_eq_add] at h
  norm_num at h
  exact h

theorem logp_contAt0 : ContinuousAt (fun u : ℝ => Real.log (1 + u)) 0 := by
  have h1 : ContinuousAt (fun u : ℝ => 1 + u) 0 := by fun_prop
  exact ContinuousAt.comp_of_eq (Real.continuousAt_log (by norm_num : (1: ℝ) ≠ 0)) h1 (by norm_num)

theorem logp_contAt1 : ContinuousAt (fun u : ℝ => Real.log (1 + u)) 1 := by
  have h1 : ContinuousAt (fun u : ℝ => 1 + u) 1 := by fun_prop
  exact ContinuousAt.comp_of_eq (Real.continuousAt_log (by norm_num : (2: ℝ) ≠ 0)) h1 (by norm_num)

theorem mono_cont (c : ℝ) (k : ℕ) : Continuous fun w : ℝ => c * w ^ k :=
  Continuous.mul continuous_const (by fun_prop : Continuous fun w : ℝ => w ^ k)

theorem mono_contAt (c : ℝ) (k : ℕ) (x : ℝ) : ContinuousAt (fun w : ℝ => c * w ^ k) x :=
  (mono_cont c k).continuousAt

theorem tendsto_t_log_t : Tendsto (fun t : ℝ => t * Real.log t) (nhdsWithin 0 (Set.Ioi 0)) (nhds 0) := by
  simpa [mul_comm] using tendsto_log_mul_rpow_nhdsGT_zero one_pos

theorem tendsto_alm {G : ℝ → ℝ} (hG : ContinuousAt G 1) :
    Tendsto (fun u : ℝ => ((1 - u) * Real.log (1 - u)) * G u) (nhdsWithin 1 (Set.Iio 1)) (nhds 0) := by
  have hsub : Tendsto (fun u : ℝ => 1 - u) (nhdsWithin 1 (Set.Iio 1)) (nhdsWithin 0 (Set.Ioi 0)) := by
    have h1 : ContinuousWithinAt (fun u : ℝ => 1 - u) (Set.Iio 1) 1 := by fun_prop
    have h2 : Tendsto (fun u : ℝ => 1 - u) (nhdsWithin 1 (Set.Iio 1)) (nhdsWithin ((1: ℝ) - 1) (Set.Ioi 0)) :=
      h1.tendsto_nhdsWithin (t := Set.Ioi 0) (fun z hz => by
        simp only [Set.mem_Iio, Set.mem_Ioi] at hz ⊢
        linarith)
    rwa [show ((1: ℝ) - 1) = 0 by norm_num] at h2
  have h2 : Tendsto (fun u : ℝ => (1 - u) * Real.log (1 - u)) (nhdsWithin 1 (Set.Iio 1)) (nhds 0) :=
    tendsto_t_log_t.comp hsub
  simpa using h2.mul (hG.tendsto.mono_left nhdsWithin_le_nhds)

theorem poly_core_2 : ∫ u in (0: ℝ)..1, u ^ 2 = ((1: ℝ) / 3) := by
  have hderiv : ∀ x ∈ Set.Ioo (0: ℝ) 1, HasDerivAt (fun w : ℝ => w ^ 3 / 3) (x ^ 2) x := by
    intro x _
    refine ((hasDerivAt_pow 3 x).div_const 3) |>.congr_deriv ?_
    ring
  have hint : IntervalIntegrable (fun x : ℝ => x ^ 2) volume 0 1 := Continuous.intervalIntegrable (by fun_prop) 0 1
  have ha : Tendsto (fun w : ℝ => w ^ 3 / 3) (nhdsWithin (0: ℝ) (Set.Ioi 0)) (nhds (((0: ℝ) ^ 3) / 3)) :=
    ((by fun_prop : ContinuousAt (fun w : ℝ => w ^ 3 / 3) 0) |>.tendsto |>.mono_left nhdsWithin_le_nhds)
  have hb : Tendsto (fun w : ℝ => w ^ 3 / 3) (nhdsWithin (1: ℝ) (Set.Iio 1)) (nhds (((1: ℝ) ^ 3) / 3)) :=
    ((by fun_prop : ContinuousAt (fun w : ℝ => w ^ 3 / 3) 1) |>.tendsto |>.mono_left nhdsWithin_le_nhds)
  have h := intervalIntegral.integral_eq_sub_of_hasDerivAt_of_tendsto (a := (0: ℝ)) (b := (1: ℝ)) (by norm_num : (0: ℝ) < (1: ℝ)) (f' := fun x : ℝ => x ^ 2) hderiv hint ha hb
  exact h.trans (by norm_num)

theorem poly_core_4 : ∫ u in (0: ℝ)..1, u ^ 4 = ((1: ℝ) / 5) := by
  have hderiv : ∀ x ∈ Set.Ioo (0: ℝ) 1, HasDerivAt (fun w : ℝ => w ^ 5 / 5) (x ^ 4) x := by
    intro x _
    refine ((hasDerivAt_pow 5 x).div_const 5) |>.congr_deriv ?_
    ring
  have hint : IntervalIntegrable (fun x : ℝ => x ^ 4) volume 0 1 := Continuous.intervalIntegrable (by fun_prop) 0 1
  have ha : Tendsto (fun w : ℝ => w ^ 5 / 5) (nhdsWithin (0: ℝ) (Set.Ioi 0)) (nhds (((0: ℝ) ^ 5) / 5)) :=
    ((by fun_prop : ContinuousAt (fun w : ℝ => w ^ 5 / 5) 0) |>.tendsto |>.mono_left nhdsWithin_le_nhds)
  have hb : Tendsto (fun w : ℝ => w ^ 5 / 5) (nhdsWithin (1: ℝ) (Set.Iio 1)) (nhds (((1: ℝ) ^ 5) / 5)) :=
    ((by fun_prop : ContinuousAt (fun w : ℝ => w ^ 5 / 5) 1) |>.tendsto |>.mono_left nhdsWithin_le_nhds)
  have h := intervalIntegral.integral_eq_sub_of_hasDerivAt_of_tendsto (a := (0: ℝ)) (b := (1: ℝ)) (by norm_num : (0: ℝ) < (1: ℝ)) (f' := fun x : ℝ => x ^ 4) hderiv hint ha hb
  exact h.trans (by norm_num)

theorem poly_core_6 : ∫ u in (0: ℝ)..1, u ^ 6 = ((1: ℝ) / 7) := by
  have hderiv : ∀ x ∈ Set.Ioo (0: ℝ) 1, HasDerivAt (fun w : ℝ => w ^ 7 / 7) (x ^ 6) x := by
    intro x _
    refine ((hasDerivAt_pow 7 x).div_const 7) |>.congr_deriv ?_
    ring
  have hint : IntervalIntegrable (fun x : ℝ => x ^ 6) volume 0 1 := Continuous.intervalIntegrable (by fun_prop) 0 1
  have ha : Tendsto (fun w : ℝ => w ^ 7 / 7) (nhdsWithin (0: ℝ) (Set.Ioi 0)) (nhds (((0: ℝ) ^ 7) / 7)) :=
    ((by fun_prop : ContinuousAt (fun w : ℝ => w ^ 7 / 7) 0) |>.tendsto |>.mono_left nhdsWithin_le_nhds)
  have hb : Tendsto (fun w : ℝ => w ^ 7 / 7) (nhdsWithin (1: ℝ) (Set.Iio 1)) (nhds (((1: ℝ) ^ 7) / 7)) :=
    ((by fun_prop : ContinuousAt (fun w : ℝ => w ^ 7 / 7) 1) |>.tendsto |>.mono_left nhdsWithin_le_nhds)
  have h := intervalIntegral.integral_eq_sub_of_hasDerivAt_of_tendsto (a := (0: ℝ)) (b := (1: ℝ)) (by norm_num : (0: ℝ) < (1: ℝ)) (f' := fun x : ℝ => x ^ 6) hderiv hint ha hb
  exact h.trans (by norm_num)

theorem poly_core_8 : ∫ u in (0: ℝ)..1, u ^ 8 = ((1: ℝ) / 9) := by
  have hderiv : ∀ x ∈ Set.Ioo (0: ℝ) 1, HasDerivAt (fun w : ℝ => w ^ 9 / 9) (x ^ 8) x := by
    intro x _
    refine ((hasDerivAt_pow 9 x).div_const 9) |>.congr_deriv ?_
    ring
  have hint : IntervalIntegrable (fun x : ℝ => x ^ 8) volume 0 1 := Continuous.intervalIntegrable (by fun_prop) 0 1
  have ha : Tendsto (fun w : ℝ => w ^ 9 / 9) (nhdsWithin (0: ℝ) (Set.Ioi 0)) (nhds (((0: ℝ) ^ 9) / 9)) :=
    ((by fun_prop : ContinuousAt (fun w : ℝ => w ^ 9 / 9) 0) |>.tendsto |>.mono_left nhdsWithin_le_nhds)
  have hb : Tendsto (fun w : ℝ => w ^ 9 / 9) (nhdsWithin (1: ℝ) (Set.Iio 1)) (nhds (((1: ℝ) ^ 9) / 9)) :=
    ((by fun_prop : ContinuousAt (fun w : ℝ => w ^ 9 / 9) 1) |>.tendsto |>.mono_left nhdsWithin_le_nhds)
  have h := intervalIntegral.integral_eq_sub_of_hasDerivAt_of_tendsto (a := (0: ℝ)) (b := (1: ℝ)) (by norm_num : (0: ℝ) < (1: ℝ)) (f' := fun x : ℝ => x ^ 8) hderiv hint ha hb
  exact h.trans (by norm_num)

theorem core_lm_1 : ∫ u in (0: ℝ)..1, u ^ 1 * Real.log (1 - u) = (-((3: ℝ) / 4)) := by
  have hint : IntervalIntegrable (fun x : ℝ => x ^ 1 * Real.log (1 - x)) volume 0 1 := by
    refine IntervalIntegrable.congr (show Set.EqOn (fun x : ℝ => Real.log (1 - x) * x ^ 1) (fun x : ℝ => x ^ 1 * Real.log (1 - x)) (Set.uIoc (0: ℝ) 1) from fun x _ => by ring)
      (logm_int.mul_continuousOn (Continuous.continuousOn (by fun_prop : Continuous fun x : ℝ => x ^ 1)))
  have hderiv : ∀ x ∈ Set.Ioo (0: ℝ) 1, HasDerivAt
      (fun w : ℝ => (-((1: ℝ) / 4)) * w ^ 2 + (-((1: ℝ) / 2)) * w ^ 1 + ((w ^ 2 - 1) / 2) * Real.log (1 - w))
      (x ^ 1 * Real.log (1 - x)) x := by
    intro x hx
    have hx1 : (1: ℝ) - x ≠ 0 := by have := hx.2; linarith
    have hid : HasDerivAt (fun y : ℝ => y) 1 x := hasDerivAt_id' x
    have hinner : HasDerivAt (fun y : ℝ => 1 - y) ((0: ℝ) - 1) x := (hasDerivAt_const x 1).sub hid
    have hlog : HasDerivAt (fun w : ℝ => Real.log (1 - w)) ((-1: ℝ) / (1 - x)) x := by
      refine HasDerivAt.comp_of_eq x (hasDerivAt_log hx1) hinner rfl |>.congr_deriv ?_
      ring
    have hA : HasDerivAt (fun w : ℝ => (w ^ 2 - 1) / 2) (x ^ 1) x := by
      refine ((hasDerivAt_pow 2 x).sub (hasDerivAt_const x 1)).div_const 2 |>.congr_deriv ?_
      ring
    have hQ : (x: ℝ) ^ 2 - 1 = ((1 - x)) * ((-((1: ℝ) / 1)) * x ^ 1 + (-((1: ℝ) / 1))) := by ring
    have hP : HasDerivAt (fun w : ℝ => (-((1: ℝ) / 4)) * w ^ 2 + (-((1: ℝ) / 2)) * w ^ 1) (((1: ℝ) / 2) * ((-((1: ℝ) / 1)) * x ^ 1 + (-((1: ℝ) / 1)))) x := by
      refine (((hasDerivAt_pow 2 x).const_mul (-((1: ℝ) / 4))).add ((hasDerivAt_pow 1 x).const_mul (-((1: ℝ) / 2)))) |>.congr_deriv ?_
      ring
    refine (hP.add (hA.mul hlog)).congr_deriv ?_
    field_simp [hQ]; ring
  have hPc0 : ContinuousAt (fun w : ℝ => (-((1: ℝ) / 4)) * w ^ 2 + (-((1: ℝ) / 2)) * w ^ 1) 0 := ((mono_contAt (-((1: ℝ) / 4)) 2 0).add (mono_contAt (-((1: ℝ) / 2)) 1 0))
  have hPc1 : ContinuousAt (fun w : ℝ => (-((1: ℝ) / 4)) * w ^ 2 + (-((1: ℝ) / 2)) * w ^ 1) 1 := ((mono_contAt (-((1: ℝ) / 4)) 2 1).add (mono_contAt (-((1: ℝ) / 2)) 1 1))
  have hAc0 : ContinuousAt (fun w : ℝ => ((1: ℝ) / 2) * w ^ 2 + (-((1: ℝ) / 2)) * w ^ 0) 0 := (mono_contAt ((1: ℝ) / 2) 2 0).add (mono_contAt (-((1: ℝ) / 2)) 0 0)
  have hAc1 : ContinuousAt (fun w : ℝ => ((1: ℝ) / 2) * w ^ 2 + (-((1: ℝ) / 2)) * w ^ 0) 1 := (mono_contAt ((1: ℝ) / 2) 2 1).add (mono_contAt (-((1: ℝ) / 2)) 0 1)
  have heq : (fun w : ℝ => (-((1: ℝ) / 4)) * w ^ 2 + (-((1: ℝ) / 2)) * w ^ 1 + ((w ^ 2 - 1) / 2) * Real.log (1 - w)) = (fun w : ℝ => (-((1: ℝ) / 4)) * w ^ 2 + (-((1: ℝ) / 2)) * w ^ 1 + (((1: ℝ) / 2) * w ^ 2 + (-((1: ℝ) / 2)) * w ^ 0) * Real.log (1 - w)) := by
    funext w
    have hdiv : (w ^ 2 - 1) / 2 = ((1: ℝ) / 2) * w ^ 2 + (-((1: ℝ) / 2)) * w ^ 0 := by ring
    rw [hdiv]
  have hc0 : ContinuousAt (fun w : ℝ => Real.log (1 - w)) 0 := by
    have h1 : ContinuousAt (fun w : ℝ => 1 - w) 0 := by fun_prop
    exact ContinuousAt.comp_of_eq (Real.continuousAt_log (by norm_num : (1: ℝ) ≠ 0)) h1 (by norm_num)
  have hv0 : ((-((1: ℝ) / 4)) * 0 ^ 2 + (-((1: ℝ) / 2)) * 0 ^ 1 + (((1: ℝ) / 2) * 0 ^ 2 + (-((1: ℝ) / 2)) * 0 ^ 0) * Real.log (1 - 0)) = (0: ℝ) := by norm_num [Real.log_one]
  have ha : Tendsto (fun w : ℝ => (-((1: ℝ) / 4)) * w ^ 2 + (-((1: ℝ) / 2)) * w ^ 1 + ((w ^ 2 - 1) / 2) * Real.log (1 - w)) (nhdsWithin (0: ℝ) (Set.Ioi 0)) (nhds (0: ℝ)) := by
    rw [heq]
    have hten : Tendsto (fun w : ℝ => (-((1: ℝ) / 4)) * w ^ 2 + (-((1: ℝ) / 2)) * w ^ 1 + (((1: ℝ) / 2) * w ^ 2 + (-((1: ℝ) / 2)) * w ^ 0) * Real.log (1 - w)) (nhdsWithin (0: ℝ) (Set.Ioi 0)) (nhds ((-((1: ℝ) / 4)) * 0 ^ 2 + (-((1: ℝ) / 2)) * 0 ^ 1 + (((1: ℝ) / 2) * 0 ^ 2 + (-((1: ℝ) / 2)) * 0 ^ 0) * Real.log (1 - 0))) :=
      (hPc0.add (hAc0.mul hc0)).tendsto.mono_left nhdsWithin_le_nhds
    rwa [hv0] at hten
  have hAeq : ∀ z : ℝ, (((1: ℝ) / 2) * z ^ 2 + (-((1: ℝ) / 2)) * z ^ 0) * Real.log (1 - z)
      = ((1 - z) * Real.log (1 - z)) * ((-((1: ℝ) / 2)) * ((1: ℝ) + z)) := by intro z; ring
  have tA2 : Tendsto (fun u : ℝ => (((1: ℝ) / 2) * u ^ 2 + (-((1: ℝ) / 2)) * u ^ 0) * Real.log (1 - u)) (nhdsWithin (1: ℝ) (Set.Iio 1)) (nhds (0: ℝ)) := by
    have key : Tendsto (fun u : ℝ => ((1 - u) * Real.log (1 - u)) * ((-((1: ℝ) / 2)) * ((1: ℝ) + u))) (nhdsWithin (1: ℝ) (Set.Iio 1)) (nhds (0: ℝ)) :=
      tendsto_alm (by fun_prop : ContinuousAt (fun u : ℝ => (-((1: ℝ) / 2)) * ((1: ℝ) + u)) 1)
    have heq2 : (fun u : ℝ => (((1: ℝ) / 2) * u ^ 2 + (-((1: ℝ) / 2)) * u ^ 0) * Real.log (1 - u))
        = (fun u : ℝ => ((1 - u) * Real.log (1 - u)) * ((-((1: ℝ) / 2)) * ((1: ℝ) + u))) := by
      funext u; rw [hAeq u]
    rw [heq2]; exact key
  have hv1 : ((-((1: ℝ) / 4)) * 1 ^ 2 + (-((1: ℝ) / 2)) * 1 ^ 1 + (0: ℝ)) = (-((3: ℝ) / 4)) := by norm_num
  have hb : Tendsto (fun w : ℝ => (-((1: ℝ) / 4)) * w ^ 2 + (-((1: ℝ) / 2)) * w ^ 1 + ((w ^ 2 - 1) / 2) * Real.log (1 - w)) (nhdsWithin (1: ℝ) (Set.Iio 1)) (nhds (-((3: ℝ) / 4))) := by
    rw [heq]
    have hten : Tendsto (fun w : ℝ => (-((1: ℝ) / 4)) * w ^ 2 + (-((1: ℝ) / 2)) * w ^ 1 + (((1: ℝ) / 2) * w ^ 2 + (-((1: ℝ) / 2)) * w ^ 0) * Real.log (1 - w)) (nhdsWithin (1: ℝ) (Set.Iio 1)) (nhds ((-((1: ℝ) / 4)) * 1 ^ 2 + (-((1: ℝ) / 2)) * 1 ^ 1 + (0: ℝ))) :=
      (hPc1.tendsto.mono_left nhdsWithin_le_nhds).add tA2
    rwa [hv1] at hten
  have h := intervalIntegral.integral_eq_sub_of_hasDerivAt_of_tendsto (a := (0: ℝ)) (b := (1: ℝ))
    (by norm_num : (0: ℝ) < (1: ℝ)) hderiv hint ha hb
  exact h.trans (by norm_num)

theorem core_lm_3 : ∫ u in (0: ℝ)..1, u ^ 3 * Real.log (1 - u) = (-((25: ℝ) / 48)) := by
  have hint : IntervalIntegrable (fun x : ℝ => x ^ 3 * Real.log (1 - x)) volume 0 1 := by
    refine IntervalIntegrable.congr (show Set.EqOn (fun x : ℝ => Real.log (1 - x) * x ^ 3) (fun x : ℝ => x ^ 3 * Real.log (1 - x)) (Set.uIoc (0: ℝ) 1) from fun x _ => by ring)
      (logm_int.mul_continuousOn (Continuous.continuousOn (by fun_prop : Continuous fun x : ℝ => x ^ 3)))
  have hderiv : ∀ x ∈ Set.Ioo (0: ℝ) 1, HasDerivAt
      (fun w : ℝ => (-((1: ℝ) / 16)) * w ^ 4 + (-((1: ℝ) / 12)) * w ^ 3 + (-((1: ℝ) / 8)) * w ^ 2 + (-((1: ℝ) / 4)) * w ^ 1 + ((w ^ 4 - 1) / 4) * Real.log (1 - w))
      (x ^ 3 * Real.log (1 - x)) x := by
    intro x hx
    have hx1 : (1: ℝ) - x ≠ 0 := by have := hx.2; linarith
    have hid : HasDerivAt (fun y : ℝ => y) 1 x := hasDerivAt_id' x
    have hinner : HasDerivAt (fun y : ℝ => 1 - y) ((0: ℝ) - 1) x := (hasDerivAt_const x 1).sub hid
    have hlog : HasDerivAt (fun w : ℝ => Real.log (1 - w)) ((-1: ℝ) / (1 - x)) x := by
      refine HasDerivAt.comp_of_eq x (hasDerivAt_log hx1) hinner rfl |>.congr_deriv ?_
      ring
    have hA : HasDerivAt (fun w : ℝ => (w ^ 4 - 1) / 4) (x ^ 3) x := by
      refine ((hasDerivAt_pow 4 x).sub (hasDerivAt_const x 1)).div_const 4 |>.congr_deriv ?_
      ring
    have hQ : (x: ℝ) ^ 4 - 1 = ((1 - x)) * ((-((1: ℝ) / 1)) * x ^ 3 + (-((1: ℝ) / 1)) * x ^ 2 + (-((1: ℝ) / 1)) * x ^ 1 + (-((1: ℝ) / 1))) := by ring
    have hP : HasDerivAt (fun w : ℝ => (-((1: ℝ) / 16)) * w ^ 4 + (-((1: ℝ) / 12)) * w ^ 3 + (-((1: ℝ) / 8)) * w ^ 2 + (-((1: ℝ) / 4)) * w ^ 1) (((1: ℝ) / 4) * ((-((1: ℝ) / 1)) * x ^ 3 + (-((1: ℝ) / 1)) * x ^ 2 + (-((1: ℝ) / 1)) * x ^ 1 + (-((1: ℝ) / 1)))) x := by
      refine (((((hasDerivAt_pow 4 x).const_mul (-((1: ℝ) / 16))).add ((hasDerivAt_pow 3 x).const_mul (-((1: ℝ) / 12)))).add ((hasDerivAt_pow 2 x).const_mul (-((1: ℝ) / 8)))).add ((hasDerivAt_pow 1 x).const_mul (-((1: ℝ) / 4)))) |>.congr_deriv ?_
      ring
    refine (hP.add (hA.mul hlog)).congr_deriv ?_
    field_simp [hQ]; ring
  have hPc0 : ContinuousAt (fun w : ℝ => (-((1: ℝ) / 16)) * w ^ 4 + (-((1: ℝ) / 12)) * w ^ 3 + (-((1: ℝ) / 8)) * w ^ 2 + (-((1: ℝ) / 4)) * w ^ 1) 0 := ((((mono_contAt (-((1: ℝ) / 16)) 4 0).add (mono_contAt (-((1: ℝ) / 12)) 3 0)).add (mono_contAt (-((1: ℝ) / 8)) 2 0)).add (mono_contAt (-((1: ℝ) / 4)) 1 0))
  have hPc1 : ContinuousAt (fun w : ℝ => (-((1: ℝ) / 16)) * w ^ 4 + (-((1: ℝ) / 12)) * w ^ 3 + (-((1: ℝ) / 8)) * w ^ 2 + (-((1: ℝ) / 4)) * w ^ 1) 1 := ((((mono_contAt (-((1: ℝ) / 16)) 4 1).add (mono_contAt (-((1: ℝ) / 12)) 3 1)).add (mono_contAt (-((1: ℝ) / 8)) 2 1)).add (mono_contAt (-((1: ℝ) / 4)) 1 1))
  have hAc0 : ContinuousAt (fun w : ℝ => ((1: ℝ) / 4) * w ^ 4 + (-((1: ℝ) / 4)) * w ^ 0) 0 := (mono_contAt ((1: ℝ) / 4) 4 0).add (mono_contAt (-((1: ℝ) / 4)) 0 0)
  have hAc1 : ContinuousAt (fun w : ℝ => ((1: ℝ) / 4) * w ^ 4 + (-((1: ℝ) / 4)) * w ^ 0) 1 := (mono_contAt ((1: ℝ) / 4) 4 1).add (mono_contAt (-((1: ℝ) / 4)) 0 1)
  have heq : (fun w : ℝ => (-((1: ℝ) / 16)) * w ^ 4 + (-((1: ℝ) / 12)) * w ^ 3 + (-((1: ℝ) / 8)) * w ^ 2 + (-((1: ℝ) / 4)) * w ^ 1 + ((w ^ 4 - 1) / 4) * Real.log (1 - w)) = (fun w : ℝ => (-((1: ℝ) / 16)) * w ^ 4 + (-((1: ℝ) / 12)) * w ^ 3 + (-((1: ℝ) / 8)) * w ^ 2 + (-((1: ℝ) / 4)) * w ^ 1 + (((1: ℝ) / 4) * w ^ 4 + (-((1: ℝ) / 4)) * w ^ 0) * Real.log (1 - w)) := by
    funext w
    have hdiv : (w ^ 4 - 1) / 4 = ((1: ℝ) / 4) * w ^ 4 + (-((1: ℝ) / 4)) * w ^ 0 := by ring
    rw [hdiv]
  have hc0 : ContinuousAt (fun w : ℝ => Real.log (1 - w)) 0 := by
    have h1 : ContinuousAt (fun w : ℝ => 1 - w) 0 := by fun_prop
    exact ContinuousAt.comp_of_eq (Real.continuousAt_log (by norm_num : (1: ℝ) ≠ 0)) h1 (by norm_num)
  have hv0 : ((-((1: ℝ) / 16)) * 0 ^ 4 + (-((1: ℝ) / 12)) * 0 ^ 3 + (-((1: ℝ) / 8)) * 0 ^ 2 + (-((1: ℝ) / 4)) * 0 ^ 1 + (((1: ℝ) / 4) * 0 ^ 4 + (-((1: ℝ) / 4)) * 0 ^ 0) * Real.log (1 - 0)) = (0: ℝ) := by norm_num [Real.log_one]
  have ha : Tendsto (fun w : ℝ => (-((1: ℝ) / 16)) * w ^ 4 + (-((1: ℝ) / 12)) * w ^ 3 + (-((1: ℝ) / 8)) * w ^ 2 + (-((1: ℝ) / 4)) * w ^ 1 + ((w ^ 4 - 1) / 4) * Real.log (1 - w)) (nhdsWithin (0: ℝ) (Set.Ioi 0)) (nhds (0: ℝ)) := by
    rw [heq]
    have hten : Tendsto (fun w : ℝ => (-((1: ℝ) / 16)) * w ^ 4 + (-((1: ℝ) / 12)) * w ^ 3 + (-((1: ℝ) / 8)) * w ^ 2 + (-((1: ℝ) / 4)) * w ^ 1 + (((1: ℝ) / 4) * w ^ 4 + (-((1: ℝ) / 4)) * w ^ 0) * Real.log (1 - w)) (nhdsWithin (0: ℝ) (Set.Ioi 0)) (nhds ((-((1: ℝ) / 16)) * 0 ^ 4 + (-((1: ℝ) / 12)) * 0 ^ 3 + (-((1: ℝ) / 8)) * 0 ^ 2 + (-((1: ℝ) / 4)) * 0 ^ 1 + (((1: ℝ) / 4) * 0 ^ 4 + (-((1: ℝ) / 4)) * 0 ^ 0) * Real.log (1 - 0))) :=
      (hPc0.add (hAc0.mul hc0)).tendsto.mono_left nhdsWithin_le_nhds
    rwa [hv0] at hten
  have hAeq : ∀ z : ℝ, (((1: ℝ) / 4) * z ^ 4 + (-((1: ℝ) / 4)) * z ^ 0) * Real.log (1 - z)
      = ((1 - z) * Real.log (1 - z)) * ((-((1: ℝ) / 4)) * ((1: ℝ) + z + z ^ 2 + z ^ 3)) := by intro z; ring
  have tA2 : Tendsto (fun u : ℝ => (((1: ℝ) / 4) * u ^ 4 + (-((1: ℝ) / 4)) * u ^ 0) * Real.log (1 - u)) (nhdsWithin (1: ℝ) (Set.Iio 1)) (nhds (0: ℝ)) := by
    have key : Tendsto (fun u : ℝ => ((1 - u) * Real.log (1 - u)) * ((-((1: ℝ) / 4)) * ((1: ℝ) + u + u ^ 2 + u ^ 3))) (nhdsWithin (1: ℝ) (Set.Iio 1)) (nhds (0: ℝ)) :=
      tendsto_alm (by fun_prop : ContinuousAt (fun u : ℝ => (-((1: ℝ) / 4)) * ((1: ℝ) + u + u ^ 2 + u ^ 3)) 1)
    have heq2 : (fun u : ℝ => (((1: ℝ) / 4) * u ^ 4 + (-((1: ℝ) / 4)) * u ^ 0) * Real.log (1 - u))
        = (fun u : ℝ => ((1 - u) * Real.log (1 - u)) * ((-((1: ℝ) / 4)) * ((1: ℝ) + u + u ^ 2 + u ^ 3))) := by
      funext u; rw [hAeq u]
    rw [heq2]; exact key
  have hv1 : ((-((1: ℝ) / 16)) * 1 ^ 4 + (-((1: ℝ) / 12)) * 1 ^ 3 + (-((1: ℝ) / 8)) * 1 ^ 2 + (-((1: ℝ) / 4)) * 1 ^ 1 + (0: ℝ)) = (-((25: ℝ) / 48)) := by norm_num
  have hb : Tendsto (fun w : ℝ => (-((1: ℝ) / 16)) * w ^ 4 + (-((1: ℝ) / 12)) * w ^ 3 + (-((1: ℝ) / 8)) * w ^ 2 + (-((1: ℝ) / 4)) * w ^ 1 + ((w ^ 4 - 1) / 4) * Real.log (1 - w)) (nhdsWithin (1: ℝ) (Set.Iio 1)) (nhds (-((25: ℝ) / 48))) := by
    rw [heq]
    have hten : Tendsto (fun w : ℝ => (-((1: ℝ) / 16)) * w ^ 4 + (-((1: ℝ) / 12)) * w ^ 3 + (-((1: ℝ) / 8)) * w ^ 2 + (-((1: ℝ) / 4)) * w ^ 1 + (((1: ℝ) / 4) * w ^ 4 + (-((1: ℝ) / 4)) * w ^ 0) * Real.log (1 - w)) (nhdsWithin (1: ℝ) (Set.Iio 1)) (nhds ((-((1: ℝ) / 16)) * 1 ^ 4 + (-((1: ℝ) / 12)) * 1 ^ 3 + (-((1: ℝ) / 8)) * 1 ^ 2 + (-((1: ℝ) / 4)) * 1 ^ 1 + (0: ℝ))) :=
      (hPc1.tendsto.mono_left nhdsWithin_le_nhds).add tA2
    rwa [hv1] at hten
  have h := intervalIntegral.integral_eq_sub_of_hasDerivAt_of_tendsto (a := (0: ℝ)) (b := (1: ℝ))
    (by norm_num : (0: ℝ) < (1: ℝ)) hderiv hint ha hb
  exact h.trans (by norm_num)

theorem core_lm_5 : ∫ u in (0: ℝ)..1, u ^ 5 * Real.log (1 - u) = (-((49: ℝ) / 120)) := by
  have hint : IntervalIntegrable (fun x : ℝ => x ^ 5 * Real.log (1 - x)) volume 0 1 := by
    refine IntervalIntegrable.congr (show Set.EqOn (fun x : ℝ => Real.log (1 - x) * x ^ 5) (fun x : ℝ => x ^ 5 * Real.log (1 - x)) (Set.uIoc (0: ℝ) 1) from fun x _ => by ring)
      (logm_int.mul_continuousOn (Continuous.continuousOn (by fun_prop : Continuous fun x : ℝ => x ^ 5)))
  have hderiv : ∀ x ∈ Set.Ioo (0: ℝ) 1, HasDerivAt
      (fun w : ℝ => (-((1: ℝ) / 36)) * w ^ 6 + (-((1: ℝ) / 30)) * w ^ 5 + (-((1: ℝ) / 24)) * w ^ 4 + (-((1: ℝ) / 18)) * w ^ 3 + (-((1: ℝ) / 12)) * w ^ 2 + (-((1: ℝ) / 6)) * w ^ 1 + ((w ^ 6 - 1) / 6) * Real.log (1 - w))
      (x ^ 5 * Real.log (1 - x)) x := by
    intro x hx
    have hx1 : (1: ℝ) - x ≠ 0 := by have := hx.2; linarith
    have hid : HasDerivAt (fun y : ℝ => y) 1 x := hasDerivAt_id' x
    have hinner : HasDerivAt (fun y : ℝ => 1 - y) ((0: ℝ) - 1) x := (hasDerivAt_const x 1).sub hid
    have hlog : HasDerivAt (fun w : ℝ => Real.log (1 - w)) ((-1: ℝ) / (1 - x)) x := by
      refine HasDerivAt.comp_of_eq x (hasDerivAt_log hx1) hinner rfl |>.congr_deriv ?_
      ring
    have hA : HasDerivAt (fun w : ℝ => (w ^ 6 - 1) / 6) (x ^ 5) x := by
      refine ((hasDerivAt_pow 6 x).sub (hasDerivAt_const x 1)).div_const 6 |>.congr_deriv ?_
      ring
    have hQ : (x: ℝ) ^ 6 - 1 = ((1 - x)) * ((-((1: ℝ) / 1)) * x ^ 5 + (-((1: ℝ) / 1)) * x ^ 4 + (-((1: ℝ) / 1)) * x ^ 3 + (-((1: ℝ) / 1)) * x ^ 2 + (-((1: ℝ) / 1)) * x ^ 1 + (-((1: ℝ) / 1))) := by ring
    have hP : HasDerivAt (fun w : ℝ => (-((1: ℝ) / 36)) * w ^ 6 + (-((1: ℝ) / 30)) * w ^ 5 + (-((1: ℝ) / 24)) * w ^ 4 + (-((1: ℝ) / 18)) * w ^ 3 + (-((1: ℝ) / 12)) * w ^ 2 + (-((1: ℝ) / 6)) * w ^ 1) (((1: ℝ) / 6) * ((-((1: ℝ) / 1)) * x ^ 5 + (-((1: ℝ) / 1)) * x ^ 4 + (-((1: ℝ) / 1)) * x ^ 3 + (-((1: ℝ) / 1)) * x ^ 2 + (-((1: ℝ) / 1)) * x ^ 1 + (-((1: ℝ) / 1)))) x := by
      refine (((((((hasDerivAt_pow 6 x).const_mul (-((1: ℝ) / 36))).add ((hasDerivAt_pow 5 x).const_mul (-((1: ℝ) / 30)))).add ((hasDerivAt_pow 4 x).const_mul (-((1: ℝ) / 24)))).add ((hasDerivAt_pow 3 x).const_mul (-((1: ℝ) / 18)))).add ((hasDerivAt_pow 2 x).const_mul (-((1: ℝ) / 12)))).add ((hasDerivAt_pow 1 x).const_mul (-((1: ℝ) / 6)))) |>.congr_deriv ?_
      ring
    refine (hP.add (hA.mul hlog)).congr_deriv ?_
    field_simp [hQ]; ring
  have hPc0 : ContinuousAt (fun w : ℝ => (-((1: ℝ) / 36)) * w ^ 6 + (-((1: ℝ) / 30)) * w ^ 5 + (-((1: ℝ) / 24)) * w ^ 4 + (-((1: ℝ) / 18)) * w ^ 3 + (-((1: ℝ) / 12)) * w ^ 2 + (-((1: ℝ) / 6)) * w ^ 1) 0 := ((((((mono_contAt (-((1: ℝ) / 36)) 6 0).add (mono_contAt (-((1: ℝ) / 30)) 5 0)).add (mono_contAt (-((1: ℝ) / 24)) 4 0)).add (mono_contAt (-((1: ℝ) / 18)) 3 0)).add (mono_contAt (-((1: ℝ) / 12)) 2 0)).add (mono_contAt (-((1: ℝ) / 6)) 1 0))
  have hPc1 : ContinuousAt (fun w : ℝ => (-((1: ℝ) / 36)) * w ^ 6 + (-((1: ℝ) / 30)) * w ^ 5 + (-((1: ℝ) / 24)) * w ^ 4 + (-((1: ℝ) / 18)) * w ^ 3 + (-((1: ℝ) / 12)) * w ^ 2 + (-((1: ℝ) / 6)) * w ^ 1) 1 := ((((((mono_contAt (-((1: ℝ) / 36)) 6 1).add (mono_contAt (-((1: ℝ) / 30)) 5 1)).add (mono_contAt (-((1: ℝ) / 24)) 4 1)).add (mono_contAt (-((1: ℝ) / 18)) 3 1)).add (mono_contAt (-((1: ℝ) / 12)) 2 1)).add (mono_contAt (-((1: ℝ) / 6)) 1 1))
  have hAc0 : ContinuousAt (fun w : ℝ => ((1: ℝ) / 6) * w ^ 6 + (-((1: ℝ) / 6)) * w ^ 0) 0 := (mono_contAt ((1: ℝ) / 6) 6 0).add (mono_contAt (-((1: ℝ) / 6)) 0 0)
  have hAc1 : ContinuousAt (fun w : ℝ => ((1: ℝ) / 6) * w ^ 6 + (-((1: ℝ) / 6)) * w ^ 0) 1 := (mono_contAt ((1: ℝ) / 6) 6 1).add (mono_contAt (-((1: ℝ) / 6)) 0 1)
  have heq : (fun w : ℝ => (-((1: ℝ) / 36)) * w ^ 6 + (-((1: ℝ) / 30)) * w ^ 5 + (-((1: ℝ) / 24)) * w ^ 4 + (-((1: ℝ) / 18)) * w ^ 3 + (-((1: ℝ) / 12)) * w ^ 2 + (-((1: ℝ) / 6)) * w ^ 1 + ((w ^ 6 - 1) / 6) * Real.log (1 - w)) = (fun w : ℝ => (-((1: ℝ) / 36)) * w ^ 6 + (-((1: ℝ) / 30)) * w ^ 5 + (-((1: ℝ) / 24)) * w ^ 4 + (-((1: ℝ) / 18)) * w ^ 3 + (-((1: ℝ) / 12)) * w ^ 2 + (-((1: ℝ) / 6)) * w ^ 1 + (((1: ℝ) / 6) * w ^ 6 + (-((1: ℝ) / 6)) * w ^ 0) * Real.log (1 - w)) := by
    funext w
    have hdiv : (w ^ 6 - 1) / 6 = ((1: ℝ) / 6) * w ^ 6 + (-((1: ℝ) / 6)) * w ^ 0 := by ring
    rw [hdiv]
  have hc0 : ContinuousAt (fun w : ℝ => Real.log (1 - w)) 0 := by
    have h1 : ContinuousAt (fun w : ℝ => 1 - w) 0 := by fun_prop
    exact ContinuousAt.comp_of_eq (Real.continuousAt_log (by norm_num : (1: ℝ) ≠ 0)) h1 (by norm_num)
  have hv0 : ((-((1: ℝ) / 36)) * 0 ^ 6 + (-((1: ℝ) / 30)) * 0 ^ 5 + (-((1: ℝ) / 24)) * 0 ^ 4 + (-((1: ℝ) / 18)) * 0 ^ 3 + (-((1: ℝ) / 12)) * 0 ^ 2 + (-((1: ℝ) / 6)) * 0 ^ 1 + (((1: ℝ) / 6) * 0 ^ 6 + (-((1: ℝ) / 6)) * 0 ^ 0) * Real.log (1 - 0)) = (0: ℝ) := by norm_num [Real.log_one]
  have ha : Tendsto (fun w : ℝ => (-((1: ℝ) / 36)) * w ^ 6 + (-((1: ℝ) / 30)) * w ^ 5 + (-((1: ℝ) / 24)) * w ^ 4 + (-((1: ℝ) / 18)) * w ^ 3 + (-((1: ℝ) / 12)) * w ^ 2 + (-((1: ℝ) / 6)) * w ^ 1 + ((w ^ 6 - 1) / 6) * Real.log (1 - w)) (nhdsWithin (0: ℝ) (Set.Ioi 0)) (nhds (0: ℝ)) := by
    rw [heq]
    have hten : Tendsto (fun w : ℝ => (-((1: ℝ) / 36)) * w ^ 6 + (-((1: ℝ) / 30)) * w ^ 5 + (-((1: ℝ) / 24)) * w ^ 4 + (-((1: ℝ) / 18)) * w ^ 3 + (-((1: ℝ) / 12)) * w ^ 2 + (-((1: ℝ) / 6)) * w ^ 1 + (((1: ℝ) / 6) * w ^ 6 + (-((1: ℝ) / 6)) * w ^ 0) * Real.log (1 - w)) (nhdsWithin (0: ℝ) (Set.Ioi 0)) (nhds ((-((1: ℝ) / 36)) * 0 ^ 6 + (-((1: ℝ) / 30)) * 0 ^ 5 + (-((1: ℝ) / 24)) * 0 ^ 4 + (-((1: ℝ) / 18)) * 0 ^ 3 + (-((1: ℝ) / 12)) * 0 ^ 2 + (-((1: ℝ) / 6)) * 0 ^ 1 + (((1: ℝ) / 6) * 0 ^ 6 + (-((1: ℝ) / 6)) * 0 ^ 0) * Real.log (1 - 0))) :=
      (hPc0.add (hAc0.mul hc0)).tendsto.mono_left nhdsWithin_le_nhds
    rwa [hv0] at hten
  have hAeq : ∀ z : ℝ, (((1: ℝ) / 6) * z ^ 6 + (-((1: ℝ) / 6)) * z ^ 0) * Real.log (1 - z)
      = ((1 - z) * Real.log (1 - z)) * ((-((1: ℝ) / 6)) * ((1: ℝ) + z + z ^ 2 + z ^ 3 + z ^ 4 + z ^ 5)) := by intro z; ring
  have tA2 : Tendsto (fun u : ℝ => (((1: ℝ) / 6) * u ^ 6 + (-((1: ℝ) / 6)) * u ^ 0) * Real.log (1 - u)) (nhdsWithin (1: ℝ) (Set.Iio 1)) (nhds (0: ℝ)) := by
    have key : Tendsto (fun u : ℝ => ((1 - u) * Real.log (1 - u)) * ((-((1: ℝ) / 6)) * ((1: ℝ) + u + u ^ 2 + u ^ 3 + u ^ 4 + u ^ 5))) (nhdsWithin (1: ℝ) (Set.Iio 1)) (nhds (0: ℝ)) :=
      tendsto_alm (by fun_prop : ContinuousAt (fun u : ℝ => (-((1: ℝ) / 6)) * ((1: ℝ) + u + u ^ 2 + u ^ 3 + u ^ 4 + u ^ 5)) 1)
    have heq2 : (fun u : ℝ => (((1: ℝ) / 6) * u ^ 6 + (-((1: ℝ) / 6)) * u ^ 0) * Real.log (1 - u))
        = (fun u : ℝ => ((1 - u) * Real.log (1 - u)) * ((-((1: ℝ) / 6)) * ((1: ℝ) + u + u ^ 2 + u ^ 3 + u ^ 4 + u ^ 5))) := by
      funext u; rw [hAeq u]
    rw [heq2]; exact key
  have hv1 : ((-((1: ℝ) / 36)) * 1 ^ 6 + (-((1: ℝ) / 30)) * 1 ^ 5 + (-((1: ℝ) / 24)) * 1 ^ 4 + (-((1: ℝ) / 18)) * 1 ^ 3 + (-((1: ℝ) / 12)) * 1 ^ 2 + (-((1: ℝ) / 6)) * 1 ^ 1 + (0: ℝ)) = (-((49: ℝ) / 120)) := by norm_num
  have hb : Tendsto (fun w : ℝ => (-((1: ℝ) / 36)) * w ^ 6 + (-((1: ℝ) / 30)) * w ^ 5 + (-((1: ℝ) / 24)) * w ^ 4 + (-((1: ℝ) / 18)) * w ^ 3 + (-((1: ℝ) / 12)) * w ^ 2 + (-((1: ℝ) / 6)) * w ^ 1 + ((w ^ 6 - 1) / 6) * Real.log (1 - w)) (nhdsWithin (1: ℝ) (Set.Iio 1)) (nhds (-((49: ℝ) / 120))) := by
    rw [heq]
    have hten : Tendsto (fun w : ℝ => (-((1: ℝ) / 36)) * w ^ 6 + (-((1: ℝ) / 30)) * w ^ 5 + (-((1: ℝ) / 24)) * w ^ 4 + (-((1: ℝ) / 18)) * w ^ 3 + (-((1: ℝ) / 12)) * w ^ 2 + (-((1: ℝ) / 6)) * w ^ 1 + (((1: ℝ) / 6) * w ^ 6 + (-((1: ℝ) / 6)) * w ^ 0) * Real.log (1 - w)) (nhdsWithin (1: ℝ) (Set.Iio 1)) (nhds ((-((1: ℝ) / 36)) * 1 ^ 6 + (-((1: ℝ) / 30)) * 1 ^ 5 + (-((1: ℝ) / 24)) * 1 ^ 4 + (-((1: ℝ) / 18)) * 1 ^ 3 + (-((1: ℝ) / 12)) * 1 ^ 2 + (-((1: ℝ) / 6)) * 1 ^ 1 + (0: ℝ))) :=
      (hPc1.tendsto.mono_left nhdsWithin_le_nhds).add tA2
    rwa [hv1] at hten
  have h := intervalIntegral.integral_eq_sub_of_hasDerivAt_of_tendsto (a := (0: ℝ)) (b := (1: ℝ))
    (by norm_num : (0: ℝ) < (1: ℝ)) hderiv hint ha hb
  exact h.trans (by norm_num)

theorem core_lm_7 : ∫ u in (0: ℝ)..1, u ^ 7 * Real.log (1 - u) = (-((761: ℝ) / 2240)) := by
  have hint : IntervalIntegrable (fun x : ℝ => x ^ 7 * Real.log (1 - x)) volume 0 1 := by
    refine IntervalIntegrable.congr (show Set.EqOn (fun x : ℝ => Real.log (1 - x) * x ^ 7) (fun x : ℝ => x ^ 7 * Real.log (1 - x)) (Set.uIoc (0: ℝ) 1) from fun x _ => by ring)
      (logm_int.mul_continuousOn (Continuous.continuousOn (by fun_prop : Continuous fun x : ℝ => x ^ 7)))
  have hderiv : ∀ x ∈ Set.Ioo (0: ℝ) 1, HasDerivAt
      (fun w : ℝ => (-((1: ℝ) / 64)) * w ^ 8 + (-((1: ℝ) / 56)) * w ^ 7 + (-((1: ℝ) / 48)) * w ^ 6 + (-((1: ℝ) / 40)) * w ^ 5 + (-((1: ℝ) / 32)) * w ^ 4 + (-((1: ℝ) / 24)) * w ^ 3 + (-((1: ℝ) / 16)) * w ^ 2 + (-((1: ℝ) / 8)) * w ^ 1 + ((w ^ 8 - 1) / 8) * Real.log (1 - w))
      (x ^ 7 * Real.log (1 - x)) x := by
    intro x hx
    have hx1 : (1: ℝ) - x ≠ 0 := by have := hx.2; linarith
    have hid : HasDerivAt (fun y : ℝ => y) 1 x := hasDerivAt_id' x
    have hinner : HasDerivAt (fun y : ℝ => 1 - y) ((0: ℝ) - 1) x := (hasDerivAt_const x 1).sub hid
    have hlog : HasDerivAt (fun w : ℝ => Real.log (1 - w)) ((-1: ℝ) / (1 - x)) x := by
      refine HasDerivAt.comp_of_eq x (hasDerivAt_log hx1) hinner rfl |>.congr_deriv ?_
      ring
    have hA : HasDerivAt (fun w : ℝ => (w ^ 8 - 1) / 8) (x ^ 7) x := by
      refine ((hasDerivAt_pow 8 x).sub (hasDerivAt_const x 1)).div_const 8 |>.congr_deriv ?_
      ring
    have hQ : (x: ℝ) ^ 8 - 1 = ((1 - x)) * ((-((1: ℝ) / 1)) * x ^ 7 + (-((1: ℝ) / 1)) * x ^ 6 + (-((1: ℝ) / 1)) * x ^ 5 + (-((1: ℝ) / 1)) * x ^ 4 + (-((1: ℝ) / 1)) * x ^ 3 + (-((1: ℝ) / 1)) * x ^ 2 + (-((1: ℝ) / 1)) * x ^ 1 + (-((1: ℝ) / 1))) := by ring
    have hP : HasDerivAt (fun w : ℝ => (-((1: ℝ) / 64)) * w ^ 8 + (-((1: ℝ) / 56)) * w ^ 7 + (-((1: ℝ) / 48)) * w ^ 6 + (-((1: ℝ) / 40)) * w ^ 5 + (-((1: ℝ) / 32)) * w ^ 4 + (-((1: ℝ) / 24)) * w ^ 3 + (-((1: ℝ) / 16)) * w ^ 2 + (-((1: ℝ) / 8)) * w ^ 1) (((1: ℝ) / 8) * ((-((1: ℝ) / 1)) * x ^ 7 + (-((1: ℝ) / 1)) * x ^ 6 + (-((1: ℝ) / 1)) * x ^ 5 + (-((1: ℝ) / 1)) * x ^ 4 + (-((1: ℝ) / 1)) * x ^ 3 + (-((1: ℝ) / 1)) * x ^ 2 + (-((1: ℝ) / 1)) * x ^ 1 + (-((1: ℝ) / 1)))) x := by
      refine (((((((((hasDerivAt_pow 8 x).const_mul (-((1: ℝ) / 64))).add ((hasDerivAt_pow 7 x).const_mul (-((1: ℝ) / 56)))).add ((hasDerivAt_pow 6 x).const_mul (-((1: ℝ) / 48)))).add ((hasDerivAt_pow 5 x).const_mul (-((1: ℝ) / 40)))).add ((hasDerivAt_pow 4 x).const_mul (-((1: ℝ) / 32)))).add ((hasDerivAt_pow 3 x).const_mul (-((1: ℝ) / 24)))).add ((hasDerivAt_pow 2 x).const_mul (-((1: ℝ) / 16)))).add ((hasDerivAt_pow 1 x).const_mul (-((1: ℝ) / 8)))) |>.congr_deriv ?_
      ring
    refine (hP.add (hA.mul hlog)).congr_deriv ?_
    field_simp [hQ]; ring
  have hPc0 : ContinuousAt (fun w : ℝ => (-((1: ℝ) / 64)) * w ^ 8 + (-((1: ℝ) / 56)) * w ^ 7 + (-((1: ℝ) / 48)) * w ^ 6 + (-((1: ℝ) / 40)) * w ^ 5 + (-((1: ℝ) / 32)) * w ^ 4 + (-((1: ℝ) / 24)) * w ^ 3 + (-((1: ℝ) / 16)) * w ^ 2 + (-((1: ℝ) / 8)) * w ^ 1) 0 := ((((((((mono_contAt (-((1: ℝ) / 64)) 8 0).add (mono_contAt (-((1: ℝ) / 56)) 7 0)).add (mono_contAt (-((1: ℝ) / 48)) 6 0)).add (mono_contAt (-((1: ℝ) / 40)) 5 0)).add (mono_contAt (-((1: ℝ) / 32)) 4 0)).add (mono_contAt (-((1: ℝ) / 24)) 3 0)).add (mono_contAt (-((1: ℝ) / 16)) 2 0)).add (mono_contAt (-((1: ℝ) / 8)) 1 0))
  have hPc1 : ContinuousAt (fun w : ℝ => (-((1: ℝ) / 64)) * w ^ 8 + (-((1: ℝ) / 56)) * w ^ 7 + (-((1: ℝ) / 48)) * w ^ 6 + (-((1: ℝ) / 40)) * w ^ 5 + (-((1: ℝ) / 32)) * w ^ 4 + (-((1: ℝ) / 24)) * w ^ 3 + (-((1: ℝ) / 16)) * w ^ 2 + (-((1: ℝ) / 8)) * w ^ 1) 1 := ((((((((mono_contAt (-((1: ℝ) / 64)) 8 1).add (mono_contAt (-((1: ℝ) / 56)) 7 1)).add (mono_contAt (-((1: ℝ) / 48)) 6 1)).add (mono_contAt (-((1: ℝ) / 40)) 5 1)).add (mono_contAt (-((1: ℝ) / 32)) 4 1)).add (mono_contAt (-((1: ℝ) / 24)) 3 1)).add (mono_contAt (-((1: ℝ) / 16)) 2 1)).add (mono_contAt (-((1: ℝ) / 8)) 1 1))
  have hAc0 : ContinuousAt (fun w : ℝ => ((1: ℝ) / 8) * w ^ 8 + (-((1: ℝ) / 8)) * w ^ 0) 0 := (mono_contAt ((1: ℝ) / 8) 8 0).add (mono_contAt (-((1: ℝ) / 8)) 0 0)
  have hAc1 : ContinuousAt (fun w : ℝ => ((1: ℝ) / 8) * w ^ 8 + (-((1: ℝ) / 8)) * w ^ 0) 1 := (mono_contAt ((1: ℝ) / 8) 8 1).add (mono_contAt (-((1: ℝ) / 8)) 0 1)
  have heq : (fun w : ℝ => (-((1: ℝ) / 64)) * w ^ 8 + (-((1: ℝ) / 56)) * w ^ 7 + (-((1: ℝ) / 48)) * w ^ 6 + (-((1: ℝ) / 40)) * w ^ 5 + (-((1: ℝ) / 32)) * w ^ 4 + (-((1: ℝ) / 24)) * w ^ 3 + (-((1: ℝ) / 16)) * w ^ 2 + (-((1: ℝ) / 8)) * w ^ 1 + ((w ^ 8 - 1) / 8) * Real.log (1 - w)) = (fun w : ℝ => (-((1: ℝ) / 64)) * w ^ 8 + (-((1: ℝ) / 56)) * w ^ 7 + (-((1: ℝ) / 48)) * w ^ 6 + (-((1: ℝ) / 40)) * w ^ 5 + (-((1: ℝ) / 32)) * w ^ 4 + (-((1: ℝ) / 24)) * w ^ 3 + (-((1: ℝ) / 16)) * w ^ 2 + (-((1: ℝ) / 8)) * w ^ 1 + (((1: ℝ) / 8) * w ^ 8 + (-((1: ℝ) / 8)) * w ^ 0) * Real.log (1 - w)) := by
    funext w
    have hdiv : (w ^ 8 - 1) / 8 = ((1: ℝ) / 8) * w ^ 8 + (-((1: ℝ) / 8)) * w ^ 0 := by ring
    rw [hdiv]
  have hc0 : ContinuousAt (fun w : ℝ => Real.log (1 - w)) 0 := by
    have h1 : ContinuousAt (fun w : ℝ => 1 - w) 0 := by fun_prop
    exact ContinuousAt.comp_of_eq (Real.continuousAt_log (by norm_num : (1: ℝ) ≠ 0)) h1 (by norm_num)
  have hv0 : ((-((1: ℝ) / 64)) * 0 ^ 8 + (-((1: ℝ) / 56)) * 0 ^ 7 + (-((1: ℝ) / 48)) * 0 ^ 6 + (-((1: ℝ) / 40)) * 0 ^ 5 + (-((1: ℝ) / 32)) * 0 ^ 4 + (-((1: ℝ) / 24)) * 0 ^ 3 + (-((1: ℝ) / 16)) * 0 ^ 2 + (-((1: ℝ) / 8)) * 0 ^ 1 + (((1: ℝ) / 8) * 0 ^ 8 + (-((1: ℝ) / 8)) * 0 ^ 0) * Real.log (1 - 0)) = (0: ℝ) := by norm_num [Real.log_one]
  have ha : Tendsto (fun w : ℝ => (-((1: ℝ) / 64)) * w ^ 8 + (-((1: ℝ) / 56)) * w ^ 7 + (-((1: ℝ) / 48)) * w ^ 6 + (-((1: ℝ) / 40)) * w ^ 5 + (-((1: ℝ) / 32)) * w ^ 4 + (-((1: ℝ) / 24)) * w ^ 3 + (-((1: ℝ) / 16)) * w ^ 2 + (-((1: ℝ) / 8)) * w ^ 1 + ((w ^ 8 - 1) / 8) * Real.log (1 - w)) (nhdsWithin (0: ℝ) (Set.Ioi 0)) (nhds (0: ℝ)) := by
    rw [heq]
    have hten : Tendsto (fun w : ℝ => (-((1: ℝ) / 64)) * w ^ 8 + (-((1: ℝ) / 56)) * w ^ 7 + (-((1: ℝ) / 48)) * w ^ 6 + (-((1: ℝ) / 40)) * w ^ 5 + (-((1: ℝ) / 32)) * w ^ 4 + (-((1: ℝ) / 24)) * w ^ 3 + (-((1: ℝ) / 16)) * w ^ 2 + (-((1: ℝ) / 8)) * w ^ 1 + (((1: ℝ) / 8) * w ^ 8 + (-((1: ℝ) / 8)) * w ^ 0) * Real.log (1 - w)) (nhdsWithin (0: ℝ) (Set.Ioi 0)) (nhds ((-((1: ℝ) / 64)) * 0 ^ 8 + (-((1: ℝ) / 56)) * 0 ^ 7 + (-((1: ℝ) / 48)) * 0 ^ 6 + (-((1: ℝ) / 40)) * 0 ^ 5 + (-((1: ℝ) / 32)) * 0 ^ 4 + (-((1: ℝ) / 24)) * 0 ^ 3 + (-((1: ℝ) / 16)) * 0 ^ 2 + (-((1: ℝ) / 8)) * 0 ^ 1 + (((1: ℝ) / 8) * 0 ^ 8 + (-((1: ℝ) / 8)) * 0 ^ 0) * Real.log (1 - 0))) :=
      (hPc0.add (hAc0.mul hc0)).tendsto.mono_left nhdsWithin_le_nhds
    rwa [hv0] at hten
  have hAeq : ∀ z : ℝ, (((1: ℝ) / 8) * z ^ 8 + (-((1: ℝ) / 8)) * z ^ 0) * Real.log (1 - z)
      = ((1 - z) * Real.log (1 - z)) * ((-((1: ℝ) / 8)) * ((1: ℝ) + z + z ^ 2 + z ^ 3 + z ^ 4 + z ^ 5 + z ^ 6 + z ^ 7)) := by intro z; ring
  have tA2 : Tendsto (fun u : ℝ => (((1: ℝ) / 8) * u ^ 8 + (-((1: ℝ) / 8)) * u ^ 0) * Real.log (1 - u)) (nhdsWithin (1: ℝ) (Set.Iio 1)) (nhds (0: ℝ)) := by
    have key : Tendsto (fun u : ℝ => ((1 - u) * Real.log (1 - u)) * ((-((1: ℝ) / 8)) * ((1: ℝ) + u + u ^ 2 + u ^ 3 + u ^ 4 + u ^ 5 + u ^ 6 + u ^ 7))) (nhdsWithin (1: ℝ) (Set.Iio 1)) (nhds (0: ℝ)) :=
      tendsto_alm (by fun_prop : ContinuousAt (fun u : ℝ => (-((1: ℝ) / 8)) * ((1: ℝ) + u + u ^ 2 + u ^ 3 + u ^ 4 + u ^ 5 + u ^ 6 + u ^ 7)) 1)
    have heq2 : (fun u : ℝ => (((1: ℝ) / 8) * u ^ 8 + (-((1: ℝ) / 8)) * u ^ 0) * Real.log (1 - u))
        = (fun u : ℝ => ((1 - u) * Real.log (1 - u)) * ((-((1: ℝ) / 8)) * ((1: ℝ) + u + u ^ 2 + u ^ 3 + u ^ 4 + u ^ 5 + u ^ 6 + u ^ 7))) := by
      funext u; rw [hAeq u]
    rw [heq2]; exact key
  have hv1 : ((-((1: ℝ) / 64)) * 1 ^ 8 + (-((1: ℝ) / 56)) * 1 ^ 7 + (-((1: ℝ) / 48)) * 1 ^ 6 + (-((1: ℝ) / 40)) * 1 ^ 5 + (-((1: ℝ) / 32)) * 1 ^ 4 + (-((1: ℝ) / 24)) * 1 ^ 3 + (-((1: ℝ) / 16)) * 1 ^ 2 + (-((1: ℝ) / 8)) * 1 ^ 1 + (0: ℝ)) = (-((761: ℝ) / 2240)) := by norm_num
  have hb : Tendsto (fun w : ℝ => (-((1: ℝ) / 64)) * w ^ 8 + (-((1: ℝ) / 56)) * w ^ 7 + (-((1: ℝ) / 48)) * w ^ 6 + (-((1: ℝ) / 40)) * w ^ 5 + (-((1: ℝ) / 32)) * w ^ 4 + (-((1: ℝ) / 24)) * w ^ 3 + (-((1: ℝ) / 16)) * w ^ 2 + (-((1: ℝ) / 8)) * w ^ 1 + ((w ^ 8 - 1) / 8) * Real.log (1 - w)) (nhdsWithin (1: ℝ) (Set.Iio 1)) (nhds (-((761: ℝ) / 2240))) := by
    rw [heq]
    have hten : Tendsto (fun w : ℝ => (-((1: ℝ) / 64)) * w ^ 8 + (-((1: ℝ) / 56)) * w ^ 7 + (-((1: ℝ) / 48)) * w ^ 6 + (-((1: ℝ) / 40)) * w ^ 5 + (-((1: ℝ) / 32)) * w ^ 4 + (-((1: ℝ) / 24)) * w ^ 3 + (-((1: ℝ) / 16)) * w ^ 2 + (-((1: ℝ) / 8)) * w ^ 1 + (((1: ℝ) / 8) * w ^ 8 + (-((1: ℝ) / 8)) * w ^ 0) * Real.log (1 - w)) (nhdsWithin (1: ℝ) (Set.Iio 1)) (nhds ((-((1: ℝ) / 64)) * 1 ^ 8 + (-((1: ℝ) / 56)) * 1 ^ 7 + (-((1: ℝ) / 48)) * 1 ^ 6 + (-((1: ℝ) / 40)) * 1 ^ 5 + (-((1: ℝ) / 32)) * 1 ^ 4 + (-((1: ℝ) / 24)) * 1 ^ 3 + (-((1: ℝ) / 16)) * 1 ^ 2 + (-((1: ℝ) / 8)) * 1 ^ 1 + (0: ℝ))) :=
      (hPc1.tendsto.mono_left nhdsWithin_le_nhds).add tA2
    rwa [hv1] at hten
  have h := intervalIntegral.integral_eq_sub_of_hasDerivAt_of_tendsto (a := (0: ℝ)) (b := (1: ℝ))
    (by norm_num : (0: ℝ) < (1: ℝ)) hderiv hint ha hb
  exact h.trans (by norm_num)

theorem core_lm_9 : ∫ u in (0: ℝ)..1, u ^ 9 * Real.log (1 - u) = (-((7381: ℝ) / 25200)) := by
  have hint : IntervalIntegrable (fun x : ℝ => x ^ 9 * Real.log (1 - x)) volume 0 1 := by
    refine IntervalIntegrable.congr (show Set.EqOn (fun x : ℝ => Real.log (1 - x) * x ^ 9) (fun x : ℝ => x ^ 9 * Real.log (1 - x)) (Set.uIoc (0: ℝ) 1) from fun x _ => by ring)
      (logm_int.mul_continuousOn (Continuous.continuousOn (by fun_prop : Continuous fun x : ℝ => x ^ 9)))
  have hderiv : ∀ x ∈ Set.Ioo (0: ℝ) 1, HasDerivAt
      (fun w : ℝ => (-((1: ℝ) / 100)) * w ^ 10 + (-((1: ℝ) / 90)) * w ^ 9 + (-((1: ℝ) / 80)) * w ^ 8 + (-((1: ℝ) / 70)) * w ^ 7 + (-((1: ℝ) / 60)) * w ^ 6 + (-((1: ℝ) / 50)) * w ^ 5 + (-((1: ℝ) / 40)) * w ^ 4 + (-((1: ℝ) / 30)) * w ^ 3 + (-((1: ℝ) / 20)) * w ^ 2 + (-((1: ℝ) / 10)) * w ^ 1 + ((w ^ 10 - 1) / 10) * Real.log (1 - w))
      (x ^ 9 * Real.log (1 - x)) x := by
    intro x hx
    have hx1 : (1: ℝ) - x ≠ 0 := by have := hx.2; linarith
    have hid : HasDerivAt (fun y : ℝ => y) 1 x := hasDerivAt_id' x
    have hinner : HasDerivAt (fun y : ℝ => 1 - y) ((0: ℝ) - 1) x := (hasDerivAt_const x 1).sub hid
    have hlog : HasDerivAt (fun w : ℝ => Real.log (1 - w)) ((-1: ℝ) / (1 - x)) x := by
      refine HasDerivAt.comp_of_eq x (hasDerivAt_log hx1) hinner rfl |>.congr_deriv ?_
      ring
    have hA : HasDerivAt (fun w : ℝ => (w ^ 10 - 1) / 10) (x ^ 9) x := by
      refine ((hasDerivAt_pow 10 x).sub (hasDerivAt_const x 1)).div_const 10 |>.congr_deriv ?_
      ring
    have hQ : (x: ℝ) ^ 10 - 1 = ((1 - x)) * ((-((1: ℝ) / 1)) * x ^ 9 + (-((1: ℝ) / 1)) * x ^ 8 + (-((1: ℝ) / 1)) * x ^ 7 + (-((1: ℝ) / 1)) * x ^ 6 + (-((1: ℝ) / 1)) * x ^ 5 + (-((1: ℝ) / 1)) * x ^ 4 + (-((1: ℝ) / 1)) * x ^ 3 + (-((1: ℝ) / 1)) * x ^ 2 + (-((1: ℝ) / 1)) * x ^ 1 + (-((1: ℝ) / 1))) := by ring
    have hP : HasDerivAt (fun w : ℝ => (-((1: ℝ) / 100)) * w ^ 10 + (-((1: ℝ) / 90)) * w ^ 9 + (-((1: ℝ) / 80)) * w ^ 8 + (-((1: ℝ) / 70)) * w ^ 7 + (-((1: ℝ) / 60)) * w ^ 6 + (-((1: ℝ) / 50)) * w ^ 5 + (-((1: ℝ) / 40)) * w ^ 4 + (-((1: ℝ) / 30)) * w ^ 3 + (-((1: ℝ) / 20)) * w ^ 2 + (-((1: ℝ) / 10)) * w ^ 1) (((1: ℝ) / 10) * ((-((1: ℝ) / 1)) * x ^ 9 + (-((1: ℝ) / 1)) * x ^ 8 + (-((1: ℝ) / 1)) * x ^ 7 + (-((1: ℝ) / 1)) * x ^ 6 + (-((1: ℝ) / 1)) * x ^ 5 + (-((1: ℝ) / 1)) * x ^ 4 + (-((1: ℝ) / 1)) * x ^ 3 + (-((1: ℝ) / 1)) * x ^ 2 + (-((1: ℝ) / 1)) * x ^ 1 + (-((1: ℝ) / 1)))) x := by
      refine (((((((((((hasDerivAt_pow 10 x).const_mul (-((1: ℝ) / 100))).add ((hasDerivAt_pow 9 x).const_mul (-((1: ℝ) / 90)))).add ((hasDerivAt_pow 8 x).const_mul (-((1: ℝ) / 80)))).add ((hasDerivAt_pow 7 x).const_mul (-((1: ℝ) / 70)))).add ((hasDerivAt_pow 6 x).const_mul (-((1: ℝ) / 60)))).add ((hasDerivAt_pow 5 x).const_mul (-((1: ℝ) / 50)))).add ((hasDerivAt_pow 4 x).const_mul (-((1: ℝ) / 40)))).add ((hasDerivAt_pow 3 x).const_mul (-((1: ℝ) / 30)))).add ((hasDerivAt_pow 2 x).const_mul (-((1: ℝ) / 20)))).add ((hasDerivAt_pow 1 x).const_mul (-((1: ℝ) / 10)))) |>.congr_deriv ?_
      ring
    refine (hP.add (hA.mul hlog)).congr_deriv ?_
    field_simp [hQ]; ring
  have hPc0 : ContinuousAt (fun w : ℝ => (-((1: ℝ) / 100)) * w ^ 10 + (-((1: ℝ) / 90)) * w ^ 9 + (-((1: ℝ) / 80)) * w ^ 8 + (-((1: ℝ) / 70)) * w ^ 7 + (-((1: ℝ) / 60)) * w ^ 6 + (-((1: ℝ) / 50)) * w ^ 5 + (-((1: ℝ) / 40)) * w ^ 4 + (-((1: ℝ) / 30)) * w ^ 3 + (-((1: ℝ) / 20)) * w ^ 2 + (-((1: ℝ) / 10)) * w ^ 1) 0 := ((((((((((mono_contAt (-((1: ℝ) / 100)) 10 0).add (mono_contAt (-((1: ℝ) / 90)) 9 0)).add (mono_contAt (-((1: ℝ) / 80)) 8 0)).add (mono_contAt (-((1: ℝ) / 70)) 7 0)).add (mono_contAt (-((1: ℝ) / 60)) 6 0)).add (mono_contAt (-((1: ℝ) / 50)) 5 0)).add (mono_contAt (-((1: ℝ) / 40)) 4 0)).add (mono_contAt (-((1: ℝ) / 30)) 3 0)).add (mono_contAt (-((1: ℝ) / 20)) 2 0)).add (mono_contAt (-((1: ℝ) / 10)) 1 0))
  have hPc1 : ContinuousAt (fun w : ℝ => (-((1: ℝ) / 100)) * w ^ 10 + (-((1: ℝ) / 90)) * w ^ 9 + (-((1: ℝ) / 80)) * w ^ 8 + (-((1: ℝ) / 70)) * w ^ 7 + (-((1: ℝ) / 60)) * w ^ 6 + (-((1: ℝ) / 50)) * w ^ 5 + (-((1: ℝ) / 40)) * w ^ 4 + (-((1: ℝ) / 30)) * w ^ 3 + (-((1: ℝ) / 20)) * w ^ 2 + (-((1: ℝ) / 10)) * w ^ 1) 1 := ((((((((((mono_contAt (-((1: ℝ) / 100)) 10 1).add (mono_contAt (-((1: ℝ) / 90)) 9 1)).add (mono_contAt (-((1: ℝ) / 80)) 8 1)).add (mono_contAt (-((1: ℝ) / 70)) 7 1)).add (mono_contAt (-((1: ℝ) / 60)) 6 1)).add (mono_contAt (-((1: ℝ) / 50)) 5 1)).add (mono_contAt (-((1: ℝ) / 40)) 4 1)).add (mono_contAt (-((1: ℝ) / 30)) 3 1)).add (mono_contAt (-((1: ℝ) / 20)) 2 1)).add (mono_contAt (-((1: ℝ) / 10)) 1 1))
  have hAc0 : ContinuousAt (fun w : ℝ => ((1: ℝ) / 10) * w ^ 10 + (-((1: ℝ) / 10)) * w ^ 0) 0 := (mono_contAt ((1: ℝ) / 10) 10 0).add (mono_contAt (-((1: ℝ) / 10)) 0 0)
  have hAc1 : ContinuousAt (fun w : ℝ => ((1: ℝ) / 10) * w ^ 10 + (-((1: ℝ) / 10)) * w ^ 0) 1 := (mono_contAt ((1: ℝ) / 10) 10 1).add (mono_contAt (-((1: ℝ) / 10)) 0 1)
  have heq : (fun w : ℝ => (-((1: ℝ) / 100)) * w ^ 10 + (-((1: ℝ) / 90)) * w ^ 9 + (-((1: ℝ) / 80)) * w ^ 8 + (-((1: ℝ) / 70)) * w ^ 7 + (-((1: ℝ) / 60)) * w ^ 6 + (-((1: ℝ) / 50)) * w ^ 5 + (-((1: ℝ) / 40)) * w ^ 4 + (-((1: ℝ) / 30)) * w ^ 3 + (-((1: ℝ) / 20)) * w ^ 2 + (-((1: ℝ) / 10)) * w ^ 1 + ((w ^ 10 - 1) / 10) * Real.log (1 - w)) = (fun w : ℝ => (-((1: ℝ) / 100)) * w ^ 10 + (-((1: ℝ) / 90)) * w ^ 9 + (-((1: ℝ) / 80)) * w ^ 8 + (-((1: ℝ) / 70)) * w ^ 7 + (-((1: ℝ) / 60)) * w ^ 6 + (-((1: ℝ) / 50)) * w ^ 5 + (-((1: ℝ) / 40)) * w ^ 4 + (-((1: ℝ) / 30)) * w ^ 3 + (-((1: ℝ) / 20)) * w ^ 2 + (-((1: ℝ) / 10)) * w ^ 1 + (((1: ℝ) / 10) * w ^ 10 + (-((1: ℝ) / 10)) * w ^ 0) * Real.log (1 - w)) := by
    funext w
    have hdiv : (w ^ 10 - 1) / 10 = ((1: ℝ) / 10) * w ^ 10 + (-((1: ℝ) / 10)) * w ^ 0 := by ring
    rw [hdiv]
  have hc0 : ContinuousAt (fun w : ℝ => Real.log (1 - w)) 0 := by
    have h1 : ContinuousAt (fun w : ℝ => 1 - w) 0 := by fun_prop
    exact ContinuousAt.comp_of_eq (Real.continuousAt_log (by norm_num : (1: ℝ) ≠ 0)) h1 (by norm_num)
  have hv0 : ((-((1: ℝ) / 100)) * 0 ^ 10 + (-((1: ℝ) / 90)) * 0 ^ 9 + (-((1: ℝ) / 80)) * 0 ^ 8 + (-((1: ℝ) / 70)) * 0 ^ 7 + (-((1: ℝ) / 60)) * 0 ^ 6 + (-((1: ℝ) / 50)) * 0 ^ 5 + (-((1: ℝ) / 40)) * 0 ^ 4 + (-((1: ℝ) / 30)) * 0 ^ 3 + (-((1: ℝ) / 20)) * 0 ^ 2 + (-((1: ℝ) / 10)) * 0 ^ 1 + (((1: ℝ) / 10) * 0 ^ 10 + (-((1: ℝ) / 10)) * 0 ^ 0) * Real.log (1 - 0)) = (0: ℝ) := by norm_num [Real.log_one]
  have ha : Tendsto (fun w : ℝ => (-((1: ℝ) / 100)) * w ^ 10 + (-((1: ℝ) / 90)) * w ^ 9 + (-((1: ℝ) / 80)) * w ^ 8 + (-((1: ℝ) / 70)) * w ^ 7 + (-((1: ℝ) / 60)) * w ^ 6 + (-((1: ℝ) / 50)) * w ^ 5 + (-((1: ℝ) / 40)) * w ^ 4 + (-((1: ℝ) / 30)) * w ^ 3 + (-((1: ℝ) / 20)) * w ^ 2 + (-((1: ℝ) / 10)) * w ^ 1 + ((w ^ 10 - 1) / 10) * Real.log (1 - w)) (nhdsWithin (0: ℝ) (Set.Ioi 0)) (nhds (0: ℝ)) := by
    rw [heq]
    have hten : Tendsto (fun w : ℝ => (-((1: ℝ) / 100)) * w ^ 10 + (-((1: ℝ) / 90)) * w ^ 9 + (-((1: ℝ) / 80)) * w ^ 8 + (-((1: ℝ) / 70)) * w ^ 7 + (-((1: ℝ) / 60)) * w ^ 6 + (-((1: ℝ) / 50)) * w ^ 5 + (-((1: ℝ) / 40)) * w ^ 4 + (-((1: ℝ) / 30)) * w ^ 3 + (-((1: ℝ) / 20)) * w ^ 2 + (-((1: ℝ) / 10)) * w ^ 1 + (((1: ℝ) / 10) * w ^ 10 + (-((1: ℝ) / 10)) * w ^ 0) * Real.log (1 - w)) (nhdsWithin (0: ℝ) (Set.Ioi 0)) (nhds ((-((1: ℝ) / 100)) * 0 ^ 10 + (-((1: ℝ) / 90)) * 0 ^ 9 + (-((1: ℝ) / 80)) * 0 ^ 8 + (-((1: ℝ) / 70)) * 0 ^ 7 + (-((1: ℝ) / 60)) * 0 ^ 6 + (-((1: ℝ) / 50)) * 0 ^ 5 + (-((1: ℝ) / 40)) * 0 ^ 4 + (-((1: ℝ) / 30)) * 0 ^ 3 + (-((1: ℝ) / 20)) * 0 ^ 2 + (-((1: ℝ) / 10)) * 0 ^ 1 + (((1: ℝ) / 10) * 0 ^ 10 + (-((1: ℝ) / 10)) * 0 ^ 0) * Real.log (1 - 0))) :=
      (hPc0.add (hAc0.mul hc0)).tendsto.mono_left nhdsWithin_le_nhds
    rwa [hv0] at hten
  have hAeq : ∀ z : ℝ, (((1: ℝ) / 10) * z ^ 10 + (-((1: ℝ) / 10)) * z ^ 0) * Real.log (1 - z)
      = ((1 - z) * Real.log (1 - z)) * ((-((1: ℝ) / 10)) * ((1: ℝ) + z + z ^ 2 + z ^ 3 + z ^ 4 + z ^ 5 + z ^ 6 + z ^ 7 + z ^ 8 + z ^ 9)) := by intro z; ring
  have tA2 : Tendsto (fun u : ℝ => (((1: ℝ) / 10) * u ^ 10 + (-((1: ℝ) / 10)) * u ^ 0) * Real.log (1 - u)) (nhdsWithin (1: ℝ) (Set.Iio 1)) (nhds (0: ℝ)) := by
    have key : Tendsto (fun u : ℝ => ((1 - u) * Real.log (1 - u)) * ((-((1: ℝ) / 10)) * ((1: ℝ) + u + u ^ 2 + u ^ 3 + u ^ 4 + u ^ 5 + u ^ 6 + u ^ 7 + u ^ 8 + u ^ 9))) (nhdsWithin (1: ℝ) (Set.Iio 1)) (nhds (0: ℝ)) :=
      tendsto_alm (by fun_prop : ContinuousAt (fun u : ℝ => (-((1: ℝ) / 10)) * ((1: ℝ) + u + u ^ 2 + u ^ 3 + u ^ 4 + u ^ 5 + u ^ 6 + u ^ 7 + u ^ 8 + u ^ 9)) 1)
    have heq2 : (fun u : ℝ => (((1: ℝ) / 10) * u ^ 10 + (-((1: ℝ) / 10)) * u ^ 0) * Real.log (1 - u))
        = (fun u : ℝ => ((1 - u) * Real.log (1 - u)) * ((-((1: ℝ) / 10)) * ((1: ℝ) + u + u ^ 2 + u ^ 3 + u ^ 4 + u ^ 5 + u ^ 6 + u ^ 7 + u ^ 8 + u ^ 9))) := by
      funext u; rw [hAeq u]
    rw [heq2]; exact key
  have hv1 : ((-((1: ℝ) / 100)) * 1 ^ 10 + (-((1: ℝ) / 90)) * 1 ^ 9 + (-((1: ℝ) / 80)) * 1 ^ 8 + (-((1: ℝ) / 70)) * 1 ^ 7 + (-((1: ℝ) / 60)) * 1 ^ 6 + (-((1: ℝ) / 50)) * 1 ^ 5 + (-((1: ℝ) / 40)) * 1 ^ 4 + (-((1: ℝ) / 30)) * 1 ^ 3 + (-((1: ℝ) / 20)) * 1 ^ 2 + (-((1: ℝ) / 10)) * 1 ^ 1 + (0: ℝ)) = (-((7381: ℝ) / 25200)) := by norm_num
  have hb : Tendsto (fun w : ℝ => (-((1: ℝ) / 100)) * w ^ 10 + (-((1: ℝ) / 90)) * w ^ 9 + (-((1: ℝ) / 80)) * w ^ 8 + (-((1: ℝ) / 70)) * w ^ 7 + (-((1: ℝ) / 60)) * w ^ 6 + (-((1: ℝ) / 50)) * w ^ 5 + (-((1: ℝ) / 40)) * w ^ 4 + (-((1: ℝ) / 30)) * w ^ 3 + (-((1: ℝ) / 20)) * w ^ 2 + (-((1: ℝ) / 10)) * w ^ 1 + ((w ^ 10 - 1) / 10) * Real.log (1 - w)) (nhdsWithin (1: ℝ) (Set.Iio 1)) (nhds (-((7381: ℝ) / 25200))) := by
    rw [heq]
    have hten : Tendsto (fun w : ℝ => (-((1: ℝ) / 100)) * w ^ 10 + (-((1: ℝ) / 90)) * w ^ 9 + (-((1: ℝ) / 80)) * w ^ 8 + (-((1: ℝ) / 70)) * w ^ 7 + (-((1: ℝ) / 60)) * w ^ 6 + (-((1: ℝ) / 50)) * w ^ 5 + (-((1: ℝ) / 40)) * w ^ 4 + (-((1: ℝ) / 30)) * w ^ 3 + (-((1: ℝ) / 20)) * w ^ 2 + (-((1: ℝ) / 10)) * w ^ 1 + (((1: ℝ) / 10) * w ^ 10 + (-((1: ℝ) / 10)) * w ^ 0) * Real.log (1 - w)) (nhdsWithin (1: ℝ) (Set.Iio 1)) (nhds ((-((1: ℝ) / 100)) * 1 ^ 10 + (-((1: ℝ) / 90)) * 1 ^ 9 + (-((1: ℝ) / 80)) * 1 ^ 8 + (-((1: ℝ) / 70)) * 1 ^ 7 + (-((1: ℝ) / 60)) * 1 ^ 6 + (-((1: ℝ) / 50)) * 1 ^ 5 + (-((1: ℝ) / 40)) * 1 ^ 4 + (-((1: ℝ) / 30)) * 1 ^ 3 + (-((1: ℝ) / 20)) * 1 ^ 2 + (-((1: ℝ) / 10)) * 1 ^ 1 + (0: ℝ))) :=
      (hPc1.tendsto.mono_left nhdsWithin_le_nhds).add tA2
    rwa [hv1] at hten
  have h := intervalIntegral.integral_eq_sub_of_hasDerivAt_of_tendsto (a := (0: ℝ)) (b := (1: ℝ))
    (by norm_num : (0: ℝ) < (1: ℝ)) hderiv hint ha hb
  exact h.trans (by norm_num)

theorem core_lp_1 : ∫ u in (0: ℝ)..1, u ^ 1 * Real.log (1 + u) = ((1: ℝ) / 4) := by
  have hint : IntervalIntegrable (fun x : ℝ => x ^ 1 * Real.log (1 + x)) volume 0 1 := by
    refine IntervalIntegrable.congr (show Set.EqOn (fun x : ℝ => Real.log (x + 1) * x ^ 1) (fun x : ℝ => x ^ 1 * Real.log (1 + x)) (Set.uIoc (0: ℝ) 1) from fun x _ => by ring)
      (logp_int.mul_continuousOn (Continuous.continuousOn (by fun_prop : Continuous fun x : ℝ => x ^ 1)))
  have hderiv : ∀ x ∈ Set.Ioo (0: ℝ) 1, HasDerivAt
      (fun w : ℝ => (-((1: ℝ) / 4)) * w ^ 2 + ((1: ℝ) / 2) * w ^ 1 + ((w ^ 2 - 1) / 2) * Real.log (1 + w))
      (x ^ 1 * Real.log (1 + x)) x := by
    intro x hx
    have hx1 : (1: ℝ) + x ≠ 0 := by have := hx.1; linarith
    have hid : HasDerivAt (fun y : ℝ => y) 1 x := hasDerivAt_id' x
    have hinner : HasDerivAt (fun y : ℝ => 1 + y) ((0: ℝ) + 1) x := (hasDerivAt_const x 1).add hid
    have hlog : HasDerivAt (fun w : ℝ => Real.log (1 + w)) ((1: ℝ) / (1 + x)) x := by
      refine HasDerivAt.comp_of_eq x (hasDerivAt_log hx1) hinner rfl |>.congr_deriv ?_
      ring
    have hA : HasDerivAt (fun w : ℝ => (w ^ 2 - 1) / 2) (x ^ 1) x := by
      refine ((hasDerivAt_pow 2 x).sub (hasDerivAt_const x 1)).div_const 2 |>.congr_deriv ?_
      ring
    have hQ : (x: ℝ) ^ 2 - 1 = ((1 + x)) * (x ^ 1 + (-((1: ℝ) / 1))) := by ring
    have hP : HasDerivAt (fun w : ℝ => (-((1: ℝ) / 4)) * w ^ 2 + ((1: ℝ) / 2) * w ^ 1) ((-((1: ℝ) / 2)) * (x ^ 1 + (-((1: ℝ) / 1)))) x := by
      refine (((hasDerivAt_pow 2 x).const_mul (-((1: ℝ) / 4))).add ((hasDerivAt_pow 1 x).const_mul ((1: ℝ) / 2))) |>.congr_deriv ?_
      ring
    refine (hP.add (hA.mul hlog)).congr_deriv ?_
    field_simp [hQ]; ring
  have hPc0 : ContinuousAt (fun w : ℝ => (-((1: ℝ) / 4)) * w ^ 2 + ((1: ℝ) / 2) * w ^ 1) 0 := ((mono_contAt (-((1: ℝ) / 4)) 2 0).add (mono_contAt ((1: ℝ) / 2) 1 0))
  have hPc1 : ContinuousAt (fun w : ℝ => (-((1: ℝ) / 4)) * w ^ 2 + ((1: ℝ) / 2) * w ^ 1) 1 := ((mono_contAt (-((1: ℝ) / 4)) 2 1).add (mono_contAt ((1: ℝ) / 2) 1 1))
  have hAc0 : ContinuousAt (fun w : ℝ => ((1: ℝ) / 2) * w ^ 2 + (-((1: ℝ) / 2)) * w ^ 0) 0 := (mono_contAt ((1: ℝ) / 2) 2 0).add (mono_contAt (-((1: ℝ) / 2)) 0 0)
  have hAc1 : ContinuousAt (fun w : ℝ => ((1: ℝ) / 2) * w ^ 2 + (-((1: ℝ) / 2)) * w ^ 0) 1 := (mono_contAt ((1: ℝ) / 2) 2 1).add (mono_contAt (-((1: ℝ) / 2)) 0 1)
  have heq : (fun w : ℝ => (-((1: ℝ) / 4)) * w ^ 2 + ((1: ℝ) / 2) * w ^ 1 + ((w ^ 2 - 1) / 2) * Real.log (1 + w)) = (fun w : ℝ => (-((1: ℝ) / 4)) * w ^ 2 + ((1: ℝ) / 2) * w ^ 1 + (((1: ℝ) / 2) * w ^ 2 + (-((1: ℝ) / 2)) * w ^ 0) * Real.log (1 + w)) := by
    funext w
    have hdiv : (w ^ 2 - 1) / 2 = ((1: ℝ) / 2) * w ^ 2 + (-((1: ℝ) / 2)) * w ^ 0 := by ring
    rw [hdiv]
  have hv0 : ((-((1: ℝ) / 4)) * 0 ^ 2 + ((1: ℝ) / 2) * 0 ^ 1 + (((1: ℝ) / 2) * 0 ^ 2 + (-((1: ℝ) / 2)) * 0 ^ 0) * Real.log (1 + 0)) = (0: ℝ) := by norm_num [Real.log_one]
  have hv1 : ((-((1: ℝ) / 4)) * 1 ^ 2 + ((1: ℝ) / 2) * 1 ^ 1 + (((1: ℝ) / 2) * 1 ^ 2 + (-((1: ℝ) / 2)) * 1 ^ 0) * Real.log (1 + 1)) = ((1: ℝ) / 4) := by norm_num [Real.log_one]
  have ha : Tendsto (fun w : ℝ => (-((1: ℝ) / 4)) * w ^ 2 + ((1: ℝ) / 2) * w ^ 1 + ((w ^ 2 - 1) / 2) * Real.log (1 + w)) (nhdsWithin (0: ℝ) (Set.Ioi 0)) (nhds (0: ℝ)) := by
    rw [heq]
    have hten : Tendsto (fun w : ℝ => (-((1: ℝ) / 4)) * w ^ 2 + ((1: ℝ) / 2) * w ^ 1 + (((1: ℝ) / 2) * w ^ 2 + (-((1: ℝ) / 2)) * w ^ 0) * Real.log (1 + w)) (nhdsWithin (0: ℝ) (Set.Ioi 0)) (nhds ((-((1: ℝ) / 4)) * 0 ^ 2 + ((1: ℝ) / 2) * 0 ^ 1 + (((1: ℝ) / 2) * 0 ^ 2 + (-((1: ℝ) / 2)) * 0 ^ 0) * Real.log (1 + 0))) :=
      (hPc0.add (hAc0.mul logp_contAt0)).tendsto.mono_left nhdsWithin_le_nhds
    rwa [hv0] at hten
  have hb : Tendsto (fun w : ℝ => (-((1: ℝ) / 4)) * w ^ 2 + ((1: ℝ) / 2) * w ^ 1 + ((w ^ 2 - 1) / 2) * Real.log (1 + w)) (nhdsWithin (1: ℝ) (Set.Iio 1)) (nhds ((1: ℝ) / 4)) := by
    rw [heq]
    have hten : Tendsto (fun w : ℝ => (-((1: ℝ) / 4)) * w ^ 2 + ((1: ℝ) / 2) * w ^ 1 + (((1: ℝ) / 2) * w ^ 2 + (-((1: ℝ) / 2)) * w ^ 0) * Real.log (1 + w)) (nhdsWithin (1: ℝ) (Set.Iio 1)) (nhds ((-((1: ℝ) / 4)) * 1 ^ 2 + ((1: ℝ) / 2) * 1 ^ 1 + (((1: ℝ) / 2) * 1 ^ 2 + (-((1: ℝ) / 2)) * 1 ^ 0) * Real.log (1 + 1))) :=
      (hPc1.add (hAc1.mul logp_contAt1)).tendsto.mono_left nhdsWithin_le_nhds
    rwa [hv1] at hten
  have h := intervalIntegral.integral_eq_sub_of_hasDerivAt_of_tendsto (a := (0: ℝ)) (b := (1: ℝ))
    (by norm_num : (0: ℝ) < (1: ℝ)) hderiv hint ha hb
  exact h.trans (by norm_num)

theorem core_lp_3 : ∫ u in (0: ℝ)..1, u ^ 3 * Real.log (1 + u) = ((7: ℝ) / 48) := by
  have hint : IntervalIntegrable (fun x : ℝ => x ^ 3 * Real.log (1 + x)) volume 0 1 := by
    refine IntervalIntegrable.congr (show Set.EqOn (fun x : ℝ => Real.log (x + 1) * x ^ 3) (fun x : ℝ => x ^ 3 * Real.log (1 + x)) (Set.uIoc (0: ℝ) 1) from fun x _ => by ring)
      (logp_int.mul_continuousOn (Continuous.continuousOn (by fun_prop : Continuous fun x : ℝ => x ^ 3)))
  have hderiv : ∀ x ∈ Set.Ioo (0: ℝ) 1, HasDerivAt
      (fun w : ℝ => (-((1: ℝ) / 16)) * w ^ 4 + ((1: ℝ) / 12) * w ^ 3 + (-((1: ℝ) / 8)) * w ^ 2 + ((1: ℝ) / 4) * w ^ 1 + ((w ^ 4 - 1) / 4) * Real.log (1 + w))
      (x ^ 3 * Real.log (1 + x)) x := by
    intro x hx
    have hx1 : (1: ℝ) + x ≠ 0 := by have := hx.1; linarith
    have hid : HasDerivAt (fun y : ℝ => y) 1 x := hasDerivAt_id' x
    have hinner : HasDerivAt (fun y : ℝ => 1 + y) ((0: ℝ) + 1) x := (hasDerivAt_const x 1).add hid
    have hlog : HasDerivAt (fun w : ℝ => Real.log (1 + w)) ((1: ℝ) / (1 + x)) x := by
      refine HasDerivAt.comp_of_eq x (hasDerivAt_log hx1) hinner rfl |>.congr_deriv ?_
      ring
    have hA : HasDerivAt (fun w : ℝ => (w ^ 4 - 1) / 4) (x ^ 3) x := by
      refine ((hasDerivAt_pow 4 x).sub (hasDerivAt_const x 1)).div_const 4 |>.congr_deriv ?_
      ring
    have hQ : (x: ℝ) ^ 4 - 1 = ((1 + x)) * (x ^ 3 + (-((1: ℝ) / 1)) * x ^ 2 + x ^ 1 + (-((1: ℝ) / 1))) := by ring
    have hP : HasDerivAt (fun w : ℝ => (-((1: ℝ) / 16)) * w ^ 4 + ((1: ℝ) / 12) * w ^ 3 + (-((1: ℝ) / 8)) * w ^ 2 + ((1: ℝ) / 4) * w ^ 1) ((-((1: ℝ) / 4)) * (x ^ 3 + (-((1: ℝ) / 1)) * x ^ 2 + x ^ 1 + (-((1: ℝ) / 1)))) x := by
      refine (((((hasDerivAt_pow 4 x).const_mul (-((1: ℝ) / 16))).add ((hasDerivAt_pow 3 x).const_mul ((1: ℝ) / 12))).add ((hasDerivAt_pow 2 x).const_mul (-((1: ℝ) / 8)))).add ((hasDerivAt_pow 1 x).const_mul ((1: ℝ) / 4))) |>.congr_deriv ?_
      ring
    refine (hP.add (hA.mul hlog)).congr_deriv ?_
    field_simp [hQ]; ring
  have hPc0 : ContinuousAt (fun w : ℝ => (-((1: ℝ) / 16)) * w ^ 4 + ((1: ℝ) / 12) * w ^ 3 + (-((1: ℝ) / 8)) * w ^ 2 + ((1: ℝ) / 4) * w ^ 1) 0 := ((((mono_contAt (-((1: ℝ) / 16)) 4 0).add (mono_contAt ((1: ℝ) / 12) 3 0)).add (mono_contAt (-((1: ℝ) / 8)) 2 0)).add (mono_contAt ((1: ℝ) / 4) 1 0))
  have hPc1 : ContinuousAt (fun w : ℝ => (-((1: ℝ) / 16)) * w ^ 4 + ((1: ℝ) / 12) * w ^ 3 + (-((1: ℝ) / 8)) * w ^ 2 + ((1: ℝ) / 4) * w ^ 1) 1 := ((((mono_contAt (-((1: ℝ) / 16)) 4 1).add (mono_contAt ((1: ℝ) / 12) 3 1)).add (mono_contAt (-((1: ℝ) / 8)) 2 1)).add (mono_contAt ((1: ℝ) / 4) 1 1))
  have hAc0 : ContinuousAt (fun w : ℝ => ((1: ℝ) / 4) * w ^ 4 + (-((1: ℝ) / 4)) * w ^ 0) 0 := (mono_contAt ((1: ℝ) / 4) 4 0).add (mono_contAt (-((1: ℝ) / 4)) 0 0)
  have hAc1 : ContinuousAt (fun w : ℝ => ((1: ℝ) / 4) * w ^ 4 + (-((1: ℝ) / 4)) * w ^ 0) 1 := (mono_contAt ((1: ℝ) / 4) 4 1).add (mono_contAt (-((1: ℝ) / 4)) 0 1)
  have heq : (fun w : ℝ => (-((1: ℝ) / 16)) * w ^ 4 + ((1: ℝ) / 12) * w ^ 3 + (-((1: ℝ) / 8)) * w ^ 2 + ((1: ℝ) / 4) * w ^ 1 + ((w ^ 4 - 1) / 4) * Real.log (1 + w)) = (fun w : ℝ => (-((1: ℝ) / 16)) * w ^ 4 + ((1: ℝ) / 12) * w ^ 3 + (-((1: ℝ) / 8)) * w ^ 2 + ((1: ℝ) / 4) * w ^ 1 + (((1: ℝ) / 4) * w ^ 4 + (-((1: ℝ) / 4)) * w ^ 0) * Real.log (1 + w)) := by
    funext w
    have hdiv : (w ^ 4 - 1) / 4 = ((1: ℝ) / 4) * w ^ 4 + (-((1: ℝ) / 4)) * w ^ 0 := by ring
    rw [hdiv]
  have hv0 : ((-((1: ℝ) / 16)) * 0 ^ 4 + ((1: ℝ) / 12) * 0 ^ 3 + (-((1: ℝ) / 8)) * 0 ^ 2 + ((1: ℝ) / 4) * 0 ^ 1 + (((1: ℝ) / 4) * 0 ^ 4 + (-((1: ℝ) / 4)) * 0 ^ 0) * Real.log (1 + 0)) = (0: ℝ) := by norm_num [Real.log_one]
  have hv1 : ((-((1: ℝ) / 16)) * 1 ^ 4 + ((1: ℝ) / 12) * 1 ^ 3 + (-((1: ℝ) / 8)) * 1 ^ 2 + ((1: ℝ) / 4) * 1 ^ 1 + (((1: ℝ) / 4) * 1 ^ 4 + (-((1: ℝ) / 4)) * 1 ^ 0) * Real.log (1 + 1)) = ((7: ℝ) / 48) := by norm_num [Real.log_one]
  have ha : Tendsto (fun w : ℝ => (-((1: ℝ) / 16)) * w ^ 4 + ((1: ℝ) / 12) * w ^ 3 + (-((1: ℝ) / 8)) * w ^ 2 + ((1: ℝ) / 4) * w ^ 1 + ((w ^ 4 - 1) / 4) * Real.log (1 + w)) (nhdsWithin (0: ℝ) (Set.Ioi 0)) (nhds (0: ℝ)) := by
    rw [heq]
    have hten : Tendsto (fun w : ℝ => (-((1: ℝ) / 16)) * w ^ 4 + ((1: ℝ) / 12) * w ^ 3 + (-((1: ℝ) / 8)) * w ^ 2 + ((1: ℝ) / 4) * w ^ 1 + (((1: ℝ) / 4) * w ^ 4 + (-((1: ℝ) / 4)) * w ^ 0) * Real.log (1 + w)) (nhdsWithin (0: ℝ) (Set.Ioi 0)) (nhds ((-((1: ℝ) / 16)) * 0 ^ 4 + ((1: ℝ) / 12) * 0 ^ 3 + (-((1: ℝ) / 8)) * 0 ^ 2 + ((1: ℝ) / 4) * 0 ^ 1 + (((1: ℝ) / 4) * 0 ^ 4 + (-((1: ℝ) / 4)) * 0 ^ 0) * Real.log (1 + 0))) :=
      (hPc0.add (hAc0.mul logp_contAt0)).tendsto.mono_left nhdsWithin_le_nhds
    rwa [hv0] at hten
  have hb : Tendsto (fun w : ℝ => (-((1: ℝ) / 16)) * w ^ 4 + ((1: ℝ) / 12) * w ^ 3 + (-((1: ℝ) / 8)) * w ^ 2 + ((1: ℝ) / 4) * w ^ 1 + ((w ^ 4 - 1) / 4) * Real.log (1 + w)) (nhdsWithin (1: ℝ) (Set.Iio 1)) (nhds ((7: ℝ) / 48)) := by
    rw [heq]
    have hten : Tendsto (fun w : ℝ => (-((1: ℝ) / 16)) * w ^ 4 + ((1: ℝ) / 12) * w ^ 3 + (-((1: ℝ) / 8)) * w ^ 2 + ((1: ℝ) / 4) * w ^ 1 + (((1: ℝ) / 4) * w ^ 4 + (-((1: ℝ) / 4)) * w ^ 0) * Real.log (1 + w)) (nhdsWithin (1: ℝ) (Set.Iio 1)) (nhds ((-((1: ℝ) / 16)) * 1 ^ 4 + ((1: ℝ) / 12) * 1 ^ 3 + (-((1: ℝ) / 8)) * 1 ^ 2 + ((1: ℝ) / 4) * 1 ^ 1 + (((1: ℝ) / 4) * 1 ^ 4 + (-((1: ℝ) / 4)) * 1 ^ 0) * Real.log (1 + 1))) :=
      (hPc1.add (hAc1.mul logp_contAt1)).tendsto.mono_left nhdsWithin_le_nhds
    rwa [hv1] at hten
  have h := intervalIntegral.integral_eq_sub_of_hasDerivAt_of_tendsto (a := (0: ℝ)) (b := (1: ℝ))
    (by norm_num : (0: ℝ) < (1: ℝ)) hderiv hint ha hb
  exact h.trans (by norm_num)

theorem core_lp_5 : ∫ u in (0: ℝ)..1, u ^ 5 * Real.log (1 + u) = ((37: ℝ) / 360) := by
  have hint : IntervalIntegrable (fun x : ℝ => x ^ 5 * Real.log (1 + x)) volume 0 1 := by
    refine IntervalIntegrable.congr (show Set.EqOn (fun x : ℝ => Real.log (x + 1) * x ^ 5) (fun x : ℝ => x ^ 5 * Real.log (1 + x)) (Set.uIoc (0: ℝ) 1) from fun x _ => by ring)
      (logp_int.mul_continuousOn (Continuous.continuousOn (by fun_prop : Continuous fun x : ℝ => x ^ 5)))
  have hderiv : ∀ x ∈ Set.Ioo (0: ℝ) 1, HasDerivAt
      (fun w : ℝ => (-((1: ℝ) / 36)) * w ^ 6 + ((1: ℝ) / 30) * w ^ 5 + (-((1: ℝ) / 24)) * w ^ 4 + ((1: ℝ) / 18) * w ^ 3 + (-((1: ℝ) / 12)) * w ^ 2 + ((1: ℝ) / 6) * w ^ 1 + ((w ^ 6 - 1) / 6) * Real.log (1 + w))
      (x ^ 5 * Real.log (1 + x)) x := by
    intro x hx
    have hx1 : (1: ℝ) + x ≠ 0 := by have := hx.1; linarith
    have hid : HasDerivAt (fun y : ℝ => y) 1 x := hasDerivAt_id' x
    have hinner : HasDerivAt (fun y : ℝ => 1 + y) ((0: ℝ) + 1) x := (hasDerivAt_const x 1).add hid
    have hlog : HasDerivAt (fun w : ℝ => Real.log (1 + w)) ((1: ℝ) / (1 + x)) x := by
      refine HasDerivAt.comp_of_eq x (hasDerivAt_log hx1) hinner rfl |>.congr_deriv ?_
      ring
    have hA : HasDerivAt (fun w : ℝ => (w ^ 6 - 1) / 6) (x ^ 5) x := by
      refine ((hasDerivAt_pow 6 x).sub (hasDerivAt_const x 1)).div_const 6 |>.congr_deriv ?_
      ring
    have hQ : (x: ℝ) ^ 6 - 1 = ((1 + x)) * (x ^ 5 + (-((1: ℝ) / 1)) * x ^ 4 + x ^ 3 + (-((1: ℝ) / 1)) * x ^ 2 + x ^ 1 + (-((1: ℝ) / 1))) := by ring
    have hP : HasDerivAt (fun w : ℝ => (-((1: ℝ) / 36)) * w ^ 6 + ((1: ℝ) / 30) * w ^ 5 + (-((1: ℝ) / 24)) * w ^ 4 + ((1: ℝ) / 18) * w ^ 3 + (-((1: ℝ) / 12)) * w ^ 2 + ((1: ℝ) / 6) * w ^ 1) ((-((1: ℝ) / 6)) * (x ^ 5 + (-((1: ℝ) / 1)) * x ^ 4 + x ^ 3 + (-((1: ℝ) / 1)) * x ^ 2 + x ^ 1 + (-((1: ℝ) / 1)))) x := by
      refine (((((((hasDerivAt_pow 6 x).const_mul (-((1: ℝ) / 36))).add ((hasDerivAt_pow 5 x).const_mul ((1: ℝ) / 30))).add ((hasDerivAt_pow 4 x).const_mul (-((1: ℝ) / 24)))).add ((hasDerivAt_pow 3 x).const_mul ((1: ℝ) / 18))).add ((hasDerivAt_pow 2 x).const_mul (-((1: ℝ) / 12)))).add ((hasDerivAt_pow 1 x).const_mul ((1: ℝ) / 6))) |>.congr_deriv ?_
      ring
    refine (hP.add (hA.mul hlog)).congr_deriv ?_
    field_simp [hQ]; ring
  have hPc0 : ContinuousAt (fun w : ℝ => (-((1: ℝ) / 36)) * w ^ 6 + ((1: ℝ) / 30) * w ^ 5 + (-((1: ℝ) / 24)) * w ^ 4 + ((1: ℝ) / 18) * w ^ 3 + (-((1: ℝ) / 12)) * w ^ 2 + ((1: ℝ) / 6) * w ^ 1) 0 := ((((((mono_contAt (-((1: ℝ) / 36)) 6 0).add (mono_contAt ((1: ℝ) / 30) 5 0)).add (mono_contAt (-((1: ℝ) / 24)) 4 0)).add (mono_contAt ((1: ℝ) / 18) 3 0)).add (mono_contAt (-((1: ℝ) / 12)) 2 0)).add (mono_contAt ((1: ℝ) / 6) 1 0))
  have hPc1 : ContinuousAt (fun w : ℝ => (-((1: ℝ) / 36)) * w ^ 6 + ((1: ℝ) / 30) * w ^ 5 + (-((1: ℝ) / 24)) * w ^ 4 + ((1: ℝ) / 18) * w ^ 3 + (-((1: ℝ) / 12)) * w ^ 2 + ((1: ℝ) / 6) * w ^ 1) 1 := ((((((mono_contAt (-((1: ℝ) / 36)) 6 1).add (mono_contAt ((1: ℝ) / 30) 5 1)).add (mono_contAt (-((1: ℝ) / 24)) 4 1)).add (mono_contAt ((1: ℝ) / 18) 3 1)).add (mono_contAt (-((1: ℝ) / 12)) 2 1)).add (mono_contAt ((1: ℝ) / 6) 1 1))
  have hAc0 : ContinuousAt (fun w : ℝ => ((1: ℝ) / 6) * w ^ 6 + (-((1: ℝ) / 6)) * w ^ 0) 0 := (mono_contAt ((1: ℝ) / 6) 6 0).add (mono_contAt (-((1: ℝ) / 6)) 0 0)
  have hAc1 : ContinuousAt (fun w : ℝ => ((1: ℝ) / 6) * w ^ 6 + (-((1: ℝ) / 6)) * w ^ 0) 1 := (mono_contAt ((1: ℝ) / 6) 6 1).add (mono_contAt (-((1: ℝ) / 6)) 0 1)
  have heq : (fun w : ℝ => (-((1: ℝ) / 36)) * w ^ 6 + ((1: ℝ) / 30) * w ^ 5 + (-((1: ℝ) / 24)) * w ^ 4 + ((1: ℝ) / 18) * w ^ 3 + (-((1: ℝ) / 12)) * w ^ 2 + ((1: ℝ) / 6) * w ^ 1 + ((w ^ 6 - 1) / 6) * Real.log (1 + w)) = (fun w : ℝ => (-((1: ℝ) / 36)) * w ^ 6 + ((1: ℝ) / 30) * w ^ 5 + (-((1: ℝ) / 24)) * w ^ 4 + ((1: ℝ) / 18) * w ^ 3 + (-((1: ℝ) / 12)) * w ^ 2 + ((1: ℝ) / 6) * w ^ 1 + (((1: ℝ) / 6) * w ^ 6 + (-((1: ℝ) / 6)) * w ^ 0) * Real.log (1 + w)) := by
    funext w
    have hdiv : (w ^ 6 - 1) / 6 = ((1: ℝ) / 6) * w ^ 6 + (-((1: ℝ) / 6)) * w ^ 0 := by ring
    rw [hdiv]
  have hv0 : ((-((1: ℝ) / 36)) * 0 ^ 6 + ((1: ℝ) / 30) * 0 ^ 5 + (-((1: ℝ) / 24)) * 0 ^ 4 + ((1: ℝ) / 18) * 0 ^ 3 + (-((1: ℝ) / 12)) * 0 ^ 2 + ((1: ℝ) / 6) * 0 ^ 1 + (((1: ℝ) / 6) * 0 ^ 6 + (-((1: ℝ) / 6)) * 0 ^ 0) * Real.log (1 + 0)) = (0: ℝ) := by norm_num [Real.log_one]
  have hv1 : ((-((1: ℝ) / 36)) * 1 ^ 6 + ((1: ℝ) / 30) * 1 ^ 5 + (-((1: ℝ) / 24)) * 1 ^ 4 + ((1: ℝ) / 18) * 1 ^ 3 + (-((1: ℝ) / 12)) * 1 ^ 2 + ((1: ℝ) / 6) * 1 ^ 1 + (((1: ℝ) / 6) * 1 ^ 6 + (-((1: ℝ) / 6)) * 1 ^ 0) * Real.log (1 + 1)) = ((37: ℝ) / 360) := by norm_num [Real.log_one]
  have ha : Tendsto (fun w : ℝ => (-((1: ℝ) / 36)) * w ^ 6 + ((1: ℝ) / 30) * w ^ 5 + (-((1: ℝ) / 24)) * w ^ 4 + ((1: ℝ) / 18) * w ^ 3 + (-((1: ℝ) / 12)) * w ^ 2 + ((1: ℝ) / 6) * w ^ 1 + ((w ^ 6 - 1) / 6) * Real.log (1 + w)) (nhdsWithin (0: ℝ) (Set.Ioi 0)) (nhds (0: ℝ)) := by
    rw [heq]
    have hten : Tendsto (fun w : ℝ => (-((1: ℝ) / 36)) * w ^ 6 + ((1: ℝ) / 30) * w ^ 5 + (-((1: ℝ) / 24)) * w ^ 4 + ((1: ℝ) / 18) * w ^ 3 + (-((1: ℝ) / 12)) * w ^ 2 + ((1: ℝ) / 6) * w ^ 1 + (((1: ℝ) / 6) * w ^ 6 + (-((1: ℝ) / 6)) * w ^ 0) * Real.log (1 + w)) (nhdsWithin (0: ℝ) (Set.Ioi 0)) (nhds ((-((1: ℝ) / 36)) * 0 ^ 6 + ((1: ℝ) / 30) * 0 ^ 5 + (-((1: ℝ) / 24)) * 0 ^ 4 + ((1: ℝ) / 18) * 0 ^ 3 + (-((1: ℝ) / 12)) * 0 ^ 2 + ((1: ℝ) / 6) * 0 ^ 1 + (((1: ℝ) / 6) * 0 ^ 6 + (-((1: ℝ) / 6)) * 0 ^ 0) * Real.log (1 + 0))) :=
      (hPc0.add (hAc0.mul logp_contAt0)).tendsto.mono_left nhdsWithin_le_nhds
    rwa [hv0] at hten
  have hb : Tendsto (fun w : ℝ => (-((1: ℝ) / 36)) * w ^ 6 + ((1: ℝ) / 30) * w ^ 5 + (-((1: ℝ) / 24)) * w ^ 4 + ((1: ℝ) / 18) * w ^ 3 + (-((1: ℝ) / 12)) * w ^ 2 + ((1: ℝ) / 6) * w ^ 1 + ((w ^ 6 - 1) / 6) * Real.log (1 + w)) (nhdsWithin (1: ℝ) (Set.Iio 1)) (nhds ((37: ℝ) / 360)) := by
    rw [heq]
    have hten : Tendsto (fun w : ℝ => (-((1: ℝ) / 36)) * w ^ 6 + ((1: ℝ) / 30) * w ^ 5 + (-((1: ℝ) / 24)) * w ^ 4 + ((1: ℝ) / 18) * w ^ 3 + (-((1: ℝ) / 12)) * w ^ 2 + ((1: ℝ) / 6) * w ^ 1 + (((1: ℝ) / 6) * w ^ 6 + (-((1: ℝ) / 6)) * w ^ 0) * Real.log (1 + w)) (nhdsWithin (1: ℝ) (Set.Iio 1)) (nhds ((-((1: ℝ) / 36)) * 1 ^ 6 + ((1: ℝ) / 30) * 1 ^ 5 + (-((1: ℝ) / 24)) * 1 ^ 4 + ((1: ℝ) / 18) * 1 ^ 3 + (-((1: ℝ) / 12)) * 1 ^ 2 + ((1: ℝ) / 6) * 1 ^ 1 + (((1: ℝ) / 6) * 1 ^ 6 + (-((1: ℝ) / 6)) * 1 ^ 0) * Real.log (1 + 1))) :=
      (hPc1.add (hAc1.mul logp_contAt1)).tendsto.mono_left nhdsWithin_le_nhds
    rwa [hv1] at hten
  have h := intervalIntegral.integral_eq_sub_of_hasDerivAt_of_tendsto (a := (0: ℝ)) (b := (1: ℝ))
    (by norm_num : (0: ℝ) < (1: ℝ)) hderiv hint ha hb
  exact h.trans (by norm_num)

theorem core_lp_7 : ∫ u in (0: ℝ)..1, u ^ 7 * Real.log (1 + u) = ((533: ℝ) / 6720) := by
  have hint : IntervalIntegrable (fun x : ℝ => x ^ 7 * Real.log (1 + x)) volume 0 1 := by
    refine IntervalIntegrable.congr (show Set.EqOn (fun x : ℝ => Real.log (x + 1) * x ^ 7) (fun x : ℝ => x ^ 7 * Real.log (1 + x)) (Set.uIoc (0: ℝ) 1) from fun x _ => by ring)
      (logp_int.mul_continuousOn (Continuous.continuousOn (by fun_prop : Continuous fun x : ℝ => x ^ 7)))
  have hderiv : ∀ x ∈ Set.Ioo (0: ℝ) 1, HasDerivAt
      (fun w : ℝ => (-((1: ℝ) / 64)) * w ^ 8 + ((1: ℝ) / 56) * w ^ 7 + (-((1: ℝ) / 48)) * w ^ 6 + ((1: ℝ) / 40) * w ^ 5 + (-((1: ℝ) / 32)) * w ^ 4 + ((1: ℝ) / 24) * w ^ 3 + (-((1: ℝ) / 16)) * w ^ 2 + ((1: ℝ) / 8) * w ^ 1 + ((w ^ 8 - 1) / 8) * Real.log (1 + w))
      (x ^ 7 * Real.log (1 + x)) x := by
    intro x hx
    have hx1 : (1: ℝ) + x ≠ 0 := by have := hx.1; linarith
    have hid : HasDerivAt (fun y : ℝ => y) 1 x := hasDerivAt_id' x
    have hinner : HasDerivAt (fun y : ℝ => 1 + y) ((0: ℝ) + 1) x := (hasDerivAt_const x 1).add hid
    have hlog : HasDerivAt (fun w : ℝ => Real.log (1 + w)) ((1: ℝ) / (1 + x)) x := by
      refine HasDerivAt.comp_of_eq x (hasDerivAt_log hx1) hinner rfl |>.congr_deriv ?_
      ring
    have hA : HasDerivAt (fun w : ℝ => (w ^ 8 - 1) / 8) (x ^ 7) x := by
      refine ((hasDerivAt_pow 8 x).sub (hasDerivAt_const x 1)).div_const 8 |>.congr_deriv ?_
      ring
    have hQ : (x: ℝ) ^ 8 - 1 = ((1 + x)) * (x ^ 7 + (-((1: ℝ) / 1)) * x ^ 6 + x ^ 5 + (-((1: ℝ) / 1)) * x ^ 4 + x ^ 3 + (-((1: ℝ) / 1)) * x ^ 2 + x ^ 1 + (-((1: ℝ) / 1))) := by ring
    have hP : HasDerivAt (fun w : ℝ => (-((1: ℝ) / 64)) * w ^ 8 + ((1: ℝ) / 56) * w ^ 7 + (-((1: ℝ) / 48)) * w ^ 6 + ((1: ℝ) / 40) * w ^ 5 + (-((1: ℝ) / 32)) * w ^ 4 + ((1: ℝ) / 24) * w ^ 3 + (-((1: ℝ) / 16)) * w ^ 2 + ((1: ℝ) / 8) * w ^ 1) ((-((1: ℝ) / 8)) * (x ^ 7 + (-((1: ℝ) / 1)) * x ^ 6 + x ^ 5 + (-((1: ℝ) / 1)) * x ^ 4 + x ^ 3 + (-((1: ℝ) / 1)) * x ^ 2 + x ^ 1 + (-((1: ℝ) / 1)))) x := by
      refine (((((((((hasDerivAt_pow 8 x).const_mul (-((1: ℝ) / 64))).add ((hasDerivAt_pow 7 x).const_mul ((1: ℝ) / 56))).add ((hasDerivAt_pow 6 x).const_mul (-((1: ℝ) / 48)))).add ((hasDerivAt_pow 5 x).const_mul ((1: ℝ) / 40))).add ((hasDerivAt_pow 4 x).const_mul (-((1: ℝ) / 32)))).add ((hasDerivAt_pow 3 x).const_mul ((1: ℝ) / 24))).add ((hasDerivAt_pow 2 x).const_mul (-((1: ℝ) / 16)))).add ((hasDerivAt_pow 1 x).const_mul ((1: ℝ) / 8))) |>.congr_deriv ?_
      ring
    refine (hP.add (hA.mul hlog)).congr_deriv ?_
    field_simp [hQ]; ring
  have hPc0 : ContinuousAt (fun w : ℝ => (-((1: ℝ) / 64)) * w ^ 8 + ((1: ℝ) / 56) * w ^ 7 + (-((1: ℝ) / 48)) * w ^ 6 + ((1: ℝ) / 40) * w ^ 5 + (-((1: ℝ) / 32)) * w ^ 4 + ((1: ℝ) / 24) * w ^ 3 + (-((1: ℝ) / 16)) * w ^ 2 + ((1: ℝ) / 8) * w ^ 1) 0 := ((((((((mono_contAt (-((1: ℝ) / 64)) 8 0).add (mono_contAt ((1: ℝ) / 56) 7 0)).add (mono_contAt (-((1: ℝ) / 48)) 6 0)).add (mono_contAt ((1: ℝ) / 40) 5 0)).add (mono_contAt (-((1: ℝ) / 32)) 4 0)).add (mono_contAt ((1: ℝ) / 24) 3 0)).add (mono_contAt (-((1: ℝ) / 16)) 2 0)).add (mono_contAt ((1: ℝ) / 8) 1 0))
  have hPc1 : ContinuousAt (fun w : ℝ => (-((1: ℝ) / 64)) * w ^ 8 + ((1: ℝ) / 56) * w ^ 7 + (-((1: ℝ) / 48)) * w ^ 6 + ((1: ℝ) / 40) * w ^ 5 + (-((1: ℝ) / 32)) * w ^ 4 + ((1: ℝ) / 24) * w ^ 3 + (-((1: ℝ) / 16)) * w ^ 2 + ((1: ℝ) / 8) * w ^ 1) 1 := ((((((((mono_contAt (-((1: ℝ) / 64)) 8 1).add (mono_contAt ((1: ℝ) / 56) 7 1)).add (mono_contAt (-((1: ℝ) / 48)) 6 1)).add (mono_contAt ((1: ℝ) / 40) 5 1)).add (mono_contAt (-((1: ℝ) / 32)) 4 1)).add (mono_contAt ((1: ℝ) / 24) 3 1)).add (mono_contAt (-((1: ℝ) / 16)) 2 1)).add (mono_contAt ((1: ℝ) / 8) 1 1))
  have hAc0 : ContinuousAt (fun w : ℝ => ((1: ℝ) / 8) * w ^ 8 + (-((1: ℝ) / 8)) * w ^ 0) 0 := (mono_contAt ((1: ℝ) / 8) 8 0).add (mono_contAt (-((1: ℝ) / 8)) 0 0)
  have hAc1 : ContinuousAt (fun w : ℝ => ((1: ℝ) / 8) * w ^ 8 + (-((1: ℝ) / 8)) * w ^ 0) 1 := (mono_contAt ((1: ℝ) / 8) 8 1).add (mono_contAt (-((1: ℝ) / 8)) 0 1)
  have heq : (fun w : ℝ => (-((1: ℝ) / 64)) * w ^ 8 + ((1: ℝ) / 56) * w ^ 7 + (-((1: ℝ) / 48)) * w ^ 6 + ((1: ℝ) / 40) * w ^ 5 + (-((1: ℝ) / 32)) * w ^ 4 + ((1: ℝ) / 24) * w ^ 3 + (-((1: ℝ) / 16)) * w ^ 2 + ((1: ℝ) / 8) * w ^ 1 + ((w ^ 8 - 1) / 8) * Real.log (1 + w)) = (fun w : ℝ => (-((1: ℝ) / 64)) * w ^ 8 + ((1: ℝ) / 56) * w ^ 7 + (-((1: ℝ) / 48)) * w ^ 6 + ((1: ℝ) / 40) * w ^ 5 + (-((1: ℝ) / 32)) * w ^ 4 + ((1: ℝ) / 24) * w ^ 3 + (-((1: ℝ) / 16)) * w ^ 2 + ((1: ℝ) / 8) * w ^ 1 + (((1: ℝ) / 8) * w ^ 8 + (-((1: ℝ) / 8)) * w ^ 0) * Real.log (1 + w)) := by
    funext w
    have hdiv : (w ^ 8 - 1) / 8 = ((1: ℝ) / 8) * w ^ 8 + (-((1: ℝ) / 8)) * w ^ 0 := by ring
    rw [hdiv]
  have hv0 : ((-((1: ℝ) / 64)) * 0 ^ 8 + ((1: ℝ) / 56) * 0 ^ 7 + (-((1: ℝ) / 48)) * 0 ^ 6 + ((1: ℝ) / 40) * 0 ^ 5 + (-((1: ℝ) / 32)) * 0 ^ 4 + ((1: ℝ) / 24) * 0 ^ 3 + (-((1: ℝ) / 16)) * 0 ^ 2 + ((1: ℝ) / 8) * 0 ^ 1 + (((1: ℝ) / 8) * 0 ^ 8 + (-((1: ℝ) / 8)) * 0 ^ 0) * Real.log (1 + 0)) = (0: ℝ) := by norm_num [Real.log_one]
  have hv1 : ((-((1: ℝ) / 64)) * 1 ^ 8 + ((1: ℝ) / 56) * 1 ^ 7 + (-((1: ℝ) / 48)) * 1 ^ 6 + ((1: ℝ) / 40) * 1 ^ 5 + (-((1: ℝ) / 32)) * 1 ^ 4 + ((1: ℝ) / 24) * 1 ^ 3 + (-((1: ℝ) / 16)) * 1 ^ 2 + ((1: ℝ) / 8) * 1 ^ 1 + (((1: ℝ) / 8) * 1 ^ 8 + (-((1: ℝ) / 8)) * 1 ^ 0) * Real.log (1 + 1)) = ((533: ℝ) / 6720) := by norm_num [Real.log_one]
  have ha : Tendsto (fun w : ℝ => (-((1: ℝ) / 64)) * w ^ 8 + ((1: ℝ) / 56) * w ^ 7 + (-((1: ℝ) / 48)) * w ^ 6 + ((1: ℝ) / 40) * w ^ 5 + (-((1: ℝ) / 32)) * w ^ 4 + ((1: ℝ) / 24) * w ^ 3 + (-((1: ℝ) / 16)) * w ^ 2 + ((1: ℝ) / 8) * w ^ 1 + ((w ^ 8 - 1) / 8) * Real.log (1 + w)) (nhdsWithin (0: ℝ) (Set.Ioi 0)) (nhds (0: ℝ)) := by
    rw [heq]
    have hten : Tendsto (fun w : ℝ => (-((1: ℝ) / 64)) * w ^ 8 + ((1: ℝ) / 56) * w ^ 7 + (-((1: ℝ) / 48)) * w ^ 6 + ((1: ℝ) / 40) * w ^ 5 + (-((1: ℝ) / 32)) * w ^ 4 + ((1: ℝ) / 24) * w ^ 3 + (-((1: ℝ) / 16)) * w ^ 2 + ((1: ℝ) / 8) * w ^ 1 + (((1: ℝ) / 8) * w ^ 8 + (-((1: ℝ) / 8)) * w ^ 0) * Real.log (1 + w)) (nhdsWithin (0: ℝ) (Set.Ioi 0)) (nhds ((-((1: ℝ) / 64)) * 0 ^ 8 + ((1: ℝ) / 56) * 0 ^ 7 + (-((1: ℝ) / 48)) * 0 ^ 6 + ((1: ℝ) / 40) * 0 ^ 5 + (-((1: ℝ) / 32)) * 0 ^ 4 + ((1: ℝ) / 24) * 0 ^ 3 + (-((1: ℝ) / 16)) * 0 ^ 2 + ((1: ℝ) / 8) * 0 ^ 1 + (((1: ℝ) / 8) * 0 ^ 8 + (-((1: ℝ) / 8)) * 0 ^ 0) * Real.log (1 + 0))) :=
      (hPc0.add (hAc0.mul logp_contAt0)).tendsto.mono_left nhdsWithin_le_nhds
    rwa [hv0] at hten
  have hb : Tendsto (fun w : ℝ => (-((1: ℝ) / 64)) * w ^ 8 + ((1: ℝ) / 56) * w ^ 7 + (-((1: ℝ) / 48)) * w ^ 6 + ((1: ℝ) / 40) * w ^ 5 + (-((1: ℝ) / 32)) * w ^ 4 + ((1: ℝ) / 24) * w ^ 3 + (-((1: ℝ) / 16)) * w ^ 2 + ((1: ℝ) / 8) * w ^ 1 + ((w ^ 8 - 1) / 8) * Real.log (1 + w)) (nhdsWithin (1: ℝ) (Set.Iio 1)) (nhds ((533: ℝ) / 6720)) := by
    rw [heq]
    have hten : Tendsto (fun w : ℝ => (-((1: ℝ) / 64)) * w ^ 8 + ((1: ℝ) / 56) * w ^ 7 + (-((1: ℝ) / 48)) * w ^ 6 + ((1: ℝ) / 40) * w ^ 5 + (-((1: ℝ) / 32)) * w ^ 4 + ((1: ℝ) / 24) * w ^ 3 + (-((1: ℝ) / 16)) * w ^ 2 + ((1: ℝ) / 8) * w ^ 1 + (((1: ℝ) / 8) * w ^ 8 + (-((1: ℝ) / 8)) * w ^ 0) * Real.log (1 + w)) (nhdsWithin (1: ℝ) (Set.Iio 1)) (nhds ((-((1: ℝ) / 64)) * 1 ^ 8 + ((1: ℝ) / 56) * 1 ^ 7 + (-((1: ℝ) / 48)) * 1 ^ 6 + ((1: ℝ) / 40) * 1 ^ 5 + (-((1: ℝ) / 32)) * 1 ^ 4 + ((1: ℝ) / 24) * 1 ^ 3 + (-((1: ℝ) / 16)) * 1 ^ 2 + ((1: ℝ) / 8) * 1 ^ 1 + (((1: ℝ) / 8) * 1 ^ 8 + (-((1: ℝ) / 8)) * 1 ^ 0) * Real.log (1 + 1))) :=
      (hPc1.add (hAc1.mul logp_contAt1)).tendsto.mono_left nhdsWithin_le_nhds
    rwa [hv1] at hten
  have h := intervalIntegral.integral_eq_sub_of_hasDerivAt_of_tendsto (a := (0: ℝ)) (b := (1: ℝ))
    (by norm_num : (0: ℝ) < (1: ℝ)) hderiv hint ha hb
  exact h.trans (by norm_num)

theorem core_lp_9 : ∫ u in (0: ℝ)..1, u ^ 9 * Real.log (1 + u) = ((1627: ℝ) / 25200) := by
  have hint : IntervalIntegrable (fun x : ℝ => x ^ 9 * Real.log (1 + x)) volume 0 1 := by
    refine IntervalIntegrable.congr (show Set.EqOn (fun x : ℝ => Real.log (x + 1) * x ^ 9) (fun x : ℝ => x ^ 9 * Real.log (1 + x)) (Set.uIoc (0: ℝ) 1) from fun x _ => by ring)
      (logp_int.mul_continuousOn (Continuous.continuousOn (by fun_prop : Continuous fun x : ℝ => x ^ 9)))
  have hderiv : ∀ x ∈ Set.Ioo (0: ℝ) 1, HasDerivAt
      (fun w : ℝ => (-((1: ℝ) / 100)) * w ^ 10 + ((1: ℝ) / 90) * w ^ 9 + (-((1: ℝ) / 80)) * w ^ 8 + ((1: ℝ) / 70) * w ^ 7 + (-((1: ℝ) / 60)) * w ^ 6 + ((1: ℝ) / 50) * w ^ 5 + (-((1: ℝ) / 40)) * w ^ 4 + ((1: ℝ) / 30) * w ^ 3 + (-((1: ℝ) / 20)) * w ^ 2 + ((1: ℝ) / 10) * w ^ 1 + ((w ^ 10 - 1) / 10) * Real.log (1 + w))
      (x ^ 9 * Real.log (1 + x)) x := by
    intro x hx
    have hx1 : (1: ℝ) + x ≠ 0 := by have := hx.1; linarith
    have hid : HasDerivAt (fun y : ℝ => y) 1 x := hasDerivAt_id' x
    have hinner : HasDerivAt (fun y : ℝ => 1 + y) ((0: ℝ) + 1) x := (hasDerivAt_const x 1).add hid
    have hlog : HasDerivAt (fun w : ℝ => Real.log (1 + w)) ((1: ℝ) / (1 + x)) x := by
      refine HasDerivAt.comp_of_eq x (hasDerivAt_log hx1) hinner rfl |>.congr_deriv ?_
      ring
    have hA : HasDerivAt (fun w : ℝ => (w ^ 10 - 1) / 10) (x ^ 9) x := by
      refine ((hasDerivAt_pow 10 x).sub (hasDerivAt_const x 1)).div_const 10 |>.congr_deriv ?_
      ring
    have hQ : (x: ℝ) ^ 10 - 1 = ((1 + x)) * (x ^ 9 + (-((1: ℝ) / 1)) * x ^ 8 + x ^ 7 + (-((1: ℝ) / 1)) * x ^ 6 + x ^ 5 + (-((1: ℝ) / 1)) * x ^ 4 + x ^ 3 + (-((1: ℝ) / 1)) * x ^ 2 + x ^ 1 + (-((1: ℝ) / 1))) := by ring
    have hP : HasDerivAt (fun w : ℝ => (-((1: ℝ) / 100)) * w ^ 10 + ((1: ℝ) / 90) * w ^ 9 + (-((1: ℝ) / 80)) * w ^ 8 + ((1: ℝ) / 70) * w ^ 7 + (-((1: ℝ) / 60)) * w ^ 6 + ((1: ℝ) / 50) * w ^ 5 + (-((1: ℝ) / 40)) * w ^ 4 + ((1: ℝ) / 30) * w ^ 3 + (-((1: ℝ) / 20)) * w ^ 2 + ((1: ℝ) / 10) * w ^ 1) ((-((1: ℝ) / 10)) * (x ^ 9 + (-((1: ℝ) / 1)) * x ^ 8 + x ^ 7 + (-((1: ℝ) / 1)) * x ^ 6 + x ^ 5 + (-((1: ℝ) / 1)) * x ^ 4 + x ^ 3 + (-((1: ℝ) / 1)) * x ^ 2 + x ^ 1 + (-((1: ℝ) / 1)))) x := by
      refine (((((((((((hasDerivAt_pow 10 x).const_mul (-((1: ℝ) / 100))).add ((hasDerivAt_pow 9 x).const_mul ((1: ℝ) / 90))).add ((hasDerivAt_pow 8 x).const_mul (-((1: ℝ) / 80)))).add ((hasDerivAt_pow 7 x).const_mul ((1: ℝ) / 70))).add ((hasDerivAt_pow 6 x).const_mul (-((1: ℝ) / 60)))).add ((hasDerivAt_pow 5 x).const_mul ((1: ℝ) / 50))).add ((hasDerivAt_pow 4 x).const_mul (-((1: ℝ) / 40)))).add ((hasDerivAt_pow 3 x).const_mul ((1: ℝ) / 30))).add ((hasDerivAt_pow 2 x).const_mul (-((1: ℝ) / 20)))).add ((hasDerivAt_pow 1 x).const_mul ((1: ℝ) / 10))) |>.congr_deriv ?_
      ring
    refine (hP.add (hA.mul hlog)).congr_deriv ?_
    field_simp [hQ]; ring
  have hPc0 : ContinuousAt (fun w : ℝ => (-((1: ℝ) / 100)) * w ^ 10 + ((1: ℝ) / 90) * w ^ 9 + (-((1: ℝ) / 80)) * w ^ 8 + ((1: ℝ) / 70) * w ^ 7 + (-((1: ℝ) / 60)) * w ^ 6 + ((1: ℝ) / 50) * w ^ 5 + (-((1: ℝ) / 40)) * w ^ 4 + ((1: ℝ) / 30) * w ^ 3 + (-((1: ℝ) / 20)) * w ^ 2 + ((1: ℝ) / 10) * w ^ 1) 0 := ((((((((((mono_contAt (-((1: ℝ) / 100)) 10 0).add (mono_contAt ((1: ℝ) / 90) 9 0)).add (mono_contAt (-((1: ℝ) / 80)) 8 0)).add (mono_contAt ((1: ℝ) / 70) 7 0)).add (mono_contAt (-((1: ℝ) / 60)) 6 0)).add (mono_contAt ((1: ℝ) / 50) 5 0)).add (mono_contAt (-((1: ℝ) / 40)) 4 0)).add (mono_contAt ((1: ℝ) / 30) 3 0)).add (mono_contAt (-((1: ℝ) / 20)) 2 0)).add (mono_contAt ((1: ℝ) / 10) 1 0))
  have hPc1 : ContinuousAt (fun w : ℝ => (-((1: ℝ) / 100)) * w ^ 10 + ((1: ℝ) / 90) * w ^ 9 + (-((1: ℝ) / 80)) * w ^ 8 + ((1: ℝ) / 70) * w ^ 7 + (-((1: ℝ) / 60)) * w ^ 6 + ((1: ℝ) / 50) * w ^ 5 + (-((1: ℝ) / 40)) * w ^ 4 + ((1: ℝ) / 30) * w ^ 3 + (-((1: ℝ) / 20)) * w ^ 2 + ((1: ℝ) / 10) * w ^ 1) 1 := ((((((((((mono_contAt (-((1: ℝ) / 100)) 10 1).add (mono_contAt ((1: ℝ) / 90) 9 1)).add (mono_contAt (-((1: ℝ) / 80)) 8 1)).add (mono_contAt ((1: ℝ) / 70) 7 1)).add (mono_contAt (-((1: ℝ) / 60)) 6 1)).add (mono_contAt ((1: ℝ) / 50) 5 1)).add (mono_contAt (-((1: ℝ) / 40)) 4 1)).add (mono_contAt ((1: ℝ) / 30) 3 1)).add (mono_contAt (-((1: ℝ) / 20)) 2 1)).add (mono_contAt ((1: ℝ) / 10) 1 1))
  have hAc0 : ContinuousAt (fun w : ℝ => ((1: ℝ) / 10) * w ^ 10 + (-((1: ℝ) / 10)) * w ^ 0) 0 := (mono_contAt ((1: ℝ) / 10) 10 0).add (mono_contAt (-((1: ℝ) / 10)) 0 0)
  have hAc1 : ContinuousAt (fun w : ℝ => ((1: ℝ) / 10) * w ^ 10 + (-((1: ℝ) / 10)) * w ^ 0) 1 := (mono_contAt ((1: ℝ) / 10) 10 1).add (mono_contAt (-((1: ℝ) / 10)) 0 1)
  have heq : (fun w : ℝ => (-((1: ℝ) / 100)) * w ^ 10 + ((1: ℝ) / 90) * w ^ 9 + (-((1: ℝ) / 80)) * w ^ 8 + ((1: ℝ) / 70) * w ^ 7 + (-((1: ℝ) / 60)) * w ^ 6 + ((1: ℝ) / 50) * w ^ 5 + (-((1: ℝ) / 40)) * w ^ 4 + ((1: ℝ) / 30) * w ^ 3 + (-((1: ℝ) / 20)) * w ^ 2 + ((1: ℝ) / 10) * w ^ 1 + ((w ^ 10 - 1) / 10) * Real.log (1 + w)) = (fun w : ℝ => (-((1: ℝ) / 100)) * w ^ 10 + ((1: ℝ) / 90) * w ^ 9 + (-((1: ℝ) / 80)) * w ^ 8 + ((1: ℝ) / 70) * w ^ 7 + (-((1: ℝ) / 60)) * w ^ 6 + ((1: ℝ) / 50) * w ^ 5 + (-((1: ℝ) / 40)) * w ^ 4 + ((1: ℝ) / 30) * w ^ 3 + (-((1: ℝ) / 20)) * w ^ 2 + ((1: ℝ) / 10) * w ^ 1 + (((1: ℝ) / 10) * w ^ 10 + (-((1: ℝ) / 10)) * w ^ 0) * Real.log (1 + w)) := by
    funext w
    have hdiv : (w ^ 10 - 1) / 10 = ((1: ℝ) / 10) * w ^ 10 + (-((1: ℝ) / 10)) * w ^ 0 := by ring
    rw [hdiv]
  have hv0 : ((-((1: ℝ) / 100)) * 0 ^ 10 + ((1: ℝ) / 90) * 0 ^ 9 + (-((1: ℝ) / 80)) * 0 ^ 8 + ((1: ℝ) / 70) * 0 ^ 7 + (-((1: ℝ) / 60)) * 0 ^ 6 + ((1: ℝ) / 50) * 0 ^ 5 + (-((1: ℝ) / 40)) * 0 ^ 4 + ((1: ℝ) / 30) * 0 ^ 3 + (-((1: ℝ) / 20)) * 0 ^ 2 + ((1: ℝ) / 10) * 0 ^ 1 + (((1: ℝ) / 10) * 0 ^ 10 + (-((1: ℝ) / 10)) * 0 ^ 0) * Real.log (1 + 0)) = (0: ℝ) := by norm_num [Real.log_one]
  have hv1 : ((-((1: ℝ) / 100)) * 1 ^ 10 + ((1: ℝ) / 90) * 1 ^ 9 + (-((1: ℝ) / 80)) * 1 ^ 8 + ((1: ℝ) / 70) * 1 ^ 7 + (-((1: ℝ) / 60)) * 1 ^ 6 + ((1: ℝ) / 50) * 1 ^ 5 + (-((1: ℝ) / 40)) * 1 ^ 4 + ((1: ℝ) / 30) * 1 ^ 3 + (-((1: ℝ) / 20)) * 1 ^ 2 + ((1: ℝ) / 10) * 1 ^ 1 + (((1: ℝ) / 10) * 1 ^ 10 + (-((1: ℝ) / 10)) * 1 ^ 0) * Real.log (1 + 1)) = ((1627: ℝ) / 25200) := by norm_num [Real.log_one]
  have ha : Tendsto (fun w : ℝ => (-((1: ℝ) / 100)) * w ^ 10 + ((1: ℝ) / 90) * w ^ 9 + (-((1: ℝ) / 80)) * w ^ 8 + ((1: ℝ) / 70) * w ^ 7 + (-((1: ℝ) / 60)) * w ^ 6 + ((1: ℝ) / 50) * w ^ 5 + (-((1: ℝ) / 40)) * w ^ 4 + ((1: ℝ) / 30) * w ^ 3 + (-((1: ℝ) / 20)) * w ^ 2 + ((1: ℝ) / 10) * w ^ 1 + ((w ^ 10 - 1) / 10) * Real.log (1 + w)) (nhdsWithin (0: ℝ) (Set.Ioi 0)) (nhds (0: ℝ)) := by
    rw [heq]
    have hten : Tendsto (fun w : ℝ => (-((1: ℝ) / 100)) * w ^ 10 + ((1: ℝ) / 90) * w ^ 9 + (-((1: ℝ) / 80)) * w ^ 8 + ((1: ℝ) / 70) * w ^ 7 + (-((1: ℝ) / 60)) * w ^ 6 + ((1: ℝ) / 50) * w ^ 5 + (-((1: ℝ) / 40)) * w ^ 4 + ((1: ℝ) / 30) * w ^ 3 + (-((1: ℝ) / 20)) * w ^ 2 + ((1: ℝ) / 10) * w ^ 1 + (((1: ℝ) / 10) * w ^ 10 + (-((1: ℝ) / 10)) * w ^ 0) * Real.log (1 + w)) (nhdsWithin (0: ℝ) (Set.Ioi 0)) (nhds ((-((1: ℝ) / 100)) * 0 ^ 10 + ((1: ℝ) / 90) * 0 ^ 9 + (-((1: ℝ) / 80)) * 0 ^ 8 + ((1: ℝ) / 70) * 0 ^ 7 + (-((1: ℝ) / 60)) * 0 ^ 6 + ((1: ℝ) / 50) * 0 ^ 5 + (-((1: ℝ) / 40)) * 0 ^ 4 + ((1: ℝ) / 30) * 0 ^ 3 + (-((1: ℝ) / 20)) * 0 ^ 2 + ((1: ℝ) / 10) * 0 ^ 1 + (((1: ℝ) / 10) * 0 ^ 10 + (-((1: ℝ) / 10)) * 0 ^ 0) * Real.log (1 + 0))) :=
      (hPc0.add (hAc0.mul logp_contAt0)).tendsto.mono_left nhdsWithin_le_nhds
    rwa [hv0] at hten
  have hb : Tendsto (fun w : ℝ => (-((1: ℝ) / 100)) * w ^ 10 + ((1: ℝ) / 90) * w ^ 9 + (-((1: ℝ) / 80)) * w ^ 8 + ((1: ℝ) / 70) * w ^ 7 + (-((1: ℝ) / 60)) * w ^ 6 + ((1: ℝ) / 50) * w ^ 5 + (-((1: ℝ) / 40)) * w ^ 4 + ((1: ℝ) / 30) * w ^ 3 + (-((1: ℝ) / 20)) * w ^ 2 + ((1: ℝ) / 10) * w ^ 1 + ((w ^ 10 - 1) / 10) * Real.log (1 + w)) (nhdsWithin (1: ℝ) (Set.Iio 1)) (nhds ((1627: ℝ) / 25200)) := by
    rw [heq]
    have hten : Tendsto (fun w : ℝ => (-((1: ℝ) / 100)) * w ^ 10 + ((1: ℝ) / 90) * w ^ 9 + (-((1: ℝ) / 80)) * w ^ 8 + ((1: ℝ) / 70) * w ^ 7 + (-((1: ℝ) / 60)) * w ^ 6 + ((1: ℝ) / 50) * w ^ 5 + (-((1: ℝ) / 40)) * w ^ 4 + ((1: ℝ) / 30) * w ^ 3 + (-((1: ℝ) / 20)) * w ^ 2 + ((1: ℝ) / 10) * w ^ 1 + (((1: ℝ) / 10) * w ^ 10 + (-((1: ℝ) / 10)) * w ^ 0) * Real.log (1 + w)) (nhdsWithin (1: ℝ) (Set.Iio 1)) (nhds ((-((1: ℝ) / 100)) * 1 ^ 10 + ((1: ℝ) / 90) * 1 ^ 9 + (-((1: ℝ) / 80)) * 1 ^ 8 + ((1: ℝ) / 70) * 1 ^ 7 + (-((1: ℝ) / 60)) * 1 ^ 6 + ((1: ℝ) / 50) * 1 ^ 5 + (-((1: ℝ) / 40)) * 1 ^ 4 + ((1: ℝ) / 30) * 1 ^ 3 + (-((1: ℝ) / 20)) * 1 ^ 2 + ((1: ℝ) / 10) * 1 ^ 1 + (((1: ℝ) / 10) * 1 ^ 10 + (-((1: ℝ) / 10)) * 1 ^ 0) * Real.log (1 + 1))) :=
      (hPc1.add (hAc1.mul logp_contAt1)).tendsto.mono_left nhdsWithin_le_nhds
    rwa [hv1] at hten
  have h := intervalIntegral.integral_eq_sub_of_hasDerivAt_of_tendsto (a := (0: ℝ)) (b := (1: ℝ))
    (by norm_num : (0: ℝ) < (1: ℝ)) hderiv hint ha hb
  exact h.trans (by norm_num)

theorem term_a0 : ∫ u in (0: ℝ)..1, (-((21: ℝ) / 40)) * u ^ 4 = (-((21: ℝ) / 200)) := by
  rw [intervalIntegral.integral_const_mul, poly_core_4]
  norm_num

theorem term_a1 : ∫ u in (0: ℝ)..1, ((63: ℝ) / 40) * u ^ 2 = ((21: ℝ) / 40) := by
  rw [intervalIntegral.integral_const_mul, poly_core_2]
  norm_num

theorem term_a2 : ∫ u in (0: ℝ)..1, (-((57: ℝ) / 80)) * (u ^ 1 * Real.log (1 - u)) = ((171: ℝ) / 320) := by
  rw [intervalIntegral.integral_const_mul, core_lm_1]
  norm_num

theorem term_a3 : ∫ u in (0: ℝ)..1, (-((39: ℝ) / 40)) * (u ^ 3 * Real.log (1 + u)) = (-((91: ℝ) / 640)) := by
  rw [intervalIntegral.integral_const_mul, core_lp_3]
  norm_num

theorem term_a4 : ∫ u in (0: ℝ)..1, (-((21: ℝ) / 80)) * (u ^ 5 * Real.log (1 - u)) = ((343: ℝ) / 3200) := by
  rw [intervalIntegral.integral_const_mul, core_lm_5]
  norm_num

theorem term_a5 : ∫ u in (0: ℝ)..1, ((21: ℝ) / 80) * (u ^ 5 * Real.log (1 + u)) = ((259: ℝ) / 9600) := by
  rw [intervalIntegral.integral_const_mul, core_lp_5]
  norm_num

theorem term_a6 : ∫ u in (0: ℝ)..1, ((39: ℝ) / 40) * (u ^ 3 * Real.log (1 - u)) = (-((65: ℝ) / 128)) := by
  rw [intervalIntegral.integral_const_mul, core_lm_3]
  norm_num

theorem term_a7 : ∫ u in (0: ℝ)..1, ((57: ℝ) / 80) * (u ^ 1 * Real.log (1 + u)) = ((57: ℝ) / 320) := by
  rw [intervalIntegral.integral_const_mul, core_lp_1]
  norm_num

theorem term_b0 : ∫ u in (0: ℝ)..1, (-((26: ℝ) / 35)) * u ^ 6 = (-((26: ℝ) / 245)) := by
  rw [intervalIntegral.integral_const_mul, poly_core_6]
  norm_num

theorem term_b1 : ∫ u in (0: ℝ)..1, ((21: ℝ) / 40) * u ^ 2 = ((7: ℝ) / 40) := by
  rw [intervalIntegral.integral_const_mul, poly_core_2]
  norm_num

theorem term_b2 : ∫ u in (0: ℝ)..1, ((1613: ℝ) / 840) * u ^ 4 = ((1613: ℝ) / 4200) := by
  rw [intervalIntegral.integral_const_mul, poly_core_4]
  norm_num

theorem term_b3 : ∫ u in (0: ℝ)..1, (-((669: ℝ) / 560)) * (u ^ 5 * Real.log (1 + u)) = (-((8251: ℝ) / 67200)) := by
  rw [intervalIntegral.integral_const_mul, core_lp_5]
  norm_num

theorem term_b4 : ∫ u in (0: ℝ)..1, (-((129: ℝ) / 280)) * (u ^ 3 * Real.log (1 - u)) = ((215: ℝ) / 896) := by
  rw [intervalIntegral.integral_const_mul, core_lm_3]
  norm_num

theorem term_b5 : ∫ u in (0: ℝ)..1, (-((29: ℝ) / 80)) * (u ^ 1 * Real.log (1 - u)) = ((87: ℝ) / 320) := by
  rw [intervalIntegral.integral_const_mul, core_lm_1]
  norm_num

theorem term_b6 : ∫ u in (0: ℝ)..1, (-((13: ℝ) / 35)) * (u ^ 7 * Real.log (1 - u)) = ((9893: ℝ) / 78400) := by
  rw [intervalIntegral.integral_const_mul, core_lm_7]
  norm_num

theorem term_b7 : ∫ u in (0: ℝ)..1, ((13: ℝ) / 35) * (u ^ 7 * Real.log (1 + u)) = ((6929: ℝ) / 235200) := by
  rw [intervalIntegral.integral_const_mul, core_lp_7]
  norm_num

theorem term_b8 : ∫ u in (0: ℝ)..1, ((29: ℝ) / 80) * (u ^ 1 * Real.log (1 + u)) = ((29: ℝ) / 320) := by
  rw [intervalIntegral.integral_const_mul, core_lp_1]
  norm_num

theorem term_b9 : ∫ u in (0: ℝ)..1, ((129: ℝ) / 280) * (u ^ 3 * Real.log (1 + u)) = ((43: ℝ) / 640) := by
  rw [intervalIntegral.integral_const_mul, core_lp_3]
  norm_num

theorem term_b10 : ∫ u in (0: ℝ)..1, ((669: ℝ) / 560) * (u ^ 5 * Real.log (1 - u)) = (-((1561: ℝ) / 3200)) := by
  rw [intervalIntegral.integral_const_mul, core_lm_5]
  norm_num

theorem term_c0 : ∫ u in (0: ℝ)..1, (-((61: ℝ) / 280)) * u ^ 8 = (-((61: ℝ) / 2520)) := by
  rw [intervalIntegral.integral_const_mul, poly_core_8]
  norm_num

theorem term_c1 : ∫ u in (0: ℝ)..1, ((21: ℝ) / 40) * u ^ 4 = ((21: ℝ) / 200) := by
  rw [intervalIntegral.integral_const_mul, poly_core_4]
  norm_num

theorem term_c2 : ∫ u in (0: ℝ)..1, ((29: ℝ) / 84) * u ^ 6 = ((29: ℝ) / 588) := by
  rw [intervalIntegral.integral_const_mul, poly_core_6]
  norm_num

theorem term_c3 : ∫ u in (0: ℝ)..1, (-((141: ℝ) / 560)) * (u ^ 5 * Real.log (1 + u)) = (-((1739: ℝ) / 67200)) := by
  rw [intervalIntegral.integral_const_mul, core_lp_5]
  norm_num

theorem term_c4 : ∫ u in (0: ℝ)..1, (-((123: ℝ) / 560)) * (u ^ 7 * Real.log (1 + u)) = (-((21853: ℝ) / 1254400)) := by
  rw [intervalIntegral.integral_const_mul, core_lp_7]
  norm_num

theorem term_c5 : ∫ u in (0: ℝ)..1, (-((61: ℝ) / 560)) * (u ^ 9 * Real.log (1 - u)) = ((450241: ℝ) / 14112000) := by
  rw [intervalIntegral.integral_const_mul, core_lm_9]
  norm_num

theorem term_c6 : ∫ u in (0: ℝ)..1, (-((29: ℝ) / 80)) * (u ^ 3 * Real.log (1 - u)) = ((145: ℝ) / 768) := by
  rw [intervalIntegral.integral_const_mul, core_lm_3]
  norm_num

theorem term_c7 : ∫ u in (0: ℝ)..1, ((29: ℝ) / 80) * (u ^ 3 * Real.log (1 + u)) = ((203: ℝ) / 3840) := by
  rw [intervalIntegral.integral_const_mul, core_lp_3]
  norm_num

theorem term_c8 : ∫ u in (0: ℝ)..1, ((61: ℝ) / 560) * (u ^ 9 * Real.log (1 + u)) = ((99247: ℝ) / 14112000) := by
  rw [intervalIntegral.integral_const_mul, core_lp_9]
  norm_num

theorem term_c9 : ∫ u in (0: ℝ)..1, ((123: ℝ) / 560) * (u ^ 7 * Real.log (1 - u)) = (-((93603: ℝ) / 1254400)) := by
  rw [intervalIntegral.integral_const_mul, core_lm_7]
  norm_num

theorem term_c10 : ∫ u in (0: ℝ)..1, ((141: ℝ) / 560) * (u ^ 5 * Real.log (1 - u)) = (-((329: ℝ) / 3200)) := by
  rw [intervalIntegral.integral_const_mul, core_lm_5]
  norm_num

theorem ch_a : ∫ u in (0: ℝ)..1, (-((21: ℝ) / 40)) * u ^ 4 + (((63: ℝ) / 40) * u ^ 2 + ((-((57: ℝ) / 80)) * (u ^ 1 * Real.log (1 - u)) + ((-((39: ℝ) / 40)) * (u ^ 3 * Real.log (1 + u)) + ((-((21: ℝ) / 80)) * (u ^ 5 * Real.log (1 - u)) + (((21: ℝ) / 80) * (u ^ 5 * Real.log (1 + u)) + (((39: ℝ) / 40) * (u ^ 3 * Real.log (1 - u)) + (((57: ℝ) / 80) * (u ^ 1 * Real.log (1 + u))))))))) = ((37: ℝ) / 60) := by
  have hint0 : IntervalIntegrable (fun u : ℝ => (-((21: ℝ) / 40)) * u ^ 4) volume 0 1 := by
    refine Continuous.intervalIntegrable (Continuous.mul continuous_const (by fun_prop : Continuous fun u : ℝ => u ^ 4))
      0 1
  have hint1 : IntervalIntegrable (fun u : ℝ => ((63: ℝ) / 40) * u ^ 2) volume 0 1 := by
    refine Continuous.intervalIntegrable (Continuous.mul continuous_const (by fun_prop : Continuous fun u : ℝ => u ^ 2))
      0 1
  have hint2 : IntervalIntegrable (fun u : ℝ => (-((57: ℝ) / 80)) * (u ^ 1 * Real.log (1 - u))) volume 0 1 := by
    refine IntervalIntegrable.congr (show Set.EqOn (fun x : ℝ => Real.log (1 - x) * ((-((57: ℝ) / 80)) * x ^ 1)) (fun x : ℝ => (-((57: ℝ) / 80)) * (x ^ 1 * Real.log (1 - x))) (Set.uIoc (0: ℝ) 1) from fun x _ => by ring)
      (logm_int.mul_continuousOn (Continuous.continuousOn (Continuous.mul continuous_const (by fun_prop : Continuous fun u : ℝ => u ^ 1))))
  have hint3 : IntervalIntegrable (fun u : ℝ => (-((39: ℝ) / 40)) * (u ^ 3 * Real.log (1 + u))) volume 0 1 := by
    refine IntervalIntegrable.congr (show Set.EqOn (fun x : ℝ => Real.log (x + 1) * ((-((39: ℝ) / 40)) * x ^ 3)) (fun x : ℝ => (-((39: ℝ) / 40)) * (x ^ 3 * Real.log (1 + x))) (Set.uIoc (0: ℝ) 1) from fun x _ => by ring)
      (logp_int.mul_continuousOn (Continuous.continuousOn (Continuous.mul continuous_const (by fun_prop : Continuous fun u : ℝ => u ^ 3))))
  have hint4 : IntervalIntegrable (fun u : ℝ => (-((21: ℝ) / 80)) * (u ^ 5 * Real.log (1 - u))) volume 0 1 := by
    refine IntervalIntegrable.congr (show Set.EqOn (fun x : ℝ => Real.log (1 - x) * ((-((21: ℝ) / 80)) * x ^ 5)) (fun x : ℝ => (-((21: ℝ) / 80)) * (x ^ 5 * Real.log (1 - x))) (Set.uIoc (0: ℝ) 1) from fun x _ => by ring)
      (logm_int.mul_continuousOn (Continuous.continuousOn (Continuous.mul continuous_const (by fun_prop : Continuous fun u : ℝ => u ^ 5))))
  have hint5 : IntervalIntegrable (fun u : ℝ => ((21: ℝ) / 80) * (u ^ 5 * Real.log (1 + u))) volume 0 1 := by
    refine IntervalIntegrable.congr (show Set.EqOn (fun x : ℝ => Real.log (x + 1) * (((21: ℝ) / 80) * x ^ 5)) (fun x : ℝ => ((21: ℝ) / 80) * (x ^ 5 * Real.log (1 + x))) (Set.uIoc (0: ℝ) 1) from fun x _ => by ring)
      (logp_int.mul_continuousOn (Continuous.continuousOn (Continuous.mul continuous_const (by fun_prop : Continuous fun u : ℝ => u ^ 5))))
  have hint6 : IntervalIntegrable (fun u : ℝ => ((39: ℝ) / 40) * (u ^ 3 * Real.log (1 - u))) volume 0 1 := by
    refine IntervalIntegrable.congr (show Set.EqOn (fun x : ℝ => Real.log (1 - x) * (((39: ℝ) / 40) * x ^ 3)) (fun x : ℝ => ((39: ℝ) / 40) * (x ^ 3 * Real.log (1 - x))) (Set.uIoc (0: ℝ) 1) from fun x _ => by ring)
      (logm_int.mul_continuousOn (Continuous.continuousOn (Continuous.mul continuous_const (by fun_prop : Continuous fun u : ℝ => u ^ 3))))
  have hint7 : IntervalIntegrable (fun u : ℝ => ((57: ℝ) / 80) * (u ^ 1 * Real.log (1 + u))) volume 0 1 := by
    refine IntervalIntegrable.congr (show Set.EqOn (fun x : ℝ => Real.log (x + 1) * (((57: ℝ) / 80) * x ^ 1)) (fun x : ℝ => ((57: ℝ) / 80) * (x ^ 1 * Real.log (1 + x))) (Set.uIoc (0: ℝ) 1) from fun x _ => by ring)
      (logp_int.mul_continuousOn (Continuous.continuousOn (Continuous.mul continuous_const (by fun_prop : Continuous fun u : ℝ => u ^ 1))))
  have rs7 : IntervalIntegrable (fun u : ℝ => ((57: ℝ) / 80) * (u ^ 1 * Real.log (1 + u))) volume 0 1 := hint7
  have rs6 : IntervalIntegrable (fun u : ℝ => ((39: ℝ) / 40) * (u ^ 3 * Real.log (1 - u)) + (((57: ℝ) / 80) * (u ^ 1 * Real.log (1 + u)))) volume 0 1 := hint6.add rs7
  have rs5 : IntervalIntegrable (fun u : ℝ => ((21: ℝ) / 80) * (u ^ 5 * Real.log (1 + u)) + (((39: ℝ) / 40) * (u ^ 3 * Real.log (1 - u)) + (((57: ℝ) / 80) * (u ^ 1 * Real.log (1 + u))))) volume 0 1 := hint5.add rs6
  have rs4 : IntervalIntegrable (fun u : ℝ => (-((21: ℝ) / 80)) * (u ^ 5 * Real.log (1 - u)) + (((21: ℝ) / 80) * (u ^ 5 * Real.log (1 + u)) + (((39: ℝ) / 40) * (u ^ 3 * Real.log (1 - u)) + (((57: ℝ) / 80) * (u ^ 1 * Real.log (1 + u)))))) volume 0 1 := hint4.add rs5
  have rs3 : IntervalIntegrable (fun u : ℝ => (-((39: ℝ) / 40)) * (u ^ 3 * Real.log (1 + u)) + ((-((21: ℝ) / 80)) * (u ^ 5 * Real.log (1 - u)) + (((21: ℝ) / 80) * (u ^ 5 * Real.log (1 + u)) + (((39: ℝ) / 40) * (u ^ 3 * Real.log (1 - u)) + (((57: ℝ) / 80) * (u ^ 1 * Real.log (1 + u))))))) volume 0 1 := hint3.add rs4
  have rs2 : IntervalIntegrable (fun u : ℝ => (-((57: ℝ) / 80)) * (u ^ 1 * Real.log (1 - u)) + ((-((39: ℝ) / 40)) * (u ^ 3 * Real.log (1 + u)) + ((-((21: ℝ) / 80)) * (u ^ 5 * Real.log (1 - u)) + (((21: ℝ) / 80) * (u ^ 5 * Real.log (1 + u)) + (((39: ℝ) / 40) * (u ^ 3 * Real.log (1 - u)) + (((57: ℝ) / 80) * (u ^ 1 * Real.log (1 + u)))))))) volume 0 1 := hint2.add rs3
  have rs1 : IntervalIntegrable (fun u : ℝ => ((63: ℝ) / 40) * u ^ 2 + ((-((57: ℝ) / 80)) * (u ^ 1 * Real.log (1 - u)) + ((-((39: ℝ) / 40)) * (u ^ 3 * Real.log (1 + u)) + ((-((21: ℝ) / 80)) * (u ^ 5 * Real.log (1 - u)) + (((21: ℝ) / 80) * (u ^ 5 * Real.log (1 + u)) + (((39: ℝ) / 40) * (u ^ 3 * Real.log (1 - u)) + (((57: ℝ) / 80) * (u ^ 1 * Real.log (1 + u))))))))) volume 0 1 := hint1.add rs2
  have rs0 : IntervalIntegrable (fun u : ℝ => (-((21: ℝ) / 40)) * u ^ 4 + (((63: ℝ) / 40) * u ^ 2 + ((-((57: ℝ) / 80)) * (u ^ 1 * Real.log (1 - u)) + ((-((39: ℝ) / 40)) * (u ^ 3 * Real.log (1 + u)) + ((-((21: ℝ) / 80)) * (u ^ 5 * Real.log (1 - u)) + (((21: ℝ) / 80) * (u ^ 5 * Real.log (1 + u)) + (((39: ℝ) / 40) * (u ^ 3 * Real.log (1 - u)) + (((57: ℝ) / 80) * (u ^ 1 * Real.log (1 + u)))))))))) volume 0 1 := hint0.add rs1
  rw [intervalIntegral.integral_add hint0 rs1, intervalIntegral.integral_add hint1 rs2, intervalIntegral.integral_add hint2 rs3, intervalIntegral.integral_add hint3 rs4, intervalIntegral.integral_add hint4 rs5, intervalIntegral.integral_add hint5 rs6, intervalIntegral.integral_add hint6 rs7]
  rw [term_a0, term_a1, term_a2, term_a3, term_a4, term_a5, term_a6, term_a7]
  norm_num

theorem ch_b : ∫ u in (0: ℝ)..1, (-((26: ℝ) / 35)) * u ^ 6 + (((21: ℝ) / 40) * u ^ 2 + (((1613: ℝ) / 840) * u ^ 4 + ((-((669: ℝ) / 560)) * (u ^ 5 * Real.log (1 + u)) + ((-((129: ℝ) / 280)) * (u ^ 3 * Real.log (1 - u)) + ((-((29: ℝ) / 80)) * (u ^ 1 * Real.log (1 - u)) + ((-((13: ℝ) / 35)) * (u ^ 7 * Real.log (1 - u)) + (((13: ℝ) / 35) * (u ^ 7 * Real.log (1 + u)) + (((29: ℝ) / 80) * (u ^ 1 * Real.log (1 + u)) + (((129: ℝ) / 280) * (u ^ 3 * Real.log (1 + u)) + (((669: ℝ) / 560) * (u ^ 5 * Real.log (1 - u)))))))))))) = ((701: ℝ) / 1050) := by
  have hint0 : IntervalIntegrable (fun u : ℝ => (-((26: ℝ) / 35)) * u ^ 6) volume 0 1 := by
    refine Continuous.intervalIntegrable (Continuous.mul continuous_const (by fun_prop : Continuous fun u : ℝ => u ^ 6))
      0 1
  have hint1 : IntervalIntegrable (fun u : ℝ => ((21: ℝ) / 40) * u ^ 2) volume 0 1 := by
    refine Continuous.intervalIntegrable (Continuous.mul continuous_const (by fun_prop : Continuous fun u : ℝ => u ^ 2))
      0 1
  have hint2 : IntervalIntegrable (fun u : ℝ => ((1613: ℝ) / 840) * u ^ 4) volume 0 1 := by
    refine Continuous.intervalIntegrable (Continuous.mul continuous_const (by fun_prop : Continuous fun u : ℝ => u ^ 4))
      0 1
  have hint3 : IntervalIntegrable (fun u : ℝ => (-((669: ℝ) / 560)) * (u ^ 5 * Real.log (1 + u))) volume 0 1 := by
    refine IntervalIntegrable.congr (show Set.EqOn (fun x : ℝ => Real.log (x + 1) * ((-((669: ℝ) / 560)) * x ^ 5)) (fun x : ℝ => (-((669: ℝ) / 560)) * (x ^ 5 * Real.log (1 + x))) (Set.uIoc (0: ℝ) 1) from fun x _ => by ring)
      (logp_int.mul_continuousOn (Continuous.continuousOn (Continuous.mul continuous_const (by fun_prop : Continuous fun u : ℝ => u ^ 5))))
  have hint4 : IntervalIntegrable (fun u : ℝ => (-((129: ℝ) / 280)) * (u ^ 3 * Real.log (1 - u))) volume 0 1 := by
    refine IntervalIntegrable.congr (show Set.EqOn (fun x : ℝ => Real.log (1 - x) * ((-((129: ℝ) / 280)) * x ^ 3)) (fun x : ℝ => (-((129: ℝ) / 280)) * (x ^ 3 * Real.log (1 - x))) (Set.uIoc (0: ℝ) 1) from fun x _ => by ring)
      (logm_int.mul_continuousOn (Continuous.continuousOn (Continuous.mul continuous_const (by fun_prop : Continuous fun u : ℝ => u ^ 3))))
  have hint5 : IntervalIntegrable (fun u : ℝ => (-((29: ℝ) / 80)) * (u ^ 1 * Real.log (1 - u))) volume 0 1 := by
    refine IntervalIntegrable.congr (show Set.EqOn (fun x : ℝ => Real.log (1 - x) * ((-((29: ℝ) / 80)) * x ^ 1)) (fun x : ℝ => (-((29: ℝ) / 80)) * (x ^ 1 * Real.log (1 - x))) (Set.uIoc (0: ℝ) 1) from fun x _ => by ring)
      (logm_int.mul_continuousOn (Continuous.continuousOn (Continuous.mul continuous_const (by fun_prop : Continuous fun u : ℝ => u ^ 1))))
  have hint6 : IntervalIntegrable (fun u : ℝ => (-((13: ℝ) / 35)) * (u ^ 7 * Real.log (1 - u))) volume 0 1 := by
    refine IntervalIntegrable.congr (show Set.EqOn (fun x : ℝ => Real.log (1 - x) * ((-((13: ℝ) / 35)) * x ^ 7)) (fun x : ℝ => (-((13: ℝ) / 35)) * (x ^ 7 * Real.log (1 - x))) (Set.uIoc (0: ℝ) 1) from fun x _ => by ring)
      (logm_int.mul_continuousOn (Continuous.continuousOn (Continuous.mul continuous_const (by fun_prop : Continuous fun u : ℝ => u ^ 7))))
  have hint7 : IntervalIntegrable (fun u : ℝ => ((13: ℝ) / 35) * (u ^ 7 * Real.log (1 + u))) volume 0 1 := by
    refine IntervalIntegrable.congr (show Set.EqOn (fun x : ℝ => Real.log (x + 1) * (((13: ℝ) / 35) * x ^ 7)) (fun x : ℝ => ((13: ℝ) / 35) * (x ^ 7 * Real.log (1 + x))) (Set.uIoc (0: ℝ) 1) from fun x _ => by ring)
      (logp_int.mul_continuousOn (Continuous.continuousOn (Continuous.mul continuous_const (by fun_prop : Continuous fun u : ℝ => u ^ 7))))
  have hint8 : IntervalIntegrable (fun u : ℝ => ((29: ℝ) / 80) * (u ^ 1 * Real.log (1 + u))) volume 0 1 := by
    refine IntervalIntegrable.congr (show Set.EqOn (fun x : ℝ => Real.log (x + 1) * (((29: ℝ) / 80) * x ^ 1)) (fun x : ℝ => ((29: ℝ) / 80) * (x ^ 1 * Real.log (1 + x))) (Set.uIoc (0: ℝ) 1) from fun x _ => by ring)
      (logp_int.mul_continuousOn (Continuous.continuousOn (Continuous.mul continuous_const (by fun_prop : Continuous fun u : ℝ => u ^ 1))))
  have hint9 : IntervalIntegrable (fun u : ℝ => ((129: ℝ) / 280) * (u ^ 3 * Real.log (1 + u))) volume 0 1 := by
    refine IntervalIntegrable.congr (show Set.EqOn (fun x : ℝ => Real.log (x + 1) * (((129: ℝ) / 280) * x ^ 3)) (fun x : ℝ => ((129: ℝ) / 280) * (x ^ 3 * Real.log (1 + x))) (Set.uIoc (0: ℝ) 1) from fun x _ => by ring)
      (logp_int.mul_continuousOn (Continuous.continuousOn (Continuous.mul continuous_const (by fun_prop : Continuous fun u : ℝ => u ^ 3))))
  have hint10 : IntervalIntegrable (fun u : ℝ => ((669: ℝ) / 560) * (u ^ 5 * Real.log (1 - u))) volume 0 1 := by
    refine IntervalIntegrable.congr (show Set.EqOn (fun x : ℝ => Real.log (1 - x) * (((669: ℝ) / 560) * x ^ 5)) (fun x : ℝ => ((669: ℝ) / 560) * (x ^ 5 * Real.log (1 - x))) (Set.uIoc (0: ℝ) 1) from fun x _ => by ring)
      (logm_int.mul_continuousOn (Continuous.continuousOn (Continuous.mul continuous_const (by fun_prop : Continuous fun u : ℝ => u ^ 5))))
  have rs10 : IntervalIntegrable (fun u : ℝ => ((669: ℝ) / 560) * (u ^ 5 * Real.log (1 - u))) volume 0 1 := hint10
  have rs9 : IntervalIntegrable (fun u : ℝ => ((129: ℝ) / 280) * (u ^ 3 * Real.log (1 + u)) + (((669: ℝ) / 560) * (u ^ 5 * Real.log (1 - u)))) volume 0 1 := hint9.add rs10
  have rs8 : IntervalIntegrable (fun u : ℝ => ((29: ℝ) / 80) * (u ^ 1 * Real.log (1 + u)) + (((129: ℝ) / 280) * (u ^ 3 * Real.log (1 + u)) + (((669: ℝ) / 560) * (u ^ 5 * Real.log (1 - u))))) volume 0 1 := hint8.add rs9
  have rs7 : IntervalIntegrable (fun u : ℝ => ((13: ℝ) / 35) * (u ^ 7 * Real.log (1 + u)) + (((29: ℝ) / 80) * (u ^ 1 * Real.log (1 + u)) + (((129: ℝ) / 280) * (u ^ 3 * Real.log (1 + u)) + (((669: ℝ) / 560) * (u ^ 5 * Real.log (1 - u)))))) volume 0 1 := hint7.add rs8
  have rs6 : IntervalIntegrable (fun u : ℝ => (-((13: ℝ) / 35)) * (u ^ 7 * Real.log (1 - u)) + (((13: ℝ) / 35) * (u ^ 7 * Real.log (1 + u)) + (((29: ℝ) / 80) * (u ^ 1 * Real.log (1 + u)) + (((129: ℝ) / 280) * (u ^ 3 * Real.log (1 + u)) + (((669: ℝ) / 560) * (u ^ 5 * Real.log (1 - u))))))) volume 0 1 := hint6.add rs7
  have rs5 : IntervalIntegrable (fun u : ℝ => (-((29: ℝ) / 80)) * (u ^ 1 * Real.log (1 - u)) + ((-((13: ℝ) / 35)) * (u ^ 7 * Real.log (1 - u)) + (((13: ℝ) / 35) * (u ^ 7 * Real.log (1 + u)) + (((29: ℝ) / 80) * (u ^ 1 * Real.log (1 + u)) + (((129: ℝ) / 280) * (u ^ 3 * Real.log (1 + u)) + (((669: ℝ) / 560) * (u ^ 5 * Real.log (1 - u)))))))) volume 0 1 := hint5.add rs6
  have rs4 : IntervalIntegrable (fun u : ℝ => (-((129: ℝ) / 280)) * (u ^ 3 * Real.log (1 - u)) + ((-((29: ℝ) / 80)) * (u ^ 1 * Real.log (1 - u)) + ((-((13: ℝ) / 35)) * (u ^ 7 * Real.log (1 - u)) + (((13: ℝ) / 35) * (u ^ 7 * Real.log (1 + u)) + (((29: ℝ) / 80) * (u ^ 1 * Real.log (1 + u)) + (((129: ℝ) / 280) * (u ^ 3 * Real.log (1 + u)) + (((669: ℝ) / 560) * (u ^ 5 * Real.log (1 - u))))))))) volume 0 1 := hint4.add rs5
  have rs3 : IntervalIntegrable (fun u : ℝ => (-((669: ℝ) / 560)) * (u ^ 5 * Real.log (1 + u)) + ((-((129: ℝ) / 280)) * (u ^ 3 * Real.log (1 - u)) + ((-((29: ℝ) / 80)) * (u ^ 1 * Real.log (1 - u)) + ((-((13: ℝ) / 35)) * (u ^ 7 * Real.log (1 - u)) + (((13: ℝ) / 35) * (u ^ 7 * Real.log (1 + u)) + (((29: ℝ) / 80) * (u ^ 1 * Real.log (1 + u)) + (((129: ℝ) / 280) * (u ^ 3 * Real.log (1 + u)) + (((669: ℝ) / 560) * (u ^ 5 * Real.log (1 - u)))))))))) volume 0 1 := hint3.add rs4
  have rs2 : IntervalIntegrable (fun u : ℝ => ((1613: ℝ) / 840) * u ^ 4 + ((-((669: ℝ) / 560)) * (u ^ 5 * Real.log (1 + u)) + ((-((129: ℝ) / 280)) * (u ^ 3 * Real.log (1 - u)) + ((-((29: ℝ) / 80)) * (u ^ 1 * Real.log (1 - u)) + ((-((13: ℝ) / 35)) * (u ^ 7 * Real.log (1 - u)) + (((13: ℝ) / 35) * (u ^ 7 * Real.log (1 + u)) + (((29: ℝ) / 80) * (u ^ 1 * Real.log (1 + u)) + (((129: ℝ) / 280) * (u ^ 3 * Real.log (1 + u)) + (((669: ℝ) / 560) * (u ^ 5 * Real.log (1 - u))))))))))) volume 0 1 := hint2.add rs3
  have rs1 : IntervalIntegrable (fun u : ℝ => ((21: ℝ) / 40) * u ^ 2 + (((1613: ℝ) / 840) * u ^ 4 + ((-((669: ℝ) / 560)) * (u ^ 5 * Real.log (1 + u)) + ((-((129: ℝ) / 280)) * (u ^ 3 * Real.log (1 - u)) + ((-((29: ℝ) / 80)) * (u ^ 1 * Real.log (1 - u)) + ((-((13: ℝ) / 35)) * (u ^ 7 * Real.log (1 - u)) + (((13: ℝ) / 35) * (u ^ 7 * Real.log (1 + u)) + (((29: ℝ) / 80) * (u ^ 1 * Real.log (1 + u)) + (((129: ℝ) / 280) * (u ^ 3 * Real.log (1 + u)) + (((669: ℝ) / 560) * (u ^ 5 * Real.log (1 - u)))))))))))) volume 0 1 := hint1.add rs2
  have rs0 : IntervalIntegrable (fun u : ℝ => (-((26: ℝ) / 35)) * u ^ 6 + (((21: ℝ) / 40) * u ^ 2 + (((1613: ℝ) / 840) * u ^ 4 + ((-((669: ℝ) / 560)) * (u ^ 5 * Real.log (1 + u)) + ((-((129: ℝ) / 280)) * (u ^ 3 * Real.log (1 - u)) + ((-((29: ℝ) / 80)) * (u ^ 1 * Real.log (1 - u)) + ((-((13: ℝ) / 35)) * (u ^ 7 * Real.log (1 - u)) + (((13: ℝ) / 35) * (u ^ 7 * Real.log (1 + u)) + (((29: ℝ) / 80) * (u ^ 1 * Real.log (1 + u)) + (((129: ℝ) / 280) * (u ^ 3 * Real.log (1 + u)) + (((669: ℝ) / 560) * (u ^ 5 * Real.log (1 - u))))))))))))) volume 0 1 := hint0.add rs1
  rw [intervalIntegral.integral_add hint0 rs1, intervalIntegral.integral_add hint1 rs2, intervalIntegral.integral_add hint2 rs3, intervalIntegral.integral_add hint3 rs4, intervalIntegral.integral_add hint4 rs5, intervalIntegral.integral_add hint5 rs6, intervalIntegral.integral_add hint6 rs7, intervalIntegral.integral_add hint7 rs8, intervalIntegral.integral_add hint8 rs9, intervalIntegral.integral_add hint9 rs10]
  rw [term_b0, term_b1, term_b2, term_b3, term_b4, term_b5, term_b6, term_b7, term_b8, term_b9, term_b10]
  norm_num

theorem ch_c : ∫ u in (0: ℝ)..1, (-((61: ℝ) / 280)) * u ^ 8 + (((21: ℝ) / 40) * u ^ 4 + (((29: ℝ) / 84) * u ^ 6 + ((-((141: ℝ) / 560)) * (u ^ 5 * Real.log (1 + u)) + ((-((123: ℝ) / 560)) * (u ^ 7 * Real.log (1 + u)) + ((-((61: ℝ) / 560)) * (u ^ 9 * Real.log (1 - u)) + ((-((29: ℝ) / 80)) * (u ^ 3 * Real.log (1 - u)) + (((29: ℝ) / 80) * (u ^ 3 * Real.log (1 + u)) + (((61: ℝ) / 560) * (u ^ 9 * Real.log (1 + u)) + (((123: ℝ) / 560) * (u ^ 7 * Real.log (1 - u)) + (((141: ℝ) / 560) * (u ^ 5 * Real.log (1 - u)))))))))))) = ((3491: ℝ) / 18375) := by
  have hint0 : IntervalIntegrable (fun u : ℝ => (-((61: ℝ) / 280)) * u ^ 8) volume 0 1 := by
    refine Continuous.intervalIntegrable (Continuous.mul continuous_const (by fun_prop : Continuous fun u : ℝ => u ^ 8))
      0 1
  have hint1 : IntervalIntegrable (fun u : ℝ => ((21: ℝ) / 40) * u ^ 4) volume 0 1 := by
    refine Continuous.intervalIntegrable (Continuous.mul continuous_const (by fun_prop : Continuous fun u : ℝ => u ^ 4))
      0 1
  have hint2 : IntervalIntegrable (fun u : ℝ => ((29: ℝ) / 84) * u ^ 6) volume 0 1 := by
    refine Continuous.intervalIntegrable (Continuous.mul continuous_const (by fun_prop : Continuous fun u : ℝ => u ^ 6))
      0 1
  have hint3 : IntervalIntegrable (fun u : ℝ => (-((141: ℝ) / 560)) * (u ^ 5 * Real.log (1 + u))) volume 0 1 := by
    refine IntervalIntegrable.congr (show Set.EqOn (fun x : ℝ => Real.log (x + 1) * ((-((141: ℝ) / 560)) * x ^ 5)) (fun x : ℝ => (-((141: ℝ) / 560)) * (x ^ 5 * Real.log (1 + x))) (Set.uIoc (0: ℝ) 1) from fun x _ => by ring)
      (logp_int.mul_continuousOn (Continuous.continuousOn (Continuous.mul continuous_const (by fun_prop : Continuous fun u : ℝ => u ^ 5))))
  have hint4 : IntervalIntegrable (fun u : ℝ => (-((123: ℝ) / 560)) * (u ^ 7 * Real.log (1 + u))) volume 0 1 := by
    refine IntervalIntegrable.congr (show Set.EqOn (fun x : ℝ => Real.log (x + 1) * ((-((123: ℝ) / 560)) * x ^ 7)) (fun x : ℝ => (-((123: ℝ) / 560)) * (x ^ 7 * Real.log (1 + x))) (Set.uIoc (0: ℝ) 1) from fun x _ => by ring)
      (logp_int.mul_continuousOn (Continuous.continuousOn (Continuous.mul continuous_const (by fun_prop : Continuous fun u : ℝ => u ^ 7))))
  have hint5 : IntervalIntegrable (fun u : ℝ => (-((61: ℝ) / 560)) * (u ^ 9 * Real.log (1 - u))) volume 0 1 := by
    refine IntervalIntegrable.congr (show Set.EqOn (fun x : ℝ => Real.log (1 - x) * ((-((61: ℝ) / 560)) * x ^ 9)) (fun x : ℝ => (-((61: ℝ) / 560)) * (x ^ 9 * Real.log (1 - x))) (Set.uIoc (0: ℝ) 1) from fun x _ => by ring)
      (logm_int.mul_continuousOn (Continuous.continuousOn (Continuous.mul continuous_const (by fun_prop : Continuous fun u : ℝ => u ^ 9))))
  have hint6 : IntervalIntegrable (fun u : ℝ => (-((29: ℝ) / 80)) * (u ^ 3 * Real.log (1 - u))) volume 0 1 := by
    refine IntervalIntegrable.congr (show Set.EqOn (fun x : ℝ => Real.log (1 - x) * ((-((29: ℝ) / 80)) * x ^ 3)) (fun x : ℝ => (-((29: ℝ) / 80)) * (x ^ 3 * Real.log (1 - x))) (Set.uIoc (0: ℝ) 1) from fun x _ => by ring)
      (logm_int.mul_continuousOn (Continuous.continuousOn (Continuous.mul continuous_const (by fun_prop : Continuous fun u : ℝ => u ^ 3))))
  have hint7 : IntervalIntegrable (fun u : ℝ => ((29: ℝ) / 80) * (u ^ 3 * Real.log (1 + u))) volume 0 1 := by
    refine IntervalIntegrable.congr (show Set.EqOn (fun x : ℝ => Real.log (x + 1) * (((29: ℝ) / 80) * x ^ 3)) (fun x : ℝ => ((29: ℝ) / 80) * (x ^ 3 * Real.log (1 + x))) (Set.uIoc (0: ℝ) 1) from fun x _ => by ring)
      (logp_int.mul_continuousOn (Continuous.continuousOn (Continuous.mul continuous_const (by fun_prop : Continuous fun u : ℝ => u ^ 3))))
  have hint8 : IntervalIntegrable (fun u : ℝ => ((61: ℝ) / 560) * (u ^ 9 * Real.log (1 + u))) volume 0 1 := by
    refine IntervalIntegrable.congr (show Set.EqOn (fun x : ℝ => Real.log (x + 1) * (((61: ℝ) / 560) * x ^ 9)) (fun x : ℝ => ((61: ℝ) / 560) * (x ^ 9 * Real.log (1 + x))) (Set.uIoc (0: ℝ) 1) from fun x _ => by ring)
      (logp_int.mul_continuousOn (Continuous.continuousOn (Continuous.mul continuous_const (by fun_prop : Continuous fun u : ℝ => u ^ 9))))
  have hint9 : IntervalIntegrable (fun u : ℝ => ((123: ℝ) / 560) * (u ^ 7 * Real.log (1 - u))) volume 0 1 := by
    refine IntervalIntegrable.congr (show Set.EqOn (fun x : ℝ => Real.log (1 - x) * (((123: ℝ) / 560) * x ^ 7)) (fun x : ℝ => ((123: ℝ) / 560) * (x ^ 7 * Real.log (1 - x))) (Set.uIoc (0: ℝ) 1) from fun x _ => by ring)
      (logm_int.mul_continuousOn (Continuous.continuousOn (Continuous.mul continuous_const (by fun_prop : Continuous fun u : ℝ => u ^ 7))))
  have hint10 : IntervalIntegrable (fun u : ℝ => ((141: ℝ) / 560) * (u ^ 5 * Real.log (1 - u))) volume 0 1 := by
    refine IntervalIntegrable.congr (show Set.EqOn (fun x : ℝ => Real.log (1 - x) * (((141: ℝ) / 560) * x ^ 5)) (fun x : ℝ => ((141: ℝ) / 560) * (x ^ 5 * Real.log (1 - x))) (Set.uIoc (0: ℝ) 1) from fun x _ => by ring)
      (logm_int.mul_continuousOn (Continuous.continuousOn (Continuous.mul continuous_const (by fun_prop : Continuous fun u : ℝ => u ^ 5))))
  have rs10 : IntervalIntegrable (fun u : ℝ => ((141: ℝ) / 560) * (u ^ 5 * Real.log (1 - u))) volume 0 1 := hint10
  have rs9 : IntervalIntegrable (fun u : ℝ => ((123: ℝ) / 560) * (u ^ 7 * Real.log (1 - u)) + (((141: ℝ) / 560) * (u ^ 5 * Real.log (1 - u)))) volume 0 1 := hint9.add rs10
  have rs8 : IntervalIntegrable (fun u : ℝ => ((61: ℝ) / 560) * (u ^ 9 * Real.log (1 + u)) + (((123: ℝ) / 560) * (u ^ 7 * Real.log (1 - u)) + (((141: ℝ) / 560) * (u ^ 5 * Real.log (1 - u))))) volume 0 1 := hint8.add rs9
  have rs7 : IntervalIntegrable (fun u : ℝ => ((29: ℝ) / 80) * (u ^ 3 * Real.log (1 + u)) + (((61: ℝ) / 560) * (u ^ 9 * Real.log (1 + u)) + (((123: ℝ) / 560) * (u ^ 7 * Real.log (1 - u)) + (((141: ℝ) / 560) * (u ^ 5 * Real.log (1 - u)))))) volume 0 1 := hint7.add rs8
  have rs6 : IntervalIntegrable (fun u : ℝ => (-((29: ℝ) / 80)) * (u ^ 3 * Real.log (1 - u)) + (((29: ℝ) / 80) * (u ^ 3 * Real.log (1 + u)) + (((61: ℝ) / 560) * (u ^ 9 * Real.log (1 + u)) + (((123: ℝ) / 560) * (u ^ 7 * Real.log (1 - u)) + (((141: ℝ) / 560) * (u ^ 5 * Real.log (1 - u))))))) volume 0 1 := hint6.add rs7
  have rs5 : IntervalIntegrable (fun u : ℝ => (-((61: ℝ) / 560)) * (u ^ 9 * Real.log (1 - u)) + ((-((29: ℝ) / 80)) * (u ^ 3 * Real.log (1 - u)) + (((29: ℝ) / 80) * (u ^ 3 * Real.log (1 + u)) + (((61: ℝ) / 560) * (u ^ 9 * Real.log (1 + u)) + (((123: ℝ) / 560) * (u ^ 7 * Real.log (1 - u)) + (((141: ℝ) / 560) * (u ^ 5 * Real.log (1 - u)))))))) volume 0 1 := hint5.add rs6
  have rs4 : IntervalIntegrable (fun u : ℝ => (-((123: ℝ) / 560)) * (u ^ 7 * Real.log (1 + u)) + ((-((61: ℝ) / 560)) * (u ^ 9 * Real.log (1 - u)) + ((-((29: ℝ) / 80)) * (u ^ 3 * Real.log (1 - u)) + (((29: ℝ) / 80) * (u ^ 3 * Real.log (1 + u)) + (((61: ℝ) / 560) * (u ^ 9 * Real.log (1 + u)) + (((123: ℝ) / 560) * (u ^ 7 * Real.log (1 - u)) + (((141: ℝ) / 560) * (u ^ 5 * Real.log (1 - u))))))))) volume 0 1 := hint4.add rs5
  have rs3 : IntervalIntegrable (fun u : ℝ => (-((141: ℝ) / 560)) * (u ^ 5 * Real.log (1 + u)) + ((-((123: ℝ) / 560)) * (u ^ 7 * Real.log (1 + u)) + ((-((61: ℝ) / 560)) * (u ^ 9 * Real.log (1 - u)) + ((-((29: ℝ) / 80)) * (u ^ 3 * Real.log (1 - u)) + (((29: ℝ) / 80) * (u ^ 3 * Real.log (1 + u)) + (((61: ℝ) / 560) * (u ^ 9 * Real.log (1 + u)) + (((123: ℝ) / 560) * (u ^ 7 * Real.log (1 - u)) + (((141: ℝ) / 560) * (u ^ 5 * Real.log (1 - u)))))))))) volume 0 1 := hint3.add rs4
  have rs2 : IntervalIntegrable (fun u : ℝ => ((29: ℝ) / 84) * u ^ 6 + ((-((141: ℝ) / 560)) * (u ^ 5 * Real.log (1 + u)) + ((-((123: ℝ) / 560)) * (u ^ 7 * Real.log (1 + u)) + ((-((61: ℝ) / 560)) * (u ^ 9 * Real.log (1 - u)) + ((-((29: ℝ) / 80)) * (u ^ 3 * Real.log (1 - u)) + (((29: ℝ) / 80) * (u ^ 3 * Real.log (1 + u)) + (((61: ℝ) / 560) * (u ^ 9 * Real.log (1 + u)) + (((123: ℝ) / 560) * (u ^ 7 * Real.log (1 - u)) + (((141: ℝ) / 560) * (u ^ 5 * Real.log (1 - u))))))))))) volume 0 1 := hint2.add rs3
  have rs1 : IntervalIntegrable (fun u : ℝ => ((21: ℝ) / 40) * u ^ 4 + (((29: ℝ) / 84) * u ^ 6 + ((-((141: ℝ) / 560)) * (u ^ 5 * Real.log (1 + u)) + ((-((123: ℝ) / 560)) * (u ^ 7 * Real.log (1 + u)) + ((-((61: ℝ) / 560)) * (u ^ 9 * Real.log (1 - u)) + ((-((29: ℝ) / 80)) * (u ^ 3 * Real.log (1 - u)) + (((29: ℝ) / 80) * (u ^ 3 * Real.log (1 + u)) + (((61: ℝ) / 560) * (u ^ 9 * Real.log (1 + u)) + (((123: ℝ) / 560) * (u ^ 7 * Real.log (1 - u)) + (((141: ℝ) / 560) * (u ^ 5 * Real.log (1 - u)))))))))))) volume 0 1 := hint1.add rs2
  have rs0 : IntervalIntegrable (fun u : ℝ => (-((61: ℝ) / 280)) * u ^ 8 + (((21: ℝ) / 40) * u ^ 4 + (((29: ℝ) / 84) * u ^ 6 + ((-((141: ℝ) / 560)) * (u ^ 5 * Real.log (1 + u)) + ((-((123: ℝ) / 560)) * (u ^ 7 * Real.log (1 + u)) + ((-((61: ℝ) / 560)) * (u ^ 9 * Real.log (1 - u)) + ((-((29: ℝ) / 80)) * (u ^ 3 * Real.log (1 - u)) + (((29: ℝ) / 80) * (u ^ 3 * Real.log (1 + u)) + (((61: ℝ) / 560) * (u ^ 9 * Real.log (1 + u)) + (((123: ℝ) / 560) * (u ^ 7 * Real.log (1 - u)) + (((141: ℝ) / 560) * (u ^ 5 * Real.log (1 - u))))))))))))) volume 0 1 := hint0.add rs1
  rw [intervalIntegral.integral_add hint0 rs1, intervalIntegral.integral_add hint1 rs2, intervalIntegral.integral_add hint2 rs3, intervalIntegral.integral_add hint3 rs4, intervalIntegral.integral_add hint4 rs5, intervalIntegral.integral_add hint5 rs6, intervalIntegral.integral_add hint6 rs7, intervalIntegral.integral_add hint7 rs8, intervalIntegral.integral_add hint8 rs9, intervalIntegral.integral_add hint9 rs10]
  rw [term_c0, term_c1, term_c2, term_c3, term_c4, term_c5, term_c6, term_c7, term_c8, term_c9, term_c10]
  norm_num

theorem c1_q0 : ((37: ℝ) / 60 - (1: ℝ) / 3) = ((17: ℝ) / 60) := by norm_num
theorem c1_q1 : ((701: ℝ) / 1050 - (1: ℝ) / 3) = ((117: ℝ) / 350) := by norm_num
theorem c1_q2 : ((3491: ℝ) / 18375 - (46: ℝ) / 525) = ((627: ℝ) / 6125) := by norm_num
theorem c1_law : ∀ q : ℝ, ((17: ℝ) / 60 + (117 / 350) * q + (627 / 6125) * q ^ 2)
    = ((37: ℝ) / 60 + (701 / 1050) * q + (3491 / 18375) * q ^ 2)
    - ((1: ℝ) / 3 + (1 / 3) * q + (46 / 525) * q ^ 2) := by
  intro q; ring

#print axioms ch_a
#print axioms ch_b
#print axioms ch_c

