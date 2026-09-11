import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith

/- Algebra after the radial integration-by-parts identity. Lean does not
   formalize the integral, function domain or boundary terms here. G is the
   nonnegative gradient energy, D the added density energy, norm the positive
   weighted squared norm, mu the background gap (not its square root). -/
namespace ClockRadialSpectrum
noncomputable section

theorem rayleigh_lower_bound (G D norm mu : ℝ)
    (hg : 0 ≤ G) (hd : 0 ≤ D) (hn : 0 < norm) :
    mu ≤ (G+mu*norm+D)/norm := by
  rw [le_div_iff₀ hn]
  linarith

theorem no_zero_energy (G D norm mu : ℝ)
    (hg : 0 ≤ G) (hd : 0 ≤ D) (hn : 0 < norm) (hm : 0 < mu) :
    0 < G+mu*norm+D := by
  have hp := mul_pos hm hn
  linarith

#print axioms rayleigh_lower_bound
#print axioms no_zero_energy
end
end ClockRadialSpectrum
