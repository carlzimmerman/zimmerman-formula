/-
EXT02 Lean checks (ours). Compiled against the repo's Mathlib pin (fable_independent_2026/lean_2026).
1. The pasted P2 axiom, as written, quantifies over all Lambda, a_0 and proves False.
2. The pasted P4 theorem statement is false: its hypotheses hold at Lambda = a_0 = 1, N = (0,5,10),
   while its conclusion fails. Its `sorry` is unprovable, not a gap.
3. Fairness: the algebra the pastes rely on is true. A working proof that
   (pi/a_0^2) Lambda = 32 pi^2 -> a_0 = sqrt(Lambda/(32 pi)), and that F1 <-> F3.
   These certify algebra only; the hypothesis is the open premise.
-/
import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Analysis.Real.Pi.Bounds

namespace EXT02

-- 1. the P2 axiom is inconsistent
section P2
variable (Lambda : ℝ) (a_0 : ℝ)
noncomputable def rindler_disk_area (a : ℝ) : ℝ := Real.pi / (a ^ 2)
noncomputable def cgb_norm : ℝ := 32 * (Real.pi ^ 2)
axiom topological_boundary_matching : rindler_disk_area a_0 * Lambda = cgb_norm
theorem p2_axiom_proves_false : False := by
  have h := topological_boundary_matching 0 1      -- Lambda = 0, a_0 = 1: 0 = 32 pi^2
  simp [rindler_disk_area, cgb_norm] at h
end P2

-- 2. the P4 statement is false
def boundary_anomaly_sum (N0 N_half N1 : ℤ) : ℤ := 7 * N0 - 28 * N_half + 86 * N1

theorem p4_statement_is_false :
    ¬ (∀ (Lambda a_0 : ℝ) (N0 N_half N1 : ℤ), 0 < Lambda → 0 < a_0 →
        boundary_anomaly_sum N0 N_half N1 = 720 →
        (a_0 ^ 2 * (Real.pi / a_0 ^ 2) * Lambda) * (boundary_anomaly_sum N0 N_half N1 : ℝ) / 720
          = Lambda / 32 * 32 * Real.pi →
        a_0 = Real.sqrt (Lambda / (32 * Real.pi))) := by
  intro h
  have hsum : boundary_anomaly_sum 0 5 10 = 720 := by decide
  have hpi := Real.pi_pos
  have hbal : ((1:ℝ) ^ 2 * (Real.pi / (1:ℝ) ^ 2) * 1) * (boundary_anomaly_sum 0 5 10 : ℝ) / 720
      = (1:ℝ) / 32 * 32 * Real.pi := by
    rw [hsum]; push_cast; ring
  have key := h 1 1 0 5 10 one_pos one_pos hsum hbal
  have hlt : Real.sqrt ((1:ℝ) / (32 * Real.pi)) < 1 := by
    rw [Real.sqrt_lt' one_pos]
    have : (3.14:ℝ) < Real.pi := Real.pi_gt_d2
    rw [div_lt_iff₀ (by positivity)]; nlinarith
  linarith

-- 3. the algebra itself is true (conditional on the premise h)
theorem algebra_only (Lambda a_0 : ℝ) (ha : 0 < a_0)
    (h : (Real.pi / a_0 ^ 2) * Lambda = 32 * Real.pi ^ 2) :
    a_0 = Real.sqrt (Lambda / (32 * Real.pi)) := by
  have hpi := Real.pi_pos
  have ha2 : a_0 ^ 2 ≠ 0 := by positivity
  have h' : Real.pi * Lambda = 32 * Real.pi ^ 2 * a_0 ^ 2 := by
    rw [div_mul_eq_mul_div, div_eq_iff ha2] at h; exact h
  have hsq : a_0 ^ 2 = Lambda / (32 * Real.pi) := by
    rw [eq_div_iff (by positivity)]
    have : Real.pi * (a_0 ^ 2 * (32 * Real.pi)) = Real.pi * Lambda := by linear_combination (-1:ℝ) * h'
    exact mul_left_cancel₀ hpi.ne' this
  rw [← hsq, Real.sqrt_sq ha.le]

theorem f1_iff_f3 (Lambda a_0 : ℝ) (hL : 0 < Lambda) (ha : 0 < a_0) :
    a_0 ^ 2 = Lambda / (32 * Real.pi) ↔ Lambda / (2 * a_0 ^ 2) = 16 * Real.pi := by
  have hpi := Real.pi_pos
  have h2 : (2 * a_0 ^ 2) ≠ 0 := by positivity
  rw [div_eq_iff h2, eq_div_iff (by positivity)]
  constructor
  · intro h; linear_combination (-1:ℝ) * h
  · intro h; linear_combination (-1:ℝ) * h

end EXT02

#print axioms EXT02.p2_axiom_proves_false
#print axioms EXT02.p4_statement_is_false
#print axioms EXT02.algebra_only
#print axioms EXT02.f1_iff_f3
