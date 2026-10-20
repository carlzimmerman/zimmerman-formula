module

public import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
meta import Mathlib.Tactic.FieldSimp
meta import Mathlib.Tactic.Ring.Basic
meta import Mathlib.Tactic.Linarith.Frontend
meta import Mathlib.Tactic.Positivity

public section

/-!
The operational coefficient bridge for the single-mediator convention.

The source-derived coefficient formulas are explicit inputs through the
definitions below. This file does not solve a microscopic field equation,
certify a quantum vacuum, or assert that a physical principle selects 1/4.
-/

namespace Why4.Amplitude

def ratio (epsilon C2 C3 : ℝ) : ℝ := epsilon * C3 ^ 2 / C2 ^ 3

def newton (q omega C2 : ℝ) : ℝ := q ^ 2 / (2 * omega * C2)

def mond (q C2 C3 : ℝ) : ℝ := 2 * q * C2 / (3 * C3)

def xi (epsilon q omega C2 C3 : ℝ) : ℝ :=
  mond q C2 C3 ^ 2 / (newton q omega C2 * epsilon)

theorem source_coefficient_bridge
    (epsilon q omega C2 C3 : ℝ)
    (he : 0 < epsilon) (hq : 0 < q) (ho : 0 < omega)
    (h2 : 0 < C2) (h3 : 0 < C3) :
    xi epsilon q omega C2 C3 = 8 * omega / (9 * ratio epsilon C2 C3) := by
  unfold xi mond newton ratio
  field_simp [ne_of_gt he, ne_of_gt hq, ne_of_gt ho, ne_of_gt h2, ne_of_gt h3]
  <;> ring1

theorem scalar_quarter_iff_amplitude (R : ℝ) (hR : 0 < R) :
    32 * Real.pi / (9 * R) = 1 / 4 ↔ R = 128 * Real.pi / 9 := by
  rw [div_eq_iff (by positivity : (9 : ℝ) * R ≠ 0)]
  constructor <;> intro h <;> linarith

theorem physical_quarter_iff
    (epsilon q C2 C3 : ℝ)
    (he : 0 < epsilon) (hq : 0 < q) (h2 : 0 < C2) (h3 : 0 < C3) :
    xi epsilon q (4 * Real.pi) C2 C3 = 1 / 4 ↔
      ratio epsilon C2 C3 = 128 * Real.pi / 9 := by
  rw [source_coefficient_bridge epsilon q (4 * Real.pi) C2 C3
    he hq (by positivity) h2 h3]
  have hR : 0 < ratio epsilon C2 C3 := by
    unfold ratio
    positivity
  convert scalar_quarter_iff_amplitude (ratio epsilon C2 C3) hR using 1 <;> ring1

theorem common_factor_cancels
    (epsilon C2 C3 Z : ℝ) (hZ : Z ≠ 0) (h2 : C2 ≠ 0) :
    ratio (Z * epsilon) (Z * C2) (Z * C3) = ratio epsilon C2 C3 := by
  unfold ratio
  field_simp [hZ, h2]
  <;> ring1

theorem paired_coefficients
    (A L y b f : ℝ) (hA : A ≠ 0) (hL : L ≠ 0)
    (hy : y ≠ 0) (hb : b ≠ 0) :
    ratio (A * L ^ 3 * f) ((3 / 2) * A * L * y ^ 2 * b) (A * y ^ 3)
      = 8 * f / (27 * b ^ 3) := by
  unfold ratio
  field_simp [hA, hL, hy, hb]
  <;> ring1

def reducedRatio (u : ℝ) : ℝ := 4 * (1 + 2 * u) / (27 * (1 - u))

theorem matching_fixes_free_u (u : ℝ) (hu : u < 1) :
    reducedRatio u = 128 * Real.pi / 9 ↔
      u = (96 * Real.pi - 1) / (96 * Real.pi + 2) := by
  have hd : 27 * (1 - u) ≠ 0 := by positivity
  have hp : 96 * Real.pi + 2 ≠ 0 := by positivity
  unfold reducedRatio
  rw [div_eq_iff hd]
  constructor
  · intro h
    apply (eq_div_iff hp).mpr
    nlinarith
  · intro h
    have h' := (eq_div_iff hp).mp h
    nlinarith

#print axioms source_coefficient_bridge
#print axioms physical_quarter_iff
#print axioms common_factor_cancels
#print axioms paired_coefficients
#print axioms matching_fixes_free_u

end Why4.Amplitude
