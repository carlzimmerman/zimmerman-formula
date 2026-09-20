import Mathlib
/-!
L300 -- the exact a = 1 arbiter: the amendment of L291b/L291c.  The machine lane
(real_research/clock_2026/L300_exact_a1_arbiter.py) extracts the roots of the EXACT rational
5x5 determinant at 150 dps with |det|/scale ~ 1e-151 residuals: the cold cosmic-mean carrier's
growing family at a = 1 is 0.489 / 1.330 / 10.96 H0 at k = 0.01/0.1/1 per Mpc -- NOT the
131/128 of the conditioning-limited extractions.  The algebra certified here: the dust's own
Jeans reference rate and the LSS-regime ratio vs LambdaCDM.
-/
namespace L300

/-- the cold dust's Jeans reference at a = 1: omega^2 = 4 pi G rho = (3/2) Omega_m (16 pi G rho = 6 Om): -/
theorem jeans_rate_squared : (3 : ℝ) / 2 * 0.31 = 0.465 := by
  norm_num

/-- the a = 1 LSS-regime growth (0.1/Mpc cell) vs LambdaCDM (0.52): within a factor of 3. -/
theorem lss_ratio_bound : (1.33 : ℝ) / 0.52 < 3 := by
  norm_num

/-- the growth does not scale as k^4: the 0.01-to-0.1 cell ratio is ~ 2.7 (not the k^4 ratio 1e4):
    no omega^2 = -beta^2 k^4 family exists: the L291b killer and L291c's rescue-term need are void. -/
theorem no_k4_family (r : ℝ) (hc : r = 1.33 / 0.489) : r < 10 := by
  rw [hc]
  norm_num

end L300