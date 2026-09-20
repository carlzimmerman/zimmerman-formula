import Mathlib
/-!
L295 -- the certified arithmetic of the framework's no-dark-matter CMB face
(real_research/clock_2026/L295_baryonic_cmb_face.py, 4/4, CLASS with Omega_m = Omega_baryons).
The committed frame: THE_ACTION's own sectors (khronon + MOND scalar) provably carry NO quadratic-order
cosmological gravitating component (L282 Lean cold-dust: c_s^2 = 0 exactly at J_Y = beta0; L287: exactly two
propagating DOF; L283: the khronon's FRW energy is the G_cosmo-renormalisation; L288: the roll dead in both well
shapes; L282 V1: khronon perturbations propagate near c).  The framework's cosmology is therefore the
baryonic-only one, and CLASS measures: peak3/peak2 = 1.192 (baryons-only) vs 0.992 (LCDM): a -20.3% departure
of the peak-ratio alone, and P(k) suppressed by 3-4 orders.  Certified here: the falsifier arithmetic
(departure of the baryonic ratio from the LCDM ratio; the zeros in the ratio claim -- no remainder).
-/
namespace L295

/-- the measured numbers: baryonic-only r32 = 1.192, LCDM r32 = 0.992 -/
noncomputable def r_b : ℝ := 1.192
noncomputable def r_L : ℝ := 0.992

/-- THE FALSIFIER NUMBER: the baryonic-only peak ratio departs from LCDM by (1.192-0.992)/0.992 = 25/124 ~ 20.2%
    -- the no-dark-matter face is excluded by the measured ~1%-peaks at ~20 sigma -/
theorem departure_arithmetic :
    (r_b - r_L) / r_L = (1.192 - 0.992) / 0.992 := by
  rfl

theorem departure_exact_value : ((1.192 : ℝ) - 0.992) / 0.992 = 25 / 124 := by
  norm_num

theorem departure_over_twenty_percent :
    (25 : ℝ) / 124 > 1 / 5 := by
  norm_num

theorem lcdm_ratio_not_one :
    (124 : ℝ) / 125 ≠ 1 := by
  norm_num

end L295