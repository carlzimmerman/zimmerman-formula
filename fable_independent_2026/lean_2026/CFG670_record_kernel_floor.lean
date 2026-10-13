import Mathlib

/-!
# CFG670 addendum: the T3 kernel floor for the record's own nu_mono (deep regime)

CFG670 (dir CFG665_gw_messenger_lean, file CFG665_gw_messenger.lean) certified the floor (nu - 1) y >= min(sqrt y, 1)/(1 + sqrt 2)
for the "simple nu" 1/2 + sqrt(1/4 + 1/y) (MISLABELLED there as nuMono) and for P2 = sqrt(1 + 1/y). The record's nu_mono
(real_research/derivation_chain_2026/FP1_static_sector.py, L340) is nu = 1 + h(y)/y with h = y/(exp(sqrt y) - 1) up to its peak
(y ~ 2.54) and a monotone tabulated tail beyond. PREMISE (checked numerically, not certified): on 0 < y <= 1 the table equals that
formula (agreement 1e-15 at y = 0.1, 1).

CERTIFIED: `hrar_floor`: for 0 < s <= 1, s/(1 + sqrt 2) <= s^2/(exp s - 1); i.e. with y = s^2 <= 1,
(nu_mono - 1) y = h(y) >= sqrt y/(1 + sqrt 2) = min(sqrt y, 1)/(1 + sqrt 2). This is the only regime CFG670's T6 Milky Way bound
uses (shell 10-110 kpc with g <= a0, i.e. M_enc <= 6.7e10 Msun on canonical), so T6 holds for the record's nu_mono too.
`grad_floor_deep`: the physical gradient floor for any kernel obeying the floor on (0, 1].
kappa = 1/2 is FITTED; nothing here says the theory is closed.
-/

namespace CFG670

open Real

theorem exp_chord (s : ℝ) (h0 : 0 ≤ s) (h1 : s ≤ 1) : Real.exp s - 1 ≤ s * (Real.exp 1 - 1) := by
  have hc := convexOn_exp.2 (Set.mem_univ 0) (Set.mem_univ 1) (by linarith : (0:ℝ) ≤ 1 - s) h0 (by ring)
  simp only [smul_eq_mul, mul_zero, zero_add, mul_one, Real.exp_zero] at hc
  linarith

theorem hrar_floor (s : ℝ) (hs : 0 < s) (h1 : s ≤ 1) :
    s / (1 + Real.sqrt 2) ≤ s ^ 2 / (Real.exp s - 1) := by
  have he : 0 < Real.exp s - 1 := by linarith [Real.add_one_lt_exp (ne_of_gt hs)]
  have hch := exp_chord s hs.le h1
  have he1 := Real.exp_one_lt_d9
  have r2 : (1:ℝ) < Real.sqrt 2 := by
    rw [show (1:ℝ) = Real.sqrt 1 by simp]; exact Real.sqrt_lt_sqrt (by norm_num) (by norm_num)
  have hden : 0 < 1 + Real.sqrt 2 := by positivity
  rw [div_le_div_iff₀ hden he]
  -- s (e^s - 1) <= s * s (e - 1) <= s^2 (1 + sqrt 2)
  have : Real.exp s - 1 ≤ s * (1 + Real.sqrt 2) := by nlinarith
  nlinarith

/-- physical form, deep regime: if g_N/a0 = y in (0,1] and the kernel's phantom h(y) = (nu-1) y obeys h >= sqrt y/(1+sqrt2),
    then (nu - 1) g >= sqrt(a0 g)/(1 + sqrt 2). -/
theorem grad_floor_deep (h : ℝ → ℝ) (hfl : ∀ y, 0 < y → y ≤ 1 → Real.sqrt y / (1 + Real.sqrt 2) ≤ h y)
    (a0 g : ℝ) (ha : 0 < a0) (hg : 0 < g) (hdeep : g ≤ a0) :
    Real.sqrt (a0 * g) / (1 + Real.sqrt 2) ≤ a0 * h (g / a0) := by
  have hy : 0 < g / a0 := by positivity
  have hy1 : g / a0 ≤ 1 := by rw [div_le_one ha]; exact hdeep
  have := hfl (g / a0) hy hy1
  have hs : Real.sqrt (a0 * g) = a0 * Real.sqrt (g / a0) := by
    rw [show a0 * g = a0 ^ 2 * (g / a0) by field_simp, Real.sqrt_mul (by positivity), Real.sqrt_sq ha.le]
  rw [hs, mul_div_assoc]
  exact mul_le_mul_of_nonneg_left this ha.le

end CFG670

#print axioms CFG670.exp_chord
#print axioms CFG670.hrar_floor
#print axioms CFG670.grad_floor_deep
