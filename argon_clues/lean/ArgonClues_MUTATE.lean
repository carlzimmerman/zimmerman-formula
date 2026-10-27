import Mathlib
/-! MUTATION CONTROL: each theorem below is a plausible-looking FALSE statement from the audits.
Lean must REJECT this file (exit code != 0), which shows the certificate has teeth. -/
noncomputable section
namespace ArgonCluesMut
def gN (g a : ℝ) : ℝ := g ^ 2 / (g + a)
-- false: the wrong harmonic form 1/g_N - 1/g = 1/a0
theorem wrong_harmonic (g a : ℝ) (hg : 0 < g) (ha : 0 < a) : 1 / gN g a - 1 / g = 1 / a := by
  have h : g + a ≠ 0 := by positivity
  unfold gN; field_simp; ring
-- false: kappa fixed by scale: a0 Z = 2 c H instead of c H
theorem wrong_friedmann (c G ρ H a0 : ℝ) (hH : H ^ 2 = 8 * Real.pi * G * ρ / 3)
    (ha : a0 ^ 2 = c ^ 2 * G * ρ / 4) : a0 ^ 2 * (32 * Real.pi / 3) = 4 * c ^ 2 * H ^ 2 := by
  rw [ha, hH]; ring
-- false: free fraction of the cubic tether is 1/2
theorem wrong_free (u : ℝ) (hu : 0 < u) : 1 - (u ^ 3 / 3) / (u * u ^ 2) = 1 / 2 := by
  have : u ≠ 0 := ne_of_gt hu
  field_simp; ring
end ArgonCluesMut
