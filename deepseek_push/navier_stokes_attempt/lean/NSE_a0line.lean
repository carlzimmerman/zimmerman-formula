import Mathlib

/-!
# NSE a0-line certificates (SPEC_A_LEAN.md, file 1)

This file certifies the ALGEBRA of the a0-line's two faces: the universal cap
`√(x² + a·x) ≤ x + a/2` (`a0cap_sq`, `a0cap_bound`), the deep window bounds
(`deep_lo`, `deep_hi`), the statement-level identity (`a0line_exact`), the
Newtonian/drag face (`newtonian_face`, `face_1e16`) and the suppression
factors of the S-kernel window (`window_lower_cleared`, `window_ratio`,
`window_suppression`, `window_exit`).  All proofs are genuine Lean 4
(Mathlib 4.34.0-rc2), zero `sorry`.

PHYSICS SCOPE: the a0-line itself is a MEASURED empirical law.  Lean certifies
the mathematics of the law's consequences, not that nature obeys the law.
-/

noncomputable section

open Real

theorem a0cap_sq (x a : ℝ) : (x + a / 2) ^ 2 - (x ^ 2 + a * x) = a ^ 2 / 4 := by
  ring

theorem a0cap_bound (x a : ℝ) (hx : 0 ≤ x) (ha : 0 ≤ a) :
    Real.sqrt (x ^ 2 + a * x) ≤ x + a / 2 := by
  have hrad : 0 ≤ x ^ 2 + a * x := by nlinarith [sq_nonneg x, mul_nonneg ha hx]
  have hrel : (x + a / 2) ^ 2 = x ^ 2 + a * x + a ^ 2 / 4 := by
    ring
  have ha24 : 0 ≤ a ^ 2 / 4 := by positivity
  have hsq : (Real.sqrt (x ^ 2 + a * x)) ^ 2 ≤ (x + a / 2) ^ 2 := by
    rw [Real.sq_sqrt hrad, hrel]
    nlinarith [ha24]
  have hs0 : 0 ≤ Real.sqrt (x ^ 2 + a * x) := Real.sqrt_nonneg _
  have ht0 : 0 ≤ x + a / 2 := by positivity
  simpa [abs_of_nonneg hs0, abs_of_nonneg ht0] using sq_le_sq.mp hsq

theorem deep_lo (a x : ℝ) (hx : 0 ≤ x) (ha : 0 ≤ a) :
    Real.sqrt (a * x) ≤ Real.sqrt (x ^ 2 + a * x) := by
  have _ := hx
  have _ := ha
  exact Real.sqrt_le_sqrt (by nlinarith : a * x ≤ x ^ 2 + a * x)

theorem deep_hi (a x : ℝ) (ha : 0 < a) (hx : 0 ≤ x) :
    Real.sqrt (x ^ 2 + a * x) ≤ Real.sqrt (a * x) * (1 + x / (2 * a)) := by
  have hrad : 0 ≤ x ^ 2 + a * x := by nlinarith [sq_nonneg x, mul_nonneg (le_of_lt ha) hx]
  have hax : 0 ≤ a * x := mul_nonneg (le_of_lt ha) hx
  have hs : (Real.sqrt (x ^ 2 + a * x)) ^ 2 ≤ (Real.sqrt (a * x) * (1 + x / (2 * a))) ^ 2 := by
    rw [Real.sq_sqrt hrad]
    rw [mul_pow, Real.sq_sqrt hax]
    have hsq : a * x * (1 + x / (2 * a)) ^ 2 = x ^ 2 + a * x + x ^ 3 / (4 * a) := by
      field_simp [ha.ne']
      ring
    rw [hsq]
    have hx3 : 0 ≤ x ^ 3 / (4 * a) := by positivity
    nlinarith [hx3]
  have hs0 : 0 ≤ Real.sqrt (x ^ 2 + a * x) := Real.sqrt_nonneg _
  have ht0 : 0 ≤ Real.sqrt (a * x) * (1 + x / (2 * a)) := by positivity
  simpa [abs_of_nonneg hs0, abs_of_nonneg ht0] using sq_le_sq.mp hs

theorem a0line_exact (a x : ℝ) (h : 0 ≤ x ^ 2 + a * x) :
    (Real.sqrt (x ^ 2 + a * x)) ^ 2 = a * x + x ^ 2 := by
  rw [Real.sq_sqrt h]
  ring

theorem newtonian_face (a g : ℝ) (N : ℝ) (hN : 0 < N) (hg : 0 ≤ g) (hbound : N * a ≤ g) :
    Real.sqrt (g ^ 2 + a * g) ≤ g * (1 + 1 / (2 * N)) := by
  have ht0 : 0 ≤ g * (1 + 1 / (2 * N)) := by positivity
  by_cases hrad : 0 ≤ g ^ 2 + a * g
  · have hs : (Real.sqrt (g ^ 2 + a * g)) ^ 2 ≤ (g * (1 + 1 / (2 * N))) ^ 2 := by
      rw [Real.sq_sqrt hrad]
      rw [mul_pow]
      have hc : (1 + 1 / (2 * N)) ^ 2 = 1 + 1 / N + 1 / (4 * N ^ 2) := by
        field_simp [hN.ne']
        ring
      rw [hc]
      have h1 : a * g ≤ g ^ 2 / N := by
        have hlg : N * a * g ≤ g * g := mul_le_mul_of_nonneg_right hbound hg
        apply (le_div_iff₀ hN).2
        nlinarith [hlg]
      have h2 : 0 ≤ g ^ 2 / (4 * N ^ 2) := by positivity
      calc
        g ^ 2 + a * g ≤ g ^ 2 + g ^ 2 / N := by nlinarith [h1]
        _ ≤ g ^ 2 + g ^ 2 / N + g ^ 2 / (4 * N ^ 2) := by nlinarith [h2]
        _ = g ^ 2 * (1 + 1 / N + 1 / (4 * N ^ 2)) := by ring
    have hs0 : 0 ≤ Real.sqrt (g ^ 2 + a * g) := Real.sqrt_nonneg _
    exact (sq_le_sq₀ hs0 ht0).mp hs
  · have hlt : g ^ 2 + a * g < 0 := not_le.mp hrad
    have hz : Real.sqrt (g ^ 2 + a * g) = 0 := Real.sqrt_eq_zero_of_nonpos hlt.le
    rw [hz]
    exact ht0

theorem face_1e16 (a g : ℝ) (ha : 0 ≤ a) (hg : 0 ≤ g) (hbound : (10 : ℝ) ^ 16 * a ≤ g) :
    Real.sqrt (g ^ 2 + a * g) ≤ g * (1 + 1 / (2 * (10 : ℝ) ^ 16)) := by
  have _ := ha
  have hN : 0 < (10 : ℝ) ^ 16 := by positivity
  exact newtonian_face a g ((10 : ℝ) ^ 16) hN hg hbound

theorem window_lower_cleared (eta eta_c : ℝ) (h1 : 0 < eta_c) (h2 : eta_c * 3500 ≤ eta * 203) :
    (3500 / 203 : ℝ) ^ 2 ≤ (eta / eta_c) ^ 2 := by
  have hstep : (3500 / 203 : ℝ) ≤ eta / eta_c := by
    apply (div_le_div_iff₀ (by norm_num : (0 : ℝ) < 203) h1).2
    nlinarith [h2]
  have hpos1 : 0 ≤ (3500 / 203 : ℝ) := by norm_num
  have hpos2 : 0 ≤ eta / eta_c := by nlinarith [hstep, hpos1]
  exact sq_le_sq.mpr (by simpa [abs_of_nonneg hpos1, abs_of_nonneg hpos2] using hstep)

theorem window_ratio (eta eta_c : ℝ) (h1 : 0 < eta_c) (h2 : 7/2 ≤ eta)
    (h3 : eta_c ≤ 203/1000) :
    (3500 / 203) ^ 2 ≤ (eta / eta_c) ^ 2 := by
  have h2' : eta_c * 3500 ≤ eta * 203 := by
    nlinarith [h2, h3]
  exact window_lower_cleared eta eta_c h1 h2'

theorem window_suppression (w : ℝ) (hw : 255 ≤ w) : (1 + w)⁻¹ ≤ 1 / 256 := by
  have hpos : 0 < 1 + w := by nlinarith
  rw [show (1 / 256 : ℝ) = (256 : ℝ)⁻¹ by norm_num]
  exact (inv_le_inv₀ hpos (by norm_num : (0 : ℝ) < 256)).2 (by nlinarith [hw])

theorem window_exit (eta eta_c : ℝ) (h1 : 0 < eta_c) (h2 : 7/2 ≤ eta)
    (h3 : eta_c ≤ 203/1000) :
    (1 + (eta / eta_c) ^ 2)⁻¹ ≤ 1 / 256 := by
  have hratio : (3500 / 203 : ℝ) ^ 2 ≤ (eta / eta_c) ^ 2 := window_ratio eta eta_c h1 h2 h3
  have hnum : 255 ≤ (3500 / 203 : ℝ) ^ 2 := by norm_num
  have hw : 255 ≤ (eta / eta_c) ^ 2 := by nlinarith [hratio, hnum]
  exact window_suppression ((eta / eta_c) ^ 2) hw

end

#print axioms a0cap_sq
#print axioms a0cap_bound
#print axioms deep_lo
#print axioms deep_hi
#print axioms a0line_exact
#print axioms newtonian_face
#print axioms face_1e16
#print axioms window_lower_cleared
#print axioms window_ratio
#print axioms window_suppression
#print axioms window_exit