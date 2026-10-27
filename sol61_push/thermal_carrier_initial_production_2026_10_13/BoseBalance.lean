import Mathlib
namespace BoseBalance
theorem statistical_difference (r p q : ℝ) :
 r*(1+p)*(1+q)-(1+r)*p*q=r*(1+p+q)-p*q := by ring
-- a=exp(E1/T), b=exp(E2/T), with parent energy E1+E2.
-- This is an algebraic identity, not a proof of a quantum kinetic approximation.
theorem thermal_balance (a b : ℝ) (ha : a-1 ≠ 0) (hb : b-1 ≠ 0)
 (hab : a*b-1 ≠ 0) :
 (1/(a*b-1))*(1+1/(a-1))*(1+1/(b-1)) =
 (1+1/(a*b-1))*(1/(a-1))*(1/(b-1)) := by
 field_simp
 <;> ring
end BoseBalance
#print axioms BoseBalance.statistical_difference
#print axioms BoseBalance.thermal_balance
