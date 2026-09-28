import Mathlib
import Mathlib.Tactic

noncomputable section
open Real
open scoped Topology

example : (0 : ℝ) ≠ 0 := by norm_num

example : ({r : ℝ | r ≠ 0} ∈ 𝓝 (0 : ℝ)) := by
  exact isOpen_compl_singleton.mem_nhds (by norm_num)

#check isOpen_compl_singleton
#check IsOpen.mem_nhds
example : ({0}ᶜ : Set ℝ) ∈ 𝓝 (0 : ℝ) := by
  exact isOpen_compl_singleton.mem_nhds (by norm_num)

end
