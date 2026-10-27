import Mathlib
namespace CoolingBottleneck

theorem bounded_by_radiative (a b : ℝ) (ha : 0 ≤ a) (hb : 0 < b) :
    a*b/(a+b) ≤ b := by
  apply (div_le_iff₀ (by positivity : 0 < a+b)).mpr
  nlinarith [sq_nonneg b]

theorem bounded_by_formation (a b : ℝ) (ha : 0 < a) (hb : 0 ≤ b) :
    a*b/(a+b) ≤ a := by
  apply (div_le_iff₀ (by positivity : 0 < a+b)).mpr
  nlinarith [sq_nonneg a]

theorem branching_factor (a b : ℝ) :
    a*b/(a+b) = a*(b/(a+b)) := by ring

end CoolingBottleneck
#print axioms CoolingBottleneck.bounded_by_radiative
#print axioms CoolingBottleneck.bounded_by_formation
#print axioms CoolingBottleneck.branching_factor
