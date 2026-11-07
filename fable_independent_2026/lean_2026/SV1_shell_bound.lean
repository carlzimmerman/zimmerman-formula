/-
SV1 iter_1 (closure_2026_11_06/SV1_step_mechanism, criteria 74a07762ff): the shell bound T1.
On a sphere around ANY source (no symmetry assumed), with solid-angle weights w_i >= 0 summing to 1, radial field
components 0 <= g_i <= G_i (G_i = |grad Phi|) and AQUAL's Gauss law  sum_i w_i mu(G_i) g_i = g_N,
mu(G) = G/(a+G), the shell-mean radial field m = sum_i w_i g_i obeys h(m) <= g_N with h(g) = g^2/(a+g),
hence m <= the law-S root g_l (g_l^2 = g_N (g_l + a)). So the orientation-stacked lensing mass and the unweighted
spherical mass of a non-spherical source sit at or below the law. kappa = 1/2 FITTED; not theory closed.
-/
import Mathlib

namespace SV1

open Finset

/-- h(g) = g^2/(a+g) = mu(g) g. -/
noncomputable def h (a g : ℝ) : ℝ := g ^ 2 / (a + g)

/-- Tangent line of the convex h at m (slope m(m+2a)/(a+m)^2) lies below h. -/
theorem h_tangent {a m y : ℝ} (ha : 0 < a) (hm : 0 ≤ m) (hy : 0 ≤ y) :
    h a m + m * (m + 2 * a) / (a + m) ^ 2 * (y - m) ≤ h a y := by
  unfold h
  have h1 : 0 < a + m := by linarith
  have h2 : 0 < a + y := by linarith
  have key : y ^ 2 / (a + y) - (m ^ 2 / (a + m) + m * (m + 2 * a) / (a + m) ^ 2 * (y - m))
      = a ^ 2 * (y - m) ^ 2 / ((a + y) * (a + m) ^ 2) := by
    field_simp
    ring
  have : 0 ≤ a ^ 2 * (y - m) ^ 2 / ((a + y) * (a + m) ^ 2) := by positivity
  linarith

/-- A radial component below the full magnitude: h(g) <= mu(G) g. -/
theorem h_le_mu_mul {a g G : ℝ} (ha : 0 < a) (hg : 0 ≤ g) (hgG : g ≤ G) :
    h a g ≤ G / (a + G) * g := by
  unfold h
  have h1 : 0 < a + g := by linarith
  have h2 : 0 < a + G := by linarith
  rw [div_mul_eq_mul_div, div_le_div_iff₀ h1 h2]
  have : 0 ≤ g * a * (G - g) := by
    apply mul_nonneg (mul_nonneg hg ha.le); linarith
  nlinarith

/-- T1, step 1: h(shell mean) <= g_N. -/
theorem shell_h_le {ι : Type*} (s : Finset ι) (w g G : ι → ℝ) {a gN : ℝ} (ha : 0 < a)
    (hw : ∀ i ∈ s, 0 ≤ w i) (hsum : ∑ i ∈ s, w i = 1)
    (hg : ∀ i ∈ s, 0 ≤ g i) (hgG : ∀ i ∈ s, g i ≤ G i)
    (hgauss : ∑ i ∈ s, w i * (G i / (a + G i) * g i) = gN) :
    h a (∑ i ∈ s, w i * g i) ≤ gN := by
  set m := ∑ i ∈ s, w i * g i with hmdef
  have hm : 0 ≤ m := Finset.sum_nonneg (fun i hi => mul_nonneg (hw i hi) (hg i hi))
  set c := m * (m + 2 * a) / (a + m) ^ 2
  have e1 : ∑ i ∈ s, w i * (h a m + c * (g i - m)) = h a m := by
    have hpt : ∀ i, w i * (h a m + c * (g i - m)) = h a m * w i + c * (w i * g i) - (c * m) * w i := by
      intro i; ring
    rw [Finset.sum_congr rfl (fun i _ => hpt i), Finset.sum_sub_distrib, Finset.sum_add_distrib]
    simp only [← Finset.mul_sum]
    rw [hsum, ← hmdef]; ring
  have e2 : ∑ i ∈ s, w i * (h a m + c * (g i - m)) ≤ ∑ i ∈ s, w i * (G i / (a + G i) * g i) := by
    apply Finset.sum_le_sum; intro i hi
    apply mul_le_mul_of_nonneg_left _ (hw i hi)
    exact le_trans (h_tangent ha hm (hg i hi)) (h_le_mu_mul ha (hg i hi) (hgG i hi))
  linarith

/-- h is strictly increasing on [0, inf): used to pass from h(m) <= g_N to m <= g_l. -/
theorem h_strict_mono {a x y : ℝ} (ha : 0 < a) (hx : 0 ≤ x) (hxy : x < y) : h a x < h a y := by
  unfold h
  have h1 : 0 < a + x := by linarith
  have h2 : 0 < a + y := by linarith
  rw [div_lt_div_iff₀ h1 h2]
  have hy : 0 < y := by linarith
  have : 0 < a * (y ^ 2 - x ^ 2) + x * y * (y - x) := by
    have : 0 < y ^ 2 - x ^ 2 := by nlinarith
    have : 0 ≤ x * y * (y - x) := by
      apply mul_nonneg (mul_nonneg hx hy.le); linarith
    nlinarith
  nlinarith

/-- T1: the shell-mean radial field is at most the law-S root. -/
theorem shell_below_law {ι : Type*} (s : Finset ι) (w g G : ι → ℝ) {a gN gl : ℝ} (ha : 0 < a)
    (hw : ∀ i ∈ s, 0 ≤ w i) (hsum : ∑ i ∈ s, w i = 1)
    (hg : ∀ i ∈ s, 0 ≤ g i) (hgG : ∀ i ∈ s, g i ≤ G i)
    (hgauss : ∑ i ∈ s, w i * (G i / (a + G i) * g i) = gN)
    (hgl : 0 < gl) (hlaw : gl ^ 2 = gN * (gl + a)) :
    ∑ i ∈ s, w i * g i ≤ gl := by
  have hm : 0 ≤ ∑ i ∈ s, w i * g i := Finset.sum_nonneg (fun i hi => mul_nonneg (hw i hi) (hg i hi))
  have h1 := shell_h_le s w g G ha hw hsum hg hgG hgauss
  have hlg : h a gl = gN := by
    unfold h
    have : 0 < a + gl := by linarith
    rw [div_eq_iff this.ne']; rw [hlaw]; ring
  by_contra hc
  rw [not_le] at hc
  have := h_strict_mono ha hgl.le hc
  linarith

end SV1

#print axioms SV1.h_tangent
#print axioms SV1.h_le_mu_mul
#print axioms SV1.shell_h_le
#print axioms SV1.h_strict_mono
#print axioms SV1.shell_below_law
