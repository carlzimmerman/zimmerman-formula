import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.SpecialFunctions.Sqrt
import Mathlib.Tactic

/-! MUTATE twin of QX2_cluster_nogo.lean: three false claims that must FAIL to compile.
M1: the miss from a 0.30 excess exceeds 0.30 (false: s eats 0.054).
M2: the door fails even if the terms could move the mean by 0.2 each (false: 0.43 - 0.6 < 0.05).
M3: log(1 + ε) ≥ ε (false for ε > 0). -/

namespace QX2M

theorem M1 (L A B : ℝ) (hs : |L - A| ≤ 0.054) (hB : A + 0.30 ≤ B) : 0.30 < B - L := by
  have := (abs_le.mp hs).2
  linarith

theorem M2 (D t1 t2 t3 : ℝ) (hD : 0.43 ≤ D) (h1 : t1 ≤ 0.2) (h2 : t2 ≤ 0.2) (h3 : t3 ≤ 0.2) :
    0.05 < D - (t1 + t2 + t3) := by
  linarith

theorem M3 (ε : ℝ) (hε : 0 ≤ ε) : ε ≤ Real.log (1 + ε) := by
  have h := Real.log_le_sub_one_of_pos (by linarith : (0 : ℝ) < 1 + ε)
  linarith

end QX2M
