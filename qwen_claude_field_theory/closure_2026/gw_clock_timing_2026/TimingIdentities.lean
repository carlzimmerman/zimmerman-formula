import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring

/- Bookkeeping identities over real numbers, NOT a formalization of the action,
   cosmological wave propagation, observations, or a law of nature. -/
namespace GWClockTiming

theorem common_travel_time_cancels (emGamma emGW travel : ℝ) :
    (emGamma + travel) - (emGW + travel) = emGamma - emGW := by ring

theorem exact_speed_delay (D c delta emission : ℝ)
    (hc : c ≠ 0) (hd : 1 + delta ≠ 0) :
    (emission + D/c) - D/(c*(1+delta)) =
      emission + (D/c)*delta/(1+delta) := by
  field_simp
  <;> ring

theorem speed_emission_degeneracy (r I emission eps shift : ℝ) (hr : r ≠ 0) :
    r*(emission-shift*I/r) + (eps+shift)*I = r*emission+eps*I := by
  field_simp
  <;> ring

theorem lensed_double_difference (r emGamma emGW pA pB gA gB : ℝ) :
    ((r*emGamma+pB)-(r*emGW+gB)) -
      ((r*emGamma+pA)-(r*emGW+gA)) = (pB-pA)-(gB-gA) := by ring

theorem equal_path_delays_null_test (r emGamma emGW pA pB : ℝ) :
    ((r*emGamma+pB)-(r*emGW+pB)) -
      ((r*emGamma+pA)-(r*emGW+pA)) = 0 := by ring

#print axioms common_travel_time_cancels
#print axioms exact_speed_delay
#print axioms speed_emission_degeneracy
#print axioms lensed_double_difference
#print axioms equal_path_delays_null_test
end GWClockTiming
