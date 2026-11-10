import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Tactic

/-!
# GRW1: closed forms of the late-growth lane (2026-11-10)

Lane `fable52_push/GRW1_late_growth_baryons_and_law/` (criteria 11c19a2c5f, amendment A1 4dfa022e34).

T-A, the action's linear theory with the law read on the clock's acceleration: the clock's dust part is
δ_d = δ_N / (1 + c q²), so the clock's force coefficient is 1 − q²/(1 + c q²), with
c = (1/(1+x)) (1 − x μ²/(1+x)) the linear response of K P = A a0/(a0 + |A|) about an external field x a0.

1. `ta_coeff_mono`, `ta_coeff_le_cold`, `ta_coeff_one`, `cfac_unit`: the coefficient rises with c, never exceeds the
   cold value 1, equals 1/(1 + q²) at c = 1 (TPA1 4.4 at ε = 1), and 0 ≤ c ≤ 1. So c = 1 with a cold start bounds T-A
   (T-A-max).
2. `aqual_response`: 1 − c = μ_e (1 + L_e μ²), μ_e = x/(1+x), L_e = 1/(1+x): the simple law's AQUAL response.
3. `equilibrium_total`: where (1 − c) q² > 1 the static equilibrium δ_N = r (1 + c q²)/((1 − c) q² − 1) satisfies the
   hydrostatic condition, and the total source is r q²/((1 − c) q² − 1) (→ r/(1 − c) as q → ∞).
4. Matter-era growth exponents, baryon fraction f: `exp_baryons` (clock smooth), `lam_root` and `pA_root` (T-A at c = 1,
   q → ∞), `exponent_order`: for 0 < f < 1, p_baryons < p_T-A < 1 = p_cold.

κ = ½ FITTED; footings never pooled; the cold component is cold dark energy, no particle; not theory closed. Adopts nothing.
-/

open Real

namespace GRW1

/-- the T-A clock coefficient rises with c -/
theorem ta_coeff_mono (q2 c1 c2 : ℝ) (hq : 0 ≤ q2) (h1 : 0 ≤ c1) (h12 : c1 ≤ c2) :
    1 - q2 / (1 + c1 * q2) ≤ 1 - q2 / (1 + c2 * q2) := by
  have hp1 : 0 < 1 + c1 * q2 := by positivity
  have hp2 : 0 < 1 + c2 * q2 := by nlinarith
  rw [sub_le_sub_iff_left, div_le_div_iff₀ hp2 hp1]
  nlinarith [mul_nonneg hq hq, mul_le_mul_of_nonneg_right h12 (mul_nonneg hq hq)]

/-- it never exceeds the cold value -/
theorem ta_coeff_le_cold (q2 c : ℝ) (hq : 0 ≤ q2) (hc : 0 ≤ c) : 1 - q2 / (1 + c * q2) ≤ 1 := by
  have : 0 ≤ q2 / (1 + c * q2) := div_nonneg hq (by positivity)
  linarith

/-- at c = 1 it is TPA1 4.4's ε = 1 self-growth 1/(1 + q²) -/
theorem ta_coeff_one (q2 : ℝ) (hq : 0 ≤ q2) : 1 - q2 / (1 + 1 * q2) = 1 / (1 + q2) := by
  have : (1 + q2) ≠ 0 := by positivity
  field_simp
  ring

/-- 0 ≤ c ≤ 1 for any external field x ≥ 0 and any angle -/
theorem cfac_unit (x m : ℝ) (hx : 0 ≤ x) (hm0 : 0 ≤ m) (hm1 : m ≤ 1) :
    0 ≤ (1 / (1 + x)) * (1 - x * m ^ 2 / (1 + x)) ∧ (1 / (1 + x)) * (1 - x * m ^ 2 / (1 + x)) ≤ 1 := by
  have hp : 0 < 1 + x := by linarith
  have hm2 : m ^ 2 ≤ 1 := by nlinarith
  have hq : x * m ^ 2 / (1 + x) ≤ 1 := by
    rw [div_le_one hp]; nlinarith
  have hq0 : 0 ≤ x * m ^ 2 / (1 + x) := by positivity
  have hi : 1 / (1 + x) ≤ 1 := by rw [div_le_one hp]; linarith
  have hi0 : 0 ≤ 1 / (1 + x) := by positivity
  constructor
  · exact mul_nonneg hi0 (by linarith)
  · calc (1 / (1 + x)) * (1 - x * m ^ 2 / (1 + x)) ≤ 1 * 1 := by
          apply mul_le_mul hi (by linarith) (by linarith) (by norm_num)
      _ = 1 := by norm_num

/-- the simple law's AQUAL response: 1 − c = μ_e (1 + L_e μ²) -/
theorem aqual_response (x m : ℝ) (hx : 0 ≤ x) :
    1 - (1 / (1 + x)) * (1 - x * m ^ 2 / (1 + x)) = (x / (1 + x)) * (1 + m ^ 2 / (1 + x)) := by
  have : (1 + x) ≠ 0 := by positivity
  field_simp
  ring

/-- the static equilibrium of T-A and its total source -/
theorem equilibrium_total (c q2 r : ℝ) (hc : 0 ≤ c) (hq : 0 ≤ q2) (h : 1 < (1 - c) * q2) :
    (r * (1 + c * q2) / ((1 - c) * q2 - 1)) * q2 / (1 + c * q2) = r + r * (1 + c * q2) / ((1 - c) * q2 - 1) ∧
    r + r * (1 + c * q2) / ((1 - c) * q2 - 1) = r * q2 / ((1 - c) * q2 - 1) := by
  obtain ⟨D, hDdef, hDpos⟩ : ∃ D : ℝ, D = (1 - c) * q2 - 1 ∧ 0 < D := ⟨_, rfl, by linarith⟩
  have hDne : D ≠ 0 := hDpos.ne'
  have hp : (1 + c * q2) ≠ 0 := by positivity
  rw [← hDdef]
  constructor
  · field_simp
    rw [hDdef]
    ring
  · field_simp
    rw [hDdef]
    ring

/-- baryons with the clock smooth: p² + p/2 = (3/2) f -/
theorem exp_baryons (f : ℝ) (_hf : 0 ≤ f) :
    ((-1 + Real.sqrt (1 + 24 * f)) / 4) ^ 2 + ((-1 + Real.sqrt (1 + 24 * f)) / 4) / 2 = 3 / 2 * f := by
  have hs : Real.sqrt (1 + 24 * f) ^ 2 = 1 + 24 * f := Real.sq_sqrt (by linarith)
  linear_combination (1 / 16) * hs

/-- T-A at c = 1: the growth-matrix eigenvalue λ² − f λ − f (1 − f) = 0 -/
theorem lam_root (f : ℝ) (hf0 : 0 ≤ f) (hf1 : f ≤ 1) :
    ((f + Real.sqrt (f ^ 2 + 4 * f * (1 - f))) / 2) ^ 2 - f * ((f + Real.sqrt (f ^ 2 + 4 * f * (1 - f))) / 2)
      - f * (1 - f) = 0 := by
  have hs : Real.sqrt (f ^ 2 + 4 * f * (1 - f)) ^ 2 = f ^ 2 + 4 * f * (1 - f) :=
    Real.sq_sqrt (by nlinarith)
  linear_combination (1 / 4) * hs

/-- the exponent of eigenvalue λ: p² + p/2 = (3/2) λ -/
theorem pA_root (l : ℝ) (hl : 0 ≤ l) :
    ((-1 / 2 + Real.sqrt (1 / 4 + 6 * l)) / 2) ^ 2 + ((-1 / 2 + Real.sqrt (1 / 4 + 6 * l)) / 2) / 2 = 3 / 2 * l := by
  have hs : Real.sqrt (1 / 4 + 6 * l) ^ 2 = 1 / 4 + 6 * l := Real.sq_sqrt (by linarith)
  linear_combination (1 / 4) * hs

/-- the exponent as a function of the source: g(s) = (−1/2 + √(1/4 + 6 s))/2 -/
noncomputable def g (s : ℝ) : ℝ := (-1 / 2 + Real.sqrt (1 / 4 + 6 * s)) / 2

theorem g_one : g 1 = 1 := by
  have : Real.sqrt (1 / 4 + 6 * 1) = 5 / 2 := by
    rw [show (1 / 4 + 6 * 1 : ℝ) = (5 / 2) ^ 2 by norm_num]
    exact Real.sqrt_sq (by norm_num)
  unfold g; rw [this]; norm_num

theorem g_strictMono (a b : ℝ) (ha : 0 ≤ a) (hab : a < b) : g a < g b := by
  unfold g
  have : Real.sqrt (1 / 4 + 6 * a) < Real.sqrt (1 / 4 + 6 * b) := Real.sqrt_lt_sqrt (by linarith) (by linarith)
  linarith

/-- the baryons-only exponent is g f -/
theorem baryons_is_g (f : ℝ) (hf : 0 ≤ f) : (-1 + Real.sqrt (1 + 24 * f)) / 4 = g f := by
  unfold g
  have : Real.sqrt (1 + 24 * f) = 2 * Real.sqrt (1 / 4 + 6 * f) := by
    rw [show (1 + 24 * f : ℝ) = 2 ^ 2 * (1 / 4 + 6 * f) by ring, Real.sqrt_mul (by norm_num), Real.sqrt_sq (by norm_num)]
  rw [this]; ring

/-- for 0 < f < 1: f < λ < 1, hence p_baryons < p_T-A < 1 (the cold exponent) -/
theorem exponent_order (f : ℝ) (hf0 : 0 < f) (hf1 : f < 1) :
    let l := (f + Real.sqrt (f ^ 2 + 4 * f * (1 - f))) / 2
    f < l ∧ l < 1 ∧ g f < g l ∧ g l < 1 := by
  intro l
  set s := Real.sqrt (f ^ 2 + 4 * f * (1 - f)) with hsdef
  have hs0 : 0 ≤ s := Real.sqrt_nonneg _
  have hs2 : s ^ 2 = f ^ 2 + 4 * f * (1 - f) := Real.sq_sqrt (by nlinarith)
  have h1 : f < s := by
    by_contra h; rw [not_lt] at h
    have : s ^ 2 ≤ f ^ 2 := by nlinarith
    nlinarith
  have h2 : s < 2 - f := by
    by_contra h; rw [not_lt] at h
    have : (2 - f) ^ 2 ≤ s ^ 2 := by nlinarith
    nlinarith
  have hfl : f < l := by simp only [l]; linarith
  have hl1 : l < 1 := by simp only [l]; linarith
  refine ⟨hfl, hl1, g_strictMono f l hf0.le hfl, ?_⟩
  rw [← g_one]; exact g_strictMono l 1 (by linarith) hl1

end GRW1

#print axioms GRW1.ta_coeff_mono
#print axioms GRW1.ta_coeff_le_cold
#print axioms GRW1.ta_coeff_one
#print axioms GRW1.cfac_unit
#print axioms GRW1.aqual_response
#print axioms GRW1.equilibrium_total
#print axioms GRW1.exp_baryons
#print axioms GRW1.lam_root
#print axioms GRW1.pA_root
#print axioms GRW1.g_one
#print axioms GRW1.g_strictMono
#print axioms GRW1.baryons_is_g
#print axioms GRW1.exponent_order
-- κ = ½ FITTED; not theory closed. Adopts nothing.
