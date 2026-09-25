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

/-! ## Stage C (W01, 2026-09-25, W-WAVE_BRIEF.md): the Fubini-flip assembly.
Goal: chordMomentVol = 3/2 * Jtri (inner_eq + step2 + linearity), then the
triangle flip Jtri = 1/2, hence chordMomentVol = 3/4 -- closing M01's single
CONJECTURED item with the 2D change of variables still avoided. -/

noncomputable section
namespace V01

/-- The flipped triangle integrand `r * sqrt(1 - r^2 + v^2)`. -/
def tri (r v : ℝ) : ℝ := r * Real.sqrt (1 - r ^ 2 + v ^ 2)

/-- The triangle moment J. -/
def Jtri : ℝ := ∫ r in (0 : ℝ)..1, (∫ v in (-r : ℝ)..r, tri r v)

/-- The 2-argument form of the r-peeled integrand. -/
def G (r v : ℝ) : ℝ := Set.indicator (Set.Ioc (-r) r) (tri r) v

theorem tri_cont1 (r : ℝ) : Continuous (tri r) := by
  unfold tri
  exact continuous_const.mul
    (Real.continuous_sqrt.comp
      (by fun_prop : Continuous (fun v : ℝ => 1 - r ^ 2 + v ^ 2)))

theorem tri_cont2 (v : ℝ) : Continuous (fun x => tri x v) := by
  unfold tri
  fun_prop

/-- pointwise bound: |G r v| <= 2 on the box (r in [0,1], |v| <= 1). -/
theorem G_bound {r v : ℝ} (hr0 : 0 ≤ r) (hr1 : r ≤ 1) (hv : |v| ≤ 1) : |G r v| ≤ 2 := by
  have hr2 : r ^ 2 ≤ 1 := by nlinarith [sq_nonneg (r - 1)]
  have hv2 : v ^ 2 ≤ 1 := by
    rcases abs_le.mp hv with ⟨h1, h2⟩
    have h3 : 0 ≤ (1 - v) * (1 + v) :=
      mul_nonneg (by linarith) (by linarith)
    nlinarith [h3]
  have htri : |tri r v| ≤ 2 := by
    unfold tri
    rw [abs_mul, abs_of_nonneg hr0, abs_of_nonneg (Real.sqrt_nonneg _)]
    calc r * Real.sqrt (1 - r ^ 2 + v ^ 2) ≤ 1 * Real.sqrt (1 - r ^ 2 + v ^ 2) :=
          mul_le_mul_of_nonneg_right hr1 (Real.sqrt_nonneg _)
      _ = Real.sqrt (1 - r ^ 2 + v ^ 2) := (one_mul (Real.sqrt (1 - r ^ 2 + v ^ 2)))
      _ ≤ Real.sqrt 2 := Real.sqrt_le_sqrt (by nlinarith [hr2, hv2])
      _ ≤ 2 := by
          have hsq : Real.sqrt 2 * Real.sqrt 2 = 2 := by
            rw [← pow_two, Real.sq_sqrt (le_of_lt (by norm_num : (0:ℝ) < 2))]
          have hpos : 0 ≤ Real.sqrt 2 := Real.sqrt_nonneg 2
          by_contra hgt
          push_neg at hgt
          nlinarith [hsq, hpos, hgt]
  unfold G
  by_cases hmem : v ∈ Set.Ioc (-r) r
  · rw [Set.indicator_of_mem hmem]
    exact htri
  · rw [Set.indicator_apply, if_neg hmem]
    norm_num

/-- `G.uncurry` is measurable. -/
theorem G_measurable : Measurable (fun p : ℝ × ℝ => G p.1 p.2) := by
  have hf : Measurable (fun p : ℝ × ℝ => -p.1) := measurable_fst.neg
  have hs : MeasurableSet {p : ℝ × ℝ | -p.1 < p.2 ∧ p.2 ≤ p.1} :=
    (measurableSet_lt hf measurable_snd).inter
      (measurableSet_le measurable_snd measurable_fst)
  have hfm : Measurable (fun q : ℝ × ℝ => tri q.1 q.2) := by
    unfold tri
    fun_prop
  have heq : (fun p : ℝ × ℝ => G p.1 p.2)
      = {p : ℝ × ℝ | -p.1 < p.2 ∧ p.2 ≤ p.1}.indicator
          (fun q : ℝ × ℝ => tri q.1 q.2) := by
    funext p
    simp only [G, Set.indicator_apply, Set.mem_ofPred_eq, Set.mem_Ioc]
  rw [heq]
  exact hfm.indicator hs

/-- integrability of the indicator integrand on the box. -/
theorem G_integrable : MeasureTheory.IntegrableOn (fun p : ℝ × ℝ => G p.1 p.2)
    (Set.uIoc (0 : ℝ) 1 ×ˢ Set.uIoc (-1 : ℝ) 1) := by
  rw [Set.uIoc_of_le (by norm_num : (0 : ℝ) ≤ 1), Set.uIoc_of_le (by norm_num : (-1 : ℝ) ≤ 1)]
  unfold MeasureTheory.IntegrableOn
  refine ⟨G_measurable.aestronglyMeasurable, ?_⟩
  refine MeasureTheory.HasFiniteIntegral.restrict_of_bounded 2 ?_ ?_
  · have h1 : MeasureTheory.volume (Set.Ioc (0:ℝ) 1 ×ˢ Set.Ioc (-1:ℝ) 1)
        = MeasureTheory.volume (Set.Ioc (0:ℝ) 1) * MeasureTheory.volume (Set.Ioc (-1:ℝ) 1) :=
      MeasureTheory.Measure.prod_prod (s := Set.Ioc (0:ℝ) 1) (t := Set.Ioc (-1:ℝ) 1)
    rw [h1, Real.volume_Ioc, Real.volume_Ioc]
    norm_num
  · refine (MeasureTheory.ae_restrict_iff' (measurableSet_Ioc.prod measurableSet_Ioc)).2 ?_
    refine Filter.Eventually.of_forall (fun x hx => ?_)
    obtain ⟨hx1, hx2⟩ := hx
    have hr0 : (0 : ℝ) ≤ x.1 := le_of_lt hx1.1
    have hr1 : x.1 ≤ 1 := hx1.2
    have hneg : -(1 : ℝ) ≤ x.2 := le_of_lt hx2.1
    have hv : |x.2| ≤ 1 := abs_le.2 ⟨hneg, hx2.2⟩
    simpa [Real.norm_eq_abs] using G_bound hr0 hr1 hv

/-- step 2 lifted through the outer integral: chordMomentVol = 3/2 * Jtri. -/
theorem step2_all : chordMomentVol = 3 / 2 * Jtri := by
  have hcong : ∀ r ∈ Set.uIcc (0 : ℝ) 1,
      r ^ 2 * (1 / 2 * (∫ μ in (-1 : ℝ)..1, chord r μ))
        = 1 / 2 * (∫ v in (-r : ℝ)..r, tri r v) := by
    intro r hr
    rw [Set.uIcc_of_le (by norm_num : (0 : ℝ) ≤ 1), Set.mem_Icc] at hr
    rw [inner_eq r,
      show r ^ 2 * (1 / 2 * (∫ μ in (-1 : ℝ)..1, Real.sqrt (1 - r ^ 2 + r ^ 2 * μ ^ 2)))
        = 1 / 2 * (r ^ 2 * (∫ μ in (-1 : ℝ)..1, Real.sqrt (1 - r ^ 2 + r ^ 2 * μ ^ 2))) by ring,
      step2 r hr.1 hr.2]
    congr 1
    simp only [tri]
    rw [integral_const_mul]
  show 3 * (∫ r in (0 : ℝ)..1, r ^ 2 * (1 / 2 * (∫ μ in (-1 : ℝ)..1, chord r μ))) = _
  rw [integral_congr hcong]
  simp only [Jtri]
  rw [integral_const_mul]
  ring

/-- Peel the inner integral to the fixed rectangle [0,1] x [-1,1]. -/
theorem J_as_G : Jtri = ∫ r in (0 : ℝ)..1,
    (∫ v in (-1 : ℝ)..1, G r v) := by
  show (∫ r in (0 : ℝ)..1, (∫ v in (-r : ℝ)..r, tri r v)) = _
  refine integral_congr (fun r hr => ?_)
  rw [Set.uIcc_of_le (by norm_num : (0 : ℝ) ≤ 1), Set.mem_Icc] at hr
  exact peel_r r hr.1 hr.2 (tri r) (tri_cont1 r)

/-- The per-point comparison lemma: G r v equals the v-side indicator unless
    v < 0 and r = |v| (the measure-zero diagonal). -/
theorem G_eq_or_edge {r v : ℝ} (hr0 : 0 ≤ r) (hr1 : r ≤ 1) :
    G r v = Set.indicator (Set.Ici |v|) (fun x => tri x v) r ∨ (v < 0 ∧ r = |v|) := by
  simp only [G, Set.indicator_apply, Set.mem_Ioc, Set.mem_Ici]
  by_cases hL : (-r < v ∧ v ≤ r)
  · rcases hL with ⟨h1, h2⟩
    rcases abs_cases v with hv | hv
    · left
      rw [hv.1]
      simp [h1, h2, tri]
    · left
      rw [hv.1]
      have h3 : -v ≤ r := by linarith
      simp [h1, h2, h3, tri]
  · by_cases hR : |v| ≤ r
    · rcases abs_cases v with hv | hv
      · rcases eq_or_lt_of_le hr0 with rfl | hrp
        · left
          have hvz : v = 0 := le_antisymm (by rw [hv.1] at hR; linarith) hv.2
          subst hvz
          simp [tri]
        · exfalso
          have h2 : v ≤ r := by rw [hv.1] at hR; exact hR
          exact hL ⟨by linarith, h2⟩
      · right
        refine ⟨hv.2, ?_⟩
        rw [hv.1] at hR ⊢
        have hnv : ¬(-r < v) := fun h => hL ⟨h, by linarith⟩
        have h1 : r ≤ -v := by linarith
        exact le_antisymm h1 hR
    · left
      simp [hL, hR]

/-- Per fixed v, the r-integral of G over [0,1] is the flipped-ordered
    integral over [|v|, 1] (peel_v; the diagonal r = |v| is null). -/
theorem inner_flip (v : ℝ) (hv : |v| ≤ 1) :
    (∫ r in (0 : ℝ)..1, G r v) = ∫ r in |v|..1, tri r v := by
  have h1 : (∫ r in (0 : ℝ)..1, G r v)
      = ∫ r in (0 : ℝ)..1, Set.indicator (Set.Ici |v|) (fun x => tri x v) r := by
    refine integral_congr_ae ?_
    rw [MeasureTheory.ae_iff]
    refine le_antisymm
      (le_trans (MeasureTheory.measure_mono (t := {r : ℝ | r = |v|}) ?_)
        (by simp [Real.volume_singleton])) zero_le
    intro r hr
    simp only [not_imp] at hr
    obtain ⟨hmem, hne⟩ := hr
    rw [Set.uIoc_of_le (by norm_num : (0 : ℝ) ≤ 1), Set.mem_Ioc] at hmem
    rcases G_eq_or_edge hmem.1.le hmem.2 with heq | hbad
    · exact absurd heq hne
    · exact hbad.2
  rw [h1, peel_v v hv (fun x => tri x v) (tri_cont2 v)]

/-- The Fubini flip over the rectangle (mathlib's interval-integral swap). -/
theorem J_swap : (∫ r in (0 : ℝ)..1, (∫ v in (-1 : ℝ)..1, G r v))
    = ∫ v in (-1 : ℝ)..1, (∫ r in (0 : ℝ)..1, G r v) :=
  MeasureTheory.intervalIntegral_intervalIntegral_swap (F := G) G_integrable

/-- Jtri = 1/2 (flip + step4 + final_half). -/
theorem J_value : Jtri = 1 / 2 := by
  rw [J_as_G, J_swap]
  have houter : (∫ v in (-1 : ℝ)..1, (∫ r in (0 : ℝ)..1, G r v))
      = ∫ v in (-1 : ℝ)..1, (1 - |v| ^ 3) / 3 := by
    refine integral_congr (fun v hv => ?_)
    rw [Set.uIcc_of_le (by norm_num : (-1 : ℝ) ≤ 1), Set.mem_Icc] at hv
    have hv1 : |v| ≤ 1 := abs_le.2 ⟨by linarith, hv.2⟩
    rw [inner_flip v hv1]
    exact step4 v hv1
  rw [houter, final_half]

/-- MAIN: M01's conjectured volume-chord moment, certified. -/
theorem chord_moment_main : chordMomentVol = 3 / 4 := by
  rw [step2_all, J_value]
  ring

end V01

#print axioms V01.step2_all
#print axioms V01.J_as_G
#print axioms V01.G_measurable
#print axioms V01.G_integrable
#print axioms V01.G_eq_or_edge
#print axioms V01.inner_flip
#print axioms V01.J_swap
#print axioms V01.J_value
#print axioms V01.chord_moment_main
