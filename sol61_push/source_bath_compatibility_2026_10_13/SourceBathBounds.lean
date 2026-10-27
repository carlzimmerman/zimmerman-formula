import Mathlib
namespace SourceBathBounds
-- delta is the vacuum pair excess; u is the interior one-particle shift.
theorem pole_open (delta u : ℝ) : 0 < delta - 2*u ↔ u < delta/2 := by
 constructor <;> intro h <;> linarith
-- Products are born in the static bath, rather than carried into it at fixed K.
theorem confinement_margin (delta u wall : ℝ) :
 (wall-u) - (delta/2-u) = wall-delta/2 := by ring
theorem captured_energy_iff (delta u wall : ℝ) :
 delta/2-u < wall-u ↔ delta/2 < wall := by
 constructor <;> intro h <;> linarith
-- This certifies only the numerator/denominator inequality of the stipulated line.
theorem spectral_numerator_bound (r x : ℝ) :
 4*r ≤ 4*x^2 + (1+r)^2 := by nlinarith [sq_nonneg (r-1), sq_nonneg x]
end SourceBathBounds
#print axioms SourceBathBounds.pole_open
#print axioms SourceBathBounds.confinement_margin
#print axioms SourceBathBounds.captured_energy_iff
#print axioms SourceBathBounds.spectral_numerator_bound
