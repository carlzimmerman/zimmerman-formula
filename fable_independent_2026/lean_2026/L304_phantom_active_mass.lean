import Mathlib
/-!
L304 -- the phantom's active-mass face (real_research/clock_2026/L304_phantom_active_mass.py, 4/4).
The Poisson face: rho_act = (w-1) rho with w = (B + 4/3 u)/(B + 2/3 u): exactly
  w - 1 = (2/3) u / (B + (2/3) u)  (the outer suppression: -> 0 as u -> 0),
  w - 1 = 1 - B/(B + (2/3) u)      (the inner saturation: -> 1 as u -> infinity),
so rho_act > 0 with 0 < w - 1 < 1: the phantom's self-gravity is suppressed outward (M_act ~ sqrt r,
machine: r^0.58) and the active cusp sharpens to the g04a window at the inner corner (cluster -1.55).
-/
namespace L304

/-- the exact split: w - 1 = (2/3) u /(B + (2/3) u). -/
theorem w1_exact (B u : ℝ) (hd : B + (2 : ℝ) / 3 * u ≠ 0) :
  (B + (4 : ℝ) / 3 * u) / (B + (2 : ℝ) / 3 * u) - 1 = ((2 : ℝ) / 3 * u) / (B + (2 : ℝ) / 3 * u) := by
  have hden : B * 3 + u * 2 ≠ 0 := by
    intro hz
    apply hd
    nlinarith
  field_simp [hd, hden]
  nlinarith

/-- the suppression split: w - 1 = 1 - B/(B + (2/3) u). -/
theorem w1_split (B u : ℝ) (hd : B + (2 : ℝ) / 3 * u ≠ 0) :
  (B + (4 : ℝ) / 3 * u) / (B + (2 : ℝ) / 3 * u) - 1 = 1 - B / (B + (2 : ℝ) / 3 * u) := by
  have hden : B * 3 + u * 2 ≠ 0 := by
    intro hz
    apply hd
    nlinarith
  field_simp [hd, hden]
  nlinarith

/-- positivity and the upper bound: 0 < w - 1 < 1 for B > 0, u > 0. -/
theorem suppression_bounds (B u : ℝ) (hB : 0 < B) (hu : 0 < u) :
  0 < ((2 : ℝ) / 3 * u) / (B + (2 : ℝ) / 3 * u) ∧
    ((2 : ℝ) / 3 * u) / (B + (2 : ℝ) / 3 * u) < 1 := by
  have hd : 0 < B + (2 : ℝ) / 3 * u := by positivity
  constructor
  · exact div_pos (by positivity) hd
  · exact (div_lt_one hd).2 (by nlinarith [hB, hu])

/-- the active source: rho_act = (2-K)J (w-1) is (w-1) times the energy density, exactly. -/
theorem rho_act_form (K J B u : ℝ) (hd : B + (2 : ℝ) / 3 * u ≠ 0) :
  ((B + (4 : ℝ) / 3 * u) / (B + (2 : ℝ) / 3 * u) - 1) * ((2 - K) * J) =
    ((2 - K) * J) * (((2 : ℝ) / 3 * u) / (B + (2 : ℝ) / 3 * u)) := by
  rw [w1_exact B u hd]
  ring_nf

end L304