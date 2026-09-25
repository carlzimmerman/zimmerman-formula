import Mathlib
/-!
# V01 - the volume-chord moment chordMomentVol = 3/4 (M01's conjectured item)

Route (V-WAVE_BRIEF.md, 2026-09-25): the 2D change of variables that blocked M01
is AVOIDABLE.
  (1) the mu-linear term r*mu integrates to zero on the symmetric interval;
  (2) per fixed r substitute v = r*mu (1D interval substitution,
      `smul_integral_comp_mul_left`):  r^2 * int_{-1}^{1} sqrt(1-r^2+r^2*mu^2) dmu
      = r * int_{-r}^{r} sqrt(1-r^2+v^2) dv  (r = 0: both sides 0);
  (3) indicator peeling + rectangle Fubini swap over [0,1] x [-1,1] flips the
      triangle order:  int_0^1 int_{-r}^{r} = int_{-1}^{1} int_{|v|}^{1};
  (4) antiderivative d/dr [-(1/3)(1-r^2+v^2)^{3/2}] = r*sqrt(1-r^2+v^2)
      (argument >= v^2 >= 0 on [0,1]); inner integral = (1-|v|^3)/3;
      the flipped integral = int_{-1}^{1} (1-|v|^3)/3 dv = 1/2.
  chordMomentVol = 3 * (1/2) * (1/2) = 3/4.
No 2D change-of-variables theorem is used.
-/
open scoped intervalIntegral Real
open Set intervalIntegral

noncomputable section
namespace V01

/-! ## Stage A0: symmetric-integral basics -/

/-- helper: a continuous real function is interval integrable. -/
theorem intBdd (f : ℝ → ℝ) (a b : ℝ) (hc : Continuous f) :
    IntervalIntegrable f MeasureTheory.volume a b := hc.intervalIntegrable a b

/-- `int x in -1..1, x = 0`. -/
theorem integral_x_symm : ∫ x in (-1 : ℝ)..1, x = 0 := by
  have key : ∫ x in (-1 : ℝ)..1, x
      = (1 : ℝ) * 1 / 2 - (-1 : ℝ) * (-1) / 2 := by
    have hEq : Set.EqOn (fun x : ℝ => x)
        (fun x : ℝ => deriv (fun y : ℝ => y * y / 2) x) (Set.uIcc (-1) 1) := by
      intro x _; simp
    have hd : deriv (fun y : ℝ => y * y / 2) = (fun y : ℝ => y) := by
      funext x; simp
    have hdiff : ∀ x ∈ Set.uIcc (-1 : ℝ) 1, DifferentiableAt ℝ (fun y => y * y / 2) x :=
      fun x _ => by fun_prop
    have hcont : ContinuousOn (fun y : ℝ => y) (Set.uIcc (-1) 1) := by fun_prop
    rw [integral_congr hEq, hd,
      integral_deriv_eq_sub' (fun y : ℝ => y * y / 2) hd hdiff hcont]
  rw [key]; ring

/-- `int mu in -1..1, r * mu = 0`. -/
theorem mul_x_integral_zero (r : ℝ) : ∫ μ in (-1 : ℝ)..1, r * μ = 0 := by
  rw [integral_const_mul r (fun x : ℝ => x)]
  simp only [integral_x_symm, mul_zero]

/-- The M01 chord function (identical definition). -/
def chord (r μ : ℝ) : ℝ := r * μ + Real.sqrt (1 - r ^ 2 * (1 - μ ^ 2))

/-- The M01 volume-chord moment (identical definition). -/
def chordMomentVol : ℝ :=
  3 * (∫ r in (0 : ℝ)..1, r ^ 2 * (1 / 2 * (∫ μ in (-1 : ℝ)..1, chord r μ)))

/-- The mu-linear term vanishes; the sqrt argument is rewritten to the
    `1 - r^2 + r^2*mu^2` normal form. -/
theorem inner_eq (r : ℝ) :
    ∫ μ in (-1 : ℝ)..1, chord r μ
      = ∫ μ in (-1 : ℝ)..1, Real.sqrt (1 - r ^ 2 + r ^ 2 * μ ^ 2) := by
  have hEq : Set.EqOn (fun μ => Real.sqrt (1 - r ^ 2 * (1 - μ ^ 2)))
      (fun μ => Real.sqrt (1 - r ^ 2 + r ^ 2 * μ ^ 2)) (Set.uIcc (-1) 1) := by
    intro μ _
    show Real.sqrt (1 - r ^ 2 * (1 - μ ^ 2)) = Real.sqrt (1 - r ^ 2 + r ^ 2 * μ ^ 2)
    have hring : 1 - r ^ 2 * (1 - μ ^ 2) = 1 - r ^ 2 + r ^ 2 * μ ^ 2 := by ring
    rw [hring]
  simp only [chord]
  rw [integral_add (intBdd _ _ _ (by fun_prop)) (intBdd _ _ _ (by fun_prop)),
    mul_x_integral_zero, zero_add]
  exact integral_congr hEq

/-! ## Stage A1: the per-r substitution (step 2) -/

/-- Step 2 for `r` in `[0,1]`:  r^2 * int_{-1}^{1} sqrt(1-r^2+r^2*mu^2) dmu
    = r * int_{-r}^{r} sqrt(1-r^2+v^2) dv  (r = 0: both sides 0). -/
theorem step2 (r : ℝ) (hr : 0 ≤ r) (hr1 : r ≤ 1) :
    r ^ 2 * (∫ μ in (-1 : ℝ)..1, Real.sqrt (1 - r ^ 2 + r ^ 2 * μ ^ 2))
      = r * (∫ v in (-r : ℝ)..r, Real.sqrt (1 - r ^ 2 + v ^ 2)) := by
  rcases eq_or_lt_of_le hr with h0 | h0
  · subst h0; simp
  · have hrne : r ≠ 0 := ne_of_gt h0
    -- smul_integral_comp_mul_left: r • ∫ mu in -1..1, f (r * mu) = ∫ v in -r..r, f v
    have hswap := smul_integral_comp_mul_left
      (f := fun x : ℝ => Real.sqrt (1 - r ^ 2 + x ^ 2)) (c := r)
      (a := (-1 : ℝ)) (b := 1)
    have hEq : Set.EqOn (fun μ => Real.sqrt (1 - r ^ 2 + r ^ 2 * μ ^ 2))
        (fun μ => Real.sqrt (1 - r ^ 2 + (r * μ) ^ 2)) (Set.uIcc (-1) 1) := by
      intro μ _
      show Real.sqrt (1 - r ^ 2 + r ^ 2 * μ ^ 2)
          = Real.sqrt (1 - r ^ 2 + (r * μ) ^ 2)
      congr 2
      ring
    rw [integral_congr hEq.symm] at hswap
    -- hswap : r * I = J (bounds r * -1, r * 1 normalized by simp)
    have hswap' : r * (∫ μ in (-1 : ℝ)..1, Real.sqrt (1 - r ^ 2 + r ^ 2 * μ ^ 2))
        = (∫ v in (-r : ℝ)..r, Real.sqrt (1 - r ^ 2 + v ^ 2)) := by
      simpa [smul_eq_mul] using hswap
    have hI : ∫ μ in (-1 : ℝ)..1, Real.sqrt (1 - r ^ 2 + r ^ 2 * μ ^ 2)
        = r⁻¹ * (∫ v in (-r : ℝ)..r, Real.sqrt (1 - r ^ 2 + v ^ 2)) := by
      calc ∫ μ in (-1 : ℝ)..1, Real.sqrt (1 - r ^ 2 + r ^ 2 * μ ^ 2)
          = r⁻¹ * (r * ∫ μ in (-1 : ℝ)..1, Real.sqrt (1 - r ^ 2 + r ^ 2 * μ ^ 2)) := by
            field_simp
      _ = r⁻¹ * (∫ v in (-r : ℝ)..r, Real.sqrt (1 - r ^ 2 + v ^ 2)) := by
            rw [hswap']
    rw [hI]
    field_simp




/-! ## Stage B: indicator peeling + rectangle Fubini + evaluation -/

/- two measurable sets differing only inside `{x0}` carry equal set integrals. -/
theorem setIntegral_congr_of_singleton_diff (s t : Set ℝ) (hs : MeasurableSet s)
    (ht : MeasurableSet t) (x0 : ℝ) (f : ℝ → ℝ)
    (h1 : ∀ x ∈ s, x ∉ t → x = x0) (h2 : ∀ x ∈ t, x ∈ s) :
    ∫ x in s, f x = ∫ x in t, f x := by
  refine MeasureTheory.setIntegral_congr_set ?_
  rw [MeasureTheory.ae_eq_set]
  constructor
  · have hsub : s \ t ⊆ {x0} := fun x hx => Set.mem_singleton_iff.2 (h1 x hx.1 hx.2)
    refine le_antisymm (le_trans (MeasureTheory.measure_mono hsub) ?_) ?_
    · simp [Real.volume_singleton]
    · exact zero_le
  · have hempty : t \ s = ∅ := by
      rw [Set.eq_empty_iff_forall_notMem]
      intro x hx
      obtain ⟨hxt, hxs⟩ := (Set.mem_sdiff x).1 hx
      exact absurd (h2 x hxt) hxs
    rw [hempty, MeasureTheory.measure_empty]

/-- peel (r-side): the inner integral over `[-r, r]` as an integral over
    `[-1, 1]` against the indicator of `Ioc (-r) r` (`r` in `[0,1]`; all steps
    exact). -/
theorem peel_r (r : ℝ) (hr0 : 0 ≤ r) (hr1 : r ≤ 1) (f : ℝ → ℝ) (hf : Continuous f) :
    ∫ v in (-r : ℝ)..r, f v
      = ∫ v in (-1 : ℝ)..1, Set.indicator (Set.Ioc (-r) r) f v := by
  rw [intervalIntegral_eq_integral_uIoc f (-r) r MeasureTheory.volume,
      intervalIntegral_eq_integral_uIoc (Set.indicator (Set.Ioc (-r) r) f) (-1) 1
        MeasureTheory.volume]
  rw [if_pos (by linarith : (-r : ℝ) ≤ r), if_pos (by norm_num : (-1 : ℝ) ≤ 1)]
  simp only [one_smul]
  rw [MeasureTheory.setIntegral_indicator measurableSet_Ioc]
  have hset : Set.uIoc (-1 : ℝ) 1 ∩ Set.Ioc (-r) r = Set.Ioc (-r) r := by
    have hsub : Set.Ioc (-r) r ⊆ Set.Ioc (-1 : ℝ) 1 := by
      intro x hx
      obtain ⟨h3, h4⟩ := Set.mem_Ioc.1 hx
      exact Set.mem_Ioc.2 ⟨by linarith, by linarith⟩
    rw [Set.uIoc_of_le (by norm_num), Set.inter_eq_right.2 hsub]
  rw [hset, ← Set.uIoc_of_le (show (-r : ℝ) ≤ r by linarith)]

/-- peel (v-side): the integral over `[0, 1]` of the indicator of `Ici |v|`
    equals the integral over `[|v|, 1]` (the sets differ only at `r = |v|`). -/
theorem peel_v (v : ℝ) (hv : |v| ≤ 1) (g : ℝ → ℝ) (hg : Continuous g) :
    ∫ r in (0 : ℝ)..1, Set.indicator (Set.Ici |v|) g r = ∫ r in |v|..1, g r := by
  rw [intervalIntegral_eq_integral_uIoc (Set.indicator (Set.Ici |v|) g) 0 1
        MeasureTheory.volume,
      intervalIntegral_eq_integral_uIoc g |v| 1 MeasureTheory.volume]
  rw [if_pos (by norm_num : (0 : ℝ) ≤ 1), if_pos hv]
  simp only [one_smul]
  rw [Set.uIoc_of_le (by norm_num : (0 : ℝ) ≤ 1), Set.uIoc_of_le hv,
    MeasureTheory.setIntegral_indicator measurableSet_Ici]
  refine setIntegral_congr_of_singleton_diff _ _ (measurableSet_Ioc.inter measurableSet_Ici)
    measurableSet_Ioc |v| g (fun x hx hxnt => ?_) (fun x hx => ?_)
  · simp only [Set.mem_inter_iff, Set.mem_Ioc, Set.mem_Ici] at hx
    obtain ⟨⟨hx0, hx1⟩, hx2⟩ := hx
    have hle : ¬ |v| < x := by
      rintro hlt
      exact hxnt ⟨hlt, hx1⟩
    exact le_antisymm (le_of_not_gt hle) hx2
  · simp only [Set.mem_Ioc] at hx
    exact ⟨⟨lt_of_le_of_lt (abs_nonneg v) hx.1, hx.2⟩, le_of_lt hx.1⟩

/-- helper: the antiderivative-slope arithmetic for `u > 0`. -/
theorem deriv_arith (r u : ℝ) (hu : 0 < u) :
    r * Real.sqrt u
      = -(1/3) * ((0 - 2 * r) * Real.sqrt u
          + u * ((1 / (2 * Real.sqrt u)) * (0 - 2 * r))) := by
  have hA : Real.sqrt u ≠ 0 := (Real.sqrt_ne_zero (le_of_lt hu)).mpr (ne_of_gt hu)
  have hsq : Real.sqrt u ^ 2 = u := Real.sq_sqrt (le_of_lt hu)
  rw [show (0 : ℝ) - 2 * r = -(2 * r) by ring]
  field_simp [hA, hsq]
  rw [hsq]
  ring

/-- step 4: `int_{|v|}^{1} r sqrt(1-r^2+v^2) dr = (1-|v|^3)/3` for `|v| ≤ 1`,
    via `Fv r = -(1/3)(1-r^2+v^2)^{3/2}` (written `-(1/3) u sqrt u`); the FTC
    variant used needs differentiability only on the OPEN interval. -/
theorem step4 (v : ℝ) (hv : |v| ≤ 1) :
    ∫ r in |v|..1, r * Real.sqrt (1 - r ^ 2 + v ^ 2) = (1 - |v| ^ 3) / 3 := by
  set Fv : ℝ → ℝ := fun r => -(1/3) * ((1 + v ^ 2 - r ^ 2) * Real.sqrt (1 + v ^ 2 - r ^ 2))
    with hFv
  have hu_pos : ∀ r ∈ Set.Ico |v| 1, 0 < 1 + v ^ 2 - r ^ 2 := by
    intro r hr
    rw [Set.mem_Ico] at hr
    have h0 : 0 ≤ r := le_trans (abs_nonneg v) hr.1
    have h2 : 0 < 1 - r ^ 2 := by nlinarith [sq_nonneg (r - 1)]
    nlinarith
  have hcont : ContinuousOn Fv (Set.uIcc |v| 1) := by fun_prop
  have hdiff : ∀ r ∈ Set.uIoo |v| 1, DifferentiableAt ℝ Fv r := by
    intro r hr
    rw [Set.uIoo_of_le (by linarith), Set.mem_Ioo] at hr
    have hmem : r ∈ Set.Ico |v| 1 := ⟨le_of_lt hr.1, hr.2⟩
    have hu0 : 0 < 1 + v ^ 2 - r ^ 2 := hu_pos r hmem
    have hdu : DifferentiableAt ℝ (fun x : ℝ => 1 + v ^ 2 - x ^ 2) r := by fun_prop
    have hdsqrt : DifferentiableAt ℝ Real.sqrt (1 + v ^ 2 - r ^ 2) :=
      (Real.hasDerivAt_sqrt (ne_of_gt hu0)).differentiableAt
    have hcomp : DifferentiableAt ℝ
        (fun x : ℝ => (1 + v ^ 2 - x ^ 2) * Real.sqrt (1 + v ^ 2 - x ^ 2)) r :=
      hdu.mul (DifferentiableAt.comp r hdsqrt hdu)
    exact (differentiableAt_const _).mul hcomp
  have hderiv : ∀ r ∈ Set.Ico |v| 1, deriv Fv r = r * Real.sqrt (1 - r ^ 2 + v ^ 2) := by
    intro r hr
    rw [Set.mem_Ico] at hr
    have hu0 : 0 < 1 + v ^ 2 - r ^ 2 := hu_pos r hr
    have hsq : HasDerivAt (fun x : ℝ => x ^ 2) (2 * r) r := by
      simpa using hasDerivAt_pow 2 r
    have hdu : HasDerivAt (fun x : ℝ => 1 + v ^ 2 - x ^ 2) (0 - 2 * r) r :=
      (hasDerivAt_const r ((1 : ℝ) + v ^ 2)).sub hsq
    have hsqrt : HasDerivAt (fun x : ℝ => Real.sqrt (1 + v ^ 2 - x ^ 2))
        ((1 / (2 * Real.sqrt (1 + v ^ 2 - r ^ 2))) * (0 - 2 * r)) r :=
      HasDerivAt.comp r (Real.hasDerivAt_sqrt (ne_of_gt hu0)) hdu
    have hprod : HasDerivAt Fv (r * Real.sqrt (1 - r ^ 2 + v ^ 2)) r := by
      have hform : ∀ x : ℝ, 1 - x ^ 2 + v ^ 2 = 1 + v ^ 2 - x ^ 2 := by
        intro x; ring
      rw [hFv, hform]
      have h1 : HasDerivAt (fun x : ℝ => (1 + v ^ 2 - x ^ 2) * Real.sqrt (1 + v ^ 2 - x ^ 2))
          ((0 - 2 * r) * Real.sqrt (1 + v ^ 2 - r ^ 2)
            + (1 + v ^ 2 - r ^ 2) * ((1 / (2 * Real.sqrt (1 + v ^ 2 - r ^ 2))) * (0 - 2 * r))) r :=
        hdu.mul hsqrt
      have h2 : HasDerivAt (fun x : ℝ => -(1 / 3) * ((1 + v ^ 2 - x ^ 2) * Real.sqrt (1 + v ^ 2 - x ^ 2)))
          (-(1 / 3) * ((0 - 2 * r) * Real.sqrt (1 + v ^ 2 - r ^ 2)
            + (1 + v ^ 2 - r ^ 2) * ((1 / (2 * Real.sqrt (1 + v ^ 2 - r ^ 2))) * (0 - 2 * r)))) r :=
        h1.const_mul (-(1 / 3))
      convert h2 using 1
      exact deriv_arith r (1 + v ^ 2 - r ^ 2) hu0
    rw [show deriv Fv r = r * Real.sqrt (1 - r ^ 2 + v ^ 2) from hprod.deriv]
  have hae : ∀ᵐ r ∂MeasureTheory.volume, r ∈ Set.uIoc |v| 1 →
      (fun r => r * Real.sqrt (1 - r ^ 2 + v ^ 2)) r = deriv Fv r := by
    rw [MeasureTheory.ae_iff]
    refine le_antisymm
      (le_trans (MeasureTheory.measure_mono (t := {r : ℝ | r = 1}) ?_)
        (by simp [Real.volume_singleton])) zero_le
    · intro x hx
      simp only [Set.mem_setOf_eq, not_imp] at hx
      obtain ⟨hxmem, hne⟩ := hx
      rw [Set.uIoc_of_le hv] at hxmem
      obtain ⟨hlt, hle⟩ := Set.mem_Ioc.1 hxmem
      have hnic : x ∉ Set.Ico |v| 1 := by
        intro hmem2
        exact hne (hderiv x hmem2).symm
      have hge : x ≥ 1 := le_of_not_gt fun hlt2 => hnic ⟨le_of_lt hlt, hlt2⟩
      exact Set.mem_singleton_iff.2 (le_antisymm hle hge)
  have hint : IntervalIntegrable (deriv Fv) MeasureTheory.volume |v| 1 := by
    refine IntervalIntegrable.congr_ae (f := fun r => r * Real.sqrt (1 - r ^ 2 + v ^ 2))
      (intBdd _ |v| 1 (by fun_prop)) ?_
    exact (MeasureTheory.ae_restrict_iff' measurableSet_uIoc).2 hae
  have hftc : ∫ r in |v|..1, deriv Fv r = Fv 1 - Fv |v| :=
    integral_deriv_eq_sub_uIoo hcont hdiff hint
  have hconv : ∫ r in |v|..1, r * Real.sqrt (1 - r ^ 2 + v ^ 2) = Fv 1 - Fv |v| := by
    rw [integral_congr_ae (a := |v|) (b := 1) hae, hftc]
  rw [hconv]
  have hab : |v| ^ 2 = v ^ 2 := by
    have h1 : |v| ^ 2 = |v| * |v| := by ring
    rw [h1, abs_mul_abs_self v]
    ring
  have hv3 : |v| ^ 3 = v ^ 2 * |v| := by
    have h1 : |v| ^ 3 = |v| * |v| * |v| := by ring
    rw [h1, abs_mul_abs_self v]
    ring
  have hFv1 : Fv 1 = -(1 / 3) * (v ^ 2 * |v|) := by
    show -(1 / 3) * ((1 + v ^ 2 - 1 ^ 2) * Real.sqrt (1 + v ^ 2 - 1 ^ 2)) = _
    rw [show (1 : ℝ) + v ^ 2 - 1 ^ 2 = v ^ 2 by ring, Real.sqrt_sq_eq_abs v]
  have hFvm : Fv |v| = -(1 / 3) := by
    show -(1 / 3) * ((1 + v ^ 2 - |v| ^ 2) * Real.sqrt (1 + v ^ 2 - |v| ^ 2)) = _
    rw [hab, show (1 : ℝ) + v ^ 2 - v ^ 2 = 1 by ring, Real.sqrt_one]
    ring
  rw [hFv1, hFvm, ← hv3]
  ring

/-- `int_{-1}^{1} (1-|v|^3)/3 dv = 1/2`. -/
theorem final_half : ∫ v in (-1 : ℝ)..1, (1 - |v| ^ 3) / 3 = 1 / 2 := by
  have hint : ∀ c d : ℝ, ∫ v in c..d, deriv (fun y : ℝ => (y - y ^ 4 / 4) / 3) v
      = (d - d ^ 4 / 4) / 3 - (c - c ^ 4 / 4) / 3 := by
    intro c d
    have hfun : deriv (fun y : ℝ => (y - y ^ 4 / 4) / 3) = (fun y : ℝ => (1 - y ^ 3) / 3) := by
      funext y
      have h2 : HasDerivAt (fun y : ℝ => y - y ^ 4 / 4) (1 - y ^ 3) y := by
        have hy : HasDerivAt (fun y : ℝ => y) 1 y := hasDerivAt_id y
        have h4 : HasDerivAt (fun y : ℝ => y ^ 4 / 4) (y ^ 3) y := by
          simpa using (hasDerivAt_pow 4 y).div_const 4
        exact hy.sub h4
      have h3 : HasDerivAt (fun y : ℝ => (y - y ^ 4 / 4) / 3) ((1 - y ^ 3) / 3) y :=
        h2.div_const 3
      rw [h3.deriv]
    have hdiff : ∀ x ∈ Set.uIcc c d, DifferentiableAt ℝ (fun y : ℝ => (y - y ^ 4 / 4) / 3) x :=
      fun x _ => by fun_prop
    calc ∫ v in c..d, deriv (fun y : ℝ => (y - y ^ 4 / 4) / 3) v
        = ∫ v in c..d, (1 - v ^ 3) / 3 := by
          refine integral_congr (a := c) (b := d) (fun v _ => ?_)
          rw [hfun]
      _ = (d - d ^ 4 / 4) / 3 - (c - c ^ 4 / 4) / 3 :=
          integral_deriv_eq_sub' (fun y : ℝ => (y - y ^ 4 / 4) / 3) hfun hdiff (by fun_prop)
  have hintp : ∀ c d : ℝ, ∫ v in c..d, deriv (fun y : ℝ => (y + y ^ 4 / 4) / 3) v
      = (d + d ^ 4 / 4) / 3 - (c + c ^ 4 / 4) / 3 := by
    intro c d
    have hfun : deriv (fun y : ℝ => (y + y ^ 4 / 4) / 3) = (fun y : ℝ => (1 + y ^ 3) / 3) := by
      funext y
      have h2 : HasDerivAt (fun y : ℝ => y + y ^ 4 / 4) (1 + y ^ 3) y := by
        have hy : HasDerivAt (fun y : ℝ => y) 1 y := hasDerivAt_id y
        have h4 : HasDerivAt (fun y : ℝ => y ^ 4 / 4) (y ^ 3) y := by
          simpa using (hasDerivAt_pow 4 y).div_const 4
        exact hy.add h4
      have h3 : HasDerivAt (fun y : ℝ => (y + y ^ 4 / 4) / 3) ((1 + y ^ 3) / 3) y :=
        h2.div_const 3
      rw [h3.deriv]
    have hdiff : ∀ x ∈ Set.uIcc c d, DifferentiableAt ℝ (fun y : ℝ => (y + y ^ 4 / 4) / 3) x :=
      fun x _ => by fun_prop
    calc ∫ v in c..d, deriv (fun y : ℝ => (y + y ^ 4 / 4) / 3) v
        = ∫ v in c..d, (1 + v ^ 3) / 3 := by
          refine integral_congr (a := c) (b := d) (fun v _ => ?_)
          rw [hfun]
      _ = (d + d ^ 4 / 4) / 3 - (c + c ^ 4 / 4) / 3 :=
          integral_deriv_eq_sub' (fun y : ℝ => (y + y ^ 4 / 4) / 3) hfun hdiff (by fun_prop)
  have hsplit : (∫ x in (-1 : ℝ)..0, (1 - |x| ^ 3) / 3)
      + (∫ x in (0 : ℝ)..1, (1 - |x| ^ 3) / 3) = ∫ x in (-1 : ℝ)..1, (1 - |x| ^ 3) / 3 :=
    integral_add_adjacent_intervals (a := (-1 : ℝ)) (b := 0) (c := 1)
      (f := fun x => (1 - |x| ^ 3) / 3) (μ := MeasureTheory.volume)
      (intBdd (fun x => (1 - |x| ^ 3) / 3) (-1) 0 (by fun_prop))
      (intBdd (fun x => (1 - |x| ^ 3) / 3) 0 1 (by fun_prop))
  have hint_neg : ∫ v in (-1 : ℝ)..0, (1 - |v| ^ 3) / 3 = 1 / 4 := by
    have hEq : Set.EqOn (fun v => (1 - |v| ^ 3) / 3)
        (fun v => deriv (fun y : ℝ => (y + y ^ 4 / 4) / 3) v) (Set.uIcc (-1) 0) := by
      intro v hv
      rw [Set.uIcc_of_le (by norm_num : (-1 : ℝ) ≤ 0), Set.mem_Icc] at hv
      obtain ⟨hv1, hv0⟩ := hv
      show (1 - |v| ^ 3) / 3 = deriv (fun y : ℝ => (y + y ^ 4 / 4) / 3) v
      rw [abs_of_nonpos hv0]
      have hd : deriv (fun y : ℝ => (y + y ^ 4 / 4) / 3) v = (1 + v ^ 3) / 3 := by
        have h2 : HasDerivAt (fun y : ℝ => y + y ^ 4 / 4) (1 + v ^ 3) v := by
          have hy : HasDerivAt (fun y : ℝ => y) 1 v := hasDerivAt_id v
          have h4 : HasDerivAt (fun y : ℝ => y ^ 4 / 4) (v ^ 3) v := by
            simpa using (hasDerivAt_pow 4 v).div_const 4
          exact hy.add h4
        exact (h2.div_const 3).deriv
      rw [hd]
      ring
    rw [integral_congr (a := -1) (b := 0) hEq, hintp (-1 : ℝ) (0 : ℝ)]
    ring
  have hint_pos : ∫ v in (0 : ℝ)..1, (1 - |v| ^ 3) / 3 = 1 / 4 := by
    have hEq : Set.EqOn (fun v => (1 - |v| ^ 3) / 3)
        (fun v => deriv (fun y : ℝ => (y - y ^ 4 / 4) / 3) v) (Set.uIcc 0 1) := by
      intro v hv
      rw [Set.uIcc_of_le (by norm_num : (0 : ℝ) ≤ 1), Set.mem_Icc] at hv
      obtain ⟨hv0, hv1⟩ := hv
      show (1 - |v| ^ 3) / 3 = deriv (fun y : ℝ => (y - y ^ 4 / 4) / 3) v
      rw [abs_of_nonneg hv0]
      have hd : deriv (fun y : ℝ => (y - y ^ 4 / 4) / 3) v = (1 - v ^ 3) / 3 := by
        have h2 : HasDerivAt (fun y : ℝ => y - y ^ 4 / 4) (1 - v ^ 3) v := by
          have hy : HasDerivAt (fun y : ℝ => y) 1 v := hasDerivAt_id v
          have h4 : HasDerivAt (fun y : ℝ => y ^ 4 / 4) (v ^ 3) v := by
            simpa using (hasDerivAt_pow 4 v).div_const 4
          exact hy.sub h4
        exact (h2.div_const 3).deriv
      rw [hd]
    rw [integral_congr (a := 0) (b := 1) hEq, hint (0 : ℝ) (1 : ℝ)]
    ring
  rw [← hsplit, hint_neg, hint_pos]
  ring

end V01

#print axioms V01.step4
#print axioms V01.final_half
#print axioms V01.peel_r
#print axioms V01.peel_v
#print axioms V01.step2
#print axioms V01.inner_eq
