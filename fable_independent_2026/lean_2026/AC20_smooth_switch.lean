/-
AC20 (action_search_2026_11_05/AC20_smooth_switch): algebraic cores of smoothing the v3s/AC2q stiffness switch.
Criteria: iter_2_contact/FROZEN_CRITERIA.md (L1-L5), iter_3_spline/FROZEN_CRITERIA.md (L6).
kappa = 1/2 FITTED; not theory closed.
-/
import Mathlib

namespace AC20

/-- L1: H = diag(g, Π) symmetrizes the stiff-branch matrix A = [[v, Π], [g, v]] (g = F''(Π)). -/
theorem L1_symmetrizer (v P g : ℝ) :
    !![g, 0; 0, P] * !![v, P; g, v] - Matrix.transpose !![v, P; g, v] * !![g, 0; 0, P] = 0 := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Matrix.mul_apply, Fin.sum_univ_two, Matrix.transpose_apply] <;> ring

/-- L2: force-continuity core: |max(c h, 0)^m| ≤ |c|^m |h|^m, so for m ≥ 2 the one-sided difference
quotients of max(c h, 0)^m at h = 0 vanish (the stiffness force F' ∝ max(Π,0)^(n-1) is C¹-flat at a
transverse zero when n ≥ 3). -/
theorem L2_bound (c h : ℝ) (m : ℕ) : |(max (c * h) 0) ^ m| ≤ |c| ^ m * |h| ^ m := by
  have hb : |max (c * h) 0| ≤ |c * h| := by
    rcases le_total (c * h) 0 with h1 | h1
    · rw [max_eq_right h1, abs_zero]; exact abs_nonneg _
    · rw [max_eq_left h1]
  rw [abs_pow, ← mul_pow, ← abs_mul]
  exact pow_le_pow_left₀ (abs_nonneg _) hb m

/-- L2 (m = 1, the v3s kink): right quotient c, left quotient 0. -/
theorem L2_m1_right (c h : ℝ) (hc : 0 < c) (hh : 0 < h) : max (c * h) 0 / h = c := by
  rw [max_eq_left (by positivity)]; field_simp

theorem L2_m1_left (c h : ℝ) (hc : 0 < c) (hh : h < 0) : max (c * h) 0 / h = 0 := by
  rw [max_eq_right (by nlinarith)]; simp

/-- L3: convexity numerator of the contact form F = (γ/2) Π⁴/(Π+a)², u = Π/a. -/
theorem L3_numerator (u : ℝ) :
    (4 * u ^ 3 + 6 * u ^ 2) * (u + 1) - 3 * u ^ 3 * (u + 2) = u ^ 2 * (u ^ 2 + 4 * u + 6) := by ring

theorem L3_nonneg (u : ℝ) : 0 ≤ u ^ 2 * (u ^ 2 + 4 * u + 6) := by
  have h : 0 < u ^ 2 + 4 * u + 6 := by nlinarith [sq_nonneg (u + 2)]
  exact mul_nonneg (sq_nonneg u) h.le

/-- L4: the contact form's force deviates from v3s's γΠ by at most γa. -/
theorem L4_identity (Q a : ℝ) :
    Q ^ 3 * (Q + 2 * a) = Q * (Q + a) ^ 3 - a * Q * (Q ^ 2 + 3 * a * Q + a ^ 2) := by ring

theorem L4_le (Q a : ℝ) (hQ : 0 ≤ Q) (ha : 0 ≤ a) :
    Q * (Q ^ 2 + 3 * a * Q + a ^ 2) ≤ (Q + a) ^ 3 := by
  nlinarith [mul_nonneg (mul_nonneg ha ha) hQ, pow_nonneg ha 3]

/-- L5: n = 3 kink growth: second difference of Burgers slopes, nonzero for t ≠ 0, d ≠ 0. -/
theorem L5_kink (d t : ℝ) (h1 : 1 + d * t ≠ 0) (h2 : 1 - d * t ≠ 0) :
    d / (1 + d * t) + (-d) / (1 - d * t) = -2 * d ^ 2 * t / (1 - d ^ 2 * t ^ 2) := by
  have h3 : 1 - d ^ 2 * t ^ 2 ≠ 0 := by
    have : 1 - d ^ 2 * t ^ 2 = (1 + d * t) * (1 - d * t) := by ring
    rw [this]; exact mul_ne_zero h1 h2
  field_simp
  ring

/-- L6: the m = 4 spline (iter_3) is convex on the smoothing zone: f''(q) = -q²(84q³ - 225q² + 200q - 60) ≥ 0
for q ∈ [0, 1], q = Π/b. -/
theorem L6_spline_convex (q : ℝ) (h0 : 0 ≤ q) (h1 : q ≤ 1) :
    0 ≤ -q ^ 2 * (84 * q ^ 3 - 225 * q ^ 2 + 200 * q - 60) := by
  have hp : 84 * q ^ 3 - 225 * q ^ 2 + 200 * q - 60 ≤ 0 := by
    nlinarith [mul_nonneg h0 (sub_nonneg.2 h1), sq_nonneg (q - 9 / 10), sq_nonneg (q - 5 / 6),
      mul_nonneg h0 (sq_nonneg (q - 9 / 10)), mul_nonneg (sub_nonneg.2 h1) (sq_nonneg (q - 9 / 10)),
      mul_nonneg (sub_nonneg.2 h1) (sq_nonneg (q - 5 / 6)), mul_nonneg h0 (sq_nonneg (q - 5 / 6))]
  nlinarith [sq_nonneg q]

end AC20

#print axioms AC20.L1_symmetrizer
#print axioms AC20.L2_bound
#print axioms AC20.L2_m1_right
#print axioms AC20.L2_m1_left
#print axioms AC20.L3_numerator
#print axioms AC20.L3_nonneg
#print axioms AC20.L4_identity
#print axioms AC20.L4_le
#print axioms AC20.L5_kink
#print axioms AC20.L6_spline_convex
