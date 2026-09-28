/-
AS045 — Heat filter operator domain of definition (MONO branch, filtered nu_mono).
Lean certificate: the Fourier-multiplier action of the heat filter
S = exp[(xi^2/2) Delta] on plane waves, and the Gaussian convolution semigroup
composition law. These are the algebraic facts behind the operator-domain audit:

  (T1) heat_filter_multiplier:
       ∫_ℝ exp(-(x-y)^2/(2 ξ²)) · exp(i k y) dy = √(2π)·ξ · exp(i k x - ξ² k²/2)
       — i.e., in the normalized form (T2), (S e^{ik·})(x) = e^{-ξ²k²/2} e^{ikx},
       the symbol (Fourier multiplier) of S is m(k) = exp(-ξ²|k|²/2).
       Setting k = 0 gives the translation-invariant kernel mass
       ∫_ℝ exp(-(x-y)^2/(2 ξ²)) dy = √(2π)·ξ.

  (T3) heat_filter_semigroup:
       ∫_ℝ exp(-(x-y)^2/(2a)) · exp(-(y-z)^2/(2b)) dy
         = √(2πab/(a+b)) · exp(-(x-z)^2/(2(a+b)))
       — the real-space product law  S_a ∘ S_b = S_{a+b}  (the heat semigroup at
       t = ξ²/2:  S(ξ1) S(ξ2) = S(√(ξ1²+ξ2²)) for all ξ1, ξ2 > 0).

All integrals are Bochner (Lebesgue) over ℝ with values in ℂ; the identities are
Euclidean-measure statements (the operator-cell facts behind the boundedness and
smoothness legs of the audit of S* div[(nu_mono-1) grad S u]).
-/
import Mathlib

open scoped Real
open MeasureTheory
open Complex hiding exp continuous_exp

noncomputable section

namespace AS045

/-- Complex half-powers of nonnegative reals are the square root. -/
lemma half_cpow_of_nonneg (x : ℝ) (hx : 0 ≤ x) : (x : ℂ) ^ (1 / 2 : ℂ) = ↑(Real.sqrt x) := by
  have hco : (1 / 2 : ℂ) = ↑(1 / 2 : ℝ) := by norm_num
  rw [hco]
  rw [← Complex.ofReal_cpow hx (1 / 2 : ℝ)]
  congr 1
  rw [Real.sqrt_eq_rpow]

/-- The unnormalized heat-filter factor: (π/b)^(1/2) for b = 1/(2ξ²) is √(2π)·ξ.
Division electrons are double-ascripted (ℝ then ℂ) — the bare `↑(1 / ...)` parse trap. -/
lemma heat_filter_factor (xi : ℝ) (hxi : 0 < xi) :
    (↑Real.pi / (((1 / (2 * xi ^ 2)) : ℝ) : ℂ)) ^ (1 / 2 : ℂ) =
      ↑(Real.sqrt (2 * Real.pi) * xi) := by
  have hdiv : ↑Real.pi / (((1 / (2 * xi ^ 2)) : ℝ) : ℂ) =
      ↑((2 : ℝ) * Real.pi * xi ^ 2) := by
    push_cast
    field_simp [hxi.ne']
  rw [hdiv]
  rw [half_cpow_of_nonneg (((2 : ℝ) * Real.pi * xi ^ 2) : ℝ)
    (by positivity : 0 ≤ (2 : ℝ) * Real.pi * xi ^ 2)]
  congr 1
  rw [show (2 : ℝ) * Real.pi * xi ^ 2 = (2 * Real.pi) * xi ^ 2 by ring]
  rw [Real.sqrt_mul (by positivity : 0 ≤ 2 * Real.pi) (xi ^ 2)]
  rw [Real.sqrt_sq hxi.le]

/-- T1: the heat filter applied to a plane wave of wavenumber k multiplies it by
the symbol exp(-ξ² k²/2) (unnormalized kernel; the pre-factor √(2π)·ξ is the
kernel mass, independent of the center x). -/
theorem heat_filter_multiplier (xi k x : ℝ) (hxi : 0 < xi) :
    (∫ y : ℝ, cexp (((-(((x - y) ^ 2) / ((2 : ℝ) * xi ^ 2))) : ℝ) : ℂ) *
        cexp (I * ((k : ℂ) * (y : ℂ)))) =
      ↑(Real.sqrt (2 * Real.pi) * xi) *
        cexp (-(((xi ^ 2 * k ^ 2) : ℝ) : ℂ) / (2 : ℂ) + I * ((k : ℂ) * (x : ℂ))) := by
  let bre : ℝ := 1 / (2 * xi ^ 2)
  let b : ℂ := -(((bre : ℝ) : ℂ))
  let c : ℂ := (((x / xi ^ 2) : ℝ) : ℂ) + I * (k : ℂ)
  let d : ℂ := -(((x ^ 2 / (2 * xi ^ 2)) : ℝ) : ℂ)
  have hb : b.re < 0 := by
    dsimp [bre, b]
    exact neg_lt_zero.mpr (by positivity : 0 < (1 / (2 * xi ^ 2) : ℝ))
  have hcalc := integral_cexp_quadratic hb c d
  have hexp_arg (y : ℝ) :
      (((-(((x - y) ^ 2) / ((2 : ℝ) * xi ^ 2))) : ℝ) : ℂ) + I * ((k : ℂ) * (y : ℂ)) =
        b * ((y : ℂ) ^ 2) + c * (y : ℂ) + d := by
    dsimp [bre, b, c, d]
    push_cast
    field_simp [hxi.ne']
    ring_nf
  have hInt :
      (∫ y : ℝ, cexp (((-(((x - y) ^ 2) / ((2 : ℝ) * xi ^ 2))) : ℝ) : ℂ) *
          cexp (I * ((k : ℂ) * (y : ℂ)))) =
        ∫ y : ℝ, cexp (b * ((y : ℂ) ^ 2) + c * (y : ℂ) + d) := by
    apply integral_congr_ae
    filter_upwards with y
    rw [← Complex.exp_add]
    rw [hexp_arg y]
  have hfac : (π / -b) ^ (1 / 2 : ℂ) = ↑(Real.sqrt (2 * Real.pi) * xi) := by
    dsimp [bre, b]
    rw [neg_neg]
    exact heat_filter_factor xi hxi
  have hexp_exp : d - c ^ 2 / (4 * b) =
      -(((xi ^ 2 * k ^ 2) : ℝ) : ℂ) / (2 : ℂ) + I * ((k : ℂ) * (x : ℂ)) := by
    dsimp [bre, c, d, b]
    push_cast
    field_simp [hxi.ne']
    ring_nf
    rw [Complex.I_sq]
    ring
  rw [hInt, hcalc, hfac]
  congr 1
  rw [hexp_exp]

/-- T2: normalized kernel version — S(e^{ikx}) = e^{-ξ²k²/2} · e^{ikx}, i.e. the
operator S = exp[(ξ²/2)Δ] has Fourier multiplier m(k) = exp(-ξ²|k|²/2) in L²(ℝ). -/
theorem heat_filter_multiplier_normalized (xi k x : ℝ) (hxi : 0 < xi) :
    (∫ y : ℝ, (↑(Real.sqrt (2 * Real.pi * xi ^ 2)))⁻¹ *
        (cexp (((-(((x - y) ^ 2) / ((2 : ℝ) * xi ^ 2))) : ℝ) : ℂ) *
          cexp (I * ((k : ℂ) * (y : ℂ))))) =
      cexp (-(((xi ^ 2 * k ^ 2) : ℝ) : ℂ) / (2 : ℂ)) * cexp (I * ((k : ℂ) * (x : ℂ))) := by
  have hsq : (↑(Real.sqrt (2 * Real.pi * xi ^ 2)) : ℂ) = ↑(Real.sqrt (2 * Real.pi) * xi) := by
    congr 1
    rw [show 2 * Real.pi * xi ^ 2 = (2 * Real.pi) * xi ^ 2 by ring]
    rw [Real.sqrt_mul (by positivity : 0 ≤ 2 * Real.pi) (xi ^ 2)]
    rw [Real.sqrt_sq hxi.le]
  have h := heat_filter_multiplier xi k x hxi
  rw [integral_const_mul]
  rw [h]
  rw [← mul_assoc]
  have hifac : (↑(Real.sqrt (2 * Real.pi) * xi) : ℂ) ≠ 0 := by
    exact ofReal_ne_zero.mpr (ne_of_gt (by positivity : 0 < Real.sqrt (2 * Real.pi) * xi))
  rw [hsq]
  rw [inv_mul_cancel₀ hifac]
  rw [one_mul]
  rw [Complex.exp_add]

/-- The semigroup factor: (π/b)^(1/2) for b = 1/(2a) + 1/(2b) is √(2πab/(a+b)). -/
lemma heat_filter_factor2 (a b : ℝ) (ha : 0 < a) (hb : 0 < b) :
    (↑Real.pi / ((((1 / (2 * a)) + (1 / (2 * b))) : ℝ) : ℂ)) ^ (1 / 2 : ℂ) =
      ↑(Real.sqrt ((2 : ℝ) * Real.pi * a * b / (a + b))) := by
  have hdiv : ↑Real.pi / ((((1 / (2 * a)) + (1 / (2 * b))) : ℝ) : ℂ) =
      ↑(((2 : ℝ) * Real.pi * a * b / (a + b)) : ℝ) := by
    push_cast
    field_simp [ha.ne', hb.ne']
    ring
  rw [hdiv]
  rw [half_cpow_of_nonneg (((2 : ℝ) * Real.pi * a * b / (a + b)) : ℝ)
    (by positivity : 0 ≤ (2 : ℝ) * Real.pi * a * b / (a + b))]

/-- T3: Gaussian convolution semigroup — S(ξ1)∘S(ξ2) = S(√(ξ1²+ξ2²)): with
a = ξ1², b = ξ2², ∫ exp(-(x-y)^2/(2a)) exp(-(y-z)^2/(2b)) dy =
√(2πab/(a+b)) exp(-(x-z)^2/(2(a+b))). -/
theorem heat_filter_semigroup (a b x z : ℝ) (ha : 0 < a) (hb : 0 < b) :
    (∫ y : ℝ, cexp ((((-(((x - y) ^ 2) / ((2 : ℝ) * a))) : ℝ) : ℂ)) *
        cexp ((((-(((y - z) ^ 2) / ((2 : ℝ) * b))) : ℝ) : ℂ))) =
      ↑(Real.sqrt (2 * Real.pi * a * b / (a + b))) *
        cexp ((((-(((x - z) ^ 2) / ((2 : ℝ) * (a + b)))) : ℝ) : ℂ)) := by
  let bbre : ℝ := 1 / (2 * a) + 1 / (2 * b)
  let bb : ℂ := -(((bbre : ℝ) : ℂ))
  let cc : ℂ := (((x / a + z / b) : ℝ) : ℂ)
  let dd : ℂ := -(((x ^ 2 / (2 * a) + z ^ 2 / (2 * b)) : ℝ) : ℂ)
  have hab : 0 < a + b := by positivity
  have hb2 : bb.re < 0 := by
    dsimp [bbre, bb]
    exact neg_lt_zero.mpr (by positivity : 0 < (1 / (2 * a) + 1 / (2 * b) : ℝ))
  have hcalc := integral_cexp_quadratic hb2 cc dd
  have hexp_arg (y : ℝ) :
      (((-(((x - y) ^ 2) / ((2 : ℝ) * a))) : ℝ) : ℂ) +
          (((-(((y - z) ^ 2) / ((2 : ℝ) * b))) : ℝ) : ℂ) =
        bb * ((y : ℂ) ^ 2) + cc * (y : ℂ) + dd := by
    dsimp [bbre, bb, cc, dd]
    push_cast
    field_simp [ha.ne', hb.ne']
    ring_nf
  have hInt :
      (∫ y : ℝ, cexp (((-(((x - y) ^ 2) / ((2 : ℝ) * a))) : ℝ) : ℂ) *
          cexp ((((-(((y - z) ^ 2) / ((2 : ℝ) * b))) : ℝ) : ℂ))) =
        ∫ y : ℝ, cexp (bb * ((y : ℂ) ^ 2) + cc * (y : ℂ) + dd) := by
    apply integral_congr_ae
    filter_upwards with y
    rw [← Complex.exp_add]
    rw [hexp_arg y]
  have hfac : (π / -bb) ^ (1 / 2 : ℂ) = ↑(Real.sqrt (2 * Real.pi * a * b / (a + b))) := by
    dsimp [bbre, bb]
    rw [neg_neg]
    exact heat_filter_factor2 a b ha hb
  have hexp_exp : dd - cc ^ 2 / (4 * bb) =
      (((-(((x - z) ^ 2) / ((2 : ℝ) * (a + b)))) : ℝ) : ℂ) := by
    dsimp [bbre, dd, cc, bb]
    push_cast
    rw [← Complex.ofReal_pow]
    push_cast
    field_simp [ha.ne', hb.ne', hab.ne']
    norm_cast
    field_simp [hab.ne']
    ring
  rw [hInt, hcalc, hfac]
  congr 1
  rw [hexp_exp]

end AS045

#print axioms AS045.heat_filter_multiplier
#print axioms AS045.heat_filter_multiplier_normalized
#print axioms AS045.heat_filter_semigroup