module

public import AmplitudeBridge
public import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic

public section

namespace Why4.Amplitude

theorem physical_quarter_iff
    (epsilon q C2 C3 : ℝ)
    (he : 0 < epsilon) (hq : 0 < q) (h2 : 0 < C2) (h3 : 0 < C3) :
    xi epsilon q (4 * Real.pi) C2 C3 = 1 / 4 ↔
      ratio epsilon C2 C3 = 128 * Real.pi / 9 :=
  area_quarter_iff Real.pi epsilon q C2 C3 Real.pi_pos he hq h2 h3

theorem actual_pi_matching (u : ℝ) (hu : u < 1) :
    reducedRatio u = 128 * Real.pi / 9 ↔
      u = (96 * Real.pi - 1) / (96 * Real.pi + 2) :=
  matching_fixes_free_u Real.pi u Real.pi_pos hu

#print axioms physical_quarter_iff
#print axioms actual_pi_matching

end Why4.Amplitude
