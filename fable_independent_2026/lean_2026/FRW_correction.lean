/-
FRW_correction: finite algebraic leaves of the AC2q full-measure FRW reconciliation.
Lane: closure_2026_11_06/FRW_RECONCILIATION_CHAIN. Kappa = 1/2 FITTED; not theory closed.
These are algebraic leaves only. The calculus steps (first variation, ADM reduction,
Fourier averaging) are sympy-checked in that folder, not formalized here.
Standard axioms only; MUTATE twin FRW_correction_MUTATE.lean.
-/
import Mathlib

namespace FRWCorrection

/-- Eliminating the algebraic polarization mode: with c > 0 the P block
m p l/2 - c p^2/4 is bounded by m^2 l^2/(4c), attained at p = m l / c.
Here m = (1 - z) q (corrected) is the lapse/polarization mixing. -/
theorem p_block_bound (m l c p : ℝ) (hc : 0 < c) :
    m * p * l / 2 - c * p ^ 2 / 4 ≤ m ^ 2 * l ^ 2 / (4 * c) := by
  have h : 0 ≤ (c * p - m * l) ^ 2 / (4 * c) := by positivity
  have e : m ^ 2 * l ^ 2 / (4 * c) - (m * p * l / 2 - c * p ^ 2 / 4)
      = (c * p - m * l) ^ 2 / (4 * c) := by
    field_simp; ring
  linarith

theorem p_block_attained (m l c : ℝ) (hc : 0 < c) :
    m * (m * l / c) * l / 2 - c * (m * l / c) ^ 2 / 4 = m ^ 2 * l ^ 2 / (4 * c) := by
  field_simp; ring

/-- UV denominator identity: z + (1 - z)^2 = 1 - z + z^2. -/
theorem uv_denominator (z : ℝ) : z + (1 - z) ^ 2 = 1 - z + z ^ 2 := by ring

/-- Legacy minus corrected square is the polynomial z(3z - 2), not identically zero. -/
theorem legacy_discrepancy (z : ℝ) : (1 - 2 * z) ^ 2 - (1 - z) ^ 2 = z * (3 * z - 2) := by ring

/-- Explicit nonexceptional counterexample at the stress value z = 1/10: 0.64 vs 0.81. -/
theorem legacy_ne_corrected_stress :
    (1 - 2 * (1/10 : ℝ)) ^ 2 = 16/25 ∧ (1 - (1/10 : ℝ)) ^ 2 = 81/100 ∧
    (1 - 2 * (1/10 : ℝ)) ^ 2 ≠ (1 - (1/10 : ℝ)) ^ 2 := by
  refine ⟨by norm_num, by norm_num, by norm_num⟩

/-- The two squares agree only at z = 0 and z = 2/3. -/
theorem legacy_eq_iff (z : ℝ) : (1 - 2 * z) ^ 2 = (1 - z) ^ 2 ↔ z = 0 ∨ z = 2/3 := by
  constructor
  · intro h
    have : z * (3 * z - 2) = 0 := by nlinarith [legacy_discrepancy z]
    rcases mul_eq_zero.mp this with h0 | h1
    · exact Or.inl h0
    · right; linarith
  · rintro (h | h) <;> subst h <;> norm_num

/-- Native fixed-A auxiliary Hessian at the D = 0 point A0 = 1/r + gamma r:
H_rr = 1 + (A - 2 gamma r)^2/gamma - 2(A r - 1 - gamma r^2) = 1 + (1 - gamma r^2)^2/(gamma r^2). -/
theorem aux_hessian (γ r : ℝ) (hg : 0 < γ) (hr : 0 < r) :
    let A := 1 / r + γ * r
    1 + (A - 2 * γ * r) ^ 2 / γ - 2 * (A * r - 1 - γ * r ^ 2)
      = 1 + (1 - γ * r ^ 2) ^ 2 / (γ * r ^ 2) := by
  intro A
  simp only [A]
  field_simp
  ring

/-- Its inverse is the corrected FRW ultraviolet ratio z/(z + (1 - z)^2), z = gamma r^2. -/
theorem aux_uv_speed (γ r : ℝ) (hg : 0 < γ) (hr : 0 < r) :
    1 / (1 + (1 - γ * r ^ 2) ^ 2 / (γ * r ^ 2))
      = (γ * r ^ 2) / ((γ * r ^ 2) + (1 - γ * r ^ 2) ^ 2) := by
  have hz : 0 < γ * r ^ 2 := by positivity
  field_simp

/-- Frozen FRW dispersion with any mixing factor f >= 0 (corrected f = (1-z)^2, AC2 f = 1):
c^2 = E(1 + l x^2)/(E(1 + l x^2) + f x^2) lies in (0, 1]. -/
theorem phase_speed_bounds (E l f x : ℝ) (hE : 0 < E) (hl : 0 ≤ l) (hf : 0 ≤ f) :
    0 < E * (1 + l * x ^ 2) / (E * (1 + l * x ^ 2) + f * x ^ 2) ∧
    E * (1 + l * x ^ 2) / (E * (1 + l * x ^ 2) + f * x ^ 2) ≤ 1 := by
  have h1 : 0 < E * (1 + l * x ^ 2) := by positivity
  have h2 : 0 ≤ f * x ^ 2 := by positivity
  constructor
  · positivity
  · rw [div_le_one (by linarith)]; linarith

/-- Group speed does not exceed phase speed: c_ph^2 - c_g c_ph = E f x^2 / den^2 >= 0,
with c_g c_ph = (1/2x) d(w^2)/dx written out in closed form. -/
theorem group_le_phase (E l f x : ℝ) (hE : 0 < E) (hl : 0 ≤ l) (hf : 0 ≤ f) :
    let den := E * (1 + l * x ^ 2) + f * x ^ 2
    E * (1 + l * x ^ 2) / den
      - E * (E * l ^ 2 * x ^ 4 + 2 * E * l * x ^ 2 + E + f * l * x ^ 4) / den ^ 2
      = E * f * x ^ 2 / den ^ 2 ∧ 0 ≤ E * f * x ^ 2 / den ^ 2 := by
  intro den
  have hd : 0 < den := by
    have : 0 < E * (1 + l * x ^ 2) := by positivity
    have : 0 ≤ f * x ^ 2 := by positivity
    show 0 < E * (1 + l * x ^ 2) + f * x ^ 2; linarith
  refine ⟨?_, by positivity⟩
  field_simp
  ring

/-- Group speed is positive: the closed-form c_g c_ph numerator has nonnegative terms and E^2 > 0. -/
theorem group_pos (E l f x : ℝ) (hE : 0 < E) (hl : 0 ≤ l) (hf : 0 ≤ f) :
    0 < E * (E * l ^ 2 * x ^ 4 + 2 * E * l * x ^ 2 + E + f * l * x ^ 4)
          / (E * (1 + l * x ^ 2) + f * x ^ 2) ^ 2 := by
  have hd : 0 < E * (1 + l * x ^ 2) + f * x ^ 2 := by
    have : 0 < E * (1 + l * x ^ 2) := by positivity
    have : 0 ≤ f * x ^ 2 := by positivity
    linarith
  positivity

end FRWCorrection

#print axioms FRWCorrection.p_block_bound
#print axioms FRWCorrection.p_block_attained
#print axioms FRWCorrection.uv_denominator
#print axioms FRWCorrection.legacy_discrepancy
#print axioms FRWCorrection.legacy_ne_corrected_stress
#print axioms FRWCorrection.legacy_eq_iff
#print axioms FRWCorrection.aux_hessian
#print axioms FRWCorrection.aux_uv_speed
#print axioms FRWCorrection.phase_speed_bounds
#print axioms FRWCorrection.group_le_phase
#print axioms FRWCorrection.group_pos
