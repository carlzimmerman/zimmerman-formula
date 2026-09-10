import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum

/-! Exact inequalities for the derived power-law branches, not full gravity closure. -/
namespace TickingKGB

theorem halo_cones (w : ℝ) (hw : 0 < w) (h1 : w < 1) :
    0 < 3*w/(w+2) ∧ 3*w/(w+2) < 1 ∧
    0 < 3*w^2/(w+2) ∧ 3*w^2/(w+2) < 1 := by
  have hd : 0 < w+2 := by linarith
  refine ⟨div_pos (by linarith) hd, (div_lt_iff₀ hd).2 ?_,
    div_pos (mul_pos (by norm_num) (pow_pos hw _)) hd, (div_lt_iff₀ hd).2 ?_⟩
  · linarith
  · have h := mul_pos (show 0 < 1-w by linarith) (show 0 < 3*w+2 by linarith)
    nlinarith

theorem cosmological_cone (n : ℝ) (hn : 1 ≤ n) :
    0 < (16*n+7)/(3*(4*n+1)^2) ∧ (16*n+7)/(3*(4*n+1)^2) < 1 := by
  have hd : 0 < (3:ℝ)*(4*n+1)^2 :=
    mul_pos (by norm_num) (pow_pos (by linarith) _)
  constructor
  · exact div_pos (by linarith) hd
  · apply (div_lt_iff₀ hd).2
    nlinarith [sq_nonneg n]

theorem fixed_power_cannot_give_two_distinct_BTFR_masses
    (n w1 w2 K M1 M2 : ℝ) (hn : 0 < n) (hK : 0 < K)
    (h1 : 2*n*w1 = 1-w1) (h2 : 2*n*w2 = 1-w2)
    (hM1 : w1^2 = K*M1) (hM2 : w2^2 = K*M2) : M1 = M2 := by
  have hd : 2*n+1 ≠ 0 := ne_of_gt (by linarith)
  have he : (2*n+1)*w1 = (2*n+1)*w2 := by nlinarith
  have hw : w1 = w2 := mul_left_cancel₀ hd he
  apply mul_left_cancel₀ (ne_of_gt hK)
  nlinarith [hw]

#print axioms halo_cones
#print axioms cosmological_cone
#print axioms fixed_power_cannot_give_two_distinct_BTFR_masses
end TickingKGB
