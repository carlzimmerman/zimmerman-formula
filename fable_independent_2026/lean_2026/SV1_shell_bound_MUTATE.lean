/- SV1 MUTATE twin: three false claims; each must fail to compile. kappa = 1/2 FITTED; not theory closed. -/
import Mathlib
namespace SV1M
open Finset
noncomputable def h (a g : ℝ) : ℝ := g ^ 2 / (a + g)
-- M1 false: the shell mean sits ABOVE the law (the hot-system sign)
theorem shell_above_law {ι : Type*} (s : Finset ι) (w g G : ι → ℝ) {a gN gl : ℝ} (ha : 0 < a)
    (hw : ∀ i ∈ s, 0 ≤ w i) (hsum : ∑ i ∈ s, w i = 1)
    (hg : ∀ i ∈ s, 0 ≤ g i) (hgG : ∀ i ∈ s, g i ≤ G i)
    (hgauss : ∑ i ∈ s, w i * (G i / (a + G i) * g i) = gN)
    (hgl : 0 < gl) (hlaw : gl ^ 2 = gN * (gl + a)) :
    gl ≤ ∑ i ∈ s, w i * g i := by
  nlinarith [hgl, hlaw]
-- M2 false: drop g <= G (a radial component larger than the magnitude)
theorem h_le_mu_mul_wrong {a g G : ℝ} (ha : 0 < a) (hg : 0 ≤ g) :
    h a g ≤ G / (a + G) * g := by
  unfold h
  have h1 : 0 < a + g := by linarith
  rw [div_mul_eq_mul_div]
  nlinarith
-- M3 false: concavity in place of convexity (tangent line above h)
theorem h_tangent_wrong {a m y : ℝ} (ha : 0 < a) (hm : 0 ≤ m) (hy : 0 ≤ y) :
    h a y ≤ h a m + m * (m + 2 * a) / (a + m) ^ 2 * (y - m) := by
  unfold h
  have h1 : 0 < a + m := by linarith
  have h2 : 0 < a + y := by linarith
  have key : y ^ 2 / (a + y) - (m ^ 2 / (a + m) + m * (m + 2 * a) / (a + m) ^ 2 * (y - m))
      = a ^ 2 * (y - m) ^ 2 / ((a + y) * (a + m) ^ 2) := by
    field_simp
    ring
  have : 0 ≤ a ^ 2 * (y - m) ^ 2 / ((a + y) * (a + m) ^ 2) := by positivity
  linarith
end SV1M
